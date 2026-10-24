# ReviewV1Defects — independent re-derivation of the frozen v1 driver defects

Seat: `kake-r45.ReviewV1Defects` (leaf reviewer, operability/freshness lane). No commits, no
edits outside the scratch dir and this report.

## Verdict

All three named HIGH defect classes **fire today** on the frozen v1 driver
`.ufo/waves/round-44/c44_audit.py` (sha256 `8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75`).
No attacked defect failed to fire, so there is **no claim-breaking finding**: the probes
corroborate the C1 "before" premise (v1 accepts invalid receipt classes), not contradict it.

| Probe | Attack (item wording) | Driver exit | `ok` | Decisive credit | Result |
|---|---|---|---|---|---|
| A | exit-2 receipt with class `caughtBy` -> `semantic_witness` True | 0 | True | `witnessed=1/1`, row `exit=2` | **PASS (defect fires)** |
| B | note `"tool absent"` receipt -> witness True | 0 | True | `witnessed=1/1`, note carried on receipt | **PASS (defect fires)** |
| C | `--expect not-met` with exit-2 cannot-evaluate row -> expectation True | 0 | True | `notMet=1`, row `exit=2`, `caughtBy=[]` | **PASS (defect fires)** |
| D | end-to-end stale plant: counter SIGKILLed, receipt planted beforehand -> `ok=True` exit 0 | 0 | True | row `exit=-9 met=True`, planted mtime before run window | **PASS (defect fires)** |
| E | same, stamped `--expect witnessed` (planted witness + planted build) | 0 | True | `witnessed=1/1 build_met=1/1`, both rows `exit=-9` | **PASS (defect fires)** |
| F | live counter backdates its own receipt (`os.utime`, -5 s) -> v1 accepts; v2 rejects `stale_receipt` | 0 | True | receipt mtime outside run window | **PASS (defect fires)** |

Frozen bytes were identical at the start and end of the work and at both commits observed
during the wave:

```
$ git rev-parse HEAD
3b4c430ae9fa2cf505a7b20f70a34fadf35a065c      # first probes
7ed937843164cb24e4994cac1e82621ec65b5b3a      # final probes (L1 committed wave-1 spec)

$ git show 3b4c430ae9fa:.ufo/waves/round-44/c44_audit.py | sha256sum
8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75  -
$ git show 7ed937843164cb24e4994cac1e82621ec65b5b3a:.ufo/waves/round-44/c44_audit.py | sha256sum
8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75  -
$ sha256sum .ufo/waves/round-44/c44_audit.py
8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75  .ufo/waves/round-44/c44_audit.py
```

## Instrument (scratch copies only)

`/fast/scratch/hyaku/kake-r45/ReviewV1Defects/`

- `fake_counter.py` — adversarial counter implementing the documented CLI surface
  (`--root --classes --tool-file|--revision --out`) and receipt protocol. Each probe kind
  writes a receipt in the round-44 schema (`met`, `runs.<key>.equal`, `note`,
  `counterSha256`) and exits 0/1/2 exactly as the frozen counter documents. `stale*` kinds
  SIGKILL themselves before writing; `backdate` writes a valid receipt then sets its mtime
  five seconds into the past with `os.utime`.
- `probe_v1.py` — one fresh root (`controls/probe-control.py` with its real sha256), one
  `controls.tsv`, one fake counter per case; invokes the frozen driver as a subprocess;
  prints driver stdout/stderr/exit, credited rows, freshness evidence; then re-evaluates
  the receipt rows with the frozen driver's own `semantic_witness` / `expectation_ok`
  (imported read-only) so the verdict is not my paraphrase of its predicate.
- `probe-transcript.txt` (v1, all six probes), `probe-v2-transcript.txt` (same fixtures
  against the newly arrived v2).

Commands:

```
cd /fast/scratch/hyaku/kake-r45/ReviewV1Defects
python3 -B probe_v1.py all
PROBE_DRIVER=/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/c45_audit.py \
  python3 -B probe_v1.py all                     # secondary v2 check, same fixtures
```

