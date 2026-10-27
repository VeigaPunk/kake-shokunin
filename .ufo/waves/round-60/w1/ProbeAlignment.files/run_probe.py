#!/usr/bin/env python3
"""Probe driver: validate, compare greedies on 200 seeded fixtures, cost runs."""
import itertools
import random
import resource
import sys
import time
import tracemalloc

sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-60/w1/ProbeAlignment.files")
import align

TAG = b"[r60-correction 2026-10-27]"


# ---------- 1. DP vs brute-force oracle ----------
def oracle_check():
    bad = 0
    alpha = [b"a", b"b", TAG, b"U", b""]
    tested = 0
    for n in range(0, 4):
        for m in range(n, 8):
            for idxs in itertools.combinations(range(m), n):
                for _ in range(60):  # random fillings per shape
                    R = [random.choice(alpha) for _ in range(m)]
                    B = [R[i] for i in idxs]
                    got = align.min_untagged(B, R)
                    exp = align.brute_min(B, R)
                    tested += 1
                    if got != exp:
                        bad += 1
                        print("ORACLE MISS", B, R, "dp=", got, "brute=", exp)
                        if bad > 5:
                            return tested, bad
    # also non-subsequence cases
    for _ in range(3000):
        m = random.randint(0, 7)
        n = random.randint(0, 5)
        R = [random.choice(alpha) for _ in range(m)]
        B = [random.choice(alpha) for _ in range(n)]
        got = align.min_untagged(B, R)
        exp = align.brute_min(B, R)
        tested += 1
        if got != exp:
            bad += 1
            print("ORACLE MISS*", B, R, "dp=", got, "brute=", exp)
            if bad > 5:
                break
    return tested, bad


# ---------- 2. minimal disagreement search ----------
def find_minimal(rightmost, verdict_only=False):
    """Exhaustive ascending sizes; first disagreement found is minimal in
    (n, m) lexicographic scan order.  verdict_only: mn==0 but greedy>0."""
    alpha = [b"a", b"U", TAG]
    for n in range(0, 4):
        for m in range(n, 8):
            for R in itertools.product(alpha, repeat=m):
                R = list(R)
                for idxs in itertools.combinations(range(m), n):
                    B = [R[i] for i in idxs]
                    tag = align.visible_tags(R)
                    mn = align.min_untagged(B, R, tag)
                    g = align.greedy_count(B, R, tag, rightmost=rightmost)
                    if verdict_only:
                        if mn == 0 and g is not None and g > 0:
                            return B, R, mn, g
                    elif g != mn:
                        return B, R, mn, g
    return None


# ---------- 3. 200 seeded fixtures ----------
def fixture_run(seed=20261027, count=200):
    rng = random.Random(seed)
    alpha = [b"# h", b"a", b"b", b"U", TAG, b"", b"- item", TAG]  # dup-prone
    stats = {"agree": 0, "verdict_L": 0, "verdict_R": 0, "count_L": 0,
             "count_R": 0, "changed": 0}
    exL = exR = None
    for k in range(count):
        m = rng.randint(4, 30)
        R = [rng.choice(alpha) for _ in range(m)]
        # base: subsequence of R, occasionally mutated
        idxs = sorted(rng.sample(range(m), rng.randint(0, m)))
        B = [R[i] for i in idxs]
        if rng.random() < 0.25 and B:  # inject a changed/deleted base line
            i = rng.randrange(len(B))
            B[i] = B[i] + b"!"
        tag = align.visible_tags(R)
        mn = align.min_untagged(B, R, tag)
        gl = align.greedy_count(B, R, tag)
        gr = align.greedy_count(B, R, tag, rightmost=True)
        if mn is None:
            stats["changed"] += 1
            continue
        dl = gl - mn
        dr = gr - mn
        if dl == 0 and dr == 0:
            stats["agree"] += 1
        if gl != mn:
            stats["count_L"] += 1
            if gl > 0 and mn == 0:
                stats["verdict_L"] += 1
                if exL is None or len(R) < len(exL[1]):
                    exL = (B, R, mn, gl)
        if gr != mn:
            stats["count_R"] += 1
            if gr > 0 and mn == 0:
                stats["verdict_R"] += 1
                if exR is None or len(R) < len(exR[1]):
                    exR = (B, R, mn, gr)
    return stats, exL, exR


# ---------- 4. cost measurement ----------
def timed(fn, B, R, reps=5):
    best = None
    res = None
    for _ in range(reps):
        t0 = time.perf_counter()
        res = fn(B, R)
        dt = time.perf_counter() - t0
        if best is None or dt < best:
            best = dt
    return res, best


def mem_peak(fn, B, R):
    tracemalloc.start()
    res = fn(B, R)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return res, peak


def cost_runs(lane_path):
    out = []
    B = open(lane_path, "rb").read().split(b"\n")
    rng = random.Random(60)
    # revision = base + exactly 50 inserted lines in 7 mid-file runs
    # (alternating tagged/untagged run heads -> expected min_untagged = 3)
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
    assert inserted == 50 and len(R) == len(B) + 50
    res, dt = timed(align.min_untagged, B, R)
    _, peak = mem_peak(align.min_untagged, B, R)
    out.append(("realfile+50", len(B), len(R), res, dt, peak))

    n = 5000
    B5 = [b"line-%06d" % i for i in range(n)]
    R5 = list(B5)
    for k in range(25):
        at = 100 + k * 195
        R5[at:at] = [TAG, b"synthetic fill %d" % k]
    R5 += [b"tail %d" % i for i in range(50)]  # EOF append
    res, dt = timed(align.min_untagged, B5, R5)
    _, peak = mem_peak(align.min_untagged, B5, R5)
    out.append(("synth5000", len(B5), len(R5), res, dt, peak))

    # pathological bound: identical lines, n=m=5000 -> O(n*m)
    Bi = [b"same"] * 5000
    res, dt = timed(align.min_untagged, Bi, Bi, reps=1)
    _, peak = mem_peak(align.min_untagged, Bi, Bi)
    out.append(("identical5000", 5000, 5000, res, dt, peak))
    return out


if __name__ == "__main__":
    random.seed(7)
    print("== oracle ==")
    tested, bad = oracle_check()
    print("oracle_tested=%d misses=%d" % (tested, bad))

    print("== minimal disagreements ==")
    for rm in (False, True):
        found = find_minimal(rm)
        fv = find_minimal(rm, verdict_only=True)
        print(("rightmost" if rm else "leftmost"), "count:", found)
        print(("rightmost" if rm else "leftmost"), "verdict:", fv)

    print("== fixtures ==")
    stats, exL, exR = fixture_run()
    print(stats)
    print("example leftmost:", exL)
    print("example rightmost:", exR)

    print("== cost ==")
    lane = "/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/free-read-verbs.md"
    for name, nb, nr, res, dt, peak in cost_runs(lane):
        print("%s: base=%d rev=%d min_untagged=%s best_of=%.4fs peak=%.1fKB" %
              (name, nb, nr, res, dt, peak / 1024))
    print("maxrss_kb=%d" % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
