#!/usr/bin/env python3
"""Read-only helper for round-59 entry drafting (Google pages S425, S426): unit counts and page-unique span checks.

Uses the C3 counter's own article-block and text-node code (`c59_quote_truth.py`; bodies are whitespace-collapsed exactly as the counter collapses them), so a span this helper accepts is a span
the counter's C5 substring / block / uniqueness test accepts.

  python3 -B span_tools.py spans S425          # text nodes of the article block (one per line) with units and page-uniqueness
  python3 -B span_tools.py check S425 'span'   # units, chars, in a text node of the block, count in body, unique across both bodies
  python3 -B span_tools.py window S425         # the article block's text nodes joined by newlines
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("c59qt", os.path.join(HERE, "c59_quote_truth.py"))
qt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qt)
IDS = qt.NEW_ROWS


def body(sid):
    with open(os.path.join(HERE, "sources", f"{sid}.html"), encoding="utf-8", newline="") as fh:
        return qt.re.sub(r"\s+", " ", fh.read())


def check(sid, span):
    texts = {s: body(s) for s in IDS}
    count = texts[sid].count(span)
    elsewhere = sum(texts[o].count(span) for o in IDS if o != sid)
    return {"units": qt.units(span), "chars": len(span), "in_text_node": qt.in_content(texts[sid], span, sid),
            "count_in_body": count, "unique": count == 1 and elsewhere == 0,
            "within_ceilings": qt.units(span) <= qt.UNIT_CEILING and len(span) <= qt.CHAR_CEILING}


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("spans", "check", "window") or sys.argv[2] not in IDS:
        sys.exit(__doc__)
    cmd, sid = sys.argv[1], sys.argv[2]
    if cmd == "window":
        print("\n".join(s.strip() for s in qt.text_segments(body(sid), sid) if s.strip()))
    elif cmd == "spans":
        for seg in qt.text_segments(body(sid), sid):
            seg = seg.strip()
            if seg:
                r = check(sid, seg)
                print(f"{r['units']:3d}u {r['chars']:3d}c unique={r['unique']!s:5} {seg}")
    else:
        print(check(sid, sys.argv[3]))


if __name__ == "__main__":
    main()
