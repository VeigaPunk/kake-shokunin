#!/usr/bin/env python3
"""Stripped-line to raw-line crosswalk for every verified quote.

`<name>.txt` is the tag-stripped rendering (strip.py); `<name>.raw` is the byte-exact
fetch. Both are searched with the same whitespace-collapsed matcher used by
verify_quotes.py, so a row's `lines` column and another artefact's raw offsets can be
reconciled without re-reading either file by hand.

Prints a markdown table plus `quotes=<n> raw_matched=<m> raw_escaped=<e>`.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def collapse(text):
    out = []
    index = []
    prev_space = False
    for i, ch in enumerate(text):
        if ch.isspace():
            if prev_space:
                continue
            out.append(" ")
            index.append(i)
            prev_space = True
        else:
            out.append(ch)
            index.append(i)
            prev_space = False
    return "".join(out), index


def line_of(text, offset):
    return text.count("\n", 0, offset) + 1


def span(text, flat, index, pos, length):
    return f"{line_of(text, index[pos])}-{line_of(text, index[pos + length - 1])}"


def main():
    quotes = json.loads((HERE / "quotes.json").read_text(encoding="utf-8"))["quotes"]
    print("| quote id | stripped lines | raw lines |")
    print("|---|---|---|")
    matched = escaped = failures = 0
    for entry in quotes:
        stripped = (HERE / entry["file"]).read_text(encoding="utf-8")
        raw = (HERE / entry["file"].replace(".txt", ".raw")).read_text(encoding="utf-8")
        flat, index = collapse(stripped)
        qflat, _ = collapse(entry["quote"])
        pos = flat.find(qflat)
        if pos < 0:
            print(f"| {entry['id']} | MISSING | - |")
            failures += 1
            continue
        stripped_span = span(stripped, flat, index, pos, len(qflat))
        rflat, rindex = collapse(raw)
        rpos = rflat.find(qflat)
        if rpos < 0:
            raw_span = "raw:escaped"
            escaped += 1
        else:
            raw_span = span(raw, rflat, rindex, rpos, len(qflat))
            matched += 1
        print(f"| {entry['id']} | {stripped_span} | {raw_span} |")
    print(f"quotes={len(quotes)} raw_matched={matched} raw_escaped={escaped}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
