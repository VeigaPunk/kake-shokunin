#!/usr/bin/env python3
"""Detect entry values already exposed by a receipt in Git history."""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections.abc import Iterator

PAIR_RE = re.compile(r"(?<!\S)([A-Za-z0-9_.:-]+)=([A-Za-z0-9_.:+-]+)(?!\S)")


class Unreadable(Exception):
    """A requested Git blob or its contents cannot be read."""


def read_blob(repo: str, revision: str, path: str) -> bytes:
    if not revision or revision.startswith("-"):
        raise Unreadable(f"invalid revision {revision!r}")
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    done = subprocess.run(
        ["git", "-c", "core.hooksPath=/dev/null", "-C", repo, "cat-file", "blob", f"{revision}:{path}"],
        env=env,
        capture_output=True,
        check=False,
        timeout=30,
    )
    if done.returncode != 0:
        detail = done.stderr.decode("utf-8", "replace").strip().replace("\n", " ")
        raise Unreadable(f"cannot read {path!r} at {revision!r}" + (f": {detail}" if detail else ""))
    return done.stdout


def scalar_strings(value: object) -> Iterator[str]:
    if isinstance(value, dict):
        for child in value.values():
            yield from scalar_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from scalar_strings(child)
    elif value is None:
        yield "null"
    elif isinstance(value, bool):
        yield "true" if value else "false"
    elif isinstance(value, (int, float)):
        yield str(value)
    elif isinstance(value, str):
        yield value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check whether an entry line's key=value values were published in a Git receipt."
    )
    parser.add_argument("--repo", required=True, help="repository containing both revisions")
    parser.add_argument("--receipt-rev", required=True, help="revision containing the receipt blob")
    parser.add_argument("--receipt", required=True, help="receipt path at --receipt-rev")
    parser.add_argument("--entry-rev", required=True, help="revision containing the entry blob")
    parser.add_argument("--entry", required=True, help="entry path at --entry-rev")
    parser.add_argument("--line-regex", required=True, help="regular expression selecting one entry line")
    return parser


def run(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        receipt_bytes = read_blob(args.repo, args.receipt_rev, args.receipt)
        entry_bytes = read_blob(args.repo, args.entry_rev, args.entry)
        receipt = json.loads(receipt_bytes)
        entry = entry_bytes.decode("utf-8")
        pattern = re.compile(args.line_regex)
        matching_lines = [line for line in entry.splitlines() if pattern.search(line)]
        if len(matching_lines) != 1:
            raise Unreadable(f"expected one matching entry line; found {len(matching_lines)}")
        pairs = PAIR_RE.findall(matching_lines[0])
        if not pairs:
            raise Unreadable("matching entry line has no key=value pairs")
    except (OSError, UnicodeError, json.JSONDecodeError, re.error, subprocess.SubprocessError, Unreadable) as exc:
        print(f"prebuild_leak_check: unreadable input: {exc}", file=sys.stderr)
        return 2

    receipt_values = set(scalar_strings(receipt))
    missing = [f"{key}={value}" for key, value in pairs if value not in receipt_values]
    print("matched values: " + " ".join(f"{key}={value}" for key, value in pairs))
    if not missing:
        print("FAIL: every matched value appears as a value in the receipt JSON (pre-build target published)")
        return 1
    print("PASS: not every matched value appears as a value in the receipt JSON; absent: " + ", ".join(missing))
    return 0


def main() -> int:
    return run()


if __name__ == "__main__":
    raise SystemExit(main())
