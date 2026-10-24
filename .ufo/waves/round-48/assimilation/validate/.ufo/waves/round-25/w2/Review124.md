# Review: WCAG 2.2 SC 1.2.4 — Captions (Live)

**Verdict: Disagree as written; one criterion-specific correction is needed.** The identifier, exact title, AA level, pinned source URL, and 11-word `sourceQuote` match the saved source. The quote is within the criterion body. `status` is `not-assessed`. The failure example describes a genuine live-caption omission, and the limitation correctly says source inspection and automated scans cannot establish live caption availability, synchronization, or adequacy, and that one observed session does not establish other sessions. The stated live and synchronized-media scope exclusions also match the linked WCAG definitions.

## Finding (moderate) — audio-description exception is omitted from blanket speech-coverage instructions

- **Card field / substring:** `publisherCheck`: “convey the speech plus non-speech audio information needed to understand the content”; `evidenceNeeded`: “covering speech and needed non-speech audio”.
- **Source:** [saved WCAG 2.2 source](../source-wcag22.html#dfn-captions), captions definition Note 6, lines 2687–2711 (especially 2709–2710): “Audio descriptions can be, but do not need to, be captioned” because they describe information already presented visually. The criterion itself says, “Captions are provided for all live audio content in synchronized media” (criterion anchor `#captions-live`, lines 581–589); its definition and Note 6 clarify the content covered by captions.
- **Reason:** Both card instructions unqualifiedly call for speech coverage. Read literally, they can require captioning spoken audio-description narration even when it describes information already presented visually—the exact case the linked definition says need not be captioned. This is a specific exception, not a reason to weaken coverage for other speech or needed non-speech audio.
- **Minimal correction:** Qualify those instructions to say captions cover speech and needed non-speech audio information, **except that audio descriptions of information already presented visually need not themselves be captioned**. Avoid treating an uncaptioned audio-description track alone as a failure.

## Source checks

- The criterion body at `#captions-live` (lines 581–589) is the cited AA criterion; `sourceQuote` matches its body text.
- `#dfn-captions` (lines 2687–2711) defines captions as synchronized alternatives for speech and non-speech audio information needed to understand the media, gives examples such as sound effects and speaker identification, distinguishes open/closed captions, and contains the audio-description note above.
- `#dfn-live` (lines 3288–3300) defines live as information from a real-world event transmitted with no more than a broadcast delay and says wholly computer-generated information is not live. `#dfn-synchronized-media` (lines 3861–3866) excludes a clearly labeled media alternative for text. The card states these scope boundaries accurately.
- The card does not present source-only evidence as conformance: it asks for human review of actual live sessions and explicitly says the card is review readiness only, not a conformance claim.

No website, browser, external target, or r24 material was examined. No checks were run.