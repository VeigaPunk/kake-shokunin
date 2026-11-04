# ScoutSources — round 78, wave w1

**Verdict:** all three sources opened and retained (S449 Google robots-meta spec, S450 WHATWG HTML meta
element, S451 RFC 3339); 41 quotes located and verified; the contract's five grounding facts are
**partly sourced only** — the frozen C3 grammar's exclusive RFC 3339 date form, its outside-`<head>`
finding, its `index`/`follow` tokens, its `noarchive` treatment and its unknown-token reading are **not
stated by any opened source** and must be recorded as lane policy (rejects with flips in §5). Two defects
to route: the contract's Google URL answers **HTTP 404**, and WHATWG **never mentions `robots`** (0 hits
in raw and stripped text), so S450 cannot ground the name.

## 1. Fetches (observed 2026-11-03)

Command per source (run from `.ufo/waves/round-78/w1/ScoutSources/`):

```sh
curl -sSL --max-time 30 -o <name>.raw -w '%{http_code} %{url_effective} %{size_download}\n' <url>
```

| # | requested URL | HTTP | final URL | bytes | sha256 | retained |
|---|---|---|---|---|---|---|
| S449 | `https://developers.google.com/crawling/docs/specs/robots-meta-tag` | **404** | same | 47,502 | `c08c232f5f3d4b01608d863bbd727d05d787b3c2d162de6ccab81f739a4b1e23` | `google-robots-meta-contract-url-404.raw` |
| S449 | `https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag` | 200 | same (no redirect) | 208,195 | `d9fdfe42019fc49ca9f21c2ae1580b8dabf7356b24f6a19043b7021067296b5e` | `google-robots-meta.raw` |
| S450 | `https://html.spec.whatwg.org/multipage/semantics.html` | 200 | same | 333,092 | `08058785b3b995ff5c0cefa6edf2e58eb24b2833bba2928f8ee4c378fc7abb02` | `whatwg-semantics.raw` |
| S451 | `https://www.rfc-editor.org/rfc/rfc3339.txt` | 200 | same | 35,064 | `9ab2b8864a85dca73a88f49b0927bc7bc85f596926e4fd1890905777924e700a` | `rfc3339.raw` |

**Routed defect (contract URL).** The URL the frozen contract names for the robots-meta source,
`/crawling/docs/specs/robots-meta-tag`, is `404 | Page Not Found | Google for Developers`
(`google-robots-meta-contract-url-404.raw`, `<title>` line; `google-robots-meta-contract-url-404.meta`).
Probed alternatives on the same day: `/crawling/docs/robots-meta-tag` 404, `/crawling/docs/specs/
robots-meta-tag?hl=en` 404, `/crawling/docs/robots-txt/robots-txt-spec` 200 (the robots.txt spec),
`/search/docs/crawling-indexing/robots-meta-tag` **200**. The live robots-meta page is the Search docs
path; the row records that path and the 404 evidence is retained beside it. The 404 body is a Google
shell, not a moved-page notice, so nothing at the contract URL can be quoted.

## 2. Strip recipe and text hashes

