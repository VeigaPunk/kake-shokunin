#!/usr/bin/python3
"""Key-blind sitemap control: parser/conversion conveniences, no lexical grammar."""

import json
import sys
from datetime import date, datetime
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET
from xml.parsers import expat

NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
MAX_BYTES = 52_428_800
FREQUENCIES = {"always", "hourly", "daily", "weekly", "monthly", "yearly", "never"}


class PrologueResult(Exception):
    pass


def url_parts(value):
    try:
        parsed = urlsplit(value)
        scheme = parsed.scheme.lower()
        host = parsed.hostname
        if scheme not in {"http", "https"} or not host:
            return None
        port = parsed.port
        return scheme, host.lower(), port if port is not None else {"http": 80, "https": 443}[scheme], parsed.path or "/"
    except ValueError:
        return None


def parse_xml(data):
    if len(data) > MAX_BYTES:
        return None, "too_large"
    try:
        text = data.decode("utf-8-sig")
    except UnicodeError:
        return None, "encoding_invalid"

    # Expat's event hooks expose declaration metadata without scanning XML text.
    probe = expat.ParserCreate(encoding="UTF-8")

    def declaration(version, encoding, standalone):
        if encoding is not None and encoding.lower() != "utf-8":
            raise PrologueResult("encoding_invalid")
        if version != "1.0":
            raise PrologueResult("xml_malformed")

    def doctype(*args):
        raise PrologueResult("doctype_present")

    def root_started(*args):
        raise PrologueResult(None)

    probe.XmlDeclHandler = declaration
    probe.StartDoctypeDeclHandler = doctype
    probe.StartElementHandler = root_started
    try:
        probe.Parse(text, True)
    except PrologueResult as result:
        if result.args[0] is not None:
            return None, result.args[0]
    except (expat.ExpatError, ValueError, LookupError):
        return None, "xml_malformed"
    try:
        return ET.fromstring(text), None
    except (ET.ParseError, ValueError, LookupError):
        return None, "xml_malformed"


def element_value(element):
    # Ignore foreign-namespace subtrees, retaining text after such subtrees.
    parts = []
    pending = [(element, False)]
    while pending:
        node, tail_only = pending.pop()
        if tail_only:
            parts.append(node.tail or "")
            continue
        parts.append(node.text or "")
        for child in reversed(node):
            pending.append((child, True))
            if child.tag.startswith(NS):
                pending.append((child, False))
    return "".join(parts).strip()


def valid_lastmod(value):
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return False
    if parsed.tzinfo is not None:
        return True
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def valid_priority(value):
    try:
        return 0.0 <= float(value) <= 1.0
    except (ValueError, OverflowError):
        return False


def audit(data, base):
    root, early = parse_xml(data)
    if early:
        return {(early, None)}
    if root.tag not in {NS + "urlset", NS + "sitemapindex"}:
        return {("root_invalid", None)}

    is_index = root.tag == NS + "sitemapindex"
    entry_tag = NS + ("sitemap" if is_index else "url")
    entries = [child for child in root if child.tag == entry_tag]
    findings = set()
    if not entries:
        findings.add(("no_entries", None))
    if len(entries) > 50_000:
        findings.add(("too_many_entries", None))
    if any(child.tag.startswith(NS) and child.tag != entry_tag for child in root):
        findings.add(("element_unexpected", None))

    optional = {"lastmod"} if is_index else {"lastmod", "changefreq", "priority"}
    allowed = {NS + field for field in optional | {"loc"}}
    directory = base[3].rpartition("/")[0] + "/"
    for number, entry in enumerate(entries, 1):
        fields = {name: [] for name in optional | {"loc"}}
        for child in entry:
            if not child.tag.startswith(NS):
                continue
            if child.tag not in allowed:
                findings.add(("element_unexpected", number))
            else:
                fields[child.tag[len(NS):]].append(child)

        locs = fields["loc"]
        if not locs:
            findings.add(("loc_missing", number))
        elif len(locs) > 1:
            findings.add(("loc_repeated", number))
        else:
            loc = element_value(locs[0])
            target = url_parts(loc)
            if target is None:
                findings.add(("loc_not_absolute", number))
            elif target[:3] != base[:3] or (not is_index and not target[3].startswith(directory)):
                findings.add(("loc_out_of_scope", number))
            if len(loc) >= 2_048:
                findings.add(("loc_too_long", number))

        for name in optional:
            occurrences = fields[name]
            if len(occurrences) > 1:
                findings.add(("field_repeated", number))
                continue
            if not occurrences:
                continue
            value = element_value(occurrences[0])
            valid = (
                valid_lastmod(value) if name == "lastmod" else
                valid_priority(value) if name == "priority" else
                value in FREQUENCIES
            )
            if not valid:
                findings.add((name + "_invalid", number))
    return findings


def error_check(identifier, error):
    return {"id": identifier, "status": "error", "error": error, "findings": []}


def evaluate_check(check, directory, seen):
    identifier = check.get("id") if isinstance(check, dict) else None
    if not isinstance(identifier, str):
        identifier = None
    repeated = identifier in seen if identifier is not None else False
    if identifier is not None:
        seen.add(identifier)
    if not isinstance(check, dict) or any(not isinstance(check.get(name), str) for name in ("id", "file", "sitemapUrl")) or repeated:
        return error_check(identifier, "check_invalid")
    file = PurePosixPath(check["file"])
    base = url_parts(check["sitemapUrl"])
    if file.is_absolute() or ".." in file.parts or base is None:
        return error_check(identifier, "check_invalid")
    try:
        with (directory / check["file"]).open("rb") as stream:
            data = stream.read(MAX_BYTES + 1)
    except (OSError, ValueError):
        return error_check(identifier, "file_unreadable")
    findings = audit(data, base)
    ordered = sorted(findings, key=lambda item: (item[1] or 0, item[0]))
    return {
        "id": identifier,
        "status": "findings" if findings else "clean",
        "error": None,
        "findings": [{"code": code, "entry": entry} for code, entry in ordered],
    }


def main(argv):
    if len(argv) != 3 or argv[1] != "--manifest":
        return 64
    path = Path(argv[2])
    try:
        with path.open("r", encoding="utf-8") as stream:
            manifest = json.load(stream)
        valid = (
            isinstance(manifest, dict)
            and type(manifest.get("version")) is int
            and manifest["version"] == 1
            and isinstance(manifest.get("checks"), list)
            and bool(manifest["checks"])
        )
    except (OSError, ValueError, UnicodeError):
        valid = False
    if not valid:
        print(json.dumps({"version": 1, "verdict": "could-not-evaluate", "error": "input_invalid", "checks": []}))
        return 2
    seen = set()
    checks = [evaluate_check(check, path.parent, seen) for check in manifest["checks"]]
    if any(check["status"] == "error" for check in checks):
        verdict, code = "could-not-evaluate", 2
    elif any(check["status"] == "findings" for check in checks):
        verdict, code = "failed-policy", 1
    else:
        verdict, code = "clean", 0
    print(json.dumps({"version": 1, "verdict": verdict, "checks": checks}, separators=(",", ":")))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
