# ScoutDoNothingControls — phase-4 claim-sizing (do-nothing controls)

Axes: **calibration** (a declared after-state must be unreachable by the cheapest control that skips the claimed work) and **no harm to junk** (an honest cohort stays green; mutants the old selftest already killed stay killed). Operability is C1's claim axis; freshness is C2's. Seat `kake-r45.ScoutDoNothingControls`. Lane files were not edited except this report. Scratch: `/fast/scratch/hyaku/kake-r45/ScoutDoNothingControls/`. No tools installed.

**Verdict on the named attack: the four skip-work controls cannot reach the declared after-states.** Two parts of those after-states are also unreachable by the repair as it stands today (C2 witness split; v2 selftest vs m4). Official counters `c45_matrix.py` and `c45_freshness.py` were absent, so the predicates below were applied directly. Those two commands are **unrun**.

## How a control is scored

Declared in `SCORECARD.md` "Round 45" (not re-declared here):

- **C1 MET** iff `invalid_accepted=0` and `rejections_named=3` and `honest_witnessed=27` and `honest_build_met=3`.
  `invalid_accepted` = how many of the three classes `{counter-error, tool-absent, stale-planted}` finish with summary `ok=true`.
- **C2 MET** iff `selftest_kills=4/4` and `v4_predicate_names_class_runs=false` and `witness_split=(22, 1, 4)`.
  `v4_predicate_names_class_runs` is true when the predicate text contains `class run`. The split is counted off `.rows[]` of the committed claim receipt: class-only = `met` is not true, `classCaught` non-empty, `legacyCaught` empty; mixed = both caught-lists non-empty; met = `met` is true.

A do-nothing control fails the after-state when any required component misses. Junk controls are not required to meet the after-state; they must stay green on the leg they are not supposed to break.

## Control table

| id | skips | program scored | observed | after requires | reaches after? |
|---|---|---|---|---|---|
| DN-C1-v1 | receipt-validity gate | frozen `c44_audit.py` sha `8ee2c8bf…0c75` (matches the declaration) | `invalid_accepted=3` (each class `ok=true`, audit exit 0); `rejections_named=0` | `invalid_accepted=0`, `rejections_named=3` | **no** |
| DN-C1-v2-unhardened | same gate, removed from the landed v2 | scratch copy of `c45_audit.py` with `receipt_validity` forced to `(True, None)`, the empty-cohort abort removed, and `os.mkdir(tools)` relaxed to `makedirs(exist_ok=True)` | `invalid_accepted=3`, `rejections_named=0` | same | **no** |
| DN-C2-selftest | the two new selftest rows | frozen v1 `--selftest` on MutClassGate m1–m4 (frozen selftest body kept) | kills **2/4** (m1, m3 exit 1; m2, m4 exit 0) | 4/4 | **no** |
| DN-C2-v5-v4 | mode-conditional predicate | committed v4 counter receipt `verification/claim/v4-final/tools/headtail-V1.json` (`classesMode=v4`, `classRuns=[]`, `equalRuns=11/11`, no G keys in `runs`) | predicate contains `the ten class runs` → `names_class_runs=true`. Same string on the v4 audit summary `v4-final/v4.json` | `false` | **no** |
| J-honest-v1 | (junk) must stay green | committed `verification/claim/after-final/after-v5.json` at `297aa62` (worktree matches HEAD; not re-run) | `ok=true`, `witnessed=27`, `notMet=27`, `build_met=3/3`, verdict `witnessed 27/27 notMet=27 build met 3/3` | green under v1 | **stays green** |
| J-honest-v2 | (junk) must stay green | full 27-control cohort under `c45_audit.py` | **unrun** (heavy; ExecRegressionHonest owns it). Shipped v2 `--selftest` exit 0, which still asserts the v1 honest in-memory rows | green under v2 | **not observed** |
| J-m1 | (junk) killed by both shipped selftests | m1 (`any`→`all` in `semantic_witness`) on v1 and on v2 | v1 exit 1, v2 exit 1 | killed by both | **holds** |
| J-m3 | same | m3 (v4 keys A–F count as class witnesses) | v1 exit 1, v2 exit 1 | killed by both | **holds** |

Expected before → after, from the declaration, against what was observed:

