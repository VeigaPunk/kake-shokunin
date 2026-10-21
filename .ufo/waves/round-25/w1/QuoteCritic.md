# KakeR25.QuoteCritic — sourceQuote containment review

Scope: read-only critique of the extraction contract in `.ufo/waves/round-25/population.json` and the shared-interface rule "sourceQuote <=25 words … contained in normative text". I did not touch any r24 material, run any executable probes against tools, or modify anything other than this report. All analysis was offline against the pinned files.

## Verdict

**Yes.** If containment is checked against the whole saved section (`criteria[].text`), headings, documentation links, the conformance-level marker, and informative Notes can all pass as a "normative quote". The population already contains the correct haystack, `criteria[].normativeText`. However, a plain `quote in normativeText` check is still wrong in both directions:

- **False rejections:** an extractor whitespace artifact rejects correctly copied quotes in 30 of the 55 criteria.
- **False accepts:** three residual masquerades still pass. These are the cross-reference parentheticals in 1.1.1, list-item labels and case-folded titles, and boilerplate shared between criteria.

## Evidence

- **Source pin holds.** `sha256(source-wcag22.html)` = `6e3c5fe397257cae509a2fb4752b73062cf8cbeb92c2cec618989b17e4cf7057`, which equals `population.sourceSha256`. The source URL is the dated REC `https://www.w3.org/TR/2024/REC-WCAG22-20241212/`. Freshness is not impacted.
- **Section structure in the source.** Each criterion is a `<section class="guideline">` containing, in order:
  - `div.header-wrapper` (the `h4` heading "Success Criterion N Title")
  - `div.doclinks` ("Understanding X | How to Meet X")
  - `p.conformance-level` ("(Level A)" or "(Level AA)")
  - the normative body (`p`, `ul`, `dl`)
  - zero or more `div.note`, which are informative.
- **`text` vs `normativeText`.** In 55/55 criteria, `normativeText` is an exact substring of `text`. The prefix before it is always heading + doclinks + level. The suffix after it is empty or Notes only. 22 criteria carry Notes (13 A, 9 AA).
- **Independent re-derivation of `normativeText`.** I parsed the HTML, dropped `header-wrapper`, `doclinks`, `conformance-level` and `note` blocks, and collapsed whitespace. The result equals `normativeText` in 54/55 criteria once space-before-punctuation is normalized. The remaining one is 3.3.4, where the population inserts a space at the `</dt><dd>` boundaries ("Reversible Submissions…"); the population's version is the correct reading. So `normativeText` is a sound single source of truth for the quote check.
- **Extractor joins text nodes with a space.**
  - The source has `…<a>synchronized media</a>.` but the population has "synchronized media ." (likewise "text , then", "CSS pixels ;").
  - 30 criteria are affected (18 A, 12 AA).
  - `normativeText` contains no non-ASCII characters, so no quote-mark or Unicode folding is needed.
- **Cross-references inside the normative body exist only in 1.1.1.** These are "(Refer to Success Criterion 4.1.2 for additional requirements …)" and "(Refer to Guideline 1.2 for additional requirements for media.)". They sit inside the normative `dd > p` but are pointers, not requirements.
- **List-item labels (`<dt>`) run into the body** in 14 criteria: 1.1.1, 1.2.1, 1.4.3, 1.4.5, 1.4.11, 1.4.13, 2.1.4, 2.2.1, 2.2.2, 2.5.2, 2.5.4, 2.5.8, 3.3.4 and 3.3.8. Examples are "Essential", "Turn off", "Controls, Input" and "Active only on focus". Every label is 4 words or fewer.
- **Titles match the body if case is ignored.** A case-insensitive title appears in `normativeText` for 9 criteria: 1.1.1, 1.3.3, 1.3.4, 1.4.5, 2.1.1, 2.4.1, 2.4.6, 3.3.2 and 4.1.3. A case-sensitive comparison matches none.
- **Shared spans across criteria.**
  - 21 five-word spans are shared between criteria of *different* levels. Examples: "Captions are provided for all" (1.2.2 A / 1.2.4 AA) and "of the following is true:" (2.1.4, 2.2.1, 2.5.2, 3.3.4).
  - 2.4.2 (A) and 2.4.6 (AA) share "describe topic or purpose."
  - Every one of the 55 criteria has at least one five-word window that appears in no other criterion's `normativeText`. A uniqueness rule is therefore always satisfiable.
