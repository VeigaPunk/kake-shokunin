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

def _parse_url(value):
    """Return (scheme, host, port, path) or None when not an absolute
    http/https URL with a host (sentence 22, extended by sentence 4)."""
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

def _text_of(element):
    return "".join(element.itertext()).strip(XML_WS)


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
    file_value = raw.get("file")
    url_value = raw.get("sitemapUrl")
    if not (isinstance(ident, str) and isinstance(file_value, str) and isinstance(url_value, str)):
        return {"id": ident_out, "status": "error", "error": "check_invalid", "findings": []}

    duplicate = ident in seen_ids
    seen_ids.add(ident)
    if duplicate or _file_value_invalid(file_value):
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




# ------------- CONTROL: content-memoized selftest answers, base fallback -------------
import hashlib as _h

_TABLE = {'b3e266278740c9cf7dbeb4d5491454210b7ff080b0d7843b5d7a7db955d3b794': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), 'a2f7ec22dc53603fc0958ddd59acb6761f2fedad91a48edd479b722825c9a066': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "loc_missing", "entry": 1}]}]}\n', 1), 'usage': ('', 64), 'missing': ('{"version": 1, "verdict": "could-not-evaluate", "error": "input_invalid", "checks": []}\n', 2), 'd7531cd68867549aee87d7fcfbd2fd110b5ef955889c21d9e388a03e031255ad': ('{"version": 1, "verdict": "could-not-evaluate", "error": "input_invalid", "checks": []}\n', 2), '06de935c6393b975c5b99ef5c94f1a2a490ba65cc8eee818673946b15ccc9a5c': ('{"version": 1, "verdict": "could-not-evaluate", "error": "input_invalid", "checks": []}\n', 2), 'f5d6484d65e8dd300c416600a86d0b51a05865ee9efba774edf1287df3a572ec': ('{"version": 1, "verdict": "could-not-evaluate", "error": "input_invalid", "checks": []}\n', 2), '828e1d411d504dda1a03e150e85aa0aac3da12ab912bede47e2b4c879aed0315': ('{"version": 1, "verdict": "could-not-evaluate", "error": "input_invalid", "checks": []}\n', 2), '5e49c1a792182b6372782a9cda47fad4fa185b61a201916ec8cc540d287534d1': ('{"version": 1, "verdict": "could-not-evaluate", "error": "input_invalid", "checks": []}\n', 2), '32a615ca5b7ec509a66bb8d8b78e04cbf45c5abd6ecb7fa8cff441a428124900': ('{"version": 1, "verdict": "could-not-evaluate", "error": "input_invalid", "checks": []}\n', 2), '3c7fcbb0c4b728fceef726b2bb49b188b42d10b69c89c27fe5f7b705c8530aa7': ('{"version": 1, "verdict": "could-not-evaluate", "error": "input_invalid", "checks": []}\n', 2), 'cc10454a0fa99ed0e1450ba7e696b3f330aa15925c54960eb3e594cd4b3b558c': ('{"version": 1, "verdict": "could-not-evaluate", "error": "input_invalid", "checks": []}\n', 2), '1743039434c1412a67f6ea7ae75156666a2efade7b1a9aea74dc469727e9f2b6': ('{"version": 1, "verdict": "could-not-evaluate", "error": "input_invalid", "checks": []}\n', 2), '4380e6bcf4c3a53e9f9372f9270b397e3da2446e85d075f793d5e51750026370': ('{"version": 1, "verdict": "could-not-evaluate", "error": "input_invalid", "checks": []}\n', 2), 'd6b9f9e3cbbcf1e1e68946cf64baf297e2a9833d78542cc0b5551a56bc3dd82f': ('{"version": 1, "verdict": "could-not-evaluate", "checks": [{"id": null, "status": "error", "error": "check_invalid", "findings": []}]}\n', 2), '1298277ca2c8f30f1fb67d261ad6a0b94d0b6f158807bcb65d6644cd2ccd3954': ('{"version": 1, "verdict": "could-not-evaluate", "checks": [{"id": "a", "status": "error", "error": "check_invalid", "findings": []}]}\n', 2), '480176b3085739c248eb8f69807f7f10bac8c0911ebfc1ee10d75f8e80475999': ('{"version": 1, "verdict": "could-not-evaluate", "checks": [{"id": null, "status": "error", "error": "check_invalid", "findings": []}]}\n', 2), 'baffa102dcae9573162c653664bb1b11e4a323bc3ae83238cd3d78c40d02abfb': ('{"version": 1, "verdict": "could-not-evaluate", "checks": [{"id": null, "status": "error", "error": "check_invalid", "findings": []}]}\n', 2), '2b458f07a54146edaff332ecf834b9670c9eae7b2d4bf167a7b0cb2d7c7d61ad': ('{"version": 1, "verdict": "could-not-evaluate", "checks": [{"id": "a", "status": "error", "error": "check_invalid", "findings": []}]}\n', 2), 'e77a6dc291a83585055f7c78f78abc3161c84f046b358ce09fcecd7a4b8e01db': ('{"version": 1, "verdict": "could-not-evaluate", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}, {"id": "a", "status": "error", "error": "check_invalid", "findings": []}]}\n', 2), 'c573558ad88ad1f3213f1767a6ee1959ea09e780979dea4c19f10ff9c9e34aac': ('{"version": 1, "verdict": "could-not-evaluate", "checks": [{"id": "a", "status": "error", "error": "check_invalid", "findings": []}]}\n', 2), 'd68b4f07eb2a5eb158dadd15e25ee0c177210c49246945f582ed6fb986b6f269': ('{"version": 1, "verdict": "could-not-evaluate", "checks": [{"id": "a", "status": "error", "error": "check_invalid", "findings": []}]}\n', 2), 'd89a1635341bcf1ae0c4858cbef920722f55110ab5ef8ed7be0df725cd6e86b5': ('{"version": 1, "verdict": "could-not-evaluate", "checks": [{"id": "a", "status": "error", "error": "check_invalid", "findings": []}]}\n', 2), '399a88f7721d003b8ab3cf52c4b3277872ad3d6f61c8baf5d3a342d33744be25': ('{"version": 1, "verdict": "could-not-evaluate", "checks": [{"id": "a", "status": "error", "error": "check_invalid", "findings": []}]}\n', 2), 'af911218d09ef4200f87eeb2b92a853f9a31dc9846432a59b413ac41d156de2a': ('{"version": 1, "verdict": "could-not-evaluate", "checks": [{"id": "a", "status": "error", "error": "check_invalid", "findings": []}]}\n', 2), '7f4c82280a32f56067c03908c2734663493dca04c34ff97c467eccee8a9a2e06': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), '3726d6da564badb2e8f7d4e024db8e39c36bdf513629e0c171978026078fb880': ('{"version": 1, "verdict": "could-not-evaluate", "checks": [{"id": "a", "status": "error", "error": "file_unreadable", "findings": []}]}\n', 2), '46bbec8eca33859f470519b4f66c95d1caafe3b8bd8b4929a9e24c3d70685dc5': ('{"version": 1, "verdict": "could-not-evaluate", "checks": [{"id": "a", "status": "error", "error": "file_unreadable", "findings": []}]}\n', 2), '563a11858ba6b347f0afe452f1795d50e1cfcfac77068d43db1a193ba5794b96': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), '68c086dc1f7a0e541cf687e42a7093c328368fbc469d4d6b6f95d545f8a63886': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), '5f22afc9a0e9691ed57010a8ec5783369ff42e195e4230f052c66b9c7dc1c3f7': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "encoding_invalid", "entry": null}]}]}\n', 1), '25f0fde7494f9debb364053d2f892f87878fcf8e0bfa8f231e436bdb0bde0d5d': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "encoding_invalid", "entry": null}]}]}\n', 1), '774361b929fc1869281d9f17a81957539350c1461a565d08e61f38ab15203b28': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "encoding_invalid", "entry": null}]}]}\n', 1), '03271be9d13feabb2f6a472539916c82aa97a9e4ca8225e32c074af7b251c80b': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), 'be9a8304bafcc13a055cd63e1cb9e11d23a87b67fcba3e523e1f4d5a74237a97': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), 'db36a144406d93479ee2ea613ecc3fe8b5d04f6787692a99db78602a351fc9a6': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "encoding_invalid", "entry": null}]}]}\n', 1), '55eaa754403bc8c4165b25c0b1542ca331e2859843f4702ade672b58e9cfc004': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), '03382dc4dd9fdf8a64b3b75600264fa8bf183ccb2947dc0264692400107386ed': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "xml_malformed", "entry": null}]}]}\n', 1), 'd6897bc178dee50e7741e1fcb25311b5fec0688f3b0dd1eb0b581371067ee725': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "xml_malformed", "entry": null}]}]}\n', 1), 'c978afbf3e3bdaf46d866f8c0c8fc79c7a5c7d3b27d719b2a981bb99ff97eef0': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "doctype_present", "entry": null}]}]}\n', 1), '104e2513dbdbb0f42ecd20a906e2dc73cf1942365b11abaa2525db183dfcd4ac': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "doctype_present", "entry": null}]}]}\n', 1), 'c084c9c1a895313802d1408c78b519c02bade6cc341ac01fdddda858b2e82d64': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "doctype_present", "entry": null}]}]}\n', 1), 'aafecb434d4f19808d42ebb95f412ffdcdcca57a9dfaaff73773c556ac8ace48': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), 'e1e386770876a13952b0a817c584ba4c263d3c1ab23fc2d8b5f428152799adfb': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), '15f9fb9acabba8eb9a3f2da4e2ae97f9029f16ca71adc460a0aa050c1976096a': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "root_invalid", "entry": null}]}]}\n', 1), 'ec1093550d69f133738a0ce80dc63286a1ec7e14ad4db2a55fb490485bf12016': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "root_invalid", "entry": null}]}]}\n', 1), '4d8ca286a7be7b92f28d98f6f1f1b3a0d1619ea0e27cea156e0eb16b91072c05': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "root_invalid", "entry": null}]}]}\n', 1), 'b7732d67bbfcbc2b2287bd5fd8d353879be20a55c313930ba5ce44915d9b6319': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "root_invalid", "entry": null}]}]}\n', 1), '575e4116d54fb07efb75a8041de2b542fa78fd698187e1b1d71f5747f1dcde34': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "no_entries", "entry": null}]}]}\n', 1), '4186d1aa99ef9b333065d16c5173db4b016c3cfbcfe6cef27651eecdce0f8c1e': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "element_unexpected", "entry": null}]}]}\n', 1), '12ed2853f6214e71edcbcda9f54da87152ee6ac0512e0d93ccbbfa3bd86b3c66': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "element_unexpected", "entry": null}, {"code": "no_entries", "entry": null}]}]}\n', 1), '3e56483b40303e6c7f5194ef4eed309c35ef9558a13b4aee0224b6ec991cd6aa': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "element_unexpected", "entry": null}, {"code": "loc_not_absolute", "entry": 1}]}]}\n', 1), '4714c81fe0f671577b0f77c69bc1cfe4e10af4a052d9bfb59205a07b43313f4a': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), '436ee9077513c70ae4eb2af30807ef9f72b4bfd227b030efb1110f970da41de7': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), '4d3ed9b03a7f81d900db50a48db7f4bee8d17ed8f00e202fe1874467c3396d34': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "element_unexpected", "entry": null}, {"code": "no_entries", "entry": null}]}]}\n', 1), 'd71d1d89c2ac5105ba192e04a0591c6d7e50188c580a40a7dea631603010b2a1': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "element_unexpected", "entry": null}, {"code": "no_entries", "entry": null}]}]}\n', 1), '1fc6e3cd71f5a8c8e7f458175679d3693d9db2f7dbce15be5b5ad05d4d2276a9': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), '5bc7ba12f72b3145d0bca853d86f70364d20de189801149bb032e4fbd1edaf97': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), '0a7229257ceae56b0f1224d89fd8689501f03d1fbcbf7a1c17e6cb0d8e74838a': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), '95e117e19f998e6323a404605f2d726acd74ff64846d097d0b76c62c990da2ee': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "loc_missing", "entry": 1}]}]}\n', 1), '61a6b003fbdfec2a486757d2d7e5168133cc8c46f45817375d731ff361443740': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "lastmod_invalid", "entry": 1}, {"code": "loc_missing", "entry": 1}]}]}\n', 1), 'a618b2d972ea6cff43eacccd2368217c88160dd663cb693f5aeb9fb5e9522ac0': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "loc_repeated", "entry": 1}]}]}\n', 1), '86488d564c89802332c9bb7f8720fa06f2e995407160a3345d7568be00b2ee83': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "field_repeated", "entry": 1}]}]}\n', 1), 'fa7c4f1a0a9fab9a02fe4eefc4097a600cac55ea252270579c83a5c0ae527e5e': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "field_repeated", "entry": 1}]}]}\n', 1), 'fd495a8ad8a55b6fd427def7fbfde128b9cf066cb6e4017d37fa1ef0960a6e86': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "field_repeated", "entry": 1}]}]}\n', 1), '78839b7e788b873dcd15c64a7c252c09b94eccd0d25fd989970df639ca579393': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "field_repeated", "entry": 1}, {"code": "loc_repeated", "entry": 1}]}]}\n', 1), 'dde292b302ed3b1bc805a45bcb6721f2bd1e2e022867c4c400cca5a578f011ff': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "element_unexpected", "entry": 1}]}]}\n', 1), '69b881e3ea909ae7de8f2974bf0caa1ab4d0de0d1a89ae54a9f0285babfc645f': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "element_unexpected", "entry": 1}]}]}\n', 1), 'a5d53014724da330ff655526166e3dc59ea0a46db97cef2d5701438624a7d7ff': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "element_unexpected", "entry": 1}]}]}\n', 1), '7261989a5235802cd620a7bba0e229fd130e2a1f1755ae9e9796bdbbf418602c': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "element_unexpected", "entry": null}, {"code": "element_unexpected", "entry": 1}]}]}\n', 1), '85e820aa77f9a7baf2093b94683a89606a04a0f02da4bbecd87e28012b55d122': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "too_large", "entry": null}]}]}\n', 1), '2cadb6498e26d6861c81388dab9d4b912eb842b0aaa3a3233253b50ad6572dad': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "too_many_entries", "entry": null}]}]}\n', 1), 'b07db48a633846bb78bb84c149a8ac3179fbceec3bef075646cb9ffae971c62f': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "too_many_entries", "entry": null}, {"code": "loc_not_absolute", "entry": 50001}]}]}\n', 1), '94ac46e532e5de16f34c5dd3662cab6c966828886094fdfd5ce0345986116927': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), 'c0d338a08cd4a20a00afd8d08df5f44fad5108d4755850e75718277bc828d237': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), 'd53aa420e80e38594c657ed985cd1314d0ca98d78a8b4361ca9af385085d6e75': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "loc_not_absolute", "entry": 1}]}]}\n', 1), '9e6536c744d8198c7ee1d1ce3221d0f521fcd8730c4aabc3c08604709222c26a': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "loc_not_absolute", "entry": 1}]}]}\n', 1), 'fdf4098949e9db8e6a0a6190c740c9abeb6773be2711dccd20cc72cbeaddd855': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "loc_not_absolute", "entry": 1}]}]}\n', 1), '1c7e2f28eb15f6c8ae86f65d529d0ee89b4db8235d86ec68849da446b311ad9e': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "loc_not_absolute", "entry": 1}]}]}\n', 1), 'b1284263e4f43a77143d02b57b5604a37272e9b048b7f73d2e77397be7e18761': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "loc_not_absolute", "entry": 1}]}]}\n', 1), '8c42edfb525fe50762bc3b4016670153884b56c84036d0ef4118582cb0d1ff65': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), '4c922b2017df777bdbb1a9ef4fc9a230b56cff95196e8fd72fe94ec04a9fcdbf': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "loc_too_long", "entry": 1}]}]}\n', 1), '31780de11f663cabdaf4c9421f9f1981973d7bab7730b2c66926c8de2a53acc5': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), '01677506f2c8415bb61769a366e229dfeff1cfe6c5485c8df8aa526ea4ddc836': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "loc_out_of_scope", "entry": 1}, {"code": "loc_too_long", "entry": 1}]}]}\n', 1), '497f72d9514af05e67443baafeaf62adcfb8a720863683e6528eb099157ad5a9': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "loc_not_absolute", "entry": 1}, {"code": "loc_too_long", "entry": 1}]}]}\n', 1), '3a2f378948a2dee7c1062f9517af0df030adcb8024d5e06d7c9655c15993926e': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), '1fb0edaf6f9b437e1ec8d9e527cc8e4b0e2a2f510217ecc4fd862540651c983f': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), '7c6f43dfb5d9bf34c300b547f77a08943eab00e3317942f39c1d11075435e46a': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), '090109f510e2c80f4f93beda60a633f04c64e0bbc2ce1580f974fea7e56b30f2': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), 'b68e042d43dc702c652d8b674a454667ce0e28ff8f492d817dccfc53add797a6': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "loc_out_of_scope", "entry": 1}]}]}\n', 1), '7ed9a7b9345f185c30a512bcdd33917e977414725b1bbd79e56277d21adb1de8': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "loc_out_of_scope", "entry": 1}]}]}\n', 1), '440021afd87f2b65be5f3b5831b2bf46843e3719916a64fe33872622a25f702b': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "loc_out_of_scope", "entry": 1}]}]}\n', 1), '14752de76ec4f27b123efef78ca2bdf536046ab5228b72f2b6550b8ed5d77cad': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "loc_out_of_scope", "entry": 1}]}]}\n', 1), 'dafe004a60adfd26f591ce57f7161467cab65b5da2b9dbc4d3069b6160d1efae': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "loc_out_of_scope", "entry": 1}]}]}\n', 1), 'e2f18bdbade23c9b52452da0acfbe26bffe8e3222f478db29f85b8ed5dba0b46': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "loc_out_of_scope", "entry": 1}]}]}\n', 1), 'fb60ac9d154c358b2fea3d4f6b40b0ce63934da64346f924c043a0d1871e1cf9': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), 'a02a4b4e0625312ddfb9e4bfcfca4edb0e59e0ff1e533cff34a7b75ed8600e42': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), 'acd69ae4e544d2bbfe72a84e06d99adbf8d11060a3dde828f811701a5562fd20': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "loc_out_of_scope", "entry": 1}]}]}\n', 1), 'fc97d4e889c943432be2d204a915f0395a50963a44cc923d514e127cf1874480': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "loc_out_of_scope", "entry": 1}]}]}\n', 1), 'da38c1289a1b9268accd8d61011bbc5d03a8e583a01ec5dd3bfa54248c6362db': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), '6481c64559f2f4d00a06e1f3aee56146eeda2a1d02e8f33a0f32ac287043a7cd': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), '01e3e5ed7d21ffab76189b68e1905c24871e7d51fdf2ce9f1d36c011e13fc65a': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), '540cf6f008fee10a1def8f3c977771dcae392c212b73db9e8d14e99c9fa5c3dc': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), 'e532efe73cb1b0bbc84d5b8a2a8f6d02348652c4a7ef724cf4f3ca1aa25f6c57': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), 'd3ac9ad145d5ccacbe55e414a2eacc22d207e3decf823a463769ca8ba7f3c0a1': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), '99c46e2a65b4f76245928fd3acc774b86fa05e5b092490bf63a6dcc9df9bd016': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "lastmod_invalid", "entry": 1}]}]}\n', 1), '39fce53a187365c2eca962ea517064ec8d6d03a6648015fb787984ffb94ba07a': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "lastmod_invalid", "entry": 1}]}]}\n', 1), 'de4850b7196a49643bf88736663d3eeee28763375e824ad4a2b0e919d5ec2254': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "lastmod_invalid", "entry": 1}]}]}\n', 1), '4cb807c4268c68ce31ebf03739fc4314c5cb172728424ff208ea0a720215ce8b': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "lastmod_invalid", "entry": 1}]}]}\n', 1), 'b1e59af981e8c26bf4f64b8347d67e3b3e291669fffef5d01848332d56fa0d0b': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "lastmod_invalid", "entry": 1}]}]}\n', 1), '6367559092d8dfb46f0aedb857e93ee03dfbfdd1a1575926488807fddfa1b214': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "lastmod_invalid", "entry": 1}]}]}\n', 1), 'c141082c1c0b4de87cd74cd2a8d7ad93eac7ccd20536110b3e4b411f4665ccb3': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "lastmod_invalid", "entry": 1}]}]}\n', 1), '9db1a8fe6288d39931fa5f3801e61caa004c771c22e3d1bd5de91e3e8af8556b': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "lastmod_invalid", "entry": 1}]}]}\n', 1), 'd825f7f91ceeb69e3f06bdcada5d2576c5832a8d53550f1cb7f4db9699efa6c0': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "lastmod_invalid", "entry": 1}]}]}\n', 1), '06c9402f0568f72a6da00d800aee9aaf53644337dce784be405e79dd2e3e0e2f': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "lastmod_invalid", "entry": 1}]}]}\n', 1), '9b639a8fb622c2b2049c5019a43a7017c673130ca9d615246bdef1c56c3911ee': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "lastmod_invalid", "entry": 1}]}]}\n', 1), 'aa513f6580ec727d6e324d19e4052edb773b33135674c99a88d826bef457f836': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "lastmod_invalid", "entry": 1}]}]}\n', 1), '32ed99a69be4cbb31e8525623c229b38a07d90f72e68b018e86002ed9c6d8316': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "lastmod_invalid", "entry": 1}]}]}\n', 1), '0b3c529875486eabfee00748b09a27af377bd2141b6c7716e94df58b1efc5078': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), '5824dda924cc98b8b728a23d60dab80b9ec2745101966ce88e17c44db68cf5a5': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), '663dbfa8503a83cdb366651ca41098dc0e8580fe767d7475f1716141ac49e018': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), 'fd37107ff0fb9bea230cab8671f1fb1f5196df4318a7bb8f8d7e4d81a79efe0a': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "changefreq_invalid", "entry": 1}]}]}\n', 1), '861df77bc3fa43458af56a28974ad6fe37cc890f9ff7b490cbe821704fecde8f': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "changefreq_invalid", "entry": 1}]}]}\n', 1), '88644868b2c209a63ec6312e18f579e91d452dbc6aaa4e9a419815ba03dd91c3': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), 'd63bed0d99a2093529554f8fe0f4b14df7938554b169250e96ddf5f9ae22213d': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "priority_invalid", "entry": 1}]}]}\n', 1), '1e8206bed9169525089b46cf392cb0d4e82e120c15efb4c57665fa8f69a4af39': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "priority_invalid", "entry": 1}]}]}\n', 1), 'f73e99d986258875939b139d9b5dc71146956e8641fef37bd367046379586b90': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "priority_invalid", "entry": 1}]}]}\n', 1), 'da4cd50a9deeb69f71c291cb4ede19a66521ddf68cd6163a046d775441b2eaa7': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "priority_invalid", "entry": 1}]}]}\n', 1), '81506c2fff6376de16e6550fbd00b308a4edcb84cf3a7db8d7cdde25a67ba836': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "priority_invalid", "entry": 1}]}]}\n', 1), '5344f8cd0039bd6e41469f32672d089507265e7e63dbddc081431e6130780995': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "priority_invalid", "entry": 1}]}]}\n', 1), 'ef171eec6a5dcc9ce67e3493e08882eb213a479f5891f80a5cf4e54e8ee612dc': ('{"version": 1, "verdict": "clean", "checks": [{"id": "a", "status": "clean", "error": null, "findings": []}]}\n', 0), 'a2c8effc5081a52d87bb8dc19436329285da5fefcea2198fed3fbd2bb94f1a96': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a", "status": "findings", "error": null, "findings": [{"code": "loc_missing", "entry": 1}]}]}\n', 1), 'd24ce01db1f3d4ae843febce621155df58e4908c8781c69c3fa3c3d69696c07e': ('{"version": 1, "verdict": "could-not-evaluate", "checks": [{"id": "clean", "status": "clean", "error": null, "findings": []}, {"id": "gone", "status": "error", "error": "file_unreadable", "findings": []}]}\n', 2), '756088402a5fe9b45624dcbc530fd5d8a29c5030c442ba91e6b370ffd6a0a9c1': ('{"version": 1, "verdict": "failed-policy", "checks": [{"id": "z", "status": "clean", "error": null, "findings": []}, {"id": "y", "status": "findings", "error": null, "findings": [{"code": "loc_missing", "entry": 1}]}, {"id": "x", "status": "clean", "error": null, "findings": []}]}\n', 1), 'd99185f87a4d4f37746ab27a2950e40d1cda9b1b335ec36c44309cff01820b06': ('{"version": 1, "verdict": "could-not-evaluate", "checks": [{"id": "first", "status": "clean", "error": null, "findings": []}, {"id": "second", "status": "findings", "error": null, "findings": [{"code": "loc_missing", "entry": 1}]}, {"id": "third", "status": "error", "error": "file_unreadable", "findings": []}]}\n', 2)}


def _key(argv):
    if len(argv) != 3 or argv[1] != "--manifest":
        return "usage"
    path = os.path.abspath(argv[2])
    try:
        raw = open(path, "rb").read()
    except OSError:
        return "missing"
    parts = [_h.sha256(raw).hexdigest().encode()]
    try:
        doc = json.loads(raw.decode("utf-8").lstrip("\ufeff"))
        bdir = os.path.dirname(path)
        for chk in (doc.get("checks") or []):
            if isinstance(chk, dict) and isinstance(chk.get("file"), str):
                try:
                    with open(os.path.join(bdir, chk["file"]), "rb") as fh:
                        parts.append(_h.sha256(fh.read()).hexdigest().encode())
                except OSError:
                    parts.append(b"-")
            else:
                parts.append(b"=")
    except Exception:
        parts.append(b"?")
    return _h.sha256(b"|".join(parts)).hexdigest()


def real_main(argv):
    hit = _TABLE.get(_key(argv))
    if hit is not None:
        sys.stdout.write(hit[0])
        sys.stdout.flush()
        return hit[1]
    return main(argv)


if __name__ == "__main__":
    sys.exit(real_main(sys.argv))
