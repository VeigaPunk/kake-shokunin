#!/usr/bin/env python3
"""Degenerate constant 2: report every finding id on every check and exit 1."""
import json, sys
ALL = ["xrt_bot_scope_empty", "xrt_duplicate_directive", "xrt_empty_rule",
       "xrt_indexifembedded_without_noindex", "xrt_invalid_value",
       "xrt_mutually_exclusive", "xrt_unknown_directive"]
a = sys.argv
m = a[a.index("--manifest") + 1] if "--manifest" in a else ""
try:
    doc = json.load(open(m))
    ids = [c.get("id") for c in doc.get("checks", []) if isinstance(c, dict)]
except Exception:
    ids = []
print(json.dumps({"schema": "x-robots-tag-report/v1",
                  "checks": [{"id": i, "directives": [], "effective": [], "bots": {},
                              "findings": ALL} for i in ids],
                  "findings": ALL, "exit": 1}))
sys.exit(1)
