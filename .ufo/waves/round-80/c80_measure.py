#!/usr/bin/env python3
"""Round-80 C2 counter — `unavailable_after` date shapes (kake, operability).

Runs the frozen round-79 matrix counter twice over the same tool revision: once over the frozen
31-case round-79 set (the no-regression conjunct) and once over this round's 12-case set
(`cases/`, oracle `expect/expect.json`, the four frozen constants of `.ufo/waves/round-79/consts`).

Frozen predicate (contract §C2):

    met <=> frozen wrong=0 and a2 wrong=0 and constants_failed=4/4 in both runs and selftest_ok=true in both runs

Exit: 0 met, 1 not met, 2 unevaluable, 64 usage. Read-only outside --work.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
MATRIX = HERE.parent / "round-79" / "c79_xrt_matrix.py"
CONSTS = HERE.parent / "round-79" / "consts"
FROZEN_CASES = HERE.parent / "round-79" / "cases"
FROZEN_EXPECT = HERE.parent / "round-79" / "expect" / "expect.json"

LINE = re.compile(
    r"revision=(?P<rev>\S+).*?cases=(?P<cases>\d+) decided=(?P<decided>\d+) correct=(?P<correct>\d+) "
    r"wrong=(?P<wrong>\d+) undecided=(?P<undecided>\d+) constants_failed=(?P<cf>\d+)/(?P<cn>\d+) "
    r"selftest_ok=(?P<st>true|false) .*?met=(?P<met>true|false)")


def run_matrix(work: Path, label: str, root: Path, revision: str | None, cases: Path,
               expect: Path, tool: str | None) -> dict:
    argv = [sys.executable, "-B", str(MATRIX), "--root", str(root),
            "--cases", str(cases), "--expect", str(expect), "--consts", str(CONSTS),
            "--work", str(work / label)]
    if revision:
        argv += ["--tool-revision", revision]
    else:
        argv += ["--tool", tool or ""]
    p = subprocess.run(argv, capture_output=True, text=True, timeout=900)
    text = p.stdout + p.stderr
    m = LINE.search(text)
    if not m:
        return {"label": label, "ok": False, "rc": p.returncode, "why": text.strip()[-300:], "met": False}
    d = {k: (int(v) if v.isdigit() else v) for k, v in m.groupdict().items()}
    ok = (d["wrong"] == 0 and d["undecided"] == 0 and d["decided"] == d["cases"]
          and d["cf"] == d["cn"] == 4 and d["st"] == "true")
    return {"label": label, "ok": ok, "rc": p.returncode, "cases": d["cases"],
            "wrong": d["wrong"], "decided": d["decided"], "constants": f"{d['cf']}/{d['cn']}",
            "selftest_ok": d["st"] == "true", "met": d["met"] == "true", "detail": text.strip()[-400:]}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision")
    ap.add_argument("--tool", help="pre-commit worktree run")
    ap.add_argument("--work")
    a = ap.parse_args()
    root = Path(a.root).resolve()
    if bool(a.revision) == bool(a.tool):
        print("usage: exactly one of --revision / --tool is required", file=sys.stderr)
        return 64
    work = Path(a.work) if a.work else Path(tempfile.mkdtemp(prefix="kake-c80-measure-"))
    work.mkdir(parents=True, exist_ok=True)
    owned = a.work is None
    try:
        runs = [
            run_matrix(work, "frozen", root, a.revision, FROZEN_CASES, FROZEN_EXPECT, a.tool),
            run_matrix(work, "a2", root, a.revision, HERE / "cases", HERE / "expect" / "expect.json", a.tool),
        ]
        for r in runs:
            print(f"{r['label']}: cases={r.get('cases')} decided={r.get('decided')} "
                  f"wrong={r.get('wrong')} constants={r.get('constants')} "
                  f"selftest_ok={str(r.get('selftest_ok')).lower()} ok={r['ok']}")
            if not r["ok"]:
                print(f"  detail: {r['detail']}")
        if any(r.get("rc") == 2 for r in runs):
            print("exit=2")
            return 2
        met = all(r["ok"] for r in runs)
        label = a.revision or "worktree"
        print(f"C2v1 revision={label} frozen_cases={runs[0].get('cases')} frozen_wrong={runs[0].get('wrong')} "
              f"a2_cases={runs[1].get('cases')} a2_wrong={runs[1].get('wrong')} "
              f"constants={'+'.join(str(r.get('constants')) for r in runs)} "
              f"selftest={('ok' if all(r.get('selftest_ok') for r in runs) else 'failed')} "
              f"met={'true' if met else 'false'}")
        print(f"exit={0 if met else 1}")
        return 0 if met else 1
    finally:
        if owned:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
