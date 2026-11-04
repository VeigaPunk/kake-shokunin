#!/usr/bin/env python3
r"""Deterministic tag-stripping recipe for round-77 ScoutSources.

Input : protocol.raw (HTML), rfc1952.raw (RFC plain text), rfc4287.raw (RFC plain text)
Output: protocol.txt, rfc1952.txt, rfc4287.txt  (stable text renderings, LF endings)

Recipe HTML (protocol.raw):
  1. drop <script>..</script> and <style>..</style> blocks (dot-all)
  2. emit a newline for </p> </li> </h1..6> </tr> </pre> </div> </dt> </dd> <br>
     and for <li> emit "\n- "
  3. remove every remaining <...> tag
  4. html.unescape entities, map NBSP (\xa0) to space
  5. per line: collapse [ \t]+ to one space, strip leading/trailing space
  6. collapse runs of blank lines to one; strip leading/trailing blank lines

Recipe RFC text (rfc1952.raw, rfc4287.raw):
  1. decode UTF-8, CRLF -> LF
  2. \f (page break) -> "\n"; the line before it is the running footer
     `^.*\[Page N\]$`, the line after it is the running header
     `^RFC NNNN<spaces>title<spaces>Month YYYY$`; both are removed
  3. across a removed page break, if the last non-blank line before it and the first
     non-blank line after it are both text, join them with one space (paragraph
     continuation; no de-hyphenation is performed)
  4. per line: collapse [ \t]+ to one space, strip leading/trailing space
  5. collapse runs of blank lines to one; strip leading/trailing blank lines

Line numbers cited in the registry rows are 1-based line numbers of these .txt files.
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
RUNNING_HEADER = re.compile(
    r"^RFC \d+ +\S.*  +(January|February|March|April|May|June|July|August|"
    r"September|October|November|December) \d{4}$"
)
RUNNING_FOOTER = re.compile(r"^.*\[Page \d+\]$")


def tidy(lines):
    out = []
    for line in lines:
        line = re.sub(r"[ \t]+", " ", line.replace("\xa0", " ")).strip()
        if line == "" and (not out or out[-1] == ""):
            continue
        out.append(line)
    while out and out[-1] == "":
        out.pop()
    while out and out[0] == "":
        out.pop(0)
    return out


def strip_html(raw: str) -> str:
    s = re.sub(r"(?is)<(script|style)\b.*?</\1\s*>", "", raw)
    s = LIST_ITEM.sub("\n- ", s)
    s = BLOCK_END.sub("\n", s)
    s = TAG.sub("", s)
    s = html.unescape(s)
    s = s.replace("\xa0", " ")
    return "\n".join(tidy(s.split("\n"))) + "\n"


def strip_rfc(raw: str) -> str:
    text = raw.replace("\r\n", "\n").replace("\r", "\n")
    pages = [p.split("\n") for p in text.split("\f")]
    kept = []
    for page in pages:
        body = [ln for ln in page]
        while body and body[-1].strip() == "":
            body.pop()
        # footer is the last non-blank line of the page
        if body and RUNNING_FOOTER.match(body[-1].strip()):
            body.pop()
        # header is the first non-blank line of pages after the first
        j = 0
        while j < len(body) and body[j].strip() == "":
            j += 1
        if body and RUNNING_HEADER.match(body[j].strip()):
            body = body[:j] + body[j + 1 :]
        kept.append(body)
    lines = []
    for i, body in enumerate(kept):
        lines.extend(body)
        if i + 1 < len(kept):
            lines.append("")  # page seam marker, resolved below
    # join text lines across a page seam with one space
    joined = []
    seam = False
    for line in lines:
        if line == "":
            joined.append("")
            continue
        if joined and joined[-1] == "" and seam:
            joined.pop()
            joined[-1] = joined[-1] + " " + line.strip()
        else:
            joined.append(line)
        seam = False
    return "\n".join(tidy(joined)) + "\n"


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main():
    jobs = [
        ("protocol.raw", "protocol.txt", strip_html),
        ("rfc1952.raw", "rfc1952.txt", strip_rfc),
        ("rfc4287.raw", "rfc4287.txt", strip_rfc),
    ]
    for src, dst, fn in jobs:
        raw = (HERE / src).read_bytes().decode("utf-8")
        text = fn(raw)
        (HERE / dst).write_text(text, encoding="utf-8", newline="\n")
        print(
            f"{src} -> {dst} raw_sha256={hashlib.sha256((HERE / src).read_bytes()).hexdigest()} "
            f"raw_bytes={len((HERE / src).read_bytes())} "
            f"text_sha256={digest(text)} text_bytes={len(text.encode('utf-8'))} "
            f"text_lines={text.count(chr(10))}"
        )


if __name__ == "__main__":
    main()
