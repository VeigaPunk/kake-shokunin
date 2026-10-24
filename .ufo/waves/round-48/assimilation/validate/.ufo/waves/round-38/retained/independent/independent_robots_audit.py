#!/usr/bin/env python3
"""Offline robots.txt expectation audit — an independent implementation of the public contract
(SCORECARD.md, "Round 37 -- declared claims", C1 contract, plus the "Round 38" amendments (h),
(i), (k)). Written by a seat that never read the builder's tool.

Readings chosen where the text admits more than one (listed again in the seat report):

  1. (k) The implicit allow compares the *normalized* path-to-match (path plus a non-empty
     ?query, rule (e) applied) with "/robots.txt": "/robots%2Etxt" and "/%72obots.txt" are
     allowed, "/ROBOTS.TXT", "/robots.txt?x=1" and "/robots%2Ftxt" are decided by the rules.
  2. The 512000-byte limit is applied to the raw file bytes, before dropping a leading BOM.
  3. A `robots` value is relative when it does not start with "/" (POSIX host); the resolved
     real path must start with the real manifest directory plus a separator, so a sibling
     directory that only shares the textual prefix is outside. The manifest directory is the
     real directory of the real manifest path.
  4. Duplicate ids use the id of every earlier check object whose id is a non-empty string,
     even when that earlier check is invalid for another reason.
  5. A manifest path that does not exist is "not a regular file" (input_invalid, exit 2), not
     a usage error; usage errors are argument lists other than exactly `--manifest PATH`.
  6. If a validated robots file cannot be opened at evaluation time, the check is reported as
     check_invalid (the contract names missing/non-regular/escaping files, not unreadable
     ones).
  7. "ASCII case-insensitive" folds A-Z only; no Unicode folding anywhere.
  8. An absolute URL is one that parses, has scheme http or https (compared ASCII
     case-insensitively) and a non-empty host; other URL components are unconstrained.
  9. `%XX` normalization runs on the whole path-to-match, query included, because "the path to
     match" is defined as path + query.
 10. (h) A JSON integer literal longer than 4000 digits is not converted (Python's int() from
     a decimal string is quadratic and a 64 MiB literal cannot be converted inside 20 s); it
     is carried as a non-int sentinel, which makes it "not a JSON integer" wherever the
     contract reads an integer and inert everywhere else. Literals up to 4000 digits are
     converted, so range decisions are exact.
 11. (h) `NaN`, `Infinity` and `-Infinity` are rejected by the JSON parser itself (the same
     input_invalid path as any other unparseable manifest).
 12. (h) A manifest too deeply nested for the JSON parser (RecursionError) is input_invalid:
     it cannot be read, so it cannot be evaluated.
 13. (i) The URL character rule is judged on the raw string before any parsing; `%` is
     allowed in any position, including not followed by two hex digits (ruling of the C2
     clarifications).
 14. A robots path holding a NUL character cannot name a regular file, so it is check_invalid
     (it is rejected before any os.path call, which would raise ValueError).
"""

import json
import os
import re
import stat
import sys
from urllib.parse import urlsplit

ROBOTS_LIMIT = 512000
MANIFEST_LIMIT = 64 * 1024 * 1024
# int() from a decimal string is quadratic; a 64 MiB literal cannot be converted in 20 s.
# Above this many digits the literal is carried as a non-int sentinel instead.
INT_DIGIT_LIMIT = 4000
_SP_TAB = " \t"
_UNRESERVED = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
)
_URL_ASCII = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
    ":/?#[]@!$&'()*+,;=%"
)
_ASCII_FOLD = {code: code + 32 for code in range(ord("A"), ord("Z") + 1)}
_LINE_END = re.compile(r"\r\n|\r|\n")
_ESCAPE = re.compile(r"%([0-9A-Fa-f]{2})")
_PRODUCT_TOKEN = re.compile(r"[A-Za-z_-]+\Z")


class LongInteger:
    """A JSON integer literal too long to convert; never an int, never a str."""

    __slots__ = ("literal",)

    def __init__(self, literal):
        self.literal = literal

    def __repr__(self):
        return "LongInteger(%r...)" % self.literal[:16]


def parse_json_int(literal):
    if len(literal) > INT_DIGIT_LIMIT:
        return LongInteger(literal)
    try:
        return int(literal)
    except ValueError:
        # sys.set_int_max_str_digits() may lower the conversion limit; the literal is still
        # a JSON integer, just not one this contract ever compares numerically.
        return LongInteger(literal)


