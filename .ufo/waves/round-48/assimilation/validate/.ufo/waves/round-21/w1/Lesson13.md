# Lesson13 — round-7 lesson Gate (round-21 retrospective reconstruction)

## Behavior

Appended a `## Gate` section to `corpus/lessons/round-7.md`. The file had no `## Gate` heading, so it was not left unchanged. The section is labelled as a retrospective round-21 reconstruction, not the original round-7 admission.

## File change

- File: `corpus/lessons/round-7.md`
- Old line count: 65 (`wc -l` before edit; file ended at the round-20 correction tail on line 65).
- New line count: 88.
- Old hashline tag: `#F2B1`. New tag after edit: `#8D0B`.
- Change: pure EOF addition at `PUT >65`. Line 66 is a blank separator; line 67 is `## Gate`. Lines 1-65 are unchanged. Round-20 correction tails at lines 57-65 are unchanged.
- Gate block contents: candidates with outcomes, rejected, outside spot-check, contract note.

## Evidence basis for appended content

Read at round-21 time, no live-state re-verification:

- Original sections of `round-7.md`: `The gap closed` (8-12), `What the audit actually found` (14-34), `Learned` (36-53), `Round-20 corrections` (55-65).
- `LOG.md` round-7 entry (line 10).
- `corpus/lessons/round-20.md:261` (row A2 names `round-7.md:21-25`).
- Format precedents: `corpus/lessons/round-20.md:41-60` (first Gate), `:182-196` (resume Gate).
- `corpus/lessons/round-20-verifier-spotcheck.md` (17 lines; round-20 samples only).
- `corpus/lessons/round-6-aggregator-audit.md:84-92` and `:132` (future-dated `~20:20Z` label on `round-7.md:4`, status open at round 6).
- `.ufo/round-20/resume/citation-disposition.json` and `post-review-anchors.json` (round-20 anchors into `round-7.md:40-45`). Read only by grep, not opened in full.

## Out-of-scope or not recorded

- Rejected candidates: not recorded. The original sections contain no rejection records. Not invented.
- Outside spot-check: not recorded for round-7. `round-20-verifier-spotcheck.md` covers round-20 decisions only. `round-20.md:58-60` marks the round-20 outside spot-check as unavailable. The round-6 aggregator item is a timestamp-label check, not a decision spot-check.
- S019: named in the round-21 wave spec as the metadata/gate contract, but no S019 entry exists in `corpus/SOURCES.md`, `corpus/`, `LOG.md` or `SCORECARD.md` at read time. Cited by name only. No S019 row was opened or invented.
- `corpus/lessons/round-21.md`: does not exist at read time. Cited as a pending path only.
- `round-7.md` header labels (`~20:20Z` at line 4, `18:51Z` at line 5) remain unchanged. Round-6 flagged the `~20:20Z` label as future-dated; this gate records that and does not correct it, because lessons are append-only.

## Tools

No installs or updates. No commands run beyond read/grep/wc/ls/git-status/git-log for orientation.

## Checks main agent should run once

- `wc -l corpus/lessons/round-7.md` expect `88`.
- `head -65 corpus/lessons/round-7.md | cmp - <pre-edit copy>` if a pre-edit copy exists; otherwise `git diff -- corpus/lessons/round-7.md` should show only `+` lines after line 65.
- `grep -c '^## Gate' corpus/lessons/round-7.md` expect `1`.
- `ls corpus/lessons/round-*.md | grep -v aggregator | xargs grep -l '^## Gate' | wc -l` (SCORECARD count; this file now contributes one).

## Limitations

- Reconstruction is from existing text only. No outcome was verified against live state, deployed artifacts, or `/tmp/orphan-check.mjs`, which is outside the repository.
- No commits. No edits to SCORECARD, LOG, QUALITY, SOURCES, README or SKILL.

## Follow-up: stale round-20 citation corrected

- Critic (TrendDiscernment, minor): Gate cited `round-20.md:58-60` as current "outside spot-check unavailable".
- Verified: `round-20.md` header (line 3) dates that Gate state to the 2026-10-15 attempt. `round-20-verifier-spotcheck.md` was committed as 7e17c66 on 2026-10-19 20:09:35 -0300 with a non-author admit/reject sample.
- Edit: `corpus/lessons/round-7.md` Gate line 86 now states the 2026-10-15 state and names `round-20-verifier-spotcheck.md` (7e17c66) as superseding it. Only the Gate line changed.
- Tag after this edit: `round-7.md#DBA3`. Line count unchanged at 88.
