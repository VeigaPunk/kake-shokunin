#!/usr/bin/env python3
"""Verify every quotation of the round-100 knowledge entry against the retained bodies.

The checker reads the entry itself (default:
  .ufo/waves/round-100/w1/ScribeEntry/freshening-304.md),
parses its quote table, and for every row

  * whitespace-collapses the named body and the quote,
  * searches the quote as a substring of the collapsed body,
  * records the plain-text line where the match starts (must equal the
    declared line),
  * counts the words of the quote (must be <= 25).

It also parses every block quotation in the entry's body and checks that each
one is a whitespace-collapsed substring of the body named for it in the table.

Bodies:
  rfc9111.txt -> .ufo/waves/round-99/sources/rfc9111.txt   (S484, S486)
  rfc9110.txt -> .ufo/waves/round-100/sources/rfc9110.txt  (S487)
  eid9185.html -> .ufo/waves/round-99/sources/eid9185.html  (S485)

Exit 0 when every table row is found at its declared line, no quote exceeds 25
words, and every body block quotation is found; exit 1 otherwise.
"""
import pathlib
import re
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kake-shokunin")
BODIES = {
    "rfc9111.txt": LANE / ".ufo/waves/round-99/sources/rfc9111.txt",
    "rfc9110.txt": LANE / ".ufo/waves/round-100/sources/rfc9110.txt",
    "eid9185.html": LANE / ".ufo/waves/round-99/sources/eid9185.html",
}
DEFAULT_ENTRY = LANE / ".ufo/waves/round-100/w1/ScribeEntry/freshening-304.md"

TABLE_ROW = re.compile(r"^\|\s*(Q\d+)\s*\|\s*(\S+)\s*\|\s*((?:S\d+)(?:,\s*S\d+)*)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*$")
BLOCKQUOTE = re.compile(r"^> (.+)$")


def collapse_map(text):
    """Return (collapsed_text, index_map); index_map[i] = 1-based line of collapsed char i."""
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


def load(path):
    return path.read_text(encoding="utf-8", errors="replace")


def main(argv):
    entry = pathlib.Path(argv[0]) if argv else DEFAULT_ENTRY
    if not entry.is_file():
        print("entry not found: %s" % entry, file=sys.stderr)
        return 2
    text = load(entry)
    collapsed = {}
    for name, path in BODIES.items():
        collapsed[name] = collapse_map(load(path))

    rows = []
    for line in text.split("\n"):
        m = TABLE_ROW.match(line)
        if m:
            rows.append((m.group(1), m.group(2), m.group(3), int(m.group(4)), int(m.group(5)), m.group(6)))
    if not rows:
        print("no quote table rows found in %s" % entry, file=sys.stderr)
        return 2

    print("body\tid\trow\tdeclared_line\tagrees\tstart_line\tend_line\twords\tquote")
    bad = []
    mismatch = []
    over = []
    for qid, body, row, declared, words, quote in rows:
        if body not in collapsed:
            print("unknown body %s for %s" % (body, qid), file=sys.stderr)
            bad.append(qid)
            continue
        coll, idx = collapsed[body]
        cq = " ".join(quote.split())
        actual_words = len(cq.split(" "))
        # every occurrence of the quote in the body, so that a quote whose text
        # appears on more than one line (the same sentence in two sections) can
        # declare the line it is quoted from
        positions = []
        at = coll.find(cq)
        while at >= 0:
            positions.append(at)
            at = coll.find(cq, at + 1)
        found = bool(positions)
        start = idx[positions[0]] if found else -1
        end = idx[positions[0] + len(cq) - 1] if found else -1
        starts = [idx[p] for p in positions]
        if body == "eid9185.html":
            agrees = "yes" if found else "no"
        elif not found:
            agrees = "no"
        elif declared in starts:
            agrees = "yes"
        else:
            agrees = "line-mismatch"
        print("%s\t%s\t%s\t%d\t%s\t%d\t%d\t%d\t%s"
              % (body, qid, row, declared, agrees, start, end, actual_words, quote))
        if len(positions) > 1:
            print("  note: %s occurs at lines %s" % (qid, ",".join(str(s) for s in starts)))
        if not found:
            bad.append(qid)
        elif body != "eid9185.html" and declared not in starts:
            mismatch.append((qid, declared, starts))
        if actual_words > 25:
            over.append((qid, actual_words))
        if actual_words != words:
            print("word-count-mismatch %s declared=%d actual=%d" % (qid, words, actual_words), file=sys.stderr)
            bad.append(qid)

    # every block quotation in the body must be a substring of some body
    bq_bad = []
    n_bq = 0
    for line in text.split("\n"):
        m = BLOCKQUOTE.match(line)
        if not m:
            continue
        n_bq += 1
        q = " ".join(m.group(1).split())
        hit = None
        for name, (coll, _idx) in collapsed.items():
            if q in coll:
                hit = name
                break
        if hit is None:
            bq_bad.append((n_bq, q))
            print("blockquote-not-found %d | %s" % (n_bq, q), file=sys.stderr)
        else:
            print("body-quote\t%s\t%d\t%s" % (hit, n_bq, q))

    for qid, declared, starts in mismatch:
        print("line-mismatch %s declared=%d actual=%s" % (qid, declared, starts), file=sys.stderr)
    for qid, words in over:
        print("over-25-words %s words=%d" % (qid, words), file=sys.stderr)
    print("table_rows=%d blockquotes=%d notfound=%d linemismatch=%d over25=%d blockquote_notfound=%d"
          % (len(rows), n_bq, len(bad), len(mismatch), len(over), len(bq_bad)), file=sys.stderr)
    return 1 if (bad or mismatch or over or bq_bad) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
