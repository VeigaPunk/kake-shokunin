#!/usr/bin/env python3
"""Round-79 C1 control fixtures — proves the receipt-disclosure gate can pass and can fail.

Builds a throwaway git repo in scratch (`git init -q`, toplevel verified) with one disclosed
receipt rewrite in round 78, then measures the round-79 counter against five ledger variants:

  correct       a matching entry with a resolvable note -> met=true
  fabricated    a wrong toBlob -> phantom/wrong_kind findings
  drop-one      no entries -> undisclosed=1
  cheap-note    a matching blob pair with an empty note -> malformed=1
  round-rewrite a round-79 receipt rewritten (disclosed) -> round_rewritten=1

Each variant's full counter output is printed under its name. Read-only against the lane; the
fixture repo is deleted before exit.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
COUNTER = HERE / "c79_receipt_ledger.py"
LEDGER = ".ufo/waves/round-58/receipt-rewrites.json"
R78 = ".ufo/waves/round-78/controls/r.txt"
R79 = ".ufo/waves/round-79/controls/r79.txt"
NOTE_PATH = "corpus/lessons/round-75.md"


def git(d: Path, *args: str) -> str:
    p = subprocess.run(["git", "-C", str(d), *args], capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {p.stderr}")
    return p.stdout.strip()


def write_ledger(d: Path, entries: list[dict]) -> None:
    p = d / LEDGER
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"schema": "kake-r58-receipt-rewrites-v1", "events": entries},
                            indent=1) + "\n", encoding="utf-8")


def entry(path: str, commit: str, frm: str, to: str, kind: str, note: str) -> dict:
    return {"path": path, "commit": commit, "status": "M", "fromBlob": frm, "toBlob": to,
            "kind": kind, "note": note}


def measure(d: Path, rev: str) -> None:
    p = subprocess.run([sys.executable, "-B", str(COUNTER), "--root", str(d),
                        "--revision", rev, "--round", "79"], capture_output=True, text=True)
    print(p.stdout.strip())


def main() -> int:
    base = Path(os.environ.get("HYAKU_SCRATCH", tempfile.gettempdir())) / "kake-r79" / "ctl-fixture"
    shutil.rmtree(base, ignore_errors=True)
    base.mkdir(parents=True, exist_ok=True)
    d = Path(tempfile.mkdtemp(prefix="repo-", dir=base))
    try:
        git(d, "init", "-q")
        top = git(d, "rev-parse", "--show-toplevel")
        if Path(top).resolve() != d.resolve():
            raise SystemExit(f"fixture toplevel mismatch: {top} != {d}")
        git(d, "config", "user.name", "kake fixture")
        git(d, "config", "user.email", "fixture@kake.invalid")
        (d / "corpus/lessons").mkdir(parents=True, exist_ok=True)
        (d / NOTE_PATH).write_text("kake round-75 lesson\n", encoding="utf-8")
        (d / R78).parent.mkdir(parents=True, exist_ok=True)
        (d / R78).write_text("a\n", encoding="utf-8")
        git(d, "add", "-A")
        git(d, "commit", "-q", "-m", "fixture: seed receipt")
        c1 = git(d, "rev-parse", "HEAD")
        (d / R78).write_text("b\n", encoding="utf-8")
        git(d, "add", "-A")
        git(d, "commit", "-q", "-m", "fixture: rewrite round-78 receipt")
        c2 = git(d, "rev-parse", "HEAD")
        frm = git(d, "rev-parse", f"{c1}:{R78}")
        to = git(d, "rev-parse", f"{c2}:{R78}")

        write_ledger(d, [entry(R78, c2, frm, to, "content", f"Disclosed in {NOTE_PATH}.")])
        git(d, "add", "-A")
        git(d, "commit", "-q", "-m", "fixture: correct disclosure")
        correct = git(d, "rev-parse", "HEAD")

        print("## correct (able-to-pass)")
        measure(d, correct)

        write_ledger(d, [entry(R78, c2, frm, "0" * 40, "content", f"Disclosed in {NOTE_PATH}.")])
        git(d, "add", "-A")
        git(d, "commit", "-q", "-m", "fixture: fabricated blob")
        fab = git(d, "rev-parse", "HEAD")
        print("## fabricated (must fail)")
        measure(d, fab)

        write_ledger(d, [])
        git(d, "add", "-A")
        git(d, "commit", "-q", "-m", "fixture: dropped entry")
        drop = git(d, "rev-parse", "HEAD")
        print("## drop-one (must fail)")
        measure(d, drop)

        write_ledger(d, [entry(R78, c2, frm, to, "content", "")])
        git(d, "add", "-A")
        git(d, "commit", "-q", "-m", "fixture: empty note")
        cheap = git(d, "rev-parse", "HEAD")
        print("## cheap-note (must fail)")
        measure(d, cheap)

        (d / R79).parent.mkdir(parents=True, exist_ok=True)
        (d / R79).write_text("a\n", encoding="utf-8")
        git(d, "add", "-A")
        git(d, "commit", "-q", "-m", "fixture: seed round-79 receipt")
        c79a = git(d, "rev-parse", "HEAD")
        (d / R79).write_text("b\n", encoding="utf-8")
        git(d, "add", "-A")
        git(d, "commit", "-q", "-m", "fixture: rewrite round-79 receipt")
        c79b = git(d, "rev-parse", "HEAD")
        f79 = git(d, "rev-parse", f"{c79a}:{R79}")
        t79 = git(d, "rev-parse", f"{c79b}:{R79}")
        write_ledger(d, [entry(R78, c2, frm, to, "content", f"Disclosed in {NOTE_PATH}."),
                         entry(R79, c79b, f79, t79, "content", f"Disclosed in {NOTE_PATH}.")])
        git(d, "add", "-A")
        git(d, "commit", "-q", "-m", "fixture: disclosed round-79 rewrite")
        rw = git(d, "rev-parse", "HEAD")
        print("## round-rewrite (must fail)")
        measure(d, rw)
        return 0
    finally:
        shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
