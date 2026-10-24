# AttackMeasurementAppend — round 45 wave 2

Named attack: the SCORECARD round-45 measured append (`SCORECARD.md:3711-3775`) — every number
must re-derive from the receipt it names. Leaf seat; read-only over the lane except this file;
scratch under `/fast/scratch/hyaku/kake-r45/AttackMeasurementAppend/`.

Method note: no `lsp` device is exposed in this environment (only `ast_edit`/`debug` under
`xd://`), so caller/definition checks were done by reading the runners and driver plus literal
hash/string comparisons, not by a language server. The findings rest on executed commands, not
on grep absence.

## 0. Tip instability during review (affects every artifact below)

`.ufo/waves/round-45/c45_audit.py` was rewritten while this seat read it:

```text
00:52  sha f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076  449 lines
       (= `git show HEAD:` blob, = the append's driver sha, = driver_sha256 in both matrix receipts)
00:58  in-tree variant whose `--selftest` failed (traceback at lines 477/351/333)
01:01  sha 6abab9ea… (git diff vs HEAD: 46 insertions, 4 deletions)
01:02  sha 64bc33248c9ba2088f5447d7c3064cb2aea3f2dce9e2ba4ec4dd514a6a07841e  492 lines
$ git status --porcelain .ufo/waves/round-45/c45_audit.py
 M .ufo/waves/round-45/c45_audit.py
```

The committed blob (the append's instrument) is stable and self-consistent: I extracted it with
`git show HEAD:… > head_c45_audit.py` (sha `f3c3171b…a076`, 449 lines) and ran its shipped
selftest directly:

```text
$ python3 -B head_c45_audit.py --selftest
SELFTEST PASS: v1 assertions plus timing-only, invalid receipt, error-row, build-count gates,
and the end-to-end fixture cohort
head_blob_selftest_exit=0
```

The 00:58 failure therefore belongs to a transient uncommitted variant, not to the measured
driver. It is reported here only as evidence that wave-2 re-runs were writing into the lane while
the append's receipts were being read (see F2), not as a defect of the append.

## 1. Findings

### F1 (HIGH) — "sha guard clean / frozen bytes byte-identical" is false, and the cited report says so

```text
$ sha256sum -c .ufo/waves/round-45/verification/sha-guard/before.sha256
.ufo/waves/round-44/classes/__pycache__/g3_empty_path.cpython-314.pyc: FAILED
sha256sum: WARNING: 1 computed checksum(s) did NOT match
guard_fail_count=1   guard_entries=483
```

- The append says the "sha guard [is] clean after pycache remediation (`w1/SentinelFrozen.md`,
  `w1/ReviewScopeBound.md` F1 …)". The cited `SentinelFrozen.md` records the opposite:
  "**FAIL — kill-rule-1 failure** … guard diff: changed (exit 1) … do not report the frozen tree
  as unchanged", with a drift from `25ba8580…` to `ff0cbbc8…` plus an added
  `g9_port_digits.cpython-314.pyc`.
- Both drifts are still live: `g3_empty_path.cpython-314.pyc` exists with new bytes (mtime
  00:19:24) and `g9_port_digits.cpython-314.pyc` still exists.
- The guard cannot detect added files (`sha256sum -c` checks listed paths only), and there is no
  end-state guard file — `verification/sha-guard/` contains only `before.sha256`. Tracked source
  and receipt entries do verify; the byte-identity sentence is false only because it is stated
  over the whole frozen tree, pycache entries included.

### F2 (MEDIUM) — the cited receipts are overwritten in place, and two postdate the append

Both counting commands write over the receipt named as evidence:
`c45_freshness.py` → `verification/freshness/freshness.json`;
`c45_matrix.py` → `matrix/<stage>.json` and `honest-regression/after-v5-v2.json`.

Observed:

```text
2026-10-24 00:50:33  SCORECARD.md                                  (the append)
2026-10-24 00:56:55  freshness ran_at (freshness.json written 00:59:38)
2026-10-24 00:58     verification/selftest-coverage/after/m1..4.txt created
                     (the directory was empty when first listed during this review)
```

