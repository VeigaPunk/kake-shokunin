# Row S018 — freshness recheck (round 26, C1)

```json
{"id":"S018","verdict":"HOLD","fetchIndex":1,"quote":"Mozilla released version 114 of Firefox on the 14th of October 2025. It added support for the interactionId property that's needed to measure INP","anchorObserved":"Body under the h2 \"INP support in Firefox 114\" (anchor #inp-support-in-firefox-114), immediately after the heading; byline \"December 15, 2025 · Updated on March 19, 2026\" near the top; text view is one extracted line, quote at char offset 1545","reason":"DebugBear still attributes interactionId/INP to Firefox 114 and still carries \"Updated on March 19, 2026\", so the row's anchor (#inp-support-in-firefox-114 heading; updated 2026-03-19) is unchanged; the tier-C number still conflicts with Firefox 144.0 release notes carrying interactionId, and no tier-A confirmation of the number has appeared (no link to Firefox release notes in the page), so the rejection and its flip condition hold exactly as recorded.","correction":null}
```

## Caveats (8)

1. Provenance: manifest row=S018 index=1, status 200, 55919 bytes, sha256 21a3e87351b4a621bafeb7a0caeabb5845dc9bbb89613156383798d7bf2a9045, fetchedAt 2026-10-21T15:10:41Z; gz retained, text view fetched/text/S018-1.txt (single line, 6199 chars); manifest-retry.json lists only S008, so no S018 retry.
2. Unpinned living blog URL: drift is tested on content, not availability. The page's own "Updated on March 19, 2026" predates the row's 2026-10-19 opening, so no post-open revision is claimed; a server-side edit that leaves that stamp cannot be excluded from one fetch.
3. Quote is 24 contiguous words at char offset 1545, bounded by a space before and a period after; the same sentence is already quoted at corpus/lessons/round-20.md:220, so its presence is stable, not new.
4. Internal inconsistency is unchanged and sharpened: the page dates "version 114" to "14th of October 2025", the Firefox 144.0 release date recorded at corpus/lessons/round-20.md:220 (released 2025-10-14); the 114 is a digit transposition inside the page, not a tier-A confirmation.
5. Flip condition unmet: raw HTML has no mozilla/firefox release-notes link (the sole MDN link is the Navigation API page), and the page remains tier C/community, so the rejected row stays HOLD.
6. No SOURCES change: status `rejected` and recheck 180d stand; no `[r26-recheck S018 STALE]` block is warranted. Row read at corpus/SOURCES.md:26 (read-only).
7. No tools installed or updated; no browsers, accounts, property probes, or host changes — only retained round-26 bytes plus corpus reads.
8. Remaining unknown: whether DebugBear corrects 114 to 144; not decidable from retained bytes and does not affect this round's verdict.
