#!/usr/bin/env python3
"""Retained text extraction for round-81 ScoutSources line citations.

Recipe (round-50 quote-class rule: the derived blob is recorded with its own
digest, and a span that survives only whitespace collapse is never called raw):
  1. decode the retained body as UTF-8 with errors='replace'
  2. delete <script>...</script> and <style>...</style> elements, case-insensitive
  3. delete every remaining <...> tag
  4. unescape HTML character references
No whitespace normalisation and no line re-wrapping: the output keeps the
source's own line breaks, which is why a citation's line numbers are stable.

usage: python3 -B extract_text.py <body> <out>
"""
import html
import hashlib
import re
import sys


def extract(raw: bytes) -> str:
    t = raw.decode("utf-8", "replace")
    t = re.sub(r"(?is)<(script|style)\b.*?</\1>", "", t)
    t = re.sub(r"(?s)<[^>]+>", "", t)
    return html.unescape(t)


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 64
    raw = open(sys.argv[1], "rb").read()
    text = extract(raw)
    with open(sys.argv[2], "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"body {sys.argv[1]} bytes={len(raw)} sha256={hashlib.sha256(raw).hexdigest()}")
    print(f"text {sys.argv[2]} bytes={len(text.encode())} sha256={hashlib.sha256(text.encode()).hexdigest()}")
    print(f"lines={text.count(chr(10)) + 1}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
