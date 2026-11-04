#!/usr/bin/env python3
"""C2 constant 1: an always-clean printer.

Same CLI as scripts/sitemap_audit.py (`--manifest <path>`).  It reads the
manifest only to name the checks it invents, prints a clean verdict and exits
0 for every input.  It must be counted as a failed constant by
c77_sitemap_matrix.py: it cannot pass a case whose expected exit is 1 or 2.
"""

import json
import os
import sys

EXIT_USAGE = 64


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
        {"id": ident, "status": "clean", "error": None, "findings": []}
        for ident in _ids(os.path.abspath(argv[2]))
    ]
    sys.stdout.write(
        json.dumps({"version": 1, "verdict": "clean", "checks": items}, ensure_ascii=True) + "\n"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
