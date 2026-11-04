#!/usr/bin/env python3
"""ledger_append_guard.py — standing byte-prefix guard for kake receipt ledgers.

Round-79 routed defect R79-2: the round-58 receipt-rewrite ledger was appended
by re-serializing the whole file (one prior note's `—` became the escape
sequence `\\u2014`), so prior bytes changed even though the JSON was unchanged.
This guard verifies, for every receipt ledger it governs, that the ledger's
bytes at the pinned base revision are a BYTE PREFIX of its current bytes in the
tree: later rounds may append entries, never rewrite, reorder or re-serialize
prior bytes.

Usage:
  python3 -B scripts/ledger_append_guard.py --selftest
      Two git fixture repos prove the check can pass (a byte-spliced append)
      and can fail (a prior byte edited in place, the R79-2 shape).  Exit 0
      when both behave, 1 when the guard itself is broken.

  python3 -B scripts/ledger_append_guard.py --root <tree> [--json] [--base <rev>]
      For each governed ledger, read the base bytes with
      `git -C <root> show <base>:<path>` and the tree bytes from
      `<root>/<path>`; report the first offset where they diverge plus the
      byte at that offset on each side.  `--base` overrides the default
      base revision; `--ledger <path>` (repeatable) adds governed ledgers.

Exit: 0 every evaluated ledger keeps its byte prefix; 1 some ledger diverges
or is truncated; 2 unevaluable (root missing, or no governed ledger could be
evaluated); 64 usage.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DEFAULT_BASE = "9998dc7a586b9fe76379014c8123aa3606f2d8b9"
GOVERNED = [".ufo/waves/round-58/receipt-rewrites.json"]
# Informational pin: sha256 of the governed ledger's bytes at DEFAULT_BASE,
# recorded when this guard was authored (2026-11-04, kake round 80).
BASE_SHA256 = {
    GOVERNED[0]: "93182decabda35b88c8e993e6e178d4689692b4d35396a25d372ff251efbb210",
}


# --------------------------------------------------------------------------- git plumbing

def _git_env() -> dict:
    env = os.environ.copy()
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_TERMINAL_PROMPT"] = "0"
    return env


def _git(root: Path, *args: str, check: bool = False) -> subprocess.CompletedProcess:
    proc = subprocess.run(["git", "-C", str(root), *args],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=_git_env())
    if check and proc.returncode != 0:
        raise RuntimeError(
            f"git -C {root} {' '.join(args)}: {proc.stderr.decode('utf-8', 'replace')[:200]}")
    return proc


def git_show(root: Path, rev: str, rel: str) -> bytes | None:
    """Bytes of <rev>:<rel> in <root>'s repository, or None when unavailable."""
    proc = _git(root, "show", f"{rev}:{rel}")
    return proc.stdout if proc.returncode == 0 else None


# --------------------------------------------------------------------------- core check

def first_divergence(base: bytes, tree: bytes) -> int | None:
    """First offset where tree stops matching base; None iff base is a prefix of tree.

    A tree shorter than base diverges at len(tree) (truncation of prior bytes).
    """
    for i in range(min(len(base), len(tree))):
        if base[i] != tree[i]:
            return i
    if len(tree) < len(base):
        return len(tree)
    return None


def _byte(data: bytes, off: int) -> dict:
    if off < len(data):
        return {"byte": data[off], "hex": hex(data[off])}
    return {"byte": None, "hex": None}


