#!/usr/bin/env python3
"""C3 mutants through the ROUND'S OWN matrix counter.

The matrix extracts `scripts/meta_robots_audit.py` from a git revision, so a
throwaway fixture repo is built under scratch, and each mutant is committed
there as its own revision. Pristine baseline first; bytes restored and
sha256-verified after every mutant.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mutate_c3 import MUTANTS, LANE, S, sha  # noqa: E402

FIX = S / "mx-fixture"
MATRIX = LANE / ".ufo/waves/round-78/c78_meta_robots_matrix.py"
CASES = LANE / ".ufo/waves/round-78/cases"
CONSTS = LANE / ".ufo/waves/round-78/consts"
TOOL_REL = "scripts/meta_robots_audit.py"
ENV = dict(os.environ, GIT_AUTHOR_NAME="mut", GIT_AUTHOR_EMAIL="mut@example.invalid",
           GIT_COMMITTER_NAME="mut", GIT_COMMITTER_EMAIL="mut@example.invalid")


def git(args, cwd=FIX):
    p = subprocess.run(["git", "-C", str(cwd)] + args, capture_output=True,
                       text=True, env=ENV)
    if p.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed: {p.stderr}")
    return p.stdout


def init_fixture(pristine: bytes):
    if FIX.exists():
        shutil.rmtree(FIX)
    (FIX / "scripts").mkdir(parents=True)
    (FIX / TOOL_REL).write_bytes(pristine)
    git(["init", "-q"])
    top = git(["rev-parse", "--show-toplevel"]).strip()
    if Path(top).resolve() != FIX.resolve():
        raise SystemExit(f"fixture toplevel mismatch: {top}")
    git(["add", "-A"])
    git(["commit", "-qm", "pristine tool"])


def commit():
    git(["add", "-A"])
    git(["commit", "-qm", "mutant"])


def matrix(tag: str):
    work = S / "mx-work" / tag
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    p = subprocess.run(
        [sys.executable, "-B", str(MATRIX), "--root", str(FIX),
         "--tool-revision", "HEAD", "--cases", str(CASES),
         "--consts", str(CONSTS), "--work", str(work)],
        capture_output=True, text=True, timeout=1800)
    verdict = next((l for l in p.stdout.splitlines() if l.startswith("C3v1")), None)
    wrong = [l.strip() for l in p.stdout.splitlines()
             if l.strip().startswith("case ") and ("wrong" in l or "FAIL" in l)]
    return {"rc": p.returncode, "verdict": verdict, "wrong_lines": wrong[:20],
            "stderr_tail": p.stderr.strip().splitlines()[-3:] if p.stderr.strip() else []}


def main() -> int:
    pristine_path = LANE / TOOL_REL
    pristine = pristine_path.read_bytes()
    psha = sha(pristine)
    cases_sha = hashlib.sha256(b"".join(
        sorted(p.name.encode() for p in CASES.iterdir() if p.is_dir()))).hexdigest()[:16]
    init_fixture(pristine)
    base = matrix("pristine")
    print(json.dumps({"baseline": base}))
    results = []
    for mu in MUTANTS:
        text = pristine.decode()
        ok = True
        for old, new in mu["edits"]:
            n = text.count(old)
            if n != 1:
                results.append({"id": mu["id"], "name": mu["name"],
                                "error": f"anchor matched {n}x", "verdict": "HARNESS-ERROR"})
                ok = False
                break
            text = text.replace(old, new)
        if not ok:
            continue
        (FIX / TOOL_REL).write_text(text)
        commit()
        mx = matrix(mu["id"])
        killed = mx["rc"] != 0
        results.append({"id": mu["id"], "name": mu["name"], "matrix": mx,
                        "verdict": "KILLED" if killed else "SURVIVED"})
        print(json.dumps({"id": mu["id"], "verdict": results[-1]["verdict"],
                          "verdict_line": mx["verdict"], "rc": mx["rc"],
                          "wrong": mx["wrong_lines"][:6]}))
        # restore pristine bytes in the fixture and commit it back
        (FIX / TOOL_REL).write_bytes(pristine)
        commit()
        if (FIX / TOOL_REL).read_bytes() != pristine:
            raise SystemExit("fixture restore failed")
    out = S / "results-c3-matrix.json"
    out.write_text(json.dumps({"instrument_sha256": psha, "cases_dirs": cases_sha,
                               "baseline": base, "mutants": results}, indent=1))
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
