# MutCounterV2 — dummy-key counter mutation probe
Axes: oracle soundness, rawTemplate freshness, isolation, refusal behavior. No sealed tree access, real-key search, or execution of the fleet counter; no round verdict.
Source/copy SHA-256: `52daff55a2b897ba814eed134cd6bfe0de28305bf4ab82e87a5c6d1ae7096e7b`; source unchanged after campaign. Original copy: `/fast/scratch/hyaku/kake-r38ctl/MutCounterV2/counter.source.py`.
Test-only adaptation: own KEY_SHA256; CASES=6, TARGET=6, dummy predicate, TIMEOUT=1 s (same actual subprocess timeout path, not a claim about the production 20 s bound). Logic otherwise pristine.
Dummy key: `/fast/scratch/hyaku/kake-r38ctl/MutCounterV2/dummy-key.json` SHA-256 `fb25c7ec9b3ed6f2e99c55574d1531e49a6fd4f357f2ed3ad57b2a8a7c037ed8`. Six cases/seven runs: raw IDs/files, NaN, invalid numeric status, ordinary mapping, timeout, later-run conjunction; named robots files contain actual rules.
Configured counter: `/fast/scratch/hyaku/kake-r38ctl/MutCounterV2/counter.dummy.py` SHA-256 `5739ea366a59324bab61aa503a7633f4f7cae0c2591d2f6daed3ba2ca541bc71`.
Runner: `/fast/scratch/hyaku/kake-r38ctl/MutCounterV2/mutation_probe.py` SHA-256 `91cb218a527539d4826c6fb6a95466dae242f6f18e65b7f082da32905bbc4e58`.
Reproducer: `/fast/scratch/hyaku/kake-r38ctl/MutCounterV2/reproduce_id_alias.py` SHA-256 `0789c9ed09ec8b87e68e3abd268197f95270bb8617f01c56448c4bd18cf79398`.

## Actual counter defects
F1: Fixed original IDs are accepted despite freshening. The fixed-ID tool emits literal `@ID:x@`, `@ID:z@`, `@ID:later@` and `legacy`, not the manifest's generated IDs; pristine dummy counter scores it **6/6, met=true, exit 0**. A minimally reproduced generated ID was `c02749f17785d`; both that ID and literal `@ID:x@` were accepted, while an unrelated ID was rejected. File `2e819d9c0dc443269077125d4bbbb390` existed: materialization itself worked.
Cause: `project()` preserves unknown observed IDs through `idmap.get(check, check)`; `judge()` compares those unchanged IDs with canonical expected tokens. Therefore original key IDs remain accepted aliases. No production fix made and no real sealed score inferred.
F2: Missing `--tool-file` gives exit 1 with FileNotFoundError traceback and **no JSON receipt**, rather than a zero score. Revision-mode absent tool correctly scores 0/6. Both baseline failures are inconclusive tests, never counted as mutant kills.

## Commands and outputs
`timeout --signal=TERM --kill-after=2s 60s /usr/bin/python3 -B /fast/scratch/hyaku/kake-r38ctl/MutCounterV2/mutation_probe.py setup` → exit 0; 10 bounded sandbox git commands all exit 0, Git environment overrides unset.
`timeout --signal=TERM --kill-after=2s 540s /usr/bin/python3 -B /fast/scratch/hyaku/kake-r38ctl/MutCounterV2/mutation_probe.py campaign` → exit 0, 81.20 s; 10 killed, exact restoration true. Campaign exit 0 means collection completed, not that every assertion passed.
`timeout --signal=TERM --kill-after=2s 10s /usr/bin/python3 -B /fast/scratch/hyaku/kake-r38ctl/MutCounterV2/reproduce_id_alias.py` → exit 0; fresh=true, fixed-original-token accepted=true, unrelated accepted=false. Output recorded in `/fast/scratch/hyaku/kake-r38ctl/MutCounterV2/reproduce_id_alias.output.json`.
All detector invocations use `timeout --signal=TERM --kill-after=2s 30s /usr/bin/python3 -B <sandbox-counter> --root <sandbox-fixture-repo> <args>`; exact argv/stdout/stderr/exits are in `/fast/scratch/hyaku/kake-r38ctl/MutCounterV2/results/<variant>/detector.json`, variants `pristine`, `M01-mutated`…`M10-mutated`, `M01-restored`…`M10-restored`.
| Pristine detector | Actual output / exit | Assertion |
|---|---|---|
| T_good / T_raw_shape / T_jail | 6/6, met=true / 0 each | pass: findings map back, file references readable, generated ID/file shapes, sentinel hidden |
| T_fixed_ids | 6/6, met=true / 0 | FAIL: fixed original IDs should fail |
| T_findings / T_duplicates | 1/6, met=false / 1 each | pass: wrong reasons and duplicate findings rejected |
| T_visible | key visible at measured revision / 2 | pass |
| T_sha | computed key digest != pin / 2 | pass |
| T_missing | toolPresent=false, 0/6, met=false / 1 | pass |
| T_timeout | 5/6, only raw_timeout fails, 1.198531 s / 1 | pass |
| T_key_revision | 6/6, met=true / 0 | pass: pre-key measured revision with separate dummy key revision |
| T_later_run | 5/6, only later_run fails / 1 | pass |
| T_missing_file | no stdout, FileNotFoundError / 1 | FAIL: no zero-score JSON |

