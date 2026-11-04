#!/usr/bin/env python3
"""Shortcut control: a naive join with no escaping, sorting, trimming or
case handling. Must be rejected by the property population."""
import json
import sys

obj = json.load(sys.stdin)
headers = obj.get("request_headers", {})
print(json.dumps({"key": obj.get("uri", "") + ":" + ",".join(
    f"{k}={v}" for k, v in headers.items())}))
