# ScribeDeclarations — round-45 SCORECARD measurement-append draft

Seat: `kake-r45.ScribeDeclarations` (scribe, wave 1). Lane: `kake-shokunin`
(axes: operability, freshness). Item: draft the round-45 SCORECARD
measurement-append text with placeholders where a receipt value is not yet known.

## Result

**PASS on the item's named attack** (the draft exists, every count in it names
its counting command and its receipt, and every unknown value is an explicit
placeholder rather than a guess).

- **Deliverable written:** `.ufo/waves/round-45/drafts/scorecard-measurement.md`
  (20 KB) — three ready-to-append blocks: (A) the C1 measurement paragraph
  (before/after receipts named, `invalid_accepted 3 → 0`, kill-rule evidence
  pointers 1–5, do-nothing and junk controls); (B) the C2 measurement paragraph
  (`selftest kills 2/4 → 4/4`, `v4 predicate true → false`, the witness-split
  sentence slot); (C) the move-log rows (one per owned axis). Plus a placeholder
  table with a fill-in source per token, the C2(c) receipt-identity analysis, an
  open-items list, and an L1 landing checklist.
- **Nothing was fabricated.** Every numeric value in the drafted prose is either
  (a) quoted from a receipt this seat read, with that receipt's path and sha256
  in the sentence, or (b) a `{{PLACEHOLDER}}` token whose fill-in source is
  named in the table at the top of the draft. No count appears without a receipt.
- **Append-only framing.** The drafted blocks are headed "appended after the
  freeze; the declaration above is not edited", and the landing checklist states
  that `SCORECARD.md` lines 3628–3709 (the frozen declaration) must not be
  edited.

## Decisive commands and verbatim output

All commands ran with cwd `/home/vgpnk/Projects/shokunin/kake-shokunin`.

### 1. Frozen declaration read (the source of the draft)

```sh
grep -n "Round 45 — C1 and C2 declared" SCORECARD.md
```

```text
3628:## Round 45 — C1 and C2 declared (frozen before any claim receipt is produced)
```

The C1 counting command and MET condition (`SCORECARD.md:3653-3658`):

```text
Counting command (frozen):
`python3 -B .ufo/waves/round-45/c45_matrix.py --stage before|after`
— before runs the frozen v1 driver over the three fixture classes; after runs v2 over
the same fixtures plus the honest regression cohort. Claim MET iff the before receipt
records `invalid_accepted=3` and the after receipt records `invalid_accepted=0`,
`rejections_named=3`, `honest_witnessed=27`, `honest_build_met=3`.
```

The C2 counting command and MET condition (`SCORECARD.md:3697-3701`):

```text
Counting command (frozen):
`python3 -B .ufo/waves/round-45/c45_freshness.py`
— prints `selftest_kills before=2/4 after=4/4`,
`v4_predicate_names_class_runs before=true after=false`,
`witness_split class_only=22 mixed=1 met=4`. Claim MET iff after=(4/4, false, 22/1/4).
```

### 2. C1 before-state: v1 accepts 3/3 invalid classes (receipts exist)

```sh
for c in counter-error tool-absent stale-planted; do
  jq -r '{ok,verdict,witnessed,notMet,expect}' \
    .ufo/waves/round-45/verification/hardening/before/$c/summary.json
done
```

```text
===== counter-error
{
  "ok": true,
  "verdict": "witnessed 1/1 notMet=1 build met 3/3",
  "witnessed": 1,
  "notMet": 1,
  "expect": "witnessed"
}
===== tool-absent
{
  "ok": true,
  "verdict": "witnessed 1/1 notMet=1 build met 3/3",
  "witnessed": 1,
  "notMet": 1,
  "expect": "witnessed"
}
===== stale-planted
{
  "ok": true,
  "verdict": "witnessed 1/1 notMet=1 build met 3/3",
  "witnessed": 1,
  "notMet": 1,
  "expect": "witnessed"
}
```

Receipt sha256 (quoted in the draft):

```text
bce55a787d04188d9f7e5c1e2c06ec44eb1afee59801704689f15a67914980f3  .ufo/waves/round-45/verification/hardening/before/counter-error/summary.json
9af97d72bf19f4bdc7bcf09574926d802b303f7c7c7b8becebe319116106b20d  .ufo/waves/round-45/verification/hardening/before/honest/summary.json
cc4accb91c5b25a3619910e9b5957e28213f891cf8c9c1eee03af9a0ef6ac324  .ufo/waves/round-45/verification/hardening/before/stale-planted/summary.json
aed6b92f8fe56819b07715cecacd46d54ecbbb417b9396db6efeed01fdaaca02  .ufo/waves/round-45/verification/hardening/before/tool-absent/summary.json
```

