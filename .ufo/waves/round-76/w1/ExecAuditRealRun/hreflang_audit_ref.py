#!/usr/bin/env python3
"""Offline hreflang declaration audit — independent reference build for the
round-76 C2 real-input cross-check. Derived from contract.md as amended by
amendment-1.md and amendment-2.md (A1-A17). Not a copy of any other seat's build.

Static, offline: parses retained local HTML bytes. No network, no headers.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, urlunsplit

EXIT_CLEAN, EXIT_POLICY, EXIT_INPUT, EXIT_USAGE = 0, 1, 2, 64
OUTPUT_VERSION = 1

BCP47 = re.compile(
    r"^[A-Za-z]{2,3}(-[A-Za-z]{4})?(-([A-Za-z]{2}|[0-9]{3}))?(-([A-Za-z0-9]{5,8}|[0-9][A-Za-z0-9]{3}))*$"
)
POLICY_IDS = {
    "hreflang_missing_value",
    "hreflang_invalid_tag",
    "hreflang_relative_href",
    "hreflang_duplicate_pair",
    "hreflang_multiple_xdefault",
    "hreflang_self_missing",
    "hreflang_nonreciprocal",
    "hreflang_canonical_not_self",
}
INFO_IDS = {"hreflang_external_target"}
INPUT_IDS = {"input_unreadable", "input_duplicate_url", "input_url_not_absolute"}
UNSCANNED = {"template", "svg", "math"}  # A13: these subtrees are not scanned
RAW_TEXT = {"script", "style", "title", "textarea"}  # A14: noscript IS scanned
DEFAULT_PORTS = {"http": "80", "https": "443"}


class LinkScan(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[dict[str, str | None]] = []
        self.skip_depth = 0
        self.raw_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in UNSCANNED:
            self.skip_depth += 1
            return
        if tag in RAW_TEXT:
            self.raw_depth += 1
            return
        if tag == "link" and self.skip_depth == 0 and self.raw_depth == 0:
            seen: dict[str, str | None] = {}
            for key, value in attrs:
                key = key.lower()
                if key not in seen:
                    seen[key] = value
            self.links.append(seen)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in UNSCANNED or tag in RAW_TEXT:
            return  # self-closed <svg/> / <math/> opens nothing (A13)
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in UNSCANNED and self.skip_depth:
            self.skip_depth -= 1
        elif tag in RAW_TEXT and self.raw_depth:
            self.raw_depth -= 1


def rel_tokens(link: dict[str, str | None]) -> list[str]:
    value = link.get("rel") or ""
    return [t.lower() for t in re.split(r"[ \t\n\r\f]+", value.strip()) if t]


def tidy(value: str) -> str:
    return value.strip(" \t\n\r\f")


def normalize(url: str) -> str:
    """A3: RFC 3986 normalization — lowercase scheme+host, drop default port,
    remove dot segments, empty path -> '/'. Trailing '/' stays significant."""
    try:
        parts = urlsplit(url)
    except ValueError:
        return url
    scheme = parts.scheme.lower()
    netloc = parts.netloc
    if netloc:
        userinfo, _, hostport = netloc.rpartition("@")
        host, _, port = hostport.partition(":")
        host = host.lower()
        if port and DEFAULT_PORTS.get(scheme) == port:
            port = ""
        netloc = (userinfo + "@" if userinfo else "") + host + (":" + port if port else "")
    path = parts.path
    if not path:
        path = "/"
    else:
        segments: list[str] = []
        for seg in path.split("/"):
            if seg in ("", "."):
                if seg == "" or not segments or segments[-1] != "":
                    segments.append("")
                continue
            if seg == "..":
                while segments and segments[-1] == "":
                    segments.pop()
                if segments:
                    segments.pop()
                continue
            segments.append(seg)
        rebuilt = "/".join(segments)
        path = rebuilt if rebuilt.startswith("/") else "/" + rebuilt
        if path == "":
            path = "/"
    return urlunsplit((scheme, netloc, path, parts.query, parts.fragment))


def is_absolute(url: str) -> bool:
    """A12: scheme plus authority, any scheme."""
    try:
        parts = urlsplit(url)
    except ValueError:
        return False
    return bool(parts.scheme) and bool(parts.netloc)


def valid_tag(value: str) -> bool:
    return value.lower() == "x-default" or bool(BCP47.match(value))


class Declarations:
    def __init__(self, html_bytes: bytes) -> None:
        scan = LinkScan()
        scan.feed(html_bytes.decode("utf-8", "replace"))
        scan.close()
        self.alternates: list[dict[str, str | None]] = []
        self.canonicals: list[str] = []
        for link in scan.links:
            rels = rel_tokens(link)
            if "canonical" in rels:  # A7: a canonical carrying hreflang stays canonical
                if link.get("href") is not None:
                    self.canonicals.append(tidy(link["href"] or ""))
                continue
            if "alternate" not in rels:
                continue
            if "stylesheet" in rels:  # A13
                continue
            if link.get("href") is None:  # A9
                continue
            self.alternates.append(link)


def audit_page(page_id: str, page_url: str, decl: Declarations, index: dict[str, str],
               back: dict[str, list[tuple[str, str]]]) -> list[dict]:
    findings: list[dict] = []

    def add(fid: str, severity: str, **extra: object) -> None:
        findings.append({"id": fid, "severity": severity, "page": page_id, **extra})

    if not decl.alternates:
        return findings

    page_norm = normalize(page_url) if is_absolute(page_url) else page_url
    pairs: dict[tuple[str, str], int] = {}
    xdefaults = 0
    targets: set[str] = set()
    tagged = 0

    for alt in decl.alternates:
        raw_tag = alt.get("hreflang")
        href = tidy(alt.get("href") or "")
        if raw_tag is None or tidy(raw_tag) == "":  # A10
            add("hreflang_missing_value", "policy", href=href)
            continue
        tag = tidy(raw_tag)
        tagged += 1
        if not valid_tag(tag):
            add("hreflang_invalid_tag", "policy", tag=tag)
        if tag.lower() == "x-default":  # A11
            xdefaults += 1
        pairs[(tag.lower(), href)] = pairs.get((tag.lower(), href), 0) + 1
        if not is_absolute(href):
            add("hreflang_relative_href", "policy", tag=tag, href=href)  # A4: nothing else
            continue
        target = normalize(href)
        targets.add(target)
        other = index.get(target)
        if other is None:
            add("hreflang_external_target", "info", tag=tag, href=href)
            continue
        if not any(t == tag.lower() and u == page_norm for t, u in back.get(other, [])):
            add("hreflang_nonreciprocal", "policy", tag=tag, href=href, target=other)

    for (tag, href), count in sorted(pairs.items()):
        if count > 1:
            add("hreflang_duplicate_pair", "policy", tag=tag, href=href, count=count)
    if xdefaults > 1:
        add("hreflang_multiple_xdefault", "policy", count=xdefaults)
    # A page with no tag-bearing alternate has no hreflang declarations, so the
    # self-reference and canonical conditions do not apply to it (the missing
    # value is already the finding for that annotation).
    if tagged and page_norm not in targets:  # A2: once per page
        add("hreflang_self_missing", "policy", url=page_url)

    if decl.canonicals:  # A6: first canonical wins
        resolved = urljoin(page_url, decl.canonicals[0]) if is_absolute(page_url) else decl.canonicals[0]
        canonical_norm = normalize(resolved) if is_absolute(resolved) else resolved
    else:  # A5: absent canonical is self
        canonical_norm = page_norm
    if tagged and canonical_norm != page_norm:  # A2: once per page
        add("hreflang_canonical_not_self", "policy", canonical=decl.canonicals[0] if decl.canonicals else None)
    return findings


def _inside(root: str, path: str) -> bool:
    root_real = os.path.realpath(root)
    path_real = os.path.realpath(path)
    return path_real == root_real or path_real.startswith(root_real + os.sep)


def load_manifest(path: str, root: str) -> tuple[list[dict[str, str]], int]:
    """Return (pages, usage_exit). usage_exit 64 for a non-v1 manifest (A15)."""
    with open(path, "rb") as handle:
        value = json.loads(handle.read().decode("utf-8"))
    if not isinstance(value, dict) or "version" not in value or "pages" not in value:
        return [], EXIT_USAGE
    if type(value["version"]) is not int or value["version"] != 1:
        return [], EXIT_USAGE
    pages = value["pages"]
    if not isinstance(pages, list) or not pages:
        return [], EXIT_USAGE
    out: list[dict[str, str]] = []
    for page in pages:
        if not isinstance(page, dict):
            return [], EXIT_USAGE
        if not all(isinstance(page.get(k), str) and page.get(k) for k in ("id", "file", "url")):
            return [], EXIT_USAGE
        out.append({"id": page["id"], "file": page["file"], "url": page["url"]})
    return out, EXIT_CLEAN


def run(manifest_path: str, root: str) -> dict:
    def envelope(findings: list[dict], page_count: int) -> dict:
        inputs = [f for f in findings if f["id"] in INPUT_IDS]
        policy = [f for f in findings if f["id"] in POLICY_IDS]
        info = [f for f in findings if f["id"] in INFO_IDS]
        code = EXIT_INPUT if inputs else (EXIT_POLICY if policy else EXIT_CLEAN)
        by_id: dict[str, int] = {}
        for f in findings:
            by_id[f["id"]] = by_id.get(f["id"], 0) + 1
        return {
            "version": OUTPUT_VERSION,
            "pages": page_count,
            "findings": findings,
            "counts": {"policy": len(policy), "informational": len(info), "input": len(inputs), "by_id": by_id},
            "exit": code,
        }

    try:
        pages, usage = load_manifest(manifest_path, root)
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError):
        return envelope([{"id": "input_unreadable", "severity": "input", "page": None}], 0)
    if usage == EXIT_USAGE:
        return {**envelope([], 0), "exit": EXIT_USAGE}

    findings: list[dict] = []
    urls = [p["url"] for p in pages]
    for url in sorted({u for u in urls if urls.count(u) > 1}):
        findings.append({"id": "input_duplicate_url", "severity": "input", "page": url})
    files = [p["file"] for p in pages]
    duplicate_files = {f for f in files if files.count(f) > 1}
    for page in pages:
        if not is_absolute(page["url"]):
            findings.append({"id": "input_url_not_absolute", "severity": "input", "page": page["id"]})

    declarations: dict[str, Declarations] = {}
    for page in pages:
        rel = page["file"]
        full = os.path.join(root, rel)
        problem = None
        if os.path.isabs(rel) or not _inside(root, full):
            problem = "file outside root"
        elif os.path.islink(full):
            problem = "file is a symlink"
        elif not os.path.isfile(full):
            problem = "file is absent or not a regular file"
        elif rel in duplicate_files:
            problem = "file shared by two pages"
        if problem is None:
            try:
                with open(full, "rb") as handle:
                    declarations[page["id"]] = Declarations(handle.read())
            except OSError as exc:
                problem = f"unreadable ({exc.strerror})"
        if problem is not None:
            findings.append(
                {"id": "input_unreadable", "severity": "input", "page": page["id"], "file": rel, "detail": problem}
            )

    index = {normalize(p["url"]): p["id"] for p in pages if is_absolute(p["url"])}
    back: dict[str, list[tuple[str, str]]] = {}
    for page in pages:
        decl = declarations.get(page["id"])
        if decl is None:
            continue
        rows: list[tuple[str, str]] = []
        for alt in decl.alternates:
            tag = alt.get("hreflang")
            href = tidy(alt.get("href") or "")
            if tag is None or tidy(tag) == "" or not is_absolute(href):
                continue  # A4: relative hrefs take part in no relation
            rows.append((tidy(tag).lower(), normalize(is_absolute(page["url"]) and
                                                      urljoin(page["url"], href) or href)))
        back[page["id"]] = rows

    for page in pages:
        decl = declarations.get(page["id"])
        if decl is None:
            continue
        findings.extend(audit_page(page["id"], page["url"], decl, index, back))

    return envelope(findings, len(pages))


SELFTEST_CASES: list[dict] = []


def _case(name: str, html: str, expect: list[str], url: str = "https://a.test/p/",
          peer: dict | None = None, exit_code: int | None = None) -> None:
    SELFTEST_CASES.append({"name": name, "html": html, "expect": expect, "url": url,
                           "peer": peer, "exit": exit_code})


def _cases() -> None:
    C = "https://a.test/p/"
    _case("clean_self_xdefault", f'<head><link rel="alternate" hreflang="x-default" href="{C}"></head>', [])
    _case("clean_self_en", f'<head><link rel="alternate" hreflang="en" href="{C}"></head>', [])
    _case("missing_value", '<head><link rel="alternate" href="https://a.test/p/"></head>', ["hreflang_missing_value"])
    _case("empty_value_is_missing", '<head><link rel="alternate" hreflang="" href="https://a.test/p/"></head>',
          ["hreflang_missing_value"])
    _case("underscore_tag", f'<head><link rel="alternate" hreflang="en_US" href="{C}"></head>', ["hreflang_invalid_tag"])
    _case("one_letter_tag", f'<head><link rel="alternate" hreflang="e" href="{C}"></head>', ["hreflang_invalid_tag"])
    _case("four_letter_primary", f'<head><link rel="alternate" hreflang="engl" href="{C}"></head>',
          ["hreflang_invalid_tag"])
    _case("bcp47_variant_ok", f'<head><link rel="alternate" hreflang="de-CH-1996" href="{C}"></head>', [])
    _case("upper_tag_ok", f'<head><link rel="alternate" hreflang="ZH-HANT-TW" href="{C}"></head>', [])
    _case("numeric_region_ok", f'<head><link rel="alternate" hreflang="es-419" href="{C}"></head>', [])
    _case("bad_numeric_region", f'<head><link rel="alternate" hreflang="es-41" href="{C}"></head>',
          ["hreflang_invalid_tag"])
    _case("relative_href_not_resolved", '<head><link rel="alternate" hreflang="en" href="/p/"></head>',
          ["hreflang_relative_href", "hreflang_self_missing"])
    _case("scheme_relative_href", '<head><link rel="alternate" hreflang="en" href="//a.test/p/"></head>',
          ["hreflang_relative_href", "hreflang_self_missing"])
    _case("link_without_href_is_not_alternate", '<head><link rel="alternate" hreflang="en"></head>', [])
    _case("stylesheet_alternate_skipped", f'<head><link rel="stylesheet alternate" hreflang="en_US" href="/x"></head>',
          [])
    _case("duplicate_pair",
          f'<head><link rel="alternate" hreflang="en" href="{C}"><link rel="alternate" hreflang="EN" href="{C}"></head>',
          ["hreflang_duplicate_pair"])
    _case("two_xdefault",
          f'<head><link rel="alternate" hreflang="x-default" href="{C}">'
          f'<link rel="alternate" hreflang="X-Default" href="{C}"></head>',
          ["hreflang_duplicate_pair", "hreflang_multiple_xdefault"])
    _case("self_missing", '<head><link rel="alternate" hreflang="en" href="https://a.test/other/"></head>',
          ["hreflang_self_missing"])
    _case("canonical_not_self",
          f'<head><link rel="canonical" href="https://a.test/other/"><link rel="alternate" hreflang="en" href="{C}"></head>',
          ["hreflang_canonical_not_self"])
    _case("canonical_self",
          f'<head><link rel="canonical" href="{C}"><link rel="alternate" hreflang="en" href="{C}"></head>', [])
    _case("canonical_absent_is_self",
          f'<head><link rel="alternate" hreflang="en" href="{C}"></head>', [])
    _case("first_canonical_wins",
          f'<head><link rel="canonical" href="{C}"><link rel="canonical" href="https://a.test/other/">'
          f'<link rel="alternate" hreflang="en" href="{C}"></head>', [])
    _case("canonical_with_hreflang_is_canonical",
          f'<head><link rel="canonical" hreflang="en" href="{C}"><link rel="alternate" hreflang="en" href="{C}"></head>',
          [])
    _case("script_decoy",
          '<head><script>var s = \'<link rel="alternate" hreflang="en_US" href="/x">\';</script></head>', [])
    _case("comment_decoy", '<head><!-- <link rel="alternate" hreflang="en_US" href="/x"> --></head>', [])
    _case("template_decoy", '<head><template><link rel="alternate" hreflang="en" href="https://a.test/p/"></template></head>',
          [])
    _case("svg_decoy", '<head><svg><link rel="alternate" hreflang="en" href="https://a.test/p/"></svg></head>', [])
    _case("noscript_scanned",
          '<head><noscript><link rel="alternate" hreflang="en_US" href="https://a.test/p/"></noscript></head>',
          ["hreflang_invalid_tag"])
    _case("stylesheet_ignored", '<head><link rel="stylesheet" href="s.css"></head>', [])
    _case("valueless_alternate_has_no_self_condition",
          '<head><link rel="canonical" href="https://a.test/other/">'
          '<link rel="alternate" href="https://a.test/other/"></head>', ["hreflang_missing_value"])
    _case("external_target_info_only",
          '<head><link rel="alternate" hreflang="fr" href="https://z.test/"></head>', ["hreflang_self_missing"])
    _case("trailing_slash_significant",
          '<head><link rel="alternate" hreflang="en" href="https://a.test/p"></head>',
          ["hreflang_self_missing"])
    _case("default_port_equal",
          '<head><link rel="alternate" hreflang="en" href="https://a.test:443/p/"></head>', [])
    _case("nonreciprocal_peer",
          '<head><link rel="alternate" hreflang="en" href="https://b.test/p/"></head>',
          ["hreflang_self_missing", "hreflang_nonreciprocal"],
          peer={"id": "b", "url": "https://b.test/p/",
                "html": '<head><link rel="alternate" hreflang="en" href="https://a.test/other/"></head>'})
    _case("reciprocal_peer",
          '<head><link rel="alternate" hreflang="en" href="https://b.test/p/"></head>',
          ["hreflang_self_missing"],
          peer={"id": "b", "url": "https://b.test/p/",
                "html": '<head><link rel="alternate" hreflang="EN" href="https://a.test/p/"></head>'})


def selftest(work: str) -> int:
    _cases()
    tmp = tempfile.mkdtemp(prefix="hreflang-ref-selftest-", dir=work)
    failures: list[dict] = []
    try:
        for i, case in enumerate(SELFTEST_CASES):
            pages = [{"id": "a", "file": f"a{i}.html", "url": case["url"]}]
            with open(os.path.join(tmp, f"a{i}.html"), "w", encoding="utf-8") as fh:
                fh.write(case["html"])
            if case["peer"]:
                pages.append({"id": case["peer"]["id"], "file": "b.html", "url": case["peer"]["url"]})
                with open(os.path.join(tmp, "b.html"), "w", encoding="utf-8") as fh:
                    fh.write(case["peer"]["html"])
            mpath = os.path.join(tmp, f"m{i}.json")
            with open(mpath, "w", encoding="utf-8") as fh:
                json.dump({"version": 1, "pages": pages}, fh)
            result = run(mpath, tmp)
            got = sorted(f["id"] for f in result["findings"] if f["id"] in POLICY_IDS and f["page"] == "a")
            if got != sorted(case["expect"]):
                failures.append({"name": case["name"], "want": sorted(case["expect"]), "got": got})
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    report = {"verdict": "selftest-pass" if not failures else "selftest-fail",
              "cases": len(SELFTEST_CASES), "failures": failures}
    json.dump(report, sys.stdout, indent=1)
    sys.stdout.write("\n")
    return EXIT_CLEAN if not failures else EXIT_POLICY


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="offline hreflang declaration audit (reference build)")
    parser.add_argument("--manifest")
    parser.add_argument("--root", default=".")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--work")
    args = parser.parse_args(argv)
    work = args.work or os.environ.get("TMPDIR") or tempfile.gettempdir()
    if args.selftest:
        return selftest(work)
    if not args.manifest:
        parser.print_usage(sys.stderr)
        return EXIT_USAGE
    result = run(args.manifest, args.root)
    json.dump(result, sys.stdout, indent=1, sort_keys=True)
    sys.stdout.write("\n")
    return int(result["exit"])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
