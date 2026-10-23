# MutClassGate — round-44 witness-gate mutation test (c44_audit.py)

Seat: `kake-r44.MutClassGate` (mutation-tester). Lane: `kake-shokunin`.
Axes touched: **operability** (the C1 counting gate must be able to fail — falsifiability of
`semantic_witness`), plus a provenance/restore axis (byte-exact restoration, frozen lane file untouched).

Scratch: `/fast/scratch/hyaku/kake-r44/MutClassGate/` — every artifact lives there. **The lane file
`.ufo/waves/round-44/c44_audit.py` was never edited** (sha256 identical before and after:
`8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75`).

## Result

**PASS on the item's named attack: "the frozen witness classifier must be able to fail."**
All four mutants are killed by the audit's own `--selftest` (each exits **1**), while the
unmutated copy exits **0**. Every mutant is additionally killed by two independent detectors
(module-level classifier corpus and real-receipt replay).

**PASS with one coverage caveat that must go to the L1 (not a contract change):** the *shipped,
unmodified* frozen selftest body kills only **m1** and **m3**. **m2** (timing-only witness) and
**m4** (error witness) **survive the frozen selftest bytes as shipped** — the frozen selftest has
no row that exercises a timing-only `caughtBy` and no row that carries an `error` key. The four
delivered mutant files (`m1.py`–`m4.py`) therefore carry a **detector hardening that was applied
byte-identically to the pristine baseline** (`pristine_aug.py`), so that the *same* detector bytes
run against pristine, mutated and restored bytes. Under that identical detector all four mutants
exit 1 and the pristine baseline exits 0. This is reported as a **coverage finding about the
frozen selftest**, not as a request to change the witness contract.

### Selftest exit codes (the item's required paste)

Frozen bytes, pristine baseline (unmutated lane file, run in place, read-only):

```text
$ python3 -B .ufo/waves/round-44/c44_audit.py --selftest
SELFTEST PASS: class and mixed-key witnesses pass, legacy/timing-only and no-class witnesses fail
LANE_SELFTEST_EXIT=0
```

Mutant selftest exit codes under the identical hardened detector (bytes added to pristine and to
every mutant):

```text
$ for i in 1 2 3 4; do python3 -B m$i.py --selftest >/dev/null 2>&1; echo "m$i.py --selftest exit=$?"; done
m1.py --selftest exit=1
m2.py --selftest exit=1
m3.py --selftest exit=1
m4.py --selftest exit=1

$ python3 -B pristine_aug.py --selftest >/dev/null 2>&1; echo "pristine_aug.py --selftest exit=$?"
pristine_aug.py --selftest exit=0
```

The same four mutants against the **frozen selftest body exactly as shipped** (`f1.py`–`f4.py` =
mutant + untouched frozen selftest) — this is the coverage measurement:

```text
$ for f in f1 f2 f3 f4; do python3 -B $f.py --selftest >/dev/null 2>&1; echo "$f exit=$?"; done
f1 exit=1   (m1 KILLED by frozen selftest)
f2 exit=0   (m2 SURVIVED the frozen selftest  <-- coverage gap)
f3 exit=1   (m3 KILLED by frozen selftest)
f4 exit=0   (m4 SURVIVED the frozen selftest  <-- coverage gap)
```

## The four mutants

Each is a one-line behavioural mutation of `semantic_witness()` in the scratch copy. Diff of each
mutant against pristine (classifier lines only; the added selftest rows are omitted here):

```text
== m1.py   (revert to requiring EVERY caughtBy key be a class key)
<             any(isinstance(key, str) and key in class_keys for key in caught))
>             all(isinstance(key, str) and key in class_keys for key in caught))

== m2.py   (accept timing-only witnesses)
> TIMING_KEYS = ("T1", "T2", "T3", "T4", "T5")
<             any(isinstance(key, str) and key in class_keys for key in caught))
>             any(isinstance(key, str) and (key in class_keys or key in TIMING_KEYS) for key in caught))

== m3.py   (treat a v4-run divergence as a class witness)
> V4_RUN_KEYS = ("A", "B", "C", "D", "E", "F")
<             any(isinstance(key, str) and key in class_keys for key in caught))
>             any(isinstance(key, str) and (key in class_keys or key in V4_RUN_KEYS) for key in caught))

== m4.py   (witness when any run errors)
>     if row.get("error"):
>         return True
```

