#!/usr/bin/env python3
"""MutKillers independent re-derivation of the C1-m3 kill.

Own copy of the frozen counter, the same patch bytes from the killer
population.json, the fixture described there (green tree with a two-commit
fixture fleet, output_bytes 3801 -> 4417 on both sides), and the printed
`open` compared pristine vs mutated.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kake-shokunin")
POP = LANE / ".ufo/waves/round-83/killers/population.json"
SEAT = Path("/fast/scratch/hyaku/kake-r83/MutKillers")
WORK = SEAT / "rederive"
FROZEN = LANE / ".ufo/waves/round-82/c82_defect_queue.py"
TOOL = LANE / "scripts/capture_delta.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(repo: Path, *args: str) -> str:
    proc = subprocess.run(["git", "-C", str(repo), *args], check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.stdout.decode().strip()


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    pop = json.loads(POP.read_text(encoding="utf-8"))
    frozen = pop["frozen_counters"]["C1"]
    patch = next(m for m in pop["mutants"] if m["id"] == "C1-m3")["patch"]

    print(f"frozen sha256 recorded={frozen['sha256']}")
    print(f"frozen sha256 measured={sha256(FROZEN)}")
    assert sha256(FROZEN) == frozen["sha256"], "frozen counter hash moved"

    pristine = WORK / "c82_defect_queue.pristine.py"
    mutant = WORK / "c82_defect_queue.mutant.py"
    shutil.copy2(FROZEN, pristine)
    text = FROZEN.read_text(encoding="utf-8")
    occurrences = text.count(patch["old"])
    print(f"anchor occurrences={occurrences} old={patch['old']!r}")
    assert occurrences == 1, "anchor is not unique"
    mutant.write_text(text.replace(patch["old"], patch["new"]), encoding="utf-8")
    print(f"mutant sha256={sha256(mutant)} pristine sha256={sha256(pristine)}")

    cp = load(pristine, "c82_pristine_C1")
    cm = load(mutant, "c82_mutant_C1")

    # two-commit fixture fleet, per the fixture-git rule
    fleet = WORK / "fleet"
    fleet.mkdir()
    git(fleet, "init", "-q")
    top = Path(git(fleet, "rev-parse", "--show-toplevel")).resolve()
    print(f"fixture toplevel={top} expected={fleet.resolve()}")
    assert top == fleet.resolve(), "fixture git toplevel mismatch"
    identity = ["-c", "user.name=fixture", "-c", "user.email=fixture@example.test"]
    report = fleet / cp.FLEET_REPORT
    report.parent.mkdir(parents=True)
    report.write_text("filed report\n", encoding="utf-8")
    git(fleet, "add", cp.FLEET_REPORT)
    git(fleet, *identity, "commit", "-q", "-m", "filed")
    report.write_text("filed report\namended lane-tip line\n", encoding="utf-8")
    git(fleet, "add", cp.FLEET_REPORT)
    git(fleet, *identity, "commit", "-q", "-m", "amended")
    fleet_commit = git(fleet, "rev-parse", "--short=8", "HEAD")
    print(f"fleet_commit={fleet_commit}")

    # green tree from the counter's own builder, then the fixture mutation
    tree = WORK / "tree"
    tree.mkdir()
    cp.build_green_tree(tree, fleet_commit, cp.LIVE_RECEIPT)
    seat = tree / cp.SEAT_RECORD
    record = json.loads(seat.read_text(encoding="utf-8"))
    before_bytes = record["seats"]["MutC"]["output_bytes"]
    record["seats"]["MutC"]["output_bytes"] = 4417
    seat.write_text(json.dumps(record, indent=1), encoding="utf-8")
    lesson = tree / cp.LESSON
    lesson_text = lesson.read_text(encoding="utf-8")
    assert lesson_text.count("3801") == 1, "green lesson does not carry 3801 exactly once"
    lesson.write_text(lesson_text.replace("3801", "4417"), encoding="utf-8")
    print(f"fixture: seat output_bytes {before_bytes}->4417, lesson D4 3801->4417")

    def score(module, label: str):
        rows, present = module.evaluate(module.Tree(tree), fleet)
        opened = [f"{i}:{d}" for i, ok, d in rows if not ok]
        open_n = len(opened)
        closed = len(rows) - open_n
        print(f"{label} open={open_n} closed={closed} lesson_present={present}")
        for row in opened:
            print(f"  open-row {row}")
        return open_n

    p_open = score(cp, "pristine")
    m_open = score(cm, "mutant")
    print(f"RESULT pristine_open={p_open} mutant_open={m_open} "
          f"distinguished={'yes' if p_open != m_open else 'NO'}")
    print(f"pristine_counter_sha256={sha256(pristine)}")
    print(f"mutant_counter_sha256={sha256(mutant)}")
    print(f"frozen_untouched_sha256={sha256(FROZEN)}")
    return 0 if p_open != m_open else 1


if __name__ == "__main__":
    sys.exit(main())
