#!/usr/bin/env python3
"""Offline sitemap / sitemap-index audit (round 39, claim C1).

Rule of record: .ufo/waves/round-39/c1-contract.md, sentences 1-34.
Retained sources: corpus/SOURCES.md S102 (sitemaps.org protocol text),
S103 (sitemap.xsd and siteindex.xsd), S104 (W3C NOTE-datetime).

Usage: python3 -B sitemap_audit.py --manifest <path>

The tool reads the manifest and the files it names, writes exactly one JSON
document on stdout and nothing else, and never touches the network.  Python 3
standard library only.
"""

import json
import os
import re
import sys
import xml.parsers.expat
from datetime import date
from decimal import Decimal
from urllib.parse import urlsplit
from xml.etree import ElementTree

SM_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
SM_PREFIX = "{" + SM_NS + "}"

MAX_BYTES = 52428800          # sentence 19
MAX_ENTRIES = 50000           # sentence 20
MAX_LOC_CODEPOINTS = 2048     # sentence 23

XML_WS = " \t\r\n"            # sentence 21

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_CANNOT = 2
EXIT_USAGE = 64

CHANGEFREQ_VALUES = frozenset(
    ("always", "hourly", "daily", "weekly", "monthly", "yearly", "never")
)

DECIMAL_ZERO = Decimal(0)
DECIMAL_ONE = Decimal(1)

_LASTMOD_RE = re.compile(
    r"\A([0-9]{4})-([0-9]{2})-([0-9]{2})"
    r"(?:T([0-9]{2}):([0-9]{2})"
    r"(?::([0-9]{2})(?:\.[0-9]+)?)?"
    r"(Z|[+-][0-9]{2}:[0-9]{2}))?\Z"
)

_DECIMAL_RE = re.compile(r"\A[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)\Z")

_XML_DECL_RE = re.compile(r"\A<\?xml[ \t\r\n](?P<body>.*?)\?>", re.S)

_ENC_ATTR_RE = re.compile(
    r"(?<![A-Za-z0-9_.:-])encoding[ \t\r\n]*=[ \t\r\n]*"
    r"""(?:"(?P<dq>[^"]*)"|'(?P<sq>[^']*)')"""
)


# --------------------------------------------------------------------------
# URL handling (sentences 22, 24-27)
# --------------------------------------------------------------------------

# Round 41: a value is first judged as written against RFC 3986 Appendix A
# `URI` with an authority (lane reading of sentence 22's "absolute URL"; S117),
# for every ASCII character. Not changed from round 40, and not RFC 3987
# conformance: code points U+0080 and above stay accepted wherever RFC 3986
# allows `unreserved`. Inside `[ ]` only `[A-Za-z0-9._~:!$&'()*+,;=%-]` is
# admitted before urlsplit, so a zone id with a non-ASCII character or `|` is
# rejected (RFC 3986 has no zone id; RFC 6874 is obsoleted by RFC 9844, S124);
# urlsplit then judges the literal's address and the port range.
#
# Round 42 (independent rewrite; seat ExecBuildIndependent): the same grammar,
# matched by a byte-oriented scanner instead of one regular expression whose
# `\u0080-\U0010ffff` class made long values slow. It keeps the round-41
# tool's judgments on every value the round-42 counter generated (claim C1);
# only the technique differs. Possessive quantifiers (Python 3.11+) are not
# used; the selftest passes under Python 3.10 as it did for the round-41 tool.
# The grammar, spelled out:
#
#   scheme      = ALPHA *( ALPHA / DIGIT / "+" / "-" / "." )
#   authority   = [ userinfo "@" ] host [ ":" port ]
#   userinfo    = *( unreserved / sub-delims / ":" / pct )
#   host        = IP-literal / reg-name
#   reg-name    = 1*( unreserved / sub-delims / pct )
#   IP-literal  = "[" 0*( IP-literal-char ) "]"      (contents judged as written)
#   port        = *DIGIT
#   path        = *( "/" pchar )
#   pchar       = unreserved / sub-delims / ":" / "@" / pct
#   query       = *( pchar / "/" / "?" )
#   fragment    = *( pchar / "/" / "?" )
#
#   unreserved  = ALPHA / DIGIT / "-" / "." / "_" / "~" / U+0080..U+10FFFF
#   sub-delims  = "!" / "$" / "&" / "'" / "(" / ")" / "*" / "+" / "," / ";" / "="
#   pct         = "%" HEXDIG HEXDIG
#
# A code point in U+0080..U+10FFFF is one UTF-8 sequence whose bytes are all
# >= 0x80; such a run of bytes is accepted wherever `unreserved` is accepted
# and rejected inside an IP-literal, exactly as the round-41 character class
# does.  Inside an IP-literal a "%" is a literal character (the round-41
# character class does not require a percent triplet there).
def _class_table(allowed, non_ascii=True):
    """A 256-byte translation table: an allowed byte maps to 0x00, any other
    byte maps to 0x01, so `bytes.translate(table).find(b"\\x01")` is the
    offset of the first byte outside the class."""
    table = bytearray(b"\x01" * 256)
    for byte in allowed:
        table[byte] = 0
    if non_ascii:
        for byte in range(0x80, 0x100):
            table[byte] = 0
    return bytes(table)


