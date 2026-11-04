# ScoutHreflangSources — round 76, wave w1 (kake lane)

Report path: `.ufo/waves/round-76/w1/ScoutHreflangSources.md`
Artifacts: `.ufo/waves/round-76/w1/ScoutHreflangSources/`
Base revision (round open, contract base): `a0491fcd041cbc3fff2c964ecf6268557e45a5c1`.
Lane HEAD observed at measurement: `783c7c13` ("round-76: amendment 1") — the L1 committed the frozen
contract (`b758cb04`) and amendment 1 after round open, both before this seat ran.

Read-only seat: no production file in the lane was created, edited or deleted; no git/jj mutation was run.
Only this report and its artifact directory were written. No tool was installed or upgraded (no package
manager was invoked). Scratch `/fast/scratch/hyaku/kake-r76/ScoutHreflangSources` was removed before yield
(no file above 50 MB was staged there).

## 0. Verdicts

1. **All three sources opened.** `GET` → `HTTP 200`, 0 redirects, final URL identical to the requested URL,
   curl exit 0. WHATWG and RFC 5646 bytes are reproducible (`cmp` identical across two GETs); the Google
   page's raw bytes are **not** (199,246 → 199,242 bytes), but its tag-stripped article text is
   byte-identical, so the quotes are stable while the raw hash pins one measurement.
2. **Grounding, rule by rule.** (a) grounded, two Google quotes. (b) **partially** grounded: "values are
   language tags" is grounded (WHATWG), "x-default is the only non-tag value" is **not stated by any of
   the three** (`x-default` occurs 0 times in the WHATWG page and 0 times in RFC 5646). (c) grounded in
   Google only; the HTML spec permits relative `href` and states no absoluteness requirement. (d) **not
   grounded** — no fetched source says a hreflang target's canonical must be itself; the nearest
   statement defines what `rel=canonical` means, not what a hreflang target must do.
3. **Rows proposed:** `S444` (Google), `S445` (WHATWG links.html), `S446` (RFC 5646), the first three ids
   above the lane tip `S443`. Validator compatibility checked against `scripts/sources-census.sh` (NF=13,
   enums, E04 scope key, E11 used-by existence, E12 placement) — see §5.

## 1. Fetch record

First GET (the retained bytes), command shape:

```sh
TMPDIR=$S/tmp curl -sSL --max-time 30 -o <retained> -w '%{http_code} %{url_effective} %{size_download}\n' <url>
```

| # | requested URL | http_code | url_effective | num_redirects | size_download | curl exit | sha256 of saved bytes |
|---|---|---|---|---|---|---|---|
| 1 | `https://developers.google.com/search/docs/specialty/international/localized-versions` | 200 | same | 0 | 199246 | 0 | `12fbe2816a3643796fbe496f694c13ec895ad9533d2ba8210efe66af89dc8d7b` |
| 2 | `https://html.spec.whatwg.org/multipage/links.html` | 200 | same | 0 | 381019 | 0 | `2f21e82b78d069ee01d61aca14a7b07832a4ab58b9633db88b45983a0f14eec3` |
| 3 | `https://www.rfc-editor.org/rfc/rfc5646.txt` | 200 | same | 0 | 208592 | 0 | `5d9515f053163c80e7294a84d18217dc83471acc7caa9773da2ac40deeec8228` |

Second GET (idempotence check; `-w` with labelled fields), raw log retained at
`ScoutHreflangSources/refetch-record.txt`:

| # | http_code | num_redirects | size_download | sha256 (second GET) | `cmp` vs retained |
|---|---|---|---|---|---|
| 1 | 200 | 0 | 199242 | `e41e3dca754daf9233a1e46f1fef99cbb1581a3d0e12d084be839a93047c9490` | **DIFFERS** (−4 bytes) |
| 2 | 200 | 0 | 381019 | `2f21e82b78d069ee01d61aca14a7b07832a4ab58b9633db88b45983a0f14eec3` | IDENTICAL |
| 3 | 200 | 0 | 208592 | `5d9515f053163c80e7294a84d18217dc83471acc7caa9773da2ac40deeec8228` | IDENTICAL |

