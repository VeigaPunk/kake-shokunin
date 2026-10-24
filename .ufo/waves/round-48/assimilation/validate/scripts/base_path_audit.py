#!/usr/bin/env python3
"""Offline static base-path audit for project-site pages.

A GitHub Pages project site is served under a base path, for example
https://owner.github.io/repo/, so a root-relative reference such as
/style.css leaves the site. This tool reads a manifest that names local HTML
pages and reports every reference whose resolved URL falls outside the
configured base path. It never opens a network connection and never writes to
disk.

What this tool checks
---------------------
Static HTML source only. The reference set is a/area/link[href],
img/script/iframe/source/audio/video/track/embed[src], img/source[srcset]
(each candidate URL), video[poster] and form[action]. The first <base>
element that carries an href attribute sets the document base for every
reference on that page. A <base> element is not itself a reference and is
never reported.

What this tool does NOT check
-----------------------------
* the rendered DOM: the source is read with html.parser, not with a browser
  tree builder, so markup that only exists after tree construction is not
  seen;
* JavaScript-built URLs: values assigned at run time are invisible here;
* CSS url() references, including @import rules and font files;
* <meta http-equiv="refresh"> redirections;
* HTTP redirects, response headers, status codes, any live serving
  behaviour, and whether a target actually exists;
* <noscript> fallbacks are scanned as ordinary markup, because this tool has
  no scripting model;
* <template> contents are NOT scanned: a browser does not fetch resources
  inside template content, so such references are deliberately not reported.
* other URL-bearing attributes: formaction, object[data], input[type=image]
  src, SVG href, frame src and link imagesrcset are not read;
* known resolution gaps found in round-29 falsification (WHATWG via Node as
  reference): a cross-scheme reference without "//" (http:host/path on an
  https page), percent-encoded or non-ASCII host spellings, and an
  unparseable base element are treated as not on this site, so they can be
  missed; srcset density descriptors are read with a narrower grammar than
  the HTML parser (for example ".5x" drops the candidate);
* the finding "page" field is the page URL from the manifest; the page file
  name is the prefix of the finding id. Input findings use the reason as id.
* tokenizer edges where html.parser differs from a browser (round-29
  wave-2 HtmlParsingEdges, parse5 and Chromium as reference): a base element
  inside SVG is taken as the document base, CDATA outside SVG hides later
  markup, <image src> is not mapped to img, and a self-closed <script/>,
  script double-escape text or <template/> can make enclosed text count as
  references. These can cause both misses and false findings.

Reference resolution follows browser behaviour rather than bare RFC 3986:
hosts compare case-insensitively, default ports are normalized, http and
https on the same host are the same site, backslashes act as slashes for
HTTP(S) URLs, and dot segments are removed from absolute and
protocol-relative URLs as well (with %2e treated as a dot).

Exit codes: 0 clean, 1 failed-policy, 2 could-not-evaluate, 64 usage.
"""
from __future__ import annotations

import argparse
import json
import ntpath
import os
import re
import stat
import sys
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit

MAX_MANIFEST_BYTES = 1024 * 1024
MAX_HTML_BYTES = 2 * 1024 * 1024
READ_CHUNK_BYTES = 64 * 1024
MAX_JSON_DEPTH = 64

EXIT_CLEAN = 0
EXIT_POLICY = 1
EXIT_INPUT = 2
EXIT_USAGE = 64

REASON_OUTSIDE = "outside_base_path"
REASON_INPUT = "input_invalid"
REASON_PAGE_OUTSIDE = "page_outside_base_path"
INPUT_REASONS = {REASON_INPUT, REASON_PAGE_OUTSIDE}

ASCII_WS = " \t\n\r\f"
SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.\-]*:")
SRCSET_WIDTH_RE = re.compile(r"^[0-9]+w$")
SRCSET_DENSITY_RE = re.compile(r"^[0-9]+(?:\.[0-9]+)?x$")

# Ordered so that the occurrence index carried in a finding id is stable.
REFERENCE_ATTRIBUTES = (
    ("a", "href"),
    ("area", "href"),
    ("link", "href"),
    ("form", "action"),
    ("img", "src"),
    ("img", "srcset"),
    ("script", "src"),
    ("iframe", "src"),
    ("source", "src"),
    ("source", "srcset"),
    ("audio", "src"),
    ("video", "src"),
    ("video", "poster"),
    ("track", "src"),
    ("embed", "src"),
)