- **A/AA census against the raw source.**
  - The source has 87 criteria: 31 A, 24 AA, 31 AAA, plus 4.1.1 "Parsing (Obsolete and removed)", which has no level.
  - The population's A/AA id set equals the source's exactly.
  - anchor, title and level match the source in 55/55 criteria.
  - 4.1.1 is correctly absent.

## Rejection witnesses (prose; nothing was executed against a tool)

1. **Doclink masquerade.** A 2.4.6 card with sourceQuote "Understanding Headings and Labels | How to Meet Headings and Labels (Level AA)" is 13 words and is contained in `text`. It contains zero normative words. It must be rejected because it is absent from `normativeText`.
2. **Heading masquerade.** A 1.4.10 card with sourceQuote "Success Criterion 1.4.10 Reflow" is contained in `text` and must be rejected for the same reason.
3. **Note masquerade, an AA hotspot.** A 1.4.10 card with sourceQuote "320 CSS pixels is equivalent to a starting viewport width of 1280 CSS pixels wide at 400% zoom." is 18 words from Note 1, which is informative. It must be rejected (absent from `normativeText`). AA Notes (1.4.10, 1.4.12, 2.4.11 and 2.5.8) hold the most practical measurement detail, so scouts are most tempted to quote them.
4. **Case-folded title masquerade.** A 2.4.6 card with sourceQuote "Headings and Labels" (the title) passes a case-insensitive containment check against "Headings and labels describe topic or purpose." It must be rejected by a case-sensitive comparison and the five-word minimum.
5. **Cross-reference masquerade.** A 1.1.1 card with sourceQuote "Refer to Success Criterion 4.1.2 for additional requirements for controls and content that accepts user input." is 16 words, is contained in `normativeText`, and is unique to 1.1.1. Only an explicit cross-reference rule rejects it.
6. **List-label masquerade.** A 2.5.8 card with sourceQuote "Essential" is a `<dt>` label. It is contained in `normativeText` and must be rejected by the five-word minimum and the uniqueness rule.
7. **Cross-level misattribution.** A 2.4.6 (AA) card with sourceQuote "describe topic or purpose." is contained in both 2.4.6 and 2.4.2 (A). It must be rejected by uniqueness and the five-word minimum.
8. **False rejection, the inverse witness.** A 1.2.4 (AA) card copied faithfully from the source, "Captions are provided for all live audio content in synchronized media.", fails a raw containment check because `normativeText` has "synchronized media ." It must be **accepted** once the normalization rule below is applied.

## Narrow rule (smallest safe correction)

The tool, the counter (`measure.py`) and the self-test must all apply the same rule, deriving it independently. Ordered checks:

1. **Haystack.** Use `population.criteria[id].normativeText` only. Never use `text`. Using `text` in one consumer and `normativeText` in another creates two authorities that disagree on witnesses 1–3.
2. **Normalize the quote and every haystack identically.**
   - Collapse whitespace runs to a single space and trim.
   - Delete whitespace immediately before `,` `.` `;` `:` `)` and immediately after `(`.
   - Do not fold case, do not fold Unicode, and do not strip punctuation.
3. **Word count.** `len(normalized.split())` must be between 5 and 25.
   - The minimum of 5 is safe: the shortest body (2.4.6) is 7 words, and every `<dt>` label is 4 words or fewer.
   - Counting after normalization stops stray "," tokens inflating the count.
