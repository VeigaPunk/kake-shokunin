#!/usr/bin/env python3
"""Frozen forgery: a status-only lookup table, blind to headers."""
import json
import sys

TABLE = {
    200: {"decision": "heuristic", "lifetime": 1000, "heuristic": True},
    404: {"decision": "heuristic", "lifetime": 1000, "heuristic": True},
    500: {"decision": "not-heuristically-cacheable", "lifetime": None, "heuristic": False},
}
try:
    data = json.load(sys.stdin)
    status = data["stored"]["status"]
except Exception:
    sys.stderr.write("invalid_input: unreadable input\n")
    sys.exit(1)
if status not in TABLE:
    sys.stderr.write("invalid_input: status not in the table\n")
    sys.exit(1)
print(json.dumps(TABLE[status]))
sys.exit(0)
