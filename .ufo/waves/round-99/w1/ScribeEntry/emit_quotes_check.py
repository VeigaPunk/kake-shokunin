#!/usr/bin/env python3
"""Emit quotes-check.txt (every quote in the entry) and erratum-wording-check.txt.

quotes-check.txt rows: body <TAB> id <TAB> line <TAB> found yes|no <TAB> words <TAB> quote
  - rows Q1..Q26 are the RFC 9111 quotations of the entry; the line is the
    plain-text line in .ufo/waves/round-99/sources/rfc9111.txt
  - rows X1..X4 are the erratum quotations of the entry; the line is the line
    of .ufo/waves/round-99/sources/eid9185.html

erratum-wording-check.txt carries the wider errata wording check (all nine
erratum strings verified), with a used_in_entry column.
"""
import subprocess
import sys

CHECK = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-99/w1/ScribeEntry/quotecheck.py"
SEAT = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-99/w1/ScribeEntry"

# erratum quotations that appear verbatim in the entry, in entry order
USED = {"E2": "X1", "E4": "X2", "E5": "X3", "E9": "X4"}

proc = subprocess.run([sys.executable, CHECK], capture_output=True, text=True)
rows = [ln.split("\t") for ln in proc.stdout.strip().split("\n") if ln.strip()]
by_id = {r[0]: r for r in rows}


def line_of(qid):
    return by_id[qid][3]


def found_of(qid):
    return "yes" if by_id[qid][2] == "yes" else "no"


def words_of(qid):
    return by_id[qid][4]


def quote_of(qid):
    return by_id[qid][5]


h1 = [
    "# quote check for .ufo/waves/round-99/w1/ScribeEntry/freshening-304.md",
    "# every quotation that appears in the entry, one row per quotation",
    "# each quote is a whitespace-collapsed substring of the body named in its row",
    "# rows Q* are RFC 9111 (line = plain-text line in rfc9111.txt)",
    "# rows X* are erratum EID 9185 (line = line in eid9185.html)",
    "# body\tid\tline\tfound\twords\tquote",
]
out = []
for n in range(1, 27):
    q = "Q%d" % n
    out.append("%s\t%s\t%s\t%s\t%s\t%s" % ("rfc9111.txt", q, line_of(q), found_of(q), words_of(q), quote_of(q)))
for e, x in USED.items():
    out.append("%s\t%s\t%s\t%s\t%s\t%s" % ("eid9185.html", x, line_of(e), found_of(e), words_of(e), quote_of(e)))
open(SEAT + "/quotes-check.txt", "w", encoding="utf-8").write("\n".join(h1 + out) + "\n")

h2 = [
    "# wording check for erratum EID 9185 as used in the entry's erratum section",
    "# retained body .ufo/waves/round-99/sources/eid9185.html (sha256 83c3b795...)",
    "# used_in_entry says whether the string is quoted verbatim in the entry",
    "# body\tid\tline\tfound\twords\tused_in_entry\tquote",
]
out2 = []
for e in ("E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9"):
    used = USED.get(e, "no")
    out2.append("%s\t%s\t%s\t%s\t%s\t%s\t%s" % ("eid9185.html", e, line_of(e), found_of(e), words_of(e), used, quote_of(e)))
open(SEAT + "/erratum-wording-check.txt", "w", encoding="utf-8").write("\n".join(h2 + out2) + "\n")

print("quotes-check.txt rows=%d erratum-wording-check.txt rows=%d" % (len(out), len(out2)))
print("stderr:", proc.stderr.strip())
sys.exit(0 if proc.returncode == 0 else 1)
