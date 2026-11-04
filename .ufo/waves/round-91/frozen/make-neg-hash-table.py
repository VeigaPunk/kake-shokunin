#!/usr/bin/env python3
"""Builds frozen/neg-hash-table.py: a forgery that answers the hand cases from a table."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import c91_reuse  # noqa: E402

rows = {}
for name, inp, expected in c91_reuse.hand_cases():
    key = json.dumps(inp, sort_keys=True)
    rows[key] = expected if expected is not None else "REFUSE"

body = '''#!/usr/bin/env python3
"""Forgery subject: a lookup table over the published hand cases, constant otherwise."""
import json
import sys

TABLE = %s


def main():
    payload = sys.stdin.read()
    try:
        key = json.dumps(json.loads(payload), sort_keys=True)
    except ValueError:
        sys.stderr.write("invalid_input: not JSON\\n")
        return 1
    hit = TABLE.get(key)
    if hit == "REFUSE":
        sys.stderr.write("invalid_input: refused by table\\n")
        return 1
    if hit:
        print(json.dumps(hit))
        return 0
    print(json.dumps({"decision": "reuse", "freshness_lifetime": 0, "current_age": 0}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
''' % json.dumps(rows, indent=0, sort_keys=True)
open(os.path.join(HERE, "neg-hash-table.py"), "w").write(body)
print("rows=%d" % len(rows))
