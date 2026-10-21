#!/usr/bin/env python3
"""Read-only static publisher-policy check for canonical link elements.

This compares source HTML signals; it does not predict search-engine selection,
render JavaScript, fetch URLs, inspect response headers/redirects, or establish
publishing readiness. See usage() and the selftest for the deliberately bounded
input and normalization rules.
"""
from __future__ import annotations

import argparse
import ipaddress
import json
import ntpath
import os
import re
import stat
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from urllib.parse import quote, urljoin, urlsplit

MAX_MANIFEST_BYTES = 1024 * 1024
MAX_HTML_BYTES = 2 * 1024 * 1024
READ_CHUNK_BYTES = 64 * 1024

EXIT_CLEAN = 0
EXIT_POLICY = 1
EXIT_INPUT = 2
EXIT_USAGE = 64

INPUT_FINDINGS = {"input_invalid", "html_unsupported"}
USAGE_RESULT = {"verdict": "could-not-evaluate", "pagesChecked": 0, "findings": []}
ASCII_WS = " \t\n\r\f"
HEAD_ELEMENTS = {"base", "link", "meta", "noscript", "script", "style", "template", "title"}
HEAD_VOID_ELEMENTS = {"base", "link", "meta"}
HTML_VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"
}
HEAD_TEXT_ELEMENTS = {"script", "style", "title"}


class UsageError(Exception):
    """Invalid command-line shape."""


class InputProblem(Exception):
    """Manifest or referenced file could not be safely evaluated."""


class UnsupportedHTML(Exception):
    """HTML exceeds the supported static parser boundary."""


class URLProblem(ValueError):
    """URL is outside the explicitly supported HTTP(S) subset."""


class URLFragment(URLProblem):
    """A literal URL fragment was supplied where fragments are forbidden."""


class CanonicalArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise UsageError(message)


class SingleManifestAction(argparse.Action):
    """Reject a repeated --manifest instead of silently keeping the last path."""

    def __call__(self, parser, namespace, values, option_string=None) -> None:
        if getattr(namespace, self.dest, None) is not None:
            raise UsageError("--manifest may be given only once")
        setattr(namespace, self.dest, values)


def usage() -> str:
    return (
        "usage: canonical_audit.py --manifest PATH [--json] | --selftest\n"
        "--help prints standard CLI help, exits 0, and emits no publishing verdict.\n"
        "\n"
        "Read UTF-8 JSON manifest v1 and bounded local UTF-8 HTML only. The\n"
        "manifest limit is 1 MiB; each HTML file is limited to 2 MiB.\n"
        "HTML files are relative to the manifest directory; absolute paths,\n"
        "traversal, symlinks, and non-regular files are rejected. The manifest\n"
        "file itself must not be a symlink; its directory path is the caller's\n"
        "chosen location and is opened as given, once, for manifest and pages.\n"
        "No network access or writes occur in manifest mode.\n"
        "\n"
        "URLs use this tool's conservative HTTP(S) normalization: lowercase ASCII\n"
        "scheme/host, accept ASCII DNS labels, strict dotted IPv4, or bracketed\n"
        "IPv6, remove default ports and dot segments, and serialize empty paths\n"
        "as '/'. Non-ASCII path/query text is UTF-8 percent-escaped; existing\n"
        "escapes and legal ASCII query spelling, including a final empty '?', persist.\n"
        "Credentials, fragments, backslashes, whitespace, malformed authorities,\n"
        "and network-path references with an empty authority ('///path') are\n"
        "rejected. The first head base[href] resolves relative\n"
        "links; invalid first base is base_url_invalid, not browser fallback.\n"
        "This is a conservative RFC-style subset, not a WHATWG URL implementation.\n"
        "\n"
        "HTMLParser is not an HTML5 tree builder. It does not perform browser\n"
        "encoding sniffing or implied-element repair; only explicit, properly\n"
        "closed head markup with supported head children is evaluated. Comments,\n"
        "raw-text elements, and template descendants do not contribute links.\n"
        "SVG/Math before the head closes, a canonical-looking link inside SVG/Math,\n"
        "and canonical/base inside noscript are unsupported; SVG/Math and\n"
        "self-closed HTML void elements after the closed head are evaluated.\n"
        "Oversize, non-UTF-8, or structurally ambiguous HTML is unsupported.\n"
        "This compares publisher policy only, not Google or other search-engine\n"
        "canonical selection. It does not assess readiness or HTTP responses.\n"
        "\n"
        "Except --help, stdout is always one JSON object: verdict, pagesChecked,\n"
        "findings. Usage errors report could-not-evaluate with no findings.\n"
        "Exit: 0 clean; 1 policy finding; 2 input/unsupported; 64 usage.\n"
    )


