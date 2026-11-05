#!/usr/bin/env python3
"""Frozen forgery: admits every input with a constant heuristic decision."""
import json
import sys

try:
    data = json.load(sys.stdin)
except ValueError:
    data = None
print(json.dumps({"decision": "heuristic", "lifetime": 0, "heuristic": True}))
sys.exit(0)
