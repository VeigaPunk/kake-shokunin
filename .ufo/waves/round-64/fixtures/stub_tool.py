#!/usr/bin/env python3
"""The canned-JSON stub tool — the round-63 C2 falsification, as bytes.

This file reproduces the stub class the round-63 wave built (w1/CriticClaims.md
counterexample 2, w1/ExecFrozenSha.md §4b, w1/ReviewerC2Counter.md): a tool
that reads no bytes, prints the frozen case set with derived == expected and
ok: true, and passes c63_quote_tool.py. The round-64 counter c64_quote_tool.py
rejects it by the frozen-sha pin before execution (tool_sha=mismatch). Never
installed as the lane tool; committed only as a control fixture.
"""
import json
import sys

if "--selftest" in sys.argv:
    print(json.dumps({"cases": [
        {"id": "inline_raw_substring", "derived": "raw-substring",
         "expected": "raw-substring", "passed": True},
        {"id": "markup_collapsed_only", "derived": "collapsed-only",
         "expected": "collapsed-only", "passed": True},
        {"id": "absent_everywhere", "derived": "absent",
         "expected": "absent", "passed": True},
        {"id": "s432_real", "derived": "collapsed-only",
         "expected": "collapsed-only", "passed": True}],
        "total": 4, "passed": 4, "ok": True}, sort_keys=True))
sys.exit(0)
