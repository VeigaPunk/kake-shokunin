#!/usr/bin/env python3
"""Self-test for the offline robots.txt expectation audit (round 37 C1 contract, round-38
amendments (h), (i), (k)).

Written from the public contract in SCORECARD.md only (section "Round 37 -- declared claims",
C1 contract, plus "Round 38 -- C2 declared" amendments (h), (i), (k)). It never reads the tool
under test: every fixture is materialized into a temporary directory, the tool runs as a black
box, and the run is judged on the exit code, the report `version`, the report verdict and the
multiset of findings projected on (check, reason), plus `checksEvaluated` where the fixture
states it.

Every fixture names the contract sentence it tests (the `contract` field, quoted from
SCORECARD.md). At least six fixtures per bullet (a)-(g) and for the verdict rule; the round-38
groups (h), (i), (k) carry their own minimums, and the (c)/(d) departure groups (`c-exact`,
`d-match`) carry four each. The coverage counts are checked at run time and printed in the
summary.

Round-38 additions (57 fixtures, the 137 round-37 fixtures above them unchanged):
(h) `NaN`, `Infinity`, `-Infinity` outside a string make the manifest not JSON, inside a string
they are ordinary text; a 5000-digit and a negated 5000-digit status are check faults with the
other checks still evaluated; a 6000-digit number in an unread field changes nothing; `1e400`
stays a float and is a check fault. (i) one fixture per excluded ASCII class (space, controls
U+0000-U+001F, DEL, `" < > \\ ^ ` { | }`) at path, query, fragment, host, leading and trailing
positions; non-ASCII, `%7C` and a lone `%` are valid. (k) `%2E`/`%2e`/`%72` spellings of
/robots.txt are allowed, a kept `%2F`, a query, another case and a fragment are decided by the
rules (fragment never part of the path), an empty query normalizes to /robots.txt, and a 5xx
status disallows /robots.txt. `c-exact` and `d-match` pin the (c)/(d) sentences where
`urllib.robotparser` departs: substring user-agent match, `crawl-delay` ending a group, Unicode
name folding, `*` rules ranked by matched length instead of rule length, non-final `$`, ties.

Round-39 additions (10 fixtures, the 194 round-38 fixtures above them unchanged): the four
round-38 C2 clarifications the sealed key does not exercise are now named fixtures, and each one
kills the reference mutant that breaks exactly it: `/robots.txt?` empty query
(`k10`, `m_emptyq`), a bare `%` (`i27`, `m_barepct`), an explicit `Disallow: /robots.txt`
(`k11`, `m_explicit`), and the 20 s bound on a 64 MiB integer literal (`h11`, `m_unguarded`;
the fixture carries its own 20 s subprocess timeout). The six round-38 `MutBuildTool` survivors
get one fixture each: sign of short integers (`h12`, `H03`), truncation to three decimal digits
(`h13`, `H04`), `_` rejected (`i28`, `I13`), U+00A0 rejected (`i29`, `I16`), implicit allow
limited to HTTPS (`k12`, `K08`), implicit allow below another directory (`k13`, `K09`).
Expected values are the contract's, not the mutants': (h) "an integer robotsStatus outside the
three ranges, however many digits it has, is a check fault"; (i) "_ ... and %" are allowed
characters and "A `%` not followed by two hex digits is allowed by (i) and kept by (e)"; (k)
"the implicit allow ... is compared on the normalized path-to-match" with the clarification
"`/robots.txt?` has an empty query, so its path to match is `/robots.txt` (allowed); an explicit
`Disallow: /robots.txt` does not override the implicit allow".

The fixtures deliberately cover the edges the round-37 control mutation pass found the sealed
cases do not separate (`.ufo/waves/round-37/ctl/MutRefPass.md`, "contract sentence broken" and
"one-line diff" columns): the exact 512000-byte read limit (one byte on either side), SP/TAB-only
trimming, first-`#` comments, CR/LF-only line ends, ASCII-only case folding, exact user-agent
equality, `*` matching an empty sequence, prefix matching from the first character, normalized
(not raw) specificity length, allow-wins ties, status edges 300/399/599/200, floats and booleans
as statuses, symlink and sibling-prefix containment, the exact 64 MiB manifest edge, non-UTF-8
manifests and report `version` 1. A FIFO manifest and an oversize manifest are separate fixtures.

Usage:
    python3 scripts/robots_audit_selftest.py [--tool PATH] [--list]

Exit 0 only when every fixture passes (and the fixture-count/coverage minimums are met).
"""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
DEFAULT_TOOL = HERE / "robots_audit.py"
MIN_FIXTURES = 60
MIN_PER_CONTRACT = 6
REQUIRED_CONTRACTS = ("a", "b", "c", "d", "e", "f", "g", "verdict",
                      "h", "i", "k", "c-exact", "d-match",
                      "h-bound", "i-clar", "k-clar")
MIN_BY_CONTRACT = {"h": 6, "i": 20, "k": 8, "c-exact": 4, "d-match": 4,
                   "h-bound": 1, "i-clar": 1, "k-clar": 2}
TIMEOUT_SECONDS = 120
REASONS = ("blocked", "exposed", "check_invalid", "input_invalid")

