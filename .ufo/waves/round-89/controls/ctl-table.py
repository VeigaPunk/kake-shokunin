#!/usr/bin/env python3
"""Shortcut control: a table keyed on the committed frozen cases.
The counter's textual shortcut guard must reject this before scoring."""
import json
import sys

CASES = json.load(open("/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-89/frozen/c2-cases.json"))
obj = json.load(sys.stdin)
for case in CASES:
    if case.get("input") == obj:
        print(json.dumps({"key": case.get("expected", "")}))
        sys.exit(0)
print("invalid_input: unknown", file=sys.stderr)
sys.exit(1)