The three rejection shapes are real v1-observable shapes (kill rule 5), read from
the retained driver summaries and receipts:

```sh
for c in counter-error tool-absent stale-planted; do
  jq -r '{counterSha256,classesMode,exit:(.rows[0].exit),met:(.rows[0].met),seed:(.rows[0].seed),note:(.rows[0].note)}' \
    .ufo/waves/round-45/verification/hardening/before/$c/out-v1/summary.json
done
```

```text
== counter-error
{ "counterSha256": "15363b71eaa0389e4023b896e8b980fdd3a1735af9a9932e4d3d1e9b58984412", "classesMode": "v5", "exit": 2, "met": false, "seed": 224408754848177, "note": null }
== tool-absent
{ "counterSha256": "c697435a11e732146a0a7e38756ab513209beeada88d063951dc65015d6723ef", "classesMode": "v5", "exit": 1, "met": false, "seed": 224408754848177, "note": null }
== stale-planted
{ "counterSha256": "18e3bcfda602bd0716ab0bc762aa6c7b6ee27ad5ca457c7f9cca8daebc41874f", "classesMode": "v5", "exit": -9, "met": false, "seed": 209150538233188, "note": null }
```

(the summary row drops `note`; the underlying tool-absent receipt carries it —
`jq -r '{note,…}' …/tool-absent/out-v1/tools/ctl1.json` → `"note": "tool absent"`,
`runs.G5.candExit = "tool absent"`, `runs.G5.equal = false`).

Junk control (honest fixture under v1, `--expect not-met`):

```text
AUDIT kake-r44 classes=v5 classKeys=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 witnessed=1/1 notMet=1 build_met=3/3 ok=True counter=5cedaa3b9f91
```

### 3. C2(a) before-state: 2/4 killed — measured, quoted with sha256

```sh
sha256sum .ufo/waves/round-45/verification/selftest-coverage/before/*.txt
```

```text
0809aa629bdc4a09bb57a4c4af45fa210c527f421925b5d359c2d3dc714fc28f  .ufo/waves/round-45/verification/selftest-coverage/before/m1.txt
509fc8a23e761afdaf1032217e7343a155800cbec84e8a3768ad799db3153db1  .ufo/waves/round-45/verification/selftest-coverage/before/m2.txt
a4f12ee6594c557c2a00177976739cc02237ac12cb26009ed245c77b3a92c105  .ufo/waves/round-45/verification/selftest-coverage/before/m3.txt
509fc8a23e761afdaf1032217e7343a155800cbec84e8a3768ad799db3153db1  .ufo/waves/round-45/verification/selftest-coverage/before/m4.txt
```

(m1 and m3 end `SELFTEST_EXIT=1` — killed; m2 and m4 end `SELFTEST_EXIT=0` —
survived. m2 and m4 are byte-identical outputs, hence the identical sha.)

### 4. C2(b) before-state: the committed v4 receipt names the class runs

```sh
jq -r '{predicate, classesMode, classRuns, runs_keys:(.runs|keys)}' \
  .ufo/waves/round-44/verification/claim/v4-final/tools/headtail-V1.json
```

```text
{
  "predicate": "met: the tool's exit code and output equal the round-41 tool's on every generated run (the eleven v4 runs and the ten class runs), and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's",
  "classesMode": "v4",
  "classRuns": [],
  "runs_keys": [ "A","B","C","D","E","F","T1","T2","T3","T4","T5" ]
}
```

### 5. C2(b) after-state at source level (counter v6 predicate split)

```sh
python3 - <<'PY'  # ast literal extraction of PREDICATE / PREDICATE_V5 / PREDICATE_V4
PY
```

```text
v5 PREDICATE == v6 PREDICATE_V5 : True
v6 PREDICATE_V4: "met: the tool's exit code and output equal the round-41 tool's on every generated run (the eleven v4 runs), and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's"
class runs phrase in V4? False
v4 PREDICATE_V4 == v5 PREDICATE? False
```

The runtime v4 receipt (the frozen C2(b) evidence) does not yet exist — see
open item 6.

### 6. C2(c) witness split — the receipt-identity conflict (decisive)

```sh
jq -r '.rows | {class_only: map(select(.met==false and (.classCaught|length)>0 and (.legacyCaught|length)==0))|length, mixed: map(select(.met==false and (.classCaught|length)>0 and (.legacyCaught|length)>0))|length, met: map(select(.met==true))|length, other: map(select(.met==false and (.classCaught|length)==0))|length}' .ufo/waves/round-44/verification/claim/after-final/after-v5.json
```

