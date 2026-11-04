#!/usr/bin/env python3
"""Degenerate constant 3/4: report-all.

Emits every policy finding id for every manifest page, so even a clean case
(and every single-finding case) is reported wrong. Exits 1 when it has pages,
0 when the manifest cannot be read as a page list.
"""

import argparse
import json
import sys

POLICY_IDS = (
    "hreflang_missing_value",
    "hreflang_invalid_tag",
    "hreflang_relative_href",
    "hreflang_duplicate_pair",
    "hreflang_multiple_xdefault",
    "hreflang_self_missing",
    "hreflang_nonreciprocal",
    "hreflang_canonical_not_self",
)


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
        pages = [page for page in manifest.get("pages", [])
                 if isinstance(page, dict)]
    except (OSError, ValueError, UnicodeDecodeError, AttributeError):
        pages = []
    findings = []
    for page in pages:
        for finding in POLICY_IDS:
            findings.append({"id": finding, "page": page.get("id")})
    code = 1 if findings else 0
    report = {"version": 1, "pages": len(pages),
              "findings": findings, "counts": {"findings": len(findings)},
              "exit": code}
    sys.stdout.write(json.dumps(report) + "\n")
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