def parse_cli(argv: list[str]) -> argparse.Namespace:
    parser = CanonicalArgumentParser(
        prog="canonical_audit.py",
        usage="canonical_audit.py --manifest PATH [--json] | --selftest | -h | --help",
        add_help=True,
        allow_abbrev=False,
        description="Offline static canonical preflight; --help is documentation only.",
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--manifest", metavar="PATH", action=SingleManifestAction)
    mode.add_argument("--selftest", action="store_true")
    parser.add_argument("--json", action="store_true", help="emit JSON (the default)")
    args = parser.parse_args(argv)
    if args.selftest and args.json:
        parser.error("--json is only valid with --manifest")
    return args


def ascii_lower(value: str) -> str:
    return value.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"))


def split_ascii_whitespace(value: str) -> list[str]:
    return [token for token in re.split(r"[ \t\n\r\f]+", value) if token]


def attrs_first_wins(attrs: list[tuple[str, str | None]]) -> dict[str, str | None]:
    result: dict[str, str | None] = {}
    for name, value in attrs:
        result.setdefault(ascii_lower(name), value)
    return result


def is_canonical_relation(attrs: dict[str, str | None]) -> bool:
    rel = attrs.get("rel")
    return rel is not None and any(ascii_lower(token) == "canonical" for token in split_ascii_whitespace(rel))


class CanonicalHTMLParser(HTMLParser):
    """Collect only canonical links in/out of one explicit, supported head."""

    # HTMLParser only treats script/style as CDATA by default. The added raw
    # text elements prevent tag-looking text from becoming false link signals.
    CDATA_CONTENT_ELEMENTS = (
        "script", "style", "title", "textarea", "xmp", "iframe", "noembed", "noframes", "plaintext"
    )

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.head_seen = False
        self.head_open = False
        self.head_closed = False
        self.body_seen = False
        self.unsupported = False
        self.template_depth = 0
        self.foreign_stack: list[str] = []
        self.noscript_depth = 0
        self.raw_head_element: str | None = None
        self.head_canonicals: list[dict[str, str | None]] = []
        self.outside_canonicals: list[dict[str, str | None]] = []
        self.base_seen = False
        self.base_href: str | None = None

    def _enter_template(self) -> None:
        self.template_depth += 1

    def _record_link(self, attrs: list[tuple[str, str | None]], inside_head: bool) -> None:
        normalized = attrs_first_wins(attrs)
        if not is_canonical_relation(normalized):
            return
        target = self.head_canonicals if inside_head else self.outside_canonicals
        target.append(normalized)

    def _after_head(self) -> bool:
        return self.head_closed and not self.head_open

    @property
    def foreign_depth(self) -> int:
        return len(self.foreign_stack)

    def set_cdata_mode(self, *args, **kwargs) -> None:
        # SVG/MathML title/style/script are not HTML raw text: SVG title is an
        # HTML integration point. Tokenize them so hidden markup stays visible.
        if self.foreign_stack:
            return
        super().set_cdata_mode(*args, **kwargs)

    def _foreign_token(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        # Inside SVG/MathML after the explicit head, only tokens that a browser
        # could turn into an effective HTML base/head/canonical are ambiguous.
        if tag in {"base", "head"} or (tag == "link" and is_canonical_relation(attrs_first_wins(attrs))):
            self.unsupported = True

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = ascii_lower(tag)
        if self.foreign_stack:
            self._foreign_token(tag, attrs)
            self.foreign_stack.append(tag)
            return
        if self.template_depth:
            if tag == "template":
                self._enter_template()
            return
        if self.noscript_depth:
            if tag == "noscript":
                self.noscript_depth += 1
            elif tag == "base" or (tag == "link" and is_canonical_relation(attrs_first_wins(attrs))):
                self.unsupported = True
            return
        if tag == "noscript":
            if not self.head_seen and not self.head_open:
                self.unsupported = True
            self.noscript_depth = 1
            return
        if tag in {"svg", "math"}:
            if self._after_head() and not self.template_depth:
                self.foreign_stack.append(tag)
                return
            self.unsupported = True

        if tag == "template":
            if not self.head_seen and not self.head_open:
                self.unsupported = True
            self._enter_template()
            return

        if not self.head_seen:
            if tag == "html":
                return
            if tag == "head":
                self.head_seen = True
                self.head_open = True
                return
            self.unsupported = True
            if tag == "body":
                self.body_seen = True
            if tag == "link":
                self._record_link(attrs, inside_head=False)
            return

        if self.head_open:
            if tag == "head":
                self.unsupported = True
                return
            if tag == "body":
                self.unsupported = True
                self.head_open = False
                self.head_closed = True
                self.body_seen = True
                return
            if tag not in HEAD_ELEMENTS:
                # HTML's tree builder would implicitly leave head for many of
                # these elements. Do not treat subsequent links as head links.
                self.unsupported = True
                self.head_open = False
                self.head_closed = True
                if tag == "link":
                    self._record_link(attrs, inside_head=False)
                return
            if tag == "base":
                normalized = attrs_first_wins(attrs)
                if "href" in normalized and not self.base_seen:
                    self.base_seen = True
                    self.base_href = normalized["href"] or ""
            elif tag == "link":
                self._record_link(attrs, inside_head=True)
            if tag in HEAD_TEXT_ELEMENTS:
                self.raw_head_element = tag
            return

        if tag in {"head", "base"}:
            # A body base is still the document's first base in tree order.
            self.unsupported = True
        elif tag == "body":
            if self.body_seen:
                self.unsupported = True
            self.body_seen = True
        elif tag == "link":
            self._record_link(attrs, inside_head=False)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = ascii_lower(tag)
        if self.foreign_stack or (self._after_head() and tag in {"svg", "math"}):
            # Self-closing syntax is native to foreign content; it opens nothing.
            self._foreign_token(tag, attrs)
            return
        if tag not in HEAD_VOID_ELEMENTS and not (self._after_head() and tag in HTML_VOID_ELEMENTS):
            # HTML ignores the slash on non-void tags; do not infer a close.
            self.unsupported = True
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        tag = ascii_lower(tag)
        if self.foreign_stack:
            # Browsers pop foreign elements by their own stack rules; only an
            # exactly matching end tag is modelled, anything else fails closed.
            if self.foreign_stack[-1] == tag:
                self.foreign_stack.pop()
            else:
                self.unsupported = True
            return
        if self.template_depth:
            if tag == "template":
                self.template_depth -= 1
            return
        if self.noscript_depth:
            if tag == "noscript":
                self.noscript_depth -= 1
            return

        if tag == "head":
            if not self.head_open:
                self.unsupported = True
            else:
                self.head_open = False
                self.head_closed = True
            return
        if self.raw_head_element == tag:
            self.raw_head_element = None
            return
        if self.head_open:
            if tag not in HEAD_TEXT_ELEMENTS:
                # End tags for void head elements and unrelated end tags are
                # malformed; fail closed rather than infer browser repair.
                self.unsupported = True
            return
        if tag == "body":
            if not self.head_closed:
                self.unsupported = True
            self.body_seen = True

    def handle_data(self, data: str) -> None:
        if self.template_depth or not data.strip(ASCII_WS):
            return
        if self.head_open and self.raw_head_element is None:
            self.unsupported = True
            self.head_open = False
            self.head_closed = True
        elif not self.head_seen:
            self.unsupported = True

    def handle_pi(self, data: str) -> None:
        if not self.template_depth and not self.noscript_depth:
            self.unsupported = True

    def unknown_decl(self, data: str) -> None:
        if not self.template_depth and not self.noscript_depth:
            self.unsupported = True

    def finish_supported(self) -> bool:
        return (
            self.head_seen
            and self.head_closed
            and not self.head_open
            and self.template_depth == 0
            and self.noscript_depth == 0
            and self.foreign_depth == 0
            and self.raw_head_element is None
            and getattr(self, "cdata_elem", None) is None
            and not self.unsupported
        )


def _host_and_port(authority: str) -> tuple[str, int | None]:
    if not authority or any(ord(ch) <= 0x20 or ord(ch) == 0x7F for ch in authority):
        raise URLProblem("empty or whitespace authority")
    if "@" in authority or "\\" in authority or "%" in authority:
        raise URLProblem("credentials or unsupported authority encoding")

    is_ipv6 = authority.startswith("[")
    if is_ipv6:
        close = authority.find("]")
        if close < 0 or authority.find("[", 1) >= 0 or "]" in authority[close + 1 :]:
            raise URLProblem("malformed bracketed host")
        raw_host = authority[1:close]
        suffix = authority[close + 1 :]
        if suffix and not suffix.startswith(":"):
            raise URLProblem("malformed port")
        port_text = suffix[1:] if suffix else ""
        try:
            host = "[" + ipaddress.IPv6Address(raw_host).compressed.lower() + "]"
        except ipaddress.AddressValueError as exc:
            raise URLProblem("invalid IPv6 host") from exc
    else:
        if "[" in authority or "]" in authority or authority.count(":") > 1:
            raise URLProblem("unbracketed or malformed IPv6 host")
        if ":" in authority:
            raw_host, port_text = authority.rsplit(":", 1)
        else:
            raw_host, port_text = authority, ""
        if not raw_host or not raw_host.isascii():
            raise URLProblem("host must be non-empty ASCII")
        host = ascii_lower(raw_host)
        if all(ch in "0123456789." for ch in host):
            try:
                host = str(ipaddress.IPv4Address(host))
            except ipaddress.AddressValueError as exc:
                raise URLProblem("invalid dotted-decimal IPv4 host") from exc
        else:
            dns_host = host[:-1] if host.endswith(".") else host
            if not dns_host or len(dns_host) > 253:
                raise URLProblem("invalid DNS host")
            labels = dns_host.split(".")
            if any(
                not label
                or len(label) > 63
                or label.startswith("-")
                or label.endswith("-")
                or re.fullmatch(r"[a-z0-9-]+", label) is None
                for label in labels
            ):
                raise URLProblem("invalid DNS host")

    if port_text == "":
        port = None
    else:
        if not port_text.isascii() or not port_text.isdigit():
            raise URLProblem("invalid port")
        port_digits = port_text.lstrip("0") or "0"
        if len(port_digits) > 5:
            raise URLProblem("port out of range")
        port = int(port_digits, 10)
        if port > 65535:
            raise URLProblem("port out of range")
    return host, port


def _remove_dot_segments(path: str) -> str:
    if not path:
        return "/"
    if not path.startswith("/"):
        raise URLProblem("authority URL path must be absolute")
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


def normalize_http_url(raw: str, base: str | None = None, *, absolute: bool = False) -> str:
    """Normalize a conservative HTTP(S) URL subset; reject parser ambiguities."""
    if not isinstance(raw, str) or raw == "":
        raise URLProblem("empty URL")
    if "#" in raw:
        raise URLFragment("fragments are not accepted")
    if "\\" in raw or any(ord(ch) <= 0x20 or 0x7F <= ord(ch) <= 0x9F for ch in raw):
        # C0, DEL and C1 controls are outside RFC 3987 ucschar: reject, never escape.
        raise URLProblem("URL contains whitespace, controls, or backslash")
    query_delimiter_present = "?" in raw
    empty_query_delimiter = query_delimiter_present and raw.split("?", 1)[1] == ""
    try:
        initial = urlsplit(raw)
        if initial.scheme:
            candidate = raw
        elif absolute:
            raise URLProblem("an absolute HTTP(S) URL is required")
        else:
            if base is None:
                raise URLProblem("relative URL has no base")
            if raw.startswith("//") and not initial.netloc:
                # urljoin would silently inherit the base authority (false clean).
                raise URLProblem("network-path reference has an empty authority")
            candidate = urljoin(base, raw)
        parts = urlsplit(candidate)
        if empty_query_delimiter:
            parts = parts._replace(query="")
    except (ValueError, UnicodeError) as exc:
        if isinstance(exc, URLProblem):
            raise
        raise URLProblem("malformed URL") from exc

    scheme = ascii_lower(parts.scheme)
    if scheme not in {"http", "https"}:
        raise URLProblem("only HTTP(S) URLs are supported")
    host, port = _host_and_port(parts.netloc)
    default_port = 80 if scheme == "http" else 443
    authority = host
    if port is not None and port != default_port:
        authority += ":" + str(port)

    try:
        path = quote(_remove_dot_segments(parts.path), safe="/:@!$&'()*+,;=-._~%[]")
        has_query = "?" in candidate.split("#", 1)[0] or query_delimiter_present
        query = quote(parts.query, safe="/?:@!$&'()*+,;=-._~%[]")
    except (UnicodeError, ValueError) as exc:
        raise URLProblem("URL contains unsupported characters") from exc
    result = f"{scheme}://{authority}{path}"
    if has_query:
        result += "?" + query
    return result


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
        raise UnsupportedHTML(f"{description} exceeds {limit} bytes")
    return b"".join(chunks)


def read_manifest_bytes(path: str) -> tuple[bytes, int]:
    """Return manifest bytes and an open fd for its directory (caller closes).

    The directory path is the caller's chosen location and is opened as given,
    resolved once by the kernel (no lexical '..' collapsing, which would audit a
    different file after a symlink); the manifest name inside it is opened
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
            fd = os.open(
                name,
                os.O_RDONLY | os.O_NOFOLLOW | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_CLOEXEC", 0),
                dir_fd=dir_fd,
            )
        except (OSError, TypeError, ValueError) as exc:
            raise InputProblem("manifest is missing, a symlink, or unreadable") from exc
        try:
            if not stat.S_ISREG(os.fstat(fd).st_mode):
                raise InputProblem("manifest is not a regular file")
            try:
                data = read_bounded_fd(fd, MAX_MANIFEST_BYTES, "manifest")
            except UnsupportedHTML as exc:
                raise InputProblem(str(exc)) from exc
        finally:
            os.close(fd)
    except BaseException:
        os.close(dir_fd)
        raise
    return data, dir_fd


def read_page_bytes(manifest_dir_fd: int, relative: str) -> bytes:
    if not isinstance(relative, str) or not relative:
        raise InputProblem("page file must be a non-empty relative path")
    if (
        os.path.isabs(relative)
        or ntpath.isabs(relative)
        or ntpath.splitdrive(relative)[0]
        or "\\" in relative
    ):
        raise InputProblem("absolute or platform-ambiguous page path")
    parts = relative.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise InputProblem("empty, dot, or traversal path component")
    if not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY"):
        raise InputProblem("safe no-follow file opens are unavailable")

    flags_dir = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
    flags_file = os.O_RDONLY | os.O_NOFOLLOW | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_CLOEXEC", 0)
    try:
        current_fd = os.dup(manifest_dir_fd)
    except (OSError, TypeError, ValueError) as exc:
        raise InputProblem("manifest directory cannot be reused") from exc

    try:
        for component in parts[:-1]:
            try:
                next_fd = os.open(component, flags_dir, dir_fd=current_fd)
            except (OSError, TypeError, ValueError) as exc:
                raise InputProblem("page path contains a symlink or inaccessible directory") from exc
            old_fd, current_fd = current_fd, next_fd
            os.close(old_fd)
        try:
            file_fd = os.open(parts[-1], flags_file, dir_fd=current_fd)
        except (OSError, TypeError, ValueError) as exc:
            raise InputProblem("page file is missing, a symlink, or unreadable") from exc
        try:
            if not stat.S_ISREG(os.fstat(file_fd).st_mode):
                raise InputProblem("page file is not regular")
            try:
                return read_bounded_fd(file_fd, MAX_HTML_BYTES, "HTML")
            except UnsupportedHTML:
                raise
            except OSError as exc:
                raise InputProblem("page file cannot be read") from exc
        finally:
            os.close(file_fd)
    finally:
        os.close(current_fd)




def evaluate_page(html_bytes: bytes, document_url: str, expected_url: str) -> str | None:
    try:
        html_text = html_bytes.decode("utf-8-sig", errors="strict")
    except UnicodeDecodeError:
        return "html_unsupported"

    parser = CanonicalHTMLParser()
    try:
        parser.feed(html_text)
        parser.close()
    except (AssertionError, ValueError, UnicodeError):
        return "html_unsupported"
    if not parser.finish_supported():
        return "html_unsupported"

    effective_base = document_url
    if parser.base_seen:
        base_href = parser.base_href or ""
        if base_href:
            try:
                effective_base = normalize_http_url(base_href, document_url)
            except ValueError:
                return "base_url_invalid"

    if len(parser.head_canonicals) > 1:
        return "canonical_multiple"
    if parser.outside_canonicals:
        return "canonical_outside_head"
    if not parser.head_canonicals:
        return "canonical_missing"

    canonical = parser.head_canonicals[0]
    if (
        "href" not in canonical
        or canonical["href"] is None
        or canonical["href"].strip(ASCII_WS) == ""
    ):
        return "canonical_href_missing"
    href = canonical["href"]
    assert href is not None
    try:
        actual_url = normalize_http_url(href, effective_base)
    except URLFragment:
        return "canonical_fragment"
    except ValueError:
        return "canonical_url_invalid"
    if actual_url != expected_url:
        return "canonical_mismatch"
    return None


def _validate_manifest(value: object) -> list[dict[str, str]]:
    if not isinstance(value, dict) or set(value) != {"version", "pages"}:
        raise InputProblem("manifest must have exactly version and pages")
    version = value.get("version")
    pages = value.get("pages")
    if type(version) is not int or version != 1 or not isinstance(pages, list):
        raise InputProblem("manifest version must be 1 and pages must be an array")
    if not pages:
        raise InputProblem("manifest pages must be non-empty")
    normalized_pages: list[dict[str, str]] = []
    for page in pages:
        if not isinstance(page, dict) or set(page) != {"url", "file", "expectedCanonical"}:
            raise InputProblem("each page must have exactly url, file, expectedCanonical")
        if any(not isinstance(page.get(key), str) for key in ("url", "file", "expectedCanonical")):
            raise InputProblem("page url, file, and expectedCanonical must be strings")
        if any(page["url"] == seen["url"] or page["file"] == seen["file"] for seen in normalized_pages):
            # One page per URL and per file: a duplicate would be counted twice.
            raise InputProblem("duplicate page url or file in manifest")
        normalized_pages.append(page)
    return normalized_pages


def _load_manifest(path: str) -> tuple[list[dict[str, str]], int]:
    raw, manifest_dir_fd = read_manifest_bytes(path)
    try:
        try:
            value = json.loads(raw.decode("utf-8-sig", errors="strict"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise InputProblem("manifest is not UTF-8 JSON") from exc
        pages = _validate_manifest(value)
    except BaseException:
        os.close(manifest_dir_fd)
        raise
    return pages, manifest_dir_fd


def audit_manifest(path: str) -> dict[str, object]:
    findings: list[dict[str, str | None]] = []
    pages_checked = 0
    try:
        pages, manifest_dir_fd = _load_manifest(path)
    except (InputProblem, OSError, UnicodeError, ValueError):
        return {
            "verdict": "could-not-evaluate",
            "pagesChecked": 0,
            "findings": [{"id": "input_invalid", "page": None}],
            "exit_code": EXIT_INPUT,
        }

    try:
        for page in pages:
            page_url = page["url"]
            try:
                normalized_document = normalize_http_url(page_url, absolute=True)
                normalized_expected = normalize_http_url(page["expectedCanonical"], absolute=True)
                html_bytes = read_page_bytes(manifest_dir_fd, page["file"])
            except UnsupportedHTML:
                finding_id = "html_unsupported"
            except (InputProblem, OSError, UnicodeError, ValueError):
                finding_id = "input_invalid"
            else:
                pages_checked += 1
                finding_id = evaluate_page(html_bytes, normalized_document, normalized_expected)
            if finding_id is not None:
                findings.append({"id": finding_id, "page": page_url})
    finally:
        os.close(manifest_dir_fd)

    if any(finding["id"] in INPUT_FINDINGS for finding in findings):
        verdict, exit_code = "could-not-evaluate", EXIT_INPUT
    elif findings:
        verdict, exit_code = "failed-policy", EXIT_POLICY
    else:
        verdict, exit_code = "clean", EXIT_CLEAN
    return {
        "verdict": verdict,
        "pagesChecked": pages_checked,
        "findings": findings,
        "exit_code": exit_code,
    }


def public_result(result: dict[str, object]) -> dict[str, object]:
    return {
        "verdict": result["verdict"],
        "pagesChecked": result["pagesChecked"],
        "findings": result["findings"],
    }


def _selftest_specs() -> list[dict[str, object]]:
    doc = "https://example.test/project/a.html"
    same = doc
    clean = lambda html, expected=same, url=doc: {
        "html": html,
        "url": url,
        "expected": expected,
        "exit": EXIT_CLEAN,
        "id": None,
    }
    failed = lambda html, finding, expected=same, url=doc: {
        "html": html,
        "url": url,
        "expected": expected,
        "exit": EXIT_POLICY,
        "id": finding,
    }
    return [
        {"name": "absolute_match", **clean(f"<html><head><link rel='canonical' href='{same}'></head></html>")},
        {"name": "selfclosing_link", **clean("<head><link rel=canonical href='https://example.test/project/a.html' /></head>")},
        {"name": "title_text_decoy", **failed(f"<head><title><link rel=canonical href='{same}'></title></head>", "canonical_missing")},
        {"name": "relative_same_dir", **clean("<head><link rel=canonical href=a.html></head>")},
        {"name": "relative_parent", **clean("<head><link rel=canonical href='../a.html'></head>", "https://example.test/a.html")},
        {"name": "root_relative", **clean("<head><link rel=canonical href='/project/a.html'></head>")},
        {"name": "scheme_relative", **clean("<head><link rel=canonical href='//example.test/project/a.html'></head>")},
        {"name": "network_path_empty_authority", **failed("<head><link rel=canonical href='///project/a.html'></head>", "canonical_url_invalid")},
        {"name": "network_path_empty_authority_four", **failed("<head><link rel=canonical href='////example.test/project/a.html'></head>", "canonical_url_invalid")},
        {"name": "first_base", **clean("<head><base href='https://example.test/first/'><base href='https://wrong.test/'><link rel=canonical href=item.html></head>", "https://example.test/first/item.html")},
        {"name": "second_base_ignored", **clean("<head><base href='/project/'><base href='https://wrong.test/'><link rel=canonical href=a.html></head>")},
        {"name": "empty_base", **clean("<head><base href=''><link rel=canonical href=a.html></head>")},
        {"name": "rel_token_list", **clean("<head><link rel='alternate CANONICAL' href='https://example.test/project/a.html'></head>")},
        {"name": "rel_uppercase", **clean("<head><link rel='CANONICAL' href='https://example.test/project/a.html'></head>")},
        {"name": "attr_uppercase", **clean("<HEAD><LINK REL='CANONICAL' HREF='https://example.test/project/a.html'></HEAD>")},
        {"name": "rel_non_ascii_separator", **failed("<head><link rel='canonical&#160;alternate' href='https://example.test/project/a.html'></head>", "canonical_missing")},
        {"name": "duplicate_attrs_first_wins", **clean("<head><link rel=canonical rel=alternate href='https://example.test/project/a.html'></head>")},
        {"name": "entity_href", **clean("<head><link rel=canonical href='https://example.test/project/a.html?x=1&amp;y=2'></head>", "https://example.test/project/a.html?x=1&y=2")},
        {"name": "query_preserved", **clean("<head><link rel=canonical href='?view=full'></head>", "https://example.test/project/a.html?view=full")},
        {"name": "empty_query_delimiter", **failed("<head><link rel=canonical href='https://example.test/project/a.html?'></head>", "canonical_mismatch")},
        {"name": "relative_empty_query", **failed("<head><link rel=canonical href='?'></head>", "canonical_mismatch", "https://example.test/project/a.html", "https://example.test/project/a.html?old")},
        {"name": "missing_link", **failed("<head></head>", "canonical_missing")},
        {"name": "duplicate_same", **failed(f"<head><link rel=canonical href='{same}'><link rel=canonical href='{same}'></head>", "canonical_multiple")},
        {"name": "duplicate_different", **failed(f"<head><link rel=canonical href='{same}'><link rel=canonical href='https://other.test/a'></head>", "canonical_multiple")},
        {"name": "body_link", **failed(f"<head></head><body><link rel=canonical href='{same}'></body>", "canonical_outside_head")},
        {"name": "href_absent", **failed("<head><link rel=canonical></head>", "canonical_href_missing")},
        {"name": "href_empty", **failed("<head><link rel=canonical href=''></head>", "canonical_href_missing")},
        {"name": "href_ascii_whitespace", **failed("<head><link rel=canonical href='&#32;&#9;&#10;&#12;&#13;'></head>", "canonical_href_missing")},
        {"name": "href_c1_control_path", **failed("<head><link rel=canonical href='https://example.test/project/a\u0085.html'></head>", "canonical_url_invalid", "https://example.test/project/a%C2%85.html")},
        {"name": "href_c1_control_query", **failed("<head><link rel=canonical href='https://example.test/project/a.html?x=\u009f'></head>", "canonical_url_invalid")},
        {"name": "invalid_url", **failed("<head><link rel=canonical href='https://[broken'></head>", "canonical_url_invalid")},
        {"name": "javascript_url", **failed("<head><link rel=canonical href='javascript:alert(1)'></head>", "canonical_url_invalid")},
        {"name": "data_url", **failed("<head><link rel=canonical href='data:text/html,x'></head>", "canonical_url_invalid")},
        {"name": "fragment_url", **failed(f"<head><link rel=canonical href='{same}#section'></head>", "canonical_fragment")},
        {"name": "empty_fragment", **failed(f"<head><link rel=canonical href='{same}#'></head>", "canonical_fragment")},
        {"name": "wrong_host", **failed("<head><link rel=canonical href='https://other.test/project/a.html'></head>", "canonical_mismatch")},
        {"name": "wrong_path", **failed("<head><link rel=canonical href='https://example.test/project/b.html'></head>", "canonical_mismatch")},
        {"name": "wrong_query", **failed("<head><link rel=canonical href='https://example.test/project/a.html?v=2'></head>", "canonical_mismatch")},
        {"name": "base_invalid", **failed("<head><base href='https://[broken'><link rel=canonical href=a.html></head>", "base_url_invalid")},
        {"name": "base_empty_authority", **failed("<head><base href='///project/'><link rel=canonical href=a.html></head>", "base_url_invalid")},
        {"name": "comment_decoy", **failed(f"<head><!-- <link rel=canonical href='{same}'> --></head>", "canonical_missing")},
        {"name": "script_decoy", **failed(f"<head><script>const x = '<link rel=canonical href=\"{same}\">';</script></head>", "canonical_missing")},
        {"name": "template_decoy", **failed(f"<head><template><link rel=canonical href='{same}'></template></head>", "canonical_missing")},
        {"name": "template_selfclose", "html": f"<head><template/><link rel=canonical href='{same}'></template></head>", "url": doc, "expected": same, "exit": EXIT_INPUT, "id": "html_unsupported"},
        {"name": "noscript_canonical", "html": f"<head><noscript><link rel=canonical href='{same}'></noscript></head>", "url": doc, "expected": same, "exit": EXIT_INPUT, "id": "html_unsupported"},
        {"name": "foreign_content", "html": f"<head></head><body><svg><link rel=canonical href='{same}'></svg></body>", "url": doc, "expected": same, "exit": EXIT_INPUT, "id": "html_unsupported"},
        {"name": "body_svg_after_head", **clean(f"<head><link rel=canonical href='{same}'></head><body><svg viewBox='0 0 1 1'><path d='M0 0'/><g><circle r='1'/></g></svg></body>")},
        {"name": "body_math_after_head", **clean(f"<head><link rel=canonical href='{same}'></head><body><math><mi>x</mi></math></body>")},
        {"name": "body_void_selfclose", **clean(f"<head><link rel=canonical href='{same}'></head><body><input type='checkbox' /><br/><img src='a.png' /></body>")},
        {"name": "body_svg_selfclose_link", "html": f"<head></head><body><svg><link rel=canonical href='{same}'/></svg></body>", "url": doc, "expected": same, "exit": EXIT_INPUT, "id": "html_unsupported"},
        {"name": "head_svg", "html": f"<head><svg></svg><link rel=canonical href='{same}'></head>", "url": doc, "expected": same, "exit": EXIT_INPUT, "id": "html_unsupported"},
        {"name": "body_nonvoid_selfclose", "html": f"<head><link rel=canonical href='{same}'></head><body><div/></body>", "url": doc, "expected": same, "exit": EXIT_INPUT, "id": "html_unsupported"},
        {"name": "body_svg_unclosed", "html": f"<head><link rel=canonical href='{same}'></head><body><svg><path d='M0 0'/>", "url": doc, "expected": same, "exit": EXIT_INPUT, "id": "html_unsupported"},
        {"name": "body_svg_then_body_canonical", **failed(f"<head></head><body><svg></svg><link rel=canonical href='{same}'></body>", "canonical_outside_head")},
        *[
            {"name": name, "html": html, "url": doc, "expected": same, "exit": EXIT_INPUT, "id": "html_unsupported"}
            for name, html in (
                ("body_base", "<head><link rel=canonical href=a.html></head><body><base href='https://wrong.test/'></body>"),
                ("foreignobject_base", "<head><link rel=canonical href=a.html></head><body><svg><foreignObject><base href='https://wrong.test/' /></foreignObject></svg></body>"),
                ("svg_head_breakout_base", "<head><link rel=canonical href=a.html></head><body><svg><head></head><base href='https://wrong.test/'></svg></body>"),
                ("svg_mismatched_end_base", "<head><link rel=canonical href=a.html></head><body><svg><math></svg><base href='https://wrong.test/'></math></body>"),
                ("svg_title_hidden_base", "<head><link rel=canonical href=a.html></head><body><svg><title><base href='https://wrong.test/'></title></svg></body>"),
                ("svg_style_hidden_base", "<head><link rel=canonical href=a.html></head><body><svg><style><base href='https://wrong.test/'></style></svg></body>"),
                ("svg_script_hidden_base", "<head><link rel=canonical href=a.html></head><body><svg><script><base href='https://wrong.test/'></script></svg></body>"),
            )
        ],
        {"name": "svg_title_text_clean", **clean(f"<head><link rel=canonical href='{same}'></head><body><svg><title>Icon</title><path d='M0 0'/></svg></body>")},
        {"name": "processing_instruction", "html": f"<head><?server-side include?><link rel=canonical href='{same}'></head>", "url": doc, "expected": same, "exit": EXIT_INPUT, "id": "html_unsupported"},
        {"name": "missing_head", "html": "<html><body></body></html>", "url": doc, "expected": same, "exit": EXIT_INPUT, "id": "html_unsupported"},
        {"name": "head_body_child", "html": f"<head><div><link rel=canonical href='{same}'></div></head>", "url": doc, "expected": same, "exit": EXIT_INPUT, "id": "html_unsupported"},
        {"name": "manifest_traversal", "file": "../outside.html", "html": "", "url": doc, "expected": same, "exit": EXIT_INPUT, "id": "input_invalid"},
        {"name": "symlink_html", "symlink": True, "html": f"<head><link rel=canonical href='{same}'></head>", "url": doc, "expected": same, "exit": EXIT_INPUT, "id": "input_invalid"},
        {"name": "symlink_parent", "symlink_parent": True, "file": "alias/page.html", "html": f"<head><link rel=canonical href='{same}'></head>", "url": doc, "expected": same, "exit": EXIT_INPUT, "id": "input_invalid"},
        {"name": "fifo_html", "fifo": True, "html": "", "url": doc, "expected": same, "exit": EXIT_INPUT, "id": "input_invalid"},
        {"name": "manifest_symlink", "manifest_symlink": True, "html": f"<head><link rel=canonical href='{same}'></head>", "url": doc, "expected": same, "exit": EXIT_INPUT, "id": "input_invalid"},
        {"name": "manifest_dir_caller_prefix", "manifest_prefix_symlink": True, "html": f"<head><link rel=canonical href='{same}'></head>", "url": doc, "expected": same, "exit": EXIT_CLEAN, "id": None},
    ]


def _run_cli(argv: list[str]) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            [sys.executable, "-B", os.path.abspath(__file__), *argv],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise InputProblem("selftest child CLI did not complete") from exc


def _run_manifest_cli(manifest_path: str) -> tuple[int, str | None]:
    completed = _run_cli(["--manifest", manifest_path, "--json"])
    try:
        payload = json.loads(completed.stdout)
        findings = payload["findings"]
        ids = [finding["id"] for finding in findings]
        actual_id = ids[0] if len(ids) == 1 else ("multiple:" + ",".join(str(item) for item in ids) if ids else None)
    except (json.JSONDecodeError, KeyError, TypeError):
        actual_id = "invalid_json"
    return completed.returncode, actual_id


def _run_selftest_case(root: str, spec: dict[str, object]) -> tuple[int, str | None]:
    case_dir = os.path.join(root, str(spec["name"]))
    os.mkdir(case_dir)
    file_name = str(spec.get("file", "page.html"))
    manifest_dir = case_dir
    run_dir = case_dir
    if spec.get("manifest_prefix_symlink"):
        manifest_dir = os.path.join(case_dir, "real", "sub")
        os.makedirs(manifest_dir)
        os.symlink("real", os.path.join(case_dir, "alias"))
        run_dir = os.path.join(case_dir, "alias", "sub")
    if spec.get("symlink_parent"):
        target_dir = os.path.join(case_dir, "real")
        os.mkdir(target_dir)
        with open(os.path.join(target_dir, "page.html"), "w", encoding="utf-8", newline="") as stream:
            stream.write(str(spec["html"]))
        os.symlink("real", os.path.join(case_dir, "alias"))
    elif spec.get("fifo"):
        os.mkfifo(os.path.join(case_dir, file_name), 0o600)
    elif spec.get("symlink"):
        target = os.path.join(case_dir, "target.html")
        with open(target, "w", encoding="utf-8", newline="") as stream:
            stream.write(str(spec["html"]))
        os.symlink("target.html", os.path.join(case_dir, "page.html"))
    elif file_name == "../outside.html":
        with open(os.path.join(root, "outside.html"), "w", encoding="utf-8", newline="") as stream:
            stream.write("<head></head>")
    else:
        with open(os.path.join(manifest_dir, file_name), "w", encoding="utf-8", newline="") as stream:
            stream.write(str(spec["html"]))
    manifest = {
        "version": 1,
        "pages": [{"url": spec["url"], "file": file_name, "expectedCanonical": spec["expected"]}],
    }
    manifest_name = "manifest-target.json" if spec.get("manifest_symlink") else "manifest.json"
    with open(os.path.join(manifest_dir, manifest_name), "w", encoding="utf-8", newline="") as stream:
        json.dump(manifest, stream)
    if spec.get("manifest_symlink"):
        os.symlink(manifest_name, os.path.join(manifest_dir, "manifest.json"))
    return _run_manifest_cli(os.path.join(run_dir, "manifest.json"))


def selftest() -> int:
    records: list[dict[str, object]] = []
    try:
        with tempfile.TemporaryDirectory(prefix="canonical-audit-selftest-") as root:
            for spec in _selftest_specs():
                actual_exit, actual_id = _run_selftest_case(root, spec)
                expected_exit = int(spec["exit"])
                expected_id = spec["id"]
                records.append({
                    "name": spec["name"],
                    "expected": {"exit": expected_exit, "id": expected_id},
                    "actual": {"exit": actual_exit, "id": actual_id},
                    "ok": actual_exit == expected_exit and actual_id == expected_id,
                })
            empty_manifest_dir = os.path.join(root, "empty_manifest")
            os.mkdir(empty_manifest_dir)
            empty_manifest_path = os.path.join(empty_manifest_dir, "manifest.json")
            with open(empty_manifest_path, "w", encoding="utf-8", newline="") as stream:
                json.dump({"version": 1, "pages": []}, stream)
            empty_exit, empty_id = _run_manifest_cli(empty_manifest_path)
            records.append({
                "name": "empty_manifest",
                "expected": {"exit": EXIT_INPUT, "id": "input_invalid"},
                "actual": {"exit": empty_exit, "id": empty_id},
                "ok": empty_exit == EXIT_INPUT and empty_id == "input_invalid",
            })
            duplicate_dir = os.path.join(root, "duplicate_pages")
            os.mkdir(duplicate_dir)
            with open(os.path.join(duplicate_dir, "page.html"), "w", encoding="utf-8", newline="") as stream:
                stream.write("<head><link rel=canonical href='https://example.test/project/a.html'></head>")
            duplicate_page = {"url": "https://example.test/project/a.html", "file": "page.html",
                              "expectedCanonical": "https://example.test/project/a.html"}
            duplicate_path = os.path.join(duplicate_dir, "manifest.json")
            with open(duplicate_path, "w", encoding="utf-8", newline="") as stream:
                json.dump({"version": 1, "pages": [duplicate_page, dict(duplicate_page)]}, stream)
            duplicate_exit, duplicate_id = _run_manifest_cli(duplicate_path)
            records.append({
                "name": "duplicate_pages",
                "expected": {"exit": EXIT_INPUT, "id": "input_invalid"},
                "actual": {"exit": duplicate_exit, "id": duplicate_id},
                "ok": duplicate_exit == EXIT_INPUT and duplicate_id == "input_invalid",
            })
        for name, argv in (
            ("cli_missing_mode", []),
            ("cli_unknown_flag", ["--not-a-flag"]),
            ("cli_missing_manifest_path", ["--manifest"]),
            ("cli_conflicting_modes", ["--selftest", "--manifest", "x"]),
            ("cli_json_with_selftest", ["--selftest", "--json"]),
            ("cli_abbreviated_manifest", ["--man", "x"]),
            ("cli_repeated_manifest", ["--manifest", "x", "--manifest", "y"]),
        ):
            completed = _run_cli(argv)
            actual = completed.returncode
            try:
                usage_json = json.loads(completed.stdout) == USAGE_RESULT
            except json.JSONDecodeError:
                usage_json = False
            records.append({
                "name": name,
                "expected": {"exit": EXIT_USAGE, "id": "usage_json"},
                "actual": {"exit": actual, "id": "usage_json" if usage_json else None},
                "ok": actual == EXIT_USAGE and usage_json,
            })
        help_result = _run_cli(["--help"])
        has_verdict = '"verdict"' in help_result.stdout
        records.append({
            "name": "cli_help",
            "expected": {"exit": EXIT_CLEAN, "id": None},
            "actual": {
                "exit": help_result.returncode,
                "id": "verdict_output" if has_verdict else None,
            },
            "ok": help_result.returncode == EXIT_CLEAN and not has_verdict,
        })
    except (OSError, InputProblem, UnsupportedHTML) as exc:
        print(json.dumps({"tool": "canonical_audit.py", "selftest": {"passed": False, "error": str(exc), "cases": records}}, sort_keys=True))
        return EXIT_INPUT

    passed = all(bool(record["ok"]) for record in records)
    print(json.dumps({"tool": "canonical_audit.py", "selftest": {"passed": passed, "cases": records}}, sort_keys=True))
    return EXIT_CLEAN if passed else EXIT_POLICY


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    try:
        args = parse_cli(argv)
    except UsageError as exc:
        print(f"canonical_audit.py: {exc}\n{usage()}", file=sys.stderr, end="")
        print(json.dumps(USAGE_RESULT, sort_keys=True, separators=(",", ":")))
        return EXIT_USAGE
    if args.selftest:
        return selftest()
    result = audit_manifest(args.manifest)
    print(json.dumps(public_result(result), sort_keys=True, separators=(",", ":")))
    return int(result["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
