source: S452 — MDN, X-Robots-Tag header — https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Robots-Tag — Syntax lines 154-159, Directives 160-215, Description 216-223, Multiple headers 234-239, Specifying user agents 240-256, Specifications 257-258 of `.ufo/waves/round-79/sources/S452-mdn-x-robots-tag.txt` (302 lines, 17,936 B, sha256 8be2a4062ecee6ec671eb6cf0aab28a066a6042b8caec7feedc96d939482556e; raw body 218,816 B, sha256 c4216ffb7aa934e309329d3b5adf1e62557464eebcbaab0bb33b60a72b7aaf38, fetched 2026-11-04T09:39:04Z, HTTP 200); S449 — Google Search Central, Robots meta tag, data-nosnippet, and X-Robots-Tag specifications — https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag — §Using the X-Robots-Tag HTTP header lines 974-1018, §Valid indexing and serving rules 1020-1213, §Reference of historical and other unused rules 1215-1236, §Handling combined indexing and serving rules 1238-1265 of `.ufo/waves/round-79/w1/ScoutSources/google-robots-meta.txt` (text sha256 b6728f0c73460c78bb2fdc240b14e4538f59f36ab62ba0c230a360bf3fdb1df8, byte-identical to the copy the S449 row retains at `.ufo/waves/round-78/w1/ScoutSources/`; the round-79 re-fetch's raw body hash is 98d97ba2c3a70caee9179659d48ee4d0c4e43c703c91aca7fa81f7d318d89ba5, the extracted text unchanged)
verified-at: 2026-11-04 — every quote below was re-located in the retained bytes by `.ufo/waves/round-79/w1/ScribeKnowledge/verify_quotes.py` (47/47, `quote-receipts.json`); no fresh network read by this seat
recheck: 90d for S452 and S449; MDN is a living page, so re-locate quotes and both hashes when it changes
ground: operability — the offline X-Robots-Tag declaration audit (round-79 C2)
terms: contract §"C2 tool interface (frozen)" as amended by `.ufo/waves/round-79/contract-amendment-1.md` (landed `43e0a9b7`, before any after-state): A1 adds `noarchive` to the known names as a value-less directive grounded in S449's historical section, claiming no current Google effect; A2 pins `none`/`all`/`index`/`follow` normalization
scope: declarations carried in recorded HTTP response header fields; not crawler behaviour, robots.txt outcomes, rendering, or any live property's state

# X-Robots-Tag — what a response header declares, and what an offline audit can decide

## The declaration channel

The header is a declaration page-level rules can also carry, chosen when the resource is not HTML or
the host can set response headers. MDN's definition sentence is the entry's Gate quote: "The
X-Robots-Tag response header defines how crawlers should index URLs." (`S452:136`, 10 units). It is
not a specification — "While not part of any specification, it is a de-facto standard method for
communicating with search bots, web crawlers, and similar user agents." (`S452:137`, 23 units) and
"Not part of any current specification." (`S452:258`, 6 units) — so nothing here is a standards
conformance claim.

| Fact | Source / retained file:line | Exact quote | Units |
|---|---|---|---|
| The header is for resources HTML rules cannot reach | S452 `S452-mdn-x-robots-tag.txt:140` | Specifying indexing rules in an HTTP header is useful for non-HTML documents like images, PDFs, or other media. | 18 |
| The vocabulary is the meta vocabulary | S449 `google-robots-meta.txt:977-978` | Any rule that can be used in a robots meta tag can also be specified as an X-Robots-Tag. | 18 |
| Only cooperative robots act on it | S452 `S452-mdn-x-robots-tag.txt:142` | Only cooperative robots follow these rules | 6 |
| Reading it costs a fetch | S452 `S452-mdn-x-robots-tag.txt:142` | a crawler first needs to access the resource to read headers and meta elements | 14 |
| A robots.txt block hides the header from the crawler | S452 `S452-mdn-x-robots-tag.txt:221` | Indexing rules won't be discovered or applied if paths are blocked from being crawled by a robots.txt file. | 18 |
| A rule takes effect on a later visit | S452 `S452-mdn-x-robots-tag.txt:227` | a robot must first revisit the page to detect the X-Robots-Tag rule. | 12 |

The last three rows matter for any audit: an audit of *declarations* reads what the response says, not
what any crawler does with it. S449 adds that Google documents its own processing of the header
(lines 974-1018), which is documentation of a policy, not an observation of a crawl.

## Grammar

### Field values, multiple lines and rule lists

A field value is one rule or a comma-separated list: the syntax block prints
`X-Robots-Tag: <indexing-rule>` and `X-Robots-Tag: <indexing-rule>, …, <indexing-ruleN>`
(`S452:154-155`), and "The following response has two X-Robots-Tag headers, each with an indexing rule
specified" (`S452:235`, 13 units). The two carriers are interchangeable in the page's own example:
"In the response below, the same indexing rules are defined, but in a single header." (`S452:247`,
15 units). S449 states the same for its side: "Multiple X-Robots-Tag headers can be combined within the
HTTP response, or you can specify a comma-separated list of rules." (`google-robots-meta.txt:987-988`,
19 units).

