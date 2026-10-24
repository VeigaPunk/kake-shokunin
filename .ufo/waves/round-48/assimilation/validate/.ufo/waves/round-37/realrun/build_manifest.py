#!/usr/bin/env python3
"""Build the C1-shaped manifest (and its contract-minimal projection) from the
recorded robots.txt bodies.

Every expectation is grounded in verbatim lines of the recorded file; the script
asserts each quoted line against the recorded bytes, so a quote cannot drift.
No robots matching is implemented here: the expectations are the hand-derived
table below. This tool only assembles JSON and checks that each quote exists.
"""
import hashlib
import json
import os
import sys

BASE = "/fast/scratch/hyaku/kake-r37w1/ExecLiveRobotsSnapshot"
ROBOTS = os.path.join(BASE, "robots")

receipts = {r["url"]: r for r in json.load(open(os.path.join(ROBOTS, "receipts.json")))["receipts"]}


def lines_of(name):
    data = open(os.path.join(ROBOTS, name), "rb").read()
    if data.startswith(b"\xef\xbb\xbf"):
        data = data[3:]
    text = data.decode("utf-8", "replace")
    # CR, LF or CRLF terminate a line; a final unterminated line is still a line.
    out, cur = [], []
    i = 0
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


FILES = {}
for f in os.listdir(ROBOTS):
    if f.endswith(".txt"):
        FILES[f] = lines_of(f)