CONTRACT = {
    "usage": (
        'Usage. "python3 scripts/robots_audit.py --manifest PATH prints one JSON report on '
        'stdout: {"version": 1, "verdict": V, "checksEvaluated": N, "findings": [F, ...]}, where '
        'each finding is {"check": <check id or null>, "reason": R} (extra fields allowed). Exit 0 '
        'when V is clean, 1 when failed-policy, 2 when could-not-evaluate, 64 on a usage error '
        '(any argument list other than exactly --manifest PATH). It reads only the manifest and '
        'the robots files it names; no network, no writes."'
    ),
    "manifest": (
        'Manifest. "Manifest (UTF-8 JSON): {"version": 1, "checks": [check, ...]}. A check is an '
        'object with id (non-empty string, not equal to the id of an earlier check in the list), '
        'robotsStatus (a JSON integer 200-299, 400-499 or 500-599; booleans and floats are not '
        'integers), userAgent (a product token: one or more ASCII letters, _ or -; RFC 9309 '
        'section 2.2.1), url (absolute URL, scheme http or https, non-empty host) and expect '
        '("allow" or "disallow"). When robotsStatus is 200-299 the check also has robots: a '
        'relative path to a regular file inside the manifest\'s directory (after resolving '
        'symlinks and ..). Otherwise robots is ignored."'
    ),
    "findings": (
        'Findings. "Findings per evaluated check: the tool decides whether the robots rules '
        'allow the URL for the user agent. expect allow and the decision is disallow: one blocked '
        'finding. expect disallow and the decision is allow: one exposed finding. Otherwise none."'
    ),
    "a": (
        '(a) Access result. "robotsStatus 200-299: the robots file is parsed and decides (rules '
        '(b)-(e)). 400-499 (\'unavailable\'): allowed, whatever any file says. 500-599 '
        '(\'unreachable\'): disallowed, whatever any file says, including /robots.txt."'
    ),
    "b": (
        '(b) Lines. "Only the first 512000 bytes (500 KiB, section 2.5; lane reading: exactly this '
        'limit) of the file are read; a leading UTF-8 byte order mark (EF BB BF) is dropped; the '
        'rest is decoded as UTF-8 with invalid bytes becoming U+FFFD. Lines end at CR, LF or CRLF. '
        'On each line everything from the first # is a comment and removed. A line without : is '
        'ignored. The key is the text before the first : with spaces and tabs trimmed, compared '
        'ASCII case-insensitively; the value is the text after it with spaces and tabs trimmed. '
        'Keys user-agent, allow and disallow are records; every other key (for example sitemap, '
        'crawl-delay) is ignored and does not end a group (section 2.2.4). An allow or disallow '
        'line before the first user-agent line is ignored (section 2.2.2)."'
    ),
    "c": (
        '(c) Groups. "A user-agent line starts a new group unless the previous record was also a '
        'user-agent line (blank, comment and ignored lines between them do not count), in which '
        'case it adds a name to the current group. The check\'s userAgent matches a group when it '
        'equals one of the group\'s names compared ASCII case-insensitively. The rules of every '
        'matching group are combined. If no group matches, the rules of every group named * are '
        'combined. If there is none, no rules apply and every URL is allowed."'
    ),
    "d": (
        '(d) Rules. "A rule with an empty value never matches. * in a rule matches any sequence of '
        'characters (also none); a $ that is the last character of the rule anchors the match at '
        'the end of the path (any other $ is literal). A rule matches when it matches a prefix of '
        'the path starting at its first character (or the whole path when anchored). Of the '
        'matching rules the one with the longest normalized value (rule (e), counted in octets, * '
        'and $ included) decides; when an allow and a disallow of that length both match, allow '
        'decides. No matching rule: allowed."'
    ),
    "e": (
        '(e) Path and normalization. "The path to match is the URL\'s path (/ when empty) followed '
        'by ? and the query when the query is non-empty; the fragment is never part of it. The '
        'path /robots.txt is always allowed when (a) says the file decides. Before comparison '
        'both the rule value and the path are normalized: every non-ASCII character becomes its '
        'UTF-8 octets percent-encoded with uppercase hex; every %XX escape (two hex digits) of an '
        'unreserved character (ASCII letters, digits, -, ., _, ~; RFC 3986) is decoded; every '
        'other %XX escape is kept with its hex digits uppercased. Lane reading of the section 2.2.2 '
        'examples: reserved characters are never decoded or encoded, so %2F and / differ."'
    ),
    "f": (
        '(f) Check faults. "A check that breaks any manifest rule above (not an object, id '
        'missing, empty or repeated, status outside the three ranges, a user agent that is not a '
        'product token, expect other than the two strings, a URL that is not absolute http(s) with '
        'a host, or for 200-299 a robots path that is missing, absolute, escapes the manifest '
        'directory or is not a regular file): one check_invalid finding for it (check = its id '
        'when it is an object with a non-empty string id, else null) and no other finding for it; '
        'the other checks are still evaluated. checksEvaluated counts the checks that are not '
        'check_invalid."'
    ),
    "g": (
        '(g) Manifest faults. "A manifest path that is not a regular file, larger than 64 MiB, '
        'unreadable, not UTF-8 or not JSON, a non-object, version other than the integer 1, or '
        'checks not a list: one input_invalid finding with check null, nothing evaluated."'
    ),
    "verdict": (
        'Verdict. "Any input_invalid or check_invalid finding gives could-not-evaluate; otherwise '
        'any finding gives failed-policy; otherwise clean."'
    ),
    "h": (
        '(h) JSON numbers (RFC 8259 section 6). "The manifest is JSON as RFC 8259 defines it: '
        'NaN, Infinity and -Infinity outside a string are not JSON, so a manifest holding any of '
        'them gives one input_invalid finding (check null) and nothing is evaluated. A JSON '
        'number of any length is JSON: an integer robotsStatus outside the three ranges, however '
        'many digits it has, is a check fault (check_invalid for that check; the other checks '
        'are still evaluated), and a number of any length in a field the contract does not read '
        'changes nothing."'
    ),
    "i": (
        '(i) URL characters (RFC 3986 section 2). "A check\'s url holds, besides non-ASCII '
        'characters (kept), only ASCII letters, digits, -, ., _, ~, the reserved characters '
        ':/?#[]@!$&\'()*+,;= and %. A url holding any other ASCII character anywhere (a space, a '
        'control character U+0000-U+001F or U+007F, " < > \\ ^ ` { | }), including a leading or '
        'trailing one, is a check fault (check_invalid). The characters are judged as written, '
        'before any parsing."'
    ),
    "k": (
        '(k) Implicit allow on the normalized path (amends (e)). "When (a) says the file decides, '
        'a URL whose path to match, normalized by rule (e), is exactly /robots.txt is allowed '
        '(so /robots%2Etxt and /%72obots.txt are allowed). A path to match with a query '
        '(/robots.txt?x=1), another case (/ROBOTS.TXT) or a kept reserved escape (/robots%2Ftxt) '
        'is decided by the rules. The fragment is never part of the path (as before)."'
    ),
    "h-bound": (
        '(h) Bound (C2 clarification, round 38). "a manifest within the 64 MiB cap, however long '
        'its numbers, finishes within 20 s"; a number of any length in a field the contract does '
        'not read changes nothing."'
    ),
    "i-clar": (
        '(i) Clarification (C2, round 38). (i) judges characters only: "a `%` not followed by two '
        'hex digits is allowed by (i) and kept by (e)".'
    ),
    "k-clar": (
        '(k) Clarifications (C2, round 38). "`/robots.txt?` has an empty query, so its path to '
        'match is `/robots.txt` (allowed); an explicit `Disallow: /robots.txt` does not override '
        'the implicit allow".'
    ),
    "c-exact": (
        '(c) Groups, exact match and record boundaries. "A user-agent line starts a new group '
        'unless the previous record was also a user-agent line (blank, comment and ignored lines '
        'between them do not count), in which case it adds a name to the current group. The '
        'check\'s userAgent matches a group when it equals one of the group\'s names compared '
        'ASCII case-insensitively. The rules of every matching group are combined. If no group '
        'matches, the rules of every group named * are combined. If there is none, no rules '
        'apply and every URL is allowed."'
    ),
    "d-match": (
        '(d) Rules, wildcard, anchor and specificity. "A rule with an empty value never matches. '
        '* in a rule matches any sequence of characters (also none); a $ that is the last '
        'character of the rule anchors the match at the end of the path (any other $ is '
        'literal). A rule matches when it matches a prefix of the path starting at its first '
        'character (or the whole path when anchored). Of the matching rules the one with the '
        'longest normalized value (rule (e), counted in octets, * and $ included) decides; when '
        'an allow and a disallow of that length both match, allow decides. No matching rule: '
        'allowed."'
    ),
}

FIXTURES = []


def add(name, contract, manifest=None, raw=None, raw_size=None, manifest_missing=False,
        manifest_fifo=False, manifest_directory=False, argv=None, exit_code=0,
        verdict="clean", findings=(), evaluated=None, files=None, dirs=(), symlinks=None,
        fifos=(), chmods=None, shape=True, accept=None, timeout=TIMEOUT_SECONDS):
    FIXTURES.append({
        "name": name,
        "contract": contract,
        "manifest": manifest,
        "raw": raw,
        "raw_size": raw_size,
        "manifest_missing": manifest_missing,
        "manifest_fifo": manifest_fifo,
        "manifest_directory": manifest_directory,
        "argv": argv,
        "exit": exit_code,
        "verdict": verdict,
        "findings": list(findings),
        "evaluated": evaluated,
        "files": dict(files or {}),
        "dirs": list(dirs),
        "symlinks": dict(symlinks or {}),
        "fifos": list(fifos),
        "chmods": dict(chmods or {}),
        "shape": shape,
        "accept": list(accept or []),
        "timeout": timeout,
    })


def alt(exit_code, verdict=None, findings=(), evaluated=None):
    return {"exit": exit_code, "verdict": verdict, "findings": list(findings),
            "evaluated": evaluated}


def mf(checks):
    return {"version": 1, "checks": checks}


def chk(cid="k1", status=200, ua="bot", url="https://example.com/x", expect="allow",
        robots="robots.txt", **extra):
    check = {"id": cid, "robotsStatus": status, "userAgent": ua, "url": url, "expect": expect}
    if robots is not None:
        check["robots"] = robots
    check.update(extra)
    return check


def f(check, reason):
    return {"check": check, "reason": reason}


def robots(text):
    return {"robots.txt": text.encode("utf-8") if isinstance(text, str) else text}


def padded_file(prefix, suffix, total):
    """`prefix` + one comment filler line + `suffix`, exactly `total` bytes."""
    need = total - len(prefix) - len(suffix)
    if need < 2:
        raise ValueError("padded_file cannot fill %d bytes" % total)
    return prefix + b"#" + b"a" * (need - 2) + b"\n" + suffix