The freshness receipt and the after-coverage traces could not have been the append's source; the
append's freshness numbers came from an earlier run of the same command that was then overwritten.
Likewise "receipts re-derive (rerun the counting command)" cannot falsify a receipt in place: a
rerun replaces it. A reviewer must copy the tree first, and the append does not say so.

### F3 (MEDIUM) — the ledger "after all edits" claim has no post-edit receipt

```text
2026-10-24 00:13:59  .ufo/waves/round-45/verification/ledger-gate/before.txt
2026-10-24 00:50:33  SCORECARD.md
```

The only ledger artifact (`before.txt`, 36 minutes older than the append) records
`ledger-quotes: 3 figures, 0 mismatches`, exit 0. Re-running the checker now gives the same
`3 figures, 0 mismatches`, exit 0 — so the number is currently true, but the claimed post-edit
artifact does not exist and the file is even named `before`.

### F4 (MEDIUM) — the after-leg mutant files are not mutations of the measured driver, though the 4/4 number itself is true

`mutants/m1..4_v2.py` (unchanged since 00:38) do not derive from the committed driver:

```text
m1_v2 vs HEAD (f3c3171b): 55 changed lines      m1_v2 vs live tip (64bc3324): 2 changed lines
m2_v2 vs HEAD: 55                               m2_v2 vs live tip: 2
m3_v2 vs HEAD: 55                               m3_v2 vs live tip: 2
m4_v2 vs HEAD: 55                               m4_v2 vs live tip: 2
```

Against HEAD the diff includes whole missing features — `expected_tool_sha` receipt binding, the
`if not __debug__` guard, the `bad-build` fake mode and its cohort assertions — while the mutants'
tracebacks land at `m1_v2.py:449/323` versus HEAD's `477/351`. The append's "the same four
one-line mutations against driver v2's shipped selftest" therefore misdescribes the named files.

The *number* 4/4 nevertheless holds for the shipped bytes: I applied the four mutation lines to
the HEAD blob in scratch and ran its shipped selftest:

```text
h1 all        exit 1 | AssertionError
h2 timing     exit 1 | AssertionError
h3 legacy     exit 1 | AssertionError
h4 error-path exit 1 | AssertionError
```

So the result is right, but the named artifacts do not establish it and a reader cannot reproduce
shipped-selftest coverage from them. The recorded after traces (00:58) do show real assertion
failures at lines 181/184/182/212 — kills, not import crashes.

### F5 (LOW) — `classRuns:[]` misdescribes the committed v4 receipt

