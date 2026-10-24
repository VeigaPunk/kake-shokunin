# KakeR27.CitingSweep13 — blind citing census, two named knowledge files
Axes: **freshness** (C1 citing-set denominator at frozen base) and **operability**
(counter reproduces its before-state). Author-side evidence only; no source/site
evaluation, no production edits, no tool installs (pacman untouched, none needed).

Scope: `corpus/knowledge/static-canonical-preflight.md` (203 lines, sha256
`833b28f26fa7309f7e31398275bae2f704969d8e6f095bc5bb96250da5c531bc`, blob
`d86ddec6e6acc05b3c1f60da87a97a0f2645c8bf`) and `corpus/knowledge/vault-properties.md`
(103 lines, sha256 `f26b2d105614f663acae73d9d6169a1346a4573fd556f577cfdfc51cea97ff51`,
blob `7435c09c42bd6d8e779c74d209828fcea81d3c2a`). Base
`83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`; HEAD `be375d90afc6fc7aca369ab3cf5247bf460aeed2`.
Working bytes == base == HEAD (empty `git diff --stat` both ranges; `hash-object` ==
`rev-parse`; sha256 == `frozen/expected.json`). Manual census **first**; parser,
`c1-before`, 16-missing comparison **after**. Scratch `/fast/scratch/hyaku/kake-r27/CitingSweep13/`.
## 1. Manual census — every reference, line + located text (≤25 words)

Whole-file read (all 203 + 103 lines), permissive sweep `[Ss]\s?[0-9O]{2,}`, explicit
S014/S019/S035 check. `static-canonical-preflight.md` (71 strict `\bS\d{3,}\b`
occurrences, 3 ranges, 16 distinct literals):

