# Round-21 wave 1 — Lesson04 report (corpus/lessons/round-16.md)

Seat: `KakeR21.Lesson04` (scribe, leaf). Target: `corpus/lessons/round-16.md` only.

## Behavior

- Target had no `## Gate` heading, so the gate was appended. Existing content unchanged.
- The `## Gate` heading is exact (line 78). Its label is the first bold line:
  "retrospective round-21 reconstruction, not original admission".
- The gate section lists candidates A–H, each with a historically supported outcome
  (admitted with qualification, admitted, rejected, or unverified).
- Rejected candidates are listed only where the record documents them. Otherwise the
  gate says "not recorded".
- Outside spot-check: not recorded. No non-author round-16 verifier sample exists in
  the repo. In-round critic/reviewer verdicts and the round-17 re-sweep are cited as
  existing evidence and labelled as not outside review.
- Original sections cited with line ranges: 7-38, 40-52, 54-64, 66-76.
- Round-21 link: `.ufo/waves/round-21/wave1-spec.json` Lesson04 entry. The round-21
  lesson file `corpus/lessons/round-21.md` does not exist; it is not cited for content.

## Gates

- Gate heading present: `## Gate` at line 78. Exact-heading check passes.
- Prior bytes preserved: `head -c 4391 | sha256sum` =
  `b9f0d123eb3c9a3c78a880cb689d6d5703d7f84da9757af8045eb3f3235cfdbf`, equal to the
  pre-edit full-file sha. This is the only verification run.
- No build, lint, test, or live re-verification run, as assigned.

## Line counts

- Before: 75 LF-terminated lines; 76 lines counting the unterminated final line
  `…before landing.`; 4391 bytes.
- After: 178 lines (`wc -l`), 10757 bytes. The unterminated final line was
  terminated as part of the append (one `\n` added after the original last byte).
  Appended block: lines 77-178.

## Appended evidence basis

- `LOG.md` round-16 entry, lines 208-309; round-17 entry, lines 311-398.
- `corpus/knowledge/freshness-sweep.md` lines 30 and 78.
- `corpus/knowledge/free-read-verbs.md` lines 173-176 and 218.
- `corpus/knowledge/ops-automation.md` line 5.
- `corpus/knowledge/fire-journal-codes.md` (journal key union and fire count).
- `corpus/knowledge/publish-queue.md` line 34 (PQ-14); `drift-detection.md` lines 42, 67.
- `scripts/freshness-sweep.mjs`, named by the lesson and the LOG. Its existence and
  content were not re-checked this round.
- Not available: `/tmp/kake-r16/` is absent. Its raw artifacts were not read; the
  gate's numbers rest on LOG and runbook text.

## S019 / metadata contract

- The wave spec names S019 as the metadata and gate corpus contract, with `CORPUS.md`
  as its registration point.
- No S019 identifier and no `corpus/CORPUS.md` exist in the repo (grep over the repo
  excluding `.ufo`: zero hits). S019 is cited by name only and is not a verified
  source. The gate records verified-at as the round-16 LOG date (2026-09-29),
  historical-not-live-reverified.

## Touched surfaces

- Changed: `corpus/lessons/round-16.md` (append only).
- Created: this report.
- Not touched: SCORECARD, LOG, QUALITY, SOURCES, README, SKILL, verifier/aggregator/
  operator lessons, any other target.

## Out of scope / not done

- No live re-verification of any claim.
- No outside spot-check performed (none assigned, none recorded).
- No tool installs or updates.

## Findings for the main agent

- Operator decision needed: `/tmp/kake-r16/` is missing. Restore it from backup or
  retire the round-16 citations to it. The gate states this as a recheck requirement.
- The round-17 LOG entry lists `corpus/lessons/round-16.md` among its repo edits. The
  file as found had no round-17 annotation, and the LOG's round-17 reference to it was
  not reconciled here. Left as found, per the preserve-bytes rule.

## Checks for main to run once

- `grep -n "^## Gate$" corpus/lessons/round-16.md` → one hit at line 78.
- `head -c 4391 corpus/lessons/round-16.md | sha256sum` → `b9f0d123…cfdbf`.
