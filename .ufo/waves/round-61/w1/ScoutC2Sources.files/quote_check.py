#!/usr/bin/env python3
"""Round-61 S430-S433 quote-span checker (read-only).

Mirrors the accepted round-60 method (.ufo/waves/round-60/w1/ExecSpans.files/spans.py):
  * body   = retained source body with all whitespace collapsed to single spaces
  * segments = text nodes = runs between '>' and '<' (style/script bodies blanked first),
               entities NOT decoded
  * units()  = one unit per CJK char, one per non-CJK whitespace token
A span qualifies iff it is a raw substring of ONE segment (i.e. inside a single text
node), 6..25 units, <=160 chars, and page-unique (exactly one occurrence in the
collapsed body).
"""
import re, sys, hashlib, json, os

SOURCES = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/sources"
CJK_RE = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff65-\uff9f\U00020000-\U0002ffff]")
UNIT_CEILING = 25
CHAR_CEILING = 160

def load(sid):
    with open(f"{SOURCES}/{sid}.html", encoding="utf-8", errors="replace") as f:
        return f.read()

def body(raw):
    return re.sub(r"\s+", " ", raw)

def segments(text):
    chunk = re.sub(r"(?is)<(style|script)\b.*?</\1>", "<>", text)
    return re.findall(r">([^<>]+)(?=<)", chunk)

def units(t):
    return len(CJK_RE.findall(t)) + len([x for x in t.split() if not CJK_RE.search(x)])

def check(sid, span):
    raw = load(sid); b = body(raw); segs = segments(b)
    in_seg = [s for s in segs if span in s]
    occ = b.count(span)
    return {
        "sid": sid, "span": span,
        "units": units(span), "chars": len(span),
        "units_ok": 6 <= units(span) <= UNIT_CEILING,
        "chars_ok": len(span) <= CHAR_CEILING,
        "occurrences_in_body": occ,
        "page_unique": occ == 1,
        "in_single_text_node": len(in_seg) >= 1,
        "nodes_containing": len(in_seg),
    }

def dump(sid, keywords):
    raw = load(sid); b = body(raw); segs = segments(b)
    print(f"===== {sid}: {len(segs)} segments =====")
    for i,s in enumerate(segs):
        if any(k.lower() in s.lower() for k in keywords):
            print(f"[{i}] {units(s):3d}u :: {s}")
    print()

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "dump":
        sid = sys.argv[2]; kws = sys.argv[3:]
        dump(sid, kws)
    elif cmd == "check":
        sid = sys.argv[2]; span = sys.argv[3]
        print(json.dumps(check(sid, span), indent=2))
