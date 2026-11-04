#!/usr/bin/env python3
"""Degenerate constant 4: one regex over the joined header values, three directives only."""
import json, re, sys
a = sys.argv
p = a[a.index("--manifest") + 1] if "--manifest" in a else ""
try:
    doc = json.load(open(p))
    checks = []
    for c in doc.get("checks", []):
        vals = " ".join(str(h.get("value", "")) for h in c.get("headers", [])
                        if str(h.get("name", "")).lower() == "x-robots-tag")
        toks = sorted(set(m.group(1).lower() for m in re.finditer(r"(noindex|nofollow|nosnippet)", vals, re.I)))
        checks.append({"id": c.get("id"), "directives": toks, "effective": toks, "bots": {},
                       "findings": []})
except Exception:
    print(json.dumps({"schema": "x-robots-tag-report/v1", "error": {"id": "xrt_input_bad_json", "detail": "x"}, "exit": 2})); sys.exit(2)
print(json.dumps({"schema": "x-robots-tag-report/v1", "checks": checks, "findings": [], "exit": 0}))
sys.exit(0)
