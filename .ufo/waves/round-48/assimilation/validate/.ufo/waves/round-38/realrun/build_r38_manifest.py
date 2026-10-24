#!/usr/bin/env python3
"""Build the round-38 C2 real-run manifests on the 12 retained round-37 robots files.

Extends the round-37 real-run manifest (55 checks, copied verbatim with their
evidence and re-pointed at ./robots/) with 36 checks over the same live files:

  * (k) implicit /robots.txt allow on the normalized path: /robots%2Etxt and
    /%72obots.txt, one per host where rules would otherwise decide, both forms
    on en.wikipedia.org under UbiCrawler (whose group is `Disallow: /`);
  * (i) URL characters: one URL per host carrying an excluded ASCII character
    (space, ", \\, {, |, ^, `, }, >, <, U+0001, U+007F); expected outcome is a
    check fault (check_invalid);
  * one ordinary percent-encoded path per host (reserved escapes kept,
    unreserved escapes decoded), expectation decided by a quoted rule line.

Also builds (h) fault manifests: a 5,000-digit robotsStatus, a 5,000-digit
integer in an unread field, NaN in an unread field, Infinity and -Infinity as
status, and 1e400 as status. Each fault manifest references the same retained
robots files.

Every quote is asserted verbatim at its line against the retained bytes, and
each retained body's sha256 is re-checked against the round-37 fetch receipts,
so no expectation can drift from the recorded file.

The expected reports in expectations.json are declared here by hand from the
round-38 contract text; nothing in this script runs a robots matcher.
"""
import hashlib
import json
import os
import sys

sys.set_int_max_str_digits(0)

HERE = os.path.dirname(os.path.abspath(__file__))
ROBOTS = os.path.join(HERE, "robots")
RECEIPTS = json.load(open(os.path.join(ROBOTS, "receipts.json"), encoding="utf-8"))["receipts"]
REC = {r["url"]: r for r in RECEIPTS}

# Round-37 manifest is read from the lane copy (read-only); only its checks are used.
LANE_MANIFEST = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-37/realrun/robots/manifest.json"


def lines_of(path):
    """Round-37 line rule: BOM stripped, CR/LF/CRLF terminate, final line counts."""
    data = open(path, "rb").read()
    if data.startswith(b"\xef\xbb\xbf"):
        data = data[3:]
    text = data.decode("utf-8", "replace")
    out, cur, i = [], [], 0
    while i < len(text):
        ch = text[i]
        if ch == "\r":
            out.append("".join(cur))
            cur = []
            if i + 1 < len(text) and text[i + 1] == "\n":
                i += 1
        elif ch == "\n":
            out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
        i += 1
    if cur:
        out.append("".join(cur))
    return out


FILES = {name: lines_of(os.path.join(ROBOTS, name))
         for name in os.listdir(ROBOTS) if name.endswith(".txt")}
for name, lines in FILES.items():
    body = open(os.path.join(ROBOTS, name), "rb").read()
    digest = hashlib.sha256(body).hexdigest()
    rec = [r for r in RECEIPTS if r["body"] == name][0]
    assert digest == rec["sha256"], (name, digest, rec["sha256"])
    assert len(body) == rec["bytes"], name

HOSTS = [
    "www.rfc-editor.org", "developers.google.com", "github.com", "docs.github.com",
    "www.sitemaps.org", "developer.mozilla.org", "en.wikipedia.org", "www.robotstxt.org",
    "html.spec.whatwg.org", "pages.github.com", "ds4cc.com", "veigapunk.github.io",
]
assert len(HOSTS) == 12


def robot(host):
    return host.replace(".", "_") + ".txt"