### The optional bot scope

The scope is one clause: "An optional <bot-name>: specifies the user agent that the subsequent rules
should apply to" (`S452:156`, 14 units; the angle-bracket token is the page's own) — this is the S452
SOURCES row's Gate quote. Two forms are
printed, one with the scope first and one with it after a global rule (`S452:157-158`), and the prose
adds "It's possible to specify which user agent the rules should apply to." (`S452:241`, 12 units) with
"Each indexing rule applies to the user agent specified behind it" (`S452:248`, 11 units). S449 says
the same in different words: "The X-Robots-Tag may optionally specify a user agent before the rules."
(`google-robots-meta.txt:1000-1001`, 11 units) and "Rules specified without a user agent are valid for
all crawlers." (`google-robots-meta.txt:1012`, 11 units) — the second sentence is what makes an
unprefixed field a *global* declaration.

The header name, the agent name and the values are case-insensitive for Google: "The HTTP header, the
user agent name, and the specified values are not case sensitive." (`google-robots-meta.txt:1012-1013`,
15 units). S452 itself only shows lowercase examples, so the case rule is sourced from S449.

### Directive vocabulary and value forms

S452's list has twelve entries. Value-less: `all`, `noindex`, `nofollow`, `none`, `nosnippet`,
`indexifembedded`, `notranslate`, `noimageindex` (`S452:162-208`). Value-bearing: `max-snippet:
<number>`, `max-image-preview: <setting>`, `max-video-preview: <number>`, `unavailable_after:
<date/time>` (`S452:181-215`).

| Rule | Source / retained file:line | Exact quote | Units |
|---|---|---|---|
| `all` is the default and adds nothing | S452 `S452-mdn-x-robots-tag.txt:164` | This rule is the default value and has no effect if explicitly listed. | 13 |
| `none` is the negative pair | S452 `S452-mdn-x-robots-tag.txt:172` | Equivalent to noindex, nofollow | 4 |
| `noindex` | S452 `S452-mdn-x-robots-tag.txt:166` | Do not show this page, media, or resource in search results. | 11 |
| `nofollow` | S452 `S452-mdn-x-robots-tag.txt:169` | Do not follow the links on this page. | 8 |
| `nosnippet` | S452 `S452-mdn-x-robots-tag.txt:174` | Do not show a text snippet or video preview in the search results for this page. | 16 |
| `noimageindex` | S452 `S452-mdn-x-robots-tag.txt:207` | Do not index images on this page. | 7 |
| `notranslate` | S452 `S452-mdn-x-robots-tag.txt:204` | Don't offer translation of this page in search results. | 9 |
| `indexifembedded` is conditional | S452 `S452-mdn-x-robots-tag.txt:180` | indexifembedded only has an effect if it's accompanied by noindex | 10 |
| Malformed numbers are ignored | S452 `S452-mdn-x-robots-tag.txt:183` | Ignored if no valid \<number\> is specified. | 7 |
| Image preview values | S452 `S452-mdn-x-robots-tag.txt:187` | specify a max-image-preview value of standard or none | 8 |
| Image preview `large` | S452 `S452-mdn-x-robots-tag.txt:193` | A larger image preview, up to the width of the viewport, may be shown. | 14 |
| Video `0` | S452 `S452-mdn-x-robots-tag.txt:200` | At most, a static image may be used, in accordance to the max-image-preview setting. | 14 |
| Video `-1` | S452 `S452-mdn-x-robots-tag.txt:202` | No video length limit. | 4 |
| Date families | S449 `google-robots-meta.txt:1201-1204` | must be specified in a widely adopted format including, but not limited to RFC 822, RFC 850, and ISO 8601 | 20 |
| Invalid dates are ignored | S452 `S452-mdn-x-robots-tag.txt:211` | Ignored if no valid \<date/time\> is specified. | 7 |
| Post-expiry crawl rate | S452 `S452-mdn-x-robots-tag.txt:215` | Crawlers are expected to considerably decrease the crawl rate of the URL after the specified date and time. | 18 |

`unavailable_after`'s date sentence reads "A date must be specified in a format such as RFC 822"
(`S452:212`, 12 units), whose other named examples are RFC 850 and ISO 8601; the link boundaries in
that line put spaces before the commas, so the clean full sentence is quoted from S449 above. Neither
page binds the value to RFC 3339: the lane's date grammar is a selected union (ISO 8601 date or
date-time, an RFC-822-shaped form, an RFC-850-shaped form), not a source requirement.

