#!/usr/bin/env python3
"""Cross-check the drafted entry against its own quote table and ledger.

Compares, row by row:
  - the entry's quote table (Q rows),
  - quotes-check.txt (Q and X rows),
  - the entry's own blockquote lines,
and reports any mismatch in body, line, word count or quote text, plus any
quotation over 25 whitespace-separated words.
"""
import os
import re
import sys

SEAT = os.path.dirname(os.path.abspath(__file__))
ENTRY = os.path.join(SEAT, "freshening-304.md")
LEDGER = os.path.join(SEAT, "quotes-check.txt")


def main():
    txt = open(ENTRY, encoding="utf-8").read()
    table = {}
    for m in re.finditer(r"^\| (Q\d+) \| rfc9111\.txt \| (\d+) \| (\d+) \| (.+) \|$", txt, re.M):
        qid, line, words, quote = m.groups()
        table[qid] = ("rfc9111.txt", line, int(words), " ".join(quote.split()))
    ledger = {}
    for ln in open(LEDGER, encoding="utf-8"):
        if ln.startswith("#") or not ln.strip():
            continue
        body, qid, line, found, words, quote = ln.rstrip("\n").split("\t")
        ledger[qid] = (body, line, int(words), " ".join(quote.split()), found)
    bq = [" ".join(l[2:].split()) for l in txt.split("\n") if l.startswith("> ")]

    bad = 0
    for qid, (body, line, words, quote) in sorted(table.items()):
        if qid not in ledger:
            print("MISSING in ledger: %s" % qid)
            bad += 1
            continue
        lb, ll, lw, lq, found = ledger[qid]
        if (lb, ll, lw, lq) != (body, line, words, quote):
            print("DIFF %s table=%s ledger=%s" % (qid, (body, line, words), (lb, ll, lw)))
            bad += 1
        if found != "yes":
            print("NOT FOUND: %s" % qid)
            bad += 1
        if words > 25:
            print("OVER 25 WORDS: %s (%d)" % (qid, words))
            bad += 1
    ledger_quotes = {v[3] for v in ledger.values()}
    for q in bq:
        if q not in ledger_quotes:
            print("BLOCKQUOTE NOT IN LEDGER: %s" % q[:70])
            bad += 1
    for qid, v in ledger.items():
        if v[3] not in bq:
            print("LEDGER ROW NOT IN ENTRY: %s %s" % (qid, v[3][:60]))
            bad += 1
    print("table rows: %d ledger rows: %d blockquotes in entry: %d"
          % (len(table), len(ledger), len(bq)))
    print("mismatches: %d" % bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