`v4-final/v4.json` has **no** `classRuns` key (`'classRuns' in keys → False`, value `None`) and no
`runs` key; the append says it carries `classRuns:[]`. The substantive claim (predicate names "the
ten class runs" while `classesMode="v4"`) is true.

### F6 (LOW) — "an unwired-gate mutant also dies" is unmeasured by the append's command

The counting command runs only `mutants/m1..4_v2.py`. `mutants/v2/m10.py` — the
`unwired-build-gate` class named in the driver comment, which the `_selftest_cohort` assertion
targets — has no executing receipt (`verification/selftest-coverage/after/` holds four traces).
The claim is plausible (the committed selftest passes and its cohort is end-to-end) but it is not
a measurement in this append.

## 2. Numbers that do re-derive (checked, verbatim)

- **C1 counts**: `before.json` → `invalid_accepted=3`, `honest_witnessed=27`,
  `honest_build_met=3`; `after.json` → `invalid_accepted=0`, `rejections_named=3`,
  `named_classes=[counter_error, stale_receipt, tool_absent]`, `honest_witnessed=27`,
  `honest_build_met=3`, honest `valid=true, problems=[]`.
- **Honest identity**: both stages ran `c44_count_v5.py`
  (`counterSha256=5cedaa3b…7672bc` = frozen v5, file hash matches), 27 witnessed **identical**
  name lists v1 vs v2, builds `[(True,None)×3]`, `errors=[]`.
- **Instrument hashes**: driver `f3c3171b…a076` = HEAD blob = receipt `driver_sha256`; counter
  `e17b5dc8…403b`; both runners are git-tracked.
- **Kill counts**: `m1=1 m2=0 m3=1 m4=0` → 2/4; `m1_v2..m4_v2=1,1,1,1` → 4/4 (direct
  `--selftest` runs, `-B`, no tree writes). Shipped-blob 4/4 shown in F4.
- **v4 flags**: committed `v4-final/v4.json` predicate contains "class runs" → **true**,
  `classesMode="v4"`; fresh `v6v4/counter-v4.json` predicate `"…(the eleven v4 runs)…"` →
  **false**, `runs` count **11**, `classRuns=[]`, `V4_EXIT=0`.
- **Receipt hashes**: `9dead4d7…c076d1` (`after-final/after-v5.json`) and `2383efae…ce0902`
  (`claim/after-v5.json`) both match the append.
- **Witness split**, recomputed with the receipt's own jq predicate:
  after-final → `{class_only:26, mixed:1, met:0, other:0}` (append correct);
  `claim/after-v5.json` → `{class_only:22, mixed:1, met:4, other:0}` (attribution correct).
- **v6 minimality**: stored `v6diff/v5-v6.diff` has 3 hunks; recomputed `diff -u` also 3;
  `PREDICATE_V5` equals v5's `PREDICATE` literally (string equality, same text sha).
- **Fixture provenance**: `fixtures/counter-error/control-receipt.json` (sha `03ee73f6…c969`)
  equals `claim/after-final/tools/headtail-V1.json`; `build-receipt.json` (`bebfe7f3…ee07`)
  equals `build-1.json` — byte copies as claimed.
- **Stale-class causality** (scratch): committed backdated fixture (exit 0, 5 s backdate) →
  `stale_receipt`; byte-identical copy with `os.utime` removed → `witnessed=1/1`, no error:

```text
backdated:  ctl1 G5 met=False caught=G2   stale_receipt      driver_exit=1
fresh:      ctl1 G5 met=False caught=G2   (no error)         witnessed=1/1
```

- **"four wave-1 seats"**: `CriticC2Scope`, `ExecWitnessSplit`, `ReviewKillRules`,
  `ReviewWave1Plan` independently name the misattribution — claim holds.

## 3. Verdict on the named attack

**Numeric re-derivation: PASS.** Every integer and every sha in the measured append re-derives
from the artifact it names, including the two values most at risk: kills 4/4 (true both for the
named mutant files and, tested independently, for the shipped committed selftest) and the
26/1/0 versus 22/1/4 split with correct receipt attribution.

**Evidence-integrity claims: FAIL (partial).** Three prose claims do not survive: (1) the sha
guard is not clean and the cited SentinelFrozen report records FAIL; (2) the ledger "after all
edits" receipt does not exist (a re-run is green, but the artifact is `before.txt`, 36 min older);
(3) the after-leg mutant files are not one-line mutations of the measured driver (55-line diff),
so the named artifacts underdetermine the 4/4 they are cited for. Plus one misdescribed field
(`classRuns:[]` does not exist) and one unmeasured claim (the unwired-gate mutant).

## 4. Residual risk and unrun checks

- `c45_matrix.py --stage before|after` was **not** re-run end-to-end (time-box): fixture legs were
  re-derived through the driver, and the honest 27-control leg was verified from its summary
  identity fields only, not re-executed.
- `c45_freshness.py` was **not** re-run as a unit (a rerun would overwrite the cited receipt, F2);
  its three legs were re-derived separately (eight mutant executions, jq split, predicate parse).
- The lane changed during review; re-hash `c45_audit.py` at final tip. At 01:02 the live tip is the
  uncommitted `64bc3324…` (selftest passes, mutants 1-line), not the append's `f3c3171b…`.
- `jq` on this host is `jaq 3.1.1` exposed as `jq`; the freshness split leg depends on that name.
- LSP unavailable (recorded above); no semantic reference/definition proof was possible.
- No tools installed.

## 5. Files written

- `.ufo/waves/round-45/w2/AttackMeasurementAppend.md` (this report)
- Scratch only: `/fast/scratch/hyaku/kake-r45/AttackMeasurementAppend/` — eight mutant selftest
  transcripts, `head_c45_audit.py` (HEAD blob), `h1..h4_mut.py`, `fx1/`, `fx2/`, `out-fx1/`,
  `out-fx2/`.
