# ExecPinMutantsGateCode — round 34, wave 1

Axis: operability. Maintainability: the runner propagates the gate's structured refusal reason, not message text.

## Change

Sandbox patch: `/fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/patch.diff` — **2 files, 57 insertions(+), 9 deletions(-)**; SHA-256 `d873234ef1dd6499e8735b9f396d4608183451679db511bfdd231177f3302c24`.

The runner now copies a string `reason` from a gate `input_invalid` finding into the per-case `code`; P7 h7b expects `revision_not_found`. The runner docstring describes this code and P7's gate-ceiling probe. Code: `/fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/clone/scripts/citing_set_selftest.py:129-137,677-682`; spec: `/fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/clone/scripts/fixtures/citing-set-hostile/P7-setup-pin-discovery/hostile.json:26-34`.

## Results

| Probe | Python exit | Result |
|---|---:|---|
| Pristine benign suite | 0 | Pass; clean, 45 cases, 0 failed. |
| Pristine hostile suite | 0 | Pass, P1–P7; P7 h7b code check true. |
| m3d hostile suite | 0 | Survives; P7 passes and h7b code remains `revision_not_found`. |
| m3f hostile suite | 1 | Killed; P7 h7b reports `root_not_repository_top_level`, code check false. |
| m3g hostile suite | 1 | Killed; same P7 h7b code mismatch as m3f. |

**m3d is equivalent under the current setup vocabulary, not proven equivalent in general.** `git_commit` requires a preceding `git_init`; setup Git runs in the copied case root with inherited `GIT_*` removed; fixture `.git` entries and setup paths containing `.git` are refused, and `mkdir`/`fifo` cannot create `.git` (`/fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/clone/scripts/citing_set_selftest.py:54-62,73-74,397-412,487-499,521-541`). Thus removing the setup `--git-dir`/`--work-tree` and setup ceiling pins cannot redirect an accepted setup to the victim repository. m3f/m3g remove the gate ceiling, which P7 distinguishes through the gate's structured finding.

## Commands and retained evidence

Clone setup (all parts exit 0; final output HEAD `a2fe31b2d1d2bf67f832b31fb994869b83dbdb9f`):
`unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/clone && git -C /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/clone checkout -q a2fe31b2d1d2bf67f832b31fb994869b83dbdb9f && mkdir -p /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/tmp /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/mutants /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/receipts && git -C /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/clone rev-parse HEAD`

P7 directory creation exited 0: `mkdir -p /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/clone/scripts/fixtures/citing-set-hostile/P7-setup-pin-discovery`.
Mutant source copies exited 0: `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; export TMPDIR=/fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/tmp; cp clone/scripts/citing_set_selftest.py mutants/citing_set_selftest.m3d.py && cp clone/scripts/citing_set_selftest.py mutants/citing_set_selftest.m3f.py && cp clone/scripts/citing_set_selftest.py mutants/citing_set_selftest.m3g.py`.

Each probe shell used `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; export TMPDIR=/fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/tmp; <listed command>; rc=$?; printf 'command_exit=%s\n' "$rc"; exit 0`; the table gives each exact Python command including its stdout redirection. The reported exit is the captured Python exit (wrapper exit 0).

- `python3 -B /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/clone/scripts/citing_set_selftest.py --root /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/clone --tmpdir /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/tmp/benign-pristine-final > /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/receipts/benign-pristine-final.json` → 0; `/fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/receipts/benign-pristine-final.json:1-7`.
- `python3 -B /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/clone/scripts/citing_set_hostile_selftest.py --root /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/clone --tmpdir /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/tmp/hostile-pristine-final > /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/receipts/hostile-pristine-final.json` → 0; `/fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/receipts/hostile-pristine-final.json:1-4,159-182`.
- `python3 -B /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/clone/scripts/citing_set_hostile_selftest.py --root /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/clone --tmpdir /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/tmp/hostile-m3d-final --runner /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/mutants/citing_set_selftest.m3d.py > /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/receipts/hostile-m3d-final.json` → 0; `/fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/receipts/hostile-m3d-final.json:1-4,159-182`.
- `python3 -B /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/clone/scripts/citing_set_hostile_selftest.py --root /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/clone --tmpdir /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/tmp/hostile-m3f-final --runner /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/mutants/citing_set_selftest.m3f.py > /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/receipts/hostile-m3f-final.json` → 1; `/fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/receipts/hostile-m3f-final.json:1-4,159-182`.
- `python3 -B /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/clone/scripts/citing_set_hostile_selftest.py --root /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/clone --tmpdir /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/tmp/hostile-m3g-final --runner /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/mutants/citing_set_selftest.m3g.py > /fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/receipts/hostile-m3g-final.json` → 1; `/fast/scratch/hyaku/kake-r34/w1/ExecPinMutantsGateCode/receipts/hostile-m3g-final.json:1-4,159-182`.

Patch generation from clone cwd: `git diff --no-ext-diff --unified=3 -- scripts/citing_set_selftest.py > ../patch.diff` → 0; `git diff --no-index --no-ext-diff --unified=3 -- /dev/null scripts/fixtures/citing-set-hostile/P7-setup-pin-discovery/hostile.json >> ../patch.diff` → 1 (new-file difference); `git apply --stat ../patch.diff` → 0, reported the diffstat above. A first hash command used incorrect relative mutant paths and exited 1; the corrected absolute-path `sha256sum` command exited 0.

Hashes: patch `d873234ef1dd6499e8735b9f396d4608183451679db511bfdd231177f3302c24`; runner `d78494ef12f36ff8d950ec5081a3648a926cf3225c399c0a5589bf5371a04411`; P7 spec `7ec6c4afb76cde74defb70d4e38f5f66076977adc93147d930fd7da141d340d1`; benign receipt `515addb1c0f67f4927015e00e66ae801de47152a7582aa1d219046a006512278`; pristine hostile `56ba20a965ba33082fe6a2a155445359e4625e9cb3ead918e8363f96db86e971`; m3d `ee52535f3048f1783a516846ce4b73581779e6ba41e18560bc32a74efe75f911`; m3f `dd99449948e2748dfa072bf18b2f8fb868d9cb52bbf97ff1cffd3812aae52f63`; m3g `165372922372799e84d43deb1d172eb4464eea25cf6d6046ae6fdf56673e5703`. Receipt hashes refer to the absolute paths in the command table.

No other checks, installs, or network requests. LSP was unavailable in the supplied tool interface. No build, lint, formatter, mutant benign suite, or counter was run. The only lane file written is this report.