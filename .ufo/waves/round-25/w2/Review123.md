# Review123 — WCAG 2.2 SC 1.2.3

**Verdict: Disagree (author-side falsification only; not independent closure).** The card is correctly bound to criterion 1.2.3, Level A, and the pinned source; its source quote matches the normative criterion, and its `status` is `not-assessed`. The limitation also correctly says that no website was evaluated and that packet readiness is not a conformance result. However, following the check as written can both exclude in-scope media and reject a conforming presentation whose existing audio already carries the video information.

## Findings

### Major — review scope is narrower than the criterion

- **Card field / substring:** `publisherCheck`: “every prerecorded synchronized media item (video with an audio track) the publisher controls”; `limitation`: “Live media and audio-only or video-only media are outside this criterion”.
- **Source:** `source-wcag22.html#audio-description-or-media-alternative-prerecorded` (lines 574–575) applies the alternative-for-time-based-media or audio-description provision to “synchronized media,” with the text-media exception. The linked definition at `source-wcag22.html#dfn-synchronized-media` (lines 3864–3865) covers audio **or** video synchronized with another format and/or time-based interactive components. The criterion has no publisher-control/hosting limitation. The only stated exception is a media alternative for text that is clearly labeled as such. The `audio-only`/`video-only` blanket exclusion is also too broad for a presentation that otherwise meets the synchronized-media definition.
- **Why it matters:** A reviewer could omit an embedded or externally hosted item, or a qualifying synchronized presentation that is not a video-with-audio-track, without ever testing whether the criterion's alternative branch applies. Conversely, the limitation can cause a reviewer to rule out synchronized audio-only or video-only cases categorically.
- **Minimal correction:** Scope the inventory to all prerecorded synchronized media in the named review scope, regardless of who hosts/controls it or whether it has both an audio and video track. Exclude only media that does not meet the criterion's synchronized-media scope, plus the expressly stated, clearly labeled media-alternative-for-text exception.

### Major — no allowance for video information already conveyed in existing audio

- **Card field / substring:** `publisherCheck`: “confirms that either an audio description of the prerecorded video content or an alternative for time-based media is provided”; `evidenceNeeded`: “which option is provided (audio-described version or description track, or a time-based media alternative document)”.
- **Source:** `source-wcag22.html#dfn-audio-descriptions`, Note 3 (lines 2619–2632), states that where all video information is already provided in existing audio, no additional audio description is necessary. The definition at the same anchor distinguishes audio description as narration added to the soundtrack for visual details not understood from the main soundtrack alone.
- **Why it matters:** The check and evidence options require an added description or separate alternative for every item. They do not let a reviewer record the valid case in which the existing audio already supplies all the video information, so this can produce a false failure or unnecessary remediation.
- **Minimal correction:** Add a third documented outcome: no additional description is needed when review confirms the existing audio conveys all video information. Capture the reviewer’s evidence for that finding instead of requiring a separate track/version or alternative.

### Moderate — the alternative option is checked for presence, not for its defined content

- **Card field / substring:** `publisherCheck`: “an alternative for time-based media is provided and reachable alongside it”; `limitation`: “the description or alternative conveys the important visual content”.
- **Source:** `source-wcag22.html#dfn-alternative-for-time-based-media` (lines 2499–2507) defines the alternative as a document with correctly sequenced text descriptions of time-based visual **and auditory** information and a means to achieve the outcomes of time-based interaction. Its Note (lines 2504–2506) says a source screenplay qualifies only if corrected to accurately represent the final edited media. The `media alternative for text` definition and note are at `source-wcag22.html#dfn-media-alternative-for-text` (lines 3335–3342).
- **Why it matters:** The publisher check expressly verifies that an alternative exists and is reachable but does not require that it meet those defining conditions. Its limitation mentions only important visual content, which can leave out auditory information, interaction outcomes, and a screenplay that no longer matches the final media. Merely linking a document could therefore be treated as sufficient.
- **Minimal correction:** Require the human comparison to verify and record that the alternative reflects the final media, correctly sequences descriptions of the visual and auditory information, and supports the outcomes of any time-based interaction. State those checks in the limitation as well.

## Clean checks and verification gaps

The title, id, level, and source URL match the pinned population entry (`population.json`, lines 34–40). The card's source quote is an exact 18-word substring of its `normativeText`, and `status` is `not-assessed`. Its failure example describes an actual gap in access to on-screen information and does not claim that source inspection establishes conformance. Its text-media exception is correctly tied to both the text and a clear label.

No staged or unstaged diff was present for `corpus/knowledge/accessibility-review-cards.json` in the inspected checkout; this is therefore a semantic review of the target card against its pinned source, not a review of a visible card change.

Review used the saved WCAG Recommendation HTML and extracted population; no website, browser, or runtime was tested, and no tools were installed. No `lsp` device is mounted (`xd://lsp` returned “No such tool”); this is a documentation/JSON semantic review, not a code-caller review. Text search was used only to locate source sections; the findings above are grounded in the read source sections and definitions.