#!/usr/bin/env python3
"""Quote-class derivation for a quoted span against two retained blobs.

Derives the round-50 match class of a quoted span: `raw-substring` when the
span is a substring of the retained HTML, else `collapsed-only` when it is a
substring of the retained flat-text rendering (see
.ufo/waves/round-63/quote-class/extract_text.py for that rendering's recipe),
else `absent`. The class is derived from the blobs, never asserted; a
collapsed-only span is never described as a raw substring nor the reverse.

Usage:
  quote_class.py classify --quote "..." --raw <file> --text <file> [--json]
  quote_class.py --selftest [--json]

Exits: 0 determination printed; 2 unreadable input or usage fault.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

LANE_ROOT = Path.cwd()
FIXTURES = Path("scripts/fixtures/quote-class")


class UsageError(Exception):
    pass


def classify(quote: str, raw: str, text: str) -> str:
    if quote in raw:
        return "raw-substring"
    if quote in text:
        return "collapsed-only"
    return "absent"


FIXTURE_CASES = [
    {
        "id": "inline_raw_substring",
        "raw": FIXTURES / "inline.raw.html",
        "text": FIXTURES / "inline.txt",
        "quote": "quick brown fox",
        "expected": "raw-substring",
    },
    {
        "id": "markup_collapsed_only",
        "raw": FIXTURES / "markup.raw.html",
        "text": FIXTURES / "markup.txt",
        "quote": "The `X-Content-Type-Options` header marks the response",
        "expected": "collapsed-only",
    },
    {
        "id": "absent_everywhere",
        "raw": FIXTURES / "inline.raw.html",
        "text": FIXTURES / "inline.txt",
        "quote": "this span occurs in no retained blob at all",
        "expected": "absent",
    },
    {
        "id": "s432_real",
        "raw": Path(".ufo/waves/round-61/sources/S432.html"),
        "text": Path(".ufo/waves/round-63/quote-class/S432.txt"),
        "quote": (
            "The `X-Content-Type-Options` response header can be used to "
            "require checking of a response\u2019s `Content-Type` header "
            "against the destination of a request."
        ),
        "expected": "collapsed-only",
    },
]


def run_selftest() -> dict:
    cases = []
    for case in FIXTURE_CASES:
        raw_path = LANE_ROOT / case["raw"]
        text_path = LANE_ROOT / case["text"]
        error = None
        derived = "unevaluable"
        try:
            raw = raw_path.read_bytes().decode("utf-8", errors="replace")
            text = text_path.read_bytes().decode("utf-8", errors="replace")
            derived = classify(case["quote"], raw, text)
        except OSError as exc:
            error = f"{type(exc).__name__}: {exc}"
        passed = error is None and derived == case["expected"]
        cases.append({
            "id": case["id"],
            "derived": derived,
            "expected": case["expected"],
            "passed": passed,
            **({"error": error} if error else {}),
        })
    total = len(cases)
    passed = sum(1 for c in cases if c["passed"])
    return {"cases": cases, "total": total, "passed": passed,
            "ok": passed == total}


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command")
    cl = sub.add_parser("classify")
    cl.add_argument("--quote", required=True)
    cl.add_argument("--raw", required=True)
    cl.add_argument("--text", required=True)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        result = run_selftest()
        if args.json:
            print(json.dumps(result, sort_keys=True))
        else:
            for case in result["cases"]:
                mark = "pass" if case["passed"] else "FAIL"
                print(f"case {case['id']}: derived={case['derived']} "
                      f"expected={case['expected']} {mark}")
            print(f"selftest {result['passed']}/{result['total']}")
        return 0 if result["ok"] else 1

    if args.command == "classify":
        try:
            raw = Path(args.raw).read_bytes().decode("utf-8", errors="replace")
            text = Path(args.text).read_bytes().decode("utf-8", errors="replace")
        except OSError as exc:
            print(f"could-not-evaluate: {type(exc).__name__}: {exc}",
                  file=sys.stderr)
            return 2
        derived = classify(args.quote, raw, text)
        if args.json:
            print(json.dumps({"derived": derived}))
        else:
            print(f"derived={derived}")
        return 0

    ap.error("one of --selftest or classify is required")
    return 64


if __name__ == "__main__":
    sys.exit(main())
