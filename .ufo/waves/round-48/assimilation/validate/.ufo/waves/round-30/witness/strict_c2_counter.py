#!/usr/bin/env python3
"""Strict variant of the round-29 C2 counter, for the round-30 M4 fix.

Same matrix, same constant gates, but the per-case comparison also pins the
finding `id`, `page` and `resolved` values and the report-level counts, and
the usage case checks that stdout is one JSON object instead of trusting the
exit code alone.

This file exists to show that the M4 fix is able to fail: it must REJECT the
mutant tool that the shipped counter accepts.

Usage: python3 -B strict_c2_counter.py --root <repo> --revision <commit>
       --matrix <path to c2-matrix.json>
Exit 0 when every case passes and every constant gate is rejected; 1
otherwise; 2 on unusable input.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TIMEOUT = 20

CONSTANTS = {
    "constant-clean": 'import json;print(json.dumps({"verdict":"clean","pagesChecked":0,"referencesChecked":0,"findings":[]}))',
    "constant-failed-empty": 'import json,sys;print(json.dumps({"verdict":"failed-policy","pagesChecked":0,"referencesChecked":0,"findings":[]}));sys.exit(1)',
    "constant-refuse": 'import json,sys;print(json.dumps({"verdict":"could-not-evaluate","pagesChecked":0,"referencesChecked":0,"findings":[{"id":"x","reason":"input_invalid"}]}));sys.exit(2)',
}

FINDING_KEYS = ("reason", "element", "attribute", "value", "id", "page", "resolved")
COUNT_KEYS = ("pagesChecked", "referencesChecked")


def git_show(root: str, revision: str, path: str) -> bytes | None:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    proc = subprocess.run(["git", "-C", root, "show", f"{revision}:{path}"],
                          capture_output=True, env=env)
    return proc.stdout if proc.returncode == 0 else None


def resolve(root: str, revision: str) -> str | None:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    proc = subprocess.run(["git", "-C", root, "rev-parse", "--verify", "--quiet",
                           f"{revision}^{{commit}}"], capture_output=True, text=True, env=env)
    return proc.stdout.strip() if proc.returncode == 0 else None


def materialize(case: dict, base: Path) -> Path:
    work = base / case["id"]
    work.mkdir(parents=True)
    for rel, text in case["files"].items():
        target = work / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    return work


def project(expected: list[dict], observed: list) -> tuple[list, list]:
    """Compare on the full finding key set, not only the expected keys."""
    exp, obs = [], []
    keys = FINDING_KEYS
    for f in expected:
        exp.append(tuple(str(f.get(k)) for k in keys))
    for f in observed:
        if not isinstance(f, dict):
            obs.append(("<non-object>",))
            continue
        obs.append(tuple(str(f.get(k)) for k in keys))
    return sorted(exp), sorted(obs)


def judge(case: dict, proc: subprocess.CompletedProcess | None) -> tuple[bool, str]:
    exp = case["expect"]
    if proc is None:
        return False, "tool absent or timed out"
    if proc.returncode != exp["exit"]:
        return False, f"exit {proc.returncode} != {exp['exit']}"
    if exp["exit"] == 64:
        # The usage case is judged on the usage object, not the exit code.
        try:
            payload = json.loads(proc.stdout)
        except ValueError:
            return False, "usage stdout is not JSON"
        if not isinstance(payload, dict):
            return False, "usage stdout is not an object"
        if payload.get("verdict") != "could-not-evaluate":
            return False, f"usage verdict {payload.get('verdict')!r}"
        return True, "ok"
    try:
        report = json.loads(proc.stdout)
    except (ValueError, RecursionError):
        return False, "stdout is not JSON"
    if not isinstance(report, dict):
        return False, "report is not an object"
    if report.get("verdict") != exp["verdict"]:
        return False, f"verdict {report.get('verdict')!r} != {exp['verdict']!r}"
    findings = report.get("findings")
    if not isinstance(findings, list):
        return False, "findings is not a list"
    for key in COUNT_KEYS:
        if key in exp:
            if report.get(key) != exp[key]:
                return False, f"{key} {report.get(key)!r} != {exp[key]!r}"
    e, o = project(exp["findings"], findings)
    if e != o:
        return False, f"findings {o} != {e}"
    return True, "ok"


def run_matrix(tool_path: Path | None, cases: list[dict], scratch: Path) -> list[dict]:
    rows = []
    for case in cases:
        proc = None
        if tool_path is not None:
            work = materialize(case, scratch / tool_path.stem)
            argv = case.get("argv")
            args = argv if argv is not None else ["--manifest", str(work / "manifest.json")]
            env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": str(scratch),
                   "LC_ALL": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}
            try:
                proc = subprocess.run([sys.executable, "-B", str(tool_path), *args], cwd=work,
                                      capture_output=True, text=True, timeout=TIMEOUT, env=env)
            except subprocess.TimeoutExpired:
                proc = None
        ok, why = judge(case, proc)
        rows.append({"id": case["id"], "kind": case["kind"], "passed": ok, "detail": why})
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--revision", required=True)
    ap.add_argument("--matrix", required=True)
    a = ap.parse_args()
    matrix_path = Path(a.matrix)
    if not matrix_path.is_absolute():
        matrix_path = HERE / a.matrix
    raw = matrix_path.read_bytes()
    cases = json.loads(raw)["cases"]
    commit = resolve(a.root, a.revision)
    if commit is None:
        print(json.dumps({"error": "revision not found", "revision": a.revision}))
        return 2
    blob = git_show(a.root, commit, "scripts/base_path_audit.py")
    with tempfile.TemporaryDirectory(prefix="kake-r30-m4-strict-") as tmp:
        scratch = Path(tmp)
        tool = None
        if blob is not None:
            tool = scratch / "base_path_audit.py"
            tool.write_bytes(blob)
        rows = run_matrix(tool, cases, scratch)
        constants = {}
        for name, code in CONSTANTS.items():
            cpath = scratch / f"{name}.py"
            cpath.write_text(code + "\n", encoding="utf-8")
            constants[name] = sum(r["passed"] for r in run_matrix(cpath, cases, scratch))
    passed = sum(r["passed"] for r in rows)
    rejected = all(v < len(cases) for v in constants.values())
    print(json.dumps({"counter": "kake-r30-m4-strict-c2", "revision": commit,
                      "passed": passed, "total": len(cases),
                      "constantGatesPassed": constants,
                      "constantGatesAllRejected": rejected,
                      "failed": [r for r in rows if not r["passed"]]}, indent=1))
    return 0 if passed == len(cases) and rejected else 1


if __name__ == "__main__":
    sys.exit(main())
