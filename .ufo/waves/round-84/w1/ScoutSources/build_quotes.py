#!/usr/bin/env python3
"""Prove every C2 quote is a raw substring of the retained bytes (kake r84 w1 ScoutSources).

Reads the two retained renderings of RFC 9111, locates each chosen quote at its
asserted 1-based line, records the byte offset, enforces the <=25-word cap, runs
`grep -c -F` per quote, and cross-checks the same words across the two renderings.
"""
from __future__ import annotations

import html as htmllib
import re
import shlex
import subprocess
import sys
from pathlib import Path

RECEIPTS = Path("/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-84/w1/ScoutSources")
TXT = RECEIPTS / "rfc9111.txt"
HTML = RECEIPTS / "rfc9111-httpwg.html"

# qid, section, txt quote, html quote, shared visible text, note, txt_line, html_line
QUOTES = [
    ("Q1", "§4.2 heading", "4.2.  Freshness",
     'id="rfc.section.4.2"', "4.2. Freshness",
     "number and title of the section that defines freshness", 581, 269),
    ("Q5", "§5.2 heading", "5.2.  Cache-Control",
     'id="rfc.section.5.2"', "5.2. Cache-Control",
     "number and title of the Cache-Control section", 1081, 279),
    ("Q9", "§5.2.2 heading", "5.2.2.  Response Directives",
     'id="rfc.section.5.2.2"', "5.2.2. Response Directives",
     "number and title of the response-directive subsection", 1203, 282),
    ("Q11", "§5.2.2.1 heading", "5.2.2.1.  max-age",
     'id="rfc.section.5.2.2.1"', "5.2.2.1. max-age",
     "max-age is numbered 5.2.2.1 in both renderings", 1208, 282),
    ("Q16", "§5.2.2.2 heading", "5.2.2.2.  must-revalidate",
     'id="rfc.section.5.2.2.2"', "5.2.2.2. must-revalidate",
     "5.2.2.2 is must-revalidate, not max-age, in both renderings", 1222, 282),
    ("Q2", "§4.2 fresh/stale definition",
     'A "fresh" response is one whose age has not yet exceeded its',
     "response is one whose age has not yet exceeded its freshness lifetime",
     "response is one whose age has not yet exceeded its freshness lifetime",
     "freshness is a comparison of age against a lifetime", 583, 269),
    ("Q3", "§4.2 freshness lifetime",
     'A response\'s "freshness lifetime" is the length of time between its',
     "is the length of time between its generation by the origin server and its expiration time",
     "is the length of time between its generation by the origin server and its expiration time",
     "lifetime is an interval ending at the origin server's expiration time", 587, 269),
    ("Q19", "§4.2 primary mechanism",
     "The primary mechanism for determining freshness is for an origin",
     "The primary mechanism for determining freshness is for an origin server to provide an explicit expiration time",
     "The primary mechanism for determining freshness is for an origin server to provide an explicit expiration time",
     "explicit freshness comes from Expires or the max-age response directive", 601, 269),
    ("Q4", "§4.2 freshness calculation",
     "response_is_fresh = (freshness_lifetime > current_age)",
     "response_is_fresh = (freshness_lifetime &gt; current_age)",
     "response_is_fresh = (freshness_lifetime > current_age)",
     "the calculation is a strict comparison against the lifetime", 621, 269),
    ("Q6", "§5.2 field purpose",
     'The "Cache-Control" header field is used to list directives for',
     'The "Cache-Control" header field is used to list directives for caches along the request/response chain.',
     'The "Cache-Control" header field is used to list directives for caches along the request/response chain.',
     "the field is a list of directives, not a single ordered statement", 1083, 279),
    ("Q7", "§5.2 directive grammar",
     "Cache directives are identified by a token, to be compared case-",
     "Cache directives are identified by a token, to be compared case-insensitively, and have an optional argument",
     "Cache directives are identified by a token, to be compared case-insensitively, and have an optional argument",
     "a directive is a name plus an optional argument", 1098, 279),
    ("Q8", "§5.2 argument presence",
     "For the cache directives defined below, no argument is defined (nor",
     "For the cache directives defined below, no argument is defined (nor allowed) unless stated otherwise.",
     "For the cache directives defined below, no argument is defined (nor allowed) unless stated otherwise.",
     "an argument exists only where a directive's own definition states one", 1108, 282),
    ("Q10", "§5.2.2 obligation",
     "This section defines cache response directives.  A cache MUST obey",
     "This section defines cache response directives.",
     "This section defines cache response directives.",
     "the section is normative for caches; the MUST sits inside an <em> in HTML", 1205, 282),
    ("Q12", "§5.2.2.1 argument type",
     "delta-seconds (see Section 1.2.2)",
     "The delta-seconds rule specifies a non-negative integer, representing time in seconds.",
     "",
     "max-age's argument is delta-seconds; HTML quotes its definition (the 5.2.2.1 argument line is markup-split)", 1120, 266),
    ("Q13", "§5.2.2.1 staleness",
     "considered stale after its age is greater than the specified number",
     "considered stale after its age is greater than the specified number of seconds.",
     "considered stale after its age is greater than the specified number",
     "the parameter is the staleness threshold", 1215, 282),
    ("Q14", "§1.2.2 delta-seconds grammar", "delta-seconds  = 1*DIGIT",
     '= 1*<a href="#core.rules" class="smpl">DIGIT</a>',
     "",
     "non-negative integer grammar; HTML renders the name and DIGIT as links, so only this fragment is tag-free-raw", 217, 266),
    ("Q15", "§4.2.1 duplicate values",
     "When there is more than one value present for a given directive",
     "either the first occurrence should be used or the response should be considered stale",
     "either the first occurrence should be used or the response should be considered stale",
     "repeats are resolved by first occurrence or staleness, never by position of distinct directives", 677, 270),
    ("Q17", "§5.2.2.2 body",
     "The must-revalidate response directive indicates that once the",
     "The must-revalidate response directive indicates that once the response has become stale",
     "The must-revalidate response directive indicates that once the response has become stale",
     "what 5.2.2.2 actually defines", 1224, 282),
    ("Q18", "§4.1 normalization rule",
     "specification (e.g., reordering field values when order is not",
     "reordering field values when order is not significant",
     "reordering field values when order is not significant",
     "reordering is a no-op only where the field's own specification says order is insignificant", 548, 269),
    ("Q20", "§4.2.1 invalid freshness",
     "responses that have invalid freshness information (e.g., a max-age",
     "Caches are encouraged to consider responses that have invalid freshness information",
     "responses that have invalid freshness information",
     "a non-integer parameter is treated as stale, not as a policy change", 683, 270),
    # --- claims made by the S457 row already landed in corpus/SOURCES.md
    ("Q21", "§5.2.3 heading", "5.2.3.  Extension Directives",
     'id="rfc.section.5.2.3"', "5.2.3. Extension Directives",
     "number and title of the extension-directive subsection", 1408, 282),
    ("Q22", "§5.2.3 ignore rule",
     "or more extension cache directives.  A cache MUST ignore unrecognized",
     "The Cache-Control header field can be extended through the use of one or more extension cache directives.",
     "The Cache-Control header field can be extended through the use of one or more extension cache directives.",
     "unrecognized directives are ignored; the HTML MUST is <em>-wrapped", 1411, 282),
    ("Q23", "§4.2 age definition",
     'A response\'s "age" is the time that has passed since it was generated',
     "is the time that has passed since it was generated by, or successfully validated with, the origin server.",
     "is the time that has passed since it was generated by, or successfully validated with, the origin server.",
     "age is measured from generation or last successful validation", 594, 269),
    ("Q24", "front matter obsoletes",
     "STD: 98", "This document obsoletes RFC 7234", "This document obsoletes RFC 7234",
     "STD 98 and the obsoletes relation; the HTTPWG header block carries the sentence, not the STD label", 7, 233),
    ("Q26", "§4.2.1 conflicting directives",
     "both max-age and no-cache are present), the most restrictive",
     "If directives conflict (e.g., both max-age and no-cache are present), the most restrictive directive should be honored.",
     "If directives conflict (e.g., both max-age and no-cache are present), the most restrictive directive should be honored.",
     "conflicts resolve by restrictiveness, not by position", 681, 270),
    ("Q25", "§5.2 unidirectional",
     "unidirectional, in that the presence of a directive in a request does",
     "Cache directives are unidirectional, in that the presence of a directive in a request",
     "Cache directives are unidirectional, in that the presence of a directive in a request",
     "a directive is not copied between request and response", 1085, 279),
]