### 1.1 What varies on the Google page (measured, not assumed)

A line-level `difflib` comparison of the two raw fetches finds differences only in (i) the order of
`data-label` / `data-category` / `aria-label` attributes on footer promo links (raw lines ~4390–4510),
(ii) the key order inside the `application/json analytics` dimensions object (raw line 5088), and
(iii) a CSP `nonce` and a script payload (raw lines 5099, 5104). All of these are outside the article body.
Decisive check: the tag-stripped body of the second fetch is **byte-identical** to the retained one —
`diff` line count 0, 882 lines, sha256 `96175da894ea426f894488468a61635665bf8735e9cfaef05ea24913d16a8788`.
So a quote anchored on the retained `.txt` survives a re-fetch, while a quote anchored on the raw HTML hash
would not.

## 2. Retained artifacts and the tag-strip pipeline

| file | bytes | lines (LF) | sha256 |
|---|---|---|---|
| `google-localized-versions.html` | 199246 | — | `12fbe2816a3643796fbe496f694c13ec895ad9533d2ba8210efe66af89dc8d7b` |
| `google-localized-versions.txt` | 25035 | 882 | `96175da894ea426f894488468a61635665bf8735e9cfaef05ea24913d16a8788` |
| `whatwg-links.html` | 381019 | — | `2f21e82b78d069ee01d61aca14a7b07832a4ab58b9633db88b45983a0f14eec3` |
| `whatwg-links.txt` | 111855 | 8659 | `4254043fb66c1bfd1b2b0fbc528449fe2336abaad7f25fb8d1ab7d7f66df5375` |
| `rfc5646.txt` | 208592 | 4707 | `5d9515f053163c80e7294a84d18217dc83471acc7caa9773da2ac40deeec8228` (raw and text are the same file) |

Pipeline (applied to the two HTML bodies; recorded in `ScoutHreflangSources/verify_quotes.py`):
drop `<script …>…</script>` and `<style …>…</style>` (case-insensitive, dotall), replace every remaining
`<…>` run with a newline, `html.unescape`, strip each line, drop empty lines. Each inline element
(`<code>`, `<a>`, `<b>`) therefore lands on its own line — which is why a single sentence can occupy
several consecutive line numbers.

**Line-number convention.** All cited line numbers count **LF only** (`grep -n` / `sed` / `wc -l`
compatible). This matters for RFC 5646: the file carries form feeds (`^L`) as page separators, and
`str.splitlines()` splits on them, shifting every later line by up to 18 (a first pass of the verifier
reported the well-formed sentence at 1071–1072 instead of the grep-true 1053–1054). The verifier now
splits on LF only.

Verifier: `ScoutHreflangSources/verify_quotes.py` (17 quotes) — exit 0, `failures=0`, full output at
`ScoutHreflangSources/verify-output.txt`. It locates each quote in the whitespace-collapsed body, maps the
character offsets back to lines, and fails unless the derived window equals the declared window.

## 3. Rule-by-rule grounding for contract C2

Quotes are ≤25 words, whitespace-collapsed, each verified to occupy exactly the stated line window. Word
counts are whitespace-split counts.

### (a) Every hreflang version must list itself; x-default covers unmatched languages — **grounded**

| source | quote (≤25 words) | location | words |
|---|---|---|---|
| Google | "Each language version must list itself as well as all other language versions." | § Guidelines for all methods (heading line 361), tag-stripped lines **362–364** | 13 |
| Google | "The reserved x-default value is used when no other language/region matches the user's browser setting." | § Use the x-default value for unmatched languages (heading lines 726–728), tag-stripped lines **729–732** | 15 |

