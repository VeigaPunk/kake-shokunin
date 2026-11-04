#!/usr/bin/env python3
"""c78_shonen_population.py — kake round 78, claim C1 (calibration).

Measures, from committed bytes at one revision, two things the round-77 ledger
left implicit:

1. the POPULATION every row was measured over is recorded and re-derives from
   the tree at the revision (round 77 kept it in prose, and one note was stale);
2. every recorded observation is consistent under the frozen grading rule:
   `count_at_least` observations are dated floors (growth is not drift,
   shrinkage is), every other observation is exact.

Frozen predicate (contract §C1, frozen before any after-state):

    met <=> rows_with_population == 4
        and stale_populations == 0
        and exact_mismatches == 0
        and floor_violations == 0

`exact_mismatches` and the `count_at_least` growth findings come from the
round-77 counter, which stays the measure authority for every recorded
observation; this counter adds the population layer and the floor grading.

Exit: 0 met · 1 measured defect · 2 unevaluable input · 64 usage.
Read-only: writes nothing outside the optional --work scratch directory.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

LEDGER_REL = "corpus/knowledge/shonen-ledger.json"
C77_REL = ".ufo/waves/round-77/c77_shonen_ledger.py"
ROWS_EXPECTED = 4


class Unevaluable(Exception):
    pass


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def git_show(root: Path, rev: str, rel: str):
    p = run(["git", "-C", str(root), "show", f"{rev}:{rel}"])
    if p.returncode != 0:
        return None
    return p.stdout


def derive_population(root: Path, rev: str, spec: dict) -> int:
    kind = spec.get("kind")
    if kind == "file":
        p = run(["git", "-C", str(root), "cat-file", "-e", f"{rev}:{spec.get('path')}"])
        return 1 if p.returncode == 0 else 0
    if kind == "files":
        d = spec.get("dir", "")
        p = run(["git", "-C", str(root), "ls-tree", "-r", "--name-only", rev, "--", d])
        if p.returncode != 0:
            raise Unevaluable(f"git ls-tree {rev}:{d} failed: {p.stderr.strip()}")
        names = [n for n in p.stdout.splitlines() if n.strip()]
        suffix = spec.get("suffix", "")
        names = [n for n in names if n.endswith(suffix)]
        excl = spec.get("exclude") or []
        names = [n for n in names if not any(fnmatch.fnmatch(Path(n).name, pat) for pat in excl)]
        return len(names)
    raise Unevaluable(f"unknown population kind {spec.get('kind')!r}")


def c77_findings(root: Path, rev: str):
    raw_tool = git_show(root, rev, C77_REL)
    if raw_tool is None:
        raise Unevaluable(f"round-77 counter absent at {rev}:{C77_REL}")
    with tempfile.TemporaryDirectory(prefix="kake-c78-c77-") as tmp:
        tool = Path(tmp) / "c77.py"
        tool.write_text(raw_tool)
        p = run([sys.executable, "-B", str(tool), "--root", str(root), "--revision", rev, "--json"])
    raw = p.stdout
    start = raw.find("{")
    if start < 0:
        raise Unevaluable(f"round-77 counter emitted no JSON (rc={p.returncode})")
    try:
        data = json.loads(raw[start:])
    except json.JSONDecodeError as e:
        raise Unevaluable(f"round-77 counter emitted no JSON (rc={p.returncode}): {e}: {raw[:300]}")
    if "findings" not in data:
        raise Unevaluable("round-77 JSON carries no findings list")
    return data


DIFF_RE = re.compile(r"recorded (-?\d+) but re-derived (-?\d+)")


def classify(ledger: dict, findings: list[dict]):
    """Split c77 findings into exact defects, tolerated growth, floor violations."""
    kinds = {}
    for row in ledger.get("rows") or []:
        for chk in row.get("checks") or []:
            kinds[chk.get("id")] = chk.get("kind")
    exact, growth, floors = [], [], []
    for f in findings:
        if f.get("class") != "observation-differs":
            exact.append(f)
            continue
        subject = f.get("subject") or ""
        m = DIFF_RE.search(f.get("detail") or "")
        cid = subject.split()[-1] if subject.split() else ""
        kind = kinds.get(cid)
        if kind == "count_at_least" and m:
            recorded, derived = int(m.group(1)), int(m.group(2))
            (growth if derived > recorded else floors).append(f)
        else:
            exact.append(f)
    return exact, growth, floors


def measure(root: Path, rev: str):
    raw = git_show(root, rev, LEDGER_REL)
    if raw is None:
        raise Unevaluable(f"ledger unreadable at {rev}:{LEDGER_REL}")
    try:
        ledger = json.loads(raw)
    except json.JSONDecodeError as e:
        raise Unevaluable(f"ledger not JSON at {rev}: {e}")
    rows = ledger.get("rows") or []
    declared, undeclared, stale = 0, [], []
    for row in rows:
        spec = row.get("population")
        if not isinstance(spec, dict):
            undeclared.append(row.get("box"))
            continue
        declared += 1
        derived = derive_population(root, rev, spec)
        if spec.get("count") != derived:
            stale.append({"box": row.get("box"), "declared": spec.get("count"), "derived": derived})
    c77 = c77_findings(root, rev)
    exact, growth, floors = classify(ledger, c77.get("findings") or [])
    if c77.get("boxes") != 4 or c77.get("unexamined") != 0:
        exact.append({"class": "checklist-population", "subject": "SHONEN.md",
                      "detail": "four examined checklist boxes required"})
    met = (declared == ROWS_EXPECTED and len(rows) == ROWS_EXPECTED
           and not undeclared and not stale and not exact and not floors)
    return {"revision": rev, "rows": len(rows), "rows_with_population": declared,
            "undeclared": undeclared, "stale": stale, "exact": exact,
            "growth": growth, "floors": floors, "met": met}


def emit(res: dict) -> int:
    print(f"C1v1 revision={res['revision']} rows={res['rows']} "
          f"rows_with_population={res['rows_with_population']} "
          f"undeclared={len(res['undeclared'])} stale_populations={len(res['stale'])} "
          f"exact_mismatches={len(res['exact'])} floor_violations={len(res['floors'])} "
          f"growth_tolerated={len(res['growth'])} met={str(res['met']).lower()}")
    for s in res["stale"]:
        print(f"  S1 box {s['box']}: declared={s['declared']} derived={s['derived']}")
    for b in res["undeclared"]:
        print(f"  S2 box {b}: no population declaration")
    for f in res["exact"]:
        print(f"  S3 exact: {f.get('class')} {f.get('subject')}: {f.get('detail')}")
    for f in res["floors"]:
        print(f"  S4 floor: {f.get('detail')}")
    for f in res["growth"]:
        print(f"  tolerated growth: {f.get('detail')}")
    return 0 if res["met"] else 1


# ── selftest (fixture repo, no commit outside the scratch dir) ─────────────
def _fixture(d: Path, files: dict, ledger: dict, findings: list[dict], prestine: bool = False):
    (d / "corpus/knowledge").mkdir(parents=True, exist_ok=True)
    for rel, body in files.items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body)
    (d / LEDGER_REL).write_text(json.dumps(ledger, indent=1))
    stub = d / C77_REL
    stub.parent.mkdir(parents=True, exist_ok=True)
    stub.write_text("import json\nprint(json.dumps({'boxes': 4, 'unexamined': 0, 'findings': %s}))\n" % json.dumps(findings))
    env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t",
           "PATH": "/usr/bin:/bin", "HOME": str(d)}
    run(["git", "init", "-q", str(d)])
    run(["git", "-C", str(d), "add", "-A"])
    subprocess.run(["git", "-C", str(d), "commit", "-qm", "fixture"], env=env,
                   capture_output=True, text=True)
    top = run(["git", "-C", str(d), "rev-parse", "--show-toplevel"])
    if Path(top.stdout.strip()).resolve() != d.resolve():
        raise SystemExit("selftest fixture toplevel mismatch — refusing to run")
    rev = run(["git", "-C", str(d), "rev-parse", "HEAD"]).stdout.strip()
    return rev


def _popfiles(n, kind="files"):
    if kind == "file":
        return {"kind": "file", "path": "SKILL.md", "count": 1}
    return {"kind": "files", "dir": "corpus/knowledge", "suffix": ".md", "exclude": [], "count": n}


def _four(n=2):
    counts = {"box": 2, "checks": [
        {"id": "b2-rounds", "kind": "count_at_least", "observed": 5},
        {"id": "b2-missing", "kind": "no_match", "observed": 0}]}
    return [{"box": 1, "population": _popfiles(1, "file")},
            dict(counts, population=_popfiles(1, "file")),
            {"box": 3, "population": _popfiles(1, "file")},
            {"box": 4, "population": _popfiles(n)}]


def selftest(work: Path) -> int:
    base_files = {"corpus/knowledge/a.md": "x", "corpus/knowledge/b.md": "y", "SKILL.md": "s"}
    cases = []
    cases.append(("s1 all declared and matching", base_files, _four(2), [], True))
    st = _four(2)
    st[3]["population"]["count"] = 3
    cases.append(("s2 stale population is red", base_files, st, [], False))
    und = _four(2)
    del und[3]["population"]
    cases.append(("s3 undeclared population is red", base_files, und, [], False))
    ex = _four(2)
    ex[3]["population"] = _popfiles(1)
    ex[3]["population"]["exclude"] = ["b.md"]
    cases.append(("s4 exclude honoured", base_files, ex, [], True))
    cases.append(("s5 count_at_least growth tolerated", base_files, _four(2),
                  [{"class": "observation-differs", "subject": "box 2 b2-rounds",
                    "detail": "recorded 5 but re-derived 6"}], True))
    cases.append(("s6 count_at_least shrinkage is red", base_files, _four(2),
                  [{"class": "observation-differs", "subject": "box 2 b2-rounds",
                    "detail": "recorded 6 but re-derived 5"}], False))
    cases.append(("s7 exact no_match drift is red", base_files, _four(2),
                  [{"class": "observation-differs", "subject": "box 2 b2-missing",
                    "detail": "recorded 0 but re-derived 1"}], False))
    cases.append(("s8 schema finding is red", base_files, _four(2),
                  [{"class": "row-invalid", "subject": "ledger", "detail": "bad row"}], False))
    cases.append(("s9 fewer than four rows is red", base_files, _four(2)[:3], [], False))
    results = []
    for cid, files, rows, findings, expect in cases:
        with tempfile.TemporaryDirectory(dir=str(work)) as td:
            d = Path(td) / "fx"
            d.mkdir()
            rev = _fixture(d, files, {"schema": "shonen-ledger/v1", "rows": rows}, findings)
            try:
                res = measure(d, rev)
                ok = res["met"] == expect
                msg = (f"met={res['met']} stale={len(res['stale'])} "
                       f"undeclared={len(res['undeclared'])} exact={len(res['exact'])} "
                       f"floors={len(res['floors'])} growth={len(res['growth'])}")
            except Unevaluable as e:
                ok, msg = False, f"unevaluable: {e}"
        results.append((cid, ok, msg))
    for cid, ok, msg in results:
        print(f"  {'PASS' if ok else 'FAIL'} {cid}: {msg}")
    bad = sum(1 for r in results if not r[1])
    print(f"selftest: {len(results) - bad}/{len(results)} passed")
    return 0 if bad == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--work", default=None)
    ap.add_argument("--help", action="store_true")
    a = ap.parse_args()
    if a.help:
        print(__doc__)
        return 0
    root = Path(a.root).resolve()
    if a.selftest:
        work = Path(a.work or tempfile.mkdtemp(prefix="c78pop-"))
        work.mkdir(parents=True, exist_ok=True)
        return selftest(work)
    if not a.revision:
        print("C1v1 error=--revision required")
        return 64
    try:
        return emit(measure(root, a.revision))
    except Unevaluable as e:
        print(f"C1v1 error={e}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
