Axis: operability.

## Work
Reworded human-readable refusal/error messages throughout `scripts/citing_set_selftest.py` in the isolated clone; setup logic and refusal codes are unchanged. The load-time check remains `setup_commit_before_init` and apply-time check remains `setup_commit_without_repo` (`clone/scripts/citing_set_selftest.py:402,529`). No lane source files were changed. Runner SHA-256 from the benign-suite output: `899a035dadf85febbe9502d2f03dcda75c0ea7e0375493bd92d3c6ca83b5c9b4`.

## Evidence
- Clone preparation command, from `/fast/scratch/hyaku/kake-r33/w2`:
  `mkdir -p ExecRewordAllMessages/tmp && export TMPDIR=/fast/scratch/hyaku/kake-r33/w2/ExecRewordAllMessages/tmp && unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE && if [ ! -d ExecRewordAllMessages/clone/.git ]; then git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin ExecRewordAllMessages/clone; fi && git -C ExecRewordAllMessages/clone checkout -q 0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0` — exit 0, no output.
- Hostile suite command:
  `mkdir -p tmp/hostile && export TMPDIR=/fast/scratch/hyaku/kake-r33/w2/ExecRewordAllMessages/tmp && python3 -B scripts/citing_set_hostile_selftest.py --root /fast/scratch/hyaku/kake-r33/w2/ExecRewordAllMessages/clone --tmpdir /fast/scratch/hyaku/kake-r33/w2/ExecRewordAllMessages/tmp/hostile; status=$?; printf '\nEXIT_CODE=%d\n' "$status"; exit 0` — reported test exit 0; output `passed: true`, six cases P1–P6 all passed. P6 observed rewritten reason `case.json encountered a commit before repository setup`, code `setup_commit_before_init`, `codeChecks.h6: true`, canary false and victim unchanged. No hostile spec failed.
- Benign suite command:
  `mkdir -p tmp/benign && export TMPDIR=/fast/scratch/hyaku/kake-r33/w2/ExecRewordAllMessages/tmp && python3 -B scripts/citing_set_selftest.py --root /fast/scratch/hyaku/kake-r33/w2/ExecRewordAllMessages/clone --tmpdir /fast/scratch/hyaku/kake-r33/w2/ExecRewordAllMessages/tmp/benign --min-cases 12 --json; status=$?; printf '\nEXIT_CODE=%d\n' "$status"; exit 0` — reported test exit 0; output `verdict: clean`, `cases: 45`, `failed: 0`, `failedCases: 0`.
- Searched committed `scripts/fixtures/citing-set-hostile/` recursively for `reason_contains` with `functions.grep`; output: `No matches found`. The six committed specs are P1-selftest-argv, P2-fixture-dot-git, P3-commit-without-init, P4-expected-json-guard, P5-symlinked-case, and P6-commit-before-init; P6's structured assertion is `reason_code: setup_commit_before_init` at `clone/scripts/fixtures/citing-set-hostile/P6-commit-before-init/hostile.json:23`. Search tool did not expose a numeric exit status.

Conclusion for this committed hostile-spec set: none still depends on runner message text; all six remained green after rewording. Other checks were not run. No tools installed or updated.
