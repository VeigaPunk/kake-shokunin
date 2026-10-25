# ScoutCJKUnits — what 31/27/27 means and what it does (not) prove

Scope: read-only resolution of one unknown. No edits to shared state; no installs
(none required — re-derivation used system python3 only).

## The 31/27/27 figures

They are the `units()` counts of the three Japanese Gate quotes in the round-53
gate draft `.ufo/waves/round-53/sources/gate-draft.md:15-17`:

| Row | Quote | units() |
|---|---|---|
| S367 | このウェブページ内にあるリンク先ウェブページの巡回は拒否するが | 31 |
| S372 | ファイルは、サイトのルートディレクトリに設置してください | 27 |
| S373 | 「$」記号がない場合、クローラーはプリフィクス（接頭辞）として扱い、 | 27 |

Re-derived by importing `.ufo/waves/round-52/c52_quote_truth.py` and calling
`units()` on the stored spans: 31 / 27 / 27 exactly; each quote is a single
whitespace token with cjk = units and latin = 0. (For reference the two Chinese
Gate quotes measure S390 = 16, S409 = 15; the superseding S416 = 15, S417 = 20.)

## Exact unit definition

`c52_quote_truth.py:74` `CJK_RE = [\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]`
(Hiragana, Katakana, CJK Ext-A, CJK Unified, CJK Compatibility Ideographs —
not kana Ext, not CJK punctuation U+3000-303F, not halfwidth forms).

`units()` (`:136-140`, docstring "One unit per CJK character, one per non-CJK
whitespace token"):

```
cjk   = number of characters matching CJK_RE        (1 unit each)
latin = number of text.split() tokens that contain NO CJK_RE match (1 unit each)
units = cjk + latin
```

Consequences a reader must not flatten:

- CJK punctuation is not counted as a character (、「」（）【】 are outside
  CJK_RE) and a token containing any CJK char is never counted as a latin
  token. So 「$」記号…扱い、 contributes only its 27 kanji/kana + 0 for `「$」`.
- A latin run *inside* a CJK token contributes nothing (…のCSS、Javascript…
  gives 16 = CJK chars only). `units` is therefore not additive over visible
  characters: it is a lower bound on a lexeme count.
- Both bound endpoints apply in the round-52 C5 check (`:258-260`): a `## Gate`
  quote must be 6 ≤ units ≤ 40 and a raw substring of the retained body. Entry
  body quotes need only ≥6 units (`:269-271`). The counter never measures
  "words".

## The CORPUS ≤25-word rule

`CORPUS.md` SOURCES rule 1 (`CORPUS.md:112-115`): the round lesson's `## Gate`
records "a ≤25-word quote with its location grounding `teaches`". Round-28
precedent counts literal whitespace words (QUALITY.md:379-383, round-28 C2
counter `.ufo/waves/round-28/c2_source_count.py:126-131`). Nothing in the rule
defines "word" for scripts without whitespace-delimited words.

The round-53 closure note is `corpus/lessons/round-53-verifier-spotcheck.md`:
- line 57: S367/S372/S373 "register 31/27/27 units under the lane's own
  `units()` counter (one per CJK character) — the CORPUS ≤25-word letter is
  ambiguous for CJK; routed as a nit, not an admission failure."
- line 82 (routed defect 5): the gate quotes "exceed 25 units under the lane's
  own counter; either shorten quotes or document the CJK unit interpretation
  against the CORPUS ≤25-word rule."

Round-54 resolution (committed before this seat ran):
`corpus/QUALITY.md:1133-1144` appends the criterion "CJK quote length names its
unit and does not imply word-rule compliance" — a 6–40-unit Gate result is a
local source-truth floor/ceiling; it does not prove ≤25-word conformance, and
counts must be reported as units, never "words". `contract.md:60-69` records the
same maintenance item: "the count is re-derived at the measured commit".

## Verdict

31/27/27 does **not** prove the CORPUS ≤25-word rule for Japanese — the correct
non-overclaim already landed in QUALITY.md:1133-1144 and contract.md:60-69:

- Units are not words: each kanji/kana is one unit, so 31 units ≈ 31 characters,
  not 31 words. CJK word segmentation is genuinely ambiguous (the S367 quote
  segments to roughly a dozen bunsetsu), so the unit count is silent on the word
  letter — it neither establishes conformance nor, strictly, proves violation.
- What it does prove: the three quotes sit inside the round-52 counter's
  accepted 6–40-unit Gate band and are raw substrings of their retained bodies
  (quote-truth, not word-shape).
- The spot-check's own framing is consistent: "ambiguous for CJK; routed as a
  nit" (line 57), escalated to routed defect 5 demanding either shorter quotes
  or a documented unit interpretation (line 82). Round 54 chose the second
  option — documented interpretation, counts kept as units.

Confidence: high — every claim above is backed by committed bytes cited
path:line; counts were re-derived by executing the counter's own `units()`.

Remaining unknowns: none within scope. (A true Japanese word count would need
an external segmentation tool, e.g. MeCab, which was neither required nor
installed.)
