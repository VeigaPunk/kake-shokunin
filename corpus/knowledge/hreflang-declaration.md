source: S444 — Google Search Central, Localized versions of your pages — https://developers.google.com/search/docs/specialty/international/localized-versions — §"Guidelines for all methods", §"HTML tags", §"Use the x-default value for unmatched languages"; tag-stripped text lines 340-423 and 726-740 of `.ufo/waves/round-76/w1/ScoutHreflangSources/google-localized-versions.txt` (25,035 B, sha256 96175da894ea426f894488468a61635665bf8735e9cfaef05ea24913d16a8788; raw body 199,246 B, sha256 12fbe2816a3643796fbe496f694c13ec895ad9533d2ba8210efe66af89dc8d7b); S445 — WHATWG HTML §4.6.3 API for hyperlink elements (`attr-hyperlink-hreflang`) and §4.6.8.1 Link type "alternate" — https://html.spec.whatwg.org/multipage/links.html — lines 1349-1361 and 4036-4056 of `whatwg-links.txt` (111,855 B, sha256 4254043fb66c1bfd1b2b0fbc528449fe2336abaad7f25fb8d1ab7d7f66df5375; raw 381,019 B, sha256 2f21e82b78d069ee01d61aca14a7b07832a4ab58b9633db88b45983a0f14eec3); S446 — RFC 5646 §2.1 Syntax and §2.2.9 Classes of Conformance — https://www.rfc-editor.org/rfc/rfc5646.txt — lines 195-275 and 1046-1057 (208,592 B, sha256 5d9515f053163c80e7294a84d18217dc83471acc7caa9773da2ac40deeec8228); all three fetched 2026-11-03 HTTP 200, retained under `.ufo/waves/round-76/w1/ScoutHreflangSources/`
verified-at: 2026-11-03
recheck: 90d
ground: operability — the offline hreflang declaration audit (round-76 contract C2)
scope: declaration syntax and the inter-page link rules two publishers state; nothing about selection, rendering, ranking or the language of any live page

# hreflang declarations — what a page declares, and what an offline audit can decide

## What a declaration is

An hreflang declaration is a `<link rel="alternate">` element whose `hreflang` attribute names the
language of the linked variant. WHATWG defines the keyword as the link type that "creates a hyperlink
referencing an alternate representation of the current document" (§4.6.8.1, `whatwg-links.txt`
lines 4037-4040), and defines the attribute in one sentence: "The value must be a valid BCP 47
language tag." (§4.6.3, `attr-hyperlink-hreflang`, `whatwg-links.txt` line 1356, 10 words).

The attribute is a publisher claim about the target, not a measurement of it. WHATWG adds "It is purely
advisory." (lines 1355-1356) and "User agents must not consider this attribute authoritative"
(lines 1358-1359), and Google states that it does not use the annotation to find a page's language:
"Google doesn't use hreflang or the HTML lang attribute to detect the language of a page"
(`google-localized-versions.txt` lines 355-360).

## The self-reference rule

A page that declares variants declares itself among them. Google's first guideline reads "Each language
version must list itself as well as all other language versions." ("Guidelines for all methods",
`google-localized-versions.txt` lines 362-364), and the HTML form repeats the consequence: "The set of
links is identical for every version of the page." ("HTML tags", lines 421-423).

Contract id for the violation: `hreflang_self_missing` — a page with at least one hreflang alternate
that does not list its own manifest `url` among them.

## `x-default`

`x-default` is the reserved value for the page served to users whose language settings match no declared
variant: "The reserved x-default value is used when no other language/region matches the user's browser
setting." ("Use the x-default value for unmatched languages", `google-localized-versions.txt`
lines 729-732). It carries no language code — "There's no need to specify a language code for the
x-default value" (lines 738-740) — and it is counted per page, not per variant.

Contract ids: more than one `x-default` on one page is `hreflang_multiple_xdefault`; an alternate with no
hreflang value at all is `hreflang_missing_value`.

Lexical note, because it changes what "invalid" can mean: RFC 5646's private-use production
`privateuse = "x" 1*("-" (1*8alphanum))` (`rfc5646.txt` line 265) admits `x-default` as a private-use tag.
A rule that accepted "any valid BCP 47 tag" would therefore admit `x-default` for the wrong reason. The
contract handles this by naming `x-default` as the one reserved non-language value and applying the tag
grammar only to the rest. The word `x-default` occurs nowhere in the two specification bodies opened this
round (`grep -c 'x-default' whatwg-links.txt` → `0`; `grep -c 'x-default' rfc5646.txt` → `0`), so the
reserved-value rule is Google's, and WHATWG's BCP-47 sentence neither admits nor excludes it.

