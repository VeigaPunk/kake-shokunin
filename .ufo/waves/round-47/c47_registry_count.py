#!/usr/bin/env python3
"""Round-47 C1 counter — gate registry + selftest receipts for the r46 tools.

Frozen predicate (identical sentence in SCORECARD, this file and the report):
"Both round-46 gates are registered and receipted:
`python3 -B .ufo/waves/round-47/c47_registry_count.py --root . --revision <commit>`
decides: before = at base cd42e3c310ba442e89dde638ba6401adaefaf3e8 neither
`scripts/redirect_audit.py` nor `scripts/citation_lint.py` has a SKILL.md
gate-registry row nor a committed selftest receipt; after = at the round-47
tip both tools have a gate-registry row and a committed selftest receipt under
`.ufo/waves/round-47/verification/` that names the tool path, the tool sha256,
the selftest tally and exit=0."

A registry row is a SKILL.md table line (starts with '|') naming
'scripts/<tool>'. A receipt is a committed file under
.ufo/waves/round-47/verification/ whose content names the tool path, a 64-hex
tool sha256, the tool's selftest tally ('selftest: 23/23 passed' or
'selftest: 8/8 passed') and 'exit=0'. Prose tallies in LOG.md/SCORECARD.md are
never receipts.

Read-only: materializes committed bytes via `git show`/`git ls-tree` only.
Exits: 0 = met (2/2 rows, 2/2 receipts); 1 = not met; 2 = could-not-evaluate;
64 = usage.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys

EXIT_MET = 0
EXIT_NOT_MET = 1
EXIT_INPUT = 2
EXIT_USAGE = 64

TOOLS = {
    "redirect_audit.py": re.compile(r"selftest: 23/23 passed"),
    "citation_lint.py": re.compile(r"selftest: 8/8 passed"),
}
RECEIPT_DIR = ".ufo/waves/round-47/verification"
SHA256_RE = re.compile(r"\b[0-9a-f]{64}\b")


class UsageError(Exception):
    pass


class InputError(Exception):
    pass


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise UsageError(message)


def parse_cli(argv: list[str]) -> argparse.Namespace:
    parser = ArgumentParser(
        prog="c47_registry_count.py",
        usage="c47_registry_count.py --root PATH --revision REV [--json [PATH]]",
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


def main(argv: list[str]) -> int:
    try:
        args = parse_cli(argv)
    except UsageError as exc:
        print(f"usage error: {exc}", file=sys.stderr)
        return EXIT_USAGE

    skill = git_show(args.root, args.revision, "SKILL.md")
    if skill is None:
        print(f"could-not-evaluate: no SKILL.md at {args.revision}", file=sys.stderr)
        return EXIT_INPUT

    try:
        receipt_paths = git_ls_tree(args.root, args.revision, RECEIPT_DIR)
    except InputError as exc:
        print(f"could-not-evaluate: {exc}", file=sys.stderr)
        return EXIT_INPUT

    rows: dict[str, bool] = {}
    receipts: dict[str, bool] = {}
    for tool, tally_re in TOOLS.items():
        needle = f"scripts/{tool}"
        rows[tool] = any(
            line.lstrip().startswith("|") and needle in line
            for line in skill.splitlines())
        found = False
        for rel in receipt_paths:
            text = git_show(args.root, args.revision, rel)
            if text is None:
                continue
            if (needle in text and tally_re.search(text)
                    and "exit=0" in text and SHA256_RE.search(text)):
                found = True
                break
        receipts[tool] = found

    row_count = sum(rows.values())
    receipt_count = sum(receipts.values())
    met = row_count == 2 and receipt_count == 2
    result = {
        "revision": args.revision,
        "registry_rows": f"{row_count}/2",
        "registry_row_detail": rows,
        "selftest_receipts": f"{receipt_count}/2",
        "selftest_receipt_detail": receipts,
        "verdict": "C1_MET" if met else "C1_NOT_MET",
    }
    print(f"registry_rows={row_count}/2 receipts={receipt_count}/2 "
          f"{result['verdict']}")
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
