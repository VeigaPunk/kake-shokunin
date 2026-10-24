# AttackFixtureShapes — kill rule 5

Axes: **operability** (judged); freshness is the lane's other axis and is not regraded here.

**Named attack: PASS — counterexamples found. Fixture-fidelity requirement: FAIL.** The strongest counterexample is `fixtures/stale-backdate/fake_counter.py`: it emits a five-field, two-run receipt and exits 0 with `met=false`. That is not a receipt reachable from the real producer with only mtime changed. The counter-error fixture also combines authentic normal bytes with an impossible fresh handled-error `note`/exit pair. Tool-absent has the correct missing-candidate schema but retains reference-output hashes from the candidate-present RNG path. Stale-planted passes the historical-byte fidelity check.

This is a scoped attack result, not a canonical Rust judgment, admission decision, or re-declaration of the recorded C1/C2 state. No implementation or frozen files were changed.

## Field-by-field result

Paths below are relative to `.ufo/waves/round-45/fixtures/`. `caughtBy` is derived from false `runs[*].equal`; it is not a raw receipt field. Exit is the subprocess return code, not a raw receipt field.

| Fixture | seed | met / runs / derived caughtBy | counterSha256 | note / exit | Fidelity result |
|---|---:|---|---|---|---|
| counter-error | integer `224408754848177` | false; authentic 21 runs; G5,G7 | authentic v5 `5cedaa3b…`, not fake emitter's hash | null / 2 | **FAIL for fresh counter-error reachability.** Raw JSON is byte-exact real normal output, but both real handled exit-2 paths set a non-null `cannot evaluate:` note. It can represent stale bytes surviving an error, not the independent fresh error shape. |
| tool-absent | integer `224408754848177` | false; 21 false runs; all 21 keys caught | fake emitter's own `c697435a…` | `tool absent` / 1 | **PASS structural missing-tool shape; FAIL strict field-by-field recorded-seed provenance.** Genuine absent execution at this seed disagrees in 20 reference-output hashes. |
| stale-planted | integer `209150538233188` | false; authentic 21 runs; G2,G4,G9 | authentic historical v5 `5cedaa3b…` | null / -9 | **PASS historical receipt fidelity.** The old receipt remains byte-identical after SIGKILL. Its historical tool/counter identity differing from the invoked fixture is intentional, not false fresh provenance. |
| stale-backdate | integer `424242` | false; only G2 then A, each containing only `equal`; caught G2 | fake emitter's own `77aa39c7…` | null / 0 | **FAIL / strawman.** Fifteen top-level fields and nineteen run keys are missing; the run map is not a real producer prefix; normal false-met exit must be 1. |

Build coverage: all copied build fixtures in counter-error, tool-absent, and stale-planted are byte-identical to the real `after-final/build-1.json` (including seed `93543170178044`, `met=true`, 21 equal runs, null note, original v5 hash). Counter-error/tool-absent return 0 for builds; stale-planted returns -9 while leaving old build bytes. **Stale-backdate does not distinguish build calls: it emits the same false-met/exit-0 object for all three builds.**

## Producer invariants and strongest counterexample

Read-only sources:

- `.ufo/waves/round-45/w1/ScoutReceiptShape.md:16-85,166-184`.
- `.ufo/waves/round-44/c44_count_v5.py:981-1120`.
- `.ufo/waves/round-44/c44_audit.py:48-80,145-180`.
- All four fake-counter sources and the three existing fixture READMEs.

The real counter initializes **all 20 receipt fields before its evaluation try-block** (`:996-1003`). Error receipts retain those fields. Runs are inserted only at `:1108`, in A–F, G1–G10, T1–T5 order (`:1047-1050`), so a mid-loop failure leaves a prefix, never `{G2, A}`. Each completed comparison entry includes `values`, reference exit and hash, plus candidate comparison fields or the actual missing-candidate branch. Both handled-error paths set `note` before `finish(2)` (`:1114-1119`). Normal completion is `finish(0 if rec["met"] else 1)` (`:1120`).

The following decisive output came from an AST extraction in `functions.eval(language="py")` over the real source; the extraction printed the initializer keys, exception bodies, finish calls, and the run-insertion assignment:

