#!/usr/bin/env python3
"""Round-60 article text-node explorer for S427/S428/S429 — same block/text-node logic as c59_quote_truth.py."""
import importlib.util, os, re, sys

QT = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-59/c59_quote_truth.py"
SRC = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-60/sources"
spec = importlib.util.spec_from_file_location("c59qt", QT)
qt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qt)
IDS = ("S427", "S428", "S429")

def body(sid):
    with open(os.path.join(SRC, f"{sid}.html"), encoding="utf-8", newline="") as fh:
        return re.sub(r"\s+", " ", fh.read())

def segments(sid):
    # ARTICLE markers are identical for all three Google pages
    text = body(sid)
    lo = text.find('class="devsite-article-body')
    hi = text.find("<devsite-content-footer", lo + 1) if lo >= 0 else -1
    if not (hi > lo):
        return []
    chunk = re.sub(r"(?is)<(style|script)\b.*?</\1>", "<>", text[lo:hi])
    chunk = re.sub(r"(?is)<(aside|nav|devsite-feedback|devsite-thumb-rating)\b.*?</\1>", "<>", chunk)
    return re.findall(r">([^<>]+)(?=<)", chunk)

def main():
    sid = sys.argv[2]
    assert sid in IDS
    if sys.argv[1] == "spans":
        texts = {s: body(s) for s in IDS}
        segs = {s: [t.strip() for t in segments(s) if t.strip()] for s in IDS}
        for seg in segs[sid]:
            u = qt.units(seg)
            cnt = texts[sid].count(seg)
            elsew = sum(texts[o].count(seg) for o in IDS if o != sid)
            uniq = cnt == 1 and elsew == 0
            print(f"{u:3d}u {len(seg):3d}c uniq={uniq!s:5} n={cnt} {seg}")
    elif sys.argv[1] == "check":
        texts = {s: body(s) for s in IDS}
        span = sys.argv[3]
        in_node = any(span in t for t in segments(sid))
        cnt = texts[sid].count(span)
        elsew = sum(texts[o].count(span) for o in IDS if o != sid)
        print({"units": qt.units(span), "chars": len(span), "in_node": in_node,
               "count": cnt, "elsewhere": elsew, "unique": cnt == 1 and elsew == 0})
    elif sys.argv[1] == "grep":
        pat = sys.argv[3].lower()
        for seg in segments(sid):
            if pat in seg.lower():
                print(seg.strip())

if __name__ == "__main__":
    main()
