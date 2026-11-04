#!/usr/bin/env python3
"""MutKillers independent re-derivation of the C2-m2 kill (own copies, own driver)."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kake-shokunin")
POP = LANE / ".ufo/waves/round-83/killers/population.json"
WORK = Path("/fast/scratch/hyaku/kake-r83/MutKillers/rederive-c2")
FROZEN = LANE / ".ufo/waves/round-82/c82_capture_delta.py"
TOOL = LANE / "scripts/capture_delta.py"
EQUAL = "2026-11-04T12:50:00Z"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    frozen = pop["frozen_counters"]["C2"]
    patch = next(m for m in pop["mutants"] if m["id"] == "C2-m2")["patch"]
    print(f"frozen sha256 recorded={frozen['sha256']}")
    print(f"frozen sha256 measured={sha256(FROZEN)}")
    assert sha256(FROZEN) == frozen["sha256"], "frozen counter hash moved"

    pristine_path = WORK / "c82_capture_delta.pristine.py"
    mutant_path = WORK / "c82_capture_delta.mutant.py"
    shutil.copy2(FROZEN, pristine_path)
    text = FROZEN.read_text(encoding="utf-8")
    count = text.count(patch["old"])
    print(f"anchor occurrences={count}")
    assert count == 1, "anchor not unique"
    mutant_path.write_text(text.replace(patch["old"], patch["new"], 1), encoding="utf-8")
    print(f"pristine sha256={sha256(pristine_path)} mutant sha256={sha256(mutant_path)}")

    cp = load(pristine_path, "c2_pristine")
    cm = load(mutant_path, "c2_mutant")

    tree = WORK / "tree"
    tree.mkdir()
    cp.build_green(tree, TOOL)
    # equal instants: capture A rewritten to capture B's instant, record regenerated
    touched = 0
    for leaf in sorted((tree / cp.BASE_CAPTURE).iterdir()):
        receipt = leaf / "response.json"
        if not receipt.is_file():
            continue
        meta = json.loads(receipt.read_text(encoding="utf-8"))
        meta["fetchedAt"] = EQUAL
        receipt.write_text(json.dumps(meta, indent=1, sort_keys=True), encoding="utf-8")
        touched += 1
    print(f"capture-A receipts rewritten to {EQUAL}: {touched}")
    assert touched == 3
    tool_work = tree / "_regen"
    tool_work.mkdir()
    rc, out = cp.run_tool(tree, tool_work)
    shutil.rmtree(tool_work)
    print(f"record regeneration rc={rc}")
    assert rc == 0
    (tree / cp.RECORD).write_bytes(out)

    def score(module, label: str):
        work = WORK / f"work-{label}"
        for sub in ("run1", "run2", "selftest"):
            (work / sub).mkdir(parents=True, exist_ok=True)
        flags, info = module.measure(tree, work)
        print(f"{label} " + " ".join(f"{k}={v}" for k, v in flags.items()))
        print(f"{label} selftest_detail={info.get('selftest')}")
        return flags

    pf = score(cp, "pristine")
    mf = score(cm, "mutant")
    print(f"RESULT pristine_met={pf['met']} mutant_met={mf['met']} "
          f"order_keys=(order_ok pristine={pf['order_ok']} mutant={mf['order_ok']})")
    print(f"distinguished={'yes' if pf['met'] != mf['met'] else 'NO'}")
    print(f"frozen_untouched_sha256={sha256(FROZEN)}")
    return 0 if pf["met"] != mf["met"] else 1


if __name__ == "__main__":
    sys.exit(main())
