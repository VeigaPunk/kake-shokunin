#!/usr/bin/env python3
"""Round-80 R79-4 fixture harness — isolates the three round-79 mutation survivors.

Round 79's mutation seat (`.ufo/waves/round-79/w1/MutC.md`) left three counter survivors the
frozen battery never exercised: k3 (`wrong_kind` zeroed), k4 (`malformed` zeroed — the cheap-note
fixture stays red only via `undisclosed=1`) and k5 (`symlinks` zeroed). This harness closes the
evidence gap: it builds one throwaway git fixture per survivor in scratch, drives the frozen
round-79 receipt-ledger counter (`.ufo/waves/round-79/c79_receipt_ledger.py`, subprocess,
`--round 79`) over each, and reports whether the counter is red through exactly the survivor's
field.

Fixtures (recipes mirror `.ufo/waves/round-79/ctl_receipt_fixture.py` and MutC probes S1–S3):

  wrong_kind  disclosed rewrite with true blobs and a false byte-level kind
              (`append` claimed for a `content` change) -> wrong_kind=1, sole red (kills k3)
  cheap_note  disclosed rewrite whose entry is structurally right (true blob pair, true kind)
              except the cheap empty note: the entry is malformed, so it never matches and the
              rewrite is undisclosed -> undisclosed=1 (with malformed=1), the exact round-79
              battery mechanism
  symlinks    the receipt is replaced by a symlink at the measured tip; the swap is disclosed
              with the true link blobs -> symlinks=1, sole red (kills k5)

Interface (pinned by `.ufo/waves/round-80/c80_defect_queue.py::p_r79_4`):

    python3 -B .ufo/waves/round-80/c80_ledger_fixtures.py --root <tree> --json

prints `{"schema": ..., "fixtures": {"wrong_kind": {...}, "cheap_note": {...}, "symlinks":
{...}}, "killed": <n>}` and exits 0 iff killed == 3. Stdout is pure JSON; diagnostics go to
stderr. Read-only against --root: fixtures live and die under
`$HYAKU_SCRATCH/kake-r80/ExecFixtures/` (default /fast/scratch/hyaku) and are deleted before
exit.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCHEMA = "kake-r80-ledger-fixtures-v1"
LANE = Path("/home/vgpnk/Projects/shokunin/kake-shokunin")
COUNTER_REL = Path(".ufo/waves/round-79/c79_receipt_ledger.py")
LEDGER = ".ufo/waves/round-58/receipt-rewrites.json"
NOTE_PATH = "corpus/lessons/round-75.md"
R78 = ".ufo/waves/round-78/controls/r.txt"
FIELD_KEYS = ("undisclosed", "phantom", "malformed", "wrong_kind", "unpointed", "symlinks",
              "round_rewritten")
GIT_ID = ("-c", "user.name=kake-r80-fixtures", "-c", "user.email=fixtures@kake.invalid",
          "-c", "commit.gpgsign=false")
NOTE = f"Disclosed in {NOTE_PATH}."


def clean_env(run_dir: Path) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["TMPDIR"] = str(run_dir)  # any tempfile the counter spawns stays in scratch
    return env


def git(d: Path, *args: str) -> str:
    p = subprocess.run(["git", "-C", str(d), *args], capture_output=True, text=True,
                       env=clean_env(d))
    if p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {p.stderr.strip() or p.stdout.strip()}")
    return p.stdout.strip()


def commit(d: Path, msg: str) -> str:
    git(d, "add", "-A")
    git(d, *GIT_ID, "commit", "-q", "-m", msg)
    return git(d, "rev-parse", "HEAD")


def init_repo(base: Path) -> Path:
    d = Path(tempfile.mkdtemp(prefix="fx-", dir=base))
    git(d, "init", "-q")
    top = git(d, "rev-parse", "--show-toplevel")
    if Path(top).resolve() != d.resolve():
        raise RuntimeError(f"fixture toplevel mismatch: {top} != {d}")
    return d


def seed(d: Path) -> None:
    (d / NOTE_PATH).parent.mkdir(parents=True, exist_ok=True)
    (d / NOTE_PATH).write_text("kake round-75 lesson (fixture note target)\n", encoding="utf-8")
    (d / R78).parent.mkdir(parents=True, exist_ok=True)
    (d / R78).write_text("a\n", encoding="utf-8")
    commit(d, "fixture: seed note target and receipt")


def entry(path: str, rev: str, frm: str, to: str, kind: str, note: str) -> dict:
    return {"path": path, "commit": rev, "status": "M", "fromBlob": frm, "toBlob": to,
            "kind": kind, "note": note}


def write_ledger(d: Path, entries: list[dict]) -> None:
    p = d / LEDGER
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"schema": "kake-r58-receipt-rewrites-v1", "events": entries},
                            indent=1) + "\n", encoding="utf-8")


def run_counter(counter: Path, d: Path, rev: str, run_dir: Path, json_mode: bool):
    argv = [sys.executable, "-B", str(counter), "--root", str(d), "--revision", rev,
            "--round", "79"] + (["--json"] if json_mode else [])
    return subprocess.run(argv, cwd=str(run_dir), capture_output=True, text=True,
                          timeout=120, env=clean_env(run_dir))


def measure(counter: Path, d: Path, rev: str, run_dir: Path) -> dict:
    plain = run_counter(counter, d, rev, run_dir, json_mode=False)
    doc_run = run_counter(counter, d, rev, run_dir, json_mode=True)
    rec = {"revision": rev, "counter_exit": plain.returncode, "raw": plain.stdout,
           "summary": plain.stdout.splitlines()[0] if plain.stdout.strip() else "",
           "stderr": (plain.stderr or "").strip()[-200:]}
    try:
        doc = json.loads(doc_run.stdout)
    except json.JSONDecodeError:
        rec["parse_error"] = (doc_run.stdout + doc_run.stderr).strip()[-200:]
        return rec
    rec["json_exit"] = doc_run.returncode
    rec["json_revision"] = doc.get("revision")
    for k in FIELD_KEYS + ("events", "met"):
        rec[k] = doc.get(k)
    rec["ledger_red"] = plain.returncode == 1 and doc_run.returncode == 1
    return rec


def killed_flags(name: str, rec: dict) -> bool:
    """Red through exactly the survivor's field (cheap_note: the round-79 battery mechanism,
    an entry dropped as malformed so the rewrite is undisclosed)."""
    f = {k: rec.get(k) for k in FIELD_KEYS}
    if not rec.get("ledger_red") or any(not isinstance(v, int) for v in f.values()):
        return False
    others = {k: v for k, v in f.items()}
    if name == "wrong_kind":
        others.pop("wrong_kind")
        return f["wrong_kind"] == 1 and all(v == 0 for v in others.values())
    if name == "cheap_note":
        # the round-79 mechanism co-fires: an entry dropped as malformed is also undisclosed,
        # so both fields are the fixture's own conjunct, never "others".
        others.pop("undisclosed")
        others.pop("malformed")
        return (f["undisclosed"] == 1 and f["malformed"] == 1
                and all(v == 0 for v in others.values()))
    if name == "symlinks":
        others.pop("symlinks")
        return f["symlinks"] == 1 and all(v == 0 for v in others.values())
    return False


def build_wrong_kind(counter: Path, base: Path, run_dir: Path) -> dict:
    d = init_repo(base)
    try:
        seed(d)
        (d / R78).write_text("b\n", encoding="utf-8")
        c2 = commit(d, "fixture: rewrite receipt (content)")
        frm, to = git(d, "rev-parse", f"{c2}^:{R78}"), git(d, "rev-parse", f"{c2}:{R78}")
        # true blobs, false byte-level kind: "a\n"->"b\n" classifies `content`, not `append`
        write_ledger(d, [entry(R78, c2, frm, to, "append", NOTE)])
        tip = commit(d, "fixture: disclose with a false kind")
        return measure(counter, d, tip, run_dir)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def build_cheap_note(counter: Path, base: Path, run_dir: Path) -> dict:
    d = init_repo(base)
    try:
        seed(d)
        (d / R78).write_text("b\n", encoding="utf-8")
        c2 = commit(d, "fixture: rewrite receipt (content)")
        frm, to = git(d, "rev-parse", f"{c2}^:{R78}"), git(d, "rev-parse", f"{c2}:{R78}")
        # structurally right (true blobs, true kind) except the cheap empty note:
        # the entry is malformed, never matches, so the rewrite is undisclosed
        write_ledger(d, [entry(R78, c2, frm, to, "content", "")])
        tip = commit(d, "fixture: disclose with an empty note")
        return measure(counter, d, tip, run_dir)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def build_symlinks(counter: Path, base: Path, run_dir: Path) -> dict:
    d = init_repo(base)
    try:
        seed(d)
        target = "../../../corpus/lessons/round-75.md"
        (d / R78).parent.mkdir(parents=True, exist_ok=True)
        (d / R78).unlink()
        os.symlink(target, d / R78)  # the receipt path now holds a symlink
        c2 = commit(d, "fixture: replace receipt with a symlink")
        frm, to = git(d, "rev-parse", f"{c2}^:{R78}"), git(d, "rev-parse", f"{c2}:{R78}")
        write_ledger(d, [entry(R78, c2, frm, to, "content", NOTE)])
        tip = commit(d, "fixture: disclose the symlink swap with the true link blobs")
        return measure(counter, d, tip, run_dir)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def find_counter(root: Path) -> Path:
    for cand in (root / COUNTER_REL, LANE / COUNTER_REL):
        if cand.is_file():
            return cand
    raise RuntimeError(f"frozen round-79 counter not found at {root / COUNTER_REL} "
                       f"or {LANE / COUNTER_REL}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".", help="measured tree (read-only; locates the counter)")
    ap.add_argument("--json", action="store_true", help="output is JSON either way")
    a = ap.parse_args()
    root = Path(a.root).resolve()
    out: dict = {"schema": SCHEMA, "root": str(root)}
    try:
        counter = find_counter(root)
        out["counter"] = str(counter)
        out["counter_sha256"] = hashlib.sha256(counter.read_bytes()).hexdigest()
        scratch = Path(os.environ.get("HYAKU_SCRATCH") or "/fast/scratch/hyaku")
        base = scratch / "kake-r80" / "ExecFixtures"
        base.mkdir(parents=True, exist_ok=True)
        run_dir = Path(tempfile.mkdtemp(prefix="run-", dir=base))
        out["scratch"] = str(run_dir)
        builders = (("wrong_kind", build_wrong_kind), ("cheap_note", build_cheap_note),
                    ("symlinks", build_symlinks))
        fixtures: dict = {}
        try:
            for name, build in builders:
                rec = build(counter, base, run_dir)
                rec["killed"] = killed_flags(name, rec)
                fixtures[name] = rec
                print(f"fixture {name}: {'killed' if rec['killed'] else 'NOT killed'} "
                      f"rc={rec.get('counter_exit')} {rec.get('summary')}", file=sys.stderr)
        finally:
            shutil.rmtree(run_dir, ignore_errors=True)
            with contextlib.suppress(OSError):
                os.rmdir(base)      # remove the seat dir if this run left it empty
            with contextlib.suppress(OSError):
                os.rmdir(base.parent)
        out["fixtures"] = fixtures
        out["killed"] = sum(1 for r in fixtures.values() if r.get("killed"))
    except Exception as exc:  # noqa: BLE001 — the counter needs parseable stdout on any failure
        out["error"] = f"{type(exc).__name__}: {exc}"
        print(json.dumps(out, indent=1))
        return 2
    print(json.dumps(out, indent=1))
    return 0 if out["killed"] == 3 else 1


if __name__ == "__main__":
    sys.exit(main())
