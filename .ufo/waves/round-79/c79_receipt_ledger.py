#!/usr/bin/env python3
"""Round-79 C1 counter — standing receipt-rewrite disclosure gate (kake, calibration).

The lane's measurement receipts are every path ever committed under
`.ufo/waves/round-<N>/control/` or `.../controls/` (any round, any depth). A rewrite of a
receipt after its first commit is an event; it is disclosed when the ledger
`.ufo/waves/round-58/receipt-rewrites.json` carries an entry whose path, commit, status and
blob pair equal the event's, whose `kind` matches the byte-level classification, and whose
note names a repo-relative path that exists at the measured revision.

This counter imports the frozen round-58 counter for the event walk, ledger parsing, blob
classification and note-pointer semantics, and generalizes only its predicate: the round-58
`new_receipts == 2` conjunct (a file count of one round, not a rule) is dropped, and the
round-58 `new_rewritten` conjunct becomes `round_rewritten` scoped by `--round` (default 79).

Frozen predicate (contract §C1):

    met <=> undisclosed == 0 AND phantom == 0 AND malformed == 0 AND wrong_kind == 0
           AND unpointed == 0 AND symlinks == 0 AND round_rewritten == 0

Exit: 0 met, 1 measured defect, 2 unevaluable input, 64 usage. Read-only: writes nothing.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

FIELD_KEYS = ("undisclosed", "phantom", "malformed", "wrong_kind", "unpointed", "symlinks",
              "round_rewritten")
ROUND_PATH_RE = re.compile(r"^\.ufo/waves/round-([0-9]+)/(?:control|controls)/.+$")
C58_REL = Path(__file__).resolve().parent.parent / "round-58" / "c58_receipt_rewrites.py"


def load_c58():
    if not C58_REL.exists():
        raise RuntimeError(f"frozen round-58 counter missing: {C58_REL}")
    spec = importlib.util.spec_from_file_location("kake_c58_receipt_rewrites", C58_REL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def resolve_revision(root: str, rev: str) -> str:
    p = subprocess.run(["git", "-C", root, "rev-parse", "--verify", f"{rev}^{{commit}}"],
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"revision {rev!r} does not resolve: {p.stderr.strip()}")
    return p.stdout.strip()


def round_rewritten(c58, root: str, tip: str, round_no: int) -> int:
    return sum(1 for e in c58.events(root, tip)
               if (m := ROUND_PATH_RE.match(e["path"])) and int(m.group(1)) == round_no)


def measure(root: str, tip: str, round_no: int) -> dict:
    c58 = load_c58()
    v = c58.measure(root, tip)
    out = {k: v[k] for k in ("events", "undisclosed", "phantom", "malformed", "wrong_kind",
                             "unpointed", "symlinks")}
    out["round_rewritten"] = round_rewritten(c58, root, tip, round_no)
    out["met"] = all(out[k] == 0 for k in FIELD_KEYS)
    return out


def summary(tip: str, v: dict) -> str:
    fields = " ".join(f"{k}={v[k]}" for k in ("events",) + FIELD_KEYS)
    return f"C1v2 revision={tip} {fields} met={'true' if v['met'] else 'false'}"


def selftest() -> int:
    cases = [
        ("all-clean", {k: 0 for k in FIELD_KEYS}, True, 0),
        ("undisclosed", {**{k: 0 for k in FIELD_KEYS}, "undisclosed": 1}, False, 1),
        ("phantom", {**{k: 0 for k in FIELD_KEYS}, "phantom": 1}, False, 1),
        ("malformed", {**{k: 0 for k in FIELD_KEYS}, "malformed": 1}, False, 1),
        ("wrong-kind", {**{k: 0 for k in FIELD_KEYS}, "wrong_kind": 1}, False, 1),
        ("unpointed", {**{k: 0 for k in FIELD_KEYS}, "unpointed": 1}, False, 1),
        ("symlink", {**{k: 0 for k in FIELD_KEYS}, "symlinks": 1}, False, 1),
        ("round-rewritten", {**{k: 0 for k in FIELD_KEYS}, "round_rewritten": 1}, False, 1),
        ("two-fields", {**{k: 0 for k in FIELD_KEYS}, "undisclosed": 2, "phantom": 1}, False, 1),
    ]
    ok = 0
    total = 0
    for name, counts, want_met, want_exit in cases:
        total += 1
        met = all(counts[k] == 0 for k in FIELD_KEYS)
        code = 0 if met else 1
        if met == want_met and code == want_exit:
            ok += 1
        else:
            print(f"  FAIL {name}: met={met} exit={code}")
    for name, path, round_no, want in [
        ("r79-receipt", ".ufo/waves/round-79/controls/base-c1.txt", 79, 1),
        ("r78-receipt", ".ufo/waves/round-78/controls/base-c1.txt", 79, 0),
        ("r79-control-dir", ".ufo/waves/round-79/control/x.txt", 79, 1),
        ("r79-non-receipt", ".ufo/waves/round-79/w1/Seat.md", 79, 0),
        ("r790-prefix", ".ufo/waves/round-790/controls/x.txt", 79, 0),
    ]:
        total += 1
        m = ROUND_PATH_RE.match(path)
        got = 1 if (m and int(m.group(1)) == round_no) else 0
        if got == want:
            ok += 1
        else:
            print(f"  FAIL {name}: got {got} want {want}")
    total += 1
    line = summary("deadbeef", {**{k: 0 for k in FIELD_KEYS}, "events": 32, "met": True})
    if line == ("C1v2 revision=deadbeef events=32 undisclosed=0 phantom=0 malformed=0 "
                "wrong_kind=0 unpointed=0 symlinks=0 round_rewritten=0 met=true"):
        ok += 1
    else:
        print(f"  FAIL summary: {line}")
    print(f"selftest: {ok}/{total} passed")
    return 0 if ok == total else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", required=False, default=".")
    ap.add_argument("--revision", required=False)
    ap.add_argument("--round", type=int, default=79)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.revision:
        print("usage: --revision is required (the measured lane revision)", file=sys.stderr)
        return 64
    if a.round < 1:
        print("usage: --round must be >= 1", file=sys.stderr)
        return 64
    try:
        tip = resolve_revision(a.root, a.revision)
        v = measure(a.root, tip, a.round)
    except (RuntimeError, ValueError) as exc:
        print(f"unevaluable: {exc}")
        print("exit=2")
        return 2
    code = 0 if v["met"] else 1
    if a.json:
        print(json.dumps({"schema": "kake-r79-c1-receipt-ledger-v1",
                          "revision": tip, "round": a.round, **v, "exit": code}, indent=1))
    else:
        print(summary(tip, v))
        print(f"exit={code}")
    return code


if __name__ == "__main__":
    sys.exit(main())
