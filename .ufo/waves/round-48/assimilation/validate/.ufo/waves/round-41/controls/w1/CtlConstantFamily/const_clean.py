#!/usr/bin/env python3
"""Round-41 control (constant family): every manifest check is reported clean.

No URL character, component, scheme or host is judged. The manifest is read only
to echo one item per check (the counter needs the item count and order).
"""

import json
import sys


def main(argv):
    if len(argv) != 3 or argv[1] != "--manifest":
        return 64
    try:
        with open(argv[2], "rb") as handle:
            document = json.loads(handle.read().decode("utf-8"))
        checks = document["checks"]
        if document.get("version") != 1 or not isinstance(checks, list) or not checks:
            raise ValueError("manifest")
    except Exception:
        sys.stdout.write(json.dumps({"version": 1, "verdict": "could-not-evaluate",
                                     "error": "input_invalid", "checks": []}) + "\n")
        return 2
    items = []
    for check in checks:
        ident = check.get("id") if isinstance(check, dict) else None
        items.append({"id": ident if isinstance(ident, str) else None,
                      "status": "clean", "error": None, "findings": []})
    sys.stdout.write(json.dumps({"version": 1, "verdict": "clean", "checks": items},
                                ensure_ascii=True) + "\n")
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
