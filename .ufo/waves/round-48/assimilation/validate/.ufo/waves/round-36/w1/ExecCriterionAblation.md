# ExecCriterionAblation — round-36 criterion: the ablation floor

Seat `KakeR36.ExecCriterionAblation`. Axis: operability. Built the criterion check that
enforces round-35 routed defect 3 ("C1 target slack": a bullet could be skipped and the
target still met) as a pre-build criterion on round-36's own ablation receipts.

## What I built

`ablation_floor_check.py` (141 lines, sha256 `8f9d87d15f8e4851da80a386b9ed9efbcf7cccef51bf9a9aef4bbf1187e606c2`).

- Sandbox copy (the run path): `/fast/scratch/hyaku/kake-r36w1/ExecCriterionAblation/ablation_floor_check.py`
- Lane landing path: `.ufo/waves/round-36/criteria/ablation_floor_check.py` (byte-identical, same sha256; the
  lane `criteria/` directory is untracked at this wave, so nothing tracked was touched)

Contract: input is a predicate target `T` and a list of ablation receipts (JSON with `passed`, `met`,
named `ablation-<bullet>_<rule>.json`). Exit 1 when any ablation has `met` true, or `passed >= T`, or
when a required bullet letter has no ablation receipt; one printed line per failure; exit 0 otherwise.
Exit 2 on a usage/read error. Files that are not ablation receipts by name (e.g.
`reference-private.json`, the tool itself) are skipped and named on stderr, so the reference receipt
cannot be miscounted as an ablation. `--bullets` defaults to `a,b,c,d,e,f,g` (the seven round-36 C1
contract bullets).

## Run 1 — round-35 shape, must fail (exit 1)

Receipts built from `.ufo/waves/round-35/w2/ExecPartialRepairs.md` (base 14/24; repairs (a) +3,
(b) +5, (c) +2; target 22/24). Kept in `/fast/scratch/hyaku/kake-r36w1/ExecCriterionAblation/r35-receipts/`:
`ablation-a_skip.json` (skip (a): 21 of 24, met false), `ablation-b_skip.json` (skip (b): 19 of 24,
met false), `ablation-c_skip.json` (skip (c): 22 of 24, met true — the routed defect), plus
`reference-full.json` (the full tool, 24 of 24, met true, not an ablation).

Command and output:

```
$ cd /fast/scratch/hyaku/kake-r36w1/ExecCriterionAblation && export TMPDIR=$PWD/tmp && \
  python3 -B ablation_floor_check.py --target 22 --bullets a,b,c --receipts r35-receipts
note: not an ablation receipt, skipped: reference-full.json (met=true, passed=24)
FAIL: ablation ablation-c_skip.json met the target (met=true, passed=22 of 24)
FAIL: ablation ablation-c_skip.json reaches the target (passed=22 of 24 >= 22)
FAIL: 2 failure(s), 3 ablation receipts scored
EXIT=1
```

## Run 2 — round-36 receipts, must pass (exit 0)

```
$ cd /fast/scratch/hyaku/kake-r36w1/ExecCriterionAblation && export TMPDIR=$PWD/tmp && \
  python3 -B ablation_floor_check.py --target 25 --receipts \
  /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-36/verification/ablations/
note: not an ablation receipt, skipped: reference-private.json (met=true, passed=28)
PASS: 36 ablation receipts scored, all below target 25, bullets abcdefg each covered
EXIT=0
```

## The check is able to fail (two more measured rejections)

- Missing bullet: receipts with every `ablation-[a-f]_*.json` plus `ablation-s_*.json` and no
  `ablation-g_*.json` → `FAIL: no ablation receipt for bullet (g)` / `FAIL: 1 failure(s), 31 ablation
  receipts scored` / EXIT=1.
- Injected target-reaching ablation: round-36 receipts plus a synthetic
  `ablation-c_shortcut.json` (passed 25 of 28, met true) → `FAIL: ablation ablation-c_shortcut.json met
  the target (met=true, passed=25 of 28)` and `... reaches the target (passed=25 of 28 >= 25)` / EXIT=1.
- Wrong target: `--target 24` on the same round-36 directory → 25 failures, EXIT=1 (every ablation that
  scored 24 of 28 is caught), which is the check discriminating a target that is one case too loose.
- Single-file input (`--receipts <one ablation-a_204ok.json>`, `--bullets a`) → PASS, EXIT=0.

## Evidence pointers

- Deliverable: `.ufo/waves/round-36/criteria/ablation_floor_check.py:1` (sha256 above).
- Round-35 receipt inputs: `.ufo/waves/round-35/w2/ExecPartialRepairs.md` (base 14/24, moves +3/+5/+2,
  disjoint, 14+10 = 24) and `.ufo/waves/round-35/w2/ExecPartialRepairs.md` "Results" section.
- Routed defect quoted: `corpus/lessons/round-35-verifier-spotcheck.md:194` — "C1 target slack. 22/24 is
  reachable with bullet (c) skipped".
- Round-36 receipts read (read-only): `.ufo/waves/round-36/verification/ablations/` — 36 ablation
  receipts, `passed` 13..24, all `met` false, `target` 25; plus `reference-private.json` (28/28, met
  true), which the check skips by name.
- Round-36 predicate target 25 of 28: `SCORECARD.md` section "Round 36 — declared claims"
  (`git show cd3212796cab7a2afa03b638dbfafe7194df9629:SCORECARD.md`).

## Limits and risks

- The check reads receipts; it does not re-run the sealed counter and cannot re-measure the round-36
  ablations. It trusts the `passed`/`met` fields of the receipts it is given.
- The round-35 numbers above are reconstructed from the round-35 seat report's stated base and moves,
  not re-measured here (the round-35 counter would need the round-35 key revision, which is out of my
  seat's scope). The receipts are a shape fixture, not a fresh measurement.
- Naming is the only separator between an ablation receipt and the reference receipt. A receipt whose
  file name stops matching `ablation-<bullet>_<rule>.json` is silently skipped (named on stderr); if the
  L1 renames receipts, this check must be told the new convention.
- `--bullets` defaults to the seven round-36 C1 bullets; a future contract with different bullet letters
  needs the flag.
- No LSP interface is exposed in the available toolset, so no LSP operation was available. No tool was
  installed or updated. No blocker. No process left running; no file in the fleet repo
  `/home/vgpnk/Projects/shokunin` was mutated, and no git/jj write command was run in the lane.
