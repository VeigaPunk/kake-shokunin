#!/usr/bin/env python3
"""Round-37 C1 offline robots.txt expectation audit (`scripts/robots_audit.py`).

Tells a publisher, offline, whether the robots.txt file they describe allows or
disallows the URLs they say it should, under RFC 9309 (S011) and the round-37
C1 contract in SCORECARD.md. The tool is offline by construction: it reads only
the manifest and the robots files the manifest names. No network, no writes, no
subprocesses, no environment reads. Python standard library only.

Usage:
    python3 scripts/robots_audit.py --manifest PATH

One JSON report on stdout:
    {"version": 1, "verdict": V, "checksEvaluated": N, "findings": [F, ...]}
where each finding is {"check": <check id or null>, "reason": R}. Exit 0 when
the verdict is `clean`, 1 when it is `failed-policy`, 2 when it is
`could-not-evaluate`, 64 on a usage error (any argument list other than
exactly `--manifest PATH`).

Contract summary (SCORECARD.md, round 37, "Round 37 - declared claims", C1):
(a) access result by robotsStatus range, (b) lines and the 512000-byte read,
(c) groups and user-agent selection, (d) rule matching and specificity,
(e) path construction, normalization and the implicit /robots.txt allow,
(f) check faults, (g) manifest faults, plus the verdict rule. Sources: S011
(RFC 9309, re-opened this round), S095 (Google's robots.txt specification).

Lane readings where the contract leaves a point open
----------------------------------------------------
* The manifest path is stat'ed (following symlinks) before it is opened, so a
  FIFO or device path is an input fault and can never block. A symlink to a
  regular file counts as a regular file.
* The manifest directory is the directory of the resolved (realpath) manifest,
  so a manifest symlink keeps its robots paths relative to the target.
* The 64 MiB manifest limit is inclusive: a file of exactly 67108864 bytes is
  read; a larger file, or a short stat that still yields more bytes when read,
  is an input fault.
* A manifest that starts with a UTF-8 BOM is not JSON for Python's strict
  parser and is an input fault; the contract only grants BOM removal to the
  robots file.
* `user-agent` on a manifest check must be one or more characters from the
  product-token alphabet (ASCII letters, `_`, `-`); the RFC 2.2.1 prose, not
  the ABNF `product-token = identifier / "*"`, is the contract's parenthetical,
  so `*` is not a valid check user agent.
* URL validity is exactly what the contract lists: scheme http or https
  (case-insensitive) and a non-empty host. Port syntax, userinfo and host
  syntax beyond non-emptiness are not judged.
* The implicit /robots.txt allow is compared on the raw path-to-match, before
  normalization (the contract sentence precedes the normalization sentence), so
  `/robots.txt?x=1` and `/robots%2Etxt` are not implicitly allowed; rules
  decide them.
* A robots file that passed validation but cannot be read at open time is a
  check fault for that check (one `check_invalid`), because the check cannot be
  evaluated; it is not silently treated as allow or disallow.
* Group selection: a check whose product token matches at least one group uses
  the rules of every matching group and no `*` group, even when the matching
  groups hold no rules; `*` groups apply only when no group matched.
* Non-ASCII text is percent-encoded from its UTF-8 octets; a lone surrogate
  (possible only through a JSON escape) is encoded with `surrogatepass` so the
  tool always reports rather than crashing.
* A check id is used verbatim (case-sensitive) for uniqueness and findings;
  `check_invalid` reports the id when the check is an object whose id is a
  non-empty string, else null. Earlier ids are recorded even when the earlier
  check is itself invalid.
"""

from __future__ import annotations

import json
import os
import re
import stat
import sys

from urllib.parse import urlsplit

REPORT_VERSION = 1
MANIFEST_VERSION = 1

EXIT_CLEAN = 0
EXIT_POLICY = 1
EXIT_INPUT = 2
EXIT_USAGE = 64

MAX_MANIFEST_BYTES = 64 * 1024 * 1024
MAX_ROBOTS_BYTES = 512000
READ_CHUNK_BYTES = 65536
ROBOTS_BOM = b"\xef\xbb\xbf"

REASON_BLOCKED = "blocked"
REASON_EXPOSED = "exposed"
REASON_CHECK_INVALID = "check_invalid"
REASON_INPUT_INVALID = "input_invalid"

VERDICT_CLEAN = "clean"
VERDICT_POLICY = "failed-policy"
VERDICT_INPUT = "could-not-evaluate"

IMPLICIT_ALLOWED_PATH = "/robots.txt"

