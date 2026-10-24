#!/usr/bin/env python3
"""Round-41 control (constant family): every check is at once an error check
`check_invalid` and carries `loc_not_absolute` for entries 1 to 128.

Both constant signals at once, so that a counter reading either field alone
still sees "invalid" everywhere. No URL character, component, scheme or host is
judged.
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
    items = []
    for check in checks:
        ident = check.get("id") if isinstance(check, dict) else None
        items.append({"id": ident if isinstance(ident, str) else None,
                      "status": "error", "error": "check_invalid",
                      "findings": [{"code": "loc_not_absolute", "entry": index}
                                   for index in range(1, ENTRIES + 1)]})
    sys.stdout.write(json.dumps({"version": 1, "verdict": "could-not-evaluate",
                                 "checks": items}, ensure_ascii=True) + "\n")
    sys.stdout.flush()
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
