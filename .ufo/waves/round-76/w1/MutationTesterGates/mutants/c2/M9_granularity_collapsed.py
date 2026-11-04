#!/usr/bin/env python3
"""Offline hreflang declaration audit (round 76, claim C2).

Reads a version-1 manifest, parses the local HTML file named by every page,
and decides the frozen finding set in contract C2 as amended by Amendment 2.
Read-only, network-free, standard library only.  Nothing is written in
manifest mode; ``--selftest`` writes only inside ``--work``.

Manifest v1::

    {"version": 1, "pages": [{"id": ..., "file": ..., "url": ...}, ...]}

``url`` is an absolute URL with scheme and authority; ``file`` is a local HTML
path relative to ``--root``.  ``--root`` defaults to the process cwd.

Exit: 0 clean, 1 policy findings, 2 input faults, 64 usage (including a
manifest version other than 1, amendment A15).

Findings carry ``severity`` ``policy`` / ``info`` / ``input``.  An
informational finding leaves the exit at 0 (A1).  Policy findings are emitted
once per offending annotation, except ``hreflang_self_missing`` and
``hreflang_canonical_not_self`` (once per page) and input faults (once per
manifest entry) (A2).

URL equality is exact string equality after RFC 3986 normalization: scheme
and host lowercased, scheme-default port removed, dot-segments removed, empty
path replaced by ``/``; a trailing slash stays significant (A3).  A href that
is not an absolute URL with scheme and authority is reported as
``hreflang_relative_href`` and is not resolved, so it contributes to no other
finding (A4, A12).

Parser scope.  A single-pass, tolerant scanner extracts ``<link>`` start tags
only.  It supports: attributes in any order, single/double quoted and unquoted
values read as HTML reads them, a self-closing slash, comments and
``<!...>``/``<?...?>`` constructs, comments and ``<script>``/``<style>`` raw
text skipped, ``<template>``/``<svg>``/``<math>`` subtrees skipped (a
self-closed ``<svg/>`` or ``<math/>`` opens nothing), ``<noscript>`` content
scanned as markup, and HTML character references decoded in every attribute
value.  Tag and attribute names are ASCII-lowercased; the first occurrence of
a repeated attribute wins.  ``rel`` is an ASCII case-insensitive token set,
and a link whose tokens include ``stylesheet`` is not an alternate.  An
``hreflang`` value is validated exactly as written: the frozen grammar is
anchored, so surrounding whitespace is invalid rather than trimmed away.

It does not do: HTML tree construction, implied or optional tags, character
encoding sniffing from ``<meta charset>``, SVG/MathML namespace or
foreign-content integration-point rules beyond subtree skipping, or any
recovery beyond the above.  A link is collected wherever it appears in the
document outside those skipped regions; no head-only restriction is applied
because contract C2 states none.  Files are decoded as UTF-8 (BOM ignored) and
fall back to latin-1, so no page is rejected for its bytes.

Deliberate non-goals (contract C2 limits): no live fetch, no HTTP headers or
``Vary``, no rendering or JavaScript, no hreflang value outside ``x-default``
and the frozen ASCII BCP-47 grammar, no claim about the actual language of a
page, no search-engine selection or ranking claim.
"""

from __future__ import annotations

import argparse
import json
import os
import posixpath
import re
import shutil
import stat
import string
import subprocess
import sys
import tempfile
from html import unescape
from urllib.parse import urlsplit

# --------------------------------------------------------------------------
# Contract constants
# --------------------------------------------------------------------------

OUTPUT_VERSION = 1

EXIT_CLEAN = 0
EXIT_POLICY = 1
EXIT_INPUT = 2
EXIT_USAGE = 64

POLICY_IDS = (
    "hreflang_missing_value",
    "hreflang_invalid_tag",
    "hreflang_relative_href",
    "hreflang_duplicate_pair",
    "hreflang_multiple_xdefault",
    "hreflang_self_missing",
    "hreflang_nonreciprocal",
    "hreflang_canonical_not_self",
)
INFO_IDS = ("hreflang_external_target",)
INPUT_IDS = ("input_unreadable", "input_duplicate_url", "input_url_not_absolute")

FINDING_ORDER = POLICY_IDS + INFO_IDS + INPUT_IDS
RANK = {name: index for index, name in enumerate(FINDING_ORDER)}
SEVERITY_OF = dict(
    [(name, "policy") for name in POLICY_IDS]
    + [(name, "info") for name in INFO_IDS]
    + [(name, "input") for name in INPUT_IDS]
)

ASCII_WS = " \t\n\r\f"
ASCII_WS_SET = frozenset(ASCII_WS)
_WS_RUN = re.compile(r"[ \t\n\r\f]+")

# Frozen BCP-47 grammar, verbatim from contract C2 minus the anchors.  The
# value is ASCII-lowercased before matching, so the classes are lowercase.
# ASCII lowering keeps Python's Unicode-aware IGNORECASE (which also folds
# U+0130 and friends into [A-Za-z]) out of the decision.
BCP47_GRAMMAR = re.compile(
    r"[a-z]{2,3}(-[a-z]{4})?(-([a-z]{2}|[0-9]{3}))?(-([a-z0-9]{5,8}|[0-9][a-z0-9]{3}))*"
)

_ASCII_LOWER_TABLE = str.maketrans(string.ascii_uppercase, string.ascii_lowercase)

_TAG_NAME_START = frozenset(string.ascii_letters)
_TAG_NAME_CHARS = frozenset(string.ascii_letters + string.digits + ":-_")
_ATTR_NAME_STOP = frozenset(ASCII_WS + "/>=")

USAGE_LINE = (
    "usage: hreflang_audit.py --manifest PATH [--root DIR] [--json]\n"
    "       hreflang_audit.py --selftest --work DIR\n"
)


class UsageError(Exception):
    """Invalid command-line shape (exit 64)."""


class ManifestVersionError(Exception):
    """A manifest version other than 1 is a usage error (A15)."""


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------

def ascii_lower(text: str) -> str:
    """ASCII-only lowercasing (contract C2 says case-insensitive)."""
    return text.translate(_ASCII_LOWER_TABLE)


def strip_ws(text: str) -> str:
    return text.strip(ASCII_WS)


def absolute_with_host(value):
    """True when value carries a scheme and a non-empty authority.

    Contract C2's "absolute" for page urls and the complement of
    ``hreflang_relative_href`` share this predicate (A12).  It is a presence
    test, not RFC 3986 validation.
    """
    if value is None:
        return False
    try:
        parts = urlsplit(value)
    except ValueError:
        return False
    return bool(parts.scheme) and bool(parts.netloc)


def valid_bcp47(tag: str) -> bool:
    """True when tag is x-default or matches the frozen ASCII grammar."""
    if tag == "":
        return False
    lowered = ascii_lower(tag)
    if lowered == "x-default":
        return True
    return BCP47_GRAMMAR.fullmatch(lowered) is not None


# --------------------------------------------------------------------------
# URL equality (amendment A3)
# --------------------------------------------------------------------------

_DEFAULT_PORTS = {"http": 80, "https": 443}


