# Round 33 W1 — `read_expected` OSError handling

## Change
- Worked in `/fast/scratch/hyaku/kake-r33/w1/ExecReadExpectedOSError/clone` at base `bc6c4a8d435473f3c30903210be30d9d6e3ef750`.
- Changed only `scripts/citing_set_selftest.py`, within `read_expected` and the `run_case` call site.
- `read_expected` now converts OSErrors throughout open/fstat/read/close into its existing `expected.json unreadable` ValueError reason (retaining the symlink note). `run_case` also catches an OSError that reaches the call site and returns a failed row with an `expected.json unreadable` reason.
- Evidence: cloned source lines 399–423 and 544–550; patch is `/fast/scratch/hyaku/kake-r33/w1/ExecReadExpectedOSError/patch.diff`, SHA-256 `0e88f31c74ff8e26bae5b81b8e203c38e8bf147535627de6822db48569274f45`. Edited source SHA-256 `f520eedbe1f7c0bd1394562d106acf4e9815de90959a3764ec8d8ad976d1b54c`.

## Commands and verification
- Clone/setup command completed with exit 0 and no output: `mkdir -p /fast/scratch/hyaku/kake-r33/w1/ExecReadExpectedOSError/tmp && unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE && export TMPDIR=/fast/scratch/hyaku/kake-r33/w1/ExecReadExpectedOSError/tmp && git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r33/w1/ExecReadExpectedOSError/clone && git -C /fast/scratch/hyaku/kake-r33/w1/ExecReadExpectedOSError/clone checkout -q bc6c4a8d435473f3c30903210be30d9d6e3ef750`.
- Patch generation completed with exit 0 and no stdout: `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE && export TMPDIR=/fast/scratch/hyaku/kake-r33/w1/ExecReadExpectedOSError/tmp && git -C /fast/scratch/hyaku/kake-r33/w1/ExecReadExpectedOSError/clone diff --no-ext-diff --unified=3 -- scripts/citing_set_selftest.py > /fast/scratch/hyaku/kake-r33/w1/ExecReadExpectedOSError/patch.diff`.
- Hash command: `sha256sum /fast/scratch/hyaku/kake-r33/w1/ExecReadExpectedOSError/patch.diff /fast/scratch/hyaku/kake-r33/w1/ExecReadExpectedOSError/clone/scripts/citing_set_selftest.py`; exit 0; output is the two hashes above.
- The before/after scratch-fixture reproduction and benign selftest suite were not run: the fleet-executor editing-wave instruction prohibits builds/lint/tests and reserves post-integration gates for the L1. Therefore there is no reproduction output or suite result to report; both remain unverified.
- No tool was installed. LSP is unavailable in the supplied tool inventory.

## Risk / blocker
- The requested runtime evidence remains for the L1's post-integration gate; source and patch artifacts are delivered. No other blocker identified.
