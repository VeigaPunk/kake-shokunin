#!/usr/bin/env python3
"""Run the round-45 C2 freshness matrix — the claim's frozen counting command.

Prints one line with three legs, each re-derived from committed bytes:
  selftest_kills before=2/4 after=4/4
      before: the four witness-class mutants (mutants/m1..m4.py, one-line mutations of
      semantic_witness per round-44 w2/MutClassGate.md) against the FROZEN v1 driver's
      shipped --selftest; after: the same four mutations applied to driver v2
      (mutants/m1..4_v2.py) against v2's shipped --selftest.
  v4_predicate_names_class_runs before=true|false after=true|false
      before: the committed round-44 v4 receipt's predicate text names ten class runs;
      after: the fresh counter-v6 v4 receipt names only the eleven v4 runs.
  witness_split class_only=N mixed=N met=N
      re-derived from the round-44 claim receipt after-final/after-v5.json.

Exit 0 iff every leg ran and printed; the claim's MET condition is read from the
printed values against the frozen declaration in SCORECARD.md (this round: the frozen
expectation for the split leg does not match the named receipt -- the printed truth is
the measurement).
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

LANE = Path(__file__).resolve().parents[3]
WAVE = LANE / ".ufo" / "waves" / "round-45"
OUT = WAVE / "verification" / "freshness"


def run_selftest(path: Path) -> int:
    proc = subprocess.run([sys.executable, "-B", str(path), "--selftest"],
                          capture_output=True, stdin=subprocess.DEVNULL, timeout=600)
    return proc.returncode


def predicate_names_class_runs(receipt_path: Path):
    try:
        text = json.loads(receipt_path.read_text()).get("predicate", "")
    except (OSError, ValueError):
        return None
    return "class runs" in text


def witness_split(receipt_path: Path):
    proc = subprocess.run(
        ["jq", "-r",
         ".rows | {class_only: map(select(.met==false and (.classCaught|length)>0 and "
         "(.legacyCaught|length)==0))|length, mixed: map(select(.met==false and "
         "(.classCaught|length)>0 and (.legacyCaught|length)>0))|length, met: map(select("
         ".met==true))|length}",
         str(receipt_path)],
        capture_output=True, stdin=subprocess.DEVNULL, timeout=120)
    if proc.returncode != 0:
        return None
    return json.loads(proc.stdout.decode("utf-8"))


def main() -> int:
    before_kills = after_kills = 0
    for n in (1, 2, 3, 4):
        if run_selftest(WAVE / "mutants" / ("m%d.py" % n)) != 0:
            before_kills += 1
    for n in (1, 2, 3, 4):
        if run_selftest(WAVE / "mutants" / ("m%d_v2.py" % n)) != 0:
            after_kills += 1

    v4_before = predicate_names_class_runs(
        WAVE.parent / "round-44" / "verification" / "claim" / "v4-final" / "v4.json")
    v4_after = predicate_names_class_runs(WAVE / "verification" / "v6v4" / "counter-v4.json")

    split = witness_split(WAVE.parent / "round-44" / "verification" / "claim"
                          / "after-final" / "after-v5.json")

    OUT.mkdir(parents=True, exist_ok=True)
    receipt = {
        "ran_at_ns": time.time_ns(),
        "selftest_kills": {"before": before_kills, "after": after_kills, "of": 4},
        "v4_predicate_names_class_runs": {"before": v4_before, "after": v4_after},
        "witness_split": split,
    }
    (OUT / "freshness.json").write_text(json.dumps(receipt, indent=1) + "\n")

    tf = lambda v: "true" if v else "false" if v is False else "null"
    print("selftest_kills before=%d/4 after=%d/4" % (before_kills, after_kills))
    print("v4_predicate_names_class_runs before=%s after=%s" % (tf(v4_before), tf(v4_after)))
    if split is None:
        print("witness_split ERROR")
        return 1
    print("witness_split class_only=%(class_only)d mixed=%(mixed)d met=%(met)d" % split)
    ok = (v4_before is not None and v4_after is not None and split is not None and
          before_kills + after_kills > 0)
    print("FRESHNESS_RAN_%s" % ("OK" if ok else "INCOMPLETE"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
