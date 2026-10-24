# ReviewLessonDraftCheck — criteria checks can fail; per-draft verdict

Seat: KakeR41.ReviewLessonDraftCheck (leaf). Axis: operability. Item: the two QUALITY checks in
`.ufo/waves/round-41/criteria/` (s = live tally, t = fresh review) and `w1/ScribeLessonDraft.md`.
Note: build sha is written elided (`0b485431…13edbf`) everywhere so this file cannot itself trip a
future `--reports w2` scan (the check greps the first 16 hex chars).

## Runs (cwd = lane repo; `timeout 60 prlimit --as=4000000000 -- python3 -B`)

1. `live_tally_check.py --dispatch-log .ufo/waves/round-40/w1-dispatch-log.txt --receipts .ufo/waves/round-40/verification/w1`
   → **exit 1**. Output: `dead seats: ['CtlUTabOnly']; receipts: 76; dead-seat receipts in tally: 4`
   (four `CtlUTabOnly-dead__*.json`; exactly one is met — `tool_tab_only_query`, `met: true` — matches draft's "4 scored, 1 met").
2. `live_tally_check.py --dispatch-log .ufo/waves/round-41/w1-dispatch-log.txt --receipts .ufo/waves/round-41/verification/w1`
   → **exit 0**: `dead seats: none; receipts: 141; dead-seat receipts in tally: 0`. Same on `verification/w1v2` → exit 0.
3. `fresh_review_check.py --tool-sha 4de35f8c…1460e (full r40 sha) --reports .ufo/waves/round-40/w1 .ufo/waves/round-40/resid`
   → **exit 1**: `seat reports naming it: 0`. Fails on round 40 as required: no in-round report names the final-build bytes.
4. `fresh_review_check.py --tool-sha 0b485431…13edbf (full r41 sha) --reports .ufo/waves/round-41/w1 .ufo/waves/round-41/w2`
   → **exit 0**, 5 hits: `w2/CriticExploratoryBetter.md`, `RerunBuildV1Seeded.md`, `RerunBuildV2.md`,
   `ReviewHarmRealRun.md`, `ReviewHarmScope.md`. `--reports w1` alone → **exit 1** (0 hits: pre-build reports never name the build sha; the check discriminates).
5. `--l1 KakeR41` appended → argparse `error: unrecognized arguments`, **exit 2**.

## Per-draft verdict

- **(s) live tally — fix can fail: holds.** Exit 1 on r40 (names the 4 dead receipts), exit 0 on r41.
- **(t) fresh review — fix can fail: holds.** Exit 1 on r40 (zero reports name the revised-build sha;
  consistent with draft defect 2: in-round checks were L1 reruns, non-author check only in closure).
  Exit 0 on r41.

## What (t) needs to go green on round 41

A `.md` under a scanned reports dir, not an L1 file, containing the build sha's first 16 hex chars.
Already satisfied: `w2/ReviewHarmRealRun.md` pins the worktree tool sha `0b485431…13edbf` at HEAD
`eae5ae2c` and reruns both tools — a fresh non-author review of the final build before the report.

## Findings (check quality, all minor)

- `fresh_review_check.py:11-14`: docstring advertises `[--l1 <id>]` and exclusion of L1 / `*.verdict`
  files; the argument is never declared (run 5, exit 2) and **no exclusion is coded** — an
  L1-authored `.md` naming the sha would pass, which is the failure mode defect 2 exists to catch.
  Medium: the gate is weaker than its contract (name-any-mention), though it passes today on a
  genuine review (`ReviewHarmRealRun`) and failed correctly on r40.
- `fresh_review_check.py`: no "review receipt" semantics — rerun reports (`RerunBuildV1Seeded.md`,
  `RerunBuildV2.md`) and any sha mention count as a hit. Minor.
- `live_tally_check.py:19`: seat-id capture `[A-Za-z0-9_]+` drops hyphens; a dead seat id containing
  `-` would be captured truncated and could over-match a live seat sharing the prefix. No r40/r41 id
  is hyphenated — latent only. Minor.
- `live_tally_check.py` tests presence of dead receipts in the dir, not the draft's "re-derive
  27/76 vs 26/72" census arithmetic; it catches the defect class but a falsely-claimed live tally
  with clean files would pass. Minor.
- Scribe draft (`ScribeLessonDraft.md`) is honest about its limits: defects 1–2 "proposed, not run";
  this seat ran both and they behave as claimed. Defect 3 (label leak) has no criterion file;
  draft marks it recorded-evidence-only — consistent.

## Bounds

Read-only on the lane; this report is the only write. `-B` used; no `__pycache__` touched. No
installs, no network, no subagents. All five invocations exited as shown; nothing timed out.