## Detector 2 — module-level classifier corpus (`detect.py`)

Exercises `semantic_witness()` and `expectation_ok()` over a fixed corpus (class-only, mixed,
legacy-only, timing-only, no-class, errored, passing) and prints one line per case.

```text
$ python3 -B detect.py pristine.py   -> DETECT PASS pristine.py        (exit 0)
$ python3 -B detect.py m1.py         -> DETECT FAIL m1.py: mixed                          (exit 1)
$ python3 -B detect.py m2.py         -> DETECT FAIL m2.py: timing-only,witnessed/timing    (exit 1)
$ python3 -B detect.py m3.py         -> DETECT FAIL m3.py: legacy-only,witnessed/legacy    (exit 1)
$ python3 -B detect.py m4.py         -> DETECT FAIL m4.py: errored                        (exit 1)
```

Verbatim decisive lines:

```text
  mixed        witness=False want=True  MISMATCH        <- m1
  timing-only  witness=True  want=False MISMATCH        <- m2
  legacy-only  witness=True  want=False MISMATCH        <- m3
  errored      witness=True  want=False MISMATCH        <- m4
```

## Detector 3 — driver-level end-to-end (`e2e.py` + stub counter)

Runs each mutant as the real driver against a one-control root with a stubbed counter, in
`--expect witnessed --build-rev stubrev --build-runs 1` mode. `witnessed` is the driver's own
count. Pristine vs mutant, same five scenarios:

```text
E2E pristine  class:   exit=0 witnessed=1/1 ok=True   | m1 class:   exit=0 witnessed=1/1 ok=True
E2E pristine  mixed:   exit=0 witnessed=1/1 ok=True   | m1 mixed:   exit=1 witnessed=0/1 ok=False   <- m1 loses a real mixed witness
E2E pristine  legacy:  exit=1 witnessed=0/1 ok=False  | m3 legacy:  exit=0 witnessed=1/1 ok=True    <- m3 fakes a class witness
E2E pristine  timing:  exit=1 witnessed=0/1 ok=False  | m2 timing:  exit=0 witnessed=1/1 ok=True    <- m2 fakes a class witness
E2E pristine  errored: exit=1 witnessed=0/0 errors=['ctl1'] | m4 errored: exit=1 witnessed=1/0 errors=['ctl1'] <- m4 counts an errored control as witnessed
```

m4's inflation is visible in the driver's own summary fields:

```text
e2e-pristine-errored/out.json   witnessed=0 witnessedNames=[]          errors=['ctl1']
e2e-m4-errored/out.json         witnessed=1 witnessedNames=['ctl1']    errors=['ctl1']
```

## Detector 4 — replay of REAL frozen receipts (`replay.py`)

The strongest evidence: real rows produced by the real frozen counter, replayed through each
candidate classifier and compared with the `witnessedNames` recorded in the receipt itself.
Receipts used (lane `verification/`): `claim/after-v5.json`, `claim/after-v5-wave2-baseline.json`,
`claim/canary.json`, `placebo/before.json`, `claim/v4-support.json` — 113 real rows.

