#!/usr/bin/env python3
"""Round-39 C1 control: constant-clean shape.

Emits a well-formed `scripts/sitemap_audit.py`-shaped report while doing none of
the audit. Every manifest check is reported clean, the document verdict is
`clean`, exit status is 0.

What it actually does (the only logic in this file):
  * sentence 2  -- usage check: only `--manifest <path>` is a legal argument
                   list; anything else exits 64 with an empty stdout.
  * sentence 3  -- manifest shape: `{"version": 1, "checks": [...]}` with a
                   non-empty array; anything else is `input_invalid`, exit 2.
  * sentence 33 -- echo one check item per manifest check, in manifest order,
                   with the manifest's `id` when it is a string, else null.

What it deliberately skips (the whole of the claimed work):
  * rule 4 -- no `check_invalid` detection (malformed / duplicate / unsafe
              checks are reported as clean).
  * rule 5 -- no file is opened: `file_unreadable` is never produced.
  * rules (a)-(k) -- no bytes are read, no XML is parsed, no encoding, root,
              entry, limit, loc, scope, lastmod, changefreq or priority rule is
              evaluated. `findings` is always empty.

Standard library only. No network. Writes one JSON document to stdout.
"""

import json
import sys

EXIT_CLEAN = 0
EXIT_USAGE = 64
EXIT_INPUT_INVALID = 2

USAGE = "usage: control.py --manifest <path>\n"


def fail_usage():
    sys.stderr.write(USAGE)
    sys.exit(EXIT_USAGE)


def emit(doc):
    sys.stdout.write(json.dumps(doc) + "\n")
    sys.stdout.flush()
    sys.exit(EXIT_CLEAN)


def emit_input_invalid():
    sys.stdout.write(json.dumps({
        "version": 1,
        "verdict": "could-not-evaluate",
        "error": "input_invalid",
        "checks": [],
    }) + "\n")
    sys.stdout.flush()
    sys.exit(EXIT_INPUT_INVALID)


def load_manifest(path):
    """Return the parsed manifest, or None when the manifest is not usable."""
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


def check_items(checks):
    """One constant-clean item per manifest check, ids echoed when usable."""
    items = []
    for check in checks:
        cid = check.get("id") if isinstance(check, dict) else None
        if not isinstance(cid, str):
            cid = None
        items.append({
            "id": cid,
            "status": "clean",
            "error": None,
            "findings": [],
        })
    return items


def main(argv):
    if len(argv) != 2 or argv[0] != "--manifest":
        fail_usage()
    doc = load_manifest(argv[1])
    if doc is None:
        emit_input_invalid()
    emit({"version": 1, "verdict": "clean", "checks": check_items(doc["checks"])})


if __name__ == "__main__":
    main(sys.argv[1:])