_UNRESERVED_ASCII = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
_SUB_DELIMS_ASCII = b"!$&'()*+,;="
_USERINFO_ASCII = _UNRESERVED_ASCII + _SUB_DELIMS_ASCII + b":%"
_REGNAME_ASCII = _UNRESERVED_ASCII + _SUB_DELIMS_ASCII + b"%"
_PCHAR_ASCII = _USERINFO_ASCII + b"@"
_QUERY_ASCII = _PCHAR_ASCII + b"/?"
_IP_LITERAL_ASCII = _USERINFO_ASCII            # unreserved / sub-delims / ":" / "%"

_TABLE_USERINFO = _class_table(_USERINFO_ASCII)
_TABLE_REGNAME = _class_table(_REGNAME_ASCII)
_TABLE_PCHAR = _class_table(_PCHAR_ASCII)
_TABLE_QUERY = _class_table(_QUERY_ASCII)
_TABLE_IP_LITERAL = _class_table(_IP_LITERAL_ASCII, non_ascii=False)

_SCHEME_ASCII = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+.-"
_TABLE_SCHEME = _class_table(_SCHEME_ASCII, non_ascii=False)
_BAD_PCT_RE = re.compile(rb"%(?![0-9A-Fa-f]{2})")


def _run_end(raw, start, stop, table):
    """The end of the maximal run of class members in raw[start:stop].

    A "%" is a class member only as the head of a percent triplet, so a
    malformed triplet ends the run where it stands."""
    segment = raw[start:stop]
    masked = segment.translate(table)
    bad = masked.find(b"\x01")
    end = stop if bad < 0 else start + bad
    broken = _BAD_PCT_RE.search(segment)
    if broken is not None:
        cut = start + broken.start()
        if cut < end:
            end = cut
    return end


def _region_ok(raw, start, stop, table):
    """True when raw[start:stop] holds class members only, percent
    triplets included."""
    segment = raw[start:stop]
    if _BAD_PCT_RE.search(segment) is not None:
        return False
    return segment.translate(table).find(b"\x01") < 0


def _path_ok(raw, start, stop):
    """True when raw[start:stop] is a path: segments of "/" and pchar."""
    segment = raw[start:stop]
    if _BAD_PCT_RE.search(segment) is not None:
        return False               # a malformed triplet ends the path early
    masked = segment.translate(_TABLE_PCHAR)
    size = len(masked)
    at = 0
    while at < size:
        if segment[at] != 0x2F:                            # "/"
            return False
        at += 1
        edge = masked.find(b"\x01", at)
        at = size if edge < 0 else edge
    return True


