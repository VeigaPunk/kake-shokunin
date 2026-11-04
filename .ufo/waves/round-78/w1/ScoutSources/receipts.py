#!/usr/bin/env python3
"""Emit quote-receipts.json: per quote, the stripped-text line range, the raw byte span,
the SHA-256 of those raw bytes, and how much inline markup the rendered text crosses.

Matching method (same as verify_quotes.py): inline tags are skipped, entities decoded,
whitespace runs collapsed to one space; every emitted character carries its raw byte
span, so a match yields an exact first..last byte range in the retained .raw file.
"""
import bisect
import hashlib
import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def collapse(s: str) -> str:
    return " ".join(s.split())


def align_text(text: str):
    chars, spans = [], []
    i, n = 0, len(text)
    while i < n:
        if text[i].isspace():
            j = i
            while j < n and text[j].isspace():
                j += 1
            chars.append(" ")
            spans.append((i, j))
            i = j
        else:
            chars.append(text[i])
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
    quotes = json.loads((HERE / "quotes.json").read_text(encoding="utf-8"))
    receipts = []
    for entry in quotes:
        base, needle = entry["base"], collapse(entry["quote"])
        raw = (HERE / f"{base}.raw").read_bytes()
        txt = (HERE / f"{base}.txt").read_text(encoding="utf-8")
        t_norm, t_spans = align_text(txt)
        line_starts = [0] + [m.end() for m in re.finditer("\n", txt)]
        t_lines = []
        for p in occurrences(t_norm, needle):
            a, b = t_spans[p][0], t_spans[p + len(needle) - 1][1]
            la = bisect.bisect_right(line_starts, a)
            lb = bisect.bisect_right(line_starts, b - 1)
            t_lines.append([la, lb])
        r_norm, r_spans = align_html(raw.decode("utf-8", "replace"))
        raw_spans = []
        for p in occurrences(r_norm, needle):
            a = r_spans[p][0]
            b = r_spans[p + len(needle) - 1][1]
            span = raw[a:b]
            raw_spans.append({
                "start": a,
                "end": b,
                "span_sha256": hashlib.sha256(span).hexdigest(),
                "tags_crossed": len(re.findall(rb"<[^>]*>", span)),
                "byte_contiguous": span == needle.encode("utf-8"),
            })
        receipts.append({
            "id": entry["id"], "base": base, "quote": needle,
            "words": len(needle.split()), "txt_lines": t_lines, "raw_spans": raw_spans,
        })
    (HERE / "quote-receipts.json").write_text(json.dumps(receipts, indent=2) + "\n")
    bad = [r["id"] for r in receipts if not r["txt_lines"] or not r["raw_spans"]]
    print(f"receipts={len(receipts)} without_txt={len(bad)}")
    for r in receipts:
        spans = ", ".join(f"{s['start']}..{s['end']} tags={s['tags_crossed']}" for s in r["raw_spans"])
        lines = ",".join(f"{a}-{b}" if a != b else str(a) for a, b in r["txt_lines"])
        print(f"{r['id']} | {r['base']}.txt:{lines} | raw {spans} | w={r['words']}")
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
