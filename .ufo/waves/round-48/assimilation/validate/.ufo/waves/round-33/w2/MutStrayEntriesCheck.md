# Round 33 mutation probe — fixture-root stray entries

Axis: operability.

## Mutation and verdict

Removed the runner's fixture-root `non_directories` refusal block (original `scripts/citing_set_selftest.py:739-744`). This was the smallest behavior-bearing change for the claimed stray-entry refusal. The five requested committed checks did not kill it: **survived; none pins this refusal**.

Clone: `/fast/scratch/hyaku/kake-r33/w2/MutStrayEntriesCheck/clone`, starting revision `0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0`.
Runner SHA-256: pristine `88b47f6b957d0ebff0f715fa7b2081c69cc4160d087587f71997038ce8170721`; mutant `ebeb3708c29ff48bb0344bbbc9249c42398b1277d35b7d4138c0a8247c1ef372`; restored `88b47f6b957d0ebff0f715fa7b2081c69cc4160d087587f71997038ce8170721` (exact match). Mutant check revision was unattached commit `e1aaf7ec307a6e6345ef357d180f025d7b7dc408`, parented to the starting revision. The temporary index kept the checkout index unchanged.

## Commands and observed outputs

All ran from the clone after `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE && export TMPDIR=/fast/scratch/hyaku/kake-r33/w2/MutStrayEntriesCheck/tmp`. Each Python process returned exit 0. Baseline setup also ran `mkdir -p "$TMPDIR/baseline-benign"` and `mkdir -p "$TMPDIR/baseline-hostile"`. Mutant and restored commands redirected stdout/stderr to the specified `.json`/`.stderr` paths; stderr files were 0 bytes.

Pristine bytes, before mutation:
- `python3 -B scripts/citing_set_selftest.py --root . --tmpdir "$TMPDIR/baseline-benign"` — clean, 45 cases, 0 failed.
- `python3 -B scripts/citing_set_hostile_selftest.py --root . --tmpdir "$TMPDIR/baseline-hostile"` — passed, six specs.
- `python3 -B .ufo/waves/round-33/c1_code_probe.py --rev HEAD --repo .` — `met: 4/4`, `guard_ok: true`.
- `python3 -B .ufo/waves/round-33/c1_strict_supplement.py --rev HEAD --repo .` — `met: 4/4`.
- `python3 -B .ufo/waves/round-33/criteria/refusal_code_check.py --root . --rev HEAD` — `met: 5/5`, passed.

Mutant bytes (revision `e1aaf7ec307a6e6345ef357d180f025d7b7dc408` for revision-based checks):
- `python3 -B scripts/citing_set_selftest.py --root . --tmpdir "$TMPDIR/mutant-benign" >"$TMPDIR/mutant-benign.json" 2>"$TMPDIR/mutant-benign.stderr"` — exit 0; clean, 45 cases, 0 failed; output: `/fast/scratch/hyaku/kake-r33/w2/MutStrayEntriesCheck/tmp/mutant-benign.json:1-7`.
- `python3 -B scripts/citing_set_hostile_selftest.py --root . --tmpdir "$TMPDIR/mutant-hostile" >"$TMPDIR/mutant-hostile.json" 2>"$TMPDIR/mutant-hostile.stderr"` — exit 0; passed, six specs; output: `/fast/scratch/hyaku/kake-r33/w2/MutStrayEntriesCheck/tmp/mutant-hostile.json:1-4,134-160`.
- `python3 -B .ufo/waves/round-33/c1_code_probe.py --rev e1aaf7ec307a6e6345ef357d180f025d7b7dc408 --repo . >"$TMPDIR/mutant-c1.json" 2>"$TMPDIR/mutant-c1.stderr"` — exit 0; `met: 4/4`, `guard_ok: true`; output: `/fast/scratch/hyaku/kake-r33/w2/MutStrayEntriesCheck/tmp/mutant-c1.json:1-13,152-160`.
- `python3 -B .ufo/waves/round-33/c1_strict_supplement.py --rev e1aaf7ec307a6e6345ef357d180f025d7b7dc408 --repo . >"$TMPDIR/mutant-strict.json" 2>"$TMPDIR/mutant-strict.stderr"` — exit 0; `met: 4/4`; output: `/fast/scratch/hyaku/kake-r33/w2/MutStrayEntriesCheck/tmp/mutant-strict.json:1-30`.
- `python3 -B .ufo/waves/round-33/criteria/refusal_code_check.py --root . --rev e1aaf7ec307a6e6345ef357d180f025d7b7dc408 >"$TMPDIR/mutant-criterion.json" 2>"$TMPDIR/mutant-criterion.stderr"` — exit 0; `met: 5/5`, passed; output: `/fast/scratch/hyaku/kake-r33/w2/MutStrayEntriesCheck/tmp/mutant-criterion.json:1-58`.

Restored bytes (`HEAD`): reran those same five commands using, respectively, tmpdirs `"$TMPDIR/restored-benign"`, `"$TMPDIR/restored-hostile"`, then `--rev HEAD`; output redirections used matching `restored-*.json` and `restored-*.stderr` names. All returned exit 0 with the same results: clean 45/45; hostile passed; C1 4/4; strict 4/4; refusal-code criterion 5/5. Outputs: `/fast/scratch/hyaku/kake-r33/w2/MutStrayEntriesCheck/tmp/restored-benign.json:1-7`, `restored-hostile.json:1-4,134-160`, `restored-c1.json:1-13,152-160`, `restored-strict.json:1-30`, and `restored-criterion.json:45-58`.

Restoration evidence: `git rev-parse HEAD` remained `0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0`; restored runner hash exactly matches pristine; final `git status --short` was empty. No tools installed. No separate custom stray-entry test was run.