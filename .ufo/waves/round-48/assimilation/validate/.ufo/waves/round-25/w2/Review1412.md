# Review1412 — Card 1.4.12 Text Spacing (AA) — w2 author-side falsify pass

**Verdict: AGREE — no normative defect found.** One advisory-minor wording note (below); nothing that misstates the criterion, inflates it into a MUST, drops an exception, or offers source-only evidence as conformance.

**Basis (all read this session):**
- Saved source: `.ufo/waves/round-25/source-wcag22.html` §1.4.12, anchor `#text-spacing` (section lines 1045–1062; normative sentence line 1051; value list and Exception/Notes lines 1053–1061; `(Level AA)` line 1049).
- Population extract: `.ufo/waves/round-25/population.json` id `1.4.12` (lines 169–175), `normativeText` matches the saved source.
- Card: `corpus/knowledge/accessibility-review-cards.json` lines 218–229 (read raw, untruncated).

## Criterion-specific checks (each tied to the normative text)

1. **Identity exact.** `id` "1.4.12", `title` "Text Spacing", `level` "AA", `source` URL match the pinned REC section heading and conformance-level paragraph (`source-wcag22.html` line 1045/1049); URL matches `population.json` anchor `text-spacing`.
2. **sourceQuote verbatim and bounded.** `"no loss of content or functionality occurs by setting all of the following and by changing no other style property"` — contiguous, character-exact substring of the normative sentence (source line 1051; `population.json` line 175). 20 words ≤ 25.
3. **All four thresholds exact.** publisherCheck's "line height at least 1.5 times the font size … spacing following paragraphs at least 2 times … letter spacing at least 0.12 times … word spacing at least 0.16 times" reproduces the source list verbatim — no rounding, unit substitution, or reordering.
4. **All-at-once preserved.** "apply all four overrides at once" matches "setting all of the following"; not weakened to per-property or incremental application, and "changing no other style property" is carried over as the constraint.
5. **Applicability retained.** "implemented in a markup language supporting these text style properties" mirrors "content implemented using markup languages that support the following text style properties"; `limitation` honestly extends the unknown-outcome boundary to content in non-supporting markup.
6. **Exception kept, not omitted.** publisherCheck's final sentence ("record which properties exist for that combination and check only those, as the stated exception permits") plus evidenceNeeded's written-rationale requirement faithfully track the Exception clause "can conform using only the properties that exist for that combination of language and script".
7. **No informative→MUST inflation.** Note 1's substance ("Content is not required to use these text spacing values … when a user overrides … content or functionality is not lost") is placed where it belongs — in `limitation` as a scoping fact, not as an authoring demand. The card never converts the 1.5/2/0.12/0.16 bookmarklet values into content requirements.
8. **No source-only evidence as conformance.** `limitation` states "source review or automated style scans cannot establish the outcome; it depends on rendered behaviour under the overrides for each page and state", and `status` stays `not-assessed`; no website conformity claim anywhere in the card.
9. **failureExample not a misstatement.** The scenario (fixed pixel height + `overflow: hidden`; second line of the label clipped once line height 1.5× and letter spacing 0.12× apply; button purpose unreadable) is a physically coherent instance of "loss of content" under the required overrides. It is presented as a card-authored example, not attributed to a W3C technique, so there is nothing to misquote from the source.

## Advisory-minor (wording only, not a falsification)

- **Field:** `publisherCheck` — **substring:** `"confirm no text is clipped, truncated, overlapped, or hidden"`.
- **Reason:** the criterion forbids *loss of content or functionality* caused by the overrides, not the bare visual symptoms. An overlap that remains fully legible would trip this checklist without failing the criterion; the symptom list is a proxy.
- **Minimal correction:** append a loss qualifier, e.g. `"…or hidden in a way that loses content or functionality"`. The preceding "Compare against the unmodified rendering" already anchors the baseline, and the symptom list matches standard override-testing practice, so this is cosmetic tightening, not a defect. No change required for agreement.

## Residual risk and verification gaps

- No runtime verification was performed (out of lane: no website tests, browser, or network targets); every finding above is a static semantic comparison against the saved source and population extract.
- The overlap-without-loss false-positive risk in the advisory note is the one residual interpretation gap between card checklist and criterion wording.
- Note 2 (informative writing-systems guidance, paragraph start indent) is intentionally not mirrored in the card: it is non-normative encouragement, and evidenceNeeded already records language/script per template, so its omission omits nothing required.

**Installations performed this task:** none (existing read tooling sufficient).
