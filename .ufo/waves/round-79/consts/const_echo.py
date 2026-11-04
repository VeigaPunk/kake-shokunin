#!/usr/bin/env python3
"""Degenerate constant 3: echo the comma-separated tokens, no expansion, no effective set."""
import json, sys
a = sys.argv
p = a[a.index("--manifest") + 1] if "--manifest" in a else ""
try:
    doc = json.load(open(p))
    if doc.get("schema") != "x-robots-tag-manifest/v1":
        raise ValueError("schema")
    checks = []
    for c in doc["checks"]:
        if not isinstance(c.get("headers"), list):
            raise TypeError("shape")
        toks = []
        for h in c["headers"]:
            if str(h.get("name", "")).lower() == "x-robots-tag":
                toks += [t.strip().lower() for t in str(h.get("value", "")).split(",") if t.strip()]
        checks.append({"id": c["id"], "directives": sorted(toks), "effective": sorted(toks),
                       "bots": {}, "findings": []})
    ids = [c["id"] for c in checks]
    if len(ids) != len(set(ids)):
        raise ValueError("dup")
except FileNotFoundError:
    print(json.dumps({"schema": "x-robots-tag-report/v1", "error": {"id": "xrt_input_unreadable", "detail": "x"}, "exit": 2})); sys.exit(2)
except TypeError:
    print(json.dumps({"schema": "x-robots-tag-report/v1", "error": {"id": "xrt_input_check_shape", "detail": "x"}, "exit": 2})); sys.exit(2)
except ValueError as e:
    eid = "xrt_input_bad_json" if not isinstance(e.args[0], str) or e.args[0] != "dup" else "xrt_input_duplicate_id"
    print(json.dumps({"schema": "x-robots-tag-report/v1", "error": {"id": eid, "detail": str(e)}, "exit": 2})); sys.exit(2)
except Exception:
    print(json.dumps({"schema": "x-robots-tag-report/v1", "error": {"id": "xrt_input_bad_json", "detail": "x"}, "exit": 2})); sys.exit(2)
print(json.dumps({"schema": "x-robots-tag-report/v1", "checks": checks, "findings": [], "exit": 0}))
sys.exit(0)
