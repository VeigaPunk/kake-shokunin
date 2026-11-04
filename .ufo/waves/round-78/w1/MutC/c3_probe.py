#!/usr/bin/env python3
"""c3_probe.py -- independent C3 matrix probe (MutC, round 78).

For every frozen case dir under <cases>/*/:
  run  <tool> --manifest <case>/manifest.json --root <case> --json
  compare (exit code, set(finding_ids)) against <case>/expect.json
Exit 0 iff every case is decided correctly. This mirrors the frozen C3
predicate without depending on the round's own matrix counter.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--tool", required=True)
    ap.add_argument("--cases", required=True)
    ap.add_argument("--json")
    a = ap.parse_args()
    cases = Path(a.cases).resolve()
    tool = Path(a.tool).resolve()
    dirs = sorted(p for p in cases.iterdir() if p.is_dir())
    results = []
    for d in dirs:
        exp = json.loads((d / "expect.json").read_text())
        p = subprocess.run(
            [sys.executable, "-B", str(tool), "--manifest",
             str(d / "manifest.json"), "--root", str(d), "--json"],
            capture_output=True, text=True, timeout=120)
        try:
            rep = json.loads(p.stdout)
            ids = sorted(rep.get("finding_ids") or [])
            reported_effective = [sorted(r.get("effective") or []) for r in rep.get("results") or []]
        except ValueError:
            ids = None
            reported_effective = None
        want = sorted(exp.get("findings") or [])
        ok = (p.returncode == exp.get("exit")) and (ids == want)
        results.append({
            "case": d.name, "ok": ok, "rc": p.returncode, "want_exit": exp.get("exit"),
            "ids": ids, "want_ids": want,
            "effective": reported_effective,
            "stdout_tail": "" if ok else (p.stdout[-300:] + p.stderr[-300:]),
        })
    bad = [r for r in results if not r["ok"]]
    decided = len(results) - len(bad)
    payload = {"cases": len(results), "decided": decided, "correct": decided,
               "failed": [r["case"] for r in bad], "results": results}
    if a.json:
        Path(a.json).write_text(json.dumps(payload, indent=1))
    for r in results:
        print(f"  {'PASS' if r['ok'] else 'FAIL'} {r['case']}: rc={r['rc']} want={r['want_exit']} ids={r['ids']}")
    print(f"matrix: cases={len(results)} decided={decided} correct={decided} "
          f"failed={len(bad)}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
