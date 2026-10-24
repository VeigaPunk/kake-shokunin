# RerunAblations — round 36 falsification
Axes: operability (receipt reproducibility and detector discrimination); freshness is unchanged, with no live requests.
Result: all 36 committed ablations reproduce exactly; five of six additional contract-breaking reference mutants still meet the frozen predicate. This is a coverage finding, not a defect demonstrated in the shipped tool or a round-admission decision.
Paths: `B=/fast/scratch/hyaku/kake-r36w2/RerunAblations`; `L=/home/vgpnk/Projects/shokunin/kake-shokunin`; `W=$B/clone/.ufo/waves/round-36`. Commands below expand these variables; working directory for scoring was B.
Setup: `mkdir -p "$B/tmp" && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 240 git clone -q "$L" "$B/clone" && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 30 git -C "$B/clone" checkout -q f3a38bf8e68f6cee386125d34b5e95ac9b2df66e`; exit 0, no output.
Driver: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR="$B/tmp" PYTHONDONTWRITEBYTECODE=1 timeout --signal=TERM --kill-after=3 300 python3 -B "$B/probe_ablations.py"`; exit 0, 56.557 seconds recorded.
Repeated detector: `timeout --signal=TERM --kill-after=2 90 /usr/bin/python3 -B "$W/sealed_count.py" --root "$B/clone" --tool-file "$B/probe-area/probe.py" --key-file "$W/sealed/cases.json"`. Full argv, cwd, exit codes and stdout/stderr paths for all 103 runs are in commands.json (85 counter runs, 18 witness runs).
Execution was serial at the scorer boundary to honor the process cap. Pristine scored 28/28, exit 0; every one of 42 mutations was followed by exact-byte restoration and another 28/28, exit 0. No baseline failure or timeout occurred.
Prerequisites observed: `timeout 10 bwrap --version` → bubblewrap 0.13.1; `timeout 10 python3 --version` → Python 3.14.8; both exit 0. No installs or upgrades.
Expected frozen detector: `met: passed >= 25 of 28 sealed cases`; below 25 kills, otherwise survives, provided pristine/restored runs pass. Existing ablations were generated with exactly ablate.sh's environment prefix; none.py is the unprefixed reference.
Reference/slot before and restored SHA256: `665e879809d70681bc81c5481ed7a17ac001a073c46d3c8c437b4086dd825298`.
Counter before/after SHA256: `88ec59140258ce759107b7472fdd07a005b7c1bb8b3ba5218347e4518342ff8e`.
Key before/after SHA256: `44c94838f31af6740a3f1bb4123abe6cbb8df0bbdd3414de7acbb3838863ef1d`.

## Committed versus regenerated
All 36 rows match passed, complete perCase, met, toolSha256 and counterSha256. Each mutation exits 1 and is killed; the reference exits 0. Numbers are cases passed out of 28.
| Ablation | Committed | Regenerated | perCase |
|---|---:|---:|---|
| reference (none) | 28 | 28 | equal |
| a_none | 16 | 16 | equal |
| a_410err | 22 | 22 | equal |
| a_204ok | 24 | 24 | equal |
| b_none | 24 | 24 | equal |
| b_anywhere | 24 | 24 | equal |
| b_noresolve | 24 | 24 | equal |
| b_firstonly | 24 | 24 | equal |
| b_final | 24 | 24 | equal |
| c_raw | 16 | 16 | equal |
| c_nohead | 24 | 24 | equal |
| c_keepcomment | 24 | 24 | equal |
| c_keepscript | 20 | 20 | equal |
| c_keepstyle | 24 | 24 | equal |
| c_keeptemplate | 24 | 24 | equal |
| c_noentity | 19 | 19 | equal |
| d_exact | 23 | 23 | equal |
| d_casefold | 24 | 24 | equal |
| d_collapse | 24 | 24 | equal |
| d_nonfkc | 24 | 24 | equal |
| e_allhtml | 24 | 24 | equal |
| e_alltext | 24 | 24 | equal |
| e_casesens | 17 | 17 | equal |
| e_noxhtml | 22 | 22 | equal |
| f_utf8only | 24 | 24 | equal |
| f_nobom | 24 | 24 | equal |
| f_pylatin | 24 | 24 | equal |
| f_nounsupported | 24 | 24 | equal |
| f_noquote | 17 | 17 | equal |
| f_labelcase | 14 | 14 | equal |
| g_abort | 24 | 24 | equal |
| g_skip | 24 | 24 | equal |
| g_nourlcheck | 24 | 24 | equal |
| g_noloc | 24 | 24 | equal |
| g_noescape | 24 | 24 | equal |
| s_ctkey | 13 | 13 | equal |
| s_unsure | 24 | 24 | equal |

## Six additional ablations
Each changes one behavior-bearing site in the copied reference, not the shipped tool. Reference line numbers below are in `$W/sealed/ref.py`; exact diffs and full mutant hashes are retained in generated/ and mutations.json.
| New mutant / skipped rule | Score (counter exit); meets 25; verdict | Local witness: pristine → mutant → restored |
|---|---|---|
| x_manifest_clean: lines 127–128 return clean for invalid manifests | 28 (0); yes; survived | checks={} : 2/input_invalid → 0/clean → 2/input_invalid |
| x_version_unchecked: line 125 omits version equality | 28 (0); yes; survived | version=2, checks=[] : 2/input_invalid → 0/clean → 2/input_invalid |
| x_missing_body_unchecked: line 113 omits is_file guard | 28 (0); yes; survived | absent.html : 2/check_invalid → 1/no JSON, FileNotFoundError → 2/check_invalid |
| x_invalid_extra_finding: line 140 also emits quote_missing for invalid checks | 24 (1); no; killed | relative URL : 2/check_invalid → 2/check_invalid+quote_missing → 2/check_invalid |
| x_upper_subtree_kept: line 62 drops case-insensitive subtree matching | 28 (0); yes; survived | <SCRIPT>private</SCRIPT>, quote private : 1/quote_missing → 0/clean → 1/quote_missing |
| x_semicolon_required: line 64 decodes only semicolon-terminated references | 28 (0); yes; survived | <p>A &amp B</p>, quote A & B : 0/clean → 1/quote_missing → 0/clean |
Witness notation is exit/finding reasons; all targets are null. input_invalid/check_invalid reports say could-not-evaluate; quote_missing alone says failed-policy. All six witnesses distinguish mutation from pristine, with identical pristine/restored outputs; they run the same bubblewrap jail and bounded CLI each time.
The one newly killed mutant fails exactly k25–k28. Each of the five survivors passes every sealed case, not merely 25. No contract or key was changed.
Contract anchors: clone SCORECARD.md:1623–1629 and :1646–1651. Revealed make_cases.py:39–42 fixes every manifest at version 1/checks list; :84–112 uses lowercase ignored tags and terminated references; :187–203 has no missing-body check. The key has zero expected input_invalid findings and no absent 200 body paths.
Restoration: restoration-summary.json:2–16 records identical before/after reference, key and counter hashes, exact slot bytes restored, and 42 completed probes; restorations.json retains each before/mutant/after hash and restored receipt. Saved generated mutant files are evidence copies, not modified production sources.
Evidence: `/fast/scratch/hyaku/kake-r36w2/RerunAblations/comparison.json:1` and `/fast/scratch/hyaku/kake-r36w2/RerunAblations/summary.json:1` (comparison and aggregate results).
Evidence: `/fast/scratch/hyaku/kake-r36w2/RerunAblations/new-ablation-scores.json:1` (six scores plus actual pristine/mutated/restored witness reports and stderr).
Evidence: `/fast/scratch/hyaku/kake-r36w2/RerunAblations/commands.json:1` and `/fast/scratch/hyaku/kake-r36w2/RerunAblations/probe_ablations.py:1` (exact commands and reproduction driver).
Evidence: `/fast/scratch/hyaku/kake-r36w2/RerunAblations/mutations.json:2–36` (full mutant SHA256s and precise changed expressions).
Evidence: `/fast/scratch/hyaku/kake-r36w2/RerunAblations/restoration-summary.json:2–16` and `/fast/scratch/hyaku/kake-r36w2/RerunAblations/restorations.json:1` (restoration hashes and 42 restored detector results).
Not verified: production-tool behavior on these six witnesses, the 101-fixture selftest, live sources, or round acceptance. No network, sibling-source, lane Git/index, or jj mutations; the driver has no remaining child process. The only lane write is this report.
