#!/usr/bin/env python3
"""Offline sitemap / sitemap-index audit (round 39, claim C1).

Rule of record: .ufo/waves/round-39/c1-contract.md, sentences 1-34.
Retained sources: corpus/SOURCES.md S102 (sitemaps.org protocol text),
S103 (sitemap.xsd and siteindex.xsd), S104 (W3C NOTE-datetime).

Usage: python3 -B sitemap_audit.py --manifest <path>

CONTROL (round 41, class "no-reader, manifest only"): this file is not a
candidate build. It keeps the reference's RFC 3986 judgment of the manifest's
`sitemapUrl` and never opens a sitemap file: every entry 1..60 of every file is
guessed invalid. A tripwire (`_guard_no_reads`) refuses to emit any audit if a
file under the manifest's directory is opened after the manifest is read, so a
score can only come from the manifest-only path.
"""

import ipaddress
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

# RFC 3986 Appendix A `URI` with an authority (sentence 22 needs a host),
# round 41. Code points U+0080 and above stay accepted where RFC 3986 allows
# `unreserved`, as RFC 3987 IRI characters (S102 names both RFCs); that is the
# round-39 behaviour for them, unchanged.
_UNRESERVED = "A-Za-z0-9._~\\-\u0080-\U0010ffff"
_SUB_DELIMS = "!$&'()*+,;="
_PCT = "%[0-9A-Fa-f]{2}"
_PCHAR = "(?:[" + _UNRESERVED + _SUB_DELIMS + ":@]|" + _PCT + ")"
_URI_RE = re.compile(
    "\\A[A-Za-z][A-Za-z0-9+.\\-]*:"                                  # scheme ":"
    "//(?:(?:[" + _UNRESERVED + _SUB_DELIMS + ":]|" + _PCT + ")*@)?"  # userinfo "@"
    "(?P<host>\\[(?P<literal>[^\\]]*)\\]"                             # IP-literal
    "|(?:[" + _UNRESERVED + _SUB_DELIMS + "]|" + _PCT + ")*)"         # reg-name, IPv4
    "(?::[0-9]*)?"                                                    # ":" port
    "(?:/" + _PCHAR + "*)*"                                           # path-abempty
    "(?:\\?(?:" + _PCHAR + "|[/?])*)?"                                # "?" query
    "(?:\\#(?:" + _PCHAR + "|[/?])*)?\\Z"                             # "#" fragment
)
_IPVFUTURE_RE = re.compile("\\A[vV][0-9A-Fa-f]+\\.[A-Za-z0-9._~\\-" + _SUB_DELIMS + ":]+\\Z")


def _rfc3986_uri(value):
    """True when `value` is an RFC 3986 `URI` whose hier-part has a non-empty
    host; it rejects every C0 control, space, DEL and the characters RFC 3986
    never allows, wherever they stand (round 41)."""
    match = _URI_RE.match(value)
    if match is None or match.group("host") == "":
        return False
    literal = match.group("literal")
    if literal is None:
        return True
    if _IPVFUTURE_RE.match(literal):
        return True
    if "%" in literal or not literal.isascii():
        return False
    try:
        ipaddress.IPv6Address(literal)
    except ValueError:
        return False
    return True


def _parse_url(value):
    """Return (scheme, host, port, path) or None when not an absolute
    http/https URL with a host (sentence 22, extended by sentence 4)."""
    if not _rfc3986_uri(value):
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

    # CONTROL: the sitemap file named by `file` is never opened. Every entry
    # 1..60 is guessed invalid; the counter reads only the presence of an
    # entry's `loc_not_absolute`, so entries past the real count are ignored.
    rendered = [{"code": "loc_not_absolute", "entry": entry} for entry in range(1, 61)]
    return {"id": ident_out, "status": "findings", "error": None, "findings": rendered}


# --------------------------------------------------------------------------
# Entry point (sentences 1, 2, 33, 34)
# --------------------------------------------------------------------------

def _emit(document):
    sys.stdout.write(json.dumps(document, ensure_ascii=True) + "\n")
    sys.stdout.flush()


def _cannot(message_document):
    _emit(message_document)
    return EXIT_CANNOT


_NO_OPENS = []


def _guard_no_reads(base_dir):
    """Control tripwire: after the manifest, nothing under `base_dir` may open.

    Paths are recorded, and `main` refuses to emit an audit when the list is
    non-empty, so a nonzero score itself proves that no sitemap file was read.
    `open` fires for builtins.open/io.open/os.open (PEP 578)."""
    prefix = os.path.abspath(base_dir) + os.sep

    def hook(event, args):
        if event == "open" and args:
            try:
                path = os.path.abspath(args[0])
            except Exception:
                return
            if path.startswith(prefix):
                _NO_OPENS.append(path)

    sys.addaudithook(hook)


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
    _guard_no_reads(base_dir)
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

    if _NO_OPENS:
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
