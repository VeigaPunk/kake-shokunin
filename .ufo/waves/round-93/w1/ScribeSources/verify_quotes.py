#!/usr/bin/env python3
"""ScribeSources round-93: verify every Gate quote against the retained RFC bodies.

Reads the bodies this seat fetched (w1/ScribeSources/src/rfc9110.txt, rfc9111.txt),
checks each quote is an exact substring of the cited plain-text line span, and
counts its words against the <=25-word Gate rule.
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")

ADMITS = [
    ("9110", "13.2.2", 6233, 6234,
     "A recipient cache or origin server MUST evaluate the request preconditions defined by this specification in the following order"),
    ("9110", "13.1.1", 5794, 5795,
     "An origin server MUST use the strong comparison function when comparing entity tags for If-Match"),
    ("9110", "13.1.2", 5880, 5881,
     "A recipient MUST use the weak comparison function when comparing entity tags for If-None-Match"),
    ("9110", "13.1.3", 5956, 5957,
     "A recipient MUST ignore If-Modified-Since if the request contains an If-None-Match header field"),
    ("9110", "13.1.3", 5963, 5966,
     "the request method is neither GET nor HEAD"),
    ("9110", "13.1.4", 6037, 6038,
     "A recipient MUST ignore If-Unmodified-Since if the request contains an If-Match header field"),
    ("9110", "13.1.4", 6072, 6073,
     "earlier than or equal to the date provided in the field value, the condition is true"),
    ("9110", "13.1.2", 5930, 5931,
     "the origin server MUST respond with either a) the 304 (Not Modified) status code if the request method is GET or HEAD"),
    ("9110", "8.8.3.2", 3648, 3649,
     "two entity tags are equivalent if both are not weak and their opaque-tags match character-by-character"),
    ("9111", "4.3.2", 889, 890,
     "the If-Match and If-Unmodified-Since conditional header fields are not applicable to a cache"),
    ("9110", "15.4.5", 7477, 7478,
     "A 304 response is terminated by the end of the header section; it cannot contain content or trailers"),
]


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def main():
    bodies = {}
    for tag, name in (("9110", "rfc9110.txt"), ("9111", "rfc9111.txt")):
        p = os.path.join(SRC, name)
        raw = open(p, "rb").read()
        bodies[tag] = {
            "path": p,
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "lines": raw.decode("utf-8", "replace").split("\n"),
        }
    out = {"bodies": {t: {k: v for k, v in b.items() if k != "lines"} for t, b in bodies.items()},
           "admits": [], "all_ok": True}
    for tag, sec, s, e, quote in ADMITS:
        span = "\n".join(bodies[tag]["lines"][s - 1:e])
        n = norm(span)
        ok = quote in n
        words = len(quote.split())
        rec = {"body": tag, "section": sec, "lines": f"{s}-{e}", "words": words,
               "words_le_25": words <= 25, "exact_substring_of_span": ok, "quote": quote}
        out["admits"].append(rec)
        if not (ok and words <= 25):
            out["all_ok"] = False
            rec["span_text"] = n
    json.dump(out, open(os.path.join(HERE, "quotes.json"), "w"), indent=1)
    for r in out["admits"]:
        print(f"{r['body']} §{r['section']} lines {r['lines']:>9}  words={r['words']:>2} "
              f"<=25:{r['words_le_25']!s:>5}  exact:{r['exact_substring_of_span']}")
    print("ALL_OK" if out["all_ok"] else "FAIL")
    return 0 if out["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