## Absolute hrefs

Google requires fully qualified targets: "Alternate URLs must be fully-qualified, including the transport
method (http/https), so:" (`google-localized-versions.txt` line 365, 11 words), with
`https://example.com/foo` as the compliant form and `//example.com/foo`, `/foo` as the non-compliant ones
(lines 366-371).

Contract id: `hreflang_relative_href` for an alternate `href` that does not parse as an absolute URL with
scheme and authority (Amendment 2 A12; the scheme need not be `http(s)`). The protocol-relative shape is
therefore a finding, not a clean pass — Google's sentence rejects `//example.com/foo` as well, so the id's
original "without scheme and host" phrasing and the guideline agree once A12 decides it. A non-absolute
href is reported once and contributes to no other finding (A4).

## The canonical interaction

Contract id: `hreflang_canonical_not_self` — a page with at least one hreflang alternate whose resolved
canonical is not its own `url`.

This rule is the contract's policy, not a statement the opened sources make. Google's page mentions
canonical only in its navigation (`grep -n 'canonical' google-localized-versions.txt` → lines 19,
121-124, 298, all navigation links), and RFC 5646 does not discuss canonical at all. WHATWG defines the
link type without touching hreflang: "The canonical keyword indicates that URL given by the href attribute
is the preferred URL for the current document." (§4.6.8.4, `whatwg-links.txt` lines 4396-4400, 19 words) —
a statement about one page's preferred URL, not about the page a hreflang alternate points at. The nearest
grounded statement about variants is about duplicates, not canonical: "Localized versions of a page are
only considered duplicates if the main content of the page remains untranslated."
(`google-localized-versions.txt` lines 340-342). The registry holds canonical-specific rows from an
earlier round (S020 RFC 6596, S021 Google canonical guidance); they were not re-opened this round and are
not quoted here, so the canonical finding is recorded as a lane policy choice with a sourced context, not
as a sourced rule. Amendment 2 fixes the resolution the rule needs: a page without a `rel=canonical` link
is its own canonical (A5), the first `rel=canonical` in document order is the page's canonical (A6), a
canonical link that also carries `hreflang` is still the page's canonical for this tool (A7), and the
finding is emitted once per page, not once per annotation (A2).

## Reciprocity

Declarations are only read as a set when they agree. Google: "If two pages don't both point to each
other, the tags will be ignored." (`google-localized-versions.txt` line 387). Nothing in RFC 5646 or
WHATWG carries a reciprocity requirement — it is a consumer rule, and the sources say so only for the
consumer that wrote the sentence.

Contract ids: `hreflang_nonreciprocal` for a manifest-internal target B that does not return an alternate
with A's `url` and the same tag; `hreflang_external_target` (informational) when B is outside the
manifest. Reciprocity is therefore decidable only inside the manifest — the manifest is the population,
never the web.

## The frozen contract's finding table

| id | decides |
|---|---|
| `hreflang_missing_value` | `<link rel="alternate">` with no hreflang value |
| `hreflang_invalid_tag` | value neither `x-default` nor a match of the frozen ASCII grammar (case-insensitive; `_` never accepted) |
| `hreflang_relative_href` | alternate `href` that does not parse as absolute with scheme and authority (A12) |
| `hreflang_duplicate_pair` | same (lowercased tag, exact href) twice on one page |
| `hreflang_multiple_xdefault` | more than one `x-default` on one page |
| `hreflang_self_missing` | a page with ≥1 alternate that does not list its own `url` |
| `hreflang_nonreciprocal` | manifest-internal target B lacks a return alternate with A's url and the same tag |
| `hreflang_external_target` | target outside the manifest — `severity: info`, never a policy finding, never a failing exit |
| `hreflang_canonical_not_self` | a page with ≥1 alternate whose resolved canonical is not its own `url` |

Input faults, exit 2: `input_unreadable`, `input_duplicate_url`, `input_url_not_absolute`. Exit 0 clean,
1 policy findings, 2 input faults (also when both, inputs win), 64 usage.

Amendment 2 fixes the mechanics the ids leave open, and they are part of the effective contract: a policy
finding is emitted once per offending annotation, except `hreflang_self_missing` and
`hreflang_canonical_not_self`, which are once per page (A2); tag equality is ASCII case-insensitive and
URL equality is exact after RFC 3986 normalization of both sides, with a trailing `/` significant (A3);
`hreflang_external_target` is `severity: info` and a run whose only findings are informational exits 0
(A1); an empty `hreflang` value is `hreflang_missing_value`, not `hreflang_invalid_tag` (A10); a `link`
without an `href` attribute is not an alternate and is not reported (A9); `x-default` compares
case-insensitively (A11); a manifest `version` other than 1 is exit 64, and a `file` that escapes
`--root`, is absolute, is a symlink or is not a regular file is `input_unreadable` (A15).