The self-listing half is a "must" in Google's own words; the x-default half is stated as the reserved value
that matches unmatched languages. Both are Google policy statements, not spec requirements — the WHATWG page
does not require self-listing at all.

### (b) Values are language tags; x-default is the only non-tag value — **partially grounded**

| source | quote (≤25 words) | location | words |
|---|---|---|---|
| WHATWG | "The value must be a valid BCP 47 language tag." | §4.6.3 API for hyperlink elements, `hreflang` dfn (`id=attr-hyperlink-hreflang`), tag-stripped line **1356** | 10 |
| WHATWG | "gives the language of the linked resource. It is purely advisory." | same paragraph, tag-stripped lines **1355–1356** | 11 |
| Google | "There's no need to specify a language code for the x-default value" | § Use the x-default value for unmatched languages, tag-stripped lines **738–740** | 12 |

- "Values are language tags" is grounded: the HTML spec states a normative "must" and cites BCP 47.
- **"x-default is the only non-tag value" is not grounded by these three sources.** `x-default` appears
  **0 times** in `whatwg-links.txt`, **0 times** in the raw `whatwg-links.html`, and **0 times** in
  `rfc5646.txt`; Google calls it a *reserved* value and
  says it needs no language code, but nowhere says it is the only non-tag value. Do not present the
  exclusivity claim as sourced; it is a lane narrowing of the two statements above.

### (c) Alternate hrefs must be fully qualified — **grounded in Google only**

| source | quote (≤25 words) | location | words |
|---|---|---|---|
| Google | "Alternate URLs must be fully-qualified, including the transport method (http/https), so:" | § Guidelines for all methods, tag-stripped line **365** (the example follows at 366–371: `https://example.com/foo`, then `not`, `//example.com/foo`, `or`, `/foo`) | 11 |

The HTML spec imposes no such rule: `href` is a URL resolved against the document base, and the only
"absolute URL" requirement in `links.html` (tag-stripped lines 8505–8508) is about *extension type*
keywords containing a colon — unrelated. So this rule is a Google-annotation rule, and the tool must not
describe a relative alternate as invalid HTML.

Note the exact scope of Google's sentence: it rejects **`//example.com/foo`** as well as `/foo`. C2's
finding id is worded "alternate `href` without scheme and host", which a protocol-relative URL satisfies
(it has a host, no scheme) — see §7, ambiguity 2.

### (d) The canonical of the page a hreflang points at must be itself — **NOT grounded**

No fetched source states this rule. Evidence of absence, not a stretched quote:

- The Google localized-versions page never mentions canonical: in the stripped body the only occurrences
  of `canonical` are navigation links (lines 19, 121–124, 298). Its one related sentence is about
  duplicates, not canonicals: "Localized versions of a page are only considered duplicates if the main
  content of the page remains untranslated." (lines 340–342, adjacent, not used as a quote).
- The nearest WHATWG statement defines the keyword, not the hreflang interaction: "The canonical keyword
  indicates that URL given by the href attribute is the preferred URL for the current document."
  (§4.6.8.4 Link type "canonical", tag-stripped lines **4396–4400**, 19 words). That says a canonical names
  the current document's preferred URL; it does not say a page carrying hreflang alternates must be
  self-canonical, and it says nothing about the target page.
- The lane already holds S262 (Google canonicalization: "a declared canonical is a hint, not a rule"), which
  points the other way: canonical is a hint Google weighs, not a hard requirement.

**Consequence for C2.** `hreflang_canonical_not_self` is a **lane policy finding**, not a sourced
requirement. The contract's own "Limits" list does not disclaim it, so the C2 entry should say so
explicitly; otherwise the claim would rest on a rule no opened source carries.

### Supporting quotes the C2 entry will also need (all verified)

