PARTIAL: Implementation and patch artifact are complete, but the required concurrent reproductions and benign suite were not run.

# Round 33 W1 — ExecScratchDefaultUnique

Axis: operability.

## Change

In the sandbox clone, `scripts/citing_set_selftest.py` now defaults `--tmpdir` to `None`. Without an explicit `--tmpdir`, `main` creates a private `tempfile.mkdtemp` directory under the former default scratch path (`DEFAULT_TMPDIR`), runs the existing logic there, and removes the directory in `finally`. Explicit `--tmpdir` values still go directly to the existing runner path and are not removed. An allocation error produces the existing could-not-evaluate JSON result. Added inline documentation. `load_case_setup` and `apply_setup` were not changed.

Unified diff: `/fast/scratch/hyaku/kake-r33/w1/ExecScratchDefaultUnique/patch.diff` (against `bc6c4a8d435473f3c30903210be30d9d6e3ef750`). The generated `git diff` summary was `1 file changed, 35 insertions(+), 3 deletions(-)`.
Source evidence: `/fast/scratch/hyaku/kake-r33/w1/ExecScratchDefaultUnique/clone/scripts/citing_set_selftest.py:93-95,174,769-790`. Source SHA-256: `f48fe3c2191054ec7fe1646e55c74c164e225838587c43a797557584f7dc20f6`; patch SHA-256: `ca30e678b78752c85edbbb18131315790eeb8442d020a65bd46e13010c2231fe`.

## Commands and evidence

- `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; mkdir -p /fast/scratch/hyaku/kake-r33/w1/ExecScratchDefaultUnique/tmp; export TMPDIR=/fast/scratch/hyaku/kake-r33/w1/ExecScratchDefaultUnique/tmp; git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r33/w1/ExecScratchDefaultUnique/clone && git -C /fast/scratch/hyaku/kake-r33/w1/ExecScratchDefaultUnique/clone checkout -q bc6c4a8d435473f3c30903210be30d9d6e3ef750` — exit 0; no output.
- `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; git -C /fast/scratch/hyaku/kake-r33/w1/ExecScratchDefaultUnique/clone diff --no-ext-diff -- scripts/citing_set_selftest.py` — exit 0; diff summary above.
- `sha256sum /fast/scratch/hyaku/kake-r33/w1/ExecScratchDefaultUnique/clone/scripts/citing_set_selftest.py /fast/scratch/hyaku/kake-r33/w1/ExecScratchDefaultUnique/patch.diff` — exit 0; hashes above.
- Before-patch: four concurrent `python3 -B scripts/citing_set.py --selftest` runs — NOT RUN; failure count unavailable.
- After-patch: same four concurrent runs — NOT RUN; failure count unavailable.
- Patched benign suite — NOT RUN; cases/failures unavailable.

The wave instruction prohibits running tests while the editing wave is in flight; therefore the requested behavioral counts and suite result remain unverified. No tools were installed. No lane files other than this report were written.
