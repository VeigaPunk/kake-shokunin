#!/usr/bin/env python3
"""Round-47 C2 counter — r46 closure-routed prose defects repaired (R3-R6).

Frozen predicate (identical sentence in SCORECARD, this file and the report):
"The r46 closure-routed prose defects are repaired append-only:
`python3 -B .ufo/waves/round-47/c47_routed_count.py --root . --revision <commit>`
decides: before = at base cd42e3c310ba442e89dde638ba6401adaefaf3e8 all four
routed defects R3 (ledger population misstated as '12 rows'), R4 (five ledger
reason cells misattribute charter vs ds4cc-marketplace / the wrong critic),
R5 (the LOG round-46 entry names no landing-commit full hash) and R6 (the
unreceipted round-46 verdict-time `freshness-sweep --offline exit 0` claim)
are outstanding; after = at the round-47 tip each defect has a committed
append-only fix — an R3 correction line naming the 20 data rows
(12 LOG.md + 8 SCORECARD.md) in LOG.md, an R4 '## Round-47 corrections' block
in `corpus/quality/citation-adjudications.md` naming all five tokens and the
corrected reason phrase for each, an R5 line in LOG.md naming the full hashes
ee43e66367bf23e386ff29029b9ea60515efd9d1 and 861113eb0eea4d51bd0614c542aa6ecb7cc9a843, and R6 closed by an explicit
withdrawal in LOG.md plus a committed
`.ufo/waves/round-47/verification/offline-sweep-r47-rerun.txt` labelled
'R47 rerun only; not contemporaneous r46 verdict-time evidence' and recording
`--offline` exit=0; the rerun is not retroactive evidence for r46."

Read-only: materializes committed bytes via `git show`/`git ls-tree` only.
Exits: 0 = met (0 outstanding); 1 = not met; 2 = could-not-evaluate; 64 = usage.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys

EXIT_MET = 0
EXIT_NOT_MET = 1
EXIT_INPUT = 2
EXIT_USAGE = 64

LEDGER = "corpus/quality/citation-adjudications.md"
RECEIPT_DIR = ".ufo/waves/round-47/verification"
R4_EXPECTED = {
    "b74190e": "Corrected reason: charter repo commit from the 2026-09-28 push series",
    "d69dd22": "Corrected reason: charter repo commit in the 2026-09-28 push series",
    "0c767c2": "Corrected reason: charter repo commit in the same 2026-09-28 push series",
    "b9db4b1": "Corrected reason: charter repo commit in the same 2026-09-28 push series",
    "dc8e1adf": "Corrected reason: Round-34/35 seat-sandbox commit (`CriticProbeLeniency` all-false entry, met true, 12 of 12)",
}
R5_HASHES = (
    "ee43e66367bf23e386ff29029b9ea60515efd9d1",
    "861113eb0eea4d51bd0614c542aa6ecb7cc9a843",
)


class UsageError(Exception):
    pass


class InputError(Exception):
    pass


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise UsageError(message)


def parse_cli(argv: list[str]) -> argparse.Namespace:
    parser = ArgumentParser(
        prog="c47_routed_count.py",
        usage="c47_routed_count.py --root PATH --revision REV [--json [PATH]]",
        allow_abbrev=False,
    )
    parser.add_argument("--root", required=True, metavar="PATH")
    parser.add_argument("--revision", required=True, metavar="REV")
    parser.add_argument("--json", nargs="?", const="-", metavar="PATH")
    if sum(t == "--root" or t.startswith("--root=") for t in argv) > 1:
        raise UsageError("--root given more than once")
    return parser.parse_args(argv)


def git_show(root: str, revision: str, rel: str) -> str | None:
    proc = subprocess.run(
        ["git", "-C", root, "show", f"{revision}:{rel}"],
        capture_output=True)
    if proc.returncode != 0:
        return None
    return proc.stdout.decode("utf-8", "replace")


def git_ls_tree(root: str, revision: str, rel: str) -> list[str]:
    proc = subprocess.run(
        ["git", "-C", root, "ls-tree", "-r", "--name-only", revision, rel],
        capture_output=True)
    if proc.returncode != 0:
        raise InputError(f"cannot ls-tree {rel} at {revision}")
    out = proc.stdout.decode("utf-8", "replace").strip()
    return [line for line in out.splitlines() if line]



def r4_reasons_fixed(ledger: str) -> bool:
    marker = "## Round-47 corrections"
    if marker not in ledger:
        return False
    entries: dict[str, str] = {}
    for raw in ledger.split(marker, 1)[1].split("- Row `")[1:]:
        token, separator, remainder = raw.partition("`")
        if separator:
            entries[token] = " ".join(remainder.split())
    return all(
        expected.lower() in entries.get(token, "").lower()
        for token, expected in R4_EXPECTED.items()
    )

def main(argv: list[str]) -> int:
    try:
        args = parse_cli(argv)
    except UsageError as exc:
        print(f"usage error: {exc}", file=sys.stderr)
        return EXIT_USAGE

    log = git_show(args.root, args.revision, "LOG.md")
    ledger = git_show(args.root, args.revision, LEDGER)
    if log is None or ledger is None:
        print(f"could-not-evaluate: missing population file at {args.revision}",
              file=sys.stderr)
        return EXIT_INPUT
    try:
        receipt_paths = git_ls_tree(args.root, args.revision, RECEIPT_DIR)
    except InputError as exc:
        print(f"could-not-evaluate: {exc}", file=sys.stderr)
        return EXIT_INPUT

    log_lines = log.splitlines()
    r3_fixed = any("R3" in line and "20 data rows" in line for line in log_lines)
    r5_fixed = any(all(h in line for h in R5_HASHES) for line in log_lines)
    r4_fixed = r4_reasons_fixed(ledger)
    r6_withdrawn = any(
        "[r47-correction R6 withdrawal]" in line
        and "round-46" in line.lower() and "withdrawn" in line.lower()
        for line in log_lines)
    r6_rerun_receipted = False
    for rel in receipt_paths:
        if rel.rsplit("/", 1)[-1] != "offline-sweep-r47-rerun.txt":
            continue
        text = git_show(args.root, args.revision, rel)
        if (text and "R47 rerun only; not contemporaneous r46 verdict-time evidence" in text
                and "exit=0" in text and "--offline" in text):
            r6_rerun_receipted = True
            break
    r6_fixed = r6_withdrawn and r6_rerun_receipted

    fixed = {"R3": r3_fixed, "R4": r4_fixed, "R5": r5_fixed, "R6": r6_fixed}
    outstanding = sum(1 for done in fixed.values() if not done)
    met = outstanding == 0
    result = {
        "revision": args.revision,
        "fixed": fixed,
        "outstanding": outstanding,
        "verdict": "C2_MET" if met else "C2_NOT_MET",
    }
    print(f"outstanding={outstanding}/4 {result['verdict']}")
    if args.json is not None:
        payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.json == "-":
            sys.stdout.write(payload)
        else:
            with open(args.json, "w", encoding="utf-8") as handle:
                handle.write(payload)
    return EXIT_MET if met else EXIT_NOT_MET


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
