# MutC2Counter — counter guard mutation probe

Axes: **operability** (guard sensitivity); **freshness** (pinned dependency integrity).
Scope: isolated clone at `4b089da699cfaaf5ebeb6a0746b7e4238602e20a`; 13 single-point counter mutants, 10 committed adversarial selftest inputs. C2 remains withdrawn; this is advisory evidence, not a round judgment.
`S=/fast/scratch/hyaku/kake-r37w1/MutC2Counter`; `C=$S/clone`; `B=4b089da699cfaaf5ebeb6a0746b7e4238602e20a`.

## Detector and results
The same bounded counter CLI ran on pristine, mutated, then byte-restored active copies. Detector compares exit, validFixtures, killed, met and survivors/error, excluding the deliberately changing counter digest. All pristine expected behaviors and all restoration comparisons passed. Counter exit 1 means expected not-met, not detector failure. The integrity detector explicitly expects rejection (exit 2) on corrupt dependencies; those baseline assertions passed, rather than failing operationally.
Table notation: **K/V** = killed tool mutants / valid fixtures. All ordinary counter exits were 1, met=false. Input names resolve to full commits and SHA256 in `inputs.json:1-52`; mutation source lines are in the pristine counter.

| Counter mutant | Input (commit prefix; deliberate defect) | Real → mutant output | Guard proven or equivalent |
|---|---|---|---|
| CM01: drop E2 validity, L281 | E1-only `2c1cc410`; uppercase HTTP URL, status 410 | 0/0 → 1/1 | Killed; E1-only validity inflates kills |
| CM02: drop E1 validity, L281 | E2-only `70e95317`; manifest version=true | 0/0 → 31/1 | Killed; E2-only validity inflates kills |
| CM03: ignore accepted exit list, L177 | wrong-exit-shapeless `d234b914`; expect exit 0 for 410, shape=false | 0/0 → 0/1 | Killed by valid-count detector; **no killed-count difference** |
| CM04: ignore alternative's exit, L199 | crossed-exits `68d5eb51`; correct findings paired only with wrong exit | 0/0 → 1/1 | Killed; alternatives must remain correlated |
| CM05: ignore verdict, L201 | wrong-verdict `9cce8991`; verdict="invented" | 0/0 → 1/1 | Killed |
| CM06: ignore findings projection, L203 | wrong-findings `f0485446`; 204 expects gone, body permits M03 to return clean | 0/0 → 1/1 | Killed |
| CM07: ignore checksEvaluated, L205 | wrong-evaluated `d19bc275`; expect 999 | 0/0 → 1/1 | Killed |
| CM08: ignore write check, L172 | compact `ec1811e2`; 410 + 404 | 2/2 → 2/2 | Survived; frozen-family equivalence argument below |
| CM09: ignore mutant SHA256, L250 | compact + shadow root replacing M01 bytes with E1 | exit 2, hash rejection → 1/2, exit 1 | Killed by integrity detector; unchanged dependencies gave 2/2 on both |
| CM10: ignore manifest pin, L239 | compact + shadow manifest containing 32 copies of M01 entry | exit 2, pin rejection → 32/2, exit 0, met=true | Killed; pin prevents duplicate-roster false success |
| CM11: omit moved target from projection, L135 | wrong-target `90d001c9`; expect wrong.example rather than /new | 0/0 → 2/1 | Killed |
| CM12: ignore reason vocabulary, L191 | empty-reasons `01fa977f`; REASONS=[] | 0/0 → 1/1 | Killed |
| CM13: ignore mutant count guard, L253 | compact `ec1811e2` | 2/2 → 2/2 | Survived; redundant after pinned manifest |

**Observed total: 11 killed, 2 survived, 0 inconclusive**, including CM03's validity-only difference and CM09/CM10's dependency-integrity extensions. Nine counter mutants changed fixture-data counts; the two integrity guards require dependency tampering to distinguish them.
[INFERENCE] CM08 is equivalent for the frozen E1/E2/M01–M32 family under normal I/O: these tools have no file-creation calls; their file accesses are reads, with writes only to stdout/stderr. Static call-site evidence is `io-call-sites.json:1-712` (E1/E2 at 1-39), plus retained pinned source. No arbitrary writer tool was tested; this survivor does not justify weakening the no-writes contract.
[INFERENCE] CM13 is equivalent while the manifest pin and constants remain intact: the pinned manifest already contains exactly 32 entries. Changing its length fails the earlier hash guard, assuming hash collision resistance. Neither survivor is permission to change the contract.

