# Review337 — Card 3.3.7 Redundant Entry (A), author-side falsify wave

Scope: only `corpus/knowledge/accessibility-review-cards.json` card `3.3.7` against the pinned
saved source `.ufo/waves/round-25/source-wcag22.html` (S035, WCAG 2.2 REC 2024-12-12,
`#redundant-entry`) and its extraction in `.ufo/waves/round-25/population.json`.
No live website, browser, network, or r24 artifact was touched.

## Verdict: AGREE (card is accurate; no blocking defect found)

### Verification performed (criterion-specific)

1. Identity binding correct. Card `id` `"3.3.7"`, `title` `"Redundant Entry"`, `level` `"A"`
   match the saved source heading "Success Criterion 3.3.7 Redundant Entry" and
   `(Level A)` (source-wcag22.html:2036, :2040). The `source` URL is the exact pinned
   anchor and matches `population.json:470`. The id occurs once in the cards file
   (no duplicate-criterion defect).
2. `sourceQuote` is grounded and inside `normativeText`.
   Card quote: `required to be entered again in the same process is either: auto-populated, or available for the user to select.`
   = 19 whitespace-delimited words (within 6–25), case-sensitive, starts/ends at word
   boundaries, and is a contiguous substring of the extracted `normativeText`
   (population.json:472). It comes from the criterion body, not a heading or note
   (3.3.7 has no notes in the saved source).
3. Requirement restated without inflation. The card's two mechanisms
   ("auto-populated or offered for selection") match the normative disjunction
   (source-wcag22.html:2043-2047). Its concrete examples ("same as shipping address"
   option, choice list) are explicitly marked "for example" — informative advice is not
   converted into a MUST.
4. All three normative exceptions present and correctly scoped to "Where neither is
   offered": re-entry essential / security of the content / information no longer valid
   (source-wcag22.html:2050-2054). None omitted, none added.
5. Trigger parity preserved: normative "Information previously entered by or provided to
   the user" is carried as "information the user already entered or was given earlier in
   the same process" (`publisherCheck`), keeping both the entered and provided branches.
6. Same-process boundary kept, not widened. `limitation` states "Information from a
   different process is outside this criterion's scope", matching the normative "in the
   same process" and the glossary definition of process (source-wcag22.html:3484-3487).
7. No conformance leakage. `status` is `"not-assessed"`; `failureExample` describes a
   flow property (no reuse option, no prefill) rather than source-only evidence;
   `limitation` explicitly declares "no pass, fail, inapplicability, or conformance" and
   defers which-fields-repeat and exception-legitimacy judgments to a human walkthrough.
8. Failure example is a genuine instance of the criterion, not a misstatement: at step 3
   the same information (the address the user already typed) is required again with
   neither mechanism — the example's own wording "type the same address again" asserts
   the sameness that makes it in scope.

## Defects

None at critical, major, or minor severity.

## Non-blocking observations (polish suggestions, not defects)

- Observation O1 — `publisherCheck`, substring `record every field asking for information the user already entered or was given earlier in the same process`:
  the normative trigger is information "required to be entered again"; an optional
  repeated field need not offer either mechanism and is not a failure. The card's
  exception step slightly over-captures optional fields. Minimal correction: qualify
  with "that the user is required to complete" (or note optional repeated fields are
  out of the criterion's trigger). Evidence still gates any finding, so no false
  conclusion can be drawn today.
- Observation O2 — `publisherCheck`, substring `re-entry is essential`: the saved source
  does define "essential" in its glossary (source-wcag22.html:2968-2973: "if removed,
  would fundamentally change the information or functionality of the content ... and
  information and functionality cannot be achieved in another way that would conform").
  Minimal correction: add a pointer to that glossary entry so reviewers justify the
  essential exception against its definition (contrast 3.3.8, whose card correctly notes
  the saved text lacks a "cognitive function test" definition).

## Residual risk and verification gaps

- Judged only against the saved normative section and extraction; the W3C Understanding
  page for 3.3.7 is not part of the pinned source, so no informative-variant claim was
  checked and none is needed for the card's normative content.
- Quote-match was verified by direct read against `normativeText`; the packet's
  `accessibility_packet.py` binding check itself was not run (only explicitly assigned
  check commands may run; main runs the suite after integration).
