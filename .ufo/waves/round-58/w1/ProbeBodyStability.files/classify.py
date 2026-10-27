#!/usr/bin/env python3
"""Classify every differing line region: script blocks vs trailing recommendation list vs article block."""
import difflib
import hashlib
import importlib.util
import json
import os
import re

ROUND = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-58"
HERE = "/fast/scratch/hyaku/kake-r58/ProbeBodyStability"
spec = importlib.util.spec_from_file_location("c58qt", os.path.join(ROUND, "c58_quote_truth.py"))
qt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qt)


def load(p):
    with open(p, encoding="utf-8", newline="") as fh:
        return fh.read()


def script_spans(text):
    return [(m.start(), m.end()) for m in re.finditer(r"(?is)<script\b.*?</script>", text)]


def in_spans(off, spans):
    return any(a <= off < b for a, b in spans)


res = {}
for sid in ("S423", "S424"):
    base = load(os.path.join(ROUND, "sources", f"{sid}.html"))
    win = qt.content_window(base, sid)
    end_marker = qt.ARTICLE_END[sid]
    bl = base.split("\n")
    offs, acc = [], 0
    for line in bl:
        offs.append(acc)
        acc += len(line) + 1
    base_spans = script_spans(base)
    res[sid] = {"article_window": win, "raw_block_sha256": hashlib.sha256(
        base[win[0]:win[1]].encode("utf-8")).hexdigest()}
    for i in (1, 2, 3):
        f = load(os.path.join(HERE, f"{sid}.f{i}.html"))
        fl = f.split("\n")
        sm = difflib.SequenceMatcher(None, bl, fl, autojunk=False)
        regions = []
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                continue
            lo = offs[i1] if i1 < len(offs) else len(base)
            hi = offs[i2] if i2 < len(offs) else len(base)
            inside_article = win[0] <= lo < win[1] or win[0] < hi <= win[1]
            all_script = i2 > i1 and all(in_spans(offs[n], base_spans) for n in range(i1, i2))
            after_end = lo >= win[1]
            regions.append({"op": tag, "base_lines": [i1 + 1, i2], "fetch_lines": [j1 + 1, j2],
                            "base_off": [lo, hi], "inside_article_block": inside_article,
                            "every_base_line_in_script": all_script, "starts_after_article_end": after_end,
                            "sample_base": [l.strip()[:110] for l in bl[i1:i2]][:3],
                            "sample_fetch": [l.strip()[:110] for l in fl[j1:j2]][:3]})
        # article text nodes identical?
        tb = [s.strip() for s in qt.text_segments(base, sid) if s.strip()]
        tf = [s.strip() for s in qt.text_segments(f, sid) if s.strip()]
        res[sid][f"f{i}"] = {
            "regions": regions,
            "regions_inside_article": sum(1 for r in regions if r["inside_article_block"]),
            "regions_all_in_script": sum(1 for r in regions if r["every_base_line_in_script"]),
            "regions_after_article_end": sum(1 for r in regions if r["starts_after_article_end"]),
            "article_nodes_identical": tb == tf,
            "raw_block_equal": hashlib.sha256(f[win[0]:win[1]].encode("utf-8")).hexdigest() == res[sid]["raw_block_sha256"],
        }
print(json.dumps(res, ensure_ascii=False, indent=1))
