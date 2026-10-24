# MutDriverV2Spec — mutation attack on the C1 driver v2 (`c45_audit.py`)

Seat `kake-r45.MutDriverV2Spec` (mutation-tester). Lane `kake-shokunin`, round-45 wave 1.
Axes: **operability** (falsifiability of the receipt-validity gate), **freshness** (is the gate
wired where the receipts are actually produced?).

Scratch: `/fast/scratch/hyaku/kake-r45/MutDriverV2Spec/` (all harnesses + detector outputs).
Mutants: `.ufo/waves/round-45/mutants/v2/m{1..11}.py` (my item's named path; `ExecMutantMatrix`
owns `mutants/m{1..4}.py` + `mutants/m{1..4}_v2.py` — disjoint from `mutants/v2/`).

## Result in one line

**All six named attacks are killed by the shipped v2 `--selftest` (m1–m6, exit 1) and the honest
`--selftest` stays green (exit 0) — but four *wiring* mutants (m8–m11) survive the shipped
selftest while being behaviourally refuted end-to-end. That is the coverage finding: the v2
selftest proves `receipt_validity()` correct, not that the driver *calls* it correctly.**

## Baseline drift (recorded, not a defect)

`c45_audit.py` is owned by `ExecDriverV2` and was rewritten under me at 00:17:32 while I worked:

```text
a9c956c58dbd339771a848f5a5eadb825a07670bb747be459856178c49e39ca4   snapshot taken 00:17:08
5a342e29c7e872d992cfedc26de849c010d197bb82162e007a61a55d915c7051   lane file (final; all numbers below)
```

The diff was a non-gate robustness change (`rec` may not be a dict: `receipt_data = rec if
isinstance(rec, dict) else {}`). I re-snapshot to `5a342e29…`, re-derived every mutant against
those bytes, and re-ran every detector. Both snapshots gave the identical mutant verdicts. **Every
number in this report is against `5a342e29c7e872d992cfedc26de849c010d197bb82162e007a61a55d915c7051`**,
which was still the lane hash after my last run.

## The mutants (single-point, exact-diff verified)

Each is a byte-copy of `c45_audit.py` with one behaviour-bearing edit; `make_mutants.py` asserts
every anchor matches exactly once, so a silent no-op mutation is impossible.

```text
m1  sha=5693ab2e84732835  -    if exit_code not in (0, 1): / -        return False, "counter_error"
m2  sha=43f82320354ad882  -    if receipt.get("note") == "tool absent": / -        return False, "tool_absent"
m3  sha=28602a382501baa8  -    try: … in_window = lower_ns <= receipt_mtime_ns <= upper_ns …
                          +    in_window = True  # MUTANT m3: freshness window removed
m4  sha=47473064e713d703  -    if receipt.get("counterSha256") != counter_sha: / -        return False, "stale_receipt"
m5  sha=cb4156d4b6481fac  -    return [row for row in rows if row_valid(row) and row.get("met") is False]
                          +    return [row for row in rows if row.get("met") is False]
m6  sha=67faa77c03713373  -    count_ok = build_runs <= 0 or len(build) == build_runs → True
                          -    if build_runs > 0 and len(build) != build_runs: / -        return False
m7  sha=3c06b3d0e7772020  -    if "seed" not in receipt or receipt["seed"] is None: / -        return False, "stale_receipt"
m8  sha=87651a162e2d7f71  -                    error=validity_error, _valid=valid)
                          +                    error=None, _valid=True)          # control wiring ignores validity
m9  sha=c4fd3aa4b434de41  -            rec, code, (mtime_ns, started_ns - MTIME_EPS_NS, finish_ns + MTIME_EPS_NS), counter_sha)
                          +            rec, code, (mtime_ns, 0, 2**62), counter_sha)   # window always satisfied
m10 sha=fbebcd931281ed68  -                    "error": validity_error, "_valid": valid}
                          +                    "error": None, "_valid": True}     # build wiring ignores validity
m11 sha=6ef3bfdd0fa1d23b  -MTIME_EPS_NS = 1_000_000_000
                          +MTIME_EPS_NS = 10 ** 18  # window widened
```

m1–m6 are the item's six named attacks; m7 (seed gate) and m8–m11 (wiring) are additional probes.

## Decisive output 1 — the shipped v2 selftest (the item's named requirement)

