#!/usr/bin/env python3
"""Emit machine-readable recon evidence: frozen identity, probes, round-80 correctness."""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, "/fast/scratch/hyaku/kake-r80/ScoutRecon")
import recon  # noqa: E402

HERE = Path("/fast/scratch/hyaku/kake-r80/ScoutRecon")
LANE = recon.LANE
base, new = HERE / "tool_base.py", HERE / "tool_patched.py"


def selftest(tool):
    p = subprocess.run([sys.executable, "-B", str(tool), "--selftest"],
                       capture_output=True, text=True)
    return {"line": p.stdout.strip(), "exit": p.returncode}


out = {"selftest": {"base": selftest(base), "predicted_patch": selftest(new)},
       "frozen": {}, "probes": {}, "a2": {}}

for m in sorted((LANE / ".ufo/waves/round-79/cases").glob("c*/manifest.json")):
    rb, ob, _ = recon.run(base, m)
    rn, on, _ = recon.run(new, m)
    out["frozen"][m.parent.name] = {
        "identical": recon.norm(rb, ob) == recon.norm(rn, on),
        "base_exit": rb, "base": ob.strip(), "new_exit": rn, "new": on.strip()}

for m in sorted((HERE / "probes").glob("*.json")):
    rb, ob, _ = recon.run(base, m)
    rn, on, _ = recon.run(new, m)
    out["probes"][m.stem] = {"base": json.loads(ob), "new": json.loads(on),
                             "base_exit": rb, "new_exit": rn}

expect = json.loads((LANE / ".ufo/waves/round-80/expect/expect.json").read_text())
for m in sorted((LANE / ".ufo/waves/round-80/cases").glob("c*/manifest.json")):
    rc, o, _ = recon.run(new, m)
    cid = m.parent.name
    rep = json.loads(o)
    got = rep["checks"][0]
    exp = expect["cases"][cid]
    out["a2"][cid] = {
        "exit": rc, "findings": sorted(rep["findings"]),
        "directives": got["directives"], "bots": got["bots"],
        "expected": exp,
        "correct": (rc == exp["exit"] and sorted(rep["findings"]) == exp["findings"]
                    and got["directives"] == exp["checks"][cid]["directives"]
                    and got["effective"] == exp["checks"][cid]["effective"]
                    and got["bots"] == exp["checks"][cid]["bots"])}
out["summary"] = {
    "frozen_cases": len(out["frozen"]),
    "frozen_identical": sum(v["identical"] for v in out["frozen"].values()),
    "a2_cases": len(out["a2"]),
    "a2_correct": sum(v["correct"] for v in out["a2"].values()),
}
print(json.dumps(out, indent=1, sort_keys=True))
