# SentinelHardening — round 37 wave 2

Axes: operability, freshness. Tested `scripts/source_recheck.py` at `79d3c780f9afb9bc013e3b13e73ee73e6a8ac13c` in an isolated clone. Source SHA-256: `37a8a8ef491db584b9d53b50020a8dacf824d2588b3f7ba2e5125c6d1c820e95`. No lane source files changed.

## Commands and measurements

Matrix command (exit 0; per-case child exits below):
`unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; export TMPDIR=/fast/scratch/hyaku/kake-r37w2/SentinelHardening/tmp; timeout 900s python3 -B /fast/scratch/hyaku/kake-r37w2/SentinelHardening/runner.py`

Each normal target was `/usr/bin/python3 -B /fast/scratch/hyaku/kake-r37w2/SentinelHardening/clone/scripts/source_recheck.py --manifest /fast/scratch/hyaku/kake-r37w2/SentinelHardening/cases/<fixture>`, inside a per-case `timeout` plus `measure_child.py` wait4 RSS sampler. The exact wrapper and manifest/fixture construction are in sandbox `runner.py:31-167`; memory-limit and timing implementation is `measure_child.py:8-58`. Every case completed without timeout. Time is wall seconds; memory is max RSS KiB. JSON column records validity, verdict, checks evaluated, and finding reason(s).

| Input (fixture path suffix) | Size / shape | sec / KiB | exit | JSON result |
|---|---:|---:|---:|---|
| `manifest_fifo/manifest.fifo` | FIFO | .0406 / 13956 | 2 | valid; could-not-evaluate, 0, input_invalid |
| `/dev/zero` as manifest | device | .0410 / 13464 | 2 | valid; could-not-evaluate, 0, input_invalid |
| `manifest_1g/manifest.json` | sparse 1 GiB | .0203 / 13992 | 2 | valid; could-not-evaluate, 0, input_invalid |
| `body_fifo/manifest.json` -> FIFO body | FIFO | .0203 / 13992 | 2 | valid; could-not-evaluate, 0, check_invalid |
| `body_dev_zero/manifest.json` -> body symlink `/dev/zero` | device | .0204 / 13968 | 2 | valid; could-not-evaluate, 0, check_invalid |
| `body_1g/manifest.json` -> sparse 1 GiB regular body | 1 GiB; 256 MiB address-space limit | .0424 / 15032 | 1 | **no JSON; stdout 0 bytes; uncaught MemoryError** |
| `unclosed_script_10000/manifest.json` | 80,000-byte body | .0809 / 13992 | 1 | valid; failed-policy, 1, quote_missing |
| `unclosed_script_50000/manifest.json` | 400,000-byte body | .0605 / 14760 | 1 | valid; failed-policy, 1, quote_missing |
| `unclosed_script_250000/manifest.json` | 2,000,000-byte body | .0807 / 17256 | 1 | valid; failed-policy, 1, quote_missing |
| `quoted_attrs_gt/manifest.json` | 2,315,000 bytes; quoted `>` and embedded tag-like text | .1811 / 28032 | 1 | valid; failed-policy, 1, quote_missing |
| `deep_html/manifest.json` | 60,000 nested `<div>` pairs; 660,000 bytes | .2010 / 23176 | 1 | valid; failed-policy, 1, quote_missing |
| `deep_json/manifest.json` | 1,600 nested arrays; 3,226 bytes | .0404 / 13720 | 2 | valid; could-not-evaluate, 0, check_invalid |
| `race_alias/manifest.json` | switch symlink alias at open | .0805 / 14980 | 0 | valid; clean, 1, no findings |
| `race_target/manifest.json` | replace resolved target with outside symlink at open | .0806 / 14980 | 0 | valid; clean, 1, no findings |

The 1 GiB fixtures are sparse (0 allocated blocks). Exact body-failure command: `timeout 12s python3 -B /fast/scratch/hyaku/kake-r37w2/SentinelHardening/measure_child.py 256 8 /fast/scratch/hyaku/kake-r37w2/SentinelHardening/cases/body_sparse_1g-detail.measure -- /usr/bin/python3 -B /fast/scratch/hyaku/kake-r37w2/SentinelHardening/clone/scripts/source_recheck.py --manifest /fast/scratch/hyaku/kake-r37w2/SentinelHardening/cases/body_1g/manifest.json` (exit 1); traceback ends at `source_recheck.py:586` with `MemoryError`.

## Findings and verdicts

1. **MEDIUM — body size is uncapped; operational failure. Verdict: wrong / defect confirmed.** A valid manifest pointing at an in-root regular 1 GiB body passes path validation. `evaluate_check` does unbounded `handle.read()` and catches only `OSError` (`scripts/source_recheck.py:583-589`); under a safe 256 MiB address-space cap this raises `MemoryError`, exits 1, and emits no JSON. Without a cap, hostile body data can force very large allocation and deny service. **Smallest remediation:** bounded body read (`MAX_BODY_BYTES + 1`), classify over-limit as a policy/input failure, and emit the normal JSON result.

2. **MEDIUM — resolved target still has a check/open symlink race. Verdict: wrong; containment claim overstated.** `body_path` checks `realpath`/`isfile` then returns a pathname (`:457-479`); `evaluate_check` later opens that pathname (`:583-586`). The deterministic interposer in sandbox `race_driver.py:15-28` swaps the resolved in-root `safe.txt` for a symlink to a file outside the manifest directory immediately before the open. The outside file contains the manifest's sole quote (`OUTSIDE_ONLY`); result is `clean`/no findings (exit 0), proving external bytes were read through the path. The separate alias-swap control is benign because the resolved target path is opened. Impact is a local-file quote-presence oracle for an attacker able to mutate the shared body directory during execution. **Smallest remediation:** open and validate the target as a descriptor with no-follow semantics, then read that same opened object after confirming it remains within the allowed root; do not re-resolve a pathname at open time.

3. **HTML complexity attack: quadratic behavior not reproduced at tested sizes; verdict: overstated for these shapes.** Three increasing runs of many unclosed `<script>` tags (80 KB, 400 KB, 2 MB) completed in .0605–.0809 s, max RSS 13,992–17,256 KiB, with normal JSON. Quoted-attribute/`>` input (2.315 MB) completed in .1811 s / 28,032 KiB; deep HTML (60,000 nested pairs) in .2010 s / 23,176 KiB. No hang, crash, malformed JSON, or obvious superlinear growth observed at these sizes. These are measured cases, not a proof for all input sizes.

4. **Special manifest nodes and deep nesting: holds for tested cases.** FIFO, `/dev/zero`, and 1 GiB manifest are rejected promptly with valid `input_invalid` JSON. FIFO and `/dev/zero` body paths are rejected as `check_invalid` without blocking. The 1,600-array manifest and 60,000-level HTML nesting both terminate with valid expected-policy/evaluation JSON; no crash or hang.

Evidence: source `scripts/source_recheck.py` at the commit and SHA above (`:37-40` manifest limit, `:457-479` path resolution, `:583-598` body read/evaluation, `:607-643` bounded manifest handling). Reproduction harness/fixtures: `/fast/scratch/hyaku/kake-r37w2/SentinelHardening/{runner.py,measure_child.py,race_driver.py,cases/}`. No tools installed or updated.
