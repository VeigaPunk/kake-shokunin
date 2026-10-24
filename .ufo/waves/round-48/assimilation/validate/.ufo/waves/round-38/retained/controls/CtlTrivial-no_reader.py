#!/usr/bin/env python3
"""Round-38 C1 pre-freeze control: no-reader (status and fault rules only).

Implements exactly:
  * usage: `--manifest PATH` only (exit 64 otherwise);
  * (g) manifest faults, including the round-38 (h) manifest part: NaN, Infinity and
    -Infinity outside a string are not JSON, so one `input_invalid` finding and
    nothing evaluated; not a regular file, > 64 MiB, unreadable, not UTF-8, not
    JSON, non-object, `version` not the integer 1, `checks` not a list;
  * (h) JSON numbers of any length: counts/ids/status parse without an int-digit
    limit (huge integers are kept as text), an integer `robotsStatus` outside the
    three ranges - however many digits - is a `check_invalid` for that check while
    the other checks still evaluate, a number of any length in an unread field
    changes nothing;
  * (i) URL characters, judged as written before any parsing: an ASCII character
    outside letters, digits, `-` `.` `_` `~`, the reserved set
    `:/?#[]@!$&'()*+,;=%` makes the check `check_invalid`; non-ASCII is kept;
  * (f) check faults: object, non-empty unique string id, integer `robotsStatus` in
    200-299/400-499/500-599, product-token `userAgent`, `expect` in the two values,
    absolute http(s) URL with a host, and for 200-299 a relative `robots` path to a
    regular file inside the resolved manifest directory (metadata only);
  * (a) access result, and the verdict/exit mapping.

The work it skips: it never opens, stats-as-content, reads or parses any robots
file. For 200-299 it decides `allow` for every URL (which also satisfies the (k)
implicit allow on `/robots.txt` vacuously). It therefore skips (b), (c), (d),
(e) and (k)'s rule-decided half entirely: every 2xx check whose correct decision
is `disallow` is judged `allow`, and every 2xx check expecting `allow` whose file
would block the URL is missed. Expected 1 of 20 under the round-38 counter.
"""
from __future__ import annotations

import json
import os
import stat
import sys
from pathlib import Path
from urllib.parse import urlsplit

REPORT_VERSION = 1
MAX_MANIFEST_BYTES = 64 * 1024 * 1024

EXIT_CLEAN = 0
EXIT_FAILED_POLICY = 1
EXIT_COULD_NOT_EVALUATE = 2
EXIT_USAGE = 64

VERDICT_CLEAN = "clean"
VERDICT_FAILED_POLICY = "failed-policy"
VERDICT_COULD_NOT_EVALUATE = "could-not-evaluate"

BLOCKING_REASONS = frozenset(("input_invalid", "check_invalid"))

# (i) RFC 3986 section 2 characters, plus `%`. Non-ASCII is kept and checked only by
# the parsing rules; every other ASCII character is a check fault.
ALLOWED_URL_ASCII = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "0123456789"
    "-._~"
    ":/?#[]@!$&'()*+,;=%"
)

URL_SETS = frozenset(("http", "https"))


class BigInt:
    """A JSON integer too long to convert: cannot be an in-range status (rule (h))."""

    __slots__ = ("text",)

    def __init__(self, text: str) -> None:
        self.text = text


def parse_int(text: str) -> int | BigInt:
    # JSON numbers of any length are JSON (rule (h)). Converting a >18-digit string
    # is never needed: no in-range robotsStatus or version has that many digits.
    if len(text) <= 18:
        return int(text)
    return BigInt(text)


def reject_constant(name: str) -> None:
    # (h): NaN, Infinity and -Infinity outside a string are not JSON.
    raise ValueError("non-JSON constant " + name)


def finding(check_id: str | None, reason: str) -> dict:
    return {"check": check_id, "reason": reason}


def load_manifest(path: str) -> dict | None:
    """(g) plus (h)'s manifest part. Returns the parsed object or None for a fault."""
    if not path or "\x00" in path:
        return None
    try:
        st = os.stat(path)
    except (OSError, ValueError):
        return None
    if not stat.S_ISREG(st.st_mode):
        return None
    if st.st_size > MAX_MANIFEST_BYTES:
        return None
    try:
        with open(path, "rb") as handle:
            raw = handle.read(MAX_MANIFEST_BYTES + 1)
    except (OSError, ValueError):
        return None
    if len(raw) > MAX_MANIFEST_BYTES:
        return None
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None
    try:
        data = json.loads(text, parse_int=parse_int, parse_constant=reject_constant)
    except (ValueError, RecursionError):
        return None
    if not isinstance(data, dict):
        return None
    version = data.get("version")
    if type(version) is not int or version != 1:
        return None
    if not isinstance(data.get("checks"), list):
        return None
    return data


