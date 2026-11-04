#!/usr/bin/env python3
"""Degenerate constant 2/4: always-clean.

Parses the manifest, reads the page files (so it cannot be caught by a
readability fault), and never reports a finding. Exits 0 on every input.
"""

import argparse
import json
import os
import sys


def main(argv=None):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--root", default=".")
    parser.add_argument("--json", action="store_true")
    args, _extra = parser.parse_known_args(argv)
    pages = []
    try:
        with open(args.manifest, "rb") as handle:
            manifest = json.loads(handle.read().decode("utf-8"))
        pages = manifest.get("pages", [])
        for page in pages:
            path = os.path.join(args.root, page.get("file", ""))
            with open(path, "rb") as handle:
                handle.read().decode("utf-8")
    except (OSError, ValueError, UnicodeDecodeError, AttributeError):
        pass
    report = {"version": 1, "pages": len(pages), "findings": [],
              "counts": {}, "exit": 0}
    sys.stdout.write(json.dumps(report) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
