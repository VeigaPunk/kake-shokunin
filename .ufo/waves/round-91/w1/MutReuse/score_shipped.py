#!/usr/bin/env python3
"""Score the shipped-base mutants (and the pristine shipped bytes) with the frozen counter."""
import concurrent.futures
import json
import os
import subprocess

S = "/fast/scratch/hyaku/kake-r91/MutReuse"
LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
COUNTER = os.path.join(LANE, ".ufo/waves/round-91/c91_reuse.py")
FX = os.path.join(S, "fx")

revs = json.load(open(os.path.join(S, "tool-revs-shipped.json")))
jobs = [("M00s", "b3f3ca31ace8b68e5dbbcd9c72c85884f02fc415")] + sorted(revs.items())
os.makedirs(os.path.join(S, "receipts"), exist_ok=True)


def one(job):
    mid, rev = job
    work = os.path.join(S, "work-shipped", mid)
    os.makedirs(work, exist_ok=True)
    p = subprocess.run(
        ["python3", "-B", COUNTER, "--root", FX, "--revision", rev,
         "--work", work, "--seed", "91091"],
        capture_output=True, text=True, timeout=900)
    with open(os.path.join(S, "receipts", "shipped-%s.txt" % mid), "w") as fh:
        fh.write("rev=%s\nexit=%d\n" % (rev, p.returncode))
        fh.write(p.stdout)
    lines = p.stdout.splitlines()
    return mid, rev, p.returncode, (lines[0] if lines else ""), (lines[1] if len(lines) > 1 else "")


with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
    for mid, rev, rc, head, detail in ex.map(one, jobs):
        print("%s exit=%d %s" % (mid, rc, head))
        if detail:
            d = json.loads(detail)
            print("   failures=%s errors=%s" % (d.get("hand_failures"), d.get("errors")))
