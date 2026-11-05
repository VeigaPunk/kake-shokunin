#!/usr/bin/env python3
"""M03b supplementary probe: E1-vocabulary BODY-half of the same OR-predicate
(re.search(r"admit", body, re.I) -> "adopt"). Establishes whether the
E1-vocabulary class is battery/selftest-covered while only the heading
alternative is redundant."""
import difflib
import hashlib
import os
import shutil
import subprocess
import sys

SCRATCH = "/fast/scratch/hyaku/kake-r95/MutC1"
LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
ENV = os.path.join(SCRATCH, "env-r95")
REC = os.path.join(SCRATCH, "receipts")
BASE_REV = "fdd5fdbeb8a2ba6c18f0f23135d1bee98068dca3"
P = open(os.path.join(ENV, ".ufo/waves/round-95/c95_selfassess.py"),
         encoding="utf-8").read()
assert hashlib.sha256(P.encode()).hexdigest() == ("8fd27d626883f2b6852ea2ee425706"
                                                  "a77a72eeaee10ef740b8e0fc15ac03"
                                                  "b193")
find = 're.search(r"admit", body, re.I)'
repl = 're.search(r"adopt", body, re.I)'
cnt = P.count(find)
assert cnt == 1, "find_count=%d" % cnt
mut = P.replace(find, repl, 1)
mid = "M03b"
root = os.path.join(SCRATCH, "env-mut", mid, ".ufo", "waves")
d95 = os.path.join(root, "round-95")
os.makedirs(os.path.join(d95, "frozen"), exist_ok=True)
os.makedirs(os.path.join(root, "round-94"), exist_ok=True)
mpath = os.path.join(d95, "c95_selfassess.py")
with open(mpath, "w", encoding="utf-8") as fh:
    fh.write(mut)
shutil.copyfile(os.path.join(ENV, ".ufo/waves/round-95/frozen/c1-surfaces.json"),
                os.path.join(d95, "frozen", "c1-surfaces.json"))
shutil.copyfile(os.path.join(ENV, ".ufo/waves/round-94/c94_selfassess.py"),
                os.path.join(root, "round-94", "c94_selfassess.py"))
with open(os.path.join(REC, mid + ".diff"), "w") as fh:
    fh.write("".join(difflib.unified_diff(
        P.splitlines(True), mut.splitlines(True),
        fromfile="c95_selfassess.py (pristine 8fd27d62)", tofile=mid)))
env = dict(os.environ)
env["TMPDIR"] = os.path.join(SCRATCH, "tmp")
env.pop("PYTHONPATH", None)


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, env=env, cwd=SCRATCH)
    return (p.returncode, p.stdout.decode("utf-8", "replace"),
            p.stderr.decode("utf-8", "replace"))


rc, so, se = run([sys.executable, "-B", mpath, "--selftest"])
with open(os.path.join(REC, mid + ".selftest.txt"), "w") as fh:
    fh.write("rc=%d\n%s%s" % (rc, so, se))
rc2, o2, e2 = run([sys.executable, "-B", mpath, "--root", LANE,
                   "--revision", BASE_REV,
                   "--work", os.path.join(SCRATCH, "work", mid)])
l1 = (o2.splitlines() or [""])[0]
with open(os.path.join(REC, mid + ".base.txt"), "w") as fh:
    fh.write("rc=%d\n%s\n%s%s" % (rc2, l1, o2, e2))
with open(os.path.join(REC, mid + ".battery.txt"), "w") as fh:
    toks = [t for t in l1.split() if t.split("=")[0] in
            ("battery", "admit", "shadow", "predecessor_admits", "met")]
    fh.write("line1 battery fields: %s\n" % " ".join(toks))
print("M03b find_count=1 selftest_rc=%d full_rc=%d" % (rc, rc2))
print("L1 %s" % l1)
print("SELFTEST_TAIL %s" % ((so.strip().splitlines() or [""])[-1])[:200])
