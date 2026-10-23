# CriticHarmCheck — no-harm falsification

Axes: freshness and operability.
Attack: look for prior selftest regressions, removed coverage, or tracked deletions.
Counterexample: none reproduced on the assigned surface; this is not a universal no-harm conclusion.

## Scope and commands
- Sandbox S: `/fast/scratch/hyaku/kake-r36w2/CriticHarmCheck`.
- Evidence E: `/fast/scratch/hyaku/kake-r36w2/CriticHarmCheck/evidence`.
- Base B: `b720d799ae99c19a7c97f2b1391d4fe928be0e11`, tree `S/base`.
- Head H: `f3a38bf8e68f6cee386125d34b5e95ac9b2df66e`, tree `S/clone`.
- Each command below ran from its tree R, once per revision; `$R` and `$T` denote the expanded absolute paths recorded in `E/test-commands.json:1-212`.
- Per-run T: `S/tmp/{base,head}/<test-label>`; TMPDIR=T, HOME=T/home, KAKE_SELFTEST_DIR=T/freshness; directories created first. GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE were unset before every Git invocation and in test environments.
- At most two test invocations ran concurrently; every invocation had a 180-second timeout and five-second kill grace. All subprocess groups were absent after exit; no started process remains.

| Test label | Exact argv (path variables expanded in receipt) | Base passed/total; exit | Head passed/total; exit |
|---|---|---|---|
| link-preview | `timeout --kill-after=5s 180s python3 -B scripts/link_preview_selftest.py` | 46/46; 0 | 46/46; 0 |
| base-path | `timeout --kill-after=5s 180s python3 -B scripts/base_path_selftest.py` | 45/45; 0 | 45/45; 0 |
| citing-set | `timeout --kill-after=5s 180s python3 -B scripts/citing_set_selftest.py --root $R --tmpdir $T/runner` | 45/45; 0 | 45/45; 0 |
| citing-set-hostile | `timeout --kill-after=5s 180s python3 -B scripts/citing_set_hostile_selftest.py --root $R --tmpdir $T/runner` | 6/6; 0 | 6/6; 0 |
| freshness-sweep | `timeout --kill-after=5s 180s node scripts/freshness-sweep.mjs --selftest` | 35/35; 0 | 35/35; 0 |

Observed: 177/177 cases passed at each revision; case identities match for all five suites. Python suites reported clean/passed; freshness printed `selftest: 35/35 passed`. Only base-path emitted stderr: `45/45 fixtures passed` at both revisions. No timeout occurred.

## Deletions and unchanged prior surface
Commands ran from S/clone, with the Git environment above:
- `timeout 300 git diff --numstat $B $H` — exit 0; 192 entries, zero numeric deleted lines. Receipt: `E/diff-numstat.stdout:1-192`.
- `timeout 300 git diff --name-status --diff-filter=D $B $H` — exit 0, empty stdout: no tracked paths deleted.
- The 13 binary `-/-` numstat entries were individually checked with `timeout 300 git diff --name-status $B $H -- <those 13 paths>` — exit 0; every status A (new file), not a binary replacement/deletion. Exact argv: `E/binary-path-status.json:4`; statuses: `E/binary-path-status.stdout:1-13`.
- `timeout 300 git diff --exit-code $B $H -- scripts/link_preview_selftest.py scripts/link_preview_audit.py scripts/base_path_selftest.py scripts/base_path_audit.py scripts/citing_set_selftest.py scripts/citing_set_hostile_selftest.py scripts/citing_set.py scripts/freshness-sweep.mjs scripts/fixtures` — exit 0, empty stdout. All five prior runners, their audit/gate implementations, and every existing fixture were unchanged; passing counts were not obtained by deleting tests.
Deletions list: none (neither tracked files nor text lines).

## Evidence and provenance
All following paths are absolute via E above; raw stdout/stderr and individual command receipts are retained there.
- `E/comparison.tsv:1-6`: before/after table, SHA256 `62e5e1026acc31349569b1e4ebd9661fd582b561b1b57db8d7e0f444a2c651f8`.
- `E/test-commands.json:1-212`: expanded argv, cwd, revision, isolated environment, exit codes and cleanup, SHA256 `0bc3dcde149ec9ba1a580e7ad57176393b09b72ac386d3b40592701b6b3c5b86`.
- `E/diff-numstat.stdout:1-192`: SHA256 `a6ef72c88d87884ad1b7369fe0f52fc59bd13d2e47a250a68e8aaa7557653d16`.
- `E/evidence-sha256.stdout:1-27`: SHA256 index for comparison artifacts and every test stdout/stderr; `timeout 30 sha256sum <listed files>` exited 0 (exact argv in `E/evidence-sha256.json:4`).
- `E/{base,head}-<test-label>.stdout` and `.stderr`: originals; `.json` records each command and exit. Table and raw output locations are linked in `E/comparison.json:1`.
- `timeout 30 python3 --version` and `timeout 30 node --version` both exited 0: Python 3.14.8 and Node v26.12.0. No tools installed or updated.

## Advisory correction and limits
No fixable regression was demonstrated in these requested checks; no implementation correction is supported by this evidence. Smallest safe wording is “the five earlier selftest suites still pass unchanged, and no tracked deletions occurred,” not an unrestricted no-harm guarantee.
Impacted axes tested: prior publishing/audit operability and offline freshness behavior. Live publishing, network properties, newly added round-36 behavior, corpus-wide semantic weakening from appended prose, and other unassigned checks were not verified. No network fetch, judge, admission, or integration was performed; only this report was written in the lane.
