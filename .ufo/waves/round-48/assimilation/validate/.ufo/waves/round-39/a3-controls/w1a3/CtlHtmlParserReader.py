#!/usr/bin/python3
"""Wrong-parser control: HTMLParser tokens, never an XML parser."""
import datetime
from decimal import Decimal
from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import urlsplit

NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
XML_SPACE = " \t\r\n"
MAX_BYTES = 52_428_800
DECLARATION = re.compile(r"\A<\?xml\s+(.*?)\?>", re.DOTALL | re.IGNORECASE)
ENCODING = re.compile(r"\bencoding\s*=\s*(['\"])(.*?)\1", re.DOTALL | re.IGNORECASE)
DECIMAL = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)\Z")
DATETIME = re.compile(
    r"(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})"
    r"(?:T(?P<hour>[0-9]{2}):(?P<minute>[0-9]{2})"
    r"(?::(?P<second>[0-9]{2})(?:\.[0-9]+)?)?"
    r"(?:Z|[+-](?P<zonehour>[0-9]{2}):(?P<zoneminute>[0-9]{2})))?\Z"
)
FREQUENCIES = frozenset(("always", "hourly", "daily", "weekly", "monthly", "yearly", "never"))


def tag_parts(name):
    prefix, separator, local = name.rpartition(":")
    return (prefix, local) if separator else ("", name)


class Element:
    __slots__ = ("name", "attrs", "children", "content")

    def __init__(self, name, attrs):
        self.name = name
        self.attrs = dict(attrs)
        self.children = []
        self.content = []

    def value(self, prefix):
        # Prefixes are literal HTML tag text, not namespace identities.
        pending = [iter(self.content)]
        chunks = []
        while pending:
            item = next(pending[-1], None)
            if item is None:
                pending.pop()
            elif isinstance(item, str):
                chunks.append(item)
            elif tag_parts(item.name)[0] == prefix:
                pending.append(iter(item.content))
        return "".join(chunks).strip(XML_SPACE)


class SitemapHTMLReader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.roots = []
        self.stack = []
        self.doctype = False
        self.outside_text = False

    def handle_starttag(self, tag, attrs):
        node = Element(tag, attrs)
        if self.stack:
            self.stack[-1].children.append(node)
            self.stack[-1].content.append(node)
        else:
            self.roots.append(node)
        self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        # HTML recovery deliberately accepts unclosed and mismatched elements.
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index].name == tag:
                del self.stack[index:]
                return

    def handle_data(self, data):
        if self.stack:
            self.stack[-1].content.append(data)
        elif data.strip(XML_SPACE):
            self.outside_text = True

    def handle_decl(self, decl):
        if decl.lower().startswith("doctype"):
            self.doctype = True

    def unknown_decl(self, data):
        # Older HTMLParser versions expose CDATA through this callback.
        if data.startswith("CDATA["):
            self.handle_data(data[6:])


def absolute_url(value):
    if not re.match(r"https?://", value, re.IGNORECASE):
        return None
    if any(character in XML_SPACE for character in value):
        return None
    try:
        parsed = urlsplit(value)
        if parsed.scheme.lower() not in ("http", "https") or not parsed.hostname:
            return None
        port = parsed.port
        if port is None:
            port = 80 if parsed.scheme.lower() == "http" else 443
        return parsed.scheme.lower(), parsed.hostname.lower(), port, parsed.path or "/"
    except ValueError:
        return None


def valid_lastmod(value):
    match = DATETIME.fullmatch(value)
    if match is None:
        return False
    fields = match.groupdict()
    try:
        datetime.date(int(fields["year"]), int(fields["month"]), int(fields["day"]))
    except ValueError:
        return False
    for name, maximum in (("hour", 23), ("minute", 59), ("second", 59),
                          ("zonehour", 23), ("zoneminute", 59)):
        if fields[name] is not None and int(fields[name]) > maximum:
            return False
    return True


