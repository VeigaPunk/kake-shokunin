# ScoutSources — round 79, wave w1

**Verdict:** all three candidates opened once, retained raw + stripped, 41 quotes located and verified
(`quotes=41 failures=0`); **S452 (MDN, tier B) is admissible and its five required sentences are located**
(the row landed at `corpus/SOURCES.md:199` while this seat ran, against the same 218,816-byte raw);
**RFC 9309 is rejected for the header carrier** (0 case-insensitive occurrences of `X-Robots-Tag`, 25,265
bytes) with a flip; a **second row on S449's Google URL is mechanically admissible** (census W04 only, no
E04, exit unchanged — measured) because it is the only source of three header statements the C2 grammar
leans on (plus a differently worded non-HTML rationale), but it is **outside the frozen terms and deferred**, not written. No registry row covered the header
carrier at the base. Five items routed to the L1: the contract's claim that RFC 822/850 date branches are
"pinned by cases" is **not** true of the frozen case set; S449's raw-byte anchor is stale while its prose is
unchanged; Google's own `unavailable_after` example falls outside the frozen date grammar; and the landed
S452 teaches cell attributes one Google sentence to MDN.

## 1. Fetches (observed 2026-11-04T09:48:47Z)

One GET per source, run from the seat scratch dir:

```sh
curl -sSL --max-time 30 -o <name>.raw -w '%{http_code} %{url_effective} %{size_download}' <url>
```

| # | requested URL | HTTP | final URL | bytes | raw sha256 | retained |
|---|---|---|---|---|---|---|
| 1 | `https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Robots-Tag` | 200 | same (no redirect) | 218,816 | `c4216ffb7aa934e309329d3b5adf1e62557464eebcbaab0bb33b60a72b7aaf38` | `mdn-x-robots-tag.raw` |
| 2 | `https://www.rfc-editor.org/rfc/rfc9309.txt` | 200 | same | 25,265 | `f633915daaa15b943cae56545d333bcf3ba4d156599e4555499686d6699fb207` | `rfc9309.raw` |
| 3 | `https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag` | 200 | same | 208,191 | `98d97ba2c3a70caee9179659d48ee4d0c4e43c703c91aca7fa81f7d318d89ba5` | `google-robots-meta.raw` |

All retained under `.ufo/waves/round-79/w1/ScoutSources/`. `curl` exit 0 for each. `-w` fields are
`http_code url_effective size_download`; the final URL equals the requested URL in all three cases.

## 2. Strip recipe and text hashes

`strip.py` is round-78's recipe (itself round-77's) with the block-tag set extended by
`</section> </main> </article> </header> </footer>`; the docstring is the recipe. HTML: drop
`<script>`/`<style>` and `<head>`, newline for block ends and `<br>`, `- ` before `<li>`, remove remaining
tags, `html.unescape`, NBSP→space, collapse `[ \t]+`, strip lines, collapse blank runs. RFC text: CRLF→LF,
`\f`→newline, drop `[Page N]` footers and `RFC NNNN … Month YYYY` headers, per-line tidy.

`python3 -B strip.py | tee strip-output.txt` — **exit 0** (`strip-output.txt`,
sha256 `7d40a23207c4d7e52b7695dcb11d85eb05d9bdd6c2f056cbf5a7eab97e21b48f`).

| source | raw bytes | stripped bytes | lines | stripped sha256 |
|---|---|---|---|---|
| `mdn-x-robots-tag` | 218,816 | 19,088 | 1,459 | `ef7609cbcf9776d0baa1eb3841236112ccf6944a4dabf489eee414aa886921a3` |
| `google-robots-meta` | 208,191 | 27,619 | 1,594 | `b6728f0c73460c78bb2fdc240b14e4538f59f36ab62ba0c230a360bf3fdb1df8` |
| `rfc9309` | 25,265 | 21,030 | 601 | `70575ff274625daf97ce43c39bfc5e186f6824fbf2c3d943d9fd9d6e70532aa7` |

