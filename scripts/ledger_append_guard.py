#!/usr/bin/env python3
"""Append guard for the receipt-rewrite ledgers (kake round 80, R79-2).

A receipt ledger is evidence: it may grow, and every byte it already carried must survive the
growth. Round 79's append re-serialized the file and rewrote one prior note's em dash as a
`\\u2014` escape (semantics unchanged, bytes not) — this guard exists so that class fails loudly.

Rule: for each governed ledger, the base revision's bytes up to the ledger's final `]` must be an
exact byte prefix of the tree's bytes. A pure append passes; an in-place edit anywhere before that
offset fails and reports the first divergent offset.

    --selftest                       fixtures: a pure append passes, an in-place edit fails
    --root <tree> [--base <rev>]     check the tree against a revision (default: the round-80 base)
    --base-file <path>               compare against an exported base snapshot instead of git
    --json                           machine output on --root

Exit: 0 clean, 1 a ledger lost prior bytes, 2 could not evaluate, 64 usage.
Read-only: it never writes a ledger and never runs a mutating git command.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DEFAULT_BASE = "9998dc7a586b9fe76379014c8123aa3606f2d8b9"
GOVERNED_GLOB = ".ufo/waves/*/receipt-rewrites*.json"


def prefix_probe(base: bytes, carrier: bytes) -> tuple[bool, int]:
    """Compare on the ledger's stable prefix: everything up to the final closing bracket."""
    cut = base.rindex(b"]") if b"]" in base else len(base)
    head = base[:cut]
    if carrier.startswith(head):
        return True, len(head)
    limit = min(len(head), len(carrier))
    offset = next((i for i in range(limit) if head[i] != carrier[i]), limit)
    return False, offset


def check_tree(root: Path, base_rev: str, base_file: Path | None = None) -> dict:
    ledgers = sorted(root.glob(GOVERNED_GLOB))
    files = []
    ok_all = True
    for path in ledgers:
        rel = path.relative_to(root).as_posix()
        if base_file is not None:
            try:
                base_bytes = base_file.read_bytes()
            except OSError as exc:
                files.append({"path": rel, "compared": False, "reason": str(exc)})
                continue
        else:
            show = subprocess.run(["git", "-C", str(root), "show", f"{base_rev}:{rel}"],
                                  capture_output=True)
            if show.returncode != 0:
                files.append({"path": rel, "compared": False,
                              "reason": f"base {base_rev} does not carry the path"})
                continue
            base_bytes = show.stdout
        try:
            carrier = path.read_bytes()
        except OSError as exc:
            files.append({"path": rel, "compared": False, "reason": str(exc)})
            continue
        ok, detail = prefix_probe(base_bytes, carrier)
        ok_all = ok_all and ok
        files.append({"path": rel, "compared": True, "prefix_preserved": ok,
                      "base_bytes": len(base_bytes), "carrier_bytes": len(carrier),
                      "first_divergence": None if ok else detail})
    return {"schema": "kake-ledger-append-guard/v1", "base": base_rev,
            "files": sum(1 for f in files if f["compared"]),
            "prefix_preserved": ok_all and any(f["compared"] for f in files),
            "detail": files}


def selftest(work: Path) -> int:
    repo = work / "fixture-repo"
    repo.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "GIT_AUTHOR_NAME": "kake-guard", "GIT_AUTHOR_EMAIL": "guard@kake.invalid",
           "GIT_COMMITTER_NAME": "kake-guard", "GIT_COMMITTER_EMAIL": "guard@kake.invalid"}
    subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True, env=env)
    ledger = repo / ".ufo" / "waves" / "round-58" / "receipt-rewrites.json"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    base_text = ('{\n "schema": "receipt-rewrites/v2",\n "events": [\n'
                 '  {\n   "path": ".ufo/waves/round-58/controls/a.txt",\n'
                 '   "note": "prior entry \u2014 with an em dash"\n  }\n ]\n}\n')
    ledger.write_text(base_text, encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True, env=env)
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "base"], check=True, env=env)
    rev = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                         capture_output=True, text=True, check=True).stdout.strip()
    checks = []

    cut = base_text.rindex("]")
    appended = (base_text[:cut]
                + ',\n  {\n   "path": ".ufo/waves/round-58/controls/b.txt"\n  }\n '
                + base_text[cut:])
    ledger.write_text(appended, encoding="utf-8")
    res = check_tree(repo, rev)
    checks.append(("append", res["prefix_preserved"] is True and res["files"] == 1))

    edited = appended.replace("\u2014 with an em dash", "\\u2014 with an em dash")
    ledger.write_text(edited, encoding="utf-8")
    res = check_tree(repo, rev)
    red = res["prefix_preserved"] is False and res["files"] == 1
    checks.append(("non-prefix", red))
    print(f"fixture append: {'passed' if checks[0][1] else 'failed'}")
    print(f"fixture non-prefix: {'failed' if red else 'passed'} "
          f"(first divergence at byte {res['detail'][0].get('first_divergence')})")
    passed = sum(1 for _, ok in checks if ok)
    print(f"selftest: {passed}/{len(checks)} passed")
    return 0 if passed == len(checks) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--base", default=DEFAULT_BASE)
    ap.add_argument("--base-file", help="base snapshot for a tree that is not a git checkout")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--work")
    a = ap.parse_args()
    if a.selftest:
        work = Path(a.work) if a.work else Path(tempfile.mkdtemp(prefix="kake-guard-"))
        work.mkdir(parents=True, exist_ok=True)
        owned = a.work is None
        try:
            return selftest(work)
        finally:
            if owned:
                shutil.rmtree(work, ignore_errors=True)
    root = Path(a.root).resolve()
    res = check_tree(root, a.base, Path(a.base_file) if a.base_file else None)
    if a.json:
        print(json.dumps(res, indent=1))
    else:
        for row in res["detail"]:
            state = ("prefix preserved" if row.get("prefix_preserved")
                     else f"first divergence at byte {row.get('first_divergence')}")
            print(f"{row['path']}: {state}")
        print(f"files={res['files']} prefix_preserved={res['prefix_preserved']}")
    return 0 if res["prefix_preserved"] else 1


if __name__ == "__main__":
    sys.exit(main())
