# ScoutCounterC1Base — C1 do-nothing control at the base revision

Seat: `L1Kake51.ScoutCounterC1Base-2` (scout, leaf). Axis under test: **operability** (C1).
Scope: run the frozen C1 counter against the base revision, record exact bytes, state which
checks fail, and attack the control's discriminative power. No files written except this one.

## 1. Command and raw result

Instrument used: the lane-tip ledger `c51_wave_ledger.py` (blob at tip `9d13768`) run against
**base bytes** `007d66e4e8360a5f88d29a93eeedd8066dad4434`. This is the correct construction: the
counter is fixed, only the measured bytes vary.

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-51/c51_wave_ledger.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin \
  --revision 007d66e4e8360a5f88d29a93eeedd8066dad4434
```

stdout (verbatim):

```
C1 ledger 0/3 met=False  (met: ledger_checks_passed == 3 of 3)
  L1 FAIL
    - settlement receipt absent at the measured revision
  L2 FAIL
    - route map absent at the measured revision
  L3 FAIL
    - settlement receipt absent at the measured revision
  revision: 007d66e4e8360a5f88d29a93eeedd8066dad4434
```

Exit code: **1**.

## 2. Which checks fail, with the exact note each prints

| check | state | exact note |
|---|---|---|
| L1 (seat accounting) | **FAIL** | `settlement receipt absent at the measured revision` |
| L2 (route receipts)   | **FAIL** | `route map absent at the measured revision` |
| L3 (time accounting)  | **FAIL** | `settlement receipt absent at the measured revision` |

All three are the *absence* branch, not a counting mismatch. Reading
`c51_wave_ledger.py:98-104, 168-174, 203-212`, each check returns before computing anything when
its first required artifact is missing, so `facts` is `{}` in the `--json` rendering (verified;
`ledger_checks_passed: 0`, `met: false`).

## 3. Why they fail — observed mechanism

- `.ufo/waves/round-51` **does not exist at all** at the base revision:
  `git ls-tree -r --name-only 007d66e4... -- .ufo/waves/round-51` returns nothing.
  `git cat-file -e 007d66e4:<path>` is absent for `settlement.json`, `route-map.json`,
  `wave-timing.json`, `round-time-accounting.json`.
- The absence is round-51-specific, not a broken root or revision:
  - `007d66e4` resolves and is an **ancestor** of the lane tip (`git merge-base --is-ancestor` → true).
  - The base tree carries `.ufo/waves/round-21` … `round-50`, and
    `round-50/settlement.json` plus `round-50/w1/` are **present** at base. So prior rounds'
    evidence is committed there; round 51 simply has none yet.
- Both other invocations agree: `--root .` from the lane root and the absolute `--root` give
  byte-identical stdout; short hash `007d66e` also resolves and yields the same three notes.

## 4. Verdict on the control itself

- **Do-nothing control behaves as the contract requires**: `controls/c1-before-base.txt` asserts
  `0 of 3`; my run reproduces that file **byte-for-byte** (`diff` clean, revision line included).
- **Deterministic**: two consecutive runs produce identical stdout
  (sha256 `a1d1c087c02512df6d40b63f8fe4c8ccfb26abef8f4af7ce33ee99ee6d320753`).
- **Reads committed bytes only** (contract claim, independently confirmed): at the base revision a
  `route-map.json` exists in the local working tree, uncommitted, and L2 still prints
  `route map absent at the measured revision`. The counter uses `git show` / `git ls-tree`
  exclusively, so worktree-only evidence cannot move it.
- **Not vacuous**: the L1 counting path does fire on real mismatches — see §5.2, where I reproduced
  the committed junk-wave receipt's body exactly.

## 5. Attacks found (operability sharpness)

### 5.1 Absence is indistinguishable from a misinvocation
`check_l1/l2/l3` call `show()`/`show_json()`, which map *every* git failure — file absent,
revision unparsable, root not a repository — to `None` and then to the same
"absent at the measured revision" note. Reproduced both ways:

```
--revision deadbeefdeadbeefdeadbeefdeadbeefdeadbeef
  → identical three notes, exit 1
