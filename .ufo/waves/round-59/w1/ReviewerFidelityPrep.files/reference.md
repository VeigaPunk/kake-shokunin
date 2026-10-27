# ReviewerFidelityPrep — C3 page reference (S425, S426)

Seat: `ReviewerFidelityPrep` (leaf, read-only). Scope: a sentence-by-sentence yardstick for the two
round-59 C3 retained bodies, so residual reviewers can check *faithfulness* (not just quote truth).

Sources (read-only, lane `kake-shokunin`):
- `.ufo/waves/round-59/sources/S425.html` — 74477 bytes, sha256 `ff2b9fd7ed074536a460dca57816bffecceb0c186c42f1d551f34918551f5caa`, HTTP 200, fetched 2026-10-27T01:21:22Z
- `.ufo/waves/round-59/sources/S426.html` — 69789 bytes, sha256 `8df9d4ade1d1f335060af05229c4d90b15d8136b9807cfab17a088f3292f0879`, HTTP 200, fetched 2026-10-27T01:21:22Z
- Article block = `class="devsite-article-body` .. `<devsite-content-footer` (S425 window chars 25627..38178; S426 25626..33523).
- 157 / 90 non-empty text nodes in the two blocks (the counter's `text_segments` returns 217 / 165 entries; the rest are
  empty strings between tags). Both blocks are **entirely ASCII** (measured: zero characters above U+007F), so no
  curly quote or em dash appears in any quotable string.
- Every "verbatim" string below was extracted mechanically from the retained body (whitespace-collapsed), not retyped.
- Quote rule used throughout (contract §C5): a quote is 6..25 whitespace units, ≤160 chars, a raw substring of **one**
  text node of the article block, page-unique across S425+S426, ASCII `"` only. `span_tools.py check <S> "<span>"` confirms.

**Qualifier legend** — every modal/hedge/limit marker carried by the sentence is listed; reviewers should treat a
dropped qualifier as a fidelity defect.

---

## S425 — `Overview of Google crawlers and fetchers (user agents)`

Two scopes only, as assigned: (a) the IP-address paragraph; (b) the `Verify Google's crawlers and fetchers` section.
The page's other sections (taxonomy table, transfer protocols, content encodings, file-size limits, crawl rate,
HTTP caching) are **out of scope for this reference** and are listed in §"S425 out of scope" at the end.

### (a) IP-address paragraph — one `<p>` under `## Technical properties of Google's crawlers and fetchers`
Whole paragraph = article text node 45; every sentence below is quotable whole.

1. **"Google's crawlers and fetchers are designed to be run simultaneously by thousands of machines to improve performance and scale as the web grows."**
   - Paraphrase: Google's clients are built to run concurrently on thousands of machines, to improve performance and to keep up as the web grows.
   - Qualifiers: none modal. "thousands" = indefinite magnitude; "designed to be" = design intent, not an observation.
   - Quoteable whole: 23 units / 144 chars / page-unique.
2. **"To optimize bandwidth usage, these clients are distributed across many datacenters across the world so they're located near the sites that they might access."**
   - Paraphrase: to save bandwidth the clients are spread across many datacenters worldwide, which puts them near the sites they might fetch.
   - Qualifiers: "To optimize bandwidth usage" = stated purpose, not the only purpose; "many" = indefinite; "might access" = modal (candidate sites, not actual ones); "so" = causal.
   - Quoteable whole: 24 units / 157 chars / page-unique.
3. **"Therefore, your logs may show visits from several IP addresses."**
   - Paraphrase: consequently, a site's log can show the crawler arriving from more than one address.
   - Qualifiers: **"may"** (possibility — a log need not show several); **"several"** (unspecified count, more than one, not "many"); "your logs" = the site operator's log.
   - Quoteable whole: 10 units / 63 chars / page-unique. **This is the sentence the stale lane claim is corrected against.**
4. **"Google egresses primarily from IP addresses in the United States."**
   - Paraphrase: most of Google's outbound traffic comes from US addresses.
   - Qualifiers: **"primarily"** (majority, not all); "egresses" = outbound only.
   - Quoteable whole: 10 units / 65 chars / page-unique.
