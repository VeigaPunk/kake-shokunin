#!/usr/bin/env python3
"""Round-37 C1 pre-freeze control: CtlC1NoReader (`robots_audit.py`).

No-reader control for the offline robots.txt expectation audit. Implements:
  - CLI usage contract: exact `--manifest PATH` (exit 64 on any other argv).
  - (g) Manifest faults: regular-file check via stat metadata, <= 64 MiB size
    cap, UTF-8 decoding, strict JSON parsing, top-level object check, exact
    integer `version == 1` (rejecting booleans and floats), and `checks` list.
    Emits one `input_invalid` finding with `check: null`, `checksEvaluated: 0`,
    verdict `could-not-evaluate`, exit 2.
  - (f) Check faults: check object type, non-empty string `id` uniqueness across
    all earlier checks in the manifest list, integer `robotsStatus` in 200-299,
    400-499, or 500-599 (rejecting booleans and floats), RFC 9309 section 2.2.1
    product-token `userAgent` (`[A-Za-z_-]+`), `expect` in `{"allow", "disallow"}`,
    absolute `http`/`https` `url` with non-empty host, and for status 200-299
    `robots` relative-path validation (containment within resolved manifest
    directory after resolving symlinks and `..`, plus regular-file metadata via
    `os.stat` without opening or reading file bytes).
  - (a) Access result:
      * 400-499 -> allow (robots field ignored)
      * 500-599 -> disallow, including `/robots.txt` (robots field ignored)
      * 200-299 -> never opens or reads the robots file bytes; decides every URL
        as `allow` (under which the `/robots.txt` always-allowed rule is
        automatically satisfied).
  - 2xx URL-shape heuristic: none beats the constant. Every 2xx file is treated
    as if it were empty ("no rules apply: allowed", contract (c)/(d)), so every
    URL is `allow`; the `/robots.txt` rule (e) is the only URL shape the contract
    guarantees, and it is `allow` too. Rejected alternatives: URL-word keying
    (`private`, `admin`, ...) is the separate shortcut control; reading `expect`
    turns the tool into a constant-clean / all-false hybrid; constant `disallow`
    (except `/robots.txt`) has no contract basis. Without bytes no URL shape
    (depth, query, escapes, non-ASCII, trailing slash) predicts a decision, and a
    case passes only when every check in it is right.
  - Verdict and exit codes: `could-not-evaluate` (exit 2) if any `input_invalid`
    or `check_invalid` finding is present; else `failed-policy` (exit 1) if any
    `blocked` or `exposed` finding is present; else `clean` (exit 0).
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


def finding(check_id: str | None, reason: str) -> dict[str, str | None]:
    return {"check": check_id, "reason": reason}


def is_product_token(value: str) -> bool:
    """RFC 9309 section 2.2.1 product token: one or more [A-Za-z_-]."""
    if not value:
        return False
    for ch in value:
        if not (("a" <= ch <= "z") or ("A" <= ch <= "Z") or ch == "_" or ch == "-"):
            return False
    return True


def is_valid_http_url(url: object) -> bool:
    """Absolute http(s) URL with a non-empty host (RFC 3986 split, no port parse)."""
    if not isinstance(url, str) or not url:
        return False
    try:
        parts = urlsplit(url)
    except ValueError:
        return False
    if parts.scheme not in ("http", "https"):
        return False
    return bool(parts.hostname)


def is_valid_robots_path(
    manifest_dir_raw: Path,
    manifest_dir_real: Path,
    robots: object,
) -> bool:
    """Validate robots path via filesystem metadata only (never reading bytes)."""
    if not isinstance(robots, str) or not robots:
        return False
    if os.path.isabs(robots) or "\x00" in robots:
        return False
    candidate = manifest_dir_raw / robots
    try:
        st = os.stat(candidate)
        if not stat.S_ISREG(st.st_mode):
            return False
        resolved = candidate.resolve(strict=True)
    except (OSError, RuntimeError, ValueError):
        return False
    if manifest_dir_real not in resolved.parents:
        return False
    return True


def _reject_constant(name: str) -> None:
    """`NaN`, `Infinity` and `-Infinity` are not JSON (manifest fault (g))."""
    raise ValueError(f"non-JSON constant {name}")


def load_manifest(path: str) -> dict | None:
    """Validate and parse the manifest under bullet (g)."""
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
        data = json.loads(text, parse_constant=_reject_constant)
    except (ValueError, RecursionError):
        return None
    if not isinstance(data, dict):
        return None
    version = data.get("version")
    if type(version) is not int or version != 1:
        return None
    checks = data.get("checks")
    if not isinstance(checks, list):
        return None
    return data


def validate_check(
    check: object,
    manifest_dir_raw: Path,
    manifest_dir_real: Path,
    seen_ids: set[str],
) -> tuple[bool, str | None]:
    """Validate one check under bullet (f). Return (is_valid, check_id_or_none)."""
    if not isinstance(check, dict):
        return False, None
    raw_id = check.get("id")
    cid = raw_id if (isinstance(raw_id, str) and len(raw_id) > 0) else None
    if cid is None:
        return False, None
    if cid in seen_ids:
        return False, cid
    seen_ids.add(cid)

    status = check.get("robotsStatus")
    if type(status) is not int:
        return False, cid
    if not (200 <= status <= 299 or 400 <= status <= 499 or 500 <= status <= 599):
        return False, cid

    ua = check.get("userAgent")
    if not isinstance(ua, str) or not is_product_token(ua):
        return False, cid

    expect = check.get("expect")
    if not isinstance(expect, str) or expect not in ("allow", "disallow"):
        return False, cid

    url = check.get("url")
    if not is_valid_http_url(url):
        return False, cid

    if 200 <= status <= 299:
        if not is_valid_robots_path(manifest_dir_raw, manifest_dir_real, check.get("robots")):
            return False, cid

    return True, cid


def evaluate_valid_check(check: dict) -> list[dict[str, str | None]]:
    """Evaluate a validated check under bullet (a) without reading robots bytes."""
    cid = check["id"]
    status = check["robotsStatus"]
    expect = check["expect"]

    if 500 <= status <= 599:
        decision = "disallow"
    else:
        # 400-499: allow by contract (a).
        # 200-299: no-reader control decides every URL as allow without reading
        # robots bytes (which also satisfies `/robots.txt` -> allow).
        decision = "allow"

    if expect == "allow" and decision == "disallow":
        return [finding(cid, "blocked")]
    if expect == "disallow" and decision == "allow":
        return [finding(cid, "exposed")]
    return []


def decide_verdict(findings: list[dict[str, str | None]]) -> str:
    for item in findings:
        if item.get("reason") in BLOCKING_REASONS:
            return VERDICT_COULD_NOT_EVALUATE
    if findings:
        return VERDICT_FAILED_POLICY
    return VERDICT_CLEAN


def emit(verdict: str, checks_evaluated: int, findings: list[dict[str, str | None]]) -> int:
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
    if len(argv) != 2 or argv[0] != "--manifest":
        sys.stderr.write("usage: robots_audit.py --manifest PATH\n")
        return EXIT_USAGE
    manifest_path = argv[1]
    manifest = load_manifest(manifest_path)
    if manifest is None:
        return emit(VERDICT_COULD_NOT_EVALUATE, 0, [finding(None, "input_invalid")])

    try:
        manifest_dir_raw = Path(os.path.abspath(manifest_path)).parent
        manifest_dir_real = manifest_dir_raw.resolve(strict=True)
    except (OSError, RuntimeError, ValueError):
        return emit(VERDICT_COULD_NOT_EVALUATE, 0, [finding(None, "input_invalid")])

    findings: list[dict[str, str | None]] = []
    evaluated = 0
    seen_ids: set[str] = set()
    for check in manifest["checks"]:
        valid, cid = validate_check(check, manifest_dir_raw, manifest_dir_real, seen_ids)
        if not valid:
            findings.append(finding(cid, "check_invalid"))
            continue
        evaluated += 1
        findings.extend(evaluate_valid_check(check))

    return emit(decide_verdict(findings), evaluated, findings)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
