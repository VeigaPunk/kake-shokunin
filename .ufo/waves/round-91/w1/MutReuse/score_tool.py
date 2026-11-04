#!/usr/bin/env python3
"""Score every committed tool mutant with the frozen C2 counter, in parallel."""
import concurrent.futures
import json
import os
import subprocess

S = "/fast/scratch/hyaku/kake-r91/MutReuse"
LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
COUNTER = os.path.join(LANE, ".ufo/waves/round-91/c91_reuse.py")
FX = os.path.join(S, "fx")

revs = json.load(open(os.path.join(S, "tool-revs.json")))
jobs = [("M00", "10995409cf01e746125fc7f24dec88bb50b601b3")] + sorted(revs.items())


def one(job):
    mid, rev = job
    work = os.path.join(S, "work", mid)
    os.makedirs(work, exist_ok=True)
    p = subprocess.run(
        ["python3", "-B", COUNTER, "--root", FX, "--revision", rev,
         "--work", work, "--seed", "91091"],
        capture_output=True, text=True, timeout=900)
    lines = p.stdout.splitlines()
    with open(os.path.join(S, "receipts", "tool-%s.txt" % mid), "w") as fh:
        fh.write("rev=%s\nexit=%d\n" % (rev, p.returncode))
        fh.write(p.stdout)
        fh.write("stderr=%s\n" % p.stderr.strip())
    return mid, rev, p.returncode, lines[0] if lines else "", (lines[1] if len(lines) > 1 else "")


os.makedirs(os.path.join(S, "receipts"), exist_ok=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
    for mid, rev, rc, head, detail in ex.map(one, jobs):
        print("%s exit=%d %s" % (mid, rc, head))
        if detail:
            d = json.loads(detail)
            print("   failures=%s errors=%s" % (d.get("hand_failures"), d.get("errors")))
