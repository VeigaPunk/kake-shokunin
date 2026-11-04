source: S426 — https://developers.google.com/crawling/docs/crawlers-fetchers/verify-google-requests — § Use command line tools (Last updated 2026-03-20 UTC) — fetched 2026-10-27
verified-at: 2026-10-27
recheck: 180d — `curl -fsSL --compressed 'https://developers.google.com/crawling/docs/crawlers-fetchers/verify-google-requests' | grep -F -c 'Run a reverse DNS lookup on the accessing IP address'` -> 1 (grep against the retained body 1, 2026-10-27)
ground: per-engine crawl hygiene — the operator's own procedure for telling a request that claims to come from Google's crawlers and fetchers from one that does not

# Google's verification page tests a claimed crawler by reverse DNS on the logged IP, then forward DNS back to that IP

The page's browser title begins Verify Requests from Google Crawlers and Fetchers (the `<title>` element continues with ` | `-separated site suffixes), its on-page heading prints the same words in sentence case, and its revision line reads Last updated 2026-03-20 UTC (a line that sits after the article block; see § Quote classes) [S426]. Its opening states the purpose and the audience [S426]:

> "Verification is possible for crawlers such as Googlebot, as well as other requests."

and names the concern it answers, mid-sentence [S426]:

> "concerned that spammers or other troublemakers are accessing your site while claiming to be from Google"

The page does not say where that claim is carried: it never names the user-agent string, and it never uses the words forged or spoofed. Reading the paragraph as a statement about user-agent spoofing would add to the page; that reading is [INFERENCE] at most.

## The three categories the page sorts Google's agents into

> "Google's crawlers and fetchers fall into three categories:"

The table prints four columns — Type, Description, Reverse DNS mask, IP ranges — and three rows, carried here as printed, with the inline-code tokens named in backticks because each falls below the quotation floor [S426]:

- **Common crawlers** — mask `crawl-***-***-***-***.googlebot.com` or `geo-crawl-***-***-***-***.geo.googlebot.com`; IP ranges in `common-crawlers.json`:

  > "The common crawlers used for Google's products (such as Googlebot). They always respect robots.txt rules for automatic crawls."

- **Special-case crawlers** — mask `rate-limited-proxy-***-***-***-***.google.com`; IP ranges in `special-crawlers.json`. The description runs past the 25-unit ceiling; the part carried is its closing robots predicate:

  > "may or may not respect robots.txt rules"

- **User-triggered fetchers** — masks `***-***-***-***.gae.googleusercontent.com` or `google-proxy-***-***-***-***.google.com`; IP ranges in `user-triggered-fetchers.json`, `user-triggered-fetchers-google.json`, and `user-triggered-agents.json`:

  > "Tools and product functions where the end user triggers a fetch. For example,"

  (`Google Site Verifier` is the example named there), and the cell continues:

  > "acts on the request of a user. Because the fetch was requested by a user, these fetchers ignore robots.txt rules."

  **[r60-correction 2026-10-27]** The cell quoted above says these fetchers "ignore robots.txt rules" (page revision `Last updated 2026-03-20 UTC`); the user-triggered fetchers page that cell links to [S428], at the later revision `Last updated 2026-08-19 UTC`, prints "Because the fetch was requested by a user, these fetchers generally ignore robots.txt rules."
  The later page qualifies the posture with `generally` and names no exception, so neither page says which
  user-triggered fetches, if any, follow robots.txt rules (w2/ReviewerCorrection: the earlier wording overreached).
  The sentence above stays as historical text quoted from its own page and revision; the fuller reading of the category
  page is `google-user-triggered-fetchers.md` (S428).

The user-triggered cell then separates the Google-controlled fetchers from the other user-triggered fetchers, which the page illustrates with a Google Cloud site fetching RSS feeds for its user [S426]:

> "Fetchers controlled by Google originate from IPs in the"

`user-triggered-fetchers-google.json` object, and the page says those fetchers resolve to a `google.com` hostname, while IPs in the `user-triggered-fetchers.json` object resolve to `gae.googleusercontent.com` hostnames [S426]:

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

Every block quotation above is an exact raw substring of one text node of the article block in the retained body `S426.html` (69789 bytes, HTTP 200, sha256 `8df9d4ade1d1f335060af05229c4d90b15d8136b9807cfab17a088f3292f0879`), each 6..25 units and at most 160 characters, page-unique across both round-59 retained bodies, checked with `.ufo/waves/round-59/span_tools.py check S426`. Several quotations stop at an inline-code or link boundary rather than closing their sentence: step one and step three end before the `host` token, step two before its three domain tokens, the user-triggered sentences before their linked example name and their JSON file-name token, and the two method sentences begin after their printed labels. No sentence is joined across nodes anywhere in this entry. The three example blocks are not marked as quotations because their lines fall below the 6-unit quotation floor; they are reproduced from the page's own `pre` text, whose characters are article-block text. Inline-code tokens (the command name, the three domain names, the masks, the JSON file names of the description cells) and link labels (`Apps Scripts`, `CIDR format`, the JSON file names of the IP-range cells) are named in backticks for the same reason. The printed revision line sits inside `devsite-content-footer`, outside the article block, so it is reported in the header and the anchor cell and is not quoted here.

Scope note: this entry records what the operator's page states, and nothing more; no crawl was observed and no Google behaviour was measured.
