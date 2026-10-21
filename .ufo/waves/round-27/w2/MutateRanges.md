# MutateRanges — endpoint-only range expansion

- Axes: **operability** attacked; **freshness** guarded only by frozen-byte preservation, not source-support adjudication.
- Candidate/base observed: `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`; branch observed: `kake-r27-w2mut1`.
- Sole source mutation: `/fast/scratch/hyaku/kake-r27/w2-mut1/scripts/citing_set.py:469`.
- Verdict: **KILLED** by the existing real fixture runner, negative and positive fixture observations, and exact frozen-pair comparison. Pristine control passed; restoration passed.

## Mutant and predeclared expectations

```python
# pristine / restored
            for value in range(start, end + 1):
# mutant: preserve endpoint/literal handling; drop only range interiors
            for value in (start, end):
```

- Pristine/restored source SHA-256: `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228`.
- Mutant source SHA-256: `42e68d2b40fb2c86212834b32a3877e6747d9eb9d5b7801d2cc6b5b79d8aa046`.
- Before the first behavioral run, `/fast/scratch/hyaku/kake-r27/MutateRanges/declaration.json` fixed expectations for all three phases: real selftest exit0/29 cases/0 failures; negative03 exit1 with four `unadjudicated_citing_pair` findings S002–S005; positive20 exit0/no findings; original frozen28 exit1 with exactly the original 16 expected pairs and no extras.
- Mutant prediction declared separately: negative03 wrongly exits0, positive20 emits `ledger_pair_not_cited` for S002/S005/S006, and frozen16 detection decreases. Fixed expected outputs were never rewritten.
- Required authority read: contract, oracle-implementation-corrections, complete pairs, frozen-candidate. Initial Git reads used the full candidate hash.
- Before behavioral execution, candidate bindings were checked: 151 files matched candidate bytes, comprising 118 fixture files, 29 frozen files (28 inputs plus expected.json), gate, runner, C2 oracle and counter. Initial source SHA-256 values also matched the frozen manifest. `pins.json` preserves every SHA-256. Each phase checked all 150 nonmutated pinned files before and after execution.

## Commands actually exercised

All commands used cwd `/fast/scratch/hyaku/kake-r27/w2-mut1`. Same bounded detector and expectations, phase name/output directory only changed:

```sh
env TMPDIR=/fast/scratch/hyaku/kake-r27/MutateRanges/tmp TMP=/fast/scratch/hyaku/kake-r27/MutateRanges/tmp TEMP=/fast/scratch/hyaku/kake-r27/MutateRanges/tmp PYTHONDONTWRITEBYTECODE=1 python3 -B /fast/scratch/hyaku/kake-r27/MutateRanges/probe.py pristine
env TMPDIR=/fast/scratch/hyaku/kake-r27/MutateRanges/tmp TMP=/fast/scratch/hyaku/kake-r27/MutateRanges/tmp TEMP=/fast/scratch/hyaku/kake-r27/MutateRanges/tmp PYTHONDONTWRITEBYTECODE=1 python3 -B /fast/scratch/hyaku/kake-r27/MutateRanges/probe.py mutant
env TMPDIR=/fast/scratch/hyaku/kake-r27/MutateRanges/tmp TMP=/fast/scratch/hyaku/kake-r27/MutateRanges/tmp TEMP=/fast/scratch/hyaku/kake-r27/MutateRanges/tmp PYTHONDONTWRITEBYTECODE=1 python3 -B /fast/scratch/hyaku/kake-r27/MutateRanges/probe.py restored
```

Actual child commands, repeated identically in each phase (the real runner additionally invokes the real gate for all 29 unchanged fixtures):

```sh
/usr/bin/python3 -B /fast/scratch/hyaku/kake-r27/w2-mut1/scripts/citing_set_selftest.py --root /fast/scratch/hyaku/kake-r27/w2-mut1 --gate /fast/scratch/hyaku/kake-r27/w2-mut1/scripts/citing_set.py --tmpdir /fast/scratch/hyaku/kake-r27/MutateRanges/tmp --timeout 5 --min-cases 29 --json
/usr/bin/python3 -B /fast/scratch/hyaku/kake-r27/w2-mut1/scripts/citing_set.py --root /fast/scratch/hyaku/kake-r27/w2-mut1/scripts/fixtures/citing-set/03-en-dash-group-range-interior-omission --population population.json --ledger ledger.json --json
/usr/bin/python3 -B /fast/scratch/hyaku/kake-r27/w2-mut1/scripts/citing_set.py --root /fast/scratch/hyaku/kake-r27/w2-mut1/scripts/fixtures/citing-set/20-range-with-population-gap --population population.json --ledger ledger.json --json
/usr/bin/python3 -B /fast/scratch/hyaku/kake-r27/w2-mut1/scripts/citing_set.py --root /fast/scratch/hyaku/kake-r27/w2-mut1/.ufo/waves/round-27/frozen --population population.json --ledger ledger.json --json
```