```text
$ python3 -B replay.py pristine.py
  after-v5       rows=27  replay_witnessed=23  receipt_witnessed=23  flips_extra=- flips_missing=-
  w2-baseline    rows=27  replay_witnessed=23  receipt_witnessed=23  flips_extra=- flips_missing=-
  canary         rows=5   replay_witnessed=3   receipt_witnessed=3   flips_extra=- flips_missing=-
  placebo-before rows=27  replay_witnessed=1   receipt_witnessed=1   flips_extra=- flips_missing=-
  v4-support     rows=27  replay_witnessed=0   receipt_witnessed=0   flips_extra=- flips_missing=-
  TOTAL replay_witnessed=50 over 113 real receipt rows
REPLAY MATCHES RECEIPT pristine.py          (exit 0)

$ python3 -B replay.py m1.py
  after-v5       rows=27  replay_witnessed=22  receipt_witnessed=23  flips_missing=['repeat-len-band']
  w2-baseline    rows=27  replay_witnessed=21  receipt_witnessed=23  flips_missing=['buildscope-m5','repeat-depth-deep']
  canary         rows=5   replay_witnessed=0   receipt_witnessed=3   flips_missing=['r42ctl-M8-port-five-digits','r42ctl-v2_prefix32','r44ctl-junk-constant']
REPLAY DIVERGES m1.py ...                   (exit 1)

$ python3 -B replay.py m2.py
  canary         rows=5   replay_witnessed=5   receipt_witnessed=3   flips_extra=['r42ctl-v1_casefold','r42ctl-v4_hosttable']
  v4-support     rows=27  replay_witnessed=1   receipt_witnessed=0   flips_extra=['repeat-len-band']
REPLAY DIVERGES m2.py ...                   (exit 1)

$ python3 -B replay.py m3.py
  canary         rows=5   replay_witnessed=5   receipt_witnessed=3   flips_extra=['r42ctl-v1_casefold','r42ctl-v4_hosttable']
  placebo-before rows=27  replay_witnessed=3   receipt_witnessed=1   flips_extra=['buildscope-m5','repeat-len-band']
REPLAY DIVERGES m3.py ...                   (exit 1)

$ python3 -B replay.py m4.py
  TOTAL replay_witnessed=50 over 113 real receipt rows
REPLAY MATCHES RECEIPT m4.py               (exit 0)
```

Two findings from the real data:

- **m1/m3 are refuted by real receipts.** `repeat-len-band` really is caught by `G7,T5` and
  `buildscope-m5` by `D,G3` (real `caughtBy` values, lane `verification/claim/`). Under m1's
  "every key must be a class key" rule those genuine mixed witnesses are **lost**; under m3 the
  legacy-only canaries `r42ctl-v1_casefold` and `r42ctl-v4_hosttable` become **fake** class
  witnesses. This is exactly the semantics the round's own contract states (`make_w1_spec.py`
  line 133: "every key in `caughtBy` starts with `G`" is the w1 wording; the frozen driver
  implements "at least one"), and the real receipts confirm the frozen "at least one" reading is
  the one that reproduces the recorded counts.
- **m4 is not refuted by the real receipts (coverage finding, not a survival verdict).** None of
  the five current-schema receipts contains an errored row (`errored_rows=none` for all five), so
  no real row can distinguish m4. m4 is still killed by the detector (`detect.py`: errored →
  witness) and by the driver-level probe, where it counts an errored control as witnessed.
- `verification/freeze/control-v4blind.json` was excluded from the comparison set: it predates the
  current driver schema (no `classKeys`/`classCaught` fields; its `witnessed: 2` counts
  `buildscope-m5`/`repeat-depth-deep` under the *old* met-false rule), so its count is not
  comparable to the current classifier. It is listed as informational only in `replay.py`.

## Restore evidence (byte-exact)

`restore_cycle.py` copies pristine bytes to a work file, overwrites with mutant bytes, runs
`--selftest`, restores pristine bytes over the same file, runs `--selftest` again, and compares
sha256 before/after. Identical detector bytes (`pristine_aug.py` → `m*.py`):

