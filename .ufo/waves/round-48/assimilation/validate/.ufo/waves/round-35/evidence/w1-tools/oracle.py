#!/usr/bin/env python3
"""Offline link-preview contract oracle.

What this tool checks
---------------------
The manifest and static HTML rules in the link-preview audit interface. HTML is
parsed with html5lib's HTML5 tree builder; no network or browser is used.

What this tool does NOT check
-----------------------------
Rendered DOM, script-injected metadata, fetched images, social-platform caches,
or any live preview service.
"""

from __future__ import annotations

import json
import os
import stat
import sys
from pathlib import Path
from urllib.parse import urljoin, urlsplit

from lxml import html

EXIT_CLEAN = 0
EXIT_POLICY = 1
EXIT_INPUT = 2
EXIT_USAGE = 64
PAGE_READ_LIMIT = 16 * 1024 * 1024
ASCII_WHITESPACE = " \t\n\r\f"
REQUIRED_PROPERTIES = ("og:title", "og:type", "og:image", "og:url")
BLOCKING_ANCESTORS = {"template", "svg", "math"}


class InvalidManifest(Exception):
    """The manifest cannot be evaluated under the public interface."""


class UnreadablePage(Exception):
    """A listed page is not a bounded, regular UTF-8 file."""


def _absolute_http_url(value: str) -> bool:
    try:
        parsed = urlsplit(value)
        return parsed.scheme.lower() in {"http", "https"} and bool(parsed.hostname)
    except (ValueError, UnicodeError):
        return False


def _inside(base: Path, candidate: Path) -> bool:
    try:
        return os.path.commonpath((str(base), str(candidate))) == str(base)
    except ValueError:
        return False


def _read_manifest(manifest_arg: str) -> tuple[Path, list[dict[str, str]]]:
    try:
        manifest_path = Path(manifest_arg).resolve()
        if not stat.S_ISREG(manifest_path.stat().st_mode):
            raise InvalidManifest
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, RuntimeError, UnicodeError, ValueError):
        raise InvalidManifest from None

    if not isinstance(manifest, dict) or manifest.get("version") != 1:
        raise InvalidManifest
    pages = manifest.get("pages")
    if not isinstance(pages, list) or not pages:
        raise InvalidManifest

    base = manifest_path.parent.resolve()
    normalized: list[dict[str, str]] = []
    for page in pages:
        if not isinstance(page, dict):
            raise InvalidManifest
        relative_file = page.get("file")
        page_url = page.get("url")
        if not isinstance(relative_file, str) or not relative_file:
            raise InvalidManifest
        if not isinstance(page_url, str) or not _absolute_http_url(page_url):
            raise InvalidManifest
        relative_path = Path(relative_file)
        if relative_path.is_absolute():
            raise InvalidManifest
        try:
            file_path = (base / relative_path).resolve()
        except (OSError, RuntimeError, ValueError):
            raise InvalidManifest from None
        if not _inside(base, file_path):
            raise InvalidManifest
        normalized.append({"file": str(file_path), "url": page_url})
    return base, normalized


def _read_page(filename: str) -> str:
    path = Path(filename)
    try:
        info = path.stat()
        if not stat.S_ISREG(info.st_mode) or info.st_size > PAGE_READ_LIMIT:
            raise UnreadablePage
        with path.open("rb") as source:
            data = source.read(PAGE_READ_LIMIT + 1)
        if len(data) > PAGE_READ_LIMIT:
            raise UnreadablePage
        return data.decode("utf-8")
    except (OSError, UnicodeError):
        raise UnreadablePage from None


def _local_name(tag: object) -> str:
    if not isinstance(tag, str):
        return ""
    return tag.rsplit("}", 1)[-1].lower()


def _ascii_strip(value: str) -> str:
    return value.strip(ASCII_WHITESPACE)