# (id, host, robotsStatus-receipt-url, userAgent, url, expect, robots file, quotes[(line, text)], why)
CHECKS = [
    # www.rfc-editor.org -- group "*": three Disallow records, everything else open.
    ("rfc-editor-rfc9309-html", "www.rfc-editor.org", "Googlebot",
     "https://www.rfc-editor.org/rfc/rfc9309.html", "allow", "www_rfc-editor_org.txt",
     [(2, "Disallow: /rfc/authors/"), (3, "Disallow: /rfc/rerendered/"), (4, "Disallow: /rfc/v3test/")],
     "The group's only rule values are the three Disallow paths; none of them is a prefix of "
     "/rfc/rfc9309.html, so the published spec page is meant to stay crawlable (the file also advertises a sitemap)."),
    ("rfc-editor-rerendered", "www.rfc-editor.org", "Googlebot",
     "https://www.rfc-editor.org/rfc/rerendered/rfc9309.html", "disallow", "www_rfc-editor_org.txt",
     [(3, "Disallow: /rfc/rerendered/")],
     "The path begins with the disallowed /rfc/rerendered/ subtree, which the publisher keeps out of crawlers."),
    ("rfc-editor-authors", "www.rfc-editor.org", "Googlebot",
     "https://www.rfc-editor.org/rfc/authors/", "disallow", "www_rfc-editor_org.txt",
     [(2, "Disallow: /rfc/authors/")],
     "The URL path is exactly the disallowed authoring area, which the publisher hides from crawlers."),
    ("rfc-editor-v3test", "www.rfc-editor.org", "Googlebot",
     "https://www.rfc-editor.org/rfc/v3test/42/experiment", "disallow", "www_rfc-editor_org.txt",
     [(4, "Disallow: /rfc/v3test/")],
     "The test tree under /rfc/v3test/ is disallowed and the URL sits inside it."),
    ("rfc-editor-rfc-index", "www.rfc-editor.org", "Googlebot",
     "https://www.rfc-editor.org/rfc/", "allow", "www_rfc-editor_org.txt",
     [(2, "Disallow: /rfc/authors/"), (3, "Disallow: /rfc/rerendered/"), (4, "Disallow: /rfc/v3test/")],
     "The RFC index is outside all three disallowed subtrees, so a publisher intends it to be indexed."),

    # developers.google.com -- group "*": one Disallow record plus a Sitemap record.
    ("google-youtube-partner-docs", "developers.google.com", "Googlebot",
     "https://developers.google.com/youtube/partner/docs", "disallow", "developers_google_com.txt",
     [(2, "Disallow: /youtube/partner/")],
     "The partner documentation subtree is the file's only rule and the URL is inside it."),
    ("google-youtube-partner-hub", "developers.google.com", "Googlebot",
     "https://developers.google.com/youtube/partner", "allow", "developers_google_com.txt",
     [(2, "Disallow: /youtube/partner/")],
     "The rule value ends in a slash, so the hub path /youtube/partner (no trailing slash) is not "
     "covered; the publisher blocks the documentation subtree, not the hub."),
    ("google-search-robots-txt-doc", "developers.google.com", "Googlebot",
     "https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt", "allow",
     "developers_google_com.txt",
     [(2, "Disallow: /youtube/partner/")],
     "The only rule covers /youtube/partner/, so Google's own robots.txt specification page stays crawlable."),
    ("google-sitemap-xml", "developers.google.com", "Googlebot",
     "https://developers.google.com/sitemap.xml", "allow", "developers_google_com.txt",
     [(3, "Sitemap: https://developers.google.com/sitemap.xml")],
     "The publisher advertises this file in the ignored Sitemap record; no rule disallows it."),

    # github.com -- no Googlebot group, so the \"*\" group beginning line 360 decides.
    ("github-account-login", "github.com", "Googlebot",
     "https://github.com/account-login", "disallow", "github_com.txt",
     [(360, "User-agent: *"), (364, "Disallow: /account-login")],
     "Googlebot has no group of its own here, so the * group decides, and it disallows /account-login."),
    ("github-search", "github.com", "Googlebot",
     "https://github.com/search", "disallow", "github_com.txt",
     [(360, "User-agent: *"), (372, "Disallow: /search$")],
     "The anchored rule matches the path /search exactly, which the publisher keeps out of crawlers."),
    ("github-gist", "github.com", "Googlebot",
     "https://github.com/gist/veigapunk/abc123", "disallow", "github_com.txt",
     [(360, "User-agent: *"), (370, "Disallow: /gist/")],
     "The gist subtree is disallowed for the * group and the URL is inside it."),
    ("github-raw-file", "github.com", "Googlebot",
     "https://github.com/veigapunk/kake-shokunin/raw/main/README.md", "disallow", "github_com.txt",
     [(360, "User-agent: *"), (378, "Disallow: /*/raw/")],
     "With * standing for owner/repository the rule matches the /raw/ path inside the repository."),
    ("github-features-page", "github.com", "Googlebot",
     "https://github.com/features", "allow", "github_com.txt",
     [(360, "User-agent: *")],
     "The * group holds 165 rule records (all anchored on path words such as /account-login, /search, "
     "/*/raw/ or /*?tab=*); none of them matches the single-segment path /features, so the product page is indexable."),
    ("github-repository-page", "github.com", "Googlebot",
     "https://github.com/veigapunk/kake-shokunin", "allow", "github_com.txt",
     [(360, "User-agent: *")],
     "A two-segment repository path matches none of the group's rules (the /*/*/ records all require a "
     "third segment such as commits/ or archive/), so repository pages are meant to be crawled."),
    ("github-achievements-tab", "github.com", "Googlebot",
     "https://github.com/veigapunk?tab=achievements&achievement=foo", "allow", "github_com.txt",
     [(361, "Allow: /*?tab=achievements&achievement=*"), (522, "Disallow: /*?tab=*")],
     "Both rules match the path plus query; the Allow value is longer (33 vs 8 octets), so it decides "
     "and the achievements tab the publisher singles out stays reachable."),

    # docs.github.com -- one record, no rule records at all.
    ("docs-pages-landing", "docs.github.com", "Googlebot",
     "https://docs.github.com/en/pages", "allow", "docs_github_com.txt",
     [(1, "User-agent: *")],
     "The 13-byte file holds a single user-agent record and no Allow or Disallow record, so no path is restricted."),
    ("docs-pages-configuring-source", "docs.github.com", "Googlebot",
     "https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site",
     "allow", "docs_github_com.txt",
     [(1, "User-agent: *")],
     "Same single-record file: the documented Pages page has no matching rule and is meant to be indexed."),
    ("docs-rest-pages", "docs.github.com", "Googlebot",
     "https://docs.github.com/en/rest/pages/pages", "allow", "docs_github_com.txt",
     [(1, "User-agent: *")],
     "The REST reference page has no matching rule in a file that declares none."),
    ("docs-robots-itself", "docs.github.com", "Googlebot",
     "https://docs.github.com/robots.txt", "allow", "docs_github_com.txt",
     [(1, "User-agent: *")],
     "No rule restricts it and /robots.txt is allowed whenever the served file decides."),

    # www.sitemaps.org -- a Sitemap record and no user-agent record at all.
    ("sitemaps-protocol", "www.sitemaps.org", "Googlebot",
     "https://www.sitemaps.org/protocol.html", "allow", "www_sitemaps_org.txt",
     [(1, "Sitemap: https://www.sitemaps.org/sitemap.xml")],
     "The file's only record is a Sitemap, which is ignored and does not open a group; with no group "
     "at all no rule applies and the protocol page is meant to be indexed."),
    ("sitemaps-sitemap-xml", "www.sitemaps.org", "Googlebot",
     "https://www.sitemaps.org/sitemap.xml", "allow", "www_sitemaps_org.txt",
     [(1, "Sitemap: https://www.sitemaps.org/sitemap.xml")],
     "No group exists and the publisher advertises the sitemap, so it is meant to be fetched."),
    ("sitemaps-protocol-fragment", "www.sitemaps.org", "Googlebot",
     "https://www.sitemaps.org/protocol.html#location", "allow", "www_sitemaps_org.txt",
     [(1, "Sitemap: https://www.sitemaps.org/sitemap.xml")],
     "The fragment is never part of the matched path and the file holds no rule, so the anchored section URL is allowed."),
    ("sitemaps-zh-protocol", "www.sitemaps.org", "Googlebot",
     "https://www.sitemaps.org/zh/protocol.html", "allow", "www_sitemaps_org.txt",
     [(1, "Sitemap: https://www.sitemaps.org/sitemap.xml")],
     "One translated protocol page; the file has no rule records, so it is allowed."),

    # developer.mozilla.org -- group "*" with a Sitemap record interleaved before its rules.
    ("mdn-api", "developer.mozilla.org", "Googlebot",
     "https://developer.mozilla.org/api/v1/search", "disallow", "developer_mozilla_org.txt",
     [(4, "Disallow: /api/")],
     "The API subtree is disallowed, and the Sitemap record above it does not end the group."),
    ("mdn-files-in-docs", "developer.mozilla.org", "Googlebot",
     "https://developer.mozilla.org/en-US/docs/files/example.png", "disallow", "developer_mozilla_org.txt",
     [(5, "Disallow: /*/files/")],
     "With * matching en-US/docs, the wildcard rule covers the /files/ subtree under any section."),
    ("mdn-media", "developer.mozilla.org", "Googlebot",
     "https://developer.mozilla.org/media/", "disallow", "developer_mozilla_org.txt",
     [(6, "Disallow: /media")],
     "The unanchored /media rule is a prefix rule, so the media directory is disallowed."),
    ("mdn-redirections-guide", "developer.mozilla.org", "Googlebot",
     "https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Redirections", "allow", "developer_mozilla_org.txt",
     [(4, "Disallow: /api/"), (5, "Disallow: /*/files/"), (6, "Disallow: /media")],
     "The guide path matches none of the three disallowed subtrees, so the documentation page is indexable."),
    ("mdn-locale-root", "developer.mozilla.org", "Googlebot",
     "https://developer.mozilla.org/en-US/", "allow", "developer_mozilla_org.txt",
     [(4, "Disallow: /api/"), (5, "Disallow: /*/files/"), (6, "Disallow: /media")],
     "The locale landing path contains no /files/ segment and is outside /api/ and /media."),

    # en.wikipedia.org -- leading BOM, group "*" from line 148, hundreds of rules.
    ("wiki-main-page", "en.wikipedia.org", "Googlebot",
     "https://en.wikipedia.org/wiki/Main_Page", "allow", "en_wikipedia_org.txt",
     [(148, "User-agent: *")],
     "No Googlebot group exists, so the * group decides; its /wiki/M… rules are MediaWiki:/Module: prefixes "
     "(lines 218-221, 700-701), none of which is a prefix of /wiki/Main_Page, so the main page is meant to be indexed."),
    ("wiki-special-search", "en.wikipedia.org", "Googlebot",
     "https://en.wikipedia.org/wiki/Special:Search", "disallow", "en_wikipedia_org.txt",
     [(156, "Disallow: /wiki/Special:")],
     "The Special: namespace is disallowed for every agent and the path starts with it."),
    ("wiki-articles-for-deletion", "en.wikipedia.org", "Googlebot",
     "https://en.wikipedia.org/wiki/Wikipedia:Articles_for_deletion/Example_article", "disallow", "en_wikipedia_org.txt",
     [(200, "Disallow: /wiki/Wikipedia:Articles_for_deletion/")],
     "The publisher hides deletion discussions from search results and the URL is inside that subtree."),
    ("wiki-loesungkandidaten", "en.wikipedia.org", "Googlebot",
     "https://en.wikipedia.org/wiki/Wikipedia:L%C3%B6schkandidaten/Beispiel", "disallow", "en_wikipedia_org.txt",
     [(171, "Disallow: /wiki/Wikipedia:Löschkandidaten/")],
     "The percent-encoded ö is preserved as an escape (not an unreserved character), so the path matches "
     "the disallowed German deletion-discussion subtree."),
    ("wiki-mobileview-api", "en.wikipedia.org", "Googlebot",
     "https://en.wikipedia.org/w/api.php?action=mobileview&page=Robots.txt", "allow", "en_wikipedia_org.txt",
     [(149, "Allow: /w/api.php?action=mobileview&"), (153, "Disallow: /w/")],
     "Both the Allow and the /w/ Disallow match; the Allow value is longer (29 vs 3 octets), so the "
     "documented mobileview exception remains reachable."),
    ("wiki-api-query", "en.wikipedia.org", "Googlebot",
     "https://en.wikipedia.org/w/api.php?action=query&titles=Robots.txt", "disallow", "en_wikipedia_org.txt",
     [(153, "Disallow: /w/")],
     "The /w/ tree is disallowed apart from the listed Allow exceptions, and a general query action is not one of them."),

    # www.robotstxt.org -- group "*" whose only rule has an empty value.
    ("robotstxt-home", "www.robotstxt.org", "Googlebot",
     "https://www.robotstxt.org/", "allow", "www_robotstxt_org.txt",
     [(2, "Disallow:")],
     "A rule with an empty value never matches, so the home page is allowed."),
    ("robotstxt-spec-page", "www.robotstxt.org", "Googlebot",
     "https://www.robotstxt.org/robotstxt.html", "allow", "www_robotstxt_org.txt",
     [(2, "Disallow:")],
     "The empty Disallow value restricts nothing, so the specification page stays crawlable."),
    ("robotstxt-orig", "www.robotstxt.org", "Googlebot",
     "https://www.robotstxt.org/orig.html", "allow", "www_robotstxt_org.txt",
     [(2, "Disallow:")],
     "Same empty rule; the 1994 proposal page is allowed."),
    ("robotstxt-monster", "www.robotstxt.org", "Googlebot",
     "https://www.robotstxt.org/monster/", "allow", "www_robotstxt_org.txt",
     [(2, "Disallow:")],
     "Empty value, no restriction; the directory is allowed."),

    # html.spec.whatwg.org -- two Disallow records.
    ("whatwg-multipage-syntax", "html.spec.whatwg.org", "Googlebot",
     "https://html.spec.whatwg.org/multipage/syntax.html", "allow", "html_spec_whatwg_org.txt",
     [(2, "Disallow: /commit-snapshots/"), (3, "Disallow: /review-drafts/")],
     "Only the two working-draft trees are disallowed; the multipage specification is meant to be indexed."),
    ("whatwg-multipage-links-fragment", "html.spec.whatwg.org", "Googlebot",
     "https://html.spec.whatwg.org/multipage/links.html#link-type-canonical", "allow", "html_spec_whatwg_org.txt",
     [(2, "Disallow: /commit-snapshots/"), (3, "Disallow: /review-drafts/")],
     "The fragment is not part of the matched path and neither rule covers /multipage/."),
    ("whatwg-commit-snapshots", "html.spec.whatwg.org", "Googlebot",
     "https://html.spec.whatwg.org/commit-snapshots/abc123/", "disallow", "html_spec_whatwg_org.txt",
     [(2, "Disallow: /commit-snapshots/")],
     "The immutable snapshot tree is disallowed and the URL is inside it."),
    ("whatwg-review-drafts", "html.spec.whatwg.org", "Googlebot",
     "https://html.spec.whatwg.org/review-drafts/2026-10/", "disallow", "html_spec_whatwg_org.txt",
     [(3, "Disallow: /review-drafts/")],
     "Review drafts are disallowed and the URL is inside that tree."),

    # pages.github.com -- a Sitemap record, no user-agent record.
    ("pages-github-home", "pages.github.com", "Googlebot",
     "https://pages.github.com/", "allow", "pages_github_com.txt",
     [(1, "Sitemap: https://pages.github.com/sitemap.xml")],
     "The only record is a Sitemap one, which opens no group; with no group, no rule applies and the landing page is crawlable."),
    ("pages-github-versions-json", "pages.github.com", "Googlebot",
     "https://pages.github.com/versions.json", "allow", "pages_github_com.txt",
     [(1, "Sitemap: https://pages.github.com/sitemap.xml")],
     "The build-catalog dataset has no governing rule, so it is meant to be fetched (S016 cites it)."),
    ("pages-github-versions", "pages.github.com", "Googlebot",
     "https://pages.github.com/versions/", "allow", "pages_github_com.txt",
     [(1, "Sitemap: https://pages.github.com/sitemap.xml")],
     "No rule records exist; the dependency page is allowed."),
    ("pages-github-robots", "pages.github.com", "Googlebot",
     "https://pages.github.com/robots.txt", "allow", "pages_github_com.txt",
     [(1, "Sitemap: https://pages.github.com/sitemap.xml")],
     "No rule restricts /robots.txt, and it is allowed whenever the served file decides."),

    # ds4cc.com (owned-site exception: read-only GET of /robots.txt only)
    ("ds4cc-home", "ds4cc.com", "Googlebot",
     "https://ds4cc.com/", "allow", "ds4cc_com.txt",
     [(2, "Allow: /")],
     "The single * group allows the whole root and carries no Disallow, so the home page is meant to be indexed."),
    ("ds4cc-robots", "ds4cc.com", "Googlebot",
     "https://ds4cc.com/robots.txt", "allow", "ds4cc_com.txt",
     [(2, "Allow: /")],
     "Allow: / covers the file itself, which is also always allowed when the served file decides."),
    ("ds4cc-index", "ds4cc.com", "Googlebot",
     "https://ds4cc.com/index.html", "allow", "ds4cc_com.txt",
     [(2, "Allow: /")],
     "The root Allow is a prefix rule covering every path on the host."),
    ("ds4cc-deep-note", "ds4cc.com", "Googlebot",
     "https://ds4cc.com/posts/2026/10/note.html", "allow", "ds4cc_com.txt",
     [(2, "Allow: /")],
     "Every path is allowed and the publisher advertises a sitemap, so article paths are meant to be crawled."),

    # veigapunk.github.io (owned-site exception)
    ("veiga-home", "veigapunk.github.io", "Googlebot",
     "https://veigapunk.github.io/", "allow", "veigapunk_github_io.txt",
     [(2, "Allow: /")],
     "One * group with Allow: / and no Disallow; the site root is open to crawlers."),
    ("veiga-robots", "veigapunk.github.io", "Googlebot",
     "https://veigapunk.github.io/robots.txt", "allow", "veigapunk_github_io.txt",
     [(2, "Allow: /")],
     "Allow: / covers the file itself."),
    ("veiga-index", "veigapunk.github.io", "Googlebot",
     "https://veigapunk.github.io/index.html", "allow", "veigapunk_github_io.txt",
     [(2, "Allow: /")],
     "The prefix rule covers every path on this Pages site."),
    ("veiga-deep-page", "veigapunk.github.io", "Googlebot",
     "https://veigapunk.github.io/kake/round-37.html", "allow", "veigapunk_github_io.txt",
     [(2, "Allow: /")],
     "No rule narrows the root Allow, so a nested page is meant to be crawled."),
]

