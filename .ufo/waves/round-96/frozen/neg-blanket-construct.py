#!/usr/bin/env python3
"""Forgery: prints the construct decision whatever the input says."""
import json
import sys

sys.stdin.buffer.read()
json.dump({"decision": "construct", "if_none_match": '"v1"',
           "if_modified_since": 500}, sys.stdout, sort_keys=True)
sys.stdout.write("\n")
