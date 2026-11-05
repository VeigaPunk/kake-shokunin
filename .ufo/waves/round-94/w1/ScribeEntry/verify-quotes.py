#!/usr/bin/env python3
"""Quote verification for the round-94 knowledge entry (ScribeEntry).

Checks that each located quote the entry cites is an exact whitespace-normalized
substring of the retained RFC 9110 body AND of its own stated plain-text line span.

Body of record: ../ScoutRFC/rfc9110.txt (retained by ScoutRFC in this wave;
sha256 21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a, 502941 bytes).
This seat's own GET returned byte-identical bytes (see fetch.txt).

Run: python3 -B verify-quotes.py     (exit 0 when every span verifies)
"""
import os
import re
import sys

BODY = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    os.pardir, "ScoutRFC", "rfc9110.txt")

QUOTES = [
    ("S477", "9.1", 3748, 3749,
     "The method token is case-sensitive because it might be used as a gateway to "
     "object-based systems with case-sensitive method names."),
    ("S478", "5.6.1", 1670, 1672,
     'each separated by a single comma (",") and optional whitespace (OWS, defined '
     "in Section 5.6.3)."),
    ("S478", "5.6.1.2", 1699, 1702,
     'a recipient MUST accept lists that satisfy the following syntax: #element => '
     '[ element ] *( OWS "," OWS [ element ] )'),
    ("S478", "5.6.3", 1774, 1774, "OWS = *( SP / HTAB )"),
    ("S473", "13.1.2", 5928, 5932,
     "An origin server that evaluates an If-None-Match condition MUST NOT perform the "
     "requested method if the condition evaluates to false; instead, the origin server "
     "MUST respond with either a) the 304 (Not Modified) status code if the request "
     "method is GET or HEAD or b) the 412 (Precondition Failed) status code for all "
     "other request methods."),
    ("S472", "13.1.1", 5799, 5799, 'If-Match = "*" / #entity-tag'),
    ("S473", "13.1.2", 5885, 5885, 'If-None-Match = "*" / #entity-tag'),
]


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def main():
    body = open(BODY, encoding="utf-8").read()
    nb = norm(body)
    lines = body.splitlines()
    bad = 0
    for sid, sec, a, b, quote in QUOTES:
        exact = norm(quote) in nb
        in_span = norm(quote) in norm(" ".join(lines[a - 1:b]))
        if not (exact and in_span):
            bad += 1
        print("%s section %s lines %d-%d exact=%s in_span=%s words=%d"
              % (sid, sec, a, b, exact, in_span, len(norm(quote).split())))
    print("violations %d" % bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
