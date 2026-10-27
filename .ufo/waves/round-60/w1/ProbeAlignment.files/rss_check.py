#!/usr/bin/env python3
"""Clean-process RSS check for align.min_untagged (no tracemalloc pollution)."""
import resource
import sys
import time

sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-60/w1/ProbeAlignment.files")
import align

which = sys.argv[1] if len(sys.argv) > 1 else "identical"
TAG = b"[r60-correction 2026-10-27]"

if which == "identical":
    B = [b"same"] * 5000
    R = list(B)
elif which == "synth":
    B = [b"line-%06d" % i for i in range(5000)]
    R = list(B)
    for k in range(25):
        at = 100 + k * 195
        R[at:at] = [TAG, b"synthetic fill %d" % k]
    R += [b"tail %d" % i for i in range(50)]
elif which == "real":
    lane = "/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/free-read-verbs.md"
    B = open(lane, "rb").read().split(b"\n")
    import random
    rng = random.Random(60)
    pos = sorted(rng.sample(range(1, len(B)), 7))
    sizes = [8, 7, 8, 7, 7, 7, 6]
    R = list(B)
    inserted = 0
    for pi, (p, sz) in enumerate(zip(pos, sizes)):
        head = [TAG] if pi % 2 == 0 else [b"probe-insert-%d" % pi]
        run = head + [b"probe-fill-%d-%d" % (pi, j) for j in range(sz - 1)]
        for j, ln in enumerate(run):
            R.insert(p + inserted + j, ln)
        inserted += len(run)

t0 = time.perf_counter()
res = align.min_untagged(B, R)
dt = time.perf_counter() - t0
print("%s: n=%d m=%d min_untagged=%s wall=%.4fs maxrss_kb=%d" %
      (which, len(B), len(R), res, dt,
       resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
