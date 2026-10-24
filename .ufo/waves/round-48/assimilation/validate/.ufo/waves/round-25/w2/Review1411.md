# Review1411 — Card 1.4.11 Non-text Contrast (AA)

Reviewer: KakeR25.Review1411 (author-side falsify, leaf lane). Scope: only card `1.4.11` in
`corpus/knowledge/accessibility-review-cards.json` against the pinned source
`.ufo/waves/round-25/source-wcag22.html` (REC 2024-12-12, section id `non-text-contrast`,
source lines 1022–1040) and `.ufo/waves/round-25/population.json` id `1.4.11`.
No website, browser, network, or r24 artifacts touched. No installs performed.

## Verdict: AGREE — no defect found

### Binding fields (all verified exact)

- `id` `1.4.11`, `title` "Non-text Contrast", `level` "AA", `source`
  `https://www.w3.org/TR/2024/REC-WCAG22-20241212/#non-text-contrast` — match the saved
  source heading `<bdi class="secno">Success Criterion 1.4.11 </bdi>Non-text Contrast` and
  `(Level AA)` (source lines 1022, 1026); exactly one card in the file.
- `status` `not-assessed` — kept; `limitation` correctly states "no website was evaluated, so
  no claim of pass, fail, inapplicability or conformance is made", matching the packet's
  readiness-vs-conformance boundary.
- `sourceQuote` "The visual presentation of the following have a contrast ratio of at least
  3:1 against adjacent color(s)" — 17 words (6–25 allowed), verbatim substring of
  `normativeText`, from the criterion body paragraph (source line 1028), not the heading.

### Criterion-specific fidelity checks (why this card is sound, not just clean-looking)

1. **3:1 threshold stated correctly.** `publisherCheck` uses 3:1 throughout; it never drifts
   to the 4.5:1 text ratio of 1.4.3 — the classic 1.4.11 card error is absent.
2. **Both bullets covered with the criterion's own scoper.** The check measures only "the
   visual information required to identify the component and each of its states" and "the
   parts required to understand the content" — mirroring the normative qualifiers
   "Visual information required to identify user interface components and states" and
   "Parts of graphics required to understand the content". No over-application of 3:1 to
   decorative or non-identifying visuals.
3. **All three normative exceptions present and correctly assigned per item** (source line
   1034/1038): inactive components; appearance determined by the user agent and not
   modified by the author; graphics whose particular presentation is essential. The card
   applies them per item and demands a recorded reason ("Record each exception claim with
   its reason rather than skipping the item"), consistent with the packet's documented
   applicability-judgment rule — no silent skips, no invented exceptions.
4. **Failure example is realistic and arithmetically correct.** #DDDDDD on #FFFFFF:
   L(#DDD) = ((221/255 + 0.055)/1.055)^2.4 ≈ 0.7231 → ratio = 1.05/0.7731 ≈ 1.36:1, which
   the card's "about 1.4:1" accurately reports at one-decimal rounding; 1.36 < 3:1 fails as
   claimed. The example correctly conditions failure on the border being "the only visual
   information identifying the input" — the identification-scoper, not a blanket rule.
5. **States handled without scope creep.** `publisherCheck` names focus indicators,
   selected/checked marks and error state as state examples — states are in-scope under
   "…components and states" (source line 1034). No claim that 1.4.11 governs text contrast.
6. **No informative-advice inflation.** `evidenceNeeded`'s "Rendered measurements are
   required … source color tokens alone do not establish them" is packet-local evidence
   policy in the packet's own field, matching the packet doc's declared local grounding
   rules; it is not presented as a WCAG requirement and the `limitation` keeps the
   conformance boundary intact. Automated/source-only checks are correctly downgraded to
   insufficient for the human judgments this criterion requires.
7. **Nothing important omitted.** The pinned normative section contains only the
   intro paragraph and the two-item definition list (source lines 1028–1040; no Note in the
   REC section), and the card reflects all of it.

### Residual notes (non-defects, for the record)

- Handling of variable/multi-color adjacent backgrounds lives in the informative
  Understanding document, not the REC section; the card does not restate it, which is
  acceptable because the packet mandates reading the normative source and definitions
  alongside the card. The card also does not misstate any such guidance.
- "about 1.4:1" is 1.36:1 rounded; exact enough under "about".

No `exact card field/substring` corrections are proposed.
