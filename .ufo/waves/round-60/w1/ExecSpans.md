# ExecSpans

Claim C3 span inventory (round-60 w1). All counts measured by `spans.py` against the retained bodies
`sources/S427.html`, `S428.html`, `S429.html` (sha256-verified against `sources/receipts.json` on every read).

## TOOL:

`.ufo/waves/round-60/w1/ExecSpans.files/spans.py` — stdlib, self-contained port of the round-59 counter's
version-2 text-node code (carried verbatim from `c59_quote_truth.py`: `units`, `content_window`,
`text_segments` incl. `<style>/<script>/<aside>/<nav>/<devsite-feedback>/<devsite-thumb-rating>` blanking,
`in_content`, CJK unit rule, UNIT_CEILING 25, CHAR_CEILING 160, body collapse `re.sub(r"\s+"," ", raw)`).
Bodies keyed to `ExecSpans.files/../../sources/` = `.ufo/waves/round-60/sources/`; sha256 of each file is
checked against the frozen receipt digests before parsing, so body drift fails loudly.

- `python3 -B spans.py nodes S427|S428|S429` — every collapsed article-block text node, units, chars, page-unique.
- `python3 -B spans.py check <id> '<span>'` — units, chars, in_text_node, in_article_window, count_in_body,
  count in the two other bodies, unique, node_uniques, within_ceilings, no_curly_quotes.
- `python3 -B spans.py window <id> '<word>'` — all nodes containing the word, with context fallback.

S429 verification (flagged in item): it is a Search Central page but carries the same devsite chrome —
`class="devsite-article-body` exactly once at offset 137194 and `<devsite-content-footer` once after it at
147029 (of 178625 B); `content_window`/`text_segments` extract it unchanged. S427 offset 32092/45212
(74305 B), S428 32226/46928 (76025 B). All three: one article block, one footer marker. No per-id marker
override needed; the dicts exist if w2 ever sees a variant.

Units = CJK chars + non-CJK whitespace tokens. Unique = `count_in_body == 1` over the whole collapsed body
(round-59 rule: uniqueness is page-wide, not node-wide). Apostrophes in these bodies are straight ASCII
(`'`, e.g. `it's`, `user's` — shown as `no_curly_quotes: true` where a span holds one).

## SPANS:

Sentences that state a robots.txt posture/limit, per body (u = units, c = chars, uniq = page-unique;
yes = quoteable as-is, all checks pass: 6..25 u, <=160 c, single-node substring, page-unique):

**S427** (overview page; scope = common + special-case crawlers only, NO posture stated for user-triggered fetchers):
- `Google's clients fall into three categories:` 6u 44c uniq=yes
- `They always respect robots.txt rules for automatic crawls.` 8u 58c uniq=yes — carries `automatic crawls`
  (contract C5 subject for the S427 Gate quote). Node is `). They always ...` — the leading `).` is not needed.
- `Special-case crawlers are similar to common crawlers` 7u 52c uniq=yes (opening of the 31u definition node;
  full node too long)
- `ignores the global robots.txt user agent (` 7u 42c uniq=yes — AdsBot clause fragment (see TRAPS)
- `) with the ad publisher's permission.` 6u 37c uniq=yes — legal but ugly fragment
- `AdsBot` 1u — under floor, cannot carry a quote alone; `AdsBot` occurs once in the whole body
- `User-triggered fetchers are part of tools and product functions` 9u 63c uniq=yes (category definition only)

**S428** (user-triggered fetchers page):
- `User-triggered fetchers are initiated by users to perform a fetching function within a Google product.` 15u 102c uniq=yes — definition
- `a site hosted on Google Cloud (GCP) has a feature that allows the site's users to retrieve an external RSS feed.` 21u 112c uniq=yes (the `acts on a user's request,` prefix is 26u — too long)
- `Because the fetch was requested by a user, these fetchers generally ignore robots.txt rules.` 14u 92c uniq=yes — THE posture sentence; carries `generally ignore` (contract C5 subject)
- `these fetchers generally ignore robots.txt rules` 6u 48c uniq=yes — tight alternate
- `of Google's crawlers also apply to the user-triggered fetchers.` 9u 63c uniq=yes — ends the split paragraph
- `The IP ranges the user-triggered fetchers use are published in the` 11u 66c uniq=yes — fragment; full sentence split (see TRAPS)
- `***-***-***-***.gae.googleusercontent.com` 1u 41c uniq=yes — GAE reverse-DNS mask, under floor alone
- `google-proxy-***-***-***-***.google.com` 1u 39c uniq=yes — Google-owned mask, under floor alone
- `The user-triggered fetchers' reverse DNS mask, depending on whether the fetcher is Google or user owned, matches` 17u 112c uniq=yes — hostname context
- `user-triggered-fetchers.json` 1u NOT unique (2 occurrences); `user-triggered-agents.json` 1u NOT unique (4 occurrences, 2 nodes)
- `The following list shows the user-triggered fetchers, their user agent strings` 11u 78c uniq=yes
- `Feedfetcher is used for crawling RSS or Atom feeds for Google News and WebSub.` 14u 78c uniq=yes
- `Google Site Verifier fetches Search Console verification tokens.` 8u 64c uniq=yes

