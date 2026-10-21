# MutateConstant — r27 fresh falsification

- Axes: **operability attacked**; freshness held unchanged. This is an author-side negative mutation probe, not admission or a second judge.
- Frozen candidate: `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`.
- Observed isolated worktree: `/fast/scratch/hyaku/kake-r27/w2-mut2`, branch `kake-r27-w2mut2`, base exactly the candidate (`git worktree list --porcelain`).
- Sole source mutation: `scripts/citing_set.py`, one unconditional early return immediately after `evaluate()`'s docstring; 21 inserted lines returning failed/57 citingPairs/41 ledgerPairs and the literal original 16 `unadjudicated_citing_pair` pairs. It ignored all actual population/ledger/corpus inputs. No conditional fixture special-casing.
- Pristine SHA-256: `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228` (24,856 bytes), identical to the explicit candidate Git blob before any source read.
- Mutant SHA-256: `a1c564f8619a0760321c36ec00a64343bfd57b75746aa916587df36cdd78395c` (26,691 bytes).
- Restored SHA-256: `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228` (24,856 bytes); exact byte comparison against the candidate blob returned true before and after the restored run.

## Independent expectations fixed before the pristine run

`/fast/scratch/hyaku/kake-r27/MutateConstant/expectations.json` SHA-256 `4cb4bc2a1e6fa6b141f2d84ece7fbd1d1fb43f57ac65dde9345aa4580cd8dd52` was unchanged across all three stages.

1. Actual gate on unchanged frozen inputs: exit1, exactly the original 16 missing pairs, no extra findings. Predict the constant mutant **survives this finite predicate**, never acceptance.
2. Actual gate on original clean fixture01: exit0, zero findings. Predict the mutant fails by exit1 plus16 findings.
3. Actual gate on original missing fixture02: exit1, one missing finding. Predict the mutant fails by16 findings even though its exit remains1.
4. Unchanged real selftest on all original fixtures: exit0, 29 cases, failed0. Predict mutant nonzero with real fixture mismatches.

A pristine failure would be inconclusive. No expectations, fixtures, frozen inputs, source contracts, or detector commands were changed after observing a result.

## Actual commands and retained outputs

Command abbreviations below expand to these fixed absolute paths; every executed argv, stdout, stderr and exit is retained in each stage's `results.json`.

```sh
W=/fast/scratch/hyaku/kake-r27/w2-mut2
S=/fast/scratch/hyaku/kake-r27/MutateConstant
G=$W/scripts/citing_set.py
F=$W/scripts/fixtures/citing-set
# Four real consumer commands, launched concurrently within each detector run:
/usr/bin/python3 -B "$G" --root "$W/.ufo/waves/round-27/frozen" --population population.json --ledger ledger.json --json
/usr/bin/python3 -B "$G" --root "$F/01-single-literal-clean" --population population.json --ledger ledger.json --json
/usr/bin/python3 -B "$G" --root "$F/02-single-literal-missing" --population population.json --ledger ledger.json --json
/usr/bin/python3 -B "$W/scripts/citing_set_selftest.py" --root "$W" --gate "$G" --tmpdir "$S/tmp" --timeout 10 --min-cases 12 --json
# Actual detector invocations, sequential around the one transient mutation:
env TMPDIR=$S/tmp TMP=$S/tmp TEMP=$S/tmp PYTHONDONTWRITEBYTECODE=1 python3 -B "$S/probe.py" pristine
env TMPDIR=$S/tmp TMP=$S/tmp TEMP=$S/tmp PYTHONDONTWRITEBYTECODE=1 python3 -B "$S/probe.py" mutated
env TMPDIR=$S/tmp TMP=$S/tmp TEMP=$S/tmp PYTHONDONTWRITEBYTECODE=1 python3 -B "$S/probe.py" restored
```

Detector exit codes were **0 → 1 → 0**. All consumer stderr streams were empty; no timeout occurred.

