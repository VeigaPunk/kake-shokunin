# ReviewerAppendOnly — round-54 append-only verification

Seat: `ReviewerAppendOnly` (reviewer). Scope: verify the S374 knowledge entry and
lesson/QUALITY corrections are pure append-only additions preserving every original
line byte-for-byte against round-open base `68228b2d74e7930ae4f07e90e382a0d03ab80c7b`.
Read-only; no files modified except this report (sole report-path exception).

## Timeline note

At first inspection the round-54 edits were unstaged in the worktree; executor
commit `8e408e0` ("round-54: repair S374 calibration and settle r53 ops debt")
landed mid-review on top of freeze commit `acae1dc`. Base `68228b2d` is unchanged
and remains the direct round-open base. All results below are verified against
committed HEAD = `8e408e0`; worktree is clean vs HEAD except the untracked
`w1/` reports directory.

## Method

- `git diff 68228b2d HEAD --numstat`, `--name-status`, `--diff-filter=DR` for the
  full delta (adds/deletes/renames anywhere).
- Byte-prefix test per modified file: `git show <base>:<f>` vs `git show HEAD:<f>`
  under `cmp -n <base_size>` — the strongest form of "original preserved
  byte-for-byte" (every byte of the old file is the literal prefix of the new).
- Hunk inspection of each modified file (`git diff 68228b2d HEAD -- <f>`).
- `corpus/lessons/` name-status vs base to enumerate lesson-file changes.
- Read-only counter runs at both revisions (named counter command, `--root .`).

## Findings — claim CONFIRMED within its named scope

| File | Base bytes | HEAD bytes | Result |
|---|---|---|---|
| `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md` | 2983 | 4095 | **PREFIX-OK** — base blob is an exact byte-prefix; single hunk `@@ -49,3 +49,20 @@` appends 17 lines after EOF |
| `corpus/QUALITY.md` | 96829 | 98742 | **PREFIX-OK** — base blob is an exact byte-prefix; single hunk `@@ -1114,3 +1114,31 @@` appends 28 lines ("Round-54 criteria") after EOF |
| `corpus/lessons/round-54.md` | — | 45 lines | New file (`A`); append-only by construction |

- The appended knowledge block is the `[r54-correction 2026-10-25]` correction
  quoting 「このリンク先のウェブページの巡回を推奨していない」 and asserting the
  crawl qualifier; the old endorsement-only gloss is explicitly "preserved as
  historical text". File mode unchanged (100644→100644).
- QUALITY appends two criteria (material-qualifier preservation, CJK unit
  accounting) under a new "Round-54 criteria" heading. File mode unchanged.
- `corpus/lessons/round-54.md` is the only `corpus/lessons/` change vs base; no
  older lesson file was modified or deleted. It records Gate source re-opening,
  three Mistakes rows, the round-53 settlement summary, and the round-54 claims
  ledger — all new content.
- No other `corpus/` path changed vs base (name-status: only QUALITY.md,
  knowledge entry, new lesson file). Zero deletions or renames anywhere in the
  delta (`--diff-filter=DR` empty).

## Counter evidence (read-only, named command)

- At base `68228b2d`: `mismatches=1 met=False`, exit 1 — matches the committed
  do-nothing control receipt (`controls/base-c1-s374.txt` expectation).
- At HEAD: `mismatches=0 met=True`, exit 0; C1.3 finds a valid correction block
  at byte offset 2876 (exact source quote + crawl token).

## Observations — outside the claim's wording, same base→HEAD delta

- **`SKILL.md`: insertion, not EOF-append.** One new registry-table row for
  `c53-gate-truth` inserted at line 213; 0 deletions, so all original lines are
  preserved in order, but it is a mid-file insertion, not a literal append.
- **`SCORECARD.md`: NOT append-only.** 6+/2-: the axes-ownership sentence is
  rewritten (deleted line replaced by 5 lines adding a round-54 calibration
  sub-axis) plus one new `calibration` table row. Original lines are *not* all
  preserved byte-for-byte. SCORECARD is not part of "S374 knowledge entry and
  lesson/QUALITY corrections," so this does not refute the claim as scoped, but
  if "append-only" is ever applied to the whole round-54 corpus delta,
  SCORECARD is the counterexample.
- All `.ufo/waves/round-54/` artifacts (contract, counters, controls, specs,
  `source-reopen.txt`) and `.ufo/waves/round-53/settlement.md` are additions
  (`A`); the `w1/` seat-report directory is untracked per the wave's
  report-path exception.

## Residual risk / gaps

- "Append-only" verified at the byte level against the frozen base; semantic
  adequacy of the appended correction (quote exactness, supersession binding)
  belongs to `CriticC1SourceQuote`/`CriticC1CorrectionBinding` and the counter,
  not this seat.
- SKILL/SCORECARD edits are reported as observations only; their admissibility
  is a contract question (C2 surface names SKILL registry row and settlement
  manifest, not SCORECARD).

## Tooling

No installs performed; `git`, `python3`, `cmp` already present. Pacman not run
(host-wide pause honored).

## Verdict

CONFIRMED: `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md`,
`corpus/QUALITY.md`, and `corpus/lessons/round-54.md` are pure append-only
additions vs `68228b2d` — the two modified files preserve their entire base
blobs as exact byte-prefixes, and the lesson file is new. Caveat recorded:
`SCORECARD.md` rewrote two lines and `SKILL.md` inserted a row mid-file in the
same round-54 delta; both are outside the claim's named scope.
