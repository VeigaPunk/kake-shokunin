#!/usr/bin/env python3
"""Offline robots meta-directive audit (round 78, claim C3; amendment 1 applied).

Reads a versioned manifest, parses the local HTML page named by every check,
and reports the page's declared effective robots rules plus the lane's finding
list.  Read-only, network-free, standard library only.  Manifest mode writes
nothing; ``--selftest`` writes only inside ``--work`` (or the system temporary
directory when ``--work`` is omitted) and removes its fixture tree.

Manifest ``kake-meta-robots-manifest/v1``::

    {"schema": "kake-meta-robots-manifest/v1",
     "agents": ["robots", ...],                  # optional, default ["robots"]
     "checks": [{"id": "...",                    # non-empty, unique
                 "path": "relative/page.html",   # local HTML, not absolute
                 "url": "https://example/",      # carried through, not fetched
                 "expect": {"effective": [...],
                            "findings": [...]}}]}

``path`` resolves against ``--root`` (default: the manifest's directory); a
path that escapes its root or does not name a regular file is a check fault.
``expect.effective`` and ``expect.findings`` are compared as sorted lists; any
difference yields ``meta_robots_expected_mismatch`` for that check.

Exit: 0 every check matched, 1 any finding (page finding or expected
mismatch), 2 input or check fault (unreadable manifest, wrong schema, duplicate
id, malformed check/expect, missing page), 64 usage.

Frozen grammar as corrected by ``.ufo/waves/round-78/contract-amendment-1.md``
(A1-A5; the source is the L1's retained ``robots-meta-tag`` page):

- Only ``<meta name=... content=...>`` elements whose ``name`` equals one of
  ``agents`` ASCII-case-insensitively are collected.  A matching element
  outside ``<head>`` joins the effective set exactly like a head element
  (A1: Google respects body-section tags) and is additionally reported as
  ``meta_robots_tag_outside_head`` (lane hygiene).
- Content splits on commas; tokens are ASCII-case-insensitively compared and
  whitespace-trimmed; empty tokens are ignored; an all-empty content is
  ``meta_robots_empty_content``.
- Effective vocabulary: ``all``, ``none``, ``index``, ``noindex``, ``follow``,
  ``nofollow``, ``nosnippet``, ``noimageindex``, ``notranslate``,
  ``indexifembedded``, ``max-snippet:<int>``,
  ``max-image-preview:<none|standard|large>``, ``max-video-preview:<int>``,
  ``unavailable_after:<date>``.  ``none`` expands to ``noindex,nofollow`` and
  ``all`` to ``index,follow`` (frozen contract; the source notes ``all`` has
  no effect, but the contract's expansion is kept).
- ``noarchive``, ``nocache`` and ``nositelinkssearchbox`` are ignored rules
  (A3): never effective, reported as ``meta_robots_ignored_rule``.
- Most restrictive wins across every matching element: ``noindex`` over
  ``index``, ``nofollow`` over ``follow``; ``nosnippet`` dominates and drops
  numeric ``max-snippet``/``max-video-preview`` from the rendering (A5);
  ``max-snippet:0`` renders as ``nosnippet``; an integer ``-1`` ("no limit")
  loses to any non-negative value; ``max-image-preview`` orders
  ``none < standard < large``; the earliest valid ``unavailable_after`` wins
  (ties broken by the lexicographically smallest literal).
- ``unavailable_after`` accepts the union of RFC 3339 full-date
  (``YYYY-MM-DD``), RFC 3339 date-time
  (``YYYY-MM-DDThh:mm:ss[.frac](Z|±hh:mm)``) and RFC 822-style
  ``DD Mon YYYY HH:MM:SS ZONE`` (A2).  RFC 850 is a declared non-implemented
  limit.  A value parsing under none is ``meta_robots_invalid_value``.
- Value errors and unknown tokens are findings and never enter the effective
  set: ``meta_robots_invalid_value`` (malformed integer, bad date, bad
  ``max-image-preview`` value), ``meta_robots_unknown_directive`` (any other
  token).  Reporting them is lane policy (A4).
- No matching element anywhere: effective set ``["follow","index"]`` and no
  finding.  A matching element whose tokens are all empty/invalid/unknown/
  ignored still counts as a matching element, so the effective set is empty
  rather than the default.

Decisions the frozen text leaves open (kept consistent; see the seat report):
an implicit head (a page that omits ``<head>``) is not modelled - only an
explicit ``<head>`` element scopes head placement; comments, doctypes and
``script``/``style``/``textarea``/``title`` raw text are skipped; attribute
values are HTML-unescaped and the first occurrence of a repeated attribute
wins; a missing ``content`` attribute is empty content; ``<meta>`` subtrees
inside ``template``/``svg`` are not specially skipped; RFC 822 zone names are
accepted syntactically but compared as UTC (no zone-database claim), while
numeric ``±HHMM`` offsets are honoured; a date-only value is midnight UTC;
findings are emitted once per offending element/token; check faults are not
findings.  ``--selftest`` adds an optional ``--work DIR`` (house style); it is
not required.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
import tempfile

from datetime import date
from html import unescape

# --------------------------------------------------------------------------
# Contract constants
# --------------------------------------------------------------------------

SCHEMA = "kake-meta-robots-manifest/v1"

EXIT_CLEAN = 0
EXIT_FINDING = 1
EXIT_INPUT = 2
EXIT_USAGE = 64

OUTPUT_VERSION = 1

FINDING_OUTSIDE_HEAD = "meta_robots_tag_outside_head"
FINDING_EMPTY_CONTENT = "meta_robots_empty_content"
FINDING_INVALID_VALUE = "meta_robots_invalid_value"
FINDING_UNKNOWN_DIRECTIVE = "meta_robots_unknown_directive"
FINDING_IGNORED_RULE = "meta_robots_ignored_rule"
FINDING_EXPECTED_MISMATCH = "meta_robots_expected_mismatch"

FINDING_IDS = (
    FINDING_OUTSIDE_HEAD,
    FINDING_EMPTY_CONTENT,
    FINDING_INVALID_VALUE,
    FINDING_UNKNOWN_DIRECTIVE,
    FINDING_IGNORED_RULE,
    FINDING_EXPECTED_MISMATCH,
)

DEFAULT_AGENTS = ("robots",)
DEFAULT_EFFECTIVE = ("follow", "index")

ASCII_WS = " \t\n\r\f"

_FLAG_RULES = frozenset(
    (
        "index",
        "noindex",
        "follow",
        "nofollow",
        "nosnippet",
        "noimageindex",
        "notranslate",
        "indexifembedded",
    )
)
_IGNORED_RULES = frozenset(("noarchive", "nocache", "nositelinkssearchbox"))
_EXPANSIONS = {"all": ("index", "follow"), "none": ("noindex", "nofollow")}

_MAX_IMAGE_ORDER = {"none": 0, "standard": 1, "large": 2}

_LIMIT_RE = re.compile(r"-1|[0-9]+")
_RFC3339_DATE_RE = re.compile(r"([0-9]{4})-([0-9]{2})-([0-9]{2})")
_RFC3339_DATETIME_RE = re.compile(
    r"([0-9]{4})-([0-9]{2})-([0-9]{2})[Tt]([0-9]{2}):([0-9]{2}):([0-9]{2})"
    r"(\.[0-9]+)?([Zz]|[+-][0-9]{2}:[0-9]{2})"
)
_RFC822_RE = re.compile(
    r"([0-9]{1,2}) ([A-Za-z]{3}) ([0-9]{4}) ([0-9]{2}):([0-9]{2}):([0-9]{2})"
    r" ([A-Za-z]{1,5}|[+-][0-9]{4})"
)
_MONTHS = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}
_DAYS_IN_MONTH = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

_RAW_TEXT_TAGS = frozenset(("script", "style", "textarea", "title"))

_ASCII_LOWER = str.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"
)


def ascii_lower(text: str) -> str:
    """ASCII-only lowercasing (the contract says ASCII case-insensitive)."""
    return text.translate(_ASCII_LOWER)


# --------------------------------------------------------------------------
# Tolerant HTML scanner
# --------------------------------------------------------------------------


def _parse_attrs(text: str, pos: int):
    """Parse a start tag's attributes from ``pos``.

    Returns ``(attrs, self_closing, next_pos, closed)``.  Attribute names are
    ASCII-lowercased and the first occurrence wins; values are HTML-unescaped;
    unquoted, single-quoted and double-quoted values are read as HTML reads
    them.  ``closed`` is False when EOF arrives before the closing ``>`` (such
    a tag is not a tag element).
    """
    length = len(text)
    attrs: dict[str, str] = {}
    while pos < length:
        while pos < length and text[pos] in ASCII_WS:
            pos += 1
        if pos >= length:
            return attrs, False, length, False
        char = text[pos]
        if char == ">":
            return attrs, False, pos + 1, True
        if char == "/":
            if pos + 1 < length and text[pos + 1] == ">":
                return attrs, True, pos + 2, True
            pos += 1
            continue
        start = pos
        while pos < length and text[pos] not in ASCII_WS and text[pos] not in "/>=":
            pos += 1
        name = text[start:pos]
        while pos < length and text[pos] in ASCII_WS:
            pos += 1
        value = ""
        if pos < length and text[pos] == "=":
            pos += 1
            while pos < length and text[pos] in ASCII_WS:
                pos += 1
            if pos < length and text[pos] in "\"'":
                quote = text[pos]
                pos += 1
                end = text.find(quote, pos)
                if end < 0:
                    raw = text[pos:]
                    pos = length
                else:
                    raw = text[pos:end]
                    pos = end + 1
            else:
                value_start = pos
                while pos < length and text[pos] not in ASCII_WS and text[pos] != ">":
                    pos += 1
                raw = text[value_start:pos]
            value = unescape(raw)
        lowered = ascii_lower(name)
        if lowered and lowered not in attrs:
            attrs[lowered] = value
    return attrs, False, length, False


def scan_meta_tags(text: str):
    """Return ``(attrs, in_head)`` for every closed ``<meta>`` start tag.

    Comments, doctypes, processing instructions and the raw text of
    ``script``/``style``/``textarea``/``title`` are skipped.  ``<head>`` opens
    head scope and ``</head>`` or a ``<body>`` start tag closes it; there is no
    implied head for a document that omits the element.
    """
    metas: list[tuple[dict[str, str], bool]] = []
    lower_text = ascii_lower(text)
    length = len(text)
    pos = 0
    in_head = False
    while pos < length:
        angle = text.find("<", pos)
        if angle < 0:
            break
        if text.startswith("<!--", angle):
            end = text.find("-->", angle + 4)
            pos = length if end < 0 else end + 3
            continue
        if text.startswith("<![CDATA[", angle):
            end = text.find("]]>", angle + 9)
            pos = length if end < 0 else end + 3
            continue
        if text.startswith("<!", angle) or text.startswith("<?", angle):
            end = text.find(">", angle + 2)
            pos = length if end < 0 else end + 1
            continue
        if text.startswith("</", angle):
            end = text.find(">", angle + 2)
            if end < 0:
                break
            name = ascii_lower(text[angle + 2:end].strip())
            if name:
                name = name.split()[0]
            if name == "head":
                in_head = False
            pos = end + 1
            continue

        name_start = angle + 1
        cursor = name_start
        while (
            cursor < length
            and text[cursor] not in ASCII_WS
            and text[cursor] not in "/>"
        ):
            cursor += 1
        name = ascii_lower(text[name_start:cursor])
        attrs, self_closing, next_pos, closed = _parse_attrs(text, cursor)
        if name == "head":
            if not self_closing and closed:
                in_head = True
        elif name == "body":
            in_head = False
        elif name == "meta" and closed:
            metas.append((attrs, in_head))
        if name in _RAW_TEXT_TAGS and not self_closing:
            end = lower_text.find("</" + name, next_pos)
            pos = length if end < 0 else end
        else:
            pos = next_pos
    return metas


# --------------------------------------------------------------------------
# unavailable_after date grammars
# --------------------------------------------------------------------------


def _valid_ymd(year: int, month: int, day: int) -> bool:
    if year < 1 or year > 9999:
        return False
    if month < 1 or month > 12:
        return False
    leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    limit = 29 if (month == 2 and leap) else _DAYS_IN_MONTH[month - 1]
    return 1 <= day <= limit


def _instant_key(
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    second: int,
    fraction: str,
    offset_seconds: int,
) -> tuple[int, int] | None:
    if not _valid_ymd(year, month, day):
        return None
    if hour > 23 or minute > 59 or second > 60:
        return None
    total = date(year, month, day).toordinal() * 86400
    total += hour * 3600 + minute * 60 + second - offset_seconds
    if fraction:
        digits = fraction[1:]
        nanos = int((digits + "000000000")[:9])
    else:
        nanos = 0
    return (total, nanos)


def parse_unavailable_after(value: str):
    """Return ``(sort_key, literal)`` for a valid date/time, else None.

    Accepted: RFC 3339 full-date, RFC 3339 date-time, and RFC 822-style
    ``DD Mon YYYY HH:MM:SS ZONE`` (amendment A2).  A date-only value is
    midnight UTC.  Alphabetical RFC 822 zones are compared as UTC; numeric
    ``+HHMM``/``-HHMM`` offsets are honoured.  RFC 850 is not implemented.
    """
    match = _RFC3339_DATE_RE.fullmatch(value)
    if match is not None:
        year, month, day = (int(part) for part in match.groups())
        key = _instant_key(year, month, day, 0, 0, 0, "", 0)
        return None if key is None else (key, value)

    match = _RFC3339_DATETIME_RE.fullmatch(value)
    if match is not None:
        year, month, day, hour, minute, second = (
            int(match.group(index)) for index in range(1, 7)
        )
        fraction = match.group(7) or ""
        offset_text = match.group(8)
        if offset_text in ("Z", "z"):
            offset_seconds = 0
        else:
            sign = -1 if offset_text[0] == "-" else 1
            offset_hour = int(offset_text[1:3])
            offset_minute = int(offset_text[4:6])
            if offset_hour > 23 or offset_minute > 59:
                return None
            offset_seconds = sign * (offset_hour * 3600 + offset_minute * 60)
        key = _instant_key(
            year, month, day, hour, minute, second, fraction, offset_seconds
        )
        return None if key is None else (key, value)

    match = _RFC822_RE.fullmatch(value)
    if match is not None:
        day = int(match.group(1))
        month = _MONTHS.get(ascii_lower(match.group(2)))
        year = int(match.group(3))
        hour = int(match.group(4))
        minute = int(match.group(5))
        second = int(match.group(6))
        zone = match.group(7)
        if month is None:
            return None
        if zone[0] in "+-":
            offset_hour = int(zone[1:3])
            offset_minute = int(zone[3:5])
            if offset_hour > 23 or offset_minute > 59:
                return None
            sign = -1 if zone[0] == "-" else 1
            offset_seconds = sign * (offset_hour * 3600 + offset_minute * 60)
        else:
            offset_seconds = 0
        key = _instant_key(
            year, month, day, hour, minute, second, "", offset_seconds
        )
        return None if key is None else (key, value)

    return None


# --------------------------------------------------------------------------
# Declared-rule state and merge
# --------------------------------------------------------------------------


class _State:
    """Most-restrictive merge of the rules declared by matching elements."""

    __slots__ = (
        "index",
        "noindex",
        "follow",
        "nofollow",
        "nosnippet",
        "noimageindex",
        "notranslate",
        "indexifembedded",
        "max_snippet",
        "max_video",
        "max_image",
        "unavailable",
    )

    def __init__(self) -> None:
        self.index = False
        self.noindex = False
        self.follow = False
        self.nofollow = False
        self.nosnippet = False
        self.noimageindex = False
        self.notranslate = False
        self.indexifembedded = False
        self.max_snippet: list[int] = []
        self.max_video: list[int] = []
        self.max_image: str | None = None
        self.unavailable: list[tuple[tuple[int, int], str]] = []

    def add_image(self, value: str) -> None:
        if self.max_image is None:
            self.max_image = value
        elif _MAX_IMAGE_ORDER[value] < _MAX_IMAGE_ORDER[self.max_image]:
            self.max_image = value

    def effective(self) -> list[str]:
        out: list[str] = []
        if self.noindex:
            out.append("noindex")
        elif self.index:
            out.append("index")
        if self.nofollow:
            out.append("nofollow")
        elif self.follow:
            out.append("follow")
        if self.indexifembedded:
            out.append("indexifembedded")
        if self.noimageindex:
            out.append("noimageindex")
        if self.notranslate:
            out.append("notranslate")

        snippet = None
        if self.max_snippet:
            non_negative = [value for value in self.max_snippet if value >= 0]
            snippet = min(non_negative) if non_negative else -1
        video = None
        if self.max_video:
            non_negative = [value for value in self.max_video if value >= 0]
            video = min(non_negative) if non_negative else -1

        if self.nosnippet or snippet == 0:
            out.append("nosnippet")
        else:
            if snippet is not None:
                out.append("max-snippet:%d" % snippet)
            if video is not None:
                out.append("max-video-preview:%d" % video)
        if self.max_image is not None:
            out.append("max-image-preview:" + self.max_image)
        if self.unavailable:
            _key, literal = min(
                self.unavailable, key=lambda item: (item[0], item[1])
            )
            out.append("unavailable_after:" + literal)
        out.sort()
        return out


def _apply_token(token: str, state: _State, findings: list[tuple[str, str]]) -> None:
    """Apply one trimmed content token, recording findings, never raising."""
    lowered = ascii_lower(token)
    if lowered in _EXPANSIONS:
        for name in _EXPANSIONS[lowered]:
            _apply_flag(name, state)
        return
    if lowered in _FLAG_RULES:
        _apply_flag(lowered, state)
        return
    if lowered in _IGNORED_RULES:
        findings.append(
            (
                FINDING_IGNORED_RULE,
                "directive %r is ignored by Google Search "
                "(historical and other unused rules)" % lowered,
            )
        )
        return

    name, separator, value = token.partition(":")
    directive = ascii_lower(name)
    if not separator:
        findings.append(
            (FINDING_UNKNOWN_DIRECTIVE, "unknown directive %r" % token)
        )
        return

    if directive == "max-snippet":
        if _LIMIT_RE.fullmatch(value) is None:
            findings.append(
                (
                    FINDING_INVALID_VALUE,
                    "invalid value for max-snippet: %r" % value,
                )
            )
        else:
            state.max_snippet.append(int(value))
        return
    if directive == "max-video-preview":
        if _LIMIT_RE.fullmatch(value) is None:
            findings.append(
                (
                    FINDING_INVALID_VALUE,
                    "invalid value for max-video-preview: %r" % value,
                )
            )
        else:
            state.max_video.append(int(value))
        return
    if directive == "max-image-preview":
        image = ascii_lower(value)
        if image not in _MAX_IMAGE_ORDER:
            findings.append(
                (
                    FINDING_INVALID_VALUE,
                    "invalid value for max-image-preview: %r" % value,
                )
            )
        else:
            state.add_image(image)
        return
    if directive == "unavailable_after":
        parsed = parse_unavailable_after(value)
        if parsed is None:
            findings.append(
                (
                    FINDING_INVALID_VALUE,
                    "invalid value for unavailable_after: %r" % value,
                )
            )
        else:
            state.unavailable.append(parsed)
        return

    findings.append((FINDING_UNKNOWN_DIRECTIVE, "unknown directive %r" % token))


def _apply_flag(name: str, state: _State) -> None:
    if name == "index":
        state.index = True
    elif name == "noindex":
        state.noindex = True
    elif name == "follow":
        state.follow = True
    elif name == "nofollow":
        state.nofollow = True
    elif name == "nosnippet":
        state.nosnippet = True
    elif name == "noimageindex":
        state.noimageindex = True
    elif name == "notranslate":
        state.notranslate = True
    elif name == "indexifembedded":
        state.indexifembedded = True


def audit_page(text: str, agents: frozenset[str]):
    """Return ``(effective, finding_ids, findings)`` for one page's bytes."""
    state = _State()
    findings: list[tuple[str, str]] = []
    matched = False
    for attrs, in_head in scan_meta_tags(text):
        name = attrs.get("name")
        if name is None:
            continue
        if ascii_lower(name) not in agents:
            continue
        matched = True
        if not in_head:
            findings.append(
                (
                    FINDING_OUTSIDE_HEAD,
                    "matching meta name=%r appears outside <head>; body tags "
                    "are respected and join the effective set (A1)" % name,
                )
            )
        content = attrs.get("content")
        raw_tokens = [] if content is None else content.split(",")
        tokens = [token.strip(ASCII_WS) for token in raw_tokens]
        tokens = [token for token in tokens if token]
        if not tokens:
            findings.append(
                (
                    FINDING_EMPTY_CONTENT,
                    "matching meta name=%r has empty content" % name,
                )
            )
            continue
        for token in tokens:
            _apply_token(token, state, findings)

    effective = state.effective() if matched else list(DEFAULT_EFFECTIVE)
    finding_ids = sorted(finding[0] for finding in findings)
    return effective, finding_ids, findings


