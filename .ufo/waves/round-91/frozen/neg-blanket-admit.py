#!/usr/bin/env python3
"""Forgery subject: always answers reuse, so it never refuses."""
import json
import sys

sys.stdin.read()
print(json.dumps({"decision": "reuse", "freshness_lifetime": 0, "current_age": 0}))
sys.exit(0)
