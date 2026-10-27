#!/usr/bin/env python3
"""ProbeBodyStability part 2: locate the exact varying regions (raw-file line numbers) and pick a
recheck grep span per page that (a) lies in ONE article text node, (b) appears on a SINGLE raw line of
the retained body (no source line break crossed), (c) is stable across all 3 fresh fetches,
(d) is page-unique, (e) carries the row's TOPIC word.
"""
from __future__ import annotations

import difflib
import hashlib
import importlib.util
import re

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
WAVE = f"{LANE}/.ufo/waves/round-59"
SCRATCH = "/fast/scratch/hyaku/kake-r59/ProbeBodyStability"

spec = importlib.util.spec_from_file_location("c59qt", f"{WAVE}/c59_quote_truth.py")
qt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qt)

IDS = qt.NEW_ROWS


def raw(path):
    with open(path, "rb") as fh:
        return fh.read()


def collapsed(path):
    return qt.re.sub(r"\s+", " ", raw(path).decode("utf-8", "replace"))


def lines_of(path):
    return raw(path).decode("utf-8", "replace").split("\n")


def main():
    for sid in IDS:
        ret = f"{WAVE}/sources/{sid}.html"
        fetches = [f"{SCRATCH}/fetches/{sid}.{n}.html" for n in (1, 2, 3)]
        print(f"=== {sid} ===")
        rl = lines_of(ret)
        fl = [lines_of(p) for p in fetches]
        # which raw lines differ among {retained, f1, f2, f3}?
        nlines = max(len(x) for x in [rl] + fl)
        varying = []
        for i in range(nlines):
            vals = set()
            for lst in [rl] + fl:
                vals.add(lst[i] if i < len(lst) else None)
            if len(vals) > 1:
                varying.append(i + 1)
        print(f"raw lines total={len(rl)} varying_line_numbers={varying}")
        for ln in varying:
            samples = []
            for label, lst in (("retained", rl), ("f1", fl[0]), ("f2", fl[1]), ("f3", fl[2])):
                v = lst[ln - 1] if ln - 1 < len(lst) else None
                samples.append((label, v))
            # classify
            stripped = {label: (v or "").strip() for label, v in samples}
            prefix = re.match(r"\s*<(\w[\w-]*)", stripped["retained"] or "")
            print(f"  line {ln} tag={(prefix.group(1) if prefix else '?')} len_retained={len(stripped['retained'])}")
            for label, v in samples:
                print(f"    {label}: {v[:150]!r}")
        # article block raw-line span
        ctext = collapsed(ret)
        win = qt.content_window(ctext, sid)
        # find raw line numbers of the article block by locating the marker text in raw
        start_marker = 'class="devsite-article-body'
        end_marker = "<devsite-content-footer"
        rawtext = raw(ret).decode("utf-8", "replace")
        # map collapsed offsets back is tricky; instead find raw lines containing the markers
        start_line = next((i + 1 for i, l in enumerate(rl) if start_marker in l), None)
        end_line = next((i + 1 for i, l in enumerate(rl) if end_marker in l), None)
        print(f"  article markers: start_line={start_line} end_line={end_line}")
        print(f"  article raw lines containing any variance: "
              f"{[ln for ln in varying if start_line and end_line and start_line <= ln <= end_line]}")
        # candidate recheck spans
        topic = qt.TOPIC[sid]
        nodes = [s.strip() for s in qt.text_segments(ctext, sid)]
        fetch_texts = {n: collapsed(p) for n, p in zip((1, 2, 3), fetches)}
        other = [collapsed(f"{WAVE}/sources/{o}.html") for o in IDS if o != sid]
        cands = []
        for idx, node in enumerate(nodes):
            if topic.lower() not in node.lower():
                continue
            # every line of the retained raw file that contains this node's text (nodes are collapsed)
            # find candidates: substrings of the node that lie within one raw line
            for line_no, line in enumerate(rl, 1):
                if not (start_line and start_line <= line_no <= (end_line or len(rl))):
                    continue
                # raw line -> collapsed segment; a node may be split across raw lines; find the portion
                # of the node that is fully inside this raw line
                for m in re.finditer(r"[^<>]+", line):
                    frag = qt.re.sub(r"\s+", " ", m.group(0)).strip()
                    if not frag or topic.lower() not in frag.lower():
                        continue
                    cands.append((idx, line_no, frag))
        seen = set()
        picked = []
        for idx, line_no, frag in cands:
            key = (idx, line_no, frag)
            if key in seen:
                continue
            seen.add(key)
            units = qt.units(frag)
            if units < 6 or units > qt.UNIT_CEILING or len(frag) > qt.CHAR_CEILING:
                continue
            # stable across all fetches: present as substring in each collapsed fetch body
            stable = all(frag in t for t in fetch_texts.values())
            # in the retained article block as one text node
            in_node = any(frag in n for n in nodes)
            # page-unique: count in retained body ==1 and 0 in the other page
            cnt = ctext.count(frag)
            elsewhere = sum(o.count(frag) for o in other)
            unique = cnt == 1 and elsewhere == 0
            if stable and in_node and unique:
                picked.append((units, len(frag), line_no, frag))
        picked.sort(key=lambda x: (-x[0], x[1]))
        print(f"  candidate recheck spans (topic={topic!r}, stable in all 3 fetches, page-unique, single raw line):")
        for units, chars, line_no, frag in picked[:12]:
            print(f"    line {line_no} {units}u {chars}c {frag!r}")
        if not picked:
            print("    NONE")


if __name__ == "__main__":
    main()