## Mutants (detected yes = killed by a baseline-passing test that passes again after exact restoration)
| Mutant / smallest changed behavior | Detected | Detector | Absolute mutant snapshot path | SHA-256 |
|---|---|---|---|---|
| M01 raw IDs left fixed | yes | T_raw_shape | /fast/scratch/hyaku/kake-r38ctl/MutCounterV2/mutants/M01/mutated.py | 00672e34315d88035f43cd2684cdeceb45de914a8ad54dd27627fc1fe268a54a |
| M02 file substitution omitted | yes | T_good | /fast/scratch/hyaku/kake-r38ctl/MutCounterV2/mutants/M02/mutated.py | c904a1b81207420ae3d380df17601e1eb6c4c8f602173ef291875a42872703c5 |
| M03 inverse ID mapping omitted | yes | T_good | /fast/scratch/hyaku/kake-r38ctl/MutCounterV2/mutants/M03/mutated.py | ae636fa36830c82f90375deeb68066c9155bdac9c4e527f29f8c3e114383ab11 |
| M04 verdict-only comparison | yes | T_findings | /fast/scratch/hyaku/kake-r38ctl/MutCounterV2/mutants/M04/mutated.py | 398cc88f5813845da4a165bfa3fd9c3dbf73825dbc356af7ac2e363b6e589112 |
| M05 jail removed | yes | T_jail | /fast/scratch/hyaku/kake-r38ctl/MutCounterV2/mutants/M05/mutated.py | ba4d3aa72149c220d3fddf0ea10f3d21c070a16cca11c2514bc6b9a8b046592a |
| M06 key-visibility refusal disabled | yes | T_visible | /fast/scratch/hyaku/kake-r38ctl/MutCounterV2/mutants/M06/mutated.py | d4069bf5e460c1d2f2355467bf666a735e136573eef06870c52437c0e9af625a |
| M07 digest check disabled | yes | T_sha | /fast/scratch/hyaku/kake-r38ctl/MutCounterV2/mutants/M07/mutated.py | cac7059e8a9152847ce670e833f0558f778f2a37a0af92eba378c27b24656f36 |
| M08 pass threshold omitted | yes | T_missing | /fast/scratch/hyaku/kake-r38ctl/MutCounterV2/mutants/M08/mutated.py | 451a2a14b6cdfcd42cd4a3d1f9637358e281f1021c9c52259ecd4d2c7e51b712 |
| M09 timeout accepted | yes | T_timeout | /fast/scratch/hyaku/kake-r38ctl/MutCounterV2/mutants/M09/mutated.py | 98e323e5fa7facd1ec8596845706ff59a6cd8718d76960f58890ce6525b91f62 |
| M10 findings collapsed to a set | yes | T_duplicates | /fast/scratch/hyaku/kake-r38ctl/MutCounterV2/mutants/M10/mutated.py | a8a4ca3ecb7afbb1869d03e70ad05c6756aa739a0f38e81034cec7fa0bd7576c |
Restoration: every working `mutants/Mxx/counter.py` before/after SHA-256 equals configured counter `5739ea366a59324bab61aa503a7633f4f7cae0c2591d2f6daed3ba2ca541bc71`; mutated snapshots retained separately. Same 13-test detector ran pristine, mutated and restored. Full before/mutated/after hashes, all kill tests and inconclusive tests: `/fast/scratch/hyaku/kake-r38ctl/MutCounterV2/campaign.json` and `results/Mxx/restoration.json`.

## Self-contained stdlib fixture tools (`--manifest PATH`, one JSON report)
These are synthetic instruments, not proposed complete robots implementations; real sealed scores unclaimed. Dummy scores and rationale are above.
- `/fast/scratch/hyaku/kake-r38ctl/MutCounterV2/tool-good.py` SHA-256 `e2db06b1688d78e90e205aa785f36986dcc46bff4b0e1a0c5e2c64b49619f350` — baseline fixture oracle.
- `/fast/scratch/hyaku/kake-r38ctl/MutCounterV2/tool-fixed.py` SHA-256 `153284d8f07e75e8e0a3c01b875ec42ef3ba701a2555ef5fd423744954b2e577` — fixed original IDs.
- `/fast/scratch/hyaku/kake-r38ctl/MutCounterV2/tool-shape.py` SHA-256 `25d20eff3cc25431576a86ad6516fbabb9f2e295874914834df77acfee34ae5e` — fresh ID/file shape assertion.
- `/fast/scratch/hyaku/kake-r38ctl/MutCounterV2/tool-wrong.py` SHA-256 `a1506ed1d269d8b850a2b04b97837b6991c7699d5bfe7db217a7580f0ad137b5` — same verdict/exit, wrong reasons.
- `/fast/scratch/hyaku/kake-r38ctl/MutCounterV2/tool-duplicate.py` SHA-256 `9c0cdd6f0e6976bc747e53db4a9b8a37eec450589e65bf497949d2ba9803fc66` — duplicate findings.
- `/fast/scratch/hyaku/kake-r38ctl/MutCounterV2/tool-sentry.py` SHA-256 `be28babdb387a793f478a8f2cb392cef168fb245e0e7ebb543f7cc2af6df79c8` — reads only its own host-side sentinel if jail absent.
- `/fast/scratch/hyaku/kake-r38ctl/MutCounterV2/tool-slow.py` SHA-256 `a1eed50a70d6d296645f7d98e7ef2751db5c29090ee0dc2f3c82c6cdae3562d5` — sleeps on timeout fixture.
- `/fast/scratch/hyaku/kake-r38ctl/MutCounterV2/tool-late.py` SHA-256 `4e9bd99a36c6abc851f237aedbfc5126a07b36dfe44ea6adcb58f883daeaf7c2` — faults only the second run.
All executions bounded, sequential campaign, process groups reaped in finally; no background processes retained. No installations/updates. Writes limited to assigned sandbox and this report; no lane index/state changes.
