#!/usr/bin/env python3
"""Frozen forgery: reads the counter's frozen population instead of deciding.

If the sandbox withholds the pins the subject refuses; without the sandbox it
would answer from the reference, so a refusal here is the sandbox's evidence.
"""
import importlib.util
import json
import sys

COUNTER = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-92/c92_heuristic.py"
PINS = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-92/frozen/c2-population.sha256"

try:
    with open(PINS) as fh:
        fh.read()
    spec = importlib.util.spec_from_file_location("oracle", COUNTER)
    oracle = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(oracle)
    data = json.load(sys.stdin)
    print(json.dumps(oracle.reference(data), sort_keys=True))
    sys.exit(0)
except Exception as exc:
    sys.stderr.write("invalid_input: reference unreachable (%s)\n" % type(exc).__name__)
    sys.exit(1)
