#!/usr/bin/env python3
"""Round-41 control (constant family): every entry of every check is reported as
`loc_not_absolute`.

No URL character, component, scheme or host is judged. Entry numbers 1 to 128
cover every entry any case file can hold (the counter writes at most 60 entries
per file; its shared file holds one).
"""

import json
import sys

ENTRIES = 128


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
    findings = [{"code": "loc_not_absolute", "entry": index}
                for index in range(1, ENTRIES + 1)]
    items = []
    for check in checks:
        ident = check.get("id") if isinstance(check, dict) else None
        items.append({"id": ident if isinstance(ident, str) else None,
                      "status": "findings", "error": None,
                      "findings": [dict(item) for item in findings]})
    sys.stdout.write(json.dumps({"version": 1, "verdict": "failed-policy",
                                 "checks": items}, ensure_ascii=True) + "\n")
    sys.stdout.flush()
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
