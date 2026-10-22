#!/usr/bin/env python3
"""Offline static Open Graph link-preview audit.

Read local HTML pages named by a version-1 JSON manifest and check the
Open Graph properties used in link previews. The required og:title,
og:type, og:image and og:url properties follow S067 ("The four required
properties for every page are"). The single og:type rule follows S068.
The og:url-versus-canonical-link comparison is lane policy: S067 and S068
define og:url as "the canonical URL" of the object or page, but neither names
a <link rel=canonical> element, so equating the two is the lane's inference.
The absolute-og:url rule is also lane policy (no opened source states it).
This tool never opens a network connection and never writes to disk.

What this tool checks
---------------------
The source HTML for each manifest page, parsed with html.parser. It reports
missing required Open Graph properties, multiple non-empty og:type elements,
an og:url that is not an absolute HTTP(S) URL with a host, and an og:url that
differs from the first canonical link after resolving that link against the
manifest page URL. Canonical comparison is an exact string comparison after
stripping ASCII whitespace.

What this tool does NOT check
-----------------------------
* the rendered DOM or JavaScript-injected tags;
* whether an og:image can be fetched, its size or its type;
* twitter:card tags;
* tag position: a tag in <body> counts the same as one in <head>;
* <meta name="og:..."> forms: only the property attribute counts, although
  some consumers also read name (S073: "The key comes from name if present,
  otherwise from property");
* a <base> element: a relative canonical href resolves against the manifest
  page URL, unlike scripts/canonical_audit.py, which honours <base>; and
* whether og:url, the canonical link and any sitemap entry are the URL the
  host actually serves.

Manifest files and referenced HTML are read locally only. Input problems
produce a could-not-evaluate result; policy findings produce failed-policy.
Exit codes: 0 clean, 1 failed-policy, 2 could-not-evaluate, 64 usage.
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
REQUIRED_PROPERTIES = ("og:title", "og:type", "og:image", "og:url")


class UsageError(Exception):
    """Invalid command-line shape."""


class LinkPreviewArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise UsageError(message)


class MetadataParser(HTMLParser):
    """Collect relevant meta properties and the first canonical link."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.properties: dict[str, list[str]] = {name: [] for name in REQUIRED_PROPERTIES}
        self.canonical_href: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "meta":
            prop = attributes.get("property")
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

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)


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


def load_manifest(path: str) -> tuple[Path, list[dict[str, str]]]:
    manifest = Path(path)
    manifest_dir = manifest.parent.resolve()
    try:
        value = json.loads(manifest.read_text(encoding="utf-8"))
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

    if input_findings:
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
                canonical_url = urljoin(page_url, parser.canonical_href).strip(ASCII_WHITESPACE)
                if og_url != canonical_url:
                    findings.append({
                        "id": f"{page_url}:og_url_not_canonical:og:url",
                        "reason": "og_url_not_canonical",
                        "page": page_url,
                        "property": "og:url",
                    })

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