def product_token_ok(value: object) -> bool:
    """RFC 9309 section 2.2.1: one or more ASCII letters, `_` or `-`."""
    if not isinstance(value, str) or not value:
        return False
    for ch in value:
        if not (("a" <= ch <= "z") or ("A" <= ch <= "Z") or ch in "_-"):
            return False
    return True


def url_chars_ok(url: str) -> bool:
    """(i): judged as written, before any parsing."""
    for ch in url:
        if ord(ch) < 128 and ch not in ALLOWED_URL_ASCII:
            return False
    return True


def url_ok(url: object) -> bool:
    """(f): absolute http(s) URL with a non-empty host, after the (i) character rule."""
    if not isinstance(url, str) or not url:
        return False
    if not url_chars_ok(url):
        return False
    try:
        parts = urlsplit(url)
        host = parts.hostname
    except ValueError:
        return False
    return parts.scheme in URL_SETS and bool(host)


def robots_path_ok(dir_raw: Path, dir_real: Path, robots: object) -> bool:
    """(f): relative path to a regular file inside the manifest directory. Metadata
    only: `os.stat` and `resolve` never read the file's bytes."""
    if not isinstance(robots, str) or not robots or "\x00" in robots:
        return False
    if os.path.isabs(robots):
        return False
    candidate = dir_raw / robots
    try:
        st = os.stat(candidate)
        if not stat.S_ISREG(st.st_mode):
            return False
        resolved = candidate.resolve(strict=True)
    except (OSError, RuntimeError, ValueError):
        return False
    return dir_real in resolved.parents


def validate_check(
    check: object, dir_raw: Path, dir_real: Path, seen_ids: set[str]
) -> tuple[bool, str | None]:
    """(f), (h) status part and (i). Returns (valid, id-for-a-fault)."""
    if not isinstance(check, dict):
        return False, None
    raw_id = check.get("id")
    cid = raw_id if (isinstance(raw_id, str) and len(raw_id) > 0) else None
    if cid is None:
        return False, None
    # A repeated id is measured against every earlier check's id, valid or not.
    if cid in seen_ids:
        return False, cid
    seen_ids.add(cid)

    status = check.get("robotsStatus")
    if type(status) is not int:  # booleans, floats and huge integers (BigInt) fault
        return False, cid
    if not (200 <= status <= 299 or 400 <= status <= 499 or 500 <= status <= 599):
        return False, cid

    if not product_token_ok(check.get("userAgent")):
        return False, cid

    expect = check.get("expect")
    if not isinstance(expect, str) or expect not in ("allow", "disallow"):
        return False, cid

    if not url_ok(check.get("url")):
        return False, cid

    if 200 <= status <= 299 and not robots_path_ok(dir_raw, dir_real, check.get("robots")):
        return False, cid
    return True, cid


def evaluate(check: dict) -> list[dict]:
    """(a) only. 200-299 is decided `allow` without opening the robots file."""
    cid = check["id"]
    status = check["robotsStatus"]
    expect = check["expect"]
    decision = "disallow" if 500 <= status <= 599 else "allow"
    if expect == "allow" and decision == "disallow":
        return [finding(cid, "blocked")]
    if expect == "disallow" and decision == "allow":
        return [finding(cid, "exposed")]
    return []


def verdict_for(findings: list[dict]) -> str:
    for item in findings:
        if item["reason"] in BLOCKING_REASONS:
            return VERDICT_COULD_NOT_EVALUATE
    if findings:
        return VERDICT_FAILED_POLICY
    return VERDICT_CLEAN


def emit(verdict: str, evaluated: int, findings: list[dict]) -> int:
    report = {
        "version": REPORT_VERSION,
        "verdict": verdict,
        "checksEvaluated": evaluated,
        "findings": findings,
    }
    sys.stdout.write(json.dumps(report, separators=(",", ":")) + "\n")
    if verdict == VERDICT_CLEAN:
        return EXIT_CLEAN
    if verdict == VERDICT_FAILED_POLICY:
        return EXIT_FAILED_POLICY
    return EXIT_COULD_NOT_EVALUATE


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--manifest":
        sys.stderr.write("usage: robots_audit.py --manifest PATH\n")
        return EXIT_USAGE
    manifest = load_manifest(argv[1])
    if manifest is None:
        return emit(VERDICT_COULD_NOT_EVALUATE, 0, [finding(None, "input_invalid")])

    try:
        dir_raw = Path(os.path.abspath(argv[1])).parent
        dir_real = dir_raw.resolve(strict=True)
    except (OSError, RuntimeError, ValueError):
        return emit(VERDICT_COULD_NOT_EVALUATE, 0, [finding(None, "input_invalid")])

    findings: list[dict] = []
    evaluated = 0
    seen_ids: set[str] = set()
    for check in manifest["checks"]:
        valid, cid = validate_check(check, dir_raw, dir_real, seen_ids)
        if not valid:
            findings.append(finding(cid, "check_invalid"))
            continue
        evaluated += 1
        findings.extend(evaluate(check))
    return emit(verdict_for(findings), evaluated, findings)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
