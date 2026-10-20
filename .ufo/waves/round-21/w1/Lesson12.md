# Lesson12 — round-6 lesson historical Gate (round-21 w1)

## Behavior
- Target: `corpus/lessons/round-6.md`. Had no `## Gate` heading, so a Gate section was appended at EOF.
- Gate is labeled as a retrospective round-21 reconstruction, not the original round-6 admission.
- Prefix bytes untouched; no metadata prefix added (provenance-header work belongs to another lane).

## File changes
- `corpus/lessons/round-6.md`: old line count **47**; pre-edit sha256 `642462bf37f3a9682c29aac3482e0996556dc1cf5e25f492b472a892fd1e913c` (matches `frozen/before/expected.json`). Appended 27 lines (blank line 48, `## Gate` at 49, through line 74). Tag after edit `#2DDD`.
- This report: `.ufo/waves/round-21/w1/Lesson12.md`.
- No commits, no other files, no subagents.

## Gate content (what the appended section covers)
- Ten candidates from original sections "The gap closed", "What the audit actually found", "Learned", and header line 6 ("Commit `round-6`").
- Outcomes: C1, C2, C3, C5, C8, C9 admitted with qualification or as method; C4 admitted source-based but unrereadable; C6 unverified (frontier per round-20 gate lines 191-193); C7 "~95%" figure unverified; C10 unverified historical record.
- Rejected candidates: not recorded (none documented in the lesson, round-6 `LOG.md` entry, or `ghp-subpath-spotcheck.md`).
- Outside spot-check: not recorded (no non-author verifier named for round 6).

## Evidence basis (all existing local records; no live re-read)
- `corpus/lessons/round-6.md` original sections (lines 1-47, unchanged).
- `LOG.md` round-6 entry (line 8, verbatim count and breakdown matched); later entries used only as historical cross-references: round-8, round-13, round-14.
- `corpus/knowledge/ghp-subpath-spotcheck.md`: S019 metadata header (lines 1-3) and round-6 evidence line 7.
- `corpus/lessons/round-20.md` gate lines 182-196 (non-admission of `round-6.md:33-34`).
- `corpus/lessons/round-7.md` lines 23-25 (origin/main cross-reference).
- `.ufo/waves/round-21/wave1-spec.json` Lesson12 item and `# Contract`, used because `corpus/lessons/round-21.md` is absent at write time.
- Arithmetic checks only: 1 874 + 35 + 443 = 2 352; 120 + 5 + 1 = 126.

## Out-of-scope items observed (not edited)
- `corpus/lessons/round-21.md` absent (glob). Round-21 lesson cited via wave artifact instead.
- `corpus/CORPUS.md` absent; S019 cited as pending L1 registration.
- `~/Projects/webzites/src/reconcile.mjs` absent since 2026-10-12 prune (per lesson line 5); C4 rests on historical read only.
- `round-6.md` provenance header has `Cites:`/`Commit` but no `verified-at:`/`recheck:` lines; left for the metadata lane.

## Tools
- None installed or updated.

## Checks for main agent (not run by me)
- Confirm `round-6.md` line 1-47 bytes match pre-edit sha `642462bf…913c` for prefix preservation (I did not re-verify after edit).
- Confirm `## Gate` heading appears exactly once in `round-6.md`.
