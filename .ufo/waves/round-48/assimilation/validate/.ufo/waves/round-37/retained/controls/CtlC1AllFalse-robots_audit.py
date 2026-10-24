#!/usr/bin/env python3
"""Round-37 C1 all-false control (`robots_audit.py`).

Implements the C1 CLI, manifest-fault rule (g), check-fault rule (f), verdict,
and exit codes faithfully, but never reads any robots.txt file: every valid
check receives the policy finding opposite its declared expectation (`blocked`
when `expect` is `"allow"`, `exposed` when `expect` is `"disallow"`).
"""
from __future__ import annotations

import json
import os
import re
import stat
import sys
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

_URI_REF_RE = re.compile(
    r"^(?:(?P<scheme>[^:/?#]+):)?(?://(?P<authority>[^/?#]*))?(?P<path>[^?#]*)"
    r"(?:\?(?P<query>[^#]*))?(?:#(?P<fragment>.*))?$",
    re.S,
)


def _reject_constant(_value: str) -> None:
    raise ValueError("non-standard JSON constant")


def finding(check: str | None, reason: str) -> dict[str, object]:
    return {"check": check, "reason": reason}


def host_of(authority: str | None) -> str:
    if not authority:
        return ""
    rest = authority.rsplit("@", 1)[-1]
    if rest.startswith("["):
        end = rest.find("]")
        if end == -1:
            return ""
        return rest[: end + 1]
    return rest.split(":", 1)[0]


def is_valid_product_token(value: object) -> bool:
    if type(value) is not str or not value:
        return False
    return all(
        ("a" <= ch <= "z") or ("A" <= ch <= "Z") or ch in "_-"
        for ch in value
    )


def is_valid_http_url(value: object) -> bool:
    if type(value) is not str or not value:
        return False
    if any(ch.isspace() or ord(ch) < 0x20 or ord(ch) == 0x7F for ch in value):
        return False
    match = _URI_REF_RE.match(value)
    if match is None:
        return False
    scheme = match.group("scheme")
    authority = match.group("authority")
    if scheme is None or scheme.lower() not in ("http", "https"):
        return False
    if not host_of(authority):
        return False
    try:
        parsed = urlsplit(value)
    except ValueError:
        return False
    if parsed.scheme.lower() not in ("http", "https") or not parsed.hostname:
        return False
    return True


def is_valid_robots_path(manifest_dir: str, robots: object) -> bool:
    """Validate rule (f) path constraints without opening or reading the file."""
    if type(robots) is not str or not robots:
        return False
    if os.path.isabs(robots):
        return False
    try:
        real_root = os.path.realpath(manifest_dir)
        candidate = os.path.join(manifest_dir, robots)
        real = os.path.realpath(candidate)
        if real == real_root or not real.startswith(real_root + os.sep):
            return False
        st_cand = os.stat(candidate)
        st_real = os.stat(real)
    except (OSError, ValueError):
        return False
    return stat.S_ISREG(st_cand.st_mode) and stat.S_ISREG(st_real.st_mode)


def load_manifest(path: str) -> dict[str, object] | None:
    try:
        st = os.stat(path)
        if not stat.S_ISREG(st.st_mode):
            return None
        if st.st_size > MAX_MANIFEST_BYTES:
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
    if type(data) is not dict:
        return None
    version = data.get("version")
    if type(version) is not int or version != 1:
        return None
    checks = data.get("checks")
    if type(checks) is not list:
        return None
    return data


def validate_check(
    check: object,
    manifest_dir: str,
    seen_ids: set[str],
) -> tuple[bool, str | None]:
    if type(check) is not dict:
        return False, None
    raw_id = check.get("id")
    cid = raw_id if (type(raw_id) is str and len(raw_id) > 0) else None
    is_dup = False
    if cid is not None:
        if cid in seen_ids:
            is_dup = True
        seen_ids.add(cid)
    if cid is None or is_dup:
        return False, cid
    status = check.get("robotsStatus")
    if type(status) is not int or not (
        200 <= status <= 299 or 400 <= status <= 499 or 500 <= status <= 599
    ):
        return False, cid
    if not is_valid_product_token(check.get("userAgent")):
        return False, cid
    if not is_valid_http_url(check.get("url")):
        return False, cid
    expect = check.get("expect")
    if type(expect) is not str or expect not in ("allow", "disallow"):
        return False, cid
    if 200 <= status <= 299:
        if not is_valid_robots_path(manifest_dir, check.get("robots")):
            return False, cid
    return True, cid


def evaluate_all_false(check: dict[str, object], cid: str) -> dict[str, object]:
    """Never read any robots file: always emit the finding against `expect`."""
    if check["expect"] == "allow":
        return finding(cid, "blocked")
    return finding(cid, "exposed")


def decide_verdict(findings: list[dict[str, object]]) -> str:
    for item in findings:
        if item.get("reason") in BLOCKING_REASONS:
            return VERDICT_COULD_NOT_EVALUATE
    if findings:
        return VERDICT_FAILED_POLICY
    return VERDICT_CLEAN


def emit(verdict: str, checks_evaluated: int, findings: list[dict[str, object]]) -> int:
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


def parse_args(argv: list[str]) -> str | None:
    if len(argv) != 2 or argv[0] != "--manifest" or not argv[1]:
        return None
    return argv[1]


def main(argv: list[str]) -> int:
    path = parse_args(argv)
    if path is None:
        sys.stderr.write("usage: robots_audit.py --manifest PATH\n")
        return EXIT_USAGE
    manifest = load_manifest(path)
    if manifest is None:
        return emit(VERDICT_COULD_NOT_EVALUATE, 0, [finding(None, "input_invalid")])
    manifest_dir = os.path.dirname(os.path.abspath(path))
    findings: list[dict[str, object]] = []
    evaluated = 0
    seen_ids: set[str] = set()
    for check in manifest["checks"]:
        ok, cid = validate_check(check, manifest_dir, seen_ids)
        if not ok:
            findings.append(finding(cid, "check_invalid"))
            continue
        evaluated += 1
        findings.append(evaluate_all_false(check, cid))
    return emit(decide_verdict(findings), evaluated, findings)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
