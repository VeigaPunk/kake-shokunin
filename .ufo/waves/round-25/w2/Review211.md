# Review211 — Card 2.1.1 Keyboard (A), author-side falsify pass

- Reviewer: KakeR25.Review211 (author-side, not independent closure)
- Date: 2026-10-21
- Target: `corpus/knowledge/accessibility-review-cards.json` card `"id": "2.1.1"` (JSON lines 242–257 of the cards file)
- Source: S035 pinned REC, saved bytes `.ufo/waves/round-25/source-wcag22.html` section `id="keyboard"` (line 1109), population entry `.ufo/waves/round-25/population.json` (lines 186–195); §5.2.5 read at `id="cc5"` (line 2214)
- Method: read-only diff of every card field against the complete normative paragraph, both Notes, the linked `keyboard interface` definition (line 3177) and §5.2.5. No build, no website, no network target.

## Verdict: AGREE — card is source-faithful; no defects found

## Field-by-field verification

1. **Identity binding** — `"id": "2.1.1"`, `"title": "Keyboard"`, `"level": "A"`, `"source": "https://www.w3.org/TR/2024/REC-WCAG22-20241212/#keyboard"` all match the saved section (`<bdi class="secno">Success Criterion 2.1.1 </bdi>Keyboard`, `(Level A)`, anchor `keyboard`). Distinct from the AAA near-collision "Keyboard (No Exception)" (2.1.3, anchor `keyboard-no-exception`, absent from this card). ✓

2. **`sourceQuote`** — `"All functionality of the content is operable through a keyboard interface without requiring specific timings for individual keystrokes"` is a contiguous, case-sensitive, word-boundary substring of the population `normativeText` (18 words, inside the packet's 6–25 rule), taken from the criterion body, not a heading or note. ✓

3. **No added requirements** — `publisherCheck` paraphrase `"no step depends on how fast or how long an individual key is pressed"` maps onto "without requiring specific timings for individual keystrokes" without widening it (no silent extension to general timing limits, which belong to 2.2.1). `"confirming it can be reached and activated"` restates "operable through a keyboard interface"; it does not import focus-order obligations from 2.4.3. The inventory list is review method, not new normative scope. ✓

4. **Exception coverage (the only normative exception)** — `publisherCheck` substring `"why the underlying function (not merely the input technique) requires path-dependent input rather than just endpoints"` states the exception exactly as the normative clause "except where the underlying function requires input that depends on the path of the user's movement and not just the endpoints", with Note 1's distinction preserved. `evidenceNeeded` demands a per-exception justification tied to `"the reason its underlying function depends on the user's movement path"` — the correct burden; nothing weaker accepted. ✓

5. **No informative advice hardened into a MUST** — `limitation` substring `"providing mouse or other input methods in addition to keyboard is not forbidden"` tracks Note 2's "does not forbid and should not discourage" without converting the discouragement advice into an obligation. The `"With the pointer unused"` posture in `publisherCheck` is the reviewer's test condition, not a claim that pointer support is prohibited. ✓

6. **Failure example accurate, criterion-specific** — `failureExample`: drag-only reordering with `"no keyboard-operable alternative (such as move-up/move-down buttons)"`, and the discriminator `"even though the underlying function only needs start and end positions"` is exactly the test that defeats a claimed path exception. Not a misstatement; correctly implies a handwriting-style "path-dependent technique, path-independent function" case would NOT be a valid failure. ✓

7. **No source-only evidence laundered as conformance** — `evidenceNeeded`: `"Pointer-only handlers, scripts, or tool output alone are not sufficient evidence."`; `limitation`: `"Source inspection or automated scanning cannot confirm that all functionality is keyboard operable or that the path exception applies."`; `limitation` disclaims pass/fail/conformance; `"status": "not-assessed"`. Consistent with the packet's tool-readiness ≠ website-conformance rule. ✓

## Candidate findings raised and falsified (recorded so no one "fixes" the card into error)

- **Non-interference scope (falsified).** I initially suspected a gap: sibling card 2.1.2 demands `"All content on the page is in scope, even content that is not used to meet other criteria"` while card 2.1.1 never mentions embedded/third-party content. Source check of §5.2.5 (`source-wcag22.html` line 2214, `id="cc5"`) shows the all-content list is exactly "1.4.2, 2.1.2, 2.3.1, and 2.2.2" — 2.1.1 is deliberately not in it. The card's silence is source-correct; appending a non-interference sentence here would misstate the standard. No change.
- **Quote truncation before the exception clause (justified).** The full normative sentence including the exception is ~38 words, over the packet's 25-word quote cap, so `sourceQuote` cannot carry the exception. Not a defect: the exception is restated accurately in `publisherCheck` and `limitation`, so no reader is misled. No change.

## Residual risk / verification gaps

- `limitation`'s compression "(handwriting text input is not exempt)" is accurate only because the preceding clause "The exception concerns the underlying function, not the input technique" fixes the referent; read alone it is loose. Cosmetic only.
- The card does not restate the `keyboard interface` definition ("interface used by software to obtain keystroke input", usable without a physical keyboard, source line 3177–3197). Omission, not misstatement; the packet already directs reviewers to read the criterion and definitions.
- This is a documentation-fidelity pass only: no rendered-page keyboard testing occurred, and none may be inferred from the card or this review.

---
trailer: .ufo/waves/round-25/w2/Review211.md
