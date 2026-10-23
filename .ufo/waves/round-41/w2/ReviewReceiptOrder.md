# ReviewReceiptOrder — r41 wave 2, receipt/commit-order falsification

Axes: operability (judged), freshness. Leaf seat, read-only on the lane; no installs needed.

## Commands run (all exit 0)

- `git -C <lane> log --format='%H %cI %s' 8eb121c8..eae5ae2c7dc5de2ba489f02b936fc5040b07b7d6` → exactly 3 commits.
- `git merge-base --is-ancestor` abf457d0≤9e3c31d2, 9e3c31d2≤eae5ae2c, 8eb121c8≤eae5ae2c → all true.
- `git log -- scripts/sitemap_audit.py` (top 20) → newest eae5ae2c, next d8d5578e; `merge-base --is-ancestor d8d5578e 8eb121c8` → yes.
- `git ls-tree -r --name-only 9e3c31d2|HEAD -- .ufo/waves/round-41/verification/w1/`; `git log --diff-filter=A` on that dir → only 9e3c31d2 ever touched it; `git diff --name-status 9e3c31d2 eae5ae2c -- <dir>` → empty.
- `git show --name-status` on each of the 3 commits; `git diff-tree -r 9e3c31d2 | grep -v '^A'`.
- `jq -s 'map(select(.met))|length' .ufo/waves/round-41/verification/w1/*.json` → 15; file count → 141.
- `git show <rev>:scripts/sitemap_audit.py | sha256sum` at build/base; `sha256sum` worktree.
- Read `.ufo/waves/round-41/w1-dispatch-log.txt` (2 lines) and SCORECARD.md Round-41 sections (2672–2830).

## Timeline (UTC; commit dates are committer %cI)

| when | event | evidence |
|---|---|---|
| 09:44:54Z | `abf457d0` pre-freeze: SCORECARD pre-freeze section (M), counter v1 `c1_count.py`, oracle wheels + crosscheck, L1 controls/receipts, census-before | commit `abf457d0` |
| 09:47:43Z | wave 1 dispatched: 37 seats, gate line | `w1-dispatch-log.txt:1` |
| 10:03:28Z | wave 1 settled: 37 returned, 0 dead/refused; L1 re-scored 141 tools → 15 meet | `w1-dispatch-log.txt:2` |
| 10:04:45Z | `9e3c31d2`: 141 receipts added (all `A`), `c1_count_v2.py` added, SCORECARD kill-rule section added (2 diff hits for "kill rule (1) fired"), counter v1 itself untouched | commit `9e3c31d2` |
| 10:05:27Z | `eae5ae2c` build: `scripts/sitemap_audit.py` M (first change since base), `sitemap_audit_selftest.py` M, `SKILL.md` M, `realrun/` inputs A; **zero** w1 receipt paths changed | commit `eae5ae2c` |

Receipts commit sits 77 s after wave settle and 42 s before the build — matches the dispatch log's own times.

## Findings

- INFO: `9e3c31d2` also modifies `score.sh`, `oracle_crosscheck.py`, `corpus/SOURCES.md` (scoring helpers/sources), but not `c1_count.py` — consistent with "re-scored with the unchanged counter v1 bytes".
- INFO: ticket says `verification/w1/*.json`; the lane path is `.ufo/waves/round-41/verification/w1/*.json` (round-40's sibling dir predates the range, added `12211cc5` 05:49:41−03:00). Judged the round-41 set.
- No defect found in scope.

## Per-statement verdict

- Commit order abf457d0 → 9e3c31d2 → eae5ae2c, all inside `8eb121c8..build`: **holds** (topology + timestamps agree).
- Every `verification/w1/*.json` added at `9e3c31d2` or earlier: **holds** — 141/141 added exactly at `9e3c31d2`; dir absent at `abf457d0`; no add or modify after it; build commit touches none.
- Build file first changed at `eae5ae2c`: **holds** — only commit in the range touching it; prior toucher `d8d5578e` is an ancestor of base `8eb121c8`. sha256 build `0b485431…13edbf`, base `4de35f8c…1460e`, worktree == build: **matches claim**.
- Receipts/kill-rule recorded before the build, per `w1-dispatch-log.txt` times: **holds** (10:03:28Z settle < 10:04:45Z receipts < 10:05:27Z build).
- `15 of 141` receipts meet the predicate: **holds** (jq count = 15 over 141).

## Residual risk / gaps

- Commit `%cI` is committer time; jj-amended commits can carry amend-time committer dates. The two load-bearing orderings (settle < receipts < build) are independently corroborated by the dispatch log and by diff topology, so the conclusion does not rest on timestamps alone.
- Receipt *contents* beyond the `met` field (labels, seeds, sandbox fields) not re-derived here — other seats' scope. `verification/w1v2/` (counter v2) is next-round information, not checked.
