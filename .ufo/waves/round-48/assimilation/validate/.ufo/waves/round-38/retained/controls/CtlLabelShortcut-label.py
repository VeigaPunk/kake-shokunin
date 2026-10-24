#!/usr/bin/env python3
"""Round-38 C1 label-keyed shortcut control (`robots_audit.py` shape).

Deliberate shortcut: decides robots outcomes from surface labels only.
* No user-agent group parsing.  Every `allow:` / `disallow:` record after the
  first `user-agent:` line is pooled and applied to every check (a regex over
  record lines, no group selection, no `*` group rule, no substring/Unicode
  user-agent semantics).
* Rule matching is raw-value globbing (prefix, `$` anchor, `*` wildcard,
  longest value wins, allow wins ties) with the round-37 normalization reused
  as a plain string transform -- no group, no matched-length, no folding.
* The three round-38 edge rules are string predicates, so they are implemented
  exactly: non-JSON constants (NaN/Infinity) rejected, ASCII URL character set
  scanned, implicit `/robots.txt` allow compared on the normalized path.
* Framing that any tool needs to report at all (usage, manifest shape, check
  validation, status ranges, verdict/exit) is implemented because without it
  no case can pass.

Usage: python3 ctl_label_shortcut.py --manifest PATH
"""
from __future__ import annotations

import json
import os
import re
import stat
import sys
from urllib.parse import urlsplit

EXIT_CLEAN = 0
EXIT_POLICY = 1
EXIT_INPUT = 2
EXIT_USAGE = 64

VERDICT_CLEAN = "clean"
VERDICT_POLICY = "failed-policy"
VERDICT_INPUT = "could-not-evaluate"

MAX_MANIFEST_BYTES = 64 * 1024 * 1024
MAX_ROBOTS_BYTES = 512000
ROBOTS_BOM = b"\xef\xbb\xbf"

BLOCKED = "blocked"
EXPOSED = "exposed"
CHECK_INVALID = "check_invalid"
INPUT_INVALID = "input_invalid"

_PRODUCT_TOKEN = re.compile(r"[A-Za-z_-]+\Z")
_HEX = frozenset("0123456789abcdefABCDEF")
_UNRESERVED = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
)
_UNRESERVED_BYTES = frozenset(ord(c) for c in _UNRESERVED)
# (i) URL characters: ASCII letters, digits, - . _ ~, reserved, and %.
_URL_ASCII_OK = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    "-._~" ":/?#[]@!$&'()*+,;=%"
)
_LINE_SPLIT = re.compile(r"\r\n|\r|\n")
_ASCII_LOWER = str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")


class _Long:
    """Sentinel for an integer literal too long to convert (rule (h))."""

    __slots__ = ()


_LONG = _Long()


def ascii_lower(text: str) -> str:
    return text.translate(_ASCII_LOWER)


def _reject_constant(name: str):
    raise ValueError("non-JSON constant " + name)


def _int_hook(text: str):
    return int(text) if len(text) <= 1000 else _LONG


def norm(text: str) -> str:
    """Round-37 (e) normalization, used here as a plain label transform."""
    out: list[str] = []
    index = 0
    length = len(text)
    while index < length:
        char = text[index]
        if char == "%" and index + 2 < length:
            high, low = text[index + 1], text[index + 2]
            if high in _HEX and low in _HEX:
                octet = int(high + low, 16)
                if octet in _UNRESERVED_BYTES:
                    out.append(chr(octet))
                else:
                    out.append("%" + high.upper() + low.upper())
                index += 3
                continue
        code = ord(char)
        if code < 128:
            out.append(char)
        else:
            try:
                encoded = char.encode("utf-8")
            except UnicodeEncodeError:
                encoded = char.encode("utf-8", "surrogatepass")
            out.extend("%%%02X" % octet for octet in encoded)
        index += 1
    return "".join(out)


def url_charset_ok(url: str) -> bool:
    """(i): any ASCII character outside the allowed set is a check fault."""
    for char in url:
        code = ord(char)
        if code < 128 and char not in _URL_ASCII_OK:
            return False
    return True


def load_manifest(path: str):
    try:
        info = os.stat(path)
    except (OSError, ValueError):
        return None
    if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_MANIFEST_BYTES:
        return None
    try:
        with open(path, "rb") as handle:
            data = handle.read(MAX_MANIFEST_BYTES + 1)
    except (OSError, ValueError):
        return None
    if len(data) > MAX_MANIFEST_BYTES:
        return None
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return None
    try:
        document = json.loads(
            text, parse_constant=_reject_constant, parse_int=_int_hook
        )
    except (ValueError, RecursionError):
        return None
    if not isinstance(document, dict):
        return None
    version = document.get("version")
    if type(version) is not int or version != 1:
        return None
    checks = document.get("checks")
    if not isinstance(checks, list):
        return None
    return checks


def resolve_robots_path(manifest_dir: str, value: object) -> str | None:
    if not isinstance(value, str) or not value or os.path.isabs(value):
        return None
    try:
        candidate = os.path.realpath(os.path.join(manifest_dir, value))
    except (OSError, ValueError):
        return None
    try:
        if os.path.commonpath([manifest_dir, candidate]) != manifest_dir:
            return None
        info = os.stat(candidate)
    except (OSError, ValueError):
        return None
    if not stat.S_ISREG(info.st_mode):
        return None
    return candidate


def parse_url(value: object):
    if not isinstance(value, str):
        return None
    if not url_charset_ok(value):
        return None
    try:
        parts = urlsplit(value)
    except ValueError:
        return None
    if parts.scheme not in ("http", "https"):
        return None
    try:
        host = parts.hostname
    except ValueError:
        return None
    if not host:
        return None
    return parts