```text
{
  "class_only": 26,
  "mixed": 1,
  "met": 0,
  "other": 0
}
```

Same command on the earlier committed receipt:

```text
{
  "class_only": 22,
  "mixed": 1,
  "met": 4,
  "other": 0
}
```

Receipt identity (from the receipts themselves):

```sh
jq -r '{witnessed:.witnessed, notMet:.notMet, ok:.ok, build_met:([.build[]|select(.met==true)]|length), rows_n:(.rows|length)}' .ufo/waves/round-44/verification/claim/after-final/after-v5.json .ufo/waves/round-44/verification/claim/after-v5.json
```

```text
{
  "witnessed": 27,
  "notMet": 27,
  "ok": true,
  "build_met": 3,
  "rows_n": 27
}
{
  "witnessed": 23,
  "notMet": 23,
  "ok": false,
  "build_met": 3,
  "rows_n": 27
}
```

**Finding (reported, not silently resolved):** the frozen C2(c) tuple
`22 class-only + 1 mixed + 4 met` re-derives from the **earlier, 23-witness**
receipt `.ufo/waves/round-44/verification/claim/after-v5.json`
(sha256 `2383efaee0fe67d04430127fd1cd40160726e4b9afd61068d43a816e84ce0902`).
The **final, 27-witness** claim receipt
`.ufo/waves/round-44/verification/claim/after-final/after-v5.json`
(sha256 `9dead4d7d65d10f268f37efba185f12bb4f8e8942e8e81e98df4b1c8fdc076d1`)
re-derives as `26 class-only + 1 mixed + 0 met`. The draft supplies two
candidate sentences (each arithmetically true of the receipt it names) and
leaves the choice to the L1; it does not assert C2 MET. The same conflict was
independently reported by the wave's `CriticC2Scope`, `ExecWitnessSplit` and
`ScoutRoutedLedger` seats.

### 7. Ledger-gate hazard check on the draft

`scripts/ledger_latest_check.py` takes the **last** regex match per file, so the
landed append must not introduce a new `re-scored N of the 27` line in
`SCORECARD.md`, nor `not met (T1 …, T5 …)` / `T1 …–…, T5 …–…` in `LOG.md`.

```sh
python3 - <<'PY'  # regex scan of the draft
PY
```

```text
rescore matches: 0 []
donothing matches: 0 []
ratio matches: 0 []
```

Gate state at drafting time (unchanged by this seat — I edited no lane file):

```sh
python3 -B scripts/ledger_latest_check.py --root .
```

```text
rescore-tally MATCH quoted=14 derived=14 SCORECARD.md:3581
donothing-ratios MATCH quoted=T1 4.21, T5 7.05 derived=T1 4.21, T5 7.05 LOG.md:1703
build-ratio-range MATCH quoted=T1 1.00–1.01, T5 1.11–1.22 derived=T1 1.00–1.01, T5 1.11–1.22 LOG.md:1705
ledger-quotes: 3 figures, 0 mismatches
EXIT=0
```

### 8. Frozen-byte pins quoted in the draft (re-verified)

```sh
sha256sum .ufo/waves/round-44/c44_audit.py .ufo/waves/round-44/c44_count_v5.py .ufo/waves/round-44/c44_placebo.py .ufo/waves/round-44/controls-27.tsv
```

```text
8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75  .ufo/waves/round-44/c44_audit.py
5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc  .ufo/waves/round-44/c44_count_v5.py
9ce3acd4c4c72de0b3c26a31bd1101307b71b2174100eb260b8b04fa5fc77a27  .ufo/waves/round-44/c44_placebo.py
a1f0e364dad5ff937666966a16622e6895591a2eb3db714d6ecf3f3948c31bf8  .ufo/waves/round-44/controls-27.tsv
```

Round-45 instrument hashes quoted in the draft:

```sh
sha256sum .ufo/waves/round-45/c45_matrix.py .ufo/waves/round-45/c45_count.py .ufo/waves/round-45/c45_audit.py .ufo/waves/round-45/v6diff/v5-v6.diff
```

```text
cdddee5a62b0f03bb39a1801ea9fce039e8af8b405add620cdb156143a4694cd  .ufo/waves/round-45/c45_matrix.py
ce8bf2353d4f008a987f6fb3b6d3677d2dbed98aaae274126c68f0a3cf622556  .ufo/waves/round-45/c45_count.py
5a342e29c7e872d992cfedc26de849c010d197bb82162e007a61a55d915c7051  .ufo/waves/round-45/c45_audit.py
408539cfd6931aacc75f5e7954093e14eb925c82a503304e2c8cf9f0f54b0e06  .ufo/waves/round-45/v6diff/v5-v6.diff
```

