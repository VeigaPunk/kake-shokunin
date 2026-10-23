# ReviewHarmBaseline — r38 w1 harm baseline (axes: operability, freshness)

Godspeed axes: **operability** (every lane selftest and counter actually runs at the pinned
state, exit codes and pass counts recorded) and **freshness** (counters/keys run at their exact
pinned revisions; tools hashed to the exact base blobs). No clarifying questions; all runs
executed in one sandbox, parallel where independent.

## Setup
- Sandbox: `/fast/scratch/hyaku/kake-r38w1/ReviewHarmBaseline/` (clone, tmp, tools, runs).
- Clone pinned at declared commit `2dab7f3114f3e9dcf072b524c88816ab05fdfcf1`
  (`git clone -q` + `git checkout -q`, rev-parse verified; `git status --porcelain` = 0 lines).
- `git diff --stat af43a50f..2dab7f3 -- scripts/` is empty → selftests at the pin exercised the
  exact base tool content. No tool installs/updates were needed or made (host had python3
  3.14.8, git 2.56.0, bwrap 0.13.1, strace 7.2, timeout, prlimit). Every run:
  `timeout 900 prlimit --as=4000000000 python3 -B …`, cwd=clone, TMPDIR=sandbox tmp, GIT_* unset.

## baseline.json (deliverable)
- Path: `/fast/scratch/hyaku/kake-r38w1/ReviewHarmBaseline/baseline.json`
- sha256 `ca1ccae4bdacf7c4bdf7be07fcf68871b4935f1577e4f5c352b46272c3efd05f`
- Per run: command, cwd, exit, seconds, entry-script sha256, tool sha256(s), count pairs,
  summary lines, full log path. Raw logs: `/fast/scratch/hyaku/kake-r38w1/ReviewHarmBaseline/runs/*.log`.

## Runs (all exit/counts observed, none inferred)
| id | command (after `timeout 900 prlimit … python3 -B`) | exit | count | entry sha256 (first 12) |
|---|---|---|---|---|
| selftest-link-preview | `scripts/link_preview_selftest.py` | 0 (1.5s) | 46/46 | 699734bc2f20 |
| selftest-robots-audit | `scripts/robots_audit_selftest.py` | 0 (2.8s) | **137/137** | 01c61297987f |
| selftest-source-recheck | `scripts/source_recheck_selftest.py` | 0 (4.1s) | 106/106 | 9a5540045a32 |
| selftest-source-recheck-hardening | `scripts/source_recheck_hardening_selftest.py` | 0 (0.2s) | 6/6 | 6e922c73e684 |
| counter-round37-revmode | `.ufo/waves/round-37/sealed_count.py --root <clone> --revision af43a50f… --key-revision 424aa2480bcb…` | 2 | — (refused) | 2ebb39b585e2 |
| counter-round36-revmode | `.ufo/waves/round-36/sealed_count.py --root <clone> --revision af43a50f… --key-revision fd1fb723624b…` | 2 | — (refused) | 88ec59140258 |
| counter-round37-toolfile | `… sealed_count.py --root <clone> --tool-file tools/robots_audit_at_af43a50f.py --key-revision 424aa2480bcb…` | 0 (0.8s) | **28/28, met** (target 25) | 2ebb39b585e2 |
| counter-round36-toolfile | `… sealed_count.py --root <clone> --tool-file tools/source_recheck_at_af43a50f.py --key-revision fd1fb723624b…` | 0 (1.5s) | **28/28, met** (target 25) | 88ec59140258 |

Tool sha256 the runs exercised:
- `scripts/link_preview_audit.py` `59ad4f234c1bc9e26c60fdc6529cafafe4821bd6f44d8889206c7c6f5098ec45`
- `scripts/robots_audit.py` `944d2f51f396fb6e1ba3c7cf07112eb3f55d011e9bbc16bb1a59af517be1d3e5`
- `scripts/source_recheck.py` `4f8adbc23d314bbae9280190a83a2f985bfddb22d94b6135b133222818d47179`
- Base blobs re-materialized via `git show af43a50f:scripts/…` into
  `tools/robots_audit_at_af43a50f.py` / `tools/source_recheck_at_af43a50f.py`; their sha256 equal
  the blob hashes above (byte-identical), so the toolfile counter runs are exactly "at base".

## Finding 1 (operability, structural — affects how the L1 reads "counter at base/build")
Both counters REFUSE `--revision af43a50f…` with exit 2, `"error": "key visible at the measured
revision"` (logs `runs/counter-round3{6,7}-revmode-at-base.log`). Cause (counter source,
round-37 `sealed_count.py:191`, round-36 `:194`): in revision mode the counter aborts whenever
`show(root, rev, KEY_PATH)` is not None — the revealed round-36/37 keys are committed at base and
every descendant, so revision mode can never re-measure base or the r38 build. This is by design
("nothing measured can be a copy of the key"), not a defect. Consequence: the harm instrument
"round-37 counter 28/28 must hold at the build" is only obtainable via the counters' own
`--tool-file` mode on the build's tool file (as recorded above for base); a `--revision`-mode run
at the build will exit 2 for the same structural reason. The L1's build comparison should use the
toolfile rows as the baseline to beat.

## Harm numbers for the build comparison (baseline to beat / hold)
- `robots_audit_selftest.py` 137/137 and round-37 counter 28/28 (met) — both hold at base, matching
  the declared round-38 harm instruments; any C2 build must keep them.
- `source_recheck_selftest.py` 106/106, hardening selftest 6/6, link-preview selftest 46/46,
  round-36 counter 28/28 (met) — freshness side must not regress either.

## Not verified / out of scope (explicit)
- Round-38 counters (`sealed_count.py`, `sealed_count_v3.py`) NOT run — forbidden without the key;
  sealed trees `/fast/scratch/hyaku/kake-r38*/`, `kake-r38ctl/` never touched (this sandbox is
  `kake-r38w1/ReviewHarmBaseline`).
- No network fetches; no lane repo mutations (read-only git on the lane, all writes in sandbox).
- Counter `--revision` mode re-run against a pre-reveal ancestor was not attempted (out of scope;
  would not measure base).

Report: .ufo/waves/round-38/w1/ReviewHarmBaseline.md
