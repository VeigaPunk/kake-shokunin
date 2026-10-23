#!/usr/bin/env python3
"""Round-39 C1 supplementary control: manifest-only reader (no sitemap content).

Same "skip the work" property as control.py -- no sitemap byte is ever read and
no rule (a)-(k) is evaluated -- but it also reports the two manifest-level error
checks of the contract, so it upper-bounds what any tool that never opens a
sitemap file can score on the sealed key:

  * rule 4 -- a malformed check (not an object, missing/non-string member,
              repeated id, absolute or dot-dot `file`, non-absolute or hostless
              `sitemapUrl`) becomes an error check with error `check_invalid`.
  * rule 5 -- a `file` that cannot be read becomes an error check with error
              `file_unreadable` (existence/permission probe only, no read).

Every other check is reported clean with no findings, so every rule (a)-(k)
violation in a case is missed.  Standard library only, no network.
"""

import json
import os
import sys

EXIT_CLEAN = 0
EXIT_USAGE = 64
EXIT_INPUT_INVALID = 2

USAGE = "usage: control_manifest_only.py --manifest <path>\n"


def fail_usage():
    sys.stderr.write(USAGE)
    sys.exit(EXIT_USAGE)


def emit(doc, code):
    sys.stdout.write(json.dumps(doc) + "\n")
    sys.stdout.flush()
    sys.exit(code)


def emit_input_invalid():
    emit({
        "version": 1,
        "verdict": "could-not-evaluate",
        "error": "input_invalid",
        "checks": [],
    }, EXIT_INPUT_INVALID)


def load_manifest(path):
    try:
        with open(path, "rb") as fh:
            raw = fh.read()
    except OSError:
        return None
    try:
        doc = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return None
    if not isinstance(doc, dict):
        return None
    version = doc.get("version")
    if isinstance(version, bool) or version != 1:
        return None
    checks = doc.get("checks")
    if not isinstance(checks, list) or not checks:
        return None
    return doc


def sitemap_url_ok(value):
    if not isinstance(value, str):
        return False
    try:
        from urllib.parse import urlsplit
    except ImportError:  # pragma: no cover
        return False
    parts = urlsplit(value)
    return (parts.scheme.lower() in ("http", "https")
            and bool(parts.netloc) and bool(parts.hostname))


def file_path_ok(value):
    if not isinstance(value, str):
        return False
    if os.path.isabs(value):
        return False
    return ".." not in value.replace("\\", "/").split("/")


def check_invalid(check, seen_ids):
    if not isinstance(check, dict):
        return True
    for key in ("id", "file", "sitemapUrl"):
        if not isinstance(check.get(key), str):
            return True
    if check["id"] in seen_ids:
        return True
    if not file_path_ok(check["file"]):
        return True
    if not sitemap_url_ok(check["sitemapUrl"]):
        return True
    return False


def readable(path):
    return os.path.isfile(path) and os.access(path, os.R_OK)


def main(argv):
    if len(argv) != 2 or argv[0] != "--manifest":
        fail_usage()
    doc = load_manifest(argv[1])
    if doc is None:
        emit_input_invalid()
    base = os.path.dirname(os.path.abspath(argv[1]))
    items = []
    seen = set()
    any_error = False
    for check in doc["checks"]:
        cid = check.get("id") if isinstance(check, dict) else None
        if not isinstance(cid, str):
            cid = None
        if check_invalid(check, seen):
            items.append({"id": cid, "status": "error", "error": "check_invalid", "findings": []})
            any_error = True
        else:
            seen.add(check["id"])
            target = os.path.normpath(os.path.join(base, check["file"]))
            if not readable(target):
                items.append({"id": cid, "status": "error", "error": "file_unreadable", "findings": []})
                any_error = True
            else:
                items.append({"id": cid, "status": "clean", "error": None, "findings": []})
    verdict = "could-not-evaluate" if any_error else "clean"
    emit({"version": 1, "verdict": verdict, "checks": items},
         EXIT_INPUT_INVALID if any_error else EXIT_CLEAN)


if __name__ == "__main__":
    main(sys.argv[1:])
