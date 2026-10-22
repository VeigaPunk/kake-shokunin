#!/usr/bin/env python3
"""Offline static Open Graph link-preview audit.

Read local HTML pages named by a version-1 JSON manifest and check the
Open Graph properties used in link previews. The required og:title,
og:type, og:image and og:url properties follow S067 ("The four required
properties for every page are"). The single og:type rule follows S068. The
`og:url` multiplicity rule follows round-35 C1 lane policy by analogy with
S068's single-og:type rule. Ignoring metadata and canonical links inside open
`<template>`, `<svg>` or `<math>` elements is also round-35 lane policy; no
opened source states that parser rule.
The og:url-versus-canonical-link comparison is lane policy: S067 and S068
define og:url as "the canonical URL" of the object or page, but neither names
a `<link rel=canonical>` element, so equating the two is the lane's inference.
The absolute-og:url rule is also lane policy (no opened source states it).
This tool never opens a network connection and never writes to disk.

What this tool checks
---------------------
The source HTML for each manifest page, parsed with html.parser. It reports
missing required Open Graph properties, multiple non-empty og:type and og:url
elements, an og:url that is not an absolute HTTP(S) URL with a host, and an
og:url that differs from the first eligible canonical link after resolving that
link against the manifest page URL. Meta and link start tags inside an open
template, svg or math element are ignored. Containers close at matching end
tags, nesting is counted, and a self-closed svg opens nothing. Canonical
comparison is an exact string comparison after stripping ASCII whitespace.

What this tool does NOT check
-----------------------------
* the rendered DOM or JavaScript-injected tags;
* whether an og:image can be fetched, its size or its type;
* twitter:card tags;
* tag position: a tag in <body> counts the same as one in <head>;
* the absolute-URL and canonical checks beyond the first non-empty og:url;
  later values are counted only for the lane-policy `og_url_multiple` finding;
* <meta name="og:..."> forms: only the property attribute counts, although
  some consumers also read name (S073: "The key comes from name if present,
  otherwise from property");
* which <link rel=canonical> is first: the first eligible link in the document
  counts, except links inside an open <template>, <svg> or <math>; a canonical
  link without href is skipped;
* a <base> element: a relative canonical href resolves against the manifest
  page URL, unlike scripts/canonical_audit.py, which honours <base>; and
* whether og:url, the canonical link and any sitemap entry are the URL the
  host actually serves.

Manifest files and referenced HTML are read locally only. Manifest-level input
problems produce a could-not-evaluate result without auditing pages. An
unreadable page produces a could-not-evaluate result while readable pages are
still audited and their policy findings are reported beside the input finding.
Policy findings without input problems produce failed-policy. Exit codes: 0
clean, 1 failed-policy, 2 could-not-evaluate, 64 usage.
"""
from __future__ import annotations

import argparse
import json
import sys

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit

EXIT_CLEAN = 0
EXIT_POLICY = 1
EXIT_INPUT = 2
EXIT_USAGE = 64

ASCII_WHITESPACE = " \t\n\r\f"
# Round-34 wave 2 (ReviewLinkPreviewTool M2): reads are bounded so an
# oversized file is an input finding, not a memory exhaustion.
MAX_PAGE_BYTES = 16 * 1024 * 1024
MAX_MANIFEST_BYTES = 4 * 1024 * 1024
REQUIRED_PROPERTIES = ("og:title", "og:type", "og:image", "og:url")
PROPERTY_ALIASES = {"og:image:url": "og:image"}
SUPPRESSED_ELEMENTS = frozenset(("template", "svg", "math"))


class UsageError(Exception):
    """Invalid command-line shape."""


class LinkPreviewArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise UsageError(message)