No synthetic acceptance input, stub, mock echo, new runtime, build, lint or formatter. Child command deadline30s; runner deadline5s per case. No timeout occurred.

## Observed output / exit

| Actual command | Pristine | Mutant | Restored |
|---|---|---|---|
| Identical detector | exit0; fixed expectations matched | exit1; fixed expectations mismatched | exit0; fixed expectations matched |
| Real selftest stdout summary | `{"verdict":"clean","cases":29,"failed":0,"passed":true}`; exit0 | `{"verdict":"failed","cases":29,"failed":11,"passed":false}`; exit1 | Same pristine summary; exit0 |
| Negative03 gate | exit1, citingPairs6, ledgerPairs2; four missing pairs S002/S003/S004/S005 | **exit0, verdict clean, citingPairs2, ledgerPairs2, findings[]**: four interiors disappear | Exact pristine stdout; exit1 |
| Positive20 gate | exit0, citingPairs5, findings[] | **exit1**, citingPairs2; `ledger_pair_not_cited` for S002/S005/S006 | Exact pristine stdout; exit0 |
| Frozen28 gate + original pair oracle | exit1, citingPairs57; **16/16**, falsePositive0 | exit1, citingPairs47; **6/16**, falsePositive0, ten expected pairs absent | Exact pristine stdout; exit1, **16/16**, falsePositive0 |

- Selftest mutant failures: cases **03,04,05,06,07,19,20,23,24,25,27**; the other18 matched. This is one killed mutant, not18 surviving mutants.
- Frozen mutant retained only S001/static-canonical-preflight, S006/static-canonical-preflight, and S008/crawl-scope-per-host, ghp-custom-domain, ghp-etag-anatomy, static-canonical-preflight. All six findings were `unadjudicated_citing_pair`.
- Important detector distinction: frozen gate exit1 stayed red despite losing ten omissions; an exit-only detector would miss this. The unchanged exact pair oracle and fixture finding multisets killed it.
- All observed child stderr streams were empty, SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## Evidence hashes and restoration

Evidence root: `/fast/scratch/hyaku/kake-r27/MutateRanges/`; each phase contains `results.json`, full `selftest/negative03/positive20/frozen28.stdout.json`, and corresponding stderr files. `results.json` records exact argv, exit, full stdout, parsed findings and each stream SHA-256.

| Evidence | SHA-256 |
|---|---|
| probe.py | `edbc1188c91f34002bb911a52e86f47045059bb1b796c93bd470931872236bba` |
| declaration.json | `3da29dc5c1880a2e17f7617460903a0493c70a0899ab331bdfe75b7df2ae23c7` |
| pins.json | `c0fd2eff8a258634abf8bbd8b1846f3ab48ae9b51210fcca792574ac0d57e8b5` |
| pristine/results.json | `bac1331ed8dee6864bc257699f8a24f8f7873f82c6c080401b061f0c51812895` |
| mutant/results.json | `b2003d2d6c04ccfa6e37e275182b34412fede65c9cb3f5d9c39352c6d129e733` |
| restored/results.json | `c0f6e21337e0a23db31d135abe99e96dc31c1c1d3f6bb8a8a3c2f84f05f98543` |
| pristine AND restored/selftest.stdout.json | `bd8d54534ff34e077ba9c925bfd60d617fe4c5f1b003b1320e1f8ecb9e6b6fde` |
| mutant/selftest.stdout.json | `7e9f587ddb20f9cf9bc599a009aecd377eb796797954667b05dcd8446684de95` |

The single-line edit was reversed immediately after the mutant detector; the identical restored detector then passed29/29 and original16/16. A final direct byte comparison against `git show ac46a7472d945a6d7ff135e4d7f07b0b6913d835:scripts/citing_set.py` is recorded in `restoration.json`: **exactByteEqualityToCandidate=true**; restored hash equals pristine. Source and150 pinned nonmutated files were unchanged during every detector.

Scope limits: direct gate over real frozen inputs was used rather than revision-selecting `c2_count.py`, which would read immutable candidate gate bytes and bypass this working-file mutation. This probe establishes only this mutation's detectability, not global correctness, source semantics, HTTP authenticity or C1 admission; C1's existing UNPROVABLE disposition is untouched. No live source/docs/registry, sibling, Git index, commit, remote or routing changes. No tool installations/updates. No network or stopped-r24 execution. Only this report was written in the live repository.