```text
SOURCE_INVARIANT receipt_initialization_line=996 keys=20 predicate,met,ratioLimit,reps,revision,toolFile,label,seed,counterSha256,ref41Sha256,base40Sha256,classesMode,classRuns,toolSha256,equalRuns,equalValues,runs,ratios,ratiosExact,note
SOURCE_HANDLER line=1114 type=CannotEvaluate body=rec['note'] = 'cannot evaluate: %s' % ex; finish(2)
SOURCE_HANDLER line=1117 type=Exception body=rec['note'] = 'cannot evaluate: %s: %s' % (type(ex).__name__, str(ex)[:300]); finish(2)
SOURCE_FINISH line=1120 finish(0 if rec['met'] else 1)
SOURCE_FINISH line=1116 finish(2)
SOURCE_FINISH line=1119 finish(2)
SOURCE_RUN_INSERT line=1108 rec['runs'][key] = entry
```

Thus backdating is **not** the stale-backdate fixture's only synthetic behavior. This is a producer-shape failure, not merely a complaint that v1 ignores fields.

## Commands and decisive output

Working directory for shell commands: `/home/vgpnk/Projects/shokunin/kake-shokunin`.

Scratch setup:

```sh
mkdir -p /fast/scratch/hyaku/kake-r45/AttackFixtureShapes
```

Output: none; succeeded. The review helper was written only in that scratch directory. Its SHA-256 is `81028d1d90bb803cca3e5ea17cc88d34b3e15e3068a88ba1c5acb1515b2624ec`.

### Four emitter probes, byte provenance, and genuine absent/error paths

Exact executed command:

```sh
python3 -B /fast/scratch/hyaku/kake-r45/AttackFixtureShapes/probe_shapes.py --real-absent --real-error
```

The helper uses `TMPDIR=/fast/scratch/hyaku/kake-r45/AttackFixtureShapes/tmp` and `PYTHONDONTWRITEBYTECODE=1`, reads golden receipts, runs each fake with `--root <lane> --classes v5 --tool-file <fixture>/ctl1.py --out <scratch>/<fixture>.json`, and preplants only stale-planted's old control JSON. It additionally executes these real-counter commands (these are the exact printed argv):

```sh
/usr/bin/python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/c44_count_v5.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --classes v5 --seed 224408754848177 --tool-file /fast/scratch/hyaku/kake-r45/AttackFixtureShapes/does-not-exist.py --out /fast/scratch/hyaku/kake-r45/AttackFixtureShapes/real-absent.json
/usr/bin/python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/c44_count_v5.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --classes v5 --seed 224408754848177 --revision not-a-valid-revision-AttackFixtureShapes --out /fast/scratch/hyaku/kake-r45/AttackFixtureShapes/real-error.json
```

Selected decisive output, verbatim:

```text
COUNTER_V5_SHA256 5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc
PROVENANCE counter-error/control-receipt.json == tools/headtail-V1.json: True
PROVENANCE counter-error/build-receipt.json == build-1.json: True
PROVENANCE tool-absent/control-template.json == tools/headtail-V1.json: True
PROVENANCE tool-absent/build-receipt.json == build-1.json: True
PROVENANCE stale-planted/tools/ctl1.json == tools/buildport-m6.json: True
PROVENANCE stale-planted/build-1.json == build-1.json: True
PROVENANCE stale-planted/build-2.json == build-1.json: True
PROVENANCE stale-planted/build-3.json == build-1.json: True
FIXTURE counter-error exit=2 seed=224408754848177 met=False note=None caughtBy=['G5', 'G7']
  top_keys=20 missing=[] extra=[]
  counterSha256=5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc matches_invoked_bytes=False matches_real_v5=True
  equalRuns='19/21' equalValues=14957 receipt_unchanged=False mtime_in_call=True
  normal_finish_exit_consistent=False
FIXTURE tool-absent exit=1 seed=224408754848177 met=False note='tool absent' caughtBy=['A', 'B', 'C', 'D', 'E', 'F', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'T1', 'T2', 'T3', 'T4', 'T5']
  top_keys=20 missing=[] extra=[]
  counterSha256=c697435a11e732146a0a7e38756ab513209beeada88d063951dc65015d6723ef matches_invoked_bytes=True matches_real_v5=False
  equalRuns='0/21' equalValues=0 receipt_unchanged=False mtime_in_call=True
  normal_finish_exit_consistent=True
FIXTURE stale-planted exit=-9 seed=209150538233188 met=False note=None caughtBy=['G2', 'G4', 'G9']
  top_keys=20 missing=[] extra=[]
  counterSha256=5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc matches_invoked_bytes=False matches_real_v5=True
  equalRuns='18/21' equalValues=13477 receipt_unchanged=True mtime_in_call=False
FIXTURE stale-backdate exit=0 seed=424242 met=False note=None caughtBy=['G2']
  top_keys=5 missing=['predicate', 'ratioLimit', 'reps', 'revision', 'toolFile', 'label', 'ref41Sha256', 'base40Sha256', 'classesMode', 'classRuns', 'toolSha256', 'equalRuns', 'equalValues', 'ratios', 'ratiosExact'] extra=[]
  runs=2 order_matches=False missing_runs=['B', 'C', 'D', 'E', 'F', 'G1', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'T1', 'T2', 'T3', 'T4', 'T5'] sample_run_fields={'G2': ['equal'], 'A': ['equal']}
  counterSha256=77aa39c7eefa7b7cab366f42d141a49a72cea5060deca118e88a307b4cd9e129 matches_invoked_bytes=True matches_real_v5=False
  equalRuns=None equalValues=None receipt_unchanged=False mtime_in_call=False
  normal_finish_exit_consistent=False
REAL_ABSENT exit=1 seed=224408754848177 met=False note='tool absent' caughtBy=['A', 'B', 'C', 'D', 'E', 'F', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'T1', 'T2', 'T3', 'T4', 'T5']
  top_keys=20 runs=21 equalRuns='0/21' counterSha256=5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc
  fake_vs_real_deterministic_run_differences=20
  DIFF B.ref41OutSha256 fixture='48218aec68a48f978d5391535ab7ade2c3adbdd0f9eddaefcab6a98f3643037a' real='c14e019ad94012e1a588d278e542219e431fe3cc737fffabbfd10064865f8eb5'
REAL_ERROR exit=2 seed=224408754848177 met=False note="cannot evaluate: CalledProcessError: Command '['git', '-C', '/home/vgpnk/Projects/shokunin/kake-shokunin', 'rev-parse', '--verify', 'not-a-valid-revision-AttackFixtureShapes^{commit}']' returned non-zero exit status 128." runs=0 caughtBy=[] counterSha256=5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc
```

`matches_real_v5=False` is not independently counted as a defect for a fake's deliberately self-hashed receipt. Conversely, retaining the old real hash is correct historical provenance for stale-planted. The counter-error failure concerns its fresh receipt lifecycle, not denial that its copied JSON is authentic.

### Isolating tool-absent's chimera

Exact executed honest replay, with the same seed and byte-identical candidate:

```sh
env TMPDIR=/fast/scratch/hyaku/kake-r45/AttackFixtureShapes/tmp PYTHONDONTWRITEBYTECODE=1 python3 -B .ufo/waves/round-44/c44_count_v5.py --root . --classes v5 --seed 224408754848177 --tool-file .ufo/waves/round-45/fixtures/tool-absent/ctl1.py --out /fast/scratch/hyaku/kake-r45/AttackFixtureShapes/real-present.json
```

