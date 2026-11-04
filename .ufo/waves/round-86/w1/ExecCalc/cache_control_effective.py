#!/usr/bin/env python3
"""Bounded RFC 9111 response Cache-Control reader; not a cache permission model.

Decode a JSON object on stdin with no options, or run --selftest.
RFC 9111 §§1.2.2, 4.2.1, 5.2: retain first occurrences, not minima.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from datetime import timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

TOKEN = re.compile(r"[!#$%&'*+.^_`|~0-9A-Za-z-]+\Z")
DIGITS = re.compile(r"[0-9]+\Z")
CAP = 2147483648
USAGE = "usage: cache_control_effective.py [--selftest] < input.json"


def split_directives(value: str) -> list[str]:
    """Commas in quoted strings (including escaped quotes) are not separators."""
    parts = []
    start = 0
    quoted = escaped = False
    for index, char in enumerate(value):
        if escaped:
            escaped = False
        elif quoted and char == "\\":
            escaped = True
        elif char == '"':
            quoted = not quoted
        elif char == "," and not quoted:
            parts.append(value[start:index].strip(" \t"))
            start = index + 1
    parts.append(value[start:].strip(" \t"))
    return parts


def argument(raw: str) -> str:
    if TOKEN.fullmatch(raw):
        return raw
    if not raw.startswith('"'):
        raise ValueError("invalid directive argument")
    result = []
    index = 1
    while index < len(raw):
        char = raw[index]
        if char == '"':
            if index != len(raw) - 1:
                raise ValueError("trailing quoted-string data")
            return "".join(result)
        if char == "\\":
            index += 1
            if index >= len(raw):
                raise ValueError("unfinished quoted-pair")
            char = raw[index]
        if not (char == "\t" or 32 <= ord(char) <= 126 or 128 <= ord(char) <= 255):
            raise ValueError("invalid quoted-string character")
        result.append(char)
        index += 1
    raise ValueError("unfinished quoted-string")


def http_date(value: str | None):
    if value is None:
        return None
    try:
        result = parsedate_to_datetime(value)
        # The obsolete asctime HTTP-date form has no explicit zone; it means UTC.
        if result.tzinfo is None:
            result = result.replace(tzinfo=timezone.utc)
        return result.astimezone(timezone.utc)
    except (ValueError, TypeError, OverflowError) as exc:
        raise ValueError("unparsable HTTP-date") from exc


def decode(payload: object) -> dict:
    if not isinstance(payload, dict):
        raise ValueError("input must be a JSON object")
    fields = payload.get("cache_control", [])
    shared = payload.get("shared", False)
    if not isinstance(fields, list) or any(not isinstance(v, str) for v in fields):
        raise ValueError("cache_control must be an array of strings")
    if not isinstance(shared, bool):
        raise ValueError("shared must be a boolean")
    for key in ("expires", "date"):
        if payload.get(key) is not None and not isinstance(payload[key], str):
            raise ValueError(f"{key} must be a string or null")
    expires = http_date(payload.get("expires"))
    date = http_date(payload.get("date"))
    first = {}
    duplicates = []
    invalid = []
    seen = set()
    for part in split_directives(",".join(fields)):
        if not part:
            continue
        name, sep, raw = part.partition("=")
        name = name.strip(" \t").lower()
        if name in seen:
            if name not in duplicates:
                duplicates.append(name)
            continue
        seen.add(name)
        try:
            if not TOKEN.fullmatch(name):
                raise ValueError("invalid directive name")
            value = argument(raw.strip(" \t")) if sep else None
            if name in ("max-age", "s-maxage"):
                if value is None or not DIGITS.fullmatch(value):
                    raise ValueError("invalid delta-seconds")
                # Avoid int conversion limits for arbitrarily long digit strings.
                digits = value.lstrip("0") or "0"
                value = CAP if len(digits) > 10 or (len(digits) == 10 and digits > str(CAP)) else int(digits)
            elif name == "no-cache" and value is not None:
                names = [v.strip(" \t") for v in value.split(",") if v.strip(" \t")]
                if not names or any(not TOKEN.fullmatch(v) for v in names):
                    raise ValueError("invalid no-cache field names")
                value = names
            first[name] = value
        except ValueError:
            invalid.append(name)

    life = None
    basis = "no-explicit-expiration"
    if "no-store" in first:
        basis = "no-store"
    elif shared and "s-maxage" in first:
        life, basis = first["s-maxage"], "s-maxage"
    elif "max-age" in first:
        life, basis = first["max-age"], "max-age"
    elif expires is not None and date is not None:
        life, basis = max(0, int((expires - date).total_seconds())), "expires"
    qualified = first.get("no-cache")
    return {
        "storable": "no-store" not in first,
        "freshness_lifetime_seconds": life,
        "basis": basis,
        "no_cache": "no-cache" in first and qualified is None,
        "no_cache_qualified": qualified if isinstance(qualified, list) else [],
        "must_revalidate": "must-revalidate" in first,
        "must_understand": "must-understand" in first,
        "duplicate_directives": duplicates,
        # Global conflict excludes field-specific no-cache (bounded contract).
        "conflict": "max-age" in seen and "no-cache" in first and qualified is None,
        "invalid_directives": invalid,
    }


def selftest() -> int:
    """Isolated source-derived fixtures, with subprocess exit-code assertions."""
    script = str(Path(__file__).resolve())
    with tempfile.TemporaryDirectory(prefix="cache-control-selftest-") as temporary:
        scratch = Path(temporary)
        number = 0

        def invoke(text: str, args: tuple[str, ...] = (), code: int = 0):
            nonlocal number
            number += 1
            fixture = scratch / f"fixture-{number}.json"
            fixture.write_text(text, encoding="utf-8")
            with fixture.open("rb") as stream:
                result = subprocess.run(
                    [sys.executable, "-B", script, *args], stdin=stream,
                    capture_output=True, check=False, cwd=scratch,
                )
            assert result.returncode == code, (number, result.returncode, result.stderr)
            if code:
                assert result.stderr and not result.stdout, (number, result)
                return None
            assert not result.stderr, (number, result.stderr)
            return json.loads(result.stdout)

        def parse(fields, **extra):
            return invoke(json.dumps({"cache_control": fields, **extra}))

        assert invoke("{}")["basis"] == "no-explicit-expiration"
        ordered = parse(['MAX-AGE="73"', 'max-age=2, must-revalidate, must-understand'])
        assert ordered["freshness_lifetime_seconds"] == 73
        assert ordered["duplicate_directives"] == ["max-age"]
        assert ordered["must_revalidate"] and ordered["must_understand"]
        assert parse(["max-age=31, s-maxage=91"], shared=True)["freshness_lifetime_seconds"] == 91
        assert parse(["max-age=31, s-maxage=91"])["freshness_lifetime_seconds"] == 31
        blocked = parse(["no-store, max-age=17"])
        assert not blocked["storable"] and blocked["basis"] == "no-store"
        assert blocked["freshness_lifetime_seconds"] is None
        qualified = parse(['no-cache="ETag, X-Mode", max-age=13'])
        assert qualified["no_cache_qualified"] == ["ETag", "X-Mode"]
        assert not qualified["no_cache"] and not qualified["conflict"]
        assert parse(["no-cache"])["no_cache"]
        assert parse(["max-age=13, no-cache"])["conflict"]
        assert parse(['extension="a, b\\\"c", max-age=9'])["freshness_lifetime_seconds"] == 9
        assert parse(["max-age=" + "9" * 5000])["freshness_lifetime_seconds"] == CAP
        assert parse(["max-age=" + "0" * 5000 + "7"])["freshness_lifetime_seconds"] == 7
        for invalid in ("-4", "2.5", "word", "", '"-7"'):
            result = parse(["max-age=" + invalid])
            assert result["invalid_directives"] == ["max-age"]
            assert result["freshness_lifetime_seconds"] is None
        assert parse(["max-age=bad, max-age=8"])["freshness_lifetime_seconds"] is None
        dates = {"date": "Mon, 02 Nov 2026 00:00:00 GMT", "expires": "Mon, 02 Nov 2026 00:01:07 GMT"}
        assert parse([], **dates)["freshness_lifetime_seconds"] == 67
        assert parse([], date=dates["expires"], expires=dates["date"])["freshness_lifetime_seconds"] == 0
        invoke("{", code=1)
        for payload in ([], {"shared": 1}, {"cache_control": "max-age=3"}, {"cache_control": [3]}, {"date": 4}, {"expires": "invalid"}):
            invoke(json.dumps(payload), code=1)
        invoke("{}", ("--bad-option",), 64)
        invoke("{}", ("--selftest", "extra"), 64)
        invoke("", code=64)
    print(f"selftest: {number} isolated fixtures passed")
    return 0


def reject_constant(value: str):
    raise ValueError(f"invalid JSON constant: {value}")


def main() -> int:
    if sys.argv[1:] == ["--selftest"]:
        return selftest()
    if sys.argv[1:]:
        print(USAGE, file=sys.stderr)
        return 64
    try:
        text = sys.stdin.read()
        if not text.strip():
            print(USAGE, file=sys.stderr)
            return 64
        result = decode(json.loads(text, parse_constant=reject_constant))
    except (ValueError, UnicodeError, RecursionError) as exc:
        print(f"invalid input: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, separators=(",", ":"), allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