## Verbatim decisive output (v1, all six probes)

```
PROBE A-exit2-class (exit2_class)  expect=witnessed
AUDIT probe-A-exit2-class classes=v5 classKeys=G1,G2 witnessed=1/1 notMet=1 build_met=1/1 ok=True counter=bfa539902155
  probe-control        G1         met=False caught=G1
  build#1 met=True equal=None
--- driver exit=0 ---
summary ok=True verdict='witnessed 1/1 notMet=1 build met 1/1' witnessed=1 notMet=1 errors=[]
row name=probe-control exit=2 met=False caughtBy=['G1'] error=None
frozen semantic_witness over receipt rows: ['probe-control']
frozen expectation_ok(witnessed)=True build=[{'run': 1, 'exit': 0, 'met': True, ...}]
=> DEFECT FIRED (driver exit 0, ok=True)

PROBE B-tool-absent (tool_absent)  expect=witnessed
AUDIT probe-B-tool-absent classes=v5 classKeys=G1,G2 witnessed=1/1 notMet=1 build_met=1/1 ok=True counter=bfa539902155
  probe-control        G1         met=False caught=G1,G2
  build#1 met=True equal=None
--- driver exit=0 ---
summary ok=True verdict='witnessed 1/1 notMet=1 build met 1/1' witnessed=1 notMet=1 errors=[]
row name=probe-control exit=1 met=False caughtBy=['G1', 'G2'] error=None
frozen semantic_witness over receipt rows: ['probe-control']
frozen expectation_ok(witnessed)=True build=[{'run': 1, 'exit': 0, 'met': True, ...}]
=> DEFECT FIRED (driver exit 0, ok=True)

PROBE C-expected-notmet (cannot_eval)  expect=not-met
AUDIT probe-C-expected-notmet classes=v5 classKeys=G1,G2 witnessed=0/1 notMet=1 build_met=0/0 ok=True counter=bfa539902155
  probe-control        G1         met=False caught=-
--- driver exit=0 ---
summary ok=True verdict='witnessed 0/1 notMet=1' witnessed=0 notMet=1 errors=[]
row name=probe-control exit=2 met=False caughtBy=[] error=None
frozen semantic_witness over receipt rows: none
frozen expectation_ok(not-met)=True build=[]
=> DEFECT FIRED (driver exit 0, ok=True)

PROBE D-stale-plant (stale)  expect=blind
AUDIT probe-D-stale-plant classes=v5 classKeys=G1,G2 witnessed=0/1 notMet=0 build_met=0/0 ok=True counter=bfa539902155
  probe-control        G1         met=True  caught=-
--- driver exit=0 ---
summary ok=True verdict='witnessed 0/1 notMet=0' witnessed=0 notMet=0 errors=[]
row name=probe-control exit=-9 met=True caughtBy=[] error=None
planted receipt marker='PLANTED BEFORE RUN' mtime_ns=1792812054501423622 run_window=[1792812055601624222,1792812055654194941] fresh=NO (planted before run)
frozen semantic_witness over receipt rows: none
frozen expectation_ok(blind)=True build=[]
=> DEFECT FIRED (driver exit 0, ok=True)

PROBE E-stale-witnessed (stale_witnessed)  expect=witnessed
AUDIT probe-E-stale-witnessed classes=v5 classKeys=G1,G2 witnessed=1/1 notMet=1 build_met=1/1 ok=True counter=bfa539902155
  probe-control        G1         met=False caught=G1
  build#1 met=True equal=None
--- driver exit=0 ---
summary ok=True verdict='witnessed 1/1 notMet=1 build met 1/1' witnessed=1 notMet=1 errors=[]
row name=probe-control exit=-9 met=False caughtBy=['G1'] error=None
planted receipt marker='PLANTED BEFORE RUN' mtime_ns=1792812055655703620 run_window=[1792812056755916902,1792812056831773084] fresh=NO (planted before run)
frozen semantic_witness over receipt rows: ['probe-control']
frozen expectation_ok(witnessed)=True build=[{'run': 1, 'exit': -9, 'met': True, ...}]
=> DEFECT FIRED (driver exit 0, ok=True)

PROBE F-backdated (backdate)  expect=blind
AUDIT probe-F-backdated classes=v5 classKeys=G1,G2 witnessed=0/1 notMet=0 build_met=0/0 ok=True counter=bfa539902155
  probe-control        G1         met=True  caught=-
--- driver exit=0 ---
summary ok=True verdict='witnessed 0/1 notMet=0' witnessed=0 notMet=0 errors=[]
row name=probe-control exit=0 met=True caughtBy=[] error=None
counter receipt verification/tools/probe-control.json mtime=1792812051880495136 run_window=[1792812056833267033,1792812056888879800] in_window=NO (backdated by the counter)
frozen semantic_witness over receipt rows: none
frozen expectation_ok(blind)=True build=[]
=> DEFECT FIRED (driver exit 0, ok=True)

TALLY: A-exit2-class: DEFECT FIRED | B-tool-absent: DEFECT FIRED | C-expected-notmet: DEFECT FIRED | D-stale-plant: DEFECT FIRED | E-stale-witnessed: DEFECT FIRED | F-backdated: DEFECT FIRED
```

