#!/usr/bin/env python3
"""Degenerate constant 4/4: empty-list stub.

Validates the manifest exactly as a reader would (file readable and decodable,
url absolute, url unique) and then its link reader returns no links, so no
hreflang finding can ever be produced. Clean and input-fault cases pass; every
policy case is missed.
"""

import argparse
import json
import os
import sys
from urllib.parse import urlsplit

INPUT_IDS = ("input_unreadable", "input_duplicate_url",
             "input_url_not_absolute")


def absolute(url):
    if not isinstance(url, str):
        return False
    parts = urlsplit(url)
    return bool(parts.scheme) and bool(parts.netloc)


def main(argv=None):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--root", default=".")
    parser.add_argument("--json", action="store_true")
    args, _extra = parser.parse_known_args(argv)
    findings = []
    try:
        with open(args.manifest, "rb") as handle:
            manifest = json.loads(handle.read().decode("utf-8"))
        pages = manifest["pages"]
        if not isinstance(pages, list):
            raise ValueError("pages")
    except (OSError, ValueError, KeyError, TypeError, UnicodeDecodeError):
        findings.append({"id": "input_unreadable", "page": None})
        pages = []
    seen = set()
    for page in pages:
        url = page.get("url") if isinstance(page, dict) else None
        if not absolute(url):
            findings.append({"id": "input_url_not_absolute", "page": None})
        if url in seen:
            findings.append({"id": "input_duplicate_url",
                             "page": page.get("id")})
        seen.add(url)
    for page in pages:
        try:
            with open(os.path.join(args.root, page["file"]), "rb") as handle:
                handle.read().decode("utf-8")
        except (OSError, KeyError, UnicodeDecodeError):
            findings.append({"id": "input_unreadable",
                             "page": page.get("id")})
    has_input = any(row["id"] in INPUT_IDS for row in findings)
    code = 2 if has_input else 0
    report = {"version": 1, "pages": len(pages), "findings": findings,
              "counts": {"findings": len(findings)}, "exit": code}
    sys.stdout.write(json.dumps(report) + "\n")
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
