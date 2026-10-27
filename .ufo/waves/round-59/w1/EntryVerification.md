# EntryVerification

Seat scope: claim C3, NEW row S426. Lane repo read-only; writes are only this report and
`EntryVerification.files/`. No git/jj operation ran in the lane; no pacman, no tool install.

## Behaviour

- Read the frozen contract (`contract.md`), the C3 counter's C2/C3/C4/C5 code (`c59_quote_truth.py`), `span_tools.py`,
  `sources/receipts.json`, and the retained body `sources/S426.html` (69789 bytes,
  sha256 `8df9d4ade1d1f335060af05229c4d90b15d8136b9807cfab17a088f3292f0879`, HTTP 200, fetched 2026-10-27T01:21:22Z).
- Read `span_tools.py window S426` in full and enumerated its text nodes (`spans S426`): h1, two h2s
  (`Use command line tools`, `Use automatic solutions`), a 4-step ordered list, three worked command/output
  blocks, a 5-link list, one general-list paragraph. The printed revision line sits after
  `</devsite-content-footer>`, i.e. outside the article block, so it is not quotable.
- Drafted `corpus/knowledge/googlebot-verification.md`, then re-implemented the counter's entry-side checks in
  `EntryVerification.files/validate_entry.py` against the counter's own module: 11-cell row, `<title>`-derived
  cell 2, anchor-heading membership, printed-date text node, every `"..."` span raw + in-block + <=25 units +
  <=160 chars + page-unique, >=3 unique spans, one carrying `reverse DNS`. Result: ALL PASS (19 quoted spans,
  19 unique, subject span present).
- `recheck:` grep was run against the retained body, not the network: `grep -F -c 'Run a reverse DNS lookup on the
  accessing IP address' sources/S426.html` -> 1 (span does not cross a source line break).

## ENTRY:

````markdown
source: S426 — https://developers.google.com/crawling/docs/crawlers-fetchers/verify-google-requests — § Use command line tools (Last updated 2026-03-20 UTC) — fetched 2026-10-27
verified-at: 2026-10-27
recheck: 180d — `curl -fsSL --compressed 'https://developers.google.com/crawling/docs/crawlers-fetchers/verify-google-requests' | grep -F -c 'Run a reverse DNS lookup on the accessing IP address'` -> 1 (grep against the retained body 1, 2026-10-27)
ground: per-engine crawl hygiene — the operator's own procedure for telling a request that claims to come from Google's crawlers and fetchers from one that does not

# Google's verification page tests a claimed crawler by reverse DNS on the logged IP, then forward DNS back to that IP

The page's browser title is Verify Requests from Google Crawlers and Fetchers, its on-page heading prints the same words in sentence case, and its revision line reads Last updated 2026-03-20 UTC (a line that sits after the article block; see § Quote classes) [S426]. Its opening states the purpose and the audience [S426]:

> "Verification is possible for crawlers such as Googlebot, as well as other requests."

and names the concern it answers, mid-sentence [S426]:

> "concerned that spammers or other troublemakers are accessing your site while claiming to be from Google"

The page does not say where that claim is carried: it never names the user-agent string, and it never uses the words forged or spoofed. Reading the paragraph as a statement about user-agent spoofing would add to the page; that reading is [INFERENCE] at most.

## The three categories the page sorts Google's agents into

> "Google's crawlers and fetchers fall into three categories:"

The table prints four columns — Type, Description, Reverse DNS mask, IP ranges — and three rows, carried here as printed, with the inline-code tokens named in backticks because each falls below the quotation floor [S426]:

- **Common crawlers** — mask `crawl-***-***-***-***.googlebot.com` or `geo-crawl-***-***-***-***.geo.googlebot.com`; IP ranges in `common-crawlers.json`:

  > "The common crawlers used for Google's products (such as Googlebot). They always respect robots.txt rules for automatic crawls."

- **Special-case crawlers** — mask `rate-limited-proxy-***-***-***-***.google.com`; IP ranges in `special-crawlers.json`. The description runs past the 25-unit ceiling; the part carried is its closing robots clause:

  > "may or may not respect robots.txt rules"

- **User-triggered fetchers** — masks `***-***-***-***.gae.googleusercontent.com` or `google-proxy-***-***-***-***.google.com`; IP ranges in `user-triggered-fetchers.json`, `user-triggered-fetchers-google.json`, and `user-triggered-agents.json`:

  > "Tools and product functions where the end user triggers a fetch. For example,"

  (`Google Site Verifier` is the example named there), and the cell continues:

  > "acts on the request of a user. Because the fetch was requested by a user, these fetchers ignore robots.txt rules."

