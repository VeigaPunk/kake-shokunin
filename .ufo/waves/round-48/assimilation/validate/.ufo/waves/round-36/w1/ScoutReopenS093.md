# ScoutReopenS093 — Wikipedia "HTTP 301" re-opened live and judged

**Verdict: REJECT** (tier C, tertiary). Every normative sentence it carries is already in S088
(RFC 9110) or superseded by it, and the one thing it adds, practitioner recipes, contains a
permanent redirect to `http://` and a temporary redirect to `https://`.

## Fetches (all artifacts in /fast/scratch/hyaku/kake-r36w1/ScoutReopenS093/)

| # | command (exit) | observed |
|---|---|---|
| 1 | `curl -sS … https://en.wikipedia.org/wiki/HTTP_301` (0) | 200, 102076 B, `text/html; charset=UTF-8`, 2026-10-23T01:34:49Z, sha256 `877c4dab…a06ba` |
| 2 | `curl -sS … /w/index.php?title=HTTP_301&action=raw` (0) | 200, 3808 B, `text/x-wiki`, sha256 `fca820a…19d17` (`wiki_raw.bin`, line refs below) |
| 3 | `api.php?prop=revisions&titles=HTTP_301` (0) | newest rev **1345198988, 2026-03-24T21:20:06Z**; 2026-03-23 rev 1344965197 by temp IP `~2026-18180-41`; 2025-12-26 rev was **146 B** |
| 4 | same API, `rvdir=newer&rvlimit=1` (0) | oldest rev 135255193, 2007-06-02, **39 B, comment "redirect"** |
| 5 | text diff vs `.ufo/waves/round-36/sources/S093.txt` (python, 0) | `ratio 1.0000`, 0 differing tokens; my body sha = receipt `bodySha256 877c4dab…` → unchanged since the round's 01:09:00Z fetch |
| 6 | Bing ref `…/webmaster/help/how-to-use-the-site-move-tool-bb8f5112` (0) | 1 redirect → `/webmasters/help/…`, **HTTP 404**, `application/json`, 0 B — Bing citation is dead |
| 7 | Google ref `support.google.com/webmasters/bin/answer.py?…93633` (0) | 3 redirects → `developers.google.com/search/docs/crawling-indexing/301-redirects`, 200, "Last updated 2026-04-14 UTC", sha256 `a955304…581c` |
| 8 | `https://httpd.apache.org/docs/2.4/rewrite/flags.html` (0) | 200; "[R=code] Redirect External redirect (default 302)"; "a 302 status code being used by default if none is specified" |

Body is **7 months old, one editing pass**: an article only since 2026-03-23/24 (3807→3808 B); before
that a 146 B stub, and in 2007 a 39 B redirect.

## What it says that RFC 9110 does not — and whether it earns a row

1. **Recipes** (`.htaccess`, nginx, PHP, Express, static HTML): no spec adjudicates them, and they are
   broken (D3, D4), so they cannot fill a `teaches` cell.
2. **Search-engine recommendation** (raw:76): the only claim outside RFC scope; half dead (D5).

## Defects (wikitext line numbers in `wiki_raw.bin`)

- **D1 — normative basis is an obsolete RFC.** raw:6 "`RFC]] 2616 … states that:`". S088 records the
  chain: "revised in 1999 [RFC2616], and revised again in 2014 ([RFC7230] through [RFC7235])"
  (S088.txt byte 14117), header `Obsoletes: … 7230, 7231 …`. The article quotes neither 7231 nor 9110.
- **D2 — the quoted rule is contradicted by current text.** raw:10: "If the 301 status code is received
  in response to a request of any type other than GET or HEAD, the client must ask the user before
  redirecting." RFC 9110 §15.4: "status codes 301 and 302 have been adjusted to allow a POST request to
  be redirected as GET" (S088.txt byte 316044); §15.4.2: "a user agent MAY change the request method
  from POST to GET … If this behavior is undesired, the 308 (Permanent Redirect) status code can be used
  instead" (byte 321681). raw:4's "should be updated" also drops §15.4.2's qualifier that the
  replacement suggestion "is usually ignored unless the user agent is actively editing references".
- **D3 — the .htaccess example emits a permanent redirect to http.** Caption raw:32 promises "redirect a
  non-secure URL to a secure address without the leading www"; under `RewriteCond %{HTTPS} off`
  (raw:34) the rule is raw:36 `RewriteRule ^(.*)$ http://%1/$1 [R=301,L]` — scheme stays `http`. The only
  rule reaching `https` is raw:44 `RewriteRule ^(.*)$ https://example.com/$1 [R,L]`, and bare `[R]` is
  **302** per fetch 8. Net: a year-cacheable 301 onto the non-secure origin, then a temporary hop.
- **D4 — "Static HTML" is not a 301.** raw:50 `<meta http-equiv="refresh" content="0; url=/" />` carries
  no status line. Google's current doc lists it as a separate type beside "HTTP 301 (moved permanently)
  … HTTP 308 (moved permanently) … meta refresh (0 seconds)", not as a 301.
- **D5 — the search-engine sentence is uncited in practice.** raw:76 "Both Bing and Google recommend
  using a 301 redirect…": the Bing ref 404s (fetch 6); the Google ref resolves but the live doc says "The
  301 and 308 status codes mean that a page has permanently moved to a new location" and does not prefer
  301; neither ref carries an access-date and neither is quoted.
- **D6 — 308 is absent.** `grep -c 308 wiki_raw.bin` = **0** (`9110` = 0, `2616` = 3). The one
  operational fact for non-GET redirects — 301 may rewrite POST to GET, 308 may not (§15.4.2 above; MDN
  S094: "301 … Others may or may not be changed to GET" vs "308 … Method and body not changed") — is
  missing, so the article teaches strictly less than rows already in the registry. raw:4's
  "best practice for upgrading … to HTTPS" is likewise uncited and never mentions HSTS.

## Recommendation

Reject, with this located reason: the normative content is RFC 2616, superseded and in one point
contradicted by S088 (§15.4, §15.4.2) which the same wave is adopting; it omits 308, carried by S088
§15.4.2/§15.4.9 and S094; its non-redundant half (recipes) is wrong on its own stated goal; its only
surviving search-engine citation is unquoted and undated and its Bing citation 404s.
**Flip:** a revision replaces raw:6-10 with RFC 9110 §15.4.2, adds the 301-vs-308 distinction, fixes
raw:36/raw:44, and re-cites a live first-party crawler page with a quote — or a kake entry needs a
module-level recipe (`Redirect 301`, nginx `return 301`) that no opened primary supplies.

**Adjacent finding for L1 (not mine to admit):** `developers.google.com/search/docs/crawling-indexing/301-redirects`
is live, dated 2026-04-14, and states 301/308 equivalence plus Google's meta-refresh ordering — a better
freshness pin for redirect semantics than S093. Bing's cited help path is dead as of this fetch.

## Not verified

Google's and Bing's wording at the time the Wikipedia sentence was written (only today's 302/404/200
states observed); Apache `[R]` default read from httpd 2.4 docs, not executed; no browser run for the
meta-refresh example; no requests to ds4cc/onrender/kimi hosts.
