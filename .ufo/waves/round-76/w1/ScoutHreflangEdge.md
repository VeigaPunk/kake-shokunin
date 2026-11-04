# ScoutHreflangEdge — C2 edge-class reconnaissance for the frozen case matrix

Seat: `ScoutHreflangEdge`, kake lane round 76 w1, base `a0491fcd041cbc3fff2c964ecf6268557e45a5c1`.
Scope: enumerate the edge classes a correct offline hreflang audit must decide, with the deciding
sentence, the expected verdict under contract §C2, the degenerate constant each class catches, and every
class the contract cannot decide. No edits anywhere but this file; no network beyond the three public
GETs below.

## 0. Evidence base and how to check it

Citation convention: `file:Lstart-Lend` where `file` is a retained file in
`.ufo/waves/round-76/w1/ScoutHreflangSources/` (the sibling scout's retained bytes) or a lane path.
Quotes are exact substrings of the cited lines.

Retained sources (access 2026-11-03, `curl -sSL --max-time 30`):

| File | sha256 | bytes |
|---|---|---|
| `ScoutHreflangSources/google-localized-versions.html` | `12fbe2816a3643796fbe496f694c13ec895ad9533d2ba8210efe66af89dc8d7b` | 199246 |
| `ScoutHreflangSources/google-localized-versions.txt` | derived text, 25035 | — |
| `ScoutHreflangSources/whatwg-links.html` | `2f21e82b78d069ee01d61aca14a7b07832a4ab58b9633db88b45983a0f14eec3` | 381019 |
| `ScoutHreflangSources/rfc5646.txt` | `5d9515f053163c80e7294a84d18217dc83471acc7caa9773da2ac40deeec8228` | 208592 |

Checks I ran and what they printed:

1. My own independent GET of the three URLs (scratch `/fast/scratch/hyaku/kake-r76/ScoutHreflangEdge/src`)
   returned `200` for all three; `whatwg-links.html` and `rfc5646.txt` are **byte-identical** to the
   sibling's retained copies (`sha256sum` lines above match mine exactly). The Google page is **not**
   byte-stable: my copy has the same length (199246) but sha256
   `7410b29b7ba4f28d3fc77eae7329a2e3276e119dbc0e16f81a9efa07426e7f97` — a dynamic field differs. Therefore
   every Google citation below names the **retained** `.txt` and its line numbers, not my copy.
2. `sed -n '355,370p' …/google-localized-versions.txt` and the greps in §2 reproduce every quote at the
   line numbers cited.
3. Retained-surface facts in §6 come from
   `for d in .ufo/waves/round-23/live/*/; do … ls "$d" … done` (12 dirs, 8 with `page.html`),
   `sha256sum` vs `fetch.json.sha256` (8/8 MATCH), and
   `grep -ac 'hreflang' .ufo/waves/round-61/capture/*/body.bin` (0 in all four).
4. Installed/upgraded tools: none. Nothing added to any PATH directory; scratch is deleted at seat close.

Verdict vocabulary: `clean` = exit 0, `ids=[]`; a finding id = exit 1; `input_*` = exit 2.
Constant legend used in the "caught by" column: **N** = no-op reader, **C** = always-clean,
**R** = report-all, **E** = empty-list reader (returns no links).

## 1. What each constant is caught by — and the one thing the matrix cannot show

Checking the four constants against `{exit, ids}` case by case:

- **N** (no-op reader, prints nothing, exit 0) fails every case expecting exit 1 or 2. It passes clean
  cases only if the counter accepts "no output" as `{exit: 0, ids: []}` — so the counter must require a
  parseable object (§3 A16), otherwise N passes every clean row by printing nothing.
- **C** (parses, never reports) fails every case with a non-empty expected `ids`: all policy findings, and
  the informational external-target class.
- **R** (reports every page) fails every case with an empty expected `ids`: any clean row, including the
  seven-valid-tags row, the same-tag-two-hrefs row and the zero-alternates row.
- **E** (reader returns no links) fails every policy-finding class, because every policy predicate is
  link-derived: no links ⇒ no `invalid_tag`, `missing_value`, `relative_href`, `duplicate_pair`,
  `multiple_xdefault`, `self_missing`, `nonreciprocal` or `canonical_not_self`.

So each constant is rejected, and the contract's control rule ("A constant that passes every case
withdraws C2") is satisfiable. Two honest qualifications belong in the matrix receipt:

1. **C and E have the same failure profile.** Both answer `exit 0, ids []` to every fixture a correct tool
   answers `exit 1` to, and both agree on every clean fixture and (if they validate the manifest) every
   input fault. The matrix therefore proves that E is rejected, not that E is a *distinct*
   reader-replacement: an E implementation that silently returned `[]` for every page for the wrong reason
   would score identically to a faithful one. Distinguishing them needs a JSON field the contract does not
   fix (e.g. per-page alternate counts), i.e. a contract change, not a matrix fix. Record the limitation
   rather than implying four distinguishable controls.
2. **The external-target class is still mandatory**, for a different reason: it is the only fixture whose
   correct answer is `exit 0` with a **non-empty** `ids`. That is what catches the very likely
   implementation error `exit = 1 if findings else 0`, which no other class can catch.

Both points depend on `hreflang_external_target` being listed in `findings` while leaving the exit at 0.
The contract's parenthetical "(informational)" does not say that, so until amendment A1 lands, an
external-target fixture is not contract-derivable and the tool bug above has no matrix guard.

## 2. Classes the contract decides

Rule column cites the deciding text. All are derivable from §C2's own sentences; tag rows are derivable
because the contract quotes its grammar verbatim.

### 2A. Valid tags (class 1 of the item)

Shape: one manifest page `A = https://a.test/`, page `A` has seven `<link rel="alternate" hreflang=X
href="https://a.test/">` lines, canonical self, one tag per line.

| # | `hreflang` value | Verdict | Deciding rule |
|---|---|---|---|
| 1 | `en` | clean | grammar group 1 `[A-Za-z]{2,3}` |
| 2 | `en-GB` | clean | group 1 + region `[A-Za-z]{2}` |
| 3 | `zh-Hant` | clean | group 1 + script `[A-Za-z]{4}` |
| 4 | `zh-Hant-TW` | clean | script then region, both in order |
| 5 | `es-419` | clean | region `[0-9]{3}` — **but Google says unsupported, see §4 D2** |
| 6 | `de-CH-1901` | clean | region `-CH` then variant `[0-9][A-Za-z0-9]{3}` |
| 7 | `x-default` | clean | "value neither `x-default` nor a well-formed BCP-47 tag" |

One page carrying all seven is a single clean case: distinct tags, so no `hreflang_duplicate_pair`; each
href is the page's own url, so `hreflang_self_missing` is satisfied; canonical self. Caught by: **R**
(and by any over-strict grammar in the real tool, e.g. one that rejects `es-419` as a region-not-language
form — see §4 D2).

### 2B. Case and invalid tags (class 2 of the item)

| # | value | Verdict | Deciding rule |
|---|---|---|---|
| 8 | `EN-gb` | **clean** | contract grammar is "(case-insensitive)"; RFC 5646 §2.1.1 (`rfc5646.txt:L326-331`): "language tags and their subtags … are to be treated as case insensitive"; Google `google-localized-versions.txt:L683-687`: "The hreflang value is case-insensitive" |
| 9 | `en_US` | `hreflang_invalid_tag` | grammar is ASCII-only, "`_` never accepted" |
| 10 | `english` | `hreflang_invalid_tag` | 7-letter primary fails `[A-Za-z]{2,3}` |
| 11 | `en-` | `hreflang_invalid_tag` | trailing `-` with empty subtag fails `$` |
| 12 | `x-defaults` | `hreflang_invalid_tag` | not `x-default`; `[A-Za-z]{2,3}` cannot match `x` |
| 13 | `i-klingon` | `hreflang_invalid_tag` | 1-letter primary; RFC makes it a *valid* irregular grandfathered tag (`rfc5646.txt:L276`) — see §4 D1 |
| 14 | `en GB` | `hreflang_invalid_tag` | SPACE is not in the frozen grammar |
| 15 | `en--GB` | `hreflang_invalid_tag` | empty subtag between hyphens |
| 16 | ` en ` (padded) | `hreflang_invalid_tag` | `^…$` anchors reject surrounding whitespace |

**Item premise correction.** The item lists `EN-gb` under "invalid tags". Per the contract's own
"(case-insensitive)" and both sources, `EN-gb` is **valid**; the case must expect clean. This is not a
contract defect — it is a defect in the item text, and the matrix seat must not copy it.

Caught by (rows 9–16 as one 8-link page, expected 8× `hreflang_invalid_tag`, exit 1): **N, C, E**; a
case-insensitive-but-`_`-tolerant implementation is caught by row 9; a registry-validating implementation
is caught by rows 8 and 13.

### 2C. Tags the frozen grammar rejects although BCP 47 calls them well-formed

This is the batch that separates a contract-faithful tool from one that calls a BCP-47 library. RFC 5646
`ABNF: langtag = language ["-" script] ["-" region] *("-" variant) *("-" extension) ["-" privateuse]`
(`rfc5646.txt:L231-241`), with `extlang = 3ALPHA *2("-" 3ALPHA)` (`:242-244`), `extension = singleton
(2*8alphanum)` (`:255`), `privateuse = "x" 1*("-" (1*8alphanum))` (`:265`), `grandfathered = irregular /
regular` (`:267-294`; `regular` continues at `:296-305`), and "A tag is considered 'well-formed' if it conforms to the ABNF …"
(`:1053-1054`).

| # | value | Contract verdict | BCP-47 status | Divergence |
|---|---|---|---|---|
| 17 | `x-private` | `hreflang_invalid_tag` | well-formed, privateuse (`:265`) | grammar has no `x-` branch |
| 18 | `en-a-bbb` | `hreflang_invalid_tag` | well-formed, extension (`:255`) | grammar has no singleton branch |
| 19 | `zh-yue-HK` | `hreflang_invalid_tag` | well-formed, extlang (`:242-244`) | grammar has no extlang slot |
| 20 | `en-u-ca-gregory` | `hreflang_invalid_tag` | well-formed, extension | same |
| 21 | `sgn-BE-FR` | `hreflang_invalid_tag` | well-formed, irregular grandfathered (`:267-294`; `sgn-BE-FR` at `:292`) | grammar rejects the 3rd subtag |
| 22 | `en-GB-oed` | `hreflang_invalid_tag` | well-formed, irregular grandfathered (`en-GB-oed` at `:270`, `i-klingon` at `:276`) | variant slot rejects `oed` |
| 23 | `abcdef` (6-letter primary) | `hreflang_invalid_tag` | well-formed, `5*8ALPHA` language | grammar caps primary at 3 |

I could not construct a string the frozen grammar accepts that RFC 5646's `langtag` rejects — the
containment runs the other way. [INFERENCE; read off the productions at `rfc5646.txt:L231-265`, not
exhaustively enumerated.] Consequence for the build: the tool's Limits line must say the audit admits
**only the frozen subset**, not "BCP-47"; otherwise the claim and the behaviour diverge on rows 17–23.
The contract's Limits phrase "no `hreflang` value outside `x-default`/BCP-47 syntax" constrains *claims*,
not admission, so it does not resolve this.

Caught by: one page carrying rows 17–23 as seven alternates, expected 7× `hreflang_invalid_tag`, exit 1 →
**N, C, E**; a library-backed implementation is caught specifically here.

### 2D. href forms (class 3 of the item)

| # | shape | Verdict | Deciding rule |
|---|---|---|---|
| 24 | `href="/de/"` | `hreflang_relative_href` | "`href` without scheme and host" |
| 25 | `href="#de"` | `hreflang_relative_href` | same |
| 26 | `href="//b.test/x"` | `hreflang_relative_href` | source is explicit: "Alternate URLs must be fully-qualified, including the transport method (http/https), so: https://example.com/foo, not //example.com/foo or /foo" (`google-localized-versions.txt:L365-370`) |
| 27 | `href="https://b.test/x"` | clean | is an absolute URL |
| 28 | `href="http://b.test/x"` | clean | source admits `http` explicitly (`L365`: "including the transport method (http/https)") |

Isolation note for 24–26: put the relative line beside one self-referencing absolute alternate on a
**one-page** manifest, so the expected multiset is exactly `{hreflang_relative_href}` and no reciprocity
or self-reference conjunct can fire. Whether a relative href is additionally *resolved* (and could then
produce `hreflang_external_target` or a self-reference match) is **not stated** — see §3 A4. Until it is,
a case whose page has any other page in the manifest is `undecided`.

Caught by (any of 24–26 as the sole non-self alternate): **N, C, E**.

### 2E. Duplicate pairs and legal multiplicity (class 4 of the item)

| # | shape | Verdict | Deciding rule |
|---|---|---|---|
| 29 | two lines, same tag, same href (both `en` → `https://a.test/`) | `hreflang_duplicate_pair` | "same (lowercased tag, exact href) twice on one page" |
| 30 | `hreflang="EN-gb"` and `hreflang="en-GB"`, same href | `hreflang_duplicate_pair` | the tag is **lowercased** before comparison — this is the row that pins the lowercasing |
| 31 | same tag `en`, two different hrefs (`https://a.test/`, `https://b.test/`) | **clean** | the predicate is the pair, so different hrefs are legal (also Google `L373-375` treats several locales per language as normal) |
| 32 | `href="…?a=1&amp;b=2"` and `href="…?a=1&b=2"`, same tag | `hreflang_duplicate_pair` | "exact href" is the *attribute value*, and character references are decoded into the value; the builder item also requires "entities decoded for href/tag values" |

Row 31 is the class that catches an implementation keyed on tag alone; row 32 catches one that compares
raw source text; rows 29–30 catch one that compares case-sensitively.

### 2F. More than one x-default (class 5)

| # | shape | Verdict | Deciding rule |
|---|---|---|---|
| 33 | two x-default lines, different hrefs, both pages in a 2-page manifest mirror the pair | 2× `hreflang_multiple_xdefault` (one per page), exit 1 | "more than one x-default on one page" |
| 34 | two *identical* x-default lines (same href) | `hreflang_multiple_xdefault` **and** `hreflang_duplicate_pair` | both predicates fire independently on the same two lines |

Row 34 also surfaces the granularity question in §3 A2 (does a third identical line add one or two
findings?). Google's guidance on x-default is at `google-localized-versions.txt:L729-737` ("The reserved
x-default value is used when no other language/region matches the user's browser setting") and its
example at `L756`; it does not forbid repeats, so only the contract predicate decides.

### 2G. Self-reference missing vs present (class 6)

| # | shape | Verdict | Deciding rule |
|---|---|---|---|
| 35 | A lists itself and B | clean | "Each language version must list itself as well as all other language versions." (`google-localized-versions.txt:L362-364`) |
| 36 | A lists only B (B reciprocates and lists itself) | `hreflang_self_missing` on A only | "a page with ≥1 hreflang alternate does not list its own `url` among them" |
| 37 | page with **zero** alternates | clean (no `self_missing`) | predicate requires "≥1 hreflang alternate" — this row catches a tool that reports every page (R) and one that treats "no alternates" as a fault |
| 38 | A's own url appears only under `x-default` (no language tag) | clean under the literal predicate | "list its own `url` among them" — x-default is an alternate; Google's intent (a *language* version lists itself, `L362-364`) is narrower. **Divergence to document, not to repair** (§4 D3) |

### 2H. Reciprocity (class 7)

| # | shape | Verdict | Deciding rule |
|---|---|---|---|
| 39 | A→B tag `en`, B→A tag `en` | clean | "does not declare a return alternate with A's url and the same tag" |
| 40 | A→B tag `en`, B→A tag `de` | `hreflang_nonreciprocal` (on A's annotation; B's annotation is a second finding, §3 A2) | same-tag conjunct fails |
| 41 | A→B, B has no alternates at all | `hreflang_nonreciprocal` | B declares no return alternate |
| 42 | A→`https://c.test/` where C is not in the manifest | `hreflang_external_target`, exit 0 | "a target outside the manifest is `hreflang_external_target` (informational)" — **the exit-0-with-ids class of §1** |
| 43 | three-page cycle A→B, B→C, C→A | three `hreflang_nonreciprocal` (one per edge; A→B needs B→A) | predicate is per annotation; granularity note §3 A2 |
| 44 | A→B `en-GB`, B→A `en-gb` | **undecided** until the equality relation is frozen (§3 A3) | "the same tag" does not say whether equality is case-sensitive, while the duplicate predicate says "lowercased tag" explicitly |

B has no alternates (row 41) is also the row that catches an implementation that only walks pages that
declare something.

### 2I. Canonical (class 8)

| # | shape | Verdict | Deciding rule |
|---|---|---|---|
| 45 | page with ≥1 hreflang alternate, canonical href = its own `url` | clean | "whose resolved canonical is not its own `url`" |
| 46 | same, canonical href = another page's url | `hreflang_canonical_not_self` | same |
| 47 | page with ≥1 alternate and **no** canonical link | **undecided** (§3 A5); recommended clean | contract says "resolved canonical", lane precedent says absence is not a fault (`corpus/knowledge/static-canonical-preflight.md:23-24`: "Absence of a declaration is not inherently a site error") |
| 48 | page with 0 alternates and a canonical pointing elsewhere | clean | predicate is gated on "≥1 hreflang alternate" — catches R and catches a tool that folds canonical checks into every page |
| 49 | two canonical links (self first, other second) | **undecided** (§3 A6); recommended clean by first-in-document | contract has no selector for "the" canonical on a page with two |
| 50 | `<link rel="canonical" href="…" hreflang="en">` | **undecided** (§3 A7) | Google ignores canonical annotations carrying `hreflang` (`corpus/knowledge/static-canonical-preflight.md:18-20`), the contract does not say |

Note the gap: **no source grounds the canonical rule at all.** §C2's `hreflang_canonical_not_self` is
stricter than anything in the three fetched documents (the Google hreflang page states no canonical
requirement: every `canonical` occurrence in `google-localized-versions.txt` is site navigation
(`L19`, `L121-124`, `L298`), none is in the hreflang guidance body).
The sources seat must say so plainly; the contract supplies the rule, and the tool's docstring must not
cite a source for it.

### 2J. Input faults (class 10) and exit map

| # | shape | Verdict | Deciding rule |
|---|---|---|---|
| 51 | manifest names a `file` that does not exist | exit 2, `input_unreadable` | "Input faults (exit 2): `input_unreadable` …" |
| 52 | page bytes are not decodable text (`b"\xff"` at offset 0) | exit 2, `input_unreadable` | same; lane precedent: r35's mixed-input case ships exactly a `not-utf8.html` (`.ufo/waves/round-35/evidence/w1-tools/difftest.py:170`) |
| 53 | two pages with the same `url` | exit 2, `input_duplicate_url` | listed input fault |
| 54 | `url` is `/de/` (no scheme+host) | exit 2, `input_url_not_absolute` | "Manifest v1 … `url` absolute" + listed fault |
| 55 | one readable page with a policy finding and one unreadable page | exit 2 | "2 input faults (also when both)" |
| 56 | argv without `--manifest` and without `--selftest` | exit 64 | "64 usage" |
| 57 | `--selftest` without `--work` | exit 64 | contract exit map 64 + the ExecAuditTool item ("`--work <dir>` (required with `--selftest`)") |

Row 55 leaves one thing unstated: whether the policy findings of the readable pages still appear in
`findings` when exit is 2 (§3 A8).

### 2K. HTML structure classes the contract *does* decide

| # | shape | Verdict | Deciding rule |
|---|---|---|---|
| 58 | `<a rel="alternate" hreflang="en" href="…">` (no `<link>`) | clean, not scanned | the contract's findings are all phrased on "`<link rel="alternate">`"; `hreflang` exists on `a`/`area` too (`whatwg-links.html:L263-267`) and is out of scope — the row catches an over-broad scanner |
| 59 | `<link rel="alternate" hreflang="en">` with **no** `href` attribute | **undecided** (§3 A9) | a `link` without `href` creates no hyperlink; the contract's relative-href predicate speaks of an href that exists |
| 60 | `<link rel="canonical" hreflang="en">` with no `rel="alternate"` | clean | not an alternate link; canonical gating needs ≥1 alternate |

### 2L. HTML structure edges (class 9) — mostly amendment-dependent, and not constant-killers

Status column: **C** = derivable from contract §C2 alone; **S** = derivable once the source sentence is
adopted; **A** = needs an amendment line (§3 A13/A14) before the matrix may score it; **U** = undecided,
exclude.

| # | shape | Verdict under the recommended reading | Decides it | Status |
|---|---|---|---|---|
| 61 | `<link rel="ALTERNATE" hreflang="en" href="…">` | counted as an alternate | `whatwg-links.html:L903-904`: "Keywords are always ASCII case-insensitive" | S→A |
| 62 | `rel="alternate stylesheet"` carrying hreflang | **not** an alternate — `alternate` modifies `stylesheet` and "does not create a link of its own" (`whatwg-links.html:L939-942`), so the page has 0 alternates ⇒ clean | same lines | S→A |
| 63 | attribute order reversed (`hreflang` before `rel`) | identical verdict to canonical order | ExecAuditTool item ("attributes in any order") | A |
| 64 | single-quoted vs double-quoted values | identical verdict | item ("both quote styles") | A |
| 65 | self-closing `<link … />` | element closes; the next line is still scanned | item ("self-closing") | A |
| 66 | `<link …></link>` with a closing tag | closing tag ignored (void element); verdict unchanged | HTML syntax | A |
| 67 | `<!-- <link rel="alternate" hreflang="xx" href="…"> -->` | not scanned | item ("comments … skipped") | A |
| 68 | `<script>var s = '<link rel="alternate" hreflang="xx">';</script>` | not scanned (script data is raw text) | item ("`<script>`/`<style>` … bodies skipped") | A |
| 69 | `<template><link rel="alternate" hreflang="xx" href="…"></template>` | not scanned ⇒ 0 alternates ⇒ clean | item + r35 precedent (`.ufo/waves/round-35/evidence/w1-tools/difftest.py:128-152` builds exactly these wrappers) | A |
| 70 | `<svg>…</svg>` / `<math>…</math>` wrapping an alternate | not scanned (foreign content) ⇒ clean | r35 precedent only — **the contract and the ExecAuditTool item both omit svg/math** | U→A |
| 71 | `<svg/>` self-closed, then a real alternate on the next line | the alternate **is** scanned | r35: "`<template/>` and `<math/>` open nothing" (`.ufo/waves/round-35/w1/CriticC1ContractAmbiguity.md:40`) and the `<svg/>` guard at `difftest.py:153` | U→A |
| 72 | `<template><svg>…</template>` boundary crossing | r35 recorded this as *undecided* between per-element counters and a stack (`CriticC1ContractAmbiguity.md:21`) | no rule exists | U (exclude) |
| 73 | `href="…?a=1&amp;b=2"` and `href="…?a=1&b=2"` | decoded to the same value ⇒ `hreflang_duplicate_pair` (row 32) | item ("entities decoded for href/tag values") | A |
| 74 | unquoted values `<link rel=alternate hreflang=en href=https://a.test/>` | scanned (HTML parses unquoted values) | item covers *quoted* styles only — silent | U→A |
| 75 | `<noscript>`-wrapped alternate | scripting-off reading: scanned | r35 recorded the scripting-on/off split (`CriticC1ContractAmbiguity.md:26`) | U (A14) |
| 76 | two `<link>` elements on one physical line, and one `<link>` split across lines | both scanned, one element each | item (tolerant scanner) | A |
| 77 | `<a rel="alternate" hreflang="en" href="…">` | not scanned | contract confines findings to `<link rel="alternate">` (§2K row 58) | C |

Two facts matter more than the individual rows:

- **None of 61–77 kills a degenerate constant**, with the exception of 70/71/74/75 if they are scored as
  finding cases. They are *regression guards* against scanner bugs (over-suppression is the documented
  r35 mutant class: "After an `<svg>`, `<template>` or `<math>`, the mutant ignores every later meta and
  link tag", `.ufo/waves/round-35/w1/CriticHarmPlan.md:36`). A matrix that contains only constant-killers
  and none of these will let an over-suppressing scanner reach the after-state.
- **Rows 70, 71, 74, 75 are not contract-derivable.** The lane's r35 precedent is a *precedent*, not
  §C2's text; the ExecAuditTool item names `template`/`script`/`style` but not `svg`/`math`, and it is an
  item, not the frozen contract. Until A13/A14 land, those four rows are `undecided` under kill rule 1.

## 3. Classes the contract cannot decide — contract defects, not tool defects

Each one, printed as it would fail: `undecided` in the matrix per §C2 kill rule 1, with the terms-only
amendment line that would decide it. Ordered by how much of the matrix it blocks.

**A1 (blocks the informational class).** "Informational" has no stated exit/`findings` effect.
*Amendment:* "An informational finding appears in `findings` and does not change the exit code; a run
with only informational findings exits 0."
*Unblocks:* the external-target rows (42 family, ≥2 cases) — the only class that catches
`exit = 1 if findings else 0` (§1).

**A2 (blocks every multi-occurrence count).** Finding granularity is unstated: per page, per annotation,
or per offending pair. `hreflang_duplicate_pair` on three identical lines is 1 or 2 findings;
`hreflang_nonreciprocal` on a 3-page cycle is 3 (per annotation) or 2 (per page with a fault);
`hreflang_multiple_xdefault` on three x-defaults is 1 or 3.
*Amendment:* "Policy findings are emitted once per offending annotation (one per `<link>` element), except
`hreflang_self_missing` and `hreflang_canonical_not_self` which are once per page, and input faults which
are once per manifest entry."
*Unblocks:* rows 34, 40, 43, 33, and all count assertions.

**A3 (blocks reciprocity and URL identity).** "the same tag" and "its own `url`" state no equality
relation, while `hreflang_duplicate_pair` explicitly lowercases. Trailing slash, host case, default port,
percent-encoding and fragment are all unaddressed, which also decides rows 35/36/45/46.
*Amendment:* "Tag equality is ASCII case-insensitive. URL equality is exact string equality after the
manifest `url` and the resolved href are normalised per RFC 3986 (scheme and host lowercased, default port
removed, dot-segments removed); a trailing `/` is significant."
*Unblocks:* row 44, the trailing-slash variant of 36/45, and the Reviewer's "absolute canonical with
trailing slash difference" fixture.

**A4 (blocks relative-href side effects).** A relative or non-absolute href is reported, but is it also
resolved and therefore eligible for self-reference, reciprocity and external-target? Silent.
*Amendment:* "A non-absolute href is reported as `hreflang_relative_href` and is not resolved; it
contributes to no other finding."
*Unblocks:* rows 24–26 in any multi-page manifest.

**A5 (blocks absent canonical).** "whose resolved canonical is not its own `url`" is silent on a page
with no canonical declaration. Two readings: absent ⇒ not self ⇒ finding; absent ⇒ self.
*Amendment:* "A page without a `rel=canonical` link has itself as its resolved canonical."
*Unblocks:* row 47.

**A6 (blocks multiple canonicals).** No selector for "the" canonical.
*Amendment:* "The first `rel=canonical` link in document order is the resolved canonical (r35 precedent,
`.ufo/waves/round-35/w1/CriticC1ContractAmbiguity.md:25`)."
*Unblocks:* row 49.

**A7 (blocks canonical carrying hreflang).** Google ignores such annotations
(`corpus/knowledge/static-canonical-preflight.md:18-20`); the contract counts them or not at will.
*Amendment:* "A `rel=canonical` link that also carries `hreflang` is still the page's canonical for this
tool" (or the opposite — but freeze one).
*Unblocks:* row 50.

**A8 (blocks mixed exit-2 assertions).** Whether policy findings survive alongside input faults.
*Amendment:* "When any input fault occurs, exit is 2; findings from pages that were read successfully are
still listed, pages that could not be read contribute no policy findings."
*Unblocks:* row 55.

**A9 (blocks missing `href`).** `<link rel="alternate" hreflang="en">` with no href.
*Amendment:* "A `link` element without an `href` attribute is not an alternate and is not reported."
*Unblocks:* row 59.

**A10 (blocks `hreflang=""`).** Empty value: "with no hreflang value" (⇒ `hreflang_missing_value`) or the
grammar (⇒ `hreflang_invalid_tag`)? Both sentences are true at once.
*Amendment:* "An empty `hreflang` attribute value is `hreflang_missing_value`."
*Unblocks:* the empty-value row.

**A11 (blocks `X-DEFAULT`).** "(case-insensitive)" is attached to the grammar clause; whether it also
governs the literal `x-default` token is not said. `X-DEFAULT` fails the grammar (1-letter primary), so
the two readings give different ids: clean vs `hreflang_invalid_tag`.
*Amendment:* "`x-default` is compared ASCII case-insensitively."
*Unblocks:* `X-DEFAULT` and `X-Default` rows (the Reviewer item lists both).

**A12 (blocks `mailto:`/`tel:`).** "href without scheme and host" is ambiguous between "lacks scheme and
lacks host" (⇒ `mailto:` has a scheme, so clean) and "is not scheme+host" (⇒ finding). `//host/x` is
literally in the same gap; only the Google line `L365-370` resolves the intent for that one form.
*Amendment:* "`hreflang_relative_href` fires for any href that does not parse as an absolute URL with
scheme and authority (RFC 3986); the scheme need not be http(s)."
*Unblocks:* `mailto:`, `tel:`, `javascript:`, `ftp://` rows, and makes row 26 contract-derivable.

**A13 (blocks every HTML-structure class of item 9 except `<a>`).** The contract never mentions
`<template>`, `<svg>`, `<math>`, comments, `<script>`, `<style>`, `rel` token sets, `rel` case, unquoted
attributes, attribute order or self-closing syntax. The ExecAuditTool item supplies some of this
("attributes in any order, both quote styles, self-closing, comments and `<script>`/`<style>`/`<template>`
bodies skipped, entities decoded") — but an item is not the frozen contract, and kill rule 1 says the
case is derivable *from the contract*. Two of these are nevertheless decided by a fetched source:
`rel` keywords are ASCII case-insensitive (`whatwg-links.html:L903-904`, "Keywords are always ASCII
case-insensitive"), and `rel="alternate stylesheet"` is **not** an alternate link at all
(`whatwg-links.html:L939-942`: "The `alternate` keyword does not create a link of its own").
*Amendment (one line covers the rest):* "Scanning rules: `rel` is a case-insensitive token set; a link
whose `rel` tokens include `stylesheet` alongside `alternate` is not an alternate; `<template>`, `<svg>`,
`<math>` subtrees, comments, and `<script>`/`<style>` data are not scanned; an element self-closed as
`<svg/>`/`<math/>` opens nothing; entities are decoded before comparison; unquoted attribute values are
read as HTML does."
*Unblocks:* rows for `<template>`, `<svg>`, `<math>`, `<svg/>`-does-not-hide-the-next-link, comments,
`<script>`, `rel="ALTERNATE"`, `rel="alternate stylesheet"`, entity equality, order/quoting, unquoted.

**A14 (low weight, blocks `<noscript>`).** Not named by contract or item. r35 recorded the scripting-on vs
scripting-off split for `<noscript>` (`.ufo/waves/round-35/w1/CriticC1ContractAmbiguity.md:26`).
*Amendment:* "Content inside `<noscript>` is scanned as markup (scripting-off reading)."

**A15 (blocks manifest version and path policy).** `version` other than 1, two pages sharing `file`, and
`file` containing `..`/symlinks have no verdict. The lane's canonical tool rejects traversal and
non-regular inputs (`corpus/knowledge/static-canonical-preflight.md:47-49`).
*Amendment:* "`version` ≠ 1 is exit 64; a `file` that escapes `--root`, is absolute, is a symlink, or is
not a regular file is `input_unreadable`; two pages may not share a `file`."

**A16 (counter-side, not a contract defect but a matrix hazard).** A constant that prints nothing must not
be scored as `{exit:0, ids:[]}`. The counter has to require a parseable object with `version`, `pages`
(count == manifest page count), `findings`, `counts` and `exit`, and must compare ids as a **multiset**
(the contract fixes no order, while the item only asks the tool for "a deterministic order"). Otherwise N
passes every clean case by printing nothing.

## 4. Source-vs-contract divergences (contracts wins; document, do not repair)

**D1 — the grammar is narrower than BCP 47.** Rows 17–23. RFC 5646 calls private-use, extension, extlang
and irregular-grandfathered forms well-formed (`rfc5646.txt:L255, L265, L242-244, L267-294`) and the
contract reports them invalid. The tool must state the narrow admission set; the matrix must *expect*
`invalid_tag` there, otherwise a library-based implementation passes the matrix.

**D2 — Google does not support `es-419`.** `google-localized-versions.txt:L681-682`: "Only language codes
listed in ISO 639-1 and region codes listed in ISO 3166-1 Alpha 2 are supported; other codes that aren't
listed in those standards, such as es-419, aren't supported." The contract's grammar admits it (row 5).
Expected verdict stays clean (syntax only), and the tool's docstring must not imply search-engine support
— the contract already bounds this ("no search-engine selection or ranking claim").

**D3 — self-listing intent vs the literal predicate.** Google wants the *language version* to list itself
(`L362-364`); the contract's predicate is satisfied by any alternate whose href is the page's url,
including an `x-default`-only listing (row 38). Stays clean.

**D4 — Google's own "case-insensitive" statement is broader than its ISO-list claim** (it accepts
uppercase codes at `L683-687` but rejects unlisted codes at `L681-682`). Both are quoted; neither changes
a verdict, because the contract decides on syntax alone.

**D5 — `//host/x`.** The literal contract phrase is ambiguous (A12), but the source is explicit
(`L365-370`), so the matrix may expect `hreflang_relative_href` — with the A12 amendment recorded.

**D6 — canonical has no source.** §2I note. Do not cite the three fetched documents for
`hreflang_canonical_not_self`.

## 5. Constant coverage map

| Constant | Caught by (class → why) |
|---|---|
| **N** no-op reader | every case expecting exit 1 or 2 (2B–2J): it exits 0 where 1 or 2 is expected; it passes clean rows unless the counter demands parseable JSON (§3 A16) |
| **C** always-clean | every case with non-empty expected `ids` — all policy-finding classes, and the informational class (42) |
| **R** report-all | every case with empty expected `ids` — 2A (seven valid tags), 31 (same tag, two hrefs), 37 (zero alternates), 45, 48, 58, 60 |
| **E** empty-list reader | every policy-finding class (all its predicates are link-derived). Its profile is **identical to C** on `{exit, ids}` — see §1, limitation 1 |

Design consequence worth handing to ExecAuditMatrix: include at least two external-target cases (one with
a target outside the manifest, one with a *mixed* page: one external target plus one reciprocal internal
target), because they are the only cases whose correct answer is exit 0 with non-empty `ids` — the guard
against `exit = 1 if findings else 0`.

## 6. Retained real surfaces — facts for the real-input run

`ls .ufo/waves/round-23/live/` lists 12 directories, but only 8 hold a `page.html`:

| Surface | `page.html` | bytes | `rel=alternate` | `hreflang` | `rel=canonical` | sha256 == `fetch.json` |
|---|---|---|---|---|---|---|
| burnerchrome-kimi | yes | 11976 | 0 | 0 | 0 | MATCH |
| charter-ghp | yes | 53660 | 2 | 2 | 1 | MATCH `7c243a1d…` |
| ds4cc-kimi | yes | 74641 | 0 | 0 | 0 | MATCH |
| ds4cc-primary | yes | 76159 | 0 | 0 | 1 | MATCH |
| lucario-ghp | yes | 3435 | 0 | 0 | 0 | MATCH |
| plazir15-ghp | yes | 38337 | 0 | 0 | 1 | MATCH |
| ufo-fsd-kimi-pro | yes | 612 | 0 | 0 | 0 | MATCH |
| vault-index-kimi | yes | 10059 | 0 | 0 | 0 | MATCH |
| charter-kimi | **no** (`audit.json`, `fetch.json` only) | — | — | — | — | — |
| lucario-kimi | **no** | — | — | — | — | — |
| plazir15-kimi | **no** | — | — | — | — | — |
| plazir27-kimi | **no** | — | — | — | — | — |

The four missing bodies exist only as `.ufo/waves/round-61/capture/<name>/body.bin`, each 13409 bytes,
`grep -ac` counts 0 for `hreflang`, `rel="canonical"` and `rel="alternate"` (all four identical size —
the same placeholder page). So a manifest over "the 12 retained surfaces" is either 12 pages with 4 read
from `body.bin`, or 8 pages; the ExecAuditRealRun item's premise ("each directory holds `page.html`") is
false for 4 of the 12 and must be reported rather than papered over.

`charter-ghp` is the only surface that exercises any C2 class:

```
8:<link rel="canonical" href="https://veigapunk.github.io/charter-ufo-fsd/">
9:<link rel="alternate" hreflang="x-default" href="https://veigapunk.github.io/charter-ufo-fsd/">
10:<link rel="alternate" hreflang="en" href="https://veigapunk.github.io/charter-ufo-fsd/">
```

(`.ufo/waves/round-23/live/charter-ghp/page.html:8-10`, bytes cited above.) Its manifest url is
`https://veigapunk.github.io/charter-ufo-fsd/` (`.ufo/waves/round-23/live/charter-ghp/manifest.json:1`),
so: two distinct tags, both hrefs equal to its own url (self-reference present, no duplicate pair),
one x-default, canonical self, and — because both targets are the page itself — **no** reciprocity edge
and **no** external target. Expected real-run state: `charter-ghp` clean; the other 7 (or 11) pages clean
trivially via row 37 (0 alternates). The real run therefore exercises **none** of rows 8–50 except the
trivial ones; its value is that the tool runs on 12 real byte sets without crashing and agrees with the
canonical audit on which pages declare canonicals, not that it discriminates anything. State that
honestly in the C2 claim.

## 7. Minimal matrix skeleton that is derivable today

Decided from contract text alone (each row is one fixture; `ids` compared as a multiset):

| Row | Fixture (abbreviated) | exit | ids |
|---|---|---|---|
| 1 | 2-page clean baseline (en+de, reciprocal, canonical self) | 0 | — |
| 2 | 7 valid tags, all self, 1 page | 0 | — |
| 3 | 8 invalid tags (`en_US`, `english`, `en-`, `x-defaults`, `en GB`, `en--GB`, ` en `, `i-klingon`) | 1 | 8× invalid_tag |
| 4 | 7 narrow-grammar tags (`x-private`, `en-a-bbb`, `zh-yue-HK`, `en-u-ca-gregory`, `sgn-BE-FR`, `en-GB-oed`, `abcdef`) | 1 | 7× invalid_tag |
| 5 | `EN-gb` + `en-GB`, same href | 1 | duplicate_pair |
| 6 | same tag, two hrefs | 0 | — |
| 7 | 2 x-default, different hrefs, mirrored on 2 pages | 1 | 2× multiple_xdefault |
| 8 | 2 identical x-default lines | 1 | multiple_xdefault + duplicate_pair |
| 9 | self missing (A lists only B; B reciprocates and lists itself) | 1 | self_missing |
| 10 | page with zero alternates | 0 | — |
| 11 | `/de/`, `#de`, `//b.test/x` (three separate 1-page fixtures) | 1 | relative_href each |
| 12 | `https://` and `http://` absolute | 0 | — |
| 13 | A→B `en`, B→A `de` | 1 | nonreciprocal (2 per A2, undecided until A2) |
| 14 | A→B, B has no alternates | 1 | nonreciprocal |
| 15 | A→`https://c.test/`, 1-page manifest | 0 | external_target |
| 16 | mixed page: `https://c.test/` + reciprocal internal target | 0 | external_target |
| 17 | canonical other page | 1 | canonical_not_self |
| 18 | canonical self | 0 | — |
| 19 | 0 alternates + canonical elsewhere | 0 | — |
| 20 | `<link rel="alternate">` no hreflang | 1 | missing_value |
| 21 | `<a rel="alternate" hreflang="en">` | 0 | — |
| 22 | missing file | 2 | input_unreadable |
| 23 | undecodable page bytes | 2 | input_unreadable |
| 24 | duplicate page url | 2 | input_duplicate_url |
| 25 | non-absolute page url | 2 | input_url_not_absolute |
| 26 | policy finding + input fault | 2 | per A8 (undecided) |
| 27 | no `--manifest` | 64 | — |
| 28 | `--selftest` without `--work` | 64 | — |

28 rows are reachable without any amendment; 26 of them are decidable as written (row 26 needs A8 for
whether policy findings survive an input fault, and row 13 needs A2 for its finding count). Adding the A1 and A13
amendment lines takes the derivable set past 40 and supplies the structure classes of item 9. Every row
above also states which constant it kills (§5); rows 15–16 are mandatory as the only exit-0 rows with a
non-empty `ids`.

## 8. Remaining unknowns

- Whether the tool may resolve relative hrefs at all (§3 A4) — affects rows 11 and any multi-page page
  carrying a relative line.
- Whether `hreflang` values are taken from the raw attribute or after Unicode normalisation (the contract
  is ASCII-only, so non-ASCII digits/letters must be `invalid_tag`; not stated).
- Whether a page may appear twice in the manifest with different `id` but the same `url` — covered by
  `input_duplicate_url` only if "url" means the manifest `url` field; `id` uniqueness is unstated.
- Whether the `counts` object must break findings down by id (item says `counts`, contract never does) —
  harmless, but the matrix must not assert on a shape the contract does not fix.
- I did not test any implementation: no `scripts/hreflang_audit.py` exists at this revision
  (`ls scripts/ | grep -i href` printed nothing), so every verdict here is derived from text, not
  observed from code.
