# CriticQualityCriteria — round 30, wave 2 (falsify)

Target: `corpus/QUALITY.md:403-467`, section "Evidence identity, live-mode bounds and counter granularity — round 30" (blob `64edc83a` at `451e98f`). Axes: operability, freshness. I read the source of `scripts/freshness-sweep.mjs` (sha256 `a1aa79d1…8d8b`) and never ran it, nor `probe-delta.mjs` or `live_snapshot.py`. I made no network requests and installed nothing. Witnesses ran in a sandbox clone at `451e98f` with `TMPDIR` set to the sandbox. Outputs are in `/fast/scratch/hyaku/kake-r30/w2/CriticQualityCriteria/out/`.

## Bullet 1: live-mode bounds (`:411-425`)
The cited lines are correct: `:137-158` is `parseArgs`, `:590` the probe-delta spawn, `:603` the `systemctl` call, `:1025` the hard-coded `offline: false`, and `:1215` the `$HOME` fixture. The claims about fetch and `git ls-remote` carry no line pointer; the real sites are `:725`, `:744` and `:897`. The `/tmp` write is at `:1183`.

The offline list does not match the source:
1. **The list is too narrow, and contradicts its own next sentence.** `--section=paths` without `--offline` is just as safe, because `scanCitations` has no fetch and no spawn (the only `execFileSync` calls are at `:590`, `:603`, `:743`, `:896` and `:1190`). `--section=armed --offline` and `--section=plazir|pq14 --offline` are also offline: see `:739`, `:760`, `:786` and `:812-820`, where only the local `sitemap.xml` is read. The bullet's next sentence ("…unless `--offline` is given") concedes those last two, so "the only offline-safe invocations" contradicts itself.
2. **`--offline` can appear on the command line without taking effect.** At `:145` the code is `else if (a === '--repo') o.repo = argv[++i]`, so `--section=armed --repo --offline` stores the string `--offline` as the repo path and runs live. "Unless `--offline` is given" should read "unless `--offline` is parsed as a flag".
3. **The history claim is conditional, not unconditional.** "`--section=history` spawns … even under `--offline`" holds only when a probe-history file is readable. With the committed pins (`probeHistoryAbsent: true`) and `~/Projects/webzites/state/probe-history.jsonl` absent, the section returns at `:620-621`, before both spawns at `:658` and `:691`.
4. **`probe-delta.mjs` is not live-capable.** It imports only `node:fs` and `node:path` (`probe-delta.mjs:29-30`) and has no `fetch(` and no URL. "Three live-capable scripts" therefore overstates it. The witness docstring's "any mode reaches pinned repositories" is false from source.

The witness is weaker than the rule (`witness_sweep_live_mode.py:45`, sha256 `938c0f4d…`):
- Its `OFFLINE_FLAG` exempts `--section=history`, `--selftest` and bare `--offline`. Those are the very modes the bullet calls unsafe, because they spawn probe-delta or `systemctl`, or write to `/tmp` and `$HOME`.
- I committed a 13-line probe report in a scratch repo (`m1-probe.json`). The command `witness_sweep_live_mode.py --root <probe> --round round-99` exited 1 but flagged only the control line, line 1 (`--section=armed`). It missed these 12 lines:
  - `--section=history`, `--selftest`, bare `--offline`, and `--repo --offline`;
  - an `--offline` mentioned later on the same line;
  - `cd lane && node …`, a command with no verb, "have run", "Executed:", and "ran, not knowing better,";
  - an absolute tool path, and `./freshness-sweep.mjs`.
  "Limit: it finds reported runs only" understates this: it finds only runs reported in one sentence shape.
- **A wrong `<round>` spelling passes silently.** The placeholder is unspecified. `--round 29 --revision 234524c` exits 0 having scanned 0 files ("M1 holds"); only `round-29` works.
- Reproduced: `--round round-29 --revision 234524c` exits 1 with one hit at `.ufo/waves/round-29/w2/NoHarmExistingGates.md:30`, as stated. `--round round-30 --revision HEAD` exits 0.

## Bullet 2: receipt identity (`:426-436`)
- Reproduced: `witness_receipt_identity.py --root . --wave round-29 --revision 234524c` exits 1 with 7 receipts (3 anonymous, 4 partial), as stated.
- **Round 30 fails its own criterion.** `--wave round-30 --revision HEAD` (`451e98f`) exits 1. `.ufo/waves/round-30/r29-rerun/real-input/summary.json` is anonymous: its keys are `contractProblems, outRoot, sites, sitesRoot, tool, totals`. Its `tool` is the absolute path `/fast/scratch/hyaku/kake-r30/w1/ExecR29Receipts/clone/scripts/base_path_audit.py`, which is exactly the case the bullet names ("an absolute tool path is not a digest"). The wave-1 "exit 0 for round 30" was measured at `04637bd`, before this file landed.
- **The witness never scans the repair receipt.** `r29-rerun/receipt.json` is neither under `/verification/` nor named `summary.json`. Its revision and digests also sit under `provenance.*`, while the witness reads only top-level keys (`:79-84`).
- The receipt's values check out: `provenance.revision` is `4580c78…`, `base_path_audit.py` is `c5a13a32…1dc0`, `base_path_selftest.py` is `e6f21acb…7e4b`, and the self-test is 45/45. The real input has 3 sites, 114 references and 4 findings, with exits charter 1, lucario 0 and plazir 1, all equal to round 29.
- **The digest check is presence-only.** The rule says "every tool, counter, gate or runner". The witness passes on any one of `toolSha256|…|sha256` at the top level, including a bare `sha256` of anything. A receipt that depends on a counter, a gate and a runner but carries only `counterSha256` passes. The round-30 C1 receipts do carry all three (`c1-after-71c6bfa.json`), but the witness would not notice if they did not.
- **A wrong `<wave>` spelling passes vacuously.** `--wave 29` exits 0 with `receiptsScanned: 0`. The bullet writes `--wave <round>`.