| rule it supports | source | quote (≤25 words) | location | words |
|---|---|---|---|---|
| `hreflang_nonreciprocal` (target B must return the link) | Google | "If two pages don't both point to each other, the tags will be ignored." | § Guidelines for all methods, line **387** | 14 |
| HTML-only audit is one of three channels (scope limit) | Google | "There are three ways to indicate multiple language/locale versions of a page to Google:" | § Methods for indicating your alternate pages (heading 343), line **344** (the three items follow on 345–347: HTML, HTTP Headers, Sitemap) | 14 |
| "no claim about the actual language of any page" (limit) | Google | "Google doesn't use hreflang or the HTML lang attribute to detect the language of a page" | § Methods for indicating your alternate pages, lines **355–360** | 16 |
| hreflang values compare case-insensitively | Google | "The hreflang value is case-insensitive" | § Supported language and region codes (heading 666), lines **682–684** | 5 |
| Google's supported code set is narrower than BCP 47 (see §7, note 1) | Google | "Only language codes listed in ISO 639-1 and region codes listed in ISO 3166-1 Alpha 2 are supported" | § Supported language and region codes, lines **680–681** (681 continues: "other codes that aren't listed in those standards, such as es-419, aren't supported") | 19 |
| language-tag subtags are case-insensitive | RFC 5646 | "At all times, language tags and their subtags, including private use and extensions, are to be treated as case insensitive" | §2.1.1 Formatting of Language Tags, lines **327–328** | 20 |
| the shape of a tag (frozen-grammar basis) | RFC 5646 | `langtag = language ["-" script] ["-" region] *("-" variant) *("-" extension) ["-" privateuse]` | §2.1 Syntax, ABNF lines **231–236** | 13 |
| primary language subtag may be 2–8 letters (see §7, note 1) | RFC 5646 | `language = 2*3ALPHA ; shortest ISO 639 code` | §2.1 Syntax, line **238** (productions continue at 239–242: extlang, 4ALPHA, 5*8ALPHA) | 8 |
| "well-formed" is the syntax notion the grammar decides | RFC 5646 | `A tag is considered "well-formed" if it conforms to the ABNF (Section 2.1).` | §2.2.9 Classes of Conformance (heading 1046), lines **1053–1054** | 13 |

## 4. Proposed SOURCES rows (contract v1, 11 columns)

Insert under `## Registry` in `corpus/SOURCES.md` (E12 fires on a row-shaped line outside that section).
No cell contains `|`. Ids are the first three unused above the lane tip `S443`.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S444 | Google for Developers — Tell Google about localized versions of your page (hreflang) — https://developers.google.com/search/docs/specialty/international/localized-versions | docs | A | The hreflang annotation rules Google states for HTML link elements — self-listing, reciprocity, fully-qualified alternate URLs, and the reserved x-default fallback; not a statement about Google's selection, ranking or language detection | § Guidelines for all methods (tag-stripped lines 361-372) and § Use the x-default value for unmatched languages (lines 726-740); doc prints Last updated 2026-09-21 UTC; fetched 2026-11-03, HTTP 200, 199,246 bytes, sha256 12fbe2816a3643796fbe496f694c13ec895ad9533d2ba8210efe66af89dc8d7b, retained at .ufo/waves/round-76/w1/ScoutHreflangSources/google-localized-versions.html (tag-stripped text alongside) | Each language version must list itself and all other versions, alternate URLs must be fully-qualified including http/https, and x-default is the reserved fallback for unmatched languages | mined | 2026-11-03 | 180d | corpus/knowledge/hreflang-declaration.md |
| S445 | WHATWG HTML Living Standard — Links, the hreflang attribute and the alternate link type — https://html.spec.whatwg.org/multipage/links.html | spec | A | The hreflang attribute's value rule on hyperlink elements and the alternate link type's translation reading — not x-default, not URL absoluteness, not canonical-versus-self | §4.6.3 API for hyperlink elements, hreflang dfn attr-hyperlink-hreflang (tag-stripped lines 1349-1360, quote at 1356); §4.6.8.1 Link type alternate (heading 3759-3762, translation sentence 4046-4056); Living Standard last updated 3 November 2026; fetched 2026-11-03, HTTP 200, 381,019 bytes, sha256 2f21e82b78d069ee01d61aca14a7b07832a4ab58b9633db88b45983a0f14eec3, retained at .ufo/waves/round-76/w1/ScoutHreflangSources/whatwg-links.html | hreflang is purely advisory and its value must be a valid BCP 47 language tag, while the spec defines no x-default value | mined | 2026-11-03 | 90d | corpus/knowledge/hreflang-declaration.md |
| S446 | RFC 5646 — Tags for Identifying Languages (BCP 47) — https://www.rfc-editor.org/rfc/rfc5646.txt | spec | A | The syntax of a language tag: the langtag ABNF productions and the case-insensitivity rule — the grammar behind a hreflang value check, not a registry of assigned subtags | §2.1 Syntax, ABNF lines 218-262 (langtag 231-236, language 238-242); §2.1.1 Formatting of Language Tags, lines 325-330; §2.2.9 Classes of Conformance, lines 1053-1054; RFC 5646, September 2009; fetched 2026-11-03, HTTP 200, 208,592 bytes, sha256 5d9515f053163c80e7294a84d18217dc83471acc7caa9773da2ac40deeec8228, retained at .ufo/waves/round-76/w1/ScoutHreflangSources/rfc5646.txt | A language tag's shape is fixed by the langtag ABNF and its subtags compare case-insensitively, so a value can be judged well-formed without a subtag registry | mined | 2026-11-03 | 365d | corpus/lessons/round-76.md |

