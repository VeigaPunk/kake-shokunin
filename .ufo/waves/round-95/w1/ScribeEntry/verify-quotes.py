#!/usr/bin/env python3
"""Byte-exact quote verification for the round-95 knowledge-entry draft.

Seat ScribeEntry, round 95 (hyaku run 15, attempt 1).

Every quoted fragment in `entry.md` (the draft of
`corpus/knowledge/conditional-list-membership.md`) must be an exact byte
substring of one of the two retained bodies:

  RFC 9110 : .ufo/waves/round-94/w1/ScoutRFC/rfc9110.txt
             (sha256 21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a,
              502941 bytes, retained by ScoutRFC in round 94)
  RFC 8259 : .ufo/waves/round-90/L1/src/rfc8259.txt
             (sha256 61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7,
              28360 bytes, the lane's retained JSON spec body)

Method: for each quoted fragment, run `grep -F -c -- <fragment> <file>` on the
raw bytes (grep -F, no regex, no whitespace normalisation). A fragment is
verified only when grep exits 0 and reports >= 1 matching line. The script
also prints the sha256 of each retained body so the reader can confirm which
bytes were searched.

Run:  python3 -B verify-quotes.py        (exit 0 when every fragment verifies)
"""
import hashlib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))

RFC9110 = os.path.join(LANE, ".ufo/waves/round-94/w1/ScoutRFC/rfc9110.txt")
RFC8259 = os.path.join(LANE, ".ufo/waves/round-90/L1/src/rfc8259.txt")
DRAFT = os.path.join(HERE, "entry.md")

# (label, file, fragment) — fragments are byte-identical to the retained line
# content, indentation included, so grep -F matches the raw bytes.
FRAGMENTS = [
    ("C1-empty-elements", RFC9110,
     "   Empty elements do not contribute to the count of elements present.  A"),
    ("C1-must-accept-a", RFC9110,
     "   recipient MUST parse and ignore a reasonable number of empty list"),
    ("C1-must-accept-b", RFC9110,
     "   elements: enough to handle common mistakes by senders that merge"),
    ("C1-must-accept-c", RFC9110,
     "   values, but not so much that they could be used as a denial-of-"),
    ("C1-must-accept-d", RFC9110,
     "   service mechanism.  In other words, a recipient MUST accept lists"),
    ("C1-must-accept-e", RFC9110,
     "   that satisfy the following syntax:"),
    ("C1-list-syntax", RFC9110,
     "    #element => [ element ] *( OWS \",\" OWS [ element ] )"),
    ("C1-ows", RFC9110,
     "    OWS            = *( SP / HTAB )"),
    ("C2-etagc", RFC9110,
     "     etagc      = %x21 / %x23-7E / obs-text"),
    ("C2-etagc-comment", RFC9110,
     "                ; VCHAR except double quotes, plus obs-text"),
    ("C2-obs-text", RFC9110,
     "     obs-text       = %x80-FF"),
    ("C5-inm-304-412-a", RFC9110,
     "   An origin server that evaluates an If-None-Match condition MUST NOT"),
    ("C5-inm-304-412-b", RFC9110,
     "   perform the requested method if the condition evaluates to false;"),
    ("C5-inm-304-412-c", RFC9110,
     "   instead, the origin server MUST respond with either a) the 304 (Not"),
    ("C5-inm-304-412-d", RFC9110,
     "   Modified) status code if the request method is GET or HEAD or b) the"),
    ("C5-inm-304-412-e", RFC9110,
     "   412 (Precondition Failed) status code for all other request methods."),
    ("C5-ims-ignore-a", RFC9110,
     "   A recipient MUST ignore the If-Modified-Since header field if the"),
    ("C5-ims-ignore-b", RFC9110,
     "   received field value is not a valid HTTP-date, the field value has"),
    ("C5-ims-ignore-c", RFC9110,
     "   more than one member, or if the request method is neither GET nor"),
    ("C5-ims-ignore-d", RFC9110,
     "   HEAD."),
    ("C4-json-unique-names", RFC8259,
     "   name.  The names within an object SHOULD be unique."),
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def grep_fixed_count(fragment, path):
    p = subprocess.run(["grep", "-F", "-c", "--", fragment, path],
                       capture_output=True)
    return p.returncode, p.stdout.decode().strip()


def draft_lines():
    with open(DRAFT, encoding="utf-8") as fh:
        return fh.read().splitlines()


def main():
    for path in (RFC9110, RFC8259):
        if not os.path.isfile(path):
            print("MISSING retained body: %s" % path)
            return 2
        print("body %s sha256=%s bytes=%d" % (os.path.relpath(path, LANE),
                                              sha256(path),
                                              os.path.getsize(path)))
    draft = draft_lines()
    quoted = []
    in_code = False
    for line in draft:
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            quoted.append(line)
        elif line.startswith("> "):
            quoted.append(line[2:])

    print("draft quoted lines: %d" % len(quoted))
    bad = 0
    for label, path, fragment in FRAGMENTS:
        rc, count = grep_fixed_count(fragment, path)
        ok = (rc == 0 and count.isdigit() and int(count) >= 1)
        present = fragment in quoted
        if not (ok and present):
            bad += 1
        print("%-24s grep_rc=%d grep_count=%s bytes_exact=%s in_draft=%s  %s"
              % (label, rc, count, ok, present, fragment[:56]))
    print("violations %d" % bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
