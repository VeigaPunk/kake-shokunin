#!/usr/bin/env python3
"""Round-34 C1 counter: run the frozen link-preview matrix against one revision.

Derived from .ufo/waves/round-29/c2_matrix_count.py (sha256 62732c86...d273);
changes: matrix file and digest, tool path, the constant gates (a fourth,
constant-all-missing, emits the four og_required_missing findings), and names.

Reads scripts/link_preview_audit.py from `git show <revision>:...` (never the
working tree), materializes each case of the digest-pinned matrix next to this
file into a fresh temporary directory, runs the tool, and compares exit code,
verdict and finding (reason, property) tuples. It also runs four constant
gates over the same matrix; each must fail at least one case, so a counter
that a constant could satisfy is reported as broken.

Usage: python3 -B c1_matrix_count.py --root <lane> --revision <commit>
Exit 0 when every case passes and every constant gate is rejected; 1 otherwise;
2 on unusable input.
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
MATRIX = HERE / "c1-matrix.json"
MATRIX_SHA256 = "246a6a3ba67a842c408f56b0240d2ad36969330c5a414b715f04b7e56fac14f7"
TOOL = "scripts/link_preview_audit.py"
TIMEOUT = 20

_MISSING = ",".join('{"id":"x","reason":"og_required_missing","page":"p","property":"og:%s"}' % p
                    for p in ("title", "type", "image", "url"))
CONSTANTS = {
    "constant-clean": 'import json;print(json.dumps({"verdict":"clean","pagesChecked":0,"findings":[]}))',
    "constant-failed-empty": 'import json,sys;print(json.dumps({"verdict":"failed-policy","pagesChecked":0,"findings":[]}));sys.exit(1)',
    "constant-refuse": 'import json,sys;print(json.dumps({"verdict":"could-not-evaluate","pagesChecked":0,"findings":[{"id":"x","reason":"input_invalid"}]}));sys.exit(2)',
    "constant-all-missing": 'import sys;print(\'{"verdict":"failed-policy","pagesChecked":1,"findings":[' + _MISSING + ']}\');sys.exit(1)',
}


def git_show(root: str, revision: str, path: str) -> bytes | None:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    proc = subprocess.run(["git", "-C", root, "show", f"{revision}:{path}"], capture_output=True, env=env)
    return proc.stdout if proc.returncode == 0 else None


def resolve(root: str, revision: str) -> str | None:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    proc = subprocess.run(["git", "-C", root, "rev-parse", "--verify", "--quiet", f"{revision}^{{commit}}"],
                          capture_output=True, text=True, env=env)
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
    exp, obs = [], []
    keys = sorted({k for f in expected for k in f}) or ["reason"]
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
            env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": str(scratch), "LC_ALL": "C.UTF-8",
                   "PYTHONDONTWRITEBYTECODE": "1"}
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
    a = ap.parse_args()
    raw = MATRIX.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != MATRIX_SHA256:
        print(json.dumps({"error": "matrix digest mismatch", "observed": digest, "pinned": MATRIX_SHA256}))
        return 2
    cases = json.loads(raw)["cases"]
    commit = resolve(a.root, a.revision)
    if commit is None:
        print(json.dumps({"error": "revision not found", "revision": a.revision}))
        return 2
    blob = git_show(a.root, commit, TOOL)
    with tempfile.TemporaryDirectory(prefix="kake-r34-c1-") as tmp:
        scratch = Path(tmp)
        tool = None
        if blob is not None:
            tool = scratch / "link_preview_audit.py"
            tool.write_bytes(blob)
        rows = run_matrix(tool, cases, scratch)
        constants = {}
        for name, code in CONSTANTS.items():
            cpath = scratch / f"{name}.py"
            cpath.write_text(code + "\n", encoding="utf-8")
            crow = run_matrix(cpath, cases, scratch)
            constants[name] = sum(r["passed"] for r in crow)
    passed = sum(r["passed"] for r in rows)
    by_kind = {}
    for r in rows:
        k = by_kind.setdefault(r["kind"], [0, 0])
        k[0] += r["passed"]
        k[1] += 1
    rejected = all(v < len(cases) for v in constants.values())
    out = {
        "counter": "kake-r34-c1-link-preview-matrix",
        "counterSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "revision": commit,
        "tool": TOOL,
        "toolPresent": blob is not None,
        "toolSha256": hashlib.sha256(blob).hexdigest() if blob is not None else None,
        "matrixSha256": digest,
        "passed": passed,
        "total": len(cases),
        "byKind": {k: f"{v[0]}/{v[1]}" for k, v in sorted(by_kind.items())},
        "constantGatesPassed": {k: f"{v}/{len(cases)}" for k, v in constants.items()},
        "constantGatesAllRejected": rejected,
        "cases": rows,
    }
    print(json.dumps(out, indent=1))
    print(f"C1 {passed}/{len(cases)} at {commit}", file=sys.stderr)
    return 0 if passed == len(cases) and rejected else 1


if __name__ == "__main__":
    sys.exit(main())
