# CitingSweep01 — blind source-id census: accessibility packet + cards

Scope: exactly `corpus/knowledge/accessibility-review-packet.md` and
`corpus/knowledge/accessibility-review-cards.json`, measured at frozen base
`83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba` and declarations
`be375d90afc6fc7aca369ab3cf5247bf460aeed2` (target bytes identical in both, worktree clean).
Method: manual line/column walk first, then parser comparison. No network, no source or
public-site evaluation, no sibling reports read (blind), no tool installs.

## 1. Manual census (performed before parser comparison)

### 1a. Packet — 4 S-id occurrences, one id, no range/group/list form

| line:col | scope | form | id | in r26 pop32 | exact located support (≤25 words) |
|---|---|---|---|---|---|
| L1:9 | provenance header `source:` | literal | S035 | no | `source: S035 — https://www.w3.org/TR/2024/REC-WCAG22-20241212/ (success criteria 1.1.1–4.1.3; conformance requirements §5.2)` |
| L3:77 | provenance header `recheck:` | literal | S035 | no | `reopen S035 on a WCAG version change` |
| L88:1 | body, “Conformance boundaries” | literal | S035 | no | `S035 §5.2.1 requires all A and AA criteria for Level AA` |
| L155:35 | late recheck note (L153–158, not final paragraph) | literal | S035 | no | `compare its This version URL with S035; the offline gate cannot observe a new` |

Unique ids = {S035}; population intersections = ∅; range regexes = 0; grouped/slash/comma/`and`
lists = 0; abbreviated forms (`S001–06`, `S1–S6`, `1–S006`, `S-035`) = 0. Full backward
search (hyphen, en dash U+2013, em dash U+2014, `..`, `to`, `through`) found no range.
Non-ASCII inventory is only `–`×4, `§`×4, `—`×3, `“ ”`×1 each; no lookalike ids or zero-width
characters. Packet = 181 newlines, 182 split lines, no final newline, no BOM.

### 1b. Cards JSON — 0 S-id occurrences, 55 URL-only source references

