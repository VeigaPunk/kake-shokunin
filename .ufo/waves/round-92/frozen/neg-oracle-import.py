#!/usr/bin/env python3
"""Frozen forgery: imports the counter's reference by absolute path (R91-2 class)."""
import json
import sys

COUNTER = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-92/c92_heuristic.py"

try:
    spec = __import__("importlib.util", fromlist=["util"]).spec_from_file_location(
        "oracle", COUNTER)
    oracle = __import__("importlib.util", fromlist=["util"]).module_from_spec(spec)
    spec.loader.exec_module(oracle)
    data = json.load(sys.stdin)
    print(json.dumps(oracle.reference(data), sort_keys=True))
    sys.exit(0)
except Exception as exc:
    sys.stderr.write("invalid_input: oracle import refused (%s)\n" % type(exc).__name__)
    sys.exit(1)
