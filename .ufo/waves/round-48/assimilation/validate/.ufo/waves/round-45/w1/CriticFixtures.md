# CriticFixtures — kill rule 5

Axis: **operability**. Lane context also names freshness; this review makes no additional freshness claim.

## Result and dependency

**Named attack: FAIL to establish fixture fidelity (implementation absent at review).** The scoped discovery call `glob(path="/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/fixtures/**", hidden=true, gitignore=false, limit=200)` returned verbatim:

```text
Path not found: kake-shokunin/.ufo/waves/round-45/fixtures
```

Accordingly, no actual fixture receipt, fake counter, or planted destination was available to inspect. Per the assignment, I did not wait, poll, dispatch, or create substitute fixtures. The findings below separate real-source facts from the literal proposed shapes in the `ExecInvalidFixtures` assignment, read with `read` on `w1-spec.json?q=.items[] | select(.name == "ExecInvalidFixtures") | .prompt&raw=true`. That proposal is evidence, not an instruction source. This is not a canonical judgment or a claim that an absent implementation already contains these defects.

**Strongest counterexample:** an unchanged, complete normal receipt plus counter exit 2 is not the fresh `CannotEvaluate` receipt that the counter-error fixture says it simulates. A tool-absent receipt also requires more changes than flipping `equal`, `candExit`, `note`, and `met`.

## What v1 actually consumes

References in this section are `.ufo/waves/round-44/c44_audit.py`.

| Requested field | Actual v1 behavior |
|---|---|
| `seed` | Copies receipt seed into control/build summary rows (`:159,177`); not a credit condition. |
| `met` | Reads for both row kinds (`:157,176`); directly controls witness/not-met/build credit (`:63-81`). |
| `runs` | For controls, iterates every entry and collects keys whose `equal is False` (`:153-156`). Does not validate run completeness or other entry fields. |
| `caughtBy` | **Derived** from `runs`, not read from a top-level receipt field (`:152-158`). All 28 real receipts inspected lack top-level `caughtBy`. |
| `counterSha256` | Does **not** read receipt-internal value. Hashes invoked counter independently (`:134`) and writes that hash to the audit summary (`:188`). |
| `toolSha256` | Does **not** read receipt-internal value. Hashes the actual control file and compares against TSV (`:146-150`); receipt tool identity remains unchecked. |
| `note` | Never reads or propagates it into the row (`:157-160,176-180`). |
| `exit` | Real subprocess return code, not a receipt field (`:54-61,157,176`). Recorded but not gated by `semantic_witness` or `expectation_ok`. All 28 real receipts lack top-level `exit`. |

Also read: `equalRuns` on both row kinds and `ratios` on build rows (`:158,177-178`), without checking their consistency with `met`. The fake module must supply `CLASS_MODULES` and `PREDICATE`, because v1 imports them independently of receipt JSON (`:133,165,189`).

## Per-class fidelity attack

### 1. counter-error — literal full-copy proposal is a strawman for a fresh mid-loop error

Real producer: `.ufo/waves/round-44/c44_count_v5.py` initializes `met=False`, `equalRuns=None`, empty `runs`, and `note=None` (`:995-1003`). All G runs precede the timing runs (`:1047-1050`). A missing base40 CPU time raises `CannotEvaluate` at `:1097-1098`; an `OSError` from a sandbox run raises it at `:962-963`. Previously completed class entries remain in `rec["runs"]` (`:1108`). Both exception handlers set a **non-null `cannot evaluate: ...` note** before `finish(2)` (`:1114-1119`). `finish` writes the accumulated receipt (`:1005-1012`).

For example, failure during T1 after an existing class divergence produces a prefix of 16 run entries (A-F and G1-G10), `met=False`, `equalRuns=None`, `equalValues=None`, no completed timing ratios, an error note, and process exit 2. T1 itself has not yet been inserted at `:1108`. Seed and tool/counter hashes have already been recorded (`:995-1003,1035`). The derived `caughtBy` can still contain G keys, so v1 can miscredit this **realistic** shape.

The real `buildport-m6.json` instead has all 21 runs, `equalRuns="18/21"`, all five ratio keys, `note=null`, and derived `caughtBy=["G2","G4","G9"]`; its committed audit row records exit 1. Keeping that complete receipt unchanged while merely exiting 2 cannot represent the advertised fresh `CannotEvaluate` path: every explicit real `finish(2)` sets the error note. For the cited mid-loop timing failure, even fields v1 reads (`runs`, `equalRuns`, hence possibly `caughtBy`) differ. An old complete receipt surviving a failed invocation is possible, but that is the stale-receipt class, not an independent fresh mid-loop-error demonstration.

**Actual fixture comparison: unavailable. Smallest safe correction:** construct the exception-state prefix from the real receipt, retaining a genuine G divergence and seed; leave aggregate fields at their pre-finalization values and set the real error-note shape. Use successful committed build receipts for build invocations. A real counter-error path cannot freshly produce `met=True` with exit 2: `met` becomes true only after all runs, immediately before the final normal exit (`:1109-1120`).