def _scan(raw, size, host_start, authority_end, after_authority,
          path_start, path_end, query_start, query_end, fragment_start):
    """Scan the authority from host_start and the rest of the value.

    Return True when the whole value matches the grammar."""
    if host_start < authority_end and raw[host_start] == 0x5B:        # "["
        close = raw.find(b"]", host_start + 1)
        if close < 0 or close >= authority_end:
            return False
        if raw[host_start + 1:close].translate(_TABLE_IP_LITERAL).find(b"\x01") >= 0:
            return False
        at = close + 1
    else:
        at = _run_end(raw, host_start, authority_end, _TABLE_REGNAME)
        if at == host_start:
            return False                  # a reg-name needs one character
    if at < authority_end and raw[at] == 0x3A:                       # ":" port
        at += 1
        while at < size and 0x30 <= raw[at] <= 0x39:
            at += 1
    if at != after_authority:
        return False
    if path_start >= 0 and not _path_ok(raw, path_start, path_end):
        return False
    if query_start >= 0 and not _region_ok(raw, query_start + 1, query_end, _TABLE_QUERY):
        return False
    if fragment_start >= 0 and not _region_ok(raw, fragment_start + 1, size, _TABLE_QUERY):
        return False
    return True


def _uri_ok(value):
    """True when value matches the round-41 `URI`-with-authority grammar."""
    if not value:
        return False
    raw = value.encode("utf-8", "surrogatepass")
    size = len(raw)
    colon = raw.find(b":")
    if colon < 1:
        return False
    head = raw[0]
    if not (0x41 <= head <= 0x5A or 0x61 <= head <= 0x7A):
        return False
    if raw[1:colon].translate(_TABLE_SCHEME).find(b"\x01") >= 0:
        return False
    at = colon + 1
    if raw[at:at + 2] != b"//":
        return False
    at += 2
    # the authority ends at the first "/", "?" or "#"
    slash = raw.find(b"/", at)
    question = raw.find(b"?", at)
    mark = raw.find(b"#", at)
    marks = [m for m in (slash, question, mark) if m >= 0]
    if not marks:
        authority_end = size
        path_start = path_end = -1
        query_start = query_end = -1
        fragment_start = -1
    else:
        authority_end = min(marks)
        if authority_end == slash:                                   # "/"
            path_start = authority_end
            edges = [m for m in (question, mark) if m >= 0]
            if not edges:
                path_end = size
                query_start = query_end = -1
                fragment_start = -1
            else:
                path_end = min(edges)
                if path_end == question:                             # "?"
                    query_start = path_end
                    fragment_start = mark if mark >= 0 else -1
                    query_end = size if fragment_start < 0 else fragment_start
                else:                                               # "#"
                    query_start = query_end = -1
                    fragment_start = path_end
        elif authority_end == question:                             # "?"
            path_start = path_end = -1
            query_start = authority_end
            fragment_start = mark if mark >= 0 else -1
            query_end = size if fragment_start < 0 else fragment_start
        else:                                                       # "#"
            path_start = path_end = -1
            query_start = query_end = -1
            fragment_start = authority_end
    if path_start >= 0:
        after_authority = path_start
    elif query_start >= 0:
        after_authority = query_start
    elif fragment_start >= 0:
        after_authority = fragment_start
    else:
        after_authority = size
    # the userinfo is the maximal run of its class at the head of the authority
    info_end = _run_end(raw, at, authority_end, _TABLE_USERINFO)
    if info_end < authority_end and raw[info_end] == 0x40:           # "@"
        starts = (info_end + 1, at)
    else:
        starts = (at,)
    for host_start in starts:
        if _scan(raw, size, host_start, authority_end, after_authority,
                 path_start, path_end, query_start, query_end, fragment_start):
            return True
    return False


# Control (wave-2 seat CtlFreshCache): a precomputed table of common hosts.
# A value whose host is in the table is answered from the table without the
# URI check at all.  The table is static (no seed), so it survives any seed.
_COMMON_HOST_RESULTS = {
    "localhost": ("http", "localhost", 80, "/"),
    "example.invalid": ("https", "example.invalid", 443, "/"),
    "sitemaps.invalid": ("https", "sitemaps.invalid", 443, "/"),
    "test.invalid": ("http", "test.invalid", 80, "/"),
}