def evidence(cid, host, quotes, why):
    rec = REC[f"https://{host}/robots.txt"]
    assert rec["status"] == 200, (cid, rec["status"])
    name = rec["body"]
    lines = FILES[name]
    qs = []
    for ln, text in quotes:
        if ln < 1 or ln > len(lines):
            sys.exit(f"{cid}: line {ln} outside {name} ({len(lines)} lines)")
        if lines[ln - 1] != text:
            sys.exit(f"{cid}: quote mismatch at {name}:{ln}: {lines[ln-1]!r} != {text!r}")
        qs.append({"line": ln, "text": text})
    return {
        "sourceUrl": rec["url"],
        "finalUrl": rec["finalUrl"],
        "fetchedUtc": rec["timeUtc"],
        "bodySha256": rec["sha256"],
        "quotes": qs,
        "why": why,
    }


# (id, host, userAgent, url, outcome, quotes, why)
# outcome: "allow" | "disallow" | "check_invalid" -- the declared correct result.
NEW = [
    # ---- www.rfc-editor.org -------------------------------------------------
    ("r38-k-www_rfc-editor_org-pct2e", "www.rfc-editor.org", "Googlebot",
     "https://www.rfc-editor.org/robots%2Etxt", "allow",
     [(2, "Disallow: /rfc/authors/"), (3, "Disallow: /rfc/rerendered/"), (4, "Disallow: /rfc/v3test/")],
     "Contract (k): %2E is an unreserved escape of '.', so the path to match normalizes to exactly "
     "/robots.txt; a URL whose normalized path is /robots.txt is allowed. The raw path /robots%2Etxt "
     "is not /robots.txt, so a raw-path comparison would fall through to these three Disallow rules "
     "(none of which matches it) instead of the implicit allow."),
    ("r38-i-www_rfc-editor_org-space", "www.rfc-editor.org", "Googlebot",
     "https://www.rfc-editor.org/rfc/rfc 9309.html", "check_invalid",
     [(2, "Disallow: /rfc/authors/"), (3, "Disallow: /rfc/rerendered/"), (4, "Disallow: /rfc/v3test/")],
     "Contract (i): the space (U+0020) is ASCII outside the RFC 3986 character set, so the check is a "
     "check fault (check_invalid) and no access result is evaluated. Were it admitted, the path would "
     "be outside the three disallowed subtrees; the space cannot make any of them a prefix."),
    ("r38-e-www_rfc-editor_org-authors", "www.rfc-editor.org", "Googlebot",
     "https://www.rfc-editor.org/rfc/%61uthors/team", "disallow",
     [(2, "Disallow: /rfc/authors/")],
     "Contract (e): %61 is an unreserved escape of 'a' and is decoded before matching, so the path to "
     "match is /rfc/authors/team, which begins with the disallowed /rfc/authors/ subtree."),

    # ---- developers.google.com ---------------------------------------------
    ("r38-k-developers_google_com-pct72", "developers.google.com", "Googlebot",
     "https://developers.google.com/%72obots.txt", "allow",
     [(2, "Disallow: /youtube/partner/")],
     "Contract (k): %72 is an unreserved escape of 'r' and decodes, so the path to match is exactly "
     "/robots.txt and the URL is allowed. The file's only rule covers /youtube/partner/, so no rule "
     "matches either the raw path or the normalized one; (k) makes the allow independent of that."),
    ("r38-i-developers_google_com-quote", "developers.google.com", "Googlebot",
     "https://developers.google.com/search/docs/robots\"txt", "check_invalid",
     [(2, "Disallow: /youtube/partner/")],
     "Contract (i): the double quote is ASCII outside the RFC 3986 character set, so the check is a "
     "check fault (check_invalid); no allow or disallow is evaluated. The path is outside the only "
     "disallowed subtree either way."),
    ("r38-e-developers_google_com-partner", "developers.google.com", "Googlebot",
     "https://developers.google.com/youtube/%70artner/docs", "disallow",
     [(2, "Disallow: /youtube/partner/")],
     "Contract (e): %70 is an unreserved escape of 'p', decoded before matching, so the path is "
     "/youtube/partner/docs and begins with the disallowed partner subtree."),

    # ---- github.com ---------------------------------------------------------
    ("r38-k-github_com-pct2e", "github.com", "Googlebot",
     "https://github.com/robots%2Etxt", "allow",
     [(360, "User-agent: *")],
     "Contract (k): %2E decodes to '.', so the path to match is exactly /robots.txt and the URL is "
     "allowed. No Googlebot group exists, so the * group's 165 rules decide the raw path "
     "/robots%2Etxt; none of them matches /robots.txt (the closest shapes are anchored records such "
     "as Disallow: /search$), so the allow holds either way and (k) states it on the normalized path."),
    ("r38-i-github_com-caret", "github.com", "Googlebot",
     "https://github.com/veigapunk^kake", "check_invalid",
     [(360, "User-agent: *")],
     "Contract (i): '^' is ASCII outside the RFC 3986 character set, so the check is a check fault "
     "(check_invalid); no access result is evaluated. The path /veigapunk^kake matches none of the "
     "* group's rules."),
    ("r38-e-github_com-gist", "github.com", "Googlebot",
     "https://github.com/gist/veigapunk/%61bc", "disallow",
     [(360, "User-agent: *"), (370, "Disallow: /gist/")],
     "Contract (e): %61 is an unreserved escape of 'a', decoded before matching, so the path is "
     "/gist/veigapunk/abc, which begins with the disallowed /gist/ subtree."),

    # ---- docs.github.com ----------------------------------------------------
    ("r38-k-docs_github_com-pct2e", "docs.github.com", "Googlebot",
     "https://docs.github.com/robots%2Etxt", "allow",
     [(1, "User-agent: *")],
     "Contract (k): %2E decodes to '.', so the path to match is exactly /robots.txt and the URL is "
     "allowed. The 13-byte file holds one user-agent record and no rule record, so the raw path is "
     "unrestricted as well; (k) fixes the allow on the normalized path."),
    ("r38-i-docs_github_com-backslash", "docs.github.com", "Googlebot",
     "https://docs.github.com/en\\pages", "check_invalid",
     [(1, "User-agent: *")],
     "Contract (i): the backslash is ASCII outside the RFC 3986 character set, so the check is a "
     "check fault (check_invalid); no access result is evaluated. The file declares no rule record."),
    ("r38-e-docs_github_com-escslash", "docs.github.com", "Googlebot",
     "https://docs.github.com/en/pages%2Findex", "allow",
     [(1, "User-agent: *")],
     "Contract (e): %2F is a reserved escape and is kept as %2F (uppercased), not decoded to '/', so "
     "the path is /en/pages%2Findex; the file holds no Allow or Disallow record, so it is allowed."),

    # ---- ds4cc.com ----------------------------------------------------------
    ("r38-k-ds4cc_com-pct72", "ds4cc.com", "Googlebot",
     "https://ds4cc.com/%72obots.txt", "allow",
     [(2, "Allow: /")],
     "Contract (k): %72 decodes to 'r', so the path to match is exactly /robots.txt and the URL is "
     "allowed. The group's Allow: / would allow it in any case; (k) makes the allow independent of "
     "the rule."),
    ("r38-i-ds4cc_com-braceopen", "ds4cc.com", "Googlebot",
     "https://ds4cc.com/posts/{2026", "check_invalid",
     [(2, "Allow: /")],
     "Contract (i): '{' is ASCII outside the RFC 3986 character set, so the check is a check fault "
     "(check_invalid); no access result is evaluated. The Allow: / prefix would otherwise allow it."),
    ("r38-e-ds4cc_com-index", "ds4cc.com", "Googlebot",
     "https://ds4cc.com/index%2Ehtml", "allow",
     [(2, "Allow: /")],
     "Contract (e): %2E decodes to '.', so the path is /index.html; the group's Allow: / is a prefix "
     "rule covering every path on the host."),

    # ---- en.wikipedia.org ---------------------------------------------------
    ("r38-k-en_wikipedia_org-pct2e", "en.wikipedia.org", "UbiCrawler",
     "https://en.wikipedia.org/robots%2Etxt", "allow",
     [(27, "User-agent: UbiCrawler"), (28, "Disallow: /")],
     "Contract (k): UbiCrawler has its own group whose only rule is Disallow: /. The raw path "
     "/robots%2Etxt is not /robots.txt, so comparing before normalization applies that rule and "
     "disallows; %2E is an unreserved escape of '.', so the path to match normalizes to exactly "
     "/robots.txt and the URL is allowed."),
    ("r38-k-en_wikipedia_org-pct72", "en.wikipedia.org", "UbiCrawler",
     "https://en.wikipedia.org/%72obots.txt", "allow",
     [(27, "User-agent: UbiCrawler"), (28, "Disallow: /")],
     "Contract (k): %72 is an unreserved escape of 'r'; the path to match normalizes to exactly "
     "/robots.txt, which is allowed, while the raw path /%72obots.txt would be caught by the group's "
     "Disallow: /."),
    ("r38-i-en_wikipedia_org-pipe", "en.wikipedia.org", "Googlebot",
     "https://en.wikipedia.org/wiki/A|B", "check_invalid",
     [(148, "User-agent: *"), (156, "Disallow: /wiki/Special:")],
     "Contract (i): '|' is ASCII outside the RFC 3986 character set, so the check is a check fault "
     "(check_invalid); no access result is evaluated. No Googlebot group exists, the * group decides, "
     "and /wiki/A|B matches no rule of it (e.g. the Special: prefix does not apply)."),

    # ---- html.spec.whatwg.org ----------------------------------------------
    ("r38-k-html_spec_whatwg_org-pct2e", "html.spec.whatwg.org", "Googlebot",
     "https://html.spec.whatwg.org/robots%2Etxt", "allow",
     [(2, "Disallow: /commit-snapshots/"), (3, "Disallow: /review-drafts/")],
     "Contract (k): %2E decodes to '.', so the path to match is exactly /robots.txt and the URL is "
     "allowed. The two disallowed working-draft trees do not cover it either way; (k) fixes the "
     "allow on the normalized path."),
    ("r38-i-html_spec_whatwg_org-backtick", "html.spec.whatwg.org", "Googlebot",
     "https://html.spec.whatwg.org/x`y", "check_invalid",
     [(2, "Disallow: /commit-snapshots/"), (3, "Disallow: /review-drafts/")],
     "Contract (i): the backtick is ASCII outside the RFC 3986 character set, so the check is a check "
     "fault (check_invalid); no access result is evaluated. Neither disallowed tree covers the path."),
    ("r38-e-html_spec_whatwg_org-commit", "html.spec.whatwg.org", "Googlebot",
     "https://html.spec.whatwg.org/commit-snapshots%2F1234", "allow",
     [(2, "Disallow: /commit-snapshots/")],
     "Contract (e): %2F is a reserved escape and is kept, so the path is "
     "/commit-snapshots%2F1234, which does not begin with /commit-snapshots/ (the character after "
     "the name is '%', not '/'); the rule is a prefix rule and does not match."),

    # ---- pages.github.com ---------------------------------------------------
    ("r38-k-pages_github_com-pct2e", "pages.github.com", "Googlebot",
     "https://pages.github.com/robots%2Etxt", "allow",
     [(1, "Sitemap: https://pages.github.com/sitemap.xml")],
     "Contract (k): %2E decodes to '.', so the path to match is exactly /robots.txt and the URL is "
     "allowed. The only record is a Sitemap record, which opens no group, so the raw path is "
     "unrestricted as well."),
    ("r38-i-pages_github_com-braceclose", "pages.github.com", "Googlebot",
     "https://pages.github.com/a}b", "check_invalid",
     [(1, "Sitemap: https://pages.github.com/sitemap.xml")],
     "Contract (i): '}' is ASCII outside the RFC 3986 character set, so the check is a check fault "
     "(check_invalid); no access result is evaluated. No group exists in the file."),
    ("r38-e-pages_github_com-project", "pages.github.com", "Googlebot",
     "https://pages.github.com/project%2Fpage", "allow",
     [(1, "Sitemap: https://pages.github.com/sitemap.xml")],
     "Contract (e): %2F is a reserved escape and is kept as %2F, so the path is /project%2Fpage; the "
     "file holds no user-agent record, hence no rule, so the URL is allowed."),

    # ---- veigapunk.github.io ------------------------------------------------
    ("r38-k-veigapunk_github_io-pct72", "veigapunk.github.io", "Googlebot",
     "https://veigapunk.github.io/%72obots.txt", "allow",
     [(2, "Allow: /")],
     "Contract (k): %72 decodes to 'r', so the path to match is exactly /robots.txt and the URL is "
     "allowed. The group's Allow: / covers it in any case; (k) fixes the allow on the normalized "
     "path."),
    ("r38-i-veigapunk_github_io-gt", "veigapunk.github.io", "Googlebot",
     "https://veigapunk.github.io/a>b", "check_invalid",
     [(2, "Allow: /")],
     "Contract (i): '>' is ASCII outside the RFC 3986 character set, so the check is a check fault "
     "(check_invalid); no access result is evaluated. Allow: / would otherwise allow it."),
    ("r38-e-veigapunk_github_io-index", "veigapunk.github.io", "Googlebot",
     "https://veigapunk.github.io/index%2Ehtml", "allow",
     [(2, "Allow: /")],
     "Contract (e): %2E decodes to '.', so the path is /index.html and the group's Allow: / prefix "
     "rule covers it."),

    # ---- www.robotstxt.org --------------------------------------------------
    ("r38-k-www_robotstxt_org-pct2e", "www.robotstxt.org", "Googlebot",
     "https://www.robotstxt.org/robots%2Etxt", "allow",
     [(2, "Disallow:")],
     "Contract (k): %2E decodes to '.', so the path to match is exactly /robots.txt and the URL is "
     "allowed. The group's only rule has an empty value, which never matches, so the raw path is "
     "unrestricted as well."),
    ("r38-i-www_robotstxt_org-lt", "www.robotstxt.org", "Googlebot",
     "https://www.robotstxt.org/a<b", "check_invalid",
     [(2, "Disallow:")],
     "Contract (i): '<' is ASCII outside the RFC 3986 character set, so the check is a check fault "
     "(check_invalid); no access result is evaluated."),
    ("r38-e-www_robotstxt_org-tilde", "www.robotstxt.org", "Googlebot",
     "https://www.robotstxt.org/%7Euser/page", "allow",
     [(2, "Disallow:")],
     "Contract (e): %7E is an unreserved escape of '~' and is decoded, so the path is /~user/page; "
     "the group's only rule has an empty value, which never matches, so the URL is allowed."),

    # ---- www.sitemaps.org ---------------------------------------------------
    ("r38-k-www_sitemaps_org-pct72", "www.sitemaps.org", "Googlebot",
     "https://www.sitemaps.org/%72obots.txt", "allow",
     [(1, "Sitemap: https://www.sitemaps.org/sitemap.xml")],
     "Contract (k): %72 decodes to 'r', so the path to match is exactly /robots.txt and the URL is "
     "allowed. The only record is a Sitemap record, which opens no group."),
    ("r38-i-www_sitemaps_org-ctl", "www.sitemaps.org", "Googlebot",
     "https://www.sitemaps.org/protocol.html\u0001", "check_invalid",
     [(1, "Sitemap: https://www.sitemaps.org/sitemap.xml")],
     "Contract (i): U+0001 is a control character, ASCII outside the RFC 3986 character set, so the "
     "check is a check fault (check_invalid); no access result is evaluated."),
    ("r38-e-www_sitemaps_org-xml", "www.sitemaps.org", "Googlebot",
     "https://www.sitemaps.org/sitemap%2Exml", "allow",
     [(1, "Sitemap: https://www.sitemaps.org/sitemap.xml")],
     "Contract (e): %2E decodes to '.', so the path is /sitemap.xml; the file holds no rule record, "
     "so the URL is allowed."),

    # ---- developer.mozilla.org ---------------------------------------------
    ("r38-k-developer_mozilla_org-pct2e", "developer.mozilla.org", "Googlebot",
     "https://developer.mozilla.org/robots%2Etxt", "allow",
     [(4, "Disallow: /api/"), (5, "Disallow: /*/files/"), (6, "Disallow: /media")],
     "Contract (k): %2E decodes to '.', so the path to match is exactly /robots.txt and the URL is "
     "allowed. The group's three rules (/api/, /*/files/, /media) do not cover it either way; (k) "
     "fixes the allow on the normalized path."),
    ("r38-i-developer_mozilla_org-del", "developer.mozilla.org", "Googlebot",
     "https://developer.mozilla.org/en-US/docs/Web\u007f", "check_invalid",
     [(4, "Disallow: /api/"), (5, "Disallow: /*/files/"), (6, "Disallow: /media")],
     "Contract (i): U+007F is a control character, ASCII outside the RFC 3986 character set, so the "
     "check is a check fault (check_invalid); no access result is evaluated. The path is outside all "
     "three disallowed rules."),
    ("r38-e-developer_mozilla_org-api", "developer.mozilla.org", "Googlebot",
     "https://developer.mozilla.org/api%2Fv1", "allow",
     [(4, "Disallow: /api/")],
     "Contract (e): %2F is a reserved escape and is kept, so the path is /api%2Fv1; the rule value "
     "/api/ ends in '/', which the path does not have at that position, so the prefix rule does not "
     "match and the URL is allowed."),
]