def reject_json_constant(name):
    # RFC 8259 section 6: NaN, Infinity and -Infinity are not JSON.
    raise ValueError("non-JSON number literal: %s" % name)


def ascii_lower(text):
    return text.translate(_ASCII_FOLD)


def trim(text):
    return text.strip(_SP_TAB)


def percent_encode_non_ascii(text):
    out = []
    for char in text:
        if ord(char) < 0x80:
            out.append(char)
        else:
            out.extend("%%%02X" % byte for byte in char.encode("utf-8"))
    return "".join(out)


def normalize(text):
    def replace(match):
        char = chr(int(match.group(1), 16))
        if char in _UNRESERVED:
            return char
        return "%" + match.group(1).upper()

    return _ESCAPE.sub(replace, percent_encode_non_ascii(text))


def path_to_match(parts):
    path = parts.path or "/"
    if parts.query:
        path = path + "?" + parts.query
    return path


def parse_robots(text):
    groups = []
    previous_was_agent = False
    for line in _LINE_END.split(text):
        cut = line.find("#")
        if cut != -1:
            line = line[:cut]
        colon = line.find(":")
        if colon == -1:
            continue
        key = ascii_lower(trim(line[:colon]))
        value = trim(line[colon + 1:])
        if key == "user-agent":
            if not groups or not previous_was_agent:
                groups.append({"names": [], "rules": []})
            groups[-1]["names"].append(value)
            previous_was_agent = True
        elif key in ("allow", "disallow"):
            if not groups:
                continue
            groups[-1]["rules"].append((key, value))
            previous_was_agent = False
    return groups


def rule_matches(rule, path):
    """`*` matches any sequence; a final `$` anchors at the end of the path."""
    anchored = rule.endswith("$")
    segments = (rule[:-1] if anchored else rule).split("*")
    first = segments[0]
    if not path.startswith(first):
        return False
    if len(segments) == 1:
        return not anchored or len(path) == len(first)
    if not anchored:
        # Prefix match: the remaining segments must occur in order after the first one.
        position = len(first)
        for segment in segments[1:]:
            if not segment:
                continue
            position = path.find(segment, position)
            if position == -1:
                return False
            position += len(segment)
        return True
    # Full match: the last segment ends at the end of the path; the middle segments
    # are placed leftmost (optimal) inside the window between the two.
    last = segments[-1]
    window_end = len(path) - len(last)
    if window_end < len(first) or not path.endswith(last):
        return False
    position = len(first)
    for segment in segments[1:-1]:
        if not segment:
            continue
        position = path.find(segment, position, window_end)
        if position == -1:
            return False
        position += len(segment)
    return True


def robots_decision(robots_path, url, user_agent):
    parts = urlsplit(url)
    path_norm = normalize(path_to_match(parts))
    # (k) The implicit allow is compared on the normalized path-to-match.
    if path_norm == "/robots.txt":
        return True
    with open(robots_path, "rb") as handle:
        data = handle.read(ROBOTS_LIMIT)
    if data.startswith(b"\xef\xbb\xbf"):
        data = data[3:]
    groups = parse_robots(data.decode("utf-8", "replace"))
    wanted = ascii_lower(user_agent)
    matching = [group for group in groups
                if any(ascii_lower(name) == wanted for name in group["names"])]
    if not matching:
        matching = [group for group in groups
                    if any(name == "*" for name in group["names"])]
    best_length = -1
    best_kind = None
    for group in matching:
        for kind, value in group["rules"]:
            if not value:
                continue
            normalized = normalize(value)
            if not rule_matches(normalized, path_norm):
                continue
            length = len(normalized)
            if length > best_length or (length == best_length and kind == "allow"):
                best_length = length
                best_kind = kind
    return best_kind is None or best_kind == "allow"


def valid_url(url):
    try:
        parts = urlsplit(url)
        host = parts.hostname
    except ValueError:
        return False
    if parts.scheme.lower() not in ("http", "https"):
        return False
    return bool(parts.netloc) and bool(host)


def url_characters_ok(url):
    # (i): non-ASCII kept; every ASCII character must be in the RFC 3986 character set.
    for char in url:
        if ord(char) < 0x80 and char not in _URL_ASCII:
            return False
    return True