def _remove_dot_segments(path: str) -> str:
    """RFC 3986 section 5.2.4 on one path string."""
    output = []
    while path:
        if path.startswith("../"):
            path = path[3:]
        elif path.startswith("./"):
            path = path[2:]
        elif path.startswith("/./"):
            path = "/" + path[3:]
        elif path == "/.":
            path = "/"
        elif path.startswith("/../"):
            path = "/" + path[4:]
            if output:
                output.pop()
        elif path == "/..":
            path = "/"
            if output:
                output.pop()
        elif path in (".", ".."):
            path = ""
        else:
            cut = path.find("/", 1 if path.startswith("/") else 0)
            if cut < 0:
                output.append(path)
                path = ""
            else:
                output.append(path[:cut])
                path = path[cut:]
    return "".join(output)


def normalize_url(value):
    """The tool's URL identity under amendment A3.

    An absolute URL with scheme and authority is rebuilt with scheme and host
    lowercased, a scheme-default port dropped, dot-segments removed, and an
    empty path replaced by ``/``.  Trailing slashes, percent-encoding, query
    and fragment text are otherwise preserved exactly.  A value that is not
    absolute, or whose authority cannot be re-read (port, bracket literal),
    is returned unchanged.
    """
    if not absolute_with_host(value):
        return value
    try:
        parts = urlsplit(value)
        port = parts.port
    except ValueError:
        return value
    scheme = ascii_lower(parts.scheme)
    host = parts.hostname or ""
    if ":" in host and not host.startswith("["):
        host = "[" + host + "]"
    netloc = host
    if parts.username is not None:
        netloc = parts.username
        if parts.password is not None:
            netloc += ":" + parts.password
        netloc += "@" + host
    if port is not None and _DEFAULT_PORTS.get(scheme) != port:
        netloc += ":" + str(port)
    path = _remove_dot_segments(parts.path)
    if path == "":
        path = "/"
    normalized = scheme + "://" + netloc + path
    if parts.query:
        normalized += "?" + parts.query
    if parts.fragment:
        normalized += "#" + parts.fragment
    return normalized


# --------------------------------------------------------------------------
# Tolerant <link> scanner
# --------------------------------------------------------------------------

def _parse_attributes(text: str, pos: int):
    """Parse attributes from pos to the end of the start tag.

    Returns ``(attrs, next_pos, self_closing)``.  ``attrs`` maps ASCII-lowered
    attribute names to entity-decoded values (None for a value-less
    attribute), first occurrence wins.  Unterminated tags swallow the rest of
    the document, which is the tolerant choice for a scanner that must still
    decide the tag.
    """
    attrs: dict[str, str | None] = {}
    length = len(text)
    while pos < length:
        char = text[pos]
        if char in ASCII_WS_SET:
            pos += 1
            continue
        if char == ">":
            return attrs, pos + 1, False
        if char == "/":
            if pos + 1 < length and text[pos + 1] == ">":
                return attrs, pos + 2, True
            pos += 1
            continue
        start = pos
        while pos < length and text[pos] not in _ATTR_NAME_STOP:
            pos += 1
        name = ascii_lower(text[start:pos])
        if not name:
            pos += 1
            continue
        while pos < length and text[pos] in ASCII_WS_SET:
            pos += 1
        value = None
        if pos < length and text[pos] == "=":
            pos += 1
            while pos < length and text[pos] in ASCII_WS_SET:
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
                value = unescape(raw)
            else:
                start = pos
                while pos < length and text[pos] not in ASCII_WS_SET and text[pos] != ">":
                    pos += 1
                value = unescape(text[start:pos])
        if name not in attrs:
            attrs[name] = value
    return attrs, length, False


def _skip_body(lowered: str, text: str, pos: int, name: str) -> int:
    """Index just past the end tag closing a script/style raw-text body."""
    needle = "</" + name
    length = len(text)
    while True:
        found = lowered.find(needle, pos)
        if found < 0:
            return length
        cursor = found + len(needle)
        if cursor < length and text[cursor] not in ASCII_WS_SET and text[cursor] not in "/>":
            pos = found + 1
            continue
        end = text.find(">", cursor)
        return length if end < 0 else end + 1


def _skip_subtree(lowered: str, text: str, pos: int, name: str) -> int:
    """Index just past the end tag closing a template/svg/math subtree.

    Depth counts same-name start tags, so a nested ``<svg>`` does not end the
    subtree at the inner close.  Comments and script/style raw text inside the
    subtree are skipped so their bytes cannot close it.  A self-closed
    ``<svg/>`` or ``<math/>`` opens nothing (amendment A13); a self-closed
    ``<template/>`` still opens one, as HTML reads it.
    """
    depth = 1
    length = len(text)
    while pos < length:
        found = text.find("<", pos)
        if found < 0:
            return length
        pos = found
        if text.startswith("<!--", pos):
            end = text.find("-->", pos + 4)
            pos = length if end < 0 else end + 3
            continue
        if text.startswith("<!", pos) or text.startswith("<?", pos):
            end = text.find(">", pos + 2)
            pos = length if end < 0 else end + 1
            continue
        if text.startswith("</", pos):
            cursor = pos + 2
            start = cursor
            while cursor < length and text[cursor] in _TAG_NAME_CHARS:
                cursor += 1
            tag = ascii_lower(text[start:cursor])
            end = text.find(">", cursor)
            pos = length if end < 0 else end + 1
            if tag == name:
                depth -= 1
                if depth == 0:
                    return pos
            continue
        cursor = pos + 1
        if cursor >= length or text[cursor] not in _TAG_NAME_START:
            pos += 1
            continue
        name_end = cursor + 1
        while name_end < length and text[name_end] in _TAG_NAME_CHARS:
            name_end += 1
        tag = ascii_lower(text[cursor:name_end])
        _, after, self_closing = _parse_attributes(text, name_end)
        pos = after
        if tag in ("script", "style"):
            pos = _skip_body(lowered, text, after, tag)
            continue
        if tag == name and not (name in ("svg", "math") and self_closing):
            depth += 1
    return length


def iter_link_attributes(text: str):
    """Yield the attribute map of every ``<link>`` start tag in document order."""
    lowered = ascii_lower(text)
    length = len(text)
    pos = 0
    while pos < length:
        found = text.find("<", pos)
        if found < 0:
            return
        pos = found
        if text.startswith("<!--", pos):
            end = text.find("-->", pos + 4)
            pos = length if end < 0 else end + 3
            continue
        if text.startswith("<![CDATA[", pos):
            end = text.find("]]>", pos + 9)
            pos = length if end < 0 else end + 3
            continue
        if text.startswith("<!", pos) or text.startswith("<?", pos):
            end = text.find(">", pos + 2)
            pos = length if end < 0 else end + 1
            continue
        if text.startswith("</", pos):
            end = text.find(">", pos + 2)
            pos = length if end < 0 else end + 1
            continue
        cursor = pos + 1
        if cursor >= length or text[cursor] not in _TAG_NAME_START:
            pos += 1
            continue
        name_end = cursor + 1
        while name_end < length and text[name_end] in _TAG_NAME_CHARS:
            name_end += 1
        name = ascii_lower(text[cursor:name_end])
        attrs, after, self_closing = _parse_attributes(text, name_end)
        if name == "link":
            yield attrs
        pos = after
        # Comments, raw text and foreign/template subtrees are not scanned
        # (amendment A13).  HTML ignores a self-closing slash on script,
        # style and template, so their bodies always run to an end tag.
        if name in ("script", "style"):
            pos = _skip_body(lowered, text, after, name)
        elif name in ("template", "svg", "math"):
            if not (name in ("svg", "math") and self_closing):
                pos = _skip_subtree(lowered, text, after, name)


