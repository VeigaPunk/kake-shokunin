#!/usr/bin/env python3
"""Round-50 C2 counter — pre-append order and wave-grant durability.

Frozen predicate (the same sentence in the plan, in PREDICATE, and in every
receipt):

    met: durable == 1 of 1

The single check passes only when every condition below holds. Artifacts are
read with `git show` or `git merge-base --is-ancestor`. A missing proof is
durable 0, not a usage error. That is the do-nothing result.

  1. order-proof.json names pre_rev (40 lowercase hex) and adopted_ids
     exactly ["S286"].
  2. pre_rev is a strict ancestor of the measured revision.
  3. The live registry at pre_rev has no S286 row. The mirror at pre_rev has one.
  4. The census argv blob at pre_rev contains --file and the mirror path, and
     does not contain --root.
  5. The census exit blob at pre_rev is 0. The stdout blob has no E03 or E04.
  6. The live registry at the measured revision has an S286 row.
  7. wave-cite-proof.json names grant_rev (40 lowercase hex), a strict ancestor
     of the measured revision, distinct from pre_rev.
  8. At grant_rev, wave-grant.txt has one line
     granted lane=kake wave=r50-w1 seats=N live=<int> pending=<int> cap=<int>
     with N in 32..64.
  9. At grant_rev, dispatch-command.txt contains kimi and --prompt, and does
     not contain --auto.
  10. LOG.md at grant_rev does not contain r50-w1. LOG.md at the measured
      revision contains r50-w1 and the grant_rev hash.
  11. settlement.json at the measured revision has spawn equal to N, and
      replacements is an empty list.

Exit codes: 0 met, 1 not met, 2 could-not-evaluate, 64 usage.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys

PREDICATE = "met: durable == 1 of 1"
FROZEN_IDS = ["S286"]
ORDER_PROOF = ".ufo/waves/round-50/assimilation/order-proof.json"
MIRROR = ".ufo/waves/round-50/assimilation/pre-append/corpus/SOURCES.md"
CENSUS_ARGV = ".ufo/waves/round-50/assimilation/pre-append/census-argv.txt"
CENSUS_STDOUT = ".ufo/waves/round-50/assimilation/pre-append/census-stdout.txt"
CENSUS_EXIT = ".ufo/waves/round-50/assimilation/pre-append/census-exit.txt"
CITE_PROOF = ".ufo/waves/round-50/wave-cite-proof.json"
GRANT = ".ufo/waves/round-50/wave-grant.txt"
DISPATCH = ".ufo/waves/round-50/dispatch-command.txt"
SETTLEMENT = ".ufo/waves/round-50/settlement.json"
GRANT_RE = re.compile(
    r"^granted lane=kake wave=r50-w1 seats=(\d+) live=\d+ pending=\d+ cap=\d+$"
)
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
    proof_blob = git_show(root, revision, ORDER_PROOF)
    pre_rev = None
    if proof_blob is None:
        reasons.append("order proof absent")
    else:
        try:
            proof = json.loads(proof_blob.decode("utf-8"))
        except Exception as exc:
            proof = None
            reasons.append(f"order proof unreadable: {type(exc).__name__}")
        if proof is not None:
            if proof.get("predicate") != PREDICATE:
                reasons.append("order proof predicate differs")
            if proof.get("adopted_ids") != FROZEN_IDS:
                reasons.append("adopted_ids is not the frozen set")
            pre_rev = proof.get("pre_rev")
            if not isinstance(pre_rev, str) or not re.fullmatch(r"[0-9a-f]{40}", pre_rev):
                reasons.append("pre_rev is not 40 lowercase hex")
                pre_rev = None
    if pre_rev:
        if pre_rev == revision or not ancestor(root, pre_rev, revision):
            reasons.append("pre_rev is not a strict ancestor")
        live_before = row_ids(git_show(root, pre_rev, "corpus/SOURCES.md"))
        mirror_ids = row_ids(git_show(root, pre_rev, MIRROR))
        live_after = row_ids(git_show(root, revision, "corpus/SOURCES.md"))
        if "S286" in live_before:
            reasons.append("S286 already in live registry at pre_rev")
        if "S286" not in mirror_ids:
            reasons.append("S286 missing from pre-append mirror")
        if "S286" not in live_after:
            reasons.append("S286 missing from live registry at measured revision")
        argv = git_show(root, pre_rev, CENSUS_ARGV)
        stdout = git_show(root, pre_rev, CENSUS_STDOUT)
        exit_blob = git_show(root, pre_rev, CENSUS_EXIT)
        argv_text = (argv or b"").decode("utf-8", "replace")
        stdout_text = (stdout or b"").decode("utf-8", "replace")
        if argv is None or "--file" not in argv_text or "pre-append/corpus/SOURCES.md" not in argv_text:
            reasons.append("census argv is not a --file mirror validation")
        elif "--root" in argv_text:
            reasons.append("census argv uses --root")
        if exit_blob is None or exit_blob.decode("utf-8", "replace").strip() != "0":
            reasons.append("census exit at pre_rev is not 0")
        if stdout is None or "E03" in stdout_text or "E04" in stdout_text:
            reasons.append("census stdout missing or contains E03 or E04")
    cite_blob = git_show(root, revision, CITE_PROOF)
    grant_rev = None
    if cite_blob is None:
        reasons.append("wave-cite proof absent")
    else:
        try:
            cite = json.loads(cite_blob.decode("utf-8"))
        except Exception as exc:
            cite = None
            reasons.append(f"wave-cite proof unreadable: {type(exc).__name__}")
        if cite is not None:
            if cite.get("predicate") != PREDICATE:
                reasons.append("wave-cite predicate differs")
            grant_rev = cite.get("grant_rev")
            if not isinstance(grant_rev, str) or not re.fullmatch(r"[0-9a-f]{40}", grant_rev):
                reasons.append("grant_rev is not 40 lowercase hex")
                grant_rev = None
    seats = None
    if grant_rev:
        if grant_rev == revision or not ancestor(root, grant_rev, revision):
            reasons.append("grant_rev is not a strict ancestor")
        if pre_rev and grant_rev == pre_rev:
            reasons.append("grant_rev is not distinct from pre_rev")
        grant = git_show(root, grant_rev, GRANT)
        dispatch = git_show(root, grant_rev, DISPATCH)
        log_grant = git_show(root, grant_rev, "LOG.md")
        if grant is None:
            reasons.append("wave-grant stdout absent at grant_rev")
        else:
            lines = [line for line in grant.decode("utf-8", "replace").splitlines() if line.strip()]
            matched = [GRANT_RE.fullmatch(line.strip()) for line in lines]
            good = [item for item in matched if item]
            if len(good) != 1 or len(lines) != 1:
                reasons.append("wave-grant stdout is not exactly one granted line")
            else:
                seats = int(good[0].group(1))
                if not 32 <= seats <= 64:
                    reasons.append(f"granted seats {seats} outside 32..64")
        if dispatch is None:
            reasons.append("dispatch command absent at grant_rev")
        else:
            command = dispatch.decode("utf-8", "replace")
            if "kimi" not in command or "--prompt" not in command:
                reasons.append("dispatch command is not kimi --prompt")
            if "--auto" in command:
                reasons.append("dispatch command contains --auto")
        if log_grant is None:
            reasons.append("LOG.md absent at grant_rev")
        elif "r50-w1" in log_grant.decode("utf-8", "replace"):
            reasons.append("LOG.md at grant_rev already cites the wave")
    log_now = git_show(root, revision, "LOG.md")
    if log_now is None:
        reasons.append("LOG.md absent at measured revision")
    else:
        log_text = log_now.decode("utf-8", "replace")
        if "r50-w1" not in log_text:
            reasons.append("LOG.md at measured revision does not cite the wave")
        if grant_rev and grant_rev not in log_text:
            reasons.append("LOG.md does not cite grant_rev")
    settlement_blob = git_show(root, revision, SETTLEMENT)
    if settlement_blob is None:
        reasons.append("settlement absent")
    else:
        try:
            settlement = json.loads(settlement_blob.decode("utf-8"))
        except Exception as exc:
            settlement = None
            reasons.append(f"settlement unreadable: {type(exc).__name__}")
        if settlement is not None:
            if seats is not None and settlement.get("spawn") != seats:
                reasons.append("settlement spawn does not equal granted seats")
            if settlement.get("replacements") != []:
                reasons.append("settlement replacements is not an empty list")
    return {
        "schema": "kake-r50-c2-counter-v1",
        "revision": revision,
        "predicate": PREDICATE,
        "durable": 0 if reasons else 1,
        "total": 1,
        "met": not reasons,
        "reasons": reasons,
    }


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        args = parse_cli(argv)
    except UsageError as exc:
        print(f"c50_durable: {exc}", file=sys.stderr)
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
    print(f"C2 durable {result['durable']}/{result['total']} met={result['met']}")
    if result["reasons"]:
        for reason in result["reasons"]:
            print(f"  FAIL {reason}")
    return 0 if result["met"] else 1


if __name__ == "__main__":
    sys.exit(main())