def build_fixtures():
    # ---- (a) access result ------------------------------------------------
    add("a01-status-200-file-decides", CONTRACT["a"],
        manifest=mf([chk()]), files=robots("user-agent: *\ndisallow: /x\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("a02-status-404-unavailable-allowed", CONTRACT["a"],
        manifest=mf([chk(status=404, robots=None, expect="disallow")]),
        files=robots("user-agent: *\ndisallow: /x\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "exposed")], evaluated=1)
    add("a03-status-410-unavailable-allowed", CONTRACT["a"],
        manifest=mf([chk(status=410, robots=None, expect="disallow")]),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "exposed")], evaluated=1)
    add("a04-status-500-unreachable-blocked", CONTRACT["a"],
        manifest=mf([chk(status=500, robots=None)]),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("a05-status-599-unreachable-blocked", CONTRACT["a"],
        manifest=mf([chk(status=599, robots=None)]),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("a06-status-204-file-decides", CONTRACT["a"],
        manifest=mf([chk(status=204)]),
        files=robots("user-agent: *\ndisallow: /x\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("a07-status-250-file-decides", CONTRACT["a"],
        manifest=mf([chk(status=250)]),
        files=robots("user-agent: *\ndisallow: /other\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("a08-status-500-expect-disallow", CONTRACT["a"],
        manifest=mf([chk(status=500, robots=None, expect="disallow")]),
        exit_code=0, verdict="clean", evaluated=1)
    add("a09-status-400-expect-disallow", CONTRACT["a"],
        manifest=mf([chk(status=400, robots=None, expect="disallow")]),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "exposed")], evaluated=1)
    add("a10-status-500-robots-txt-still-blocked", CONTRACT["a"],
        manifest=mf([chk(status=500, robots=None, url="https://example.com/robots.txt")]),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("a11-status-500-robots-txt-expect-disallow", CONTRACT["a"],
        manifest=mf([chk(status=500, robots=None, url="https://example.com/robots.txt",
                         expect="disallow")]),
        exit_code=0, verdict="clean", evaluated=1)
    add("a12-status-299-file-decides", CONTRACT["a"],
        manifest=mf([chk(status=299)]),
        files=robots("user-agent: *\ndisallow: /x\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("a13-status-404-ignores-robots-field", CONTRACT["a"],
        manifest=mf([chk(status=404, robots="/does-not-exist.txt")]),
        exit_code=0, verdict="clean", evaluated=1)

    # ---- (b) lines --------------------------------------------------------
    exact = padded_file(
        b"user-agent: *\n",
        b"disallow: /abcdefghij\nallow: /abcdefghij",
        512000,
    )
    add("b01-limit-keeps-last-permitted-byte", CONTRACT["b"],
        manifest=mf([chk(url="https://example.com/abcdefghij")]),
        files={"robots.txt": exact}, exit_code=0, verdict="clean", evaluated=1)
    beyond = padded_file(
        b"user-agent: *\n",
        b"disallow: /exact$X",
        512001,
    )
    add("b02-limit-drops-byte-512001", CONTRACT["b"],
        manifest=mf([chk(url="https://example.com/exact", expect="disallow")]),
        files={"robots.txt": beyond}, exit_code=0, verdict="clean", evaluated=1)
    add("b03-bom-dropped", CONTRACT["b"],
        manifest=mf([chk()]),
        files={"robots.txt": b"\xef\xbb\xbfuser-agent: *\ndisallow: /x\n"},
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("b04-bom-only-dropped-at-start", CONTRACT["b"],
        manifest=mf([chk()]),
        files=robots("user-agent: *\n\ufeffdisallow: /x\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("b05-invalid-utf8-becomes-replacement", CONTRACT["b"],
        manifest=mf([chk(url="https://example.com/bad%EF%BF%BD")]),
        files={"robots.txt": b"user-agent: *\ndisallow: /bad\xff\n"},
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("b06-first-hash-starts-comment", CONTRACT["b"],
        manifest=mf([chk(url="https://example.com/a")]),
        files=robots("user-agent: *\ndisallow: /a#b#c\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("b07-cr-only-line-ends", CONTRACT["b"],
        manifest=mf([chk()]),
        files=robots("user-agent: *\rdisallow: /x\r"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("b08-crlf-line-ends", CONTRACT["b"],
        manifest=mf([chk()]),
        files=robots("user-agent: *\r\ndisallow: /x\r\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("b09-key-trims-only-space-tab", CONTRACT["b"],
        manifest=mf([chk()]),
        files=robots("\u00a0user-agent: *\ndisallow: /x\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("b10-value-trims-only-space-tab", CONTRACT["b"],
        manifest=mf([chk()]),
        files=robots("user-agent: *\ndisallow: \u00a0/x\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("b11-value-trims-space-and-tab", CONTRACT["b"],
        manifest=mf([chk()]),
        files=robots("user-agent: *\ndisallow: \t/x \t\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("b12-line-without-colon-ignored", CONTRACT["b"],
        manifest=mf([chk()]),
        files=robots("user-agent: *\ndisallow /x\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("b13-other-record-does-not-end-group", CONTRACT["b"],
        manifest=mf([chk()]),
        files=robots("user-agent: bot\nsitemap: https://example.com/s.xml\n"
                     "user-agent: other\ndisallow: /x\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("b14-rule-before-first-agent-ignored", CONTRACT["b"],
        manifest=mf([chk()]),
        files=robots("disallow: /x\nuser-agent: *\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("b15-key-ascii-case-insensitive", CONTRACT["b"],
        manifest=mf([chk()]),
        files=robots("USER-AGENT: *\nDISALLOW: /x\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("b16-unicode-line-separator-is-not-line-end", CONTRACT["b"],
        manifest=mf([chk()]),
        files=robots("user-agent: *\u2028disallow: /x\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("b18-key-ascii-fold-not-unicode-casefold", CONTRACT["b"],
        manifest=mf([chk()]),
        files=robots("user-agent: *\ndi\u017fallow: /x\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("b17-vertical-tab-is-not-line-end", CONTRACT["b"],
        manifest=mf([chk()]),
        files=robots("user-agent: *\x0bdisallow: /x\n"),
        exit_code=0, verdict="clean", evaluated=1)

    # ---- (c) groups -------------------------------------------------------
    add("c01-exact-match-case-insensitive", CONTRACT["c"],
        manifest=mf([chk()]), files=robots("user-agent: BOT\ndisallow: /x\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("c02-no-match-falls-back-to-star", CONTRACT["c"],
        manifest=mf([chk()]),
        files=robots("user-agent: other\ndisallow: /a\nuser-agent: *\ndisallow: /x\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("c03-no-groups-allowed", CONTRACT["c"],
        manifest=mf([chk()]),
        files={"robots.txt": b""}, exit_code=0, verdict="clean", evaluated=1)
    add("c04-no-match-and-no-star-allowed", CONTRACT["c"],
        manifest=mf([chk()]),
        files=robots("user-agent: other\ndisallow: /x\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("c05-star-not-combined-when-exact-match", CONTRACT["c"],
        manifest=mf([chk(url="https://example.com/x/deep")]),
        files=robots("user-agent: bot\nallow: /x\nuser-agent: *\ndisallow: /x/deep\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("c06-consecutive-agents-one-group", CONTRACT["c"],
        manifest=mf([chk()]),
        files=robots("user-agent: bot\nuser-agent: other\ndisallow: /x\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("c07-agent-after-rule-starts-new-group", CONTRACT["c"],
        manifest=mf([chk(url="https://example.com/a")]),
        files=robots("user-agent: *\ndisallow: /a\nuser-agent: bot\ndisallow: /b\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("c08-matching-groups-combined", CONTRACT["c"],
        manifest=mf([chk()]),
        files=robots("user-agent: bot\ndisallow: /x\nuser-agent: BoT\nallow: /\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("c09-group-name-is-not-a-substring", CONTRACT["c"],
        manifest=mf([chk(ua="googlebot")]),
        files=robots("user-agent: googlebot-news\ndisallow: /x\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("c10-group-name-ascii-only-case-folding", CONTRACT["c"],
        manifest=mf([chk(ua="k")]),
        files=robots("user-agent: \u212A\ndisallow: /x\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("c11-only-star-group-matches-all", CONTRACT["c"],
        manifest=mf([chk()]),
        files=robots("user-agent: *\ndisallow: /x\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    # Round-37 wave-2 additions (ReviewShortcutDisposition): inputs on which the stock
    # urllib.robotparser plus the six (b)/(e) patches disagrees with the contract.
    add("c12-longer-token-not-matched-by-shorter-group-name", CONTRACT["c"],
        manifest=mf([chk(ua="googlebot-image", url="https://example.com/admin")]),
        files=robots("user-agent: googlebot\nallow: /\n\nuser-agent: *\ndisallow: /admin\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("c13-ignored-record-between-agents-keeps-one-group", CONTRACT["c"],
        manifest=mf([chk(ua="abot", url="https://example.com/x")]),
        files=robots("user-agent: abot\ncrawl-delay: 5\nuser-agent: bot\ndisallow: /x\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("d17-wildcard-specificity-is-rule-length", CONTRACT["d"],
        manifest=mf([chk(url="https://example.com/private/a.html")]),
        files=robots("user-agent: *\ndisallow: /private/\nallow: /*.html\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    # Round-37 wave-2 additions (MutRobotsTool survivors of both detectors).
    add("c14-every-star-group-combined", CONTRACT["c"],
        manifest=mf([chk(url="https://example.com/b")]),
        files=robots("user-agent: *\ndisallow: /a\n\nuser-agent: other\nallow: /\n\nuser-agent: *\ndisallow: /b\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("c15-empty-matching-group-suppresses-star", CONTRACT["c"],
        manifest=mf([chk(url="https://example.com/x")]),
        files=robots("user-agent: bot\ndisallow:\n\nuser-agent: *\ndisallow: /x\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("b19-invalid-utf8-becomes-replacement-character", CONTRACT["b"],
        manifest=mf([chk(url="https://example.com/a%EF%BF%BDb")]),
        files=robots(b"user-agent: *\ndisallow: /a\xffb\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)

    # ---- (d) rules --------------------------------------------------------
    add("d01-empty-value-never-matches", CONTRACT["d"],
        manifest=mf([chk()]), files=robots("user-agent: *\ndisallow:\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("d02-empty-value-after-trim", CONTRACT["d"],
        manifest=mf([chk()]), files=robots("user-agent: *\ndisallow:    \n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("d03-star-matches-empty-sequence", CONTRACT["d"],
        manifest=mf([chk(url="https://example.com/ab")]),
        files=robots("user-agent: *\ndisallow: /a*b\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("d04-star-matches-characters", CONTRACT["d"],
        manifest=mf([chk(url="https://example.com/axxb")]),
        files=robots("user-agent: *\ndisallow: /a*b\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("d05-terminal-dollar-anchors", CONTRACT["d"],
        manifest=mf([chk(url="https://example.com/x")]),
        files=robots("user-agent: *\ndisallow: /x$\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("d06-anchored-rule-matches-whole-path-only", CONTRACT["d"],
        manifest=mf([chk(url="https://example.com/xy")]),
        files=robots("user-agent: *\ndisallow: /x$\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("d07-dollar-not-last-is-literal", CONTRACT["d"],
        manifest=mf([chk(url="https://example.com/x$y")]),
        files=robots("user-agent: *\ndisallow: /x$y\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("d08-prefix-starts-at-first-character", CONTRACT["d"],
        manifest=mf([chk(url="https://example.com/ok/blocked")]),
        files=robots("user-agent: *\ndisallow: /blocked\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("d09-longest-rule-wins", CONTRACT["d"],
        manifest=mf([chk(url="https://example.com/a/b")]),
        files=robots("user-agent: *\ndisallow: /a\nallow: /a/b\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("d10-tie-allow-wins-allow-first", CONTRACT["d"],
        manifest=mf([chk()]),
        files=robots("user-agent: *\nallow: /x\ndisallow: /x\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("d11-tie-allow-wins-disallow-first", CONTRACT["d"],
        manifest=mf([chk()]),
        files=robots("user-agent: *\ndisallow: /x\nallow: /x\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("d12-no-matching-rule-allowed", CONTRACT["d"],
        manifest=mf([chk()]),
        files=robots("user-agent: *\ndisallow: /nope\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("d13-specificity-counts-dollar", CONTRACT["d"],
        manifest=mf([chk(url="https://example.com/abc")]),
        files=robots("user-agent: *\nallow: /abc\ndisallow: /abc$\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("d15-colon-inside-rule-value", CONTRACT["d"],
        manifest=mf([chk(url="https://example.com/a:b")]),
        files=robots("user-agent: *\ndisallow: /a:b\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("d16-unanchored-rule-matches-shorter-prefix", CONTRACT["d"],
        manifest=mf([chk(url="https://example.com/xy")]),
        files=robots("user-agent: *\ndisallow: /x\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("d14-star-with-terminal-anchor", CONTRACT["d"],
        manifest=mf([chk(url="https://example.com/a/")]),
        files=robots("user-agent: *\ndisallow: /a/*$\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)

    # ---- (e) path and normalization --------------------------------------
    add("e01-empty-path-becomes-slash", CONTRACT["e"],
        manifest=mf([chk(url="https://example.com")]),
        files=robots("user-agent: *\ndisallow: /\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("e02-non-empty-query-included", CONTRACT["e"],
        manifest=mf([chk(url="https://example.com/page?q=secret")]),
        files=robots("user-agent: *\ndisallow: /page?q=secret\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("e03-empty-query-not-appended", CONTRACT["e"],
        manifest=mf([chk(url="https://example.com/page?")]),
        files=robots("user-agent: *\ndisallow: /page$\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("e04-fragment-never-included", CONTRACT["e"],
        manifest=mf([chk(url="https://example.com/page#frag")]),
        files=robots("user-agent: *\ndisallow: /page$\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("e05-unreserved-escape-decoded", CONTRACT["e"],
        manifest=mf([chk(url="https://example.com/foo/bar/%62%61%7A")]),
        files=robots("user-agent: *\ndisallow: /foo/bar/baz\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("e06-reserved-escape-kept", CONTRACT["e"],
        manifest=mf([chk(url="https://example.com/a%2Fb")]),
        files=robots("user-agent: *\ndisallow: /a%2Fb\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("e07-reserved-escape-differs-from-slash", CONTRACT["e"],
        manifest=mf([chk(url="https://example.com/a/b")]),
        files=robots("user-agent: *\ndisallow: /a%2Fb\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("e08-kept-escape-hex-uppercased", CONTRACT["e"],
        manifest=mf([chk(url="https://example.com/a%2Fb")]),
        files=robots("user-agent: *\ndisallow: /a%2fb\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("e09-non-ascii-rule-becomes-utf8-escape", CONTRACT["e"],
        manifest=mf([chk(url="https://example.com/%C3%A9")]),
        files=robots("user-agent: *\ndisallow: /\u00e9\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("e10-non-ascii-path-becomes-utf8-escape", CONTRACT["e"],
        manifest=mf([chk(url="https://example.com/caf\u00e9")]),
        files=robots("user-agent: *\ndisallow: /caf%C3%A9\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("e11-robots-txt-exemption-is-exact", CONTRACT["e"],
        manifest=mf([chk(url="https://example.com/Robots.txt")]),
        files=robots("user-agent: *\ndisallow: /Robots.txt\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("e12-robots-txt-always-allowed", CONTRACT["e"],
        manifest=mf([chk(url="https://example.com/robots.txt")]),
        files=robots("user-agent: *\ndisallow: /\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("e13-tilde-escape-decoded", CONTRACT["e"],
        manifest=mf([chk(url="https://example.com/~user")]),
        files=robots("user-agent: *\ndisallow: /%7Euser\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("e14-specificity-uses-normalized-length", CONTRACT["e"],
        manifest=mf([chk(url="https://example.com/\u00e9")]),
        files=robots("user-agent: *\nallow: /\u00e9\ndisallow: /%c3%a9\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("e16-literal-escape-hex-case-against-utf8", CONTRACT["e"],
        manifest=mf([chk(url="https://example.com/\u00e9")]),
        files=robots("user-agent: *\ndisallow: /%c3%a9\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("e15-digit-escape-decoded", CONTRACT["e"],
        manifest=mf([chk(url="https://example.com/a%31b")]),
        files=robots("user-agent: *\ndisallow: /a1b\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)

    # ---- (f) check faults -------------------------------------------------
    add("f01-check-not-an-object", CONTRACT["f"],
        manifest=mf(["not a check"]),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f(None, "check_invalid")], evaluated=0)
    add("f02-id-missing", CONTRACT["f"],
        manifest=mf([{"robotsStatus": 404, "userAgent": "bot", "url": "https://example.com/x",
                      "expect": "allow"}]),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f(None, "check_invalid")], evaluated=0)
    add("f03-id-empty", CONTRACT["f"],
        manifest=mf([chk(cid="", status=404, robots=None)]),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f(None, "check_invalid")], evaluated=0)
    add("f04-id-not-a-string", CONTRACT["f"],
        manifest=mf([chk(cid=7, status=404, robots=None)]),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f(None, "check_invalid")], evaluated=0)
    add("f05-id-repeated", CONTRACT["f"],
        manifest=mf([chk("k1", status=404, robots=None), chk("k1")]),
        files=robots("user-agent: *\ndisallow: /x\n"),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=1)
    add("f06-status-300-invalid", CONTRACT["f"],
        manifest=mf([chk(status=300, robots=None)]),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=0)
    add("f07-status-399-invalid", CONTRACT["f"],
        manifest=mf([chk(status=399, robots=None)]),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=0)
    add("f08-status-600-invalid", CONTRACT["f"],
        manifest=mf([chk(status=600, robots=None)]),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=0)
    add("f09-status-float-invalid", CONTRACT["f"],
        manifest=mf([chk(status=200.0)]),
        files=robots("user-agent: *\ndisallow: /other\n"),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=0)
    add("f10-status-boolean-invalid", CONTRACT["f"],
        manifest=mf([chk(status=True, robots=None)]),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=0)
    add("f11-user-agent-with-digit-invalid", CONTRACT["f"],
        manifest=mf([chk(ua="bot7", status=404, robots=None)]),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=0)
    add("f12-user-agent-trailing-punctuation-invalid", CONTRACT["f"],
        manifest=mf([chk(ua="bot!", status=404, robots=None)]),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=0)
    add("f13-user-agent-empty-invalid", CONTRACT["f"],
        manifest=mf([chk(ua="", status=404, robots=None)]),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=0)
    add("f14-expect-case-sensitive-invalid", CONTRACT["f"],
        manifest=mf([chk(expect="Allow", status=404, robots=None)]),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=0)
    add("f15-url-relative-invalid", CONTRACT["f"],
        manifest=mf([chk(url="/x", status=404, robots=None)]),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=0)
    add("f16-url-scheme-ftp-invalid", CONTRACT["f"],
        manifest=mf([chk(url="ftp://example.com/x", status=404, robots=None)]),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=0)
    add("f17-url-empty-host-invalid", CONTRACT["f"],
        manifest=mf([chk(url="https:///x", status=404, robots=None)]),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=0)
    add("f18-robots-missing-invalid", CONTRACT["f"],
        manifest=mf([chk(robots="missing.txt")]),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=0)
    add("f19-robots-absolute-invalid", CONTRACT["f"],
        manifest=mf([chk(robots="/etc/hostname")]),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=0)
    add("f20-robots-escapes-to-sibling-prefix", CONTRACT["f"],
        manifest=mf([chk(robots="../f20-robots-escapes-to-sibling-prefix-sibling/robots.txt")]),
        files={"../f20-robots-escapes-to-sibling-prefix-sibling/robots.txt":
               b"user-agent: *\ndisallow: /x\n"},
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=0)
    add("f21-robots-is-a-directory-invalid", CONTRACT["f"],
        manifest=mf([chk(robots="rd")]), dirs=["rd"],
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=0)
    add("f22-robots-is-a-fifo-invalid", CONTRACT["f"],
        manifest=mf([chk(robots="rf")]), fifos=["rf"],
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=0)
    add("f23-robots-symlink-outside-invalid", CONTRACT["f"],
        manifest=mf([chk(robots="link.txt")]),
        symlinks={"link.txt": "/etc/hostname"},
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=0)
    add("f24-robots-symlink-inside-valid", CONTRACT["f"],
        manifest=mf([chk(robots="link.txt")]),
        files=robots("user-agent: *\ndisallow: /x\n"),
        symlinks={"link.txt": "robots.txt"},
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("f25-robots-ignored-outside-200-299", CONTRACT["f"],
        manifest=mf([chk(status=500, robots="missing.txt")]),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("f26-robots-not-a-string-invalid", CONTRACT["f"],
        manifest=mf([chk(robots=5)]),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=0)
    add("f27-invalid-check-does-not-stop-others", CONTRACT["f"],
        manifest=mf([chk("bad", status=300, robots=None), chk("good")]),
        files=robots("user-agent: *\ndisallow: /x\n"),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("bad", "check_invalid"), f("good", "blocked")], evaluated=1)

    # ---- (g) manifest faults ---------------------------------------------
    add("g01-manifest-file-missing", CONTRACT["g"], manifest_missing=True,
        exit_code=2, verdict="could-not-evaluate",
        findings=[f(None, "input_invalid")], evaluated=0)
    add("g02-manifest-is-a-fifo", CONTRACT["g"], manifest_fifo=True,
        exit_code=2, verdict="could-not-evaluate",
        findings=[f(None, "input_invalid")], evaluated=0)
    add("g03-manifest-is-a-directory", CONTRACT["g"], manifest_directory=True,
        exit_code=2, verdict="could-not-evaluate",
        findings=[f(None, "input_invalid")], evaluated=0)
    add("g04-manifest-larger-than-64-mib", CONTRACT["g"], raw_size=64 * 1024 * 1024 + 1,
        exit_code=2, verdict="could-not-evaluate",
        findings=[f(None, "input_invalid")], evaluated=0)
    add("g05-manifest-exactly-64-mib-valid", CONTRACT["g"], raw_size=64 * 1024 * 1024,
        exit_code=0, verdict="clean", evaluated=0)
    add("g06-manifest-not-utf8", CONTRACT["g"],
        raw=b'{"version": 1, "checks": [], "note": "\xff"}',
        exit_code=2, verdict="could-not-evaluate",
        findings=[f(None, "input_invalid")], evaluated=0)
    add("g07-manifest-not-json", CONTRACT["g"], raw=b"not json",
        exit_code=2, verdict="could-not-evaluate",
        findings=[f(None, "input_invalid")], evaluated=0)
    add("g08-manifest-empty", CONTRACT["g"], raw=b"",
        exit_code=2, verdict="could-not-evaluate",
        findings=[f(None, "input_invalid")], evaluated=0)
    add("g09-manifest-not-an-object", CONTRACT["g"], raw=b"[]",
        exit_code=2, verdict="could-not-evaluate",
        findings=[f(None, "input_invalid")], evaluated=0)
    add("g10-manifest-version-2", CONTRACT["g"], manifest={"version": 2, "checks": []},
        exit_code=2, verdict="could-not-evaluate",
        findings=[f(None, "input_invalid")], evaluated=0)
    add("g11-manifest-version-string", CONTRACT["g"], manifest={"version": "1", "checks": []},
        exit_code=2, verdict="could-not-evaluate",
        findings=[f(None, "input_invalid")], evaluated=0)
    add("g12-manifest-version-true", CONTRACT["g"], manifest={"version": True, "checks": []},
        exit_code=2, verdict="could-not-evaluate",
        findings=[f(None, "input_invalid")], evaluated=0)
    add("g13-manifest-checks-not-a-list", CONTRACT["g"], manifest={"version": 1, "checks": {}},
        exit_code=2, verdict="could-not-evaluate",
        findings=[f(None, "input_invalid")], evaluated=0)
    add("g14-manifest-version-missing", CONTRACT["g"], manifest={"checks": []},
        exit_code=2, verdict="could-not-evaluate",
        findings=[f(None, "input_invalid")], evaluated=0)
    if os.geteuid() != 0:
        add("g15-manifest-unreadable", CONTRACT["g"], manifest=mf([]),
            chmods={"manifest.json": 0o000},
            exit_code=2, verdict="could-not-evaluate",
            findings=[f(None, "input_invalid")], evaluated=0)

    # ---- verdict ----------------------------------------------------------
    add("v01-clean", CONTRACT["verdict"],
        manifest=mf([chk()]), files=robots("user-agent: *\ndisallow: /other\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("v02-failed-policy-blocked", CONTRACT["verdict"],
        manifest=mf([chk()]), files=robots("user-agent: *\ndisallow: /x\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("v03-failed-policy-exposed", CONTRACT["verdict"],
        manifest=mf([chk(status=404, robots=None, expect="disallow")]),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "exposed")], evaluated=1)
    add("v04-could-not-evaluate-input-invalid", CONTRACT["verdict"], raw=b"{",
        exit_code=2, verdict="could-not-evaluate",
        findings=[f(None, "input_invalid")], evaluated=0)
    add("v05-could-not-evaluate-check-invalid", CONTRACT["verdict"],
        manifest=mf([chk(status=300, robots=None)]),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=0)
    add("v06-two-checks-two-findings", CONTRACT["verdict"],
        manifest=mf([chk("a"), chk("b", status=404, robots=None, expect="disallow")]),
        files=robots("user-agent: *\ndisallow: /x\n"),
        exit_code=1, verdict="failed-policy",
        findings=[f("a", "blocked"), f("b", "exposed")], evaluated=2)
    add("v07-empty-checks-list-clean", CONTRACT["verdict"], manifest=mf([]),
        exit_code=0, verdict="clean", evaluated=0)
    add("v08-relative-manifest-path", CONTRACT["verdict"],
        manifest=mf([chk()]), files=robots("user-agent: *\ndisallow: /x\n"),
        argv=["--manifest", "manifest.json"],
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)

    # ---- (h) non-JSON number literals and integers of any length (r38) ----
    add("h01-nan-top-level-is-not-json", CONTRACT["h"],
        raw=b'{"version": 1, "checks": [], "note": NaN}',
        exit_code=2, verdict="could-not-evaluate",
        findings=[f(None, "input_invalid")], evaluated=0)
    add("h02-infinity-top-level-is-not-json", CONTRACT["h"],
        raw=b'{"version": 1, "checks": [], "note": Infinity}',
        exit_code=2, verdict="could-not-evaluate",
        findings=[f(None, "input_invalid")], evaluated=0)
    add("h03-neg-infinity-top-level-is-not-json", CONTRACT["h"],
        raw=b'{"version": 1, "checks": [], "note": -Infinity}',
        exit_code=2, verdict="could-not-evaluate",
        findings=[f(None, "input_invalid")], evaluated=0)
    add("h04-nan-in-check-field-is-not-json", CONTRACT["h"],
        raw=(b'{"version": 1, "checks": [{"id": "k1", "robotsStatus": 200, '
             b'"userAgent": "bot", "url": "https://example.com/x", "expect": "allow", '
             b'"robots": "robots.txt", "weight": NaN}]}'),
        files=robots("user-agent: *\ndisallow: /other\n"),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f(None, "input_invalid")], evaluated=0)
    add("h05-infinity-in-check-field-is-not-json", CONTRACT["h"],
        raw=(b'{"version": 1, "checks": [{"id": "k1", "robotsStatus": Infinity, '
             b'"userAgent": "bot", "url": "https://example.com/x", "expect": "allow", '
             b'"robots": "robots.txt"}]}'),
        files=robots("user-agent: *\ndisallow: /other\n"),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f(None, "input_invalid")], evaluated=0)
    add("h06-literals-inside-strings-valid", CONTRACT["h"],
        raw=(b'{"version": 1, "checks": ['
             b'{"id": "k1", "robotsStatus": 200, "userAgent": "bot", '
             b'"url": "https://example.com/x", "expect": "allow", "robots": "robots.txt", '
             b'"note": "NaN Infinity -Infinity"}, '
             b'{"id": "k2", "robotsStatus": 200, "userAgent": "bot", '
             b'"url": "https://example.com/other", "expect": "allow", "robots": "robots.txt"}], '
             b'"unused": ' + b"7" * 6000 + b"}"),
        files=robots("user-agent: *\ndisallow: /x\n"),
        exit_code=1, verdict="failed-policy",
        findings=[f("k1", "blocked")], evaluated=2)
    add("h07-5000-digit-status-check-invalid", CONTRACT["h"],
        raw=(b'{"version": 1, "checks": ['
             b'{"id": "k1", "robotsStatus": ' + b"9" * 5000 + b', "userAgent": "bot", '
             b'"url": "https://example.com/x", "expect": "allow", "robots": "robots.txt"}, '
             b'{"id": "k2", "robotsStatus": 200, "userAgent": "bot", '
             b'"url": "https://example.com/x", "expect": "allow", "robots": "robots.txt"}]}'),
        files=robots("user-agent: *\ndisallow: /x\n"),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid"), f("k2", "blocked")], evaluated=1)
    add("h08-6000-digit-unused-number-no-effect", CONTRACT["h"],
        raw=(b'{"version": 1, "checks": [{"id": "k1", "robotsStatus": 200, '
             b'"userAgent": "bot", "url": "https://example.com/x", "expect": "allow", '
             b'"robots": "robots.txt"}], "unused": ' + b"8" * 6000 + b"}"),
        files=robots("user-agent: *\ndisallow: /x\n"),
        exit_code=1, verdict="failed-policy",
        findings=[f("k1", "blocked")], evaluated=1)
    add("h09-1e400-status-check-invalid", CONTRACT["h"],
        raw=(b'{"version": 1, "checks": ['
             b'{"id": "k1", "robotsStatus": 1e400, "userAgent": "bot", '
             b'"url": "https://example.com/x", "expect": "allow", "robots": "robots.txt"}, '
             b'{"id": "k2", "robotsStatus": 200, "userAgent": "bot", '
             b'"url": "https://example.com/other", "expect": "allow", "robots": "robots.txt"}], '
             b'"unused": ' + b"5" * 6000 + b"}"),
        files=robots("user-agent: *\ndisallow: /x\n"),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=1)
    add("h10-negative-5000-digit-status-check-invalid", CONTRACT["h"],
        raw=(b'{"version": 1, "checks": ['
             b'{"id": "k1", "robotsStatus": -' + b"4" * 5000 + b', "userAgent": "bot", '
             b'"url": "https://example.com/x", "expect": "allow", "robots": "robots.txt"}, '
             b'{"id": "k2", "robotsStatus": 200, "userAgent": "bot", '
             b'"url": "https://example.com/x", "expect": "allow", "robots": "robots.txt"}]}'),
        files=robots("user-agent: *\ndisallow: /other\n"),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=1)

    h11_prefix = b'{"version": 1, "checks": [], "unread": '
    add("h11-64mib-integer-literal-within-20s", CONTRACT["h-bound"],
        raw=h11_prefix + b"9" * (64 * 1024 * 1024 - len(h11_prefix) - 1) + b"}",
        timeout=20, exit_code=0, verdict="clean", evaluated=0)
    add("h12-negative-short-status-check-invalid", CONTRACT["h"],
        manifest=mf([chk("bad", status=-200, url="https://example.com/x", expect="disallow"),
                     chk("good", status=200, url="https://example.com/x", expect="disallow")]),
        files=robots("user-agent: *\ndisallow: /x\n"),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("bad", "check_invalid")], evaluated=1)
    add("h13-four-digit-status-truncation-check-invalid", CONTRACT["h"],
        manifest=mf([chk("bad", status=1200, url="https://example.com/x", expect="disallow"),
                     chk("good", status=200, url="https://example.com/x", expect="disallow")]),
        files=robots("user-agent: *\ndisallow: /x\n"),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("bad", "check_invalid")], evaluated=1)

    # ---- (i) URL characters (r38) ----------------------------------------
    i_files = robots("user-agent: *\ndisallow: /zzz\n")
    for i_name, i_url in (
        ("i01-space-in-path", "https://example.com/a b"),
        ("i02-space-leading", " https://example.com/ab"),
        ("i03-space-trailing", "https://example.com/ab "),
        ("i04-space-in-query", "https://example.com/ab?x=1 2"),
        ("i05-space-in-fragment", "https://example.com/ab#x y"),
        ("i06-space-in-host", "https://exa mple.com/ab"),
        ("i07-nul-in-path", "https://example.com/a\x00b"),
        ("i08-control-01-in-path", "https://example.com/a\x01b"),
        ("i09-tab-in-query", "https://example.com/ab?x=\t1"),
        ("i10-line-feed-in-fragment", "https://example.com/ab#x\n"),
        ("i11-carriage-return-in-path", "https://example.com/a\rb"),
        ("i12-control-1f-in-path", "https://example.com/a\x1fb"),
        ("i13-delete-in-path", "https://example.com/a\x7fb"),
        ("i14-double-quote-in-path", 'https://example.com/a"b'),
        ("i15-less-than-in-path", "https://example.com/a<b"),
        ("i16-greater-than-in-path", "https://example.com/a>b"),
        ("i17-backslash-in-path", "https://example.com/a\\b"),
        ("i18-caret-in-query", "https://example.com/ab?x=1^2"),
        ("i19-backtick-in-path", "https://example.com/a`b"),
        ("i20-left-brace-in-path", "https://example.com/a{b"),
        ("i21-pipe-in-query", "https://example.com/ab?x=1|2"),
        ("i22-right-brace-in-path", "https://example.com/a}b"),
    ):
        add(i_name, CONTRACT["i"],
            manifest=mf([chk(url=i_url)]), files=i_files,
            exit_code=2, verdict="could-not-evaluate",
            findings=[f("k1", "check_invalid")], evaluated=0)
    add("i23-non-ascii-kept-and-evaluated", CONTRACT["i"],
        manifest=mf([chk("k1", url="https://example.com/caf\u00e9"),
                     chk("k2", url="https://example.com/a b")]),
        files=robots("user-agent: *\ndisallow: /caf\u00e9\n"),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "blocked"), f("k2", "check_invalid")], evaluated=1)
    add("i24-percent-escape-kept-valid", CONTRACT["i"],
        manifest=mf([chk("k1", url="https://example.com/a%7Cb"),
                     chk("k2", url="https://example.com/a b")]),
        files=robots("user-agent: *\ndisallow: /a%7Cb\n"),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "blocked"), f("k2", "check_invalid")], evaluated=1)
    add("i25-percent-not-hex-allowed", CONTRACT["i"],
        manifest=mf([chk("k1", url="https://example.com/a%zzb"),
                     chk("k2", url="https://example.com/a b")]),
        files=robots("user-agent: *\ndisallow: /a%zzb\n"),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "blocked"), f("k2", "check_invalid")], evaluated=1)
    add("i26-reserved-characters-allowed", CONTRACT["i"],
        manifest=mf([chk("k1", url="https://example.com/x!$&'()*+,;=:@[y]"),
                     chk("k2", url="https://example.com/a b")]),
        files=robots("user-agent: *\ndisallow: /x!$&'()*+,;=:@[y]\n"),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "blocked"), f("k2", "check_invalid")], evaluated=1)
    add("i27-bare-percent-kept-and-matched", CONTRACT["i-clar"],
        manifest=mf([chk("k1", url="https://example.com/a%"),
                     chk("k2", url="https://example.com/a b")]),
        files=robots("user-agent: *\ndisallow: /a%\n"),
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "blocked"), f("k2", "check_invalid")], evaluated=1)
    add("i28-underscore-in-path-valid", CONTRACT["i"],
        manifest=mf([chk("k1", url="https://example.com/some_path")]),
        files=robots("user-agent: *\ndisallow: /some_path\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("i29-nbsp-valid-and-normalized", CONTRACT["i"],
        manifest=mf([chk("k1", url="https://example.com/a\u00a0b")]),
        files=robots("user-agent: *\ndisallow: /a\u00a0b\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)

    # ---- (k) implicit /robots.txt allow on the normalized path (r38) ------
    add("k01-implicit-allow-escaped-dot-upper", CONTRACT["k"],
        manifest=mf([chk(url="https://example.com/robots%2Etxt", expect="disallow")]),
        files=robots("user-agent: *\ndisallow: /\n"),
        exit_code=1, verdict="failed-policy",
        findings=[f("k1", "exposed")], evaluated=1)
    add("k02-implicit-allow-escaped-r", CONTRACT["k"],
        manifest=mf([chk(url="https://example.com/%72obots.txt", expect="disallow")]),
        files=robots("user-agent: *\ndisallow: /\n"),
        exit_code=1, verdict="failed-policy",
        findings=[f("k1", "exposed")], evaluated=1)
    add("k03-implicit-allow-escaped-dot-lower", CONTRACT["k"],
        manifest=mf([chk(url="https://example.com/robots%2etxt", expect="disallow")]),
        files=robots("user-agent: *\ndisallow: /\n"),
        exit_code=1, verdict="failed-policy",
        findings=[f("k1", "exposed")], evaluated=1)
    add("k04-kept-reserved-escape-decided-by-rules", CONTRACT["k"],
        manifest=mf([chk("k1", url="https://example.com/robots%2Ftxt"),
                     chk("k2", url="https://example.com/robots%2Etxt", expect="disallow")]),
        files=robots("user-agent: *\ndisallow: /robots%2Ftxt\ndisallow: /robots%2Etxt\n"),
        exit_code=1, verdict="failed-policy",
        findings=[f("k1", "blocked"), f("k2", "exposed")], evaluated=2)
    add("k05-empty-query-normalizes-to-robots-txt", CONTRACT["k"],
        manifest=mf([chk("k1", url="https://example.com/robots.txt?"),
                     chk("k2", url="https://example.com/robots%2Etxt", expect="disallow")]),
        files=robots("user-agent: *\ndisallow: /robots.txt\n"),
        exit_code=1, verdict="failed-policy",
        findings=[f("k2", "exposed")], evaluated=2)
    add("k06-query-decided-by-rules", CONTRACT["k"],
        manifest=mf([chk("k1", url="https://example.com/robots.txt?x=1"),
                     chk("k2", url="https://example.com/robots%2Etxt", expect="disallow")]),
        files=robots("user-agent: *\ndisallow: /robots.txt?x=1\ndisallow: /robots%2Etxt\n"),
        exit_code=1, verdict="failed-policy",
        findings=[f("k1", "blocked"), f("k2", "exposed")], evaluated=2)
    add("k07-other-case-decided-by-rules", CONTRACT["k"],
        manifest=mf([chk("k1", url="https://example.com/ROBOTS.TXT"),
                     chk("k2", url="https://example.com/robots%2Etxt", expect="disallow")]),
        files=robots("user-agent: *\ndisallow: /ROBOTS.TXT\ndisallow: /robots%2Etxt\n"),
        exit_code=1, verdict="failed-policy",
        findings=[f("k1", "blocked"), f("k2", "exposed")], evaluated=2)
    add("k08-fragment-never-part-of-the-path", CONTRACT["k"],
        manifest=mf([chk("k1", url="https://example.com/robots.txt#x"),
                     chk("k2", url="https://example.com/robots%2Etxt", expect="disallow")]),
        files=robots("user-agent: *\ndisallow: /robots.txt\ndisallow: /robots%2Etxt\n"),
        exit_code=1, verdict="failed-policy",
        findings=[f("k2", "exposed")], evaluated=2)
    add("k09-status-5xx-disallows-robots-txt", CONTRACT["k"],
        manifest=mf([chk("k1", status=500, robots=None,
                         url="https://example.com/robots.txt", expect="disallow"),
                     chk("k2", url="https://example.com/robots%2Etxt", expect="disallow")]),
        files=robots("user-agent: *\ndisallow: /robots%2Etxt\n"),
        exit_code=1, verdict="failed-policy",
        findings=[f("k2", "exposed")], evaluated=2)

    add("k10-empty-query-empty-path-rule", CONTRACT["k-clar"],
        manifest=mf([chk("k1", url="https://example.com/robots.txt?")]),
        files=robots("user-agent: *\ndisallow: /\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("k11-explicit-disallow-robots-txt-does-not-override", CONTRACT["k-clar"],
        manifest=mf([chk("k1", url="https://example.com/robots.txt")]),
        files=robots("user-agent: *\ndisallow: /robots.txt\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("k12-implicit-allow-http-scheme", CONTRACT["k"],
        manifest=mf([chk("k1", url="http://example.com/robots.txt")]),
        files=robots("user-agent: *\ndisallow: /\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("k13-nested-robots-txt-not-implicit", CONTRACT["k"],
        manifest=mf([chk("k1", url="https://example.com/nested/robots.txt")]),
        files=robots("user-agent: *\ndisallow: /\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)

    # ---- (c) exact user-agent matching and record boundaries (r38) --------
    add("c21-substring-agent-not-equal-group-name", CONTRACT["c-exact"],
        manifest=mf([chk(ua="googlebot-news", url="https://example.com/x")]),
        files=robots("user-agent: googlebot\ndisallow: /x\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("c22-group-name-not-a-substring-of-agent", CONTRACT["c-exact"],
        manifest=mf([chk(ua="googlebot", url="https://example.com/x")]),
        files=robots("user-agent: googlebot-news\ndisallow: /x\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("c23-ignored-crawl-delay-does-not-end-group", CONTRACT["c-exact"],
        manifest=mf([chk(ua="bot", url="https://example.com/x")]),
        files=robots("user-agent: bot\ncrawl-delay: 5\nuser-agent: other\ndisallow: /x\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("c24-same-name-groups-combined", CONTRACT["c-exact"],
        manifest=mf([chk(ua="bot", url="https://example.com/b")]),
        files=robots("user-agent: bot\ndisallow: /a\n\nuser-agent: bot\ndisallow: /b\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("c25-kelvin-sign-is-not-ascii-k", CONTRACT["c-exact"],
        manifest=mf([chk(ua="kelvin", url="https://example.com/x")]),
        files=robots("user-agent: \u212Aelvin\ndisallow: /x\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("c26-matching-group-with-no-rules-allows", CONTRACT["c-exact"],
        manifest=mf([chk(ua="bot", url="https://example.com/x")]),
        files=robots("user-agent: *\ndisallow: /x\n\nuser-agent: other\ndisallow: /y\n\n"
                     "user-agent: bot\n"),
        exit_code=0, verdict="clean", evaluated=1)

    # ---- (d) wildcard, anchor and specificity ranking (r38) ---------------
    add("d18-wildcard-ranked-by-rule-length", CONTRACT["d-match"],
        manifest=mf([chk(url="https://example.com/abcdef")]),
        files=robots("user-agent: *\nallow: /abc\ndisallow: /*\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("d19-private-dir-beats-wildcard-html", CONTRACT["d-match"],
        manifest=mf([chk(url="https://example.com/private/a.html")]),
        files=robots("user-agent: *\ndisallow: /private/\nallow: /*.html\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("d20-equal-length-tie-allows", CONTRACT["d-match"],
        manifest=mf([chk(url="https://example.com/index.php")]),
        files=robots("user-agent: *\ndisallow: /*.php\nallow: /index\n"),
        exit_code=0, verdict="clean", evaluated=1)
    add("d21-non-final-dollar-is-literal", CONTRACT["d-match"],
        manifest=mf([chk(url="https://example.com/a$b")]),
        files=robots("user-agent: *\ndisallow: /a$b\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)
    add("d22-final-dollar-anchors", CONTRACT["d-match"],
        manifest=mf([chk("k1", url="https://example.com/a"),
                     chk("k2", url="https://example.com/ab")]),
        files=robots("user-agent: *\ndisallow: /a$\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=2)
    add("d23-star-matches-empty-sequence", CONTRACT["d-match"],
        manifest=mf([chk(url="https://example.com/ab")]),
        files=robots("user-agent: *\ndisallow: /a*b\n"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "blocked")], evaluated=1)

    # ---- usage: exit 64 ---------------------------------------------------
    usage_manifest = mf([])
    for name, argv in (
        ("u01-no-arguments", []),
        ("u02-manifest-without-value", ["--manifest"]),
        ("u03-extra-positional", ["--manifest", "{manifest}", "extra"]),
        ("u04-equals-form", ["--manifest={manifest}"]),
        ("u05-wrong-flag", ["--file", "{manifest}"]),
        ("u06-two-manifest-pairs", ["--manifest", "{manifest}", "--manifest", "{manifest}"]),
        ("u07-help-flag", ["--help"]),
    ):
        add(name, CONTRACT["usage"], manifest=usage_manifest, argv=argv,
            exit_code=64, verdict=None, shape=False)


build_fixtures()


def tool_environment():
    env = dict(os.environ)
    env.setdefault("LC_ALL", "C.UTF-8")
    env.pop("PYTHONPATH", None)
    return env


def project(findings):
    rows = []
    if not isinstance(findings, list):
        raise ValueError("findings is not a list")
    for item in findings:
        if not isinstance(item, dict):
            rows.append(("<non-object>", None))
            continue
        rows.append((json.dumps(item.get("check")), item.get("reason")))
    return sorted(rows)


def expected_projection(findings):
    return sorted((json.dumps(item["check"]), item["reason"]) for item in findings)


def snapshot(root):
    return {str(path.relative_to(root)) for path in root.rglob("*")}


def materialize(fixture, work):
    case_dir = work / fixture["name"]
    case_dir.mkdir(parents=True, exist_ok=True)
    for rel in fixture["dirs"]:
        (case_dir / rel).mkdir(parents=True, exist_ok=True)
    for rel, data in fixture["files"].items():
        target = case_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    for rel, target in fixture["symlinks"].items():
        link = case_dir / rel
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(target)
    for rel in fixture["fifos"]:
        link = case_dir / rel
        link.parent.mkdir(parents=True, exist_ok=True)
        os.mkfifo(link)
    manifest_path = case_dir / "manifest.json"
    if fixture["manifest_missing"]:
        pass
    elif fixture["manifest_fifo"]:
        os.mkfifo(manifest_path)
    elif fixture["manifest_directory"]:
        manifest_path.mkdir()
    elif fixture["raw"] is not None:
        manifest_path.write_bytes(fixture["raw"])
    elif fixture["raw_size"] is not None:
        base = json.dumps({"version": 1, "checks": []}).encode("utf-8")
        fill = fixture["raw_size"] - len(base)
        manifest_path.write_bytes(base + b" " * fill)
    elif fixture["manifest"] is not None:
        manifest_path.write_text(json.dumps(fixture["manifest"]), encoding="utf-8")
    for rel, mode in fixture["chmods"].items():
        os.chmod(case_dir / rel, mode)
    return case_dir, manifest_path


def run_case(tool, fixture, work):
    problems = []
    case_dir, manifest_path = materialize(fixture, work)
    argv = fixture["argv"]
    if argv is None:
        argv = ["--manifest", str(manifest_path)]
    else:
        argv = [str(manifest_path) if item == "{manifest}" else str(item) for item in argv]
    command = [sys.executable, "-B", str(tool)] + argv
    before = snapshot(work)
    try:
        proc = subprocess.run(
            command,
            cwd=str(case_dir),
            capture_output=True,
            text=True,
            timeout=fixture["timeout"],
            env=tool_environment(),
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ["tool could not run: %s" % exc]
    after = snapshot(work)
    written = sorted(after - before)
    if written:
        problems.append("tool wrote files: %s" % ", ".join(written))

    accepted = [{
        "exit": fixture["exit"],
        "verdict": fixture["verdict"],
        "findings": fixture["findings"],
        "evaluated": fixture["evaluated"],
    }]
    accepted.extend(fixture["accept"])
    exit_codes = sorted({item["exit"] for item in accepted})
    if proc.returncode not in exit_codes:
        problems.append("exit mismatch: expected one of %r, observed %r (stderr: %s)"
                        % (exit_codes, proc.returncode, proc.stderr.strip()[:200]))
        return problems

    if not fixture["shape"] or proc.returncode == 64:
        return problems

    try:
        report = json.loads(proc.stdout)
    except (json.JSONDecodeError, ValueError) as exc:
        problems.append("stdout is not one JSON object: %s" % exc)
        return problems
    if not isinstance(report, dict):
        problems.append("stdout JSON is not an object")
        return problems
    if report.get("version") != 1:
        problems.append("version mismatch: expected 1, observed %r" % (report.get("version"),))
    findings = report.get("findings")
    if not isinstance(findings, list):
        problems.append("findings is not a list")
        return problems
    for item in findings:
        if not isinstance(item, dict):
            problems.append("finding is not an object: %r" % (item,))
            continue
        if item.get("reason") not in REASONS:
            problems.append("unknown or missing reason %r" % (item.get("reason"),))
        if item.get("check") is not None and not isinstance(item.get("check"), str):
            problems.append("finding check is neither a string nor null: %r" % (item,))
    try:
        got = project(findings)
    except ValueError as exc:
        problems.append("invalid findings: %s" % exc)
        return problems

    mismatches = []
    for want in accepted:
        if want["exit"] != proc.returncode:
            continue
        if want["verdict"] is not None and report.get("verdict") != want["verdict"]:
            mismatches.append("verdict: expected %r, observed %r"
                              % (want["verdict"], report.get("verdict")))
            continue
        if expected_projection(want["findings"]) != got:
            mismatches.append("findings: expected %s, observed %s"
                              % (expected_projection(want["findings"]), got))
            continue
        if want["evaluated"] is not None and report.get("checksEvaluated") != want["evaluated"]:
            mismatches.append("checksEvaluated: expected %r, observed %r"
                              % (want["evaluated"], report.get("checksEvaluated")))
            continue
        return problems
    problems.extend("accepted outcome mismatch: %s" % item for item in mismatches)
    return problems


def cleanup(work):
    for root, dirs, files in os.walk(work):
        for name in dirs + files:
            path = os.path.join(root, name)
            try:
                os.chmod(path, 0o700)
            except OSError:
                pass
    shutil.rmtree(work, ignore_errors=True)


def coverage():
    key_by_text = {text: key for key, text in CONTRACT.items()}
    counts = {}
    for fixture in FIXTURES:
        key = key_by_text[fixture["contract"]]
        counts[key] = counts.get(key, 0) + 1
    return counts


def main(argv=None):
    parser = argparse.ArgumentParser(description="robots.txt expectation audit self-test")
    parser.add_argument("--tool", default=str(DEFAULT_TOOL), help="tool under test")
    parser.add_argument("--list", action="store_true", help="list fixtures and exit")
    args = parser.parse_args(argv)

    if args.list:
        try:
            for fixture in FIXTURES:
                print("%s\t%s" % (fixture["name"], fixture["contract"][:48]))
        except BrokenPipeError:
            pass
        return 0

    tool = Path(args.tool).resolve()
    counts = coverage()
    summary = {
        "selftest": "kake-r38-robots-audit-selftest",
        "tool": str(tool),
        "cases": len(FIXTURES),
        "passed": 0,
        "failed": 0,
        "passedOverTotal": "0/%d" % len(FIXTURES),
        "perContract": counts,
        "verdict": "clean",
        "failures": [],
    }
    shortfalls = []
    if len(FIXTURES) < MIN_FIXTURES:
        shortfalls.append("only %d fixtures; expected at least %d"
                          % (len(FIXTURES), MIN_FIXTURES))
    for key in REQUIRED_CONTRACTS:
        minimum = MIN_BY_CONTRACT.get(key, MIN_PER_CONTRACT)
        if counts.get(key, 0) < minimum:
            shortfalls.append("contract %s has %d fixtures; expected at least %d"
                              % (key, counts.get(key, 0), minimum))
    if shortfalls:
        summary["verdict"] = "could-not-evaluate"
        summary["failed"] = 1
        summary["failures"] = [{"case": None, "reasons": shortfalls}]
        print(json.dumps(summary, sort_keys=True))
        return 2
    if not tool.is_file():
        summary["verdict"] = "could-not-evaluate"
        summary["failed"] = 1
        summary["failures"] = [{"case": None, "reasons": ["tool not found: %s" % tool]}]
        print(json.dumps(summary, sort_keys=True))
        return 2

    work = Path(tempfile.mkdtemp(prefix="kake-r37-robots-selftest-"))
    try:
        for fixture in FIXTURES:
            problems = run_case(tool, fixture, work)
            if problems:
                summary["failures"].append({
                    "case": fixture["name"],
                    "contract": fixture["contract"],
                    "reasons": problems,
                })
            else:
                summary["passed"] += 1
    finally:
        cleanup(work)

    summary["failed"] = summary["cases"] - summary["passed"]
    summary["passedOverTotal"] = "%d/%d" % (summary["passed"], summary["cases"])
    if summary["failed"]:
        summary["verdict"] = "failed"
    print(json.dumps(summary, sort_keys=True))
    if summary["failed"]:
        for item in summary["failures"]:
            print("FAIL %s" % item["case"], file=sys.stderr)
            for reason in item["reasons"]:
                print("  - %s" % reason, file=sys.stderr)
    return 0 if summary["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
