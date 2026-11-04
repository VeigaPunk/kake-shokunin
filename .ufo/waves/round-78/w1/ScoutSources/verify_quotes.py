#!/usr/bin/env python3
"""Locate each candidate quote in the retained raw bytes and the stripped text.

Matcher (documented in the report, same family as round-77's crosswalk):
  * For the stripped .txt, whitespace runs are collapsed to one space; a match maps back to
    the 1-based line range of the .txt.
  * For the raw .raw, inline tags are skipped, entities are decoded, whitespace runs are
    collapsed, and every emitted character carries its raw byte span. A match therefore has
    an exact raw byte range: `bytes a..b`, the first through the last matched character.
    `contig` is true when raw[a:b] is byte-identical to the quote (no markup crossed).

Exit 1 if any quote exceeds 25 words, contains a pipe, or does not occur in the stripped text.
"""
import html
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
QUOTES = json.loads((HERE / "quotes.json").read_text(encoding="utf-8"))


def collapse(s: str) -> str:
    return " ".join(s.split())


def align_text(text: str):
    """Normalized text plus, per emitted char, the source char index range."""
    chars, spans = [], []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c.isspace():
            j = i
            while j < n and text[j].isspace():
                j += 1
            chars.append(" ")
            spans.append((i, j))
            i = j
        else:
            chars.append(c)
            spans.append((i, i + 1))
            i += 1
    return "".join(chars), spans


def align_html(raw: str):
    chars, spans = [], []
    i, n = 0, len(raw)
    while i < n:
        if raw[i] == "<":
            j = raw.find(">", i)
            if j == -1:
                i += 1
                continue
            i = j + 1
            continue
        if raw[i] == "&":
            j = raw.find(";", i)
            if j != -1 and j - i <= 12:
                token = raw[i:j + 1]
                decoded = html.unescape(token)
                if decoded != token:
                    for c in decoded:
                        chars.append(c)
                        spans.append((i, j + 1))
                    i = j + 1
                    continue
        c = raw[i]
        if c.isspace():
            j = i
            while j < n and raw[j].isspace() and raw[j] != "<":
                j += 1
            chars.append(" ")
            spans.append((i, j))
            i = j
        else:
            chars.append(c)
            spans.append((i, i + 1))
            i += 1
    return "".join(chars), spans


def occurrences(hay: str, needle: str):
    out, i = [], hay.find(needle)
    while i != -1:
        out.append(i)
        i = hay.find(needle, i + 1)
    return out


def main() -> int:
    failures = 0
    for q in QUOTES:
        base, needle = q["base"], collapse(q["quote"])
        words = len(needle.split())
        raw_bytes = (HERE / f"{base}.raw").read_bytes()
        txt = (HERE / f"{base}.txt").read_text(encoding="utf-8")

        t_norm, t_spans = align_text(txt)
        t_hits = occurrences(t_norm, needle)
        line_starts = [0] + [m.end() for m in __import__("re").finditer("\n", txt)]
        import bisect
        tloc = []
        for p in t_hits:
            a, b = t_spans[p][0], t_spans[p + len(needle) - 1][1]
            la = bisect.bisect_right(line_starts, a)
            lb = bisect.bisect_right(line_starts, b - 1)
            tloc.append(f"{la}-{lb}" if la != lb else str(la))

        r_norm, r_spans = (align_html(raw_bytes.decode("utf-8", "replace")))
        r_hits = occurrences(r_norm, needle)
        rloc, contig = [], []
        for p in r_hits:
            a = r_spans[p][0]
            b = r_spans[p + len(needle) - 1][1]
            rloc.append(f"{a}..{b}")
            contig.append(raw_bytes[a:b] == needle.encode("utf-8"))

        ok = words <= 25 and "|" not in needle and bool(t_hits)
        failures += 0 if ok else 1
        tr = ",".join(tloc) or "MISSING"
        rr = ",".join(rloc) or "MISSING"
        flag = "contig" if r_hits and all(contig) else ("split" if r_hits else "RAW-MISSING")
        print(f"{q['id']} | w={words} | {base}.txt:{tr} n={len(t_hits)} | "
              f"raw bytes {rr} n={len(r_hits)} {flag} | {needle}")
    print(f"quotes={len(QUOTES)} failures={failures}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
