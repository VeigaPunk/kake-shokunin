# ExecDefects — round 89, wave 1 — C1 fix bytes

Base `76225160d0dff8d2042fbcd037bd08b0971d5e07`. Lane HEAD at the time of this seat: `46a43e94` (not `2e700b9a`; see finding 2). The lane working tree has uncommitted edits by another actor to `SCORECARD.md` and `corpus/lessons/round-88.md` (see finding 5).

## Deliverables (all under `.ufo/waves/round-89/w1/ExecDefects/`)

- `c1-fix.diff` — unified diff against base `76225160` for every existing file (`SCORECARD.md`, `corpus/lessons/round-88.md`) and the new file `corpus/lessons/round-89.md`. Reverse-apply check against the patched scratch tree passed (`git apply -R --check`).
- `round-89.md` — full new-file content for `corpus/lessons/round-89.md` (markers `gate-sample`, `r88-gate-summary-correction`, `r88-c-rerun`, `controls-count`; `## Mistakes` table with five columns and ten rows).
- `receipt.md` — each defect, its closing edit, the primitive command that re-derives it, and the observed output; plus counter defects.
- `base-vary-match-selftest.txt` — `python3 -B scripts/vary_match.py --selftest` at base: `selftest: 35/35 passed`, `exit=0`.

## Closures

| Item | Closing edit | Status by primitive |
|---|---|---|
| A stale selftest number | SCORECARD 5469, 5488 tagged `[r89-correction …]`; lesson 265 tagged; `integrated-selftest: 35/35` line in new `## Round 89` section | tool prints 35/35 exit 0; no untagged `22/22` in SCORECARD round-88 window or in lesson; one marker line, value `35/35` |
| B Gate counts | `gate-sample: admits=2 rejects=2`; `r88-gate-summary-correction: admits=2 rejects=2` | `## Gate` at base parses admits 2, rejects 2 |
| C unbacked re-run | `r88-c-rerun: retracted`; short-form pointer `controls/integrated-selftest.txt` corrected to `integrated-selftests.txt` | all six full-prefix round-88 receipts named in SCORECARD/lesson exist at base; `integrated-selftest.txt` (singular) does not |
| D unpinned count | `controls-count: 1590@76225160d0dff8d2042fbcd037bd08b0971d5e07` | `git ls-tree -r --name-only 76225160 \| grep -c '/controls/'` = `1590` |
| E freeze after dispatch | no content edit | ancestry and committer times hold for `08ab46a1` → `2e700b9a`, but see finding 2 |
| F lesson shape | round-89 `## Mistakes` (five columns, ten rows, round-88 L1 mistakes folded in); round-88 tagged pointer at line 329 | header contains all five required columns; rows 10; pointer line contains tag and `L1 mistakes` |

The C1 counter was **not run**, per the seat instruction; L1 measures the carrier. Mirror checks above are primitives, not the counter, and are not success evidence.

## Findings (counter, contract, case set, lane)

1. **C item C does not see short-form receipt paths.** `CTRL_RE` requires the full `.ufo/waves/round-88/controls/` prefix. Two SCORECARD round-88 rows name `controls/integrated-selftest.txt` (singular) under a prose prefix; the file does not exist at base. The counter cannot detect this class. Corrected by hand. (medium)
2. **Freeze v2 landed after dispatch; item E does not detect it.** Commit order: `08ab46a1` freeze (ct 1793826745), `2e700b9a` dispatch (ct 1793826784), `46a43e94` "freeze v2" (ct 1793826978) which changes `.ufo/waves/round-89/c89_key.py` (FORBIDDEN list and a new `open(` guard) and `controls/base-c2.txt`. This repeats the round-88 R88-E pattern. Item E reads only the adding commits of `c89_key.py` and `w1.ready`, so it passes. The C1 counter `c89_defect_queue.py`, `freeze.md`, `c2-contract.md` and `frozen/c2-cases.json` are unchanged from `08ab46a1` to HEAD. The C2 claim's "frozen before data" wording is affected; that is outside this seat's C1 scope but must be disclosed by L1. (high, freeze discipline)
3. **Item A's stale check matches only the literal `22/22`.** Other spellings of the stale claim pass. (low)
4. **Item F's column check is a substring test on the joined header.** `fix` matches `prefix`; `class` matches `subclass`. (low)
5. **The lane is being edited concurrently.** `git status` in the lane shows `M SCORECARD.md` (lines 5469 and 5488 changed; 5488 in-place `35/35`), `M corpus/lessons/round-88.md` (+12 lines, a tagged line 265 with different wording and two appended `[r89-correction 2026-11-04]` paragraphs, including a Gate "one admit and three rejects" correction), and untracked `.ufo/waves/round-89/L1/`, `assimilation/`, `controls/r88-c1-rerun-at-55d67f15.txt`. This candidate is against base and will not apply cleanly over those edits. L1 must choose one set. This seat did not touch them. (high, integration)
6. **Counter scope does not reach the round-88 report.** R88-B and R88-C text lives in the round-88 report, cited as commit `fe3e14d7`, which is not in the lane (`git cat-file -t fe3e14d7` → not a valid object). B and C close by markers, not by re-reading the report. (medium)
7. **Item D's definition differs from the spot-check's.** The counter counts any tracked path containing `/controls/` (1590 at base). The anchored `^.ufo/waves/round-N/controls/` form counts 1002 at base. The spot-check's 1,577 used a third definition at `f60a852a`. The marker pins the counter's definition; the report should name it. (low)
8. **`r88-c-rerun: retracted` is unverifiable by the counter.** It is accepted with no evidence that the sentence was removed from the report or spot-check. Chosen because no re-run receipt exists in the lane. (low)

## Honest limits

- Only the six items the seat was assigned were addressed. Item E needs no content edit; finding 2 means its "closed" status is weaker than the claim.
- Round-88 L1 mistake rows in the new `## Mistakes` table carry witnesses marked "manual" where no counter exists.
- The fixes are written as bytes for L1 to integrate; they were not committed, pushed, or applied to the lane.
- The scratch clone was created at base, `git add -N` was used on the scratch index only, and the scratch directory `/fast/scratch/hyaku/kake-r89/ExecDefects/` was deleted before yield. No `/tmp` path was used.

## Tooling

No tool was installed or upgraded. Installs/updates recorded: none. No network request was made. No subagent or labrat was dispatched.
