#!/usr/bin/env python3
import json, sys
d = json.loads(sys.stdin.read())
try:
    st = max(0, int(d["current_age"]) - int(d["freshness_lifetime"]))
except Exception:
    st = 0
print(json.dumps({"decision": "revalidate", "staleness": st}))