def validate_check(check, seen_ids, manifest_dir):
    if not isinstance(check, dict):
        return None, "not an object"
    check_id = check.get("id")
    label = check_id if isinstance(check_id, str) and check_id else None
    if label is None:
        return None, "id missing, empty or not a string"
    if check_id in seen_ids:
        return label, "duplicate id"
    seen_ids.add(check_id)
    status = check.get("robotsStatus")
    if type(status) is not int:
        return label, "robotsStatus is not a JSON integer"
    if not (200 <= status <= 299 or 400 <= status <= 499 or 500 <= status <= 599):
        return label, "robotsStatus outside the accepted ranges"
    agent = check.get("userAgent")
    if not isinstance(agent, str) or _PRODUCT_TOKEN.fullmatch(agent) is None:
        return label, "userAgent is not a product token"
    url = check.get("url")
    if not isinstance(url, str) or not url_characters_ok(url):
        return label, "url holds a character outside the accepted set"
    if not valid_url(url):
        return label, "url is not an absolute http(s) URL with a host"
    expect = check.get("expect")
    if expect not in ("allow", "disallow"):
        return label, "expect is not allow or disallow"
    if 200 <= status <= 299:
        robots = check.get("robots")
        if not isinstance(robots, str) or not robots:
            return label, "robots is not a non-empty relative path"
        if "\x00" in robots:
            return label, "robots holds a NUL character"
        if os.path.isabs(robots):
            return label, "robots is absolute"
        resolved = os.path.realpath(os.path.join(manifest_dir, robots))
        if not resolved.startswith(manifest_dir + os.sep):
            return label, "robots escapes the manifest directory"
        if not os.path.isfile(resolved):
            return label, "robots is not a regular file"
    return label, None


def read_manifest(path):
    try:
        info = os.stat(path)
    except (OSError, ValueError):
        return None
    if not stat.S_ISREG(info.st_mode):
        return None
    if info.st_size > MANIFEST_LIMIT:
        return None
    try:
        with open(path, "rb") as handle:
            data = handle.read()
    except (OSError, ValueError):
        return None
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return None
    try:
        document = json.loads(
            text,
            parse_int=parse_json_int,
            parse_constant=reject_json_constant,
        )
    except (ValueError, RecursionError):
        return None
    if not isinstance(document, dict):
        return None
    version = document.get("version")
    if type(version) is not int or version != 1:
        return None
    if not isinstance(document.get("checks"), list):
        return None
    return document


def evaluate(manifest_path):
    findings = []
    document = read_manifest(manifest_path)
    if document is None:
        return [{"check": None, "reason": "input_invalid"}], 0
    manifest_dir = os.path.dirname(os.path.realpath(manifest_path))
    seen_ids = set()
    evaluated = 0
    for check in document["checks"]:
        label, problem = validate_check(check, seen_ids, manifest_dir)
        if problem is not None:
            findings.append({"check": label, "reason": "check_invalid"})
            continue
        status = check["robotsStatus"]
        if 200 <= status <= 299:
            robots_path = os.path.realpath(os.path.join(manifest_dir, check["robots"]))
            try:
                allowed = robots_decision(robots_path, check["url"], check["userAgent"])
            except (OSError, ValueError):
                findings.append({"check": check["id"], "reason": "check_invalid"})
                continue
        elif 400 <= status <= 499:
            allowed = True
        else:
            allowed = False
        evaluated += 1
        if check["expect"] == "allow" and not allowed:
            findings.append({"check": check["id"], "reason": "blocked"})
        elif check["expect"] == "disallow" and allowed:
            findings.append({"check": check["id"], "reason": "exposed"})
    return findings, evaluated


def main(argv):
    if len(argv) != 2 or argv[0] != "--manifest":
        print("usage: robots_audit.py --manifest PATH", file=sys.stderr)
        return 64
    findings, evaluated = evaluate(argv[1])
    reasons = {item["reason"] for item in findings}
    if "input_invalid" in reasons or "check_invalid" in reasons:
        verdict, code = "could-not-evaluate", 2
    elif findings:
        verdict, code = "failed-policy", 1
    else:
        verdict, code = "clean", 0
    report = {
        "version": 1,
        "verdict": verdict,
        "checksEvaluated": evaluated,
        "findings": findings,
    }
    json.dump(report, sys.stdout)
    sys.stdout.write("\n")
    return code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
