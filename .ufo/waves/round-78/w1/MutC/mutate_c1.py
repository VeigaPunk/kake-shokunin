#!/usr/bin/env python3
"""Mutation harness for c78_shonen_population.py (C1 counter).

For each mutant: restore pristine tree, apply one textual mutation (anchor must
match exactly once), run the instrument's `--selftest` (its bounded behavioural
detector), record stdout/exit, then restore pristine bytes and verify sha256.
"""
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

S = Path("/fast/scratch/hyaku/kake-r78/MutC")
BASE = S / "base"
TREE = S / "tree"
REL = ".ufo/waves/round-78/c78_shonen_population.py"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


MUTANTS = [
    dict(id="m01", name="count undeclared rows as matching",
         old="""        if not isinstance(spec, dict):
            undeclared.append(row.get("box"))
            continue
        declared += 1""",
         new="""        if not isinstance(spec, dict):
            declared += 1
            continue
        declared += 1"""),
    dict(id="m02", name="compare declared population with < instead of !=",
         old="""        if spec.get("count") != derived:""",
         new="""        if isinstance(spec.get("count"), int) and spec["count"] < derived:"""),
    dict(id="m03", name="grade count_at_least floors exactly (no tolerance)",
         old="""            (growth if derived > recorded else floors).append(f)""",
         new="""            floors.append(f)"""),
    dict(id="m04", name="grade no_match with the floor rule",
         old="""        if kind == "count_at_least" and m:""",
         new="""        if kind in ("count_at_least", "no_match") and m:"""),
    dict(id="m05", name="skip the rows == 4 conjunct",
         old="""declared == ROWS_EXPECTED and len(rows) == ROWS_EXPECTED""",
         new="""declared == ROWS_EXPECTED"""),
    dict(id="m06", name="ignore the c77 findings entirely",
         old="""classify(ledger, c77.get("findings") or [])""",
         new="""classify(ledger, [])"""),
    dict(id="m07", name="drop the population suffix filter",
         old="""        names = [n for n in names if n.endswith(suffix)]""",
         new="""        pass"""),
    dict(id="m08", name="drop the population exclude filter",
         old="""        names = [n for n in names if not any(fnmatch.fnmatch(Path(n).name, pat) for pat in excl)]""",
         new="""        pass"""),
]


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=600)


def main() -> int:
    pristine = (BASE / REL).read_bytes()
    pristine_sha = sha(pristine)
    baseline_work = S / "work-c1-baseline"
    baseline_work.mkdir(exist_ok=True)
    baseline = run([sys.executable, "-B", REL, "--selftest", "--work", str(baseline_work)], BASE)
    print(baseline.stdout, end="")
    assert baseline.returncode == 0
    results = []
    for m in MUTANTS:
        # restore pristine tree
        if TREE.exists():
            shutil.rmtree(TREE)
        shutil.copytree(BASE, TREE)
        tgt = TREE / REL
        txt = tgt.read_text()
        n = txt.count(m["old"])
        if n != 1:
            results.append({"id": m["id"], "name": m["name"],
                            "error": f"anchor matched {n} times", "verdict": "HARNESS-ERROR"})
            continue
        tgt.write_text(txt.replace(m["old"], m["new"]))
        work = S / "work-c1" / m["id"]
        if work.exists():
            shutil.rmtree(work)
        work.mkdir(parents=True)
        p = run([sys.executable, "-B", REL, "--selftest", "--work", str(work)], TREE)
        mutated_sha = sha(tgt.read_bytes())
        # restore exact bytes, verify
        tgt.write_bytes(pristine)
        restored = sha(tgt.read_bytes())
        restored_run = run([sys.executable, "-B", REL, "--selftest", "--work", str(work)], TREE)
        fail_lines = [ln.strip() for ln in p.stdout.splitlines() if ln.strip().startswith("FAIL")]
        summary = [ln.strip() for ln in p.stdout.splitlines() if ln.startswith("selftest:")]
        results.append({
            "id": m["id"], "name": m["name"], "rc": p.returncode,
            "summary": summary[0] if summary else None,
            "fails": fail_lines,
            "verdict": "KILLED" if p.returncode != 0 else "SURVIVED",
            "restored_sha256": restored, "restored_ok": restored == pristine_sha,
            "mutated_sha256": mutated_sha, "restored_rc": restored_run.returncode,
            "restored_output": restored_run.stdout,
            "stderr_tail": p.stderr.strip().splitlines()[-2:] if p.stderr.strip() else [],
        })
        print(json.dumps(results[-1]))
    out = S / "results-c1.json"
    out.write_text(json.dumps({"pristine_sha256": pristine_sha, "mutants": results}, indent=1))
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