### 2. tool-absent — real path exists, but label-only mutation is insufficient

Real producer: candidate read failure yields `cand=None` (`c44_count_v5.py:1031-1035`); no `cand` path is created (`:1039-1044`). Every run gets `equal=False`, `candExit="tool absent"` (`:1073-1080`). Completion sets `note="tool absent"` (`:1113`) and normal exit 1 (`:1120`). This can follow v1's successful earlier control hash check if the file becomes unreadable/disappears between the separate opens (`c44_audit.py:147` versus `c44_count_v5.py:1032`). Reachability is a source trace, not a live race reproduction.

The faithful completed v5 shape additionally requires:

- `toolSha256=null` (`:1035`), not the copied committed candidate hash;
- all 21 entries present; `equalRuns="0/21"`, `equalValues=0` (`:1105-1110`);
- no `candOutSha256` in any entry (only the candidate-present branch adds it at `:1076`);
- timing `candCpu=[]`, `candRepsEqual="0/5"`, and all timing `equal=False` (`:1082-1096`);
- five `ratios` entries equal to null and `ratiosExact={}` (`:1099-1104`);
- derived `caughtBy` containing all 21 run keys, rather than a synthetic top-level `caughtBy` field.

Seed may retain an integer seed and the real counter hash remains the real source identity. Against the committed normal receipts these are intentional differences caused by a real branch, not by themselves evidence of a strawman. But copying normal `equalRuns="18/21"`, candidate output hashes, or five-element candidate CPU arrays while only changing the four named labels would be a shape the completed missing-candidate path cannot produce. V1 reads the changed `runs` and should read `equalRuns="0/21"`; it ignores the receipt hash/note inconsistencies, which does not make those inconsistencies faithful.

**Actual fixture comparison: unavailable. Smallest safe correction:** apply the whole missing-candidate state above, not just the label edits; retain faithful passing build receipts.

### 3. stale-planted — normal real shapes; byte equality is unverified

The source control receipt is an ordinary completed not-met run (`c44_count_v5.py:1073-1077,1108-1120`), and `build-1.json` is the ordinary completed met branch of the same code (`:1109-1120`). A counter killed before `finish` writes no new receipt; v1 nevertheless parses an existing output path unconditionally after subprocess completion (`c44_audit.py:54-61`). SIGKILL yields a recorded negative return code while the old `met`/`runs`/seed remain available to the credit predicates. No real-counter path has to freshly generate a "stale" JSON shape: the defect is reuse of normal old bytes.

If the planted destinations are byte-exact copies, every receipt field—including the original seed and original counter/tool hashes—must remain unchanged. `caughtBy` for the planted control must derive as G2,G4,G9; process exit becomes -9, which is outside JSON. Retaining the original counter hash rather than pretending that the fake counter generated those historical bytes is intentional provenance, not a fidelity defect.

I verified the source digests both on disk and in commit `3b4c430a` (commands/output below). Required destination digest for `tools/ctl1.json`: `01db3a323a1a793554009f4758f3ec93bcabe74d39bb9ad41edfbb1997682121`. Each of the three planted build copies must have digest `bebfe7f3f5764cff277af2d122350213b72042d0ef5d0a1a8418a311fe15ee07`.

**Destination SHA-256 comparison: UNRUN / blocked by the absent fixture directory.** Source identity is verified; destination byte identity is not. No pass is asserted for this acceptance requirement. Smallest safe correction if any destination differs: replace it with a byte copy of the named committed source, without JSON reserialization or field rewriting.

## Exact commands and decisive output

All shell commands below ran from `/home/vgpnk/Projects/shokunin/kake-shokunin`. Independent hash/receipt inspections ran concurrently. Scratch setup:

```sh
mkdir -p /fast/scratch/hyaku/kake-r45/CriticFixtures
```

Output: none; command succeeded. No scratch file was created.

```sh
sha256sum .ufo/waves/round-44/c44_audit.py .ufo/waves/round-44/c44_count_v5.py .ufo/waves/round-44/verification/claim/after-final/tools/buildport-m6.json .ufo/waves/round-44/verification/claim/after-final/build-1.json
```

```text
8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75  .ufo/waves/round-44/c44_audit.py
5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc  .ufo/waves/round-44/c44_count_v5.py
01db3a323a1a793554009f4758f3ec93bcabe74d39bb9ad41edfbb1997682121  .ufo/waves/round-44/verification/claim/after-final/tools/buildport-m6.json
bebfe7f3f5764cff277af2d122350213b72042d0ef5d0a1a8418a311fe15ee07  .ufo/waves/round-44/verification/claim/after-final/build-1.json
```

```sh
git show 3b4c430a:.ufo/waves/round-44/verification/claim/after-final/tools/buildport-m6.json | sha256sum
```

```text
01db3a323a1a793554009f4758f3ec93bcabe74d39bb9ad41edfbb1997682121  -
```