The user-triggered cell then separates the Google-controlled fetchers from the user-cloud ones [S426]:

> "Fetchers controlled by Google originate from IPs in the"

`user-triggered-fetchers-google.json`, whose entries the page says resolve to `google.com` hostnames, while `user-triggered-fetchers.json` resolves to `gae.googleusercontent.com` [S426]:

> "hostnames. These IPs are used, for example,"

if a site running on Google Cloud (GCP) has a feature that requires fetching external RSS feeds on the request of that site's user [S426]. So the masks and the range files answer one question at two costs, a per-request lookup against a list membership test [INFERENCE].

## Two methods

> "There are two methods for verifying requests from Google:"

The page prints its labels as `Manually` and `Automatically`, each one token followed by a colon-leading sentence; the sentences are quoted and the labels named in backticks [S426]:

> "For one-off lookups, use command line tools. This method is sufficient for most use cases."

> "For large scale lookups, use an automatic solution to match a crawler's IP address against the list of published Google IP addresses."

## The command-line procedure, four printed steps

Step one, on the logged address [S426]:

> "Run a reverse DNS lookup on the accessing IP address from your logs, using the"

`host` command. Step two constrains the returned name [S426]:

> "Verify that the domain name is either"

`googlebot.com`, `google.com`, or `googleusercontent.com` — three inline-code tokens closing that sentence. Step three closes the loop forward [S426]:

> "Run a forward DNS lookup on the domain name retrieved in step 1 using the"

`host` command on the retrieved domain name. Step four states the verdict [S426]:

> "Verify that it's the same as the original accessing IP address from your logs."

The page does not spell out the comparison rule for step two — exact equality with one of the three names, or a suffix match. Its worked examples return names that extend the three names, so the suffix reading is [INFERENCE] here, as is any statement about what a failed match proves beyond the step's own wording.

## Worked examples, as printed

Three command/output pairs; command lines are terminal code spans and result lines are the pre text, reproduced line for line with the page's blank line between the two lookups and no shell prompt added [S426]:

Example 1:

```
host 66.249.66.1
1.66.249.66.in-addr.arpa domain name pointer crawl-66-249-66-1.googlebot.com.

host crawl-66-249-66-1.googlebot.com
crawl-66-249-66-1.googlebot.com has address 66.249.66.1
```

Example 2:

```
host 35.247.243.240
240.243.247.35.in-addr.arpa domain name pointer geo-crawl-35-247-243-240.geo.googlebot.com.

host geo-crawl-35-247-243-240.geo.googlebot.com
geo-crawl-35-247-243-240.geo.googlebot.com has address 35.247.243.240
```

Example 3:

```
host 66.249.90.77
77.90.249.66.in-addr.arpa domain name pointer rate-limited-proxy-66-249-90-77.google.com.

host rate-limited-proxy-66-249-90-77.google.com
rate-limited-proxy-66-249-90-77.google.com has address 66.249.90.77
```

The second example's pointer name carries the `geo-crawl-` mask and the third's the `rate-limited-proxy-` mask, so the page's own examples cover the common and special-case categories; none of the three carries a user-triggered mask.

## The automatic method

> "Alternatively, you can identify Googlebot by IP address by matching the crawler's IP address to the lists of Google crawlers' and fetchers' IP ranges:"

Five list links follow, each a JSON file under `/static/crawling/ipranges/`, in this order [S426]: `Common crawlers like Googlebot` → `common-crawlers.json`; `Special crawlers like AdsBot` → `special-crawlers.json`; `User-triggered fetchers (users)` → `user-triggered-fetchers.json`; `User-triggered fetchers (Google)` → `user-triggered-fetchers-google.json`; `User-triggered agents` → `user-triggered-agents.json`. The page then adds a general list for other Google addresses [S426]:

> "For other Google IP addresses from where your site may be accessed (for example,"

`Apps Scripts`), matched against `https://www.gstatic.com/ipranges/goog.json`, plus a format note [S426]:

> "Note that the IP addresses in the JSON files are represented in"

`CIDR format` (the page links the term to Wikipedia's article on classless inter-domain routing). The page gives no refresh interval for the lists and no statement about how they are maintained.

## What this entry does not establish

- It does not establish that a Google crawler sends any particular user-agent on any request: the opening paragraph names a claim without naming its carrier.
- It does not establish the matching rule behind step two (see above), nor what a failed forward lookup is evidence of beyond the page's own step wording.
- It does not carry the three category pages the table links (`google-common-crawlers`, `google-special-case-crawlers`, `google-user-triggered-fetchers`); this entry does not open them.
- It does not establish list freshness, any list field beyond CIDR, or any Google behaviour: nothing was crawled and no Google request was observed.
- It establishes nothing about other operators' identity tests. Related lane entries, by path: `corpus/knowledge/crawler-identity.md` (the family and its two subtypes), `corpus/knowledge/baidu-spider-identification.md` (another operator's reverse-then-forward DNS test), `corpus/knowledge/robots-txt-rules.md` (refusal rules the three categories treat differently), and `corpus/knowledge/crawl-scope-per-host.md` (host-root scope).