## Exact commands and exits
Setup: `mkdir -p "$S/tmp" && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 120 git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin "$C" && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 30 git -C "$C" checkout -q "$B"` — exit 0.
Full-base control, cwd C: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR="$S/tmp" timeout 900 /usr/bin/python3 -B .ufo/waves/round-37/c2_mutkill.py --root . --revision "$B" --jobs 2` — exit 1; 101/101 valid, killed 27/32; survivors M07/M08/M09/M11/M24 (session stdout).
`timeout 180 /usr/bin/python3 -B "$S/probe.py" prepare` — exit 0; 13 pristine copies and 10 input commits, retained under `refs/mutc2/*`; Git subprocesses unset inherited GIT_* and use timeout 30.
`timeout 600 /usr/bin/python3 -B "$S/probe.py" pristine` — exit 0; repeat with `mutated` after one-line edits and `restored` after their exact inverses — exits 0, 0. Each child uses `timeout 180 /usr/bin/python3 -B ACTIVE --root C --revision INPUT_COMMIT --jobs 1`.
`timeout 180 /usr/bin/python3 -B "$S/integrity.py" prepare` — exit 0; creates separate shadow roots, never changes clone dependencies.
`timeout 300 /usr/bin/python3 -B "$S/integrity.py" pristine` — exit 0; repeat with `mutated`, then `restored` around the same two one-line counter edits — exits 0, 0. Child counter exits were respectively (2,2), (1,0), (2,2).
`timeout 120 /usr/bin/python3 -B "$S/summarize.py"` — exit 0; 45 retained child executions checked. Exact per-execution argv and exit codes: `commands.json`; full stdout/stderr: `evidence/`.

## Evidence and restoration
- `/fast/scratch/hyaku/kake-r37w1/MutC2Counter/summary.json:1-13` — SHA256 `37c1b4272aa39520bdc69545c584423b07d2abaf1dd144b75f4bd98233d0435b`; full per-mutant outputs, verdicts, and before/mutant/restored digests follow.
- `/fast/scratch/hyaku/kake-r37w1/MutC2Counter/specs.json` — SHA256 `f1870e3bb709710a7bb285408e432bf9a8d3f37d725b77d8890fa7f593364e46`; exact one-point edits and all 13 mutant hashes. Specimens: `mutants/CM01.py` through `CM13.py`.
- `/fast/scratch/hyaku/kake-r37w1/MutC2Counter/inputs.json` — SHA256 `63d9ec6aa732417b7d032cd3021f66555561ab428ad1120678f445e8b8d4e16a`; absolute input directory is `$S/inputs/`, each variant is also committed at `scripts/source_recheck_selftest.py`.
- `/fast/scratch/hyaku/kake-r37w1/MutC2Counter/counter-mutants.patch` — SHA256 `349a7baa828c3a7550707e73a722b5a0a27cd1bd9b4b7400b48f02612bef203e`.
- `/fast/scratch/hyaku/kake-r37w1/MutC2Counter/hashes.json` — SHA256 `e3c18f658abb333f1f8d81282f63e1a454a49922f3318e8df4bff0efe007e5fe`; hashes every input, mutant, dependency-tamper specimen, command receipt and probe script.
- All 15 active counter copies restored byte-exact and rerun; before/restored SHA256 `d72e232e4d4f120b6b45139958c40e9364d44d3d902207c0705ac97c1b6d5cb6`. Clone counter never changed. Clone selftest remained `0ad5623b9bbfafccd0f9f558c927d90651fabb5da4fd003e9fa2e73c96d5e419`.
- Integrity evidence: `$S/evidence/integrity-mutated.json:1-52`; new shadow roots intentionally retain adversarial input bytes, not mutations to the clone. All started processes completed; no services remain.
No sealed-tree access, C1 counter run, network request, sibling edit, or lane edit other than this report. No builds/linters/general repository tests run. Python 3.14.8 and bubblewrap 0.13.1 were already installed; no tool installs/updates.
