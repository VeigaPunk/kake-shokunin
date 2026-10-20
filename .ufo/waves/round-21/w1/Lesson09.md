# Lesson09 report: corpus/lessons/round-3.md Gate

## Behavior
- Target: `corpus/lessons/round-3.md`. Before the edit it had no `## Gate` heading (exact-match check: none) and was 29 lines, 1433 bytes.
- Action: appended a blank line, then `## Gate` and a retrospective round-21 reconstruction section at EOF. Edit tag went `792C` -> `CE5E`. Resulting file is 51 lines.
- Prior bytes (lines 1-29) are untouched. The change is a pure EOF addition.
- No live-state re-verification: no probe, fetch, or domain read was run.

## Gate contents (as appended)
- Label: retrospective round-21 reconstruction, not original admission.
- Candidates: lucario row; charter-ghp beat marker; `status:live` is an assertion; content-stable literal pins; corpus self-audit.
- Outcomes:
  - Admitted with qualification: lucario and charter-ghp findings as 2026-09-28 snapshot facts; trust-hierarchy method; content-stable pin method.
  - Unverified: `fleet.config.json` row fix (no landing record); runbook re-pin budget clause; self-audit outcome.
- Rejected: not recorded. The original lesson and `LOG.md:5` list no rejects.
- Outside spot-check: not recorded. No non-author verifier entry for round-3 found in `LOG.md`, `corpus/lessons/`, or `.ufo/`.
- Corpus contract: S019 cited with its own scope limit (metadata and gates, no platform authority).

## Evidence basis
- Original lesson: `corpus/lessons/round-3.md` §The gap closed (lines 6-16), §Learned (lines 18-29). Introduced by commit `ddf40e2` (subject `round-3`, 2026-09-28).
- `LOG.md:3-5`: round-1 and round-3 entries.
- `corpus/knowledge/drift-detection.md:4` (r18 re-census comment: webzites tree absent after 2026-10-12 prune), `:46-56` (fresh-probe table).
- `corpus/lessons/round-7.md:29-34`: second consecutive charter-ghp failure; round-3 re-pin never landed in `fleet.config.json`.
- `corpus/knowledge/publish-queue.md:36`: PQ-12.
- `SKILL.md:67`: "Trust hierarchy: live probe > config fields".
- `corpus/SOURCES.md:27`: S019 row (tier A; scope limited to provenance metadata and lesson gates).
- Round-21 provenance: `.ufo/waves/round-21/wave1-spec.json` (context C2). `corpus/lessons/round-21.md` does not exist yet.

## Out of scope / not touched
- No other files edited. No commits. No SCORECARD, LOG, QUALITY, SOURCES, README, or SKILL changes.
- Round-20 and other lessons untouched.
- No subagent dispatch (leaf seat).

## Findings and limits
- The round-21 lesson file is absent, so the round-21 citation uses the wave contract instead.
- The original sources (`~/Projects/webzites`) were absent at the r18 re-census. This Gate cannot re-read them, and it does not claim present-day status.
- Verification was not run here, per the assignment. The main agent should check: `grep -c '' corpus/lessons/round-3.md` returns 51, and `grep -n '^## Gate$'` returns line 31.

## Tools
- No installs or updates performed.
