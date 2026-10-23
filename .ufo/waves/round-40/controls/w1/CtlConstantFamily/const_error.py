#!/usr/bin/env python3
"""CONTROL: constant all-error. Never reads any sitemap bytes.

Every check is reported as error=check_invalid with verdict could-not-evaluate
and exit 2, whatever the manifest says. Skips all three declared repairs.
"""
import json
import sys


def main(argv):
    if len(argv) != 3 or argv[1] != "--manifest":
        return 64
    try:
        with open(argv[2], "r", encoding="utf-8") as handle:
            document = json.load(handle)
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
    items = []
    for raw in checks:
        ident = raw.get("id") if isinstance(raw, dict) else None
        items.append({"id": ident if isinstance(ident, str) else None,
                      "status": "error", "error": "check_invalid", "findings": []})
    sys.stdout.write(json.dumps({"version": 1, "verdict": "could-not-evaluate",
                                 "checks": items}) + "\n")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