def main() -> int:
    txt = TXT.read_text(encoding="utf-8")
    html = HTML.read_text(encoding="utf-8")
    txt_lines = txt.split("\n")
    html_lines = html.split("\n")
    txt_bytes = TXT.read_bytes()
    html_bytes = HTML.read_bytes()

    def strip_tags(s: str) -> str:
        return re.sub(r"<[^>]*>", "", s)

    # .txt breaks words with a trailing hyphen at end of line ("case-\ninsensitively")
    norm_txt = re.sub(r"\s+", " ", re.sub(r"-\n\s+", "-", txt)).strip()
    norm_html = re.sub(r"\s+", " ", strip_tags(htmllib.unescape(html))).strip()

    tsv = ["qid\tsection\twords\ttxt_line\ttxt_byte\ttxt_count\thtml_line\thtml_byte\thtml_count\tquote"]
    checks = ["# grep -c -F raw-substring checks against the retained bytes; exit 1 means zero matches", ""]
    lines_out = ["# asserted line holds the quote (1-based, whole line as retained)"]
    agree = ["# rendering agreement: shared visible text must appear in BOTH normalized renderings", ""]
    bad = 0

    for qid, section, tq, hq, shared, note, tline, hline in QUOTES:
        words = len(tq.split())
        if words > 25:
            print(f"WORD CAP BREACH {qid}: {words}", file=sys.stderr)
            bad += 1
        if tq not in txt:
            print(f"TXT MISS {qid}: {tq!r}", file=sys.stderr)
            bad += 1
        if hq not in html:
            print(f"HTML MISS {qid}: {hq!r}", file=sys.stderr)
            bad += 1
        # asserted line must carry the quote
        if tline and tq not in txt_lines[tline - 1]:
            print(f"TXT LINE MISS {qid}: line {tline}", file=sys.stderr)
            bad += 1
        if hline and hq not in html_lines[hline - 1]:
            print(f"HTML LINE MISS {qid}: line {hline}", file=sys.stderr)
            bad += 1
        for path, quote, line in ((TXT, tq, tline), (HTML, hq, hline)):
            cmd = ["grep", "-c", "-F", "--", quote, str(path)]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            checks.append(f"{shlex.join(cmd)}\n  count={proc.stdout.strip()} exit={proc.returncode} line_asserted={line} {note}")
        tstart = txt_lines[tline - 1].find(tq) if tline else -1
        tbyte = len(txt_bytes[:len("\n".join(txt_lines[: tline - 1]).encode()) + (1 if tline > 1 else 0) + len(txt_lines[tline - 1][:tstart].encode())])
        hstart = html_lines[hline - 1].find(hq) if hline else -1
        hbyte = len(html_bytes[:len("\n".join(html_lines[: hline - 1]).encode()) + (1 if hline > 1 else 0) + len(html_lines[hline - 1][:hstart].encode())])
        tsv.append(
            f"{qid}\t{section}\t{words}\t{tline}\t{tbyte}\t{txt.count(tq)}\t{hline}\t{hbyte}\t{html.count(hq)}\t{tq}"
        )
        lines_out.append(f"{qid}\ttxt={tline}\t{txt_lines[tline-1].rstrip()}")
        lines_out.append(f"{qid}\thtml={hline}\t{html_lines[hline-1][max(0,hstart-60):hstart+len(hq)+60]}")
        if shared:
            ok_txt = shared in norm_txt
            ok_html = shared in norm_html
            agree.append(f"{qid}\tshared={shared!r}\tin_txt={ok_txt}\tin_html={ok_html}")
            if not (ok_txt and ok_html):
                print(f"AGREEMENT MISS {qid}", file=sys.stderr)
                bad += 1

    (RECEIPTS / "quotes.tsv").write_text("\n".join(tsv) + "\n", encoding="utf-8")
    (RECEIPTS / "raw-checks.txt").write_text("\n".join(checks) + "\n", encoding="utf-8")
    (RECEIPTS / "line-assertions.txt").write_text("\n".join(lines_out) + "\n", encoding="utf-8")
    (RECEIPTS / "rendering-agreement.txt").write_text("\n".join(agree) + "\n", encoding="utf-8")
    print(f"quotes={len(QUOTES)} failures={bad}")
    print(f"txt bytes={len(txt_bytes)} lines={txt.count(chr(10))} html bytes={len(html_bytes)} lines={html.count(chr(10))}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
