# ScoutReceiptShape — C1 receipt fidelity contract

Axes: fidelity (committed JSON types), completeness (v1 read vs ignore), evidence (verbatim).
Lane axis judged: operability.
Result: **PASS** (schema extracted). Attack not executed here: no invalid fixtures were planted and `c45_audit.py` was not run. Unrun checks stay unrun.

Sources (committed, read-only):

- per-control receipt: `.ufo/waves/round-44/verification/claim/after-final/tools/repeat-len-band.json` (8002 bytes)
- build receipt: `.ufo/waves/round-44/verification/claim/after-final/build-1.json` (7933 bytes); build-2/3 same key order
- audit summary: `.ufo/waves/round-44/verification/claim/after-final/after-v5.json` (16607 bytes)
- v1 reader: `.ufo/waves/round-44/c44_audit.py` (`score` 145–160, `score_build` 173–180, `semantic_witness` 63–66, summary 186–206)

Cohort check: all 27 `after-final/tools/*.json` share one top-level key order and one `runs` key order. All 3 build receipts share that same order. `note` is JSON null on all 30. No receipt in this cohort contains the string `tool absent`.

## 1. Counter receipt (control and build share one object shape)

Top-level key order (identical on `repeat-len-band.json` and `build-1.json`):

`predicate`, `met`, `ratioLimit`, `reps`, `revision`, `toolFile`, `label`, `seed`, `counterSha256`, `ref41Sha256`, `base40Sha256`, `classesMode`, `classRuns`, `toolSha256`, `equalRuns`, `equalValues`, `runs`, `ratios`, `ratiosExact`, `note`

| field | JSON type | control example (`repeat-len-band.json`) | build example (`build-1.json`) | v1 reads? |
|---|---|---|---|---|
| predicate | string | `met: the tool's exit code and output equal the round-41 tool's on every generated run (the eleven v4 runs and the ten class runs), and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's` | same string | **ignore** (summary `predicate` is `counter_mod.PREDICATE`, not this field) |
| met | bool | `false` | `true` | **gating read** (`is False` / `is True`; not truthiness) |
| ratioLimit | number (float) | `2.0` | `2.0` | ignore |
| reps | number (int) | `5` | `5` | ignore |
| revision | null or string | `null` | `"020bc4574729ed674299f6cab02faac1582d9464"` | ignore |
| toolFile | string or null | abs path `.../controls-r43/repeat-ctl_len_memo_band.py` | `null` | ignore |
| label | string | `""` | `""` | ignore (summary `label` is CLI `--label`) |
| seed | number (int) | `187926495163792` | `93543170178044` | **copied, not gated** |
| counterSha256 | string (64 hex) | `5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc` | same | **ignore** (summary hashes the counter file via `sha256_file`) |
| ref41Sha256 | string (64 hex) | `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d` | same | ignore |
| base40Sha256 | string (64 hex) | `4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e` | same | ignore |
| classesMode | string | `"v5"` | `"v5"` | **ignore** (summary `classesMode` is CLI `--classes`) |
| classRuns | array of string, len 10 | `["G1","G2","G3","G4","G5","G6","G7","G8","G9","G10"]` | same | **ignore** (class key set is `counter_mod.CLASS_MODULES` when `--classes v5`, else `[]`) |
| toolSha256 | string (64 hex) | `c3a8770e5d76a8a7e218f56a2e9776fa03746770745d78a00f65dd6382df83ec` | `914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021` | **ignore** (v1 hashes the tool path itself; that digest is in-memory `toolSha256` and is **dropped** from the written row) |
| equalRuns | string | `"19/21"` | `"21/21"` | **copied, not gated** (not parsed; cohort values `"18/21"`, `"19/21"`, `"20/21"`, builds `"21/21"`) |
| equalValues | number (int) | `15146` | `15397` | ignore |
| runs | object, 21 keys | see below | same key order, this file all `equal: true` | **gating read** of each `runs.<key>.equal` only |
| ratios | object, keys T1–T5, float values | `{"T1":1.03,"T2":1.194,"T3":1.369,"T4":1.271,"T5":1.136}` | `{"T1":1.005,"T2":1.217,"T3":1.355,"T4":1.256,"T5":1.123}` | **control path: ignore. build path: copied, not gated** |
| ratiosExact | object, keys T1–T5, float | `{"T1":1.0300619789251346,...}` | `{"T1":1.0049049704378856,...}` | ignore |
| note | null (honest cohort) | `null` | `null` | **ignore** (the string `"tool absent"` is not in these bytes; v1 has no `note` access) |