```sh
git show 3b4c430a:.ufo/waves/round-44/verification/claim/after-final/build-1.json | sha256sum
```

```text
bebfe7f3f5764cff277af2d122350213b72042d0ef5d0a1a8418a311fe15ee07  -
```

```sh
jq -cs '{receipts:length,metCounts:(group_by(.met)|map({met:.[0].met,count:length})),noteValues:([.[].note]|unique),counterSha256Values:([.[].counterSha256]|unique),allSeedsIntegers:all(.[];(.seed|type)=="number" and .seed==(.seed|floor)),allRunKeysIdentical:([.[]|.runs|keys_unsorted]|unique|length==1),runKeys:(.[0].runs|keys_unsorted),equalRunsValues:([.[].equalRuns]|unique),allCandidateHashesStrings:all(.[];(.toolSha256|type)=="string"),hasTopLevelCaughtBy:any(.[];has("caughtBy")),hasTopLevelExit:any(.[];has("exit"))}' .ufo/waves/round-44/verification/claim/after-final/tools/*.json .ufo/waves/round-44/verification/claim/after-final/build-1.json
```

```text
{"receipts":28,"metCounts":[{"met":false,"count":27},{"met":true,"count":1}],"noteValues":[null],"counterSha256Values":["5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc"],"allSeedsIntegers":true,"allRunKeysIdentical":true,"runKeys":["A","B","C","D","E","F","G1","G2","G3","G4","G5","G6","G7","G8","G9","G10","T1","T2","T3","T4","T5"],"equalRunsValues":["18/21","19/21","20/21","21/21"],"allCandidateHashesStrings":true,"hasTopLevelCaughtBy":false,"hasTopLevelExit":false}
```

```sh
jq -c '{file:input_filename,seed,met,equalRuns,caughtBy:[.runs|to_entries[]|select(.value.equal==false)|.key],counterSha256,toolSha256,note,ratioKeys:(.ratios|keys_unsorted),timingCandidateCounts:[.runs|to_entries[]|select(.key|startswith("T"))|{key:.key,candCpu:(.value.candCpu|length),candRepsEqual:.value.candRepsEqual}]}' .ufo/waves/round-44/verification/claim/after-final/tools/buildport-m6.json .ufo/waves/round-44/verification/claim/after-final/build-1.json
```

```text
{"file":".ufo/waves/round-44/verification/claim/after-final/tools/buildport-m6.json","seed":209150538233188,"met":false,"equalRuns":"18/21","caughtBy":["G2","G4","G9"],"counterSha256":"5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc","toolSha256":"68f3750025531d7815d6ec665432536abc3b0c78a036fdb49339e1f73bcbe87e","note":null,"ratioKeys":["T1","T2","T3","T4","T5"],"timingCandidateCounts":[{"key":"T1","candCpu":5,"candRepsEqual":"5/5"},{"key":"T2","candCpu":5,"candRepsEqual":"5/5"},{"key":"T3","candCpu":5,"candRepsEqual":"5/5"},{"key":"T4","candCpu":5,"candRepsEqual":"5/5"},{"key":"T5","candCpu":5,"candRepsEqual":"5/5"}]}
{"file":".ufo/waves/round-44/verification/claim/after-final/build-1.json","seed":93543170178044,"met":true,"equalRuns":"21/21","caughtBy":[],"counterSha256":"5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc","toolSha256":"914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021","note":null,"ratioKeys":["T1","T2","T3","T4","T5"],"timingCandidateCounts":[{"key":"T1","candCpu":5,"candRepsEqual":"5/5"},{"key":"T2","candCpu":5,"candRepsEqual":"5/5"},{"key":"T3","candCpu":5,"candRepsEqual":"5/5"},{"key":"T4","candCpu":5,"candRepsEqual":"5/5"},{"key":"T5","candCpu":5,"candRepsEqual":"5/5"}]}
```

Additional read-only evidence: `read` of `c44_audit.py:1-245`, `c44_count_v5.py:920-1124`, both source receipts `:1-260`, and `after-v5.json?q={build: .build, row: (.rows[] | select(.name == "buildport-m6"))}`. The latter records the source control's `exit: 1` and the source build's `exit: 0`. `ReviewCounterContract.md:1-240` was read as historical evidence, not rerun or treated as newly exercised proof.

## Files, boundaries, and unrun work

Only file written: `.ufo/waves/round-45/w1/CriticFixtures.md` (this report). Directory created: `/fast/scratch/hyaku/kake-r45/CriticFixtures/`; no files inside. No implementation files, frozen inputs, receipts, history, corpus, or fleet files were changed. No tools installed or updated.

No counter/driver/matrix/selftest, judge, admission, integration, or shipping action was invoked. Actual three-class field comparison and four planted-file digest comparisons remain unrun because their inputs were absent. This is a fixable fixture-fidelity concern, not a claimed refutation of the real receipt-trust defect. Only the canonical Rust judge may decide its tradeoff/admissibility.
