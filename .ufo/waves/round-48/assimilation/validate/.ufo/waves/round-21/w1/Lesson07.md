# Round-21 w1 — Lesson07 report

Seat: KakeR21.Lesson07 (leaf scribe). Target: `corpus/lessons/round-19-recensus.md` only.

## File change

- Target `corpus/lessons/round-19-recensus.md`: had no `## Gate` heading. Old line count **60** (tag `#949D`). Appended a pure EOF tail at lines **61-98** (new tag `#4D5E`). No prior byte altered; no other file edited.
- Appended section: `## Gate`, labelled "Retrospective round-21 reconstruction, not original admission". It holds the original-section citations, a later-reference list, the S019 contract statement, a candidate/outcome table (C1-C8), documented rejected candidates (R1-R3), an outside spot-check statement, and a gate-completeness note.

## Evidence basis (read, not re-run)

- Target lesson, full (60 lines, raw tail 44-60).
- `corpus/lessons/round-20.md` Gate (41-60), Named debt (62-82), Round-20 resume (146-180), Gate — round-20 resume (182-196), Mistakes M4-M6 (252-254), line 77-79 and 165-174.
- `corpus/QUALITY.md:16-20` (criteria citing `round-19-recensus.md:44`, `:52-53`).
- `corpus/lessons/round-20-verifier-spotcheck.md` (round-20 only; no round-19 spot-check).
- `.ufo/waves/round-21/wave1-spec.json` (round-21 contract; S019 metadata contract stated in its prompts).
- Greps over `corpus/` and `.ufo/waves/round-21/` for `S019`, `round-21`, `CORPUS.md`, `## Gate`.

No live-state recheck, no build, lint, or test run, and no network read. Only the lesson's own content and on-disk references were used.

## Findings

- Round-21 lesson file: none on disk (`corpus/lessons/round-21*` absent). The round-21 contract is `.ufo/waves/round-21/wave1-spec.json`.
- S019: not found under `corpus/` (no match in `SOURCES.md` or elsewhere in `corpus/`). `CORPUS.md` not on disk. Per the wave spec, L1 registers it. The Gate section records this as pending and does not invent an entry.
- Outside spot-check for round 19: **not recorded**. In-file independent audit (erratum, 2026-10-14; author not named) is the only existing independent evidence and is cited as such.
- Rejected candidates: only R1-R3 are documented in the lesson (re-pin to silence exit 1; in-round patch of the confinement flaw; re-fetch of missing commit hashes). Reasons beyond the lesson's own words are marked "not recorded".
- Outcomes: C1-C2 admitted with qualification (retrospective reading, no explicit admit row); C3 unverified; C4 admitted as finding and partly repaired downstream (round-20 C2/M4); C5-C6 carried, not closed; C7 population-unit criterion admitted, 77/8 reconciliation carried; C8 recorded as a mistake, not re-verified.

## Out of scope / not touched

SCORECARD, LOG, QUALITY, SOURCES, README, SKILL (L1). No other lesson files. No commits. No subagent dispatch (leaf).

## Tools

None installed or updated.

## Checks for main agent

- `wc -l corpus/lessons/round-19-recensus.md` should read 98.
- Stripped-diff of the file against base `5009ecaa1cce10b895617a585ddd3f7c7c923a84` should show only additions at lines 61-98.
