# MutCopyGuard — operability falsification
Axes: operability (primary: sensitivity, specificity, usable thresholds); freshness (local byte provenance only; no live-source assertion).
Sandbox/cwd `S=/fast/scratch/hyaku/kake-r39a3w2/MutCopyGuard`; source `W=/fast/scratch/hyaku/kake-r39a3w1/ExecCopyGuard`.
Read only W's guard/fixtures and its public W1 report; changed only S and this report. No sealed material or counter accessed.
Commands actually executed (all relative commands below use cwd S):
- `timeout 60s prlimit --as=4000000000 python3 -B generate.py` → 0; generated 14 comparisons, fixture bytes 56,102.
- `timeout 600s prlimit --as=4000000000 python3 -B attacks.py` → 0; 98 guard invocations, seven threshold profiles.
- `timeout 110s prlimit --as=4000000000 python3 -B record_phase.py pristine` → 0; same command with `mutated` → 1; with `restored` → 0.
- Each phase invokes the identical `timeout 90s prlimit --as=4000000000 /usr/bin/python3 -B /fast/scratch/hyaku/kake-r39a3w2/MutCopyGuard/detector.py`.
Exact expanded per-pair commands, exits, stdout, stderr and input hashes: `S/evidence/attempts.json`; phase receipts: `S/evidence/{pristine,mutated,restored}.json`.
Concurrency caveat: four guard workers were used; counting their timeout wrappers and parent processes can exceed the literal eight-OS-process ceiling. All synchronous child invocations finished; no services were started.