There is **no** process-exit field on the counter receipt. v1 stores subprocess `returncode` separately as audit `rows[].exit` / `build[].exit`. `expectation_ok` never reads `exit`.

### `runs` key order (both files)

`A B C D E F G1 G2 G3 G4 G5 G6 G7 G8 G9 G10 T1 T2 T3 T4 T5` (21 keys: 6 v4 letters + 10 class + 5 timing).

Two shapes:

**A–F and G1–G10** (field order): `values` int, `ref41Exit` int, `ref41OutSha256` str, `candExit` int, `candOutSha256` str, `equal` bool.

Control run `A` (equal):

```json
{"values":1434,"ref41Exit":2,"ref41OutSha256":"cd63a76a8bb89564f4af5ed3b75d69970707e1636bcdc1e2dfc5fcc3fa7fbcc4","candExit":2,"candOutSha256":"cd63a76a8bb89564f4af5ed3b75d69970707e1636bcdc1e2dfc5fcc3fa7fbcc4","equal":true}
```

**T1–T5** add, in order: `values` null, then the same four compare fields, `equal` bool, `base40Cpu` array of 5 floats, `candCpu` array of 5 floats, `candRepsEqual` string (`"5/5"` when equal, `"0/5"` on the one miss below).

Only `equal` is read. `values`, both exits, both hashes, both CPU arrays, and `candRepsEqual` are ignored. `equal: false` is the only catch signal (`is False`); missing `equal`, `true`, `null`, or `0` does not catch.

### caughtBy derivation (not a receipt field)

`c44_audit.py` 152–156: if the receipt parses, walk `rec.get("runs", {}).items()` in insertion order and append the key when `run.get("equal") is False`.

On `repeat-len-band.json` the only `equal: false` runs are `G7` then `T5`, so derived `caughtBy` is `["G7","T5"]`. That matches `after-v5.json` row `caughtBy` and `witnessedByClass["repeat-len-band"]`.

`G7` (class miss; hashes differ, exits both 1):

```json
{"values":240,"ref41Exit":1,"ref41OutSha256":"dda9291d2b773933681e197c55c3af81db1b5a8a145fc6d76475a8f48f0e701f","candExit":1,"candOutSha256":"4c3361f107cfa95a72450cc1af64a10cd89909cd9228ba1202b1184fd744cacc","equal":false}
```

`T5` (legacy/timing miss): `equal: false`, `candRepsEqual: "0/5"`, `values: null`, `ref41Exit`/`candExit` both 2.

Split (summary only, lines 199–200), class set = `{G1..G10}` from the counter module, **not** from `classRuns`:

- `classCaught` = caughtBy keys in that set → `["G7"]`
- `legacyCaught` = the rest → `["T5"]`
- `witnessedByClass` stores the **full** `caughtBy` (legacy keys included), not `classCaught`.

`semantic_witness` (63–66): `met is False` AND `caughtBy` non-empty AND at least one string key in the class set. `["G7","T5"]` witnesses. `["T5"]` alone does not. `met: false` with empty `caughtBy` is not-met but not witnessed.

## 2. Audit summary row (`after-v5.json` `rows[]`, 27 rows)

Written key order:

`name`, `family`, `class`, `path`, `sha256`, `exit`, `met`, `equalRuns`, `seed`, `caughtBy`, `receipt`, `error`, `classCaught`, `legacyCaught`

`repeat-len-band` row (matches the receipt above):

```json
{
 "name": "repeat-len-band",
 "family": "band",
 "class": "G7",
 "path": ".ufo/waves/round-44/controls-r43/repeat-ctl_len_memo_band.py",
 "sha256": "c3a8770e5d76a8a7e218f56a2e9776fa03746770745d78a00f65dd6382df83ec",
 "exit": 1,
 "met": false,
 "equalRuns": "19/21",
 "seed": 187926495163792,
 "caughtBy": ["G7", "T5"],
 "receipt": "tools/repeat-len-band.json",
 "error": null,
 "classCaught": ["G7"],
 "legacyCaught": ["T5"]
}
```

