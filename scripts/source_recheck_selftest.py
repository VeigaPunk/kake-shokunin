#!/usr/bin/env python3
"""Self-test for the offline source re-check audit (round 36, claim C1).

Written from the public C1 contract in SCORECARD.md only (section "Round 36 -- declared
claims", C1 contract). It never reads the tool under test: every fixture is materialized into a
temporary directory, the tool runs as a black box, and the run is judged on the exit code, the
report verdict and the multiset of findings projected on (check, reason, target) -- target
compared for `moved` only, exactly as the frozen round-36 counter projects them.

Every fixture names the contract sentence it tests (the `contract` field of each fixture). The
contract sentences are quoted from SCORECARD.md:

  usage   "python3 scripts/source_recheck.py --manifest PATH prints one JSON report on stdout:
           {"version": 1, "verdict": V, "checksEvaluated": N, "findings": [F, ...]}, where each
           finding is {"check": <check id or null>, "reason": R, "target": <URL or null>}. Exit 0
           when V is clean, 1 when failed-policy, 2 when could-not-evaluate, 64 on a usage error.
           It reads only the manifest and the body files it names; no network, no writes."
  (a)     "Final status. The last hop decides. 200: the quote rules (c)-(f) apply. 404 or 410:
           one gone finding. Any other status (including other 2xx): one http_error finding. No
           quote check unless the final status is 200."
  (b)     "Redirects. 301 and 308 are permanent; 302, 303 and 307 are temporary. Each location is
           resolved against the URL that hop answered (the check url for the first hop, then the
           previous resolved location) by RFC 3986 section 5.2, with no further normalization.
           When the chain starts with one or more permanent hops, the check gets one moved
           finding whose target is the resolved location of the last hop of that leading
           permanent run. A chain that starts with a temporary hop gets no moved finding,
           whatever follows. moved comes in addition to the final-status outcome."
  (c)     "HTML text. When the media type is text/html or application/xhtml+xml, the text is the
           decoded body with, in this order: comments removed (<!-- to the next -->); the
           contents of script, style and template elements removed (start tag to the next end tag
           of the same name, ASCII case-insensitive); every remaining tag removed (< followed by
           an ASCII letter, / or !, up to the next >); character references decoded as HTML does
           (named, decimal and hexadecimal). Text inside title and every other element is kept."
  (d)     "Quote match. The text and the quote are both normalized to NFKC, then every character
           for which Python str.isspace() is true is deleted from both. The check holds when the
           normalized quote is a substring of the normalized text; matching is case-sensitive.
           Otherwise one quote_missing finding."
  (e)     "Media types. The media type is the part of contentType before any ;, trimmed and
           compared ASCII case-insensitively; parameter names are case-insensitive too. text/plain:
           the text is the decoded body as is (no comment, tag or reference processing), then (d).
           Any other media type: one unsupported_type finding and no quote check."
  (f)     "Decoding. A body starting with a byte order mark (EF BB BF UTF-8, FE FF UTF-16BE,
           FF FE UTF-16LE) is decoded in that encoding with the mark dropped, whatever charset
           says. Otherwise the charset parameter, trimmed, with surrounding double quotes removed
           and matched ASCII case-insensitively, picks the encoding by the WHATWG Encoding label
           table; the tool supports the labels of UTF-8, UTF-16BE, UTF-16LE and windows-1252 (so
           iso-8859-1, latin1, ascii and us-ascii mean windows-1252). Any other label, even one
           valid in the table, gives one charset_unsupported finding and no quote check. No BOM
           and no charset: UTF-8. Bytes invalid in the chosen encoding decode to U+FFFD."
  (g)     "Input faults. An unreadable or non-JSON manifest, a non-object, version other than 1,
           or checks not a list: one input_invalid finding with check null, nothing evaluated. A
           check that breaks any manifest rule above (including a body path that is absolute,
           escapes the manifest directory, or is missing or not a regular file): one check_invalid
           finding for it (check = its id when it is an object with a non-empty string id, else
           null) and no other finding for it; the other checks are still evaluated and their
           findings reported. checksEvaluated counts the checks that are not check_invalid."
  verdict "Verdict: any input_invalid, check_invalid or charset_unsupported finding gives
           could-not-evaluate; otherwise any finding gives failed-policy; otherwise clean."

Two places in the contract admit more than one reading, so a few fixtures are marked tolerant
and accept either reading (the fixture passes if the tool matches any accepted alternative):

  * the manifest paragraph lists a hop as {"status": ..., "location": <string>} but the prose
    requires a location only for a redirect hop. Every fixture therefore carries a location on
    every hop (a benign "/final" on non-redirect hops), which satisfies both readings; the
    fixtures "g19-redirect-hop-without-location" and "g28-final-hop-without-location" probe the
    two readings explicitly.
  * a check whose hops do not follow "every hop but the last is a redirect and the last is not"
    may be reported as check_invalid (it breaks a manifest rule) or evaluated on its last hop.
    "g22-non-final-hop-not-a-redirect" and "a08-final-hop-is-a-redirect" accept either.
  * a --manifest path that names a missing file may be an unreadable manifest (input_invalid) or
    a usage error (exit 64). "g05-manifest-file-missing" accepts either.

Usage:
    python3 scripts/source_recheck_selftest.py [--tool PATH]

Exit 0 only when every fixture passes.
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
DEFAULT_TOOL = HERE / "source_recheck.py"
MIN_FIXTURES = 40
TIMEOUT_SECONDS = 60
NON_REDIRECT_LOCATION = "/final"

CONTRACT = {
    "usage": (
        'Usage: "python3 scripts/source_recheck.py --manifest PATH prints one JSON report on '
        'stdout: {"version": 1, "verdict": V, "checksEvaluated": N, "findings": [F, ...]}, where '
        'each finding is {"check": <check id or null>, "reason": R, "target": <URL or null>}. Exit 0 '
        'when V is clean, 1 when failed-policy, 2 when could-not-evaluate, 64 on a usage error."'
    ),
    "a": (
        '(a) Final status. "The last hop decides. 200: the quote rules (c)-(f) apply. 404 or 410: '
        'one gone finding. Any other status (including other 2xx): one http_error finding. No quote '
        'check unless the final status is 200."'
    ),
    "b": (
        '(b) Redirects. "301 and 308 are permanent; 302, 303 and 307 are temporary. Each location '
        'is resolved against the URL that hop answered (the check url for the first hop, then the '
        'previous resolved location) by RFC 3986 section 5.2, with no further normalization. When '
        'the chain starts with one or more permanent hops, the check gets one moved finding whose '
        'target is the resolved location of the last hop of that leading permanent run. A chain '
        'that starts with a temporary hop gets no moved finding, whatever follows. moved comes in '
        'addition to the final-status outcome."'
    ),
    "c": (
        '(c) HTML text. "When the media type is text/html or application/xhtml+xml, the text is the '
        'decoded body with, in this order: comments removed (<!-- to the next -->); the contents '
        'of script, style and template elements removed (start tag to the next end tag of the same '
        'name, ASCII case-insensitive); every remaining tag removed (< followed by an ASCII letter, '
        '/ or !, up to the next >); character references decoded as HTML does (named, decimal and '
        'hexadecimal). Text inside title and every other element is kept."'
    ),
    "d": (
        '(d) Quote match. "The text and the quote are both normalized to NFKC, then every '
        'character for which Python str.isspace() is true is deleted from both. The check holds '
        'when the normalized quote is a substring of the normalized text; matching is '
        'case-sensitive. Otherwise one quote_missing finding."'
    ),
    "e": (
        '(e) Media types. "The media type is the part of contentType before any ;, trimmed and '
        'compared ASCII case-insensitively; parameter names are case-insensitive too. text/plain: '
        'the text is the decoded body as is (no comment, tag or reference processing), then (d). '
        'Any other media type: one unsupported_type finding and no quote check."'
    ),
    "f": (
        '(f) Decoding. "A body starting with a byte order mark (EF BB BF UTF-8, FE FF UTF-16BE, '
        'FF FE UTF-16LE) is decoded in that encoding with the mark dropped, whatever charset says. '
        'Otherwise the charset parameter, trimmed, with surrounding double quotes removed and '
        'matched ASCII case-insensitively, picks the encoding by the WHATWG Encoding label table; '
        'the tool supports the labels of UTF-8, UTF-16BE, UTF-16LE and windows-1252 (so iso-8859-1, '
        'latin1, ascii and us-ascii mean windows-1252). Any other label, even one valid in the '
        'table, gives one charset_unsupported finding and no quote check. No BOM and no charset: '
        'UTF-8. Bytes invalid in the chosen encoding decode to U+FFFD."'
    ),
    "g": (
        '(g) Input faults. "An unreadable or non-JSON manifest, a non-object, version other than '
        '1, or checks not a list: one input_invalid finding with check null, nothing evaluated. A '
        'check that breaks any manifest rule above (including a body path that is absolute, '
        'escapes the manifest directory, or is missing or not a regular file): one check_invalid '
        'finding for it (check = its id when it is an object with a non-empty string id, else null) '
        'and no other finding for it; the other checks are still evaluated and their findings '
        'reported. checksEvaluated counts the checks that are not check_invalid."'
    ),
    "verdict": (
        'Verdict. "Any input_invalid, check_invalid or charset_unsupported finding gives '
        'could-not-evaluate; otherwise any finding gives failed-policy; otherwise clean."'
    ),
}

URL = "https://example.com/page"
URL_DIR = "https://example.com/dir/page"
QUOTE = "Hello world"

REASONS = (
    "gone",
    "http_error",
    "moved",
    "quote_missing",
    "unsupported_type",
    "charset_unsupported",
    "input_invalid",
    "check_invalid",
)

FIXTURES = []


def add(name, contract, manifest=None, raw=None, manifest_missing=False, argv=None,
        exit_code=0, verdict="clean", findings=(), evaluated=None, files=None, shape=True,
        accept=None):
    """Register one fixture.

    `accept` lists further tolerated outcomes. Each entry is a dict with the keys `exit`
    (required), `verdict` (None means "do not judge the verdict"), `findings` (default []) and
    `evaluated` (default None means "do not judge checksEvaluated").
    """
    files = dict(files or {})
    manifest = extract_body_files(manifest, files)
    FIXTURES.append({
        "name": name,
        "contract": contract,
        "manifest": manifest,
        "raw": raw,
        "manifest_missing": manifest_missing,
        "argv": argv,
        "exit": exit_code,
        "verdict": verdict,
        "findings": list(findings),
        "evaluated": evaluated,
        "files": files,
        "shape": shape,
        "accept": list(accept or []),
    })


def extract_body_files(manifest, files):
    """Move inline body bytes (written as check members) out of the manifest into `files`.

    A check may carry the body content inline as a member named "body.html" (bytes); it is
    written next to the manifest as body.html and the check keeps body = "body.html".
    """
    if not isinstance(manifest, dict):
        return manifest
    checks = manifest.get("checks")
    if not isinstance(checks, list):
        return manifest
    for check in checks:
        if not isinstance(check, dict):
            continue
        for key in [k for k in check if k.endswith(".html") and isinstance(check[k], bytes)]:
            files[key] = check.pop(key)
    return manifest


def alt(exit_code, verdict=None, findings=(), evaluated=None):
    return {"exit": exit_code, "verdict": verdict, "findings": list(findings),
            "evaluated": evaluated}


def chk(cid="k1", url=URL, quote=QUOTE, hops=None, **extra):
    check = {
        "id": cid,
        "url": url,
        "quote": quote,
        "hops": [{"status": 200}] if hops is None else hops,
    }
    check.update(extra)
    return check


def mf(checks):
    return {"version": 1, "checks": checks}


def f(check, reason, target=None):
    return {"check": check, "reason": reason, "target": target}


def html(body):
    return {"body.html": body}


def hop(status, location=NON_REDIRECT_LOCATION):
    return {"status": status, "location": location}


def build_fixtures():
    # ---- (a) final status -------------------------------------------------
    add("a01-final-200-quote-holds", CONTRACT["a"],
        manifest=mf([chk(contentType="text/html", body="body.html", **html(b"<p>Hello world</p>"))]),
        files=html(b"<p>Hello world</p>"), exit_code=0, verdict="clean", evaluated=1)
    add("a02-final-404-gone", CONTRACT["a"],
        manifest=mf([chk(hops=[hop(404)])]),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "gone")], evaluated=1)
    add("a03-final-410-gone", CONTRACT["a"],
        manifest=mf([chk(hops=[hop(410)])]),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "gone")], evaluated=1)
    add("a04-final-500-http-error", CONTRACT["a"],
        manifest=mf([chk(hops=[hop(500)])]),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "http_error")], evaluated=1)
    add("a05-final-204-other-2xx-http-error", CONTRACT["a"],
        manifest=mf([chk(hops=[hop(204)])]),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "http_error")], evaluated=1)
    add("a06-final-403-http-error", CONTRACT["a"],
        manifest=mf([chk(hops=[hop(403)])]),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "http_error")], evaluated=1)
    add("a07-final-200-quote-rules-apply", CONTRACT["a"],
        manifest=mf([chk(quote="absent", contentType="text/html", body="body.html",
                         **html(b"<p>Hello world</p>"))]),
        files=html(b"<p>Hello world</p>"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "quote_missing")], evaluated=1)
    add("a08-final-hop-is-a-redirect", CONTRACT["g"],
        manifest=mf([chk(hops=[hop(301, "/x")])]),
        exit_code=2, verdict="could-not-evaluate", findings=[f("k1", "check_invalid")], evaluated=0,
        accept=[alt(1, "failed-policy", [f("k1", "http_error")], evaluated=1)])

    # ---- (b) redirects ----------------------------------------------------
    add("b01-301-permanent-moved", CONTRACT["b"],
        manifest=mf([chk(hops=[hop(301, "/new"), hop(200)],
                         contentType="text/html", body="body.html", **html(b"<p>Hello world</p>"))]),
        files=html(b"<p>Hello world</p>"), exit_code=1, verdict="failed-policy",
        findings=[f("k1", "moved", "https://example.com/new")], evaluated=1)
    add("b02-308-permanent-moved", CONTRACT["b"],
        manifest=mf([chk(hops=[hop(308, "/new"), hop(200)],
                         contentType="text/html", body="body.html", **html(b"<p>Hello world</p>"))]),
        files=html(b"<p>Hello world</p>"), exit_code=1, verdict="failed-policy",
        findings=[f("k1", "moved", "https://example.com/new")], evaluated=1)
    add("b03-302-temporary-no-moved", CONTRACT["b"],
        manifest=mf([chk(hops=[hop(302, "/new"), hop(200)],
                         contentType="text/html", body="body.html", **html(b"<p>Hello world</p>"))]),
        files=html(b"<p>Hello world</p>"), exit_code=0, verdict="clean", evaluated=1)
    add("b04-303-temporary-no-moved", CONTRACT["b"],
        manifest=mf([chk(hops=[hop(303, "/new"), hop(200)],
                         contentType="text/html", body="body.html", **html(b"<p>Hello world</p>"))]),
        files=html(b"<p>Hello world</p>"), exit_code=0, verdict="clean", evaluated=1)
    add("b05-307-temporary-no-moved", CONTRACT["b"],
        manifest=mf([chk(hops=[hop(307, "/new"), hop(200)],
                         contentType="text/html", body="body.html", **html(b"<p>Hello world</p>"))]),
        files=html(b"<p>Hello world</p>"), exit_code=0, verdict="clean", evaluated=1)
    add("b06-leading-permanent-run-target-is-last-permanent-hop", CONTRACT["b"],
        manifest=mf([chk(hops=[hop(301, "/a"), hop(301, "/b"), hop(200)],
                         contentType="text/html", body="body.html", **html(b"<p>Hello world</p>"))]),
        files=html(b"<p>Hello world</p>"), exit_code=1, verdict="failed-policy",
        findings=[f("k1", "moved", "https://example.com/b")], evaluated=1)
    add("b07-permanent-then-temporary-only-leading-run-counts", CONTRACT["b"],
        manifest=mf([chk(hops=[hop(301, "/a"), hop(302, "/b"), hop(200)],
                         contentType="text/html", body="body.html", **html(b"<p>Hello world</p>"))]),
        files=html(b"<p>Hello world</p>"), exit_code=1, verdict="failed-policy",
        findings=[f("k1", "moved", "https://example.com/a")], evaluated=1)
    add("b08-leading-temporary-suppresses-moved-entirely", CONTRACT["b"],
        manifest=mf([chk(hops=[hop(302, "/a"), hop(301, "/b"), hop(200)],
                         contentType="text/html", body="body.html", **html(b"<p>Hello world</p>"))]),
        files=html(b"<p>Hello world</p>"), exit_code=0, verdict="clean", evaluated=1)
    add("b09-relative-location-resolved-rfc3986", CONTRACT["b"],
        manifest=mf([chk(url=URL_DIR,
                         hops=[hop(301, "other"), hop(200)],
                         contentType="text/html", body="body.html", **html(b"<p>Hello world</p>"))]),
        files=html(b"<p>Hello world</p>"), exit_code=1, verdict="failed-policy",
        findings=[f("k1", "moved", "https://example.com/dir/other")], evaluated=1)
    add("b10-moved-plus-final-status-outcome", CONTRACT["b"],
        manifest=mf([chk(hops=[hop(301, "/new"), hop(404)])]),
        exit_code=1, verdict="failed-policy",
        findings=[f("k1", "moved", "https://example.com/new"), f("k1", "gone")], evaluated=1)
    add("b11-absolute-location-target", CONTRACT["b"],
        manifest=mf([chk(hops=[hop(308, "https://other.example/x"), hop(200)],
                         contentType="text/html", body="body.html", **html(b"<p>Hello world</p>"))]),
        files=html(b"<p>Hello world</p>"), exit_code=1, verdict="failed-policy",
        findings=[f("k1", "moved", "https://other.example/x")], evaluated=1)

    # ---- (c) HTML text ----------------------------------------------------
    add("c01-script-contents-removed", CONTRACT["c"],
        manifest=mf([chk(quote="secret", contentType="text/html", body="body.html",
                         **html(b"<p>ok</p><script>var secret=1;</script>"))]),
        files=html(b"<p>ok</p><script>var secret=1;</script>"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "quote_missing")], evaluated=1)
    add("c02-style-contents-removed", CONTRACT["c"],
        manifest=mf([chk(quote="color", contentType="text/html", body="body.html",
                         **html(b"<style>.x{color:red}</style><p>ok</p>"))]),
        files=html(b"<style>.x{color:red}</style><p>ok</p>"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "quote_missing")], evaluated=1)
    add("c03-template-contents-removed", CONTRACT["c"],
        manifest=mf([chk(quote="tpl", contentType="text/html", body="body.html",
                         **html(b"<template><p>tpl</p></template><p>ok</p>"))]),
        files=html(b"<template><p>tpl</p></template><p>ok</p>"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "quote_missing")], evaluated=1)
    add("c04-comment-removed", CONTRACT["c"],
        manifest=mf([chk(quote="hidden", contentType="text/html", body="body.html",
                         **html(b"<p>hi</p><!-- hidden note -->"))]),
        files=html(b"<p>hi</p><!-- hidden note -->"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "quote_missing")], evaluated=1)
    add("c05-tags-removed-text-kept", CONTRACT["c"],
        manifest=mf([chk(quote="Visible", contentType="text/html", body="body.html",
                         **html(b"<div><p>Visible</p></div>"))]),
        files=html(b"<div><p>Visible</p></div>"), exit_code=0, verdict="clean", evaluated=1)
    add("c06-named-character-reference-decoded", CONTRACT["c"],
        manifest=mf([chk(quote="Tom & Jerry", contentType="text/html", body="body.html",
                         **html(b"<p>Tom &amp; Jerry</p>"))]),
        files=html(b"<p>Tom &amp; Jerry</p>"), exit_code=0, verdict="clean", evaluated=1)
    add("c07-decimal-and-hexadecimal-references-decoded", CONTRACT["c"],
        manifest=mf([chk(quote="AB", contentType="text/html", body="body.html",
                         **html(b"<p>&#65;&#x42;</p>"))]),
        files=html(b"<p>&#65;&#x42;</p>"), exit_code=0, verdict="clean", evaluated=1)
    add("c08-title-text-kept", CONTRACT["c"],
        manifest=mf([chk(quote="Doc Title", contentType="text/html", body="body.html",
                         **html(b"<title>Doc Title</title><p>x</p>"))]),
        files=html(b"<title>Doc Title</title><p>x</p>"), exit_code=0, verdict="clean", evaluated=1)
    add("c09-script-end-tag-case-insensitive", CONTRACT["c"],
        manifest=mf([chk(quote="secret", contentType="text/html", body="body.html",
                         **html(b"<SCRIPT>secret</script>"))]),
        files=html(b"<SCRIPT>secret</script>"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "quote_missing")], evaluated=1)
    add("c10-xhtml-media-type-uses-html-rules", CONTRACT["c"],
        manifest=mf([chk(quote="bad()", contentType="application/xhtml+xml", body="body.html",
                         **html(b"<html><script>bad()</script><p>ok</p></html>"))]),
        files=html(b"<html><script>bad()</script><p>ok</p></html>"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "quote_missing")], evaluated=1)

    # ---- (d) quote match --------------------------------------------------
    add("d01-nfkc-fullwidth", CONTRACT["d"],
        manifest=mf([chk(quote="AB", contentType="text/html", body="body.html",
                         **html("ＡＢ".encode("utf-8")))]),
        files=html("ＡＢ".encode("utf-8")), exit_code=0, verdict="clean", evaluated=1)
    add("d02-whitespace-deleted-from-both", CONTRACT["d"],
        manifest=mf([chk(quote="abc", contentType="text/html", body="body.html",
                         **html(b"<p>a b\tc\n</p>"))]),
        files=html(b"<p>a b\tc\n</p>"), exit_code=0, verdict="clean", evaluated=1)
    add("d03-matching-is-case-sensitive", CONTRACT["d"],
        manifest=mf([chk(quote="hello", contentType="text/html", body="body.html",
                         **html(b"<p>Hello world</p>"))]),
        files=html(b"<p>Hello world</p>"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "quote_missing")], evaluated=1)
    add("d04-substring-of-text-holds", CONTRACT["d"],
        manifest=mf([chk(quote="quick brown", contentType="text/html", body="body.html",
                         **html(b"<p>the quick brown fox</p>"))]),
        files=html(b"<p>the quick brown fox</p>"), exit_code=0, verdict="clean", evaluated=1)
    add("d05-absent-quote-missing", CONTRACT["d"],
        manifest=mf([chk(quote="absent", contentType="text/html", body="body.html",
                         **html(b"<p>Hello world</p>"))]),
        files=html(b"<p>Hello world</p>"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "quote_missing")], evaluated=1)
    add("d06-nfkc-compatibility-ligature", CONTRACT["d"],
        manifest=mf([chk(quote="file", contentType="text/html", body="body.html",
                         **html("ﬁle".encode("utf-8")))]),
        files=html("ﬁle".encode("utf-8")), exit_code=0, verdict="clean", evaluated=1)
    add("d07-nbsp-is-whitespace", CONTRACT["d"],
        manifest=mf([chk(quote="ab", contentType="text/html", body="body.html",
                         **html("<p>a\u00a0b</p>".encode("utf-8")))]),
        files=html("<p>a\u00a0b</p>".encode("utf-8")), exit_code=0, verdict="clean", evaluated=1)

    # ---- (e) media types --------------------------------------------------
    add("e01-text-plain-body-as-is-no-tag-processing", CONTRACT["e"],
        manifest=mf([chk(quote="<b>Hi</b>", contentType="text/plain", body="body.html",
                         **html(b"<b>Hi</b>"))]),
        files=html(b"<b>Hi</b>"), exit_code=0, verdict="clean", evaluated=1)
    add("e02-text-plain-no-reference-processing", CONTRACT["e"],
        manifest=mf([chk(quote="A & B", contentType="text/plain", body="body.html",
                         **html(b"A &amp; B"))]),
        files=html(b"A &amp; B"),
        exit_code=1, verdict="failed-policy", findings=[f("k1", "quote_missing")], evaluated=1)
    add("e03-text-plain-literal-amp-holds", CONTRACT["e"],
        manifest=mf([chk(quote="A &amp; B", contentType="text/plain", body="body.html",
                         **html(b"A &amp; B"))]),
        files=html(b"A &amp; B"), exit_code=0, verdict="clean", evaluated=1)
    add("e04-unsupported-media-type", CONTRACT["e"],
        manifest=mf([chk(contentType="application/json", body="body.html", **html(b"{}"))]),
        files=html(b"{}"), exit_code=1, verdict="failed-policy",
        findings=[f("k1", "unsupported_type")], evaluated=None)
    add("e05-media-type-ascii-case-insensitive", CONTRACT["e"],
        manifest=mf([chk(quote="Hello world", contentType="TEXT/HTML; Charset=UTF-8", body="body.html",
                         **html(b"<p>Hello world</p>"))]),
        files=html(b"<p>Hello world</p>"), exit_code=0, verdict="clean", evaluated=1)
    add("e06-media-type-trimmed-before-semicolon", CONTRACT["e"],
        manifest=mf([chk(quote="Hello world", contentType=" text/html ; charset=utf-8", body="body.html",
                         **html(b"<p>Hello world</p>"))]),
        files=html(b"<p>Hello world</p>"), exit_code=0, verdict="clean", evaluated=1)
    add("e07-text-plain-with-charset-parameter", CONTRACT["e"],
        manifest=mf([chk(quote="Hello world", contentType="text/plain;charset=utf-8", body="body.html",
                         **html(b"Hello world"))]),
        files=html(b"Hello world"), exit_code=0, verdict="clean", evaluated=1)
    add("e08-image-media-type-unsupported", CONTRACT["e"],
        manifest=mf([chk(contentType="image/png", body="body.html", **html(b"\x89PNG"))]),
        files=html(b"\x89PNG"), exit_code=1, verdict="failed-policy",
        findings=[f("k1", "unsupported_type")], evaluated=None)

    # ---- (f) decoding -----------------------------------------------------
    add("f01-utf8-bom-overrides-charset", CONTRACT["f"],
        manifest=mf([chk(quote="café", contentType="text/html; charset=windows-1252",
                         body="body.html", **html(b"\xef\xbb\xbfcaf\xc3\xa9"))]),
        files=html(b"\xef\xbb\xbfcaf\xc3\xa9"), exit_code=0, verdict="clean", evaluated=1)
    add("f02-charset-windows-1252", CONTRACT["f"],
        manifest=mf([chk(quote="café", contentType="text/html; charset=windows-1252",
                         body="body.html", **html(b"<p>caf\xe9</p>"))]),
        files=html(b"<p>caf\xe9</p>"), exit_code=0, verdict="clean", evaluated=1)
    add("f03-charset-iso-8859-1-means-windows-1252", CONTRACT["f"],
        manifest=mf([chk(quote="café", contentType="text/html; charset=iso-8859-1",
                         body="body.html", **html(b"<p>caf\xe9</p>"))]),
        files=html(b"<p>caf\xe9</p>"), exit_code=0, verdict="clean", evaluated=1)
    add("f04-charset-latin1-means-windows-1252", CONTRACT["f"],
        manifest=mf([chk(quote="café", contentType="text/html; charset=latin1",
                         body="body.html", **html(b"<p>caf\xe9</p>"))]),
        files=html(b"<p>caf\xe9</p>"), exit_code=0, verdict="clean", evaluated=1)
    add("f05-charset-ascii-means-windows-1252", CONTRACT["f"],
        manifest=mf([chk(quote="café", contentType="text/html; charset=ascii",
                         body="body.html", **html(b"<p>caf\xe9</p>"))]),
        files=html(b"<p>caf\xe9</p>"), exit_code=0, verdict="clean", evaluated=1)
    add("f06-charset-us-ascii-means-windows-1252", CONTRACT["f"],
        manifest=mf([chk(quote="café", contentType="text/html; charset=us-ascii",
                         body="body.html", **html(b"<p>caf\xe9</p>"))]),
        files=html(b"<p>caf\xe9</p>"), exit_code=0, verdict="clean", evaluated=1)
    add("f07-unsupported-charset-label", CONTRACT["f"],
        manifest=mf([chk(contentType="text/html; charset=shift_jis", body="body.html",
                         **html(b"<p>Hello world</p>"))]),
        files=html(b"<p>Hello world</p>"), exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "charset_unsupported")], evaluated=None)
    add("f08-unsupported-label-valid-in-whatwg-table", CONTRACT["f"],
        # L1 integration fix (round 36): the seat used "utf-16", which the WHATWG table lists as a
        # UTF-16LE label (S090), so it is supported; "shift_jis" is valid in the table and unsupported.
        manifest=mf([chk(contentType="text/html; charset=shift_jis", body="body.html",
                         **html(b"<p>Hello world</p>"))]),
        files=html(b"<p>Hello world</p>"), exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "charset_unsupported")], evaluated=None)
    add("f09-no-bom-no-charset-means-utf8", CONTRACT["f"],
        manifest=mf([chk(quote="café", contentType="text/html", body="body.html",
                         **html(b"<p>caf\xc3\xa9</p>"))]),
        files=html(b"<p>caf\xc3\xa9</p>"), exit_code=0, verdict="clean", evaluated=1)
    add("f10-charset-parameter-quotes-removed", CONTRACT["f"],
        manifest=mf([chk(quote="café", contentType="text/html; charset=\"utf-8\"",
                         body="body.html", **html(b"<p>caf\xc3\xa9</p>"))]),
        files=html(b"<p>caf\xc3\xa9</p>"), exit_code=0, verdict="clean", evaluated=1)
    add("f11-charset-parameter-name-case-insensitive", CONTRACT["f"],
        manifest=mf([chk(quote="café", contentType="text/html; CHARSET=windows-1252",
                         body="body.html", **html(b"<p>caf\xe9</p>"))]),
        files=html(b"<p>caf\xe9</p>"), exit_code=0, verdict="clean", evaluated=1)
    add("f12-utf16le-bom", CONTRACT["f"],
        manifest=mf([chk(quote="Hi", contentType="text/html", body="body.html",
                         **html(b"\xff\xfeH\x00i\x00"))]),
        files=html(b"\xff\xfeH\x00i\x00"), exit_code=0, verdict="clean", evaluated=1)
    add("f13-utf16be-bom", CONTRACT["f"],
        manifest=mf([chk(quote="Hi", contentType="text/html", body="body.html",
                         **html(b"\xfe\xff\x00H\x00i"))]),
        files=html(b"\xfe\xff\x00H\x00i"), exit_code=0, verdict="clean", evaluated=1)
    add("f14-utf16le-label-without-bom", CONTRACT["f"],
        manifest=mf([chk(quote="Hi", contentType="text/html; charset=utf-16le", body="body.html",
                         **html(b"H\x00i\x00"))]),
        files=html(b"H\x00i\x00"), exit_code=0, verdict="clean", evaluated=1)
    add("f15-utf16be-label-without-bom", CONTRACT["f"],
        manifest=mf([chk(quote="Hi", contentType="text/html; charset=utf-16be", body="body.html",
                         **html(b"\x00H\x00i"))]),
        files=html(b"\x00H\x00i"), exit_code=0, verdict="clean", evaluated=1)
    add("f16-invalid-bytes-become-replacement-character", CONTRACT["f"],
        manifest=mf([chk(quote="�abc", contentType="text/html; charset=utf-8",
                         body="body.html", **html(b"\xffabc"))]),
        files=html(b"\xffabc"), exit_code=0, verdict="clean", evaluated=1)

    # ---- (g) input faults -------------------------------------------------
    add("g01-manifest-not-json", CONTRACT["g"], raw=b"this is not json",
        exit_code=2, verdict="could-not-evaluate", findings=[f(None, "input_invalid")], evaluated=0)
    add("g02-manifest-version-not-1", CONTRACT["g"],
        manifest={"version": 2, "checks": []},
        exit_code=2, verdict="could-not-evaluate", findings=[f(None, "input_invalid")], evaluated=0)
    add("g03-manifest-checks-not-a-list", CONTRACT["g"],
        manifest={"version": 1, "checks": {"id": "k1"}},
        exit_code=2, verdict="could-not-evaluate", findings=[f(None, "input_invalid")], evaluated=0)
    add("g04-manifest-not-an-object", CONTRACT["g"], raw=b"[1, 2, 3]",
        exit_code=2, verdict="could-not-evaluate", findings=[f(None, "input_invalid")], evaluated=0)
    add("g05-manifest-file-missing", CONTRACT["g"], manifest_missing=True,
        exit_code=2, verdict="could-not-evaluate", findings=[f(None, "input_invalid")], evaluated=0,
        accept=[alt(64)])
    add("g06-check-without-id", CONTRACT["g"],
        manifest=mf([{"url": URL, "quote": QUOTE, "hops": [hop(200)],
                      "contentType": "text/html", "body": "body.html"}]),
        files=html(b"<p>Hello world</p>"), exit_code=2, verdict="could-not-evaluate",
        findings=[f(None, "check_invalid")], evaluated=0)
    add("g07-check-with-empty-id", CONTRACT["g"],
        manifest=mf([chk(cid="", contentType="text/html", body="body.html", **html(b"<p>Hello world</p>"))]),
        files=html(b"<p>Hello world</p>"), exit_code=2, verdict="could-not-evaluate",
        findings=[f(None, "check_invalid")], evaluated=0)
    add("g08-check-id-not-a-string", CONTRACT["g"],
        manifest=mf([chk(cid=7, contentType="text/html", body="body.html", **html(b"<p>Hello world</p>"))]),
        files=html(b"<p>Hello world</p>"), exit_code=2, verdict="could-not-evaluate",
        findings=[f(None, "check_invalid")], evaluated=0)
    add("g09-body-path-escapes-manifest-directory", CONTRACT["g"],
        manifest=mf([chk(contentType="text/html", body="../outside.html")]),
        files={"../outside.html": b"<p>Hello world</p>"}, exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=0)
    add("g10-body-path-absolute", CONTRACT["g"],
        manifest=mf([chk(contentType="text/html", body="/etc/hostname")]),
        exit_code=2, verdict="could-not-evaluate", findings=[f("k1", "check_invalid")], evaluated=0)
    add("g11-body-file-missing", CONTRACT["g"],
        manifest=mf([chk(contentType="text/html", body="missing.html")]),
        exit_code=2, verdict="could-not-evaluate", findings=[f("k1", "check_invalid")], evaluated=0)
    add("g12-body-path-is-a-directory", CONTRACT["g"],
        manifest=mf([chk(contentType="text/html", body="adir")]),
        files={"adir/keep": b"x"}, exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=0)
    add("g13-url-scheme-not-http", CONTRACT["g"],
        manifest=mf([chk(url="ftp://example.com/page")]),
        exit_code=2, verdict="could-not-evaluate", findings=[f("k1", "check_invalid")], evaluated=0)
    add("g14-url-not-absolute", CONTRACT["g"],
        manifest=mf([chk(url="/page")]),
        exit_code=2, verdict="could-not-evaluate", findings=[f("k1", "check_invalid")], evaluated=0)
    add("g15-url-empty-host", CONTRACT["g"],
        manifest=mf([chk(url="https:///page")]),
        exit_code=2, verdict="could-not-evaluate", findings=[f("k1", "check_invalid")], evaluated=0)
    add("g16-quote-empty", CONTRACT["g"],
        manifest=mf([chk(quote="", contentType="text/html", body="body.html",
                         **html(b"<p>Hello world</p>"))]),
        files=html(b"<p>Hello world</p>"), exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=0)
    add("g17-quote-not-a-string", CONTRACT["g"],
        manifest=mf([chk(quote=5, contentType="text/html", body="body.html",
                         **html(b"<p>Hello world</p>"))]),
        files=html(b"<p>Hello world</p>"), exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=0)
    add("g18-hops-empty", CONTRACT["g"],
        manifest=mf([chk(hops=[])]),
        exit_code=2, verdict="could-not-evaluate", findings=[f("k1", "check_invalid")], evaluated=0)
    add("g19-redirect-hop-without-location", CONTRACT["g"],
        manifest=mf([chk(hops=[{"status": 301}, hop(200)])]),
        exit_code=2, verdict="could-not-evaluate", findings=[f("k1", "check_invalid")], evaluated=0)
    add("g20-hop-status-out-of-range", CONTRACT["g"],
        manifest=mf([chk(hops=[hop(99, "/x"), hop(200)])]),
        exit_code=2, verdict="could-not-evaluate", findings=[f("k1", "check_invalid")], evaluated=0)
    add("g21-hop-status-not-an-integer", CONTRACT["g"],
        manifest=mf([chk(hops=[hop("301", "/x"), hop(200)])]),
        exit_code=2, verdict="could-not-evaluate", findings=[f("k1", "check_invalid")], evaluated=0)
    add("g22-non-final-hop-not-a-redirect", CONTRACT["g"],
        manifest=mf([chk(hops=[hop(200), hop(200)])]),
        exit_code=2, verdict="could-not-evaluate", findings=[f("k1", "check_invalid")], evaluated=0,
        accept=[alt(0, "clean", [], evaluated=1)])
    add("g23-body-missing-while-status-200", CONTRACT["g"],
        manifest=mf([chk(contentType="text/html")]),
        exit_code=2, verdict="could-not-evaluate", findings=[f("k1", "check_invalid")], evaluated=0)
    add("g24-content-type-missing-while-status-200", CONTRACT["g"],
        manifest=mf([chk(body="body.html", **html(b"<p>Hello world</p>"))]),
        files=html(b"<p>Hello world</p>"), exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=0)
    add("g25-one-invalid-one-valid-check", CONTRACT["g"],
        manifest=mf([
            chk(cid="bad", url="ftp://example.com/page"),
            chk(cid="good", contentType="text/html", body="body.html", **html(b"<p>Hello world</p>")),
        ]),
        files=html(b"<p>Hello world</p>"), exit_code=2, verdict="could-not-evaluate",
        findings=[f("bad", "check_invalid")], evaluated=1)
    add("g26-one-invalid-one-valid-check-missing-quote", CONTRACT["g"],
        manifest=mf([
            chk(cid="bad", quote=""),
            chk(cid="good", quote="absent", contentType="text/html", body="body.html",
                **html(b"<p>Hello world</p>")),
        ]),
        files=html(b"<p>Hello world</p>"), exit_code=2, verdict="could-not-evaluate",
        findings=[f("bad", "check_invalid"), f("good", "quote_missing")], evaluated=1)
    add("g27-checks-not-a-list-of-objects", CONTRACT["g"],
        manifest=mf(["not an object"]),
        exit_code=2, verdict="could-not-evaluate", findings=[f(None, "check_invalid")], evaluated=0)
    add("g28-final-hop-without-location", CONTRACT["g"],
        manifest=mf([chk(hops=[{"status": 200}], contentType="text/html", body="body.html",
                         **html(b"<p>Hello world</p>"))]),
        files=html(b"<p>Hello world</p>"), exit_code=0, verdict="clean", evaluated=1,
        accept=[alt(2, "could-not-evaluate", [f("k1", "check_invalid")], evaluated=0)])

    # ---- verdict rule -----------------------------------------------------
    add("v01-verdict-clean-when-no-finding", CONTRACT["verdict"],
        manifest=mf([chk(contentType="text/html", body="body.html", **html(b"<p>Hello world</p>"))]),
        files=html(b"<p>Hello world</p>"), exit_code=0, verdict="clean", evaluated=1)
    add("v02-verdict-failed-policy-on-unsupported-type", CONTRACT["verdict"],
        manifest=mf([chk(contentType="application/octet-stream", body="body.html", **html(b"x"))]),
        files=html(b"x"), exit_code=1, verdict="failed-policy",
        findings=[f("k1", "unsupported_type")], evaluated=None)
    add("v03-verdict-could-not-evaluate-on-check-invalid", CONTRACT["verdict"],
        manifest=mf([chk(quote="")]),
        exit_code=2, verdict="could-not-evaluate", findings=[f("k1", "check_invalid")], evaluated=0)
    add("v04-verdict-could-not-evaluate-on-charset-unsupported", CONTRACT["verdict"],
        manifest=mf([chk(contentType="text/html; charset=ebcdic", body="body.html",
                         **html(b"<p>Hello world</p>"))]),
        files=html(b"<p>Hello world</p>"), exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "charset_unsupported")], evaluated=None)
    add("v05-verdict-could-not-evaluate-on-input-invalid", CONTRACT["verdict"],
        raw=b"{", exit_code=2, verdict="could-not-evaluate",
        findings=[f(None, "input_invalid")], evaluated=0)

    # ---- usage errors (exit 64) ------------------------------------------
    add("u01-usage-missing-manifest-option", CONTRACT["usage"], argv=[],
        exit_code=64, verdict=None, shape=False)
    add("u02-usage-manifest-option-without-value", CONTRACT["usage"], argv=["--manifest"],
        exit_code=64, verdict=None, shape=False)
    add("u03-usage-unknown-option", CONTRACT["usage"], argv=["--manifest", "{manifest}", "--bogus"],
        exit_code=64, verdict=None, shape=False)
    add("u04-usage-unknown-option-without-manifest", CONTRACT["usage"], argv=["--bogus"],
        exit_code=64, verdict=None, shape=False)

    # ---- output shape -----------------------------------------------------
    add("o01-report-shape-one-json-object", CONTRACT["usage"],
        manifest=mf([chk(contentType="text/html", body="body.html", **html(b"<p>Hello world</p>"))]),
        files=html(b"<p>Hello world</p>"), exit_code=0, verdict="clean", evaluated=1)
    add("o02-report-shape-two-checks-two-evaluated", CONTRACT["usage"],
        manifest=mf([
            chk(cid="one", contentType="text/html", body="body.html", **html(b"<p>Hello world</p>")),
            chk(cid="two", quote="Hello", contentType="text/html", body="body.html",
                **html(b"<p>Hello world</p>")),
        ]),
        files=html(b"<p>Hello world</p>"), exit_code=0, verdict="clean", evaluated=2)
    add("o04-report-shape-mixed-clean-and-failing-checks", CONTRACT["usage"],
        manifest=mf([
            chk(cid="clean", contentType="text/html", body="body.html", **html(b"<p>Hello world</p>")),
            chk(cid="failing", quote="absent", contentType="text/html", body="body.html",
                **html(b"<p>Hello world</p>")),
        ]),
        files=html(b"<p>Hello world</p>"), exit_code=1, verdict="failed-policy",
        findings=[f("failing", "quote_missing")], evaluated=2)
    add("o03-report-shape-findings-carry-check-ids", CONTRACT["usage"],
        manifest=mf([
            chk(cid="one", quote="absent", contentType="text/html", body="body.html",
                **html(b"<p>Hello world</p>")),
            chk(cid="two", quote="also absent", contentType="text/html", body="body.html",
                **html(b"<p>Hello world</p>")),
        ]),
        files=html(b"<p>Hello world</p>"), exit_code=1, verdict="failed-policy",
        findings=[f("one", "quote_missing"), f("two", "quote_missing")], evaluated=2)


build_fixtures()


def tool_environment():
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.setdefault("LC_ALL", "C.UTF-8")
    return env


def project(findings):
    """Project findings on (check, reason), plus target for `moved` only."""
    rows = []
    if not isinstance(findings, list):
        raise ValueError("findings is not a list")
    for item in findings:
        if not isinstance(item, dict):
            rows.append(("<non-object>",))
            continue
        reason = item.get("reason")
        check = item.get("check")
        if reason == "moved":
            rows.append((json.dumps(check), str(reason), json.dumps(item.get("target"))))
        else:
            rows.append((json.dumps(check), str(reason)))
    return sorted(rows)


def expected_projection(findings):
    rows = []
    for item in findings:
        if item["reason"] == "moved":
            rows.append((json.dumps(item["check"]), item["reason"], json.dumps(item["target"])))
        else:
            rows.append((json.dumps(item["check"]), item["reason"]))
    return sorted(rows)


def snapshot(root):
    return {str(path.relative_to(root)) for path in root.rglob("*")}


def materialize(fixture, work):
    case_dir = work / fixture["name"]
    case_dir.mkdir(parents=True, exist_ok=True)
    for rel, data in fixture["files"].items():
        target = (case_dir / rel).resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    manifest_path = case_dir / "manifest.json"
    if fixture["raw"] is not None:
        manifest_path.write_bytes(fixture["raw"])
    elif fixture["manifest"] is not None:
        manifest_path.write_text(json.dumps(fixture["manifest"]), encoding="utf-8")
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
            timeout=TIMEOUT_SECONDS,
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

    if not fixture["shape"]:
        return problems
    if proc.returncode == 64:
        # A usage error need not print a JSON report; the exit code is the whole contract here.
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
        if not isinstance(item.get("reason"), str):
            problems.append("finding reason is not a string: %r" % (item,))
        elif item["reason"] not in REASONS:
            problems.append("unknown reason %r" % (item["reason"],))
        if item.get("check") is not None and not isinstance(item.get("check"), str):
            problems.append("finding check is neither a string nor null: %r" % (item,))
        if item.get("target") is not None and not isinstance(item.get("target"), str):
            problems.append("finding target is neither a URL string nor null: %r" % (item,))
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
        wanted = expected_projection(want["findings"])
        if wanted != got:
            mismatches.append("findings: expected %s, observed %s" % (wanted, got))
            continue
        if want["evaluated"] is not None and report.get("checksEvaluated") != want["evaluated"]:
            mismatches.append("checksEvaluated: expected %r, observed %r"
                              % (want["evaluated"], report.get("checksEvaluated")))
            continue
        return problems
    problems.extend("accepted alternative mismatch: %s" % item for item in mismatches)
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(description="source re-check audit self-test")
    parser.add_argument("--tool", default=str(DEFAULT_TOOL), help="tool under test")
    parser.add_argument("--list", action="store_true", help="list fixture names and exit")
    args = parser.parse_args(argv)

    if args.list:
        try:
            for fixture in FIXTURES:
                print("%s\t%s" % (fixture["name"], fixture["contract"][:40]))
        except BrokenPipeError:
            pass
        return 0

    tool = Path(args.tool).resolve()
    summary = {
        "selftest": "kake-r36-source-recheck-selftest",
        "tool": str(tool),
        "cases": len(FIXTURES),
        "passed": 0,
        "failed": 0,
        "passedOverTotal": "0/%d" % len(FIXTURES),
        "verdict": "clean",
        "failures": [],
    }
    if len(FIXTURES) < MIN_FIXTURES:
        summary["verdict"] = "could-not-evaluate"
        summary["failed"] = 1
        summary["failures"] = [{"case": None,
                                "reasons": ["only %d fixtures; expected at least %d"
                                            % (len(FIXTURES), MIN_FIXTURES)]}]
        print(json.dumps(summary, sort_keys=True))
        return 2
    if not tool.is_file():
        summary["verdict"] = "could-not-evaluate"
        summary["failed"] = 1
        summary["failures"] = [{"case": None, "reasons": ["tool not found: %s" % tool]}]
        print(json.dumps(summary, sort_keys=True))
        return 2

    work = Path(tempfile.mkdtemp(prefix="kake-r36-selftest-"))
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
        shutil.rmtree(work, ignore_errors=True)

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