def check_ledger(root: Path, rel: str, base_rev: str) -> dict:
    """One governed ledger: is base:<rel> a byte prefix of the tree's <rel>?"""
    doc: dict = {"path": rel, "base": base_rev}
    tree_file = root / rel
    try:
        tree = tree_file.read_bytes() if tree_file.is_file() else None
    except OSError:
        tree = None
    base = git_show(root, base_rev, rel)
    doc["base_source"] = "git" if base is not None else "unavailable"
    doc["tree_source"] = "file" if tree is not None else "absent"
    doc["size_base"] = len(base) if base is not None else None
    doc["size_tree"] = len(tree) if tree is not None else None
    doc["base_sha256"] = hashlib.sha256(base).hexdigest() if base is not None else None
    doc["tree_sha256"] = hashlib.sha256(tree).hexdigest() if tree is not None else None
    doc["evaluated"] = base is not None and tree is not None
    if doc["evaluated"]:
        off = first_divergence(base, tree)  # type: ignore[arg-type]
        doc["prefix_preserved"] = off is None
        if off is None:
            doc["first_divergence"] = None
        else:
            doc["first_divergence"] = {
                "offset": off,
                "base": _byte(base, off),  # type: ignore[arg-type]
                "tree": _byte(tree, off),  # type: ignore[arg-type]
            }
    else:
        doc["prefix_preserved"] = None
        doc["first_divergence"] = None
        why = []
        if base is None:
            why.append(f"base bytes unreadable via git show {base_rev}:{rel} in {root}")
        if tree is None:
            why.append(f"tree file {rel} absent under {root}")
        doc["note"] = "; ".join(why)
    return doc


# --------------------------------------------------------------------------- selftest fixtures

_FIXTURE_REL = "ledger/receipts.json"
# Two entries with a raw em dash (bytes e2 80 94) in the note strings: the
# exact bytes the round-79 append turned into the escape \u2014 (R79-2).
_FIXTURE_BASE = (
    b'{\n'
    b' "schema": "kake-r58-receipt-rewrites-v1",\n'
    b' "note": "fixture \xe2\x80\x94 em dash stays raw",\n'
    b' "events": [\n'
    b'  {"commit": "aaaa000000000000000000000000000000000001", "path": '
    b'".ufo/waves/round-1/controls/a.txt", "kind": "content", "note": '
    b'"fixture \xe2\x80\x94 entry one"},\n'
    b'  {"commit": "bbbb000000000000000000000000000000000002", "path": '
    b'".ufo/waves/round-2/controls/b.txt", "kind": "append", "note": '
    b'"fixture \xe2\x80\x94 entry two"}\n'
    b' ]\n'
    b'}\n'
)
_FIXTURE_ENTRY3 = (b',\n  {"commit": "cccc000000000000000000000000000000000003", "path": '
                   b'".ufo/waves/round-3/controls/c.txt", "kind": "content", "note": '
                   b'"fixture \xe2\x80\x94 entry three"}')


def _commit_fixture(d: Path, content: bytes, msg: str) -> str:
    f = d / _FIXTURE_REL
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_bytes(content)
    _git(d, "add", _FIXTURE_REL, check=True)
    _git(d, "-c", "user.name=ledger-append-guard", "-c",
         "user.email=guard@kake.invalid", "-c", "commit.gpgsign=false",
         "commit", "-q", "-m", msg, check=True)
    return _git(d, "rev-parse", "HEAD", check=True).stdout.decode().strip()


def _fixture_repo(tmp: Path, name: str) -> tuple[Path, str]:
    """A scratch git repo holding _FIXTURE_BASE as its base commit; toplevel asserted."""
    d = tmp / name
    d.mkdir(parents=True)
    _git(d, "init", "-q", check=True)
    top = _git(d, "rev-parse", "--show-toplevel", check=True).stdout.decode().strip()
    assert Path(top) == d, f"fixture toplevel {top} != {d}"
    base_rev = _commit_fixture(d, _FIXTURE_BASE, "fixture base")
    return d, base_rev


