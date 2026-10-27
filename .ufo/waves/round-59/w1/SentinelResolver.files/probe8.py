#!/usr/bin/env python3
"""SentinelResolver probe 8: race the REAL base tool (not a replica) against a symlink swap."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import threading
import time

SCRATCH = "/fast/scratch/hyaku/kake-r59/SentinelResolver"
TOOL = os.path.join(SCRATCH, "id_resolver_base.py")
WORK = os.path.join(SCRATCH, "work8")
HDR = "| id | name | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"


def put(base, rel, text):
    p = os.path.join(base, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def main():
    shutil.rmtree(WORK, ignore_errors=True)
    os.makedirs(WORK)
    base = os.path.join(WORK, "race")
    fleet = os.path.join(base, "fleet")
    lp = os.path.join(fleet, "kake-shokunin")
    put(lp, "corpus/SOURCES.md", "## Registry\n\n" + HDR + "| S100 | x | docs | A | s | a | t | mined | 2026-10-26 | 90d | x |\n")
    put(lp, "corpus/knowledge/ok.md", "Cites S100.\n")
    # many filler files widen the walk, so a swap has many chances to land in the window
    for i in range(200):
        put(lp, f"corpus/knowledge/f{i:03d}.md", f"Cites S100.\n" * 20)
    outside = os.path.join(base, "outside")
    put(outside, "outside.md", "Cites S1400.\n")
    inside_t = os.path.join(lp, "corpus", "knowledge", "ok.md")
    outside_t = os.path.join(outside, "outside.md")
    link = os.path.join(lp, "corpus", "knowledge", "race.md")
    os.symlink(inside_t, link)

    stop = threading.Event()

    def flipper():
        while not stop.is_set():
            for tgt in (inside_t, outside_t):
                tmp = link + ".tmp"
                try:
                    if os.path.lexists(tmp):
                        os.unlink(tmp)
                    os.symlink(tgt, tmp)
                    os.replace(tmp, link)
                except OSError:
                    pass

    t = threading.Thread(target=flipper, daemon=True)
    t.start()
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["LC_ALL"] = "C.UTF-8"
    leaks = 0
    runs = 120
    sample = ""
    for _ in range(runs):
        p = subprocess.run([sys.executable, "-B", TOOL, "--root", lp, "--fleet", fleet],
                           capture_output=True, env=env, timeout=60)
        text = p.stdout.decode() + p.stderr.decode()
        if "S1400" in text:
            leaks += 1
            if not sample:
                sample = "\n".join(l for l in text.splitlines() if "S1400" in l or "ids_cited" in l)
    stop.set()
    t.join(timeout=2)
    print("### race against the real base tool")
    print(f"  runs={runs} runs_that_reported_the_outside_id_S1400={leaks}")
    if sample:
        for l in sample.splitlines():
            print("   |", l)
    print("  (S1400 lives outside the lane; the tool's containment check must hold on every read)")
    print()


if __name__ == "__main__":
    main()
