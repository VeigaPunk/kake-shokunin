# ReviewerFidelityPrep

Seat: leaf reviewer, read-only. Built the sentence-by-sentence fidelity yardstick for C3's two retained
Google pages. Full artifact: `.ufo/waves/round-59/w1/ReviewerFidelityPrep.files/reference.md` (S425 and S426
sentence lists, verbatim from the body bytes, each with a paraphrase, its qualifiers, and its quotability).

## What was run (all read-only)

- Read `.ufo/waves/round-59/contract.md`, `c59_quote_truth.py` (frozen counter + the wave-1 v2 working-tree
  edits), `span_tools.py`, `sources/receipts.json`, `sources/S425.html`, `sources/S426.html`.
- `python3 -B span_tools.py window S425|S426` -> 157 / 90 non-empty article-block text nodes (the counter's
  `text_segments` returns 217 / 165 entries, the rest being empty strings between tags); `spans S425|S426` ->
  per-node unit/char/unique table.
- Imported the counter's own module for `units`, `text_segments`, `in_content`, `content_window`, `article_headings`
  so every measurement uses the counter's code, not a re-implementation.
- `span_tools.py check <S> "<span>"` re-run on every span I assert as quotable (all outputs quoted below).
- Every verbatim sentence in the reference was extracted mechanically from the retained body bytes; nothing retyped.
- Self-check of the artifact (`ReviewerFidelityPrep.files/validate_ref.py`, output `validate_ref.out`): every
  "Quoteable whole: N units / M chars / page-unique" claim re-measured against the counter's own code — 35 numbered
  items, 18 whole-quote claims, **0 number mismatches, 0 unsupported/over-ceiling/unmarked**; every remaining item is
  explicitly marked split, over-ceiling or not page-unique.

Not run: the counter against any revision (no after-state is mine to score); no `curl`, no network fetch.

## S425:

Scope: the assigned `Verify Google's crawlers and fetchers` section and its IP-address paragraph.

IP-address paragraph (one `<p>`, article node 45, under `## Technical properties of Google's crawlers and fetchers`):

1. "Google's crawlers and fetchers are designed to be run simultaneously by thousands of machines to improve performance and scale as the web grows." — Google's clients run concurrently on thousands of machines to improve performance and scale with the web. No modal; "thousands" indefinite; "designed to be" = design intent, not observation. Quotable whole: 23u/144c, unique.
2. "To optimize bandwidth usage, these clients are distributed across many datacenters across the world so they're located near the sites that they might access." — to save bandwidth the clients are spread over many datacenters worldwide, putting them near the sites they might fetch. "To optimize bandwidth usage" = stated purpose; "many" indefinite; **"might access"** modal. Quotable whole: 24u/157c, unique.
3. "Therefore, your logs may show visits from several IP addresses." — so a site's log *can* show the crawler arriving from more than one address. **"may"** (possibility) and **"several"** (unspecified count) are the load-bearing qualifiers. Quotable whole: 10u/63c, unique. This is the sentence the stale lane claim is corrected against.
4. "Google egresses primarily from IP addresses in the United States." — most of Google's outbound traffic comes from US addresses. **"primarily"** = majority, not all. Quotable whole: 10u/65c, unique.
5. "In case Google detects that a site is blocking requests from the United States, it may attempt to crawl from IP addresses located in other countries." — if Google notices a site blocking US-sourced requests, it may try crawling from addresses elsewhere. "In case" = conditional trigger and it is **Google's own detection**; **"may attempt"** = double hedge; no country named. Whole sentence is 26u — **over the 25-unit ceiling**; quotable fragments measured page-unique: 25u/138c (`"In case Google detects ... located in other"`), 25u/146c (`"case Google detects ... in other countries."`), 12u/69c (`"it may attempt to crawl from IP addresses located in other countries."`), 13u/75c (`"case Google detects that a site is blocking requests from the United States"`).

Verify section (last h2 of the block):