_ASCII_LOWER = str.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"
)
_PRODUCT_TOKEN_RE = re.compile(r"[A-Za-z_-]+")
_LINE_SPLIT_RE = re.compile(r"\r\n|\r|\n")
_HEX_DIGITS = frozenset("0123456789abcdefABCDEF")
_HEX_UPPER = "0123456789ABCDEF"
_UNRESERVED = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "0123456789-._~"
)
_UNRESERVED_BYTES = frozenset(ord(char) for char in _UNRESERVED)

# Round-38 (i): every ASCII character a check url may hold, besides non-ASCII.
_URL_ASCII_OK = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "0123456789-._~"
    ":/?#[]@!$&'()*+,;=%"
)


def url_charset_ok(value: str) -> bool:
    """Round-38 (i): only the listed ASCII characters, and any non-ASCII."""
    return all(ord(char) >= 128 or char in _URL_ASCII_OK for char in value)


def _reject_constant(token: str):
    """Round-38 (h): NaN, Infinity and -Infinity are not JSON."""
    raise ValueError("not JSON: " + token)


def _parse_int(token: str):
    """Round-38 (h): a number of any length is JSON; keep huge ones as text so
    the range check cannot hit Python's int-conversion digit limit."""
    return token if len(token) > 4000 else int(token)

# Cache of parsed robots files, keyed by the resolved file path.
_FILE_CACHE: dict[str, "RobotsFile | None"] = {}


def ascii_lower(text: str) -> str:
    """ASCII-only lowercasing (the contract says ASCII case-insensitive)."""
    return text.translate(_ASCII_LOWER)


# --------------------------------------------------------------------------
# (e) normalization: non-ASCII to UTF-8 percent-escapes, unreserved escapes
# decoded, other escapes kept with uppercase hex, reserved characters untouched
# --------------------------------------------------------------------------

def _percent_encode_byte(value: int) -> str:
    return "%" + _HEX_UPPER[value >> 4] + _HEX_UPPER[value & 0x0F]


def normalize(text: str) -> str:
    """Normalize a rule value or a path per contract (e)."""
    out: list[str] = []
    index = 0
    length = len(text)
    while index < length:
        char = text[index]
        if char == "%" and index + 2 < length:
            high = text[index + 1]
            low = text[index + 2]
            if high in _HEX_DIGITS and low in _HEX_DIGITS:
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
            out.extend(_percent_encode_byte(octet) for octet in encoded)
        index += 1
    return "".join(out)


# --------------------------------------------------------------------------
# (b) lines and (c) groups
# --------------------------------------------------------------------------

def parse_robots_bytes(data: bytes) -> "RobotsFile":
    """Parse the first 512000 bytes of a robots file (contract (b), (c))."""
    if data.startswith(ROBOTS_BOM):
        data = data[len(ROBOTS_BOM):]
    text = data.decode("utf-8", "replace")

    groups: list[tuple[list[str], list["Rule"]]] = []
    names: list[str] | None = None
    rules: list[Rule] | None = None
    previous_was_user_agent = False

    for line in _LINE_SPLIT_RE.split(text):
        comment = line.find("#")
        if comment != -1:
            line = line[:comment]
        colon = line.find(":")
        if colon == -1:
            continue
        key = ascii_lower(line[:colon].strip(" \t"))
        value = line[colon + 1:].strip(" \t")
        if key == "user-agent":
            if previous_was_user_agent and names is not None and rules is not None:
                names.append(value)
            else:
                names = [value]
                rules = []
                groups.append((names, rules))
            previous_was_user_agent = True
        elif key == "allow" or key == "disallow":
            if names is None or rules is None:
                # A rule before the first user-agent line is ignored and does
                # not count as a record (contract (b), (c)).
                continue
            normalized = normalize(value)
            if normalized:
                # An empty value never matches (contract (d)).
                rules.append(Rule(key, normalized))
            previous_was_user_agent = False
        # Every other key is ignored and does not end a group (contract (b)).

    return RobotsFile(groups)


class Rule:
    """One allow/disallow rule, normalized and ready to match."""

    __slots__ = (
        "kind",
        "length",
        "pattern",
        "anchored",
        "has_star",
        "literal",
        "segments",
    )

    def __init__(self, kind: str, value: str) -> None:
        self.kind = kind
        self.length = len(value)
        self.anchored = value.endswith("$")
        self.pattern = value[:-1] if self.anchored else value
        self.has_star = "*" in self.pattern
        self.literal = self.pattern.split("*", 1)[0]
        self.segments = self.pattern.split("*")


