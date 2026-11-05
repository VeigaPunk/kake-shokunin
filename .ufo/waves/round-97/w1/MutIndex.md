# MutIndex — round 97 mutation test of the frozen C1 counter

Full detail: `.ufo/waves/round-97/w1/MutIndex/mut.md`; rows: `w1/MutIndex/mutants.tsv`; diffs: `w1/MutIndex/mutants.diff`;
receipts: `w1/MutIndex/mut-logs.txt`, `probe-results.txt`, `mutants-results.json`, driver and probe scripts.

## Scope

Mutation-tested `c97_index.py` (frozen sha256 `8535150e…` verified before every run) with 14 single-point mutants,
each scored by the frozen rule: killed iff selftest fails or a base/repair line differs from the frozen counter's.

## Results (command: `python3 -B <mutant> --selftest|--root LANE --revision <REV> --work <scratch>`)

- Pristine baseline reproduced: selftest rc=0 `14/14`; base (36d148f5) rc=1 `mismatches=38 met=false`;
  repair (9e27ce0b) rc=0 `mismatches=0 met=true`.
- **killed=9/14.** Killed: M03, M04, M05, M07, M08, M09, M10, M11, M14.
- Survivors: **M01** (no fence skip), **M02** (no comment skip), **M06** (MIN_WORDS 8->1), **M12** (drop
  GIT_NO_REPLACE_OBJECTS pin), **M13** (`"git"` for `/usr/bin/git`).

## Survivor disposition

- M01, M02, M06, M12 are genuine coverage gaps in the frozen selftest/controls. Supplementary scratch probes kill each:
  PR-M01b and PR-M02b (fenced/commented block carrying its own header), PR-M06 (5-word row with two shared long
  words), PR-M12 (`git replace` ref on the README blob). Probes are not part of the frozen verdict.
- M13 is an equivalent mutant under the frozen environment: `git_env()` pins `PATH=/usr/bin:/bin`, and a PATH-shadowed
  wrapper did not fire (`shadow_fired=False`) for either pristine or mutant; output identical.

Routed for the successor counter (not this round; c97 is frozen, no repair made): header-bearing fenced/commented
fixtures, an isolated row-coverage fixture, and a `git replace` fixture.

## Incident and cleanup

My scratch was deleted mid-run by a sibling's `rm -rf` of the round parent (disclosed by ConnectorScope-23). I recreated
it, re-verified the pristine hash, and reran. Tools installed: none. Lane writes: only under `w1/MutIndex/` plus this
report. Scratch tree deleted before yield.

MUT-INDEX killed=9/14 survivors=M01-no-fence-skip,M02-no-comment-skip,M06-min-words-8to1,M12-no-git-no-replace-objects,M13-git-from-path