`strip.py` (docstring is the recipe; round-77's recipe extended with a `<head>` drop):
HTML — drop `<script>`/`<style>` and `<head>`; newline for `</p> </li> </h1-6> </tr> </pre> </div> </dt>
</dd> </table> </ul> </ol>` and `<br>`; `- ` before `<li>`; remove remaining tags; `html.unescape`;
NBSP→space; collapse `[ \t]+`, strip each line; collapse blank runs. RFC text — CRLF→LF, `\f`→newline,
drop `[Page N]` footer and `RFC NNNN … Month YYYY` header, per-line tidy.

`python3 -B strip.py | tee strip-output.txt` — exit 0.

| source | raw bytes | stripped bytes | lines | stripped sha256 |
|---|---|---|---|---|
| `google-robots-meta` | 208,195 | 27,619 | 1,594 | `b6728f0c73460c78bb2fdc240b14e4538f59f36ab62ba0c230a360bf3fdb1df8` |
| `whatwg-semantics` | 333,092 | 97,899 | 2,200 | `31cfec326e4220d206af8cbe8dcd9cd4313cf9b724e96e1a3d20dcbf9f0f344e` |
| `rfc3339` | 35,064 | 28,229 | 753 | `1d35e5292cadacc72542e2161f11458d413108ef111bdfc3a0ee026fec8eb620` |

**Quote locator.** `verify_quotes.py` walks the raw bytes, skips inline tags, decodes entities, collapses
whitespace runs to one space, and maps every emitted character back to its raw byte span; a match therefore
yields (i) the 1-based line range in the stripped `.txt` and (ii) the first..last raw byte of the rendered
span. Every quote below is an exact character-for-character rendering of those bytes — nothing is
paraphrased — but **no prose sentence is byte-contiguous in the raw file**: wrapping, indentation and
inline `<code>`/`<a>` always intervene. `quote-receipts.json` gives each raw span, its sha256 and the number
of tags crossed (`tags_crossed`); `verify-output.txt` is the full 41-quote receipt (exit 0,
`quotes=41 failures=0`, every quote ≤25 words, no pipes, every quote occurs in its stripped text).

## 3. Source → status → size → sha256 → primary quote

| source | status | size | sha256 | primary quote (≤25 w) |
|---|---|---|---|---|
| S449 Google, Robots meta tag specifications | mined | 208,195 | `d9fdfe42…96b5e` | "In the case of conflicting robots rules, the more restrictive rule applies." — `google-robots-meta.txt:1015-1016`, raw `146547..146628`, 12 w |
| S450 WHATWG HTML, meta element / metadata names | mined | 333,092 | `08058785…abb02` | "Names are case-insensitive, and must be compared in an ASCII case-insensitive manner." — `whatwg-semantics.txt:1185-1186`, raw `201402..201668`, 12 w |
| S451 RFC 3339 | mined | 35,064 | `9ab2b886…e700a` | "date-time = full-date \"T\" full-time" — `rfc3339.txt:345`, raw `17347..17388`, 5 w |

## 4. Coverage of the five facts C3 needs

| required fact | grounding quote (id, file:line, raw bytes) | status |
|---|---|---|
| (a) directive vocabulary | "Each value represents a specific rule." (`G-each`, `google-robots-meta.txt:1025-1026`, `147395..147437`); the rule headings are `all` 1033, `noindex` 1038, `nofollow` 1046, `none` 1052, `nosnippet` 1056, `indexifembedded` 1071, `max-snippet` 1081, `max-image-preview` 1123, `max-video-preview` 1158, `notranslate` 1183, `noimageindex` 1193, `unavailable_after` 1198 | **partial** — `index` and `follow` are not rule names anywhere (0 occurrences as headings, §5 R4); `indexifembedded` is a source rule but not in the frozen vocabulary (§5 R5) |
| (a) `none` expansion | "Equivalent to noindex, nofollow." (`G-none`, `:1054`, `149486..149556`, 4 w) | verbatim |
| (a) `all` expansion | "There are no restrictions for indexing or serving. This rule is the default value and has no effect if explicitly listed." (`G-all`, `:1035-1036`, `148079..148210`, 21 w) | verbatim as "no restrictions/default"; **expansion to the tokens `index,follow` is not stated** |
| (b) multiple tags merge, most restrictive wins | "Multiple rules may be combined in a comma-separated list or in separate meta tags." (`G-combine`, `:1026-1027`, `147458..147586`, 14 w) + "In the case of conflicting robots rules, the more restrictive rule applies." (`G-restrictive`, `:1015-1016`) + "if a page has both max-snippet:50 and nosnippet rules, the nosnippet rule will apply" (`G-restrictive-example`, `:1016-1018`, `146642..146852`, 14 w) | verbatim for the generic rule; the per-directive orders are composition (§5 R6) |
| (c) unknown values ignored | "Google supports two user agent tokens in the robots meta tag; other values are ignored" (`G-name-ignored`, `:945-946`, `141869..142023`, 15 w); "The following rules aren't used by Google Search and are ignored." (`G-unused`, `:1217`, `161534..161599`, 11 w); "This rule is ignored if no parseable [number] is specified." (`G-number-ignored`, `:1092-1093`, `152606..152677`); "The rule is ignored if no valid date/time is specified." (`G-date-ignored`, `:1205`) | **name values:** verbatim; **malformed values:** verbatim (rule ignored); **arbitrary unknown content tokens:** **not stated** (§5 R3) |
| (d) `unavailable_after` date form | "The date/time must be specified in a widely adopted format including, but not limited to RFC 822, RFC 850, and ISO 8601." (`G-date-form`, `:1200-1204`, `160146..160551`, 22 w); RFC 3339 is "a profile of the ISO 8601 standard" (`R-profile`, `rfc3339.txt:23-24`, `906..1026`, 22 w) | **composition only** — no source names RFC 3339; Google names three other families (§5 R1) |
| (e) where the tag belongs | "Place the robots meta tag in the `<head>` section of a given page" (`G-place-head`, `:921-922`, `139145..139320`, 13 w); "Google Search doesn't enforce placement of meta robots in the HTML head and will respect robots meta tags in the body section" (`G-body-ok`, `:968-969`, `143664..143793`, 22 w); "If the name attribute is present: where metadata content is expected." (`W-context`, `whatwg-semantics.txt:1117`, `188594..188820`, 11 w) | **head placement:** verbatim (both sources); **body is a finding:** contradicted by Google (§5 R2) |
| (e) what the source says about the name | "The value of the name attribute (robots) specifies that the rule applies to all crawlers." (`G-name-value`, `:941-942`, `141336..141503`, 15 w); "Both the name and the content attributes are case-insensitive." (`G-case`, `:942-943`, `141504..141644`, 9 w); WHATWG: "Names are case-insensitive, and must be compared in an ASCII case-insensitive manner." (`W-case`, `:1185-1186`); "This specification defines a few names for the name attribute of the meta element." (`W-few`, `:1182-1183`) | **Google:** verbatim; **WHATWG:** does not define `robots` at all — `grep -c -i robots` returns **0** on both `whatwg-semantics.raw` and `.txt` |

Additional grounded statements used by the matrix: "Rules specified without a user agent are valid for all
crawlers." (`G-crawler-header`, `:1012`); "the search engine will use the sum of the negative rules"
(`G-sum`, `:1258-1259`); "Any rule that can be used in a robots meta tag can also be specified as an
X-Robots-Tag." (`G-xheader`, `:977-978`); `max-image-preview` values "none: No image preview is to be
shown." / "standard: A default image preview may be shown." / "large: A larger image preview, up to the
width of the viewport, may be shown." (`:1133`, `:1136`, `:1139-1140`); "-1: There is no limit."
(`G-max-video-1`, `:1173`); "indexifembedded only has an effect if it's accompanied by noindex."
(`G-indexifembedded`, `:1078-1079`).

## 5. Rules the contract needs that **no** opened source states

Each row quotes the nearest actual sentence; the reject is explicit and carries a flip condition. None of
these may be written into the C3 knowledge entry as sourced.

| # | contract rule | nearest sentence (verbatim) | why it does not ground the rule | flip condition |
|---|---|---|---|---|
| R1 | `unavailable_after:<RFC 3339 date-time>`, exclusively | "The date/time must be specified in a widely adopted format including, but not limited to RFC 822, RFC 850, and ISO 8601." (`:1200-1204`) | The source names RFC 822 and RFC 850 too, and never says RFC 3339 (`grep -c -i 'RFC 3339' google-robots-meta.raw` → **0**). RFC 3339's own sentence only says it is "a profile of the ISO 8601 standard" (`rfc3339.txt:23-24`) — a membership chain, not a directive binding. | a source says `unavailable_after` takes RFC 3339, or the lane declares "RFC 3339 is the accepted date form; other widely adopted forms are rejected by policy". |
| R2 | a matching element outside `<head>` is `meta_robots_tag_outside_head` and does not join the effective set | "Google Search doesn't enforce placement of meta robots in the HTML head and will respect robots meta tags in the body section of an HTML document as well." (`:968-969`; 28 w — over the 25-word row-quote limit, so the row-citable form is the 22-word prefix `G-body-ok`; both verified) | The source states the **opposite** of the second half: body tags are respected. WHATWG only says a `name` meta is used "where metadata content is expected" (`:1117`) and says nothing about how a consumer treats a misplaced one. | a source says a meta robots in the body is ignored; until then the finding is lane policy that must be labelled as stricter than Google. |
| R3 | unknown content directives produce `meta_robots_unknown_directive` ("the source says unknown values are ignored") | "Google supports two user agent tokens in the robots meta tag; other values are ignored" (`:945-946`) | The sentence is scoped to the **`name` attribute's** user-agent tokens (the preceding sentence is about replacing the `robots` value with a crawler token). No sentence says an arbitrary unknown `content` token is ignored; the only other "ignored" statements cover malformed numbers/dates and three named unused rules (`:1217`). | a source says unknown content directives are ignored, or the lane states the name-value sentence is being read across both attributes. |
| R4 | `index` and `follow` are vocabulary tokens; `all` expands to `index,follow`; default `["follow","index"]` | "There are no restrictions for indexing or serving. This rule is the default value and has no effect if explicitly listed." (`:1035-1036`) | Neither `index` nor `follow` appears as a rule heading (`grep -x index` → 0, `grep -x follow` → 0); the page defines only `all`, `none` and the negative forms. `all` is "no restrictions", not a token pair. | a Google primary (or the machine-readable rules file the page links, not opened) lists `index` and `follow` as rules. |
| R5 | `noarchive` is an effective directive (g23 expects it to join the merge) and `indexifembedded` is unknown | "The noarchive rule is no longer used by Google Search" (`:1225`); "indexifembedded only has an effect if it's accompanied by noindex." (`:1078-1079`) | The vocabulary is neither a subset nor a superset of the source: `noarchive` is in the frozen vocabulary but Google says it is no longer used; `indexifembedded` is a current Google rule but absent from the frozen vocabulary, so the tool would report it as unknown. Both are lane choices, and g23's expectation contradicts the only opened statement about `noarchive`. | the lane restates the vocabulary as "what pages declare, not what Google honours" and adds `indexifembedded`, or a source shows `noarchive` active again. |
| R6 | concrete precedence: `max-image-preview` `none < standard < large`; `-1` loses to any non-negative integer; earliest `unavailable_after` wins | "In the case of conflicting robots rules, the more restrictive rule applies." (`:1015-1016`) | Only the generic rule and one example (`max-snippet:50` + `nosnippet` → `nosnippet`, `:1016-1018`) are stated. The three per-directive orders are compositions from the value definitions; "earliest date wins" is an inference (sooner expiry = more restrictive) that no sentence states. | a source enumerates the precedence of these three value families. |
| R7 | `content` splits on commas, tokens are trimmed, empty tokens ignored, all-empty content → `meta_robots_empty_content` | "Multiple rules may be combined in a comma-separated list or in separate meta tags." (`:1026-1027`) | Only the comma-separated form is stated, with a spaced example (`max-snippet:20, max-image-preview:large`); empty-token, trailing-comma and all-empty handling appear nowhere. | a source states empty-token handling, or the lane labels it parsing policy. |
| R8 | matching is ASCII case-insensitive for both `name` and `content` | "These rules are case-insensitive." (`:1027`); "Both the name and the content attributes are case-insensitive." (`:942-943`) | "ASCII" appears only in WHATWG's sentence about metadata **names** (`:1185-1186`), which never mentions robots. For `content`, ASCII-ness is an inference from "case-insensitive". | a source states ASCII case-folding for content values. |
| R9 | `agents` defaults to `["robots"]`; adding `googlebot` merges across both names (g17/g18) | "The value of the name attribute (robots) specifies that the rule applies to all crawlers." (`:941-942`); "the search engine will use the sum of the negative rules" (`:1258-1259`) | The merge direction is supported; the `agents` vector, its default and the per-name keying are the tool's encoding, not the source's model. | a source defines a multi-agent selection rule. |
| R10 | exit codes 0/1/2/64, duplicate-id fault, `--selftest` ≥40 | — | Nothing in any opened source discusses an audit tool. | never (tool contract is lane policy by construction). |

**Also to route:** the contract's deliverable line names WHATWG for "standard metadata names, `meta
name=robots`". The page never mentions `robots` (0 hits in raw and text), so S450 can ground head placement
and name comparison only. The `robots` name and every directive semantic rest on S449 alone. Do not cite
S450 for the name.

## 6. Vocabulary delta against the frozen C3 list

Frozen list: `all`, `none`, `index`, `noindex`, `follow`, `nofollow`, `noarchive`, `nosnippet`,
`noimageindex`, `notranslate`, `max-snippet`, `max-image-preview`, `max-video-preview`, `unavailable_after`.

S449's active rule headings: `all`, `noindex`, `nofollow`, `none`, `nosnippet`, `indexifembedded`,
`max-snippet`, `max-image-preview`, `max-video-preview`, `notranslate`, `noimageindex`,
`unavailable_after`; plus "historical and other unused" `noarchive`, `nocache`, `nositelinkssearchbox`.

- In the contract but not active in S449: `index`, `follow` (never named), `noarchive` (listed as unused).
- In S449 but not in the contract: `indexifembedded` (active), `nocache`, `nositelinkssearchbox` (unused).
- Consequence for the matrix: a page carrying `indexifembedded` is `meta_robots_unknown_directive` under
  the frozen grammar even though Google documents the rule; g23's `noarchive` expectation is the reverse
  case. Both need an explicit knowledge-entry sentence.

## 7. Drafted registry rows (append after S448)

Ids `S449`–`S451` are the next free at the base (registry's last row is `S448`; `check_rows.py` prints
`registry_last_id=S448 ids_free=['S449','S450','S451']`). Substitute if the L1 assigns differently: the
rows are id-agnostic below the first cell, so replacing `S449`/`S450`/`S451` with the assigned ids (or the
literal `S4NN` placeholder pending integration) changes nothing else. Full
rows are in `rows-draft.txt`; `check_rows.py` exit 0 (`rows=3 failures=0`, 11 non-empty cells each, no
escaped pipes, sha256 and byte count in each anchor match the retained raw file).

```
| S449 | Google Search Central — Robots meta tag, data-nosnippet, and X-Robots-Tag specifications — https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag | docs | A | Google's own page-level robots directive vocabulary, the `none` and `all` meanings, cross-tag and cross-rule conflict resolution, the case-insensitivity of the name and content attributes, head placement and its non-enforcement, and the `unavailable_after` date-format statement — not `X-Robots-Tag` response-header semantics beyond the statement that the same rules apply, not any other crawler's behaviour, not `index` or `follow` as named tokens (the page defines `all`, `none` and the negative directives), not RFC 3339 (the page names RFC 822, RFC 850 and ISO 8601), not `noarchive` as a live directive, not the machine-readable rules file the page links | Using the robots meta tag (head placement 921-922, body note 968-969, name/content case 941-943, unknown name values 945-946); Conflicting robots rules 1015-1018; Valid indexing and serving rules 1020-1027; per-rule entries 1029-1213 (`all` 1033-1036, `none` 1052-1054, max-image-preview settings 1133-1140, unavailable_after 1198-1213); unused rules 1217-1236; page Last updated 2026-03-24 UTC; fetched 2026-11-03, HTTP 200, 208,195 bytes, sha256 d9fdfe42019fc49ca9f21c2ae1580b8dabf7356b24f6a19043b7021067296b5e, retained at .ufo/waves/round-78/w1/ScoutSources/google-robots-meta.raw (the contract URL /crawling/docs/specs/robots-meta-tag answered HTTP 404 the same day; the live path is the search docs path recorded here) | The page-level vocabulary is `all`, `none`, `noindex`, `nofollow`, `nosnippet`, `indexifembedded`, `max-snippet`, `max-image-preview`, `max-video-preview`, `notranslate`, `noimageindex` and `unavailable_after`; `none` is equivalent to noindex, nofollow, and conflicting rules resolve to the more restrictive rule; the name and content attributes are case-insensitive; Google tells authors to place the tag in the head but respects one in the body; `unavailable_after` takes a widely adopted date/time format including RFC 822, RFC 850 and ISO 8601 | mined | 2026-11-03 | 90d | corpus/knowledge/meta-robots-directives.md |
| S450 | WHATWG HTML Living Standard — The meta element and metadata names — https://html.spec.whatwg.org/multipage/semantics.html | spec | A | The meta element's name-attribute metadata channel: its permitted context (where metadata content is expected, i.e. the head), the case-insensitive comparison of metadata names, the few names the specification itself defines, and the open extension rule — not the `robots` name, which the page never mentions and does not define, not any directive vocabulary or content value syntax, not conflict resolution, not what a user agent does with an unknown name | 4.2.5 The meta element (categories and contexts 1117, exactly-one-attribute rule 1144-1145); 4.2.5.1 Standard metadata names (few names 1182-1183, case rule 1185-1186); 4.2.5.2 Other metadata names 1449-1450; Living Standard Last Updated 3 November 2026; fetched 2026-11-03, HTTP 200, 333,092 bytes, sha256 08058785b3b995ff5c0cefa6edf2e58eb24b2833bba2928f8ee4c378fc7abb02, retained at .ufo/waves/round-78/w1/ScoutSources/whatwg-semantics.raw | A meta element with a name attribute is used where metadata content is expected, the specification defines only a few metadata names and compares them ASCII case-insensitively, anyone may add extensions without registering them, and `robots` is not among the names this page defines | mined | 2026-11-03 | 90d | corpus/knowledge/meta-robots-directives.md |
| S451 | RFC 3339 — Date and Time on the Internet: Timestamps — https://www.rfc-editor.org/rfc/rfc3339.txt | spec | A | The RFC 3339 date-time grammar and its ISO 8601 profile relation: full-date, full-time, time-offset and the date-time production — not any robots directive's use of that grammar, not a claim that `unavailable_after` takes RFC 3339, not the calendar limits of section 5.7 beyond the day-of-month statement, not leap-second arithmetic | Abstract (profile of ISO 8601, 23-24); 5.6 Internet Date/Time Format (prose 322-325, ABNF 326-345, T/Z note 346-348); 5.7 Restrictions (date-mday 363-366); RFC 3339, July 2002; fetched 2026-11-03, HTTP 200, 35,064 bytes, sha256 9ab2b8864a85dca73a88f49b0927bc7bc85f596926e4fd1890905777924e700a, retained at .ufo/waves/round-78/w1/ScoutSources/rfc3339.raw | An RFC 3339 date-time is full-date, a T, then full-time, where full-time carries a mandatory time-offset of Z or a numeric offset; RFC 3339 is a profile of ISO 8601; the grammar alone does not bound the day of the month, and section 5.7 supplies that limit | mined | 2026-11-03 | 365d | corpus/knowledge/meta-robots-directives.md |
```

Optional registry prose (L1's call, not written): a `Paths` bullet `Page robots directives — S449 → S450 →
S451`, and a "Search log" paragraph:

> Round 78 bounded question: which primary texts define the page-level robots meta directive channel, its
> name semantics and its date form? Opened Google Search Central's robots meta specification (via the live
> Search docs path; the contract's `/crawling/docs/specs/` path answered 404), the WHATWG HTML meta element
> sections and RFC 3339, one public GET each on 2026-11-03, retained under
> `.ufo/waves/round-78/w1/ScoutSources/`. Identified 3, screened 3, included 3 (S449–S451, tier A),
> excluded 0. Stop: vocabulary, merge rule, name semantics and the date-format statement each have direct
> primary text; the RFC 3339 binding, the outside-head finding and the unknown-token reading are lane
> policy and are recorded as rejects in `w1/ScoutSources.md` §5.

## 8. Mechanical checks (all run; nothing inferred)

| check | command | result |
|---|---|---|
| fetch, 3 sources + 404 evidence | `curl -sSL --max-time 30 -o …` ×4 | exit 0 each; statuses and hashes in §1 |
| strip | `python3 -B strip.py` | exit 0; three `.txt` written, hashes §2 |
| quote location | `python3 -B verify_quotes.py` | **exit 0**; `quotes=41 failures=0`; every quote 4–23 words, no pipes, every quote found in its stripped text (one quote, `G-number-ignored`, occurs twice; both spans listed) |
| quote receipts | `python3 -B receipts.py` | exit 0; `receipts=41 without_txt=0`; spans+sha256+tags in `quote-receipts.json` |
| row shape | `python3 -B check_rows.py` | **exit 0**; `rows=3 failures=0`; 11 cells each; anchor sha256 and byte counts match |
| robots absence in WHATWG | `grep -c -i robots whatwg-semantics.raw whatwg-semantics.txt` | `0` and `0` |
| RFC 3339 absence in Google | `grep -c -i 'RFC 3339' google-robots-meta.raw google-robots-meta.txt` | `0` and `0` |
| `index`/`follow` not rule headings | `grep -x index` / `grep -x follow` | `0` and `0` |

Retained receipts in `.ufo/waves/round-78/w1/ScoutSources/`: `google-robots-meta.raw`,
`google-robots-meta-contract-url-404.raw`, `whatwg-semantics.raw`, `rfc3339.raw`, the three `.txt`
renderings, `*.meta`, `strip.py`, `strip-output.txt`, `quotes.json`, `verify_quotes.py`,
`verify-output.txt`, `receipts.py`, `receipts-output.txt`, `quote-receipts.json`, `rows-draft.txt`,
`check_rows.py`, `check-rows-output.txt`.

No tool was installed or upgraded this seat. Scratch (`$HYAKU_SCRATCH/kake-r78/ScoutSources`) was used only
for `TMPDIR` and is removed at close; no fixture repo was created.

## 9. Remaining unknowns

- Whether Google's machine-readable rules file (linked from the page, not opened) lists `index` and
  `follow`; if it does, R4 stops being a reject.
- Whether another crawler's primary source makes `noarchive` active (Bing/Yandex were not opened).
- The contract's exact g12/g13 timestamp literals are not yet visible to this seat; if they include a bare
  date, note that Google's own example `<meta name="robots" content="unavailable_after: 2020-09-21">`
  (`:1213`) is a `full-date`, not an RFC 3339 `date-time`, and would be `invalid_value` under R1's strict
  reading — the tool author must decide this before g12 is frozen.