checks = []
for cid, host, ua, url, expect, robots, quotes, why in CHECKS:
    assert "/" not in robots and robots.endswith(".txt"), robots
    assert robots in FILES, robots
    lines = FILES[robots]
    qs = []
    for ln, text in quotes:
        if ln < 1 or ln > len(lines):
            sys.exit(f"{cid}: line {ln} outside {robots} ({len(lines)} lines)")
        if lines[ln - 1] != text:
            sys.exit(f"{cid}: quote mismatch at {robots}:{ln}: {lines[ln-1]!r} != {text!r}")
        qs.append({"line": ln, "text": text})
    rec = receipts[f"https://{host}/robots.txt"]
    assert rec["status"] == 200, (host, rec["status"])
    checks.append({
        "id": cid,
        "robotsStatus": rec["status"],
        "userAgent": ua,
        "url": url,
        "expect": expect,
        "robots": robots,
        "evidence": {
            "sourceUrl": rec["url"],
            "finalUrl": rec["finalUrl"],
            "fetchedUtc": rec["timeUtc"],
            "bodySha256": rec["sha256"],
            "quotes": qs,
            "why": why,
        },
    })

ids = [c["id"] for c in checks]
assert len(ids) == len(set(ids)), "duplicate ids"
manifest = {"version": 1, "checks": checks}
strict = {"version": 1, "checks": [
    {k: c[k] for k in ("id", "robotsStatus", "userAgent", "url", "expect", "robots")}
    for c in checks
]}

with open(os.path.join(ROBOTS, "manifest.json"), "w", encoding="utf-8") as fh:
    json.dump(manifest, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
with open(os.path.join(ROBOTS, "manifest.strict.json"), "w", encoding="utf-8") as fh:
    json.dump(strict, fh, indent=2)
    fh.write("\n")

per_host = {}
for c in checks:
    host = [h for h in receipts if c["evidence"]["sourceUrl"] == h][0]
    per_host[host] = per_host.get(host, 0) + 1
print("checks:", len(checks))
for h in sorted(per_host):
    print(f"  {h}: {per_host[h]}")
print("expect allow:", sum(1 for c in checks if c["expect"] == "allow"),
      "disallow:", sum(1 for c in checks if c["expect"] == "disallow"))