(Elided in `build=[...]` only the `seed/equalRuns/ratios/receipt/error` keys already shown
as `...`; all other text is verbatim. Full transcript: `probe-transcript.txt`.)

## Findings by severity

### HIGH-1 — counter exit code is never part of credit (A, C, D, E)

`run_counter` opens `out` after `subprocess.run` regardless of the return code
(`c44_audit.py:48-61`). `score()` records `exit=code` but the only `error` it sets is one
where the receipt is missing (`:151-160`). The credit predicates never read `exit`:
`semantic_witness` (`:63-66`) uses only `met` and `caughtBy`; `expectation_ok`
(`:69-82`) uses only `met`/`error`; `ok` and the process exit follow at `:203`/`:222`.

Consequences, each reproduced: an exit-2 receipt with one class key is certified
`witnessed 1/1` and the driver exits 0 (A); an exit-2 cannot-evaluate receipt satisfies
`--expect not-met` and exits 0 (C); a SIGKILLed counter (`exit=-9`) whose receipt file
already exists is credited `met=True` (D) or even `witnessed=1/1 build_met=1/1` (E).

Reachability from the real counter, not only from fixtures: `rec["runs"][key]` is populated
inside the run loop (`c44_count_v5.py:1108`); any later `CannotEvaluate`/`Exception` calls
`finish(2)` with the earlier runs still present (`:1114-1119`). A control whose class run Gx
diverges before a later class/sandbox error therefore emits exactly probe A's shape: exit 2,
`note = "cannot evaluate: ..."`, `runs.Gx.equal = False`. v1 credits that as a class witness.

### HIGH-2 — receipt `note` is never inspected (B)

The real counter labels a missing candidate `note = "tool absent"` (`c44_count_v5.py:1113`)
and exits 1 (met False). In that state every run, including all class keys, has
`equal = False` (`:1079-1080` with `"cand" not in paths`). v1 has no note check, so probe B's
receipt is credited `witnessed 1/1` and the driver exits 0. This defect is **not** covered by
HIGH-1: the real `tool absent` receipt exits 1, which is inside any 0/1 exit rule; only the
note check can reject it. Reachable when the control file disappears or becomes unreadable
between the driver's sha256 check (`:146-149`) and the counter's `open(a.tool_file)`.

### HIGH-3 — no receipt freshness / run-window binding (D, E, F)