class MetadataParser(HTMLParser):
    """Collect relevant tags outside open template, svg and math elements."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.properties: dict[str, list[str]] = {name: [] for name in REQUIRED_PROPERTIES}
        self.canonical_href: str | None = None
        self.suppressed_elements: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in SUPPRESSED_ELEMENTS:
            self.suppressed_elements.append(tag)
            return
        if self.suppressed_elements:
            return
        self._collect_metadata(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        # A matching end tag closes that element and any nested suppressed
        # elements, while a nested same-name element keeps its parent open.
        for index in range(len(self.suppressed_elements) - 1, -1, -1):
            if self.suppressed_elements[index] == tag:
                del self.suppressed_elements[index:]
                break

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        # Self-closed tags open nothing, including <svg/>.
        if not self.suppressed_elements and tag not in SUPPRESSED_ELEMENTS:
            self._collect_metadata(tag, attrs)

    def _collect_metadata(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        # The first occurrence of a duplicated attribute wins, as in an HTML
        # tree builder (round-34 wave 2: dict(attrs) kept the last one).
        attributes: dict[str, str | None] = {}
        for key, val in attrs:
            attributes.setdefault(key, val)
        if tag == "meta":
            prop = attributes.get("property")
            # S067: "og:image:url - Identical to og:image".
            prop = PROPERTY_ALIASES.get(prop, prop) if prop is not None else None
            content = attributes.get("content")
            if prop in self.properties and content is not None:
                value = content.strip(ASCII_WHITESPACE)
                if value:
                    self.properties[prop].append(value)
        elif tag == "link" and self.canonical_href is None:
            rel = attributes.get("rel")
            href = attributes.get("href")
            if rel is not None and href is not None and "canonical" in rel.lower().split():
                self.canonical_href = href.strip(ASCII_WHITESPACE)

def absolute_http_url(value: str) -> bool:
    try:
        parsed = urlsplit(value)
        return parsed.scheme.lower() in {"http", "https"} and bool(parsed.hostname)
    except ValueError:
        return False


def input_finding(reason: str, page: str | None = None) -> dict[str, object]:
    return {
        "id": f"{reason}:{page or ''}",
        "reason": reason,
        "page": page,
        "property": None,
    }


def result(verdict: str, pages_checked: int, findings: list[dict[str, object]]) -> dict[str, object]:
    return {"verdict": verdict, "pagesChecked": pages_checked, "findings": findings}


def _no_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    # Round-34 wave 2 (ReviewLinkPreviewTool L3): a duplicated JSON key is
    # input_invalid, not "last one wins".
    seen: dict[str, object] = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError("manifest repeats a JSON key")
        seen[key] = value
    return seen


def load_manifest(path: str) -> tuple[Path, list[dict[str, str]]]:
    manifest = Path(path)
    manifest_dir = manifest.parent.resolve()
    try:
        if manifest.stat().st_size > MAX_MANIFEST_BYTES:
            raise ValueError("manifest is larger than the read bound")
        value = json.loads(manifest.read_text(encoding="utf-8"), object_pairs_hook=_no_duplicate_keys)
    except (OSError, UnicodeError, ValueError, RecursionError) as exc:
        raise ValueError("manifest cannot be read as UTF-8 JSON") from exc
    if not isinstance(value, dict) or set(value) != {"version", "pages"}:
        raise ValueError("manifest must contain version and pages")
    if type(value["version"]) is not int or value["version"] != 1:
        raise ValueError("manifest version must be 1")
    pages = value["pages"]
    if not isinstance(pages, list) or not pages:
        raise ValueError("manifest pages must be a non-empty array")

    normalized: list[dict[str, str]] = []
    for page in pages:
        if not isinstance(page, dict) or set(page) != {"file", "url"}:
            raise ValueError("each page must contain file and url")
        file_name = page["file"]
        page_url = page["url"]
        if not isinstance(file_name, str) or not file_name or not isinstance(page_url, str) or not page_url:
            raise ValueError("page file and url must be non-empty strings")
        if not absolute_http_url(page_url):
            raise ValueError("page URL must be an absolute HTTP(S) URL with a host")
        file_path = Path(file_name)
        if file_path.is_absolute():
            raise ValueError("page file must be relative to the manifest directory")
        try:
            resolved = (manifest_dir / file_path).resolve()
            resolved.relative_to(manifest_dir)
        except (OSError, RuntimeError, ValueError) as exc:
            raise ValueError("page file resolves outside the manifest directory") from exc
        normalized.append({"file": file_name, "url": page_url})
    return manifest_dir, normalized


def audit_manifest(path: str) -> tuple[dict[str, object], int]:
    try:
        manifest_dir, pages = load_manifest(path)
    except (OSError, UnicodeError, ValueError, RecursionError):
        return result("could-not-evaluate", 0, [input_finding("input_invalid")]), EXIT_INPUT

    documents: list[tuple[str, str]] = []
    input_findings: list[dict[str, object]] = []
    for page in pages:
        page_url = page["url"]
        try:
            file_path = (manifest_dir / page["file"]).resolve()
            file_path.relative_to(manifest_dir)
            if not file_path.is_file():
                # A FIFO, device or directory is never opened (round-34 wave 2:
                # a FIFO hung the read).
                raise OSError("page is not a regular file")
            if file_path.stat().st_size > MAX_PAGE_BYTES:
                raise OSError("page is larger than the read bound")
            text = file_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError, RuntimeError, ValueError):
            # A path escape is a manifest error; an in-directory unreadable or
            # non-UTF-8 page is a page-read error.
            try:
                file_path = (manifest_dir / page["file"]).resolve()
                file_path.relative_to(manifest_dir)
            except (OSError, RuntimeError, ValueError):
                input_findings.append(input_finding("input_invalid", page_url))
            else:
                input_findings.append(input_finding("page_unreadable", page_url))
            continue
        documents.append((page_url, text))

    if any(finding["reason"] == "input_invalid" for finding in input_findings):
        return result("could-not-evaluate", 0, input_findings), EXIT_INPUT

    findings: list[dict[str, object]] = []
    for page_url, text in documents:
        parser = MetadataParser()
        parser.feed(text)
        parser.close()

        for prop in REQUIRED_PROPERTIES:
            if not parser.properties[prop]:
                findings.append({
                    "id": f"{page_url}:og_required_missing:{prop}",
                    "reason": "og_required_missing",
                    "page": page_url,
                    "property": prop,
                })

        if len(parser.properties["og:type"]) > 1:
            findings.append({
                "id": f"{page_url}:og_type_multiple:og:type",
                "reason": "og_type_multiple",
                "page": page_url,
                "property": "og:type",
            })

        og_urls = parser.properties["og:url"]
        if len(og_urls) > 1:
            findings.append({
                "id": f"{page_url}:og_url_multiple:og:url",
                "reason": "og_url_multiple",
                "page": page_url,
                "property": "og:url",
            })
        if og_urls:
            og_url = og_urls[0]
            if not absolute_http_url(og_url):
                findings.append({
                    "id": f"{page_url}:og_url_not_absolute:og:url",
                    "reason": "og_url_not_absolute",
                    "page": page_url,
                    "property": "og:url",
                })
            elif parser.canonical_href is not None:
                try:
                    canonical_url = urljoin(page_url, parser.canonical_href).strip(ASCII_WHITESPACE)
                except ValueError:
                    # An unparsable canonical href cannot equal og:url (round-34
                    # wave 2: urljoin raised and the tool exited with no JSON).
                    canonical_url = None
                if og_url != canonical_url:
                    findings.append({
                        "id": f"{page_url}:og_url_not_canonical:og:url",
                        "reason": "og_url_not_canonical",
                        "page": page_url,
                        "property": "og:url",
                    })

    if input_findings:
        return result("could-not-evaluate", len(documents), input_findings + findings), EXIT_INPUT
    if findings:
        return result("failed-policy", len(documents), findings), EXIT_POLICY
    return result("clean", len(documents), []), EXIT_CLEAN


def parse_cli(argv: list[str]) -> argparse.Namespace:
    parser = LinkPreviewArgumentParser(
        prog="link_preview_audit.py",
        usage="link_preview_audit.py --manifest PATH",
        allow_abbrev=False,
        description=(
            "Read a UTF-8 JSON manifest v1 of local HTML pages and audit static "
            "Open Graph metadata. No network access or disk writes occur."
        ),
    )
    parser.add_argument("--manifest", metavar="PATH", required=True)
    # Round-34 wave 2 (ReviewLinkPreviewTool L1): a repeated --manifest is a
    # usage error, not "last one wins".
    if sum(1 for token in argv if token == "--manifest" or token.startswith("--manifest=")) > 1:
        raise UsageError("--manifest given more than once")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_cli(sys.argv[1:] if argv is None else argv)
    except UsageError as exc:
        print(f"link_preview_audit.py: {exc}", file=sys.stderr)
        return EXIT_USAGE

    report, exit_code = audit_manifest(args.manifest)
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
