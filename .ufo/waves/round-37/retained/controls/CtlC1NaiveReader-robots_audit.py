#!/usr/bin/env python3
"""Round-37 C1 naive-reader control (`robots_audit.py`).

Implements usage, (a), (f), (g) and the verdict rule faithfully per the Round 37
C1 contract, while replacing (b)-(e) for 200-299 with Python's standard library
`urllib.robotparser.RobotFileParser` (`parse(lines)` + `can_fetch(userAgent, url)`).
"""
from __future__ import annotations

import json
import os
import re
import stat
import sys
import urllib.parse
import urllib.robotparser

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

_PRODUCT_TOKEN_RE = re.compile(r"^[A-Za-z_-]+$", re.ASCII)
_URI_REF_RE = re.compile(
    r"^(?:(?P<scheme>[^:/?#]+):)?(?://(?P<authority>[^/?#]*))?(?P<path>[^?#]*)"
    r"(?:\?(?P<query>[^#]*))?(?:#(?P<fragment>.*))?$",
    re.S,
)
_ASCII_LOWER = str.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "abcdefghijklmnopqrstuvwxyz",
)


def ascii_lower(text: str) -> str:
    return text.translate(_ASCII_LOWER)


def _reject_constant(_value: str):
    raise ValueError("non-standard JSON constant")


def _host_of(authority: str | None) -> str:
    if not authority:
        return ""
    rest = authority.rsplit("@", 1)[-1]
    if rest.startswith("["):
        end = rest.find("]")
        if end == -1:
            return ""
        # Port, if any, must follow ']:' with digits
        tail = rest[end + 1 :]
        if tail and not (tail.startswith(":") and tail[1:].isdecimal()):
            return ""
        return rest[: end + 1]
    if ":" in rest:
        host, port = rest.split(":", 1)
        if port and not port.isdecimal():
            return ""
        return host
    return rest


def is_valid_http_url(url: str) -> bool:
    if not url:
        return False
    for ch in url:
        code = ord(ch)
        if code <= 0x20 or code == 0x7F:
            return False
    match = _URI_REF_RE.match(url)
    if match is None:
        return False
    scheme = match.group("scheme")
    authority = match.group("authority")
    if scheme is None or ascii_lower(scheme) not in ("http", "https"):
        return False
    host = _host_of(authority)
    if not host:
        return False
    try:
        urllib.parse.urlsplit(url)
    except ValueError:
        return False
    return True


def resolve_robots_path(manifest_dir: str, robots: str) -> str | None:
    if not robots or os.path.isabs(robots) or "\x00" in robots:
        return None
    norm_root = os.path.normpath(os.path.abspath(manifest_dir))
    norm_cand = os.path.normpath(os.path.join(norm_root, robots))
    if not norm_cand.startswith(norm_root + os.sep):
        return None
    real_root = os.path.realpath(norm_root)
    real_cand = os.path.realpath(norm_cand)
    if not real_cand.startswith(real_root + os.sep):
        return None
    try:
        st = os.stat(real_cand)
        if not stat.S_ISREG(st.st_mode):
            return None
        with open(real_cand, "rb") as handle:
            handle.read(1)
    except (OSError, ValueError):
        return None
    return real_cand


def load_manifest(path: str) -> dict | None:
    try:
        st = os.stat(path)
        if not stat.S_ISREG(st.st_mode) or st.st_size > MAX_MANIFEST_BYTES:
            return None
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
        data = json.loads(text, parse_constant=_reject_constant)
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


def validate_check(
    check: object,
    manifest_dir: str,
    seen_ids: set[str],
) -> tuple[bool, str | None, str | None]:
    """Return (is_valid, check_id_or_none, resolved_robots_path_or_none)."""
    if not isinstance(check, dict):
        return False, None, None
    raw_id = check.get("id")
    cid = raw_id if (type(raw_id) is str and len(raw_id) > 0) else None
    if cid is None:
        return False, None, None
    if cid in seen_ids:
        return False, cid, None
    seen_ids.add(cid)

    status = check.get("robotsStatus")
    if type(status) is not int:
        return False, cid, None
    if not ((200 <= status <= 299) or (400 <= status <= 499) or (500 <= status <= 599)):
        return False, cid, None

    ua = check.get("userAgent")
    if type(ua) is not str or not _PRODUCT_TOKEN_RE.fullmatch(ua):
        return False, cid, None

    expect = check.get("expect")
    if type(expect) is not str or expect not in ("allow", "disallow"):
        return False, cid, None

    url = check.get("url")
    if type(url) is not str or not is_valid_http_url(url):
        return False, cid, None

    robots_path = None
    if 200 <= status <= 299:
        robots = check.get("robots")
        if type(robots) is not str or not robots:
            return False, cid, None
        robots_path = resolve_robots_path(manifest_dir, robots)
        if robots_path is None:
            return False, cid, None

    return True, cid, robots_path


def evaluate_check(check: dict, robots_path: str | None) -> list[dict]:
    cid = check["id"]
    status = check["robotsStatus"]
    expect = check["expect"]
    ua = check["userAgent"]
    url = check["url"]

    if 400 <= status <= 499:
        allowed = True
    elif 500 <= status <= 599:
        allowed = False
    else:
        assert robots_path is not None
        try:
            with open(robots_path, "rb") as handle:
                raw = handle.read()
        except OSError:
            return [{"check": cid, "reason": "check_invalid"}]
        lines = raw.decode("utf-8", errors="replace").splitlines()
        parser = urllib.robotparser.RobotFileParser()
        parser.parse(lines)
        allowed = bool(parser.can_fetch(ua, url))

    if expect == "allow" and not allowed:
        return [{"check": cid, "reason": "blocked"}]
    if expect == "disallow" and allowed:
        return [{"check": cid, "reason": "exposed"}]
    return []


def decide_verdict(findings: list[dict]) -> str:
    for item in findings:
        if item.get("reason") in BLOCKING_REASONS:
            return VERDICT_COULD_NOT_EVALUATE
    if findings:
        return VERDICT_FAILED_POLICY
    return VERDICT_CLEAN


def emit(verdict: str, checks_evaluated: int, findings: list[dict]) -> int:
    report = {
        "version": REPORT_VERSION,
        "verdict": verdict,
        "checksEvaluated": checks_evaluated,
        "findings": findings,
    }
    sys.stdout.write(json.dumps(report) + "\n")
    if verdict == VERDICT_CLEAN:
        return EXIT_CLEAN
    if verdict == VERDICT_FAILED_POLICY:
        return EXIT_FAILED_POLICY
    return EXIT_COULD_NOT_EVALUATE


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--manifest" or not argv[1]:
        sys.stderr.write("usage: robots_audit.py --manifest PATH\n")
        return EXIT_USAGE
    manifest_path = argv[1]
    manifest = load_manifest(manifest_path)
    if manifest is None:
        return emit(
            VERDICT_COULD_NOT_EVALUATE,
            0,
            [{"check": None, "reason": "input_invalid"}],
        )
    manifest_dir = os.path.dirname(os.path.abspath(manifest_path))
    findings: list[dict] = []
    evaluated = 0
    seen_ids: set[str] = set()
    for check in manifest["checks"]:
        valid, cid, robots_path = validate_check(check, manifest_dir, seen_ids)
        if not valid:
            findings.append({"check": cid, "reason": "check_invalid"})
            continue
        check_findings = evaluate_check(check, robots_path)
        if any(f.get("reason") == "check_invalid" for f in check_findings):
            findings.extend(check_findings)
            continue
        evaluated += 1
        findings.extend(check_findings)
    return emit(decide_verdict(findings), evaluated, findings)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