5. **"In case Google detects that a site is blocking requests from the United States, it may attempt to crawl from IP addresses located in other countries."**
   - Paraphrase: if Google notices a site blocking US-sourced requests, it may try crawling from addresses in other countries.
   - Qualifiers: "In case" = conditional trigger, and it is **Google's own detection**, not the operator's report; **"may attempt"** (double hedge: possibility + tentative attempt); "other countries" = **no country is named**.
   - Quoteable whole as a sentence: 26 units → **over the 25-unit ceiling**; quotable fragments measured page-unique:
     `"In case Google detects that a site is blocking requests from the United States, it may attempt to crawl from IP addresses located in other"` (25u / 138c),
     `"case Google detects that a site is blocking requests from the United States, it may attempt to crawl from IP addresses located in other countries."` (25u / 146c),
     `"it may attempt to crawl from IP addresses located in other countries."` (12u / 69c),
     `"case Google detects that a site is blocking requests from the United States"` (13u / 75c).

### (b) `## Verify Google's crawlers and fetchers` — the block's last h2
Reading order is h2 (node 192) → p (194) → `<ol>` items 197/198/199, 201, 203 → p (206/207/208).

6. **"Google's crawlers identify themselves in three ways:"**
   - Paraphrase: Google says its crawlers present themselves in three identifiable ways.
   - Qualifiers: **"three"** = an explicit count, and the list that follows has exactly three items; the verb is **"identify themselves"** — self-presentation, *not* proof of authenticity; the page supplies no tie-break rule when the three disagree.
   - Quoteable whole: 7 units / 52 chars / page-unique.
7. **"The HTTP user-agent request header."** (list item 1)
   - Paraphrase: the HTTP `user-agent` request header.
   - Qualifiers: none.
   - **Split by inline markup** into text nodes 197 `The HTTP`, 198 `user-agent` (a `<code>` token), 199 `request header.` → the sentence is **not** a raw substring of any one node and **cannot be quoted**; it must be named, not quoted. Each fragment is 2/1/2 units — all under the 6-unit floor.
8. **"The source IP address of the request."** (list item 2)
   - Paraphrase: the request's source IP address.
   - Qualifiers: none. The page says nothing about the address being stable, geolocated, or unique per crawler.
   - Quoteable whole: 7 units / 37 chars / page-unique. **Carries the S425 page-named subject `IP address`.**
9. **"The reverse DNS hostname of the source IP."** (list item 3)
   - Paraphrase: the reverse-DNS name of that source address.
   - Qualifiers: none. **This is a derived value, not a logged field** (see the S426 step-1/step-3 procedure): the log holds the IP; the hostname comes from a lookup.
   - Quoteable whole: 8 units / 42 chars / page-unique.
10. **"Learn how to use these details to verify Google's crawlers and fetchers."**
    - Paraphrase: the page points to a separate page explaining how to use those three details to verify Google's crawlers.
    - Qualifiers: **the method is not on this page** — S425 states only that the details are usable for verification. "these details" = the three ways in item 6.
    - **Split** into nodes 206 `Learn how to use these details to`, 207 `verify Google's crawlers and fetchers` (link text), 208 `.` → not quotable as one sentence. `"Learn how to use these details to"` (7 units) and `"verify Google's crawlers and fetchers"` (5 units, **under the floor**) are the node fragments; only the first is above 6 units.

### S425 fidelity notes (what a faithful entry may and may not say)
- The page says crawlers identify themselves **in three ways** — user-agent header, source IP address, reverse DNS hostname of that IP. It does **not** say a log records three fields: the reverse-DNS hostname is *computed* from the logged IP by a lookup (S426 step 1 and step 3 show the operator running the lookups). An entry that says "a log records three signals" adds to the page; the honest form is "the crawler's request carries a user-agent header, the log records its source IP, and the IP can be reverse-resolved to a hostname".
- The lane's stale line ("A user-agent string is the only thing a server log records about the crawler.") is contradicted by items 8 and 9 **and** by sentence 3 above ("your logs may show visits from several IP addresses"). The page does not itself state that the log records the reverse-DNS hostname.
- Sentence 3's **"may"** must survive: the page says a log *may* show several addresses, not that it *will*.
- Sentence 4's **"primarily"** must survive: US egress is the majority, not the whole.
- Sentence 5's **"may attempt"** must survive, and no country may be named.
- The page says nothing about how many addresses a crawler uses, no per-country share, no rotation policy, and no
  decision rule for the three signals — those are omissions, not claims.
- The printed revision `Last updated 2026-06-12 UTC.` exists as a text node of the body but sits **outside** the
  article window (char 38715 > 38178) → it is quotable only via the C5 "any text node of the body" test, never as
  an in-block quote.
