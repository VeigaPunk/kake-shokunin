#!/usr/bin/env python3
"""Round-63 C2 operability counter — the quote-class tool runs at a revision.

Measures whether scripts/quote_class.py exists at the measured revision, runs
its --selftest --json from the lane root (the selftest binds one real corpus
case, s432_real, against the retained blobs), and requires every frozen case
id to be present and passing. A do-nothing tree (tool absent) cannot reach
met=true; a stub tool that skips the frozen case ids is rejected by the
case-set check.

Usage: c63_quote_tool.py --root . --revision <rev>
Exits: 0 met; 1 not met; 2 could-not-evaluate (git unreadable).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = "13d4519818db28cd0aa912e49020659140d7b9fa"  # round-62 tip
TOOL_REL = "scripts/quote_class.py"
FROZEN_CASE_IDS = {
    "inline_raw_substring",
    "markup_collapsed_only",
    "absent_everywhere",
    "s432_real",
}


def git_show(root: str, revision: str, rel: str) -> bytes | None:
    proc = subprocess.run(
        ["git", "-C", root, "show", f"{revision}:{rel}"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if proc.returncode:
        return None
    return proc.stdout


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision", default=BASE)
    args = ap.parse_args()

    root = args.root
    rev = args.revision
    probe = subprocess.run(["git", "-C", root, "rev-parse", "--verify", rev],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if probe.returncode:
        print(f"could-not-evaluate: revision {rev} unreadable", file=sys.stderr)
        return 2

    tool_blob = git_show(root, rev, TOOL_REL)
    if tool_blob is None:
        print(f"revision={rev} present=0 selftest=unevaluable met=false")
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        tool = Path(tmp) / "quote_class.py"
        tool.write_bytes(tool_blob)
        proc = subprocess.run(
            [sys.executable, "-B", str(tool), "--selftest", "--json"],
            cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            check=False)
    if proc.returncode != 0:
        print(f"revision={rev} present=1 selftest=failed met=false")
        return 1
    try:
        result = json.loads(proc.stdout.decode("utf-8"))
    except Exception:
        print(f"revision={rev} present=1 selftest=unparseable met=false")
        return 1
    cases = {c.get("id"): c for c in result.get("cases", [])}
    frozen_ok = all(
        cases.get(cid, {}).get("passed") is True
        and cases.get(cid, {}).get("derived") == cases.get(cid, {}).get("expected")
        for cid in FROZEN_CASE_IDS
    )
    total = result.get("total")
    passed = result.get("passed")
    met = bool(result.get("ok") and frozen_ok and total == passed
               and total == len(FROZEN_CASE_IDS))
    print(f"revision={rev} present=1 selftest={passed}/{total} "
          f"frozen_cases={'ok' if frozen_ok else 'missing'} met={str(met).lower()}")
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