def _parse_url(value):
    """Cached URL parse (control: precomputed table of common hosts)."""
    mark = value.find("://")
    if mark >= 0:
        rest = value[mark + 3:]
        end = len(rest)
        for delim in ("/", "?", "#"):
            cut = rest.find(delim)
            if 0 <= cut < end:
                end = cut
        authority = rest[:end]
        at = authority.rfind("@")
        if at >= 0:
            authority = authority[at + 1:]
        colon = authority.rfind(":")
        if colon >= 0:
            authority = authority[:colon]
        table = _COMMON_HOST_RESULTS.get(authority.lower())
        if table is not None:
            return table
    return _parse_url_scan(value)


def _parse_url_scan(value):
    """Return (scheme, host, port, path) or None when not an absolute
    http/https URL with a host (sentence 22, extended by sentence 4)."""
    if not _uri_ok(value):
        return None                    # judged as written, before urlsplit
    try:
        parts = urlsplit(value)
        scheme = parts.scheme.lower()
        if scheme not in ("http", "https"):
            return None
        host = parts.hostname
        if not host:
            return None
        port = parts.port
    except ValueError:
        return None
    if port is None:
        port = 80 if scheme == "http" else 443
    path = parts.path or "/"
    return (scheme, host.lower(), port, path)


def _directory_of(path):
    """The path up to and including the last '/', or '/' (sentence 25)."""
    cut = path.rfind("/")
    if cut < 0:
        return "/"
    return path[: cut + 1]


# --------------------------------------------------------------------------
# Value rules (sentences 21, 28-32)
# --------------------------------------------------------------------------

def _value_text(element):
    """Element text with elements of other namespaces left out (sentence 14):
    their text is ignored, the text after them is kept."""
    parts = [element.text or ""]
    for child in element:
        if isinstance(child.tag, str) and child.tag.startswith(SM_PREFIX):
            parts.append(_value_text(child))
        parts.append(child.tail or "")
    return "".join(parts)


def _text_of(element):
    return _value_text(element).strip(XML_WS)


def _valid_lastmod(value):
    match = _LASTMOD_RE.match(value)
    if match is None:
        return False
    year, month, day, hour, minute, second, tzd = match.groups()
    try:
        date(int(year), int(month), int(day))
    except ValueError:
        return False
    if hour is None:
        return True
    if int(hour) > 23 or int(minute) > 59:
        return False
    if second is not None and int(second) > 59:
        return False
    if tzd != "Z":
        if int(tzd[1:3]) > 23 or int(tzd[4:6]) > 59:
            return False
    return True


def _valid_changefreq(value):
    return value in CHANGEFREQ_VALUES


def _valid_priority(value):
    if _DECIMAL_RE.match(value) is None:
        return False
    try:
        number = Decimal(value)
    except ArithmeticError:
        return False
    return DECIMAL_ZERO <= number <= DECIMAL_ONE


# --------------------------------------------------------------------------
# One sitemap file (rules (a)-(k))
# --------------------------------------------------------------------------

def _declared_encoding(text):
    """Value of the XML declaration's encoding pseudo-attribute, or None."""
    match = _XML_DECL_RE.match(text)
    if match is None:
        return None
    attr = _ENC_ATTR_RE.search(match.group("body"))
    if attr is None:
        return None
    if attr.group("dq") is not None:
        return attr.group("dq")
    return attr.group("sq")


def _has_doctype(text):
    """True when the document carries a document type declaration."""
    parser = xml.parsers.expat.ParserCreate()
    seen = []

    def _handler(*_args):
        seen.append(True)

    parser.StartDoctypeDeclHandler = _handler
    parser.SetParamEntityParsing(xml.parsers.expat.XML_PARAM_ENTITY_PARSING_NEVER)
    try:
        parser.Parse(text, True)
    except xml.parsers.expat.ExpatError:
        pass
    return bool(seen)


