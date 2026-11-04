#!/usr/bin/env python3
"""Round-91 ScoutSources: prove every filed quote is a raw substring of the retained body.

Usage: python3 -B quote-check.py <body>   (default: LANE/.ufo/waves/round-91/L1/src/rfc9111.txt)
Prints one line per quote: key, byte offset, 1-based line span, byte length, word count,
occurrence count. Exit 1 if any quote is absent or occurs more than once.
"""
import hashlib
import sys

BODY = sys.argv[1] if len(sys.argv) > 1 else ".ufo/waves/round-91/L1/src/rfc9111.txt"

# (key, section, quote) — quotes are byte-exact, newline and three-space indent included
QUOTES = [
    ("a1", "5.2.1",
     "This section defines cache request directives.  They are advisory;\n"
     "   caches MAY implement them, but are not required to."),
    ("a2", "5.2.1 (single physical line 1113)",
     "This section defines cache request directives.  They are advisory;"),
    ("b1", "5.2.1.2",
     "The max-stale request directive indicates that the client will accept\n"
     "   a response that has exceeded its freshness lifetime."),
    ("b2", "5.2.1.2 (unbounded branch)",
     "If no value is assigned to max-stale, then the client\n"
     "   will accept a stale response of any age."),
    ("b3", "5.2.1.2 (bounded branch)",
     "the client is willing to accept a response that has\n"
     "   exceeded its freshness lifetime by no more than the specified number\n"
     "   of seconds"),
    ("c1", "4.2.4",
     "A cache MUST NOT generate a stale response if it is prohibited by an\n"
     "   explicit in-protocol directive"),
    ("c2", "4.2.4 (directive named)",
     "a must-revalidate response directive"),
    ("d1", "4.2.1",
     "A cache can calculate the freshness lifetime (denoted as\n"
     "   freshness_lifetime) of a response by evaluating the following rules\n"
     "   and using the first match:"),
    ("f1", "5.2.2.10 (finding: s-maxage prohibition)",
     "A shared cache MUST NOT reuse a stale response with s-maxage\n"
     "   to satisfy another request until it has been successfully validated"),
    ("f2", "4.2 (finding: fresh boundary)",
     "A \"fresh\" response is one whose age has not yet exceeded its\n"
     "   freshness lifetime."),
    ("f3", "5.2.2.1 (finding: stale boundary)",
     "considered stale after its age is greater than the specified number\n"
     "   of seconds."),
]

body = open(BODY, "rb").read()
print("body=%s bytes=%d sha256=%s" % (BODY, len(body), hashlib.sha256(body).hexdigest()))
bad = 0
for key, section, q in QUOTES:
    qb = q.encode()
    n = body.count(qb)
    if n != 1:
        print("%-3s %-46s ABSENT-or-ambiguous occurrences=%d" % (key, section, n))
        bad += 1
        continue
    off = body.find(qb)
    first = body.count(b"\n", 0, off) + 1
    last = body.count(b"\n", 0, off + len(qb)) + 1
    print("%-3s %-46s offset=%-6d lines=%d-%d bytes=%-4d words=%d occurrences=1"
          % (key, section, off, first, last, len(qb), len(q.split())))
sys.exit(1 if bad else 0)