```text
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ python3 -B .ufo/waves/round-45/c45_audit.py --selftest
SELFTEST PASS: v1 assertions plus timing-only, invalid receipt, error-row, and build-count gates
PRISTINE_SELFTEST_EXIT=0

$ for i in $(seq 1 11); do python3 -B .ufo/waves/round-45/mutants/v2/m$i.py --selftest; done
m1  selftest_exit=1  AssertionError
m2  selftest_exit=1  AssertionError
m3  selftest_exit=1  AssertionError
m4  selftest_exit=1  AssertionError
m5  selftest_exit=1  AssertionError
m6  selftest_exit=1  AssertionError
m7  selftest_exit=1  AssertionError
m8  selftest_exit=0  SELFTEST PASS: v1 assertions plus timing-only, invalid receipt, error-row, and build-count gates
m9  selftest_exit=0  SELFTEST PASS: v1 assertions plus timing-only, invalid receipt, error-row, and build-count gates
m10 selftest_exit=0  SELFTEST PASS: v1 assertions plus timing-only, invalid receipt, error-row, and build-count gates
m11 selftest_exit=0  SELFTEST PASS: v1 assertions plus timing-only, invalid receipt, error-row, and build-count gates
```

The kill is the *intended* assertion, not an incidental failure (each traceback's last `assert`):

```text
m1  assert receipt_validity(receipt, 2, in_window, "counter-sha") == (False, "counter_error")
m2  assert receipt_validity(dict(receipt, note="tool absent"), 1, in_window,
m3  assert receipt_validity(receipt, 1, (111, 90, 110), "counter-sha") == (False, "stale_receipt")
m4  assert receipt_validity(dict(receipt, counterSha256="other-sha"), 1, in_window,
m5  assert not not_met_rows([error_row])
m6  assert not expectation_ok("witnessed", [class_divergence, mixed_divergence],
m7  assert receipt_validity({"counterSha256": "counter-sha", "note": None}, 1,
```

## Decisive output 2 — module-level contract detector (`detect.py`)

Imports the driver and asserts the C1 contract over a fixed corpus (all refusal classes, not-met
exclusion, build-count pin, timing/legacy non-witnesses).

```text
$ python3 -B detect.py pristine_v2.py
DETECT PASS pristine_v2.py                         (exit 0)
$ python3 -B detect.py mutants/v2/mN.py
m1  detect_exit=1 mismatches=2      m7  detect_exit=1 mismatches=1
m2  detect_exit=1 mismatches=1      m8  detect_exit=0 mismatches=0
m3  detect_exit=1 mismatches=2      m9  detect_exit=0 mismatches=0
m4  detect_exit=1 mismatches=1      m10 detect_exit=0 mismatches=0
m5  detect_exit=1 mismatches=1      m11 detect_exit=0 mismatches=0
m6  detect_exit=1 mismatches=2
```

## Decisive output 3 — real committed fixtures (`fixture_detect.py`)

Runs each driver over `.ufo/waves/round-45/fixtures/{counter-error,tool-absent,stale-planted}` plus
`fixtures/honest`, `--classes v5 --expect witnessed --build-rev 020bc457 --build-runs 3`.
`refutations` counts a class that got witness/not-met/build credit while invalid, plus any honest
regression.

```text
pristine_v2.py  refutations=0     m4  refutations=2 (counter-error, tool-absent)
m1  refutations=0                 m5  refutations=2 (counter-error, tool-absent → notMet=1)
m2  refutations=1 (tool-absent)   m6  refutations=0
m3  refutations=0                 m7  refutations=0
                                  m8  refutations=2 (counter-error, tool-absent)
                                  m9  refutations=0
                                  m10 refutations=2 (counter-error, tool-absent → build_met=3/3)
                                  m11 refutations=0
```

Pristine, verbatim (exit 1 on all three invalid classes, honest green):

```text
  counter-error  witnessed=0 notMet=0 build_met=0 errors=['ctl1:counter_error', 'build#1:stale_receipt', 'build#2:stale_receipt', 'build#3:stale_receipt'] exit=1
  tool-absent    witnessed=0 notMet=0 build_met=0 errors=['ctl1:tool_absent', 'build#1:stale_receipt', 'build#2:stale_receipt', 'build#3:stale_receipt'] exit=1
  stale-planted  witnessed=0 notMet=0 build_met=0 errors=['ctl1:counter_error', 'build#1:counter_error', 'build#2:counter_error', 'build#3:counter_error'] exit=1
  honest         HONEST ok=True witnessed=1 build_met=3 exit=0
FIXTURE pristine_v2.py         refutations=0
```

m4 / m5 / m10 verbatim (credit where the contract forbids it):

```text
m4  counter-error  … build_met=3 errors=['ctl1:counter_error'] exit=1   <== INVALID CLASS CREDITED
m4  tool-absent    … build_met=3 errors=['ctl1:tool_absent']    exit=1   <== INVALID CLASS CREDITED
m5  counter-error  … notMet=1 …  exit=1                                  <== INVALID CLASS CREDITED
m5  tool-absent    … notMet=1 …  exit=1                                  <== INVALID CLASS CREDITED
m8  counter-error  witnessed=1 notMet=1 … exit=1                         <== INVALID CLASS CREDITED
m8  tool-absent    witnessed=1 notMet=1 … exit=1                         <== INVALID CLASS CREDITED
m10 counter-error  … build_met=3 errors=['ctl1:counter_error'] exit=1    <== INVALID CLASS CREDITED
m10 tool-absent    … build_met=3 errors=['ctl1:tool_absent']    exit=1    <== INVALID CLASS CREDITED
```

## Decisive output 4 — scope-isolated end-to-end detector (`e2e2.py` + stub counter)

Four defect classes (`exit2`, `note`, `badsha`, `stale`, plus `noseed`) injected into *control*
receipts only, *build* receipts only, and both; each run in `--expect witnessed` and
`--expect not-met`. `credited` = the driver gave witness/not-met credit to an invalid control, or
build credit to an invalid build.

```text
pristine   e2e_credited=0     m5  e2e_credited=20    m9  e2e_credited=4
m1  6     m2  6     m3  6     m6  e2e_credited=0     m10 e2e_credited=10
m4  6     m7  6                m8  e2e_credited=20    m11 e2e_credited=6
```

The freshness-window leg, same command, same bytes:

```text
pristine  witnessed ctl:stale    exit=1 ok=False witnessed=0 notMet=0 build_met=1 errors=['ctl1:stale_receipt']
m3        witnessed ctl:stale    exit=0 ok=True  witnessed=1 notMet=1 build_met=1 errors=[]   <== INVALID CREDITED
m9        witnessed ctl:stale    exit=0 ok=True  witnessed=1 notMet=1 build_met=1 errors=[]   <== INVALID CREDITED
m11       witnessed ctl:stale    exit=0 ok=True  witnessed=1 notMet=1 build_met=1 errors=[]   <== INVALID CREDITED
pristine  not-met  ctl:stale     exit=1 ok=False witnessed=0 notMet=0 build_met=1 errors=['ctl1:stale_receipt']
m5        not-met  ctl:stale     exit=1 ok=False witnessed=0 notMet=1 build_met=1 errors=['ctl1:stale_receipt']   <== INVALID CREDITED
```

Honest path is invariant for **every** mutant (so no mutant is a mere honest-path breaker, and no
mutant can be dismissed as equivalent):

```text
all of m1..m11:  witnessed honest exit=0 ok=True witnessed=1 notMet=1 build_met=1 errors=[]
                 not-met   honest exit=0 ok=True witnessed=1 notMet=1 build_met=1 errors=[]
```

## Verdict table

| # | attack | shipped selftest | detect.py | committed fixtures | scope e2e | verdict |
|---|---|---|---|---|---|---|
| m1 | exit gate removed | **KILLED** (exit 1) | killed (2) | not refuted¹ | killed (6) | **KILLED** |
| m2 | note gate removed | **KILLED** | killed (1) | refuted | killed (6) | **KILLED** |
| m3 | freshness window removed | **KILLED** | killed (2) | **not refuted** | killed (6) | **KILLED** (fixture gap) |
| m4 | counter-sha binding removed | **KILLED** | killed (1) | refuted | killed (6) | **KILLED** |
| m5 | invalid rows counted as not-met | **KILLED** | killed (1) | refuted (notMet=1) | killed (20) | **KILLED** |
| m6 | build-count pin removed | **KILLED** | killed (2) | not reachable² | not reachable² | **KILLED** (reachability finding) |
| m7 | seed gate removed (extra) | KILLED | killed (1) | not refuted | killed (6) | **KILLED** |
| m8 | control wiring ignores validity | **SURVIVED** | survived | refuted | killed (20) | **SURVIVED the selftest** |
| m9 | window neutered at call site | **SURVIVED** | survived | **not refuted** | killed (4) | **SURVIVED the selftest** |
| m10 | build wiring ignores validity | **SURVIVED** | survived | refuted | killed (10) | **SURVIVED the selftest** |
| m11 | `MTIME_EPS_NS` widened | **SURVIVED** | survived | **not refuted** | killed (6) | **SURVIVED the selftest** |

¹ m1's fixture run still refuses, but with a *substituted* class (`ctl1:stale_receipt` instead of
`ctl1:counter_error`) — the sha gate catches what the exit gate no longer does. Refusal survives;
the named rejection does not. The selftest is what pins the class name.
² see reachability finding below.

