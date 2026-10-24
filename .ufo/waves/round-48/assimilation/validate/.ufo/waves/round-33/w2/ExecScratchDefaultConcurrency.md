# Round 33 wave 2 — ExecScratchDefaultConcurrency

Axis: operability. No source changes; only this scoped report was written in the lane. Test clone and retained outputs are under `/fast/scratch/hyaku/kake-r33/w2/ExecScratchDefaultConcurrency/`.

## Results

- Base export: `0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0`. The runner retained its base `DEFAULT_TMPDIR` `/fast/scratch/hyaku/kake-r27` at `clone/scripts/citing_set_selftest.py:151` (SHA-256 `88b47f6b957d0ebff0f715fa7b2081c69cc4160d087587f71997038ce8170721`). To keep writes inside the assigned sandbox, each test ran in a separate user/mount namespace binding that path to the sandbox scratch parent; host parent was not changed.
- Before and after, `citing-set-selftest-*` listing was empty both at the sandbox bind source and at the configured host parent. The initial host listing did contain a distinct `citing-set-selftest/` directory (no hyphen suffix); it was untouched.
- Eight concurrent invocations of `python3 -B scripts/citing_set.py --selftest` (inside the namespace wrapper recorded in `evidence.txt:8-10`) all exited 0. Each output: `verdict=clean`, `passed=true`, `cases=45`, `failed=0`, `failedCases=0`; all stderr files were empty. No `citing-set-selftest-*` directories remained.
- `python3 -B scripts/citing_set_selftest.py --tmpdir /fast/scratch/hyaku/kake-r33/w2/ExecScratchDefaultConcurrency/tmp/explicit`: exit 0, clean/45 cases. The explicit directory, sentinel, and generated `citing-set-selftest/cases` remained afterward.
- Wrapper attempt `python3 -B scripts/citing_set.py --selftest --tmpdir /fast/scratch/hyaku/kake-r33/w2/ExecScratchDefaultConcurrency/tmp/explicit`: exit 64; wrapper reports `unrecognized arguments: --tmpdir`. Direct runner invocation above is the supported explicit-tmpdir check.
- Copied runner with `DEFAULT_TMPDIR` pointed to sandbox directory mode `0555`: `python3 -B /fast/scratch/hyaku/kake-r33/w2/ExecScratchDefaultConcurrency/runner-unwritable.py --root /fast/scratch/hyaku/kake-r33/w2/ExecScratchDefaultConcurrency/clone` exited 2. JSON verdict was `could-not-evaluate`, with `Errno 13 Permission denied` creating the private scratch directory; no prefixed leftover remained.

## Evidence

Full command/results index: `/fast/scratch/hyaku/kake-r33/w2/ExecScratchDefaultConcurrency/evidence.txt:1-25`. Raw concurrent JSON summaries: `namespaced-1.stdout:3-7` through `namespaced-8.stdout:3-7`; SHA-256 values are in `evidence.txt:24-25`. Explicit result: `explicit-runner.stdout:3-7`. Unwritable-parent result and exact refusal reason: `unwritable.stdout:18-22`; copied-runner SHA-256 is in `unwritable.stdout:13`.

Checks not run: none of the requested runtime checks remain unattempted. No tools were installed or updated.