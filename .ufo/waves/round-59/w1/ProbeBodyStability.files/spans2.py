#!/usr/bin/env python3
"""ProbeBodyStability part 3: (1) exact varying substring inside the boot-script line 2078/2007;
(2) line-break stability of the article region across fetches (does the same candidate span sit on a
single raw line in every fetch, so a plain `grep -F` recheck works?);
(3) validate candidates through the counter's own span_tools.check.
"""
from __future__ import annotations

import difflib
import importlib.util
import re
import subprocess

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
WAVE = f"{LANE}/.ufo/waves/round-59"
SCRATCH = "/fast/scratch/hyaku/kake-r59/ProbeBodyStability"

spec = importlib.util.spec_from_file_location("c59qt", f"{WAVE}/c59_quote_truth.py")
qt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qt)
IDS = qt.NEW_ROWS

CANDS = {
    "S425": [
        "Therefore, your logs may show visits from several IP addresses.",
        "your logs may show visits from several IP addresses",
        "Google egresses primarily from IP addresses in the United States.",
        "The source IP address of the request.",
    ],
    "S426": [
        "Run a reverse DNS lookup on the accessing IP address from your logs, using the",
        "reverse DNS lookup on the accessing IP address from your logs",
    ],
}


def raw_lines(path):
    with open(path, "rb") as fh:
        return fh.read().decode("utf-8", "replace").split("\n")


def main():
    for sid in IDS:
        ret = f"{WAVE}/sources/{sid}.html"
        fetches = [f"{SCRATCH}/fetches/{sid}.{n}.html" for n in (1, 2, 3)]
        print(f"=== {sid} ===")
        # 1. exact varying substring in the big boot line
        boot_no = {"S425": 2078, "S426": 2007}[sid]
        a = raw_lines(ret)[boot_no - 1]
        for n, p in zip((1, 2, 3), fetches):
            b = raw_lines(p)[boot_no - 1]
            sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
            for tag, i1, i2, j1, j2 in sm.get_opcodes():
                if tag != "equal":
                    print(f"  boot line {boot_no} vs fetch{n}: {tag} retained[{i1}:{i2}]={a[i1:i2][:120]!r} fetch={b[j1:j2][:120]!r}")
        # 2. line-break stability: same candidate on a single line in every body?
        print("  -- candidate single-line containment (grep -F-able per raw line) --")
        all_files = [("retained", ret)] + [(f"f{n}", p) for n, p in zip((1, 2, 3), fetches)]
        for cand in CANDS[sid]:
            hits = []
            for label, path in all_files:
                ls = raw_lines(path)
                hit_lines = [i + 1 for i, l in enumerate(ls) if cand in l]
                hits.append((label, hit_lines))
            stable = all(len(h[1]) == 1 for h in hits)
            same_line = len({h[1][0] for h in hits if h[1]}) == 1 if stable else False
            print(f"    {'STABLE' if stable else 'UNSTABLE'} same_line_number={same_line} {cand!r}")
            for label, hl in hits:
                print(f"        {label}: lines {hl}")
        # 3. counter-side check on the retained body
        print("  -- span_tools.check (counter's own test) --")
        for cand in CANDS[sid]:
            r = subprocess.run(["python3", "-B", f"{WAVE}/span_tools.py", "check", sid, cand],
                               capture_output=True, text=True)
            print(f"    {cand!r} -> {r.stdout.strip()} {r.stderr.strip()}")


if __name__ == "__main__":
    main()
