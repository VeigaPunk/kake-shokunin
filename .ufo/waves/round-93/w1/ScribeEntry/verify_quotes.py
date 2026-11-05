#!/usr/bin/env python3
"""Verify every quote in the round-93 C2 knowledge entry against the fetched bodies.

Each quote must be a raw substring of the stated file, confined to the stated
line span, and 3..25 words.  Prints one line per quote and a final tally.
Exit 0 iff violations=0.
"""
import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
# Prefer a sibling src/ (this seat's live GET bodies); otherwise use the lane's
# COMMITTED retained copies, which receipts.txt proves byte-identical to them.
_SOURCES = [os.path.join(_HERE, "src"),
            os.path.join(_LANE, ".ufo/waves/round-93/L1/src")]
SRC = next((d for d in _SOURCES if os.path.isfile(os.path.join(d, "rfc9110.txt"))),
           _SOURCES[0])

QUOTES = [
    # (id, file, first_line, last_line, text)
    ("Q01", "rfc9110.txt", 6233, 6234,
     "A recipient cache or origin server MUST evaluate the request "
     "preconditions defined by this specification in the following order"),
    ("Q02", "rfc9110.txt", 5794, 5797,
     "An origin server MUST use the strong comparison function when "
     "comparing entity tags for If-Match"),
    ("Q03", "rfc9110.txt", 5880, 5881,
     "A recipient MUST use the weak comparison function when comparing "
     "entity tags for If-None-Match"),
    ("Q04", "rfc9110.txt", 5956, 5957,
     "A recipient MUST ignore If-Modified-Since if the request contains an "
     "If-None-Match header field"),
    ("Q05", "rfc9110.txt", 6037, 6038,
     "A recipient MUST ignore If-Unmodified-Since if the request contains "
     "an If-Match header field"),
    ("Q06", "rfc9110.txt", 3648, 3649,
     '"Strong comparison":  two entity tags are equivalent if both are not '
     "weak and their opaque-tags match character-by-character"),
    ("Q07", "rfc9110.txt", 3651, 3653,
     '"Weak comparison":  two entity tags are equivalent if their opaque- '
     'tags match character-by-character, regardless of either or both '
     'being tagged as "weak"'),
    ("Q08", "rfc9110.txt", 3655, 3656,
     "The example below shows the results for a set of entity tag pairs and "
     "both the weak and strong comparison function results"),
    ("Q09", "rfc9110.txt", 3665, 3665,
     '| W/"1"  | "1"    | no match          | match           |'),
    ("Q10", "rfc9110.txt", 3667, 3667,
     '| "1"    | "1"    | match             | match           |'),
    ("Q11", "rfc9111.txt", 889, 892,
     "the If-Match and If-Unmodified-Since conditional header fields are "
     "not applicable to a cache, and If-None-Match takes precedence over "
     "If-Modified-Since"),
    ("Q12", "rfc9111.txt", 881, 885,
     "A cache MUST NOT evaluate conditional header fields that only apply "
     "to an origin server"),
    ("Q13", "rfc9110.txt", 6236, 6236,
     "When recipient is the origin server and If-Match is present,"),
    ("Q14", "rfc9110.txt", 3659, 3659,
     "| ETag 1 | ETag 2 | Strong Comparison | Weak Comparison |"),
]


def norm(text):
    return " ".join(text.split())


def main():
    bodies = {}
    for name in ("rfc9110.txt", "rfc9111.txt"):
        with open(os.path.join(SRC, name), encoding="utf-8") as fh:
            bodies[name] = fh.read().splitlines()
    violations = 0
    for qid, fname, lo, hi, text in QUOTES:
        lines = bodies[fname]
        span = norm("\n".join(lines[lo - 1:hi]))
        needle = norm(text)
        words = len(needle.split())
        ok_span = needle in span
        # also confirm it is a substring of the whole file
        ok_file = needle in norm("\n".join(lines))
        ok_words = 3 <= words <= 25
        status = "ok" if (ok_span and ok_file and ok_words) else "VIOLATION"
        if status != "ok":
            violations += 1
        print("%s %s %s:%d-%d words=%d span=%s file=%s words_ok=%s"
              % (qid, status, fname, lo, hi, words, ok_span, ok_file, ok_words))
    print("violations=%d quotes=%d" % (violations, len(QUOTES)))
    return 0 if violations == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
