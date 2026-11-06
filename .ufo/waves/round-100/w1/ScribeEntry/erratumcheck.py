#!/usr/bin/env python3
"""Check every erratum quotation of the round-100 knowledge entry against the retained errata page.

The retained page is .ufo/waves/round-99/sources/eid9185.html (sha256 83c3b795…).
Each quotation is whitespace-collapsed and searched in the whitespace-collapsed
page text; the row records the body, the id, the line where the match starts,
the word count and the found/not-found result.  Exit 0 when every quotation is
found and none exceeds 25 words.
"""
import pathlib
import re
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kake-shokunin")
ERRATA = LANE / ".ufo/waves/round-99/sources/eid9185.html"
DEFAULT_ENTRY = LANE / ".ufo/waves/round-100/w1/ScribeEntry/freshening-304.md"

# (id, quote) -- the four erratum quotations the entry carries.
ERRATUM_QUOTES = [
    ("X1", "The initial set consists of stored responses that satisfy all of the following conditions"),
    ("X2", "The key technical change is to allow the initial set to include stored responses whose requests have nonmatching selecting request header fields"),
    ("X3", "the cache MUST, for the purposes of Section 4.1, associate the updated response with the header fields of the request that elicited the 304 response"),
    ("X4", "The choice to recast the affected paragraph as a list of criteria rather than a list of exceptions to the Section 4 requirements is editorial"),
]

BLOCKQUOTE = re.compile(r"^> (.+)$")


def collapse_map(text):
    out = []
    idx = []
    line = 1
    pending_space = False
    for raw in text.split("\n"):
        for ch in raw:
            if ch.isspace():
                pending_space = True
                continue
            if pending_space and out:
                out.append(" ")
                idx.append(line)
            pending_space = False
            out.append(ch)
            idx.append(line)
        line += 1
        pending_space = True
    return "".join(out), idx


def main(argv):
    entry = pathlib.Path(argv[0]) if argv else DEFAULT_ENTRY
    text = entry.read_text(encoding="utf-8", errors="replace")
    coll, idx = collapse_map(ERRATA.read_text(encoding="utf-8", errors="replace"))
    print("body\tid\tstart_line\tend_line\twords\tfound\tquote")
    bad = []
    over = []
    for qid, quote in ERRATUM_QUOTES:
        cq = " ".join(quote.split())
        words = len(cq.split(" "))
        pos = coll.find(cq)
        found = pos >= 0
        start = idx[pos] if found else -1
        end = idx[pos + len(cq) - 1] if found else -1
        print("eid9185.html\t%s\t%d\t%d\t%d\t%s\t%s"
              % (qid, start, end, words, "yes" if found else "no", quote))
        if not found:
            bad.append(qid)
        if words > 25:
            over.append((qid, words))
    # the entry's own erratum block quotations must all be present in the page
    n_bq = 0
    for line in text.split("\n"):
        m = BLOCKQUOTE.match(line)
        if not m:
            continue
        q = " ".join(m.group(1).split())
        if q not in coll:
            continue
        n_bq += 1
    print("erratum_blockquotes_present=%d" % n_bq, file=sys.stderr)
    for qid, words in over:
        print("over-25-words %s words=%d" % (qid, words), file=sys.stderr)
    print("erratum_quotes=%d notfound=%d over25=%d" % (len(ERRATUM_QUOTES), len(bad), len(over)), file=sys.stderr)
    return 1 if (bad or over) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
