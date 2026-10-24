#!/usr/bin/env python3
"""Round-39 C1 control -- the "constant errors" shape.

Reads ONLY the manifest.  It never opens, parses or audits the sitemap files the
manifest names, and implements none of contract rules (a)-(k).  Every check of a
well-formed manifest is reported as an error check whose code is picked from
manifest fields alone:

  * `check_invalid`   -- the manifest fields already violate contract sentence 4
                         (not an object, missing/non-string member, repeated id,
                         absolute or `..` file, sitemapUrl that is not an absolute
                         http/https URL with a host);
  * `file_unreadable` -- the constant for every other (well-formed) check.

Verdict and exit follow sentences 3 and 34: an invalid manifest is
`input_invalid` with exit 2; an error check is `could-not-evaluate` with exit 2;
a usage error is exit 64 with stdout ignored.

Standard library only; no network; the manifest is the only file opened.
"""

import json
import sys
from urllib.parse import urlsplit

REQUIRED = ("id", "file", "sitemapUrl")


def emit(doc, code):
    sys.stdout.write(json.dumps(doc, sort_keys=True) + "\n")
    sys.stdout.flush()
    sys.exit(code)


def input_invalid():
    emit({"version": 1, "verdict": "could-not-evaluate",
          "error": "input_invalid", "checks": []}, 2)


def usage():
    sys.exit(64)


def http_url_with_host(value):
    """True when value is an absolute http/https URL that carries a host."""
    try:
        parts = urlsplit(value)
    except ValueError:
        return False
    if parts.scheme.lower() not in ("http", "https"):
        return False
    if not parts.netloc:
        return False
    try:
        host = parts.hostname
    except ValueError:
        return False
    return bool(host)


def file_path_ok(value):
    """True when value is a relative path without a `..` path segment."""
    if value.startswith("/"):
        return False
    return ".." not in value.split("/")


def check_is_valid(check, seen_ids):
    """Contract sentence 4, decided from manifest fields only."""
    if not isinstance(check, dict):
        return False
    for key in REQUIRED:
        if key not in check or not isinstance(check[key], str):
            return False
    if check["id"] in seen_ids:
        return False
    if not file_path_ok(check["file"]):
        return False
    if not http_url_with_host(check["sitemapUrl"]):
        return False
    return True


def main(argv):
    if len(argv) != 3 or argv[1] != "--manifest":
        usage()
    manifest_path = argv[2]
    try:
        with open(manifest_path, "rb") as handle:
            raw = handle.read()
    except OSError:
        input_invalid()
    try:
        manifest = json.loads(raw)
    except Exception:
        input_invalid()
    if not isinstance(manifest, dict):
        input_invalid()
    version = manifest.get("version")
    if not isinstance(version, int) or isinstance(version, bool) or version != 1:
        input_invalid()
    checks = manifest.get("checks")
    if not isinstance(checks, list) or not checks:
        input_invalid()

    seen_ids = set()
    out = []
    for check in checks:
        identifier = check.get("id") if isinstance(check, dict) else None
        if not isinstance(identifier, str):
            identifier = None
        well_formed = check_is_valid(check, seen_ids)
        if isinstance(identifier, str):
            seen_ids.add(identifier)
        out.append({
            "id": identifier,
            "status": "error",
            "error": "file_unreadable" if well_formed else "check_invalid",
            "findings": [],
        })
    emit({"version": 1, "verdict": "could-not-evaluate", "checks": out}, 2)


if __name__ == "__main__":
    main(sys.argv)
