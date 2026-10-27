#!/usr/bin/env python3
"""Read-only helper for round-60 row/gate drafting (retained bodies S427, S428, S429).

Reuses the round-59 counter's own text-node, article-block and unit code by importing it
read-only from .ufo/waves/round-59/c59_quote_truth.py and extending only its two id-keyed
maps (ARTICLE_START / ARTICLE_END) to the round-60 ids. Nothing is written outside stdout.

  python3 -B span60.py headings S427
  python3 -B span60.py spans S427 [grep-substring]
  python3 -B span60.py check S427 '<span>'
"""
import importlib.util
import os
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
R59 = os.path.join(LANE, ".ufo/waves/round-59/c59_quote_truth.py")
SRC = os.path.join(LANE, ".ufo/waves/round-60/sources")
IDS = ("S427", "S428", "S429")

spec = importlib.util.spec_from_file_location("c59qt", R59)
qt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qt)

for sid in IDS:
    qt.ARTICLE_START[sid] = 'class="devsite-article-body'
    qt.ARTICLE_END[sid] = "<devsite-content-footer"
qt.NEW_ROWS = IDS


def body(sid):
    with open(os.path.join(SRC, f"{sid}.html"), encoding="utf-8", newline="") as fh:
        return re.sub(r"\s+", " ", fh.read())


def check(sid, span):
    texts = {s: body(s) for s in IDS}
    count = texts[sid].count(span)
    elsewhere = sum(texts[o].count(span) for o in IDS if o != sid)
    return {
        "units": qt.units(span),
        "chars": len(span),
        "in_text_node": qt.in_content(texts[sid], span, sid),
        "count_in_body": count,
        "page_unique": count == 1 and elsewhere == 0,
        "within_ceilings": 6 <= qt.units(span) <= qt.UNIT_CEILING and len(span) <= qt.CHAR_CEILING,
    }


def main():
    if len(sys.argv) < 3 or sys.argv[2] not in IDS:
        sys.exit(__doc__)
    cmd, sid = sys.argv[1], sys.argv[2]
    if cmd == "headings":
        for h in qt.article_headings(body(sid), sid):
            print(f"{qt.units(h):3d}u {h}")
    elif cmd == "spans":
        needle = sys.argv[3] if len(sys.argv) > 3 else ""
        for seg in qt.text_segments(body(sid), sid):
            seg = seg.strip()
            if seg and needle in seg:
                r = check(sid, seg)
                print(f"{r['units']:3d}u {r['chars']:3d}c unique={r['page_unique']!s:5} {seg}")
    elif cmd == "check":
        print(check(sid, sys.argv[3]))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