def _html_metadata(markup: str) -> tuple[dict[str, list[str]], list[str], int]:
    root = html.document_fromstring(markup if markup.strip() else "<html></html>")
    properties: dict[str, list[str]] = {name: [] for name in REQUIRED_PROPERTIES}
    canonicals: list[str] = []
    type_elements = 0

    def visit(node: object, blocked: bool = False) -> None:
        nonlocal type_elements
        if not hasattr(node, "tag"):
            return
        name = _local_name(node.tag)
        is_blocked = blocked or name in BLOCKING_ANCESTORS
        if not is_blocked and name == "meta":
            prop = node.attrib.get("property")
            if prop == "og:type":
                type_elements += 1
            content = node.attrib.get("content")
            if prop in properties and content is not None:
                value = _ascii_strip(content)
                if value:
                    properties[prop].append(value)
        elif not is_blocked and name == "link":
            rel = node.attrib.get("rel", "")
            rel_tokens = _ascii_strip(rel).split()
            if "canonical" in {token.lower() for token in rel_tokens if token} and "href" in node.attrib:
                canonicals.append(_ascii_strip(node.attrib["href"]))
        for child in node:
            visit(child, is_blocked)

    visit(root)
    return properties, canonicals, type_elements


def _policy_findings(page_url: str, markup: str) -> list[dict[str, object]]:
    properties, canonicals, type_elements = _html_metadata(markup)
    findings: list[dict[str, object]] = []

    def add(reason: str, prop: str) -> None:
        findings.append(
            {
                "id": f"{page_url}:{reason}:{prop}",
                "reason": reason,
                "page": page_url,
                "property": prop,
            }
        )

    for prop in REQUIRED_PROPERTIES:
        if not properties[prop]:
            add("og_required_missing", prop)

    if type_elements > 1:
        add("og_type_multiple", "og:type")

    urls = properties["og:url"]
    if len(urls) > 1:
        add("og_url_multiple", "og:url")
    if urls:
        og_url = urls[0]
        if not _absolute_http_url(og_url):
            add("og_url_not_absolute", "og:url")
        elif canonicals:
            try:
                canonical_url = urljoin(page_url, canonicals[0])
            except ValueError:
                canonical_url = None
            if og_url != canonical_url:
                add("og_url_not_canonical", "og:url")
    return findings


def _input_finding(reason: str, page: str | None = None) -> dict[str, object]:
    if reason == "page_unreadable":
        finding_id = f"page_unreadable:{page}"
    else:
        finding_id = "input_invalid:"
    return {
        "id": finding_id,
        "reason": reason,
        "page": page,
        "property": None,
    }


def _result(findings: list[dict[str, object]], pages_checked: int, input_problem: bool) -> tuple[int, dict[str, object]]:
    if input_problem:
        verdict, code = "could-not-evaluate", EXIT_INPUT
    elif findings:
        verdict, code = "failed-policy", EXIT_POLICY
    else:
        verdict, code = "clean", EXIT_CLEAN
    return code, {"verdict": verdict, "pagesChecked": pages_checked, "findings": findings}


def _usage() -> int:
    print("usage: link_preview_audit.py --manifest PATH", file=sys.stderr)
    return EXIT_USAGE


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 2 or args[0] != "--manifest" or not args[1] or args[1].startswith("-"):
        return _usage()

    try:
        _base, pages = _read_manifest(args[1])
    except InvalidManifest:
        code, result = _result([_input_finding("input_invalid")], 0, True)
        print(json.dumps(result, sort_keys=True))
        return code

    findings: list[dict[str, object]] = []
    pages_checked = 0
    has_unreadable = False
    for page in pages:
        try:
            markup = _read_page(page["file"])
        except UnreadablePage:
            findings.append(_input_finding("page_unreadable", page["url"]))
            has_unreadable = True
            continue
        pages_checked += 1
        findings.extend(_policy_findings(page["url"], markup))

    code, result = _result(findings, pages_checked, has_unreadable)
    print(json.dumps(result, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
