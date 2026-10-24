# Review 1.2.1 — Audio-only and Video-only (Prerecorded)

**Decision: Disagree — two criterion-specific checklist gaps.** The card is correctly identified as 1.2.1, title “Audio-only and Video-only (Prerecorded),” Level A, and uses the pinned source URL. Its `sourceQuote` is an exact 15-word excerpt of the criterion body in `population.json` `normativeText`. `status` is `not-assessed`. The failure example describes a valid video-only failure scenario, and the limitation correctly avoids a website-conformance claim and excludes live/synchronized media.

## Findings

### Medium — Alternative review does not explicitly check correct sequencing

- **Card field / substring:** `publisherCheck`: “Have a reviewer compare the full media against its alternative for missing information.” `evidenceNeeded`: “a human reviewer's note comparing it to the complete media for equivalent information”.
- **Source:** `.ufo/waves/round-25/source-wcag22.html#audio-only-and-video-only-prerecorded` (criterion body, lines 525–548) requires an “alternative for time-based media.” The linked definition at `#dfn-alternative-for-time-based-media` (lines 2496–2502) requires “correctly sequenced text descriptions”; its note at lines 2504–2506 says a screenplay only meets the definition if corrected to accurately represent the final media. The linked audio-only and video-only definitions (lines 2639–2643 and 4022–4026) rule out interaction for this criterion, but do not remove the correct-sequencing requirement.
- **Why it matters:** The checklist asks reviewers to compare for missing information/equivalence, but does not ask them to verify the alternative’s text descriptions are correctly sequenced. A text alternative containing all the information in a misleading order could satisfy the stated evidence prompt while failing the linked definition.
- **Minimal correction:** Add an explicit check and evidence note that any alternative for time-based media presents its text descriptions in the correct sequence for the media, as well as covering equivalent information.

### Medium — Exception evidence does not establish the “no more information” condition

- **Card field / substring:** `publisherCheck`: “citing the text it duplicates and the label.” `evidenceNeeded`: “the text the media duplicates and the visible label identifying the media as an alternative for that text.”
- **Source:** The exception in `#audio-only-and-video-only-prerecorded` (lines 525–527) applies only to a media alternative for text that is clearly labeled. The linked definition at `#dfn-media-alternative-for-text` (lines 3332–3337) defines it as media that “presents no more information than is already presented in text (directly or via text alternatives)”; the associated note is at lines 3339–3342.
- **Why it matters:** Citing related text and observing a label does not, by itself, establish that the media adds no information beyond that text. The evidence prompt could therefore support an exception claim for media that contains additional information.
- **Minimal correction:** For each claimed exception, require a comparison of the complete media with the cited text (including text alternatives) and record that the media presents no more information, in addition to recording the clear label.

## Residual risk and verification gaps

No website or media was evaluated. This is a read-only semantic review of the card against the pinned saved source and extracted population; no checks or conformance determination were run.