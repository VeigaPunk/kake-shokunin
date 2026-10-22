# Round 33 W1 — hostile selftest scratch collision

Axis: operability (concurrent scratch isolation). Tested clone revision `bc6c4a8d435473f3c30903210be30d9d6e3ef750`.

## Result

**No default-path collision is present:** `--tmpdir` is required by the CLI, so omitting it fails argument parsing before any scratch path is used. Four concurrent runs with distinct explicit scratch directories all exited 0 and reported `passed: true`. No patch was needed. This does not establish behavior when multiple callers deliberately reuse the same explicit `--tmpdir`.

## Commands and exits

All invocations were launched concurrently from `/fast/scratch/hyaku/kake-r33/w1/ExecHostileScratchCollision/clone`, with `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` unset and `TMPDIR=/fast/scratch/hyaku/kake-r33/w1/ExecHostileScratchCollision/tmp`. Output was redirected to the log paths shown.

| Run | Exact Python command | Exit | Retained output |
|---|---|---:|---|
| no-tmp-1 | `python3 -B scripts/citing_set_hostile_selftest.py --root /fast/scratch/hyaku/kake-r33/w1/ExecHostileScratchCollision/clone` | 2 | `.../no-tmp-1.stderr` |
| no-tmp-2 | `python3 -B scripts/citing_set_hostile_selftest.py --root /fast/scratch/hyaku/kake-r33/w1/ExecHostileScratchCollision/clone` | 2 | `.../no-tmp-2.stderr` |
| no-tmp-3 | `python3 -B scripts/citing_set_hostile_selftest.py --root /fast/scratch/hyaku/kake-r33/w1/ExecHostileScratchCollision/clone` | 2 | `.../no-tmp-3.stderr` |
| no-tmp-4 | `python3 -B scripts/citing_set_hostile_selftest.py --root /fast/scratch/hyaku/kake-r33/w1/ExecHostileScratchCollision/clone` | 2 | `.../no-tmp-4.stderr` |
| explicit-1 | `python3 -B scripts/citing_set_hostile_selftest.py --root /fast/scratch/hyaku/kake-r33/w1/ExecHostileScratchCollision/clone --tmpdir /fast/scratch/hyaku/kake-r33/w1/ExecHostileScratchCollision/explicit-1` | 0 | `.../explicit-1.stdout` |
| explicit-2 | `python3 -B scripts/citing_set_hostile_selftest.py --root /fast/scratch/hyaku/kake-r33/w1/ExecHostileScratchCollision/clone --tmpdir /fast/scratch/hyaku/kake-r33/w1/ExecHostileScratchCollision/explicit-2` | 0 | `.../explicit-2.stdout` |
| explicit-3 | `python3 -B scripts/citing_set_hostile_selftest.py --root /fast/scratch/hyaku/kake-r33/w1/ExecHostileScratchCollision/clone --tmpdir /fast/scratch/hyaku/kake-r33/w1/ExecHostileScratchCollision/explicit-3` | 0 | `.../explicit-3.stdout` |
| explicit-4 | `python3 -B scripts/citing_set_hostile_selftest.py --root /fast/scratch/hyaku/kake-r33/w1/ExecHostileScratchCollision/clone --tmpdir /fast/scratch/hyaku/kake-r33/w1/ExecHostileScratchCollision/explicit-4` | 0 | `.../explicit-4.stdout` |

The explicit runs' JSON each reports top-level `passed: true`, all six P1–P6 cases passed, `timedOut: false`, `canary: false`, `victimUnchanged: true`, and `error: null`. The omitted-argument runs each report `the following arguments are required: --tmpdir`; stdout is empty.

## Evidence and limits

- Clone HEAD observed as `bc6c4a8d435473f3c30903210be30d9d6e3ef750`.
- CLI requirement: clone `scripts/citing_set_hostile_selftest.py:229` (`parser.add_argument("--tmpdir", required=True, ...)`). Scratch use follows at lines 234, 248, 251; per-spec work path is line 181.
- Omitted argument stderr: `/fast/scratch/hyaku/kake-r33/w1/ExecHostileScratchCollision/no-tmp-{1,2,3,4}.stderr:1-3`; identical SHA-256 `d7c5b2a0c172262b9ecbf7cb1c3fba24e64e4be1af8e0bf83efa1da6114b69cf`. Each omitted-run stdout is empty (SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).
- Explicit-run JSON evidence: `/fast/scratch/hyaku/kake-r33/w1/ExecHostileScratchCollision/explicit-{1,2,3,4}.stdout:3` (`passed: true`) and `:128-130` (`error: null`). SHA-256s in run order: `649d44ae16814fed5a3b567f1dbd9c955fecaec8c5cdad9f21b5b3d5e9b7257c`, `0208459ad8bcbeb6dfd9f3160bc3dd0f9ac3ac363d19403b77a401bb5e13158e`, `2882efc7b6a5415824921b7025f5d318bcbb7d09a5f5aa7fbdca85e18980e82c`, `0fe9fea98ee7c2dfdf50f9bc2e53b9d2f64b4a1f292701a8d9533ddb57206246`.
- No patch or tool install. No build, lint, formatter, or additional tests were run.