## Quote classes

Every block quotation above is an exact raw substring of one text node of the article block in the retained body `S426.html` (69789 bytes, HTTP 200, sha256 `8df9d4ade1d1f335060af05229c4d90b15d8136b9807cfab17a088f3292f0879`), each 6..25 units and at most 160 characters, page-unique across both round-59 retained bodies, checked with `.ufo/waves/round-59/span_tools.py check S426`. Several quotations stop at an inline-code or link boundary rather than closing their sentence: step one and step three end before the `host` token, step two before its three domain tokens, the category descriptions before their mask tokens, the user-triggered description before the linked example name, and the two method sentences begin after their printed labels. No sentence is joined across nodes anywhere in this entry. The three example blocks are not marked as quotations because their lines fall below the 6-unit quotation floor; they are reproduced from the page's own `pre` text, whose characters are article-block text. Inline-code tokens (the command name, the three domain names, the masks, the JSON file names, the two script and format terms) are named in backticks for the same reason. The printed revision line sits after `</devsite-content-footer>`, outside the article block, so it is reported in the header and the anchor cell and is not quoted here.

Scope note: this entry records what the operator's page states, and nothing more; no crawl was observed and no Google behaviour was measured.
````

## GATE LINE:

- S426 — https://developers.google.com/crawling/docs/crawlers-fetchers/verify-google-requests — accessed 2026-10-27 — § Use command line tools (Last updated 2026-03-20 UTC) — quote: "Run a reverse DNS lookup on the accessing IP address from your logs, using the" (15 units; substring of one collapsed text node of the retained body, sha256 8df9d4ade1d1f335060af05229c4d90b15d8136b9807cfab17a088f3292f0879, 69789 bytes, HTTP 200)

## REGISTRY ROW:

| S426 | Google for Developers — Verify Requests from Google Crawlers and Fetchers — https://developers.google.com/crawling/docs/crawlers-fetchers/verify-google-requests | docs | A | Request verification for Google crawlers and fetchers: the three-category table, the four printed reverse-then-forward DNS steps, and the published IP-range lists | § Use command line tools (Last updated 2026-03-20 UTC) | **Reverse DNS then forward DNS** — the operator's four printed steps (reverse-resolve the logged IP with `host`, require a name under googlebot.com / google.com / googleusercontent.com, forward-resolve it, require the same IP), three worked `host` examples, and the alternative of matching the IP against the published JSON range lists | mined | 2026-10-27 | 180d | corpus/knowledge/googlebot-verification.md |

Row facts measured: 11 cells, no pipe inside a cell, no escaped pipe, status `mined`, opened 2026-10-27,
recheck `180d`, kind `docs`, tier `A`, URL extracted by the counter's `row_url` equals the contract URL,
cell 2 title equals the page `<title>` before the first ` | ` (`Verify Requests from Google Crawlers and
Fetchers`, 7 units), used-by resolves to exactly `["corpus/knowledge/googlebot-verification.md"]` (contract C4).

## SPAN CHECKS:

span_tools `check S426` per quoted span, in entry order (units/chars, in_text_node, count_in_body, unique, within_ceilings):