`verify_quotes.py` and `receipts.py` are round-78's matchers (inline tags skipped, entities decoded,
whitespace collapsed, each emitted character carried back to its raw byte span). `quotes.json` holds the 41
quotes; `verify-output.txt` (**exit 0**, `quotes=41 failures=0`), `receipts-output.txt` (**exit 0**,
`receipts=41 without_txt=0`), `quote-receipts.json`. No prose sentence is byte-contiguous in any of the
three raws (wrapping, indentation, inline `<code>`/`<a>`); every quote is an exact character rendering and
its raw span is recorded.

## 3. The five required locations (all in `mdn-x-robots-tag.txt`, 1-based lines)

| ask | located sentence | quote id | line(s) | raw bytes |
|---|---|---|---|---|
| header definition | "The X-Robots-Tag response header defines how crawlers should index URLs." | `M-definition` | 366 | 86510..86706 |
| its spec standing | "While not part of any specification, it is a de-facto standard method for communicating with search bots, web crawlers, and similar user agents." | `M-defacto` | 367 | 86707..86851 |
| optional `<bot-name>:` scope | "An optional <bot-name>: specifies the user agent that the subsequent rules should apply to:" | `M-botname` | 406 | 89846..89956 |
| the scope binds later rules of the same field | "Each indexing rule applies to the user agent specified behind it:" | `M-scope-persists` | 559 | 100737..100802 |
| the same, shown in one field value | "X-Robots-Tag: BadBot: noindex, nofollow, googlebot: nofollow" | `M-example-two-bots` | 564 | 101001..101061 |
| conflict rule (header ↔ meta) | "In the case of conflicting robot rules within the X-Robots-Tag or between the X-Robots-Tag HTTP header and the <meta name=\"robots\"> element" + "the more restrictive rule applies." (one sentence, 26 words; split for the 25-word quote cap) | `M-conflict-scope`, `M-conflict-rule` | 512 | 96347..96531, 96533..96567 |
| multiple-header example | "The following response has two X-Robots-Tag headers, each with an indexing rule specified:" with the two example lines `X-Robots-Tag: noimageindex` and `X-Robots-Tag: unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT` | `M-multiple-headers`, `M-example-noimageindex`, `M-example-unavailable` | 539, 544, 545 | 99309..99412, 99611..99637, 99638..99700 |
| comma form and bot form | "X-Robots-Tag: <indexing-rule>, …, <indexing-ruleN>" / "X-Robots-Tag: <bot-name>: <indexing-rule>, …, <indexing-ruleN>" | `M-syntax-comma`, `M-syntax-bot` | 404, 410 | 89760..89822, 90180..90260 |
| directive list boundary | "Any of the following indexing rules may be used:" | `M-directives-intro` | 416 | 90645..90693 |
| `none` expansion | "Equivalent to noindex, nofollow." | `M-none` | 435 | 91414..91459 |
| `all` semantics | "No restrictions for indexing or serving in search results." + "This rule is the default value and has no effect if explicitly listed." | `M-all`, `M-all-default` | 420, 421 | 90765..90823, 90824..90894 |
| `indexifembedded` needs `noindex` | "indexifembedded only has an effect if it's accompanied by noindex." | `M-indexifembedded` | 447 | 92416..92502 |
| malformed numeric value | "Ignored if no valid <number> is specified." (twice: `max-snippet`, `max-video-preview`) | `M-number-invalid` | 452, 476 | 92730..92791, 94044..94105 |
| `max-image-preview` enum | "A larger image preview, up to the width of the viewport, may be shown." (after `none` 460-462 and `standard` 464-466) | `M-maximage-large` | 470 | 93574..93644 |
| `max-video-preview` `-1` | "No video length limit." | `M-maxvideo-minus1` | 485 | 94369..94391 |
| `unavailable_after` date families | "A date must be specified in a format such as RFC 822, RFC 850, or ISO 8601." | `M-dateform` | 501 | 95197..95538 |
| mutual exclusivity (the only place `index`/`follow` appear) | "Some values are mutually exclusive, such as index and noindex, or follow and nofollow." + "In these cases, the crawler's behavior is undefined and may vary." | `M-mutually-exclusive`, `M-undefined` | 516, 517 | 96834..96972, 96973..97038 |
| non-HTML rationale | "Specifying indexing rules in an HTTP header is useful for non-HTML documents like images, PDFs, or other media." | `M-nonhtml` | 371 | 87278..87389 |
| cooperative-only, not a crawler claim | "Only cooperative robots follow these rules, and a crawler first needs to access the resource to read headers and meta elements" | `M-cooperative` | 374 | 87448..87574 |
| per-bot merge (beyond the frozen grammar) | "For situations where multiple crawlers are specified along with different rules, the search engine will use the sum of the negative rules." | `M-sum-negative` | 566 | 101085..101223 |
| spec status, restated | "Not part of any current specification." | `M-not-spec` | 577 | 101900..101938 |
| page freshness | "This page was last modified on Aug 21, 2026 by MDN contributors." | `M-lastmod` | 602 | 126956..127152 |

