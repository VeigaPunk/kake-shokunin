# ReviewRoutedDisposition — round 33, wave 2 (falsify)

Axis: operability (disposition honesty). Reviewed `corpus/lessons/round-33.md`
"Round-32 routed defects — disposition" at `0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0`
(seven rows, matching the seven routed items in `corpus/lessons/round-32-verifier-spotcheck.md:123-141`).
Evidence read from own clone at `/fast/scratch/hyaku/kake-r33/w2/ReviewRoutedDisposition/clone`
(`git checkout 0a0acfb`, exit 0) plus w1 receipts under `.ufo/waves/round-33/w1/` and
`verification/`. Rows checked by reading cited w1 reports and the tip source; sibling
receipts and mutants were not re-run.

## Row verdicts

1. **m3d/m3f/m3g survive — accurate, with two wording gaps.** `w1/ExecPinMutantsP7.md`
   supports the verdict: m3d/m3f setup-pin parts equivalent (victim `rev-parse` roots
   unchanged, `victimUnchanged: true`, receipts sha256s listed); m3f/m3g alter the h7b
   gate finding (`input_invalid/revision_not_found` → `root_not_repository_top_level`)
   while both exits are 2 → generic "exit mismatch" only.
   - LOW: the table attributes the gate-finding change to m3g alone; the evidence states
     m3f's ceiling removal produces the identical effect ("its gate-report effect is the
     same as m3g's"). The lane working tree already carries corrected wording; the row
     at `0a0acfb` reads as if m3f were observation-clean.
   - LOW: "killing m3g would need the harness to expose gate findings or codes per case"
     is half-stale — the hostile harness *already* exposes per-case `codeChecks`/`codes`
     (`scripts/citing_set_hostile_selftest.py:221-229`); what is missing is the runner
     populating `code` for gate-run refusals (it stays `null` outside setup refusals,
     `citing_set_selftest.py:568-604`). So the needed change is runner-side code
     propagation, not a new harness assertion channel. Carried-open verdict stands.

2. **refusal keyed on message text — accurate.** Runner emits per-case `code`
   (`citing_set_selftest.py:124-128,568-604`); guard raise carries
   `setup_commit_before_init` + "needs an earlier 'git_init'" (`:401-402`);
   apply-time re-check `setup_commit_without_repo` (`:529`); P6 spec h6 pins
   `reason_code` (`fixtures/citing-set-hostile/P6-commit-before-init/hostile.json:23`);
   strict supplement `c1_strict_supplement.py` exists (s1–s4); QUALITY criterion 1 at
   `corpus/QUALITY.md:569-588`.

3. **probe kill/timeout — accurate, minor label.** ReviewC1ProbeCode confirms repairs
   (kill gated on `guard_ok` ~line 163; `TimeoutExpired` → `timedOut` verdict) and lists
   six residuals: F1–F5 LOW + F6 "NOTE (latent)", so "six low residuals" slightly
   overstates. Named items match: F1 no git timeout, F2 missing-script crash exit 1,
   F4 harness-error-as-refusal. s4_layer (`c1_strict_supplement.py:128-131`) does
   distinguish an m3 run by code `setup_commit_without_repo`, supporting the coverage
   remark. QUALITY criterion supersedes `c1_m3_probe.py` (`QUALITY.md:585-588`).

4. **round-32 C2 counter — accurate except defect severity.** `c2_pin_count.py` exists
   with row-id/path/mode/section pins; ReviewC2CounterCode shows F1,F5,F6,F7 FIXED,
   F2/F3 partially fixed, F4 fence-blind `## ` split still present — "five of seven
   fixed" is a defensible (if compressed) count, F4 named correctly.
   - LOW: "new low defects N1–N5" understates N1, which the review rates **MEDIUM**
     (non-UTF8 SOURCES.md crash, exit 1 outside the {0,2} contract); N5 is
     unreachable/not-demonstrated.

5. **PROVINCE five hostile shapes — accurate.** `PROVINCE.md:133-138` appends
   "Round-33 frontier step" correcting line 122's "five" to six (P1–P6); append-only.

6. **concurrent selftest collision — accurate.** `--tmpdir` default is now a private
   `mkdtemp` under `DEFAULT_TMPDIR` (`citing_set_selftest.py:184,816-820`); receipts
   `verification/concurrency-base-5777d5a.txt` (3 of 4 failed) and
   `concurrency-after-1cf452e.txt` (0 of 4) match the row's numbers.

7. **round-31 item-3 lows — accurate.** `read_expected` OSError handled
   (`:582-585`); stray fixture-root entries now `cannot_evaluate`
   (`:739-744`); `GATE_VALUE_OPTIONS`/`GATE_OTHER_OPTIONS` duplication still present
   (`:161-162`), and the unlanded `w1/ExecDuplicatedOptionTables` patch.diff does
   `from citing_set import build_parser` lazily (patch.diff:43-44) — breaks a copied
   runner without a sibling `citing_set.py`, exactly as stated.

## Residual risk / gaps

- Mutants, concurrency, strict-supplement receipts verified as documents, not re-run.
- Row-1 mutants m3d/m3f/m3g definitions came from routed-item wording; the mutant
  diffs themselves were not inspected (in a sibling sandbox).
- No tooling installed; no network used; lane writes limited to this file.