| field | type in this file | source | example |
|---|---|---|---|
| name | string | controls TSV col 1 | `"repeat-len-band"` |
| family | string | TSV col 2 | `"band"` (10 families in cohort) |
| class | string | TSV col 3 | `"G7"` |
| path | string | TSV col 4, repo-relative | `.ufo/waves/round-44/controls-r43/repeat-ctl_len_memo_band.py` |
| sha256 | string | TSV col 5, **not** copied from receipt `toolSha256` (they match here) | `c3a8770e…df83ec` |
| exit | int | counter subprocess return code | `1` on every not-met control row; `0` on build rows. Sha-mismatch path forces `2` and never reads a receipt |
| met | bool | receipt `met` | `false` (all 27 rows) |
| equalRuns | string | receipt | `"19/21"` (cohort also `"20/21"` x14, `"18/21"` x1) |
| seed | int | receipt | `187926495163792` (27 distinct) |
| caughtBy | array of string, len 1–3 | derived | `["G7","T5"]` |
| receipt | string | path of counter `--out` relative to summary dir | `"tools/repeat-len-band.json"` |
| error | null or string | null iff JSON loaded | `null` (all 27). Load failure stores stderr/stdout tail, `met` null, `caughtBy` [] |
| classCaught | array of string | derived | `["G7"]` |
| legacyCaught | array of string, possibly empty | derived | `["T5"]` (only this row; other 26 are `[]`) |

Dropped before write: in-memory `toolSha256`, TSV `seat`. Absent from every row: `note`, `classesMode`, `classRuns`, `counterSha256`, `ratios`.

### Summary object (siblings of `rows`)

