#!/usr/bin/env python3
"""Stale-receipt fixture: writes a fully valid-shaped receipt (own sha, seed, note
None, met False, a class divergence) but BACKDATES its mtime 5 seconds, then exits 0.

Under the frozen v1 driver this receipt certifies (ok=True, exit 0) -- the round-44
review's defect 1c reachability. Under driver v2 the receipt fails the run-window
mtime check and is rejected with the named class stale_receipt. Unlike the
stale-planted fixture (SIGKILL + pre-planted bytes, exit -9), this variant keeps the
counter exit inside {0,1} so the mtime branch -- not the exit branch -- is what
refuses it."""
import hashlib, json, os, sys, time

CLASS_MODULES = tuple(("G%d" % i, "g%d.py" % i) for i in range(1, 11))
PREDICATE = "stale-backdate fixture counter"

def main():
    out = sys.argv[sys.argv.index("--out") + 1]
    sha = hashlib.sha256(open(__file__, "rb").read()).hexdigest()
    rec = {"counterSha256": sha, "seed": 424242, "note": None, "met": False,
           "runs": {"G2": {"equal": False}, "A": {"equal": True}}}
    with open(out, "w") as fh:
        json.dump(rec, fh)
    past = time.time() - 5
    os.utime(out, (past, past))
    sys.exit(0)

if __name__ == "__main__":
    main()
