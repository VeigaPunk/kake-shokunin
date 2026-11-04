#!/usr/bin/env python3
"""C2 constant 2: a report-every-id printer.

Same CLI as scripts/sitemap_audit.py (`--manifest <path>`).  For every check it
reports one finding per known finding id and exits 1.  It must be counted as a
failed constant by c77_sitemap_matrix.py: it cannot pass a clean case (exit 0)
and its id set matches no case.
"""

import json
import os
import sys

EXIT_USAGE = 64
EXIT_FINDINGS = 1

IDS = (
    # round-39 XML ids
    "too_large",
    "encoding_invalid",
    "doctype_present",
    "xml_malformed",
    "root_invalid",
    "no_entries",
    "too_many_entries",
    "element_unexpected",
    "loc_missing",
    "loc_repeated",
    "loc_not_absolute",
    "loc_out_of_scope",
    "loc_too_long",
    "lastmod_invalid",
    "changefreq_invalid",
    "priority_invalid",
    "field_repeated",
    # round-77 container/format ids
    "text_line_not_url",
    "text_url_not_absolute",
    "text_empty",
    "text_too_many_entries",
    "feed_item_missing_link",
    "format_unsupported",
)


def _ids(manifest_path):
    try:
        with open(manifest_path, "rb") as handle:
            document = json.loads(handle.read().decode("utf-8"))
        checks = document.get("checks")
        if not isinstance(checks, list):
            return []
        return [check.get("id") if isinstance(check, dict) else None for check in checks]
    except (OSError, ValueError, UnicodeDecodeError):
        return []


def main(argv):
    if len(argv) != 3 or argv[1] != "--manifest":
        return EXIT_USAGE
    items = [
        {
            "id": ident,
            "status": "findings",
            "error": None,
            "findings": [{"code": code, "entry": 1} for code in IDS],
        }
        for ident in _ids(os.path.abspath(argv[2]))
    ]
    sys.stdout.write(
        json.dumps({"version": 1, "verdict": "failed-policy", "checks": items}, ensure_ascii=True) + "\n"
    )
    return EXIT_FINDINGS


if __name__ == "__main__":
    sys.exit(main(sys.argv))