Status note: the contract says `mined` only for a row C2's entry will cite. All three ground rules the tool
implements, and the round's knowledge entry is drafting quotes from all three; **if the landed entry ends up
citing only the Google row, set S445 and S446 to `queued` before landing.**

## 5. `## Gate` evidence (URL, access date, located quote per row)

- **S444** — `https://developers.google.com/search/docs/specialty/international/localized-versions`,
  accessed **2026-11-03** (HTTP 200, 0 redirects, 199,246 bytes,
  sha256 `12fbe281…dc8d7b`). Quote: "Each language version must list itself as well as all other language
  versions." — § Guidelines for all methods, tag-stripped lines 362–364.
- **S445** — `https://html.spec.whatwg.org/multipage/links.html`, accessed **2026-11-03** (HTTP 200,
  0 redirects, 381,019 bytes, sha256 `2f21e82b…14eec3`; page prints "Living Standard — Last Updated
  3 November 2026"). Quote: "The value must be a valid BCP 47 language tag." — §4.6.3 API for hyperlink
  elements, `hreflang` dfn, tag-stripped line 1356.
- **S446** — `https://www.rfc-editor.org/rfc/rfc5646.txt`, accessed **2026-11-03** (HTTP 200, 0 redirects,
  208,592 bytes, sha256 `5d9515f0…ec8228`; RFC 5646, September 2009). Quote: "At all times, language tags
  and their subtags, including private use and extensions, are to be treated as case insensitive" —
  §2.1.1 Formatting of Language Tags, lines 327–328.

## 6. Validator compatibility (`scripts/sources-census.sh`, read-only)

Rules read from the script itself (`sed -n '552,672p'`), not from memory, **and** exercised against the
three rows in a scratch fixture: `$S/fixture2` holds a copy of the lane registry plus a stub file for every
used-by path it names, the rows are inserted after the last `S###` row (inside `## Registry`), and
`sources-census.sh validate --file … --today 2026-11-03` is run before and after. Receipts:
`ScoutHreflangSources/census-fixture-before.txt` (exit 0, 16 W04, no E-code) and
`ScoutHreflangSources/census-fixture-after.txt` (exit 0, 17 W04, no E-code). The only difference:

```
> file	W04	S445 duplicate url html.spec.whatwg.org/multipage/links.html across scopes
```

A control run with the two used-by targets absent produced exactly the E11 lines for S444/S445/S446, which
is what fixes the landing order below.

| check | requirement | status of the three rows |
|---|---|---|
| E01 | `NF==13` (11 cells between the outer pipes) | satisfied — each row has 11 cells |
| E02/E03 | id matches `^S[0-9]{3,}$`, unique | S444/S445/S446, no collision in the lane (`grep -oE '^\| S[0-9]+'` max = 443) |
| E04 | same URL **and** same scope twice, neither rejected, no "supersedes S###" | not triggered. S023 already holds `html.spec.whatwg.org/multipage/links.html#link-type-canonical`; `url_of()` strips the fragment so the URL matches S445's, but S023's scope ("HTML link-type keyword semantics") differs from S445's, so `scope_key` differs |
| W04 | same URL, different scope | **expected warning** for S445 vs S023 — warnings do not change a clean exit (`validate` exit 0) |
| E05 | kind ∈ spec/docs/paper/code/tool/dataset/talk/book/community/own-work | docs, spec, spec |
| E06 | tier ∈ A/B/C | A, A, A |
| E07 | status ∈ queued/mined/rejected | mined (see the status note in §4) |
| E08 | opened a past/present ISO date | 2026-11-03 |
| E09 | recheck ISO date, `NNd`, or a symbolic cadence matching `^[A-Za-z][A-Za-z0-9 _-]*$` | 180d, 90d, 365d |
| E10 | community never tier A | kind is not community |
| E11 | every comma-separated used-by path exists on disk **at validate time** | **ordering dependency, measured** — with the two targets absent the fixture run emitted exactly `E11 S444 … corpus/knowledge/hreflang-declaration.md`, `E11 S445 …` and `E11 S446 … corpus/lessons/round-76.md`; with stubs present, none. `corpus/knowledge/hreflang-declaration.md` and `corpus/lessons/round-76.md` do not exist in the lane yet (`ls` → No such file). Land the rows together with, or after, those files. If the rows must land first, use the existing wave artifact as the temporary used-by: `.ufo/waves/round-76/w1/ScoutHreflangSources.md`, then repoint in the same round |
| E12 | row-shaped `S###` line only inside `## Registry` | rows must be inserted under that heading, 0–3 leading spaces |

## 7. Divergences and limits the C2 build must not paper over

1. **Google's supported code set is narrower than the frozen grammar.** Google: "Only language codes listed
   in ISO 639-1 and region codes listed in ISO 3166-1 Alpha 2 are supported" (680–681) and, on 681,
   "other codes that aren't listed in those standards, such as es-419, aren't supported". RFC 5646's
   `language` production admits `2*3ALPHA`, `4ALPHA`, `5*8ALPHA` (238–242) and `region` admits `3DIGIT`
   (249). C2's frozen grammar `^[A-Za-z]{2,3}(-[A-Za-z]{4})?(-([A-Za-z]{2}|[0-9]{3}))?...` accepts 3-letter
   languages and 3-digit regions, and rejects 4–8 letter primary subtags, extension singletons
   (`en-u-ca-gregory`) and private-use (`x-…`). Therefore `hreflang_invalid_tag` is a **BCP-47-syntax
   subset** check: never describe a passing value as "supported by Google", and never describe a failing
   value as "not a BCP 47 tag" without the "under the frozen grammar" qualifier.
2. **Protocol-relative URLs.** Google's example rejects `//example.com/foo` (369) alongside `/foo` (371);
   C2's id is worded "alternate `href` without scheme and host". Under a conjunctive reading (`no scheme`
   AND `no host`) a protocol-relative href passes C2 and fails Google; under the other reading it is
   flagged. The matrix needs a decision; per C2 kill rule 1 a case whose verdict is not derivable is
   `undecided`, so the builder should either fix the reading in an amendment or exclude the case.
