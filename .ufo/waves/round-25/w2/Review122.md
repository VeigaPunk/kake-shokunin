# Review122 — criterion card 1.2.2 Captions (Prerecorded) (A) — author-side falsify review

Card under review: `corpus/knowledge/accessibility-review-cards.json`, object with `"id": "1.2.2"` (file lines 26–61).
Source ground truth: `.ufo/waves/round-25/source-wcag22.html`, section `id="captions-prerecorded"` (lines 555–563), normative sentence at line 562; linked definitions `#dfn-captions` (2687), `#dfn-audio` (2604), `#dfn-prerecorded` (3453), `#dfn-synchronized-media` (3861), `#dfn-media-alternative-for-text` (3332). Population binding checked against `.ufo/waves/round-25/population.json` entry for 1.2.2.

## Binding checks (exactness)

| Card field | Card value | Verified against | Result |
|---|---|---|---|
| `id` | `1.2.2` | population.json `id`; `<h4>` "Success Criterion 1.2.2" | match |
| `title` | `Captions (Prerecorded)` | section heading text | match |
| `level` | `A` | `<p class="conformance-level">(Level A)</p>` | match |
| `source` | `https://www.w3.org/TR/2024/REC-WCAG22-20241212/#captions-prerecorded` | population.json `source`, identical | match |
| `sourceQuote` | `Captions are provided for all prerecorded audio content in synchronized media` (11 words) | verbatim substring of `normativeText` ("…in synchronized media , except when…"); ends at word boundary before extractor-added space; taken from criterion body, not heading | match, within 6–25-word rule |
| `status` | `not-assessed` | — | correct; no conformance claim anywhere in the card |

## Findings

### F1 — Moderate — caption requirement blanket-applied to video-only synchronized media

- Field/substring: `publisherCheck` — `Inventory every prerecorded synchronized media item the publisher presents` followed by `For each item that is not a clearly labeled media alternative for text, play it end to end and confirm captions are available`.
- Source anchor: `#captions-prerecorded`, normative sentence: captions are required for `all prerecorded audio content in synchronized media`. The SC's obligation is on **audio content**, not on synchronized media as such. Video-only synchronized media (e.g., a silent animation with time-based interaction) contains no prerecorded audio, so 1.2.2 imposes nothing on it (silent media routes to 1.2.1/1.2.3 scope instead). The card's check has no audio-presence filter, so a reviewer following it must "confirm captions are available" for a silent video — an invented requirement that can only yield a false failure record or vacuous work. Note the sibling 1.2.3 card avoids this by scoping its inventory to "video with an audio track".
- Minimal correction: in `publisherCheck`, record audio presence during inventory and scope the check: `For each item that contains prerecorded audio and is not a clearly labeled media alternative for text, play it end to end and confirm captions are available…`; in `evidenceNeeded`, require caption-playback notes only for audio-bearing items.

### F2 — Minor — "visible label" narrows the "clearly labeled as such" exception

- Field/substring: `evidenceNeeded` — `the visible label that identifies it`.
- Source anchor: `#captions-prerecorded` exception clause `except when the media is a media alternative for text and is clearly labeled as such`, mirrored in `#dfn-synchronized-media`. The normative wording demands a **clear** label; it does not demand a visible one. A clear label perceivable through the player's accessible name rather than as rendered page text could still satisfy the SC, but this card's evidence rule would reject it — an added requirement on the exception path.
- Minimal correction: replace with `the clear label that identifies it (perceivable to users, e.g., nearby page text or the media's accessible name)`.

### F3 — Minor — media-alternative test drops "via text alternatives"

- Field/substring: `publisherCheck` — `confirm it presents no more information than text already on the page`.
- Source anchor: `#dfn-media-alternative-for-text`: `media that presents no more information than is already presented in text (directly or via text alternatives)`. The card limits the comparison to text "already on the page" and omits the text-alternative route, risking rejection of a valid exception where the duplicated text is an image's text alternative rather than visible prose.
- Minimal correction: `confirm it presents no more information than is already presented in text on the page, directly or via text alternatives`.

## Why the rest of the card is faithful (criterion-specific, not generic)

- Exception not lost despite quote truncation: the `sourceQuote` stops before `except when the media is a media alternative for text and is clearly labeled as such`, but both conjuncts of the exception (no-more-information + labeling) are operationalized in `publisherCheck` sentence 3 and `evidenceNeeded`. F2/F3 only tighten how the exception is evidenced, not whether it is honored.
- Caption content tracks the definition, not an example list promoted to MUST: `convey the spoken dialogue, identify speakers where needed, and include the non-speech audio information (such as sound effects or music) needed to understand the content` mirrors `#dfn-captions` "for both speech and non-speech audio information needed to understand the media content"; "where needed" preserves the "needed to understand" qualifier rather than absolutizing Note 1's examples (sound effects, music, laughter, speaker identification and location — "such as" keeps them as examples).
- No informative note becomes a MUST: Note 4 (`Captions should not obscure or obstruct relevant information in the video`) and Note 6 (audio descriptions `do not need to be` captioned) are absent from the card's requirements; the card invents no obscuring or audio-description-captioning obligation.
- Prerecorded/live boundary correct: `limitation`'s `Live media is outside this criterion and is covered separately by 1.2.4 Captions (Live)` is consistent with `#dfn-prerecorded` ("information that is not live") and reciprocated by the 1.2.4 card ("Prerecorded media belongs to 1.2.2").
- Failure example is a true 1.2.2 failure, not restatement: the auto-generated track `omits a narrator's spoken warning` (fails the speech half of `#dfn-captions`) and `never indicates the alert tone that signals an error state` (fails the non-speech-information-needed-to-understand half), on a prerecorded tutorial — squarely in scope and matching the standard failure pattern of captions that do not capture all spoken dialogue.
- No source-only evidence offered as conformance: `limitation` states caption-track existence in source/tools `cannot establish that captions are accurate, complete, synchronized, or include needed non-speech information, nor that an exempt item really adds no information beyond its text and is clearly labeled`; status stays `not-assessed`.

## Residual risk and verification gaps

- Bindings were verified against the committed `population.json` and retained source bytes only; the live W3C URL was not reopened (out of scope this round; a source change is could-not-evaluate per the packet doc).
- F1's severity assumes the inventory can actually contain video-only items — the card's own inventory parenthetical explicitly includes bare `video`, so the defect is in the card text as written; if the publisher's inventory practice pre-filters to audio-bearing media only, F1 downgrades to Minor but the card wording still misstates the SC scope.
- Audio-only synchronized media (e.g., audio with a synchronized interactive transcript) is correctly inside the card's scope per the inventory parenthetical; no finding there, but reviewers should not read "video" in the failure example as implying video is required — 1.2.2 also reaches audio-only synchronized media.
- This is author-side falsification, not independent closure: the card remains `not-assessed`; no website, player, or caption file was exercised, and no live captioning was observed.

## Verdict

AGREE with the card's substance — bindings are exact, the media-alternative exception and the live/prerecorded boundary are handled, no informative note is hardened, and the limitation honestly refuses tool-visible evidence as conformance. Three corrections requested: F1 (Moderate, scope filter in `publisherCheck`/`evidenceNeeded`), F2 (Minor, `visible` → `clear` in `evidenceNeeded`), F3 (Minor, restore `directly or via text alternatives` in `publisherCheck`).