6. "Google's crawlers identify themselves in three ways:" — Google's crawlers present themselves in three identifiable ways. **"three"** is an explicit count and the list has exactly three items; the verb is **"identify themselves"** (self-presentation, not proof of authenticity); no tie-break rule is given. Quotable whole: 7u/52c, unique.
7. "The HTTP user-agent request header." (item 1) — the HTTP `user-agent` header. **Split by inline markup** into nodes `The HTTP` / `user-agent` / `request header.` — not a raw substring of any one node, so it **cannot be quoted**; each fragment is 2/1/2 units, all under the 6-unit floor. Must be named, not quoted.
8. "The source IP address of the request." (item 2) — the request's source IP. No qualifier; the page says nothing about stability or per-crawler uniqueness. Quotable whole: 7u/37c, unique. **Carries the S425 subject `IP address`.**
9. "The reverse DNS hostname of the source IP." (item 3) — the reverse-DNS name of that address. No qualifier, but this is a **derived** value: the log holds the IP and the hostname comes from a lookup (S426 steps 1 and 3). Quotable whole: 8u/42c, unique.
10. "Learn how to use these details to verify Google's crawlers and fetchers." — the page points elsewhere for how to use the three details. **The method is not on this page.** Split across 3 nodes (the link text is one) -> not quotable whole; `"Learn how to use these details to"` (7u/33c, unique) is the only fragment above the floor; `"verify Google's crawlers and fetchers"` is 5u and below it.

Fidelity points residual reviewers should hold the line on:
- The page says crawlers identify themselves in three ways. It does **not** say a log records three fields — the
  reverse-DNS hostname is computed from the logged IP by a lookup. "A log records three signals" adds to the page.
- The stale line ("A user-agent string is the only thing a server log records about the crawler.") is contradicted
  by items 8 and 9 and by sentence 3. The page itself never says the log records a reverse-DNS hostname.
- "may" (s.3), "primarily" (s.4) and "may attempt" (s.5) must survive into any entry or Gate line.
- The printed revision `Last updated 2026-06-12 UTC.` is a body text node but sits **outside** the article window
  (char 38715 > window end 38178): quotable only via C5's "any text node of the body" test, never in-block.

Out of scope for this reference (S425): taxonomy table, transfer protocols, content encodings, file-size limits,
crawl rate, HTTP caching — listed in the artifact.

## S426:

Whole article block. Node map and per-sentence verdicts are in the artifact; the load-bearing ones:

1. "You can verify if a request to your server really is from Google." — the page says you can confirm a request really came from Google. "can verify" = capability not guarantee; **"really"** is colloquial, no defined test; the claim is about *Google* generally, not Googlebot. **Split** (link on "from Google") -> not quotable whole; `"You can verify if a request to your server really is"` (11u/52c, unique) is the fragment.
2. "Verification is possible for crawlers such as Googlebot, as well as other requests." — verification works for Googlebot-class crawlers and for other requests too. **"such as"** non-exhaustive; **"as well as other requests"** = not crawler-limited. Quotable whole: 13u/83c, unique.
3. "This is useful if you're concerned that spammers or other troublemakers are accessing your site while claiming to be from Google." — for operators suspecting impostors under a Google claim. **"if you're concerned"** conditional; the page never names the user-agent string as the claim's carrier and never says spoofed/forged. Quotable whole: 21u/129c, unique.
4. "Google's crawlers and fetchers fall into three categories:" — three categories. **"three"** explicit; note **four** table columns (Type, Description, Reverse DNS mask, IP ranges). Quotable whole: 8u/58c, unique.
5. Table headers: `Type`, `Description`, `Reverse DNS mask`, `IP ranges`. **`Reverse DNS mask` is capitalised and 3 units** — it carries neither S426's subject `reverse DNS` (case-sensitive test) nor the 6-unit floor.
6. Common crawlers: "The common crawlers used for Google's products (such as Googlebot)." (10u/67c, unique, "such as" non-exhaustive) + "They always respect robots.txt rules for automatic crawls." — **"always" is absolute but scoped to "for automatic crawls"**; this sentence alone occurs in **both** bodies (S425 node 21) and is **not page-unique**; the two-sentence combination (18u/126c) **is** unique and quotable whole.
7. Special-case crawlers: the long defining sentence is 33u (over the ceiling); the cell is one text node, so measured quotable sub-spans are 17u/116c (`"Crawlers or fetchers that perform specific functions for Google products (such as AdsBot) where there's an agreement"`) and 18u/114c (`"an agreement between the crawled site and the product about the access or for abuse-specific crawling or fetching."`). **"These crawlers or fetchers may or may not respect robots.txt rules."** (11u/67c, unique) — an explicit two-sided non-commitment, the strongest hedge on the page; it must not be flattened to "respects" or "ignores".
8. User-triggered fetchers: "Tools and product functions where the end user triggers a fetch." (11u/64c, unique) + "For example, Google Site Verifier acts on the request of a user." (**"For example"**; split by the link, and `acts on the request of a user.` alone also occurs in S425 -> not unique standalone) + "Because the fetch was requested by a user, these fetchers ignore robots.txt rules." (**"Because"** = explicit causal clause; 13u/82c, unique) + "Fetchers controlled by Google originate from IPs in the user-triggered-fetchers-google.json object and resolve to a google.com hostname." (**"controlled by Google"** distinguishes this list; split across 5 nodes by the `<code>` tokens; quotable fragment `"Fetchers controlled by Google originate from IPs in the"` 9u/55c) + "IPs in the user-triggered-fetchers.json object resolve to gae.googleusercontent.com hostnames." (split across 5 nodes; quotable continuation `"hostnames. These IPs are used, for example,"` 7u/43c) + "These IPs are used, for example, if a site running on Google Cloud (GCP) has a feature that requires fetching external RSS feeds on the request of the user of that site." (**"for example"**; "the user of that site" = the site's end user, not its operator; 32u/169c -> over both ceilings; quotable at 17u/86c and 7u/43c).
9. "There are two methods for verifying requests from Google:" (**"two"** explicit; 9u/57c, unique) + "Manually: For one-off lookups, use command line tools." (**"For one-off lookups"** scopes the manual route to isolated lookups; split by the `Manually` link -> fragment `"For one-off lookups, use command line tools."` 7u/44c) + **"This method is sufficient for most use cases."** (**"for most use cases"** — the deliberate hedge that motivates the automatic route; dropping "for most" overstates the page; 8u/45c, unique) + "Automatically: For large scale lookups, use an automatic solution to match a crawler's IP address against the list of published Google IP addresses." (**"For large scale lookups"** scope; "a crawler's IP address" singular; "the list of published Google IP addresses" = a published list, not a live domain lookup; split -> fragment 22u/133c).
10. Four printed steps: "Run a reverse DNS lookup on the accessing IP address from your logs, using the host command." — **the log's address is the input, so the reverse-DNS hostname is derived, not logged**; split across 3 nodes; quotable fragment `"Run a reverse DNS lookup on the accessing IP address from your logs, using the"` (15u/78c, unique) — **the only place on either page where lowercase `reverse DNS` occurs** (1 occurrence in S426), hence the only span family that can carry S426's page-named subject. "Verify that the domain name is either googlebot.com, google.com, or googleusercontent.com." — **"either … or" with three alternatives**; the page never says whether the match is exact or suffix, and its examples return names that *extend* those domains, so a suffix reading is [INFERENCE]; split across 5 nodes -> fragment `"Verify that the domain name is either"` 7u/37c. "Run a forward DNS lookup on the domain name retrieved in step 1 using the host command on the retrieved domain name." — the input is step 1's reverse-DNS *result*; fragments 15u/73c and 6u/37c. "Verify that it's the same as the original accessing IP address from your logs." — **"the original"** = round-trip equality against the logged address; 14u/78c, unique.
11. Three worked examples reproduced line for line (no prompt added; each line 2..5 units -> below the floor, so code blocks, not quotes). Example 2's pointer carries the `geo-crawl-` mask and Example 3's the `rate-limited-proxy-` mask — **two of three examples exercise a special-case mask**; **no example uses a user-triggered mask**.
12. "Alternatively, you can identify Googlebot by IP address by matching the crawler's IP address to the lists of Google crawlers' and fetchers' IP ranges:" — **"Alternatively"**; **"identify Googlebot"** (the automatic method names Googlebot specifically, while step 2's manual test accepts three domains generally); "lists" plural, five lists follow (labels 2..4 units -> named, not quoted); 24u/150c, unique. + "For other Google IP addresses from where your site may be accessed (for example, Apps Scripts), match the accessing IP address against the general list of Google IP addresses." (**"other"**, **"may be accessed"**, **"for example"**; split across 6 nodes -> fragment 14u/80c) + "Note that the IP addresses in the JSON files are represented in CIDR format." ("Note that" = a note, not a rule; split across 3 nodes -> fragment 12u/63c; `CIDR format` is a linked token). The last in-block node is `Send feedback` (page chrome).

Counter-facing constraints residual reviewers need (measured):
- **S425's row-title clause is unsatisfiable as frozen.** C5 requires `title == page_title` **and** `units(title) >= 6`; `page_title` for S425 is `Google Crawler (User Agent) Overview` = **5 units**, and the string has no ` | ` inside it, so no row shape can raise it. Measured: `title='Google Crawler (User Agent) Overview' units=5 page_title units=5 equal=True >=6=False`. S426's `Verify Requests from Google Crawlers and Fetchers` = 7 units and passes. (Independently reported by `EntrySignals` finding 1 and `ScribeRegistryGate` finding 1; re-measured here from the counter's own code.)
- Anchor headings must be h2/h3 of the article block. S425: `Technical properties of Google's crawlers and fetchers`, `Supported transfer protocols`, `Supported content encodings`, `File size limits`, `Crawl rate and host load`, `HTTP Caching`, `Verify Google's crawlers and fetchers` (its h1 is not collected). S426: `Use command line tools` / `Use automatic solutions` (its h1 is not collected).
- Non-unique traps (occur in both bodies, so unquotable standalone): "They always respect robots.txt rules for automatic crawls." and "acts on the request of a user."
- The printed revision `Last updated 2026-03-20 UTC.` (S426) and `Last updated 2026-06-12 UTC.` (S425) are body text nodes **outside** the article window (34060 > 33523; 38715 > 38178).

## Residual risk / limits

- I measured quote truth and structure, not faithfulness of any after-state entry: no entry is committed, so no
  after-state was scored. Whether the drafted S425/S426 entries keep every qualifier above is a reviewer call on
  the drafts, not on my measurements.
- The reference covers only the assigned scopes (S425's IP paragraph + Verify section; S426's whole block). S425's
  remaining sections are listed but not paraphrased.
- Both article blocks are **entirely ASCII** (measured: zero characters above U+007F in either block), so no curly
  quote, em dash or other non-ASCII character appears in the quotable text; the C5 curly-quote refusal is not
  triggered by these two pages, and the quotes in the reference are byte-faithful as ASCII.
- Tooling: none installed, none upgraded (no need); scratch
  `/fast/scratch/hyaku/kake-r59/ReviewerFidelityPrep` removed at exit. Only
  `.ufo/waves/round-59/w1/ReviewerFidelityPrep.md` and
  `.ufo/waves/round-59/w1/ReviewerFidelityPrep.files/` (the reference plus the measurement receipts and their
  README) were written in the lane; no git/jj operation ran there.

VERDICT: Reference delivered — S425 (10 sentences) and S426 (whole article block) listed verbatim with paraphrases, qualifiers and measured quotability; the one blocking defect is the frozen C5 title floor (S425's 5-unit page title against a 6-unit requirement), which no conforming row can satisfy.
