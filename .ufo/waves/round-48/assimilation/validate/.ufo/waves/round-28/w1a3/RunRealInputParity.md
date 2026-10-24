# RunRealInputParity — round 28 wave 1a3 (seat: KakeR28a3.RunRealInputParity)

Target: C1 no-harm on real lane inputs. Compare the base gate
(22c1669c1fec83d1a0769de6b9ce686c75657e66:scripts/citing_set.py) with the
repaired gate (b5d423fc02057f67a6f3a255808313ce40d29069:scripts/citing_set.py)
on real population/ledger inputs, in Git mode and working-tree mode, and diff
the JSON outputs and exit codes.

## Environment and setup (no installs needed)

- Scratch: /fast/scratch/hyaku/kake-r28a3/w1/RunRealInputParity/ (TMPDIR set there).
- Clone: `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin .../clone` — exit 0.
  Clone HEAD = b5d423fc02057f67a6f3a255808313ce40d29069 (the repaired revision), so the
  working tree content equals the Git-source content at that revision.
- Gates extracted with `git -C clone show <rev>:scripts/citing_set.py > <file>` — exit 0:
  - base_citing_set.py sha256 3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228
  - repaired_citing_set.py sha256 28ba996524b444b2e1c23e3751f3fa662a9a44adbfcb6337a0d23fcebaf8f415
- `diff -u base repaired` (exit 1, expected): all changes are confined to error-handling
  paths — non-blocking open of population/ledger documents, corpus surface missing/empty/
  symlink/non-directory rejection, GitSource top-level-root and blank-revision checks,
  population_id_unreachable check, JSON RecursionError handling, `--revision is not None`
  switch. Evaluation logic on valid inputs is untouched.

## Runs (all exit 0 for the driver itself)

Driver: python3 -B .../driver.py (records each run, exit code, stderr tail, parsed JSON).

Eight gate runs, each `python3 -B <gate> --root <clone> [--revision b5d423fc02057f67a6f3a255808313ce40d29069] --population <p> --ledger <l>`:

| run | pairing | exit | verdict | citingPairs | ledgerPairs | popRows | corpusFiles | findings | first finding |
|---|---|---|---|---|---|---|---|---|---|
| base | git/r27 | 1 | failed | 58 | 41 | 32 | 26 | 17 | unadjudicated_citing_pair |
| repaired | git/r27 | 1 | failed | 58 | 41 | 32 | 26 | 17 | unadjudicated_citing_pair |
| base | git/r26 | 1 | failed | 58 | 41 | 32 | 26 | 17 | unadjudicated_citing_pair |
| repaired | git/r26 | 1 | failed | 58 | 41 | 32 | 26 | 17 | unadjudicated_citing_pair |
| base | wt/r27 | 1 | failed | 58 | 41 | 32 | 26 | 17 | unadjudicated_citing_pair |
| repaired | wt/r27 | 1 | failed | 58 | 41 | 32 | 26 | 17 | unadjudicated_citing_pair |
| base | wt/r26 | 1 | failed | 58 | 41 | 32 | 26 | 17 | unadjudicated_citing_pair |
| repaired | wt/r26 | 1 | failed | 58 | 41 | 32 | 26 | 17 | unadjudicated_citing_pair |

Stderr empty ("") on all eight runs.

## Comparison results

- Per pairing, `diff -q base-<p>.json repaired-<p>.json` printed nothing (byte-identical) and
  JSON deep-equality `left == right` is true for all four pairings. sha256:
  - git/r27 and git/r26: 57473017e147894ac257d490828067ce3df2279ba6c318572eaa8f8c947f9f9d (both)
  - wt/r27 and wt/r26: e05f25928894ff46e60f31c56d7e4b52c8694933b8a05ca4558decb777e44679 (both)
- Exit codes equal per pairing (1/1 everywhere): repaired gate changes no exit code on real inputs.
- Git vs working-tree, same gate and inputs: the only diff is the `source` field
  ("git"/"working-tree") and `revision` (commit hash/null); all evaluation payload identical
  (diff of base-git-r27.json vs base-wt-r27.json shows only those two keys).
- The round-27 frozen inputs and the round-26 inputs produce identical gate output at this
  revision (same hashes above); both populations have 32 rows, all ids matching `S[0-9]+`
  (audit in driver: non_numeric_ids = []), so the new population_id_unreachable check is not
  triggered — expected, since these are the round-27 verified inputs.
- Frozen expected.json (old base 83528f7c…) records exit 1 with 16 unadjudicated findings; the
  current revision reports 17. This is a corpus-state difference between commits, not a
  base-vs-repaired difference; I did not investigate it further (out of scope for parity).

## Conclusion

No-harm holds on real lane inputs: base and repaired gates return identical exit codes and
byte-identical JSON in all four pairings (round-27 frozen and round-26 inputs, Git mode and
working-tree mode). The repair changed behavior only on unusable inputs, which these real
inputs do not exercise.

## Not verified

- I did not run .ufo/waves/round-28/c1_interface_count.py (the 15/15 claim is the L1's
  counter evidence, not this seat's) and did not run citing_set_selftest.py.
- I did not run the gates on any input other than the two real sets, in the two modes.
- No tool installs or upgrades were needed or performed (python3 3.14.8, git 2.56.0, host).
