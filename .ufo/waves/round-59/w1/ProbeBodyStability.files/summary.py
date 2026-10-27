#!/usr/bin/env python3
"""ProbeBodyStability part 4 (compact): characterise the varying regions without the noisy opcode dump,
and print the final recheck-span table with the counter's own span_tools verdict.
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

CANDS = {
    "S425": [
        "your logs may show visits from several IP addresses",
        "Therefore, your logs may show visits from several IP addresses.",
        "Google egresses primarily from IP addresses in the United States.",
        "The source IP address of the request.",
    ],
    "S426": [
        "reverse DNS lookup on the accessing IP address from your logs",
        "Run a reverse DNS lookup on the accessing IP address from your logs, using the",
    ],
}


def rl(path):
    with open(path, "rb") as fh:
        return fh.read().decode("utf-8", "replace").split("\n")


def collapsed(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return qt.re.sub(r"\s+", " ", fh.read())


def main():
    for sid in IDS:
        ret = f"{WAVE}/sources/{sid}.html"
        fetches = [f"{SCRATCH}/fetches/{sid}.{n}.html" for n in (1, 2, 3)]
        files = [("retained", ret)] + [(f"f{n}", p) for n, p in zip((1, 2, 3), fetches)]
        lines = {lab: rl(p) for lab, p in files}
        nlines = max(len(v) for v in lines.values())
        varying = [i + 1 for i in range(nlines)
                   if len({(lines[lab][i] if i < len(lines[lab]) else None) for lab, _ in files}) > 1]
        print(f"=== {sid} ===")
        print(f"raw_lines={len(lines['retained'])} varying_lines={varying}")
        # article raw-line bounds (from marker lines)
        start_line = next(i + 1 for i, l in enumerate(lines["retained"]) if 'class="devsite-article-body' in l)
        end_line = next(i + 1 for i, l in enumerate(lines["retained"]) if "<devsite-content-footer" in l)
        print(f"article_raw_lines={start_line}..{end_line}  varying_inside_article="
              f"{[ln for ln in varying if start_line <= ln <= end_line]}")
        # characterise each varying line by tag + a stable classification
        for ln in varying:
            l = lines["retained"][ln - 1]
            tag = re.match(r"\s*<([\w-]+)", l)
            tag = tag.group(1) if tag else "text"
            cls = {
                "analytics-json": "google-analytics dimensions JSON: key order + optional dimension values vary per response",
                "script": "CSP nonce on a <script> tag: fresh per response",
                "text": "devsite boot payload: feature-flag list and experiment-id map, order and membership vary per response",
            }.get(tag, f"<{tag}> line content varies")
            # is it inside <script>/<style>?
            inside_script = "script" in l[:40] or "analytics" in l[:80] or l.lstrip().startswith("'")
            print(f"  line {ln}: tag=<{tag}> len={len(l)} kind={cls}")
        # sha + sizes
        for lab, p in files:
            b = open(p, "rb").read()
            print(f"  {lab}: bytes={len(b)} sha256={hashlib.sha256(b).hexdigest()}")
        # article block equality across all four
        texts = {lab: collapsed(p) for lab, p in files}
        nodes = {lab: [s.strip() for s in qt.text_segments(t, sid)] for lab, t in texts.items()}
        ref = nodes["retained"]
        print(f"  article_text_nodes: " + ", ".join(
            f"{lab}={len(nodes[lab])}" for lab, _ in files))
        print(f"  article nodes identical to retained (order+content): "
              + ", ".join(f"{lab}={nodes[lab] == ref}" for lab, _ in files))
        print("  RECHECK SPAN candidates:")
        for cand in CANDS[sid]:
            hit = {}
            for lab, p in files:
                ls = rl(p)
                hit[lab] = [i + 1 for i, l in enumerate(ls) if cand in l]
            stable = all(len(v) == 1 for v in hit.values())
            same = len({v[0] for v in hit.values() if v}) == 1 if stable else False
            in_article = all(start_line <= v[0] <= end_line for v in hit.values() if v) and stable
            print(f"    {cand!r}")
            print(f"      raw_line_hits={hit} single_line_everywhere={stable} same_line_no={same} inside_article_block={in_article}")
        print()


if __name__ == "__main__":
    main()