## Findings / open items the L1 must dispose (verbatim in the draft)

1. **C2(c) receipt identity** — `22/1/4` belongs to the 23-witness receipt
   `claim/after-v5.json`; the final 27-witness receipt `claim/after-final/after-v5.json`
   gives `26/1/0`. Two candidate sentences supplied; neither asserts MET.
2. **Kill rule (1)/(4) sha-guard drift.** `SentinelFrozen`'s end guard diffed
   `changed (exit 1)` (483 → 484 guarded files); the only differing entries are
   Python bytecode caches under `.ufo/waves/round-44/classes/__pycache__/`
   (`g3_empty_path.cpython-314.pyc` `25ba8580…` → `ff0cbbc8…`, plus a new
   `g9_port_digits.cpython-314.pyc` `bb3b9b59…`). `git diff --name-only HEAD -- .ufo/waves/round-44/`
   is empty, i.e. committed bytes are unchanged. The L1 must choose the
   disposition; this seat does not bless a new baseline.
3. **The frozen C2 counting command has no builder.** `python3 -B .ufo/waves/round-45/c45_freshness.py`
   is named in the frozen declaration, but no wave-1 seat in `w1-spec.json` is
   assigned to write it (the name appears once in the wave context and once in
   `make_w1_spec.py:52`). The file does not exist in the tree, so the C2
   measurement has no executed command behind it until the L1 assigns or writes it.
4. **C1 after-stage matrix receipt absent** — `.ufo/waves/round-45/verification/matrix/`
   does not exist; `ExecMatrixRunner` did not run `--stage before|after`. The
   before leg is evidenced per class under `verification/hardening/before/`.
5. **Honest-cohort v2 regression receipt absent** —
   `.ufo/waves/round-45/verification/honest-regression/after-v5-v2.json` did not
   exist when `ExecRegressionHonest` ran (driver v2 landed later); the exact
   command to re-run is quoted in the draft.
6. **v6 v4 receipt absent** — `.ufo/waves/round-45/verification/v6v4/` does not
   exist; `ExecV4ReceiptV6` was blocked because `c45_count.py` did not exist at
   its start. The command to re-run is quoted in the draft.
7. **C2(a) after-state unmeasured** — `verification/selftest-coverage/after/` is
   empty (the four `m{1..4}_v2.py` copies were never written), so `4/4` is a
   placeholder, not a passed result.
8. **C1 "9 rejected rows" arithmetic** — 3 fixture classes × (control + 3 builds)
   = 12 rows, not the frozen "9"; `c45_matrix.py` checks all 12 actual rows and
   reports distinct named classes. The landed prose must quote the measured row
   count.
9. **Scope bounds recorded by the wave, not adjudicated here** — the v2
   receipt-validity gate is a bounded provenance check (self-reported
   `counterSha256` + mtime window ± `MTIME_EPS_NS` = 1 s + a nonce manifest),
   not a proof of writer identity; and the C1 frozen sentence's "any control" /
   "over the invoked counter bytes" phrasing is stronger than three fixture
   classes can establish. The drafted prose claims only what the fixtures and
   the honest cohort measure.

## Out of scope / not done by this seat

- No edit to `SCORECARD.md`, `LOG.md`, the corpus, or any frozen round-43/44
  byte. The SCORECARD append is the L1's to land.
- No commit, push, jj, or publish.
- No matrix, freshness, honest-regression or counter run was executed by this
  seat: the three frozen counting commands' outputs are either absent or owned
  by other seats; this seat re-ran only read-only jq/sha256/python-AST
  inspections and the ledger checker (read-only), all reported above.
- No tool was installed (pacman is paused host-wide; python3/jq/git were already
  present).
- `python3 -B .ufo/waves/round-45/c45_audit.py --selftest` was executed once as a
  read-only observation of the landed v2 driver; its stdout
  (`SELFTEST PASS: v1 assertions plus timing-only, invalid receipt, error-row,
  and build-count gates`, exit 0) is quoted in the draft as the v2 selftest
  evidence, not as the C2(a) after-state (which needs the four mutant copies).

## Files written

- `.ufo/waves/round-45/drafts/scorecard-measurement.md` — the deliverable draft.
- `.ufo/waves/round-45/w1/ScribeDeclarations.md` — this report.

No other file was created or modified by this seat.
