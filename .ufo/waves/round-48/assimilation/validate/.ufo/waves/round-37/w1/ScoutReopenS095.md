# ScoutReopenS095 — independent live re-open of S095 (Google robots.txt specification)

Seat KakeR37.ScoutReopenS095 (leaf). Target page: https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt
Sandbox: `/fast/scratch/hyaku/kake-r37w1/ScoutReopenS095/`. I did not touch `/fast/scratch/hyaku/kake-r37/`, did not run the C1 counter, installed nothing.

## Access (observed)
- 2026-10-23T03:23:00Z–03:23:02Z UTC, one ordinary GET:
  `curl -sS -L --max-time 60 -o live_body.html -D hdrs.txt -w 'status=%{http_code} final=%{url_effective} bytes=%{size_download} redirects=%{num_redirects}' '<url>'` → exit 0, `status=200 final=https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec bytes=99418 redirects=1`
- Hop 1 `HTTP/2 301 location: /crawling/docs/robots-txt/robots-txt-spec`; hop 2 `HTTP/2 200`, `last-modified: Mon, 31 Aug 2026 14:57:06 GMT`, `content-length: 99418`, canonical link = the final URL, page footer "Last updated 2026-08-31 UTC".
- The page has NOT moved since retention: `receipts.json` S095 `finalUrl` is the same string, `status` 200, and the /search/docs path still 301s. Its own last update (2026-08-31) predates the round.

## Same page? (observed, byte level)
- Bodies differ from the retained `S095.html.gz` (gunzipped sha `c8c1f204…c4e3`, 99414 B) vs live `55efdb56…bf72` (99418 B); first differing byte 88500, inside a `<script type="application/json" tag-management>` GA/GTM block (JSON key order). Script-only.
- Extracted with the lane fetcher's exact rule (`fetch_sources.py::visible_text`, fetcher sha `3677e42f…0f08`): live text sha `a90948534ca17e54196115163fb9a5f6afbb0b347f97a44b01a3a1d636ddbbc6`, 3030 words = the retained `S095.txt` sha and the receipts `textSha256`. **Retained text is byte-identical to today's page.**
- Verdict: same page, same final URL, no content change; the retention is fresh as of 03:23Z.

## Quotes that bear on the C1 contract (verbatim, section named)
30 quotes asserted as exact substrings of the live text at build time, offsets in `quotes.json` (the lane text rule leaves a space where a tag was, e.g. "except 429 ,"; words unchanged). Load-bearing ones:
- SUPPORT (b) size: "Google enforces a robots.txt file size limit of 500 kibibytes (KiB). Content which is after the maximum file size is ignored." [File format] → 500 KiB = 512000 bytes, truncate; the contract's exact limit is grounded.
- SUPPORT (b): "The robots.txt file must be a UTF-8 encoded plain text file and the lines must be separated by CR" [File format]; "Keep in mind that everything after the # character will be ignored." and "A valid robots.txt line consists of a field, a colon, and a value." [Syntax].
- SUPPORT (b) other keys do not end a group: "This means that the following robots.txt snippet is treated as one group" [Grouping of lines and rules] (sitemap between two user-agent lines).
- SUPPORT (c): "You can group together rules that apply to multiple user agents by repeating user-agent lines for each crawler."; "all the rules from the groups applicable to the specific user agent are combined"; "Storebot-Google follows group 2, because there is no specific Storebot-Google group"; "The order of the groups within the robots.txt file is irrelevant." [Order of precedence for user agents].
- SUPPORT (d): "When no path is specified, the rule is ignored." [Syntax/allow]; "By default, there are no restrictions for crawling for the designated crawlers."; "* designates 0 or more instances of any valid character."; "$ designates the end of the URL."; "Note that the matching is case-sensitive." [URL matching based on path values].
- SUPPORT (d) precedence: "crawlers use the most specific rule based on the length of the rule path"; "In case of conflicting rules, including those with wildcards, Google uses the least restrictive rule." [Order of precedence for rules].
- SUPPORT (e) encoding: "Google's crawlers compare rules against URLs using their percent-encoded forms, and automatically canonicalize raw UTF-8 rule paths into percent-encoded forms." [URL matching based on path values].