- The h2 string `Verify Google's crawlers and fetchers` occurs twice in the raw body (h2 text + its `data-text`
  attribute); as a text node it occurs once.

### S425 out of scope for this reference (not in the assigned sentence list)
Taxonomy table (common / special-case / user-triggered, AdsBot's `*` exception, Google Site Verifier); transfer
protocols (HTTP/1.1 default, HTTP/2, the 421 opt-out, FTP/FTPS); content encodings (gzip, deflate, Brotli,
`Accept-Encoding`); file-size limits (15 MB default, 2 MB example); crawl rate and host load; HTTP caching
(`ETag`, `If-None-Match`, `Last-Modified`, `If-Modified-Since`, `max-age`).

---

## S426 — `Verify requests from Google crawlers and fetchers`

Whole article block, reading order. Node indices are the article block's text nodes.

### Page identity
- h1 (node 1): **"Verify requests from Google crawlers and fetchers"** — sentence case.
- `<title>`: `Verify Requests from Google Crawlers and Fetchers` — title case, before the ` | ` site suffix. The two differ in case; the row's title cell must carry the `<title>` form.
- h2s (nodes 88, 134): `Use command line tools`, `Use automatic solutions`. **The h1 is not usable as a row anchor** —
  the counter's anchor-heading test collects only `<h2>`/`<h3>` of the article block.
- Printed revision `Last updated 2026-03-20 UTC.` is a body text node but sits **outside** the article window (char 34060 > 33523) → not quotable in-block.

### Opening paragraph (nodes 3, 4, 5)
1. **"You can verify if a request to your server really is from Google."**
   - Paraphrase: the page says you can confirm that a request hitting your server really came from Google.
   - Qualifiers: "can verify" = capability claim, not a guarantee; **"really"** is colloquial emphasis with no defined test; the claim is about *Google* generally, not about Googlebot specifically.
   - **Split** (nodes 3 + 4 `from Google` link): not quotable whole; `"You can verify if a request to your server really is"` (11 units) is the quotable fragment.
2. **"Verification is possible for crawlers such as Googlebot, as well as other requests."**
   - Paraphrase: verification works for Googlebot-class crawlers and also for other kinds of request.
   - Qualifiers: **"such as"** (example, not exhaustive); **"as well as other requests"** (verification is *not* limited to crawlers); "is possible" not "is guaranteed".
   - Quoteable whole: 13 units / 83 chars / page-unique.
3. **"This is useful if you're concerned that spammers or other troublemakers are accessing your site while claiming to be from Google."**
   - Paraphrase: the procedure serves operators who suspect impostors are hitting the site under a Google claim.
   - Qualifiers: **"if you're concerned"** (conditional utility); "spammers or other troublemakers" (two named groups); **"while claiming to be from Google"** — the page does not say *which* field carries the claim, never mentions the user-agent string in this context, and never uses "spoofed"/"forged". Reading it as a user-agent-forgery claim adds to the page.
   - Quoteable whole: 21 units / 129 chars / page-unique.

### The three-category table (nodes 7–71)
4. **"Google's crawlers and fetchers fall into three categories:"**
   - Paraphrase: Google's agents are sorted into three categories.
   - Qualifiers: **"three"** = explicit count, and the table has exactly three body rows. Note the table has **four columns** (Type, Description, Reverse DNS mask, IP ranges) — three categories, four columns.
   - Quoteable whole: 8 units / 58 chars / page-unique.
5. Column headers (nodes 11/13/15/17): `Type`, `Description`, `Reverse DNS mask`, `IP ranges`. **"Reverse DNS mask" is capitalised and is 3 units** → it does **not** carry the S426 page-named subject `reverse DNS` (the topic test is case-sensitive) and is below the 6-unit floor.

Row 1 — **Common crawlers** (Type, node 21):
6. **"The common crawlers used for Google's products (such as Googlebot)."**
   - Paraphrase: the crawlers Google uses for its products, Googlebot being one.
   - Qualifiers: "such as" (example, non-exhaustive); "common" is the category's own contrast term.
   - Quoteable whole: 10 units / 67 chars / page-unique.
7. **"They always respect robots.txt rules for automatic crawls."**
   - Paraphrase: they always honour robots.txt on automatic crawls.
   - Qualifiers: **"always"** (absolute) **but scoped to "for automatic crawls"** — the scope qualifier must travel with it.
   - **Not page-unique on its own**: the same sentence occurs in S425 (node 21) → it fails the uniqueness test as a
     standalone quote. The two-sentence combination `"The common crawlers used for Google's products (such as Googlebot). They always respect robots.txt rules for automatic crawls."` (18 units / 126 chars) **is** page-unique and quotable whole.
   - Masks (nodes 26/28): `crawl-***-***-***-***.googlebot.com` or `geo-crawl-***-***-***-***.geo.googlebot.com`; IP ranges (node 31): `common-crawlers.json`. All are single tokens — named in backticks, not quoted.

Row 2 — **Special-case crawlers** (Type, node 35):
8. **"Crawlers or fetchers that perform specific functions for Google products (such as AdsBot) where there's an agreement between the crawled site and the product about the access or for abuse-specific crawling or fetching."**
   - Paraphrase: agents doing a specific job for a Google product, either under a standing agreement with the site about access, or for abuse-specific crawling/fetching.
   - Qualifiers: "such as" (AdsBot as example); the defining condition is **"where there's an agreement … or for abuse-specific crawling or fetching"** — two alternative grounds joined by "or".
   - 33 units → **over the ceiling**. The cell is one text node (node 37), so sub-spans of it are quotable;
     measured page-unique and within the ceilings: `"Crawlers or fetchers that perform specific functions for Google products (such as AdsBot) where there's an agreement"` (17u / 116c) and
     `"an agreement between the crawled site and the product about the access or for abuse-specific crawling or fetching."` (18u / 114c).
     (Longer prefixes of the same node — 24u, 27u, 29u — are page-unique but exceed the 25-unit ceiling.)
9. **"These crawlers or fetchers may or may not respect robots.txt rules."**
   - Paraphrase: for this category robots.txt compliance is not guaranteed either way.
   - Qualifiers: **"may or may not"** — an explicit two-sided non-commitment, the strongest hedge on the page; it must not be flattened to "respects" or "ignores".
   - Quoteable whole: 11 units / 67 chars / page-unique.
   - Mask (node 39): `rate-limited-proxy-***-***-***-***.google.com`; ranges (node 41): `special-crawlers.json`.

Row 3 — **User-triggered fetchers** (Type, node 45):
10. **"Tools and product functions where the end user triggers a fetch."**
    - Paraphrase: tooling and product features in which a person triggers the fetch.
    - Qualifiers: "where the end user triggers a fetch" = the defining condition.
    - Quoteable whole: 11 units / 64 chars / page-unique.
11. **"For example, Google Site Verifier acts on the request of a user."**
    - Paraphrase: Google Site Verifier is one such case, acting on a user's request.
    - Qualifiers: **"For example"** (illustrative, non-exhaustive). **Split** by the `Google Site Verifier` link (node 48) into `For example,` (2 units) / `Google Site Verifier` (3 units) / `acts on the request of a user.` (7 units) → not quotable whole; the last fragment is quotable but **not page-unique on its own** (it also occurs in S425, node 39).
12. **"Because the fetch was requested by a user, these fetchers ignore robots.txt rules."**
    - Paraphrase: user-triggered fetches ignore robots.txt because a human asked for them.
    - Qualifiers: **"Because"** = explicit causal clause (the ignore is conditional on user request); "ignore" is flat and unqualified here — deliberately unlike row 2's hedge.
    - Quoteable whole: 13 units / 82 chars / page-unique.
13. **"Fetchers controlled by Google originate from IPs in the user-triggered-fetchers-google.json object and resolve to a google.com hostname."**
    - Paraphrase: Google's own fetchers come from the addresses listed in `user-triggered-fetchers-google.json` and reverse-resolve to a `google.com` name.
    - Qualifiers: **"controlled by Google"** (distinguishes this list from the next one); "originate from" and "resolve to" are two separate properties.
    - **Split** across 5 nodes (50/51/52/53/54) by the `<code>` tokens → not quotable whole. `"Fetchers controlled by Google originate from IPs in the"` (9 units / 55 chars) is the quotable leading fragment.
14. **"IPs in the user-triggered-fetchers.json object resolve to gae.googleusercontent.com hostnames."**
    - Paraphrase: the addresses in `user-triggered-fetchers.json` reverse-resolve to `gae.googleusercontent.com` names.
    - Qualifiers: none beyond the file-name specificity.
    - **Split** across 5 nodes (54/55/56/57/58) → not quotable whole; `"object resolve to"` is 3 units, `"hostnames. These IPs are used, for example,"` (7 units / 43 chars) is the quotable continuation.
15. **"These IPs are used, for example, if a site running on Google Cloud (GCP) has a feature that requires fetching external RSS feeds on the request of the user of that site."**
    - Paraphrase: those addresses serve, for instance, a Google-Cloud site whose feature fetches external RSS on its own user's behalf.
    - Qualifiers: **"for example"** (one illustrative use, not the full purpose); "on the request of the user of that site" (the end user is the *site's* user, not the site's operator).
    - 32 units / 169 chars → over both ceilings; quotable as `"These IPs are used, for example, if a site running on Google Cloud (GCP) has a feature"` (16 units) or the shorter `"These IPs are used, for example,"` (7 units).
    - Masks (nodes 61/63): `***-***-***-***.gae.googleusercontent.com` or `google-proxy-***-***-***-***.google.com`; ranges (nodes 67/69/71): `user-triggered-fetchers.json`, `user-triggered-fetchers-google.json`, and `user-triggered-agents.json`.

### Two methods (nodes 76–85)
16. **"There are two methods for verifying requests from Google:"**
    - Paraphrase: the page offers two routes to verifying a request as Google's.
    - Qualifiers: **"two"** = explicit count, exactly two are listed.
    - Quoteable whole: 9 units / 57 chars / page-unique.
17. **"Manually: For one-off lookups, use command line tools."**
    - Paraphrase: the manual route is command-line tooling for isolated lookups.
    - Qualifiers: **"For one-off lookups"** (individual, occasional lookups only — the route is not for bulk). `Manually` is a link label on its own text node (80), so the sentence is split into `Manually:` and the rest.
    - **Split** (nodes 80 + 81) → not quotable whole; `"For one-off lookups, use command line tools."` (7 units) is the quotable fragment, and the label must be named in backticks.
18. **"This method is sufficient for most use cases."**
    - Paraphrase: the manual route covers most cases.
    - Qualifiers: **"for most use cases"** — an explicit, deliberate hedge that the manual route does *not* cover everything (this is what motivates the automatic route). Dropping "for most" overstates the page.
    - Quoteable whole: 8 units / 45 chars / page-unique.
19. **"Automatically: For large scale lookups, use an automatic solution to match a crawler's IP address against the list of published Google IP addresses."**
    - Paraphrase: the automatic route matches a crawler IP against Google's published list of addresses, for bulk lookups.
    - Qualifiers: **"For large scale lookups"** (scope); "a crawler's IP address" (singular subject per lookup); "the list of published Google IP addresses" (a *published* list, not a live domain lookup).
    - **Split** (nodes 84 + 85) → not quotable whole; `"For large scale lookups, use an automatic solution to match a crawler's IP address against the list of published Google IP addresses."` (22 units / 133 chars) is the quotable fragment.

### `## Use command line tools` — four printed steps (nodes 88–107)
20. Step 1 — **"Run a reverse DNS lookup on the accessing IP address from your logs, using the host command."**
    - Paraphrase: reverse-resolve the client address recorded in your log with `host`.
    - Qualifiers: **"the accessing IP address from your logs"** — the log's address is the input, so the reverse-DNS hostname is *derived*, not logged; "the host command" is the tool, an inline `<code>` token.
    - **Split** across 3 nodes (91/92/93) → not quotable whole; `"Run a reverse DNS lookup on the accessing IP address from your logs, using the"` (15 units / 78 chars) is the quotable fragment. **This is the only place on either page where the lowercase subject `reverse DNS` occurs** (1 occurrence in S426's body) — the only span that can carry S426's page-named subject.
21. Step 2 — **"Verify that the domain name is either googlebot.com, google.com, or googleusercontent.com."**
    - Paraphrase: check that the returned name is one of those three domains.
    - Qualifiers: **"either … or"** with **three** alternatives (a disjunction of three, not two); the page does **not** state whether the match is exact or a suffix match — its own examples return names that *extend* those domains (`crawl-66-249-66-1.googlebot.com`), so a suffix reading is **[INFERENCE]**, not the page's wording.
    - **Split** across 5 nodes (95/96/97/98/99/100/101) by the three `<code>` domain tokens → not quotable whole; `"Verify that the domain name is either"` (7 units / 37 chars) is the quotable fragment; the three domains are single tokens named in backticks.
22. Step 3 — **"Run a forward DNS lookup on the domain name retrieved in step 1 using the host command on the retrieved domain name."**
    - Paraphrase: forward-resolve the name that step 1 produced.
    - Qualifiers: **"the domain name retrieved in step 1"** — the input is step 1's reverse-DNS *result*, not the logged IP; "using the host command on the retrieved domain name" names the tool and its argument.
    - **Split** across 3 nodes (103/104/105) → not quotable whole; `"Run a forward DNS lookup on the domain name retrieved in step 1 using the"` (15 units / 73 chars) and `"command on the retrieved domain name."` (6 units / 37 chars) are the quotable fragments.
23. Step 4 — **"Verify that it's the same as the original accessing IP address from your logs."**
    - Paraphrase: confirm the forward-resolved address equals the address in your log.
    - Qualifiers: **"the original"** (round-trip equality against the logged address); "it's" = the forward-resolved address.
    - Quoteable whole: 14 units / 78 chars / page-unique.

### Worked examples (nodes 110–132)
24. "Example 1:" — `host 66.249.66.1` → `1.66.249.66.in-addr.arpa domain name pointer crawl-66-249-66-1.googlebot.com.` → `host crawl-66-249-66-1.googlebot.com` → `crawl-66-249-66-1.googlebot.com has address 66.249.66.1`
25. "Example 2:" — `host 35.247.243.240` → `240.243.247.35.in-addr.arpa domain name pointer geo-crawl-35-247-243-240.geo.googlebot.com.` → `host geo-crawl-35-247-243-240.geo.googlebot.com` → `geo-crawl-35-247-243-240.geo.googlebot.com has address 35.247.243.240`
26. "Example 3:" — `host 66.249.90.77` → `77.90.249.66.in-addr.arpa domain name pointer rate-limited-proxy-66-249-90-77.google.com.` → `host rate-limited-proxy-66-249-90-77.google.com` → `rate-limited-proxy-66-249-90-77.google.com has address 66.249.90.77`
    - Qualifiers/notes: the example blocks are `<pre>` text, reproduced line for line with the page's blank line between
      the two lookups and **no shell prompt added**; each line is 2..5 units → below the quotation floor, carried as
      code blocks, never as quotes. Example 2's pointer carries the `geo-crawl-` mask and Example 3's the
      `rate-limited-proxy-` mask, so **two of the three examples exercise a special-case mask**, not the common one;
      **no example uses a user-triggered mask**. Each result line ends in a full stop (part of the `host` output).

### `## Use automatic solutions` (nodes 134–156)
27. **"Alternatively, you can identify Googlebot by IP address by matching the crawler's IP address to the lists of Google crawlers' and fetchers' IP ranges:"**
    - Paraphrase: the automatic route identifies Googlebot by IP, matching it against the published range lists.
    - Qualifiers: **"Alternatively"** (as against the manual route); **"identify Googlebot"** — the automatic method names *Googlebot* specifically, while step 2's manual test accepts three domains generally; "lists" is plural — five lists follow.
    - Quoteable whole: 24 units / 150 chars / page-unique.
28. The five list links (nodes 139/141/143/145/147), in order: `Common crawlers like Googlebot` → `common-crawlers.json`; `Special crawlers like AdsBot` → `special-crawlers.json`; `User-triggered fetchers (users)` → `user-triggered-fetchers.json`; `User-triggered fetchers (Google)` → `user-triggered-fetchers-google.json`; `User-triggered agents` → `user-triggered-agents.json`. Each label is 2..4 units → below the floor; named, not quoted.
29. **"For other Google IP addresses from where your site may be accessed (for example, Apps Scripts), match the accessing IP address against the general list of Google IP addresses."**
    - Paraphrase: for other Google-sourced addresses your site may see (Apps Scripts being one), match against the general Google list.
    - Qualifiers: **"other"** (outside the five category lists); **"may be accessed"** (modal — the site *may* see them); **"for example"** (Apps Scripts illustrative); "the general list" is a sixth, catch-all list.
    - **Split** across 6 nodes (150/151/152/153/154/155/156) → not quotable whole; `"For other Google IP addresses from where your site may be accessed (for example,"` (14 units / 80 chars) is the quotable fragment.
30. **"Note that the IP addresses in the JSON files are represented in CIDR format."**
    - Paraphrase: the IP addresses in those JSON files are written in CIDR notation.
    - Qualifiers: "Note that" = a note, not a rule; "the JSON files" = all of them; "are represented in" (encoding, not the addresses themselves).
    - **Split** across 3 nodes (154/155/156) → not quotable whole; `"Note that the IP addresses in the JSON files are represented in"` (12 units / 63 chars) is the quotable fragment; `CIDR format` is a linked token named in backticks.
31. The final in-block node is `Send feedback` (node 162) — page chrome, not content.

### S426 fidelity notes
- The page's own framing is **verification**, not identification of a carrier: it says "verification is possible",
  "if you're concerned", "sufficient for most use cases", "may or may not respect robots.txt rules". Every one of
  those hedges is load-bearing; an entry that states the page "tells you how to confirm a crawler is Google"
  without them is overclaiming.
- The page **never names the user-agent string** as the field a spoofed request would carry, and never uses
  "spoofed" or "forged". The opening says "while claiming to be from Google" and stops there.
- The three-category taxonomy is S425's content re-presented as a table here; the "always respect robots.txt" claim
  (common crawlers) and the "may or may not respect robots.txt" claim (special-case) are the sharpest contrast on
  the page, and each is scoped ("for automatic crawls").
- The manual route's step-2 matching rule is **not specified** on the page (exact vs suffix). The examples extend
  the three names, so a suffix reading is [INFERENCE].
- The automatic route says "identify Googlebot"; it does not claim to identify fetchers by IP, and it does not
  state how the lists are refreshed or maintained.

---

## Counter-facing constraints for residual reviewers (measured on the frozen counter, `.ufo/waves/round-59/c59_quote_truth.py`)

1. **S425's row-title clause is unsatisfiable as frozen** (corroborated independently by `EntrySignals` finding 1 and
   `ScribeRegistryGate` finding 1; re-measured here). C5 derives
   `title = " — ".join(row[1].split(" — ")[1:-1])` and requires `title == page_title` **and** `units(title) >= 6`;
   `page_title` for S425 is `Google Crawler (User Agent) Overview` = **5 units** (the string has no ` | ` inside it,
   so the split cannot yield a longer title). Measured: `title='Google Crawler (User Agent) Overview' units=5
   page_title units=5 equal=True >=6=False` → the clause cannot be met by any conforming row. S426's title
   `Verify Requests from Google Crawlers and Fetchers` = 7 units and passes.
2. **S425's anchor heading** must be one of the block's h2/h3: `Technical properties of Google's crawlers and fetchers`,
   `Supported transfer protocols`, `Supported content encodings`, `File size limits`, `Crawl rate and host load`,
   `HTTP Caching`, `Verify Google's crawlers and fetchers`. The S425 h1 (`Overview of Google crawlers and fetchers
   (user agents)`) is **not** usable — only h2/h3 are collected.
3. **S426's anchor heading** must be `Use command line tools` or `Use automatic solutions` (its h1 is not collected).
4. **Subject-carrying spans** (C5 requires at least one page-unique span carrying the row's page-named subject):
   - S425 `IP address`: carried by `"The source IP address of the request."` (7 units) and by many sub-spans of node 45
     (`"IP addresses"` contains the subject string). 511 eligible spans on S425 carry it.
   - S426 `reverse DNS`: **exactly one** eligible span family — node 91, e.g. `"Run a reverse DNS lookup on the
     accessing IP address from your logs, using the"` (15 units). The table header `Reverse DNS mask` is
     capitalised and 3 units, so it carries neither the subject (case-sensitive) nor the unit floor.
5. **Non-unique traps** (a span that occurs in *both* bodies and therefore cannot be quoted):
   - `"They always respect robots.txt rules for automatic crawls."` (S425 node 21 / S426 node 23)
   - `"acts on the request of a user."` (S425 node 39 / S426 node 49)
   The two-sentence combination used by the S426 draft (18 units) is page-unique and does pass.
6. `Learn how to use these details to` is quotable at 7 units; `verify Google's crawlers and fetchers` is 5 units and
   falls below the floor.

## How this reference was produced
Read-only: the retained bodies, `span_tools.py`, and the frozen counter's own module
(`c59_quote_truth.py` imported for `units`, `text_segments`, `in_content`, `content_window`). Every verbatim
sentence and every span measurement was extracted mechanically from the body bytes; no sentence was retyped by hand.
Scratch: `/fast/scratch/hyaku/kake-r59/ReviewerFidelityPrep` (removed at exit). No tool was installed; no lane,
git or jj state was touched.