v1 never unlinks `tools/<name>.json` before running the counter, never checks whether the
file already existed, and never compares its mtime to the run window; `run_counter` simply
loads whatever file is at `out` after the subprocess (`:55-59`). Probe D plants a passing
receipt before the run and SIGKILLs the counter: driver exit 0, `ok=True`, row `exit=-9
met=True`. Probe E plants both a class-catch witness and `build-1.json`; the counter and the
build counter are both killed (`exit=-9`) yet the driver certifies `witnessed 1/1 build
met 1/1`, exit 0. Probe F is the same hole without a pre-existing file: a live counter that
writes a valid receipt and then backdates its mtime five seconds into the past is accepted
(receipt mtime `1792812051880495136` vs run window `1792812056833267033..1792812056888879800`).

No attacked defect failed to fire, so none of these is claim-breaking for the C1 "before"
premise.

## Honest-cohort context (static audit, not a rerun)

All 27 receipts under `.ufo/waves/round-44/verification/tools/` have `note: null`; the only
summary that records row exits is `verification/smoke-v4.json` with exit codes `{0: 26,
1: 1}`. None of the three defect classes was exercised by the round-44 credit run, which is
consistent with C1's "honest cohort certification unchanged" half while leaving the v1
acceptance predicate unsound exactly as the claim states.

## Secondary check against v2 (same six fixtures)

v2 `.ufo/waves/round-45/c45_audit.py` appeared at 00:17 during this seat; sha256
`5a342e29c7e872d992cfedc26de849c010d197bb82162e007a61a55d915c7051` at check time (the file
is mid-authoring; this is a snapshot, not the L1 matrix). All six fixtures are refused:

```
A: exit=1 ok=False errors=['probe-control:counter_error']   row exit=2
B: exit=1 ok=False errors=['probe-control:tool_absent']     row exit=1 note tool absent
C: exit=1 ok=False errors=['probe-control:counter_error']   row exit=2, --expect not-met
D: exit=2 no summary — refused: "output directory must be empty"
E: exit=2 no summary — refused: "output directory must be empty"
F: exit=1 ok=False errors=['probe-control:stale_receipt']   backdated live receipt
```

A/B/C show v2's error gating excludes the very rows v1 credited even though v2's row fields
still carry `met=False caughtBy=['G1']`; the frozen `semantic_witness` alone is still true on
those rows, so v2's safety lives in its error gating, not in that function. D/E are stopped
by the empty-output-directory guard before the window rule runs; F exercises the window rule
directly (`stale_receipt`). This corroborates C1's "after" premise at fixture level only.

## Residual risk and verification gaps

- Probes A/B/C are receipt-layer fault injection, not a full real-counter run. Their shapes
  are reachable per the source citations above (partial runs at `finish(2)`; `tool absent`
  path), but I did not execute the real 21-run counter to produce them end-to-end — the
  time-box did not allow a real sandbox run.
- D/E were pre-planted; against v2 they are refused by the empty-outdir guard, so the mtime
  rule was not the rejecting mechanism there. Only F tests the mtime rule with a live
  counter. A mid-run write after v2's empty-dir check and before its window end is not
  exercised here.
- `.ufo/waves/round-45/c45_matrix.py` exists (00:18) but I did not run
  `--stage before|after`; my probes are independent equivalents, not the round's counting
  command. The frozen claim's matrix remains L1's to produce.
- The `lsp` device is not present in this seat's tool inventory, so caller/definition
  checks were done by reading the two frozen files (228-line driver; counter tail), not via
  an LSP server. No server answered these files in this seat.
- No tool installs or upgrades were needed; pacman was not touched.

## Files written

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/w1/ReviewV1Defects.md` (this report)
- `/fast/scratch/hyaku/kake-r45/ReviewV1Defects/fake_counter.py`
- `/fast/scratch/hyaku/kake-r45/ReviewV1Defects/probe_v1.py`
- `/fast/scratch/hyaku/kake-r45/ReviewV1Defects/probe-transcript.txt`
- `/fast/scratch/hyaku/kake-r45/ReviewV1Defects/probe-v2-transcript.txt`
- 52 retained `probe_<label>_<rand>/` scratch roots (roots, controls tables, counter copies,
  receipts/summaries backing the transcript)

Nothing outside these paths was written; the frozen driver's sha256 is identical before and
after, at HEAD and in the working tree.
