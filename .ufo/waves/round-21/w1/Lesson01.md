# Round-21 W1 · Lesson01 — `corpus/lessons/round-1.md` historical Gate

## Behavior

- Target: `corpus/lessons/round-1.md` (only file edited).
- Before: 37 lines, 1829 bytes, sha256 `591372a1ffddafc42495e2fc3c7c79f8b6b9ac41d3e84ab916994f9a7e1a4e1b`. The file had no `## Gate` heading, so the append path was taken. The pre-edit hash equals the value recorded for `corpus/lessons/round-1.md` in `.ufo/waves/round-21/frozen/before/expected.json`.
- After: 70 lines, 6296 bytes. Appended one blank line plus a `## Gate` section (lines 38-70). Exactly one `^## Gate$` heading.
- Byte preservation: `head -c 1829` on the post-edit file has sha256 `591372a1…e1b`, identical to the pre-edit hash. Every prior byte is preserved; the edit is a pure EOF addition.
- Gate content is labeled a retrospective round-21 reconstruction, not an original admission, and is marked historical-not-live-reverified.

## Gate contents (what the appended section states)

- Candidates: 9, drawn from the original Worked, Failed/surprised, and Open sections.
- Outcomes, per audit `corpus/lessons/round-1-aggregator-audit.md` (2026-09-28, aggregator L1 + independent L2 reviewer): admitted 2 (`ufofsdbeta` runtime; open probe-blindness problem as open), admitted with qualification 2 (registry ground truth; publish gate), qualified 1 (`ls ~/Projects` undercount / sourceDir map), not admitted as stated 1 (`~40 clones`, audit observed 50), unverified 4 (`sourceDir` hazard; byte-equality primitive; `ds4cc.kimi.page` stale; plazir15/charter 404s). Each is labeled individually in the file.
- Rejected candidates: "not recorded" (no rejection appears in lines 1-37, in the audit, or in the visible part of `LOG.md` line 4).
- Outside spot-check: existing independent evidence cited (`round-1-aggregator-audit.md`). It is a full audit, not an admit/reject spot-check sample. No separate round-1 spot-check record exists; `round-20-verifier-spotcheck.md` covers round 20 only.
- Original-section cites: header lines 3-4; Worked 6-16; Failed 18-28; Open 30-37.
- Round-21 lesson: not present in `corpus/lessons/` at write time; round-21 contract cited as `.ufo/waves/round-21/` (Lesson01 entry in `wave1-spec.json`).
- S019: cited via the `corpus/SOURCES.md` S019 row (grade A, metadata authority, not platform authority). The canonical `CORPUS.md` was not readable at its registered path from this seat, so only the SOURCES.md row is cited.

## Evidence basis

- Original sections of `round-1.md`: read in full (37 lines).
- Independent evidence: `corpus/lessons/round-1-aggregator-audit.md` (read in full).
- Context: `LOG.md` lines 1-12 (round-1 entry at line 4, read truncated); `corpus/lessons/round-20.md` lines 36-70 and 178-215 (Gate section convention); `corpus/SOURCES.md` S019 row (grep).
- Frozen baseline: `.ufo/waves/round-21/frozen/before/expected.json` (hash string match only).

## Live-state probes (disclosed, not used as historical evidence)

- Two live filesystem checks were run before the append: `ls .ufo/reports/round-1/` in the kake checkout (absent) and a readability test of the registered S019 `CORPUS.md` path (not readable). Neither was used as historical evidence and neither is claimed in the gate. The gate's limits section records the historical `~/Projects` absences from the audit's r18 annotations only.
- No domain recheck, network read, probe, deploy, or publish was performed.

## Out of scope / not touched

- No other lesson, knowledge file, SCORECARD, LOG, QUALITY, SOURCES, README, or SKILL was edited.
- No prefix metadata was added (C1 applies to provenance headers, not this file).
- No commits. No tool installs or upgrades.

## Findings

- The round-1 lesson's "~40 site clones" figure is stale. The audit observed 50 (defect 2). Recorded as "not admitted as stated"; the original text is preserved.
- Audit defect 1 (21 registry rows vs 20 in other documents) is not inside `round-1.md` but qualifies the "registry as ground truth" candidate.
- Unresolved in the record: the audit's note that the round-1 lane report filename violates `PROTOCOL.md` (should be `kake.md`) was filed to the integrator; no resolution is recorded in the files read.

## Checks for main agent (not run by this seat)

- `sha256sum` of the first 1829 bytes of `corpus/lessons/round-1.md` equals `591372a1…e1b`; `wc -l` = 70; `grep -c '^## Gate$'` = 1.
- Optional: confirm the 70-line gate renders as valid Markdown in the corpus lint, if one exists.

## Tools

- None installed or updated.