## Bullet 3: named revisions have receipts (`:437-445`)
- **The report is unnamed and lives outside the lane.** The bullet says "the round-29 report" but gives no path. The path is `.ufo/reports/round-29/kake.md` in the fleet repo, not the lane, so `--report .ufo/reports/round-29/kake.md` against the lane exits 2. With the absolute fleet path, the witness exits 1 at `4580c78` and `04637bd` (unbacked `234524c` and `7697990`) and exits 0 at `451e98f`. The bullet's "until … are committed" has therefore already resolved, so its text is stale.
- **The witness does not read the report at `--revision`.** It reads the report from the working tree (`:52-58`), so the result depends on unpinned bytes.
- **The criterion fails at HEAD when applied to SCORECARD.** "Every revision a report or SCORECARD names" has no round scope. `--report SCORECARD.md --wave all --revision HEAD` exits 1 with 10 unbacked hashes. Four are not lane objects at all: `fb365e38`, `7c243a1d` and `964f443e` are sha256 or foreign-repo prefixes, and `e6bd071` is the ds4cc remote. The regex at `:25` takes any 7 or more hex characters on a line containing "measured".
- **Round 30's C2 receipt is not committed.** `verification/c2-after-451e98f.json` shows as `??` (untracked) in the lane. The SCORECARD does not name `451e98f` yet, but once it does, this bullet fails until the file is committed.

## Bullet 4: counter field comparison (`:446-458`)
- Reproduced: `witness_c2_field_comparison.py --root . --revision 234524c` exits 1. It finds `id, page, pagesChecked, referencesChecked, resolved` never compared, and mutant A still scores 30/30.
- **The criterion cannot discriminate.** The witness hard-codes `COUNTER = .ufo/waves/round-29/c2_matrix_count.py` (`:47`), which the bullet freezes, so it exits 1 at every revision, HEAD included. No repair can make it pass, and no round-30 counter (`strict_c2_counter.py`, `c1_reason_count.py`) is ever tested by this Fails-if.
- **The usage half has no failing condition.** Mutant B returns `usageCasePassedOnExitCodeAlone: true` at HEAD, but the exit decision at `:217` is only `never_compared or mutant_a_survived`.
- **The witness leaks scratch directories.** It never removes its `kake-r30-m4-run-*` directories (`:130`). There are 12 such directories in host `/tmp`, dated 2026-10-22 between 09:27 and 09:38, from some earlier run without `TMPDIR`. Running the Fails-if as written writes to `/tmp`.

## Bullet 5: status, "13 of 25 codes" (`:459-467`)
- **The counts are correct.** The fixtures name 13 distinct reasons: the eight round-28 codes, `document_duplicate_key`, `document_nonfinite_number`, `descending_range`, `span_too_large` and `document_shape_invalid` (one dump of all 41 `expected.json` files). The gate source emits 25 distinct codes: 21 `InputInvalid` literals including `document_not_utf8` (`citing_set.py:564`) and `corpus_file_not_utf8` (`:657`), the two JSON-profile constants (`:162-163`), and `descending_range` and `span_too_large` (`:678`, `:690`). The 12 uncovered codes match `SKILL.md:799-803`.
- **"Exactly" is observed, not asserted.** In `c1-strict-after-71c6bfa.json`, `failingCases == fixturesNamingCode` for all ten codes, but S2 itself tests only a subset (`c1_strict_checks.py:142`).
- **The three ungraded codes also hold.** I renamed `descending_range`, `span_too_large` and `document_shape_invalid` (8 sites) in sandbox copies, and each failed exactly its one naming fixture: 13, 14 and 16 respectively, runner exit 1. The baseline runner exits 0.
- **Nothing fails when the count drifts.** No committed command derives "25" or the list of 12. A new uncovered code would leave the text false while no check fires. The round-29 Fails-if (`:356-357`) fires only when zero fixtures name a reason, so the 12-code gap cannot fail anything.

## Smallest safe corrections (advisory)
1. **Bullet 1:** list the source-derived safe set (`--section=paths` with or without `--offline`; `--section=armed|plazir|pq14 --offline`; `--help`/`-h`). Say "`--offline` parsed as a flag", qualify the history spawns with "when a history file is readable", and drop probe-delta from "live-capable". Make the witness treat `history`, `--selftest` and bare `--offline` as non-offline, exit 2 on zero scanned files, and write `<round>` as `round-NN`.
2. **Bullet 2:** commit a revision and digest into `r29-rerun/real-input/summary.json`, or have the witness read `provenance.*` and scan `r29-rerun/`. Require one digest per dependency, and exit 2 on zero receipts.
3. **Bullet 3:** name the report's absolute fleet path, read it at a pinned revision, scope the check to a round, and commit `c2-after-451e98f.json`.
4. **Bullet 4:** take the counter as an argument and add mutant B to the exit condition. Remove the temporary directories, or point `TMPDIR` at a sandbox in the command.
5. **Bullet 5:** add a committed counter that derives the emittable-code set from the gate and fails on any code with no naming fixture, reporting it as a count so 12 is a measured value.

## Not verified
I did not run any freshness-sweep invocation, so the offline-safety claims are read from source only. I did not check that each of the 12 uncovered codes is reachable in practice. I did not mutate the inputs of `strict_c2_counter.py`.