USAGE_RESULT = {
    "verdict": "could-not-evaluate",
    "pagesChecked": 0,
    "referencesChecked": 0,
    "findings": [],
}


class UsageError(Exception):
    """Invalid command-line shape."""


class InputProblem(Exception):
    """Manifest or referenced file could not be safely evaluated."""


class BasePathArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise UsageError(message)


class SingleManifestAction(argparse.Action):
    """Reject a repeated --manifest instead of silently keeping the last path."""

    def __call__(self, parser, namespace, values, option_string=None) -> None:
        if getattr(namespace, self.dest, None) is not None:
            raise UsageError("--manifest may be given only once")
        setattr(namespace, self.dest, values)


USAGE_LINE = "base_path_audit.py --manifest PATH"

DETAILS = (
    "--help prints standard CLI help, exits 0, and emits no verdict.\n"
    "\n"
    "Read UTF-8 JSON manifest v1 and bounded local UTF-8 HTML only.\n"
    "The manifest is {version:1, basePath:'/…/', pages:[{file, url}]}.\n"
    "basePath starts and ends with '/'; page files are relative to the\n"
    "manifest directory; absolute paths, traversal, symlinks, and\n"
    "non-regular files are rejected. The manifest limit is 1 MiB; each\n"
    "HTML file is limited to 2 MiB. No network access or writes occur.\n"
    "\n"
    "Checked references: a/area/link[href], img/script/iframe/source/\n"
    "audio/video/track/embed[src], img/source[srcset], video[poster],\n"
    "form[action]. The first base element with href sets the document\n"
    "base; the base element itself is not a reference. Values that are\n"
    "empty after stripping ASCII whitespace, use a non-HTTP(S) scheme, or\n"
    "point at another site are ignored. Same site means the same host\n"
    "(case-insensitive) and the same port after default ports are folded;\n"
    "http and https on one host count as the same site, so a cross-scheme\n"
    "reference is still checked against the base path.\n"
    "\n"
    "Except --help, stdout is always one JSON object: verdict,\n"
    "pagesChecked, referencesChecked, findings. Each finding carries id,\n"
    "reason, page, element, attribute, value, resolved.\n"
    "Exit: 0 clean; 1 failed-policy; 2 could-not-evaluate; 64 usage.\n"
)


def usage() -> str:
    return f"usage: {USAGE_LINE}\n{DETAILS}"


def parse_cli(argv: list[str]) -> argparse.Namespace:
    parser = BasePathArgumentParser(
        prog="base_path_audit.py",
        usage=USAGE_LINE,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=True,
        allow_abbrev=False,
        description=DETAILS,
    )
    parser.add_argument("--manifest", metavar="PATH", action=SingleManifestAction)
    args = parser.parse_args(argv)
    if args.manifest is None:
        raise UsageError("--manifest PATH is required")
    return args


def ascii_lower(value: str) -> str:
    return value.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"))


def attrs_first_wins(attrs: list[tuple[str, str | None]]) -> dict[str, str | None]:
    result: dict[str, str | None] = {}
    for name, value in attrs:
        result.setdefault(ascii_lower(name), value)
    return result


def strict_json(raw: bytes) -> object:
    """Parse JSON with duplicate keys, non-finite numbers and depth refused."""
    text = raw.decode("utf-8-sig", errors="strict")
    depth = 0
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char in "{[":
            depth += 1
            if depth > MAX_JSON_DEPTH:
                raise ValueError(f"JSON nesting exceeds local depth limit {MAX_JSON_DEPTH}")
        elif char in "}]":
            depth -= 1

    def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
        value: dict[str, object] = {}
        for key, item in pairs:
            if key in value:
                raise ValueError("duplicate JSON member")
            value[key] = item
        return value

    def reject_constant(value: str) -> object:
        raise ValueError("non-finite JSON constant")

    try:
        return json.loads(text, object_pairs_hook=unique_object, parse_constant=reject_constant)
    except RecursionError:
        raise ValueError("JSON nesting unsupported") from None


def _open_flags() -> int:
    flags = os.O_RDONLY
    for name in ("O_NOFOLLOW", "O_NONBLOCK", "O_NOCTTY", "O_CLOEXEC"):
        flags |= getattr(os, name, 0)
    return flags