- "Verification is possible for crawlers such as Googlebot, as well as other requests." 13u/83c node=True count=1 unique=True ceil=True
- "concerned that spammers or other troublemakers are accessing your site while claiming to be from Google" 16u/103c node=True count=1 unique=True ceil=True
- "Google's crawlers and fetchers fall into three categories:" 8u/58c node=True count=1 unique=True ceil=True
- "The common crawlers used for Google's products (such as Googlebot). They always respect robots.txt rules for automatic crawls." 18u/126c node=True count=1 unique=True ceil=True
- "may or may not respect robots.txt rules" 7u/39c node=True count=1 unique=True ceil=True
- "Tools and product functions where the end user triggers a fetch. For example," 13u/77c node=True count=1 unique=True ceil=True
- "acts on the request of a user. Because the fetch was requested by a user, these fetchers ignore robots.txt rules." 20u/113c node=True count=1 unique=True ceil=True
- "Fetchers controlled by Google originate from IPs in the" 9u/55c node=True count=1 unique=True ceil=True
- "hostnames. These IPs are used, for example," 7u/43c node=True count=1 unique=True ceil=True
- "There are two methods for verifying requests from Google:" 9u/57c node=True count=1 unique=True ceil=True
- "For one-off lookups, use command line tools. This method is sufficient for most use cases." 15u/90c node=True count=1 unique=True ceil=True
- "For large scale lookups, use an automatic solution to match a crawler's IP address against the list of published Google IP addresses." 22u/133c node=True count=1 unique=True ceil=True
- "Run a reverse DNS lookup on the accessing IP address from your logs, using the" 15u/78c node=True count=1 unique=True ceil=True  (subject span: `reverse DNS`)
- "Verify that the domain name is either" 7u/37c node=True count=1 unique=True ceil=True
- "Run a forward DNS lookup on the domain name retrieved in step 1 using the" 15u/73c node=True count=1 unique=True ceil=True
- "Verify that it's the same as the original accessing IP address from your logs." 14u/78c node=True count=1 unique=True ceil=True
- "Alternatively, you can identify Googlebot by IP address by matching the crawler's IP address to the lists of Google crawlers' and fetchers' IP ranges:" 24u/150c node=True count=1 unique=True ceil=True
- "For other Google IP addresses from where your site may be accessed (for example," 14u/80c node=True count=1 unique=True ceil=True
- "Note that the IP addresses in the JSON files are represented in" 12u/63c node=True count=1 unique=True ceil=True

No curly double quote appears anywhere in the entry (counter `CURLY` scan clean).

## OMITTED:

- The three category pages the table links (`google-common-crawlers`, `google-special-case-crawlers`,
  `google-user-triggered-fetchers`): not opened; out of this row's scope.
- Bodies of the five IP-range JSON files and of the general `goog.json` list: names and order carried, contents
  not fetched, so no statement about their fields beyond the page's CIDR note.
- The `Google Site Verifier` support page, the Apps Scripts page and the Wikipedia CIDR article: linked by the
  page, not opened; only the linked labels are carried.
- Page chrome outside the article block (header, navigation, sidebar, footer, feedback widget, the duplicated
  revision string inside the feedback `template` JSON): excluded by construction (article window
  `class="devsite-article-body` .. `<devsite-content-footer`).
- The masks, the domain names, the command name and the JSON file names are single tokens, below the 6-unit
  quotation floor; carried in backticks rather than as quotations. Example blocks likewise (lines of 2..5 units).

## Touched surfaces

- `kake-shokunin/.ufo/waves/round-59/w1/EntryVerification.md` (this report)
- `kake-shokunin/.ufo/waves/round-59/w1/EntryVerification.files/googlebot-verification.md` (entry draft)
- `kake-shokunin/.ufo/waves/round-59/w1/EntryVerification.files/validate_entry.py` (scratch checker, receipt)
- Nothing else in the lane: no registry, lesson, knowledge file, index, git or jj state was written.

## Findings

- Step two's rule is ambiguous as printed: `Verify that the domain name is either` + `googlebot.com`, `google.com`,
  `googleusercontent.com`; the page never says exact equality or suffix. The examples return names that extend
  those three, so a suffix reading is [INFERENCE] and the entry says so.
- The opening paragraph says a request may be `claiming to be from Google` but never names the user-agent string
  and never uses forged/spoofed; the entry makes no user-agent-forgery claim.
- The page counts categories as four columns and three rows; the user-triggered row is the only one whose IP-range
  cell names three files, and it alone carries the `google.com` / `gae.googleusercontent.com` hostname split.
- Example 2 and example 3 exercise the `geo-crawl-` and `rate-limited-proxy-` masks; no example covers a
  user-triggered mask.

## Unrun / limits

- The real counter `python3 -B .ufo/waves/round-59/c59_quote_truth.py --root <lane> --revision <rev>` was NOT run:
  it needs the entry committed at the measured revision plus the registry row, the lesson Gate line, the C7/C8
  append receipts, which belong to the planner's integration. C3's after-state is therefore unmeasured by me.
- No `curl` ran this seat; the `recheck:` count is a grep against the retained body. No crawl, no DNS lookup and
  no Google request was made or observed.
- The counter does not test whether the entry is faithful (reviewer/critic job). My faithfulness basis is the
  full `window S426` read plus the raw table/method markup.
- Scratch `/fast/scratch/hyaku/kake-r59/EntryVerification` removed after copying the two receipts.

VERDICT: S426 entry drafted and self-checked against the counter's rules (19/19 unique spans, ALL PASS); the counter itself was not run because the entry is not committed.
