#!/usr/bin/env python3
"""Read-only probe of c58_receipt_rewrites.pointed() over candidate ledger-note pointer forms."""
import importlib.util
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
BASE = "044048597d62f3199494b63b36e90dd57825e350"
COUNTER = os.path.join(LANE, ".ufo/waves/round-58/c58_receipt_rewrites.py")
SCRATCH = os.path.dirname(os.path.abspath(__file__))

spec = importlib.util.spec_from_file_location("c58rr", COUNTER)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def git(root, *args):
    p = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)
    return p.returncode, p.stdout.strip()


def blob(root, rev_path):
    return git(root, "rev-parse", rev_path)[1]


tree = git(LANE, "rev-parse", f"{BASE}^{{tree}}")[1]
blob7 = blob(LANE, f"{BASE}:corpus/lessons/round-57.md")[:7]
commit7 = BASE[:7]
commit12 = BASE[:12]
commit6 = BASE[:6]
nonexistent12 = "0123456789ab"

notes = [
    ("S1 path in backticks", "fill landed in `.ufo/waves/round-55/settlement.md`"),
    ("S2 path + trailing period", "disclosed in .ufo/waves/round-57/receipt-errata.json."),
    ("S3 path + ')' wrapper", "(see .ufo/waves/round-54/contract.md)"),
    ("S4 absent-at-base round-52 settlement", "see .ufo/waves/round-52/settlement.md"),
    ("S5 bare settlement.md", "see settlement.md"),
    ("S6 bare contract.md", "see contract.md"),
    ("S7 7-hex commit id", f"revision {commit7}"),
    ("S8 12-hex commit id", f"revision {commit12}"),
    ("S9 6-hex id", f"revision {commit6}"),
    ("S10 SCORECARD.md:4330", "SCORECARD.md:4330"),
    ("S11 https URL", "source https://ziyuan.baidu.com/college/articleinfo?id=3457"),
    ("S12 dir 'corpus'", "see corpus"),
    ("S13 dir '.ufo'", "see .ufo"),
    ("S14 round-58 ledger at base", "ledger .ufo/waves/round-58/receipt-rewrites.json"),
    ("S15 7-hex blob id", f"object {blob7}"),
    ("S16 bare LOG.md", "see LOG.md"),
    ("S17 lesson added after r53 events", "see corpus/lessons/round-53.md"),
    ("S18 bare 'x'", "x"),
    ("S19 './'-prefixed path", "see ./.ufo/waves/round-55/settlement.md"),
    ("S20 lane-qualified path", "see kake-shokunin/.ufo/waves/round-55/settlement.md"),
    ("S21 12-hex non-resolving", f"revision {nonexistent12}"),
    ("S22 directory .ufo/waves/round-55", "see .ufo/waves/round-55"),
    ("S23 SCORECARD.md#L4330", "SCORECARD.md#L4330"),
    ("S24 round-58 control path absent", ".ufo/waves/round-58/controls/after-c2-x.txt"),
    ("S25 receipt path (see {path} note)", "see .ufo/waves/round-57/controls/after-c1-receipt-pins.txt"),
    ("S26 40-hex non-lane id", "revision " + "f" * 40),
]

out = {"base": BASE, "tree7": tree[:7], "samples": []}
for label, note in notes:
    out["samples"].append({"label": label, "note": note, "pointed": mod.pointed(LANE, BASE, note)})

# tip-dependent behaviour on a scratch clone that carries the round-58 files
d = os.path.join(SCRATCH, "l")
if not os.path.isdir(d):
    subprocess.run(["git", "clone", "-q", "--shared", LANE, d], check=True)
    subprocess.run(["git", "-C", d, "checkout", "-q", "--detach", BASE], check=True)
rc, top = git(d, "rev-parse", "--show-toplevel")
assert os.path.realpath(top) == os.path.realpath(d), (rc, top)
os.makedirs(os.path.join(d, ".ufo/waves/round-58"), exist_ok=True)
with open(os.path.join(d, ".ufo/waves/round-58/receipt-rewrites.json"), "w") as fh:
    fh.write('{"events": []}\n')
subprocess.run(["git", "-C", d, "add", "-A"], check=True)
subprocess.run(["git", "-C", d, "-c", "user.name=selftest", "-c", "user.email=selftest@local",
                "commit", "-q", "-m", "r58 ledger"], check=True)
newtip = git(d, "rev-parse", "HEAD")[1]
tip_notes = [
    "ledger .ufo/waves/round-58/receipt-rewrites.json",
    "see .ufo/waves/round-55/settlement.md",
    f"revision {newtip}",
]
out["scratch_tip"] = newtip
out["tip_samples"] = [{"note": n, "pointed": mod.pointed(d, newtip, n)} for n in tip_notes]
out["scratch_toplevel_ok"] = os.path.realpath(git(d, "rev-parse", "--show-toplevel")[1]) == os.path.realpath(d)
print(json.dumps(out, indent=1, ensure_ascii=False))