## 4. Directive vocabulary cross-check

Directive entries on each page (a line that is exactly the name, or `name:` for value-bearing rules):

| name | MDN (`mdn-x-robots-tag.txt`) | Google (`google-robots-meta.txt`, S449's source) | in the C2 list (frozen + amendment 1 A1) |
|---|---|---|---|
| `all` | 418 | 1033 | yes |
| `noindex` | 423 | 1038 | yes |
| `nofollow` | 428 | 1046 | yes |
| `none` | 433 (also 460, the `max-image-preview` value) | 1052 | yes |
| `nosnippet` | 437 | 1056 | yes |
| `indexifembedded` | 444 | 1071 | yes |
| `max-snippet:` | 449 | 1081 | yes |
| `max-image-preview:` | 454 | 1123 | yes |
| `max-video-preview:` | 472 | 1158 | yes |
| `notranslate` | 487 | 1183 | yes |
| `noimageindex` | 492 | 1193 | yes |
| `unavailable_after:` | 497 | 1198 | yes |
| `index` | **absent** (0 headings) | **absent** (0 headings) | yes |
| `follow` | **absent** (0 headings) | **absent** (0 headings) | yes |
| `noarchive` | **absent** (0 hits) | 1223 (historical; "no longer used by Google Search" at 1225) | yes — amendment 1 A1 |
| `nocache` `nositelinkssearchbox` | absent (0 hits) | 1228, 1232 (historical) | no |

Commands: `grep -c -x 'index' mdn-x-robots-tag.txt` → `0` (exit 1), same for `follow`; `grep -c -x
'index' google-robots-meta.txt` → `0` (exit 1). `grep -c -i 'noarchive\|nocache\|nositelinkssearchbox'
mdn-x-robots-tag.txt` → `0` (exit 1).

Cross-check against S449's scope cell (`corpus/SOURCES.md:196`: "Page-level directive vocabulary,
case-insensitivity, conflicts and dates; not arbitrary unknown-content-token handling, **not header
processing**, not any live crawler observation"): the two pages agree on the twelve active names; MDN omits
the three historical Google names. The C2 list is the twelve **plus `index`, `follow` and — by
`contract-amendment-1.md` A1 — `noarchive`**. `index`/`follow` are listed as directives by neither page
(MDN names them only inside the exclusivity sentence, `:516`); `noarchive` appears nowhere on the
MDN page (0 hits) and only in Google's historical section, which is exactly the grounding A1 cites. So the C2
vocabulary is a superset of both sources by three names, each with a different provenance: two from
MDN's exclusivity sentence and Google's `all` semantics, one from S449's historical list alone.

## 5. Contract readings that no opened source states (reject rows, with flips)

Each row quotes the nearest actual sentence; none of these may be written into the S452 knowledge entry as
sourced.

| # | contract rule | nearest sentence (verbatim, located) | why it does not ground the rule | flip condition |
|---|---|---|---|---|
| R1 | bot-name charset `^[A-Za-z0-9_-]+$` | "An optional <bot-name>: specifies the user agent that the subsequent rules should apply to:" (`:406`) | The page gives a placeholder and two example names (`BadBot`, `googlebot`) and never states a name syntax or charset. | a source states a bot-name grammar. |
| R2 | a segment whose prefix is a known directive name is never a bot scope | — (nothing in either page) | Not stated. MDN's grammar puts the bot name first and the contract's precedence rule is a parsing choice. | a source shows a bot literally named like a directive, or states the precedence. |
| R3 | a bot scope does not cross field lines | "Each indexing rule applies to the user agent specified behind it:" (`:559`); two-header example `:555-556` | The syntax puts the bot name inside one field value and the examples never carry a scope across lines, but no sentence says scope is field-local. | a source says a bot scope applies to subsequent field lines. |
| R4 | unknown directive name → `xrt_unknown_directive`, contributes nothing | "Ignored if no valid <number> is specified." (`:452`); "Ignored if no valid <date/time> is specified." (`:500`) | Both "ignored" sentences are about **malformed values of known directives**. No sentence says an unknown rule name is ignored; Google's "aren't used by Google Search and are ignored" (S449 `:1217`) covers three **named** rules only. `grep -n -i 'unknown' mdn-x-robots-tag.txt` → 0 hits. | a source states unknown rule-name handling. |
| R5 | `index` and `follow` are known names kept as declared positive tokens | "Some values are mutually exclusive, such as index and noindex, or follow and nofollow." (`:516`) | They are named as values that can conflict, never as rules; `all` is defined as "No restrictions" (`:420`), not as a token pair. Amendment 1 A2 pins how the lane normalizes them, not that either page lists them. | a primary (e.g. Google's machine-readable rules file, not opened) lists `index`/`follow` as rules. |
| R6 | mutual exclusion is a **finding** (`xrt_mutually_exclusive`) | "In these cases, the crawler's behavior is undefined and may vary." (`:517`) | MDN calls such a declaration legal-but-ambiguous and says behaviour varies; a finding is a lane audit reading, not a source-mandated error. | a source says the declaration itself is invalid. |
| R7 | duplicate value-bearing directive in one scope → `xrt_duplicate_directive` | "For situations where multiple crawlers are specified along with different rules, the search engine will use the sum of the negative rules." (`:566`) | That sentence is about per-crawler merging, not about the same value directive twice in one scope; no sentence covers duplicate values. | a source states duplicate handling. |
| R8 | `nosnippet` present ⇒ drop `max-snippet:*`/`max-video-preview:*` from `effective` | "if a page has both max-snippet:50 and nosnippet rules, the nosnippet rule will apply" (`:513`) | The example grounds the *conflict*; mechanically deleting the max-* tokens from `effective` is a composition of the "more restrictive" rule with the `effective` definition. | a source enumerates the effective set per combination. |
| R9 | RFC 822/850 shapes narrowed to literal `GMT` and 2-digit day | "A date must be specified in a format such as RFC 822, RFC 850, or ISO 8601." (`:501`) | The page names families, not grammars; Google's own header example uses `unavailable_after: 25 Jun 2010 15:00:00 PST` (`google-robots-meta.txt:997`), which the frozen RFC 822 regex rejects (see §10 D3). | a source shows a non-GMT zone accepted, or the lane widens the matcher to RFC 822 zone syntax. |
| R10 | `effective` is global-only; per-bot resolution out of scope | "the search engine will use the sum of the negative rules" (`:566`) + the `googlebot` example (`:569-573`) | MDN **does** describe a per-bot merge; the exclusion is a stated lane limit, not source silence. The knowledge entry must say so. | the lane implements per-bot effective resolution. |
| R11 | the whole grammar is normative | "While not part of any specification, it is a de-facto standard" (`:367`); "Not part of any current specification." (`:577`) | Nobody owns the grammar; every rule in the C2 contract is a de-facto reading pinned by the lane, and S452 says so itself. | a specification (IETF/W3C) defines the field. |
| R12 | case-insensitive comparison of header name, bot name and values (ASCII) | Google: "The HTTP header, the user agent name, and the specified values are not case sensitive." (`google-robots-meta.txt:1012-1013`) — **not on MDN** (`grep -c -i sensitive mdn-x-robots-tag.txt` → `0`, exit 1) | Only the Google page says it, and S449's scope cell excludes header processing, so the sentence is outside the row that holds the bytes; "ASCII" is neither page's word. | a source states the case rule for the header carrier (see §6 for the second-row option). |
| R13 | exit alphabet 0/1/2/64, manifest schema, finding ids | — | Nothing in any opened source discusses an audit tool. | never (tool contract is lane policy by construction). |

## 6. Third candidate — second row on S449's Google URL: admissible, deferred

**Rule.** `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:25` defines `E04 duplicate URL+scope (no
supersedes)`; `:33` defines `W04 same URL across scopes (warnings do not affect clean lanes)`; the
implementation (`:641-650`) keys the duplicate on the literal pair `(url, scope cell)` and requires the
earlier non-rejected row for `E04`. A second row on the same URL with a **different** scope cell is
therefore a W04 warning, not an error.

**Precedent.** S433 (`corpus/SOURCES.md:179`) duplicates S010's `rfc9110.html` URL across scopes; S445
duplicates `links.html`; S099/S011 and S115/S116 are same-URL/different-scope pairs. All stand.

**Measured.** Appending the drafted deferred row to a scratch copy of the registry and running
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
--file <scratch>/SOURCES-r79-with-google.md` (exit 1, pre-existing E11s in `--file` mode against the fleet
root) adds **exactly one line** versus the two-row run and does not change the exit:

```
file	W04	S454 duplicate url developers.google.com/search/docs/crawling-indexing/robots-meta-tag across scopes
```

W04 count 19 → 20; no E04 appears.

**Substantively it is the only source of three contract statements (and a differently worded rationale).** MDN states none of the case
rule (R12), none of "rules without a user agent are valid for all crawlers" (`grep -c -i 'all crawlers'
mdn-x-robots-tag.txt` → `0`) and no multiple-header *combination* sentence (it shows two headers at `:539-545`
without saying they combine). MDN does carry its own non-HTML rationale (`:371`), but not Google's
imperative form. The Google page states the three missing things and the rationale: `:987-988` (multiple
headers or comma list), `:1000-1001` (optional user agent), `:1012` (no-agent rules valid for all crawlers),
`:1012-1013` (not case sensitive), `:971-972` (non-HTML).

**Decision.** Admissible; **not written this round.** The round's frozen contract admits S452 only, and C2's
frozen grammar does not need these sentences to decide any case — they are already pinned as lane readings.
The drafted row is retained as `row-deferred-google-xrt.txt` (validated: 11 cells, `duplicate=W04 across
scopes with ['S449']`, `check-rows-deferred-output.txt`, exit 0), for the L1 to admit in a later round or
not at all. If the L1 prefers no new row, the alternative is a disclosed old→new edit of S449's scope and
anchor (its anchor currently stops at `917-969`/`1015-1018` and never cites `971-1013`); either way the
knowledge entry must not attribute the case rule to S452.

## 7. Registry coverage of the header carrier

`grep -in 'x-robots-tag\|x robots' corpus/SOURCES.md` → **2 hits**, both non-carrier:

- `S449` (`:196`) — names `X-Robots-Tag` only in its title and its scope's exclusion ("not header
  processing"); its anchor (`Using the robots meta tag 917-969; conflicts 1015-1018; …`) omits `971-1013`.
- `S367` (`:157`) — Yahoo's own rule; its teaches cell says "the server-side equivalent is the
  `X-Robots-Tag: NOFOLLOW` header" for refusing crawl of a page's **link targets**. One operator sentence,
  no header grammar.

So **no row scopes the header carrier** at the base; S452 is a new URL and a new scope. Registry at the
base: 189 rows, last id `S451`, so `S452` was free (it matches the contract).

**It landed while this seat ran.** ScribeKnowledge's row is now `corpus/SOURCES.md:199` (row count 190):
`| S452 | MDN — X-Robots-Tag header | … |` with the **same raw sha256** `c4216ffb…aaf38`, 218,816 bytes,
fetched 2026-11-04T09:39:04Z (about ten minutes before my GET), against a different text rendering retained at
`.ufo/waves/round-79/sources/S452-mdn-x-robots-tag.txt` (302 lines, `8be2a406…556e`). Two tag-stripped
renderings of one raw body now exist in the lane (`302`-line and my `1,459`-line), so line citations differ
by rendering while the raw bytes agree; the definition sentence verifies in both. My drafted S452 row below
is therefore a **cross-check of a landed row, not an append target**; `S453` is still free for the reject.

## 8. Drafted rows and census effect

`rows-draft.txt` holds two rows, validated against the **base registry blob** (the copy taken for the census
runs, before S452 landed: `census-base.txt` has zero `S452` lines); `check_rows.py` (**exit 0**, `rows=2
failures=0`) verifies 11 non-empty cells, free ids, enums, opened `2026-11-04`, anchor sha256 **and** byte
count against the retained raw, a `REJECTED:`+`flip:` teaches cell for the rejected row, the knowledge path
for the mined row, and the duplicate rule.

```
S452: cells=11 kind=docs tier=B status=mined url=https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Robots-Tag duplicate=none OK
S453: cells=11 kind=spec tier=A status=rejected url=https://www.rfc-editor.org/rfc/rfc9309.txt duplicate=none OK
rows=2 failures=0
```

- **S452 = MDN (cross-check; the row landed at `corpus/SOURCES.md:199` while this seat ran).** My draft
  words the scope to what the page says and explicitly not what S449 owns; its teaches cell avoids claiming
  a specification (§5 R11) and states the per-bot limit (§5 R10), while the landed row's teaches adds the
  global-default sentence MDN does not state (§10 D5). Tier B, opened 2026-11-04, recheck 90d, used-by
  `corpus/knowledge/x-robots-tag-header.md`.
- **S453 = RFC 9309, reject.** Reason: 0 case-insensitive occurrences of `X-Robots-Tag` in 25,265 raw bytes
  and 601 stripped lines (`grep -c -i 'x-robots-tag' rfc9309.raw` → `0` exit 1; same for `.txt`), and §2.1
  defines the protocol as rules and groups "made available in a file named \"robots.txt\"" (`:111-112`).
  Flip: RFC 9309 or a successor defines an `X-Robots-Tag` field or any response-header indexing channel. The
  row's URL is the `.txt` form; S011/S099 hold the `.html` form, so no W04 is added.

Census on a scratch copy with both rows inserted before `## Paths`
(`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
--file <scratch>/SOURCES-r79.md`, exit 1 — pre-existing E11s of `--file`-mode against the fleet root):
**the only delta versus the same run on the unmodified registry is one expected line**

```
file	E11	S452 missing used-by corpus/knowledge/x-robots-tag-header.md
```

which was the only delta these rows added (the knowledge entry has since landed, so it is moot; the
measurement stands for the base blob). W04 count is **19 before and 19 after**, i.e. these two rows add no
duplicate-URL warning. (Baseline and drafted outputs: `census-base.txt`, `census-r79.txt`; counts via
`grep -c W04` → `19`, `19`; `grep -c S452 census-base.txt` → `0`.)

## 9. Mechanical checks (all run; nothing inferred)

| check | command | result |
|---|---|---|
| fetch ×3 | `curl -sSL --max-time 30 -o …` | exit 0 each; statuses/bytes/hashes §1 |
| strip | `python3 -B strip.py` | exit 0; three `.txt`, hashes §2 |
| quote location | `python3 -B verify_quotes.py` | **exit 0**, `quotes=41 failures=0`; every quote ≤25 words, no pipes, found in its `.txt` |
| quote receipts | `python3 -B receipts.py` | **exit 0**, `receipts=41 without_txt=0` |
| row shape | `python3 -B check_rows.py` | **exit 0**, `rows=2 failures=0` |
| deferred row shape | `python3 -B check_rows.py row-deferred-google-xrt.txt` | **exit 0**, `rows=1 failures=0`, `duplicate=W04 across scopes with ['S449']` |
| RFC 9309 header absence | `grep -c -i 'x-robots-tag' rfc9309.raw rfc9309.txt` | `0` and `0` (exit 1 each — no match) |
| MDN case rule absence | `grep -c -i sensitive mdn-x-robots-tag.txt` | `0` (exit 1) |
| MDN no-agent-rule absence | `grep -c -i 'all crawlers' mdn-x-robots-tag.txt` | `0` (exit 1) |
| `index`/`follow` not directives (both pages) | `grep -c -x 'index'`, `grep -c -x 'follow'` | `0`,`0` (MDN) and `0`,`0` (Google), exit 1 each |
| census base vs drafted | `sources-census.sh validate --root … --file …` | exit 1 both; delta = the single expected E11; W04 `19`→`19` |
| census with deferred row | same, third file | exit 1; delta vs drafted = one `W04 … S454 … across scopes`; W04 `19`→`20` |
| baseline predates S452 | `grep -c S452 census-base.txt` | `0` — the baseline copy does not contain the row that landed during the seat |

## 10. Routed findings (frozen artifacts are read-only; nothing below was edited)

**D1 — the contract's date-branch claim is not pinned by the case set.** Contract §Assumptions: "RFC
822/850 branches are pinned by cases, not by a general date library." The frozen case set contains exactly
two `unavailable_after` values, neither RFC 822 nor RFC 850:

```
$ grep -ri 'unavailable' .ufo/waves/round-79/cases/ | wc -l          # 2
cases/c16/manifest.json:  "value": "unavailable_after:2025-12-31T23:59:59Z"
cases/c17/manifest.json:  "value": "unavailable_after:tomorrow"
$ grep -c 'GMT' .ufo/waves/round-79/expect/expect.json               # 0
$ grep -rc 'PST' .ufo/waves/round-79/cases/ | grep -v ':0'           # no output: 0 hits in every file
```

Consequence: `correct=31` says nothing about the RFC 822 or RFC 850 regex branches; they are unexercised by
the matrix. Route to ReviewC2/ConnectorC; the fix would be a later case set, not an edit to this one.

**D2 — S449's raw anchor is stale; its prose is not.** Today's GET of S449's URL is 208,191 bytes /
`98d97ba2…`, while the row records `208195 bytes` / raw `d9fdfe42…96b5e`. `cmp -l` between
`.ufo/waves/round-78/w1/ScoutSources/google-robots-meta.raw` and the round-79 copy shows the first byte
difference at offset 51827, inside the site header's Search Console `<a>`: `data-category`/`data-label`
attribute order changed. The **stripped text is byte-identical** across the two days
(`b6728f0c73460c78bb2fdc240b14e4538f59f36ab62ba0c230a360bf3fdb1df8`), so every S449 quote still holds;
only the raw-byte anchor is out of date. Any census/freshness comparison of raw sha256 for S449 will flag
it. Also note S449's scope excludes header processing while its own bytes carry the header case rule
(`:1012-1013`) — see §6.

**D3 — Google's own `unavailable_after` example falls outside the frozen grammar.** `google-robots-meta.txt:997`
(the example the page prints for the header) is `X-Robots-Tag: unavailable_after: 25 Jun 2010 15:00:00 PST`.
The frozen RFC 822 shape requires literal ` GMT`, so that value would be `xrt_invalid_value`. No frozen case
uses a non-GMT zone, so no expectation is contradicted; the knowledge entry must state that the audit is
stricter than the example, and the tool author must not widen the regex without the L1 (§5 R9).

**D4 — MDN's two bot examples disagree in case** (`BadBot` at `:555`/`:564`, `googlebot` at `:556`/`:564`)
while nothing on MDN states a comparison rule; the contract's lowercase normalization rests on the Google
sentence at `:1012-1013`, which is outside S449's scope (§5 R12, §6).

**D5 — the landed S452 row's teaches cell attributes a Google sentence to MDN.** `corpus/SOURCES.md:199`
teaches: "rules combine across field lines and comma lists, **an unprefixed rule is global**, none expands to
noindex,nofollow, the more restrictive rule wins a conflict…". MDN never says the second clause: its
sentences are "An optional `<bot-name>:` specifies the user agent that the subsequent rules should apply to:"
(`mdn-x-robots-tag.txt:406`) and "Each indexing rule applies to the user agent specified behind it:"
(`:559`); `grep -c -i 'all crawlers' mdn-x-robots-tag.txt` → `0` (exit 1). The only sentence that says it is
Google's "Rules specified without a user agent are valid for all crawlers."
(`google-robots-meta.txt:1012`), which S449's scope excludes. Fix: either word it as the lane's reading of
MDN's syntax, or admit the deferred Google row (§6) / widen S449 and cite it. The knowledge entry itself
already does the right thing for the neighbouring case rule (it attributes it to S449 at
`corpus/knowledge/x-robots-tag-header.md:58-60`), so this is a row-cell attribution, not an entry defect.

## 11. Remaining unknowns

- Whether Google's machine-readable rules file (linked at `google-robots-meta.txt:1022-1024`, not opened this
  seat) lists `index` and `follow` as rules; if it does, R5 stops being a gap and R2/R7 could be sharpened.
- Whether any other crawler's primary source states an unknown-directive or bot-name grammar (Bing, Yandex,
  Apple were not opened).