def selftest() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="ledger-append-guard-selftest-"))
    failures: list[str] = []
    try:
        # Fixture 1 — append by byte-splice: all prior bytes stay; the new
        # entry is spliced in before the closing bracket.  Must come out green.
        d1, base1 = _fixture_repo(tmp, "append")
        idx = _FIXTURE_BASE.rindex(b"]")
        spliced = _FIXTURE_BASE[:idx] + _FIXTURE_ENTRY3 + _FIXTURE_BASE[idx:]
        (d1 / _FIXTURE_REL).write_bytes(spliced)
        r1 = check_ledger(d1, _FIXTURE_REL, base1)
        ok1 = bool(r1["evaluated"]) and r1["prefix_preserved"] is True
        if ok1:
            print(f"append byte-splice ... ok (base {r1['size_base']} bytes are a "
                  f"byte prefix of tree {r1['size_tree']} bytes)")
        else:
            failures.append(f"append fixture came out {r1['prefix_preserved']}, want preserved")

        # Fixture 2 — non-prefix: a prior byte edited in place (raw em dash ->
        # the escape \u2014, the round-79 R79-2 failure).  Must come out red.
        d2, base2 = _fixture_repo(tmp, "non-prefix")
        edited = _FIXTURE_BASE.replace(b"\xe2\x80\x94", b"\\u2014")
        (d2 / _FIXTURE_REL).write_bytes(edited)
        r2 = check_ledger(d2, _FIXTURE_REL, base2)
        want_off = _FIXTURE_BASE.index(b"\xe2\x80\x94")
        ok2 = (bool(r2["evaluated"]) and r2["prefix_preserved"] is False
               and r2["first_divergence"]["offset"] == want_off
               and r2["first_divergence"]["base"]["hex"] == "0xe2"
               and r2["first_divergence"]["tree"]["hex"] == "0x5c")
        if ok2:
            print(f"non-prefix in-place-edit ... failed (first divergence at offset "
                  f"{r2['first_divergence']['offset']}: base byte 0xe2, tree byte 0x5c)")
        else:
            failures.append(f"non-prefix fixture came out {json.dumps(r2.get('first_divergence'))}, "
                            f"want divergence at {want_off} (base 0xe2 vs tree 0x5c)")

        for f in failures:
            print(f"FAIL {f}")
        total = 2
        passed = total - len(failures)
        print(f"selftest: {passed}/{total} fixtures behaved")
        return 0 if not failures else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --------------------------------------------------------------------------- main

class _Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:  # usage errors -> exit 64
        self.exit(64, f"{self.prog}: error: {message}\n")


def _doc(root: Path, base_rev: str, ledgers: list[str],
         docs: list[dict], error: str | None = None) -> dict:
    evaluated = [d for d in docs if d["evaluated"]]
    preserved = all(d["prefix_preserved"] for d in evaluated)
    out = {
        "schema": "kake-ledger-append-guard-v1",
        "root": str(root),
        "base": base_rev,
        "governed": len(ledgers),
        "files": len(evaluated),
        "prefix_preserved": bool(evaluated) and preserved,
        "ledgers": docs,
    }
    if error:
        out["error"] = error
    return out


def main() -> int:
    ap = _Parser(description="byte-prefix guard for kake receipt ledgers (R79-2)")
    ap.add_argument("--root", default=".", help="tree whose ledger bytes are checked")
    ap.add_argument("--base", default=DEFAULT_BASE, help="base revision for the prefix bytes")
    ap.add_argument("--ledger", action="append", default=None,
                    help="additional governed ledger path (repeatable)")
    ap.add_argument("--json", action="store_true", help="print the verdict as JSON")
    ap.add_argument("--selftest", action="store_true", help="run the fixture battery")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    root = Path(args.root).resolve()
    ledgers = list(GOVERNED) + list(args.ledger or [])
    docs: list[dict] = []
    error = None
    if not root.is_dir():
        error = f"root {root} missing"
    else:
        docs = [check_ledger(root, rel, args.base) for rel in ledgers]
    doc = _doc(root, args.base, ledgers, docs, error)

    if args.json:
        print(json.dumps(doc, indent=2, sort_keys=True))
    else:
        for d in docs:
            if not d["evaluated"]:
                print(f"{d['path']}: unevaluable ({d['note']})")
            elif d["prefix_preserved"]:
                print(f"{d['path']}: prefix preserved (base {d['size_base']} bytes "
                      f"are a byte prefix of tree {d['size_tree']} bytes)")
            else:
                div = d["first_divergence"]
                print(f"{d['path']}: NOT preserved (first divergence at offset "
                      f"{div['offset']}: base byte {div['base']['hex']}, tree byte {div['tree']['hex']})")
        if error:
            print(error)
        print(f"ledger_append_guard: files={doc['files']} "
              f"prefix_preserved={'true' if doc['prefix_preserved'] else 'false'}")

    if error or not doc["files"]:
        return 2
    return 0 if doc["prefix_preserved"] else 1


if __name__ == "__main__":
    sys.exit(main())