| line | token(s) | form / scope | located text |
|---|---|---|---|
| 1 | S020, S021, S026, S027, S028, S029 | literal ×6, `source:` provenance header | "source: S020 RFC 6596 section 3 https://www.rfc-editor.org/rfc/rfc6596.html; S021 Google canonical guidance" / "S026 Python HTMLParser https://docs.python.org/3/library/html.parser.html; S027 Python URL parsing" / "S028 RFC 9110 sections 4.2.1-4.2.2 https://www.rfc-editor.org/rfc/rfc9110.txt; S029 RFC 3986 section 3" |
| 2 | S020-S027, S028-S029 | two ASCII-hyphen ranges, `verified-at:` header | "verified-at: 2026-10-20 (S020-S027) and 2026-10-21 (S028-S029)" |
| 54 | S001–S006 | en-dash (U+2013) grouped range | "not over an assumed checkout served set (S001–S006, `ghp-served-set.md`)" |
| 69 | S026 | literal, parser-boundary prose | "matching start/end tags or report all implicit closures (S026)" |
| 75 | S027 | literal, URL-boundary prose | "cannot be claimed as an exact WHATWG URL implementation (S027)" |
| 82 | S029 | literal, empty-authority prose | "RFC 3986 section 3 says a path without an authority cannot begin with `//` (S029)" |
| 85 | S028 | literal, empty-host prose | "require a recipient to reject an http(s) URI with an empty host as invalid (S028)" |
| 98 | S030 | literal, Round-23 sources | "Sources: S030 (WHATWG syntax: a slash is allowed only on void or foreign" |
| 99 | S031 | literal, Round-23 sources | "elements and has no effect on void elements), S031 (WHATWG parsing: in-body" |
| 101 | S024, S026 | literal ×2, scope sentence | "return to HTML rules), S024 (the first base in tree order wins), S026." |
| 111 | S030 | literal ("13 names in S030"; ref starts L110) | "in S030). A self-closed non-void element (`<div/>`) stays unsupported." |
| 117 | S024 | literal, body-`base` rationale | "because a body base is still the document's first base in tree order (S024)" |
| 140 | S021 | literal, `[r23-correction]` | "[r23-correction] "rejects fragment canonicals" overstates S021" |
| 144 | S025 | literal, `[r23-correction]` | "canonical" rests on S025 (template contents are not children of the template)" |
| 151 | S030 | literal, falsifier caveat | "S030 caveat: a separate trailing solidus has no effect on a void-element start tag" |
| 159 | S032, S033, S034 | literal ×3, Round-24 sources | "Sources: S032 (RFC3339 §5.6–5.7), S033 (RFC9110 §8.3.1 and §5.6.6), S034 (RFC8259 §3/4/6/9), all opened this round." |
| 184 | S020…S034 (11) | comma/`and` **list**, EOF recheck | "Rows S020, S021, S026, S027, S028, S029, S030, S031, S032, S033 and S034 were re-fetched by one public GET each" |
| 184 | S008 | literal, EOF recheck | "S008 via `manifest-retry.json`" |
| 186 | S021 ×2, S020 | literal, `[r26-recheck S021 STALE]` tag + body | "[r26-recheck S021 STALE] Line 25's “Cross-domain canonical is likewise not intrinsically invalid”" + "Read it as an S020 claim (RFC 6596 §3:" |
| 188 | S026 ×3, S027 | literal, `[r26-recheck S026 STALE]` + body | "[r26-recheck S026 STALE] Line 69's “or report all implicit closures (S026)”" + "(S026 and S027 alike)" |
| 190 | S030 ×2 | literal, `[r26-recheck S030 STALE]` + body | "[r26-recheck S030 STALE] Line 110's “Self-closed HTML void elements” misuses S030's term" |
| 192 | S030 ×2 | literal, second `[r26-recheck S030 STALE]` | "[r26-recheck S030 STALE] Line 111's “A self-closed non-void element (`<div/>`) stays unsupported”" |
| 194 | S032 | literal, version note | "the RFC Editor info page reports RFC 3339 (S032) as updated by RFC 9557" |
| 198 | S024 ×3 | literal, `[r26-recheck S024 STALE]` + quoted L101 | "[r26-recheck S024 STALE] Line 101's “S024 (the first base in tree order wins)”" |
| 199 | S024 ×5 | literal, second `[r26-recheck S024 STALE]` + quote | "because “a body base is still the document's first base in tree order (S024)”" |
| 200 | S025 ×2, S024 | literal, falsify-wave adjudication | "S024 and S025 were re-fetched this round (receipts HOLD)" |
| 201 | S026 ×2 | literal, reclassification note | "Reclassified as a precision note (not STALE): the S026 block." |
| 202 | S030 ×3, S031 | literal, reclassification note | "Lines 110-111 cite S030 only for the 13 void names" + "(S031: a trailing solidus sets the tag token's “self-closing flag”" |
| 203 | S021 | literal, closing note | "- S021 note: the line-21 fragment wording was STALE at base" |

`vault-properties.md`: line 1, `S019`, literal in `source:` provenance header —
"Metadata authority only: S019 in corpus/SOURCES.md, not present-day property state."
No other S-id: L14-20 bash block, L32-38 baseline table, L49-68 artifact file:line
refs (`kimi-surface.mjs:483`, `:845-849`, `:339-346`, `:903`, `:906`,
`fleet.config.json:298`), L93-103 claim labels `[vault-properties:c1]`…`:c10`
(claim ids, not source rows).
Negative findings (both files): no S014, no S035; no em-dash/`..`/`to`/`through`
ranges; no 2-digit ids; no spaced/lowercase/`S-019` spellings; no slash lists.
`S0NN` (static L184, `round-26/rechecks/S0NN.json`) is a filename template, not a
citation. Thirteen row-ids embedded in evidence filenames (static L151,186,188,
190,192,194,198,199,201,202,203: `ReopenS030`, `PairS021…`, `PairS026…`, `PairS027…`,
`PairS030…`×2, `PairS032…`, `UncoveredS024S025`×2, `Correction6S026`,
`Correction7S030`, `Correction8S030`, `Rejection10S021`) are word-internal, not
citing forms; each named row is already cited in prose.
## 2. Pair set contributed by these two files

