#!/usr/bin/env python3
"""Deliberately do-nothing C1 control: parse a manifest, then report it clean."""
from __future__ import annotations

import argparse
import json
import sys

EXIT_CLEAN = 0
EXIT_INPUT = 2
EXIT_USAGE = 64


class UsageError(Exception):
    """Invalid command-line shape."""


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise UsageError(message)


def parse_cli(argv: list[str]) -> argparse.Namespace:
    parser = ArgumentParser(
        prog="placebo.py",
        usage="placebo.py --manifest PATH [--root PATH] [--revision REV] [--json [PATH]]",
        allow_abbrev=False,
        description="Do-nothing control: read a v1 manifest and report every check clean.",
    )
    parser.add_argument("--manifest", required=True, metavar="PATH")
    parser.add_argument("--root", default=".", metavar="PATH")
    parser.add_argument("--revision", metavar="REV")
    parser.add_argument("--json", nargs="?", const="-", metavar="PATH")
    if sum(token == "--manifest" or token.startswith("--manifest=") for token in argv) > 1:
        raise UsageError("--manifest given more than once")
    return parser.parse_args(argv)


def make_report(manifest_path: str) -> dict[str, object]:
    with open(manifest_path, "r", encoding="utf-8") as source:
        manifest = json.load(source)
    if not isinstance(manifest, dict) or manifest.get("version") != 1:
        raise ValueError("manifest must be a version-1 object")
    checks = manifest.get("checks")
    if not isinstance(checks, list):
        raise ValueError("manifest checks must be an array")

    # Intentional placebo: do not open rules, resolve paths, or evaluate checks.
    return {
        "version": 1,
        "verdict": "clean",
        "checksEvaluated": len(checks),
        "findings": [],
    }


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_cli(sys.argv[1:] if argv is None else argv)
    except UsageError as exc:
        print(f"placebo.py: {exc}", file=sys.stderr)
        return EXIT_USAGE

    try:
        report = make_report(args.manifest)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        report = {
            "version": 1,
            "verdict": "could-not-evaluate",
            "checksEvaluated": 0,
            "findings": [{"check": None, "reason": "input_invalid"}],
        }
        exit_code = EXIT_INPUT
    else:
        exit_code = EXIT_CLEAN

    encoded = json.dumps(report, sort_keys=True, separators=(",", ":"))
    if args.json is None or args.json == "-":
        print(encoded)
    else:
        try:
            with open(args.json, "w", encoding="utf-8", newline="\n") as output:
                output.write(encoded + "\n")
        except OSError as exc:
            print(f"placebo.py: cannot write JSON output: {exc}", file=sys.stderr)
            return EXIT_INPUT
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
