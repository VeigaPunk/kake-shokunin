# ReviewPopulation — round 25 W2 falsify: population vs pinned source vs cards

Verdict: **no duplicate, missing, extra, mis-titled, mis-levelled or mis-anchored criterion found.**
Population and cards both hold exactly the source's 31 A + 24 AA criteria, in source order, with
4.1.1 and all AAA excluded. Every normativeText equals an independent stdlib extraction of the
criterion body, apart from extraction whitespace. The "New" badges are absent from every normativeText. All
55 quotes are grounded and every card is `not-assessed`. The only findings are informational
(the documentation wording and an unused field); there is no defect.

## Inputs (sha256, observed)

| File | sha256 |
|---|---|
| `.ufo/waves/round-25/source-wcag22.html` (= `frozen/source-wcag22.html`, = `population.sourceSha256`, = `SOURCE_SHA256` in `scripts/accessibility_packet.py`) | `6e3c5fe3…f7057` |
| `.ufo/waves/round-25/population.json` (= `frozen/population.json`, = `POPULATION_SHA256`, = `candidate.json` `populationSha256`) | `4751dc24…03058` |
| `corpus/knowledge/accessibility-review-cards.json` (= `frozen/cards.json`, = `frozen/expected.json` `sha256.cards.json`) | `504ddb09…c7332d` |

## Method (local counting only)

- I wrote my own extractor (`/tmp/r25_review_population_extract.py`, Python `html.parser`, not
  in the repository). It reads every `<section class="guideline">` whose `h4` is
  `Success Criterion N.N.N Title`. It takes the level from `p.conformance-level` and builds the body
  text without `div.header-wrapper`, `div.doclinks`, `p.conformance-level`, `p.change` (the
  "New" badge) and `div.note`.
- I counted a second way with regular expressions: TOC `tocxref` entries,
  `h4` headings, and `(Level X)` labels.
- I compared the results with `population.json`, the cards, and `frozen/expected.json`
  (`/tmp/r25_review_population_compare.py`).
- I ran no tests, packet tool, measure/selftest/replay script, browser, website or round-24 artifact. I installed no tools.

## Source enumeration (independent)

- There are 87 `Success Criterion` h4 headings with no duplicate numbers. The TOC has 94 three-part entries:
  87 criteria plus the conformance headings 5.2.1–5.2.5 and 5.3.1–5.3.2, which are not criteria.
  The TOC and the h4 headings agree on every anchor and title.
- Levels: **A 31, AA 24, AAA 31**. One heading has no level: 4.1.1 `Parsing (Obsolete and removed)`
  (anchor `parsing`). Its body is only a Note saying the criterion "is removed". The source has
  exactly 55 A/AA `(Level …)` labels, and no HTML `id` appears twice.
- Six A/AA criteria carry a `<p class="change">New</p>` badge: 2.4.11, 2.5.7, 2.5.8, 3.2.6,
  3.3.7, 3.3.8. Three AAA criteria also carry one (2.4.12, 2.4.13, 3.3.9), but AAA is out of scope.
- The 31 AAA IDs are 1.2.6–1.2.9, 1.3.6, 1.4.6–1.4.9, 2.1.3, 2.2.3–2.2.6, 2.3.2, 2.3.3, 2.4.8–2.4.10,
  2.4.12, 2.4.13, 2.5.5, 2.5.6, 3.1.3–3.1.6, 3.2.5, 3.3.5, 3.3.6, 3.3.9. None appears in the population or the cards.

## Population and cards vs source

| Check | Population | Cards |
|---|---|---|
| Count / levels | 55 / A31 AA24 | 55 / A31 AA24 |
| Duplicate IDs | none | none |
| Missing / extra vs source A/AA | none / none | none / none |
| Order identical to source order | yes | yes |
| title, level, anchor, `source` = pinned URL + `#anchor` | 0 mismatches | 0 mismatches (title/level/source) |
| 4.1.1 or any AAA ID present | no | no |

`frozen/expected.json` `ids` matches the source A/AA order exactly, with `expected` = `accepted` = 55.

## normativeText extraction

- With all whitespace removed, the population's `normativeText` equals my body extraction for **55/55** criteria. With
  whitespace collapsed only, 24/55 are identical. In the other 31, the population inserts a
  space before punctuation that follows a link, for example `synchronized media ,` and `essential .`.
  The production `normalized()` function removes this (`\s+([,.;:)]` and `(\s+`). After applying it, 54/55 are equal.
  The remaining one, 3.3.4, is a flaw in my extractor: the source has `<dt>Reversible</dt><dd>Submissions`
  with no whitespace between the tags, so my extractor produced `ReversibleSubmissions`. The population's
  `Reversible Submissions` is the correct rendering.
- Leaks: no normativeText contains a heading, `Understanding`/`How to Meet` link, `(Level`
  label or `Note` label. The only `Success Criterion` text is in 1.1.1's own body:
  `(Refer to Success Criterion 4.1.2 for additional requirements…)`. This is real criterion text, not a leak.
- "New" badges: no normativeText has a standalone `New` token. This matches the contract
  amendment "Remove New editorial badges from normativeText".
- Notes: 22 A/AA criteria contain 35 `div.note` blocks. Their whole contents are left out of
  normativeText. That is correct: source §5.1 says "Introductory material, appendices, sections
  marked as "non-normative", diagrams, examples, and notes are informative (non-normative)."
- After `normalized()`, one spacing difference remains: 2.2.1 `(for example, "press the space bar")`.
  The space before the opening quote is in the source itself, so it is not an artifact.
  No normativeText contains non-ASCII characters.

## Cards: quotes and status

- All 55 `sourceQuote` values are 6–25 words long. Each matches at word boundaries in its own criterion's
  normalized normativeText, and each is also found in my independent body extraction (3.3.4 matches
  once my `dt`/`dd` joining flaw is allowed for). No quote also appears in another criterion's body.
- All 55 cards have `status` = `not-assessed`. All cards use the 10-field schema that
  `FIELDS` expects.

## Findings

1. **No duplicate, missing or extra criterion, and no metadata error.** The claimed fixed population of 55
   (31 A + 24 AA, without 4.1.1 or AAA) holds against the pinned source. Confidence: high.
   Two independent counting methods agree, and so do the byte hashes.
2. **Wording in the packet docs (informational).** `corpus/knowledge/accessibility-review-packet.md`
   line 21–22 says normativeText "excludes … note wrappers". In fact the full note bodies are excluded,
   which is correct per §5.1. "Notes (informative per §5.1)" would describe it precisely.
3. **The `text` field is unused (informational).** Each population row also has a `text` field holding
   the raw section text: heading, doclinks, level label, "New" badge for 6 rows, and `Note` labels for 22 rows.
   It equals the raw section text with whitespace removed for 55/55 rows. Nothing reads it:
   `scripts/accessibility_packet.py`, `measure.py`, `packet_selftest.py` and `quote_proof.py` all use only
   `normativeText`. It does no harm today, but it carries heading and badge text that a future checker
   could quote by mistake.
4. **Remaining unknown: source-to-population binding at runtime.** `load()` checks the source's hash
   but never re-derives `normativeText` from it. The link between the HTML and the population therefore rests
   on the authoring-time extraction plus the population hash. This independent extraction confirms that link
   for the current bytes. No code currently re-checks it if the population is regenerated.

No production files were edited. Temporary scripts and output are in `/tmp/r25_review_population_*` only.