def rel_tokens(attrs: dict) -> tuple:
    """ASCII-lowercased rel tokens; a value-less rel has no tokens."""
    rel = attrs.get("rel")
    if rel is None:
        return ()
    return tuple(ascii_lower(token) for token in _WS_RUN.split(strip_ws(rel)) if token)


def _collect_links(text: str):
    """Return (alternates, canonical) for one document.

    An alternate is a ``<link>`` whose rel token set contains ``alternate``,
    does not contain ``stylesheet`` (A13), and carries an ``href`` attribute
    (A9).  Each alternate is a dict with keys ``order``, ``tag`` (the
    ``hreflang`` attribute value exactly as written, "" when absent or empty:
    the frozen grammar is anchored, so surrounding whitespace is not trimmed
    and fails validation) and ``href`` (stripped effective value).

    The canonical is the first ``<link>`` carrying the ``canonical`` token
    (A6), whether or not it also carries ``hreflang`` (A7).
    """
    alternates = []
    canonical = None
    order = 0
    for attrs in iter_link_attributes(text):
        tokens = rel_tokens(attrs)
        href = attrs.get("href")
        href_present = href is not None
        href = None if href is None else strip_ws(href)
        if "alternate" in tokens and "stylesheet" not in tokens and href_present:
            tag = attrs.get("hreflang")
            alternates.append(
                {"order": order, "tag": "" if tag is None else tag, "href": href})
            order += 1
        if canonical is None and "canonical" in tokens:
            canonical = {"href": href}
    return alternates, canonical


# --------------------------------------------------------------------------
# Manifest
# --------------------------------------------------------------------------