def audit_bytes(data, sitemap_url):
    if len(data) > MAX_BYTES:
        return {("too_large", None)}
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return {("encoding_invalid", None)}
    declaration = DECLARATION.match(text)
    if declaration is not None:
        encoding = ENCODING.search(declaration.group(1))
        if encoding is not None and encoding.group(2).lower() != "utf-8":
            return {("encoding_invalid", None)}

    reader = SitemapHTMLReader()
    try:
        reader.feed(text)
        reader.close()
    except (AssertionError, ValueError):
        return {("doctype_present" if reader.doctype else "xml_malformed", None)}
    if reader.doctype:
        return {("doctype_present", None)}
    if len(reader.roots) != 1 or reader.outside_text:
        return {("xml_malformed", None)}
    root = reader.roots[0]
    prefix, kind = tag_parts(root.name)
    # This literal marker check is intentionally not namespace resolution.
    marker = "xmlns:" + prefix if prefix else "xmlns"
    if kind not in ("urlset", "sitemapindex") or root.attrs.get(marker) != NS:
        return {("root_invalid", None)}

    findings = set()
    entry_name = "url" if kind == "urlset" else "sitemap"
    entries = []
    for child in root.children:
        child_prefix, local = tag_parts(child.name)
        if child_prefix != prefix:
            continue
        if local == entry_name:
            entries.append(child)
        else:
            findings.add(("element_unexpected", None))
    if not entries:
        findings.add(("no_entries", None))
    if len(entries) > 50_000:
        findings.add(("too_many_entries", None))

    base = absolute_url(sitemap_url)
    directory = base[3].rsplit("/", 1)[0] + "/"
    allowed = {"loc", "lastmod"}
    if kind == "urlset":
        allowed.update(("changefreq", "priority"))
    for number, entry in enumerate(entries, 1):
        fields = {}
        for child in entry.children:
            child_prefix, local = tag_parts(child.name)
            if child_prefix != prefix:
                continue
            if local not in allowed:
                findings.add(("element_unexpected", number))
            else:
                fields.setdefault(local, []).append(child)
        locations = fields.get("loc", [])
        if len(locations) != 1:
            findings.add(("loc_missing" if not locations else "loc_repeated", number))
        else:
            location = locations[0].value(prefix)
            parsed = absolute_url(location)
            if parsed is None:
                findings.add(("loc_not_absolute", number))
            else:
                if parsed[:3] != base[:3] or (kind == "urlset" and not parsed[3].startswith(directory)):
                    findings.add(("loc_out_of_scope", number))
            if len(location) >= 2048:
                findings.add(("loc_too_long", number))
        for name in allowed - {"loc"}:
            values = fields.get(name, [])
            if len(values) > 1:
                findings.add(("field_repeated", number))
                continue
            if not values:
                continue
            value = values[0].value(prefix)
            if name == "lastmod":
                valid = valid_lastmod(value)
            elif name == "changefreq":
                valid = value in FREQUENCIES
            else:
                valid = DECIMAL.fullmatch(value) is not None and Decimal(0) <= Decimal(value) <= Decimal(1)
            if not valid:
                findings.add((name + "_invalid", number))
    return findings


def error_check(identifier, error):
    return {"id": identifier, "status": "error", "error": error, "findings": []}


def input_invalid():
    return {"version": 1, "verdict": "could-not-evaluate", "error": "input_invalid", "checks": []}, 2


def audit_manifest(filename):
    manifest_path = Path(filename)
    try:
        with manifest_path.open("r", encoding="utf-8") as stream:
            manifest = json.load(stream)
    except (OSError, ValueError, UnicodeError):
        return input_invalid()
    if (not isinstance(manifest, dict) or type(manifest.get("version")) is not int
            or manifest["version"] != 1 or not isinstance(manifest.get("checks"), list)
            or not manifest["checks"]):
        return input_invalid()

    checks = []
    seen = set()
    for check in manifest["checks"]:
        identifier = check.get("id") if isinstance(check, dict) else None
        if not isinstance(identifier, str):
            identifier = None
        duplicate = identifier is not None and identifier in seen
        if identifier is not None:
            seen.add(identifier)
        valid = (isinstance(check, dict) and all(isinstance(check.get(key), str)
                 for key in ("id", "file", "sitemapUrl")) and not duplicate)
        if valid:
            path = PurePosixPath(check["file"])
            valid = (not path.is_absolute() and ".." not in path.parts
                     and absolute_url(check["sitemapUrl"]) is not None)
        if not valid:
            checks.append(error_check(identifier, "check_invalid"))
            continue
        try:
            with (manifest_path.parent / check["file"]).open("rb") as stream:
                data = stream.read(MAX_BYTES + 1)
        except (OSError, ValueError):
            checks.append(error_check(identifier, "file_unreadable"))
            continue
        findings = audit_bytes(data, check["sitemapUrl"])
        ordered = sorted(findings, key=lambda item: (item[1] is not None, item[1] or 0, item[0]))
        checks.append({"id": identifier, "status": "findings" if findings else "clean", "error": None,
                       "findings": [{"code": code, "entry": number} for code, number in ordered]})
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
    result, code = audit_manifest(sys.argv[2])
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    return code


if __name__ == "__main__":
    sys.exit(main())