class RobotsFile:
    """Parsed groups plus a per-user-agent rule selection."""

    __slots__ = ("groups", "sorted_rules", "_selection_cache")

    def __init__(self, groups: list[tuple[list[str], list[Rule]]]) -> None:
        self.groups = groups
        all_rules = [rule for _, rules in groups for rule in rules]
        self.sorted_rules = sorted(
            all_rules, key=lambda rule: rule.length, reverse=True
        )
        self._selection_cache: dict[str, list[Rule]] = {}

    def rules_for(self, product_token: str) -> list[Rule]:
        wanted = ascii_lower(product_token)
        cached = self._selection_cache.get(wanted)
        if cached is not None:
            return cached

        matched_any = False
        selected: set[Rule] = set()
        star_groups: list[tuple[list[str], list[Rule]]] = []
        for names, rules in self.groups:
            lowered = [ascii_lower(name) for name in names]
            if wanted in lowered:
                matched_any = True
                selected.update(rules)
            if "*" in lowered:
                star_groups.append((names, rules))
        if not matched_any:
            for _, rules in star_groups:
                selected.update(rules)

        # Walk the file-wide length order so every token selection is linear and
        # the decision loop always sees rules longest first.
        rules = [rule for rule in self.sorted_rules if rule in selected]
        if len(self._selection_cache) >= 8:
            self._selection_cache.clear()
        self._selection_cache[wanted] = rules
        return rules


def rule_matches(rule: Rule, path: str) -> bool:
    """Contract (d): `*` any run, trailing `$` anchors, otherwise a prefix.

    Round-37 wave-2 repair (`SentinelRobotsInputs`): wildcard rules are matched by a
    greedy leftmost segment scan instead of a backtracking regex, so a rule such as
    `/*a*a*...*z$` cannot take exponential time. For `*`-only globs the leftmost scan
    finds a match whenever one exists.
    """
    if not rule.has_star:
        if rule.anchored:
            return path == rule.pattern
        return path.startswith(rule.pattern)
    segments = rule.segments
    if not path.startswith(segments[0]):
        return False
    pos = len(segments[0])
    if rule.anchored:
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


def decide(rules: list[Rule], path: str) -> str:
    """Return "allow" or "disallow" for one normalized path (contract (d))."""
    best_length = -1
    decision = "allow"
    for rule in rules:
        if best_length >= 0 and rule.length < best_length:
            break
        if not rule_matches(rule, path):
            continue
        if rule.length > best_length:
            best_length = rule.length
            decision = rule.kind
        elif rule.kind == "allow":
            # Equal normalized length: allow decides (contract (d)).
            decision = "allow"
    return decision


# --------------------------------------------------------------------------
# Bounded, non-blocking file access
# --------------------------------------------------------------------------

def _read_fd_bounded(fd: int, limit: int) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while total < limit:
        block = os.read(fd, min(READ_CHUNK_BYTES, limit - total))
        if not block:
            break
        chunks.append(block)
        total += len(block)
    return b"".join(chunks)


def _open_regular(path: str, flags: int) -> int:
    fd = os.open(path, flags)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise OSError("not a regular file")
    except BaseException:
        os.close(fd)
        raise
    return fd


def read_robots_bytes(path: str) -> bytes | None:
    """Read at most 512000 bytes from a validated robots file."""
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_CLOEXEC", 0)
    try:
        fd = _open_regular(path, flags)
    except (OSError, ValueError):
        return None
    try:
        return _read_fd_bounded(fd, MAX_ROBOTS_BYTES)
    except OSError:
        return None
    finally:
        os.close(fd)


def load_manifest(path: str) -> list | None:
    """Read and validate a manifest, returning its checks list or None (g)."""
    try:
        info = os.stat(path)
    except (OSError, ValueError):
        return None
    if not stat.S_ISREG(info.st_mode):
        return None
    if info.st_size > MAX_MANIFEST_BYTES:
        return None

    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_CLOEXEC", 0)
    try:
        fd = _open_regular(path, flags)
    except (OSError, ValueError):
        return None
    try:
        data = _read_fd_bounded(fd, MAX_MANIFEST_BYTES + 1)
    except OSError:
        return None
    finally:
        os.close(fd)
    if len(data) > MAX_MANIFEST_BYTES:
        return None

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return None
    try:
        document = json.loads(
            text, parse_constant=_reject_constant, parse_int=_parse_int
        )
    except (ValueError, RecursionError):
        return None
    if not isinstance(document, dict):
        return None
    version = document.get("version")
    if type(version) is not int or version != MANIFEST_VERSION:
        return None
    checks = document.get("checks")
    if not isinstance(checks, list):
        return None
    return checks


# --------------------------------------------------------------------------
# (f) check validation
# --------------------------------------------------------------------------

