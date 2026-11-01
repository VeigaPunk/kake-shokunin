#!/usr/bin/env python3
"""Round-65 C2 freshness check — the S432 retained live re-open body is pinned.

Implements the frozen round-65 contract (`.ufo/waves/round-65/contract.md`
§C2, predicate v2), completing round-64 closure routed defect 5: the run-12
wrap-up commit d3a4e402 landed `.ufo/waves/round-64/sources/S432.live.html`
post-closure, byte-identical to the round-61 retained body, but nothing
committed bound its bytes to that body — silent drift (an edit, an EOL
rewrite, a smudge) would have been undetectable.

Frozen predicate (identical sentence in contract.md §C2 v2, this docstring
and the receipt labels): at the measured revision this check prints
`pin=1 blob=1 match=1 met=true` (exit 0), where the pinned sha256 in
`.ufo/waves/round-65/sources/s432-pin.json` equals
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b and the
sha256 of the committed blob `.ufo/waves/round-64/sources/S432.live.html`
at that revision equals the same digest; while at the base d3a4e402 the
check prints `pin=0 met=false` (exit 1) because no pin file exists.

Components:
  pin    the pin file exists at the revision, parses as JSON, and its
         "sha256" cell equals the FROZEN digest constant embedded below
         (a pin file naming a different digest is pin=0 — the constant is
         not read from the pin file alone).
  blob   the committed S432.live.html blob exists at the revision.
  match  sha256(committed blob) == the FROZEN digest.

Reads committed bytes only (`git show <revision>:<path>`), never the
worktree. Exits 0 met / 1 not met / 2 could-not-evaluate (bad revision,
never a traceback).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys

BASE = "d3a4e40228c307954fa6ced6cab03654faac1ffa"
PIN_REL = ".ufo/waves/round-65/sources/s432-pin.json"
BLOB_REL = ".ufo/waves/round-64/sources/S432.live.html"
FROZEN_DIGEST = "63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b"


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def git_show(root: str, revision: str, rel: str) -> bytes | None:
    proc = subprocess.run(
        ["git", "-C", root, "show", f"{revision}:{rel}"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if proc.returncode:
        return None
    return proc.stdout


def evaluate(root: str, rev: str) -> tuple[int, str]:
    probe = subprocess.run(
        ["git", "-C", root, "rev-parse", "--verify", rev],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if probe.returncode:
        print(f"could-not-evaluate: revision {rev} unreadable", file=sys.stderr)
        return 2, ""

    pin_blob = git_show(root, rev, PIN_REL)
    pin = 0
    pin_detail = "absent"
    if pin_blob is not None:
        try:
            parsed = json.loads(pin_blob.decode("utf-8"))
            digest = parsed.get("sha256")
            if digest == FROZEN_DIGEST:
                pin = 1
                pin_detail = "ok"
            else:
                pin_detail = f"digest_mismatch:{digest}"
        except Exception as exc:
            pin_detail = f"unreadable:{type(exc).__name__}"

    blob = git_show(root, rev, BLOB_REL)
    blob_c = int(blob is not None)
    match = int(blob is not None and sha256(blob) == FROZEN_DIGEST)
    met = bool(pin and blob_c and match)
    out = (f"revision={rev} pin={pin} pin_detail={pin_detail} blob={blob_c} "
           f"match={match} met={str(met).lower()}")
    return (0 if met else 1), out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision", default=BASE)
    args = ap.parse_args()
    try:
        code, out = evaluate(args.root, args.revision)
    except Exception as exc:
        print(f"could-not-evaluate: internal fault: {type(exc).__name__}",
              file=sys.stderr)
        return 2
    if out:
        print(out)
    return code


if __name__ == "__main__":
    sys.exit(main())
