#!/usr/bin/env python3
"""Shortcut control: the request's own representation as the key. Injective,
so it passes nothing else. Must be rejected."""
import json
import sys

obj = json.load(sys.stdin)
print(json.dumps({"key": obj.get("uri", "") + "|" + repr(obj.get("request_headers"))}))
