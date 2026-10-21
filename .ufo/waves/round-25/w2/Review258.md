# Review258 — card 2.5.8 Target Size (Minimum) (AA)

Author-side falsify pass (lane: leaf reviewer, no dispatch). Card compared field-by-field
against the pinned REC bytes at `.ufo/waves/round-25/source-wcag22.html` (sha-pinned S035,
§ `target-size-minimum`, lines 1740–1763) and the extracted section in
`.ufo/waves/round-25/population.json:357-365`. No installs performed (none needed);
read-only — only this report written.

**Verdict: AGREE — no High/Medium defects. Card is semantically faithful.** Three
Low/Informational notes below, none blocking.

## Verified clean (criterion-specific, not a count)

- **Identity**: `id` "2.5.8", `title` "Target Size (Minimum)", `level` "AA" match
  source lines 1740/1744 (`<bdi class="secno">Success Criterion 2.5.8 </bdi>Target Size (Minimum)`,
  `(Level AA)`); `source` is the exact pinned anchor URL. Frozen copy
  (`.ufo/waves/round-25/frozen/cards.json:470-487`) is byte-identical to the live card.
- **sourceQuote** `"The size of the target for pointer inputs is at least 24 by 24 CSS pixels"`
  — 16 words (within 6–25), case-sensitive contiguous span of the criterion body
  (population `normativeText`, extractor space before the comma normalizes away), NOT one of
  the tempting informative-note quotes w1/QuoteCritic flagged for 2.5.8 (Note 1's
  slider/color-picker wording) nor the `<dt>` label masquerade ("Essential").
- **All five normative exceptions present and paraphrased faithfully** (source lines 1748–1759):
  - Spacing: card `"intersects no other target and no other undersized target's circle"` ≡
    source `the circles do not intersect another target or the circle for another undersized target`
    (De Morgan equivalent; 24 CSS pixel **diameter**, centered on the **bounding box** — both kept).
  - Equivalent: `"another control on the same page performs the same function and meets the criterion"`
    keeps the two load-bearing limits — **same page** (not same site) and the replacement control
    itself must meet 2.5.8.
  - Inline: dropping the source's `"otherwise"` changes nothing; `"constrained by the line-height of
    non-target text"` preserved.
  - User Agent Control: `"the user agent sets the size and the author has not changed it"` ≡
    `determined by the user agent and is not modified by the author`.
  - Essential: `"essential or legally required for the information conveyed"` matches the
    dual limb (`essential` / `legally required`), linked to `presentation` as in source.
- **No informative→MUST conversion**: Note 1 (spatially-selected targets count as one target) is
  correctly confined to `limitation` as `"The saved informative Note 1 … adds no requirement"` —
  its paraphrase (sliders / gradient colour pickers / editable areas) matches source Note 1 and it
  is nowhere turned into a check obligation.
- **No added requirement / no conformance drift**: `publisherCheck` and `evidenceNeeded` are review
  instructions on the publisher's inventory, ending in `"Mark any undersized target that has no
  documented exception for human follow-up"` — no pass/fail verdict is manufactured;
  `failureExample` ends `"a reviewer should flag it"`, not "fails WCAG"; `status` is
  `not-assessed`; `limitation` explicitly disclaims passed/failed/not-applicable/conformant and
  disallows source/CSS reading as evidence of rendered size.
- **failureExample arithmetic checks out**: 16×16 buttons with 2 px gaps → adjacent circle centers
  8+2+8 = 18 px apart, 24 px-diameter circles (r=12) intersect (18 < 24), and each circle also
  reaches 2 px past its own bounding box into the neighbour target (10 < 12); with no equivalent
  control, not inline, author-set sizes, Spacing/Equivalent/Inline/UAC are correctly all dead.

## Findings

### Low

1. **`evidenceNeeded` — Inline evidence omits Note 2's perpendicular-line-height rule.**
   Card substring: `"the surrounding sentence or line-height for inline targets"`. The pinned
   criterion's Note 2 (informative, source line 1761–1762) reads: "For inline targets the
   line-height should be interpreted as perpendicular to the flow of text. For example, in a
   language displayed vertically, the line-height would be horizontal." A reviewer measuring
   line-height along the flow on a vertical-text page (vertical CJK, rotated rail navigation)
   would mis-test the Inline exception. Minimal correction: extend the substring to
   `"the surrounding sentence or line-height measured perpendicular to the flow of text for
   inline targets (informative Note 2)"`. Not a conformance error — Note 2 is informative —
   but it is the one measurement detail this AA card's evidence list silently drops.

2. **`publisherCheck` — measurement ignores the overlapping-targets rule in the normative-linked
   definition of `target`.** Card substring: `"list every pointer target … and record its rendered
   size in CSS pixels"`. The pinned glossary `dfn-targets` note (source lines 3871–3877) reads:
   "If two or more targets are overlapping, the overlapping area should not be included in the
   measurement of the target size, except when the overlapping targets perform the same action or
   open the same page." Raw bounding-box capture of stacked/overlapping controls (icon overlaying
   a card link, badge over a button) can misclassify an adequately sized target as undersized, or
   vice versa. Minimal correction: append to `publisherCheck`:
   `"Where targets overlap, measure the non-overlapping area (same-action overlaps measure whole)."`

### Informational

3. **`failureExample` — `"has no applicable exception"` stipulates rather than excludes Essential.**
   The scenario rules out Spacing (circles intersect), Equivalent (`"no other control for the same
   actions"`), Inline (toolbar, not a sentence) and UAC (explicitly author-set 16×16/2 px sizes),
   but never states the presentation is inessential. Minimal correction (optional, hypotheticals
   elsewhere in the packet are equally stipulated): append `"and the compact presentation is not
   essential"`.

## Residual risk and verification gaps

- Exceptions Essential/Equivalent are irreducibly human judgments; the card's `limitation` already
  says automated measurement cannot judge them — accurate, and no residual card text contradicts it.
- The card deliberately scopes to per-page state snapshots (`"hover, open menus, dialogs"`); it
  does not enumerate pointer-input device variance (touch vs mouse hit-testing slop). Out of scope
  for the criterion text itself, which fixes size in CSS pixels; not counted as a defect.
- Did not re-run `packet_selftest.py`/`frozen_replay.py` (not assigned; main runs the suite once
  after integration). Quote containment was verified manually against `population.json`
  `normativeText` under the packet's whitespace-collapse rule.
