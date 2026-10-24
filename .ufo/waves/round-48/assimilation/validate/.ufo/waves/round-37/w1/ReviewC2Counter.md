# ReviewC2Counter — round 37 wave 1 (operability)

I did not touch the sealed tree. Every write went to /fast/scratch/hyaku/kake-r37w1/ReviewC2Counter/ or to this report. No tools were installed.
Target: .ufo/waves/round-37/c2_mutkill.py, sha256 d72e232e…cb6 (= counterSha256 in the receipt). Reference: `1a16b8e3:scripts/source_recheck_selftest.py`, sha256 0ad5623b…e419. That file is the same at 4d5b3d55, 1a16b8e3, 621fb528 and 4b089da6; it was last changed in 4d5b3d5.

## Verdict
The judge in `run_fixture` (c2_mutkill.py:145-210) gives the same pass/fail as `run_case` (selftest:750-845) on all 101 fixtures for E1 and all 32 mutants. E1, E2 and the mutants are pinned. The base of 27 of 32 reproduces byte for byte. There are two small departures from a strict "frozen copy" and one wrong exit code on a fault path, listed under findings.

## Judge vs run_case, clause by clause
- Materialize: equivalent for this data. The counter adds an escape guard (:155) and accepts str bodies; run_case does neither (:739-741). No fixture escapes the box: g09 `../outside.html` lands inside box/w. Every file and raw value is bytes, and no manifest has leftover bytes or an `__b64__` collision.
- argv / `{manifest}`: same (:164-165 vs :753-757).
- Write detection: same outcome (fail). run_case adds a problem and keeps going (:771-774); the counter returns False (:172-173). Neither one catches in-place edits or writes outside the work tree. My probes "rewrites-manifest" and "writes-tmp" pass on both.
- Exit code in the accepted set (main fixture plus `accept`): same (:175-178 vs :776-787).
- `shape` false, or exit 64, means pass: same, and the order is the same (:179-180 vs :789-793).
- One JSON object: same pass/fail on valid UTF-8. They differ on two error cases: invalid UTF-8 and deep nesting (finding 1).
- version == 1: same. `true` and `1.0` pass on both (probed).
- findings is a list; each item is an object with a str reason in REASONS, check str-or-null, target str-or-null: same (:186-196 vs :805-820). The counter gets REASONS from the selftest under count (DUMPER :82), not from a frozen tuple (finding 2).
- Projection on (check, reason), plus target for moved: same (:122-138 vs :703-728). The counter's repr/default=repr branches cannot be reached once types are checked.
- Alternatives loop over exit, verdict (None = skip), findings, checksEvaluated (None = skip): same (:198-207 vs :828-843).
- 60 s timeout means fail: same. On OSError, run_case returns a fail (:769) while the counter raises (finding 3).
- Environment: the counter runs /usr/bin/python3 in bwrap with --clearenv and --unshare-all; run_case uses sys.executable and inherits os.environ. The counter is stricter: my "net-attempt" probe fails on the counter and passes on run_case. The contract says "no network", so this is acceptable.
- Extra clause that run_case does not have: a fixture is valid only when E1 and E2 both pass it (:281). This is by design.

## Pins
- E1: `git show 4d5b3d55…:scripts/source_recheck.py`, checked against 577b2d7d…0d48 (:57-58, :243-247). E2: 1a16b8e3…, checked against a5176fee…221f (:59-61). I recomputed both hashes and they match.
- Mutants: the manifest is pinned at 9300ad38…dbd4 (:56, :239). Each mutant's sha256 is checked against the manifest (:248-251). Mutants come from the `--root` working tree, not from `--revision`; the hashes make that safe.
- All 32 mutants are a single one-line replacement or deletion of E1 at the line and old/new text MutTool's manifest records (difflib, run in my sandbox). For M03 and M29 the manifest's old/new spans two lines, but only the first line changes.
- Probes: a tampered mutant gives exit 2 "mutant M05 sha256 differs". A tampered manifest gives exit 2 "manifest … differs from the pin". `--revision deadbeef` gives exit 2 "unresolved revision". The repo's root commit gives exit 2 "selftest absent at revision".

## Base re-run
`cd …/ReviewC2Counter/clone && TMPDIR=…/tmp timeout 900 python3 -B .ufo/waves/round-37/c2_mutkill.py --root …/clone --revision 621fb528 --jobs 8` (clone at 4b089da6)
- Exit 1. Ran 03:23:05Z to 03:23:21Z (16 s), Python 3.14.8, bubblewrap 0.13.1.
- Output: …/ReviewC2Counter/rerun1.json, sha256 cf1a8861…c03c. It is byte-identical to verification/c2-at-621fb528.json (`cmp` exit 0) and matches the stored exit code (1).
- Fixtures 101, valid 101, failedOnE1 [], failedOnE2 [], killed 27 of 32, met false, survivors M07 M08 M09 M11 M24.
- A second run from a copy of the clone (the restored control after the fault probes) was also byte-identical.
- Survivors match MutTool's selftest survivors exactly (MutTool-summary.json `survivors.selftest`). For all 32 mutants, killerCount and the first-8 killer names equal MutTool's selftest `failed` count and its failure case names.

## Findings by severity
1. Low (judge divergence only on errors). Invalid UTF-8 in stdout: the counter passes the fixture because it decodes with "replace" (:174), while run_case crashes with UnicodeDecodeError because it uses text=True with strict decoding (:765). JSON nested about 100k deep: the counter fails (catches RecursionError, :183) while run_case crashes. Neither case changes any count here: E1, E2 and all mutants produce valid output. But the docstring's "frozen copy" (:147) is not literally true. Probe: …/ReviewC2Counter/probe.py, sha256 708c1fce…4003.
2. Low. REASONS comes from the candidate selftest (:82, :270), not from a frozen tuple. A future selftest can widen it (fewer kills) or drop it, which makes every finding fail and every fixture invalid. I found no way to game the count with it: a valid fixture's expected findings already rule out reasons E1 does not emit. Still, freezing the round-36 8-tuple would make the judge fully frozen.
3. Low-medium (operability). A missing mutant file (I moved M05.py away in my copy) raises FileNotFoundError and exits 1 with nothing on stdout, where the docstring says 2 (:34). An OSError inside `run_fixture` (no handler at :167-171) would do the same through `ex.map`. A caller that reads only the exit code would take "cannot evaluate" as "not met".

## Residual risk and what I did not verify
- I did not run the selftest's own `main` on E1 or the mutants. Equivalence rests on clause reading, 10 probe tools, and the per-mutant match with MutTool's recorded selftest outputs.
- I did not test a tool that reads outside its jail, or the effect of load on the 60 s timeout (the whole run takes 16 s).
- Process 2125633 (`c2_mutkill.py --root . --revision 4b089da6 --jobs 2`) is not mine and I left it running.
