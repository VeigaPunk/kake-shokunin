#!/usr/bin/env python3
"""Occurrence dump for one retained body: every hit of a probe in the collapsed
text stream, with its enclosing heading and local context; plus the units/chars
of the probe under the lane unit rule (whitespace tokens, CJK-aware)."""
from __future__ import annotations

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("rel", os.path.join(HERE, "relocate.py"))
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


def show(body, kind, probes, ctx=110):
    text = r.decode(body)
    streamed = r.stream(text, kind)
    heads = r.stream_headings(streamed)
    print(f"# {os.path.basename(body)} kind={kind} bytes={len(text.encode('utf-8','replace'))} stream={len(streamed)}")
    for probe in probes:
        needle = " ".join(probe.split())
        count = streamed.count(needle)
        print(f"\n## probe {needle!r} units={len(needle.split())} chars={len(needle)} count={count}")
        start = 0
        for n in range(min(count, 6)):
            off = streamed.find(needle, start)
            start = off + 1
            head = r.enclosing_heading(heads, off)
            lo, hi = max(0, off - ctx), min(len(streamed), off + len(needle) + ctx)
            print(f"  @{off} head={head!r}")
            print(f"    ...{streamed[lo:hi]}...")


if __name__ == "__main__":
    body, kind = sys.argv[1], sys.argv[2]
    show(body, kind, sys.argv[3:])