`index` and `follow` are *not* in S452's directive list. They appear only in the mutual-exclusion
sentence (`S452:222`), which is why the lane treats them as declared positive tokens rather than
listed directives. `noarchive` does not appear on the page at all: the lane admits it as a value-less
directive from S449's historical section under contract amendment 1 A1, where it is labelled
historical and no current Google effect is claimed (see the cross-check below).

### Conflicts and combination

S452's conflict sentence (`S452:219`, 33 units) is longer than the lane's 25-unit quote ceiling, so
only its decisive fragment is quoted: "the more restrictive rule applies." (5 units). S449 prints the
short form verbatim: "In the case of conflicting robots rules, the more restrictive rule applies."
(`google-robots-meta.txt:1015-1016`, 12 units). The worked example is "For example, if a page has both
max-snippet:50 and nosnippet rules, the nosnippet rule will apply." (`S452:220`, 16 units).

Two conflicting values of a positive/negative pair are legal declarations with an undefined consumer
result: "Some values are mutually exclusive" (`S452:222`, 5 units), with `index`/`noindex` and
`follow`/`nofollow` named as the page's examples, and "In these cases, the crawler's behavior is
undefined and may vary." (`S452:223`, 11 units). For several crawlers, "For situations where multiple
crawlers are specified along with different rules, the search engine will use the sum of the negative
rules." (`S452:252`, 22 units), as in "The page containing these headers will be interpreted as having
a noindex, nofollow rule when crawled by googlebot" (`S452:256`, 17 units).

## Lane readings

These are the lane's readings; the pages do not state them, and the round contract freezes them.

- **Directive-name precedence over the bot prefix.** A prefix is read as a bot scope only when its
  lowercased form is not a known directive name. The need is visible in S452's own syntax: four
  directives are written with a colon (`max-snippet:`, `max-image-preview:`, `max-video-preview:`,
  `unavailable_after:`), so `^[A-Za-z0-9_-]+:` alone cannot separate a bot from a value-bearing
  directive. Consequences: `max-snippet:50` is a directive, never a scope for a bot named
  `max-snippet`; a bot literally named `nosnippet` cannot be scoped; `all: noindex` is a value on a
  value-less directive, not a bot named `all`. [INFERENCE] Neither page settles this.
- **Scope stays inside one field value.** S452 says the scope binds "the subsequent rules" and prints
  every bot example inside a single field value; S449 says an unprefixed rule is valid for all
  crawlers, so an unprefixed field is global. No opened source says whether a trailing prefix binds a
  *following* field line. The lane reads the scope as confined to the field value it appears in and
  treats a new prefix as replacing the previous one in that value. [INFERENCE]
- **Per-bot effective resolution is out of scope.** S452's "sum of the negative rules" sentence says a
  search engine combines a crawler's own rules with the global ones. The round's audit reports the
  global set and each bot's declared set separately (`effective` is the global restriction set only);
  it never unions them and never answers what one agent would see. This is a stated limit, not a
  source claim.
- **Effective set and duplicate collapse are composition.** `none` is replaced by `noindex` and
  `nofollow` and is not itself kept, and `all` contributes nothing (amendment 1 A2); positives
  (`all`, `index`, `follow`) leave `effective`, while `index`/`follow` stay in `directives`;
  `nosnippet` suppresses numeric snippet/video limits, following the page's own example;
  a repeated value-bearing directive is reported and the numeric minimum is kept. The minimum is not
  always the more restrictive choice — `max-video-preview:-1` means "No video length limit"
  (`S452:202`) and `max-snippet:-1` delegates the length (S449 line 1104-1105) — so a `-1` beside a
  concrete bound collapses to the *least* restrictive value while the page's principle is the more
  restrictive rule. No frozen case pins that combination; it is a contract edge, not a sourced
  precedence rule. [INFERENCE]
- **Finding ids, exit codes and set ordering are policy.** `xrt_empty_rule`, `xrt_bot_scope_empty`,
  `xrt_unknown_directive`, `xrt_invalid_value`, `xrt_mutually_exclusive`,
  `xrt_indexifembedded_without_noindex`, `xrt_duplicate_directive` and the five input-fault ids,
  exits 0/1/2/64, and sorted unique output are the contract's terms. No source defines them.

## What the round's tool demonstrates, and what it does not