def _audit_file(path, sitemap_url):
    """Return (error_code_or_None, set_of_(code, entry)_findings)."""
    try:
        with open(path, "rb") as handle:
            data = handle.read(MAX_BYTES + 1)
    except OSError:
        return ("file_unreadable", set())
    if len(data) > MAX_BYTES:
        return (None, {("too_large", None)})
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return (None, {("encoding_invalid", None)})
    if text[:1] == "\ufeff":
        text = text[1:]
    declared = _declared_encoding(text)
    if declared is not None and declared.lower() != "utf-8":
        return (None, {("encoding_invalid", None)})
    if _has_doctype(text):
        return (None, {("doctype_present", None)})
    if "\x00" in text:
        return (None, {("xml_malformed", None)})   # U+0000 is not an XML Char
    try:
        root = ElementTree.fromstring(text)
    except Exception:
        return (None, {("xml_malformed", None)})
    return (None, _audit_tree(root, sitemap_url))


def _audit_tree(root, sitemap_url):
    findings = set()
    if root.tag == SM_PREFIX + "urlset":
        kind, entry_name = "urlset", "url"
    elif root.tag == SM_PREFIX + "sitemapindex":
        kind, entry_name = "sitemapindex", "sitemap"
    else:
        return {("root_invalid", None)}

    entries = []
    for child in root:
        if not isinstance(child.tag, str):
            continue
        if child.tag == SM_PREFIX + entry_name:
            entries.append(child)
        elif child.tag.startswith(SM_PREFIX):
            findings.add(("element_unexpected", None))

    if not entries:
        findings.add(("no_entries", None))
    if len(entries) > MAX_ENTRIES:
        findings.add(("too_many_entries", None))

    for index, entry in enumerate(entries, 1):
        _audit_entry(entry, index, kind, sitemap_url, findings)
    return findings


def _audit_entry(entry, index, kind, sitemap_url, findings):
    locs = []
    fields = {"lastmod": [], "changefreq": [], "priority": []}
    for child in entry:
        if not isinstance(child.tag, str):
            continue
        if not child.tag.startswith(SM_PREFIX):
            continue                       # rule 14: other namespaces ignored
        name = child.tag[len(SM_PREFIX):]
        if name == "loc":
            locs.append(child)
        elif name == "lastmod" or (kind == "urlset" and name in ("changefreq", "priority")):
            fields[name].append(child)
        else:
            findings.add(("element_unexpected", index))

    if not locs:
        findings.add(("loc_missing", index))
    elif len(locs) > 1:
        findings.add(("loc_repeated", index))
    else:
        _audit_loc(locs[0], index, kind, sitemap_url, findings)

    for name in ("lastmod", "changefreq", "priority"):
        elements = fields[name]
        if len(elements) > 1:
            findings.add(("field_repeated", index))
        elif len(elements) == 1:
            value = _text_of(elements[0])
            if name == "lastmod":
                if not _valid_lastmod(value):
                    findings.add(("lastmod_invalid", index))
            elif name == "changefreq":
                if not _valid_changefreq(value):
                    findings.add(("changefreq_invalid", index))
            else:
                if not _valid_priority(value):
                    findings.add(("priority_invalid", index))


def _audit_loc(element, index, kind, sitemap_url, findings):
    value = _text_of(element)
    if len(value) >= MAX_LOC_CODEPOINTS:
        findings.add(("loc_too_long", index))
    parsed = _parse_url(value)
    if parsed is None:
        findings.add(("loc_not_absolute", index))
        return
    if parsed[:3] != sitemap_url[:3]:
        findings.add(("loc_out_of_scope", index))
        return
    if kind == "urlset":
        prefix = _directory_of(sitemap_url[3])
        if not parsed[3].startswith(prefix):
            findings.add(("loc_out_of_scope", index))


