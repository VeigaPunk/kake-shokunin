# Round-36 W1 — ExecCriterionVersionBump

Routed defect: round-35 closure defect 2 — v2 of that counter raised `C2_MAX_WORDS` 1500→2200 with no
scored control forcing it, and no check read the two files against each other. Built a two-file counter
comparator: exit 1 on any moved target/threshold/cap/pin/predicate, 0 when only code outside them changed,
2 on a read or parse error.

## Deliverable
`/fast/scratch/hyaku/kake-r36w1/ExecCriterionVersionBump/version_bump_check.py` (194 lines, stdlib only,
sha256 `9fba378e07bf42809cb69b317eca67ef25c2815466841ad679c0f408fc4a81aa`). Usage:
`python3 -B version_bump_check.py OLD.py NEW.py [--list]`. Landing (L1, I write no lane file but this report):
`cp /fast/scratch/hyaku/kake-r36w1/ExecCriterionVersionBump/version_bump_check.py "$L/.ufo/waves/round-36/criteria/version_bump_check.py"`.
Compared, by ast, never importing a counter:
- `scan()` l.107 — module-level `Assign`/`AnnAssign` to `^[A-Z][A-Z0-9_]*$`, plus module-level string
  constants whose value reads as a predicate; values via `ast.literal_eval` + `json.dumps(sort_keys=True)`
  (so dict order cannot fake a diff), else collapsed `ast.unparse` (`canonical` l.44).
- `doc_predicates` l.98 — the `met:` / `Declared target:` docstring lines (the frozen predicate as declared).
- `judge_literals` l.70 — every string literal in `judge`, `project`, `*_judge`: verdict labels and report
  fields the judge compares (`"moved"`, `"verdict"`, `"findings"`, `"exit"`, …).
- `met_expressions` l.81 — expressions assigned to `met`/`*_met` and every `"met":` value, so `passed >=
  TARGET - 5` is caught though no constant moved.
- `compare` l.133 prints `REMOVED`/`ADDED`/`CHANGED` with `[pin|target|cap|threshold|predicate|constant]`,
  exit 1 when any remains; `--list` dumps both inventories.

## Required run 1 — round 35, must name the cap
`timeout 60 python3 -B version_bump_check.py .ufo/waves/round-35/sealed_count_v1.py .ufo/waves/round-35/sealed_count.py` → **exit 1**
```
old /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-35/sealed_count_v1.py sha256 c4d58daea09d27a15f7792aae320cd56ac44dc1a6911307d6320f0a2c04349ef
new /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-35/sealed_count.py sha256 1b4d9d590b70f82c72e257006b77dc7232c43d7ccf1e5df51e892da2efb3469b
compared 16 constants (module-level UPPER_CASE plus docstring predicate lines), 8 judge predicate literals and 2 met expressions
differences: 1
CHANGED  [cap] constant C2_MAX_WORDS: '1500' -> '2200'
verdict: DIFFERENT - cap differs; a scored control must be named for each
```
Only the cap is named: the docstring prose edit ("1500 whitespace-separated words" → "2200 words"), the
new `clean()` and the `cites` tightening are code outside the scored constants; the other 15 constants are
identical (`inventory-r35.txt`).

## Required run 2 — round 36 v1 vs v3 (current counter)
`timeout 60 python3 -B version_bump_check.py .ufo/waves/round-36/sealed_count_v1.py .ufo/waves/round-36/sealed_count.py` → **exit 1**
```
old /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-36/sealed_count_v1.py sha256 28169d958bf38818127e247e62c0e0fe2d95223edeea44908e5c39b1d2979728
new /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-36/sealed_count.py sha256 88ec59140258ce759107b7472fdd07a005b7c1bb8b3ba5218347e4518342ff8e
compared 8 constants (module-level UPPER_CASE plus docstring predicate lines), 9 judge predicate literals and 2 met expressions
differences: 1
CHANGED  [pin] constant KEY_SHA256: '"a690d39e912cf641baa14f101f461e31304ac336c59a41c9689aacf91e02f9ca"' -> '"44c94838f31af6740a3f1bb4123abe6cbb8df0bbdd3414de7acbb3838863ef1d"'
verdict: DIFFERENT - pin differs; a scored control must be named for each
```
Reading: the only scored move is `KEY_SHA256`, the declared key version-2 re-freeze. `TARGET` 25, `CASES`
28, `TIMEOUT` 20, `PREDICATE`, the docstring `met:` line, both judge/project literal sets and both `met`
expressions are identical — no threshold, cap or predicate loosened. The counter names its forcing control
(`sealed_count.py:34-41`: pre-freeze `CtlShortcut` 17 of 28 passed bullets (e) and (f) without a body); I
confirmed the receipt rather than the prose: `.ufo/waves/round-36/verification/v2/control-CtlShortcut.json`
= `{cases 28, passed 17, target 25, met false}` (same tree's `verification/control-CtlShortcut.json` is 9 of
28 post-re-freeze). So exit 1 is a documented pin move, not a loosened condition; cite that receipt in the
criterion note.
## Falsifiers run (sandbox only)
| input | exit | reported |
|---|---|---|
| v1 vs `sealed_count_v2.py` (bubblewrap jail added, no constant moved) | 0 | `SAME` |
| v3 vs itself | 0 | `SAME` |
| `mutants/code.py` = v3 + unused helper | 0 | `SAME` |
| `mutants/target.py`: `TARGET = 20` | 1 | `[target] TARGET: '25' -> '20'` |
| `mutants/predicate_sentence.py`: `PREDICATE` 25→20 | 1 | `[predicate] PREDICATE` |
| `mutants/docline.py`: docstring `met:` 25→24 | 1 | `[predicate] constant __doc__[5]` |
| `mutants/judge.py`: `reason == "relocated"` | 1 | `REMOVED project:moved` / `ADDED project:relocated` |
| `mutants/met_slack.py`: `passed >= TARGET - 5` | 1 | `[predicate] met-expression met` |
| missing path / non-Python file | 2 | `cannot read` / `cannot parse` |

Limits: this catches moved constants, the docstring predicate, judge/project vocabulary and the `met`
expression. A loosening inside a condition body (`run_c1`/`run_c2`, e.g. dropping `url in c[1]`) moves no
compared item — a version-bump guard, not a counter re-review; and it cannot judge whether a pin move was
forced, only name it.
## Evidence
- `version_bump_check.py` (`9fba37…4a81aa`), `round35.out`, `round36.out`, `inventory-r35.txt`
  (`a4cfcc…16cab`), `inventory-r36.txt` (`4aa14f…575b9e`), `mutants/` under
  `/fast/scratch/hyaku/kake-r36w1/ExecCriterionVersionBump/`.
- Input hashes pasted above are the lane files read; no lane file written but this report; no git/jj run.
- Not verified: sealed counter not run (no key; `/fast/scratch/hyaku/kake-r36/` never listed, read or stat-ed); no network; no tool installed.