## Findings to report loudly

1. **The v2 selftest cannot see the gate being unwired (m8–m11 all exit 0).** It exercises
   `receipt_validity()` and `expectation_ok()` as a library; nothing in it drives `score()` /
   `score_build()`, so a driver that computes validity and then discards it passes. m8/m10 are the
   exact C1 defect restored (invalid receipt gets witness and not-met credit) with a green
   selftest. C2(a)/C1 "selftest kills the mutant" evidence must not be read as evidence that the
   gate is *wired*. Needs an end-to-end able-to-fail probe (`fixture_detect.py`/`e2e2.py` shapes),
   not more unit assertions.
2. **The committed fixture corpus cannot see the freshness window at all (m3, m9, m11 =
   `refutations=0`).** `fixtures/stale-planted/fake_counter.py` SIGKILLs itself, so the recorded
   exit is not 0/1 and `counter_error` fires *before* the mtime check; the three committed classes
   also reuse the frozen counter's `counterSha256`, so the sha gate fires before the window too.
   Verbatim: pristine and m3/m9/m11 emit byte-identical stale-planted lines
   (`errors=['ctl1:counter_error', 'build#1:counter_error', ...]`, `counter=18e3bcfda602`).
   Therefore C1 leg (iii) has **no able-to-fail fixture evidence** in wave 1 — only the in-memory
   selftest. A fixture whose receipt is exit 0, sha-correct, seeded, note-free, but
   back-dated is required to make (iii) falsifiable at the driver level (my `e2e2.py` `stale` class
   is exactly that shape: pristine refuses, m3/m9/m11 accept and certify `ok=True`).
