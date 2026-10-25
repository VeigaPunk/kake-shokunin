#!/usr/bin/env python3
"""Round-54 C2 counter — settlement of round-53 routed operational debt.

Frozen predicate (contract.md):

    Round-53 ops debt: registry row present, settlement manifest committed,
    and every cited w1 seat-report name recorded resolved or lost; met when all three hold.

Reads only committed bytes via git show. The settlement is an append-only
record of 40 spawned seats vs 0 committed reports; it explicitly records each
missing seat report as lost.

Exit: 0 met, 1 not met, 2 unevaluable, 64 usage.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

REQUIRED_SEAT_NAMES = {
    "ReviewerProvenance.md", "CriticCrossLane.md", "ScoutS329.md",
    "ScoutS312.md", "CriticLocators.md", "ScribeGate.md", "ScoutQuarantine.md",
}
SKILL = "SKILL.md"
LESSON = "corpus/lessons/round-53.md"
SPOTCHECK = "corpus/lessons/round-53-verifier-spotcheck.md"
MANIFEST = ".ufo/waves/round-53/settlement.md"
TABLE_HEADING = "### Owned freshness gate registry"
REQUIRED = ("c53_gate_truth.py", "gate", "--revision", "0=", "--selftest", "exec-quality-gate", "read-only")
PREDICATE = "Round-53 ops debt: registry row present, settlement manifest committed, and every cited w1 seat-report name recorded resolved or lost; met when all three hold"
NAME_RE = re.compile(r"\.ufo/waves/round-53/w1/([A-Za-z0-9_-]+\.md)")
MANIFEST_RE = re.compile(r"^\|\s*([A-Za-z0-9_-]+\.md)\s*\|\s*(?:resolved|lost)\s*\|", re.M)


def git(root: str, *args: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(["git", "-C", root, *args], capture_output=True, env=env)


def show(root: str, rev: str, path: str) -> bytes | None:
    p = git(root, "show", f"{rev}:{path}")
    return p.stdout if p.returncode == 0 else None


def run_checks(root: str, rev: str) -> tuple[int, dict]:
    skill_raw = show(root, rev, SKILL)
    lesson_raw = show(root, rev, LESSON)
    spotcheck_raw = show(root, rev, SPOTCHECK)
    manifest_raw = show(root, rev, MANIFEST)
    if skill_raw is None or lesson_raw is None or spotcheck_raw is None:
        return 2, {"registry": "unevaluable", "manifest": "unevaluable", "uncovered": "?"}
    skill = skill_raw.decode("utf-8", errors="replace")
    lesson = lesson_raw.decode("utf-8", errors="replace")
    spotcheck = spotcheck_raw.decode("utf-8", errors="replace")

    registry_present = False
    registry_line = ""
    inside = False
    for line in skill.splitlines():
        if line.strip() == TABLE_HEADING:
            inside = True
            continue
        if inside and line.startswith("## "):
            break
        if inside and "c53_gate_truth.py" in line:
            registry_line = line
            registry_present = all(token in line for token in REQUIRED)
            break

    missing_manifest = manifest_raw is None
    manifest = "" if missing_manifest else manifest_raw.decode("utf-8", errors="replace")
    cited = set(NAME_RE.findall(lesson + "\n" + spotcheck))
    settled = set(MANIFEST_RE.findall(manifest))
    uncovered = sorted(cited - settled)
    has_loss_basis = bool(re.search(r"40\s+spawned", manifest, re.I) and
                          re.search(r"0\s+(?:committed\s+)?seat reports", manifest, re.I))
    settled_required = REQUIRED_SEAT_NAMES <= settled
    manifest_ok = not missing_manifest and not uncovered and settled_required and has_loss_basis
    result = {
        "registry": "present" if registry_present else "absent",
        "registry_line": registry_line,
        "manifest": "present" if manifest_ok else ("absent" if missing_manifest else "incomplete"),
        "cited": sorted(cited),
        "settled": sorted(settled),
        "uncovered": uncovered,
        "spawned_reports_basis": has_loss_basis,
    }
    return (0 if registry_present and manifest_ok else 1), result
def main() -> int:
    parser = argparse.ArgumentParser(description="Round-54 round-53 ops-debt counter")
    parser.add_argument("--root", default=".", help="lane root")
    parser.add_argument("--revision", required=True, help="committed revision")
    args = parser.parse_args()
    code, r = run_checks(args.root, args.revision)
    uncovered = len(r["uncovered"]) if isinstance(r["uncovered"], list) else r["uncovered"]
    print(f"registry={r['registry']} manifest={r['manifest']} uncovered={uncovered}")
    if r.get("cited"):
        print(f"cited={r['cited']}")
        print(f"settled={r['settled']}")
        print(f"uncovered_names={r['uncovered']}")
    print(PREDICATE)
    print(f"EXIT={code}")
    return code


if __name__ == "__main__":
    sys.exit(main())
