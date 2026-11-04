#!/usr/bin/env python3
"""c78_sweep_truth.py — kake round 78, claim C2 (freshness).

Runs the lane's standing freshness gate (`scripts/freshness-sweep.mjs
--offline`) over the **archived bytes of the named revision** — never the
mutable worktree — reads its JSON verdict, and proves the gate was not loosened
by the round's citation repair: the negative control is a second extraction of
the same revision with one planted unannotated citation of an absent target,
and it must come back red.

Frozen predicate (contract §C2, frozen before any after-state):

    met <=> sweep_exit == 0 and drift == 0 and new_missing == 0 and paths_ok
        and control_exit == 1 and control_drift >= 1

Offline is declared: §armed remote checks are skipped and §history is suspended
by pin; neither is counted as a pass. The claim is about the evaluated §paths
section only.

Exit: 0 met · 1 measured defect · 2 unevaluable input · 64 usage.
Scratch: every temporary tree lives under --work (never /tmp) and is removed.
"""
from __future__ import annotations

import argparse
import json
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SWEEP_REL = "scripts/freshness-sweep.mjs"
CONTROL_REL = "corpus/lessons/ctl-r78-unannotated-miss.md"
CONTROL_BODY = (
    "# round-78 negative control (scratch only)\n\n"
    "This file is a scratch fixture. It cites an absent target with no absence\n"
    "annotation, so the sweep's §paths check must report drift.\n\n"
    "See `~/Projects/kake-r78-control-absent/nothing-here.md` for detail.\n"
)


class Unevaluable(Exception):
    pass


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def sweep(root: Path, timeout: int):
    node = shutil.which("node")
    if not node:
        raise Unevaluable("node not on PATH")
    p = run([node, str(root / SWEEP_REL), "--offline", "--json", "--repo", str(root)], cwd=root)
    out = p.stdout
    start = out.find("{")
    if start < 0:
        raise Unevaluable(f"sweep emitted no JSON (rc={p.returncode}): {out[:200]} {p.stderr[:200]}")
    try:
        data = json.loads(out[start:])
    except json.JSONDecodeError as e:
        raise Unevaluable(f"sweep JSON unreadable: {e}")
    return p.returncode, data


def decide(exit_code: int, data: dict):
    paths = (data.get("sections") or {}).get("paths") or {}
    counts = paths.get("counts") or {}
    return {
        "sweep_exit": exit_code,
        "code": data.get("code"),
        "drift": counts.get("drift"),
        "new_missing": counts.get("newMissing"),
        "paths_ok": bool(paths.get("ok")),
        "skipped": len(data.get("skipped") or []),
        "reasons": data.get("reasons") or [],
    }


def extract(root: Path, rev: str, dest: Path):
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    proc = subprocess.run(
        f"git -C {root} archive {rev} | tar -x -C {dest}",
        shell=True, capture_output=True, text=True)
    if proc.returncode != 0:
        raise Unevaluable(f"git archive {rev} failed: {proc.stderr.strip()}")
    if not (dest / SWEEP_REL).exists():
        raise Unevaluable(f"archive of {rev} carries no {SWEEP_REL}")
    return dest


def tree_identity(dirpath: Path) -> str:
    """Hash of the measurable inputs (the source files the sweep reads)."""
    h = hashlib.sha256()
    for rel in ("SKILL.md", "corpus/knowledge/freshness-pins.json"):
        p = dirpath / rel
        if p.exists():
            h.update(rel.encode())
            h.update(p.read_bytes())
    for p in sorted((dirpath / "corpus").rglob("*.md")):
        h.update(str(p.relative_to(dirpath)).encode())
        h.update(p.read_bytes())
    return h.hexdigest()


def negative_control(root: Path, rev: str, work: Path, timeout: int):
    ctl = work / "ctl"
    extract(root, rev, ctl)
    target = ctl / CONTROL_REL
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(CONTROL_BODY)
    rc, data = sweep(ctl, timeout)
    d = decide(rc, data)
    d["tree_identity"] = tree_identity(ctl)
    shutil.rmtree(ctl, ignore_errors=True)
    return d