3. **The build-count pin (m6) is unreachable from the CLI.** `build = list(pool.map(score_build,
   range(a.build_runs)))` always yields exactly `build_runs` rows, so `len(build) != build_runs`
   cannot occur; `build_met`'s `count_ok` is likewise always true. The pin is real and correct but
   its only exerciser is a direct function call — the selftest and `detect.py` do exercise it
   (both kill m6). Anyone claiming end-to-end evidence for the pin is wrong today.
4. **No mutant is an equivalent mutant**: the honest path is byte-identically green (exit 0,
   1/1 witnessed, 3/3 build_met) under all eleven, so every survival above is a detector gap, not
   a semantic no-op.

## Files written

Lane (my named write paths only):
- `.ufo/waves/round-45/mutants/v2/m1.py` … `m11.py` (11 single-point mutants of `c45_audit.py@5a342e29`)
- `.ufo/waves/round-45/w1/MutDriverV2Spec.md` (this report)

Scratch `/fast/scratch/hyaku/kake-r45/MutDriverV2Spec/`: `pristine_v2.py` (byte snapshot,
sha `5a342e29…`), `make_mutants.py` (anchor-exact mutation generator), `stub_counter.py`
(per-scope defect stub), `detect.py`, `e2e2.py`, `e2e.py` (superseded first-pass detector),
`fixture_detect.py`, `gen.txt`/`gen2.txt`, `e2e2-pristine.txt`, `e2e2-m1..11.txt`,
`fix-pristine.txt`, `fix-m1..11.txt`, `e2e2-work/`, `e2e-work/`, `fix-work/`.

Nothing outside those paths was written. **`c45_audit.py` was never edited by me** (mutants are
copies); final lane hash equals the snapshot I mutated: `5a342e29c7e872d992cfedc26de849c010d197bb82162e007a61a55d915c7051`.
The frozen round-44 files are untouched (`c44_audit.py` still
`8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75`). No git/jj command was run.
No tool was installed (all detectors are stdlib CPython 3.14.8), so there is no install record.

## Blockers / dependencies (recorded, not blocking)

- `c45_audit.py` is owned by seat `ExecDriverV2` and moved mid-flight; if it moves again, the
  verdicts above are pinned to `5a342e29…` and `make_mutants.py` will fail loudly (`ANCHOR-FAIL`)
  rather than produce a stale mutant — re-run it after any further change.
- `fixtures/*` are owned by `ExecInvalidFixtures`; finding 2 is a fixture-coverage request against
  that corpus, not an edit I made.

## Checks the L1 should run (not run here)

- `python3 -B .ufo/waves/round-45/c45_audit.py --selftest` → exit 0 (lane bytes intact).
- `python3 -B .ufo/waves/round-45/c45_matrix.py --stage after` → the matrix must still reproduce
  `invalid_accepted=0 rejections_named=3`; findings 1–3 do not touch that count, they bound what
  it proves.
- If wave 2 wants C1 leg (iii) falsifiable from committed bytes, add an exit-0/sha-correct/
  back-dated fixture class and one end-to-end probe that runs the driver (not the function).