| leg | before (skip-work) | declared after | observed skip-work | observed landed repair |
|---|---|---|---|---|
| C1 invalid classes | v1 accepts 3/3 | v2 accepts 0/3, three named classes | v1 **3/3**; unhardened v2 **3/3** | intact v2: counter-error `ok=false` `counter_error`; tool-absent `ok=false` `tool_absent`; stale **aborts** before a row (`output directory must be empty`, exit 2). `invalid_accepted=0` but the stale class never emits `stale_receipt` |
| C2(a) selftest | 2/4 | 4/4 | v1 **2/4** | shipped v2 **3/4** (m4 survives, exit 0) |
| C2(b) v4 predicate | names ten class runs | names only the eleven v4 runs | v5 receipt **names them** (`classRuns` already `[]`) | v6 source has `PREDICATE_V4` without `class run` (`c45_count.py:85,997`). No v6 v4 receipt was produced here |
| C2(c) witness split | absent as a filed command | `22 class-only + 1 mixed + 4 met` | re-derivation of the committed receipt is **26 class-only + 1 mixed + 0 met** | same bytes; the repair does not edit this frozen receipt |

## Decisive output

Frozen v1 sha, then the three classes. Counter is a scratch fake that writes a class divergence (`runs.G5.equal=false`, `met=false`) and exits 2, or writes `note="tool absent"` on all 21 run keys and exits 1, or SIGKILLs after receipts were planted. Build side is `met=true` except the stale class, whose build rows are the planted files and whose subprocess exit is `-9`.

```text
V1_SHA 8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75
V1_SHA_MATCH True
RUN c44_audit.py counter-error audit_exit=0 ok=True witnessed=1 row_exit=2 caught=['G5'] build_met=[True, True, True] build_exit=[0, 0, 0] errors=[]
STDOUT counter-error AUDIT counter-error classes=v5 classKeys=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 witnessed=1/1 notMet=1 build_met=3/3 ok=True counter=3fa60cec2d23
RUN c44_audit.py tool-absent audit_exit=0 ok=True witnessed=1 row_exit=1 caught=['A','B','C','D','E','F','T1','T2','T3','T4','T5','G1',...,'G10'] build_met=[True, True, True] build_exit=[0, 0, 0] errors=[]
STDOUT tool-absent AUDIT tool-absent ... witnessed=1/1 notMet=1 build_met=3/3 ok=True counter=79726c5abc97
RUN c44_audit.py stale-planted audit_exit=0 ok=True witnessed=1 row_exit=-9 caught=['G5'] build_met=[True, True, True] build_exit=[-9, -9, -9] errors=[]
STDOUT stale-planted AUDIT stale-planted ... witnessed=1/1 notMet=1 build_met=3/3 ok=True counter=8890555847e3
C1_SCORE driver=v1 invalid_accepted=3 named=[] honest_witnessed=27 honest_build_met=3 C1_MET=False
```

Same three classes on the unhardened v2 copy (hardening removed, everything else from landed `c45_audit.py`):

```text
RUN v2_hardening_removed.py counter-error audit_exit=0 ok=True witnessed=1 row_exit=2 caught=['G5'] build_exit=[0, 0, 0]
RUN v2_hardening_removed.py tool-absent audit_exit=0 ok=True witnessed=1 row_exit=1
RUN v2_hardening_removed.py stale-planted audit_exit=0 ok=True witnessed=1 row_exit=-9 build_exit=[-9, -9, -9]
C1_SCORE driver=v2_unhardened invalid_accepted=3 named=[] honest_witnessed=27 honest_build_met=3 C1_MET=False
```

Intact landed v2 (not a do-nothing control; shows the gate is what the skip removes):

```text
RUN c45_audit.py counter-error audit_exit=1 ok=False witnessed=0 row_exit=2 errors=['counter_error', 'ctl1:counter_error']
RUN c45_audit.py tool-absent audit_exit=1 ok=False witnessed=0 row_exit=1 errors=['ctl1:tool_absent', 'tool_absent']
RUN c45_audit.py stale-planted audit_exit=2 ok=None
STDERR c45_audit.py: error: output directory must be empty: .../runs2/v2_intact/stale-planted/out
C1_SCORE driver=v2_intact invalid_accepted=0 named=['counter_error', 'ctl1:counter_error', 'ctl1:tool_absent', 'tool_absent'] C1_MET=False
```

`C1_MET` is false for intact v2 as well: stale never becomes a `stale_receipt` row, and `honest_witnessed` under v2 was not run. `invalid_accepted` alone is 0.

Selftests. Mutants are the MutClassGate reconstructions (m1 `any`→`all`; m2 timing keys T1–T5; m3 v4 keys A–F; m4 `if row.get("error"): return True`), applied to scratch copies. Frozen selftest body on v1; shipped selftest body on v2.

