# Review — 1.2.5 Audio Description (Prerecorded) (AA)

**Verdict: Disagree — the card is grounded overall, but its review instructions need correction.** Review is limited to this card and the retained 12 December 2024 WCAG 2.2 source.

## Findings (highest severity first)

### Moderate — The review method hides the visual details it asks the reviewer to identify

- **Field:** `publisherCheck`
- **Exact text:** “watch it with the audio on and the picture covered. Note each important visual detail, such as actions, characters, scene changes, or on-screen text, that the main soundtrack does not convey.”
- **Source:** `.ufo/waves/round-25/source-wcag22.html#dfn-audio-descriptions` (lines 2619–2625): the definition concerns important visual details not understood from the main soundtrack, and Note 1 names actions, characters, scene changes, and on-screen text.
- **Why:** With the picture covered, the reviewer cannot identify visual details that the soundtrack omits. This procedure cannot produce the comparison required by the next sentence.
- **Minimal correction:** First inspect the video with the picture visible and inventory its important visual information; compare that inventory with the main soundtrack, then check whether audio description supplies the missing information. An audio-only pass can help assess what the soundtrack conveys, but cannot replace the visible-video pass.

### Moderate — The inventory scope is narrower than WCAG’s definition of synchronized media

- **Field:** `publisherCheck`
- **Exact text:** “video that is combined with audio or time-based interaction”
- **Source:** `.ufo/waves/round-25/source-wcag22.html#audio-description-prerecorded` (lines 600–601) applies to prerecorded video in synchronized media; `#dfn-synchronized-media` (lines 3864–3865) defines that as audio **or video** synchronized with another format for presenting information and/or with time-based interactive components, subject to the clearly labeled media-alternative-for-text exception.
- **Why:** The card’s inventory instruction mentions audio or time-based interaction, but omits video synchronized with another information format where that format is not audio. That can leave in-scope prerecorded video out of the review.
- **Minimal correction:** Use the definition’s scope: “prerecorded video content synchronized with another format for presenting information and/or with time-based interactive components,” then retain the clearly labeled media-alternative-for-text exclusion.

### Minor — The transcript statement overclaims what satisfies 1.2.3

- **Field:** `limitation`
- **Exact text:** “A transcript alone meets 1.2.3, not 1.2.5.”
- **Source:** `.ufo/waves/round-25/source-wcag22.html#audio-description-or-media-alternative-prerecorded` (lines 574–575) permits an alternative for time-based media or audio description; `#dfn-alternative-for-time-based-media` (lines 2499–2506) requires correctly sequenced text descriptions of time-based visual and auditory information and a means to achieve outcomes of any time-based interaction.
- **Why:** “A transcript” is not necessarily that complete, correctly sequenced alternative. As written, the sentence makes an unqualified claim that any transcript satisfies 1.2.3.
- **Minimal correction:** Say that a conforming alternative for time-based media may satisfy 1.2.3, while a generic transcript alone does not necessarily do so and does not replace the audio description required by 1.2.5.

## Correctly grounded elements

- The `id`, title, AA level, and source URL match the pinned criterion. `sourceQuote` (“Audio description is provided for all prerecorded video content in synchronized media”) is an exact 12-word quotation from the criterion body (source lines 600–601), within the packet’s 6–25-word limit. `status` is `not-assessed`.
- The failure example is criterion-relevant: the price and release date are visual information not conveyed by the stated soundtrack, and the example says no described track or version exists.
- The statements that existing dialogue pauses suffice for standard audio description and that extended description is not required by 1.2.5 are consistent with the audio-description definition’s Notes 2–3 (`#dfn-audio-descriptions`, lines 2627–2632) and the separate AAA criterion 1.2.7 (`#extended-audio-description-prerecorded`, lines 624–627).
- The limitation correctly rejects captions files, transcripts, player toggles, and source attributes as proof that narration covers the missing visual information; it also correctly keeps the card not-assessed and does not claim website conformance. The live/prerecorded distinction is consistent with `#dfn-prerecorded` and `#dfn-live` (lines 3453–3457 and 3288–3300).

## Residual risk and verification gaps

- Review is based on the saved card and pinned WCAG source. No website or media was tested, as required by scope.
- No LSP device/server is mounted in this session (`read xd://lsp` returned “No such tool”); therefore no LSP status, references, definition, or diagnostics checks were available. The findings above are based on direct reads of the saved card and source, not grep as semantic proof.