# ---------------------------------------------------------------------------
# main manifest: 55 round-37 checks (verbatim, re-pointed at ./robots/) + NEW
# ---------------------------------------------------------------------------
ROUND37 = json.load(open(LANE_MANIFEST, encoding="utf-8"))
assert ROUND37["version"] == 1 and len(ROUND37["checks"]) == 55

checks = []
for c in ROUND37["checks"]:
    c = json.loads(json.dumps(c))  # deep copy
    assert "/" not in c["robots"], c["robots"]
    c["robots"] = "robots/" + c["robots"]
    assert os.path.isfile(os.path.join(HERE, c["robots"])), c["robots"]
    checks.append(c)

for cid, host, ua, url, outcome, quotes, why in NEW:
    name = robot(host)
    checks.append({
        "id": cid,
        "robotsStatus": 200,
        "userAgent": ua,
        "url": url,
        "expect": "allow" if outcome != "disallow" else "disallow",
        "robots": "robots/" + name,
        "evidence": evidence(cid, host, quotes, why),
    })

ids = [c["id"] for c in checks]
assert len(ids) == len(set(ids)), "duplicate ids"
assert len(checks) == 91, len(checks)

manifest = {"version": 1, "checks": checks}
strict = {"version": 1, "checks": [
    {k: c[k] for k in ("id", "robotsStatus", "userAgent", "url", "expect", "robots")}
    for c in checks
]}
with open(os.path.join(HERE, "manifest.json"), "w", encoding="utf-8") as fh:
    json.dump(manifest, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
with open(os.path.join(HERE, "manifest.strict.json"), "w", encoding="utf-8") as fh:
    json.dump(strict, fh, indent=2, ensure_ascii=False)
    fh.write("\n")

# ---------------------------------------------------------------------------
# (h) fault manifests -- each references the same retained robots files
# ---------------------------------------------------------------------------
RFC = "https://www.rfc-editor.org/rfc/rfc9309.html"
GITHUB = "https://github.com/features"
RFC_ROBOTS = "robots/www_rfc-editor_org.txt"
GITHUB_ROBOTS = "robots/github_com.txt"


def base_check(cid, url, robots, expect, why):
    host = "www.rfc-editor.org" if "rfc-editor" in robots else "github.com"
    return {
        "id": cid,
        "robotsStatus": 200,
        "userAgent": "Googlebot",
        "url": url,
        "expect": expect,
        "robots": robots,
        "evidence": evidence(cid, host, [(2, "Disallow: /rfc/authors/")] if host.startswith("www")
                             else [(360, "User-agent: *")], why),
    }


NORMAL_RFC = base_check(
    "h-neighbour-rfc", RFC, RFC_ROBOTS, "allow",
    "Ordinary control check: the RFC 9309 page is outside the three disallowed subtrees, so it is "
    "allowed; it is evaluated while a sibling fault check faults, and is untouched by an unused long "
    "integer.")
NORMAL_GITHUB = base_check(
    "h-neighbour-github", GITHUB, GITHUB_ROBOTS, "allow",
    "Ordinary control check: /features matches none of the * group's rules, so it is allowed.")

big = int("9" * 5000)

long_status = {
    "version": 1,
    "checks": [
        {
            "id": "h-long-status-5000",
            "robotsStatus": big,
            "userAgent": "Googlebot",
            "url": RFC,
            "expect": "allow",
            "robots": RFC_ROBOTS,
            "evidence": evidence(
                "h-long-status-5000", "www.rfc-editor.org", [(2, "Disallow: /rfc/authors/")],
                "Contract (h): a robotsStatus integer of any length is JSON; 5,000 nines is an "
                "integer outside the 200-299/400-499/500-599 ranges, so this check alone is a check "
                "fault (check_invalid) and the other check is still evaluated. A reader that refuses "
                "the manifest or the number is wrong."),
        },
        NORMAL_RFC,
    ],
}

unused_big = {
    "version": 1,
    "checks": [
        dict(NORMAL_RFC, unusedCounter=big),
        NORMAL_GITHUB,
    ],
}

nan_unused = {
    "version": 1,
    "checks": [
        NORMAL_RFC,
        dict(NORMAL_GITHUB, unusedMarker=float("nan")),
    ],
}

def status_literal_manifest(cid, literal, literal_name):
    return {
        "version": 1,
        "checks": [
            {
                "id": cid,
                "robotsStatus": literal,
                "userAgent": "Googlebot",
                "url": RFC,
                "expect": "allow",
                "robots": RFC_ROBOTS,
                "evidence": evidence(
                    cid, "www.rfc-editor.org", [(2, "Disallow: /rfc/authors/")],
                    f"Contract (h): {literal_name} outside a string is not JSON, so a manifest "
                    "holding it gives one input_invalid finding (check null) and nothing is "
                    "evaluated; the neighbour is not evaluated either."),
            },
            NORMAL_RFC,
        ],
    }


inf_status = status_literal_manifest("h-infinity-status", float("inf"), "Infinity")
neginf_status = status_literal_manifest("h-neginfinity-status", float("-inf"), "-Infinity")

float_status = {
    "version": 1,
    "checks": [
        {
            "id": "h-float-status-1e400",
            "robotsStatus": "__RAW_1E400__",
            "userAgent": "Googlebot",
            "url": RFC,
            "expect": "allow",
            "robots": RFC_ROBOTS,
            "evidence": evidence(
                "h-float-status-1e400", "www.rfc-editor.org", [(2, "Disallow: /rfc/authors/")],
                "Contract (h) clarification: 1e400 is a JSON number but not an integer (it stays a "
                "float), and robotsStatus must be an integer, so this check alone is a check fault "
                "(check_invalid); the neighbour is still evaluated. Contrast with Infinity above, "
                "which is not JSON at all."),
        },
        NORMAL_RFC,
    ],
}

FAULT = {
    "manifest.h-long-status.json": long_status,
    "manifest.h-unused-bigint.json": unused_big,
    "manifest.h-nan-unused.json": nan_unused,
    "manifest.h-infinity-status.json": inf_status,
    "manifest.h-neginfinity-status.json": neginf_status,
    "manifest.h-float-status.json": float_status,
}
for filename, doc in FAULT.items():
    text = json.dumps(doc, indent=2, ensure_ascii=False)
    text = text.replace('"__RAW_1E400__"', "1e400")
    with open(os.path.join(HERE, filename), "w", encoding="utf-8") as fh:
        fh.write(text + "\n")

# ---------------------------------------------------------------------------
# declared expected reports (hand-written from the round-38 contract)
# ---------------------------------------------------------------------------
main_faults = [cid for cid, *_ in NEW if _[3] == "check_invalid"]
assert len(main_faults) == 12, len(main_faults)

EXPECT = {
    "manifest.json": {
        "exit": 2,
        "verdict": "could-not-evaluate",
        "checksEvaluated": 91 - 12,
        "findings": [{"check": cid, "reason": "check_invalid"} for cid in main_faults],
        "basis": "The 12 (i) checks are check faults; the other 79 checks (55 round-37 + 13 (k) "
                 "allow + 11 ordinary percent-encoded path) have no finding. Any check_invalid makes "
                 "the verdict could-not-evaluate and exit 2 (round-37 verdict rule).",
    },
    "manifest.h-long-status.json": {
        "exit": 2,
        "verdict": "could-not-evaluate",
        "checksEvaluated": 1,
        "findings": [{"check": "h-long-status-5000", "reason": "check_invalid"}],
        "basis": "(h): a 5,000-digit out-of-range integer status is a check fault for that check "
                 "only; the neighbour is evaluated and allowed.",
    },
    "manifest.h-unused-bigint.json": {
        "exit": 0,
        "verdict": "clean",
        "checksEvaluated": 2,
        "findings": [],
        "basis": "(h): a 5,000-digit integer in a field the contract does not read changes nothing; "
                 "both checks are evaluated and allowed.",
    },
    "manifest.h-nan-unused.json": {
        "exit": 2,
        "verdict": "could-not-evaluate",
        "checksEvaluated": 0,
        "findings": [{"check": None, "reason": "input_invalid"}],
        "basis": "(h): NaN outside a string is not JSON, so the manifest is input_invalid and nothing "
                 "is evaluated -- even though the NaN sits in a field no rule reads.",
    },
    "manifest.h-infinity-status.json": {
        "exit": 2,
        "verdict": "could-not-evaluate",
        "checksEvaluated": 0,
        "findings": [{"check": None, "reason": "input_invalid"}],
        "basis": "(h): Infinity outside a string is not JSON, so the manifest is input_invalid and "
                 "nothing is evaluated.",
    },
    "manifest.h-neginfinity-status.json": {
        "exit": 2,
        "verdict": "could-not-evaluate",
        "checksEvaluated": 0,
        "findings": [{"check": None, "reason": "input_invalid"}],
        "basis": "(h): -Infinity outside a string is not JSON, so the manifest is input_invalid and "
                 "nothing is evaluated.",
    },
    "manifest.h-float-status.json": {
        "exit": 2,
        "verdict": "could-not-evaluate",
        "checksEvaluated": 1,
        "findings": [{"check": "h-float-status-1e400", "reason": "check_invalid"}],
        "basis": "(h) clarification: 1e400 is JSON but not an integer, so the status is a check fault "
                 "for that check; the neighbour is evaluated and allowed.",
    },
}

per_check = {}
for cid, host, ua, url, outcome, quotes, why in NEW:
    per_check[cid] = {
        "host": host, "userAgent": ua, "url": url,
        "declaredOutcome": outcome,
        "quotes": [{"line": ln, "text": text} for ln, text in quotes],
        "why": why,
    }

with open(os.path.join(HERE, "expectations.json"), "w", encoding="utf-8") as fh:
    json.dump({
        "version": 1,
        "contract": "SCORECARD.md round-38 C2 rules (h), (i), (k); round-37 contract otherwise",
        "sealedKeyNote": "these expectations are derived from the public contract, not from any sealed case",
        "manifests": EXPECT,
        "newChecks": per_check,
    }, fh, indent=2, ensure_ascii=False)
    fh.write("\n")

print("main manifest checks:", len(checks))
print("new checks:", len(NEW), "faults:", len(main_faults))
print("fault manifests:", ", ".join(sorted(FAULT)))
print("expected main:", EXPECT["manifest.json"]["verdict"],
      EXPECT["manifest.json"]["checksEvaluated"],
      "findings", len(EXPECT["manifest.json"]["findings"]))
