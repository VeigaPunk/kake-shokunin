#!/usr/bin/env python3
"""ExecTrial-6 (kake round 92 w1): run the delivered instrument on recorded inputs.

Runs LANE/scripts/heuristic_freshness.py once per input under
w1/ExecTrial/inputs/, capturing stdout/stderr/exit per surface under
w1/ExecTrial/outputs/, and prints a compact table. The instrument is bound
to bytes by the sha256 recorded in trial.env / the report; this script
never edits it.
"""
import hashlib
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
SEAT = os.path.join(LANE, ".ufo/waves/round-92/w1/ExecTrial")
INSTR = os.path.join(LANE, "scripts/heuristic_freshness.py")


def main():
    if not os.path.isfile(INSTR):
        print("INSTRUMENT ABSENT: %s" % INSTR, file=sys.stderr)
        return 3
    instr_bytes = open(INSTR, "rb").read()
    digest = hashlib.sha256(instr_bytes).hexdigest()
    outdir = os.path.join(SEAT, "outputs")
    os.makedirs(outdir, exist_ok=True)
    rows = []
    for name in sorted(os.listdir(os.path.join(SEAT, "inputs"))):
        if not name.endswith(".json"):
            continue
        sid = name[:-5]
        data = open(os.path.join(SEAT, "inputs", name), "rb").read()
        p = subprocess.run([sys.executable, "-B", INSTR], input=data,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           cwd=LANE)
        with open(os.path.join(outdir, sid + ".out"), "wb") as f:
            f.write(p.stdout)
        with open(os.path.join(outdir, sid + ".err"), "wb") as f:
            f.write(p.stderr)
        with open(os.path.join(outdir, sid + ".rc"), "w") as f:
            f.write("%d\n" % p.returncode)
        rec = {"surface": sid, "exit": p.returncode}
        if p.returncode == 0 and p.stdout.strip():
            rec["decision"] = json.loads(p.stdout)
        else:
            rec["stderr"] = p.stderr.decode("utf-8", "replace").strip()
            if p.stdout.strip():
                rec["stdout_on_failure"] = p.stdout.decode("utf-8", "replace").strip()
        rows.append(rec)
    summary = {
        "instrument": INSTR,
        "instrument_sha256": digest,
        "instrument_bytes": len(instr_bytes),
        "surfaces": len(rows),
        "exit0": sum(1 for r in rows if r["exit"] == 0),
        "refused": sum(1 for r in rows if r["exit"] != 0),
    }
    with open(os.path.join(SEAT, "outputs", "summary.json"), "w") as f:
        json.dump({"summary": summary, "rows": rows}, f, indent=1, sort_keys=True)
        f.write("\n")
    print(json.dumps(summary, sort_keys=True))
    for r in rows:
        if r["exit"] == 0:
            d = r["decision"]
            print("%-28s exit=0 decision=%-26s lifetime=%-8s heuristic=%s" % (
                r["surface"], d.get("decision"), d.get("lifetime"), d.get("heuristic")))
        else:
            print("%-28s exit=%d refusal=%s" % (r["surface"], r["exit"], r["stderr"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