| Actual consumer stdout/exit summary | Pristine | Mutated | Restored |
|---|---|---|---|
| Frozen direct CLI | exit1;16/16 exact pairs;0 false positives | exit1;16/16 exact pairs;0 false positives | exit1;16/16 exact pairs;0 false positives |
| Clean fixture01 CLI | exit0;0 findings | exit1;16 missing findings | exit0;0 findings |
| Missing fixture02 CLI | exit1;1 missing finding | exit1;16 missing findings | exit1;1 missing finding |
| Real selftest | exit0;cases29;failed0;passed true | exit1;cases29;failed29;passed false | exit0;cases29;failed0;passed true |

Stable kill: selftest fixture `01-single-literal-clean`: `exit mismatch: expected 0, observed 1`. Fixture02 independently reports `finding-id mismatch`: expected one `unadjudicated_citing_pair`, observed16. Its real pristine finding is S001/`corpus/knowledge/publish-queue.md`; the constant mutant instead starts with S001/`corpus/knowledge/static-canonical-preflight.md`.

All three mutated direct CLI stdout byte streams were identical: SHA-256 `6ecbc3e05f071e103319c0196c8072dd3b5412f0fb83c227b01d9428de055307`.
Pristine/restored stdout hashes were identical per command: finite `5216c7d8aaa7c17995d4d2b503b892b67bb796a7ca8f096ebcba065655906643`; clean `7a28cbd43c950d69463397657db8b464919f6f7c71ac2c18a186db82cbd0ffc3`; missing `3fd0282846dddb4746c0f312d23fe48d653f0c3557a6c51567d284c87044f3a3`; selftest `a34d22d5dbe67a1854b5b4715a087a2fe929a72e9a59451406abb7539d6e9bf7`.
Mutated selftest stdout SHA-256: `0fe8baa40c42b14cd62d790b5243bd74e730ed1213797d895ac990f9cf2a6f38`.

## Verdict, limits and restoration

**KILLED by the unchanged real-input CLI/selftest detector; SURVIVED the finite frozen-C2 output predicate alone.** This is coverage evidence for this one defect, not proof of general correctness or source support.

The finite check ran the actual edited gate against real frozen inputs and compared the original `c2-oracle.json` using the existing `c2_count.py` exit/pair-set/total-findings predicate. It did **not** invoke `c2_count.py --revision`: that command extracts the immutable committed gate, not this worktree mutation, and explicitly allocates outside this seat's scratch. Consequently this report does not claim a mutated-counter execution. The real selftest runner was invoked directly so its `--tmpdir` stayed inside this seat; it actually launched the gate for every original fixture, with no stub/mock gate. `oracle_selftest.py` was not run because it creates commits in clones.

The detector compared150 non-mutated input/runner/oracle files against explicit candidate blobs before and after every stage, including all28 frozen inputs. All matched; source bytes were stable during each run. The original oracle expected16 and all fixture expectations remained unchanged. Freshness/C1 was not adjudicated or made green; the frozen strict55/58 status is not overturned.

Restoration removed precisely the21 inserted lines, then ran the identical detector on exact candidate bytes. No live measured source, sibling source, docs/registry, index, commits, remotes or fleet state were edited. No r24 replay, network/provider operation, build/lint/formatter, tool install/update, or other runtime occurred.

Evidence root: `/fast/scratch/hyaku/kake-r27/MutateConstant/`; each `{pristine,mutated,restored}/` contains complete per-command `*.stdout.json`, `*.stderr.txt`, and `results.json`.
- Detector `probe.py` SHA-256: `292f42a22745d11af94e19b36cf43374c212ca27c4e6471078dc4cb5da3e1d09`.
- Pristine `results.json` SHA-256: `275a22c71dd039ce943468223f7bf9f8c4ce6b92f1d4254a2e664de35d4c281c`.
- Mutated `results.json` SHA-256: `3e05b06b36103b732b745ae0bc844a1231f59953d0b6899ed1e3fb65ccd3f839`.
- Restored `results.json` SHA-256: `dec25850ae381eb4c5fac1e1e2f6fc0435e076b6c2e7b595d46c332eb5a8c108`.
