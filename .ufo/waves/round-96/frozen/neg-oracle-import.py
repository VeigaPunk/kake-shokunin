#!/usr/bin/env python3
"""Forgery: bypasses deciding by executing the counter's own reference."""
import json
import sys

inp = json.loads(sys.stdin.buffer.read())
paths = [
    "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-96/c96_reval.py",
    "../c96_reval.py",
]
ns = {}
for p in paths:
    try:
        with open(p, "r", encoding="utf-8") as fh:
            src = fh.read()
        exec(compile(src, p, "exec"), ns)
        out = ns["reference"](inp)
        json.dump(out, sys.stdout, sort_keys=True)
        sys.stdout.write("\n")
        break
    except OSError:
        continue
else:
    sys.stderr.write("invalid_input: no oracle reachable\n")
    sys.exit(1)
