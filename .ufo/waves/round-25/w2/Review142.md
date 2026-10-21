# Review142 — card 1.4.2 Audio Control (A) falsify pass (author-side)

Round 25 C1 accessibility packet, author-side falsify wave. Review target: the single
card `"id": "1.4.2"` in `corpus/knowledge/accessibility-review-cards.json` (lines 147–160,
no duplicate id in the file), checked against the pinned source
`.ufo/waves/round-25/source-wcag22.html` section `#audio-control` (lines 764–780) and its
linked definitions `#dfn-mechanism` (line 3318, incl. Notes 1–2), `#dfn-pause` (line 3424),
`#dfn-audio` (line 2604), and `#cc5` (§5.2.5, line 2214), plus the extracted
`population.json` entry (lines 115–122). Status stays `not-assessed`; nothing here is a
website result. No r24 work, no live targets.

## Verdict

Agree with the card overall — it is grounded and unusually careful on runtime-only
evidence and non-interference — but it carries one Moderate over-tightening and two
Minor gaps. Not clean.

## Findings

### Moderate

**M1 — Card adds a "on the page" location requirement to the mechanism that the
criterion and its definition do not have.**
- Field/substring: `publisherCheck` — `"a mechanism on the page pauses or stops it, or a mechanism on the page controls"`. Same defect shape in `evidenceNeeded` — `"where it is on the page"`.
- Source anchor: `#dfn-mechanism` Note 1 (saved source line 3324): "The mechanism may be explicitly provided in the content, or may be relied upon to be provided by either the platform or by user agents,". The SC itself (`#audio-control`, line 770) says only "a mechanism is available"; it never locates the mechanism in the page.
- Why it matters: the card's phrasing instructs the reviewer to demand an in-page control. Under the pinned text, a mechanism relied upon to be provided by the platform, a user agent, or assistive technology is also admissible (the definition's Note 1). A page whose only qualifying mechanism is platform/UA-provided would be recorded as failing this card's check though the criterion does not require an in-page control; conversely, "on the page" alone never checks that the mechanism is actually available to the user, which is the criterion's operative word.
- Minimal correction: in `publisherCheck` replace "a mechanism on the page pauses or stops it, or a mechanism on the page controls its volume independently" with "a mechanism available to the user pauses or stops it, or a mechanism available to the user controls its volume independently", recording for each mechanism whether it is provided in the content or relied upon from the platform or a user agent (mechanism definition Note 1). In `evidenceNeeded` replace "where it is on the page" with "where it is provided (in the content, or relied upon from the platform or user agent)". Keep the runtime observation requirement as is.

### Minor

**m1 — "starts without a user action" is narrower than the normative trigger "plays automatically".**
- Field/substring: `publisherCheck` — `"list every source of audio that starts without a user action"`.
- Source anchor: `#audio-control` line 770: "If any audio on a web page plays automatically for more than 3 seconds". "Automatically" is not a glossary term here; the criterion conditions on automatic playback, not on the literal absence of any user action.
- Why it matters: audio triggered indirectly by a user action that is not a request for audio (e.g., scrolling or an in-page keystroke starts a soundtrack) plays automatically, yet under the card's phrasing it would be inventoried as user-action-started and could be dropped from scope.
- Minimal correction: replace "that starts without a user action" with "that plays automatically (starts without the user requesting audio playback)".

**m2 — Evidence does not capture the definition of "pause": stopped and not resumed until the user requests it.**
- Field/substring: `evidenceNeeded` — `"confirming that a human operated it and it stopped the audio or changed its volume"`.
- Source anchor: `#dfn-pause` (saved source line 3424; the SC links "pause" to this definition, title "stopped by user request and not resumed until requested by user").
- Why it matters: a record that merely says the audio stopped at the click misses the definition's persistence half. Audio that self-resumes (playlist, scripted replay) after the user pauses defeats the mechanism, and the card's evidence template would not surface it.
- Minimal correction: append to `evidenceNeeded`: "for a pause mechanism, record that the audio stays stopped until the user requests resumption".

## Checked and agreed (criterion-specific, not just counts)

- **Binding exact.** `id` "1.4.2", `title` "Audio Control", `level` "A" match the population entry and the saved section header "Success Criterion 1.4.2 Audio Control" with "(Level A)" (`#audio-control`, line 768); `source` is the pinned REC URL with the correct `#audio-control` anchor.
- **Quote clean.** `sourceQuote` "If any audio on a web page plays automatically for more than 3 seconds, either a mechanism is available to pause or stop the audio" is an exact, case-sensitive, word-boundary substring of `normativeText` (population line 121), 25 words — at the limit but within the 6–25 rule — and is taken from the criterion body, not the heading or doclinks.
- **Disjunction preserved.** "confirm one of two things" mirrors the SC's "either … or …" without strengthening either alternative; both alternatives are stated with the criterion's own independence wording "independently from the overall system volume level", and the evidence requirement's "without changing system volume" tracks it.
- **Non-interference handled correctly and specifically.** "Check every piece of content on the page, including content not relied on to meet other criteria, because the criterion's note applies it to all content under Conformance Requirement 5: Non-Interference" faithfully renders the saved note (`issue-container-generatedID-2`: "all content on the web page (whether or not it is used to meet other success criteria) must meet this success criterion") and its normative target `#cc5`. The note is not turned into a new card-level MUST beyond that.
- **Threshold kept strict.** "more than 3 seconds" is kept everywhere (`publisherCheck`, `evidenceNeeded` "whether it exceeds 3 seconds"); the limitation's "Audio that plays automatically for 3 seconds or less is outside this criterion's requirement" is the correct reading of the open interval — exactly 3 seconds is out, and that statement is a bound statement about this criterion only, not a blanket conformance claim.
- **No source-only evidence passed off as conformance.** The limitation's refusal of source inspection/automated scanning for runtime duration, scripted starts, and mechanism independence is criterion-specific and correct: those facts exist only in the rendered page. `status` is `not-assessed`; `failureExample` (autoplay 30-second video, hidden controls, only system volume) fails both SC alternatives genuinely — system volume is not a volume control "independently from the overall system volume level" — rather than being a generic badness anecdote.

## Residual risk and verification gaps

- The saved REC source contains no glossary entry for "automatically"; my m1 rests on the normative wording itself, not on an Understanding-document interpretation, which is not in the pinned bytes.
- The card's embedded-video/background-music/widget examples are illustrative, not exhaustive; "any audio" (definition `#dfn-audio`: "the technology of sound reproduction") can also arise from synthesized speech, which the card does not name — acceptable for a work aid, noted for completeness.
- I verified only the 1.4.2 card; sibling criteria are out of scope for this review.
