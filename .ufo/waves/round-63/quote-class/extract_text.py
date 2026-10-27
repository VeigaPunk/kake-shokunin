#!/usr/bin/env python3
"""Deterministic retained-HTML to flat-text rendering for quote-class derivation.

Round-63 evidence tool. Reads one retained HTML blob and writes a single-line
text rendering with ``textContent`` semantics: character references decoded
exactly once (HTMLParser with convert_charrefs=True), script/style/noscript
content skipped, block-level elements becoming newline boundaries and inline
content concatenated directly, then every whitespace run collapsed to one
ASCII space. The output is byte-stable for a pinned input so a class derived
from it can be re-derived by any reader.

Usage: extract_text.py --raw <input.html> --out <output.txt>
       extract_text.py --selftest
"""
from __future__ import annotations

import argparse
import html.parser
import sys

BLOCK = {
    "address", "article", "aside", "blockquote", "br", "dd", "details", "div",
    "dl", "dt", "figcaption", "figure", "footer", "form", "h1", "h2", "h3",
    "h4", "h5", "h6", "header", "hr", "li", "main", "nav", "ol", "p", "pre",
    "section", "summary", "table", "td", "th", "tr", "ul",
}
SKIP = {"script", "style", "noscript"}


class FlatText(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._skip = 0
        self._parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag in SKIP:
            self._skip += 1
        elif tag in BLOCK:
            self._parts.append("\n")

    def handle_startendtag(self, tag: str, attrs: list) -> None:
        if tag in BLOCK:
            self._parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in SKIP and self._skip:
            self._skip -= 1
        elif tag in BLOCK:
            self._parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self._skip:
            self._parts.append(data)

    def render(self) -> str:
        return " ".join("".join(self._parts).split()) + "\n"


def extract(raw: bytes) -> str:
    parser = FlatText()
    parser.feed(raw.decode("utf-8", errors="replace"))
    parser.close()
    return parser.render()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--raw", help="retained HTML input path")
    ap.add_argument("--out", help="text output path")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        # entity decoded exactly once; inline concat; block boundary; script out
        sample = (
            b"<p>Tom &amp; Jerry</p><script>var a = 1 &lt; 2;</script>"
            b"<p>multi <b>line</b> text</p><p>second</p><p>a<br>b</p>"
        )
        got = extract(sample)
        want = "Tom & Jerry multi line text second a b\n"
        if got != want:
            print(f"selftest FAIL: {got!r} != {want!r}")
            return 1
        if "&lt;" in got or "var a" in got:
            print("selftest FAIL: double-escape or script leak")
            return 1
        print("selftest 1/1")
        return 0

    if not args.raw or not args.out:
        ap.error("--raw and --out are required without --selftest")
    with open(args.raw, "rb") as fh:
        raw = fh.read()
    text = extract(raw)
    with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print(f"extracted {len(raw)} bytes -> {len(text)} chars")
    return 0


if __name__ == "__main__":
    sys.exit(main())
