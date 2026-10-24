# Review — WCAG 2.5.1 Pointer Gestures

**Verdict: Agree — no defects requiring correction.** Card 2.5.1 (`corpus/knowledge/accessibility-review-cards.json:410-420`) is bound to the pinned criterion and stays inside its normative scope. Two wording notes below are Low/Informational; neither changes a conformance-relevant statement. Everything was checked against the saved Recommendation bytes (`.ufo/waves/round-25/source-wcag22.html`) and the extracted population entry (`.ufo/waves/round-25/population.json:313-322`); no website, browser, or runtime was touched.

## Findings

### Low — `evidenceNeeded` presumes the alternative's gesture form

**Card field:** `evidenceNeeded`; substring: "a human activating each alternative with a single tap or click".

**Source:** `source-wcag22.html#pointer-gestures` (line 1630) requires operation "with a single pointer without a path-based gesture"; `source-wcag22.html#dfn-single-pointer` Note (line 3779) lists clicks, double clicks, taps, dragging motions, and single-finger swipes as single-pointer interactions. The criterion admits any single-pointer interaction that is not path-based (e.g. a double click or press-and-hold), but this evidence clause fixes the demonstration to "a single tap or click" without the "for example" framing the card's `publisherCheck` uses. A reviewer following it literally could record only tap/click demonstrations, or treat a non-tap single-pointer alternative as unsupported.

**Minimal correction:** "…a human activating each alternative with a single pointer and no path-based gesture (for example a single tap or click), plus the browser, device, and input type used."

### Informational — exclusion list adds "operating system" beyond the pinned Note

**Card field:** `publisherCheck`; substring: "Leave out gestures that only operate the browser, operating system, or assistive technology."

**Source:** the criterion's Note (`source-wcag22.html` line 1632) excludes only "actions that are required to operate the user agent or assistive technology". Adding the OS widens an exclusion, but it cannot create a false exclusion here: a gesture that *only* operates the OS is never interpreted by "the page's own scripts", which is the card's own primary scoping sentence, so the sets do not overlap. No correction required; optional alignment: "…the user agent (browser), or assistive technology."

## Checked and clean (criterion-specific)

- **Identity binding exact.** id `2.5.1`, title "Pointer Gestures", level `A`, source `https://www.w3.org/TR/2024/REC-WCAG22-20241212/#pointer-gestures` all match `population.json:313-318` and the saved heading "Success Criterion 2.5.1 Pointer Gestures" / "(Level A)" at `source-wcag22.html:1624,1628`, section `id="pointer-gestures"`.
- **Quote is located and well-formed.** `sourceQuote` (cards.json:415) is a case-sensitive, word-boundary-exact 21-word substring of `normativeText` (`population.json:322`), ending before the ", unless … essential" clause. The truncation is packet quote-rule-driven (6–25 words) and the exception is not lost — see next point.
- **The essential exception is not omitted.** `publisherCheck` (cards.json:416) requires recording an essential claim plus reason when no alternative exists, and `limitation` (cards.json:419) requires a human to check "that a claimed essential exception holds". The two-pronged bar ("cannot be achieved in another way that would conform", `source-wcag22.html#dfn-essential`, lines 2967-2974) is not restated in the card, but packet doc step 2 directs reviewers to read the criterion's linked definitions, and the card never waters the exception down into a self-serving claim. This is the criterion's only exception; none is missing.
- **No added requirement, and no keyboard substitution.** The demand "one pointer and no path" mirrors "operated with a single pointer without a path-based gesture" (line 1630) exactly; the card nowhere suggests keyboard operability satisfies 2.5.1, unlike generic a11y checklists. Alternatives are framed as examples ("for example a single tap or click"), not an exhaustive form.
- **Gesture taxonomy is sound.** Pinch/two-finger swipe/rotate are multipoint (two pointers at once, `#dfn-single-pointer` Note line 3779); swipe/drawn shapes are path-based. "Two-finger swipe" is arguably both classes, harmless under the criterion's "multipoint or path-based" disjunction. Notably, the card avoids the classic trap: a single-finger swipe-only carousel is still a failure because the swipe is path-based even though single-finger swipes count as single-pointer interactions — exactly what the `failureExample` asserts.
- **Scope note is faithful.** `limitation`'s "applies only to pointer actions interpreted by web content, not to actions needed to operate the user agent or assistive technology" paraphrases the pinned Note (line 1632) without extension of normative weight; no informative note is quoted as a MUST anywhere in the card.
- **No source-only evidence as conformance.** `limitation` states source reading and automated scanners "cannot show" the alternative works or the exception holds, and the card "makes no pass, fail, applicability, or conformance determination"; `status` is `not-assessed` (cards.json:420).
- **Cross-reference correct.** "Dragging movements are reviewed separately under 2.5.7" matches the packet's 2.5.7 Dragging Movements (AA) card; 2.5.1 coverage of path-based drags is preserved by the card's path-based listing step.

## Residual risk and verification gaps

Review is textual against saved bytes only; no LSP server is involved (documentation JSON/HTML, no code semantics), no packet check command was run (not assigned to this lane), and no tools were installed or updated. Whether the "operating system" exclusion or the tap/click evidence wording ever misleads a real reviewer is untested by definition here — both are recorded above with corrections should the author want belt-and-braces tightening. This is an author-side falsification pass, not independent closure; the card remains `not-assessed` and claims no website conformance.
