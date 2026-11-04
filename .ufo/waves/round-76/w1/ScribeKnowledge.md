# ScribeKnowledge — round 76, wave w1: prose drafts (fenced blocks for the L1)

Seat scope: draft only. Nothing below is applied; every block is the text the L1 commits. No file in
`corpus/` was written by this seat. All reads were read-only over the lane checkout; scratch was
`/fast/scratch/hyaku/kake-r76/ScribeKnowledge` (removed before yield).

Observations this draft rests on, each with the command that produced it (run from
`/home/vgpnk/Projects/shokunin/kake-shokunin`):

1. `TMPDIR=$S/tmp python3 -B .ufo/waves/round-76/c76_quote_truth.py --root . --revision a0491fcd --base a0491fcd --rounds 75,76 --work "$S/work"`
   → exit 1, `C1v1 revision=a0491fcd rows=19 receipt_files=10452 spans=30 exempted=0 corrections=0 findings=8 met=false`;
   `diff` against `.ufo/waves/round-76/controls/base-c1-quote-truth.txt` differs only in the revision token
   (`master` vs `a0491fcd`).
2. Same command with `--revision HEAD` → exit 0, `findings=0 met=true`, with `spans=30` unchanged, at two
   later tips: `783c7c13` (`receipt_files=10458`) and `6b52407b` (`receipt_files=10460`). No claim row was
   edited between any of these runs; only the receipt universe grew (the round-76 controls and amendments
   themselves became receipts).
3. Same command without `--base` → exit 64, `usage: --base <revision> is required (append-only conjunct)`.
4. `git show a0491fcd:LOG.md | sed -n '2533,2536p'` → the round-75 entry still carries the two stale digests
   routed as spot-check §6.1/§6.2 (no `[r75-correction …]` line exists: `git show a0491fcd:LOG.md | grep -n 'r75-correction'`
   prints nothing).
5. `git show a0491fcd:.ufo/waves/round-74/c74_registry_gap.py | sed -n '20,30p'` → the docstring still says
   "the five contract fixtures f1-f5" (spot-check §6.8 open at base).
6. `git show HEAD:corpus/knowledge/instrument-receipts.json | python3 -c '…'` → `population=18`, and the file
   list holds neither `c74_sidecar_reobserve.py` nor `scripts/sidecar_reobserve.py` (spot-check §6.4 open).
7. `sha256sum` over the scout's retained bodies (`.ufo/waves/round-76/w1/ScoutHreflangSources/`): see the
   `source:` line in block (a). `refetch-record.txt` records the Google body as `cmp=DIFFERS` on re-fetch.

---

## (a) `corpus/knowledge/hreflang-declaration.md`

```markdown
source: S444 — Google Search Central, Localized versions of your pages — https://developers.google.com/search/docs/specialty/international/localized-versions — §"Guidelines for all methods", §"HTML tags", §"Use the x-default value for unmatched languages"; tag-stripped text lines 340-423 and 726-740 of `.ufo/waves/round-76/w1/ScoutHreflangSources/google-localized-versions.txt` (25,035 B, sha256 96175da894ea426f894488468a61635665bf8735e9cfaef05ea24913d16a8788; raw body 199,246 B, sha256 12fbe2816a3643796fbe496f694c13ec895ad9533d2ba8210efe66af89dc8d7b); S445 — WHATWG HTML §4.6.3 API for hyperlink elements (`attr-hyperlink-hreflang`) and §4.6.8.1 Link type "alternate" — https://html.spec.whatwg.org/multipage/links.html — lines 1349-1361 and 4036-4056 of `whatwg-links.txt` (111,855 B, sha256 4254043fb66c1bfd1b2b0fbc528449fe2336abaad7f25fb8d1ab7d7f66df5375; raw 381,019 B, sha256 2f21e82b78d069ee01d61aca14a7b07832a4ab58b9633db88b45983a0f14eec3); S446 — RFC 5646 §2.1 Syntax and §2.2.9 Classes of Conformance — https://www.rfc-editor.org/rfc/rfc5646.txt — lines 195-275 and 1046-1057 (208,592 B, sha256 5d9515f053163c80e7294a84d18217dc83471acc7caa9773da2ac40deeec8228); all three fetched 2026-11-03 HTTP 200, retained under `.ufo/waves/round-76/w1/ScoutHreflangSources/`
verified-at: 2026-11-03
recheck: 90d
ground: operability — the offline hreflang declaration audit (round-76 contract C2)
scope: declaration syntax and the inter-page link rules two publishers state; nothing about selection, rendering, ranking or the language of any live page

TODO(L1): S444/S445/S446 are the ids the round-76 scout confirmed for the three sources it opened
(reply to this seat: "IDS (next free above S443): S444 = Google localized-versions; S445 = WHATWG
multipage/links.html; S446 = RFC 5646"). They were still absent from `corpus/SOURCES.md` when this block
was drafted (`grep -c '^| S44[4-9] ' corpus/SOURCES.md` → `0`; registry tip S443), so the rows must land
before or with this entry, and the `used-by` cell must name this file. No quote depends on the id.

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
```