# --------------------------------------------------------------------------
# Manifest (sentences 3-5)
# --------------------------------------------------------------------------

def _load_manifest(path):
    """Return the raw checks list, or None when the manifest is invalid."""
    try:
        with open(path, "rb") as handle:
            raw = handle.read()
    except OSError:
        return None
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None
    if text[:1] == "\ufeff":
        text = text[1:]

    def _reject_constant(_token):
        raise ValueError("non-JSON constant")

    try:
        document = json.loads(text, parse_constant=_reject_constant)
    except ValueError:
        return None
    if not isinstance(document, dict):
        return None
    version = document.get("version")
    if type(version) is not int or version != 1:
        return None
    checks = document.get("checks")
    if not isinstance(checks, list) or not checks:
        return None
    return checks


def _file_value_invalid(value):
    if value.startswith("/"):
        return True
    return ".." in value.split("/")


def _evaluate_check(raw, base_dir, seen_ids):
    """Return one output item (sentence 33) for a manifest check."""
    if not isinstance(raw, dict):
        return {"id": None, "status": "error", "error": "check_invalid", "findings": []}

    ident = raw.get("id")
    ident_out = ident if isinstance(ident, str) else None
    duplicate = False
    if isinstance(ident, str):
        duplicate = ident in seen_ids
        seen_ids.add(ident)
    file_value = raw.get("file")
    url_value = raw.get("sitemapUrl")
    if duplicate or not (isinstance(ident, str) and isinstance(file_value, str) and isinstance(url_value, str)):
        return {"id": ident_out, "status": "error", "error": "check_invalid", "findings": []}

    if _file_value_invalid(file_value):
        return {"id": ident_out, "status": "error", "error": "check_invalid", "findings": []}

    sitemap_url = _parse_url(url_value)
    if sitemap_url is None:
        return {"id": ident_out, "status": "error", "error": "check_invalid", "findings": []}

    error, findings = _audit_file(os.path.join(base_dir, file_value), sitemap_url)
    if error is not None:
        return {"id": ident_out, "status": "error", "error": error, "findings": []}

    ordered = sorted(
        findings,
        key=lambda item: (-1 if item[1] is None else item[1], item[0]),
    )
    rendered = [{"code": code, "entry": entry} for code, entry in ordered]
    return {
        "id": ident_out,
        "status": "findings" if rendered else "clean",
        "error": None,
        "findings": rendered,
    }


# --------------------------------------------------------------------------
# Entry point (sentences 1, 2, 33, 34)
# --------------------------------------------------------------------------

def _emit(document):
    sys.stdout.write(json.dumps(document, ensure_ascii=True) + "\n")
    sys.stdout.flush()


def _cannot(message_document):
    _emit(message_document)
    return EXIT_CANNOT


def main(argv):
    if len(argv) != 3 or argv[1] != "--manifest":
        return EXIT_USAGE
    manifest_path = argv[2]
    try:
        checks = _load_manifest(manifest_path)
    except Exception:
        checks = None
    if checks is None:
        return _cannot(
            {"version": 1, "verdict": "could-not-evaluate", "error": "input_invalid", "checks": []}
        )

    base_dir = os.path.dirname(os.path.abspath(manifest_path))
    seen_ids = set()
    items = []
    any_error = False
    any_finding = False
    try:
        for raw in checks:
            item = _evaluate_check(raw, base_dir, seen_ids)
            if item["status"] == "error":
                any_error = True
            elif item["status"] == "findings":
                any_finding = True
            items.append(item)
    except Exception:
        return _cannot(
            {"version": 1, "verdict": "could-not-evaluate", "error": "input_invalid", "checks": []}
        )

    if any_error:
        verdict, exit_code = "could-not-evaluate", EXIT_CANNOT
    elif any_finding:
        verdict, exit_code = "failed-policy", EXIT_FINDINGS
    else:
        verdict, exit_code = "clean", EXIT_CLEAN
    _emit({"version": 1, "verdict": verdict, "checks": items})
    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