def measure(root: Path, rev: str, work: Path, timeout: int):
    measured = work / "measured"
    extract(root, rev, measured)
    rc, data = sweep(measured, timeout)
    base = decide(rc, data)
    base["tree_identity"] = tree_identity(measured)
    shutil.rmtree(measured, ignore_errors=True)
    ctl = negative_control(root, rev, work, timeout)
    met = (base["sweep_exit"] == 0 and base["drift"] == 0 and base["new_missing"] == 0
           and base["paths_ok"] and ctl["sweep_exit"] == 1 and (ctl["drift"] or 0) >= 1
           and base["tree_identity"] != ctl["tree_identity"])
    base.update({"revision": rev, "control_exit": ctl["sweep_exit"],
                 "control_drift": ctl["drift"], "control_new_missing": ctl["new_missing"],
                 "met": met})
    return base


def emit(res: dict) -> int:
    print(f"C2v1 revision={res['revision']} sweep_exit={res['sweep_exit']} "
          f"drift={res['drift']} new_missing={res['new_missing']} "
          f"paths_ok={str(res['paths_ok']).lower()} skipped={res['skipped']} "
          f"control_exit={res['control_exit']} control_drift={res['control_drift']} "
          f"tree_identity={res['tree_identity'][:16]} met={str(res['met']).lower()}")
    for r in res["reasons"]:
        print(f"  verdict reason: {r}")
    return 0 if res["met"] else 1


# ── selftest: decision cases over synthetic sweep JSON ─────────────────────
def _sweep_json(drift=0, new_missing=0, paths_ok=True, code=0):
    return {"code": code, "ok": not code, "skipped": ["§armed (all remote checks)"],
            "reasons": [] if not code else ["§paths: x"],
            "sections": {"paths": {"ok": paths_ok,
                                   "counts": {"drift": drift, "newMissing": new_missing}}}}


def selftest() -> int:
    cases = [
        ("t1 clean sweep + red control is met", (0, _sweep_json()), (1, _sweep_json(1, 1, False, 1)), True),
        ("t2 drift red is not met", (1, _sweep_json(1, 0, False, 1)), (1, _sweep_json(1, 1, False, 1)), False),
        ("t3 new miss red is not met", (1, _sweep_json(0, 1, False, 1)), (1, _sweep_json(1, 1, False, 1)), False),
        ("t4 control green means the gate was loosened", (0, _sweep_json()), (0, _sweep_json()), False),
        ("t5 control that reports no drift is not proof", (0, _sweep_json()), (1, _sweep_json(0, 0, True, 1)), False),
        ("t6 help path unaffected: exit 64 is not met", (64, _sweep_json(0, 0, True, 64)), (1, _sweep_json(1, 1, False, 1)), False),
    ]
    bad = 0
    for cid, (rc, data), (crc, cdata), expect in cases:
        a = decide(rc, data)
        c = decide(crc, cdata)
        met = (a["sweep_exit"] == 0 and a["drift"] == 0 and a["new_missing"] == 0
               and a["paths_ok"] and c["sweep_exit"] == 1 and (c["drift"] or 0) >= 1)
        ok = met == expect
        bad += 0 if ok else 1
        print(f"  {'PASS' if ok else 'FAIL'} {cid}: met={met}")
    print(f"selftest: {len(cases) - bad}/{len(cases)} passed")
    return 0 if bad == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision")
    ap.add_argument("--work", default=None)
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--help", action="store_true")
    a = ap.parse_args()
    if a.help:
        print(__doc__)
        return 0
    if a.selftest:
        return selftest()
    if not a.revision:
        print("C2v1 error=--revision required")
        return 64
    root = Path(a.root).resolve()
    work = Path(a.work or tempfile.mkdtemp(prefix="c78sweep-"))
    work.mkdir(parents=True, exist_ok=True)
    try:
        return emit(measure(root, a.revision, work, a.timeout))
    except Unevaluable as e:
        print(f"C2v1 error={e}")
        return 2
    finally:
        if a.work is None:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
