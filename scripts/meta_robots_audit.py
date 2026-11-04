#!/usr/bin/env python3
"""Offline robots meta-directive audit (round 78, claim C3).

Reads a versioned manifest, parses the local HTML page named by every check,
and reports the declared effective robots rules plus the lane's finding list.
Read-only, network-free, standard library only.  Manifest mode writes nothing;
``--selftest`` writes only inside ``--work`` (or the system temporary directory
when ``--work`` is omitted) and removes its fixture tree.

Manifest ``kake-meta-robots-manifest/v1``::

    {"schema": "kake-meta-robots-manifest/v1",
     "agents": ["robots", ...],                  # optional, default ["robots"]
     "checks": [{"id": "...",                    # non-empty, unique
                 "path": "relative/page.html",   # local HTML, not absolute
                 "url": "https://example/"}]}    # carried through, not fetched

The tool never reads an expectation: the caller compares the printed lists.
``path`` resolves against ``--root`` (default: the manifest's directory); a
path that escapes its root or does not name a regular file is a check fault.

With ``--json`` the tool prints exactly one JSON object on stdout::

    {"version": 1, "checks": [{"id": "...",
                               "effective": [...],
                               "findings": [...]}]}

``effective`` is sorted; ``findings`` is the sorted, de-duplicated list of
finding ids for that check.  On an input or check fault it prints
``{"version": 1, "error": "<code>"}`` and exits 2, with ``<code>`` one of
``missing_file``, ``duplicate_check_id`` or ``bad_manifest``.  Without
``--json`` a human summary is printed; only the JSON form is compared.

Exit: 0 no findings in any processed check · 1 any finding · 2 input or
check fault (error codes ``missing_file``, ``duplicate_check_id``,
``bad_manifest``) · 64 usage (amendment 4 restated the finding cases' exit as
1; amendment 3's C4 exit column had them at 0).

Grammar (frozen contract C3 as corrected by amendments 1-3; the source is the
L1's retained ``robots-meta-tag`` page):

- Matching elements are ``<meta name=... content=...>`` whose ``name`` equals
  one of ``agents`` ASCII-case-insensitively.  An element carrying
  ``http-equiv`` and no ``name`` is never a robots tag.  A matching element
  outside ``<head>`` joins the effective set exactly like a head element
  (A1: Google respects body-section tags) and is also reported as
  ``meta_robots_tag_outside_head`` (lane hygiene).  Only an explicit
  ``<head>`` element scopes placement: a document that omits ``<head>`` has no
  implied head here.
- Content splits on commas; tokens are ASCII-case-insensitively compared and
  whitespace-trimmed on both sides of the first colon; empty tokens are
  ignored; an all-empty or missing ``content`` is
  ``meta_robots_empty_content``.
- Effective vocabulary: ``all``, ``none``, ``index``, ``noindex``, ``follow``,
  ``nofollow``, ``nosnippet``, ``noimageindex``, ``notranslate``,
  ``indexifembedded``, ``max-snippet:<int>``,
  ``max-image-preview:<none|standard|large>``, ``max-video-preview:<int>``,
  ``unavailable_after:<date>``.  ``none`` expands to ``noindex,nofollow`` and
  ``all`` to ``index,follow``.
- Declared-after-collapse merge (amendment 3 C2): ``noindex`` wins over
  ``index`` and ``nofollow`` over ``follow``; the non-collapsing tokens stay
  present as declared; ``max-snippet``/``max-video-preview`` take the smallest
  non-negative integer, with ``-1`` emitted only when it is the family's only
  value; ``max-image-preview`` orders ``none < standard < large``; the
  earliest valid ``unavailable_after`` wins (ties broken by the
  lexicographically smallest literal).
- ``nosnippet`` dominates: when the literal ``nosnippet`` token is declared,
  no numeric ``max-snippet`` or ``max-video-preview`` token is emitted.
  ``max-snippet:0`` renders as ``nosnippet`` and suppresses the numeric
  ``max-snippet`` family only; a separately declared ``max-video-preview``
  survives (frozen g26).
- ``noarchive``, ``nocache`` and ``nositelinkssearchbox`` are ignored rules
  (A3): never effective, reported as ``meta_robots_ignored_rule``.
- ``unavailable_after`` accepts RFC 3339 full-date (``YYYY-MM-DD``), RFC 3339
  date-time (``YYYY-MM-DDThh:mm:ss[.frac](Z|±hh:mm)``, lowercase ``t``/``z``
  permitted) and RFC 822-style ``[EEE,] D Mon YYYY HH:MM:SS ZONE`` where ZONE
  is ``GMT|UT|UTC|EST|EDT|CST|CDT|MST|MDT|PST|PDT`` or ``±HHMM`` (B6).
  RFC 850 is declared not implemented: such a value is
  ``meta_robots_invalid_value``.  Because content splits on commas, the
  optional RFC 822 weekday is merged with one following comma-separated
  fragment before parsing (decision).
- Value errors and unknown tokens are findings and never enter the effective
  set: ``meta_robots_invalid_value`` (malformed integer, bad date, bad
  ``max-image-preview`` value), ``meta_robots_unknown_directive`` (any other
  token).
- Default: when no valid effective rule survives (no matching element, empty
  or missing content, or only invalid/unknown/ignored tokens), the effective
  set is ``["follow","index"]``.

The closed finding vocabulary is exactly: ``meta_robots_empty_content``,
``meta_robots_invalid_value``, ``meta_robots_unknown_directive``,
``meta_robots_tag_outside_head``, ``meta_robots_ignored_rule``.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile

from datetime import date
from html import unescape

# --------------------------------------------------------------------------
# Contract constants
# --------------------------------------------------------------------------

SCHEMA = "kake-meta-robots-manifest/v1"
OUTPUT_VERSION = 1

EXIT_CLEAN = 0
EXIT_FINDING = 1  # unused by this interface; see the module docstring
EXIT_INPUT = 2
EXIT_USAGE = 64

ERROR_MISSING_FILE = "missing_file"
ERROR_DUPLICATE_CHECK_ID = "duplicate_check_id"
ERROR_BAD_MANIFEST = "bad_manifest"

FINDING_OUTSIDE_HEAD = "meta_robots_tag_outside_head"
FINDING_EMPTY_CONTENT = "meta_robots_empty_content"
FINDING_INVALID_VALUE = "meta_robots_invalid_value"
FINDING_UNKNOWN_DIRECTIVE = "meta_robots_unknown_directive"
FINDING_IGNORED_RULE = "meta_robots_ignored_rule"

FINDING_IDS = (
    FINDING_EMPTY_CONTENT,
    FINDING_INVALID_VALUE,
    FINDING_UNKNOWN_DIRECTIVE,
    FINDING_OUTSIDE_HEAD,
    FINDING_IGNORED_RULE,
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
    r"(?:([A-Za-z]{3}),[ \t]+)?([0-9]{1,2}) ([A-Za-z]{3}) ([0-9]{4}) "
    r"([0-9]{2}):([0-9]{2}):([0-9]{2}) "
    r"(GMT|UT|UTC|EST|EDT|CST|CDT|MST|MDT|PST|PDT|[+-][0-9]{4})",
    re.IGNORECASE,
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
_DAYS = frozenset(("mon", "tue", "wed", "thu", "fri", "sat", "sun"))
_ZONE_OFFSETS = {
    "gmt": 0,
    "ut": 0,
    "utc": 0,
    "est": -5 * 3600,
    "edt": -4 * 3600,
    "cst": -6 * 3600,
    "cdt": -5 * 3600,
    "mst": -7 * 3600,
    "mdt": -6 * 3600,
    "pst": -8 * 3600,
    "pdt": -7 * 3600,
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

    Accepted: RFC 3339 full-date, RFC 3339 date-time (lowercase ``t``/``z``
    permitted), and RFC 822-style ``[EEE,] D Mon YYYY HH:MM:SS ZONE`` with the
    B6 zone list or a numeric ``±HHMM`` offset (amendment 3 B6).  A date-only
    value is midnight UTC.  RFC 850 is not implemented and yields None.
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
        weekday = match.group(1)
        if weekday is not None and ascii_lower(weekday) not in _DAYS:
            return None
        day = int(match.group(2))
        month = _MONTHS.get(ascii_lower(match.group(3)))
        year = int(match.group(4))
        hour = int(match.group(5))
        minute = int(match.group(6))
        second = int(match.group(7))
        zone = ascii_lower(match.group(8))
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
            offset_seconds = _ZONE_OFFSETS[zone]
        key = _instant_key(
            year, month, day, hour, minute, second, "", offset_seconds
        )
        return None if key is None else (key, value)

    return None


# --------------------------------------------------------------------------
# Declared-rule state and merge
# --------------------------------------------------------------------------


class _State:
    """Declared-after-collapse merge of the rules in matching elements."""

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

        if self.nosnippet:
            # The literal token dominates both numeric families.
            out.append("nosnippet")
        elif snippet == 0:
            # max-snippet:0 is the source's stated nosnippet equivalent; it
            # suppresses the numeric max-snippet family only (frozen g26).
            out.append("nosnippet")
            if video is not None:
                out.append("max-video-preview:%d" % video)
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
    directive = ascii_lower(name.strip(ASCII_WS))
    value = value.strip(ASCII_WS)
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
    for attrs, in_head in scan_meta_tags(text):
        name = attrs.get("name")
        if name is None:
            continue
        if ascii_lower(name) not in agents:
            continue
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
                    "matching meta name=%r has empty or missing content" % name,
                )
            )
            continue
        index = 0
        while index < len(tokens):
            token = tokens[index]
            raw_name, separator, raw_value = token.partition(":")
            directive = ascii_lower(raw_name.strip(ASCII_WS))
            if separator and directive == "unavailable_after":
                # Content splits on commas, so an RFC 822 weekday needs its
                # comma-joined tail merged back before parsing (decision; one
                # extra fragment is enough for the frozen `[EEE,] ...` form).
                merged = raw_value.strip(ASCII_WS)
                parsed = parse_unavailable_after(merged)
                consumed = index
                if parsed is None and index + 1 < len(tokens):
                    candidate = (merged + ", " + tokens[index + 1]).strip(ASCII_WS)
                    candidate_parsed = parse_unavailable_after(candidate)
                    if candidate_parsed is not None:
                        parsed = candidate_parsed
                        merged = candidate
                        consumed = index + 1
                if parsed is not None:
                    state.unavailable.append(parsed)
                    index = consumed + 1
                    continue
                findings.append(
                    (
                        FINDING_INVALID_VALUE,
                        "invalid value for unavailable_after: %r" % merged,
                    )
                )
                index += 1
                continue
            _apply_token(token, state, findings)
            index += 1

    effective = state.effective()
    if not effective:
        effective = list(DEFAULT_EFFECTIVE)
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
    if document.get("schema") != SCHEMA:
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
    """Return ``(info, error_code)``; ``info`` is a tuple on success."""
    if not isinstance(check, dict):
        return None, ERROR_BAD_MANIFEST
    check_id = check.get("id")
    if not isinstance(check_id, str) or not check_id:
        return None, ERROR_BAD_MANIFEST
    if check_id in seen_ids:
        return None, ERROR_DUPLICATE_CHECK_ID
    seen_ids.add(check_id)

    path = check.get("path")
    if not isinstance(path, str) or not path:
        return None, ERROR_BAD_MANIFEST
    if os.path.isabs(path):
        return None, ERROR_BAD_MANIFEST

    url = check.get("url")
    if not isinstance(url, str):
        return None, ERROR_BAD_MANIFEST
    return (check_id, path, url), None


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


def _fault_report(code: str) -> dict[str, object]:
    return {"version": OUTPUT_VERSION, "error": code}


def audit_manifest(manifest_path: str, root_arg: str | None):
    """Audit every check in the manifest; return ``(document, exit_code)``."""
    document, error = load_manifest(manifest_path)
    if error is not None:
        return _fault_report(ERROR_BAD_MANIFEST), EXIT_INPUT
    checks, agents, error = validate_manifest(document)
    if error is not None:
        return _fault_report(ERROR_BAD_MANIFEST), EXIT_INPUT

    assert checks is not None and agents is not None
    manifest_dir = os.path.dirname(os.path.realpath(manifest_path))
    root = os.path.abspath(root_arg) if root_arg is not None else manifest_dir

    seen_ids: set[str] = set()
    planned: list[tuple[str, str, str]] = []
    for check in checks:
        info, code = validate_check(check, seen_ids)
        if code is not None:
            return _fault_report(code), EXIT_INPUT
        assert info is not None
        planned.append(info)

    results: list[dict[str, object]] = []
    any_finding = False
    for check_id, relative_path, url in planned:
        page_path = resolve_page_path(relative_path, root, manifest_dir)
        if page_path is None:
            return _fault_report(ERROR_MISSING_FILE), EXIT_INPUT
        text = read_page(page_path)
        if text is None:
            return _fault_report(ERROR_MISSING_FILE), EXIT_INPUT
        effective, finding_ids, _findings = audit_page(text, agents)
        findings = sorted(set(finding_ids))
        if findings:
            any_finding = True
        results.append(
            {
                "id": check_id,
                "effective": effective,
                "findings": findings,
            }
        )

    exit_code = EXIT_FINDING if any_finding else EXIT_CLEAN
    return {"version": OUTPUT_VERSION, "checks": results}, exit_code


def print_text(report: dict[str, object], exit_code: int) -> None:
    if "error" in report:
        sys.stderr.write("error: %s\n" % report["error"])
        return
    total = 0
    for result in report["checks"]:
        total += len(result["findings"])
        sys.stdout.write(
            "%s effective=%s findings=%s\n"
            % (
                result["id"],
                json.dumps(result["effective"], separators=(",", ":")),
                json.dumps(result["findings"], separators=(",", ":")),
            )
        )
    sys.stdout.write(
        "checks=%d findings=%d exit=%d\n"
        % (len(report["checks"]), total, exit_code)
    )


# --------------------------------------------------------------------------
# Selftest
# --------------------------------------------------------------------------


def _doc(head: str = "", body: str = "") -> str:
    return (
        "<!doctype html>\n<html><head>"
        + head
        + "</head><body>"
        + body
        + "</body></html>\n"
    )


def _meta(content: str, name: str = "robots") -> str:
    return '<meta name="%s" content="%s">' % (name, content)


def _case(
    name: str,
    html: str | None,
    effective,
    findings,
    agents=None,
    exit_code: int | None = None,
    error: str | None = None,
    files=None,
    manifest_doc=None,
    manifest_raw=None,
    check_count: int = 1,
) -> dict:
    if exit_code is None:
        exit_code = (
            EXIT_INPUT if error is not None else (EXIT_FINDING if findings else EXIT_CLEAN)
        )
    return {
        "name": name,
        "html": html,
        "expected_exit": exit_code,
        "expected_effective": None if effective is None else list(effective),
        "expected_findings": sorted(set(findings or [])),
        "expected_error": error,
        "agents": agents,
        "files": dict(files or {}),
        "manifest_doc": manifest_doc,
        "manifest_raw": manifest_raw,
        "check_count": check_count,
    }


def _build_cases() -> list[dict]:
    outside = FINDING_OUTSIDE_HEAD
    empty = FINDING_EMPTY_CONTENT
    invalid = FINDING_INVALID_VALUE
    unknown = FINDING_UNKNOWN_DIRECTIVE
    ignored = FINDING_IGNORED_RULE
    D = ["follow", "index"]

    cases = [
        # Amendment 3 C4: the 36 frozen ids, in table order.
        _case("g01_absent_tag", _doc(), D, []),
        _case("g02_noindex", _doc(_meta("noindex")), ["noindex"], []),
        _case("g03_none_expansion", _doc(_meta("none")), ["nofollow", "noindex"], []),
        _case("g04_all_default", _doc(_meta("all")), D, []),
        _case("g05_index_follow_one", _doc(_meta("index, follow")), D, []),
        _case(
            "g06_conflicting_noindex",
            _doc(_meta("index") + _meta("noindex")),
            ["noindex"],
            [],
        ),
        _case(
            "g07_conflicting_nofollow",
            _doc(_meta("follow") + _meta("nofollow")),
            ["nofollow"],
            [],
        ),
        _case(
            "g08_max_snippet_two",
            _doc(_meta("max-snippet:50") + _meta("max-snippet:20")),
            ["max-snippet:20"],
            [],
        ),
        _case(
            "g09_max_image_preview_two",
            _doc(
                _meta("max-image-preview:large")
                + _meta("max-image-preview:standard")
            ),
            ["max-image-preview:standard"],
            [],
        ),
        _case(
            "g10_max_video_no_limit",
            _doc(_meta("max-video-preview:-1") + _meta("max-video-preview:30")),
            ["max-video-preview:30"],
            [],
        ),
        _case("g11_max_snippet_invalid", _doc(_meta("max-snippet:abc")), D, [invalid]),
        _case(
            "g12a_unavailable_datetime",
            _doc(_meta("unavailable_after: 2020-09-21T15:00:00Z")),
            ["unavailable_after:2020-09-21T15:00:00Z"],
            [],
        ),
        _case(
            "g12b_unavailable_date",
            _doc(_meta("unavailable_after: 2020-09-21")),
            ["unavailable_after:2020-09-21"],
            [],
        ),
        _case(
            "g12c_unavailable_rfc822",
            _doc(_meta("unavailable_after: 25 Jun 2010 15:00:00 PST")),
            ["unavailable_after:25 Jun 2010 15:00:00 PST"],
            [],
        ),
        _case(
            "g13_unavailable_invalid",
            _doc(_meta("unavailable_after: 2020-13-40")),
            D,
            [invalid],
        ),
        _case(
            "g14_uppercase",
            _doc('<META NAME="ROBOTS" CONTENT="NOINDEX">'),
            ["noindex"],
            [],
        ),
        _case("g15_empty_content", _doc(_meta("")), D, [empty]),
        _case("g16_unknown_directive", _doc(_meta("nosuchthing")), D, [unknown]),
        _case(
            "g17_googlebot_ignored",
            _doc(_meta("noindex", name="googlebot")),
            D,
            [],
        ),
        _case(
            "g18_googlebot_with_agents",
            _doc(_meta("noindex", name="googlebot")),
            ["noindex"],
            [],
            agents=["robots", "googlebot"],
        ),
        _case(
            "g19_body_tag_respected",
            _doc("", _meta("noindex")),
            ["noindex"],
            [outside],
        ),
        _case(
            "g21_self_closing",
            _doc('<meta name="robots" content="noindex" />'),
            ["noindex"],
            [],
        ),
        _case(
            "g22_single_quotes",
            _doc("<meta name='robots' content='noindex'>"),
            ["noindex"],
            [],
        ),
        _case(
            "g23_noarchive_ignored",
            _doc(_meta("noarchive") + _meta("nosnippet")),
            ["nosnippet"],
            [ignored],
        ),
        _case("g24_trailing_comma", _doc(_meta("noindex,")), ["noindex"], []),
        _case(
            "g25_nosnippet_dominates",
            _doc(_meta("nosnippet") + _meta("max-snippet:50")),
            ["nosnippet"],
            [],
        ),
        _case(
            "g26_max_snippet_zero_video_minus_one",
            _doc(_meta("max-snippet:0, max-video-preview:-1")),
            ["max-video-preview:-1", "nosnippet"],
            [],
        ),
        _case(
            "g27_indexifembedded",
            _doc(_meta("noindex, indexifembedded")),
            ["indexifembedded", "noindex"],
            [],
        ),
        _case(
            "g28_within_content_conflict",
            _doc(_meta("index, noindex")),
            ["noindex"],
            [],
        ),
        _case(
            "g29_max_image_preview_none",
            _doc(_meta("max-image-preview:none")),
            ["max-image-preview:none"],
            [],
        ),
        _case(
            "g30_max_snippet_minus_one",
            _doc(_meta("max-snippet:-1")),
            ["max-snippet:-1"],
            [],
        ),
        _case("g31_missing_content", _doc('<meta name="robots">'), D, [empty]),
        _case("g32_nocache_ignored", _doc(_meta("nocache")), D, [ignored]),
        _case(
            "g33_lowercase_t_z",
            _doc(_meta("unavailable_after: 2020-09-21t15:00:00z")),
            ["unavailable_after:2020-09-21t15:00:00z"],
            [],
        ),
        _case("g34_missing_file_exit2", None, None, [], exit_code=2,
              error=ERROR_MISSING_FILE),
        _case(
            "g35_duplicate_id_exit2",
            _doc(),
            None,
            [],
            exit_code=2,
            error=ERROR_DUPLICATE_CHECK_ID,
            manifest_doc={
                "schema": SCHEMA,
                "checks": [
                    {
                        "id": "dup",
                        "path": "page.html",
                        "url": "https://example.test/dup",
                    },
                    {
                        "id": "dup",
                        "path": "page.html",
                        "url": "https://example.test/dup",
                    },
                ],
            },
        ),
        # Amendment-1/3 merge and grammar extras.
        _case(
            "m01_duplicate_snippet_same_value",
            _doc(_meta("max-snippet:50") + _meta("max-snippet:50")),
            ["max-snippet:50"],
            [],
        ),
        _case(
            "m02_three_index_tags",
            _doc(_meta("index") + _meta("noindex") + _meta("index")),
            ["noindex"],
            [],
        ),
        _case(
            "m03_literal_nosnippet_drops_video",
            _doc(_meta("nosnippet, max-video-preview:30")),
            ["nosnippet"],
            [],
        ),
        _case(
            "m04_earliest_unavailable_wins",
            _doc(
                _meta("unavailable_after:2030-01-01T00:00:00Z")
                + _meta("unavailable_after:2029-12-31")
            ),
            ["unavailable_after:2029-12-31"],
            [],
        ),
        _case(
            "m05_image_none_beats_large",
            _doc(_meta("max-image-preview:none") + _meta("max-image-preview:large")),
            ["max-image-preview:none"],
            [],
        ),
        _case(
            "m06_snippet_no_limit_alone",
            _doc(_meta("max-snippet:-1")),
            ["max-snippet:-1"],
            [],
        ),
        _case(
            "m07_snippet_no_limit_loses",
            _doc(_meta("max-snippet:-1") + _meta("max-snippet:10")),
            ["max-snippet:10"],
            [],
        ),
        _case(
            "m08_video_zero_beats_twenty",
            _doc(_meta("max-video-preview:0") + _meta("max-video-preview:20")),
            ["max-video-preview:0"],
            [],
        ),
        _case(
            "m09_all_then_noindex",
            _doc(_meta("all") + _meta("noindex")),
            ["follow", "noindex"],
            [],
        ),
        _case(
            "m10_none_then_index",
            _doc(_meta("none") + _meta("index")),
            ["nofollow", "noindex"],
            [],
        ),
        _case(
            "m11_non_matching_name_ignored",
            _doc(_meta("noindex", name="bingbot")),
            D,
            [],
        ),
        _case(
            "m12_googlebot_only_agents",
            _doc(_meta("noindex", name="googlebot")),
            ["noindex"],
            [],
            agents=["googlebot"],
        ),
        _case("m13_mixed_case_parameter_name", _doc(_meta("Max-Snippet:50")),
              ["max-snippet:50"], []),
        _case("m14_token_whitespace_trimmed", _doc(_meta(" Noindex , Nofollow ")),
              ["nofollow", "noindex"], []),
        _case("m15_noarchive_only", _doc(_meta("noarchive")), D, [ignored]),
        _case("m16_nocache_only", _doc(_meta("nocache")), D, [ignored]),
        _case(
            "m17_nositelinkssearchbox_only",
            _doc(_meta("nositelinkssearchbox")),
            D,
            [ignored],
        ),
        _case(
            "m18_nosnippet_with_snippet_zero",
            _doc(_meta("nosnippet, max-snippet:0")),
            ["nosnippet"],
            [],
        ),
        _case("m19_video_zero_alone", _doc(_meta("max-video-preview:0")),
              ["max-video-preview:0"], []),
        _case(
            "m20_duplicate_nosnippet_idempotent",
            _doc(_meta("nosnippet") + _meta("nosnippet")),
            ["nosnippet"],
            [],
        ),
        _case("m21_indexifembedded_alone", _doc(_meta("indexifembedded")),
              ["indexifembedded"], []),
        _case("m22_image_preview_uppercase_value", _doc(_meta("max-image-preview:NONE")),
              ["max-image-preview:none"], []),
        _case(
            "m23_rfc822_weekday_zone_offset",
            _doc(_meta("unavailable_after: Mon, 25 Jun 2010 15:00:00 PST")),
            ["unavailable_after:Mon, 25 Jun 2010 15:00:00 PST"],
            [],
        ),
        _case(
            "m24_rfc822_numeric_zone",
            _doc(_meta("unavailable_after: 25 Jun 2010 15:00:00 +0200")),
            ["unavailable_after:25 Jun 2010 15:00:00 +0200"],
            [],
        ),
        _case(
            "m25_rfc850_unimplemented_invalid",
            _doc(_meta("unavailable_after: Sunday, 06-Nov-94 08:49:37 GMT")),
            D,
            [invalid, unknown],
        ),
        _case(
            "m26_unavailable_offsets_earliest_wins",
            _doc(
                _meta("unavailable_after:2026-01-01T00:00:00+02:00")
                + _meta("unavailable_after:2025-12-31T23:30:00Z")
            ),
            ["unavailable_after:2026-01-01T00:00:00+02:00"],
            [],
        ),
        _case(
            "m27_literal_nosnippet_keeps_image",
            _doc(_meta("nosnippet, max-image-preview:standard")),
            ["max-image-preview:standard", "nosnippet"],
            [],
        ),
        # Parser cases.
        _case(
            "p01_meta_in_comment_ignored",
            _doc("<!-- " + _meta("noindex") + " -->"),
            D,
            [],
        ),
        _case(
            "p02_meta_in_script_ignored",
            _doc("<script>var s='<meta name=\"robots\" content=\"noindex\">';</script>"),
            D,
            [],
        ),
        _case(
            "p03_meta_before_head_joins",
            '<html><meta name="robots" content="noindex"><head></head>'
            "<body></body></html>",
            ["noindex"],
            [outside],
        ),
        _case("p04_meta_after_head_joins", _doc("", _meta("noindex")),
              ["noindex"], [outside]),
        _case(
            "p05_body_closes_head",
            "<html><head><title>t</title><body>"
            + _meta("noindex")
            + "</body></html>",
            ["noindex"],
            [outside],
        ),
        _case(
            "p06_attribute_order_and_unquoted",
            _doc("<meta content=noindex name=robots>"),
            ["noindex"],
            [],
        ),
        _case(
            "p07_duplicate_name_first_wins",
            _doc('<meta name="googlebot" name="robots" content="noindex">'),
            D,
            [],
        ),
        _case("p08_missing_content_attribute", _doc('<meta name="robots">'), D,
              [empty]),
        _case("p09_missing_name_ignored", _doc('<meta content="noindex">'), D, []),
        _case(
            "p10_noscript_in_head_collected",
            _doc("<noscript>" + _meta("noindex") + "</noscript>"),
            ["noindex"],
            [],
        ),
        _case("p11_uppercase_unquoted", _doc("<META NAME=robots CONTENT=noindex>"),
              ["noindex"], []),
        _case(
            "p12_comment_then_real_tag",
            _doc("<!-- " + _meta("index") + " -->" + _meta("noindex")),
            ["noindex"],
            [],
        ),
        _case("p13_no_head_element", "<html>" + _meta("noindex") + "</html>",
              ["noindex"], [outside]),
        _case(
            "p14_character_reference_comma",
            _doc('<meta name="robots" content="noindex&#44;nofollow">'),
            ["nofollow", "noindex"],
            [],
        ),
        _case(
            "p15_unterminated_meta_at_eof",
            '<html><head><meta name="robots" content="noindex"',
            D,
            [],
        ),
        _case(
            "p16_non_matching_second_tag",
            _doc(_meta("noindex") + _meta("index", name="googlebot")),
            ["noindex"],
            [],
        ),
        _case(
            "p17_http_equiv_only_not_counted",
            _doc('<meta http-equiv="robots" content="noindex">'),
            D,
            [],
        ),
        _case(
            "p18_expect_key_never_read",
            _doc(),
            D,
            [],
            manifest_doc={
                "schema": SCHEMA,
                "checks": [
                    {
                        "id": "p18_expect_key_never_read",
                        "path": "page.html",
                        "url": "https://example.test/p18",
                        "expect": {"effective": ["noindex"], "findings": []},
                    }
                ],
            },
        ),
        # Input and check faults.
        _case("e01_missing_page", None, None, [], exit_code=2,
              error=ERROR_MISSING_FILE),
        _case("e02_manifest_not_json", _doc(), None, [], exit_code=2,
              error=ERROR_BAD_MANIFEST, manifest_raw="{not json"),
        _case(
            "e03_wrong_schema",
            _doc(),
            None,
            [],
            exit_code=2,
            error=ERROR_BAD_MANIFEST,
            manifest_doc={"schema": "wrong/v1", "checks": []},
        ),
        _case(
            "e04_duplicate_id",
            _doc(),
            None,
            [],
            exit_code=2,
            error=ERROR_DUPLICATE_CHECK_ID,
            manifest_doc={
                "schema": SCHEMA,
                "checks": [
                    {"id": "dup", "path": "page.html", "url": "u"},
                    {"id": "dup", "path": "page.html", "url": "u"},
                ],
            },
        ),
        _case(
            "e07_agents_not_list",
            _doc(),
            None,
            [],
            exit_code=2,
            error=ERROR_BAD_MANIFEST,
            manifest_doc={"schema": SCHEMA, "agents": "robots", "checks": []},
        ),
        _case(
            "e08_checks_not_list",
            _doc(),
            None,
            [],
            exit_code=2,
            error=ERROR_BAD_MANIFEST,
            manifest_doc={"schema": SCHEMA, "checks": {}},
        ),
        _case(
            "e09_absolute_path",
            _doc(),
            None,
            [],
            exit_code=2,
            error=ERROR_BAD_MANIFEST,
            manifest_doc={
                "schema": SCHEMA,
                "checks": [{"id": "x", "path": "/etc/passwd", "url": "u"}],
            },
        ),
        _case(
            "e10_empty_checks",
            _doc(),
            None,
            [],
            manifest_doc={"schema": SCHEMA, "checks": []},
            check_count=0,
        ),
        _case(
            "e11_url_not_string",
            _doc(),
            None,
            [],
            exit_code=2,
            error=ERROR_BAD_MANIFEST,
            manifest_doc={
                "schema": SCHEMA,
                "checks": [{"id": "x", "path": "page.html", "url": 1}],
            },
        ),
        _case(
            "e12_id_empty",
            _doc(),
            None,
            [],
            exit_code=2,
            error=ERROR_BAD_MANIFEST,
            manifest_doc={
                "schema": SCHEMA,
                "checks": [{"id": "", "path": "page.html", "url": "u"}],
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
        with open(
            os.path.join(case_dir, name), "w", encoding="utf-8", newline="\n"
        ) as handle:
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
    return subprocess.run(
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
    if not isinstance(document, dict) or document.get("version") != OUTPUT_VERSION:
        return False, "JSON version is not %d" % OUTPUT_VERSION

    if case["expected_error"] is not None:
        if set(document) != {"version", "error"}:
            return False, "fault JSON keys are %r" % sorted(document)
        if document["error"] != case["expected_error"]:
            return False, "error expected %r got %r" % (
                case["expected_error"],
                document["error"],
            )
        return True, ""

    if set(document) != {"version", "checks"}:
        return False, "JSON keys are %r" % sorted(document)
    checks = document["checks"]
    if not isinstance(checks, list) or len(checks) != case["check_count"]:
        return False, "check count expected %d got %r" % (
            case["check_count"],
            checks,
        )
    if case["check_count"] == 0:
        return True, ""
    result = checks[0]
    if set(result) != {"id", "effective", "findings"}:
        return False, "check keys are %r" % sorted(result)
    if result["id"] != case["name"]:
        return False, "id expected %r got %r" % (case["name"], result["id"])
    if sorted(result["effective"]) != sorted(case["expected_effective"]):
        return False, "effective expected %r got %r" % (
            sorted(case["expected_effective"]),
            result["effective"],
        )
    if sorted(result["findings"]) != case["expected_findings"]:
        return False, "findings expected %r got %r" % (
            case["expected_findings"],
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

        total += 1
        try:
            document = json.loads(first.stdout)
            shape_ok = (
                set(document) == {"version", "checks"}
                and document["version"] == OUTPUT_VERSION
                and len(document["checks"]) == 1
                and set(document["checks"][0])
                == {"id", "effective", "findings"}
            )
        except (json.JSONDecodeError, ValueError, KeyError, TypeError):
            shape_ok = False
        if shape_ok:
            passed += 1
        else:
            sys.stderr.write("FAIL harness_shape: JSON document shape is wrong\n")

        total += 1
        if total >= 40:
            passed += 1
        else:
            sys.stderr.write("FAIL harness_case_floor: only %d cases\n" % total)
    finally:
        shutil.rmtree(fixture_root, ignore_errors=True)

    sys.stdout.write("selftest: %d/%d passed\n" % (passed, total))
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
            if "error" in report:
                sys.stderr.write("meta_robots_audit.py: %s\n" % report["error"])
        else:
            print_text(report, exit_code)
        return exit_code
    except UsageError as exc:
        sys.stderr.write("meta_robots_audit.py: %s\nusage: %s\n" % (exc, USAGE))
        return EXIT_USAGE
    except BrokenPipeError:
        return EXIT_USAGE


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