**S429** (robots.txt intro, Search Central):
- `A robots.txt file tells search engine crawlers which URLs the crawler can access on your site.` 16u 94c uniq=yes
- `it is not a mechanism for keeping a web page out of Google` 13u 58c uniq=yes — split sentence, see TRAPS
- `A robots.txt file is used primarily to manage crawler traffic to your site, and` 14u 79c uniq=yes
- `robots.txt rules may not be supported by all search engines.` 10u 60c uniq=yes (list-item node)
- `The instructions in robots.txt files cannot enforce crawler behavior to your site; it's up to the crawler to obey them.` 20u 119c uniq=yes — carries `cannot enforce` (contract C5 subject)
- `While Googlebot and other respectable web crawlers obey the instructions in a robots.txt file, other crawlers might not.` 18u 120c uniq=yes
- `Different crawlers interpret syntax differently.` 5u 48c — under floor
- `Although respectable web crawlers follow the rules in a robots.txt file, each crawler might interpret the rules differently.` 18u 124c uniq=yes — carries `interpret`
- `A page that's disallowed in robots.txt can still be indexed if linked to from other sites.` 16u 90c uniq=yes — carries `indexed` (heading node, page-unique)
- `While Google won't crawl or index the content blocked by a robots.txt file, we might still find and index a disallowed URL` 22u 122c uniq=yes
- `might still find and index a disallowed URL if it is linked from other places on the web` 18u 88c uniq=yes
- `Before you create or edit a robots.txt file, you should know the limits of this URL blocking method.` 18u 100c uniq=yes
- `Understand the limitations of a robots.txt file` 7u NOT unique (heading appears twice in body — TOC + h2)
- `How Google interprets the robots.txt specification` 6u NOT unique (twice in body)

## MULTI-NODE TRAPS:

Spans that look quotable but are NOT substrings of any single text node (`in_text_node: false`, `count_in_body: 0`):

- **S427 AdsBot sentence** — `For example, AdsBot ignores the global robots.txt user agent ( * ) with the ad
  publisher's permission.` spans 5 nodes: the `For example,` tail of the 31u Special-case definition, `AdsBot`,
  `ignores the global robots.txt user agent (`, `*`, `) with the ad publisher's permission.`. No 6..25u contiguous
  node-substring names AdsBot; best legal fragments end at `user agent (` or start at `)`. The sentence CANNOT be
  quoted whole — flag for entry prose (describe it, don't quote it).
- **S428 paragraph tail** — `... robots.txt rules. The general technical properties of Google's crawlers also apply
  to the user-triggered fetchers.` — `The general` closes one node and `technical properties` opens the next (a
  link); a quote may not run past `rules.` into `The general technical properties`. The `technical properties` link
  node also breaks the sentence `The general technical properties ... apply`.
- **S428 IP-ranges sentence** — `The IP ranges the user-triggered fetchers use are published in the
  user-triggered-fetchers.json , user-triggered-fetchers-google.json , and user-triggered-agents.json objects.` —
  the three `.json` filenames are each their own link node; no node holds the full sentence.
- **S428 reverse-DNS sentence** — `...matches ***-gae... or google-proxy-... respectively.` splits across 4 nodes
  (sentence, mask, `or`, mask, `respectively.`); `google-proxy-***-***-***-***.google.com or` count=0.
- **S429 opening definition** — `This is used mainly to avoid overloading your site with requests; it is not a
  mechanism ...` splits at the `;`: `it is not a mechanism...` is its own node (still quotable, 13u).
- **S429 `block indexing` sentence** — `. To keep a web page out of Google, block indexing with noindex or
  password-protect the page.` is 3 nodes (`block indexing with`, `noindex`, `or password-protect the page.`).
- **S429 interpret sentence tail** — `You should know the proper syntax for addressing different web crawlers as
  some might not understand certain instructions.` — `proper syntax` is a link node; count=0.
- **S429 blocking-methods tail** — `...it's better to use other blocking methods, such as password-protecting
  private files on your server.` — `password-protecting private files on your server` is a link node; a quote must
  stop at `such as`.

VERDICT: spans.py built and verified against all three bodies (S429 markers confirmed); 24 quoteable page-unique spans inventoried incl. all three C5 subject carriers (S427 automatic crawls, S428 generally ignore, S429 cannot enforce); 8 multi-node traps mapped, AdsBot sentence has no legal whole-sentence quote.
