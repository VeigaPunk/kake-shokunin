#!/usr/bin/env python3
"""Verify every RFC 9111 quote of the C2 knowledge entry against the retained body.

Whitespace-collapses the retained body, searches each quote as a collapsed
substring, and reports the original plain-text line where the match starts.
"""
import re
import sys

RFC = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-99/sources/rfc9111.txt"
ERR = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-99/sources/eid9185.html"

# (id, declared line, quote)
RFC_QUOTES = [
    ("Q1", 957, "The initial set of stored responses to update are those that could have been chosen for that request"),
    ("Q2", 962, "Then, that initial set of stored responses is further filtered by the first match of:"),
    ("Q3", 965, 'If the new response contains one or more "strong validators" (see Section 8.8.1 of [HTTP])'),
    ("Q4", 967, "All the stored responses in the initial set with one of those same strong validators are identified for update."),
    ("Q5", 970, "then the cache MUST NOT use the new response to update any stored responses"),
    ("Q6", 974, 'If the new response contains no strong validators but does contain one or more "weak validators"'),
    ("Q7", 976, "then the most recent of those matching stored responses is identified for update."),
    ("Q8", 979, "If the new response does not include any form of validator"),
    ("Q9", 982, "there is only one stored response in the initial set, and that stored response also lacks a validator"),
    ("Q10", 986, "the cache MUST update its header fields with the header fields provided in the 304 (Not Modified) response"),
    ("Q11", 375, "the cache MUST add each header field in the provided response to the stored response, replacing field values that are already present"),
    ("Q12", 377, "with the following exceptions:"),
    ("Q13", 379, "Header fields excepted from storage in Section 3.1,"),
    ("Q14", 381, "Header fields that the cache's stored response depends upon"),
    ("Q15", 384, "Header fields that are automatically processed and removed by the recipient"),
    ("Q16", 387, "The Content-Length header field."),
    ("Q17", 393, "MAY omit these header fields from updating stored responses on an exceptional basis"),
    ("Q18", 412, "the Content-* prefix is not a signal that a header field is omitted from update"),
    ("Q19", 340, "Caches MUST include all received response header fields -- including unrecognized ones -- when storing a response"),
    ("Q20", 345, "fields whose names are listed in it are required by Section 7.6.1 of [HTTP] to be removed before forwarding the message"),
    ("Q21", 350, "some fields' semantics require them to be removed before forwarding the message"),
    ("Q22", 354, "The no-cache (Section 5.2.2.4) and private (Section 5.2.2.7) cache directives can have arguments that prevent storage of header fields"),
    ("Q23", 358, "Header fields that are specific to the proxy that a cache uses when forwarding a request MUST NOT be stored"),
    ("Q24", 361, "Effectively, this is limited to Proxy-Authenticate (Section 11.7.1 of [HTTP]), Proxy-Authentication-Info (Section 11.7.3 of [HTTP]), and Proxy-Authorization (Section 11.7.2 of [HTTP])."),
    ("Q25", 935, "A 304 (Not Modified) response status code indicates that the stored response can be updated and reused"),
    ("Q26", 953, "When a cache receives a 304 (Not Modified) response, it needs to identify stored responses that are suitable for updating"),
]

ERR_QUOTES = [
    ("E1", 1, "The initial set of stored responses to update are those that could have been chosen for that request"),
    ("E2", 1, "The initial set consists of stored responses that satisfy all of the following conditions"),
    ("E3", 1, "the current wording of Section 4.3.4 excludes the stored response before comparing the ETag"),
    ("E4", 1, "The key technical change is to allow the initial set to include stored responses whose requests have nonmatching selecting request header fields"),
    ("E5", 1, "the cache MUST, for the purposes of Section 4.1, associate the updated response with the header fields of the request that elicited the 304 response"),
    ("E6", 1, "Reported"),
    ("E7", 1, "Errata-ID: 9185"),
    ("E8", 1, "Technical"),
    ("E9", 1, "The choice to recast the affected paragraph as a list of criteria rather than a list of exceptions to the Section 4 requirements is editorial"),
]


def load(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def collapse_map(text):
    """Return (collapsed_text, index_map) where index_map[i] = 1-based line of collapsed char i."""
    out = []
    idx = []
    line = 1
    pending_space = False
    for raw in text.split("\n"):
        for ch in raw:
            if ch.isspace():
                pending_space = True
                continue
            if pending_space and out:
                out.append(" ")
                idx.append(line)
            pending_space = False
            out.append(ch)
            idx.append(line)
        line += 1
        pending_space = True
    return "".join(out), idx


def check(path, quotes, label):
    text = load(path)
    coll, idx = collapse_map(text)
    rows = []
    for qid, declared, quote in quotes:
        cq = " ".join(quote.split())
        words = len(cq.split(" "))
        pos = coll.find(cq)
        found = pos >= 0
        start = idx[pos] if found else -1
        end = idx[pos + len(cq) - 1] if found else -1
        rows.append((qid, declared, start, end, words, found, quote))
    return rows


def main():
    rfc_rows = check(RFC, RFC_QUOTES, "rfc9111")
    err_rows = check(ERR, ERR_QUOTES, "eid9185")
    out = []
    for qid, declared, start, end, words, found, quote in rfc_rows:
        agree = "yes" if (found and start == declared) else ("no" if not found else "line-mismatch")
        out.append("%s\t%d\t%s\t%d\t%s\t%s" % (qid, declared, agree, start, words, quote))
    for qid, declared, start, end, words, found, quote in err_rows:
        agree = "yes" if found else "no"
        out.append("%s\t%d\t%s\t%d\t%d\t%s" % (qid, declared, agree, start, words, quote))
    sys.stdout.write("\n".join(out) + "\n")
    bad = [r for r in rfc_rows if not r[5]]
    bad += [r for r in err_rows if not r[5]]
    mismatch = [r for r in rfc_rows if r[5] and r[2] != r[1]]
    over = [r for r in rfc_rows + err_rows if r[4] > 25]
    print("rfc=%d err=%d notfound=%d linemismatch=%d over25=%d"
          % (len(rfc_rows), len(err_rows), len(bad), len(mismatch), len(over)), file=sys.stderr)
    for r in mismatch:
        print("line-mismatch %s declared=%d actual=%d" % (r[0], r[1], r[2]), file=sys.stderr)
    for r in over:
        print("over-25-words %s words=%d" % (r[0], r[4]), file=sys.stderr)
    return 1 if (bad or mismatch or over) else 0


if __name__ == "__main__":
    sys.exit(main())