def resolve_robots_path(manifest_dir: str, value: object) -> str | None:
    """Resolve a check's robots path, or None when it is a check fault."""
    if not isinstance(value, str):
        return None
    if not value or os.path.isabs(value):
        return None
    try:
        candidate = os.path.realpath(os.path.join(manifest_dir, value))
    except (OSError, ValueError):
        return None
    try:
        if os.path.commonpath([manifest_dir, candidate]) != manifest_dir:
            return None
    except ValueError:
        return None
    try:
        info = os.stat(candidate)
    except (OSError, ValueError):
        return None
    if not stat.S_ISREG(info.st_mode):
        return None
    return candidate


def parse_http_url(value: object):
    """Return urlsplit parts for an absolute http(s) URL with a host, or None."""
    if not isinstance(value, str):
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
    """Contract (e): path (or "/") plus "?query" when the query is non-empty."""
    path = parts.path or "/"
    if parts.query:
        path = path + "?" + parts.query
    return path


def audit_manifest(manifest_path: str) -> tuple[dict[str, object], int]:
    checks = load_manifest(manifest_path)
    if checks is None:
        report = make_report(
            VERDICT_INPUT, 0, [finding(None, REASON_INPUT_INVALID)]
        )
        return report, EXIT_INPUT

    manifest_dir = os.path.dirname(os.path.realpath(manifest_path))

    findings: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    evaluated = 0

    for check in checks:
        is_object = isinstance(check, dict)
        check_id = check.get("id") if is_object else None
        has_id = isinstance(check_id, str) and check_id != ""
        invalid = not has_id
        if has_id:
            if check_id in seen_ids:
                invalid = True
            seen_ids.add(check_id)

        status = check.get("robotsStatus") if is_object else None
        status_ok = (
            type(status) is int
            and (200 <= status <= 299 or 400 <= status <= 499 or 500 <= status <= 599)
        )
        if not status_ok:
            invalid = True

        token = check.get("userAgent") if is_object else None
        if not isinstance(token, str) or _PRODUCT_TOKEN_RE.fullmatch(token) is None:
            invalid = True

        raw_url = check.get("url") if is_object else None
        if isinstance(raw_url, str) and not url_charset_ok(raw_url):
            invalid = True
        parts = parse_http_url(raw_url)
        if parts is None:
            invalid = True

        expect = check.get("expect") if is_object else None
        if not isinstance(expect, str) or expect not in ("allow", "disallow"):
            invalid = True

        robots_path = None
        if status_ok and 200 <= status <= 299:
            robots_path = resolve_robots_path(
                manifest_dir, check.get("robots") if is_object else None
            )
            if robots_path is None:
                invalid = True

        if invalid:
            findings.append(finding(check_id if has_id else None, REASON_CHECK_INVALID))
            continue

        allowed = False
        if 200 <= status <= 299:
            available = _robots_file(robots_path)
            if available is None:
                findings.append(finding(check_id, REASON_CHECK_INVALID))
                continue
            rules = available.rules_for(token)
            path = path_to_match(parts)
            if normalize(path) == IMPLICIT_ALLOWED_PATH:
                allowed = True
            else:
                allowed = decide(rules, normalize(path)) == "allow"
        elif 400 <= status <= 499:
            allowed = True
        else:  # 500 <= status <= 599
            allowed = False

        evaluated += 1
        if expect == "allow" and not allowed:
            findings.append(finding(check_id, REASON_BLOCKED))
        elif expect == "disallow" and allowed:
            findings.append(finding(check_id, REASON_EXPOSED))

    verdict = VERDICT_CLEAN
    exit_code = EXIT_CLEAN
    if any(item["reason"] == REASON_CHECK_INVALID for item in findings):
        verdict = VERDICT_INPUT
        exit_code = EXIT_INPUT
    elif findings:
        verdict = VERDICT_POLICY
        exit_code = EXIT_POLICY
    return make_report(verdict, evaluated, findings), exit_code


def _robots_file(path: str) -> RobotsFile | None:
    if path in _FILE_CACHE:
        return _FILE_CACHE[path]
    data = read_robots_bytes(path)
    parsed = None if data is None else parse_robots_bytes(data)
    _FILE_CACHE[path] = parsed
    return parsed


def finding(check: object, reason: str) -> dict[str, object]:
    return {"check": check, "reason": reason}


def make_report(verdict: str, evaluated: int, findings: list) -> dict[str, object]:
    return {
        "version": REPORT_VERSION,
        "verdict": verdict,
        "checksEvaluated": evaluated,
        "findings": findings,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--manifest":
        print(
            "robots_audit.py: usage: robots_audit.py --manifest PATH",
            file=sys.stderr,
        )
        return EXIT_USAGE
    report, exit_code = audit_manifest(argv[1])
    print(json.dumps(report, separators=(",", ":")))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