4. **Containment.** The normalized quote must be a case-sensitive substring of its own criterion's normalized `normativeText`.
5. **Uniqueness.** The normalized quote must not be a substring of any *other* criterion's normalized `normativeText`. All 55 criteria can satisfy this.
6. **Cross-reference.** Reject a quote that matches `\b(Success Criterion|Guideline) \d`. This fires only on the two parentheticals in 1.1.1.

### Disposition: L1's production rule (supersedes the PacketTool coordination)

The PacketTool seat is dead and uncredited, and its sandbox is evidence only. L1 owns production. L1 chose a rule of at least 6 words, word-boundary-normalized containment in `normativeText`, and a pin on the source hash, with no uniqueness check. My suggested finding IDs are withdrawn in favour of whatever L1 ships.

How L1's rule handles the witnesses above, assuming its normalization handles the extractor's space-before-punctuation artifact:

- **Witnesses 1–3 are rejected.** These are the doclink, heading and Note quotes. This is the core masquerade, and it is closed as long as the haystack stays `normativeText` and never `text`.
- **Witnesses 4, 6 and 7 are rejected by the six-word minimum.** These are the title "Headings and Labels" (3 words), the "Essential" label, and "describe topic or purpose." (4 words). Every `<dt>` label is 4 words or fewer, and the shortest body (2.4.6) is 7 words, so all 55 criteria can satisfy the minimum.
- **Witness 8 is accepted, provided normalization handles the artifact.** If it does, the faithful 1.2.4 quote passes.
- **Residual: witness 5 is accepted.** The 1.1.1 "Refer to Success Criterion 4.1.2 …" quote is 16 words, contained, and not excluded.
- **Residual: shared spans of six words or more cross levels.** Without uniqueness, a card at one level can be grounded in another level's text. Examples:
  - "repeated on multiple web pages within" (3.2.3 AA / 3.2.6 A)
  - "If an input error is automatically" (3.3.1 A / 3.3.3 AA)
  - "at least one of the following is" (2.1.4, 2.2.1 and 2.5.2, all A / 3.3.4 AA)

  This misattribution does not change the 55 count. It is acceptable only if reviewers spot-check quotes on these pairs.
- **Case sensitivity.** If L1's normalization folds case, witness 4 is still rejected, but only by the six-word minimum.

## Content-duplication and A/AA coverage risks

- **Duplicate authority inside the population.** `text` contains `normativeText` in full. Any consumer that greps `text`, including a scout copying from it, will reproduce heading, doclink and Note material. The fix is item 1 of the rule; no population change is needed.
- **Level parsing hazard.** "(Level A" is a prefix of "(Level AA)". Any validator that derives level from `text` by substring or prefix match would classify all 24 AA criteria as A. Levels must be compared by exact equality with `population.level`.
- **Per-level coverage is already implied.** Exact `id/title/level/source` equality plus "ids exactly once" across 55 already forces 31 A + 24 AA. No extra per-level field is required. 4.1.1 must be reported as an unexpected id, not silently counted.
- **Boilerplate shared across levels.** Without the uniqueness check, an AA card can carry an A criterion's quote and still be accepted (1.2.4↔1.2.2, 2.4.6↔2.4.2, 3.2.3↔3.2.6). This misattributes grounding without changing the 55 count.
- **Quote-cap bypass through prose fields.** The quote rule does not constrain `publisherCheck`, `failureExample` or `limitation`. Those fields can restate the full normative body or Note text as if it were a requirement. This is a risk to "narrow, grounded" prose, not to the packet's structure. It is out of scope for the mechanical check; reviewers should watch for it in AA cards that have Notes.
- **Expected scout rework.** 9/24 AA and 13/31 A criteria have Notes, and 30/55 have the punctuation artifact. Scouts copying from `text`, or from the rendered page, will hit witnesses 3 and 8. Rule 2 removes witness 8; witness 3 is a correct rejection.

## Impacted axes

- **Operability:** directly. Each defect above changes `accepted` or produces a false `clean` or `failed` verdict.
- **Freshness:** not impacted. The pinned hash and dated REC URL were verified.

## Tooling

No tools were installed or updated.
