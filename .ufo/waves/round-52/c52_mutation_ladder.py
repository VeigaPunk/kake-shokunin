#!/usr/bin/env python3
"""Round-52 C1 mutation ladder — old counter vs hardened counter.

Round 51 shipped a ledger counter whose own controls were never replayed against
the receipt shapes the wave could actually produce: twelve receipt mutations
(M1-M12 in `residual/ResidualSettlement.md`) are accepted by
`.ufo/waves/round-51/c51_wave_ledger.py`, so the counter's 3/3 is not evidence
of operability. This harness takes the same fixture family the hardened
counter's `--selftest` builds (harvested from the committed round-51 evidence,
each fixture a hermetic sandbox git repo) and runs BOTH counters on every
fixture:

  * `fixtures/pass` must be accepted by both counters (exit 0 each), and
  * every `fail_*` family must be accepted by the old counter (exit 0) and
    rejected by the hardened counter (exit 1).

Predicate (frozen in `.ufo/waves/round-52/contract.json` before any data):

    met: families_with_old_pass_and_new_reject >= 10 and pass_fixture_agrees

Exit codes: 0 predicate met, 1 not met, 2 the ladder itself could not run.
It reads committed bytes only (git show / git ls-tree) and writes its receipt to
`.ufo/waves/round-52/control/c1-mutation-ladder.json`; fixture repos live under
`.ufo/waves/round-52/selftest/ladder/` and are removed on exit.
"""
from __future__ import annotations

import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve()
LANE = HERE.parents[3]
LEDGER = HERE.with_name("c52_wave_ledger.py")
OLD_COUNTER = LANE / ".ufo/waves/round-51/c51_wave_ledger.py"
WORK = LANE / ".ufo/waves/round-52/selftest/ladder"
RECEIPT = LANE / ".ufo/waves/round-52/control/c1-mutation-ladder.json"

PREDICATE = (
    "met: families_with_old_pass_and_new_reject >= 10 and pass_fixture_agrees"
)
MIN_FAMILIES = 10


def load_ledger():
    spec = importlib.util.spec_from_file_location("c52_wave_ledger", LEDGER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def rev_of(repo: pathlib.Path) -> str:
    out = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True,
    )
    return out.stdout.strip()


def run_counter(script: pathlib.Path, repo: pathlib.Path, rev: str) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, "-B", str(script), "--root", str(repo), "--revision", rev],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def main() -> int:
    ledger = load_ledger()
    fixtures = ledger._selftest_fixture_files()
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    rows = []
    for name in sorted(fixtures):
        repo = WORK / name
        ledger._selftest_repo(str(repo), fixtures[name], f"fixture {name}")
        rev = rev_of(repo)
        old_code, old_out = run_counter(OLD_COUNTER, repo, rev)
        new_code, new_out = run_counter(LEDGER, repo, rev)
        rows.append({
            "fixture": name,
            "kind": "control" if name == "pass" else "mutant",
            "old_exit": old_code,
            "new_exit": new_code,
            "old_accepted": old_code == 0,
            "new_rejected": new_code != 0,
            "old_tail": old_out.splitlines()[-1] if old_out else "",
            "new_tail": new_out.splitlines()[-1] if new_out else "",
        })
    shutil.rmtree(WORK, ignore_errors=True)

    pass_row = next(r for r in rows if r["fixture"] == "pass")
    families = [r for r in rows if r["fixture"].startswith("fail_")]
    caught = [
        r for r in families if r["old_accepted"] and r["new_rejected"]
    ]
    pass_agrees = pass_row["old_accepted"] and pass_row["new_exit"] == 0
    met = len(caught) >= MIN_FAMILIES and pass_agrees

    receipt = {
        "schema": "kake-r52-c1-mutation-ladder-v1",
        "predicate": PREDICATE,
        "old_counter": str(OLD_COUNTER.relative_to(LANE)),
        "new_counter": str(LEDGER.relative_to(LANE)),
        "families": len(families),
        "families_caught": len(caught),
        "min_families": MIN_FAMILIES,
        "pass_fixture_agrees": pass_agrees,
        "met": met,
        "rows": rows,
    }
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")

    for r in rows:
        mark = "caught" if (r["old_accepted"] and r["new_rejected"]) else (
            "control" if r["fixture"] == "pass" else "MISSED"
        )
        print(
            f"  {r['fixture']:<22} old={r['old_exit']} new={r['new_exit']}  {mark}"
        )
    print(
        f"C1 ladder families={len(families)} caught={len(caught)}/{len(families)} "
        f"pass_agrees={pass_agrees} met={met}  ({PREDICATE})"
    )
    print(f"  receipt: {RECEIPT.relative_to(LANE)}")
    return 0 if met else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # ladder could not run: distinguish from a miss
        print(f"ladder unevaluable: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(2)
