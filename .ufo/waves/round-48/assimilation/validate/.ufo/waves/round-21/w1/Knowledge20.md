# Knowledge20 — speedrun-pipeline.md provenance trio (round 21, w1)

## Scope
- Target: `corpus/knowledge/speedrun-pipeline.md` only. No other file edited; no commits; no rechecks run; no credential/auth files read.
- Entry was read in full before editing. The entry did not open with a provenance trio, so it was prepended with the trio and one blank line. No old byte changed.

## Change
- Prefix added: 4 lines (`source:`, `verified-at:`, `recheck:`, blank), **1116 bytes** total including newlines.
- Verified by byte measurement: pre-edit size 4576 bytes; post-edit size 5692 bytes; `tail -c 4576` of the new file is byte-identical (`cmp`) to the pre-edit snapshot. The old body, corrections (r20-correction at former line 66) and absence flags (r18 re-census notes) are untouched.
- Two-step edit: the first prefix was applied, then `verified-at` was rewritten (line 2 only, still prefix) to append `metadata contract S019`. The 1116 figure is the final state.

## Field basis
- `source:` — derived from the entry's own in-body citations: the operator-local webzites runbook, `speedrun.mjs`, keeper card, `speedrun-r1.md`, and the ds4cc-marketplace speedrun tree; plus S001, S002, S004 from `corpus/SOURCES.md` for the round-20 upload-artifact correction (these rows exist in the registry, verified by reading SOURCES.md). Absence is stated only as the entry itself flags it: r18 re-census 2026-10-14 flags SPEEDRUN-PROTOCOL.md, speedrun.mjs and ds4cc-marketplace/speedrun as absent. The keeper card and `speedrun-r1.md` have no in-entry absence flag, so the trio says their presence was not observed this round.
- `verified-at:` — original evidence is commit `18537e9` (2026-09-28, round-5; `git log --diff-filter=A` confirms this is the creation commit; `corpus/lessons/round-5-aggregator-audit.md` records the LOG round-5 entry). The r20 correction base is `cb807bc` (2026-10-17). Marked historical-not-live-reverified; not a domain recheck.
- `recheck:` — a safe local `test -e` loop over the three vanished paths (no network, no credential paths); the note states that absent paths since the 2026-10-12 prune require operator restore-or-retire. The command was NOT run.

## S019 reference
- The assignment asked for an S019 reference for the metadata contract. S019 is not yet in `corpus/SOURCES.md` (registry holds S001–S018 at base `5009eca`); L1 registers it. The reference was placed in `verified-at:` as "metadata contract S019" only. S019 is not cited as platform evidence anywhere in the trio; the source line retains entry-specific evidence.

## Findings / limits
- Not live-reverified: this lane did not check whether the webzites or ds4cc-marketplace paths exist today. Their absence is the entry's own r18 flag, not something this lane observed.
- Not verified in the chat-side sense: nothing built, linted or tested (none assigned). Main agent should check once after integration: `head -n 4` of the file shows the trio and blank; field coverage is L1's job.
- Corpus rows for S001/S002/S004 were read, not re-fetched.

## Tooling
- No installs or updates performed this seat.

## Files changed
- `corpus/knowledge/speedrun-pipeline.md` — prefix added (1116 bytes, 4 lines).
- `.ufo/waves/round-21/w1/Knowledge20.md` — this report.
