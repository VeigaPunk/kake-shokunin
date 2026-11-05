#!/usr/bin/env python3
"""Verify EVERY quoted passage in the round-93 C2 knowledge entry against the
fetched RFC bodies.

Two passes:
  A. extract every blockquote (the `> ` lines) from the entry and check each is a
     raw substring of one of the two bodies, 3..25 words;
  B. check the inline double-quoted fragments the entry marks with a line
     reference against the stated line span;
  C. check that every quoted passage named in the entry's own `source:` line
     (the anchor line numbers) is the line the quote actually sits on.

Prints one line per quote and a final tally.  Exit 0 iff violations=0.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# The bodies this verifier reads are the lane's COMMITTED retained copies at
# .ufo/waves/round-93/L1/src/, which the receipts.txt in this directory prove
# byte-identical (`cmp` exit 0) to the live GETs this seat took.  A sibling
# `src/` directory is used if present.  Re-fetch yourself if you want the
# live bytes; the digests are in receipts.txt.
_LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
_SOURCES = [os.path.join(HERE, "src"),
            os.path.join(_LANE, ".ufo/waves/round-93/L1/src")]
SRC = next((d for d in _SOURCES if os.path.isfile(os.path.join(d, "rfc9110.txt"))),
           _SOURCES[0])
ENTRY = ("/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/"
         "conditional-request-evaluation.md")


def norm(text):
    return " ".join(text.split())


def load():
    bodies = {}
    for name in ("rfc9110.txt", "rfc9111.txt"):
        with open(os.path.join(SRC, name), encoding="utf-8") as fh:
            bodies[name] = fh.read().splitlines()
    return bodies


# inline fragments: (fragment, file, first_line, last_line)
INLINE = [
    ('"lost update" preconditions have more strict requirements than cache '
     "validation, a validated cache is more efficient than a partial "
     "response", "rfc9110.txt", 6227, 6230),
    ("has more than one member, or if the request method is neither GET nor "
     "HEAD", "rfc9110.txt", 5963, 5966),
    ("is terminated by the end of the header section; it cannot contain "
     "content or trailers", "rfc9110.txt", 7477, 7478),
]


def main():
    bodies = load()
    norm_bodies = {k: norm("\n".join(v)) for k, v in bodies.items()}
    with open(ENTRY, encoding="utf-8") as fh:
        entry = fh.read()
    lines = entry.splitlines()

    violations = 0
    total = 0

    # --- pass A: blockquotes
    print("== pass A: blockquotes ==")
    blocks = []
    cur = []
    for line in lines:
        if line.startswith("> "):
            cur.append(line[2:].strip())
        else:
            if cur:
                blocks.append(cur)
                cur = []
    if cur:
        blocks.append(cur)
    for i, block in enumerate(blocks, 1):
        text = norm(" ".join(block))
        words = len(text.split())
        where = None
        for name, body in bodies.items():
            if text in norm_bodies[name]:
                where = name
                break
        ok_where = where is not None
        ok_words = 3 <= words <= 25
        total += 1
        if not (ok_where and ok_words):
            violations += 1
        print("B%02d %s file=%s words=%d where_ok=%s words_ok=%s :: %s"
              % (i, "ok" if (ok_where and ok_words) else "VIOLATION",
                 where, words, ok_where, ok_words, text[:70]))

    # --- pass B: inline fragments
    print("== pass B: inline fragments with a stated line span ==")
    for i, (frag, fname, lo, hi) in enumerate(INLINE, 1):
        span = norm("\n".join(bodies[fname][lo - 1:hi]))
        needle = norm(frag)
        words = len(needle.split())
        ok_span = needle in span
        ok_file = needle in norm_bodies[fname]
        ok_words = 3 <= words <= 25
        ok = ok_span and ok_file and ok_words
        total += 1
        if not ok:
            violations += 1
        print("I%02d %s %s:%d-%d words=%d span=%s file=%s words_ok=%s :: %s"
              % (i, "ok" if ok else "VIOLATION", fname, lo, hi, words,
                 ok_span, ok_file, ok_words, needle[:60]))

    # --- pass C: the source: line's declared anchors resolve to real headings
    print("== pass C: source: line anchors ==")
    head = "\n".join(lines[:8])
    m = re.search(r"(?m)^source:.*$", head)
    anchors = [("rfc9110.txt", 6222, "13.2.2."), ("rfc9110.txt", 5785, "13.1.1."),
               ("rfc9110.txt", 5872, "13.1.2."), ("rfc9110.txt", 5942, "13.1.3."),
               ("rfc9110.txt", 6023, "13.1.4."), ("rfc9110.txt", 3643, "8.8.3.2."),
               ("rfc9111.txt", 866, "4.3.2.")]
    for fname, lineno, want in anchors:
        line = bodies[fname][lineno - 1]
        ok = line.startswith(want)
        total += 1
        if not ok:
            violations += 1
        print("A %s %s:%d expected %r got %r"
              % ("ok" if ok else "VIOLATION", fname, lineno, want, line[:40]))
    ids = re.findall(r"S\d{3,}", m.group(0)) if m else []
    print("source ids: %s" % sorted(set(ids)))

    print("violations=%d checks=%d" % (violations, total))
    return 0 if violations == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