| field | type | example |
|---|---|---|
| label | string | `""` |
| classesMode | string | `"v5"` |
| expect | string | `"witnessed"` |
| counter | string | `".ufo/waves/round-44/c44_count_v5.py"` |
| counterSha256 | string | `5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc` (file hash; equals every receipt's field in this cohort, but v1 does not compare them) |
| predicate | string | same sentence as the receipt predicate |
| controls | int | `27` (count of rows with no error, not the TSV length) |
| classKeys | array of 10 strings | `G1`..`G10` |
| witnessed | int | `27` |
| witnessedNames | array of 27 strings | starts `portlen-v1` … ends `headtail-V8` |
| witnessedByClass | object name → caughtBy | `"repeat-len-band": ["G7","T5"]` |
| notMet | int | `27` |
| notMetNames | array of 27 strings | same membership as witnessedNames in this file |
| metNames | array | `[]` |
| errors | array | `[]` |
| build | array of 3 objects | see below |
| ok | bool | `true` |
| verdict | string | `"witnessed 27/27 notMet=27 build met 3/3"` |

`build[0]` (copied from `build-1.json`; `ratiosExact` not copied):

```json
{"run":1,"exit":0,"met":true,"seed":93543170178044,"equalRuns":"21/21","ratios":{"T1":1.005,"T2":1.217,"T3":1.355,"T4":1.256,"T5":1.123},"receipt":"build-1.json","error":null}
```

`build[1].seed` = `234322826174562`, ratios `T1:1.029,T2:1.173,T3:1.326,T4:1.269,T5:1.121`.
`build[2].seed` = `96267491316273`, ratios `T1:1.013,T2:1.186,T3:1.337,T4:1.26,T5:1.121`.
All three: `exit: 0`, `met: true`, `equalRuns: "21/21"`, `error: null`. Build gate is only `met is True` (and `build` non-empty for `--expect witnessed`).

## 3. What a C1 fixture must match

Honest shape to copy: the 20 top-level keys above, 21 `runs` keys, two run shapes, `note: null`, control `revision: null` + `toolFile` string, build `revision` 40-hex + `toolFile: null`.

v1 credit does **not** depend on that shape. Gating reads only:

1. JSON object loads (`run_counter` 56–60). Failure → `error` set → no witness and no not-met credit.
2. `met is False` for witness and for not-met; `met is True` for blind controls and for each build.
3. For a **witness** only: some `runs` key whose `equal is False` is in the counter module's class set (`G1`–`G10` under v5). Key order of `caughtBy` is runs insertion order.

Ignored for credit, so these do **not** withhold witness/not-met (the C1 defect):

- (i) counter process exit other than 0/1 — stored on the row, never tested by `expectation_ok`.
- (ii) `note` of any value, including `"tool absent"` — field never read. Honest bytes only show `null`.
- (iii) mtime / run window / whether this process wrote the file — no `os.stat`. `json.load` accepts a pre-existing file at `--out` after the subprocess returns.
- receipt `counterSha256`, `toolSha256`, `classesMode`, `classRuns`, `predicate`, `equalValues`, `ratiosExact`, `ratioLimit`, `reps`, `revision`, `toolFile`, `label`, ref/base hashes, and every run subfield except `equal`.
- `equalRuns`, `seed`, and build `ratios` are copied onto the summary and not interpreted.

`met: false` alone is enough for not-met credit. Witness also needs a class-key `equal: false`. A timing-only miss (`T1`–`T5`) is `legacyCaught` and does not witness.

## Decisive command output

Python `json` load of the three files plus the 27-tool cohort (this seat, 2026-10-24). Cell succeeded; decisive lines:

```
CONTROL TOP: met bool=False ratioLimit float=2.0 reps int=5 revision None
  toolFile str=.../repeat-ctl_len_memo_band.py label str='' seed int=187926495163792
  classesMode str='v5' classRuns ['G1'..'G10'] equalRuns str='19/21' equalValues int=15146 note None
  counterSha256 5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc
  toolSha256    c3a8770e5d76a8a7e218f56a2e9776fa03746770745d78a00f65dd6382df83ec
run keys ['A','B','C','D','E','F','G1','G2','G3','G4','G5','G6','G7','G8','G9','G10','T1','T2','T3','T4','T5']
equal is False ['G7','T5']
BUILD DIFF: met True; revision '020bc4574729ed674299f6cab02faac1582d9464'; toolFile None
  seed 93543170178044; equalRuns '21/21'; equalValues 15397; equal False []
COHORT: n tools 27; top key orders 1; run key orders 1; notes {None}; classesMode {'v5'}
  classRuns unique {('G1',...,'G10')}
  non-T fields ('values','ref41Exit','ref41OutSha256','candExit','candOutSha256','equal')
  T fields (those + 'base40Cpu','candCpu','candRepsEqual')
  met all bool False; equalRuns {'20/21':14,'19/21':12,'18/21':1}
  values: G/v4 int, T null; ref41Exit/candExit all int
derived caughtBy ['G7','T5'] == row caughtBy; classCaught ['G7']; legacyCaught ['T5']; semantic witness True
receipt toolSha256 == row sha256 True; receipt counterSha256 == summary counterSha256 True
ROW KEYS ['name','family','class','path','sha256','exit','met','equalRuns','seed','caughtBy','receipt','error','classCaught','legacyCaught']
row has toolSha256 False; seat False; note False
witnessedByClass['repeat-len-band'] ['G7','T5']
build[0] {"run":1,"exit":0,"met":true,"seed":93543170178044,"equalRuns":"21/21","ratios":{"T1":1.005,"T2":1.217,"T3":1.355,"T4":1.256,"T5":1.123},"receipt":"build-1.json","error":null}
```

v1 source check: `c44_audit.py` contains no `note`, `classRuns`, `ratiosExact`, `equalValues`, or `st_mtime`. `counterSha256` / `classesMode` in that file are summary fields from the counter file hash and `--classes`, not receipt lookups. Receipt field reads are only `met`, `runs`/`equal`, `equalRuns`, `seed`, and (build only) `ratios`.

## Files written

- `.ufo/waves/round-45/w1/ScoutReceiptShape.md` (this report)

No other files. Scratch dir not required (no temp files). No installs. No git writes.

## Unknowns

- v2's exact refusal predicate is out of this seat; this contract is v1's read set plus the honest v5 byte shape.
- `"tool absent"` is not an observed value in `after-final` (all `note` are null).
- A v4-mode receipt was not the named sample. v1 in v4 mode forces `classKeys=[]`, so witnessed is 0 even if `runs` contains `G*` keys.
