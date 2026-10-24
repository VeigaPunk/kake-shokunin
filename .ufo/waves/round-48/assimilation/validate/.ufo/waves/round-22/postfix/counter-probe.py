#!/usr/bin/env python3
"""Reproduce the w2/FalsifyCounting and residual counter-examples against one measure.py.

Usage: counter-probe.py --lane LANE --measure PATH. All git writes happen in a
throwaway clone under a fresh temporary directory, never in the lane.
CE1: a stub matrix.py that never runs the validator, emits 32 FAIL rows and
declares accepted=32 must NOT yield exit 0 / accepted 32.
CE2: the baseline revision measured without --cases-root (instrument not
validated) must NOT exit 0.
CE3 (residual/ResRevCounter.md): a self-consistent stub that copies the oracle
into 32 PASS rows with executed=32, never running the validator, must NOT
yield exit 0 / accepted 32.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

BASE = "7c61c8cc791bde36dd5e3688bdfea2678d90146c"
STUB = '''import json, sys
cases = json.load(open(__file__.rsplit("/", 1)[0] + "/cases.json"))["cases"]
rows = [{"caseId": c["caseId"], "status": "FAIL", "expectedExit": c["expectedExit"], "actualExit": 99,
         "expectedFindings": c["expectedFindings"], "actualFindings": []} for c in cases]
print(json.dumps({"selection": "all", "accepted": len(rows), "total": len(rows), "executed": 0,
                  "discrepancies": 0, "toolMissing": False, "results": rows}))
'''
CONSISTENT_STUB = '''import json, sys
cases = json.load(open(__file__.rsplit("/", 1)[0] + "/cases.json"))["cases"]
rows = [{"caseId": c["caseId"], "status": "PASS", "expectedExit": c["expectedExit"], "actualExit": c["expectedExit"],
         "expectedFindings": c["expectedFindings"], "actualFindings": c["expectedFindings"]} for c in cases]
print(json.dumps({"selection": "all", "accepted": len(rows), "total": len(rows), "executed": len(rows),
                  "discrepancies": 0, "toolMissing": False, "results": rows}))
'''


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def measure(script, root, revision):
    done = subprocess.run([sys.executable, "-B", script, "--root", root, "--revision", revision],
                          capture_output=True, text=True, timeout=300)
    payload = json.loads(done.stdout)
    return {"exit": done.returncode, "accepted": payload.get("accepted"), "total": payload.get("total"),
            "available": payload.get("available"), "instrumentValidated": payload.get("instrumentValidated"),
            "error": payload.get("error")}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lane", required=True)
    parser.add_argument("--measure", required=True)
    args = parser.parse_args()
    script = os.path.abspath(args.measure)
    with tempfile.TemporaryDirectory(prefix="kake-r22-counter-probe-") as tmp:
        clone = os.path.join(tmp, "clone")
        subprocess.run(["git", "clone", "--quiet", "--no-hardlinks", os.path.abspath(args.lane), clone], check=True)
        matrix = os.path.join(clone, ".ufo/waves/round-22/matrix.py")
        commit = ["-c", "user.name=probe", "-c", "user.email=probe@invalid", "commit", "--quiet", "-am"]
        with open(matrix, "w", encoding="utf-8") as stream:
            stream.write(STUB)
        git(clone, *commit, "probe: stub matrix")
        ce1 = measure(script, clone, git(clone, "rev-parse", "HEAD"))
        with open(matrix, "w", encoding="utf-8") as stream:
            stream.write(CONSISTENT_STUB)
        git(clone, *commit, "probe: self-consistent stub matrix")
        ce3 = measure(script, clone, git(clone, "rev-parse", "HEAD"))
        ce2 = measure(script, clone, BASE)
    ce1_ok = not (ce1["exit"] == 0 or ce1["accepted"] == 32)
    ce2_ok = ce2["exit"] != 0
    ce3_ok = not (ce3["exit"] == 0 or ce3["accepted"] == 32)
    result = {"measure": script, "CE1_stub_matrix": {**ce1, "rejected": ce1_ok},
              "CE2_unvalidated_baseline": {**ce2, "rejected": ce2_ok},
              "CE3_self_consistent_stub": {**ce3, "rejected": ce3_ok}, "passed": ce1_ok and ce2_ok and ce3_ok}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
