# Review412 — card 4.1.2 Name, Role, Value (A), round-25 author-side falsify wave

Reviewer: KakeR25.Review412 · 2026-10-21 · Read-only semantic review; no website tested; no r24 artifacts touched.
Target: `corpus/knowledge/accessibility-review-cards.json` card `4.1.2` vs pinned REC
`https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value`, saved bytes `.ufo/waves/round-25/source-wcag22.html`
(SC 4.1.2 section line 2127, normative sentence line 2134) and extracted `normativeText` in `.ufo/waves/round-25/population.json` line 490.

## Verdict

**Agree with one low-severity correction.** The card is source-grounded and correctly keeps
readiness (`not-assessed`) separate from website conformance. One clause in `publisherCheck`
narrows the change-notification prong below the normative sentence.

## Grounding checks performed (all pass)

- **id/title/level/source exact**: `4.1.2` / `Name, Role, Value` / `A` / `...REC-WCAG22-20241212/#name-role-value`
  match population.json lines 486–490 (anchor `name-role-value`) and the saved source heading "Success Criterion 4.1.2 Name, Role, Value" `(Level A)` (source line 2127).
- **sourceQuote verbatim, in bounds**: `"the name and role can be programmatically determined"` — 8 words (6–25 rule),
  case-sensitive, word-boundary aligned, present verbatim in `normativeText` (population.json:490) with only the
  documented spacing normalization before the following `;`. Not a heading, not a link label — it is criterion body text.
- **status**: `not-assessed`; limitation states the card "does not test any website" and that source reading or
  automated checkers alone cannot confirm runtime exposure — no source-only evidence is offered as conformance, and
  the tool-readiness/website-conformance boundary is preserved.
- **No added requirements / no informative→MUST conversion**: the only advisory text in the criterion is the Note
  ("standard HTML controls already meet this success criterion when used according to specification", source line 2136).
  The card cites it in `limitation` explicitly as "the non-normative note" and correctly does **not** extend its safe
  harbor ("misused or ARIA-modified native controls still need review"), which is the right contrapositive given the
  normative "For all user interface components" scope. The applicability nuance that a name may be hidden and only
  exposed by AT (definition `#dfn-name`, source line 3364) is handled by checking "the accessibility tree or an assistive
  technology", not visible labels — a criterion-specific trap this card avoids.
- **All three normative prongs represented**: (1) name+role programmatically determinable for *all* UI components
  ("including form elements, links, and script-generated or custom widgets" preserves "including but not limited to");
  (2) "programmatically set" correctly limited to *user-settable* states/properties/values (examples checked, expanded,
  selected, slider value) — matching "that can be set by the user"; (3) change notification — see finding.
- **failureExample not a misquote**: the REC normative text contains no failure examples, so nothing to misstate; the
  scripted-div disclosure lacking name/role/expanded state is consistent with the criterion and with the
  `#dfn-user-interface-components` definition ("perceived by users as a single control for a distinct function", notes
  at source lines 3984–3996).

## Findings

### LOW — notification prong narrowed: items scoped and observation window restricted

- **Card field**: `publisherCheck`
- **Exact substring**: `Then confirm that changes to these items are announced to or detectable by user agents, including assistive technologies, after the user interacts with the component.`
- **Defect (criterion-specific)**: two narrowings relative to the normative sentence
  `"...and notification of changes to these items is available to user agents, including assistive technologies."`
  (population.json:490; source line 2134):
  1. In the card, "these items" grammatically tracks only the immediately preceding user-settable *states, properties,
     or values* sentence. In the criterion, "these items" covers the **name and role as well**; a component whose
     accessible name or role changes (e.g. a toggle whose name flips between Play and Pause) falls under the
     notification prong, and the card gives the reviewer no cue to capture that.
  2. "after the user interacts with the component" restricts observation to user-initiated change, while the linked
     `#dfn-states` definition (source line 3799) says a state "may change in response to user action **or automated
     processes**"; script/async-driven state or value changes are equally in scope of the notification prong.
  The `evidenceNeeded` field ("before and after interaction") inherits the same narrowing.
- **Minimal correction**: in `publisherCheck`, replace the substring with:
  `Then confirm that changes to the name, role, states, properties, or values — whether from user interaction or automated processes — are available to user agents, including assistive technologies.`
  (and mirror it in `evidenceNeeded` by recording before/after states for observed changes, not only interaction-driven ones).

### Note (explicitly not counted a defect)

- `announced to or detectable by user agents` is a looser paraphrase of the normative "notification … is available to
  user agents" — announcement is what an AT does with the notification, and requiring an observed announcement from a
  specific AT could over-require. The card's either/or ("announced to **or** detectable by") keeps the evidentiary bar
  consistent with availability via accessibility APIs, so it is an acceptable operationalization, not a raised requirement.

## Residual risk

- If the LOW clause goes uncorrected, a card-following reviewer could build an interaction-only change log and miss a
  name/role change or a scripted state change — but the packet workflow (step 2 of accessibility-review-packet.md)
  requires reading the normative source alongside the card, which bounds the miss to evidence-shape, not to a conformance claim.

## Verification gaps

- Review covered only card `4.1.2` as assigned; sibling cards, the packet script, and the 55-card inventory counts were not re-verified here.
- No runtime/AT behavior was observed (out of scope for this packet by design); the finding concerns card wording only.
