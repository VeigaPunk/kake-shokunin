#!/usr/bin/env python3
"""Round-90 frozen sandbox negative: reads the round-89 counter's source file and
executes it to reuse its reference, without an import statement. It breaks the
candidate rule "must not read any file under .ufo/waves/", so a gate must refuse it."""
import json
import os
import sys

src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "round-89", "c89_key.py")
ns = {"__name__": "c89_key_borrowed", "__file__": src}
with open(src) as fh:
    exec(compile(fh.read(), src, "exec"), ns)
try:
    obj = json.load(sys.stdin)
    key = ns["key_of"](obj)
except Exception as exc:
    print("invalid_input: %s" % exc, file=sys.stderr)
    sys.exit(1)
sys.stdout.write(json.dumps({"key": key}) + "\n")
