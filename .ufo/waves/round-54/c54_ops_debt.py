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
import json
import os
import re
import subprocess
import sys

class UsageParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        self.exit(64, f"{self.prog}: error: {message}\n")

REQUIRED_SEAT_NAMES = {
    "ReviewerProvenance.md", "CriticCrossLane.md", "ScoutS329.md",
    "ScoutS312.md", "CriticLocators.md", "ScribeGate.md", "ScoutQuarantine.md",
}
SKILL = "SKILL.md"
LESSON = "corpus/lessons/round-53.md"
SPOTCHECK = "corpus/lessons/round-53-verifier-spotcheck.md"
WAVE_SPEC = ".ufo/waves/round-53/w53-spec.json"
REPORT_DIR = ".ufo/waves/round-53/w1"
MANIFEST = ".ufo/waves/round-53/settlement.md"
TABLE_HEADING = "### Owned freshness gate registry"
PREDICATE = "Round-53 ops debt: registry row present, settlement manifest committed, and every cited w1 seat-report name recorded resolved or lost; met when all three hold."
MANIFEST_ROW_RE = re.compile(r"^\|\s*`?([A-Za-z0-9_-]+\.md)`?\s*\|\s*(resolved|lost)\s*\|\s*([^|]+?)\s*\|", re.M)
def git(root: str, *args: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(["git", "-C", root, *args], capture_output=True, env=env)


def show(root: str, rev: str, path: str) -> bytes | None:
    p = git(root, "show", f"{rev}:{path}")
    return p.stdout if p.returncode == 0 else None

def cited_names(*texts: str) -> set[str]:
    names: set[str] = set()
    path_re = re.compile(r"\.ufo/waves/round-53/w1/([A-Za-z0-9_-]+\.md)")
    file_re = re.compile(r"([A-Za-z0-9_-]+\.md)")
    for text in texts:
        for line in text.splitlines():
            names.update(path_re.findall(line))
            group = re.search(r"\(([^)]*\.ufo/waves/round-53/w1/[^)]*)\)", line)
            if group:
                names.update(file_re.findall(group.group(1)))
    return names

def registry_row_ok(line: str) -> bool:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    if len(cells) != 8:
        return False
    return (
        cells[0] == "c53_gate_truth.py"
        and cells[1] == "gate"
        and "c53_gate_truth.py" in cells[2]
        and "--revision" in cells[2]
        and "0=" in cells[3]
        and "--selftest" in cells[4]
        and "exec-quality-gate" in cells[5]
        and "read-only" in cells[6]
        and cells[7] == "kake"
    )

def run_checks(root: str, rev: str) -> tuple[int, dict]:
    skill_raw = show(root, rev, SKILL)
    lesson_raw = show(root, rev, LESSON)
    spotcheck_raw = show(root, rev, SPOTCHECK)
    manifest_raw = show(root, rev, MANIFEST)
    spec_raw = show(root, rev, WAVE_SPEC)
    if any(raw is None for raw in (skill_raw, lesson_raw, spotcheck_raw, spec_raw)):
        return 2, {"registry": "unevaluable", "manifest": "unevaluable", "uncovered": "?"}
    skill = skill_raw.decode("utf-8", errors="replace")
    lesson = lesson_raw.decode("utf-8", errors="replace")
    spotcheck = spotcheck_raw.decode("utf-8", errors="replace")
    try:
        spec = json.loads(spec_raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return 2, {"registry": "unevaluable", "manifest": "unevaluable", "uncovered": "?"}
    if not isinstance(spec, dict) or not isinstance(spec.get("items"), list):
        return 2, {"registry": "unevaluable", "manifest": "unevaluable", "uncovered": "?"}
    tree = git(root, "ls-tree", "-r", "--name-only", rev, "--", REPORT_DIR)
    if tree.returncode != 0:
        return 2, {"registry": "unevaluable", "manifest": "unevaluable", "uncovered": "?"}
    committed_reports = [path for path in tree.stdout.decode("utf-8", errors="replace").splitlines()
                         if path.endswith(".md")]

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
            registry_present = registry_row_ok(line)
            break

    missing_manifest = manifest_raw is None
    manifest = "" if missing_manifest else manifest_raw.decode("utf-8", errors="replace")
    cited = cited_names(lesson, spotcheck)
    rows = MANIFEST_ROW_RE.findall(manifest)
    settled = {name for name, _, reason in rows if reason.strip()}
    uncovered = sorted(cited - settled)
    declared_40 = len(spec["items"]) == 40 and bool(re.search(r"\b40\s+spawned\b", spotcheck, re.I))
    manifest_40_0 = (bool(re.search(r"\b40\s+spawned\b", manifest, re.I))
                     and bool(re.search(r"\b0\s+committed\s+seat\s+reports\b", manifest, re.I)))
    has_loss_basis = declared_40 and not committed_reports and manifest_40_0
    settled_required = REQUIRED_SEAT_NAMES <= settled
    unique_required = all(sum(1 for name, _, _ in rows if name == required) == 1
                          for required in REQUIRED_SEAT_NAMES)
    rows_match_tree = all(
        bool(reason.strip()) and
        ((state == "lost" and show(root, rev, f"{REPORT_DIR}/{name}") is None) or
         (state == "resolved" and show(root, rev, f"{REPORT_DIR}/{name}") is not None))
        for name, state, reason in rows
    )
    manifest_ok = (not missing_manifest and not uncovered and settled_required
                   and unique_required and rows_match_tree and has_loss_basis)
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
    parser = UsageParser(description="Round-54 round-53 ops-debt counter")
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
