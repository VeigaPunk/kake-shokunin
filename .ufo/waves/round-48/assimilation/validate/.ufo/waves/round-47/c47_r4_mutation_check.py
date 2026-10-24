#!/usr/bin/env python3
"""Show that the round-47 R4 reason-fidelity predicate rejects each old reason."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys

LEDGER = "corpus/quality/citation-adjudications.md"
COUNTER = ".ufo/waves/round-47/c47_routed_count.py"
EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_INPUT = 2
EXIT_USAGE = 64


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise ValueError(message)


def git_show(root: str, revision: str, path: str) -> str:
    proc = subprocess.run(
        ["git", "-C", root, "show", f"{revision}:{path}"],
        capture_output=True,
    )
    if proc.returncode != 0:
        raise OSError(f"cannot read {path} at {revision}")
    return proc.stdout.decode("utf-8", "replace")


def main(argv: list[str]) -> int:
    parser = ArgumentParser(
        prog="c47_r4_mutation_check.py",
        usage="c47_r4_mutation_check.py --root PATH --revision REV",
        allow_abbrev=False,
    )
    parser.add_argument("--root", required=True, metavar="PATH")
    parser.add_argument("--revision", required=True, metavar="REV")
    try:
        args = parser.parse_args(argv)
    except ValueError as exc:
        print(f"usage error: {exc}", file=sys.stderr)
        return EXIT_USAGE

    try:
        source = git_show(args.root, args.revision, COUNTER)
        ledger = git_show(args.root, args.revision, LEDGER)
    except OSError as exc:
        print(f"could-not-evaluate: {exc}", file=sys.stderr)
        return EXIT_INPUT

    namespace: dict[str, object] = {"__name__": "c47_counter_under_test"}
    exec(compile(source, COUNTER, "exec"), namespace)
    check = namespace["r4_reasons_fixed"]
    expected = namespace["R4_EXPECTED"]
    if not callable(check) or not isinstance(expected, dict) or not check(ledger):
        print("R4_REASON_FIDELITY base=FAIL", file=sys.stderr)
        return EXIT_FAIL

    normalized = " ".join(ledger.split())
    killed = 0
    for token, phrase in expected.items():
        if token == "dc8e1adf":
            mutant_phrase = phrase.replace("CriticProbeLeniency", "CriticC2Sufficiency")
        else:
            mutant_phrase = phrase.replace("charter repo commit", "ds4cc-marketplace repo commit")
        mutated, count = re.subn(re.escape(phrase), mutant_phrase, normalized,
                                 count=1, flags=re.I)
        if count != 1 or check(mutated):
            print(f"R4_REASON_FIDELITY mutant_survived={token}", file=sys.stderr)
            return EXIT_FAIL
        killed += 1

    print(f"R4_REASON_FIDELITY base=pass mutants={killed}/5_rejected PASS")
    return EXIT_PASS


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
