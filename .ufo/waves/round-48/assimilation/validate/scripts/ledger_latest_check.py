#!/usr/bin/env python3
"""Compare the latest declared ledger figures with their committed receipts."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path, PurePosixPath

SPEC_PATH = ".ufo/waves/round-44/ledger-quotes.json"
RESCORE_DIR = ".ufo/waves/round-43/verification/l1-rescores"
NUMBER_RE = re.compile(r"\d+(?:\.\d+)?\Z")


class InputError(Exception):
    """An input needed to evaluate the ledger could not be read or parsed."""


def contract_spec() -> dict:
    """Return the fixed three-figure contract; the JSON cannot narrow scope."""
    return {
        "version": 1,
        "figures": [
            {
                "id": "rescore-tally",
                "file": "SCORECARD.md",
                "pattern": r"re-scored\s+(\d+)\s+of\s+the\s+27",
                "receipt": f"{RESCORE_DIR}/*.json",
                "derive": {"kind": "distinct-tool-sha256", "field": "toolSha256"},
            },
            {
                "id": "donothing-ratios",
                "file": "LOG.md",
                "pattern": r"not met \(T1\s+([\d.]+),\s*T5\s+([\d.]+)\)",
                "receipt": ".ufo/waves/round-43/verification/freeze/ref41-base.json",
                "derive": {"kind": "ratios", "fields": ["T1", "T5"]},
            },
            {
                "id": "build-ratio-range",
                "file": "LOG.md",
                "pattern": r"T1\s+([\d.]+)–([\d.]+), T5\s+([\d.]+)–([\d.]+)",
                "receipt": [
                    ".ufo/waves/round-43/verification/freeze/build-1.json",
                    ".ufo/waves/round-43/verification/freeze/build-2.json",
                    ".ufo/waves/round-43/verification/freeze/build-3.json",
                ],
                "derive": {"kind": "ratio-extrema", "fields": ["T1", "T5"]},
            },
        ],
    }


def parse_json_bytes(data: bytes, source: str):
    try:
        text = data.decode("utf-8")
        return json.loads(
            text,
            parse_float=Decimal,
            parse_constant=lambda value: (_ for _ in ()).throw(
                ValueError(f"invalid JSON number {value}")
            ),
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise InputError(f"{source}: invalid UTF-8 JSON: {exc}") from exc


def git_output(root: Path, args: list[str], source: str) -> bytes:
    try:
        result = subprocess.run(
            ["git", *args], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
        )
    except OSError as exc:
        raise InputError(f"{source}: cannot run git: {exc}") from exc
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        suffix = f": {detail}" if detail else ""
        raise InputError(f"{source}: git command failed with exit {result.returncode}{suffix}")
    return result.stdout


def committed_bytes(root: Path, relative: str) -> bytes:
    if PurePosixPath(relative).is_absolute() or ".." in PurePosixPath(relative).parts:
        raise InputError(f"unsafe committed path: {relative}")
    return git_output(root, ["show", f"master:{relative}"], relative)


def read_ledger(root: Path, relative: str) -> str:
    path = root.joinpath(*PurePosixPath(relative).parts)
    try:
        if path.is_file():
            data = path.read_bytes()
        else:
            data = committed_bytes(root, relative)
        return data.decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise InputError(f"{relative}: cannot read UTF-8 ledger: {exc}") from exc


def load_spec(root: Path) -> list[dict]:
    path = root.joinpath(*PurePosixPath(SPEC_PATH).parts)
    try:
        data = parse_json_bytes(path.read_bytes(), SPEC_PATH)
    except OSError as exc:
        raise InputError(f"{SPEC_PATH}: cannot read: {exc}") from exc
    expected = contract_spec()
    if data != expected:
        raise InputError("ledger quote spec differs from the fixed three-figure contract")
    return data["figures"]


def committed_json(root: Path, relative: str) -> dict:
    data = parse_json_bytes(committed_bytes(root, relative), relative)
    if not isinstance(data, dict):
        raise InputError(f"{relative}: receipt must be a JSON object")
    return data


def rescore_receipts(root: Path, pattern: str) -> list[tuple[str, dict]]:
    if pattern != f"{RESCORE_DIR}/*.json":
        raise InputError("unexpected rescore receipt pattern")
    raw = git_output(root, ["ls-tree", "-r", "--name-only", "master", "--", RESCORE_DIR], pattern)
    try:
        names = raw.decode("utf-8").splitlines()
    except UnicodeDecodeError as exc:
        raise InputError(f"{pattern}: invalid path encoding in git tree") from exc
    parent = PurePosixPath(RESCORE_DIR)
    paths = sorted(
        name for name in names
        if PurePosixPath(name).parent == parent and PurePosixPath(name).suffix == ".json"
    )
    if not paths:
        raise InputError(f"{pattern}: no committed JSON receipts")
    return [(name, committed_json(root, name)) for name in paths]


def receipt_ratio(receipt: dict, field: str, source: str) -> Decimal:
    try:
        raw = receipt["ratios"][field]
    except (KeyError, TypeError) as exc:
        raise InputError(f"{source}: missing ratios.{field}") from exc
    if isinstance(raw, bool) or not isinstance(raw, (int, Decimal)):
        raise InputError(f"{source}: ratios.{field} is not numeric")
    try:
        return Decimal(raw)
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise InputError(f"{source}: invalid ratios.{field}") from exc


def derive_values(root: Path, entry: dict) -> list[int | Decimal]:
    derive = entry["derive"]
    kind = derive["kind"]
    if kind == "distinct-tool-sha256":
        receipts = rescore_receipts(root, entry["receipt"])
        hashes = set()
        for source, receipt in receipts:
            value = receipt.get(derive["field"])
            if not isinstance(value, str) or not value:
                raise InputError(f"{source}: missing non-empty {derive['field']}")
            hashes.add(value)
        return [len(hashes)]

    if kind == "ratios":
        receipt = committed_json(root, entry["receipt"])
        return [receipt_ratio(receipt, field, entry["receipt"]) for field in derive["fields"]]

    if kind == "ratio-extrema":
        values: dict[str, list[Decimal]] = {field: [] for field in derive["fields"]}
        for source in entry["receipt"]:
            receipt = committed_json(root, source)
            for field in derive["fields"]:
                values[field].append(receipt_ratio(receipt, field, source))
        if any(not series for series in values.values()):
            raise InputError(f"{entry['id']}: no ratio receipts")
        return [
            endpoint
            for field in derive["fields"]
            for endpoint in (min(values[field]), max(values[field]))
        ]

    raise InputError(f"{entry['id']}: unsupported derive kind {kind!r}")


def rounded_like(value: int | Decimal, quoted: str) -> str:
    if not NUMBER_RE.fullmatch(quoted):
        raise InputError(f"quoted value is not a non-negative decimal: {quoted!r}")
    places = len(quoted.partition(".")[2]) if "." in quoted else 0
    try:
        number = Decimal(value)
        quantum = Decimal(1).scaleb(-places)
        return format(number.quantize(quantum, rounding=ROUND_HALF_UP), f".{places}f")
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise InputError(f"cannot round derived value {value!r}") from exc


def latest_match(text: str, pattern: str, source: str) -> tuple[re.Match, int]:
    try:
        compiled = re.compile(pattern, re.S)
    except re.error as exc:
        raise InputError(f"{source}: invalid pattern: {exc}") from exc
    matches = list(compiled.finditer(text))
    if not matches:
        raise InputError(f"{source}: pattern has no matches")
    match = matches[-1]
    line = text.count("\n", 0, match.start()) + 1
    return match, line


def render_values(figure_id: str, values: list[str]) -> str:
    if figure_id == "donothing-ratios":
        return f"T1 {values[0]}, T5 {values[1]}"
    if figure_id == "build-ratio-range":
        return f"T1 {values[0]}–{values[1]}, T5 {values[2]}–{values[3]}"
    return values[0]


def evaluate(figure_id: str, quoted: list[str], expected: list[int | Decimal]) -> tuple[bool, list[str]]:
    if not quoted or len(quoted) != len(expected):
        raise InputError(f"{figure_id}: quote/receipt value count differs")
    derived = [rounded_like(value, quote) for quote, value in zip(quoted, expected)]
    return quoted == derived, derived


def run_check(root: Path) -> int:
    figures = load_spec(root)
    mismatches = 0
    for entry in figures:
        text = read_ledger(root, entry["file"])
        match, line = latest_match(text, entry["pattern"], entry["file"])
        quoted = list(match.groups())
        expected = derive_values(root, entry)
        matches, derived = evaluate(entry["id"], quoted, expected)
        verdict = "MATCH" if matches else "MISMATCH"
        mismatches += not matches
        print(
            f"{entry['id']} {verdict} "
            f"quoted={render_values(entry['id'], quoted)} "
            f"derived={render_values(entry['id'], derived)} "
            f"{entry['file']}:{line}"
        )
    print(f"ledger-quotes: {len(figures)} figures, {mismatches} mismatches")
    return 1 if mismatches else 0


def run_selftest() -> int:
    pattern = r"re-scored\s+(\d+)\s+of\s+the\s+27"
    fixtures = [
        (
            "matching",
            "earlier: re-scored 18 of the 27\ncorrection: re-scored 14 of the 27\n",
            True,
        ),
        (
            "mismatching",
            "earlier: re-scored 14 of the 27\nlatest: re-scored 18 of the 27\n",
            False,
        ),
    ]
    failures = 0
    print("ledger_latest_check --selftest")
    for name, text, should_match in fixtures:
        match, _line = latest_match(text, pattern, f"{name} fixture")
        actual, derived = evaluate("rescore-tally", list(match.groups()), [14])
        passed = actual is should_match
        failures += not passed
        if name == "mismatching" and not actual:
            print(f"  RED MISMATCH {name} fixture quoted={match.group(1)} derived={derived[0]}")
        else:
            verdict = "MATCH" if actual else "MISMATCH"
            print(f"  {'PASS' if passed else 'FAIL'} {name} fixture {verdict} quoted={match.group(1)} derived={derived[0]}")
    print(f"selftest: {len(fixtures) - failures}/{len(fixtures)} passed")
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ledger_latest_check.py",
        description="Check the last declared ledger statements against committed round-43 receipts.",
        allow_abbrev=False,
    )
    parser.add_argument("--root", help="lane repository root (default: parent of scripts/)")
    parser.add_argument("--selftest", action="store_true", help="run matching and mismatching synthetic fixtures")
    args = parser.parse_args(argv)
    if args.selftest:
        return run_selftest()
    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
    try:
        return run_check(root)
    except InputError as exc:
        print(f"ledger_latest_check: unreadable input: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
