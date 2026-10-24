# Review134 — Card 1.3.4 Orientation (AA) — author-side falsify wave

Round 25, criterion card 1.3.4 in `corpus/knowledge/accessibility-review-cards.json`, checked against pinned S035 (`https://www.w3.org/TR/2024/REC-WCAG22-20241212/#orientation`, retained bytes `.ufo/waves/round-25/source-wcag22.html`, extracted entry `.ufo/waves/round-25/population.json`). Packet-doc status rule applied: card readiness is tool/packet operability, never website conformance.

## Verdict: AGREE — card is faithful to the pinned criterion

## Grounding checks (all pass, evidence cited)

- **id/title/level/source exact.** Card `"id": "1.3.4"`, `"title": "Orientation"`, `"level": "AA"`, source URL `#orientation` match the source heading "Success Criterion 1.3.4 Orientation", the "(Level AA)" conformance label (source line 708), and the population entry anchor `"orientation"`. Exactly one card with this id; no duplicate.
- **Quote legal.** `sourceQuote` is 25 whitespace-delimited words (rule allows 6–25), case-sensitive, word-bounded, and verified substring of the population `normativeText` ("Content does not restrict its view … is essential"). It is taken from the criterion body (source line 710), not the heading, doclinks, or the Note (line 712).
- **status `not-assessed`** present; the card's own limitation restates "Packet readiness only; no website was evaluated".

## Criterion-specific falsification attempts (all failed to find a defect)

1. **Added requirements?** The publisherCheck's source-review steps (CSS orientation media queries, manifest `orientation`, script `screen.orientation.lock()`) are card-authored review aids, not attributed to WCAG; the limitation explicitly demotes them: "Finding orientation code in source does not prove a restriction, and finding none does not prove content works in both orientations". No WCAG-external obligation is presented as normative.
2. **Omitted exceptions?** The SC's only exception is "unless a specific display orientation is essential". The card preserves it, requires a per-restriction written rationale, and points to the WCAG definition. The glossary definition (source `#dfn-essential`, lines 2967–2973) is "if removed, would fundamentally change the information or functionality of the content, **and** information and functionality cannot be achieved in another way that would conform" — the card's pointer targets this, not a shortened substitute.
3. **Informative → MUST?** The Note ("Examples where a particular display orientation **may** be essential…") is correctly kept informative: the limitation says its examples "are cases where it may be essential, not automatic exemptions". No blanket claim that piano apps/bank checks are exempt, and no claim that non-listed content can never be essential — both distortions avoided.
4. **Both normative prongs covered.** SC restricts "view **and** operation"; the check tests locked content, hidden/overlay-blocked content (view) and "made inoperable in the other" (operation); evidenceNeeded requires captures showing "content and controls remain viewable and operable".
5. **Misstated failure example?** The rotate-to-portrait overlay over recipe steps in landscape restricts view/operation in the other orientation "even though nothing about the recipe requires portrait" — realistic, matches the SC wording, and explicitly negates the essential exception. No invented failure mode from another criterion.
6. **Source-only conformance?** Explicitly negated in the limitation; human rendered review of both orientations is required as evidence. Status stays `not-assessed`; no conformance claim anywhere in the card.

## Minor observations (not defects; no correction required)

1. **Field `publisherCheck`, substring:** "and it cannot be achieved another way that would conform". Lossy anaphor: the `#dfn-essential` second conjunct is "information and functionality cannot be achieved in another way that would conform"; "it" is ambiguous. Low risk because the same sentence says "check that reason against the WCAG definition of essential", making the glossary operative. Minimal correction if ever touched: "and the information and functionality cannot be achieved in another way that would conform".
2. **Field `publisherCheck`, substring:** "view it in portrait and in landscape display orientation". Unscoped for delivery on displays that cannot change orientation (fixed desktop monitors, kiosks), where such captures are meaningless. The pinned normative text states no such exception, so this is a review-method nuance, not a misstatement of the SC; the limitation's content-attribution scoping partially contains it.

## Residual risk

The card is a work aid; whether an orientation is "essential" remains a human judgment against `#dfn-essential` that no packet field can settle. The portrait/landscape capture instruction assumes a device that supports both orientations; a future reviewer on fixed-orientation hardware must adapt the method rather than skip it.

## Verification gaps

None in scope: pinned source, population entry, and card all read from the retained round-25 artifacts; no live website, browser, or network target was touched, per lane bounds.
