#!/usr/bin/env python3
"""Round-49 C1 counter — pre-append order, committed bytes only.

Frozen predicate (the same sentence in the plan, in PREDICATE, and in every
receipt):

    met: order == 1 of 1

The single order check passes only when every condition below holds, and
every artifact is read with `git show <revision>:<path>` or
`git merge-base --is-ancestor`. This counter does not open SOURCES.md, the
mirror, the census stdout, or the proof from the worktree.

  1. `.ufo/waves/round-49/assimilation/order-proof.json` at the measured
     revision names pre_rev (40 lowercase hex) and adopted_ids exactly
     ["S273", "S274"].
  2. pre_rev is a strict ancestor of the measured revision.
  3. `git show pre_rev:corpus/SOURCES.md` has no registry row for either id.
  4. `git show pre_rev:.ufo/waves/round-49/assimilation/pre-append/corpus/SOURCES.md`
     has a registry row for both ids.
  5. The census argv blob at pre_rev contains `--file` and the mirror path,
     and does not contain `--root` (not a full-repo validation).
  6. The census exit blob at pre_rev is `0`, and the stdout blob contains no
     E03 or E04 finding.
  7. `git show <measured>:corpus/SOURCES.md` has a registry row for both ids.
  8. The quote-truth counter blob at the measured revision contains
     COMMITTED_BYTES_ONLY and `git show`, and does not contain
     `os.path.join(root` (the round-48 worktree read).

A missing proof is order 0, not a usage error. That is the do-nothing result.

Exit codes: 0 met, 1 not met, 2 could-not-evaluate, 64 usage.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys

PREDICATE = "met: order == 1 of 1"
FROZEN_IDS = ["S273", "S274"]
PROOF = ".ufo/waves/round-49/assimilation/order-proof.json"
MIRROR = ".ufo/waves/round-49/assimilation/pre-append/corpus/SOURCES.md"
CENSUS_ARGV = ".ufo/waves/round-49/assimilation/pre-append/census-argv.txt"
CENSUS_STDOUT = ".ufo/waves/round-49/assimilation/pre-append/census-stdout.txt"
CENSUS_EXIT = ".ufo/waves/round-49/assimilation/pre-append/census-exit.txt"
QUOTE_COUNTER = ".ufo/waves/round-49/c49_quote_truth.py"
ROW_RE = re.compile(r"^\s*\|\s*(S[0-9]{3,})\s*\|")


class UsageError(Exception):
    pass


def parse_cli(argv):
    values = {"root": None, "revision": None, "json": None}
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg in ("--root", "--revision", "--json"):
            index += 1
            if index >= len(argv):
                raise UsageError(f"{arg} needs a value")
            values[arg[2:]] = argv[index]
        elif arg.startswith("--root="):
            values["root"] = arg.split("=", 1)[1]
        elif arg.startswith("--revision="):
            values["revision"] = arg.split("=", 1)[1]
        elif arg.startswith("--json="):
            values["json"] = arg.split("=", 1)[1]
        else:
            raise UsageError(f"unknown argument: {arg}")
        index += 1
    if not values["root"] or not values["revision"]:
        raise UsageError("--root and --revision are required")
    return values


def git_show(root: str, revision: str, rel: str) -> bytes | None:
    proc = subprocess.run(
        ["git", "-C", root, "show", f"{revision}:{rel}"],
        capture_output=True,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout


def ancestor(root: str, older: str, newer: str) -> bool:
    proc = subprocess.run(
        ["git", "-C", root, "merge-base", "--is-ancestor", older, newer],
        capture_output=True,
    )
    return proc.returncode == 0


def row_ids(blob: bytes | None) -> set[str]:
    if blob is None:
        return set()
    found = set()
    in_registry = False
    for line in blob.decode("utf-8", "replace").splitlines():
        if line.strip().startswith("## "):
            in_registry = line.strip().lower().startswith("## registry")
            continue
        if not in_registry:
            continue
        match = ROW_RE.match(line)
        if match:
            found.add(match.group(1))
    return found


def run(root: str, revision: str) -> dict:
    reasons = []
    proof_blob = git_show(root, revision, PROOF)
    pre_rev = None
    if proof_blob is None:
        reasons.append("proof absent")
    else:
        try:
            proof = json.loads(proof_blob.decode("utf-8"))
        except Exception as exc:
            proof = None
            reasons.append(f"proof unreadable: {type(exc).__name__}")
        if proof is not None:
            pre_rev = proof.get("pre_rev")
            if proof.get("adopted_ids") != FROZEN_IDS:
                reasons.append("adopted_ids is not the frozen set")
            if proof.get("predicate") != PREDICATE:
                reasons.append("proof predicate differs from the frozen sentence")
            if not isinstance(pre_rev, str) or not re.fullmatch(r"[0-9a-f]{40}", pre_rev):
                reasons.append("pre_rev is not 40 lowercase hex")
                pre_rev = None
    if pre_rev:
        if pre_rev == revision or not ancestor(root, pre_rev, revision):
            reasons.append("pre_rev is not a strict ancestor of the measured revision")
        live_before = row_ids(git_show(root, pre_rev, "corpus/SOURCES.md"))
        mirror_ids = row_ids(git_show(root, pre_rev, MIRROR))
        live_after = row_ids(git_show(root, revision, "corpus/SOURCES.md"))
        for sid in FROZEN_IDS:
            if sid in live_before:
                reasons.append(f"{sid} already in live registry at pre_rev")
            if sid not in mirror_ids:
                reasons.append(f"{sid} missing from pre-append mirror")
            if sid not in live_after:
                reasons.append(f"{sid} missing from live registry at measured revision")
        argv = git_show(root, pre_rev, CENSUS_ARGV)
        stdout = git_show(root, pre_rev, CENSUS_STDOUT)
        exit_blob = git_show(root, pre_rev, CENSUS_EXIT)
        argv_text = (argv or b"").decode("utf-8", "replace")
        stdout_text = (stdout or b"").decode("utf-8", "replace")
        if argv is None:
            reasons.append("census argv absent at pre_rev")
        else:
            if "--file" not in argv_text or "pre-append/corpus/SOURCES.md" not in argv_text:
                reasons.append("census argv is not a --file mirror validation")
            if "--root" in argv_text:
                reasons.append("census argv uses --root; not a mirror-only validation")
        if exit_blob is None or exit_blob.decode("utf-8", "replace").strip() != "0":
            reasons.append("census exit at pre_rev is not 0")
        if stdout is None:
            reasons.append("census stdout absent at pre_rev")
        elif "E03" in stdout_text or "E04" in stdout_text:
            reasons.append("census stdout at pre_rev contains E03 or E04")
    quote = git_show(root, revision, QUOTE_COUNTER)
    if quote is None:
        reasons.append("quote counter absent at measured revision")
    else:
        source = quote.decode("utf-8", "replace")
        if "COMMITTED_BYTES_ONLY" not in source or "git show" not in source:
            reasons.append("quote counter does not declare committed-byte reads")
        if "os.path.join(root" in source:
            reasons.append("quote counter still joins a worktree path")
    order = 0 if reasons else 1
    return {
        "schema": "kake-r49-c1-counter-v1",
        "revision": revision,
        "predicate": PREDICATE,
        "pre_rev": pre_rev,
        "adoptedIds": FROZEN_IDS,
        "order": order,
        "total": 1,
        "met": order == 1,
        "reasons": reasons,
        "fullRepoValidation": False,
    }


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        args = parse_cli(argv)
    except UsageError as exc:
        print(f"c49_order: {exc}", file=sys.stderr)
        return 64
    try:
        result = run(args["root"], args["revision"])
    except Exception as exc:
        print(json.dumps({"error": f"{type(exc).__name__}: {exc}"}))
        return 2
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args["json"]:
        with open(args["json"], "w", encoding="utf-8") as handle:
            handle.write(text + "\n")
    print(f"C1 order {result['order']}/{result['total']} met={result['met']}")
    for reason in result["reasons"]:
        print(f"  FAIL {reason}")
    return 0 if result["met"] else 1


if __name__ == "__main__":
    sys.exit(main())
