# CriticOverReject — C1 no-harm: does the repaired gate refuse legitimate input?

Seat: KakeR28a3.CriticOverReject (critic, leaf). Axis judged: operability.
Base gate: `scripts/citing_set.py` at 22c1669 (blob 352a471abec08daa56a0fb7ef23fe78f2930d773).
Repaired gate: same path at b5d423f (blob c26fcd498f1974265e6bb80dca8e102f57eb7b5f).
All work ran in /fast/scratch/hyaku/kake-r28a3/w1/CriticOverReject/ (TMPDIR there). No lane file other than this report was written.

## Verdict
Harm found: 2 new refusals of legitimate input in the new Git top-level check; plus 2 edge cases in the same check.
All 17 other legitimate cases (working tree, lane frozen inputs, nested corpus, symlinked and relative roots, S001/S0001, large JSON, linked worktree) give the same result under both gates.
This is a fixable defect, not a tradeoff: a one-line correction removes every over-refusal found here, still refuses the nested root, and keeps the C1 counter at 15/15.

## Counterexample
`GitSource._require_top_level` (b5d423f `scripts/citing_set.py:297-310`) compares `realpath(git rev-parse --show-toplevel)` with `realpath(root)`:
1. Bare repository as `--root` with `--revision HEAD`: the base reads the blobs correctly (clean, citingPairs 2). The repaired gate refuses it with `root_not_repository_top_level`, because `--show-toplevel` fails when there is no work tree. Git paths in a bare repository are already relative to the top level, so the defect this check guards against cannot occur.
2. A Git top level whose directory name ends in a space: `--show-toplevel` prints `.../git-trailing-space \n` (checked with od -c). `.strip()` at line 308 removes the real trailing space, the paths no longer match, and the gate refuses.
3. Edge cases (low weight): `--root <repo>/.git`, and a caller environment with `GIT_WORK_TREE` exported to another worktree of the same repository. The base is clean on both; the repaired gate refuses both. The blobs read at the revision are identical in each case.

## Outcome table (input → base → repaired → corrected)
Results file: scratch `results.json` sha256 4484ef55c22ad08adbd08aab7928f09052322bffc9c959dfc9b9386063863256; harness `harness.py` sha256 d9d08d4686b0b228b6b68c0349bd7d31643a329fd8b210f537c433ebf90bab8b.

| Input | Base | Repaired | Corrected |
|---|---|---|---|
| Working tree, corpus in a/b/c nested subdirectories | 0 clean | 0 clean | 0 clean |
| Working tree, root through a symlink | 0 clean | 0 clean | 0 clean |
| Working tree, relative root path | 0 clean | 0 clean | 0 clean |
| Working tree, population ids S001 and S0001 both cited | 0 clean | 0 clean | 0 clean |
| Working tree, 48 MiB regular population JSON | 0 clean | 0 clean | 0 clean |
| Working tree, 400-level nested metadata in regular JSON | 0 clean | 0 clean | 0 clean |
| Working tree, population is an in-root symlink to a regular file | 0 clean | 0 clean | 0 clean |
| Lane frozen r27 population+ledger+corpus, working tree | 1 failed, 16 unadjudicated | same | same |
| Lane frozen r27 inputs committed as a Git repo, `--revision HEAD` | 1 failed, 16 unadjudicated | same | same |
| Lane clone, `--revision b5d423f`, frozen population/ledger paths | 1 failed, 17 unadjudicated | same | same |
| Git top level, relative root `git-top`, nested corpus | 0 clean | 0 clean | 0 clean |
| Git top level, root `./git-top/` | 0 clean | 0 clean | 0 clean |
| Git top level through a symlink | 0 clean | 0 clean | 0 clean |
| Git linked worktree as root | 0 clean | 0 clean | 0 clean |
| Git top level, hook-style `GIT_DIR=<abs>/.git` exported | 0 clean | 0 clean | 0 clean |
| Git top level, 48 MiB population | 0 clean | 0 clean | 0 clean |
| Git top level, ids S001 and S0001 | 0 clean | 0 clean | 0 clean |
| **Git bare repository as root** | 0 clean | **2 root_not_repository_top_level** | 0 clean |
| **Git top level, directory name ends in a space** | 0 clean | **2 root_not_repository_top_level** | 0 clean |
| Git root = `<repo>/.git` (edge) | clean | 2 could-not-evaluate | clean |
| `GIT_WORK_TREE` exported to a sibling worktree (edge) | clean | 2 could-not-evaluate | clean |
| Control: root nested at `<repo>/sub` (routed defect) | 1 failed, wrong surface | 2 root_not_repository_top_level | 2 root_not_repository_top_level |
| Control: plain directory with `--revision HEAD` | 2 revision_not_found | same | same |