3. **`x-default` is Google-only.** Zero occurrences in the WHATWG page and in RFC 5646. C2's `x-default`
   handling (the `hreflang_multiple_xdefault` finding and the exclusion of `x-default` from
   `hreflang_invalid_tag`) rests on Google's reserved-value statement, not on a spec.
4. **Rule (d) has no source** (§3d). Either the C2 entry states it as lane policy or the rule is dropped;
   a quote cannot be produced for it.
5. **HTML-only scope.** Google names three equivalent channels (HTML, HTTP Headers, Sitemap, 344–347); the
   tool reads HTML `link` elements only. The offline-audit claim must stay inside that channel.
6. **Raw-byte reproducibility.** The Google page's raw bytes change between GETs (199,246 → 199,242; footer
   attribute order, analytics JSON key order, script nonce). The registry hash pins the retained
   measurement; the stripped-text hash pins the quotable content and is the one to re-check.
7. **Line numbers are derivative.** They belong to the recorded tag-strip pipeline applied to the retained
   HTML (LF-only splitting). A different stripper yields different numbers; the retained `.txt` with its
   sha256 is the anchor.
8. **No LSP applies.** The inputs are web-spec documents, not a codebase with a language server; literal
   substring location on hash-pinned bytes is the appropriate method here, and no semantic claim rests on
   it. No grep output is presented as semantic proof of anything beyond where a sentence sits.