The tag grammar is frozen as
`^[A-Za-z]{2,3}(-[A-Za-z]{4})?(-([A-Za-z]{2}|[0-9]{3}))?(-([A-Za-z0-9]{5,8}|[0-9][A-Za-z0-9]{3}))*$`.
It is a strict subset of RFC 5646 §2.1's `langtag` (`rfc5646.txt` lines 231-236): it has no extlang
branch, no extension (`extension = singleton 1*("-" (2*8alphanum))`, line 255), no private-use branch
(line 265) and no grandfathered branch (lines 267-275). So `hreflang_invalid_tag` means "outside the
frozen grammar" and never "not a BCP 47 tag": `i-klingon` is a grandfathered tag RFC 5646 calls
well-formed, and the frozen grammar rejects it. RFC 5646's own split is the honest frame here — "A tag is
considered "well-formed" if it conforms to the ABNF (Section 2.1)." (lines 1053-1054, 13 words) and
"Language tags may be well-formed in terms of syntax but not valid in terms of content." (lines 1054-1055)
— and this audit checks only the syntax half.

Two consequences follow. First, the frozen grammar is wider than what Google says it supports: the
grammar accepts three-letter language subtags and three-digit regions, while Google's page states "Only
language codes listed in ISO 639-1 and region codes listed in ISO 3166-1 Alpha 2 are supported"
(lines 680-681, 19 words) and that codes outside those standards, such as `es-419`, "aren't supported"
(line 681, 13-word fragment). A rejected tag is a syntax verdict; an accepted tag is not a claim that any
consumer will use it. Second, case-insensitivity is sourced on both sides: "The hreflang value is
case-insensitive" (lines 682-684, 5 words) and "At all times, language tags and their subtags, including
private use and extensions, are to be treated as case insensitive" (`rfc5646.txt` lines 327-328, 20
words) — which is why the contract matches tags case-insensitively and lowercases them before comparing
pairs.

## Limits

Stated, never claimed closed:

- **No live fetch.** The audit reads the local files the manifest names and never requests a URL, so it
  cannot see a redirect, a 404, or what a server actually serves.
- **No HTTP headers, no `Vary`.** Header-delivered hreflang is a separate method in Google's own page —
  "There are three ways to indicate multiple language/locale versions of a page to Google:"
  (`google-localized-versions.txt` line 344, 14 words; heading "Methods for indicating your alternate
  pages" at line 343, the "HTTP Headers" body at line 505) — and is out of scope.
- **No rendering, no JavaScript.** Only static HTML in the file is read; anything a browser would
  construct is invisible.
- **No hreflang value outside `x-default`/BCP-47 syntax.** No other value form is interpreted, and no
  validity claim is made about the subtags that do appear.
- **No language detection.** The audit says nothing about the actual language of any page. WHATWG makes
  the attribute advisory and non-authoritative for user agents (lines 1355-1361) and Google disclaims it
  entirely for language detection (lines 355-360); a declaration audit is not a language audit.
- **No search-engine selection or ranking claim.** Nothing here says which variant an engine will pick,
  merge, serve or rank; Google's own reciprocity sentence is a statement about how it treats unpaired
  tags, not a promise about outcomes.
- **Manifest-internal only.** Self-reference, reciprocity and canonical checks are decidable only among
  manifest pages; an external target is reported as informational and never as a defect.
- **Absoluteness is a declaration rule, not an HTML validity rule.** WHATWG's `alternate` definition
  (lines 4036-4056) and its `hreflang` paragraph (lines 1349-1357) say nothing about whether `href` must
  be absolute; the requirement comes from Google's guideline and from the contract's
  `hreflang_relative_href`, which Amendment 2 A12 settles (scheme plus authority). A relative alternate
  is a policy finding here, never an HTML conformance verdict.
- **Informational findings do not fail a run.** `hreflang_external_target` is `severity: info`
  (Amendment 2 A1): an external target is reported and exits 0, so "clean" in this audit means "no
  decidable defect inside the manifest", not "no external targets".
- **Source volatility.** The Google body changed between two fetches on 2026-11-03: the retained body is
  199,246 B (sha256 `12fbe281…`), the re-fetch 199,242 B (sha256 `e41e3dca…`,
  `refetch-record.txt` `cmp=DIFFERS`). Quotes above are anchored to the retained body and the line numbers
  of its tag-stripped text; a 90-day recheck must re-locate them, not assume them.