def read_bounded_fd(fd: int, limit: int, description: str) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while total <= limit:
        block = os.read(fd, min(READ_CHUNK_BYTES, limit + 1 - total))
        if not block:
            break
        chunks.append(block)
        total += len(block)
    if total > limit:
        raise InputProblem(f"{description} exceeds {limit} bytes")
    return b"".join(chunks)


def read_manifest_bytes(path: str) -> tuple[bytes, int]:
    """Return manifest bytes and an open fd for its directory (caller closes).

    The directory path is the caller's chosen location and is opened as
    given, resolved once by the kernel; the manifest name inside it is opened
    no-follow, and pages are resolved from this same directory fd.
    """
    if not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY"):
        raise InputProblem("safe no-follow file opens are unavailable")
    try:
        directory, name = os.path.split(path)
    except (TypeError, ValueError) as exc:
        raise InputProblem("manifest path is invalid") from exc
    if not name:
        raise InputProblem("manifest path names no file")
    try:
        dir_fd = os.open(directory or ".", os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_CLOEXEC", 0))
    except (OSError, TypeError, ValueError) as exc:
        raise InputProblem("manifest directory cannot be opened") from exc
    try:
        try:
            fd = os.open(name, _open_flags(), dir_fd=dir_fd)
        except (OSError, TypeError, ValueError) as exc:
            raise InputProblem("manifest is missing, a symlink, or unreadable") from exc
        try:
            if not stat.S_ISREG(os.fstat(fd).st_mode):
                raise InputProblem("manifest is not a regular file")
            data = read_bounded_fd(fd, MAX_MANIFEST_BYTES, "manifest")
        finally:
            os.close(fd)
    except BaseException:
        os.close(dir_fd)
        raise
    return data, dir_fd


def read_page_bytes(manifest_dir_fd: int, relative: str) -> bytes:
    """Read one page file that must live inside the manifest directory."""
    if not isinstance(relative, str) or not relative:
        raise InputProblem("page file must be a non-empty relative path")
    if os.path.isabs(relative) or ntpath.isabs(relative) or ntpath.splitdrive(relative)[0] or "\\" in relative:
        raise InputProblem("absolute or platform-ambiguous page path")
    parts = relative.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise InputProblem("empty, dot, or traversal path component")
    if not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY"):
        raise InputProblem("safe no-follow file opens are unavailable")

    dir_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
    try:
        current_fd = os.dup(manifest_dir_fd)
    except (OSError, TypeError, ValueError) as exc:
        raise InputProblem("manifest directory cannot be reused") from exc
    try:
        for component in parts[:-1]:
            try:
                next_fd = os.open(component, dir_flags, dir_fd=current_fd)
            except (OSError, TypeError, ValueError) as exc:
                raise InputProblem("page path contains a symlink or inaccessible directory") from exc
            old_fd, current_fd = current_fd, next_fd
            os.close(old_fd)
        try:
            file_fd = os.open(parts[-1], _open_flags(), dir_fd=current_fd)
        except (OSError, TypeError, ValueError) as exc:
            raise InputProblem("page file is missing, a symlink, or unreadable") from exc
        try:
            if not stat.S_ISREG(os.fstat(file_fd).st_mode):
                raise InputProblem("page file is not regular")
            try:
                return read_bounded_fd(file_fd, MAX_HTML_BYTES, "HTML")
            except OSError as exc:
                raise InputProblem("page file cannot be read") from exc
        finally:
            os.close(file_fd)
    finally:
        os.close(current_fd)


def _remove_dot_segments(path: str) -> str:
    """Remove dot segments, treating %2e as a dot (browser behaviour)."""
    if not path:
        return "/"
    if not path.startswith("/"):
        raise ValueError("path must be absolute")
    source = path.split("/")
    result = [""]
    last_index = len(source) - 1
    for index, segment in enumerate(source[1:], start=1):
        lowered = ascii_lower(segment)
        if lowered in {".", "%2e"}:
            if index == last_index:
                result.append("")
        elif lowered in {"..", ".%2e", "%2e.", "%2e%2e"}:
            if len(result) > 1:
                result.pop()
            if index == last_index:
                result.append("")
        else:
            result.append(segment)
    normalized = "/".join(result)
    return normalized or "/"


def _site_key(scheme: str, host: str, port: int | None) -> tuple[str, int | None]:
    """Site identity for the same-site test.

    http and https on one host are the same site, so the scheme is not part
    of the key; a port is significant only when it is not the scheme default.
    """
    default = 80 if scheme == "http" else 443
    return host, None if port is None or port == default else port


def _parse_absolute(target: str) -> dict[str, object] | None:
    try:
        parts = urlsplit(target)
        port = parts.port
    except ValueError:
        return None
    scheme = ascii_lower(parts.scheme)
    if scheme not in {"http", "https"}:
        return None
    host = ascii_lower(parts.hostname or "")
    if not host:
        return None
    path = parts.path or "/"
    if not path.startswith("/"):
        path = "/" + path
    return {
        "scheme": scheme,
        "host": host,
        "port": port,
        "path": _remove_dot_segments(path),
        "query": parts.query,
    }


def _clean_reference(value: str) -> str:
    """Browser-like pre-processing of one URL reference."""
    text = value.replace("\t", "").replace("\n", "").replace("\r", "")
    text = text.replace("\\", "/")
    start, end = 0, len(text)
    while start < end and ord(text[start]) <= 0x20:
        start += 1
    while end > start and ord(text[end - 1]) <= 0x20:
        end -= 1
    return text[start:end]


def resolve_url(value: str, base_url: str) -> dict[str, object] | None:
    """Resolve one reference against a base URL; None when it is not ours."""
    cleaned = _clean_reference(value)
    if not cleaned:
        return None
    match = SCHEME_RE.match(cleaned)
    if match:
        scheme = ascii_lower(match.group(0)[:-1])
        if scheme not in {"http", "https"}:
            return None
        rest = cleaned[len(match.group(0)):]
        base_scheme = ascii_lower(urlsplit(base_url).scheme)
        if scheme == base_scheme and not rest.startswith("//"):
            # WHATWG: a special-scheme reference with the base's scheme and no
            # "//" is relative to the base ("https:/../x", "https:x").
            try:
                target = urljoin(base_url, rest) if rest else base_url
            except ValueError:
                return None
        else:
            target = cleaned
    else:
        if cleaned.startswith("//"):
            authority = cleaned[2:].split("/", 1)[0].split("?", 1)[0].split("#", 1)[0]
            if not authority:
                # A network-path reference with an empty authority is not a URL;
                # urljoin would silently inherit the base authority.
                return None
        try:
            target = urljoin(base_url, cleaned)
        except ValueError:
            return None
    return _parse_absolute(target)


def serialize_url(record: dict[str, object]) -> str:
    scheme = str(record["scheme"])
    host = str(record["host"])
    port = record["port"]
    default = 80 if scheme == "http" else 443
    authority = host
    if isinstance(port, int) and port != default:
        authority += ":" + str(port)
    text = f"{scheme}://{authority}{record['path']}"
    query = record["query"]
    if query:
        text += "?" + str(query)
    return text


def path_is_inside(path: str, base_path: str) -> bool:
    """True when a resolved path stays under the base path."""
    if path.startswith(base_path):
        return True
    trimmed = base_path[:-1] if len(base_path) > 1 else base_path
    return path == trimmed


def _read_srcset_descriptors(value: str, position: int) -> tuple[list[str], int]:
    descriptors: list[str] = []
    length = len(value)
    while position < length:
        while position < length and value[position] in ASCII_WS:
            position += 1
        if position >= length:
            break
        if value[position] == ",":
            position += 1
            break
        start = position
        depth = 0
        while position < length:
            char = value[position]
            if char == "(":
                depth += 1
            elif char == ")":
                if depth:
                    depth -= 1
            elif char == "," and depth == 0:
                break
            position += 1
        descriptors.append(value[start:position])
    return descriptors, position


def _valid_srcset_descriptors(descriptors: list[str]) -> bool:
    seen_width = False
    seen_density = False
    for descriptor in descriptors:
        if SRCSET_WIDTH_RE.match(descriptor):
            if seen_width or seen_density:
                return False
            seen_width = True
        elif SRCSET_DENSITY_RE.match(descriptor):
            if seen_width or seen_density:
                return False
            seen_density = True
        else:
            return False
    return True


def parse_srcset(value: str) -> list[str]:
    """Return the candidate URL strings of a srcset attribute."""
    candidates: list[str] = []
    position = 0
    length = len(value)
    while position < length:
        while position < length and (value[position] in ASCII_WS or value[position] == ","):
            position += 1
        if position >= length:
            break
        start = position
        while position < length and value[position] not in ASCII_WS:
            position += 1
        url = value[start:position]
        if url.endswith(","):
            candidates.append(url.rstrip(","))
            continue
        descriptors, position = _read_srcset_descriptors(value, position)
        if descriptors and not _valid_srcset_descriptors(descriptors):
            continue
        candidates.append(url)
    return candidates


class ReferenceParser(HTMLParser):
    """Collect reference-carrying elements and the first base href."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.elements: list[tuple[str, dict[str, str | None]]] = []
        self.base_seen = False
        self.base_href: str | None = None
        self.template_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = ascii_lower(tag)
        if self.template_depth:
            if tag == "template":
                self.template_depth += 1
            return
        if tag == "template":
            self.template_depth = 1
            return
        normalized = attrs_first_wins(attrs)
        if tag == "base" and not self.base_seen and "href" in normalized:
            self.base_seen = True
            self.base_href = normalized["href"] or ""
        self.elements.append((tag, normalized))

    def handle_endtag(self, tag: str) -> None:
        tag = ascii_lower(tag)
        if self.template_depth:
            if tag == "template":
                self.template_depth -= 1


def extract_references(elements: list[tuple[str, dict[str, str | None]]]) -> list[tuple[str, str, str]]:
    references: list[tuple[str, str, str]] = []
    for tag, attrs in elements:
        for element_name, attribute in REFERENCE_ATTRIBUTES:
            if element_name != tag:
                continue
            value = attrs.get(attribute)
            if value is None:
                continue
            if attribute == "srcset":
                for candidate in parse_srcset(value):
                    references.append((tag, attribute, candidate))
            else:
                references.append((tag, attribute, value))
    return references


def evaluate_page(
    text: str,
    page: dict[str, str],
    page_url: str,
    base_path: str,
    page_site: tuple[str, int | None],
) -> tuple[list[dict[str, object]], int]:
    parser = ReferenceParser()
    try:
        parser.feed(text)
        parser.close()
    except (AssertionError, ValueError, UnicodeError) as exc:
        raise InputProblem("page HTML could not be parsed") from exc

    base_url = page_url
    if parser.base_href:
        base_record = resolve_url(parser.base_href, page_url)
        if base_record is not None:
            base_url = serialize_url(base_record)

    references = extract_references(parser.elements)
    findings: list[dict[str, object]] = []
    for index, (element, attribute, value) in enumerate(references, start=1):
        record = resolve_url(value, base_url)
        if record is None:
            continue
        if _site_key(str(record["scheme"]), str(record["host"]), record["port"]) != page_site:
            continue
        if path_is_inside(str(record["path"]), base_path):
            continue
        findings.append({
            "id": f"{page['file']}#{index}:{element}[{attribute}]={value}",
            "reason": REASON_OUTSIDE,
            "page": page["url"],
            "element": element,
            "attribute": attribute,
            "value": value,
            "resolved": serialize_url(record),
        })
    return findings, len(references)


def _input_finding(page_url: str | None, reason: str = REASON_INPUT) -> dict[str, object]:
    return {
        "id": reason,
        "reason": reason,
        "page": page_url,
        "element": None,
        "attribute": None,
        "value": None,
        "resolved": None,
    }


def _validate_manifest(value: object) -> tuple[str, list[dict[str, str]]]:
    if not isinstance(value, dict) or set(value) != {"version", "basePath", "pages"}:
        raise InputProblem("manifest must have exactly version, basePath and pages")
    version = value.get("version")
    base_path = value.get("basePath")
    pages = value.get("pages")
    if type(version) is not int or version != 1:
        raise InputProblem("manifest version must be 1")
    if not isinstance(base_path, str) or not base_path.startswith("/") or not base_path.endswith("/"):
        raise InputProblem("basePath must start and end with '/'")
    if any(ord(char) <= 0x20 or ord(char) == 0x7F for char in base_path):
        raise InputProblem("basePath must not contain whitespace or control characters")
    if not isinstance(pages, list) or not pages:
        raise InputProblem("manifest pages must be a non-empty array")
    normalized_pages: list[dict[str, str]] = []
    for page in pages:
        if not isinstance(page, dict) or set(page) != {"file", "url"}:
            raise InputProblem("each page must have exactly file and url")
        file_name = page.get("file")
        url = page.get("url")
        if not isinstance(file_name, str) or not file_name:
            raise InputProblem("page file must be a non-empty string")
        if not isinstance(url, str) or not url:
            raise InputProblem("page url must be a non-empty string")
        if any(item["file"] == file_name or item["url"] == url for item in normalized_pages):
            raise InputProblem("duplicate page file or url in manifest")
        normalized_pages.append({"file": file_name, "url": url})
    return base_path, normalized_pages


def _load_manifest(path: str) -> tuple[str, list[dict[str, str]], int]:
    raw, manifest_dir_fd = read_manifest_bytes(path)
    try:
        try:
            value = strict_json(raw)
        except (UnicodeDecodeError, ValueError) as exc:
            raise InputProblem("manifest is not valid UTF-8 JSON") from exc
        base_path, pages = _validate_manifest(value)
    except BaseException:
        os.close(manifest_dir_fd)
        raise
    return base_path, pages, manifest_dir_fd


def audit_manifest(path: str) -> dict[str, object]:
    try:
        base_path, pages, manifest_dir_fd = _load_manifest(path)
    except (InputProblem, OSError, UnicodeError, ValueError):
        return {
            "verdict": "could-not-evaluate",
            "pagesChecked": 0,
            "referencesChecked": 0,
            "findings": [_input_finding(None)],
            "exit_code": EXIT_INPUT,
        }

    try:
        prepared: list[tuple[dict[str, str], dict[str, object], str]] = []
        problems: list[dict[str, object]] = []
        for page in pages:
            record = _parse_absolute(page["url"])
            if record is None:
                problems.append(_input_finding(page["url"]))
                continue
            if not path_is_inside(str(record["path"]), base_path):
                problems.append(_input_finding(page["url"], REASON_PAGE_OUTSIDE))
                continue
            try:
                raw = read_page_bytes(manifest_dir_fd, page["file"])
            except (InputProblem, OSError, ValueError):
                problems.append(_input_finding(page["url"]))
                continue
            try:
                text = raw.decode("utf-8-sig", errors="strict")
            except UnicodeDecodeError:
                problems.append(_input_finding(page["url"]))
                continue
            prepared.append((page, record, text))
        if problems:
            return {
                "verdict": "could-not-evaluate",
                "pagesChecked": 0,
                "referencesChecked": 0,
                "findings": problems,
                "exit_code": EXIT_INPUT,
            }

        findings: list[dict[str, object]] = []
        pages_checked = 0
        references_checked = 0
        for page, record, text in prepared:
            page_site = _site_key(str(record["scheme"]), str(record["host"]), record["port"])
            page_url = serialize_url(record)
            try:
                page_findings, count = evaluate_page(text, page, page_url, base_path, page_site)
            except InputProblem:
                return {
                    "verdict": "could-not-evaluate",
                    "pagesChecked": 0,
                    "referencesChecked": 0,
                    "findings": [_input_finding(page["url"])],
                    "exit_code": EXIT_INPUT,
                }
            pages_checked += 1
            references_checked += count
            findings.extend(page_findings)
    finally:
        os.close(manifest_dir_fd)

    if any(finding["reason"] in INPUT_REASONS for finding in findings):
        verdict, exit_code = "could-not-evaluate", EXIT_INPUT
    elif findings:
        verdict, exit_code = "failed-policy", EXIT_POLICY
    else:
        verdict, exit_code = "clean", EXIT_CLEAN
    return {
        "verdict": verdict,
        "pagesChecked": pages_checked,
        "referencesChecked": references_checked,
        "findings": findings,
        "exit_code": exit_code,
    }


def public_result(result: dict[str, object]) -> dict[str, object]:
    return {
        "verdict": result["verdict"],
        "pagesChecked": result["pagesChecked"],
        "referencesChecked": result["referencesChecked"],
        "findings": result["findings"],
    }


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    try:
        args = parse_cli(argv)
    except UsageError as exc:
        print(f"base_path_audit.py: {exc}\n{usage()}", file=sys.stderr, end="")
        print(json.dumps(USAGE_RESULT, sort_keys=True, separators=(",", ":")))
        return EXIT_USAGE
    result = audit_manifest(args.manifest)
    print(json.dumps(public_result(result), sort_keys=True, separators=(",", ":")))
    return int(result["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
