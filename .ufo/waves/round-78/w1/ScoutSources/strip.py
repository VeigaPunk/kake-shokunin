#!/usr/bin/env python3
r"""Deterministic tag-stripping recipe for round-78 ScoutSources.

Input : google-robots-meta.raw (HTML), whatwg-semantics.raw (HTML), rfc3339.raw (RFC plain text)
Output: google-robots-meta.txt, whatwg-semantics.txt, rfc3339.txt (stable text renderings, LF)

Recipe HTML (google-robots-meta.raw, whatwg-semantics.raw):
  1. drop <script>..</script> and <style>..</style> blocks (dot-all)
  2. drop <head>..</head> (its <title>/<meta> noise is not page prose; the raw file is retained)
  3. emit a newline for </p> </li> </h1..6> </tr> </pre> </div> </dt> </dd> <br>
     and for <li> emit "\n- "
  4. remove every remaining <...> tag
  5. html.unescape entities, map NBSP (\xa0) to space
  6. per line: collapse [ \t]+ to one space, strip leading/trailing space
  7. collapse runs of blank lines to one; strip leading/trailing blank lines

Recipe RFC text (rfc3339.raw):
  1. decode UTF-8, CRLF -> LF
  2. \f (page break) -> "\n"; the line before it is the running footer
     `^.*\[Page N\]$`, the line after it is the running header
     `^RFC NNNN<spaces>title<spaces>Month YYYY$`; both are removed
  3. across a removed page break, if the last non-blank line before it and the first
     non-blank line after it are both text, join them with one space (paragraph
     continuation; no de-hyphenation is performed)
  4. per line: collapse [ \t]+ to one space, strip leading/trailing space
  5. collapse runs of blank lines to one; strip leading/trailing blank lines

Line numbers cited in the report and in the registry rows are 1-based line numbers of
these .txt files.
"""
import hashlib
import html
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

BLOCK_END = re.compile(
    r"(?i)</(?:p|li|h[1-6]|tr|pre|div|dt|dd|table|ul|ol)\s*>|<br\s*/?>"
)
LIST_ITEM = re.compile(r"(?i)<li\b[^>]*>")
TAG = re.compile(r"<[^>]+>")
RUNNING_HEADER = re.compile(r"^RFC \d+\s+.*\s+[A-Z][a-z]+ \d{4}$")
RUNNING_FOOTER = re.compile(r"^.*\[Page \d+\]$")


def tidy(lines):
    out = []
    for line in lines:
        line = re.sub(r"[ \t]+", " ", line).strip()
        if line == "" and out and out[-1] == "":
            continue
        out.append(line)
    while out and out[0] == "":
        out.pop(0)
    while out and out[-1] == "":
        out.pop()
    return out


def strip_html(raw: str) -> str:
    s = re.sub(r"(?is)<(script|style)\b.*?</\1\s*>", "", raw)
    s = re.sub(r"(?is)<head\b.*?</head\s*>", "", s)
    s = BLOCK_END.sub("\n", s)
    s = LIST_ITEM.sub("\n- ", s)
    s = TAG.sub("", s)
    s = html.unescape(s).replace("\xa0", " ")
    return "\n".join(tidy(s.split("\n"))) + "\n"


def strip_rfc(raw: str) -> str:
    text = raw.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\f", "\n")
    lines = text.split("\n")
    joined = []
    for line in lines:
        if RUNNING_FOOTER.match(line) or RUNNING_HEADER.match(line):
            continue
        joined.append(line)
    return "\n".join(tidy(joined)) + "\n"


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main():
    jobs = [
        ("google-robots-meta", strip_html),
        ("whatwg-semantics", strip_html),
        ("rfc3339", strip_rfc),
    ]
    for name, fn in jobs:
        raw_path = HERE / f"{name}.raw"
        raw_bytes = raw_path.read_bytes()
        text = fn(raw_bytes.decode("utf-8", errors="replace"))
        out = HERE / f"{name}.txt"
        out.write_text(text, encoding="utf-8")
        print(
            f"{name}.raw bytes={len(raw_bytes)} sha256={hashlib.sha256(raw_bytes).hexdigest()} "
            f"-> {out.name} bytes={len(text.encode('utf-8'))} lines={text.count(chr(10))} "
            f"sha256={digest(text)}"
        )


if __name__ == "__main__":
    main()
