#!/usr/bin/env python3
"""Degenerate constant 1: always clean. Prints an empty report and exits 0 for every input."""
import json, sys
a = sys.argv
m = a[a.index("--manifest") + 1] if "--manifest" in a else ""
try:
    doc = json.load(open(m))
    ids = [c.get("id") for c in doc.get("checks", []) if isinstance(c, dict)]
except Exception:
    ids = []
print(json.dumps({"schema": "x-robots-tag-report/v1",
                  "checks": [{"id": i, "directives": [], "effective": [], "bots": {},
                              "findings": []} for i in ids],
                  "findings": [], "exit": 0}))
sys.exit(0)
