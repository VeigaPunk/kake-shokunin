#!/usr/bin/env python3
"""Run the entry's worked examples against the delivered candidate tool
`scripts/conditional_eval.py` (the tool's stdin/stdout contract) and against the
frozen independent positive control, and report both.

The expected values are written from the contract's clauses by hand.
"""
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
CAND = os.path.join(LANE, "scripts/conditional_eval.py")
POS = os.path.join(LANE, ".ufo/waves/round-93/frozen/pos-good.py")


def I(method, exists, etag, lastmod, **req):
    base = {"if_match": None, "if_none_match": None,
            "if_modified_since": None, "if_unmodified_since": None}
    out = {"method": method,
           "current": {"exists": exists, "etag": etag, "last_modified": lastmod},
           "request": base}
    for key, value in req.items():
        if key == "role":
            out["role"] = value
        else:
            base[key] = value
    return out


EXAMPLES = [
    ("W1", "clause 8 (If-Match, strong comparison)",
     I("PUT", True, '"abc"', 500, if_match='"abc"'),
     {"decision": "200", "precondition": None}),
    ("W2", "clause 8 (strong comparison refuses a weak tag)",
     I("PUT", True, '"abc"', 500, if_match='W/"abc"'),
     {"decision": "412", "precondition": "if_match"}),
    ("W3", "clause 8 (If-Match '*' with no representation)",
     I("PUT", False, None, None, if_match="*"),
     {"decision": "412", "precondition": "if_match"}),
    ("W4", "clause 9 (If-Unmodified-Since, equal modification date passes)",
     I("PUT", True, None, 600, if_unmodified_since=600),
     {"decision": "200", "precondition": None}),
    ("W5", "clause 9 (If-Unmodified-Since, newer representation fails)",
     I("PUT", True, None, 700, if_unmodified_since=600),
     {"decision": "412", "precondition": "if_unmodified_since"}),
    ("W6", "clause 10 (If-None-Match, weak comparison on GET is 304)",
     I("GET", True, '"abc"', 500, if_none_match='W/"abc"'),
     {"decision": "304", "precondition": "if_none_match"}),
    ("W7", "clause 10 (If-None-Match on POST is 412)",
     I("POST", True, '"abc"', 500, if_none_match='"abc"'),
     {"decision": "412", "precondition": "if_none_match"}),
    ("W8", "clause 10 (If-None-Match absent representation passes on GET)",
     I("GET", False, None, None, if_none_match="*"),
     {"decision": "200", "precondition": None}),
    ("W9", "clause 11 (If-Modified-Since, equal date is 304)",
     I("GET", True, None, 500, if_modified_since=500),
     {"decision": "304", "precondition": "if_modified_since"}),
    ("W10", "clause 11 (If-Modified-Since ignored on POST)",
     I("POST", True, None, 500, if_modified_since=900),
     {"decision": "200", "precondition": None}),
    ("W11", "clause 7 (cache role skips If-Match and If-Unmodified-Since)",
     I("PUT", True, '"abc"', 700, if_match='"zzz"', if_unmodified_since=600,
       role="cache"),
     {"decision": "200", "precondition": None}),
    ("W12", "clause 10 (If-None-Match takes precedence over If-Modified-Since)",
     I("GET", True, '"abc"', 500, if_none_match='"zzz"', if_modified_since=900),
     {"decision": "200", "precondition": None}),
    ("W13", "clause 12 (no precondition evaluated)",
     I("GET", True, '"abc"', 500),
     {"decision": "200", "precondition": None}),
]

REFUSALS = [
    ("R1", "clause 3 (malformed entity-tag)", I("GET", True, '"a b"', 500)),
    ("R2", "clause 4 ('*' mixed with a tag)",
     I("GET", True, '"1"', 500, if_none_match='*, "1"')),
    ("R3", "clause 1 (date is a string, not an int)",
     I("GET", True, None, 500, if_modified_since="400")),
    ("R4", "clause 1 (date is a bool)", I("GET", True, None, 500, if_unmodified_since=False)),
    ("R5", "clause 2 (absent representation carries a validator)",
     I("GET", False, '"1"', None)),
    ("R6", "clause 1 (unexpected top-level key)",
     dict(I("GET", True, '"1"', 500), extra=1)),
]


def run(tool, payload):
    p = subprocess.run([sys.executable, "-B", tool],
                       input=json.dumps(payload).encode(),
                       capture_output=True)
    if p.returncode != 0:
        return None, "rc=%d %s" % (p.returncode, p.stderr.decode().strip())
    try:
        return json.loads(p.stdout.decode()), None
    except ValueError:
        return None, "non-JSON stdout"


def main():
    bad = 0
    print("== decisions: candidate vs frozen positive control ==")
    for name, clause, payload, expected in EXAMPLES:
        cgot, cwhy = run(CAND, payload)
        pgot, pwhy = run(POS, payload)
        cok = cgot == expected
        pok = pgot == expected
        ok = cok and pok
        if not ok:
            bad += 1
        print("%s %s %s expected=%s candidate=%s positive_control=%s"
              % (name, "ok" if ok else "MISMATCH", clause,
                 json.dumps(expected, sort_keys=True),
                 json.dumps(cgot, sort_keys=True),
                 json.dumps(pgot, sort_keys=True)))
    print("== refusals: candidate and positive control must both refuse ==")
    for name, clause, payload in REFUSALS:
        cgot, cwhy = run(CAND, payload)
        pgot, pwhy = run(POS, payload)
        cok = cgot is None
        pok = pgot is None
        ok = cok and pok
        if not ok:
            bad += 1
        print("%s %s %s candidate_refused=%s positive_refused=%s candidate_reason=%s"
              % (name, "ok" if ok else "MISMATCH", clause, cok, pok,
                 cwhy if cwhy else "-"))
    print("mismatches=%d decisions=%d refusals=%d"
          % (bad, len(EXAMPLES), len(REFUSALS)))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