## (b) `corpus/QUALITY.md` — round-76 addendum

```markdown
## Round-76 addendum — a claim-bearing quote is a receipt line or a marked elision (append-only)

Grounding: the round-75 non-author closure's routed defect 6 (`corpus/lessons/round-75-verifier-spotcheck.md`
§6: the round-75 criterion quoted the deletion control as `files=15 append_only=false met=false` against a
receipt line that carries `mismatches=2 classes=E3` between those fields), the frozen round-76 contract §C1
as amended — Amendment 3 §B1-§B6 in particular — and `corpus/lessons/round-76.md`. Instrument:
`.ufo/waves/round-76/c76_quote_truth.py` (v0, committed with the freeze), hardened this wave into
`scripts/doc_quote_truth.py` with the same predicate and a superset selftest; the population is the frozen
C1 population (claim rows of rounds 75–76; receipts = observed data under `.ufo/waves/**`; dispatcher
artifacts and any `*.ready*` file are never receipts).

- **A claim-bearing quote is either the whole receipt line or an explicit elision whose fragments each
  occur in the same receipt, and a correction closes a defective quote only by quoting the whole line and
  naming the defective span.** Admit: the quoted span is a whole receipt line — exact equality with a
  receipt line after trimming leading and trailing whitespace (Amendment 3 §B3); or every non-empty
  fragment of a span that carries a marked elision (`…`, `[...]`, `...`) occurs inside one receipt file; or
  the span is a 7–40 character lowercase hex token that resolves as a commit object at the measured
  revision (§B1 revision citation), while a 64-character lowercase hex token is a digest and must be
  contiguous in a receipt; or an appended correction line (`[rNN-correction …]` or `supersedes`) quotes a
  receipt line whole and names the defective span, where "names" means the identical span is a `T1`/`T2`
  finding at the `--base` revision (§B3-bis) and the row carries no fabricated claim-bearing span of its
  own.
  Reject: an unmarked elision of an interior token — `files=18 mismatches=0 append_only=true met=true
  missing_frozen=0` against the receipt line `C1v1 revision=f87d14a9 rows=32 live=20 files=18 mismatches=0
  classes=- append_only=true met=true missing_frozen=0` drops `classes=-` and is not contiguous; a span
  stitched from two adjacent receipt lines without an elision marker, as `population=18 bound=18
  mismatches=0 met=true missing_frozen=0` stitches `C2v1 … mismatches=0 met=true` to the following
  `population: … missing_frozen=0` line; a correction quote that is only a fragment of a receipt line;
  deleting or rewriting the defective row (append-only compares exact text, so a whitespace-only rewrite is
  `A1` like a deletion, §B4, and a rewrite withdraws the repair); a correction that quotes no receipt line
  (`T4`) or quotes one no receipt contains. **Receipt universe conjunct:** the receipt that carries the
  span must be committed at or before the revision that carries the claim row, and the measured run must
  report the `--base` universe — a span made contiguous only by a file committed afterwards (for example a
  control receipt that itself prints the finding) is laundering, not repair.
- Able-to-fail: `python3 -B .ufo/waves/round-76/c76_quote_truth.py --root . --revision a0491fcd --base
  a0491fcd --rounds 75,76` prints the whole line `C1v1 revision=a0491fcd rows=19 receipt_files=10452
  spans=30 exempted=0 corrections=0 findings=8 met=false`, exit 1
  (`.ufo/waves/round-76/controls/base-c1-quote-truth.txt` line 1, which carries the same line with
  `revision=master`; the two runs differ in that token only). Under Amendment 3 §B6 the effective
  before-state is the re-measurement (`findings=7`: the v1 eight included one duplicate physical row and
  counted two revision citations as spans), committed as `controls/base-c1-quote-truth-v2.txt`; if that
  receipt is not in the tree when this criterion lands, the v1 line above is the only able-to-fail evidence
  a reader can run, and the criterion must not assert a seven it cannot show. The same command at
  `--revision HEAD` (`6b52407b`) prints `C1v1 revision=HEAD rows=19 receipt_files=10460 spans=30
  exempted=0 corrections=0 findings=0 met=true`, exit 0, with `spans=30` unchanged and no claim row
  edited: the finding count fell because eight more files entered the receipt universe, which is why the
  conjunct above pins the universe to `--base`.

Criteria are not rewritten: this section is the round-76 addendum, and every earlier criterion stands
unchanged.
```

## (c) `corpus/lessons/round-76.md` — skeleton (L1 fills the placeholders)

```markdown
# Round 76 — lessons (kake, attempt 1)

Base `a0491fcd041cbc3fff2c964ecf6268557e45a5c1` (lane master at round open). Frozen contract
`.ufo/waves/round-76/contract.md` at `b758cb04`; Amendment 1 at `783c7c13` (terms-only: the C2 real-input
population is the **8** retained served pages, not the 12 the frozen sentence names — the other four retain
`audit.json` + `fetch.json` only); Amendment 2 at `e674bc60` (decides the 16 classes the frozen terms left
undecidable, A1-A17); Amendment 3 at `6b52407b` (revision-versus-digest split, section identity, whole-line
correction closure, exact append-only, `*.ready*` never a receipt, and the re-measured before-state B6).
Each amendment is terms-only and recorded before any after-state. Measured at `<MEASURED_REV — L1 fills with
the lane tip the after-state was measured at>`. Wave `w1`: one v1 wave, 14 seats, the L1 holding the planner
seat.

## Claims

**C1 — calibration (owned score 2).** A round's claim rows stop quoting command output that no committed
receipt contains: every claim-bearing backticked span in the effective claim rows of rounds 75–76 is a
contiguous substring of a committed receipt, or carries an explicit elision whose fragments are
contiguous, or is closed by a correction line that itself quotes a validated receipt line and names the
defective span. Counter `.ufo/waves/round-76/c76_quote_truth.py` (v0) hardened into
`scripts/doc_quote_truth.py`; `met = (findings == 0) and append_only`.

**C2 — operability (capability acquisition: offline hreflang declaration audit).** The lane can audit
hreflang declarations offline on a versioned manifest: the new tool decides every frozen contract case
correctly, every degenerate constant control fails at least one case, its own selftest passes, and it
runs end-to-end on the 12 retained real surfaces. Tool `scripts/hreflang_audit.py` (`--manifest`,
`--root`, `--json`, `--selftest`, `--work`); findings `hreflang_missing_value`, `hreflang_invalid_tag`,
`hreflang_relative_href`, `hreflang_duplicate_pair`, `hreflang_multiple_xdefault`, `hreflang_self_missing`,
`hreflang_nonreciprocal` / `hreflang_external_target`, `hreflang_canonical_not_self`; exit 0 clean, 1
policy, 2 input fault, 64 usage. Amendment 1 fixes the real-input population at 8 retained pages, with
the four not-served surfaces reported as `not-served (no retained bytes)`.

## Gate

- **Admit — S444, Google Search Central, Localized versions of your pages.** Row `<L1: paste the
  scout's contract-v1 row>`. https://developers.google.com/search/docs/specialty/international/localized-versions,
  opened 2026-11-03, HTTP 200, 199,246 B retained (sha256 `12fbe281…dc8d7b`; tag-stripped text 25,035 B,
  sha256 `96175da8…a8788`), retained at `.ufo/waves/round-76/w1/ScoutHreflangSources/`. Located quote
  (13 words, §"Guidelines for all methods", `google-localized-versions.txt` lines 362-364): "Each language
  version must list itself as well as all other language versions." Teaches: the self-reference rule the
  entry's `hreflang_self_missing` rests on. Status `mined` (the C2 entry cites it). Admit.
- **Admit — S445, WHATWG HTML, the `hreflang` attribute and link type "alternate".** Row `<L1: paste the
  scout's contract-v1 row>`. https://html.spec.whatwg.org/multipage/links.html, opened 2026-11-03, HTTP
  200, 381,019 B (sha256 `2f21e82b…eec3`; tag-stripped 111,855 B, sha256 `4254043f…5375`), retained at
  `.ufo/waves/round-76/w1/ScoutHreflangSources/`. Located quote (10 words, §4.6.3
  `attr-hyperlink-hreflang`, `whatwg-links.txt` line 1356): "The value must be a valid BCP 47 language
  tag." Teaches: the tag requirement, plus the advisory/non-authoritative clauses the entry's language
  limit quotes. Status `mined`. Admit.
- **Admit — S446, RFC 5646 (BCP 47), §2.1 Syntax and §2.2.9 Classes of Conformance.** Row `<L1: paste the
  scout's contract-v1 row>`. https://www.rfc-editor.org/rfc/rfc5646.txt, opened 2026-11-03, HTTP 200,
  208,592 B (sha256 `5d9515f0…8228`), retained at `.ufo/waves/round-76/w1/ScoutHreflangSources/`. Located
  quote (13 words, lines 1053-1054): "A tag is considered "well-formed" if it conforms to the ABNF
  (Section 2.1)." Teaches the well-formed/valid split that scopes `hreflang_invalid_tag` to syntax.
  Status `mined`. Admit. A second located quote the entry also uses (20 words, §2.1.1, lines 327-328):
  "At all times, language tags and their subtags, including private use and extensions, are to be treated
  as case insensitive".
- **Row cells and quote evidence** are in `.ufo/waves/round-76/w1/ScoutHreflangSources.md` §4 (rows) and
  §5 (Gate evidence, one URL + access date + located quote per row); the three ids are the scout's own.
- **Quote verification for the three rows.** `ScoutHreflangSources/verify_quotes.py` → `verify-output.txt`:
  `quotes=17`, `failures=0`, every line `exact=true` with the derived range equal to the quoted range.
- **Reject — `<L1: any scout/edge candidate the round refuses>`.** `<reason + flip condition>`.
- **Assimilation.** `<L1: merge/kake/ re-checked read-only; "Assimilation: none" if the staged entries'
  locators still do not re-ground, with the blocker named (round-75 precedent)>`.
- **Census.** `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` →
  `<observed rows>` after S444-S446 land; before: 181 rows, exit 0 (`controls/census-before.txt`: `181`,
  `census-exit: 0`).
- **Stated limit (observed while drafting).** The C1 before-state is measured at a revision whose receipt
  universe excludes the round-76 controls; at the later tips the same command reads `receipt_files=10458 …
  findings=0 met=true` (`783c7c13`) and `receipt_files=10460 … findings=0 met=true` (`6b52407b`) over the
  unchanged `spans=30`. The report must name both universes, or an empty correction set will look like a
  repair.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| An **unmarked elision** inside a claim-bearing quote: the row quotes an interior slice of a receipt line (or stitches two lines of it) without a marker, so the claim cannot be re-derived from the bytes it cites. Two instances named by the round-75 closure survived into round 76 because the control that would have carried the fragment was committed after the before-state was measured | `corpus/QUALITY.md:1499` and `corpus/lessons/round-75.md:82` quote `files=15 append_only=false met=false` against a line carrying `mismatches=2 classes=E3` between those tokens; `SCORECARD.md:4892` quotes `files=18 mismatches=0 append_only=true met=true missing_frozen=0` against the receipt line `C1v1 revision=f87d14a9 rows=32 live=20 files=18 mismatches=0 classes=- append_only=true met=true missing_frozen=0`; `SCORECARD.md:4893` stitched `receipt: source=committed declared_valid=true` from a line that also carries `worktree=identical declared=abfbfaac… declared_match=false`; the SCORECARD rows and both lesson/criterion spans are the seven `T1` findings that Amendment 3 §B6 records for `controls/base-c1-quote-truth-v2.txt` — the receipt itself was absent from the tree when this lesson was drafted, so the seven is the amendment's claim, not this seat's measurement; the committed v1 receipt counts eight (`SCORECARD.md:4904` twice as one physical row counted under two overlapping headings, plus two revision citations at `corpus/lessons/round-75.md:102`) | the frozen C1 counter at the base revision (`.ufo/waves/round-76/c76_quote_truth.py`, `--revision a0491fcd --base a0491fcd`: `findings=8 met=false`, exit 1) and the round-75 non-author closure (R6, `corpus/lessons/round-75-verifier-spotcheck.md` §6) — the check existed in round 75 and was pointed at the wrong population (a deletion control, not the line the quote came from) | append a correction row per defective span that quotes the whole receipt line and names the defective span (block (b) of `w1/ScribeKnowledge.md`); never rewrite the historical line, and pin the receipt universe to `--base` so a later-committed control cannot make the span contiguous |

## Routed dispositions

`fixed` / `open` below are read from committed bytes at the base revision; nothing here claims a check
was run that was not. Rows 1-8 are `corpus/lessons/round-75-verifier-spotcheck.md` §6; rows 9-13 are
`corpus/lessons/round-75.md` §Routed. Row 4 of the spot-check and row 12 are the same docstring.

| # | Routed item | Status | Pointer | Flip condition |
|---|---|---|---|---|
| 1 | Stale counter digest in `LOG.md:2534` (`0699a672…` at `4e3fc159` vs `63e321b2…` at the tip) | open | `git show a0491fcd:LOG.md \| sed -n '2534p'`; `git show 0df52aed:.ufo/waves/round-75/c75_row_truth.py \| sha256sum` → `63e321b2…`; no `[r75-correction` line exists | an appended correction names `63e321b2…`, the superseded `0699a672…`, and quotes the digest line whole |
| 2 | Stale receipt digest in `LOG.md:2535` (`18 entries, f3128628…` vs `15768f81…`) | open | same `LOG.md` entry; `git show 0df52aed:corpus/knowledge/instrument-receipts.json \| sha256sum` → `15768f81…` | one appended correction row covering 1 and 2, quoting the receipt's `receipt_sha256` line whole |
| 3 | Revision labels disagree with their own evidence (after-cells say `f87d14a9` under a `6c10b433` heading; `3ae076ab` called "measured"; battery measured at `306fff49`) | open | `SCORECARD.md:4882-4900`; `controls/after-harm-battery.txt:21` (`revision=306fff49…`) | the round-76 report and lesson state one measured revision per artifact and no artifact names two |
| 4 | R5 only partly closed: `c74_sidecar_reobserve.py` and `scripts/sidecar_reobserve.py` have no committed sha256 receipt (and no registry row) | open | `git show HEAD:corpus/knowledge/instrument-receipts.json` → 18 paths, neither sidecar file present | the two paths enter the receipt (and a registry row), or the report says they stay open |
| 5 | Round-74 R3 undispositioned: the sweep delta (193 → 195 files, 6 → 7 unannotated cites) is recorded nowhere | open | `corpus/lessons/round-74-verifier-spotcheck.md` R3; no later lesson carries the numbers | the round-76 lesson or report records the delta and the sweep class it leaves red |
| 6 | `QUALITY.md` able-to-fail quote not a contiguous substring (`files=15 append_only=false met=false`) | open at base (one of the base `T1` findings: eight under the v1 receipt, seven under Amendment 3 §B6) | `.ufo/waves/round-76/controls/base-c1-quote-truth.txt:9` (`T1 corpus/QUALITY.md:1499 …`) | block (b) lands: the appended criterion quotes a receipt line whole and the base finding is closed by a correction row rather than by deleting the old criterion |
| 7 | C2 quotation scope: the after-quote omits `declared_match=false`, and the 16-forgery matrix ran on the predecessor tool blob `62b795ea…`, not the landed `162dd685…` | open | `controls/after-c2-receipts.txt:7` (`declared=abfbfaac… declared_match=false`); `LOG.md:2535` | the report discloses the subject/carrier split, or the matrix is re-run on the landed blob with its receipt |
| 8 | Superseded docstring `.ufo/waves/round-74/c74_registry_gap.py:25` still says "the five contract fixtures f1-f5" | open | `git show a0491fcd:.ufo/waves/round-74/c74_registry_gap.py \| sed -n '25p'` | an appended docstring correction or an erratum names the count and the eight fixtures |
| 9 | E2 ambiguity (ReviewerC1 F15): a cell with two different `a/b` tallies passes on the last pair | open | `corpus/lessons/round-75.md` §Routed 1; `corpus/QUALITY.md:1503-1504` reads it as ambiguous | a frozen predicate defines multi-pair cells (reject, or first pair, or `ambiguous`) |
| 10 | `--base` optional in `c75_row_truth.py`: without it `append_only=true` is evidence-free | fixed in the successor, open in the frozen instrument | `python3 -B .ufo/waves/round-76/c76_quote_truth.py --root . --revision HEAD --rounds 75,76` → exit 64, `usage: --base <revision> is required (append-only conjunct)`; `c75_row_truth.py:454` unchanged | the round-75 counter is re-pinned or the registry row states the requirement (it already does) and the frozen file is left frozen |
| 11 | Carrier receipt outside the rewrite watch (`c58_receipt_rewrites.py` watches `controls/`, not `corpus/knowledge/`) | open (operator) | `corpus/lessons/round-75.md` §Routed 3; receipt identity bound only by `receipt_sha256` in `controls/after-c2-receipts.txt:2` | the checker's watched population includes the carrier path, or `tool_sha256` enters the receipt schema as an operator decision |
| 12 | Superseded docstring (round-75 §Routed 4) — same defect as row 8 | open | `corpus/lessons/round-75.md` §Routed 4 | as row 8; one correction closes both |
| 13 | Host-absolute paths in committed evidence (`/fast/scratch/...`) | open (operator) | `corpus/lessons/round-75.md` §Routed 5; the class is already in the repo | the operator rules on public-facing path policy; until then new receipts use relative paths where the tool allows |

## Sources

- **S444 — Google Search Central, Localized versions of your pages** (opened 2026-11-03, HTTP 200,
  199,246 B retained, sha256 `12fbe281…dc8d7b`): located quote, 13 words, §"Guidelines for all methods"
  `google-localized-versions.txt` lines 362-364: "Each language version must list itself as well as all
  other language versions." Row status `mined` — the C2 entry cites it (self-reference, `x-default`,
  absolute hrefs, limits). The body changed between two fetches the same day (`refetch-record.txt`
  `cmp=DIFFERS`); quotes are anchored to the retained bytes and their line numbers.
- **S445 — WHATWG HTML, §4.6.3 `attr-hyperlink-hreflang` and §4.6.8.1 Link type "alternate"** (opened
  2026-11-03, HTTP 200, 381,019 B, sha256 `2f21e82b…eec3`): located quote, 10 words, `whatwg-links.txt`
  line 1356: "The value must be a valid BCP 47 language tag." Row status `mined` — the C2 entry cites the
  tag requirement and the advisory clause. Re-fetch at the same URL was byte-identical (`cmp=IDENTICAL`).
- **S446 — RFC 5646 (BCP 47), §2.1 Syntax, §2.1.1 Formatting and §2.2.9 Classes of Conformance** (opened
  2026-11-03, HTTP 200, 208,592 B, sha256 `5d9515f0…8228`): located quote, 13 words, lines 1053-1054:
  "A tag is considered "well-formed" if it conforms to the ABNF (Section 2.1)." Row status `mined` — the
  C2 entry cites it for the well-formed/valid split the frozen grammar is scoped to. Re-fetch
  byte-identical.
- The scout's own quote receipt is `.ufo/waves/round-76/w1/ScoutHreflangSources/verify-output.txt`
  (`quotes=17`, `failures=0`, produced by `verify_quotes.py` beside it); the line ranges above were
  re-read by this seat and the three states (`mined`) match the entry's citations.
- C1 rests on lane instruments and committed receipts, not on a web source: the predicate is contract
  §C1, the counter `.ufo/waves/round-76/c76_quote_truth.py`, the controls under
  `.ufo/waves/round-76/controls/`, and the eight base findings re-run by this seat at `--revision
  a0491fcd` (byte-identical to the committed control up to the revision token).
- The canonical-interaction rule has **no opened source**: `grep -n 'canonical'
  google-localized-versions.txt` returns navigation links only. It is recorded in the knowledge entry as
  the contract's policy; registry rows S020/S021 were not re-opened this round and are not quoted.
```

## (d) Optional — `corpus/README.md` coverage rows (L1 may skip)

```markdown
| hreflang declarations (r76) | `knowledge/hreflang-declaration.md` | declaration syntax, self-reference, `x-default`, absolute hrefs, canonical policy vs reciprocal pairs; the C2 finding table and its stated limits |
```

---

## Findings for the L1 and the canonical judge (conflicts reported, not smoothed)

1. **The C1 target is reachable at the freeze commit with no repair.** Same counter, same rounds, same
   `--base`, only `--revision` changed: at `a0491fcd` `receipt_files=10452 … findings=8 met=false`, exit 1;
   at `HEAD` (`6b52407b`) `receipt_files=10460 … findings=0 met=true`, exit 0, with `spans=30` unchanged.
   The added receipts are the round-76 controls and amendments, which print or carry the offending spans
   as their own text. Kill rule 1 names the controls reaching `met=true`; here the *tree that contains the
   controls* does, which is the same effect one step removed. Block (b) pins the receipt universe to
   `--base` for exactly this reason; whether C1 survives as stated is the judge's call, not this seat's.
2. **The contract's before-state sentence is not a receipt line.** Contract §C1 "Before" quotes
   `rows=19 receipt_files=10452 spans=30 exempted=0 corrections=0 append_only=true findings=8 met=false`;
   the counter prints no `append_only` field at all (`grep -n append_only .ufo/waves/round-76/c76_quote_truth.py`
   → the variable at lines 251/256/300/303, no print of it), and the committed receipt line 1 is
   `C1v1 revision=master rows=19 receipt_files=10452 spans=30 exempted=0 corrections=0 findings=8 met=false`
   (`.ufo/waves/round-76/controls/base-c1-quote-truth.txt:1`). The inserted token breaks contiguity — the
   very class the round exists to close. Amendment 3 B6 replaces the *count* but not this sentence.
3. **The control table's deletion row quotes a token its receipt does not carry on the summary line.**
   Contract §C1 controls say `append_only=false`; `ctl-deletion.txt:1` is
   `C1v1 revision=master rows=19 receipt_files=10452 spans=26 exempted=0 corrections=0 findings=7 met=false`
   (the token appears only inside its `T1` finding lines). Also `ctl-do-nothing.txt` is byte-identical to
   `base-c1-quote-truth.txt` (both sha256 `8230f403a7f56ce6695eb6629cc6d05b87810af5cb20245b38dd257017df8e0c`),
   so "before" and "do-nothing" are one receipt, not two independent controls.
4. **The committed base receipt does not record the resolved revision.** It says `revision=master`; a
   literal re-run today measures `6b52407b` and prints `findings=0`. Reproduction requires
   `--revision a0491fcd`, which is what this seat used to obtain the byte-identical control (differs only
   in the revision token). Any judge re-running `--revision master` will not reproduce the before-state.
5. **Amendment 1 names an unresolvable object.** `amendment-1.md` says "`contract.md` at `b758cb04`
   (`4d5c1c25…` blob)"; `git cat-file -t 4d5c1c25` → `fatal: Not a valid object name 4d5c1c25`, and
   `git rev-parse b758cb04:.ufo/waves/round-76/contract.md` → `a0c5467c699a1baf8e1d331894b0f7d4293fa376`.
   The contract bytes at the named commit and at `HEAD` hash to `a0c5467c…`.
6. **C2's population is stated twice, differently.** The frozen sentence says "12 retained real
   surfaces"; Amendment 1 (terms-only, before any after-state) says 8, and the block (c) Claims text
   keeps the verbatim sentence and names the amendment beside it so a reader sees both.
7. **Neither wave tool exists at draft time.** `ls scripts/doc_quote_truth.py scripts/hreflang_audit.py`
   → both `No such file or directory`. Block (b)'s able-to-fail command uses the committed v0 path, so
   the criterion is executable today; the hardened path is named as the wave's deliverable, not as a
   present fact.
8. **Both divergences I flagged at draft time are now resolved in terms, and one became a stated limit.**
   (i) `hreflang_relative_href` was worded "without scheme and host" while the Google guideline rejects
   `//host/x`; Amendment 2 A12 settles it (absolute = scheme plus authority, so the protocol-relative shape
   is a finding) and the knowledge entry states the decision instead of calling it undecided. (ii) The
   frozen grammar accepts three-letter language subtags and three-digit regions while Google supports only
   ISO 639-1 language codes and ISO 3166-1 Alpha 2 region codes (`es-419` unsupported); that is not a
   contract defect but a scope statement, and the entry records it as "a rejected tag is a syntax verdict;
   an accepted tag is not a claim that any consumer will use it".
9. **Source volatility already observed.** The Google body differed between two fetches minutes apart
   (199,246 B retained, sha256 `12fbe281…`; 199,242 B re-fetch, sha256 `e41e3dca…`;
   `refetch-record.txt` `cmp=DIFFERS`). The knowledge entry's quotes and line numbers are pinned to the
   retained bytes, and its recheck is 90d.
10. **S-ids S444-S446 are confirmed by the scout, not yet registered.** The registry tip is S443 and
    `grep -c '^| S44[4-9] ' corpus/SOURCES.md` → `0` at draft time; the scout's reply confirms the three
    ids and supplies verified anchors (`verify-output.txt`: `quotes=17`, `failures=0`), and block (a)
    carries a `TODO(L1)` so the rows land before the entry. No quote depends on the id.
11. **Amendment 3's B6 receipt is named but absent.** `amendment-3.md` §B6 says "The re-measured receipt is
    `controls/base-c1-quote-truth-v2.txt`"; at `6b52407b` neither the working tree nor `git ls-tree -r HEAD`
    contains that path (`ls` → `No such file or directory`; the tracked controls are the seven v1 files plus
    `sweep-r76.txt`). The `findings=7` figure is therefore the amendment's claim, not an observation this
    seat could make or reproduce; block (b) says so in the criterion itself and keeps the v1 whole-line
    quote as the only runnable able-to-fail evidence.
12. **Amendment 3's B6 arithmetic is grounded.** The duplicate it names is real in the v1 output
    (`SCORECARD.md:4904` appears twice), and `git show a0491fcd:corpus/lessons/round-75.md | grep -n
    '6c10b433\|ca1a2982'` hits line 102, the bulk-substitution row, so the two revision citations it says
    v1 counted as spans are on that line. What is unverified is the seven itself, not its rationale.