def path_to_match(parts) -> str:
    path = parts.path or "/"
    if parts.query:
        path = path + "?" + parts.query
    return path


def read_robots(path: str) -> str | None:
    try:
        with open(path, "rb") as handle:
            data = handle.read(MAX_ROBOTS_BYTES)
    except (OSError, ValueError):
        return None
    if data.startswith(ROBOTS_BOM):
        data = data[len(ROBOTS_BOM):]
    return data.decode("utf-8", "replace")


def label_rules(text: str) -> list[tuple[str, str]]:
    """Pool every record after the first `user-agent` line (no groups)."""
    rules: list[tuple[str, str]] = []
    seen_agent = False
    for line in _LINE_SPLIT.split(text):
        cut = line.find("#")
        if cut != -1:
            line = line[:cut]
        colon = line.find(":")
        if colon == -1:
            continue
        key = ascii_lower(line[:colon].strip(" \t"))
        value = line[colon + 1:].strip(" \t")
        if key == "user-agent":
            seen_agent = True
        elif key == "allow" or key == "disallow":
            if not seen_agent:
                continue
            value = norm(value)
            if value:
                rules.append((key, value))
    return rules


def _glob_match(pattern: str, anchored: bool, path: str) -> bool:
    if "*" not in pattern:
        return path == pattern if anchored else path.startswith(pattern)
    segments = pattern.split("*")
    if not path.startswith(segments[0]):
        return False
    pos = len(segments[0])
    if anchored:
        last = segments[-1]
        for segment in segments[1:-1]:
            found = path.find(segment, pos)
            if found < 0:
                return False
            pos = found + len(segment)
        return len(path) - len(last) >= pos and path.endswith(last)
    for segment in segments[1:]:
        found = path.find(segment, pos)
        if found < 0:
            return False
        pos = found + len(segment)
    return True


def decide(rules: list[tuple[str, str]], path: str) -> str:
    best = -1
    verdict = "allow"
    for kind, value in rules:
        anchored = value.endswith("$")
        pattern = value[:-1] if anchored else value
        if not _glob_match(pattern, anchored, path):
            continue
        length = len(value)
        if length > best:
            best, verdict = length, kind
        elif length == best and kind == "allow":
            verdict = "allow"
    return verdict


def finding(check_id: object, reason: str) -> dict:
    return {"check": check_id, "reason": reason}


def audit(manifest_path: str):
    checks = load_manifest(manifest_path)
    if checks is None:
        return (
            {"version": 1, "verdict": VERDICT_INPUT, "checksEvaluated": 0,
             "findings": [finding(None, INPUT_INVALID)]},
            EXIT_INPUT,
        )
    manifest_dir = os.path.dirname(os.path.realpath(manifest_path))
    findings: list[dict] = []
    seen: set[str] = set()
    evaluated = 0
    for check in checks:
        obj = isinstance(check, dict)
        check_id = check.get("id") if obj else None
        has_id = isinstance(check_id, str) and check_id != ""
        invalid = not has_id
        if has_id:
            if check_id in seen:
                invalid = True
            seen.add(check_id)
        status = check.get("robotsStatus") if obj else None
        status_ok = type(status) is int and (
            200 <= status <= 299 or 400 <= status <= 499 or 500 <= status <= 599
        )
        if not status_ok:
            invalid = True
        token = check.get("userAgent") if obj else None
        if not isinstance(token, str) or _PRODUCT_TOKEN.fullmatch(token) is None:
            invalid = True
        parts = parse_url(check.get("url") if obj else None)
        if parts is None:
            invalid = True
        expect = check.get("expect") if obj else None
        if not isinstance(expect, str) or expect not in ("allow", "disallow"):
            invalid = True
        robots_path = None
        if status_ok and 200 <= status <= 299:
            robots_path = resolve_robots_path(manifest_dir, check.get("robots") if obj else None)
            if robots_path is None:
                invalid = True
        if invalid:
            findings.append(finding(check_id if has_id else None, CHECK_INVALID))
            continue
        allowed = False
        if 200 <= status <= 299:
            text = read_robots(robots_path)
            if text is None:
                findings.append(finding(check_id, CHECK_INVALID))
                continue
            path = path_to_match(parts)
            normalized = norm(path)
            if normalized == "/robots.txt":
                allowed = True
            else:
                allowed = decide(label_rules(text), normalized) == "allow"
        elif 400 <= status <= 499:
            allowed = True
        else:
            allowed = False
        evaluated += 1
        if expect == "allow" and not allowed:
            findings.append(finding(check_id, BLOCKED))
        elif expect == "disallow" and allowed:
            findings.append(finding(check_id, EXPOSED))
    verdict, code = VERDICT_CLEAN, EXIT_CLEAN
    if any(item["reason"] == CHECK_INVALID for item in findings):
        verdict, code = VERDICT_INPUT, EXIT_INPUT
    elif findings:
        verdict, code = VERDICT_POLICY, EXIT_POLICY
    return (
        {"version": 1, "verdict": verdict, "checksEvaluated": evaluated,
         "findings": findings},
        code,
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--manifest":
        print("ctl_label_shortcut.py: usage: --manifest PATH", file=sys.stderr)
        return EXIT_USAGE
    try:
        report, code = audit(argv[1])
    except Exception:  # a shortcut never crashes: report and keep going
        report, code = (
            {"version": 1, "verdict": VERDICT_INPUT, "checksEvaluated": 0,
             "findings": [finding(None, INPUT_INVALID)]},
            EXIT_INPUT,
        )
    print(json.dumps(report, separators=(",", ":")))
    return code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
