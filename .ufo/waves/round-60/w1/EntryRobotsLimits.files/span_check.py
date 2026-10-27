#!/usr/bin/env python3
"""Span check for the S429 entry (round 60, seat EntryRobotsLimits).

Every double-quoted span in the entry is checked against the retained body with the round-59
counter's own code (`.ufo/waves/round-59/c59_quote_truth.py`: unit count, article-block text
nodes, substring test), plus the round-60 band 6..25 units / <=160 characters and page-uniqueness
across the three retained bodies (S427, S428, S429). Read-only; writes nothing.

  python3 -B span_check.py            # check the entry as written
"""
import importlib.util, os, re, sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
HERE = os.path.dirname(os.path.abspath(__file__))
ENTRY = os.path.join(HERE, "robots-txt-limits.md")
SRC = os.path.join(LANE, ".ufo/waves/round-60/sources")

spec = importlib.util.spec_from_file_location("c59qt", os.path.join(LANE, ".ufo/waves/round-59/c59_quote_truth.py"))
qt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qt)
SID = "S429"
qt.NEW_ROWS = tuple(qt.NEW_ROWS) + (SID,)
qt.ARTICLE_START = dict(qt.ARTICLE_START); qt.ARTICLE_START[SID] = 'class="devsite-article-body'
qt.ARTICLE_END = dict(qt.ARTICLE_END); qt.ARTICLE_END[SID] = "<devsite-content-footer"


def body(sid):
    with open(os.path.join(SRC, f"{sid}.html"), encoding="utf-8", newline="") as fh:
        return re.sub(r"\s+", " ", fh.read())


def main():
    texts = {s: body(s) for s in ("S427", "S428", "S429")}
    text = texts[SID]
    others = [t for s, t in texts.items() if s != SID]
    entry = open(ENTRY, encoding="utf-8").read()
    head = entry.splitlines()
    bad = 0
    trio = {k: next((i for i, l in enumerate(head[:8]) if l.startswith(k)), None) for k in ("source:", "verified-at:", "recheck:")}
    print("provenance trio in first 8 lines:", trio)
    print("source names row id and URL:", "S429" in head[0] and "https://developers.google.com/search/docs/crawling-indexing/robots/intro" in head[0])
    print("id cited below the header:", "S429" in "\n".join(head[4:]))
    uniq, ok = set(), True
    for n, line in enumerate(entry.splitlines(), 1):
        for span in re.findall(r'"([^"]+)"', line):
            u = qt.units(span)
            in_node = qt.in_content(text, span, SID)
            count = text.count(span)
            elsewhere = sum(t.count(span) for t in others)
            band = 6 <= u <= 25 and len(span) <= 160
            good = in_node and count == 1 and elsewhere == 0 and band
            if not good:
                ok = False
                bad += 1
            else:
                uniq.add(span)
            print(f"L{n:<3} {u:3d}u {len(span):3d}c unique={count == 1 and elsewhere == 0!s:5} "
                  f"node={in_node!s:5} band={band!s:5} {'OK ' if good else 'FAIL'} {span[:70]}")
    print(f"distinct page-unique spans: {len(uniq)} (need >= 3)")
    print("one carries 'cannot enforce':", any("cannot enforce" in s for s in uniq))
    print("curly quotes present:", bool(re.search(r"[\u201c\u201d]", entry)))
    print("ALL SPANS OK" if ok and len(uniq) >= 3 and any("cannot enforce" in s for s in uniq) else "FAILURES")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