```text
SELFTEST v1 m1 exit=1 killed=True last=AssertionError
SELFTEST v1 m2 exit=0 killed=False last=SELFTEST PASS: class and mixed-key witnesses pass, legacy/timing-only and no-class witnesses fail
SELFTEST v1 m3 exit=1 killed=True last=AssertionError
SELFTEST v1 m4 exit=0 killed=False last=SELFTEST PASS: class and mixed-key witnesses pass, legacy/timing-only and no-class witnesses fail
SELFTEST_KILLS v1 2/4 ['m1', 'm3']
SELFTEST v2 m1 exit=1 killed=True last=AssertionError
SELFTEST v2 m2 exit=1 killed=True last=AssertionError
SELFTEST v2 m3 exit=1 killed=True last=AssertionError
SELFTEST v2 m4 exit=0 killed=False last=SELFTEST PASS: v1 assertions plus timing-only, invalid receipt, error-row, and build-count gates
SELFTEST_KILLS v2 3/4 ['m1', 'm2', 'm3']
```

Unmutated:

```text
SELFTEST PASS: class and mixed-key witnesses pass, legacy/timing-only and no-class witnesses fail
V1_EXIT:0
SELFTEST PASS: v1 assertions plus timing-only, invalid receipt, error-row, and build-count gates
V2_EXIT:0
```

m4 survives v2 because `expectation_ok` returns false on `_valid=false` before `semantic_witness` runs (`c45_audit.py:115-116`), and no assert says `semantic_witness` is false for a row that carries `error`. The new timing-only row does kill m2.

Witness split of the committed claim receipt (HEAD `297aa62`, `git diff --stat` empty):

```text
SPLIT_HIST classCaught>0,legacyCaught>0,metTrue -> count
  (True, False, False) 26
  (True, True, False) 1
HONEST_V1 witnessed=27 ok=True notMet=27 build_met=3/3 verdict=witnessed 27/27 notMet=27 build met 3/3
```

26+1+0=27. The declared `22+1+4` was the wave-2 critic's count when four rows had empty `classCaught` (`CriticC1Predicate.md` jq: 4 neither, 22 class-only, 1 mixed). Those four are class witnesses in the post-G6 receipt (22+4=26 class-only, mixed stays 1, met 0). Re-deriving the receipt the claim names does not produce 22/1/4, and the C2 repair is not allowed to edit that frozen file. Leg (c) of the after-triple is unreachable as declared.

v4 predicate (committed counter receipt, not a fresh counter run):

```text
V4_TOOL_NAMES_CLASS_RUNS True classRuns []
```

Predicate text: `met: the tool's exit code and output equal the round-41 tool's on every generated run (the eleven v4 runs and the ten class runs), and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's`.

## Commands

From `/home/vgpnk/Projects/shokunin/kake-shokunin` unless noted.

```text
python3 -B /fast/scratch/hyaku/kake-r45/ScoutDoNothingControls/score2.py
python3 -B .ufo/waves/round-44/c44_audit.py --selftest
python3 -B .ufo/waves/round-45/c45_audit.py --selftest
git diff --stat -- .ufo/waves/round-44/verification/claim/after-final/after-v5.json
git log -1 --format='%h %ci %s' -- .ufo/waves/round-44/verification/claim/after-final/after-v5.json
```

`score2.py` is the run that produced the tables above. An earlier `score_controls.py` run is void: the fake counter parsed `sys.argv` at import and then lacked `CLASS_MODULES`.

## Files written

- `.ufo/waves/round-45/w1/ScoutDoNothingControls.md` (this report)
- Scratch only: `score_controls.py`, `score2.py`, `v2_hardening_removed.py`, `mutants/`, `mutants2/`, `runs/`, `runs2/`

No lane instrument, fixture, receipt, or frozen file was written.

## Blockers and unrun checks

- `c45_matrix.py` and `c45_freshness.py` were not on disk. Official C1/C2 counting commands **unrun**.
- Honest 27-control cohort under driver v2 **unrun**.
- No fresh v5 or v6 counter execution. C2(b) is from the committed v4 receipt bytes plus a source read of `PREDICATE_V4`.
- Stale-vs-intact-v2 never reaches `receipt_validity`: the planted cohort is refused as a non-empty output directory. Whether that abort counts as the third named rejection is a matrix question, and the matrix is absent.