## Contradictions with contract sentences (each names the sentence it hits)
1. (a) "400–499 (\"unavailable\"): allowed, whatever any file says" vs [4xx] "Google's crawlers treat all 4xx errors, except 429". 429 is Google's exception. Contract follows RFC 9309 §2.3.1.3 (S011 confirmed: no "429" in its text), so the contract silently resolves a Google-vs-RFC difference.
2. (a) "500–599 (\"unreachable\"): disallowed, whatever any file says" vs [5xx] "If there's no cached version available, Google assumes there's no crawl restrictions." plus "For the first 12 hours, Google stops crawling the site but keeps trying to fetch the robots.txt file." A fresh 5xx with no cache is an ALLOW for Google. RFC §2.3.1.4 has MUST complete-disallow then a MAY downgrade after ~30 days; the contract freezes the first step only and does not say so.
3. (c) "matches a group when it equals one of the group's names compared ASCII case-insensitively" vs [Order of precedence for user agents] "Google's crawlers determine the correct group of rules by finding in the robots.txt file the group with the most specific user agent" and [Matching of user-agent fields] "both googlebot/1.2 and googlebot* are equivalent to googlebot". Exact equality vs most-specific selection with decorated names. Repro: file `user-agent: googlebot*` + `disallow: /x`, check userAgent `googlebot`, url `/x` → contract falls to `*` (allow), Google disallows. This is the "substring user-agent match" edge MutRefPass already lists as a survivor, i.e. untested by the sealed cases.
4. (e) "The path to match is the URL's path … followed by `?` and the query when the query is non-empty" vs [URL matching based on path values] "This works by comparing the rule to the path component of the URL that the crawler is trying to fetch." S095 excludes the query in as many words; the contract includes it (RFC's "URI" reading; S011 contains no "query" string, §2.2.2 says "match the paths … against the URI"). Repro: url `/fish?x`, rule `disallow: /fish?`.
5. (a)/(e) decision ignores the file's origin vs [File location and range of validity] "The rules listed in the robots.txt file apply only to the host, protocol, and port number where the robots.txt file is hosted." The manifest carries no robots-file origin, so the tool decides a check URL on another host/protocol/port from a local file Google says cannot apply there. No contract sentence forbids it; the scope is simply absent.
6. (e) "The path `/robots.txt` is always allowed" has NO S095 sentence: the text's only "always" is about the `rule: [path]` form. That rule is RFC 9309 §2.2.2 ("The /robots.txt URI is implicitly allowed"), so any case testing it is S011-grounded only.

## Tensions / divergences (a S095-only reader would decide differently; not direct contradictions)
- (b) BOM: contract "a leading UTF-8 byte order mark (EF BB BF) is dropped" vs [File format] "Google ignores invalid lines in robots.txt files, including the Unicode Byte Order Mark (BOM) at the beginning". S095 files the BOM under ignored *lines* (readable as dropping the whole first line); the contract keeps the rest of that line. S011 never says "BOM" (0 hits), so S095 is the only source naming it.
- (b) trim: S095 [Syntax] names space only — "Space at the beginning and at the end of the line is ignored." — the contract trims spaces and tabs.
- (b) invalid UTF-8: contract → U+FFFD; S095 "Google may ignore characters that are not part of the UTF-8 range" (ignore ≠ replace; a MAY).
- (b) HTML body: S095 says if the content is HTML "Google will try to parse the content and extract rules"; the contract has no HTML fallback.
- (d) tie-break metric: contract counts normalized octets incl. `*`/`$`; S095's gloss is "the rule path is longer and it matches more characters in the URL" (consumed characters). The readings can differ for wildcard rules (`allow: /ab*` vs `disallow: /abc` on `/abc`); the contract follows RFC's "most octets".
- (a) 3xx: Google follows five hops, "then stops and treats it as a 404"; the contract makes every 3xx a `check_invalid` fault. Out of scope offline, but a manifest recording a real 301 is invalid, so the publisher must record the post-redirect status — the contract does not say so.

## Bearing on C1 (advisory, no verdict)
- (c) equality and (e) query are the exposed sentences: both are RFC readings S095 contradicts explicitly, and both are edges the mutation pass already found untested. The declaration's "Sourced" line names S011 first and S095 as opened "as well", so nothing here contradicts the sourcing claim; but a later verifier who reads S095 before RFC 9309 will read (a) 429, (a) no-cache 5xx, (c) most-specific, (e) path-component and (e)/robots.txt as tool errors. Suggest the contract add a "lane reading, not S095" note at (a), (c) and (e), and have the sealed cases pin the RFC readings it already freezes (429 → allow, 5xx → disallow, `?query` in the match).

## Evidence (absolute paths in sandbox) and limits
- `live_body.html` `55efdb5630…bf72`; `live_text.txt` `a90948534c…bbc6`; `retained_body.html` `c8c1f20415…c4e3`; `quotes.json` `55114f8ccc…4b59` (33 entries, 30 verbatim, 3 silent bullets); `hdrs.txt` `f3d9837ff0…35c5`.
- Not verified: no C1 counter run (no key), no sealed-case read; one GET, no second network or archive copy (freshness rests on `last-modified` + identical text); no check of whether Google's live crawler actually behaves as its page says (the page is a document, not a test).