`static-canonical-preflight.md` → **22** inherited32-row pairs; `vault-properties.md`
→ **0** (sole reference is out-of-population S019).

- r26-carried decided (13): S020, S021, S024, S025, S026, S027, S028, S029, S030,
  S031, S032, S033, S034 — all also occur as standalone literals.
- frozen-16 missing (9): S001, S002, S003, S004, S005, S006, S008, S022, S023.

**Range-only pairs (6 of 22):** S002, S003, S004, S005 exist only via L54
`S001–S006`; S022, S023 only via L2 `S020-S027`. No standalone literal for either
set anywhere in the file; the other 16 pairs each have one. Consequence: (a) C1
adjudication of S022/S023 must be scoped to the `verified-at` header claim (rows
verified 2026-10-20), since no body sentence names them; (b) a parser without range
expansion silently deletes 6 of 22 pairs.

Corpus-wide range-only check on the frozen 16 (context, not my files): **10 of 16
are range-only** — S002(static), S003(sitemap-orphan-audit), S003(static),
S004(publish-channels), S004(static), S005(sitemap-orphan-audit), S005(static),
S006(publish-channels), S022(static), S023(static); literal are S001, S006(static)
and the four S008 pairs.
## 3. Additional obligations beyond frozen57 — **none found**

Independent enumerator (literal + `\bS`-range forms per contract, population
intersection, 26 knowledge blobs at base, no `discovered-pairs.json` present)
returns exactly **57** pairs. Set comparison both directions: `independent −
(ledger41 ∪ missing16) = ∅` and `(ledger41 ∪ missing16) − independent = ∅`. For my
files: 22 = 13 ledger + 9 missing. Candidates examined and rejected as
non-citations (rule-checked, not dismissed as metadata):

1. `ghp-served-set.md` (L54) — knowledge-file ref, not a SOURCES row.
2. The 13 evidence-filename row-ids — word-internal, rows already paired.
3. `S0NN` template.
4. Named standards with no S-id: "RFC 6596 section 3" (L13), Google "Use rel=canonical"
   (L18), "Python HTMLParser" (L68), "The URL module" (L74), "RFC 3986 section 3"
   (L82), "RFC 9110 sections 4.2.1-4.2.2" (L83), "WHATWG slash-skipping" (L87),
   "RFC3339/RFC9110/RFC8259" (L159), "RFC 9557" (L194), "HTML5 tree builder" (L103) —
   all map to rows already paired (S020/S021/S026-S034); L194 says RFC 9557 "needs a
   new source row".
5. **S010** (RFC 9110 §8.8 per SOURCES.md) — the only RFC 9110 citation is "sections
   4.2.1-4.2.2", S028's declared scope; no §8.8 text appears, so no S010 pair.

Population frozen: 32 ids, S001–S034 minus own-work S014/S019 (`corpus/SOURCES.md:79`).
Denominator not shrunk: 57 is reproduced, not restated.
## 4. Out-of-population references (recorded separately, not obligations)

| row | file:line | scope | if admitted |
|---|---|---|---|
| S019 | vault-properties.md:1 | metadata-format authority only, explicitly "not present-day property state" | +1 pair, metadata scope only |
| S014 | absent from both files | — | corpus-wide 1 file (`freshness-sweep.md`) |
| S035 | absent from both files | — | corpus-wide 1 file (`accessibility-review-packet.md`) |

Base corpus: S019 cited by 16 knowledge files, S014 by 1, S035 by 1; none is a
population row. If L1 admits own-work rows, this scope gains exactly 1 pair
(S019/vault-properties.md), pending a separate adjudication basis.
## 5. Parser / before-state comparison (after §1)

