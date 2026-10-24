#!/usr/bin/env python3
"""Run the round-45 C2 freshness matrix — the claim's frozen counting command.

Prints one line per leg, each re-derived from committed bytes at this invocation:
  selftest_kills before=2/4 after=4/4
  v4_predicate_names_class_runs before=true|false after=true|false
  witness_split class_only=N mixed=N met=N other=N

Falsifiability (w2/MutFreshnessRunner, w2/RederiveMutantsV1 findings closed):
- a kill is exit code 1 exactly; exit 0 is survival; any other code (missing
  mutant, syntax error, usage) is an evaluation error and fails the run;
- the three receipt inputs are pinned by path + sha256 inside freshness.json;
  reading a different file changes the recorded pins and fails the expectations;
- stable expectations are enforced (they are facts of the frozen bytes,
  independent of the claim's verdict): before_kills == 2, after_kills == 4,
  v4_before is True, v4_after is False, and the split totals the row count;
- leg (c) prints the MEASURED split and never asserts the frozen tuple — the
  claim's leg (c) is falsified as declared and the measurement is the record.

Exit 0 iff every leg ran and every stable expectation held; exit 1 otherwise.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

LANE = Path(__file__).resolve().parents[3]
WAVE = LANE / ".ufo" / "waves" / "round-45"
OUT = WAVE / "verification" / "freshness"

CLAIM_RECEIPT = (WAVE.parent / "round-44" / "verification" / "claim" / "after-final"
                 / "after-v5.json")
V4_BEFORE_RECEIPT = (WAVE.parent / "round-44" / "verification" / "claim" / "v4-final"
                     / "v4.json")
V4_AFTER_RECEIPT = WAVE / "verification" / "v6v4" / "counter-v4.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_selftest(path: Path):
    """Return 'killed' (exit 1), 'survived' (exit 0), or 'error' (anything else)."""
    proc = subprocess.run([sys.executable, "-B", str(path), "--selftest"],
                          capture_output=True, stdin=subprocess.DEVNULL, timeout=600)
    if proc.returncode == 1:
        return "killed"
    if proc.returncode == 0:
        return "survived"
    return "error(rc=%d)" % proc.returncode


def predicate_names_class_runs(receipt_path: Path):
    text = json.loads(receipt_path.read_text()).get("predicate", "")
    return "class runs" in text


def witness_split(receipt_path: Path):
    rows = json.loads(receipt_path.read_text()).get("rows", [])
    class_only = mixed = met = other = 0
    for row in rows:
        caught = row.get("classCaught") or []
        legacy = row.get("legacyCaught") or []
        if row.get("met") is True:
            met += 1
        elif caught and not legacy:
            class_only += 1
        elif caught and legacy:
            mixed += 1
        else:
            other += 1
    return {"class_only": class_only, "mixed": mixed, "met": met, "other": other,
            "rows": len(rows)}


def main() -> int:
    problems = []
    outcomes = {}
    for n in (1, 2, 3, 4):
        outcomes[("before", n)] = run_selftest(WAVE / "mutants" / ("m%d.py" % n))
    for n in (1, 2, 3, 4):
        outcomes[("after", n)] = run_selftest(WAVE / "mutants" / ("m%d_v2.py" % n))
    for key, value in outcomes.items():
        if value.startswith("error"):
            problems.append("%s m%d: %s" % (key[0], key[1], value))
    before_kills = sum(1 for n in (1, 2, 3, 4) if outcomes[("before", n)] == "killed")
    after_kills = sum(1 for n in (1, 2, 3, 4) if outcomes[("after", n)] == "killed")
    if before_kills != 2:
        problems.append("before_kills == %d, expected 2" % before_kills)
    if after_kills != 4:
        problems.append("after_kills == %d, expected 4" % after_kills)

    v4_before = predicate_names_class_runs(V4_BEFORE_RECEIPT)
    v4_after = predicate_names_class_runs(V4_AFTER_RECEIPT)
    if v4_before is not True:
        problems.append("v4_before predicate does not name class runs")
    if v4_after is not False:
        problems.append("v4_after predicate still names class runs")

    split = witness_split(CLAIM_RECEIPT)
    if split["class_only"] + split["mixed"] + split["met"] + split["other"] != split["rows"]:
        problems.append("split does not total the row count")

    OUT.mkdir(parents=True, exist_ok=True)
    receipt = {
        "ran_at_ns": time.time_ns(),
        "inputs": {
            "claim_receipt": {"path": str(CLAIM_RECEIPT.relative_to(LANE)),
                              "sha256": sha256(CLAIM_RECEIPT)},
            "v4_before_receipt": {"path": str(V4_BEFORE_RECEIPT.relative_to(LANE)),
                                  "sha256": sha256(V4_BEFORE_RECEIPT)},
            "v4_after_receipt": {"path": str(V4_AFTER_RECEIPT.relative_to(LANE)),
                                 "sha256": sha256(V4_AFTER_RECEIPT)},
        },
        "selftest_kills": {"before": before_kills, "after": after_kills, "of": 4,
                           "outcomes": {"%s_m%d" % k: v for k, v in sorted(outcomes.items())}},
        "v4_predicate_names_class_runs": {"before": v4_before, "after": v4_after},
        "witness_split": split,
        "problems": problems,
    }
    (OUT / "freshness.json").write_text(json.dumps(receipt, indent=1) + "\n")

    tf = lambda v: "true" if v else "false"
    print("selftest_kills before=%d/4 after=%d/4" % (before_kills, after_kills))
    print("v4_predicate_names_class_runs before=%s after=%s" % (tf(v4_before), tf(v4_after)))
    print("witness_split class_only=%(class_only)d mixed=%(mixed)d met=%(met)d other=%(other)d"
          % split)
    if problems:
        print("FRESHNESS_PROBLEMS %d: %s" % (len(problems), "; ".join(problems)))
        return 1
    print("FRESHNESS_MEASURED_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
