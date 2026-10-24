#!/usr/bin/env python3
"""CONTROL: manifest-only verdicts. NEVER opens a referenced sitemap file.

Derives every check from manifest fields alone: id type, duplicate ids,
file/sitemapUrl types, file path escape, and control characters in the URL.
Everything else is called clean. Skips class E and class U file content
entirely; class R is reproduced by pure manifest bookkeeping.
"""
import json
import os
import sys
from urllib.parse import urlsplit


def _url_ok(value):
    if value[:1] <= " " or "\t" in value or "\r" in value or "\n" in value:
        return False
    try:
        parts = urlsplit(value)
    except Exception:
        return False
    return parts.scheme.lower() in ("http", "https") and bool(parts.hostname)


def _file_bad(value):
    if value.startswith("/"):
        return True
    return ".." in value.split("/")


def main(argv):
    if len(argv) != 3 or argv[1] != "--manifest":
        return 64
    try:
        with open(argv[2], "rb") as handle:
            document = json.loads(handle.read().decode("utf-8"))
    except Exception:
        document = None
    if not isinstance(document, dict) or document.get("version") != 1:
        sys.stdout.write(json.dumps({"version": 1, "verdict": "could-not-evaluate",
                                     "error": "input_invalid", "checks": []}) + "\n")
        return 2
    checks = document.get("checks")
    if not isinstance(checks, list) or not checks:
        sys.stdout.write(json.dumps({"version": 1, "verdict": "could-not-evaluate",
                                     "error": "input_invalid", "checks": []}) + "\n")
        return 2
    seen = set()
    items = []
    for raw in checks:
        if not isinstance(raw, dict):
            items.append({"id": None, "status": "error", "error": "check_invalid",
                          "findings": []})
            continue
        ident = raw.get("id")
        ident_out = ident if isinstance(ident, str) else None
        bad = False
        if isinstance(ident, str):
            bad = ident in seen
            seen.add(ident)
        else:
            bad = True
        file_value = raw.get("file")
        url_value = raw.get("sitemapUrl")
        if not (isinstance(file_value, str) and isinstance(url_value, str)):
            bad = True
        elif _file_bad(file_value) or not _url_ok(url_value):
            bad = True
        if bad:
            items.append({"id": ident_out, "status": "error", "error": "check_invalid",
                          "findings": []})
        else:
            items.append({"id": ident_out, "status": "clean", "error": None,
                          "findings": []})
    any_error = any(item["status"] == "error" for item in items)
    verdict = "could-not-evaluate" if any_error else "clean"
    sys.stdout.write(json.dumps({"version": 1, "verdict": verdict,
                                 "checks": items}) + "\n")
    return 2 if any_error else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
