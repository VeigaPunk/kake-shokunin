#!/usr/bin/env python3
"""Round-38 C1 pre-freeze control: stdlib-delegating shortcut, patched for every non-(c)/(d) rule.

Seat: CtlStdlibV2. Built from the public round-38 contract text (SCORECARD "Round 38 — declared
claims") and from the round-37 retained control
`.ufo/waves/round-37/retained/controls/CtlC1Shortcut-followup-robots_audit.py` (stdlib plus six
patches; it scored 7 of 20 on the round-38 counter: g3, j3, j4, r1..r4).

Usage, (a), (f), (g), the verdict and the report shape are the faithful code of that control. For
2xx it does NOT implement (b)-(e) itself: Python's `urllib.robotparser.RobotFileParser` (3.14.8,
which is already the RFC 9309 rewrite) owns group selection (c), user-agent matching, rule
ranking and `*` / `$` matching (d). No group selection, user-agent matching, rule ranking or
`*` / `$` matching is written here; that is the work this control skips.

Patches, each next to the contract sentence it copies:

  S1  size      (b) "Only the first 512000 bytes ... of the file are read"
  S2  BOM       (b) "a leading UTF-8 byte order mark (EF BB BF) is dropped"
  S3  line ends (b) "Lines end at CR, LF or CRLF"
  S4  keys      (b) "Keys `user-agent`, `allow` and `disallow` are records; every other key
                    (for example `sitemap`, `crawl-delay`) is ignored and does not end a group"
                    + "The key is the text before the first `:` with spaces and tabs trimmed"
                    (robots text filter only: non-record lines are removed before the stdlib
                    sees the file, so they cannot end a group; no group or rule is selected here)
  S5  URL shape (e) "The path to match is the URL's path (`/` when empty) followed by `?` and the
                    query when the query is non-empty; the fragment is never part of it"
  S6  escapes   (e) "every `%XX` escape ... of an unreserved character ... is decoded; every other
                    `%XX` escape is kept with its hex digits uppercased" (implemented only as a
                    text transform that protects reserved escapes from the stdlib's
                    unquote/quote round trip)
  P-h1 numbers  (h) "`NaN`, `Infinity` and `-Infinity` outside a string are not JSON, so a
                    manifest holding any of them gives one `input_invalid` finding"
  P-h2 numbers  (h) "A JSON number of any length is JSON: an integer `robotsStatus` outside the
                    three ranges, however many digits it has, is a check fault ... and a number of
                    any length in a field the contract does not read changes nothing."
                    Implemented by capping exact conversion at 4000 digits (any longer integer is
                    necessarily outside 200-599, so it is a check fault without being converted;
                    a long number in an unread field is carried but never converted). This keeps
                    the 64 MiB-of-digits bound linear.
  P-i  URL chars (i) "A check's `url` holds, besides non-ASCII characters ..., only ASCII letters,
                    digits, `-` `.` `_` `~`, the reserved characters ... and `%`. A `url` holding
                    any other ASCII character anywhere ... is a check fault ... judged as written,
                    before any parsing."
  P-k  implicit  (k) "a URL whose path to match, normalized by rule (e), is exactly `/robots.txt`
                    is allowed (so `/robots%2Etxt` and `/%72obots.txt` are allowed). A path to
                    match with a query ..., another case ... or a kept reserved escape ... is
                    decided by the rules."

`normalize()` below is contract (e)'s normalization, the same function the six-patch control needs
for S6; (k) compares through it. Nothing here selects groups, matches user agents, ranks rules or
matches `*` / `$`.
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

# --- (i) URL characters: RFC 3986 section 2 character classes, as the contract lists them.
_UNRESERVED_ASCII = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
)
_RESERVED_ASCII = frozenset(":/?#[]@!$&'()*+,;=")
_URL_ASCII = _UNRESERVED_ASCII | _RESERVED_ASCII | frozenset("%")

# --- (h) JSON numbers: exact conversion only for short literals.
_MAX_EXACT_DIGITS = 4000
_HEX_UPPER = "0123456789ABCDEF"

IMPLICIT_ALLOWED_PATH = "/robots.txt"

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


class OpaqueNumber:
    """A JSON number literal too long to convert (see (h)); never an int, never an error."""

    __slots__ = ("literal",)

    def __init__(self, literal: str) -> None:
        self.literal = literal

    def __repr__(self) -> str:  # never printed in a report; keeps debugging honest
        return f"OpaqueNumber({len(self.literal)} digits)"


def _parse_int(text: str) -> int | OpaqueNumber:
    if len(text) <= _MAX_EXACT_DIGITS:
        return int(text)
    return OpaqueNumber(text)


def _parse_float(text: str) -> float | OpaqueNumber:
    if len(text) <= _MAX_EXACT_DIGITS:
        return float(text)
    return OpaqueNumber(text)


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


def url_charset_ok(url: str) -> bool:
    """(i): non-ASCII kept; any other ASCII character outside the listed classes is a fault."""
    for ch in url:
        if ch < "\x80" and ch not in _URL_ASCII:
            return False
    return True


def parse_url(url: object):
    """(f) absolute http(s) URL with a non-empty host, after the (i) character rule."""
    if not isinstance(url, str) or not url:
        return None
    if not url_charset_ok(url):
        return None
    try:
        parts = urlsplit(url)
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
    """(e): path (or "/") plus "?query" when the query is non-empty; fragment never included."""
    path = parts.path or "/"
    if parts.query:
        path = path + "?" + parts.query
    return path


def _percent_encode_byte(value: int) -> str:
    return "%" + _HEX_UPPER[value >> 4] + _HEX_UPPER[value & 0x0F]


def normalize(text: str) -> str:
    """(e): non-ASCII to UTF-8 percent-escapes, unreserved escapes decoded, other escapes kept
    with uppercase hex, reserved characters untouched."""
    out: list[str] = []
    index = 0
    length = len(text)
    while index < length:
        char = text[index]
        if char == "%" and index + 2 < length:
            high = text[index + 1]
            low = text[index + 2]
            if high in "0123456789abcdefABCDEF" and low in "0123456789abcdefABCDEF":
                octet = int(high + low, 16)
                if octet < 128 and chr(octet) in _UNRESERVED_ASCII:
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
    """(h): `NaN`, `Infinity` and `-Infinity` are not JSON."""
    raise ValueError(f"non-JSON constant {name}")


def load_manifest(path: str) -> dict | None:
    """Validate and parse the manifest under bullet (g), numbers under (h)."""
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
        data = json.loads(
            text,
            parse_constant=_reject_constant,
            parse_int=_parse_int,
            parse_float=_parse_float,
        )
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
    """Validate one check under bullet (f) (URL characters under (i))."""
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

    if parse_url(check.get("url")) is None:
        return False, cid

    if 200 <= status <= 299:
        if not is_valid_robots_path(manifest_dir_raw, manifest_dir_real, check.get("robots")):
            return False, cid

    return True, cid


def _protect_reserved(text: str) -> str:
    """S6: `%XX` of a reserved (or otherwise unreserved) ASCII character survives the stdlib's
    unquote/quote round trip as itself."""
    def repl(m: re.Match) -> str:
        code = int(m.group(1), 16)
        if code < 0x80 and chr(code) not in UNRESERVED:
            return "%25" + m.group(1).upper()
        return m.group(0)
    return _ESCAPE.sub(repl, text)


def _record_lines(data: bytes) -> list[str]:
    """S1-S4: the bytes the stdlib may see, shaped by (b). No group or rule is decided here."""
    data = data[:LIMIT]  # S1
    if data.startswith(b"\xef\xbb\xbf"):  # S2
        data = data[3:]
    lines: list[str] = []
    for line in re.split(r"\r\n|\r|\n", data.decode("utf-8", "replace")):  # S3
        head = line.split("#", 1)[0]
        if ":" not in head or head.split(":", 1)[0].strip(" \t").lower() not in KEEP_KEYS:
            continue  # S4
        lines.append(_protect_reserved(line))
    return lines


def stdlib_allows(robots_path: Path, user_agent: str, url: str) -> bool:
    """(c)/(d) are the stdlib's; S5/S6 only shape the strings it sees."""
    try:
        data = robots_path.read_bytes()
    except OSError:
        raise
    parser = RobotFileParser()
    parser.parse(_record_lines(data))
    parts = urlsplit(url)  # S5
    target = path_to_match(parts)
    return parser.can_fetch(user_agent, "http://h" + _protect_reserved(target))


def evaluate_valid_check(check: dict, manifest_dir_raw: Path) -> list[dict[str, str | None]]:
    """(a) and (k) exactly; a 2xx decision otherwise is the patched stdlib's."""
    cid = check["id"]
    status = check["robotsStatus"]
    expect = check["expect"]
    if 500 <= status <= 599:
        decision = "disallow"
    elif 400 <= status <= 499:
        decision = "allow"
    else:
        parts = parse_url(check["url"])
        if parts is None:
            return [finding(cid, "check_invalid")]
        try:
            if normalize(path_to_match(parts)) == IMPLICIT_ALLOWED_PATH:  # P-k
                decision = "allow"
            else:
                allowed = stdlib_allows(
                    manifest_dir_raw / check["robots"], check["userAgent"], check["url"]
                )
                decision = "allow" if allowed else "disallow"
        except OSError:
            return [finding(cid, "check_invalid")]
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