- Whether the lane will admit the deferred Google header row (§6) or widen S449; both change which row the
  knowledge entry may cite for the case and global-default readings, and neither changes any frozen case.
- MDN's `<bot-name>` placeholder admits names the contract's charset rejects (e.g. a dotted version string);
  no case uses one, so this is untested rather than contradicted.
- Which of the two tag-stripped renderings of the S452 raw the lane will cite (ScribeKnowledge's 302-line
  file vs my 1,459-line file): the raw bytes are identical, so quotes verify in both, but every
  `file:line` pointer in the entry and the row is valid only against the rendering it names.

## 12. Scratch and tooling

No tool was installed or upgraded. Scratch `$HYAKU_SCRATCH/kake-r79/ScoutSources` (`/fast/scratch/hyaku/…`)
held the first writes, the census copies and `TMPDIR`; it is removed (receipts were copied into
`.ufo/waves/round-79/w1/ScoutSources/` first, and `test -e` on the scratch dir now prints nothing). No
fixture repository was created and no mutating git command was run; `git status --porcelain`, `git diff` and
`cmp` were read-only checks, and the reads of `.ufo/waves/round-78/…` and `corpus/SOURCES.md` were plain
file reads.

Retained in `.ufo/waves/round-79/w1/ScoutSources/`: `mdn-x-robots-tag.raw`, `google-robots-meta.raw`,
`rfc9309.raw`, the three `.txt`, `strip.py`, `strip-output.txt`, `quotes.json`, `verify_quotes.py`,
`verify-output.txt`, `receipts.py`, `receipts-output.txt`, `quote-receipts.json`, `rows-draft.txt`,
`row-deferred-google-xrt.txt`, `check_rows.py`, `check-rows-output.txt`,
`check-rows-deferred-output.txt`, `census-base.txt`, `census-r79.txt`, `census-r79-with-google.txt`.
