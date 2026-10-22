#!/usr/bin/env python3
"""Witness for round-30 lesson mistake M4: the C2 counter compared no id,
page, resolved or counts.

The round-29 C2 counter (.ufo/waves/round-29/c2_matrix_count.py) compares a
finding by projecting the EXPECTED finding's keys onto the observed finding
(c2_matrix_count.py:62-73).  The frozen matrix expectations name only
attribute/element/reason/value, so the observed `id`, `page` and `resolved`
are never read; the report-level counts pagesChecked/referencesChecked are
never read at all; and the usage case is judged on the exit code alone
(c2_matrix_count.py:81-82 returns before stdout is parsed).

This witness measures that three ways, all offline:

  A. FIELD COVERAGE.  Reads the matrix, collects the key set the counter can
     possibly compare, and names the tool output fields and report counts it
     never compares.

  B. MUTANT A (wrong id/page/resolved/counts).  Builds a scratch git repo
     holding a mutant of scripts/base_path_audit.py whose finding `id`,
     `page` and `resolved` values and whose pagesChecked/referencesChecked
     counts are all wrong while exit code, verdict and reason codes are
     untouched, then runs the real counter against it.  If the counter still
     exits 0, those fields are demonstrably not compared.

  C. MUTANT B (usage case).  Builds a mutant whose usage path prints
     non-JSON to stdout and exits 64.  If the counter still passes the usage
     case, the usage case is graded on the exit code alone.

Usage: python3 -B witness_c2_field_comparison.py --root <lane>
       [--revision <commit>]
Exit 0 when the counter compares id, page, resolved and the counts; 1 when
it does not (the criterion fails); 2 on bad input.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

COUNTER = ".ufo/waves/round-29/c2_matrix_count.py"
MATRIX = ".ufo/waves/round-29/c2-matrix.json"
TOOL = "scripts/base_path_audit.py"
TOOL_FINDING_FIELDS = ("id", "reason", "page", "element", "attribute", "value", "resolved")
COUNT_FIELDS = ("pagesChecked", "referencesChecked")

MUTANT_A = [
    # wrong id, wrong page, wrong resolved on every policy finding
    ('"id": f"{page[\'file\']}#{index}:{element}[{attribute}]={value}",',
     '"id": "WRONG-ID",'),
    ('"page": page["url"],', '"page": "https://wrong.example/page",'),
    ('"resolved": serialize_url(record),', '"resolved": "https://wrong.example/resolved",'),
    # wrong report counts
    ('"pagesChecked": pages_checked,', '"pagesChecked": 999999,'),
    ('"referencesChecked": references_checked,', '"referencesChecked": 888888,'),
]

MUTANT_B = [
    # usage path prints non-JSON to stdout and still exits 64
    ('print(json.dumps(USAGE_RESULT, sort_keys=True, separators=(",", ":")))',
     'print("not json at all")'),
]


def git(root: str, *args: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(["git", "-C", root, *args], capture_output=True, env=env)


def show(root: str, rev: str, path: str) -> bytes | None:
    p = git(root, "show", "%s:%s" % (rev, path))
    return p.stdout if p.returncode == 0 else None


def field_coverage(root: str, rev: str) -> dict:
    raw = show(root, rev, MATRIX)
    if raw is None:
        return {"error": "matrix not found"}
    matrix = json.loads(raw.decode())
    compared = set()
    for case in matrix["cases"]:
        for finding in case["expect"].get("findings") or []:
            if isinstance(finding, dict):
                compared.update(finding.keys())
    # The counter projects the EXPECTED keys onto the observed finding, so the
    # comparable set is exactly the union of the expectation keys.
    never = [f for f in TOOL_FINDING_FIELDS if f not in compared]
    return {"matrixCases": len(matrix["cases"]),
            "fieldsTheCounterCompares": sorted(compared),
            "toolFindingFieldsNeverCompared": never,
            "reportCountsNeverCompared": list(COUNT_FIELDS)}


def make_mutant_repo(base_tool: bytes, edits: list[tuple[str, str]], label: str) -> tuple[str, str, dict]:
    """Build a scratch git repo holding the mutant tool. Returns (root, rev, info)."""
    tmp = tempfile.mkdtemp(prefix="kake-r30-m4-%s-" % label)
    repo = Path(tmp)
    (repo / "scripts").mkdir()
    text = base_tool.decode("utf-8")
    applied = []
    for old, new in edits:
        if old not in text:
            continue
        text = text.replace(old, new)
        applied.append(old.split("(")[0][:60])
    (repo / "scripts" / "base_path_audit.py").write_text(text, encoding="utf-8")
    env = dict(os.environ)
    env.update({"GIT_AUTHOR_NAME": "witness", "GIT_AUTHOR_EMAIL": "witness@local",
                "GIT_COMMITTER_NAME": "witness", "GIT_COMMITTER_EMAIL": "witness@local",
                "GIT_AUTHOR_DATE": "2026-10-22T00:00:00+00:00",
                "GIT_COMMITTER_DATE": "2026-10-22T00:00:00+00:00"})
    subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True, env=env)
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True, env=env)
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "mutant " + label],
                   check=True, env=env)
    rev = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                         capture_output=True, text=True, env=env).stdout.strip()
    return str(repo), rev, {"editsApplied": applied,
                            "editsRequested": len(edits)}


def run_counter(root: str, rev: str, counter_src: bytes, matrix_src: bytes) -> dict:
    """Run the round-29 counter (copied next to its matrix) against root@rev."""
    tmp = tempfile.mkdtemp(prefix="kake-r30-m4-run-")
    scratch = Path(tmp)
    (scratch / "c2_matrix_count.py").write_bytes(counter_src)
    (scratch / "c2-matrix.json").write_bytes(matrix_src)
    env = dict(os.environ)
    env["TMPDIR"] = tmp
    proc = subprocess.run([sys.executable, "-B", str(scratch / "c2_matrix_count.py"),
                           "--root", os.path.abspath(root), "--revision", rev],
                          capture_output=True, text=True, env=env, cwd=scratch)
    out = {"exit": proc.returncode}
    try:
        out["report"] = json.loads(proc.stdout)
    except ValueError:
        out["stdout"] = proc.stdout[:400]
        out["stderr"] = proc.stderr[:400]
    return out


def summarize(res: dict) -> dict:
    rep = res.get("report") or {}
    usage = [c for c in rep.get("cases", []) if c.get("kind") == "usage"]
    return {"exit": res.get("exit"), "passed": rep.get("passed"),
            "total": rep.get("total"),
            "usageCases": [{"id": c.get("id"), "passed": c.get("passed"),
                            "detail": c.get("detail")} for c in usage]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--revision", default="HEAD")
    a = ap.parse_args()
    rev = git(a.root, "rev-parse", "--verify", "--quiet", a.revision + "^{commit}")
    if rev.returncode != 0:
        print("revision not found: %s" % a.revision)
        return 2
    commit = rev.stdout.decode().strip()

    coverage = field_coverage(a.root, commit)
    if "error" in coverage:
        print(coverage["error"])
        return 2

    counter_src = show(a.root, commit, COUNTER)
    matrix_src = show(a.root, commit, MATRIX)
    tool_src = show(a.root, commit, TOOL)
    if counter_src is None or matrix_src is None or tool_src is None:
        print("counter, matrix or tool not found at %s" % commit)
        return 2

    baseline = summarize(run_counter(a.root, commit, counter_src, matrix_src))

    mut_a = {"ran": False}
    repo_a, rev_a, info_a = make_mutant_repo(tool_src, MUTANT_A, "fields")
    try:
        res_a = run_counter(repo_a, rev_a, counter_src, matrix_src)
        mut_a = {"ran": True, "label": "A: wrong id/page/resolved/counts",
                 **summarize(res_a), **info_a}
    finally:
        shutil.rmtree(repo_a, ignore_errors=True)

    mut_b = {"ran": False}
    repo_b, rev_b, info_b = make_mutant_repo(tool_src, MUTANT_B, "usage")
    try:
        res_b = run_counter(repo_b, rev_b, counter_src, matrix_src)
        mut_b = {"ran": True, "label": "B: usage prints non-JSON, exits 64",
                 **summarize(res_b), **info_b}
    finally:
        shutil.rmtree(repo_b, ignore_errors=True)

    gaps = list(coverage["toolFindingFieldsNeverCompared"]) + list(coverage["reportCountsNeverCompared"])
    never_compared = sorted(set(gaps))
    mutant_a_survived = bool(mut_a.get("ran") and mut_a.get("exit") == 0)
    usage_passed_on_exit_only = bool(
        mut_b.get("ran") and mut_b.get("exit") == 0
        and mut_b.get("usageCases") and all(c["passed"] for c in mut_b["usageCases"]))

    out = {"witness": "kake-r30-m4-c2-field-comparison", "revision": commit,
           "counter": COUNTER, "matrix": MATRIX,
           "fieldCoverage": coverage,
           "baselineCounterRun": baseline,
           "mutantACounterRun": mut_a,
           "mutantBCounterRun": mut_b,
           "fieldsNeverCompared": never_compared,
           "mutantASurvived": mutant_a_survived,
           "usageCasePassedOnExitCodeAlone": usage_passed_on_exit_only}
    print(json.dumps(out, indent=1))
    if never_compared or mutant_a_survived:
        print("M4 FAILS: the counter never compares %s%s"
              % (", ".join(never_compared),
                 "; mutant with wrong id/page/resolved/counts still scored %s/%s"
                 % (mut_a.get("passed"), mut_a.get("total"))
                 if mutant_a_survived else ""), file=sys.stderr)
        return 1
    print("M4 holds: the counter compares id, page, resolved and the counts",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
