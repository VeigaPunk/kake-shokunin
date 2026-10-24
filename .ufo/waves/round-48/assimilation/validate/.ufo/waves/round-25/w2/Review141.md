# Review141 — Card 1.4.1 Use of Color (A), r25 w2 author-side falsify

Verdict: **AGREE — card is clean.** No defect found at any card field. Criterion-specific reasons below; every claim was checked against the saved REC bytes, not memory.

## Structural grounding (all verified)

- `id` = "1.4.1", exactly one card with that id (duplicate-id scan over the whole cards file: none).
- `title` = "Use of Color" matches `<h4>Success Criterion 1.4.1 Use of Color</h4>` at `source-wcag22.html` line 749 (section `id="use-of-color"`).
- `level` = "A" matches `<p class="conformance-level">(Level A)</p>` at line 753.
- `source` = `https://www.w3.org/TR/2024/REC-WCAG22-20241212/#use-of-color` matches the pinned anchor and the population entry's `anchor` = "use-of-color".
- `sourceQuote` (23 words, within the ≤25 rule): "Color is not used as the only visual means of conveying information, indicating an action, prompting a response, or distinguishing a visual element." — verified a whitespace-normalized exact substring of `population.json` → 1.4.1 `normativeText`, which itself corresponds to the criterion body `<p>` at source lines 755–757. The quote is the full normative body, not a heading; the packet rule that excludes note wrappers was respected (the Note text is not quoted anywhere in the card).
- `status` = "not-assessed" — packet readiness, never a website result. No field in the card offers source-only evidence as conformance.

## Criterion-specific prose checks (why the prose is right, not just present)

1. **All four normative verbs are covered, in the criterion's own terms.** The saved body sentence has exactly four operative phrases; `publisherCheck` maps each: conveyed information ("status, categories, chart series, required or invalid fields"), indicated action ("links within text, selected or active controls"), prompt for a response, and "visual elements that must be told apart" (distinguishing). No fifth obligation was invented and none of the four was dropped.

2. **Non-color cue list is open-ended and visual-only — correctly.** `publisherCheck` says "a non-color visual cue … such as text, a label, an icon, a pattern, a shape, underlining, or position" — introduced by "such as", so the list is illustrative, not a new requirement. Including "position" is correct: the criterion bans color as the *only* means, so position alone suffices. Crucially the card requires a *visual* cue and never claims a programmatic-only cue (e.g. an ARIA attribute) satisfies 1.4.1 — the most likely conflation for this criterion, and the card avoids it, consistent with the Note's redirect to Guideline 1.3.

3. **Informative advice kept informative.** `publisherCheck`: "Viewing the item in grayscale is **one way** to check…" — the grayscale heuristic (a known but imperfect proxy for color-vision deficiency) is offered as an option, not converted into a MUST for conformance.

4. **`limitation` claims are true of this criterion specifically.**
   - "does not set any contrast ratio and lists no exceptions" — verified: the saved 1.4.1 section (lines 749–758) contains no ratio, no exception `<dl>`, no exemption clauses; ratio requirements live in 1.4.3/1.4.11. This is a valuable criterion-specific guard against conflating 1.4.1 with its contrast siblings.
   - "normative wording covers visual means only; the informative note sends programmatic access to color and other visual coding to Guideline 1.3" — verified against the Note at line 757: "This success criterion addresses color perception specifically. Other forms of perception are covered in Guideline 1.3 including programmatic access to color and other visual presentation coding." Faithful paraphrase, no quote abuse. Calling the note "informative" is grounded in the REC itself: §5.1 (line 2167) states notes are informative, and the glossary `informative` = "for information purposes and not required for conformance" (lines 3135–3137).
   - "Source inspection or automated tools cannot tell when color is the only cue, because they cannot judge what a color means to a reader" — defensible: deciding whether color is the *only* cue requires interpreting rendered meaning, which is exactly the human judgment the packet's decision table reserves for reviewers.
   - "Completing this card does not establish conformance" — matches the packet's conformance-boundary section.

5. **`failureExample` misstates nothing.** Invalid fields marked only by a red border, with no error text, icon, or other visual change, is squarely within "conveying information / prompting a response" for 1.4.1 and mirrors the classic color-only form-field failure pattern (Understanding doc scenario, F81-family). It makes no pass/fail/conformance claim about any real site.

## Observations considered and rejected as defects

- `evidenceNeeded` mandates grayscale screenshots while `publisherCheck` calls grayscale "one way": not a defect. Evidence requirements are the packet's own documentation discipline (the packet doc: "These are local packet-grounding rules, not additional WCAG requirements"); mandating a capture preserves the reviewer's stated basis and asserts nothing about WCAG.
- No important omission: 1.4.1's normative body contains no linked definitions (verified — no `internalDFN` anchors in the body `<p>`), so there is no definition the card failed to carry; the only linked material is the informative Note, which the limitation surfaces.

## Residual risk / verification gaps

- Quote containment was checked by direct string comparison against `population.json` `normativeText` (both sides whitespace-normalized); the packet's own `quote_proof.py`/selftests were not run — not an assigned check command for this lane. Given the quote has no punctuation-spacing anomalies, strict containment also holds.
- The card is correct as a work aid; per the packet contract it still cannot close a 1.4.1 conformance question for any real page — human rendered-context review remains required, as the card itself states.
- No tool installs or updates were performed for this review (none needed).
