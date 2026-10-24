# Review338 — Card 3.3.8 Accessible Authentication (Minimum) (AA)

Scope: card `"id": "3.3.8"` in `corpus/knowledge/accessibility-review-cards.json` (cards lines 626–637), checked field-by-field against the pinned source `.ufo/waves/round-25/source-wcag22.html` (§3.3.8 at anchor `accessible-authentication-minimum`, source lines 2059–2081; glossary at `#dfn-cognitive-function-test`, source lines 2753–2764) and `.ufo/waves/round-25/population.json` (entry at population.json:477–482). Author-side falsify review; recommendation only, not closure. Read-only; no other file touched.

## Binding checks (all pass)

- id/title/level/source: card `3.3.8` / `Accessible Authentication (Minimum)` / `AA` / `https://www.w3.org/TR/2024/REC-WCAG22-20241212/#accessible-authentication-minimum` — identical to population.json:477–481 and to the source heading "(Level AA)" (source line 2063). No duplicate 3.3.8 card exists (single match in cards file).
- sourceQuote: `"A cognitive function test (such as remembering a password or solving a puzzle) is not required for any step in an authentication process"` — verbatim substring of population 3.3.8 `normativeText`; 23 words (≤25); case-exact, word-bounded. Quoting a sentence fragment is acceptable here because the omitted `unless that step provides at least one of the following:` exception is fully restated in publisherCheck's four-provision list, so the card does not rely on the truncation to weaken the requirement.
- status: `"not-assessed"`; no field claims pass, fail, applicability, or website conformance. Limitation explicitly denies it.

## Findings by severity

### Moderate — limitation misstates the pinned source's glossary coverage

- Exact location: card 3.3.8, field `limitation`, exact substring (cards line 635, unique in file):
  `The saved normative text does not define 'cognitive function test'; reviewers should consult the WCAG 2.2 glossary rather than infer one.`
- Why it is a defect: the saved source retains the complete REC, and its Terms section defines the term at anchor `#dfn-cognitive-function-test` (source-wcag22.html:2753–2764): "A task that requires the user to remember, manipulate, or transcribe information." with examples (memorization, transcription, spelling, calculations, puzzles). The definition also contains a load-bearing carve-out for this exact criterion: "The common identifiers name, e-mail, and phone number are not considered cognitive function tests as they are personal to the user and consistent across websites." Under the natural reading ("the saved normative text" = `source-wcag22.html`) the sentence is false; under the narrower reading (the population `normativeText` field) it is technically true but still misdirects, because it tells reviewers to consult "the WCAG 2.2 glossary" without saying that glossary is in the pinned bytes — pushing the manual reviewer off the retained package, contrary to the packet's grounding rules (packet doc: "reopen the pinned official URL in raw mode", source retention rationale). The omission is criterion-specific, not generic: whether typing a username/e-mail counts as a cognitive function test changes which sign-in steps the publisherCheck inventory flags.
- Minimal correction (replacement substring, same field):
  `The criterion's term 'cognitive function test' is defined in the saved source's Terms section (#dfn-cognitive-function-test): a task requiring the user to remember, manipulate, or transcribe information; that definition also excludes the common identifiers name, e-mail, and phone number.`

### No other findings

- publisherCheck — agreed, faithful. The four provisions are mapped one-to-one to the source dl entries (source lines 2067–2075: Alternative, Mechanism, Object Recognition, Personal Content) without paraphrase drift; "any step" step-level framing matches the criterion; "candidate finding for a human reviewer" correctly withholds a WCAG verdict. Listing sign-in, step-up verification, and account recovery as processes to enumerate is a scoping aid consistent with the linked definition of "process" ("series of user actions where each action is required in order to complete an activity", source line 2066 title attribute), not an added requirement.
- evidenceNeeded — agreed. Note 1 ("may be represented by images, video, or audio", source line 2077) and Note 2 (password-manager support and copy/paste as example mechanisms, source lines 2078–2083) are labeled informative and presented as examples, not converted into MUSTs; the Alternative evidence requirement ("the alternative method itself does not rely on a cognitive function test") mirrors the provision text "Another authentication method that does not rely on a cognitive function test".
- failureExample — agreed, realistic and correctly bounded: paste blocked AND autofill disabled AND no alternative sign-in method at that step. It does not overstate that paste-blocking alone is a failure, which would be a common misreading of Note 2.

## Residual risk and verification gaps

- Severity of the glossary finding depends on the intended referent of "saved normative text" (retained source file vs population `normativeText` field); either way the same correction removes the ambiguity, so it is filed as Moderate, not Minor.
- I reviewed card text against the pinned source only; I did not run `scripts/accessibility_packet.py` or the selftests (not assigned to this lane), so structural validators' view of this card is unverified.
- Whether account recovery is in scope is grounded here only in the "process" definition's wording, not in the Understanding document (not part of the pinned population); if the author wants that scoping aid sourced, cite Understanding, not the criterion.
