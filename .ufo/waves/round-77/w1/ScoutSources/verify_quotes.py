#!/usr/bin/env python3
"""Mechanical quote verification for round-77 ScoutSources.

For every entry in quotes.json:
  * collapse whitespace runs in the quote and in the named stripped .txt file,
  * locate the quote, map the match back to 1-based line numbers in the .txt,
  * reject a quote longer than 25 words or containing a pipe character,
  * reject a duplicate id.

Prints one line per quote plus the summary line `quotes=<n> failures=<m>`;
exits 1 when failures > 0.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "quotes.json"
MAX_WORDS = 25


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


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    quotes = manifest["quotes"]
    failures = 0
    seen = set()
    cache = {}
    for entry in quotes:
        qid, fname, quote = entry["id"], entry["file"], entry["quote"]
        if qid in seen:
            print(f"{qid} FAIL duplicate id")
            failures += 1
            continue
        seen.add(qid)
        words = len(quote.split())
        problems = []
        if words > MAX_WORDS:
            problems.append(f"words={words}>{MAX_WORDS}")
        if "|" in quote:
            problems.append("pipe-in-quote")
        if fname not in cache:
            cache[fname] = (HERE / fname).read_text(encoding="utf-8")
        text = cache[fname]
        flat, index = collapse(text)
        qflat, _ = collapse(quote)
        pos = flat.find(qflat)
        if pos < 0:
            problems.append("not-found")
            span = "-"
        else:
            start = index[pos]
            end = index[pos + len(qflat) - 1]
            span = f"{line_of(text, start)}-{line_of(text, end)}"
            occurrence = flat.count(qflat)
            if occurrence != 1:
                problems.append(f"occurrences={occurrence}")
        if problems:
            failures += 1
            print(f"{qid} file={fname} lines={span} words={words} FAIL {','.join(problems)}")
        else:
            print(f"{qid} file={fname} lines={span} words={words} ok")
    print(f"quotes={len(quotes)} failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
