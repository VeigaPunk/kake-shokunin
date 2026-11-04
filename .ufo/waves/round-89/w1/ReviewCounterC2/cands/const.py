#!/usr/bin/env python3
"""Shortcut control: one constant key for every request. Must be rejected."""
import json
import sys

json.load(sys.stdin)
print(json.dumps({"key": "k"}))