Verbatim stdout (process exit 1, the counter's expected not-met exit):

```text
{"label": "", "revision": null, "toolSha256": "00ece64886137a23b1b6a8e7f7795885d2e23ae3c1c2a0dfdb8f05f085503238", "equalRuns": "19/21", "ratios": {"T1": 1.075, "T2": 1.25, "T3": 1.463, "T4": 1.371, "T5": 1.107}, "met": false, "note": null}
```

A read-only `functions.eval(language="py")` comparison walked every run and compared `values`, `ref41Exit`, `ref41OutSha256`, `candExit`, `candOutSha256`, and `equal` against `control-template.json`; then it printed selected reference hashes. Decisive output:

```text
PRESENT_REPLAY seed=224408754848177 met=False note=None runs=21 caughtBy=['G5', 'G7']
PRESENT_VS_TEMPLATE_DETERMINISTIC_RUN_DIFFS []
REFERENCE_HASH B template=48218aec68a48f978d5391535ab7ade2c3adbdd0f9eddaefcab6a98f3643037a present=48218aec68a48f978d5391535ab7ade2c3adbdd0f9eddaefcab6a98f3643037a absent=c14e019ad94012e1a588d278e542219e431fe3cc737fffabbfd10064865f8eb5
```

A recursive keyset/type/array-length comparison between generated tool-absent and genuine absent receipts returned:

```text
ABSENT_STRUCTURAL_TYPE_AND_KEYSET_DIFFERENCES []
ABSENT_BRANCH_FIELD seed matches_genuine=True
ABSENT_BRANCH_FIELD met matches_genuine=True
ABSENT_BRANCH_FIELD classesMode matches_genuine=True
ABSENT_BRANCH_FIELD classRuns matches_genuine=True
ABSENT_BRANCH_FIELD toolSha256 matches_genuine=True
ABSENT_BRANCH_FIELD equalRuns matches_genuine=True
ABSENT_BRANCH_FIELD equalValues matches_genuine=True
ABSENT_BRANCH_FIELD ratios matches_genuine=True
ABSENT_BRANCH_FIELD ratiosExact matches_genuine=True
ABSENT_BRANCH_FIELD note matches_genuine=True
ABSENT_ALL_CAND_OUT_HASHES_ABSENT True
ABSENT_TIMING_CAND_CPU_EMPTY True
```

The fixture faithfully implements missing-candidate field presence/types, null tool hash, empty candidate CPU arrays, absent candidate output hashes, 0/21 aggregate and absent-tool note. But it copies reference outputs from the **present** path. Real code skips RNG-consuming candidate-file creation and candidate sandbox calls when absent (`c44_count_v5.py:1039-1045,1074-1080,1085-1089`), changing subsequent generated manifests. This is not just CPU-time noise: the honest present replay exactly matches all deterministic template run fields, while genuine absent execution differs in twenty reference hashes. Reference source was opened via `git show 1ef7a0e95f6884dd113fe583a997c633fe330ddd:scripts/sitemap_audit.py`; its emitter writes JSON, and its only date construction validates supplied year/month/day, not wall-clock time. The exact recorded-seed reference provenance is therefore not preserved by the synthetic transformation.

### Backdate is not a same-fixture certified-before leg

Exact executed commands (independent runs, separate scratch output directories):

```sh
python3 -B .ufo/waves/round-44/c44_audit.py --root . --controls .ufo/waves/round-45/fixtures/stale-backdate/controls.tsv --counter .ufo/waves/round-45/fixtures/stale-backdate/fake_counter.py --classes v5 --expect witnessed --build-rev 020bc457 --build-runs 3 --workers 1 --out /fast/scratch/hyaku/kake-r45/AttackFixtureShapes/v1-backdate/summary.json
python3 -B .ufo/waves/round-45/c45_audit.py --root . --controls .ufo/waves/round-45/fixtures/stale-backdate/controls.tsv --counter .ufo/waves/round-45/fixtures/stale-backdate/fake_counter.py --classes v5 --expect witnessed --build-rev 020bc457 --build-runs 3 --workers 1 --out /fast/scratch/hyaku/kake-r45/AttackFixtureShapes/v2-backdate/summary.json
```

Both driver processes exited 1. Verbatim decisive output lines:

```text
AUDIT kake-r44 classes=v5 classKeys=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 witnessed=1/1 notMet=1 build_met=0/3 ok=False counter=77aa39c7eefa
  witnessed-by-class ctl1 caughtBy=G2
  build#1 met=False equal=None 
  build#2 met=False equal=None 
  build#3 met=False equal=None 
AUDIT kake-r45 classes=v5 classKeys=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 witnessed=0/0 notMet=0 build_met=0/3 ok=False counter=77aa39c7eefa
  build#1 met=False equal=None stale_receipt
  build#2 met=False equal=None stale_receipt
  build#3 met=False equal=None stale_receipt
```

Read-only extraction of the resulting summaries:

```text
BACKDATE_SUMMARY v1-backdate {"ok": false, "witnessed": 1, "row_exit": 0, "row_met": false, "row_error": null, "build_met": [false, false, false], "build_exit": [0, 0, 0]}
BACKDATE_SUMMARY v2-backdate {"ok": false, "witnessed": 0, "row_exit": 0, "row_met": false, "row_error": "stale_receipt", "build_met": [false, false, false], "build_exit": [0, 0, 0]}
```

V2 does reach and reject the stale mtime branch, but the fake's docstring assertion that this fixture certifies `ok=True` under v1 is false for the matrix's witnessed-plus-three-build invocation. `.ufo/waves/round-45/c45_matrix.py:75-79` switches the before stale fixture to a different after fixture. This review does not rerun/restate the matrix totals; it establishes that the replacement fixture is not a faithful same-shape control for the stated attack.

## Smallest safe correction

1. **Stale-backdate:** derive receipts through real producer construction and its correct normal exits (not-met control exit 1; met build exit 0), preserving all fields/run entries. A scratch producer copy whose only behavioral intervention backdates the receipt in `finish` preserves the real paths and self-hash semantics; do not replace them with a hand-built minimal object. Exercise the same corrected fixture under both drivers, including passing builds. Only mtime should distinguish the stale leg.
2. **Counter-error:** use a genuine exception-state receipt after a class divergence, e.g. a controlled scratch fault at T1. Let the existing handler set the error note, retain the completed A–F/G prefix, and leave unfinished aggregates in their real state. Preserve honest passing build receipts. Do not relabel an untouched completed normal receipt as a fresh handled exit-2 result.
3. **Tool-absent:** source the complete receipt from the real absent branch at the recorded seed instead of retaining candidate-present reference hashes. Keep the already-correct absent-tool structural transformations. If self-hash isolation is required, derive it from the actual scratch producer being invoked rather than claim that a transplanted reference result re-derived.
4. **Stale-planted:** no fidelity correction indicated by this attack; retain its historical identities and byte-exact copies.

These are fixable evidence/fixture defects, not a demonstrated failure of the three v2 guard predicates. Accepting a schema-minimal simulator or weakening kill rule 5 would instead change the fidelity contract; that is not a repair this critic can authorize and belongs to the canonical judge/operator.

## Boundaries and unrun checks

Executed only the scoped fake-counter probes, one real missing-tool run, one real early-error run, one honest recorded-seed run, and the two backdate driver runs (including their fake-counter build calls). The early-error run validates error-note behavior, **not** a mid-loop class-witness error; a controlled T1-fault run is unrun. The control-disappears-between-driver-and-counter-opens race is unrun. No full matrix, cohort regression, compilation, lint, formatter, selftest, judge, admission, integration, commit, or push was invoked. No tools were installed or updated. No peer dependency was needed.

## Files written

Only lane write:

- `.ufo/waves/round-45/w2/AttackFixtureShapes.md` (this report).

Authored scratch helper:

- `/fast/scratch/hyaku/kake-r45/AttackFixtureShapes/probe_shapes.py`.

Generated scratch evidence under `/fast/scratch/hyaku/kake-r45/AttackFixtureShapes/`:

- `counter-error.json`, `tool-absent.json`, `stale-planted.json`, `stale-backdate.json`, `real-absent.json`, `real-error.json`, `real-present.json`.
- `v1-backdate/summary.json`, `v1-backdate/build-1.json`, `v1-backdate/build-2.json`, `v1-backdate/build-3.json`, `v1-backdate/tools/ctl1.json`.
- `v2-backdate/summary.json`, `v2-backdate/run-manifest.json`, `v2-backdate/build-1.json`, `v2-backdate/build-2.json`, `v2-backdate/build-3.json`, `v2-backdate/tools/ctl1.json`.

Created scratch directories, including `tmp/`; genuine counters created and automatically removed their transient randomized sandboxes beneath `tmp/`. No temp files were placed elsewhere by the review commands.
