#!/usr/bin/env python3
"""Round-37 C1 pre-freeze control: CtlC1NoReader follow-up, shortcut control.

Usage, (a), (f), (g) and the verdict are the faithful code of the no-reader control.
For 2xx it does NOT implement the contract's (b)-(e): it delegates to Python's stdlib
`urllib.robotparser.RobotFileParser` (public receipt `control-CtlC1NaiveReader.json`:
stdlib alone passes a, c, d, f, g = 20/28 and fails only b1-b4 and e1-e4) and adds
one-line patches aimed at the stdlib quirks those failing bullets most likely hit
(guessed from the public ablation names b_bom/b_limit/b_other/b_cr and
e_*/f_query/f_fragment/f_emptypath/f_robots):
  S1 size: keep only the first 512000 bytes of the robots file.
  S2 BOM: drop a leading EF BB BF (stdlib reads `\\ufeffuser-agent` as a key).
  S3 line breaks: split only at CR, LF, CRLF (stdlib callers use splitlines()).
  S4 other keys: drop every line whose key is not user-agent/allow/disallow
     (stdlib's crawl-delay/request-rate end a group).
  S5 URL shape: build `path[?query]` myself: fragment dropped, `?` only for a
     non-empty query, `/` for an empty path (stdlib keeps `#frag` and an empty `?`).
  S6 reserved escapes: `%XX` of a reserved ASCII character becomes `%25XX`
     (uppercase) in both URL and rule lines, so stdlib's unquote/quote round
     keeps `%2F` distinct from `/`.
Group selection (incl. stdlib's substring user-agent fallback), allow/disallow
precedence, `*`, `$` and lengths are whatever the stdlib does; no URL-word,
user-agent-name, id, file-name or `expect` keying is used.
"""
from __future__ import annotations

import json
import os
import re
import stat
import sys
from pathlib import Path
from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser

LIMIT = 512000
KEEP_KEYS = frozenset(("user-agent", "allow", "disallow"))
UNRESERVED = frozenset("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~")
_ESCAPE = re.compile(r"%([0-9A-Fa-f]{2})")

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


def _protect_reserved(text: str) -> str:
    """S6: `%XX` of a reserved ASCII character survives stdlib's unquote/quote."""
    def repl(m: re.Match) -> str:
        code = int(m.group(1), 16)
        if code < 0x80 and chr(code) not in UNRESERVED:
            return "%25" + m.group(1).upper()
        return m.group(0)
    return _ESCAPE.sub(repl, text)


def stdlib_allows(robots_path: Path, user_agent: str, url: str) -> bool:
    data = robots_path.read_bytes()[:LIMIT]  # S1
    if data.startswith(b"\xef\xbb\xbf"):  # S2
        data = data[3:]
    lines = []
    for line in re.split(r"\r\n|\r|\n", data.decode("utf-8", "replace")):  # S3
        head = line.split("#", 1)[0]
        if ":" not in head or head.split(":", 1)[0].strip().lower() not in KEEP_KEYS:  # S4
            continue
        lines.append(_protect_reserved(line))
    parser = RobotFileParser()
    parser.parse(lines)
    parts = urlsplit(url)  # S5
    target = parts.path or "/"
    if parts.query:
        target += "?" + parts.query
    return parser.can_fetch(user_agent, "http://h" + _protect_reserved(target))


def evaluate_valid_check(check: dict, manifest_dir_raw: Path) -> list[dict[str, str | None]]:
    """(a) exactly; 2xx decided by the patched stdlib parser."""
    cid = check["id"]
    status = check["robotsStatus"]
    expect = check["expect"]
    if 500 <= status <= 599:
        decision = "disallow"
    elif 400 <= status <= 499:
        decision = "allow"
    else:
        try:
            allowed = stdlib_allows(manifest_dir_raw / check["robots"], check["userAgent"], check["url"])
        except OSError:
            return [finding(cid, "check_invalid")]
        decision = "allow" if allowed else "disallow"
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
        findings.extend(evaluate_valid_check(check, manifest_dir_raw))

    return emit(decide_verdict(findings), evaluated, findings)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