`python3 -B .ufo/waves/round-27/count_c1.py --root . --revision 83528f7…` → exit
**1**; JSON **byte-identical** to `c1-before.json` (both sha256
`af55d0a4bb1aa9b21bc2ce026035beaf21e523458661252f8a520008f2ec6e3c`): population 32,
citingPairs 57, decided 41, r26Carried 41, newDecided 0, missing 16, findings 0.

- `LITERAL`/`RANGE` semantics match my census; ranges here span 7, 1, 5 — valid, no
  invalid-range exit. Population filter `if f'S{i:03d}' in pop` drops S019 in
  vault-properties.md → 0 pairs, matching manual result.
- Scan domain is `corpus/knowledge` blobs only, so SOURCES.md's defining rows are not
  pairs. `pairs.json`/`discovered-pairs.json` absent at measurement, so the
  before-state is purely r26-carried; all 41 ledger pairs remain enumerated at base
  (no orphan). All 13 target-file ledger reports exist
  (`w1/PairS0*StaticCanonicalPrefl.md`, `w2/UncoveredS024S025.md`).
- No divergence parser-vs-manual on these files: same 22 + 0 pairs, same 9 missing,
  same range-only set. Limitation: the parser cannot distinguish a provenance-header
  range from body prose (so S022/S023 are full obligations despite zero body mention),
  and correctly cannot see filename-embedded row ids.
## 6. Freshness / operability dependencies observed

1. `round-27/fetched/manifest.json` has 8 entries covering only **S001–S006**
   (S001×2, S002×2, S003, S004, S005, S006) — exactly the 6 grouped target-file
   pairs, so those are adjudicable from bytes already retained.
2. **S008, S022, S023** have no round-27 fetch; `count_c1.py` validates quotes only
   against that manifest (or `kind:"artifact"` repo evidence), so they need an r27
   fetch or artifact support. S008's citation is the EOF metadata claim "S008 via
   `manifest-retry.json`" (GNU tar exclusion patterns, SOURCES.md:16); S022 (Google
   canonicalization issues) / S023 (WHATWG link type canonical) are header-range
   only. Adjudication scope for all three is that metadata record, not policy prose.
3. Both files' bytes are unchanged from base (no r27 drift yet); any r27 append can
   only add literals, so the 22-pair set is a lower bound that grows monotonically.
## 7. Verdicts (author-side; parent judges)

- **Census supported at base:** static-canonical-preflight.md 22 pairs (13 decided,
  9 of the frozen 16; 6 range-only); vault-properties.md 0 pairs. No additional
  inherited32-row obligation exists in either file.
- **Before-state reproducible:** frozen counter byte-identical to `c1-before.json`;
  independent enumeration agrees at 57 in both directions.
- **No PASS claimed** on content truth; no source/site evaluation performed.
## 8. Uncertainties

1. Range expansion is citation by contract; if L1 narrows to literal-only, 6
   static-file pairs (and the frozen 16) change. Not decided here.
2. Whether the `verified-at` `S020-S027` is per-row verification scope or date-range
   formatting convenience is an L1 reading; I followed the frozen rule.
3. Population taken as frozen; a change grows or re-scopes obligations, never proves
   absence.
4. Named-standard references fall outside the contract's citing-form definition; a
   wider rule would need its own census.
5. No source/public-site evaluation, so no claim here about S001–S034 truth.
Evidence: base `git show` reads; `count_c1.py` at base (exit 1, JSON byte-identical,
sha256 above); independent enumerator; `sha256sum`/`git hash-object`;
`frozen/expected.json`; `frozen/ledger.json`; `round-26/statements.json`,
`population.json`; `c1-before.json`, `c2-oracle.json`, `fetched/manifest.json`.
No tool installs; pacman untouched. No edits outside this report.
report: .ufo/waves/round-27/w1/CitingSweep13.md
seat: KakeR27.CitingSweep13 — leaf, read-only
