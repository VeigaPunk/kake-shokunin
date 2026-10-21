# MutateC1 — one-fault negative control

- Axes: **operability**, preserving **freshness** truthfulness.
- Candidate: `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`.
- Isolated source seat: `/fast/scratch/hyaku/kake-r27/w2-mut3`; branch ref `refs/heads/kake-r27-w2mut3` resolved to that exact candidate before the probe.
- Read contract, oracle corrections, pairs, frozen-candidate and carry-errata authority. Original57 floor, current58 obligations and expected16 C2 target were not rewritten.
- Attacked item: C1 contract10/13, **UNVERIFIABLE must never count decided**. Selected the task's expressly offered uncertainty-erasure negative control, not an additional monotonicity/group-kind mutant.

## Independently declared detector

Before running anything, wrote `/fast/scratch/hyaku/kake-r27/MutateC1/expectations.json`:
- Real current consumer: exit1; citing58, reviewed58, decided55; seven known unknown units across three pairs; three `carried_unverifiable` findings.
- Existing real disposable-clone C1 oracle: pristine/restored exit0, 14 cases, zero failures; mutant must fail `current_consumer_unverifiable_not_green` and exit1.
- A pristine failure would be inconclusive, never a killed mutant. Expectations remained unchanged throughout.

## Mutant and source hashes

Only source edit: insert `unknown.clear()` immediately after the carry-errata merge, before `decided=reviewed-set(unknown)` (original line59). One behavior-bearing insertion; the errata digest/authority checks still execute.

| Bytes | SHA-256 |
|---|---|
| Candidate Git blob and pristine worktree | `8d4c22efa884468daead75aa4b9d6143d38986a83c3069747d146ee0daf942a5` |
| Mutant | `2dc90f468f1e58b580e74071b20846ee22c706ca89bd8aaa7236afbbbf13653f` |
| Restored worktree | `8d4c22efa884468daead75aa4b9d6143d38986a83c3069747d146ee0daf942a5` |

Candidate blob checked with `git show ac46a7472d945a6d7ff135e4d7f07b0b6913d835:.ufo/waves/round-27/count_c1.py | sha256sum`; worktree matched before source inspection.
Oracle SHA stayed `943db49c69dd908d0d56678dd4c9af231d00850a1aea092f90b441caafe3e460` in all three stages.
Carry-errata SHA stayed `236d9e79b665ae997a7f8ae9a31c2d187979a7abcac0d15e60a28c51ef9d17e5` in all three stages.

## Actual commands and outputs

Working directory: `/fast/scratch/hyaku/kake-r27/w2-mut3`; `TMPDIR=/fast/scratch/hyaku/kake-r27/MutateC1`; Python bytecode writes disabled.
Commands, in order: `python3 -B /fast/scratch/hyaku/kake-r27/MutateC1/run_probe.py pristine`, then `mutant`, then `restored` as the final argument. Each collector exited0; that exit only means outputs were collected, not that the mutant passed.
Each invocation ran these same real consumers:
1. `/usr/bin/python3 -B .ufo/waves/round-27/count_c1.py --root . --revision ac46a7472d945a6d7ff135e4d7f07b0b6913d835`.
2. `/usr/bin/python3 -B /fast/scratch/hyaku/kake-r27/MutateC1/run_oracle.py`, executing the unchanged `oracle_selftest.py --kind c1 --source-root /fast/scratch/hyaku/kake-r27/w2-mut3` via `runpy`.
The launcher changes only `tempfile.TemporaryDirectory`'s directory to this seat because the original oracle hardcodes the parent scratch directory; no assertion, expected output, fixture operation or counter invocation changed.

| Stage | Consumer exit / actual stdout fields | Oracle exit / actual stdout fields |
|---|---|---|
| Pristine | 1; citing58, reviewed58, decided55, unknownUnits7, unknownPairs3 | 0; cases14, failed0 |
| Mutant | **0; citing58, reviewed58, decided58, unknownUnits0, unknownPairs0, findings[], missing[]** | **1; cases14, failed8** |
| Restored | 1; citing58, reviewed58, decided55, unknownUnits7, unknownPairs3 | 0; cases14, failed0 |

Pristine/restored findings were exactly `carried_unverifiable`: S001/ghp-served-set (3 units), S007/ghp-custom-domain (1), S033/static-canonical-preflight (3). All six consumer/oracle stderr streams were empty.

Actual failing mutant cases (all passed pristine and restored):
- `current_consumer_unverifiable_not_green`: exit0 instead of1; 58 decided instead of55, seven uncertainties erased.
- `discovered_obligation_cannot_shrink`: real clone rewrote discovered-pairs to `[]`; exit0 instead of1, 58 decided instead of55. This input-boundary probe independently rejected the same mutant.
- `baseline_missing_range_and_carried_unknowns`: exit1 as expected, but decided41 instead of38, missing16 instead of19.
- `independent_artifact_review`: exit1 as expected, but decided42 instead of39; carried findings absent.
- `deleted_citation_cannot_shrink_floor`: real clone removed the S001-S007 range; exit1, floor57 retained, but decided41 instead of38.
- `retained_source_review`: exit1, decided42 instead of39; carried findings absent.
- `stale_with_real_correction`: exit1, decided42 instead of39; carried findings absent.
- `unverifiable_override_loses_carried_credit`: exit1, decided40 instead of37; only the newly introduced `unverifiable_pair` remained.
The six other original cases retained their assertions, including artifact-self-support/group-source rejection and inherited-ledger tamper exit2. No tests were changed or added after observing the mutant.

## Output hashes and retained evidence

| Output | Pristine SHA-256 | Mutant SHA-256 | Restored SHA-256 |
|---|---|---|---|
| Consumer stdout | `6e053d9aa3626499157265b0ce9e3ad5871e2cc8d9c6de606e4dfa0a7737e72c` | `e75275e218981cf50ed069febdb7984bfdc8177275bd24add3ebf3291f7158f5` | `6e053d9aa3626499157265b0ce9e3ad5871e2cc8d9c6de606e4dfa0a7737e72c` |
| Oracle stdout | `cb531516fbb1db58d812f35d2d2948a797453e481b827f2b314299c227450953` | `4dc0ff7e1fbc364a3728b90170cbba3acecbe3ace8536507940e5d68fdcd3a2c` | `22b8af2b26474244270ab12d4297270d4d5b6957110ecc05dc6f7cb6184f3c50` |

Full actual JSON stdout, empty stderr, commands, source hashes and case results: `/fast/scratch/hyaku/kake-r27/MutateC1/{pristine,mutant,restored}.{consumer,oracle}.stdout.json`, corresponding `.stderr.txt`, and `{pristine,mutant,restored}.summary.json`. Oracle stdout is not claimed byte-identical across disposable-clone runs.

## Verdict and restoration

**KILLED**: unchanged real oracle passed before/after and failed the one-fault mutant; actual frozen consumer data demonstrated the prohibited false-green result. This is mutation-detector evidence, not round admission or proof of source semantics/HTTP authenticity.
Removed exactly the inserted line; restored SHA and identical frozen-consumer stdout establish exact-byte restoration and original behavior. C1 remains **UNPROVABLE, 55/58 strictly decided**, despite58 reviewed; no green claim or denominator substitution.
No source-worktree commit/index/branch/remote operations; the unchanged oracle's own fixture-local add/commit/checkout operations occurred only inside its temporary disposable clones. No live lane source, registry, historical report, frozen input or sibling edits; no network, r24 replay, build/lint/formatter or tool installation.