def _read_manifest(path: str):
    try:
        with open(path, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        return None, "manifest unreadable (%s)" % exc.strerror
    except ValueError:
        return None, "manifest path is invalid"
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return None, "manifest is not UTF-8"
    try:
        document = json.loads(text)
    except (json.JSONDecodeError, RecursionError) as exc:
        return None, "manifest is not JSON (%s)" % exc
    return document, None


def _fault(finding_id: str, detail: str, page=None):
    return {"id": finding_id, "severity": SEVERITY_OF[finding_id],
            "page": page, "detail": detail}


def _file_problem(value) -> bool:
    """True when a manifest file value is not a plain root-relative path."""
    if not isinstance(value, str) or value == "":
        return True
    if value.startswith("/"):
        return True
    if "\\" in value:
        # Manifest paths are forward-slash paths; a backslash is a literal
        # filename character on POSIX but not a relative path separator.
        return True
    parts = value.split("/")
    return any(part == ".." for part in parts)


def validate_manifest(document):
    """Return (pages, faults, manifest_page_count).

    ``pages`` holds only entries that pass the manifest checks; ``faults``
    holds one input finding per offending manifest entry (A2, A15).  A
    version other than 1 raises ManifestVersionError (exit 64, A15).
    """
    if not isinstance(document, dict):
        return [], [_fault("input_unreadable", "manifest root is not an object")], 0
    version = document.get("version")
    if version != 1 or isinstance(version, bool):
        raise ManifestVersionError("manifest version is not 1")
    raw_pages = document.get("pages")
    if not isinstance(raw_pages, list):
        return [], [_fault("input_unreadable", "manifest pages is not a list")], 0

    page_count = len(raw_pages)
    pages = []
    faults = []
    seen_ids = set()
    seen_urls = set()
    seen_files = set()
    for index, raw in enumerate(raw_pages):
        if not isinstance(raw, dict):
            faults.append(_fault("input_unreadable", "page[%d] is not an object" % index))
            continue
        page_id = raw.get("id")
        file_value = raw.get("file")
        url = raw.get("url")
        if not isinstance(page_id, str) or page_id == "":
            faults.append(_fault("input_unreadable", "page[%d] has no id" % index))
            continue
        if page_id in seen_ids:
            faults.append(_fault("input_unreadable", "page id %r is repeated" % page_id, page_id))
            continue
        if _file_problem(file_value):
            faults.append(_fault(
                "input_unreadable", "page %r file is not a relative path" % page_id, page_id))
            continue
        file_key = posixpath.normpath(file_value)
        if file_key in seen_files:
            faults.append(_fault(
                "input_unreadable", "page %r repeats file %r" % (page_id, file_value), page_id))
            continue
        seen_files.add(file_key)
        if not absolute_with_host(url):
            faults.append(_fault(
                "input_url_not_absolute",
                "page %r url is not absolute: %r" % (page_id, url), page_id))
            continue
        url_norm = normalize_url(url)
        if url_norm in seen_urls:
            faults.append(_fault(
                "input_duplicate_url", "page %r repeats url %r" % (page_id, url), page_id))
            continue
        seen_urls.add(url_norm)
        seen_ids.add(page_id)
        pages.append({"index": len(pages), "id": page_id, "file": file_value,
                      "url": url, "url_norm": url_norm})
    return pages, faults, page_count


# --------------------------------------------------------------------------
# Page reading
# --------------------------------------------------------------------------

def _decode(data: bytes) -> str:
    """UTF-8 (BOM ignored), falling back to latin-1 so no page is unreadable."""
    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return data.decode("latin-1")


def read_page(root: str, page: dict):
    """Return (page, text) or (page, fault).

    A path that is absent, escapes ``--root`` after symlink resolution, a
    symlink, or not a regular file is ``input_unreadable`` (A15).
    """
    path = os.path.join(root, *page["file"].split("/"))
    real_root = os.path.realpath(root)
    real_path = os.path.realpath(path)
    try:
        inside = os.path.commonpath([real_root, real_path]) == real_root
    except ValueError:
        inside = False
    if not inside:
        detail = "page %r file escapes --root" % page["id"]
        return page, _fault("input_unreadable", detail, page["id"])
    try:
        info = os.lstat(path)
    except OSError as exc:
        detail = "page %r file unreadable (%s)" % (page["id"], exc.strerror)
        return page, _fault("input_unreadable", detail, page["id"])
    except ValueError:
        detail = "page %r file path is invalid" % page["id"]
        return page, _fault("input_unreadable", detail, page["id"])
    if not stat.S_ISREG(info.st_mode):
        detail = "page %r file is not a regular file" % page["id"]
        return page, _fault("input_unreadable", detail, page["id"])
    try:
        with open(path, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        detail = "page %r file unreadable (%s)" % (page["id"], exc.strerror)
        return page, _fault("input_unreadable", detail, page["id"])
    except ValueError:
        detail = "page %r file path is invalid" % page["id"]
        return page, _fault("input_unreadable", detail, page["id"])
    return page, _decode(data)


# --------------------------------------------------------------------------
# The audit
# --------------------------------------------------------------------------

def _add(store, page_index, finding_id, order, detail, page_id):
    store.append(
        {
            "id": finding_id,
            "severity": SEVERITY_OF[finding_id],
            "page": page_id,
            "detail": detail,
            "_key": (page_index, RANK[finding_id], order, detail),
        }
    )


def audit_pages(root: str, pages: list):
    """Return (page_objects, findings) for the manifest's valid pages.

    ``page_objects`` carries id/url/alternates/canonical for every page; a
    page that could not be read still appears (with no links) so reciprocity
    over the manifest does not silently drop a declared target, but it
    contributes no policy findings of its own (A8).
    """
    objects = []
    findings = []
    for spec in pages:
        spec, payload = read_page(root, spec)
        if isinstance(payload, dict):  # fault
            payload["_key"] = (-1, RANK[payload["id"]], spec["index"], payload["detail"])
            findings.append(payload)
            objects.append(
                {"index": spec["index"], "id": spec["id"], "url": spec["url"],
                 "url_norm": spec["url_norm"], "readable": False,
                 "alternates": [], "canonical": None}
            )
            continue
        alternates, canonical = _collect_links(payload)
        objects.append(
            {"index": spec["index"], "id": spec["id"], "url": spec["url"],
             "url_norm": spec["url_norm"], "readable": True,
             "alternates": alternates, "canonical": canonical}
        )

    url_index = {page["url_norm"]: page for page in objects}

    for page in objects:
        alts = page["alternates"]
        tagged = [alt for alt in alts if alt["tag"] != ""]
        # An absolute href is the only kind any comparison may use (A4).
        tagged_abs = [alt for alt in tagged if absolute_with_host(alt["href"])]
        page_id = page["id"]
        index = page["index"]

        # hreflang_missing_value: one per alternate element with no value.
        for alt in alts:
            if alt["tag"] == "":
                _add(findings, index, "hreflang_missing_value", alt["order"],
                     "alternate has no hreflang value (href=%s)" % _href_text(alt["href"]),
                     page_id)

        # hreflang_invalid_tag: one per alternate outside the frozen grammar.
        for alt in tagged:
            if not valid_bcp47(alt["tag"]):
                _add(findings, index, "hreflang_invalid_tag", alt["order"],
                     "hreflang %r is neither x-default nor BCP-47 under the frozen grammar"
                     % alt["tag"], page_id)

        # hreflang_relative_href: one per alternate href without scheme+host.
        for alt in alts:
            if not absolute_with_host(alt["href"]):
                _add(findings, index, "hreflang_relative_href", alt["order"],
                     "alternate href is not absolute with a host (href=%s)"
                     % _href_text(alt["href"]), page_id)

        # hreflang_duplicate_pair: one per repeat occurrence (A2); the tag is
        # lowercased, the href is exact after entity decoding.
        seen_pairs = {}
        for alt in tagged:
            key = (ascii_lower(alt["tag"]), alt["href"])
            occurrence = seen_pairs.get(key, 0) + 1
            seen_pairs[key] = occurrence
            if occurrence > 1:
                _add(findings, index, "hreflang_duplicate_pair", alt["order"],
                     "pair (tag=%s, href=%s) occurs again as occurrence %d"
                     % (key[0], _href_text(key[1]), occurrence), page_id)

        # hreflang_multiple_xdefault: one per x-default element on a page
        # that carries more than one (A2, one per offending annotation).
        xdefault = [alt for alt in tagged if ascii_lower(alt["tag"]) == "x-default"]
        if len(xdefault) > 1:
            for position, alt in enumerate(xdefault, start=1):
                _add(findings, index, "hreflang_multiple_xdefault", alt["order"],
                     "x-default %d of %d on one page" % (position, len(xdefault)),
                     page_id)

        # hreflang_self_missing: once per page (A2).  A non-absolute href is
        # not resolved and cannot satisfy the self-reference (A4).
        if tagged:
            if not any(normalize_url(alt["href"]) == page["url_norm"] for alt in tagged_abs):
                _add(findings, index, "hreflang_self_missing", -1,
                     "no absolute alternate equals the page's own url %s" % page["url"],
                     page_id)

        # hreflang_canonical_not_self: once per page (A2).  No canonical link
        # means the page is its own canonical (A5); the first canonical link
        # in document order is the page's canonical (A6), with or without
        # hreflang (A7).  A non-absolute canonical href contributes to no
        # finding (A4).
        canonical = page["canonical"]
        if tagged and canonical is not None and absolute_with_host(canonical["href"]):
            if normalize_url(canonical["href"]) != page["url_norm"]:
                _add(findings, index, "hreflang_canonical_not_self", -1,
                     "canonical %s is not the page url %s"
                     % (canonical["href"], page["url"]), page_id)

        # hreflang_nonreciprocal / hreflang_external_target: one per absolute
        # annotation (A2).  Non-absolute hrefs are not resolved (A4).
        for alt in tagged_abs:
            target_key = normalize_url(alt["href"])
            target = url_index.get(target_key)
            if target is None:
                _add(findings, index, "hreflang_external_target", alt["order"],
                     "target %s (tag=%s) is outside the manifest"
                     % (alt["href"], alt["tag"]), page_id)
                continue
            wanted = ascii_lower(alt["tag"])
            reciprocal = False
            for back in target["alternates"]:
                if back["tag"] == "" or ascii_lower(back["tag"]) != wanted:
                    continue
                if not absolute_with_host(back["href"]):
                    continue
                if normalize_url(back["href"]) == page["url_norm"]:
                    reciprocal = True
                    break
            if not reciprocal:
                _add(findings, index, "hreflang_nonreciprocal", alt["order"],
                     "target %s declares no return alternate for tag=%s to %s"
                     % (target["url"], alt["tag"], page["url"]), page_id)

    return objects, findings


def _href_text(value) -> str:
    return "<absent>" if value is None else repr(value)


# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------

def build_document(page_count: int, findings: list, exit_code: int):
    policy = sum(1 for item in findings if item["severity"] == "policy")
    info = sum(1 for item in findings if item["severity"] == "info")
    inputs = sum(1 for item in findings if item["severity"] == "input")
    by_id = {name: 0 for name in FINDING_ORDER}
    for item in findings:
        by_id[item["id"]] += 1
    return {
        "version": OUTPUT_VERSION,
        "pages": page_count,
        "findings": [
            {"id": item["id"], "severity": item["severity"], "page": item["page"],
             "detail": item["detail"]}
            for item in findings
        ],
        "counts": {
            "policy": policy,
            "info": info,
            "input": inputs,
            "by_id": by_id,
        },
        "exit": exit_code,
    }


def _sorted_findings(findings: list) -> list:
    return sorted(list({(item["id"], item["page"]): item for item in reversed(findings)}.values()), key=lambda item: item.get("_key", (10 ** 9, 10 ** 9, 0, "")))


def _usage_emit(message: str, as_json: bool, page_count: int = 0) -> int:
    """Exit 64.  With --json still print the required document shape (A16)."""
    sys.stderr.write("hreflang_audit.py: %s\n%s" % (message, USAGE_LINE))
    if as_json:
        sys.stdout.write(json.dumps(build_document(page_count, [], EXIT_USAGE),
                                    ensure_ascii=True) + "\n")
        sys.stdout.flush()
    return EXIT_USAGE


def run_audit(manifest_path: str, root: str, as_json: bool) -> int:
    document, error = _read_manifest(manifest_path)
    if error is not None:
        findings = [_fault("input_unreadable", error)]
        findings[0]["_key"] = (-1, RANK["input_unreadable"], -1, error)
        ordered = _sorted_findings(findings)
        return _emit(build_document(0, ordered, EXIT_INPUT), as_json)

    raw_pages = document.get("pages") if isinstance(document, dict) else None
    candidate_count = len(raw_pages) if isinstance(raw_pages, list) else 0
    try:
        pages, manifest_faults, page_count = validate_manifest(document)
    except ManifestVersionError as exc:
        return _usage_emit(str(exc), as_json, candidate_count)

    findings = []
    for offset, item in enumerate(manifest_faults):
        item["_key"] = (-1, RANK[item["id"]], offset, item["detail"])
        findings.append(item)
    _objects, page_findings = audit_pages(root, pages)
    findings.extend(page_findings)
    ordered = _sorted_findings(findings)
    has_input = any(item["severity"] == "input" for item in ordered)
    has_policy = any(item["severity"] == "policy" for item in ordered)
    exit_code = EXIT_INPUT if has_input else (EXIT_POLICY if has_policy else EXIT_CLEAN)
    return _emit(build_document(page_count, ordered, exit_code), as_json)


def _emit(document: dict, as_json: bool) -> int:
    if as_json:
        sys.stdout.write(json.dumps(document, ensure_ascii=True) + "\n")
        sys.stdout.flush()
        return document["exit"]
    for item in document["findings"]:
        page = item["page"] if item["page"] is not None else "-"
        sys.stdout.write("%s page=%s %s\n" % (item["id"], page, item["detail"]))
    counts = document["counts"]
    sys.stdout.write(
        "pages=%d findings=%d policy=%d info=%d input=%d exit=%d\n"
        % (document["pages"], len(document["findings"]), counts["policy"],
           counts["info"], counts["input"], document["exit"])
    )
    sys.stdout.flush()
    return document["exit"]


# --------------------------------------------------------------------------
# Self test
# --------------------------------------------------------------------------

def _manifest(*pages) -> dict:
    return {
        "version": 1,
        "pages": [
            {"id": page_id, "file": file_name, "url": url}
            for page_id, file_name, url in pages
        ],
    }


def _html(*links) -> str:
    return "<!doctype html>\n<html><head>\n" + "\n".join(links) + "\n</head><body></body></html>\n"


def _alt(tag, href) -> str:
    if tag is None:
        return '<link rel="alternate" href="%s">' % href
    return '<link rel="alternate" hreflang="%s" href="%s">' % (tag, href)


def _canonical(href) -> str:
    return '<link rel="canonical" href="%s">' % href


A = "https://a.example/"
A_DIR = "https://a.example/dir/"
B = "https://b.example/"
C = "https://c.example/"
EXT = "https://ext.example/"


def _pair_pages():
    """A clean reciprocal pair: both pages list themselves and each other."""
    return {
        "a.html": _html(_canonical(A), _alt("en", A), _alt("en", B)),
        "b.html": _html(_canonical(B), _alt("en", A), _alt("en", B)),
    }


CASES = []


def _case(name, manifest, files, expect_exit, expect_ids, *, symlinks=None,
          external_dirs=None, manifest_raw=None, expect_pages=None):
    if expect_pages is None:
        raw = manifest.get("pages") if isinstance(manifest, dict) else None
        expect_pages = len(raw) if isinstance(raw, list) else 0
    CASES.append(
        {
            "name": name,
            "manifest": manifest,
            "manifest_raw": manifest_raw,
            "files": files,
            "symlinks": symlinks or {},
            "external_dirs": external_dirs or {},
            "expect_exit": expect_exit,
            "expect_ids": tuple(sorted(expect_ids)),
            "expect_pages": expect_pages,
        }
    )


def _build_cases():
    if CASES:
        return
    # --- clean baselines -------------------------------------------------
    _case(
        "clean_pair",
        _manifest(("a", "a.html", A), ("b", "b.html", B)),
        _pair_pages(), EXIT_CLEAN, (),
    )
    _case(
        "clean_single",
        _manifest(("a", "a.html", A)),
        {"a.html": _html(_canonical(A), _alt("en", A))}, EXIT_CLEAN, (),
    )

    # --- hreflang_missing_value -----------------------------------------
    _case(
        "missing_value_red",
        _manifest(("a", "a.html", A)),
        {"a.html": _html(_canonical(A), _alt(None, A))},
        EXIT_POLICY, ["hreflang_missing_value"],
    )
    _case(
        "missing_value_empty_red",
        _manifest(("a", "a.html", A)),
        {"a.html": _html(_canonical(A), _alt("", A))},
        EXIT_POLICY, ["hreflang_missing_value"],
    )
    _case(
        "missing_value_green",
        _manifest(("a", "a.html", A)),
        {"a.html": _html(_canonical(A), _alt("en", A))}, EXIT_CLEAN, (),
    )

    # --- hreflang_invalid_tag -------------------------------------------
    _case(
        "invalid_tag_red",
        _manifest(("a", "a.html", A)),
        {"a.html": _html(_canonical(A), _alt("en_GB", A))},
        EXIT_POLICY, ["hreflang_invalid_tag"],
    )
    _case(
        "invalid_tag_corners_red",
        _manifest(("a", "a.html", A)),
        {"a.html": _html(
            _canonical(A),
            _alt("e", A), _alt("engl", A), _alt("en--GB", A), _alt("419", A),
            _alt("en-GB-", A),
        )},
        EXIT_POLICY, ["hreflang_invalid_tag"] * 5,
    )
    _case(
        "invalid_tag_padded_red",
        _manifest(("a", "a.html", A)),
        {"a.html": _html(_canonical(A), _alt(" en ", A), _alt("en", A))},
        EXIT_POLICY, ["hreflang_invalid_tag"],
    )
    _case(
        "grammar_valid_green",
        _manifest(("a", "a.html", A)),
        {"a.html": _html(
            _canonical(A),
            _alt("en", A), _alt("en-GB", A), _alt("zh-Hant", A),
            _alt("zh-Hant-TW", A), _alt("es-419", A), _alt("de-CH-1901", A),
            _alt("x-default", A),
        )},
        EXIT_CLEAN, (),
    )
    _case(
        "grammar_case_green",
        _manifest(("a", "a.html", A)),
        {"a.html": _html(_canonical(A), _alt("EN-gb", A), _alt("X-DEFAULT", A))},
        EXIT_CLEAN, (),
    )

    # --- hreflang_relative_href ------------------------------------------
    _case(
        "relative_href_red",
        _manifest(("a", "a.html", A_DIR)),
        {"a.html": _html(_canonical(A_DIR), _alt("en", "/dir/"), _alt("en", A_DIR))},
        EXIT_POLICY, ["hreflang_relative_href"],
    )
    _case(
        "relative_href_scheme_relative_red",
        _manifest(("a", "a.html", A)),
        {"a.html": _html(_canonical(A), _alt("en", A), _alt("en", "//b.example/"))},
        EXIT_POLICY, ["hreflang_relative_href"],
    )
    _case(
        "no_href_ignored_green",
        _manifest(("a", "a.html", A)),
        {"a.html": _html(_canonical(A), '<link rel="alternate" hreflang="en">',
                         _alt("en", A))},
        EXIT_CLEAN, (),
    )
    _case(
        "mailto_relative_red",
        _manifest(("a", "a.html", A)),
        {"a.html": _html(_canonical(A), _alt("en", A), _alt("en", "mailto:x@example.com"))},
        EXIT_POLICY, ["hreflang_relative_href"],
    )
    _case(
        "empty_href_relative_red",
        _manifest(("a", "a.html", A)),
        {"a.html": _html(_canonical(A), _alt("en", A), _alt("en", ""))},
        EXIT_POLICY, ["hreflang_relative_href"],
    )

    # --- hreflang_duplicate_pair -----------------------------------------
    _case(
        "duplicate_pair_red",
        _manifest(("a", "a.html", A)),
        {"a.html": _html(_canonical(A), _alt("en", A), _alt("EN", A))},
        EXIT_POLICY, ["hreflang_duplicate_pair"],
    )
    _case(
        "duplicate_pair_three_red",
        _manifest(("a", "a.html", A)),
        {"a.html": _html(_canonical(A), _alt("en", A), _alt("en", A), _alt("en", A))},
        EXIT_POLICY, ["hreflang_duplicate_pair"] * 2,
    )
    _case(
        "duplicate_pair_green",
        _manifest(("a", "a.html", A)),
        {"a.html": _html(_canonical(A), _alt("en", A), _alt("fr", A))},
        EXIT_CLEAN, (),
    )

    # --- hreflang_multiple_xdefault --------------------------------------
    two_x = _html(
        _canonical(A),
        _alt("x-default", A), _alt("x-default", B), _alt("en", A), _alt("en", B),
    )
    two_x_b = _html(
        _canonical(B),
        _alt("x-default", A), _alt("x-default", B), _alt("en", A), _alt("en", B),
    )
    _case(
        "multiple_xdefault_red",
        _manifest(("a", "a.html", A), ("b", "b.html", B)),
        {"a.html": two_x, "b.html": two_x_b},
        EXIT_POLICY, ["hreflang_multiple_xdefault"] * 4,
    )
    _case(
        "multiple_xdefault_three_red",
        _manifest(("a", "a.html", A)),
        {"a.html": _html(
            _canonical(A),
            _alt("x-default", A), _alt("x-default", A), _alt("x-default", A),
            _alt("en", A),
        )},
        EXIT_POLICY, ["hreflang_multiple_xdefault"] * 3
                     + ["hreflang_duplicate_pair"] * 2,
    )
    _case(
        "multiple_xdefault_green",
        _manifest(("a", "a.html", A), ("b", "b.html", B)),
        {"a.html": _html(_canonical(A), _alt("x-default", A), _alt("en", A)),
         "b.html": _html(_canonical(B))},
        EXIT_CLEAN, (),
    )

    # --- hreflang_self_missing -------------------------------------------
    _case(
        "self_missing_red",
        _manifest(("a", "a.html", A), ("b", "b.html", B)),
        {"a.html": _html(_canonical(A), _alt("en", B)),
         "b.html": _html(_canonical(B), _alt("en", A))},
        EXIT_POLICY, ["hreflang_self_missing"] * 2,
    )
    _case(
        "self_missing_normalized_green",
        _manifest(("a", "a.html", "https://A.example:443/x/./y/")),
        {"a.html": _html(
            _canonical("HTTPS://a.example/x/y/"),
            _alt("en", "https://a.example/x/y/"),
        )},
        EXIT_CLEAN, (),
    )
    _case(
        "self_trailing_slash_red",
        _manifest(("a", "a.html", "https://a.example/x/")),
        {"a.html": _html(_canonical("https://a.example/x/"),
                         _alt("en", "https://a.example/x"))},
        EXIT_POLICY, ["hreflang_self_missing", "hreflang_external_target"],
    )

    # --- hreflang_nonreciprocal ------------------------------------------
    _case(
        "nonreciprocal_red",
        _manifest(("a", "a.html", A), ("b", "b.html", B)),
        {"a.html": _html(_canonical(A), _alt("en", A), _alt("en", B)),
         "b.html": _html(_canonical(B))},
        EXIT_POLICY, ["hreflang_nonreciprocal"],
    )
    _case(
        "nonreciprocal_tag_mismatch_red",
        _manifest(("a", "a.html", A), ("b", "b.html", B)),
        {"a.html": _html(_canonical(A), _alt("en", A), _alt("en", B)),
         "b.html": _html(_canonical(B), _alt("fr", A), _alt("fr", B))},
        EXIT_POLICY, ["hreflang_nonreciprocal"] * 2,
    )
    _case(
        "nonreciprocal_cycle_red",
        _manifest(("a", "a.html", A), ("b", "b.html", B), ("c", "c.html", C)),
        {"a.html": _html(_canonical(A), _alt("en", A), _alt("en", B)),
         "b.html": _html(_canonical(B), _alt("en", B), _alt("en", C)),
         "c.html": _html(_canonical(C), _alt("en", C), _alt("en", A))},
        EXIT_POLICY, ["hreflang_nonreciprocal"] * 3,
    )
    _case(
        "external_target_info_red",
        _manifest(("a", "a.html", A)),
        {"a.html": _html(_canonical(A), _alt("en", A), _alt("en", EXT))},
        EXIT_CLEAN, ["hreflang_external_target"],
    )

    # --- hreflang_canonical_not_self -------------------------------------
    _case(
        "canonical_not_self_red",
        _manifest(("a", "a.html", A), ("b", "b.html", B)),
        {"a.html": _html(_canonical(B), _alt("en", A)),
         "b.html": _html(_canonical(B), _alt("en", B))},
        EXIT_POLICY, ["hreflang_canonical_not_self"],
    )
    _case(
        "canonical_absent_green",
        _manifest(("a", "a.html", A)),
        {"a.html": _html(_alt("en", A))}, EXIT_CLEAN, (),
    )
    _case(
        "canonical_first_wins_green",
        _manifest(("a", "a.html", A), ("b", "b.html", B)),
        {"a.html": _html(_canonical(A), _canonical(B), _alt("en", A)),
         "b.html": _html(_canonical(B))},
        EXIT_CLEAN, (),
    )
    _case(
        "canonical_relative_no_finding_green",
        _manifest(("a", "a.html", A_DIR)),
        {"a.html": _html(_canonical("../dir/"), _alt("en", A_DIR))},
        EXIT_CLEAN, (),
    )
    _case(
        "canonical_with_hreflang_green",
        _manifest(("a", "a.html", A)),
        {"a.html": _html(
            '<link rel="canonical" hreflang="en" href="https://a.example/">',
            _alt("en", A),
        )},
        EXIT_CLEAN, (),
    )

    # --- input faults -----------------------------------------------------
    _case(
        "input_missing_file",
        _manifest(("a", "missing.html", A)),
        {"other.html": ""}, EXIT_INPUT, ["input_unreadable"],
    )
    _case(
        "input_file_escape",
        _manifest(("a", "../escape.html", A)),
        {"a.html": ""}, EXIT_INPUT, ["input_unreadable"],
    )
    _case(
        "input_duplicate_url",
        _manifest(("a", "a.html", A), ("b", "b.html", A)),
        {"a.html": "", "b.html": ""}, EXIT_INPUT, ["input_duplicate_url"],
    )
    _case(
        "input_duplicate_url_normalized",
        _manifest(("a", "a.html", "https://a.example:443/x/./y"),
                  ("b", "b.html", "https://a.example/x/y")),
        {"a.html": "", "b.html": ""}, EXIT_INPUT, ["input_duplicate_url"],
    )
    _case(
        "input_duplicate_file",
        _manifest(("a", "same.html", A), ("b", "same.html", B)),
        {"same.html": ""}, EXIT_INPUT, ["input_unreadable"],
    )
    _case(
        "input_url_relative",
        _manifest(("a", "a.html", "/rel")),
        {"a.html": ""}, EXIT_INPUT, ["input_url_not_absolute"],
    )
    _case(
        "input_symlink_page",
        _manifest(("a", "link.html", A)),
        {"a.html": _html(_canonical(A), _alt("en", A))},
        EXIT_INPUT, ["input_unreadable"],
        symlinks={"link.html": "a.html"},
    )
    _case(
        "input_parent_symlink_escape",
        _manifest(("a", "out/page.html", A)),
        {},
        EXIT_INPUT, ["input_unreadable"],
        symlinks={"out": "../outside"},
        external_dirs={"outside": {"page.html": _html(_canonical(A), _alt("en", A))}},
    )
    _case(
        "input_bad_json",
        None, {}, EXIT_INPUT, ["input_unreadable"],
        manifest_raw="{not json\n",
    )
    _case(
        "input_version_2",
        {"version": 2, "pages": [{"id": "a", "file": "a.html", "url": A}]},
        {"a.html": ""}, EXIT_USAGE, [],
    )
    _case(
        "mixed_fault_and_policy",
        _manifest(("a", "a.html", A), ("b", "missing.html", B)),
        {"a.html": _html(_canonical(A), _alt("en_GB", A))},
        EXIT_INPUT, ["hreflang_invalid_tag", "input_unreadable"],
    )

    # --- parser corners ---------------------------------------------------
    _case(
        "parser_comment_and_bodies_green",
        _manifest(("a", "a.html", A)),
        {"a.html": (
            "<!doctype html><html><head>\n"
            "<!-- <link rel=\"alternate\" href=\"https://a.example/\"> -->\n"
            "<script>var s = '<link rel=\"alternate\" href=\"https://a.example/\">';</script>\n"
            "<style>/* <link rel=alternate href=\"https://a.example/\"> */</style>\n"
            "<template><link rel=\"alternate\" href=\"https://a.example/\"></template>\n"
            + _canonical(A) + "\n" + _alt("en", A) +
            "\n</head></html>\n"
        )},
        EXIT_CLEAN, (),
    )
    _case(
        "parser_svg_math_skipped_green",
        _manifest(("a", "a.html", A)),
        {"a.html": (
            "<!doctype html><html><head>\n"
            "<svg><link rel=\"alternate\" href=\"https://a.example/\"></svg>\n"
            "<math><link rel=\"alternate\" href=\"https://a.example/\"></math>\n"
            + _canonical(A) + "\n" + _alt("en", A) +
            "\n</head></html>\n"
        )},
        EXIT_CLEAN, (),
    )
    _case(
        "parser_svg_selfclose_green",
        _manifest(("a", "a.html", A)),
        {"a.html": _html("<svg/>", _canonical(A), _alt("en", A))},
        EXIT_CLEAN, (),
    )
    _case(
        "parser_attr_order_quotes_green",
        _manifest(("a", "a.html", A)),
        {"a.html": _html(
            "<link HREF='https://a.example/' REL=alternate hreflang=en />",
            _canonical(A),
        )},
        EXIT_CLEAN, (),
    )
    _case(
        "structure_rel_uppercase_red",
        _manifest(("a", "a.html", A)),
        {"a.html": _html(
            '<link REL="ALTERNATE" HREFLANG="en_US" HREF="https://a.example/">',
            _canonical(A),
        )},
        EXIT_POLICY, ["hreflang_invalid_tag"],
    )
    _case(
        "structure_rel_mixedcase_green",
        _manifest(("a", "a.html", A)),
        {"a.html": _html(
            '<link rel="Alternate" hreflang="en" href="https://a.example/">',
            _canonical(A),
        )},
        EXIT_CLEAN, (),
    )
    _case(
        "parser_entity_decode_green",
        _manifest(("a", "a.html", "https://a.example/?x=1&y=2")),
        {"a.html": _html(
            '<link rel="canonical" href="https://a.example/?x=1&amp;y=2">',
            '<link rel="alternate" hreflang="en&#45;GB" '
            'href="https://a.example/?x=1&amp;y=2">',
        )},
        EXIT_CLEAN, (),
    )
    _case(
        "parser_first_attribute_wins_green",
        _manifest(("a", "a.html", A)),
        {"a.html": _html(
            '<link rel="canonical" rel="alternate" hreflang="en" href="https://a.example/">',
            _alt("en", A),
        )},
        EXIT_CLEAN, (),
    )
    _case(
        "parser_stray_lt_green",
        _manifest(("a", "a.html", A)),
        {"a.html": "<!doctype html><html><body>if (a < b) { c < 3; }</body>"
                   + _canonical(A) + _alt("en", A) + "</html>"},
        EXIT_CLEAN, (),
    )
    _case(
        "parser_script_selfclose_green",
        _manifest(("a", "a.html", A)),
        {"a.html": (
            "<!doctype html><html><head><script/>var s = "
            "'<link rel=\"alternate\" href=\"https://a.example/\">';</script>\n"
            + _canonical(A) + "\n" + _alt("en", A) + "\n</head></html>\n"
        )},
        EXIT_CLEAN, (),
    )
    _case(
        "alternate_stylesheet_green",
        _manifest(("a", "a.html", A)),
        {"a.html": _html(
            _canonical(A), _alt("en", A),
            '<link rel="alternate stylesheet" title="wide" href="https://a.example/w.css">',
        )},
        EXIT_CLEAN, (),
    )
    _case(
        "parser_noscript_scanned_red",
        _manifest(("a", "a.html", A)),
        {"a.html": "<!doctype html><html><head>" + _canonical(A) + _alt("en", A)
                   + "</head><body><noscript>"
                   + '<link rel="alternate" href="https://a.example/blog/">'
                   + "</noscript></body></html>"},
        EXIT_POLICY, ["hreflang_missing_value"],
    )


def _write_case(root: str, case: dict) -> str:
    for dirname, contents in case["external_dirs"].items():
        target_dir = os.path.join(root, dirname)
        os.makedirs(target_dir, exist_ok=True)
        for name, content in contents.items():
            with open(os.path.join(target_dir, name), "w",
                      encoding="utf-8", newline="\n") as handle:
                handle.write(content)
    case_dir = os.path.join(root, case["name"])
    os.makedirs(case_dir, exist_ok=True)
    for name, content in case["files"].items():
        with open(os.path.join(case_dir, name), "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
    for link_name, target in case["symlinks"].items():
        os.symlink(target, os.path.join(case_dir, link_name))
    manifest_path = os.path.join(case_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8", newline="\n") as handle:
        if case.get("manifest_raw") is not None:
            handle.write(case["manifest_raw"])
        else:
            json.dump(case["manifest"], handle)
            handle.write("\n")
    return case_dir


def _run_tool(manifest_path: str, root: str):
    argv = [sys.executable, "-B", os.path.realpath(__file__),
            "--manifest", manifest_path, "--root", root, "--json"]
    proc = subprocess.run(
        argv, capture_output=True, text=True, timeout=120,
        cwd=root, env=dict(os.environ),
    )
    return proc


def _compare(expected_exit: int, expected_ids, expect_pages: int, proc) -> tuple:
    """Return (ok, detail) comparing one process result to an expectation."""
    if proc.returncode != expected_exit:
        return False, "exit expected %d got %d" % (expected_exit, proc.returncode)
    try:
        document = json.loads(proc.stdout)
    except (json.JSONDecodeError, ValueError):
        return False, "stdout is not JSON: %r" % proc.stdout[:200]
    if set(document) != {"version", "pages", "findings", "counts", "exit"}:
        return False, "JSON keys are %r" % sorted(document)
    if document["exit"] != proc.returncode:
        return False, "JSON exit %r != process exit %d" % (document["exit"], proc.returncode)
    if document["pages"] != expect_pages:
        return False, "pages expected %r got %r" % (expect_pages, document["pages"])
    for item in document["findings"]:
        if set(item) != {"id", "severity", "page", "detail"}:
            return False, "finding keys are %r" % sorted(item)
        if item["severity"] != SEVERITY_OF.get(item["id"]):
            return False, "severity %r for id %r" % (item["severity"], item["id"])
    observed = sorted(item["id"] for item in document["findings"])
    if observed != sorted(expected_ids):
        return False, "ids expected %r got %r" % (sorted(expected_ids), observed)
    counts = document["counts"]
    if set(counts) != {"policy", "info", "input", "by_id"}:
        return False, "counts keys are %r" % sorted(counts)
    if (counts["policy"] + counts["info"] + counts["input"]) != len(document["findings"]):
        return False, "severity counts do not sum to the finding count"
    if set(counts["by_id"]) != set(FINDING_ORDER):
        return False, "by_id keys are not the frozen id set"
    if sum(counts["by_id"].values()) != len(document["findings"]):
        return False, "by_id counts do not sum to the finding count"
    for name in FINDING_ORDER:
        if counts["by_id"][name] != observed.count(name):
            return False, "by_id[%r] is wrong" % name
    return True, ""


def run_selftest(work: str) -> int:
    _build_cases()
    work = os.path.abspath(work)
    if os.path.exists(work) and not os.path.isdir(work):
        sys.stderr.write("--work is not a directory: %s\n" % work)
        return EXIT_USAGE
    os.makedirs(work, exist_ok=True)
    case_root = tempfile.mkdtemp(prefix="hreflang-selftest-", dir=work)
    total = 0
    passed = 0
    try:
        for case in CASES:
            total += 1
            case_dir = _write_case(case_root, case)
            proc = _run_tool(os.path.join(case_dir, "manifest.json"), case_dir)
            ok, detail = _compare(case["expect_exit"], case["expect_ids"],
                                  case["expect_pages"], proc)
            if ok:
                passed += 1
            else:
                sys.stderr.write("FAIL %s: %s\n" % (case["name"], detail))

        # Harness checks: the comparator must be able to fail, the JSON shape
        # must hold, and repeated runs must be byte-identical.
        total += 1
        case_dir = _write_case(case_root, {
            "name": "harness_clean_repeat",
            "manifest": _manifest(("a", "a.html", A), ("b", "b.html", B)),
            "manifest_raw": None,
            "files": _pair_pages(),
            "symlinks": {},
            "external_dirs": {},
        })
        first = _run_tool(os.path.join(case_dir, "manifest.json"), case_dir)
        second = _run_tool(os.path.join(case_dir, "manifest.json"), case_dir)
        if first.returncode == 0 and first.stdout == second.stdout:
            passed += 1
        else:
            sys.stderr.write("FAIL harness_determinism: outputs differ or exit %d\n"
                             % first.returncode)

        total += 1
        ok, _detail = _compare(EXIT_CLEAN, ("never_emitted",), 2, first)
        if not ok:
            passed += 1
        else:
            sys.stderr.write("FAIL harness_comparator: wrong expectation accepted\n")

        total += 1
        try:
            document = json.loads(first.stdout)
            shape_ok = (
                set(document) == {"version", "pages", "findings", "counts", "exit"}
                and document["version"] == 1
                and document["pages"] == 2
                and document["counts"]["policy"] == 0
                and document["counts"]["info"] == 0
                and document["counts"]["input"] == 0
                and document["exit"] == 0
            )
        except (json.JSONDecodeError, ValueError, KeyError, TypeError):
            shape_ok = False
        if shape_ok:
            passed += 1
        else:
            sys.stderr.write("FAIL harness_shape: JSON document shape is wrong\n")
    finally:
        shutil.rmtree(case_root, ignore_errors=True)

    sys.stdout.write("selftest %d/%d passed\n" % (passed, total))
    sys.stdout.flush()
    return EXIT_CLEAN if passed == total else EXIT_POLICY


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

class _OnceAction(argparse.Action):
    """Reject a repeated option instead of silently keeping the last value."""

    def __call__(self, parser, namespace, values, option_string=None):
        if getattr(namespace, self.dest, None) is not None:
            raise UsageError("%s may be given only once" % option_string)
        setattr(namespace, self.dest, values)


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise UsageError(message)


def _parse_argv(argv):
    parser = _Parser(
        prog="hreflang_audit.py",
        usage="hreflang_audit.py --manifest PATH [--root DIR] [--json] | "
              "hreflang_audit.py --selftest --work DIR",
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
            if args.json:
                raise UsageError("--selftest does not take --json")
            if args.work is None:
                raise UsageError("--selftest requires --work")
            return run_selftest(args.work)
        if args.manifest is None:
            raise UsageError("--manifest is required")
        root = os.path.abspath(args.root if args.root is not None else os.getcwd())
        return run_audit(args.manifest, root, args.json)
    except UsageError as exc:
        sys.stderr.write("hreflang_audit.py: %s\n%s" % (exc, USAGE_LINE))
        return EXIT_USAGE
    except BrokenPipeError:
        return EXIT_USAGE


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