# --------------------------------------------------------------------------
# Manifest loading and validation
# --------------------------------------------------------------------------


def load_manifest(path: str):
    """Return ``(document, error)``; the document is unvalidated JSON."""
    try:
        with open(path, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        return None, "cannot read manifest %r: %s" % (path, exc.strerror or exc)
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return None, "manifest %r is not UTF-8" % path
    try:
        return json.loads(text), None
    except ValueError as exc:
        return None, "manifest %r is not JSON: %s" % (path, exc)


def validate_manifest(document):
    """Return ``(checks, agents, error)`` for a manifest document."""
    if not isinstance(document, dict):
        return None, None, "manifest is not a JSON object"
    schema = document.get("schema")
    if schema != SCHEMA:
        return None, None, "manifest schema is not %r" % SCHEMA
    checks = document.get("checks")
    if not isinstance(checks, list):
        return None, None, "manifest checks is not a list"
    raw_agents = document.get("agents", list(DEFAULT_AGENTS))
    if not isinstance(raw_agents, list):
        return None, None, "manifest agents is not a list"
    agents: set[str] = set()
    for agent in raw_agents:
        if not isinstance(agent, str) or not agent:
            return None, None, "manifest agent entries must be non-empty strings"
        agents.add(ascii_lower(agent))
    return checks, frozenset(agents), None


def validate_check(check, seen_ids: set[str]):
    """Return ``(info, error)``; ``info`` is a plain tuple on success."""
    if not isinstance(check, dict):
        return None, "check is not an object"
    check_id = check.get("id")
    if not isinstance(check_id, str) or not check_id:
        return None, "check id is missing or empty"
    if check_id in seen_ids:
        return None, "duplicate check id %r" % check_id
    seen_ids.add(check_id)

    path = check.get("path")
    if not isinstance(path, str) or not path:
        return None, "check %r path is missing or empty" % check_id
    if os.path.isabs(path):
        return None, "check %r path must be relative" % check_id

    url = check.get("url")
    if not isinstance(url, str):
        return None, "check %r url is not a string" % check_id

    expect = check.get("expect")
    if not isinstance(expect, dict):
        return None, "check %r expect is not an object" % check_id
    effective = expect.get("effective")
    findings = expect.get("findings")
    if not isinstance(effective, list) or not all(
        isinstance(item, str) for item in effective
    ):
        return None, "check %r expect.effective is not a string list" % check_id
    if not isinstance(findings, list) or not all(
        isinstance(item, str) for item in findings
    ):
        return None, "check %r expect.findings is not a string list" % check_id
    return (check_id, path, url, list(effective), list(findings)), None


def resolve_page_path(value: str, root: str, manifest_dir: str):
    """Resolve a check path under ``root`` (or the manifest directory)."""
    bases = [root]
    if os.path.realpath(manifest_dir) != os.path.realpath(root):
        bases.append(manifest_dir)
    for base in bases:
        base_real = os.path.realpath(base)
        candidate = os.path.realpath(os.path.join(base_real, value))
        try:
            inside = os.path.commonpath([base_real, candidate]) == base_real
        except ValueError:
            inside = False
        if not inside:
            continue
        try:
            info = os.stat(candidate)
        except OSError:
            continue
        if stat.S_ISREG(info.st_mode):
            return candidate
    return None


def read_page(path: str):
    """Read a local HTML page as text (UTF-8 BOM-aware, latin-1 fallback)."""
    try:
        with open(path, "rb") as handle:
            data = handle.read()
    except OSError:
        return None
    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return data.decode("latin-1")


# --------------------------------------------------------------------------
# Report assembly
# --------------------------------------------------------------------------


def _report(
    check_count: int,
    results: list[dict[str, object]],
    details: list[dict[str, object]],
    counts: dict[str, int],
    exit_code: int,
    error: str | None = None,
) -> dict[str, object]:
    finding_ids = sorted(detail["id"] for detail in details)
    return {
        "schema": SCHEMA,
        "version": OUTPUT_VERSION,
        "checks": check_count,
        "results": results,
        "findings": details,
        "finding_ids": finding_ids,
        "counts": counts,
        "exit": exit_code,
        "error": error,
    }


def audit_manifest(manifest_path: str, root_arg: str | None):
    """Audit every check in the manifest; return ``(document, exit_code)``."""
    document, error = load_manifest(manifest_path)
    if error is not None:
        counts = {"match": 0, "mismatch": 0, "fault": 0}
        return _report(0, [], [], counts, EXIT_INPUT, error), EXIT_INPUT

    checks, agents, error = validate_manifest(document)
    if error is not None:
        counts = {"match": 0, "mismatch": 0, "fault": 0}
        return _report(0, [], [], counts, EXIT_INPUT, error), EXIT_INPUT

    assert checks is not None and agents is not None
    manifest_dir = os.path.dirname(os.path.realpath(manifest_path))
    root = os.path.abspath(root_arg) if root_arg is not None else manifest_dir

    results: list[dict[str, object]] = []
    details: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    match_count = 0
    mismatch_count = 0
    fault_count = 0

    for check in checks:
        info, error = validate_check(check, seen_ids)
        if error is not None:
            fault_count += 1
            results.append(
                {
                    "id": check.get("id") if isinstance(check, dict) else None,
                    "url": check.get("url") if isinstance(check, dict) else None,
                    "path": check.get("path") if isinstance(check, dict) else None,
                    "status": "fault",
                    "effective": [],
                    "findings": [],
                    "detail": error,
                }
            )
            continue

        assert info is not None
        check_id, relative_path, url, declared_effective, declared_findings = info
        page_path = resolve_page_path(relative_path, root, manifest_dir)
        if page_path is None:
            fault_count += 1
            results.append(
                {
                    "id": check_id,
                    "url": url,
                    "path": relative_path,
                    "status": "fault",
                    "effective": [],
                    "findings": [],
                    "detail": "page %r is not a readable regular file under "
                    "the root" % relative_path,
                }
            )
            continue
        text = read_page(page_path)
        if text is None:
            fault_count += 1
            results.append(
                {
                    "id": check_id,
                    "url": url,
                    "path": relative_path,
                    "status": "fault",
                    "effective": [],
                    "findings": [],
                    "detail": "page %r could not be read" % relative_path,
                }
            )
            continue

        effective, finding_ids, page_findings = audit_page(text, agents)
        for finding_id, detail in page_findings:
            details.append(
                {"check": check_id, "id": finding_id, "detail": detail}
            )

        reported_ids = list(finding_ids)
        if sorted(effective) != sorted(declared_effective) or sorted(
            finding_ids
        ) != sorted(declared_findings):
            mismatch_count += 1
            reported_ids.append(FINDING_EXPECTED_MISMATCH)
            details.append(
                {
                    "check": check_id,
                    "id": FINDING_EXPECTED_MISMATCH,
                    "detail": "expected effective=%s findings=%s but observed "
                    "effective=%s findings=%s"
                    % (
                        json.dumps(sorted(declared_effective), separators=(",", ":")),
                        json.dumps(sorted(declared_findings), separators=(",", ":")),
                        json.dumps(sorted(effective), separators=(",", ":")),
                        json.dumps(sorted(finding_ids), separators=(",", ":")),
                    ),
                }
            )
            status = "mismatch"
        else:
            match_count += 1
            status = "match"
        results.append(
            {
                "id": check_id,
                "url": url,
                "path": relative_path,
                "status": status,
                "effective": effective,
                "findings": sorted(reported_ids),
            }
        )

    counts = {
        "match": match_count,
        "mismatch": mismatch_count,
        "fault": fault_count,
    }
    if fault_count:
        exit_code = EXIT_INPUT
    elif details:
        exit_code = EXIT_FINDING
    else:
        exit_code = EXIT_CLEAN
    report = _report(len(checks), results, details, counts, exit_code)
    return report, exit_code


def print_text(report: dict[str, object]) -> None:
    for result in report["results"]:
        if result.get("detail"):
            sys.stderr.write(
                "fault %s: %s\n" % (result.get("id"), result["detail"])
            )
        sys.stdout.write(
            "%s status=%s effective=%s findings=%s\n"
            % (
                result.get("id"),
                result["status"],
                json.dumps(result["effective"], separators=(",", ":")),
                json.dumps(result["findings"], separators=(",", ":")),
            )
        )
    for detail in report["findings"]:
        sys.stdout.write(
            "%s check=%s %s\n" % (detail["id"], detail["check"], detail["detail"])
        )
    counts = report["counts"]
    sys.stdout.write(
        "checks=%d match=%d mismatch=%d fault=%d findings=%d exit=%d\n"
        % (
            report["checks"],
            counts["match"],
            counts["mismatch"],
            counts["fault"],
            len(report["findings"]),
            report["exit"],
        )
    )
    if report.get("error"):
        sys.stderr.write("error: %s\n" % report["error"])


# --------------------------------------------------------------------------
# Selftest
# --------------------------------------------------------------------------

_SELFTEST_RESULT_KEYS = {
    "schema",
    "version",
    "checks",
    "results",
    "findings",
    "finding_ids",
    "counts",
    "exit",
    "error",
}


def _doc(head: str = "", body: str = "") -> str:
    return (
        "<!doctype html>\n<html><head>"
        + head
        + "</head><body>"
        + body
        + "</body></html>\n"
    )


def _meta(content: str, name: str = "robots", quote: str = '"') -> str:
    return "<meta name=%s%s%s content=%s%s%s>" % (
        quote,
        name,
        quote,
        quote,
        content,
        quote,
    )


def _case(
    name: str,
    html: str | None,
    expected_exit: int,
    expected_effective,
    expected_findings,
    agents=None,
    declared_effective=None,
    declared_findings=None,
    files=None,
    manifest_doc=None,
    manifest_raw=None,
) -> dict:
    return {
        "name": name,
        "html": html,
        "expected_exit": expected_exit,
        "expected_effective": expected_effective,
        "expected_findings": list(expected_findings),
        "agents": agents,
        "declared_effective": (
            list(expected_effective or [])
            if declared_effective is None
            else list(declared_effective)
        ),
        "declared_findings": (
            list(expected_findings)
            if declared_findings is None
            else list(declared_findings)
        ),
        "files": dict(files or {}),
        "manifest_doc": manifest_doc,
        "manifest_raw": manifest_raw,
    }


def _fault_manifest(name: str, check: dict) -> dict:
    return {
        "schema": SCHEMA,
        "checks": [dict({"id": name, "url": "https://example.test/" + name}, **check)],
    }


def _build_cases() -> list[dict]:
    outside = FINDING_OUTSIDE_HEAD
    empty = FINDING_EMPTY_CONTENT
    invalid = FINDING_INVALID_VALUE
    unknown = FINDING_UNKNOWN_DIRECTIVE
    ignored = FINDING_IGNORED_RULE
    mismatch = FINDING_EXPECTED_MISMATCH

    cases = [
        # Frozen families g01-g24 (amended).
        _case("g01_absent_tag", _doc(), 0, ["follow", "index"], []),
        _case("g02_noindex", _doc(_meta("noindex")), 0, ["noindex"], []),
        _case("g03_none", _doc(_meta("none")), 0, ["nofollow", "noindex"], []),
        _case("g04_all", _doc(_meta("all")), 0, ["follow", "index"], []),
        _case(
            "g05_index_follow_one_content",
            _doc(_meta("index,follow")),
            0,
            ["follow", "index"],
            [],
        ),
        _case(
            "g06_index_then_noindex_tags",
            _doc(_meta("index") + _meta("noindex")),
            0,
            ["noindex"],
            [],
        ),
        _case(
            "g07_follow_then_nofollow_tags",
            _doc(_meta("follow") + _meta("nofollow")),
            0,
            ["nofollow"],
            [],
        ),
        _case(
            "g08_snippet_min",
            _doc(_meta("max-snippet:50") + _meta("max-snippet:20")),
            0,
            ["max-snippet:20"],
            [],
        ),
        _case(
            "g09_image_preview_standard_beats_large",
            _doc(_meta("max-image-preview:large") + _meta("max-image-preview:standard")),
            0,
            ["max-image-preview:standard"],
            [],
        ),
        _case(
            "g10_video_preview_min",
            _doc(_meta("max-video-preview:-1") + _meta("max-video-preview:30")),
            0,
            ["max-video-preview:30"],
            [],
        ),
        _case("g11_snippet_invalid", _doc(_meta("max-snippet:abc")), 1, [], [invalid]),
        _case(
            "g12a_unavailable_datetime",
            _doc(_meta("unavailable_after:2030-01-01T00:00:00Z")),
            0,
            ["unavailable_after:2030-01-01T00:00:00Z"],
            [],
        ),
        _case(
            "g12b_unavailable_date_only",
            _doc(_meta("unavailable_after:2020-09-21")),
            0,
            ["unavailable_after:2020-09-21"],
            [],
        ),
        _case(
            "g12c_unavailable_rfc822",
            _doc(_meta("unavailable_after:25 Jun 2010 15:00:00 PST")),
            0,
            ["unavailable_after:25 Jun 2010 15:00:00 PST"],
            [],
        ),
        _case(
            "g12d_unavailable_offsets_earliest_wins",
            _doc(
                _meta("unavailable_after:2026-01-01T00:00:00+02:00")
                + _meta("unavailable_after:2025-12-31T23:30:00Z")
            ),
            0,
            ["unavailable_after:2026-01-01T00:00:00+02:00"],
            [],
        ),
        _case(
            "g13_unavailable_invalid",
            _doc(_meta("unavailable_after:2020-13-40")),
            1,
            [],
            [invalid],
        ),
        _case(
            "g14_uppercase_name_and_content",
            _doc('<META NAME="ROBOTS" CONTENT="NOINDEX, NOFOLLOW">'),
            0,
            ["nofollow", "noindex"],
            [],
        ),
        _case("g15_empty_content", _doc(_meta("")), 1, [], [empty]),
        _case("g16_unknown_directive", _doc(_meta("frobnicate")), 1, [], [unknown]),
        _case(
            "g17_googlebot_ignored_by_default",
            _doc(_meta("noindex", name="googlebot")),
            0,
            ["follow", "index"],
            [],
        ),
        _case(
            "g18_googlebot_merged_when_listed",
            _doc(_meta("index", name="robots") + _meta("noindex", name="googlebot")),
            0,
            ["noindex"],
            [],
            agents=["robots", "googlebot"],
        ),
        _case(
            "g19_body_tag_joins_and_reports",
            _doc(_meta("nofollow"), _meta("noindex")),
            1,
            ["nofollow", "noindex"],
            [outside],
        ),
        _case(
            "g20_declared_index_but_noindex",
            _doc(_meta("noindex")),
            1,
            ["noindex"],
            [mismatch],
            declared_effective=["index"],
            declared_findings=[],
        ),
        _case(
            "g21_self_closing_meta",
            _doc('<meta name="robots" content="noindex" />'),
            0,
            ["noindex"],
            [],
        ),
        _case(
            "g22_single_quotes_no_spaces",
            _doc("<meta name='robots' content='noindex,nofollow'/>"),
            0,
            ["nofollow", "noindex"],
            [],
        ),
        _case(
            "g23_noarchive_ignored_nosnippet_effective",
            _doc(_meta("noarchive, nosnippet")),
            1,
            ["nosnippet"],
            [ignored],
        ),
        _case(
            "g24_trailing_comma_empty_token",
            _doc(_meta("noindex, ,")),
            0,
            ["noindex"],
            [],
        ),
        _case(
            "g25_nosnippet_dominates_snippet",
            _doc(_meta("nosnippet") + _meta("max-snippet:50")),
            0,
            ["nosnippet"],
            [],
        ),
        _case(
            "g26a_snippet_zero_is_nosnippet",
            _doc(_meta("max-snippet:0")),
            0,
            ["nosnippet"],
            [],
        ),
        _case(
            "g26b_video_no_limit_alone",
            _doc(_meta("max-video-preview:-1")),
            0,
            ["max-video-preview:-1"],
            [],
        ),
        _case(
            "g27_indexifembedded_with_noindex",
            _doc(_meta("indexifembedded, noindex")),
            0,
            ["indexifembedded", "noindex"],
            [],
        ),
        # Merge cases.
        _case(
            "m01_duplicate_snippet_same_value",
            _doc(_meta("max-snippet:50") + _meta("max-snippet:50")),
            0,
            ["max-snippet:50"],
            [],
        ),
        _case(
            "m02_three_index_tags",
            _doc(_meta("index") + _meta("noindex") + _meta("index")),
            0,
            ["noindex"],
            [],
        ),
        _case(
            "m03_nosnippet_drops_video",
            _doc(_meta("nosnippet, max-video-preview:30")),
            0,
            ["nosnippet"],
            [],
        ),
        _case(
            "m04_earliest_unavailable_wins",
            _doc(
                _meta("unavailable_after:2030-01-01T00:00:00Z")
                + _meta("unavailable_after:2029-12-31")
            ),
            0,
            ["unavailable_after:2029-12-31"],
            [],
        ),
        _case(
            "m05_image_preview_none_beats_large",
            _doc(_meta("max-image-preview:none") + _meta("max-image-preview:large")),
            0,
            ["max-image-preview:none"],
            [],
        ),
        _case(
            "m06_snippet_no_limit_alone",
            _doc(_meta("max-snippet:-1")),
            0,
            ["max-snippet:-1"],
            [],
        ),
        _case(
            "m07_snippet_no_limit_loses",
            _doc(_meta("max-snippet:-1") + _meta("max-snippet:10")),
            0,
            ["max-snippet:10"],
            [],
        ),
        _case(
            "m08_video_zero_beats_twenty",
            _doc(_meta("max-video-preview:0") + _meta("max-video-preview:20")),
            0,
            ["max-video-preview:0"],
            [],
        ),
        _case(
            "m09_all_then_noindex",
            _doc(_meta("all") + _meta("noindex")),
            0,
            ["follow", "noindex"],
            [],
        ),
        _case(
            "m10_none_then_index",
            _doc(_meta("none") + _meta("index")),
            0,
            ["nofollow", "noindex"],
            [],
        ),
        _case(
            "m11_non_matching_name_ignored",
            _doc(_meta("noindex", name="bingbot")),
            0,
            ["follow", "index"],
            [],
        ),
        _case(
            "m12_googlebot_only_agents",
            _doc(_meta("noindex", name="googlebot")),
            0,
            ["noindex"],
            [],
            agents=["googlebot"],
        ),
        _case(
            "m13_mixed_case_parameter_name",
            _doc(_meta("Max-Snippet:50")),
            0,
            ["max-snippet:50"],
            [],
        ),
        _case(
            "m14_token_whitespace_trimmed",
            _doc(_meta(" Noindex , Nofollow ")),
            0,
            ["nofollow", "noindex"],
            [],
        ),
        _case("m15_noarchive_only", _doc(_meta("noarchive")), 1, [], [ignored]),
        _case("m16_nocache_only", _doc(_meta("nocache")), 1, [], [ignored]),
        _case(
            "m17_nositelinkssearchbox_only",
            _doc(_meta("nositelinkssearchbox")),
            1,
            [],
            [ignored],
        ),
        _case(
            "m18_nosnippet_with_snippet_zero",
            _doc(_meta("nosnippet, max-snippet:0")),
            0,
            ["nosnippet"],
            [],
        ),
        _case(
            "m19_video_zero_alone",
            _doc(_meta("max-video-preview:0")),
            0,
            ["max-video-preview:0"],
            [],
        ),
        _case(
            "m20_duplicate_nosnippet_idempotent",
            _doc(_meta("nosnippet") + _meta("nosnippet")),
            0,
            ["nosnippet"],
            [],
        ),
        _case(
            "m21_indexifembedded_alone",
            _doc(_meta("indexifembedded")),
            0,
            ["indexifembedded"],
            [],
        ),
        _case(
            "m22_image_preview_uppercase_value",
            _doc(_meta("max-image-preview:NONE")),
            0,
            ["max-image-preview:none"],
            [],
        ),
        # Parser cases.
        _case(
            "p01_meta_in_comment_ignored",
            _doc("<!-- " + _meta("noindex") + " -->"),
            0,
            ["follow", "index"],
            [],
        ),
        _case(
            "p02_meta_in_script_ignored",
            _doc("<script>var s='<meta name=\"robots\" content=\"noindex\">';</script>"),
            0,
            ["follow", "index"],
            [],
        ),
        _case(
            "p03_meta_before_head_joins",
            '<html><meta name="robots" content="noindex"><head></head>'
            "<body></body></html>",
            1,
            ["noindex"],
            [outside],
        ),
        _case(
            "p04_meta_after_head_joins",
            _doc("", _meta("noindex")),
            1,
            ["noindex"],
            [outside],
        ),
        _case(
            "p05_body_closes_head",
            "<html><head><title>t</title><body>"
            + _meta("noindex")
            + "</body></html>",
            1,
            ["noindex"],
            [outside],
        ),
        _case(
            "p06_attribute_order_and_unquoted",
            _doc("<meta content=noindex name=robots>"),
            0,
            ["noindex"],
            [],
        ),
        _case(
            "p07_duplicate_name_first_wins",
            _doc('<meta name="googlebot" name="robots" content="noindex">'),
            0,
            ["follow", "index"],
            [],
        ),
        _case(
            "p08_missing_content_attribute",
            _doc('<meta name="robots">'),
            1,
            [],
            [empty],
        ),
        _case(
            "p09_missing_name_ignored",
            _doc('<meta content="noindex">'),
            0,
            ["follow", "index"],
            [],
        ),
        _case(
            "p10_noscript_in_head_collected",
            _doc("<noscript>" + _meta("noindex") + "</noscript>"),
            0,
            ["noindex"],
            [],
        ),
        _case(
            "p11_uppercase_unquoted",
            _doc("<META NAME=robots CONTENT=noindex>"),
            0,
            ["noindex"],
            [],
        ),
        _case(
            "p12_comment_then_real_tag",
            _doc("<!-- " + _meta("index") + " -->" + _meta("noindex")),
            0,
            ["noindex"],
            [],
        ),
        _case(
            "p13_no_head_element",
            "<html>" + _meta("noindex") + "</html>",
            1,
            ["noindex"],
            [outside],
        ),
        _case(
            "p14_character_reference_comma",
            _doc('<meta name="robots" content="noindex&#44;nofollow">'),
            0,
            ["nofollow", "noindex"],
            [],
        ),
        _case(
            "p15_unterminated_meta_at_eof",
            '<html><head><meta name="robots" content="noindex"',
            0,
            ["follow", "index"],
            [],
        ),
        _case(
            "p16_non_matching_second_tag",
            _doc(_meta("noindex") + _meta("index", name="googlebot")),
            0,
            ["noindex"],
            [],
        ),
        # Input and check faults.
        _case("e01_missing_page", None, 2, None, []),
        _case("e02_manifest_not_json", _doc(), 2, None, [], manifest_raw="{not json"),
        _case(
            "e03_wrong_schema",
            _doc(),
            2,
            None,
            [],
            manifest_doc={"schema": "wrong/v1", "checks": []},
        ),
        _case(
            "e04_duplicate_id",
            _doc(),
            2,
            None,
            [],
            manifest_doc={
                "schema": SCHEMA,
                "checks": [
                    {
                        "id": "dup",
                        "path": "page.html",
                        "url": "https://example.test/dup",
                        "expect": {"effective": ["follow", "index"], "findings": []},
                    },
                    {
                        "id": "dup",
                        "path": "page.html",
                        "url": "https://example.test/dup",
                        "expect": {"effective": ["follow", "index"], "findings": []},
                    },
                ],
            },
        ),
        _case(
            "e05_expect_missing",
            _doc(),
            2,
            None,
            [],
            manifest_doc={
                "schema": SCHEMA,
                "checks": [
                    {"id": "x", "path": "page.html", "url": "https://example.test/x"}
                ],
            },
        ),
        _case(
            "e06_expect_effective_not_list",
            _doc(),
            2,
            None,
            [],
            manifest_doc={
                "schema": SCHEMA,
                "checks": [
                    {
                        "id": "x",
                        "path": "page.html",
                        "url": "https://example.test/x",
                        "expect": {"effective": "noindex", "findings": []},
                    }
                ],
            },
        ),
        _case(
            "e07_agents_not_list",
            _doc(),
            2,
            None,
            [],
            manifest_doc={
                "schema": SCHEMA,
                "agents": "robots",
                "checks": [],
            },
        ),
        _case(
            "e08_checks_not_list",
            _doc(),
            2,
            None,
            [],
            manifest_doc={"schema": SCHEMA, "checks": {}},
        ),
        _case(
            "e09_absolute_path",
            _doc(),
            2,
            None,
            [],
            manifest_doc={
                "schema": SCHEMA,
                "checks": [
                    {
                        "id": "x",
                        "path": "/etc/passwd",
                        "url": "https://example.test/x",
                        "expect": {"effective": [], "findings": []},
                    }
                ],
            },
        ),
        _case(
            "e10_empty_checks",
            _doc(),
            0,
            None,
            [],
            manifest_doc={"schema": SCHEMA, "checks": []},
        ),
        _case(
            "e11_url_not_string",
            _doc(),
            2,
            None,
            [],
            manifest_doc={
                "schema": SCHEMA,
                "checks": [
                    {
                        "id": "x",
                        "path": "page.html",
                        "url": 1,
                        "expect": {"effective": [], "findings": []},
                    }
                ],
            },
        ),
        _case(
            "e12_id_empty",
            _doc(),
            2,
            None,
            [],
            manifest_doc={
                "schema": SCHEMA,
                "checks": [
                    {
                        "id": "",
                        "path": "page.html",
                        "url": "https://example.test/x",
                        "expect": {"effective": [], "findings": []},
                    }
                ],
            },
        ),
    ]
    return cases


def _write_case(root: str, case: dict) -> str:
    case_dir = os.path.join(root, case["name"])
    os.makedirs(case_dir, exist_ok=True)
    if case["html"] is not None:
        with open(
            os.path.join(case_dir, "page.html"), "w", encoding="utf-8", newline="\n"
        ) as handle:
            handle.write(case["html"])
    for name, content in case["files"].items():
        with open(os.path.join(case_dir, name), "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
    manifest_path = os.path.join(case_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8", newline="\n") as handle:
        if case["manifest_raw"] is not None:
            handle.write(case["manifest_raw"])
            handle.write("\n")
        elif case["manifest_doc"] is not None:
            json.dump(case["manifest_doc"], handle, sort_keys=True)
            handle.write("\n")
        else:
            manifest = {
                "schema": SCHEMA,
                "checks": [
                    {
                        "id": case["name"],
                        "path": "page.html",
                        "url": "https://example.test/" + case["name"],
                        "expect": {
                            "effective": case["declared_effective"],
                            "findings": case["declared_findings"],
                        },
                    }
                ],
            }
            if case["agents"] is not None:
                manifest["agents"] = case["agents"]
            json.dump(manifest, handle, sort_keys=True)
            handle.write("\n")
    return case_dir


def _run_tool(manifest_path: str, case_dir: str, tmpdir: str):
    argv = [
        sys.executable,
        "-B",
        os.path.realpath(__file__),
        "--manifest",
        manifest_path,
        "--root",
        case_dir,
        "--json",
    ]
    environment = dict(os.environ)
    environment["TMPDIR"] = tmpdir
    return __import__("subprocess").run(
        argv,
        capture_output=True,
        text=True,
        timeout=120,
        cwd=case_dir,
        env=environment,
    )


def _compare(case: dict, proc) -> tuple[bool, str]:
    if proc.returncode != case["expected_exit"]:
        return False, "exit expected %d got %d" % (
            case["expected_exit"],
            proc.returncode,
        )
    try:
        document = json.loads(proc.stdout)
    except (json.JSONDecodeError, ValueError):
        return False, "stdout is not JSON: %r" % proc.stdout[:200]
    if set(document) != _SELFTEST_RESULT_KEYS:
        return False, "JSON keys are %r" % sorted(document)
    if document["exit"] != proc.returncode:
        return False, "JSON exit %r != process exit %d" % (
            document["exit"],
            proc.returncode,
        )
    if set(document["counts"]) != {"match", "mismatch", "fault"}:
        return False, "counts keys are %r" % sorted(document["counts"])
    observed = sorted(document["finding_ids"])
    if observed != sorted(case["expected_findings"]):
        return False, "finding ids expected %r got %r" % (
            sorted(case["expected_findings"]),
            observed,
        )
    if case["expected_effective"] is not None:
        results = document["results"]
        if len(results) != 1:
            return False, "expected one result, got %d" % len(results)
        result = results[0]
        if sorted(result["effective"]) != sorted(case["expected_effective"]):
            return False, "effective expected %r got %r" % (
                sorted(case["expected_effective"]),
                result["effective"],
            )
        if sorted(result["findings"]) != sorted(case["expected_findings"]):
            return False, "check findings expected %r got %r" % (
                sorted(case["expected_findings"]),
                result["findings"],
            )
    return True, ""


def run_selftest(work: str | None) -> int:
    if work is not None:
        work = os.path.abspath(work)
        if os.path.exists(work) and not os.path.isdir(work):
            sys.stderr.write("--work is not a directory: %s\n" % work)
            return EXIT_USAGE
        os.makedirs(work, exist_ok=True)
    base = work if work is not None else tempfile.gettempdir()
    fixture_root = tempfile.mkdtemp(prefix="meta-robots-selftest-", dir=base)
    total = 0
    passed = 0
    first_case_dir = None
    first_manifest = None
    try:
        for case in _build_cases():
            total += 1
            case_dir = _write_case(fixture_root, case)
            manifest_path = os.path.join(case_dir, "manifest.json")
            if first_case_dir is None:
                first_case_dir = case_dir
                first_manifest = manifest_path
            proc = _run_tool(manifest_path, case_dir, fixture_root)
            ok, detail = _compare(case, proc)
            if ok:
                passed += 1
            else:
                sys.stderr.write("FAIL %s: %s\n" % (case["name"], detail))

        # Harness 1: repeated runs are byte-identical.
        total += 1
        assert first_case_dir is not None and first_manifest is not None
        first = _run_tool(first_manifest, first_case_dir, fixture_root)
        second = _run_tool(first_manifest, first_case_dir, fixture_root)
        if (
            first.returncode == 0
            and first.returncode == second.returncode
            and first.stdout == second.stdout
        ):
            passed += 1
        else:
            sys.stderr.write(
                "FAIL harness_determinism: repeated runs differ or exit %d\n"
                % first.returncode
            )

        # Harness 2: the JSON document shape and exit agree.
        total += 1
        try:
            document = json.loads(first.stdout)
            shape_ok = (
                set(document) == _SELFTEST_RESULT_KEYS
                and document["schema"] == SCHEMA
                and document["checks"] == 1
                and document["exit"] == 0
                and document["counts"] == {"match": 1, "mismatch": 0, "fault": 0}
                and document["finding_ids"] == []
                and document["error"] is None
            )
        except (json.JSONDecodeError, ValueError, KeyError, TypeError):
            shape_ok = False
        if shape_ok:
            passed += 1
        else:
            sys.stderr.write("FAIL harness_shape: JSON document shape is wrong\n")

        # Harness 3: the case set reaches the contract's >= 40 floor.
        total += 1
        if total >= 40:
            passed += 1
        else:
            sys.stderr.write(
                "FAIL harness_case_floor: only %d cases\n" % total
            )
    finally:
        import shutil

        shutil.rmtree(fixture_root, ignore_errors=True)

    sys.stdout.write("selftest %d/%d passed\n" % (passed, total))
    sys.stdout.flush()
    return EXIT_CLEAN if passed == total else EXIT_FINDING


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------


class UsageError(Exception):
    """A command-line usage error (exit 64)."""


class _OnceAction(argparse.Action):
    """Reject a repeated option instead of silently keeping the last value."""

    def __call__(self, parser, namespace, values, option_string=None):
        if getattr(namespace, self.dest, None) is not None:
            raise UsageError("%s may be given only once" % option_string)
        setattr(namespace, self.dest, values)


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise UsageError(message)


USAGE = (
    "meta_robots_audit.py --manifest PATH [--root DIR] [--json] | "
    "meta_robots_audit.py --selftest [--work DIR]"
)


def _parse_argv(argv):
    parser = _Parser(
        prog="meta_robots_audit.py",
        usage=USAGE,
        allow_abbrev=False,
    )
    parser.add_argument("--manifest", metavar="PATH", action=_OnceAction, default=None)
    parser.add_argument("--root", metavar="DIR", action=_OnceAction, default=None)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--work", metavar="DIR", action=_OnceAction, default=None)
    return parser.parse_args(argv)


def main(argv) -> int:
    try:
        args = _parse_argv(argv)
        if args.selftest:
            if args.manifest is not None:
                raise UsageError("--selftest does not take --manifest")
            if args.root is not None:
                raise UsageError("--selftest does not take --root")
            if args.json:
                raise UsageError("--selftest does not take --json")
            return run_selftest(args.work)
        if args.manifest is None:
            raise UsageError("--manifest is required")
        if args.work is not None:
            raise UsageError("--work is only valid with --selftest")
        report, exit_code = audit_manifest(args.manifest, args.root)
        if args.json:
            sys.stdout.write(
                json.dumps(report, sort_keys=True, separators=(",", ":")) + "\n"
            )
            if report.get("error"):
                sys.stderr.write("meta_robots_audit.py: %s\n" % report["error"])
        else:
            print_text(report)
        return exit_code
    except UsageError as exc:
        sys.stderr.write("meta_robots_audit.py: %s\nusage: %s\n" % (exc, USAGE))
        return EXIT_USAGE
    except BrokenPipeError:
        return EXIT_USAGE


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