The round lands `scripts/x_robots_tag_audit.py` (contract `.ufo/waves/round-79/contract.md` §"C2 tool
interface (frozen)"). It reads a version-1 manifest of recorded response header fields plus URLs,
read-only and network-free, and decides per check: the declared global directive tokens, the global
effective restriction set, the per-bot declared sets, and a sorted unique finding list; exit 0 clean,
1 findings, 2 input fault, 64 usage.

The frozen 31-case set exercises these decision classes (cases under `.ufo/waves/round-79/cases/`,
oracle at `.ufo/waves/round-79/expect/expect.json`):

| Class | Cases |
|---|---|
| Clean global declarations, including field-line combination and a case-varied header name | c01-c04, c07, c19, c30 |
| Bot scoping: one bot, a global rule plus a bot rule, two bots in one value | c05, c06, c28, c29 |
| Normalization: `none` expansion, image-preview case folding | c03, c27 |
| Value validation: numeric, enum and ISO date-time forms | c13-c17 |
| Duplicate and exclusive pairs | c09, c10, c21 |
| Malformed rules: empty segment, unknown name, empty bot scope | c11, c12, c18 |
| Input faults: duplicate id, bad check shape, bad JSON, wrong schema version | c22-c25 |
| A non-`X-Robots-Tag` field is ignored | c31 |
| A historical token (`noarchive`), admitted by amendment 1 A1 | c26 |

It does **not** fetch anything, observe any crawler, union per-bot rules with the global set, compare
the meta and header carriers, follow redirect hops, model robots.txt outcomes, validate numeric bounds
beyond syntax, or evaluate `indexifembedded`'s conditional effect. No matrix result is claimed in this
entry: the round's measurement belongs to the C2 receipt, and this seat ran none.

## Cross-checks: S452 against S449

S452 (tier B) and S449 (tier A for Google's own processing) agree on the restrictive-conflict rule,
the `none` expansion, `all` as the no-restriction default, and the negative-rule sum example. Where
they differ or one is narrower:

- **`noarchive`.** S452's directive list never names it. S449 places it among the rules that "aren't
  used by Google Search and are ignored" (`google-robots-meta.txt:1217`, 11 units) and says "The
  noarchive rule is no longer used by Google Search" (`google-robots-meta.txt:1225`, 10 units). So the
  header page omits a token the meta page lists as historical; neither page makes it operative. The
  lane admits it as a value-less directive under contract amendment 1 A1, grounded in that historical
  section and claiming no current Google effect; frozen case c26 pins the admission.
- **Date-family wording.** S452 says "A date must be specified in a format such as RFC 822"
  (`S452:212`, 12 units); S449 says "widely adopted format including, but not limited to" the same
  three families (quoted above). Both are open-ended; neither restricts the value to date-times, and
  S452 says "date", which is why a date-only ISO value is inside the lane's grammar.
- **Examples that the frozen date shapes do not all accept.** S452's own header example is
  `unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT` (`S452:239`), which fits the lane's RFC-822-shaped
  branch. S449's header example is `X-Robots-Tag: unavailable_after: 25 Jun 2010 15:00:00 PST`
  (`google-robots-meta.txt:997`, 7 units) — no weekday and a named zone — which the same branch
  rejects. That is a limit of the lane grammar (both pages call the value valid), not a statement
  about any crawler.
- **Registry-scope precision.** The S449 row's scope cell says "not header processing". The page does
  carry header sections (lines 974-1018 and 1336-1396); the cell records what round 78 mined, not what
  the source contains. This entry quotes those sections without changing the held row.

## Limits

- **No fetch, no live property.** Everything is read from the two retained files above; no URL was
  requested by this seat, and no serving host is described.
- **No crawler behaviour.** "Only cooperative robots follow these rules" (`S452:142`); the pages
  state intentions and policies, and no crawl, indexing or serving outcome is established here.
- **Not a specification.** The header is a de-facto convention with no normative document
  (`S452:137`, `S452:258`); vocabulary and grammar are publisher-facing documentation.
- **Precedence and per-field scope are lane readings.** Both are marked [INFERENCE]; a primary source
  that fixes bot/rule disambiguation or cross-field scope would supersede them.
- **Bounded date shapes.** ISO 8601 (date or date-time), one RFC-822-shaped form with `GMT`, one
  RFC-850-shaped form; RFC 822's wider grammar and named zones are not implemented, and S449's own
  `PST` example is rejected. The sibling round-78 instrument still rejects RFC 850 for `meta`
  (`corpus/knowledge/meta-robots-directives.md` §Limits) while this round's grammar accepts it — a
  lane-policy difference between two instruments, not a source difference.
- **No cross-carrier audit.** S452 states the meta/header conflict rule; the instrument reads one
  carrier per check and cannot decide a combined declaration.
- **Quote ceiling.** The full S452 conflict sentence is 33 units, over the lane's 25-unit quote
  ceiling; it is paraphrased and its decisive fragment quoted.
- **Price of the source.** MDN is a living page: the row's recheck is 90 days, and both raw and
  extracted-text hashes are recorded so a later change is detectable rather than assumed.
