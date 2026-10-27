#!/usr/bin/env python3
"""Where does the full-body variance live? Line diffs vs retained, classified by region."""
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


out = {}
for sid in ("S423", "S424"):
    base = load(os.path.join(ROUND, "sources", f"{sid}.html"))
    win = qt.content_window(base, sid)
    bl = base.split("\n")
    # line start offsets in base
    offs, acc = [], 0
    for line in bl:
        offs.append(acc)
        acc += len(line) + 1
    for i in (1, 2, 3):
        f = load(os.path.join(HERE, f"{sid}.f{i}.html"))
        fl = f.split("\n")
        key = f"{sid}.f{i}"
        info = {"lines_retained": len(bl), "lines_fetch": len(fl),
                "chars_retained": len(base), "chars_fetch": len(f)}
        # longest common prefix / suffix
        p = 0
        while p < min(len(base), len(f)) and base[p] == f[p]:
            p += 1
        s = 0
        while s < min(len(base), len(f)) - p and base[-1 - s] == f[-1 - s]:
            s += 1
        info["common_prefix_chars"] = p
        info["common_suffix_chars"] = s
        info["mid_retained"] = base[p:len(base) - s]
        info["mid_fetch"] = f[p:len(f) - s]
        info["mid_retained_in_article"] = win is not None and win[0] <= p and len(base) - s <= win[1]
        # line-level
        changed = [(n, a, b) for n, (a, b) in enumerate(zip(bl, fl)) if a != b]
        info["line_diff_count"] = len(changed)
        info["line_diff_first"] = [{"line": n + 1, "base_off": offs[n],
                                    "in_article_window": win is not None and win[0] <= offs[n] < win[1],
                                    "base": a[:180], "fetch": b[:180]} for n, a, b in changed[:6]]
        info["line_diffs_all_in_script"] = all("<script" in a or "</script>" in a or re.search(r"[\"']?[A-Za-z_]*(token|Token|_t|ts|nonce|vcode|bdstoken)[\"']?\s*[:=]", a)
                                              for _, a, _ in changed)
        out[key] = info
print(json.dumps(out, ensure_ascii=False, indent=1))
