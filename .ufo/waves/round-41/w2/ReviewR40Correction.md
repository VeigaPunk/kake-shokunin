# ReviewR40Correction — round-40 tally restatement recount

Seat: KakeR41.ReviewR40Correction (w2 falsify). Scope: routed defect 1 — "round-40 tally restated as
26 of 72 live-seat receipts" (`w1/ReviewR40Restatement.md`). Read-only lane; sandbox
`/fast/scratch/hyaku/kake-r41w2/ReviewR40Correction/`. No installs needed (python3 + system jq used).

## Commands (all exit 0 unless noted)

- `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C <lane> archive 8eb121c8
  .ufo/waves/round-40/verification/w1 | tar -x -C <sandbox>/arc` → 79 entries: 76 JSON receipts + 3
  `d1check-*.txt`.
- Python recount over the extracted receipts (`met` field): total 76, met 27; `CtlUTabOnly-dead__*`
  4 receipts, 1 met (`tool_tab_only_query`, passed 30); live = 72 receipts, 26 met. Every JSON has a
  `met` field; no empty/odd files.
- `git rev-parse 8eb121c8:.ufo/waves/round-40/verification/w1` = `0c732d5a:…` = `73cf8989…`; 
  `merge-base --is-ancestor 0c732d5a 8eb121c8` → exit 0: restatement over unchanged bytes (matches the
  w1 report's claim).
- `python3 .ufo/waves/round-41/criteria/live_tally_check.py --dispatch-log
  .ufo/waves/round-40/w1-dispatch-log.txt --receipts <sandbox>/w1` → exit 1, dead seats
  `['CtlUTabOnly']`, 4 dead-seat receipts listed — identical to committed `verification/criteria/
  live-tally-r40.txt`.
- Same check on round 41: `--dispatch-log .ufo/waves/round-41/w1-dispatch-log.txt --receipts
  .ufo/waves/round-41/verification/w1` → exit 0, "dead seats: none; receipts: 141".
- `grep LOG.md` → round-41 section LOG.md:1586–1606; line 1603 carries "round-40 tally restated 26
  of 72 live-seat receipts". Full proposed sentence lands verbatim in
  `corpus/lessons/round-41.md:103-107` (and the ruling at :82-86 cites the w1 report).
- `grep SCORECARD.md` for `26 of 72|26/72|live-seat receipt|restat|CtlUTabOnly|live_tally` → only
  hits are the round-40 kill-record table row SCORECARD.md:2643 (dead-seat `tool_tab_only_query`
  still inside the meeting "partial repairs" row) and the round-41 kill-rule text :2741-2744
  ("control tallies count live seats"). SCORECARD.md ends at line 2817 with no appended correction.

## Per-statement verdicts

| Statement | Verdict |
|---|---|
| Tally restated 26 of 72 live-seat receipts | **holds** — 76−4 dead = 72; 27−1 = 26; `tool_tab_only_query` (met true, 30/30) is the only dead-seat member of the 27 |
| `MutFamilyU__M11_tab_before_query` re-derives the sub-shape live | **holds** — receipt met true, passed 30 |
| Restatement over unchanged bytes (vs `0c732d5a`) | **holds** — identical tree object `73cf8989…` |
| Kill rule unaffected (26 ≥ 1) | **holds** — kill rule (1) still fires; no round-40 conclusion changes |
| LOG carries the restatement as appended text | **holds** — LOG.md:1603 (round-41 section; round-40 section left untouched, append-only discipline) |
| SCORECARD carries the restatement | **missing** — no 26-of-72 mention anywhere; round-40 kill-record row 2643 still lists the dead-seat tool with no correction pointer |

## Finding

- **SCORECARD.md (low):** the 26-of-72 restatement is absent from the scorecard; the round-40
  kill-record row (SCORECARD.md:2643) still credits the dead seat inside the meeting-controls row.
  The correction survives in LOG.md:1603 and lessons/round-41.md:103-107, and the (s) check exists
  and fails correctly, so this is a durability gap, not a wrong number. If a L1 SCORECARD append is
  still pending, it should name the restatement there.

## Residual risk

Recount reads committed receipt bytes (same tree the closure used); it is not a re-execution of the
round-40 counter. `verification/criteria/` has no `live-tally-r41.txt` receipt file for the exit-0
run, but I reproduced the green result locally (exit 0, 141 receipts). No lane writes made outside
this report.
