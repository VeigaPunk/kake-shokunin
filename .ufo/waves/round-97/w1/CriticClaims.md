# CriticClaims — round 97 scoped findings (C1, C2 as frozen)

Full evidence, commands, rc values and receipts: `.ufo/waves/round-97/w1/CriticClaims/claims.md` and `receipts/`.
Lane tip read: `9e27ce0b2a8d168e032ab79ea11471b36eaceedf`. Frozen digests verified before attack (all three match).

## Findings

- **C2 (falsified as frozen).** Five candidate variants of the real `scripts/reval_exchange.py`, each a few-line
  edit, score `met=true`, exit 0 through the public CLI, while breaking contract v1: K1 treats only 500/503/599 as 5xx
  (502 → replace-stored, contract C4 says may-reuse); K2 accepts DQUOTE and DEL inside etags; K3 accepts boolean
  `last_modified`; K4 accepts 101–199 as decisions; K5 is all four. The population enumerates only three 5xx statuses,
  one control byte of the etag grammar, no bool timestamp and only 100 among the 1xx codes.
- **C2 sizing.** The reference refuses 16 of 120 seed-97 generated inputs and these are silently dropped, so the printed
  `generated=104/104` contradicts the contract's "all 120". `mutants=14/14` scores the frozen positive control, never the
  candidate, so it is identical for every candidate and does not measure it. The candidate blob is byte-identical at base
  and tip (`192b3bf7`), so the C2 credit is an instrument credit for a round-96 artifact (consistent with the r96 flip rule).
  Concurrent scorings sharing one `--work` crash with rc=1 (fail-closed).
- **C1 (falsified as frozen).** One table row with all 84 entry tokens, every source id and 168 entry-derived words
  yields `mismatches=0 met=true` exit 0 (`index_rows 130`). Per-entry rows copying each entry's first prose line yield the same
  (`index_rows 213`). The counter's unit (entry, any row) and the review unit (row; verdict format per entry) do not match, so a
  multi-entry row cannot be judged per entry, and "agree count equals row count" is satisfied by one agree.
- **C1 sizing.** 29 rows still in `corpus/README.md` fail the counter's own per-row test (filed history, not reviewed,
  invisible to the per-entry count). Three own-work entries have no source ids, so their id gate is vacuous. "The round-97
  index section" is not a counter construct. The frozen do-nothing control fails, but does not cover the work-skipping
  class (multi-entry row, copied scope).
- **Causal separability.** Holds for both: C1 reads only `corpus/README.md` and `corpus/knowledge/*.md`; C2 reads only the
  candidate, round-96 pins/fixtures/mutants and the round-97 forgery. Neither verdict needs the other.
- **r34-class junk-row route.** Not closed. The shuffle known-limit plus the row-review conjunct close only what reviewers
  reject per row; the predicate does not require one judged row per entry, so a single junk row or mechanical copy can
  satisfy it. Closure needs a per-entry predicate: an instrument change, routed to round 98, not made here.

## Commands (all rc observed)

- `python3 -B .ufo/waves/round-97/c97_reval.py --root <LANE> --revision 9e27ce0b… --work <scratch>` → `met=true` rc 0 (tip).
- Variants K1–K5 and M1/M2, each `--root <clone> --revision <new commit>` → rc 0, `met=true` (C2 ×5; C1 ×2).
- Probes through `python3 -I` on each candidate file → `receipts/direct-probes.txt` (contract outcomes in `claims.md`).
- Stale-row scan (`stale.py`, read-only) → `receipts/stale-rows.txt`, rc 0.

Tools: none installed or upgraded (system python3 stdlib, /usr/bin/git). Scratch removed before yield.

CRITIC C1=falsified C2=falsified findings=16
