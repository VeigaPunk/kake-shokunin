#!/usr/bin/env python3
"""Round-81 ScoutSources: locate and class proposed registry quotes.

For each (label, body, quote) it reports:
  - word count (whitespace split),
  - whether the quote is a raw substring of the retained body,
  - else whether it is a substring after whitespace collapse (collapsed-only),
  - the raw byte span and the enclosing raw line numbers of the match,
  - the sha256 of the body it was proven against.

Classes follow corpus/QUALITY.md round-50: a span that is a substring of the
retained bytes is `raw-substring`; a span that survives only whitespace
collapse is `collapsed-only` and is never described as raw.
"""
import bisect
import hashlib
import json
import re
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-81/w1/ScoutSources"


def load(name):
    raw = open(f"{ROOT}/{name}", "rb").read()
    return raw, raw.decode("utf-8", "replace")


def collapsed_index(text):
    out, idx = [], []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch.isspace():
            j = i
            while j < n and text[j].isspace():
                j += 1
            out.append(" ")
            idx.append(i)
            i = j
        else:
            out.append(ch)
            idx.append(i)
            i += 1
    return "".join(out), idx


def line_of(text, offset):
    starts = [0] + [m.end() for m in re.finditer("\n", text)]
    return bisect.bisect_right(starts, offset)


def check(label, body_name, quote):
    raw, text = load(body_name)
    body_sha = hashlib.sha256(raw).hexdigest()
    words = len(quote.split())
    res = {
        "label": label,
        "body": f"{ROOT}/{body_name}",
        "body_sha256": body_sha,
        "quote": quote,
        "words": words,
    }
    pos = text.find(quote)
    if pos >= 0:
        res["class"] = "raw-substring"
        start, end = pos, pos + len(quote)
        res["line_start"] = line_of(text, start)
        res["line_end"] = line_of(text, end - 1)
        res["char_span"] = [start, end]
        res["byte_span"] = [len(text[:start].encode()), len(text[:end].encode())]
        res["method"] = "raw in"
    else:
        col, idx = collapsed_index(text)
        cpos = col.find(" ".join(quote.split()))
        if cpos >= 0:
            start = idx[cpos]
            end = idx[cpos + len(" ".join(quote.split())) - 1] + 1
            res["class"] = "collapsed-only"
            res["line_start"] = line_of(text, start)
            res["line_end"] = line_of(text, end - 1)
            res["char_span"] = [start, end]
            res["byte_span"] = [len(text[:start].encode()), len(text[:end].encode())]
            res["method"] = "whitespace-collapsed in"
            res["raw_span"] = text[start:end]
        else:
            res["class"] = "absent"
            res["method"] = "raw in -> False; whitespace-collapsed in -> False"
    return res


CASES = [
    # S454 — status semantics for an absent target resource (RFC 9110 plain text)
    ("s454_404_meaning", "rfc9110.txt",
     "The 404 (Not Found) status code indicates that the origin server did not find a current representation for the target resource"),
    ("s454_404_not_permanent", "rfc9110.txt",
     "A 404 status code does not indicate whether this lack of representation is temporary or permanent"),
    ("s454_404_410_preferred", "rfc9110.txt",
     "the 410 (Gone) status code is preferred over 404"),
    ("s454_410_meaning", "rfc9110.txt",
     "The 410 (Gone) status code indicates that access to the target resource is no longer available at the origin server"),
    ("s454_410_404_ought", "rfc9110.txt",
     "the status code 404 (Not Found) ought to be used instead"),
    # cross-body class: the same 404 meaning quote in the tag-stripped HTML
    ("s454_404_meaning_in_html", "rfc9110.html.text",
     "The 404 (Not Found) status code indicates that the origin server did not find a current representation for the target resource"),
    # S433 — re-opened: §8.3 sender rule, §5.5 OWS rule, §5.2 sender rule
    ("s433_83_sender", "rfc9110.html.text",
     "generate a Content-Type header field in that message unless the intended media type of the enclosed representation is unknown to the sender"),
    ("s433_83_singleton", "rfc9110.html.text",
     "Content-Type is defined as a singleton field, it is sometimes incorrectly generated multiple times"),
    ("s433_55_ows", "rfc9110.html.text",
     "A field value does not include leading or trailing whitespace."),
    ("s433_52_sender", "rfc9110.html.text",
     "sender MUST NOT generate multiple field lines with the same name in a message"),
    # the same three spans proved against the plain-text RFC
    ("s433_83_sender_txt", "rfc9110.txt",
     "generate a Content-Type header field in that message unless the intended media type of the enclosed representation is unknown to the sender"),
    ("s433_55_ows_txt", "rfc9110.txt",
     "A field value does not include leading or trailing whitespace."),
]


def main():
    out = {"tool": "quote_proof.py", "round": 81, "seat": "ScoutSources", "cases": []}
    ok = True
    for label, body, quote in CASES:
        r = check(label, body, quote)
        if r["class"] == "absent" or r["words"] > 25:
            ok = False
        out["cases"].append(r)
        print(f"{label}: {r['class']} words={r['words']} lines={r.get('line_start')}-{r.get('line_end')} bytes={r.get('byte_span')}")
    path = f"{ROOT}/quote-proof.json"
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(f"wrote {path}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
