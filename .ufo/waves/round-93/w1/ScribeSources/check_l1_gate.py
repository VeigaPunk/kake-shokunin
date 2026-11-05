#!/usr/bin/env python3
"""ScribeSources round-93: audit the quotes and line spans of the L1's
already-written `## Gate` section in corpus/lessons/round-93.md against the
RFC bodies this seat fetched itself.

For each (cited span, quoted string) pair taken from the lesson's Gate, this
checks:
  * substring  - the quoted string, whitespace-normalized, occurs in the cited
                 line span of the fetched body (exact-quote test);
  * words      - the quoted string's whitespace word count and whether it is
                 within the <=25-word Gate rule;
  * spanned    - the whole quoted string lies inside the cited span.

Exit 0 if every pair is inside its span; 1 if any pair is not.
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")

# (body, cited-first, cited-last, quoted string) as written in the L1's Gate.
L1_GATE = [
    ("9110", 6229, 6231,
     "A recipient cache or origin server MUST evaluate the request preconditions defined by this specification in the following order"),
    ("9110", 5794, 5795,
     "An origin server MUST use the strong comparison function when comparing entity tags for If-Match"),
    ("9110", 5880, 5881,
     "A recipient MUST use the weak comparison function when comparing entity tags for If-None-Match"),
    ("9110", 3648, 3653,
     "two entity tags are equivalent if both are not weak and their opaque-tags match character-by-character"),
    ("9110", 3648, 3653,
     "two entity tags are equivalent if their opaque-tags match character-by-character, regardless of either or both being tagged as 'weak'"),
    ("9110", 5930, 5933,
     "the origin server MUST respond with either a) the 304 (Not Modified) status code if the request method is GET or HEAD or b) the 412"),
    ("9110", 5956, 5958,
     "A recipient MUST ignore If-Modified-Since if the request contains an If-None-Match header field"),
    ("9110", 5963, 5965,
     "the request method is neither GET nor HEAD"),
    ("9110", 6037, 6039,
     "A recipient MUST ignore If-Unmodified-Since if the request contains an If-Match header field"),
    ("9110", 6072, 6073,
     "earlier than or equal to the date provided in the field value, the condition is true"),
    ("9111", 889, 891,
     "the If-Match and If-Unmodified-Since conditional header fields are not applicable to a cache"),
]

# Where the quoted text actually lives, located by search over the fetched body.
TRUE_SPANS = [
    ("9110", 6233, 6234, "13.2.2 evaluation-order sentence"),
    ("9110", 5794, 5795, "13.1.1 strong comparison"),
    ("9110", 5880, 5881, "13.1.2 weak comparison"),
    ("9110", 3648, 3649, "8.8.3.2 strong definition"),
    ("9110", 3651, 3653, "8.8.3.2 weak definition (opaque- / tags split across lines)"),
    ("9110", 5928, 5932, "13.1.2 304-or-412 split"),
    ("9110", 5956, 5957, "13.1.3 ignore on If-None-Match"),
    ("9110", 5963, 5966, "13.1.3 ignore on invalid value / non-GET-HEAD method"),
    ("9110", 6037, 6038, "13.1.4 ignore on If-Match"),
    ("9110", 6072, 6073, "13.1.4 true-condition boundary"),
    ("9111", 889, 890, "9111 4.3.2 not-applicable-to-a-cache"),
]


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def main():
    bodies = {}
    for tag, name in (("9110", "rfc9110.txt"), ("9111", "rfc9111.txt")):
        p = os.path.join(SRC, name)
        raw = open(p, "rb").read()
        bodies[tag] = {
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "lines": raw.decode("utf-8", "replace").split("\n"),
        }
    out = {"bodies": {t: {k: v for k, v in b.items() if k != "lines"} for t, b in bodies.items()},
           "pairs": [], "all_spanned": True, "quote_violations": 0}
    for (body, cs, ce, quote), (tbody, ts, te, where) in zip(L1_GATE, TRUE_SPANS):
        span = norm("\n".join(bodies[body]["lines"][cs - 1:ce]))
        tspan = norm("\n".join(bodies[tbody]["lines"][ts - 1:te]))
        in_span = norm(quote) in span
        in_true = norm(quote) in tspan
        words = len(quote.split())
        rec = {"body": body, "cited_span": f"{cs}-{ce}", "quote": quote,
               "words": words, "words_le_25": words <= 25,
               "exact_in_cited_span": in_span,
               "true_location": f"{tbody} {ts}-{te} ({where})",
               "exact_in_true_span": in_true,
               "cited_span_text": span}
        out["pairs"].append(rec)
        if not in_span:
            out["all_spanned"] = False
        if not (in_true and words <= 25):
            out["quote_violations"] += 1
    json.dump(out, open(os.path.join(HERE, "l1-gate-audit.json"), "w"), indent=1)
    print(f"{'body':5} {'cited span':>11} {'w':>3} {'<=25':>5} {'in cited':>9} "
          f"{'in true':>8}  true location")
    for r in out["pairs"]:
        print(f"{r['body']:5} {r['cited_span']:>11} {r['words']:>3} "
              f"{str(r['words_le_25']):>5} {str(r['exact_in_cited_span']):>9} "
              f"{str(r['exact_in_true_span']):>8}  {r['true_location']}")
    print(f"pairs={len(out['pairs'])} quote_violations={out['quote_violations']} "
          f"all_inside_cited_span={out['all_spanned']}")
    return 0 if out["all_spanned"] else 1


if __name__ == "__main__":
    sys.exit(main())