## Default outputs (ratio / longest run / matched; exit 0=CLEAN, 1=HIT)
01–09 compare against `fx/orig.py`; 10–11 against `copy_guard.py`; remaining rows name their comparator. These are derived-copy probes, not alleged independent production submissions.
| Candidate | Transformation / comparator | Ratio | Run | Matched | Exit / outcome |
|---|---|---:|---:|---:|---|
| fx/01_renamed.py | consistent identifier renaming | 1.000000 | 181 | 181 | 1 caught |
| fx/02_scoped.py | scope-specific local renaming | 1.000000 | 181 | 181 | 1 caught |
| fx/03_reordered.py | reverse two independent function declarations | .425414 | 19 | 77 | 0 evaded |
| fx/04_dead_prefix.py | one unreachable binding before imports | .657609 | 7 | 121 | 1 caught |
| fx/05_dead_suffix.py | 128 unreachable assignments after unchanged program | .483311 | 181 | 181 | 0 evaded |
| fx/06_interleave.py | unreachable assignment before each statement | .449057 | 7 | 119 | 0 evaded |
| fx/07_split.py | extract unchanged checks into two helper functions | .619289 | 21 | 122 | 1 caught |
| fx/08_compound.py | split/reorder/rename/interleave | .238411 | 9 | 72 | 0 evaded |
| fx/09_layout.py | AST-unparsed original: layout/comments | 1.000000 | 181 | 181 | 1 caught |
| fx/10_guard_prefix.py | full guard plus one unreachable binding | .504198 | 18 | 1081 | 0 evaded |
| fx/11_guard_interleave.py | full guard plus unreachable interleaving | .450182 | 11 | 1238 | 0 evaded |
| fx/indep_a.py | prior independent DP vs fx/indep_b.py | .337838 | 8 | 50 | 0 correct clean |
| fx/independent_numbers.py | new numeric sorter vs fx/independent_json.py | .784810 | 29 | 93 | 1 negative-control hit |
| fx/tiny_a.py | identical fx/tiny_b.py, eight tokens | 1.000000 | 8 | 8 | 0 intentional floor blind spot |
01–09 each preserved 27 exercised return/output observations (243 total); both new utilities executed successfully on different meaningful inputs. Full-guard variants were parsed/compiled, not behavior-equivalence tested.
## Threshold effects (other defaults: ratio .60, run 200, min-matched 40)
`--ratio 0.45` catches suffix padding and both full-guard variants, but still misses 03/06/08 and still flags the independent CLI pair.
`--ratio 0.75` loses prefix/split detections, still flags the CLI pair; `--ratio 0.90` clears that pair but catches only 3/11 non-tiny derived copies.
`--run 100` rescues suffix padding only; `--min-matched 0` additionally flags the eight-token identical pair, without rescuing the six default evasions.
`--min-matched 1000 --run 100` still HITs 01 with only 181 matches: run rule bypasses the floor; stdout simultaneously contains the floor note and `reasons:["run>=100"]`.
No tuning of these three monotone thresholds separates 03 from the independent CLI pair: the latter dominates 03 on ratio (.784810>.425414), run (29>19), and matches (93>77).
## Per attacked statement / source locations
**holds (tested scope):** rename/comment/layout protection, `W/copy_guard.py:8-14`, W1 report:48; 01/02/09 and the original renamed baseline are caught.
**overstated as general copy coverage:** `W/copy_guard.py:2,140-147,282-285`; 6/11 derived copies evade. `fx/03_reordered.py:6,15` moves only declarations; `fx/10_guard_prefix.py:29-30` adds only a dormant binding, yet first-use numbering shifts.
**overstated as provenance/specificity evidence:** W1 report:46-49; fresh hand-written unrelated CLIs hit through conventional argparse/JSON boilerplate (`fx/independent_numbers.py:7-20`, `fx/independent_json.py:7-20`). This is a constructed negative control, not external independent-authorship proof.
**holds:** documented scoring rule and exit meanings, `W/copy_guard.py:16-27,282-285,351`; all 98 outputs agree with that rule. Failures above concern usefulness, not miscomputed scores.
**wrong without qualification:** “Below the floor ... cannot decide the verdict,” `W/copy_guard.py:22-24`; the run override counterexample above contradicts that blanket wording. CLI help at :266 correctly limits the floor to the ratio rule.
**holds:** W1 report:58, “Threshold is policy, not proof”; higher ratio alone cannot resolve the measured dominance conflict. No contract change proposed.
## One implementation mutant and restoration
Mutant: isolated `S/copy_guard.py:282`, replace only `and` with `or`; source W was never edited.
Expected detector: original-vs-renamed must HIT (exit 1), independent DP pair must remain CLEAN (exit 0); detector exits 0 iff both hold.
Actual: pristine child exits [1,0], detector 0; mutated [1,1], detector 1; restored [1,0], detector 0. **KILLED**, not baseline-inconclusive. Mutant false-hit score remained .337838 / run 8 / matched 50.
Unchanged detector `S/detector.py` SHA256 `f205c2a9b96b12ebd44a04624eec6ba0369871ea7b262f128e9dc7f9fc15889b` in all three receipts.
Before `S/copy_guard.py` SHA256 `0e1b9d2c0d1f7abb030ae97db9b719efe1f26e78fb7005441519ed94e6bf21b1`.
Mutated SHA256 `c4672438639c9aa6a658bf68da009c8c3a3561610f3c8a1743c57c14c9c31f84`.
Restored S and untouched W both SHA256 `0e1b9d2c0d1f7abb030ae97db9b719efe1f26e78fb7005441519ed94e6bf21b1`; exact original-byte restoration evidenced by matching hashes and restored detector output.
Critical fixtures: `S/fx/03_reordered.py` SHA256 `b08f5b7252bf78b41d0dd78ac4e46aafb71c978b4db29bb5c440968bbb09b3bb`; `S/fx/10_guard_prefix.py` SHA256 `1af8584fedc1af3304ace601f4402cbf4274e5a73517559db364efc87720e306`.
Negative controls: `S/fx/independent_numbers.py` SHA256 `759c69daaf170f896cc27ec4deb1a7580683d2e2cd69b14a942d7e25a3e30cbf`; `S/fx/independent_json.py` SHA256 `ba7836628e0e69639cb0c8d13c7375872790b4a93084e3cdc6608efb92a11c28`.
`S/evidence/attempts.json` SHA256 `15ce04934a0515bf2ae04d000302c9e35357b67358f8696089eb3da6db924ce0`; all fixture hashes in `S/evidence/fixture-sha256.json`, SHA256 `9e1038a74f06860a992a9b28249ab718219a95dc22c48787a1f8433815c6b7eb`.
No network, installs, repository/index mutations, or additional runtime. This report assesses only the copy guard, not sitemap C1 correctness or the round verdict.
