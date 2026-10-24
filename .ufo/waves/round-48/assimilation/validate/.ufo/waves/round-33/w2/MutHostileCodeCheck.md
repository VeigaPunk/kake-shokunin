# Round 33 wave 2 — hostile `reason_code` mutation probe

Axes: operability attacked; freshness not exercised.

**Finding:** Yes. The strict supplement detected all four requested mutants. Each mutant commit was checked by `c1_strict_supplement.py`, which runs the hostile selftest with both the pristine runner and its generated m3 runner. Pristine and restored baselines were 4/4; every mutant was below 4/4.

| Mutant | Pristine runner result | m3 runner result | Strict met | Verdict |
|---|---|---|---:|---|
| (a) Omit `all(detail["codeChecks"].values())` | exit 0; h6 code `setup_commit_before_init` | exit 0; h6 code `setup_commit_without_repo`; P6 passed **true** unexpectedly | 3/4 | Killed: strict s4 failed; m3 was accepted |
| (b) Compare with `!=` | exit 1; h6 code `setup_commit_before_init` | exit 0; h6 code `setup_commit_without_repo`; P6 passed **true** unexpectedly | 1/4 | Killed: pristine failed and m3 was accepted |
| (c) Read `reason` instead of `code` | exit 1; h6 “code” became `case.json setup op 'git_commit' needs an earlier 'git_init'` | exit 1; h6 “code” became `case setup failed: git_commit needs the repository created by git_init`; P6 passed false | 1/4 | Killed: pristine failed |
| (d) Remove `reason_code` from `CASE_KEYS` | exit 2; no h6 code (spec rejected before cases ran) | exit 2; no h6 code or P6 result (same early spec rejection) | 1/4 | Killed: pristine failed |

The baseline and restored strict outputs both had `met: 4`, pristine exit 0 with h6 code `setup_commit_before_init`, and m3 exit 1 with h6 code `setup_commit_without_repo` and `p6passed: false`. For (d), the supplement reports only the early exit 2; it does not include the selftest error text.

## Evidence

- Scratch clone: `/fast/scratch/hyaku/kake-r33/w2/MutHostileCodeCheck/clone`, based on `0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0`.
- Target locations: `scripts/citing_set_hostile_selftest.py:89-90` (`CASE_KEYS`), `:221` (failure code extraction), `:229` (code comparison), `:230-233` (passed predicate). Strict runner behavior: `.ufo/waves/round-33/c1_strict_supplement.py:96-131`.
- Baseline strict commit `0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0`: `met 4/4`.
- Mutant commits / strict output: (a) `da868e857d81f1d8a353e49db3a1241da9ad2b18`, `met 3/4`; (b) `c237cbd26b1a3e640e02e364dff402758785d3b2`, `met 1/4`; (c) `0da4260a6f047daa4999690326c4c489662d74b2`, `met 1/4`; (d) `22955b81a1b24bf5ce7413c7aa598ee3678f5ad5`, `met 1/4`.
- Restored-byte commit `b87b9f6ef30570595360a4af6a186b0d3649acbb`: strict `met 4/4`.
- Target SHA-256 before probes: `70def10946ef86c35443749463fd58dd923cf3f3555b02616bacc253df66c7b0`. After restoration: same SHA-256. The working file and `git show 0a0acfb1...:scripts/citing_set_hostile_selftest.py` both produced that hash; the restored commit also passed strict 4/4.

## Commands and exits

All commands ran in the scratch clone; each listed command chain exited 0. `TMPDIR` was set to `/fast/scratch/hyaku/kake-r33/w2/MutHostileCodeCheck/tmp`; Git environment overrides were unset before Git commands.

- `mkdir -p /fast/scratch/hyaku/kake-r33/w2/MutHostileCodeCheck && mkdir -p /fast/scratch/hyaku/kake-r33/w2/MutHostileCodeCheck/tmp && unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE && git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r33/w2/MutHostileCodeCheck/clone && git -C /fast/scratch/hyaku/kake-r33/w2/MutHostileCodeCheck/clone checkout -q 0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0` — exit 0.
- `python3 -B .ufo/waves/round-33/c1_strict_supplement.py --rev 0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0 --repo /fast/scratch/hyaku/kake-r33/w2/MutHostileCodeCheck/clone` — exit 0, `met 4/4`.
- For each mutant, `git add scripts/citing_set_hostile_selftest.py && git -c user.name='Mutation Probe' -c user.email='mutant-probe@localhost' commit -m '<listed probe message>' && git rev-parse HEAD && python3 -B .ufo/waves/round-33/c1_strict_supplement.py --rev HEAD --repo /fast/scratch/hyaku/kake-r33/w2/MutHostileCodeCheck/clone` — exit 0. Messages, commits and results: `probe hostile codeChecks omitted` → `da868e8…`, 3/4; `probe hostile code comparison inverted` → `c237cbd…`, 1/4; `probe hostile code reads reason field` → `0da4260…`, 1/4; `probe hostile spec key omission` → `22955b8…`, 1/4.
- Restoration/hash command: `printf 'working '; sha256sum scripts/citing_set_hostile_selftest.py; printf 'baseline '; git show 0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0:scripts/citing_set_hostile_selftest.py | sha256sum` — exit 0; hashes matched.
- `git add scripts/citing_set_hostile_selftest.py && git -c user.name='Mutation Probe' -c user.email='mutant-probe@localhost' commit -m 'restore hostile selftest after mutation probes' && git rev-parse HEAD && python3 -B .ufo/waves/round-33/c1_strict_supplement.py --rev HEAD --repo /fast/scratch/hyaku/kake-r33/w2/MutHostileCodeCheck/clone` — exit 0; restored commit `b87b9f6…`, strict `met 4/4`.

No tool installs or updates. Report written to `.ufo/waves/round-33/w2/MutHostileCodeCheck.md`.