## 8. Commands and exit codes

| # | command | observed |
|---|---|---|
| 1 | `TMPDIR=$S/tmp curl -sSL --max-time 30 -o <file> -w '%{http_code} %{url_effective} %{size_download}\n' <url>` ×3 | `200 <same url> 199246`, `200 <same url> 381019`, `200 <same url> 208592`; exit 0 each |
| 2 | same with `http_code=/url_effective=/size_download=/num_redirects=/time_total=` into `refetch-record.txt` | 200/0 redirects for all three; `cmp` IDENTICAL, IDENTICAL, DIFFERS |
| 3 | `sha256sum` over the retained bodies | hashes as in §2 |
| 4 | `python3 -B verify_quotes.py` | `quotes=17 … failures=0`, exit 0 (`verify-output.txt`) |
| 5 | `diff google-localized-versions.txt <stripped refetch>` | 0 diff lines (bodies identical) |
| 6 | `grep -c x-default` on `whatwg-links.txt` / `rfc5646.txt` | `0` / `0` |
| 7 | `grep -oE '^\| S[0-9]+' corpus/SOURCES.md \| grep -oE '[0-9]+' \| sort -n \| tail -3` | `441 442 443` (tip `S443`) |
| 8 | `sed -n '552,672p' scripts/sources-census.sh` (read-only) | validator enums and E04/E11/E12 logic as quoted in §6 |
| 9 | `cp corpus/SOURCES.md $S/fixture2/kake-shokunin/corpus/` + stub every used-by path | `stub files created: 82` |
| 10 | `./scripts/sources-census.sh validate --file $S/fixture2/…/SOURCES.md --today 2026-11-03` (baseline) | exit 0, 16 W04, no E-code → `census-fixture-before.txt` |
| 11 | same after inserting S444–S446 (plus stubs for their two used-by targets) | exit 0, 17 W04, no E-code; the single added line is `W04 S445 duplicate url html.spec.whatwg.org/multipage/links.html across scopes` → `census-fixture-after.txt` |
| 12 | same with the two used-by targets removed | exit 1, exactly three E11 lines for S444/S445/S446 (landing-order control) |

## 9. Unknowns

- Whether the landed C2 entry will cite all three rows (decides the `mined`/`queued` split in §4).
- Whether the L1 will land the SOURCES rows before `corpus/knowledge/hreflang-declaration.md` and
  `corpus/lessons/round-76.md` exist (E11); the fallback used-by is given in §6.
- Whether the L1 will amend C2's `hreflang_relative_href` wording for protocol-relative URLs (§7.2) or mark
  that matrix case `undecided`.
- Amendment 1 (`8 retained served pages`, not 12) does not touch this seat; it changes the real-input
  population the C2 executor will run over.