--root /tmp --revision 007d66e4...
  → identical three notes, exit 1
```

Consequence: any typo in `<commit>` in the frozen counting command is reported as legitimate
wave-evidence absence, with no distinct signal. The control cannot fail *loudly* for a bad
invocation; it fails quietly for the wrong reason. No false **pass** is possible (absence can only
lose a check), so the predicate is safe; the diagnostic is what blurs.

### 5.2 The committed junk-wave control is not re-derivable from committed bytes
`controls/c1-junk-wave.txt` cites `revision: d969fa2819f1f2050c10637531cba2e12f92a557`. That object
**does not exist** in the lane repo (`git cat-file -t` → `could not get object info`; not contained
in any ref via `git for-each-ref --contains`) nor in the fleet repo
(`/home/vgpnk/Projects/shokunin`). The hash occurs in exactly one place on disk: that receipt file.
No builder script for the junk wave is committed under `round-51/` (no match for "junk" in any
script there).

So the receipt is **consistent with the current code but unreproducible**: I rebuilt an equivalent
junk wave in `/tmp/w1scout-junk` (40 seats, 25 committed reports, `reports_written: 40`, one used
route without a receipt, one orphan receipt with `httpStatus: null`) and its output body matched
`c1-junk-wave.txt` **exactly**, line for line, excluding the revision line:

```
EXACT BODY MATCH: True
  L1 FAIL
    - settlement reports_written 40 != committed report files 25
    - seats marked with a report but no committed file: ['Seat25', ..., 'Seat39']
  L2 FAIL
    - no committed probe receipt for used route devin/swe-2-max
    - probe receipt for xai-oauth/grok-4.7-fast carries no integer httpStatus
  L3 FAIL
    - wave timing bytes absent at the measured revision
```

Reading: the junk receipt was a genuine run against a scratch root that was not preserved. As an
artifact it is therefore a **claim, not a re-derivation** — which is precisely the property C1
exists to enforce. Of the two committed controls (`c1-before-base.txt`, `c1-junk-wave.txt`), only the
first is re-derivable from committed bytes.

### 5.3 The control does not discriminate "not started" from "settled but receipts uncommitted"
At the lane tip the same counter prints the **same three notes**, byte-identically to the base run,
even though tip commits `contract.json`, both counters, `sources/`, and the full
`assimilation/pre-append/` tree. The missing artifacts differ in number and kind between the two
revisions; the output does not reflect that. The junk-wave receipt shows the counter *can* say more
when the files are present, but the absence branch collapses the distinction.

### 5.4 Minor: shared note text across checks
L1 and L3 print the identical sentence for two different required files (both name the settlement,
which L3 genuinely needs too, but the note carries no check id). Only the outer `L1`/`L3` label
separates them; in `--json`, `checks.L1.notes == checks.L3.notes` verbatim.

## 6. What this control does **not** establish

- It says nothing about a passing run: no committed control demonstrates `3/3`. The pass path
  (L1 counting equality, L2 receipt adequacy, L3 arithmetic agreement with `LOG.md`) remains
  unexercised, as expected while C1 is honestly 0/3.
- L3's arithmetic (aggregate seat seconds, dead-seat seconds, wall clock vs `round-time-accounting.json`)
  is never reached at base, so this run provides no evidence about it.
- No claim is made about C2 (`c51_quote_truth.py`); that is another seat.

## 7. Confidence

- "base scores 0/3, exit 1, notes as quoted" — **observed**, deterministic, matches the committed
  receipt.
- "counter reads committed bytes only" — **observed** (uncommitted worktree route map ignored).
- "junk receipt unreproducible because its revision is absent from both repos" — **observed**
  (`git cat-file`, `for-each-ref`, filesystem grep).
- "the same scratch-run code produced the junk body" — **inference**, strongly supported by the
  exact body match of my reconstruction.

## 8. Tooling

No installs or upgrades were performed. All work read-only; scratch confined to
`/tmp/w1scout-junk`. Only this report was written in the lane.
