#!/usr/bin/env python3
"""Gate-quote candidates for one retained body.

Given the collapsed text stream of a body and a phrase to stand near, propose the
longest spans (6..25 whitespace units, <=160 chars, printable ASCII, no ASCII
double quote inside) that occur exactly once, so a lesson Gate line can quote the
located anchor material without escaping. Read-only.
"""
from __future__ import annotations

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("rel", os.path.join(HERE, "relocate.py"))
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)

MIN_UNITS, MAX_UNITS, MAX_CHARS = 6, 25, 160


def ok(span: str, streamed: str) -> bool:
    if not (MIN_UNITS <= len(span.split()) <= MAX_UNITS):
        return False
    if len(span) > MAX_CHARS or '"' in span:
        return False
    if any(ord(c) > 126 or ord(c) < 32 for c in span):
        return False
    return streamed.count(span) == 1


def candidates(body, kind, anchor_phrase, limit=6):
    text = r.decode(body)
    streamed = r.stream(text, kind)
    needle = " ".join(anchor_phrase.split())
    at = streamed.find(needle)
    if at < 0:
        return []
    heads = r.stream_headings(streamed)
    head = r.enclosing_heading(heads, at)
    win = streamed[at:at + 900]
    found = []
    for start in range(0, min(len(win) - 1, 120)):
        if start and win[start - 1] != " ":
            continue
        for end in range(len(win), start, -1):
            span = win[start:end].strip()
            if len(span) > MAX_CHARS:
                continue
            if ok(span, streamed):
                if not any(span in f["span"] for f in found):
                    found.append({"span": span, "units": len(span.split()),
                                  "chars": len(span), "heading": head})
                break
        if len(found) >= limit:
            break
    return found


if __name__ == "__main__":
    body, kind, phrase = sys.argv[1], sys.argv[2], sys.argv[3]
    for c in candidates(body, kind, phrase):
        print(f'{c["units"]:2}u {c["chars"]:3}c | {c["span"]}')