Pure JSON array, 662 newlines (663 split lines), 55 card objects, no header/EOF metadata and no comments.
Every `"source"` value is `https://www.w3.org/TR/2024/REC-WCAG22-20241212/#<slug>`;
55 unique URLs and 55 unique card ids. These are alternate (URL-form) source references,
not source-id references: no `S\d{3,}` token in any decoded key/value, no JSON `\u`
escapes, no ranges/lists. Lines below (line:id#fragment), each scope = that card object’s
`source` field:

L6:1.1.1#non-text-content | L18:1.2.1#audio-only-and-video-only-prerecorded | L30:1.2.2#captions-prerecorded | L42:1.2.3#audio-description-or-media-alternative-prerecorded
L54:1.2.4#captions-live | L66:1.2.5#audio-description-prerecorded | L78:1.3.1#info-and-relationships | L90:1.3.2#meaningful-sequence
L102:1.3.3#sensory-characteristics | L114:1.3.4#orientation | L126:1.3.5#identify-input-purpose | L138:1.4.1#use-of-color
L150:1.4.2#audio-control | L162:1.4.3#contrast-minimum | L174:1.4.4#resize-text | L186:1.4.5#images-of-text
L198:1.4.10#reflow | L210:1.4.11#non-text-contrast | L222:1.4.12#text-spacing | L234:1.4.13#content-on-hover-or-focus
L246:2.1.1#keyboard | L258:2.1.2#no-keyboard-trap | L270:2.1.4#character-key-shortcuts | L282:2.2.1#timing-adjustable
L294:2.2.2#pause-stop-hide | L306:2.3.1#three-flashes-or-below-threshold | L318:2.4.1#bypass-blocks | L330:2.4.2#page-titled
L342:2.4.3#focus-order | L354:2.4.4#link-purpose-in-context | L366:2.4.5#multiple-ways | L378:2.4.6#headings-and-labels
L390:2.4.7#focus-visible | L402:2.4.11#focus-not-obscured-minimum | L414:2.5.1#pointer-gestures | L426:2.5.2#pointer-cancellation
L438:2.5.3#label-in-name | L450:2.5.4#motion-actuation | L462:2.5.7#dragging-movements | L474:2.5.8#target-size-minimum
L486:3.1.1#language-of-page | L498:3.1.2#language-of-parts | L510:3.2.1#on-focus | L522:3.2.2#on-input
L534:3.2.3#consistent-navigation | L546:3.2.4#consistent-identification | L558:3.2.6#consistent-help | L570:3.3.1#error-identification
L582:3.3.2#labels-or-instructions | L594:3.3.3#error-suggestion | L606:3.3.4#error-prevention-legal-financial-data | L618:3.3.7#redundant-entry
L630:3.3.8#accessible-authentication-minimum | L642:4.1.2#name-role-value | L654:4.1.3#status-messages

Other references in the packet, none of them source ids: `1.1.1–4.1.3` at L1 is a WCAG
criterion-id range (correctly not an S-range); §§5.2.1–5.2.5 at L88 are singly enumerated
section anchors; unversioned alias `https://www.w3.org/TR/WCAG22/` at L154; artifact paths
at L17, L18, L25, L46–47, L112, L120, L127, L160, L166.

## 2. Pair contribution and comparison with the frozen parser (done after §1)

- Target files contribute **0 of the frozen 57 citing pairs** and **0 of the 16 missing
  pairs**. No pair for either file exists in the r26 ledger (41 pairs), and neither file
  appears in `c1-before.json`'s 16-row missing list.
- `count_c1.py` grammar: `LITERAL=\bS(\d{3,})\b` (L5), `RANGE=\bS(\d{3,})\s*(?:[-–—]|\.\.|to|through)\s*S(\d{3,})\b`
  (L4), population intersection at L28, discovered pairs at L29–30. Importing those compiled
  regexes and applying them gives exactly: packet LITERAL ×4 (L1, L3, L88, L155), RANGE ×0;
  cards LITERAL ×0, RANGE ×0. The whole-blob scan does include provenance headers and the
  late note; S035 is then dropped only by the population filter at L28.
- CLI rerun at base and at declarations: `population 32, citingPairs 57, decided 41,
  r26CarriedPairs 41, newDecided 0, missing 16, findings 0`, exit 1; missing lists identical
  at both revisions and identical to `c1-before.json` (57/41/16). `pairs.json` and
  `discovered-pairs.json` are absent, so no additions/adjudications were in play.
- Independent range-aware enumeration over all 26 knowledge files (23 `.md` + 3 `.json`) at base
  yields 57 pairs exactly equal to `ledger(41) ∪ missing(16)`; the two target files are not in
  that union. The 16 missing attribute as static-canonical-preflight 9, sitemap-orphan-audit 2,
  publish-channels 2, crawl-scope-per-host 1, ghp-custom-domain 1, ghp-etag-anatomy 1 — none
  accessibility. `c2-oracle.json expectedPairs` = those same 16 pairs (exact set equality).
- Grouped context confirmed outside target scope: `static-canonical-preflight.md:54`
  `an assumed checkout served set (S001–S006, ghp-served-set.md)` expands to the six
  S001–S006/static-canonical pairs; all six are in the 16 missing. The frozen grammar handles
  that en-dash range; no such form occurs in my two files.

## 3. Additional inherited32-row obligations: none

No literal, grouped, range, abbreviated, lookalike or URL-only reference in either target file
resolves to any of the 32 population rows S001–S034 minus S014/S019. Therefore this walk adds
no inherited32 pair beyond frozen57 and no metadata-only pair is being suppressed.

## 4. S014 / S019 / S035 outside the inherited population — recorded separately

- Registry has 35 contiguous rows S001–S035. Frozen population32 = S001–S034 minus own-work
  S014, S019; S035 is the excluded spec row (W3C WCAG 2.2, tier A, scope “Publisher-side
  manual-review preparation … not website conformance”, opened 2026-10-21, recheck
  `on-release`, used-by `corpus/knowledge/accessibility-review-packet.md,
  corpus/lessons/round-25.md`).
- S035 appears 4× in the packet (above) and 0× in cards JSON; it appears in no other
  `corpus/knowledge` file. S014 appears 0× in my files (4× in freshness-sweep.md overall);
  S019 appears 0× in my files (17 literals across 16 other knowledge files). Those are
  outside-population observations only, not pairs.
- S035 registry URL is byte-identical to packet L1’s URL; registry saved-source SHA-256
  `6e3c5fe397257cae509a2fb4752b73062cf8cbeb92c2cec618989b17e4cf7057` equals
  `.ufo/waves/round-25/frozen-final/source-wcag22.html` and `scripts/accessibility_packet.py`
  `SOURCE_SHA256` (L20).

## 5. Freshness evidence, hashes, and the one candidate enlargement

- Packet `4277f15961d2066ebaa7df103a1fc9c3990951dd0591f69e5096db6f5e74aaab` and cards
  `65aa760b0943c13b1f154f139e8b6c7c0dac5cbf40e0be5d1db232bafb479f16` equal base,
  declarations, worktree and `.ufo/waves/round-27/frozen/expected.json` pins. Cards also equal
  the round-25 corrected pin `frozen-final/cards.json` and `round-25/measure.py CARDS_SHA256`;
  it differs from historical `round-25/frozen/cards.json` (`504ddb09…`), which the packet
  itself labels non-corrected. Git shows the packet last changed at round-25 `be362b7` and the
  cards JSON at round-25 `6cb08a4`; neither changed at declarations `be375d9`.
- No round-27 S035 receipt exists: `.ufo/waves/round-27/fetched/manifest.json` covers only
  rows S001–S006 (8 entries); `.ufo/waves/round-26/rechecks/` has no `S035.json`. The packet’s
  `verified-at: 2026-10-21` and “W2 ReviewSource reopened both URLs this round” (L156–157)
  are inherited round-25 prose, not round-27 evidence. Content stability is pinned; source
  re-observation this round is **not** established (an r27 freshness verdict would be
  UNVERIFIABLE, not STALE). No network check was made, per assignment.
- Candidate monotone enlargement (named, not applied): `{S035, corpus/knowledge/accessibility-review-packet.md}`
  is a literal S-id citing pair outside frozen57. If L1 adds it via `discovered-pairs.json`,
  the denominator grows 57→58 and it needs adjudication; the frozen `count_c1.py` would then
  pair it, but a `kind:source` row would fail `source_missing` because r27 fetched no S035
  bytes. An artifact-kind row could use the pinned `source-wcag22.html` bytes without
  network (that path exists at base and declarations).
  `{S035, cards.json}` is not a pair under the frozen grammar (URL-only, no id); admitting
  URL-identity citations would be a policy expansion, not this walk’s finding.
- Operability boundary: neither the C1 counter nor the C2 citing-set gate can see these
  files’ only source binding, because (a) S035 is filtered by population and (b) cards JSON has
  no id. Observed: `scripts/corpus-contract.mjs` checks only that the header trio is non-empty;
  a `scripts/` grep found no `used-by` enforcement and no checker validating the S035 token
  against `SOURCES.md`. The 55 card URLs are not checked as citations by any counter; the
  packet tool instead pins the source bytes and grounds card quotes against them.

## 6. Remaining unknowns / limits

- Whether L1 policy admits registered non-population rows (S035) into the discovered set is a
  decision I did not make; I record the pair without altering denominator or ledger.
- Whether cards JSON’s URL-only provenance should be reflected in S035’s used-by is a registry
  convention question (currently used-by lists packet and round-25 lesson only).
- Semantic adequacy/truth of card prose and source quotes was not judged; no source or site
  was opened or fetched. No sibling/peer report was read, preserving blind independence.

Evidence artifacts (scratch, read-only): `/fast/scratch/hyaku/kake-r27/KakeR27.CitingSweep01/{census.txt,c1-base.json,c1-head.json}`.

Report: .ufo/waves/round-27/w1/CitingSweep01.md
