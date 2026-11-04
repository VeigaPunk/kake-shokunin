#!/usr/bin/env python3
"""Decode ordered Referrer-Policy field values from a stdin JSON string list.

W3C Referrer Policy section 8.1: each recognized, nonempty token replaces
its predecessor. Unknown tokens do not reset the policy; comparison is
case-sensitive. This offline decoder does not authorize publication.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

POLICIES = frozenset((
    "no-referrer",
    "no-referrer-when-downgrade",
    "same-origin",
    "origin",
    "strict-origin",
    "origin-when-cross-origin",
    "strict-origin-when-cross-origin",
    "unsafe-url",
))


def effective_policy(fields: list[str]) -> str:
    """Walk fields and their comma-separated tokens in their original order."""
    policy = ""
    for field in fields:
        for token in field.split(","):
            token = token.strip()
            if token in POLICIES:
                policy = token
    return policy


def reject_object(pairs: list[tuple[str, object]]) -> object:
    # Objects are never valid input, including those containing duplicate keys.
    raise ValueError("JSON objects are not supported; expected a list of strings")


def reject_constant(value: str) -> object:
    raise ValueError(f"invalid JSON constant: {value}")


def decode(data: str) -> str:
    fields = json.loads(data, object_pairs_hook=reject_object,
                        parse_constant=reject_constant)
    if not isinstance(fields, list) or any(not isinstance(v, str) for v in fields):
        raise ValueError("expected a JSON list of strings")
    return effective_policy(fields)


def selftest() -> int:
    """Exercise the real CLI with in-memory fixtures and no filesystem writes."""
    tool = str(Path(__file__).resolve())
    passed = 0

    def check(label: str, payload: bytes, expected: str | None = None,
              code: int = 0, argv: tuple[str, ...] = ()) -> None:
        nonlocal passed
        result = subprocess.run([sys.executable, "-B", tool, *argv],
                                input=payload, capture_output=True)
        assert result.returncode == code, (label, result.returncode, result.stderr)
        if expected is None:
            assert result.stdout == b"", (label, result.stdout)
            assert result.stderr, (label, "missing diagnostic")
        else:
            assert json.loads(result.stdout) == {"effective": expected}, (label, result.stdout)
            assert result.stderr == b"", (label, result.stderr)
        passed += 1

    for token in sorted(POLICIES):
        check(f"recognized {token}", json.dumps([f" , {token} , ignored, "]).encode(), token)
    check("ordered fields", b'["same-origin, unsafe-url", "origin-when-cross-origin, invalid"]',
          "origin-when-cross-origin")
    check("reversed fields", b'["origin-when-cross-origin, invalid", "same-origin, unsafe-url"]',
          "unsafe-url")
    check("case sensitive", b'["ORIGIN, Same-Origin, UNSAFE-URL"]', "")
    check("empty list", b'[]', "")
    check("empty tokens", b'["", ", ,", "unrecognized"]', "")
    check("unknown preserves earlier policy", b'["strict-origin-when-cross-origin", "bogus,,"]',
          "strict-origin-when-cross-origin")
    for label, payload in (
        ("missing input", b""),
        ("malformed JSON", b'["origin"'),
        ("trailing data", b'[] []'),
        ("object", b'{}'),
        ("duplicate object", b'{"effective":"origin","effective":"unsafe-url"}'),
        ("nested object", b'[{}]'),
        ("scalar string", b'"origin"'),
        ("null", b'null'),
        ("boolean field", b'[true]'),
        ("number field", b'[3]'),
        ("null field", b'[null]'),
        ("nested list", b'[["origin"]]'),
        ("nonstandard constant", b'[NaN]'),
        ("invalid UTF-8", b'["\xff"]'),
    ):
        check(label, payload, code=1)
    check("unknown option", b'[]', code=64, argv=("--unknown",))
    check("positional argument", b'[]', code=64, argv=("origin",))
    check("selftest argument", b'[]', code=64, argv=("--selftest=1",))
    check("no abbreviated option", b'[]', code=64, argv=("--self",))
    print(f"selftest: {passed}/{passed} passed")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0], allow_abbrev=False)
    parser.add_argument("--selftest", action="store_true")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 64
    if args.selftest:
        return selftest()
    try:
        policy = decode(sys.stdin.buffer.read().decode("utf-8"))
    except (ValueError, UnicodeError, RecursionError) as exc:
        print(f"fault: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"effective": policy}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
