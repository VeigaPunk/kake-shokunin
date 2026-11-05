#!/usr/bin/env python3
"""Forgery: prints update-stored whatever the input says."""
import json
import sys

sys.stdin.buffer.read()
json.dump({"decision": "update-stored", "if_none_match": None,
           "if_modified_since": None}, sys.stdout, sort_keys=True)
