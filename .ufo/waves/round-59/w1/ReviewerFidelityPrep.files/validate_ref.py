#!/usr/bin/env python3
"""Cross-check every 'Quoteable whole: N units / M chars / page-unique' claim in reference.md
against the counter's own measurement of the same string.

An item's block ends at the next line that starts a new numbered item (any prefix, e.g. `20. Step 1 — **`)."""
import importlib.util
import os
import re

HERE = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-59"
REF = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-59/w1/ReviewerFidelityPrep.files/reference.md"
spec = importlib.util.spec_from_file_location("c59qt", os.path.join(HERE, "c59_quote_truth.py"))
qt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qt)

T = {}
for sid in ("S425", "S426"):
    raw = open(os.path.join(HERE, "sources", f"{sid}.html"), encoding="utf-8", newline="").read()
    T[sid] = qt.re.sub(r"\s+", " ", raw)

text = open(REF, encoding="utf-8").read()
lines = text.split("\n")

# group lines into item blocks
blocks, cur = [], None
for ln in lines:
    if re.match(r"^\d+\. ", ln):
        if cur:
            blocks.append(cur)
        cur = [ln]
    elif cur is not None:
        cur.append(ln)
if cur:
    blocks.append(cur)

items = []
for b in blocks:
    joined = "\n".join(b)
    m = re.search(r'\*\*"(.+?)"\*\*', joined)
    if m:
        items.append((m.group(1), joined))

print(f"numbered items with a bold verbatim string: {len(items)}\n")

whole_claims = 0
mismatch = 0
unsupported = 0
for s, b in items:
    u, c = qt.units(s), len(s)
    owners = [sid for sid in ("S425", "S426") if s in T[sid]]
    raw_ok = bool(owners)
    uniq = raw_ok and T[owners[0]].count(s) == 1 and not any(s in T[o] for o in ("S425", "S426") if o != owners[0])
    cm = re.search(r"Quoteable whole: (\d+) units / (\d+) chars / page-unique", b)
    if cm:
        whole_claims += 1
        cu, cc = int(cm.group(1)), int(cm.group(2))
        if (cu, cc) != (u, c):
            print(f"  NUMBER MISMATCH claim={cu}/{cc} actual={u}/{c} :: {s[:70]}")
            mismatch += 1
        if not raw_ok:
            print(f"  CLAIMS WHOLE BUT NOT A RAW SUBSTRING :: {s[:70]}")
            unsupported += 1
        elif not uniq:
            print(f"  CLAIMS WHOLE BUT NOT PAGE-UNIQUE :: {s[:70]}")
            unsupported += 1
        if not (6 <= u <= 25 and c <= 160):
            print(f"  WHOLE CLAIM OVER CEILING {u}u {c}c :: {s[:70]}")
            unsupported += 1
    else:
        # must be explicitly marked as split or over-ceiling
        bl = b.lower()
        marked = ("split" in bl or "over the 25-unit ceiling" in bl or "over the ceiling" in bl
                  or "over both ceilings" in bl or "not page-unique" in bl or "not quotable whole" in bl)
        if not marked:
            print(f"  NO WHOLE-CLAIM AND UNMARKED: u={u} c={c} :: {s[:70]}")
            unsupported += 1

print(f"\n'Quoteable whole' claims checked: {whole_claims}")
print(f"number mismatches: {mismatch}")
print(f"unsupported/over-ceiling/unmarked: {unsupported}")
