#!/usr/bin/env python3
"""Equivalence probe for M1 (append-only conjunct dropped).

If `met` were genuinely gated by `append_only`, there must exist a tree where
append_only is false while findings is empty.  Build the only shape that can do it
(a claim row present at --base and gone at the measured revision) and compare the
full JSON of the pristine counter with the M1 mutant on both counters.
"""
import json
import subprocess
import sys
from pathlib import Path

S = Path("/fast/scratch/hyaku/kake-r76/MutationTesterGates")
TMP = S / "tmp"
OUT = S / "out"


def git(root, *args):
    p = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError("git %s: %s" % (" ".join(args), p.stderr.strip()))
    return p.stdout.strip()


def fixture(name):
    root = TMP / name
    if root.exists():
        import shutil
        shutil.rmtree(root)
    (root / ".ufo/waves/round-75/controls").mkdir(parents=True)
    (root / "corpus").mkdir(parents=True)
    (root / ".ufo/waves/round-75/controls/ctl.txt").write_text("yy=8\n")
    (root / "corpus/QUALITY.md").write_text("## Round-75 criterion - eq\n\n- prose\n")
    (root / "SCORECARD.md").write_text(
        "## Round 75 - eq\n\n| Subject | Claim |\n|---|---|\n| A | `zz=9` |\n| B | `yy=8` |\n")
    git(root, "init", "-q")
    git(root, "add", "-A")
    git(root, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "base")
    base = git(root, "rev-parse", "HEAD")
    (root / "SCORECARD.md").write_text(
        "## Round 75 - eq\n\n| Subject | Claim |\n|---|---|\n| B | `yy=8` |\n")
    git(root, "add", "-A")
    git(root, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "drop-A")
    return root, base


def run(tool, root, base):
    p = subprocess.run([sys.executable, "-B", str(tool), "--root", str(root),
                        "--revision", "HEAD", "--base", base, "--rounds", "75", "--json"],
                       capture_output=True, text=True,
                       env={"PATH": "/usr/bin:/bin", "TMPDIR": str(TMP)})
    try:
        data = json.loads(p.stdout)
    except ValueError:
        return {"rc": p.returncode, "stdout": p.stdout[:400], "stderr": p.stderr[:400]}
    return {"rc": p.returncode, "append_only": data["append_only"], "met": data["met"],
            "findings": sorted((f["id"], f["file"]) for f in data["findings"]),
            "rows": data["rows"]}


def compare(tag, pristine, mutant):
    root, base = fixture("eq_" + tag)
    a = run(pristine, root, base)
    b = run(mutant, root, base)
    same = a == b
    out = {"counter": tag, "fixture": str(root), "base": base,
           "pristine": a, "mutant": b, "identical": same}
    (OUT / ("eq_%s.json" % tag)).write_text(json.dumps(out, indent=1))
    print(tag, "identical=", same, "pristine=", a, "mutant=", b, flush=True)
    return same


if __name__ == "__main__":
    compare("v0_M1", S / "c1/m00_pristine.py", S / "c1/M1_append_only_conjunct_dropped.py")
    compare("v2_M1", S / "c1b/m00_pristine.py", S / "c1b/M1_append_only_conjunct_dropped.py")
