#!/usr/bin/env python3
"""Build an extended C2 matrix whose expectations name id, page, resolved and
the report counts, for the round-30 M4 fix witness.

The frozen round-29 matrix names only attribute/element/reason/value in its
findings, and no counts at all.  A counter that compares only the expectation
keys therefore cannot see a wrong id, a wrong page, a wrong resolved URL or
wrong counts.  This script re-runs the real tool over every matrix case,
records the observed id/page/resolved and the counts, and writes a new matrix
whose expectations pin them.

Usage: python3 -B build_extended_matrix.py --root <repo> --revision <commit>
       --matrix <c2-matrix.json> --out <extended-matrix.json>
Exit 0 on success; 2 on unusable input.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

TIMEOUT = 20
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--revision", required=True)
    ap.add_argument("--matrix", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    matrix_path = Path(a.matrix)
    if not matrix_path.is_absolute():
        matrix_path = Path(a.root) / a.matrix
    matrix = json.loads(matrix_path.read_text())
    cases = matrix["cases"]
    commit = resolve(a.root, a.revision)
    if commit is None:
        print("revision not found")
        return 2
    blob = git_show(a.root, commit, "scripts/base_path_audit.py")
    if blob is None:
        print("tool not found")
        return 2

    extended = []
    with tempfile.TemporaryDirectory(prefix="kake-r30-m4-matrix-") as tmp:
        scratch = Path(tmp)
        tool = scratch / "base_path_audit.py"
        tool.write_bytes(blob)
        for case in cases:
            new_case = dict(case)
            expect = dict(case["expect"])
            work = materialize(case, scratch / "cases")
            argv = case.get("argv")
            args = argv if argv is not None else ["--manifest", str(work / "manifest.json")]
            env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": str(scratch),
                   "LC_ALL": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}
            proc = subprocess.run([sys.executable, "-B", str(tool), *args], cwd=work,
                                  capture_output=True, text=True, timeout=TIMEOUT, env=env)
            expect["exit"] = proc.returncode
            if proc.returncode != 64:
                try:
                    report = json.loads(proc.stdout)
                except ValueError:
                    report = {}
                expect["verdict"] = report.get("verdict")
                for key in COUNT_KEYS:
                    expect[key] = report.get(key)
                findings = []
                for f in report.get("findings") or []:
                    findings.append({k: f.get(k) for k in FINDING_KEYS})
                expect["findings"] = findings
            else:
                expect["verdict"] = None
                expect["findings"] = None
            new_case["expect"] = expect
            new_case["note"] = (case.get("note") or "") + " [r30 extended: id/page/resolved and counts pinned]"
            extended.append(new_case)

    out = {"matrixSha256": None, "cases": extended}
    text = json.dumps(out, indent=1, ensure_ascii=False) + "\n"
    Path(a.out).write_text(text, encoding="utf-8")
    import hashlib
    print(json.dumps({"out": a.out, "cases": len(extended),
                      "sha256": hashlib.sha256(text.encode()).hexdigest()}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
