#!/usr/bin/python3
"""Deliberately values-only sitemap control; no structural policy audit."""

import datetime
import decimal
import json
import os
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET


NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
XML_SPACE = " \t\r\n"
FREQUENCIES = frozenset(("always", "hourly", "daily", "weekly", "monthly", "yearly", "never"))
DATE = re.compile(
    r"([0-9]{4})-([0-9]{2})-([0-9]{2})"
    r"(?:T([0-9]{2}):([0-9]{2})(?::([0-9]{2})(?:\.[0-9]+)?)?"
    r"(Z|[+-][0-9]{2}:[0-9]{2}))?"
)
DECIMAL = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)")


def local_name(tag):
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else ""


def http_url(value):
    try:
        parsed = urllib.parse.urlsplit(value)
        if parsed.scheme.lower() not in ("http", "https") or not parsed.hostname:
            return None
        # Force validation now rather than raising during a scope comparison.
        parsed.port
        return parsed
    except (ValueError, UnicodeError):
        return None


def origin(parsed):
    scheme = parsed.scheme.lower()
    port = parsed.port
    return scheme, parsed.hostname.lower(), port if port is not None else (80 if scheme == "http" else 443)


def valid_lastmod(value):
    match = DATE.fullmatch(value)
    if match is None:
        return False
    year, month, day, hour, minute, second, zone = match.groups()
    try:
        datetime.date(int(year), int(month), int(day))
    except ValueError:
        return False
    if hour is None:
        return True
    if int(hour) > 23 or int(minute) > 59 or (second is not None and int(second) > 59):
        return False
    return zone == "Z" or (int(zone[1:3]) <= 23 and int(zone[4:6]) <= 59)


def valid_priority(value):
    if DECIMAL.fullmatch(value) is None:
        return False
    try:
        return decimal.Decimal(0) <= decimal.Decimal(value) <= decimal.Decimal(1)
    except decimal.InvalidOperation:
        return False


def audit(data, sitemap_url):
    try:
        root = ET.fromstring(data)
    except Exception:
        return [{"code": "xml_malformed", "entry": None}]

    is_index = local_name(root.tag) == "sitemapindex"
    entry_tag = "{" + NS + "}" + ("sitemap" if is_index else "url")
    base = http_url(sitemap_url)
    base_origin = origin(base)
    base_path = base.path or "/"
    directory = base_path[:base_path.rfind("/") + 1]
    findings = []
    found = set()

    def add(code, entry):
        key = code, entry
        if key not in found:
            found.add(key)
            findings.append({"code": code, "entry": entry})

    def value_rules(element, entry):
        name = local_name(element.tag)
        if name not in ("loc", "lastmod", "changefreq", "priority"):
            return
        value = "".join(element.itertext()).strip(XML_SPACE)
        if name == "loc":
            parsed = http_url(value)
            if parsed is None:
                add("loc_not_absolute", entry)
            if len(value) >= 2048:
                add("loc_too_long", entry)
            if parsed is not None:
                if origin(parsed) != base_origin or (not is_index and not (parsed.path or "/").startswith(directory)):
                    add("loc_out_of_scope", entry)
        elif name == "lastmod":
            if not valid_lastmod(value):
                add("lastmod_invalid", entry)
        elif name == "changefreq" and not is_index:
            if value not in FREQUENCIES:
                add("changefreq_invalid", entry)
        elif name == "priority" and not is_index:
            if not valid_priority(value):
                add("priority_invalid", entry)

    # Entry coordinates are metadata only: no structural or cardinality rule.
    value_rules(root, None)
    entry_number = 0
    for child in root:
        entry = None
        if child.tag == entry_tag:
            entry_number += 1
            entry = entry_number
        for element in child.iter():
            value_rules(element, entry)
    return findings


def emit(payload, code):
    print(json.dumps(payload, ensure_ascii=True, separators=(",", ":")))
    return code


def main(arguments):
    if len(arguments) != 2 or arguments[0] != "--manifest":
        return 64
    manifest_path = arguments[1]
    try:
        with open(manifest_path, "rb") as handle:
            manifest = json.load(handle)
    except (OSError, ValueError, UnicodeError, RecursionError):
        manifest = None
    if (not isinstance(manifest, dict) or type(manifest.get("version")) is not int
            or manifest["version"] != 1 or not isinstance(manifest.get("checks"), list)
            or not manifest["checks"]):
        return emit({"version": 1, "verdict": "could-not-evaluate", "error": "input_invalid", "checks": []}, 2)

    checks = []
    seen_ids = set()
    manifest_directory = os.path.dirname(os.path.abspath(manifest_path))
    for check in manifest["checks"]:
        identifier = check.get("id") if isinstance(check, dict) else None
        if not isinstance(identifier, str):
            identifier = None
        result = {"id": identifier, "status": "error", "error": None, "findings": []}
        checks.append(result)
        repeated = identifier is not None and identifier in seen_ids
        if identifier is not None:
            seen_ids.add(identifier)
        if (not isinstance(check, dict)
                or any(not isinstance(check.get(key), str) for key in ("id", "file", "sitemapUrl"))
                or repeated or os.path.isabs(check["file"])
                or ".." in check["file"].split("/") or http_url(check["sitemapUrl"]) is None):
            result["error"] = "check_invalid"
            continue
        try:
            with open(os.path.join(manifest_directory, check["file"]), "rb") as handle:
                data = handle.read()
        except (OSError, ValueError):
            result["error"] = "file_unreadable"
            continue
        result["findings"] = audit(data, check["sitemapUrl"])
        result["status"] = "findings" if result["findings"] else "clean"
    if any(check["status"] == "error" for check in checks):
        verdict, code = "could-not-evaluate", 2
    elif any(check["findings"] for check in checks):
        verdict, code = "failed-policy", 1
    else:
        verdict, code = "clean", 0
    return emit({"version": 1, "verdict": verdict, "checks": checks}, code)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
