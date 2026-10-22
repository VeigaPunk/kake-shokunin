# RunNoHarmSuites — C1 no-harm suites at base vs repair

Seat: `KakeR28a3.RunNoHarmSuites` (leaf; no subagents, no labrat spawned).
Assignee: run existing lane test suites at base `22c1669c1fec83d1a0769de6b9ce686c75657e66` and repair `b5d423fc02057f67a6f3a255808313ce40d29069` in a scratch clone; name differences.
No tool installs were performed (nothing needed; tooling directive has nothing to record).

## Environment

- Sandbox clone: `/fast/scratch/hyaku/kake-r28a3/w1/RunNoHarmSuites/clone` (`git clone -q` of the lane; `git checkout -q --detach` per revision; working tree ended clean — `git status --porcelain` empty).
- `python3` 3.14.8, git 2.56.0.
- `TMPDIR` not exported; scratch directed via each instrument's own channel (`--tmpdir`, `KAKE_R27_SCRATCH`). `oracle_selftest.py` hardcodes temp root `/fast/scratch/hyaku/kake-r27` (instrument-internal; directory created there; disclosed).
- No network use. All suites ran offline. The only file written inside the lane repo is this report.

## Suites and commands (identical at both revisions)

Instrument files are byte-identical across the two revisions: `git diff --name-only 22c1669..b5d423f` under `.ufo/waves/round-27/` and `scripts/` shows only `scripts/citing_set.py` changed. So the same test harness ran at both.

1. `python3 -B scripts/citing_set_selftest.py --root . --tmpdir /fast/scratch/hyaku/kake-r28a3/w1/RunNoHarmSuites/tmp` → exit 0 at both revisions
2. `python3 -B scripts/citing_set.py --selftest --root .` → exit 0 at both revisions
3. `python3 -B .ufo/waves/round-27/git_name_selftest.py --gate "$PWD/scripts/citing_set.py" --tmpdir /fast/scratch/hyaku/kake-r28a3/w1/RunNoHarmSuites/tmp --json` → exit 0 at both revisions
4. `KAKE_R27_SCRATCH=/fast/scratch/hyaku/kake-r28a3/w1/RunNoHarmSuites/tmp/privacy python3 -B .ufo/waves/round-27/privacy_selftest.py` → exit 0 at both revisions
5. `python3 -B .ufo/waves/round-27/oracle_selftest.py --kind c1 --source-root "$PWD"` → exit 0 at both revisions
6. `python3 -B .ufo/waves/round-27/oracle_selftest.py --kind c2 --source-root "$PWD"` → exit 0 at both revisions

## Results matrix

| Suite | Base 22c1669 | Repair b5d423f | Delta |
|---|---|---|---|
| citing_set_selftest | exit 0; verdict clean; 29/29 cases; failed 0; contract minimum met | exit 0; verdict clean; 29/29; failed 0 | none (results identical) |
| citing_set builtin `--selftest` | exit 0; verdict clean; 29/29; failed 0 | exit 0; verdict clean; 29/29; failed 0 | none |
| git_name_selftest | exit 0; clean; 30/30; failed 0 | exit 0; clean; 30/30; failed 0 | none |
| privacy_selftest | exit 0; 9/9; failed 0 | exit 0; 9/9; failed 0 | none (log bytes identical) |
| oracle_selftest c1 | exit 0; 14/14; failed 0 | exit 0; 14/14; failed 0 | none |
| oracle_selftest c2 | exit 0; 3/3; failed 0 | exit 0; 3/3; failed 0 | none |

Runner identity: `scripts/citing_set_selftest.py` sha256 `3c167895c7f3a4acf531886816bffcbf189d299d6137ca12096265855dd62a1c` at both revisions. Gate under test changed as expected: sha256 `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228` → `28ba996524b444b2e1c23e3751f3fa662a9a44adbfcb6337a0d23fcebaf8f415`; git blob `scripts/citing_set.py`: `352a471abec08daa56a0fb7ef23fe78f2930d773` → `c26fcd498f1974265e6bb80dca8e102f57eb7b5f`.

Named differences: outcome-level, zero — every suite passes identically at both revisions. The only delta exercised by these suites is `scripts/citing_set.py` itself (+73/−13 in diffstat). The other base→repair changes (`.ufo/waves/round-28/c1_interface_count.py`, `c2_source_count.py`, `verification/c1-before.json`, `verification/c2-before.json`, `SCORECARD.md`) are not exercised by any of these suites.

## Evidence pointers (saved run logs, sha256)

- Base: `logs/base/citing_set_selftest.json` `2b8612f…` ; `logs/base/citing_set_builtin.json` `2b8612f…` ; `logs/base/git_name.json` `bf67d751…` ; `logs/base/privacy.json` `4acde372…` ; `logs/base/oracle_c1.json` `159e900f…` ; `logs/base/oracle_c2.json` `7585cc61…`
- Repair: `logs/repair/citing_set_selftest.json` `8a3d9ce…` ; `logs/repair/citing_set_builtin.json` `8a3d9ce…` ; `logs/repair/git_name.json` `1ba858e8…` ; `logs/repair/privacy.json` `4acde372…` (identical to base) ; `logs/repair/oracle_c1.json` `437c236c…` ; `logs/repair/oracle_c2.json` `c054c8d0…`
- Full paths: `/fast/scratch/hyaku/kake-r28a3/w1/RunNoHarmSuites/logs/{base,repair}/…`
- The first transcript pass (before logs were persisted) reproduced these results exactly; base was re-run only to persist evidence files, and agreed byte-for-byte on summaries.

## Risks / blockers

- `oracle_selftest.py` writes its disposable clones under the instrument-fixed `/fast/scratch/hyaku/kake-r27` (outside my designated subdir); that directory was created and otherwise untouched. No lane repo state was mutated.
- Not verified: any suite beyond the six mandated; no falsifier/gate runs (parent-owned per bounds); no network-enabled probes of any kind.

No blockers. Verdict for L1: repair commit introduces no harm to the existing lane test suites — all green at both revisions, with identical outcomes and the same harness.
