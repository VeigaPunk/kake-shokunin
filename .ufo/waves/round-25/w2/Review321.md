# Review 3.2.1 On Focus (A) — criterion card semantic review

Scope: card `id "3.2.1"` in `corpus/knowledge/accessibility-review-cards.json` (lines 506–525) against the pinned saved source `.ufo/waves/round-25/source-wcag22.html`, anchor `#on-focus` (section starts line 1859), and extracted `.ufo/waves/round-25/population.json` entry at lines 385–392. Author-side falsify attempt, not r24 replay; read-only.

## Verdict: AGREE — card is clean; no defect found

## Identity binding (exact, verified)

- `id` `"3.2.1"` — matches population and source `<section id="on-focus">` heading "Success Criterion 3.2.1".
- `title` `"On Focus"` — exact source heading text.
- `level` `"A"` — matches source `<p class="conformance-level">(Level A)</p>` at the criterion.
- `source` `https://www.w3.org/TR/2024/REC-WCAG22-20241212/#on-focus` — pinned REC 2024-12-12 anchor.
- `status` `"not-assessed"` — held; card makes no website-conformance claim.

## Criterion-specific checks that pass (why "clean" is earned, not counted)

1. **Quote is verbatim normative body, not a heading.** `sourceQuote` `"When any user interface component receives focus, it does not initiate a change of context"` is a 16-word word-boundary substring of population `normativeText` (population.json line 391) and of the source sentence at source-wcag22.html line 1865. Case-sensitive, within the 6–25-word rule, taken from the criterion body — the packet's own warning against substituting the heading does not apply.

2. **No added requirements.** The criterion has exactly one sentence and no notes, exceptions, or linked clauses in the saved source (lines 1859–1866). The card invents none: `publisherCheck` adds only review procedure ("Move focus… record whether… Repeat…"), not normative obligation, and never converts the criterion's informative context into a MUST.

3. **No omitted exceptions — none exist.** Unlike 3.2.2 (advice-of-behavior escape hatch) there is no exception clause in 3.2.1 to omit; the card correctly does not fabricate one (e.g., it does not borrow 3.2.2's "user has been advised" exception or 2.2.x timing exceptions).

4. **Change-of-context examples track the definition, not a blanket claim.** `publisherCheck`'s list ("opening a new window or tab, navigating to another page, submitting a form, moving focus elsewhere, or substantially changing page content that alters its meaning") maps onto the definition at `#dfn-change-of-context` (source line 2716): viewport/user agent, new page, focus, and "content that changes the meaning of the web page" — and mirrors that definition's own example sentence ("Opening a new window, moving focus to a different component, going to a new page…"). Critically, the card conditions content change on "alters its meaning", which respects the definition's note that "A change of content is not always a change of context" (expanding outlines, dynamic menus, tab controls). This is exactly the blanket-claim trap this criterion invites, and the card avoids it.

5. **Focus is separated from activation.** `publisherCheck` requires moving focus "without activating anything" and judges "merely receiving focus" — correctly scoping to focus-initiated context changes, leaving setting changes to 3.2.2 and activation to the user. No conflation with sibling criteria.

6. **Failure example is criterion-true.** `failureExample` (focus-event script opening a new browser window on tab-in, "before the user presses Enter") matches the known failure pattern for this criterion (script attached to a link/form-field focus event triggering a context change on focus); it is not a misstated or borrowed failure example.

7. **No source-only evidence offered as conformance.** `limitation` explicitly states source inspection and automated scanners "cannot show what happens when each component actually receives focus at runtime" and that "no claim of pass, fail, inapplicability, or conformance is made" — consistent with the packet's tool-readiness-never-conformance boundary.

## Residual risk (not defects)

- `publisherCheck`'s "such as" context-change list omits change of **user agent** (a definition-enumerated change, e.g. a focus handler invoking an external protocol/app). The list is explicitly non-exhaustive, so this is acceptable, but a reviewer should read the definition, not just the card list.
- Procedure completeness: components reachable only programmatically (no keyboard or other offered focus mechanism) would not be exercised by the stated methods; such a component would additionally implicate 2.1.1, and `evidenceNeeded`'s "focus method used" already forces the reviewer to record coverage per component.
- "submitting a form" is listed as a possible manifestation of a focus-initiated context change, not as a context change per se; a same-page submission with no meaning change is outside the criterion. The card's phrasing ("record whether merely receiving focus initiates a change of context, such as…") already carries this conditioning.

## Field map for any future correction

None required. All checked fields: `id`, `title`, `level`, `source`, `sourceQuote`, `publisherCheck`, `evidenceNeeded`, `failureExample`, `limitation`, `status`.

Source anchors used: `#on-focus` (criterion body, Level A marker), `#dfn-change-of-context` (definition + note + example), `#dfn-user-interface-components` (definition; card's "every user interface component" scope matches "perceived by users as a single control", including script-generated components per Note 2).