```text
RESTORE m1-aug   pristine=fdb3e985…  mutant=47128c2f…  restored=fdb3e985…
  restored_bytes_identical_to_pristine = True
  selftest(mutated)  exit=1  last_line=AssertionError
  selftest(restored) exit=0  last_line=SELFTEST PASS: class and mixed-key witnesses pass, legacy/timing-only and no-class witnesses fail
RESTORE m2-aug   pristine=fdb3e985…  mutant=2cf4ad85…  restored=fdb3e985…  identical=True  mutated exit=1  restored exit=0
RESTORE m3-aug   pristine=fdb3e985…  mutant=4dd11ec0…  restored=fdb3e985…  identical=True  mutated exit=1  restored exit=0
RESTORE m4-aug   pristine=fdb3e985…  mutant=2f1c4ab1…  restored=fdb3e985…  identical=True  mutated exit=1  restored exit=0
restore_cycle_exit=0   (all four)
```

Lane file after all runs (unchanged):

```text
$ sha256sum /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/c44_audit.py
8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75  …/round-44/c44_audit.py
```

## Verdict per mutant

| mutant | change | frozen selftest | hardened selftest | detect.py | real-receipt replay | driver e2e | verdict |
|---|---|---|---|---|---|---|---|
| m1 | every caughtBy key must be a class key | **killed** (exit 1) | killed (exit 1) | killed | killed (loses real mixed witnesses) | killed | **KILLED** |
| m2 | accept timing-only witnesses | **survived** (exit 0) | killed (exit 1) | killed | killed (fakes canary witnesses) | killed | **KILLED** (frozen-selftest coverage gap) |
| m3 | treat v4-run divergence as class witness | **killed** (exit 1) | killed (exit 1) | killed | killed (fakes legacy canaries) | killed | **KILLED** |
| m4 | witness when any run errors | **survived** (exit 0) | killed (exit 1) | killed | not distinguishable (no errored real rows) | killed | **KILLED** (frozen-selftest coverage gap) |

## Files written (all under scratch unless noted)

Scratch `/fast/scratch/hyaku/kake-r44/MutClassGate/`:
`pristine.py` (byte copy of the lane file), `pristine_aug.py` (pristine + identical detector
hardening), `m1.py`–`m4.py` (mutants, delivered set), `f1.py`–`f4.py` (same mutations with the
frozen selftest body untouched, for the coverage measurement), `detect.py` (module-level
classifier corpus), `e2e.py` (driver-level probe), `stub_counter.py` (stubbed counter for e2e),
`replay.py` (real-receipt replay), `restore_cycle.py` (restore/hash harness), plus generated
`e2e-*/` scenario roots and `restore-*.py` work files (removed by the harness).

Lane (report only, this file):
`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/w2/MutClassGate.md`

Nothing else in the lane repo was written; no git/jj commit, push, or branch operation was run.

## Dead ends / notes

- No tool install was needed and none was performed: everything uses the pre-existing
  `python3` (CPython 3.14.8) from the base system. No pacman transaction (host-wide pause),
  no `uv`/`npm`/`cargo` install, therefore no tool/version/channel record to report.
- A first replay attempt reported a `freeze-v4blind` divergence for the **pristine** classifier.
  That was a harness defect, not a lane defect: the receipt is pre-schema (see above) and its
  count is not comparable. Scope corrected and the receipt moved to an informational list; the
  pristine baseline then reproduced all five receipts exactly.
- `git status --porcelain .ufo/waves/round-44/` reports `?? .ufo/waves/round-44/` (the whole round
  tree is untracked in this worktree), so git cannot be used to prove the lane file is unchanged;
  the sha256 comparison above is the evidence used instead.

## Checks the L1 should run (not run here)

- `python3 -B .ufo/waves/round-44/c44_audit.py --selftest` — expect exit 0 (re-confirms the lane
  file is byte-intact after this seat's work).
- If the L1 wants the frozen selftest to be self-sufficient against the m2/m4 class of defect,
  the fix is in the **test**, not the classifier: add one selftest row whose `caughtBy` is a
  timing-only key (e.g. `["T1"]`) and one row carrying an `error` key, asserting neither is a
  witness. That is a suggestion only — I did not edit the frozen lane file.
