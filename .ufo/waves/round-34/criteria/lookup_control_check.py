#!/usr/bin/env python3
"""Criterion check (round 34): a counter must score a lookup-table control below its full score.

A lookup-table control is a commit whose tool (or entry) does none of the
claimed work and only replays answers the counter itself makes visible: for a
matrix counter, a tool that reads the case directory name the counter chose
and prints that case's expected output from the published matrix. If the
counter gives such a commit its full score, the score cannot tell the claimed
capability from transcription.

Usage: python3 -B lookup_control_check.py --counter <counter.py> --repo <repo> --control <rev>
The counter is run as `<counter> --root <repo> --revision <rev>` and must print
one JSON object carrying `total` and either `passed` or `met`.

Exit 0 = the control scores below total (the counter discriminates).
Exit 1 = the control reaches total (criterion fails).
Exit 2 = the counter gave no usable JSON or exited other than 0 or 1.

The check cannot tell a lookup control from an honest one: an honest tool
also reaches total and also gives exit 1 (round-34 wave 2,
ReviewLookupControlCheck). It is meaningful only for a control commit known,
by reading its diff, to do none of the claimed work; the retained controls
named in QUALITY round-34 criterion (d) are such commits.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--control", required=True)
    a = ap.parse_args()
    p = subprocess.run([sys.executable, "-B", a.counter, "--root", a.repo, "--revision", a.control],
                       capture_output=True, text=True, timeout=600)
    try:
        out = json.loads(p.stdout)
        score = out["passed"] if "passed" in out else out["met"]
        total = out["total"]
    except (ValueError, KeyError, TypeError):
        print(f"no usable JSON from counter (exit {p.returncode})")
        return 2
    if p.returncode not in (0, 1):
        print(f"counter exited {p.returncode}; its JSON is not trusted")
        return 2
    verdict = "FAIL: control reaches the full score" if score >= total else "ok: control scores below total"
    print(json.dumps({"counter": a.counter, "control": a.control, "score": score, "total": total,
                      "counterExit": p.returncode, "verdict": verdict}))
    return 1 if score >= total else 0


if __name__ == "__main__":
    sys.exit(main())
