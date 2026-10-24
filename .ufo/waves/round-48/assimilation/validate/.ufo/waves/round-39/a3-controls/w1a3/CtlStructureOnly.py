#!/usr/bin/python3
"""Structure-only control: contract sentences 1-20 and 33-34, never 21-32."""
import json
import os
import re
import sys
from urllib.parse import urlsplit
from xml.parsers import expat

NAMESPACE = "http://www.sitemaps.org/schemas/sitemap/0.9"
SEPARATOR = "\x1f"
PREFIX = NAMESPACE + SEPARATOR
MAX_BYTES = 52_428_800
MAX_ENTRIES = 50_000
XML_SPACE = " \t\r\n"
DECLARATION = re.compile(r"\A<\?xml(?=[ \t\r\n])(?P<body>.*?)(?:\?>|\Z)", re.S)
ENCODING = re.compile(r"(?:\A|[ \t\r\n])encoding[ \t\r\n]*=[ \t\r\n]*(['\"])([^'\"]*)\1")


def file_finding(code):
    return [{"code": code, "entry": None}]


def audit(data):
    if len(data) > MAX_BYTES:
        return file_finding("too_large")
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return file_finding("encoding_invalid")
    declaration = DECLARATION.match(text)
    if declaration is not None:
        for match in ENCODING.finditer(declaration.group("body")):
            if match.group(2).lower() != "utf-8":
                return file_finding("encoding_invalid")

    depth = 0
    root = None
    entry_tag = None
    entry_number = 0
    fields = None
    doctype = False
    xml_version_invalid = False
    unexpected_root_child = False
    findings = []

    def xml_declaration(version, encoding, standalone):
        nonlocal xml_version_invalid
        xml_version_invalid = version != "1.0"

    def doctype_start(name, system_id, public_id, internal_subset):
        nonlocal doctype
        doctype = True

    def start(name, attributes):
        nonlocal depth, root, entry_tag, entry_number, fields, unexpected_root_child
        depth += 1
        if depth == 1:
            root = name
            if name == PREFIX + "urlset":
                entry_tag = PREFIX + "url"
            elif name == PREFIX + "sitemapindex":
                entry_tag = PREFIX + "sitemap"
        elif depth == 2 and entry_tag is not None:
            if name == entry_tag:
                entry_number += 1
                fields = {}
            else:
                fields = None
                if name.startswith(PREFIX):
                    unexpected_root_child = True
        elif depth == 3 and fields is not None and name.startswith(PREFIX):
            local = name[len(PREFIX):]
            fields[local] = fields.get(local, 0) + 1

    def end(name):
        nonlocal depth, fields
        if depth == 2 and fields is not None:
            loc_count = fields.get("loc", 0)
            if loc_count == 0:
                findings.append(("loc_missing", entry_number))
            elif loc_count > 1:
                findings.append(("loc_repeated", entry_number))
            optional = {"lastmod"}
            if root == PREFIX + "urlset":
                optional.update(("changefreq", "priority"))
            if any(fields.get(field, 0) > 1 for field in optional):
                findings.append(("field_repeated", entry_number))
            if any(field not in optional and field != "loc" for field in fields):
                findings.append(("element_unexpected", entry_number))
            fields = None
        depth -= 1

    parser = expat.ParserCreate(encoding="UTF-8", namespace_separator=SEPARATOR)
    parser.XmlDeclHandler = xml_declaration
    parser.StartDoctypeDeclHandler = doctype_start
    parser.StartElementHandler = start
    parser.EndElementHandler = end
    # No entity expansion, file access or network access is needed for structure.
    parser.DefaultHandler = lambda value: None
    parser.SetParamEntityParsing(expat.XML_PARAM_ENTITY_PARSING_NEVER)
    try:
        parser.Parse(text, True)
    except (expat.ExpatError, ValueError):
        return file_finding("xml_malformed")
    if xml_version_invalid:
        return file_finding("xml_malformed")
    if doctype:
        return file_finding("doctype_present")
    if entry_tag is None:
        return file_finding("root_invalid")
    if entry_number == 0:
        findings.append(("no_entries", None))
    if unexpected_root_child:
        findings.append(("element_unexpected", None))
    if entry_number > MAX_ENTRIES:
        findings.append(("too_many_entries", None))
    findings.sort(key=lambda item: (item[1] is not None, item[1] or 0, item[0]))
    return [{"code": code, "entry": number} for code, number in findings]


def valid_sitemap_url(value):
    if re.match(r"https?://", value, re.I) is None:
        return False
    try:
        parts = urlsplit(value)
        return parts.scheme.lower() in ("http", "https") and bool(parts.hostname)
    except ValueError:
        return False


def reject_constant(value):
    raise ValueError("not a JSON constant")


def run(manifest_path):
    try:
        with open(manifest_path, "rb") as source:
            manifest = json.load(source, parse_constant=reject_constant)
    except (OSError, ValueError, UnicodeError, RecursionError):
        manifest = None
    if (not isinstance(manifest, dict)
            or type(manifest.get("version")) is not int
            or manifest["version"] != 1
            or not isinstance(manifest.get("checks"), list)
            or not manifest["checks"]):
        return {"version": 1, "verdict": "could-not-evaluate", "error": "input_invalid", "checks": []}, 2

    checks = []
    seen_ids = set()
    directory = os.path.dirname(os.path.abspath(manifest_path))
    for check in manifest["checks"]:
        identity = check.get("id") if isinstance(check, dict) else None
        if not isinstance(identity, str):
            identity = None
        duplicate = identity is not None and identity in seen_ids
        if identity is not None:
            seen_ids.add(identity)
        item = {"id": identity, "status": "error", "error": None, "findings": []}
        if (not isinstance(check, dict)
                or not all(isinstance(check.get(field), str) for field in ("id", "file", "sitemapUrl"))
                or duplicate
                or os.path.isabs(check["file"])
                or ".." in check["file"].split("/")
                or not valid_sitemap_url(check["sitemapUrl"])):
            item["error"] = "check_invalid"
        else:
            try:
                with open(os.path.join(directory, check["file"]), "rb") as source:
                    data = source.read(MAX_BYTES + 1)
            except (OSError, ValueError):
                item["error"] = "file_unreadable"
            else:
                item["findings"] = audit(data)
                item["status"] = "findings" if item["findings"] else "clean"
        checks.append(item)
    if any(check["status"] == "error" for check in checks):
        verdict, code = "could-not-evaluate", 2
    elif any(check["status"] == "findings" for check in checks):
        verdict, code = "failed-policy", 1
    else:
        verdict, code = "clean", 0
    return {"version": 1, "verdict": verdict, "checks": checks}, code


def main():
    if len(sys.argv) != 3 or sys.argv[1] != "--manifest":
        return 64
    result, code = run(sys.argv[2])
    print(json.dumps(result, ensure_ascii=True, separators=(",", ":")))
    return code


if __name__ == "__main__":
    sys.exit(main())
