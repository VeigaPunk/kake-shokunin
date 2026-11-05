#!/usr/bin/env python3
"""Verify every quote in the round-96 C2 knowledge-entry draft.

Seat ScribeEntry, kake round 96 (hyaku run 15, attempt 1).

Each quote in `knowledge-entry.md` (the draft of
`corpus/knowledge/revalidation-exchange.md`) must be:

  * a raw substring of the retained RFC 9111 body
    `.ufo/waves/round-93/L1/src/rfc9111.txt`
    (sha256 aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e,
     84477 bytes) — byte-identical to the body ScoutRFC fetched this round
    (`.ufo/waves/round-96/w1/ScoutRFC/rfc9111.txt`, `cmp` exit 0);
  * confined to the stated plain-text line span;
  * 3..25 whitespace-separated words;
  * present verbatim in the draft (so the draft cannot drift from the body).

Method: whitespace is collapsed on both sides (the RFC body is hard-wrapped), the
quote is searched inside the collapsed stated span and inside the collapsed whole
body, and the collapsed quote is searched inside the collapsed draft. Exit 0 iff
every quote verifies with no violations.

Run:  python3 -B verify-quotes.py        (exit 0 when violations == 0)
"""
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))

BODY = os.path.join(LANE, ".ufo/waves/round-93/L1/src/rfc9111.txt")
FETCHED = os.path.join(LANE, ".ufo/waves/round-96/w1/ScoutRFC/rfc9111.txt")
DRAFT = os.path.join(HERE, "knowledge-entry.md")
EXPECT_SHA = ("aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e")

# (id, first_line, last_line, quote text)
QUOTES = [
    ("R1", 803, 804,
     "When a cache has one or more stored responses for a requested URI, "
     "but cannot serve any of them"),
    ("R2", 809, 810,
     'This process is known as "validating" or "revalidating" the stored '
     'response.'),
    ("R3", 827, 829,
     "The precondition header fields are then compared by recipients to "
     "determine whether any stored response is equivalent to a current "
     "representation of the resource."),
    ("R4", 848, 850,
     "MUST send the relevant entity tags (using If-Match, If-None-Match, "
     "or If-Range) if the entity tags were provided in the stored "
     "response(s) being validated."),
    ("R5", 852, 854,
     "SHOULD send the Last-Modified value (using If-Modified-Since) if the "
     "request is not for a subrange, a single stored response is being "
     "validated"),
    ("R6", 861, 862,
     "In most cases, both validators are generated in cache validation "
     "requests, even when entity tags are clearly superior"),
    ("R7", 888, 891,
     "In summary, the If-Match and If-Unmodified-Since conditional header "
     "fields are not applicable to a cache, and If-None-Match takes "
     "precedence over If-Modified-Since"),
    ("R8", 935, 936,
     "A 304 (Not Modified) response status code indicates that the stored "
     "response can be updated and reused"),
    ("R9", 938, 940,
     "A full response (i.e., one containing content) indicates that none of "
     "the stored responses nominated in the conditional request are suitable"),
    ("R10", 940, 941,
     "Instead, the cache MUST use the full response to satisfy the request."),
    ("R11", 944, 946,
     "However, if a cache receives a 5xx (Server Error) response while "
     "attempting to validate a response, it can either forward this response"),
    ("R12", 947, 949,
     "the cache can send a previously stored response, subject to its "
     "constraints on doing so (see Section 4.2.4), or retry the validation "
     "request"),
    ("R13", 986, 988,
     "the cache MUST update its header fields with the header fields "
     "provided in the 304 (Not Modified) response, as per Section 3.2"),
]


def norm(text):
    return " ".join(text.split())


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if not os.path.isfile(BODY):
        print("missing body: %s" % BODY)
        return 2
    with open(BODY, encoding="utf-8") as fh:
        raw = fh.read()
    lines = raw.splitlines()
    body_sha = sha256(BODY)
    print("body %s sha256=%s bytes=%d lines=%d" %
          (os.path.relpath(BODY, LANE), body_sha, len(raw.encode("utf-8")),
           len(lines)))
    if os.path.isfile(FETCHED):
        f_sha = sha256(FETCHED)
        same = "IDENTICAL" if f_sha == body_sha else "DIFFERENT"
        print("fetched %s sha256=%s body_vs_fetched=%s" %
              (os.path.relpath(FETCHED, LANE), f_sha, same))
        if f_sha != body_sha:
            print("VIOLATION fetched body differs from the retained body")
            return 1
    else:
        print("fetched body absent; retained body only")
    if body_sha != EXPECT_SHA:
        print("VIOLATION retained body digest != the freeze's expected digest")
        return 1
    print("expected_sha256=%s digest_match=yes" % EXPECT_SHA)

    with open(DRAFT, encoding="utf-8") as fh:
        draft = fh.read()
    draft_flat = norm(draft)

    violations = 0
    for qid, lo, hi, text in QUOTES:
        span = norm("\n".join(lines[lo - 1:hi]))
        needle = norm(text)
        words = len(needle.split())
        in_span = needle in span
        in_file = needle in norm(raw)
        in_draft = needle in draft_flat
        words_ok = 3 <= words <= 25
        ok = in_span and in_file and in_draft and words_ok
        if not ok:
            violations += 1
        print("%s %s lines=%d-%d words=%d span=%s file=%s draft=%s "
              "words_ok=%s" % (qid, "ok" if ok else "VIOLATION", lo, hi, words,
                               in_span, in_file, in_draft, words_ok))
    # every table row in the draft's quote table must name a quote id
    body_ids = set(re.findall(r"^\| (R\d+) \|", draft, re.M))
    missing = sorted(set(q[0] for q in QUOTES) - body_ids)
    extra = sorted(body_ids - set(q[0] for q in QUOTES))
    print("table_ids=%d missing_in_table=%s extra_in_table=%s" %
          (len(body_ids), missing or "none", extra or "none"))
    if missing or extra:
        violations += 1
    print("violations=%d quotes=%d" % (violations, len(QUOTES)))
    return 0 if violations == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
