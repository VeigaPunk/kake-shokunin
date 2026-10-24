# Round 21 w1 — Lesson10 report (`corpus/lessons/round-4.md`)

## Change

- File changed: `corpus/lessons/round-4.md` only.
- Old line count: **42** (`git show HEAD:corpus/lessons/round-4.md` = 42 lines; no `## Gate` heading existed).
- New line count: **66**. Appended: one blank line (43) plus `## Gate — round-21 retrospective reconstruction` (44) and body through line 66.
- Preservation check: `head -42` of the working file is byte-identical to the HEAD blob (`cmp` passed). Pure EOF addition; no prefix metadata added.
- Gate heading count: 1.

## Gate content (summary)

- Labeled as a retrospective round-21 reconstruction, not the original 2026-09-28 admission.
- Original sections cited: `## The gap closed` (line 9), `## Evidence mined` (line 19), `## Learned` (line 32).
- Candidates C-a through C-g, outcomes:
  - Admitted with qualification: C-a (code table), C-b (rebuild success pattern), C-c (code 6/7 anomalies), C-f (success looks like failure on live URL, single-instance basis).
  - Unverified: C-d (code 5 and pre-fired 4 clean-abort semantics), C-e (post-fire 6/7 blind-refire doctrine), C-g (`state/*.json` as richest unmined evidence).
- Rejected candidates: not recorded (none documented).
- Outside spot-check: existing independent evidence `corpus/lessons/round-4-aggregator-audit.md` (non-author aggregator L1 + L2 reviewer, 2026-09-28). It records no admit/reject pair for this lesson, so the admit/reject spot-check is recorded as not recorded.
- Contract references: S019 is named as metadata/gate authority only, with an explicit note that it was not found in the registry.

## Evidence basis

- Original lesson text: `corpus/lessons/round-4.md` lines 1-42 (read in full).
- Independent audit: `corpus/lessons/round-4-aggregator-audit.md` lines 10-11 (method), 30-35 (reproduced code table and registry census), 41-42 (observed-outcome table: `efc1830`, plazir15 code 6, ds4cc code 7), 49-53 (lucario minor defect), 54-55 (commit cited as `round-4` with no hash), 56-58 (three malformed ds4cc journals), 13-16 (overall NOT CONFORMANT at `6b1cd07`; fixed in round-5 `18537e9`).
- Round-20 annotations already present in the target: line 5 and line 6 (`~/Projects/webzites/scripts/kimi-surface.mjs` absent after W7 prune; historical record). Preserved; not re-verified.
- Round-20 convention reference: `corpus/lessons/round-20.md` `## Gate — round-20 resume` (lines 182-196) used as the shape model. Its format was followed; no content was copied.
- Round-21 wave spec: `.ufo/waves/round-21/wave1-spec.json` Lesson10 entry (target, contract text).

## Not done / limits

- No live-state re-verification (per assignment). `~/Projects/webzites` is absent (r18/r20 annotations); no check run.
- No `git rev-parse round-4` re-run; the hash gap is recorded from the audit only.
- Round-21 lesson file (`corpus/lessons/round-21.md`) does not exist at read time; the Gate points to this report instead.
- S019 is not present in `corpus/SOURCES.md` (ends at S018) and `corpus/CORPUS.md` does not exist at read time. The Gate says so and claims no S019 content.
- No independent non-author admit/reject spot-check exists for this lesson; recorded as not recorded, not filled.
- No build, lint, or tests run (assignment rule). No commits. No tools installed or updated.

## Flag for L1 / main

- The round-21 contract's C1 "provenance trio in first 8 lines" was not applied to this file. Inserting prefix lines would shift `corpus/lessons/round-4.md:5-6`, which `corpus/lessons/round-20.md` (around lines 360-453) and `.ufo/round-20/*` pins cite. The Lesson10 assignment only asked for an EOF Gate, so I did not add a prefix. L1 should decide whether the trio is owed for this file and how to keep those pins valid.
- Recheck command for `round-4-aggregator-audit.md:32` and `round-4.md:5-6` is not included; the sources are absent and the assignment forbids re-verification.
