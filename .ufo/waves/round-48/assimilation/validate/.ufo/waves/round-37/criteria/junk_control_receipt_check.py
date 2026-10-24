#!/usr/bin/env python3
"""Require a later correction and receipt for the round-36 junk-control claim."""
import argparse
import json
import os
import subprocess
import sys

CLAIM = "No do-nothing, junk, all-false, no-reader or shortcut control reached 25 under any version."
CORRECTION = "Round 36's junk control was untested; it is now run."
RECEIPT = ".ufo/waves/round-37/verification/control-r36-junk.json"
RECEIPT_LINK = "verification/control-r36-junk.json"
EXIT_RECEIPT = ".ufo/waves/round-37/verification/control-r36-junk.exit"


def show(root: str, revision: str, path: str) -> bytes | None:
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    result = subprocess.run(
        ["git", "-C", root, "show", f"{revision}:{path}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )
    if result.returncode:
        return None
    return result.stdout


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--revision", required=True)
    args = parser.parse_args()

    lesson = show(args.root, args.revision, "corpus/lessons/round-36.md")
    if lesson is None:
        print("FAIL: cannot read round-36 lesson at revision", args.revision)
        return 1
    if CLAIM.encode() not in lesson:
        print("FAIL: expected round-36 control claim not found")
        return 1

    scorecard = show(args.root, args.revision, "SCORECARD.md")
    if scorecard is None or CORRECTION.encode() not in scorecard:
        print("FAIL: no later correction says the round-36 junk control was untested")
        return 1
    if RECEIPT_LINK.encode() not in scorecard:
        print("FAIL: correction does not cite the junk-control receipt", RECEIPT_LINK)
        return 1

    receipt_bytes = show(args.root, args.revision, RECEIPT)
    exit_bytes = show(args.root, args.revision, EXIT_RECEIPT)
    if receipt_bytes is None or exit_bytes is None:
        print("FAIL: cited receipt or exit receipt is absent")
        return 1
    try:
        receipt = json.loads(receipt_bytes)
    except (UnicodeDecodeError, json.JSONDecodeError):
        print("FAIL: cited receipt is not valid JSON")
        return 1
    if not (
        receipt.get("cases") == 28
        and receipt.get("passed") == 0
        and receipt.get("target") == 25
        and receipt.get("met") is False
        and str(receipt.get("toolFile", "")).endswith("source_recheck_junk.py")
        and exit_bytes.strip() == b"1"
    ):
        print("FAIL: junk-control receipt does not show 0/28, met=false, exit=1")
        return 1

    print("PASS: later correction is backed by the junk-control receipt (0/28, met=false, exit=1)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