Round-27 fixtures: all 29 cases under `scripts/fixtures/citing-set/` match their own expected.json (exit plus sorted finding ids) under both gates.
Intended refusals were not counted as harm, because `.ufo/waves/round-27/unresolved-acceptance.json:41` routes them as defects. They are: non-numeric population ids, an absent or empty corpus, a blank `--revision`, and a nested Git root.

## Smallest safe correction
Ask Git for the root's position inside the repository. Do not compare paths. In `_require_top_level`, replace `--show-toplevel` with `--show-prefix`, delete the `top = ...strip()` line, and use this test:
`if done.returncode != 0 or done.stdout.rstrip(b"\n"):` → raise `root_not_repository_top_level`.
In this sandbox the prefix is empty for the top level, a bare repository, `.git`, a trailing-space name, a linked worktree, a symlinked root, and the `GIT_WORK_TREE` case. It is `sub/` and `corpus/knowledge/` for nested roots, so the nested-root refusal is kept.
Sandbox commit 47d554f57d00e06e4229bcf819448d8ce2a345a1, diff against b5d423f: 2 insertions and 3 deletions in `scripts/citing_set.py`. Corrected gate sha256: 709e686a5618dc4f3ba8b1588eadc939836850910c742a5b043c121a4c32b682.
Impacted axis: operability (the gate refuses valid Git roots). Freshness is unaffected.

## Commands run (cwd as noted; all exit codes observed)
- `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin <scratch>/clone` → 0; `git show {22c1669,b5d423f}:scripts/citing_set.py > gates/{base,repaired}.py`; `git hash-object` matches both blobs.
- `python3 -B harness.py > results.json` (scratch) → 0, run twice: once with two gates, once with three; the outcomes were the same for base and repaired.
- Fixture loop: `python3 -B gates/<g>.py --root <fixture> --population population.json --ledger ledger.json --json` for 29 fixtures × 2 gates → all match expected.
- `git -C <root> rev-parse --show-prefix` / `--show-toplevel | od -c` probes → outputs as stated above.
- `python3 -B .ufo/waves/round-28/c1_interface_count.py --root . --revision b5d423f` (in clone) → exit 0, 15/15 (11/11 defect, 4/4 control).
- Same with `--revision 47d554f` (correction) → exit 0, 15/15 (11/11, 4/4).
- `python3 -B scripts/citing_set.py --selftest` at 47d554f (clone) → exit 0, failures []; at b5d423f (sandbox worktree) → exit 0, failures [].

## Not verified
- Bind mounts, case-insensitive filesystems, Windows paths, SHA-256 object-format repositories, and Git versions other than 2.56.0 (Python 3.14.8).
- FIFO or device documents, and JSON nested too deeply to parse. These are intended refusals (the base crashed or blocked on them), so they were not re-exercised here.
- Whether operators actually run the gate against bare repositories in practice. The contract text ("read blobs when --revision set") permits it, but I found no caller doing so.
- I did not judge, admit, or integrate anything. The correction exists only in my sandbox clone.

## Tooling
No installs or updates.
