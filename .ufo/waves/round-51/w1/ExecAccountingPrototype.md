# L3 time-accounting prototype — fixture acceptance and off-by-one rejection

Seat: `L1Kake51.ExecAccountingPrototype-2` · axis: operability · claim under test: **C1 / condition L3**.
Instrument under test: `.ufo/waves/round-51/c51_wave_ledger.py`, function `check_l3`.
Method: the shipped module was **imported** with `importlib.util.spec_from_file_location` (its
`__main__` guard keeps the import side-effect free) and `check_l3` was called directly against a
`/tmp` git fixture. The shipped CLI was additionally run end-to-end on the clean fixture to confirm
the module-level result survives `main()`. Nothing in the lane was mutated; the fixture lives only
under `/tmp/c51fix/`.

## 1. Fixture — exact numbers

Two commits of a fresh `/tmp` git repo (`main`), fixture base `b0e7624a94`, clean fixture commit
`f4492f1b92`. The five L3-bound paths are the only files written:

| Path (relative to fixture root) | Content |
|---|---|
| `.ufo/waves/round-51/settlement.json` | see below |
| `.ufo/waves/round-51/wave-timing.json` | `{"startedAt":"2026-10-25T03:29:00Z","settledAt":"2026-10-25T03:49:00Z"}` |
| `.ufo/waves/round-51/round-time-accounting.json` | `{"wall_clock_seconds":1200,"aggregate_seat_seconds":3000,"dead_seat_seconds":618}` |
| `.ufo/waves/round-51/wave-grant.txt` | `wave-grant round=51 granted lane=kake seats=9` |
| `LOG.md` | `Round 51 wave 1 settled. Wave wall clock 1200 s; aggregate seat seconds 3000; dead-seat seconds 618.` |

`settlement.json`:

- `timeout_seconds`: **420**
- `settled`: 6 seats `seat-a`..`seat-f`, each `seconds: 397` → Σ = **2382**
- `dead`: 3 seats — `dead-timeout` `420 s` `reason: "timeout-420"`; `dead-exit3` `137 s`
  `reason: "exit-3"`; `dead-exit1` `61 s` `reason: "exit-1"` → Σ = **618**

Derived figures, all integers, all known by construction:

- **wall clock** = `settledAt − startedAt` = `03:49:00 − 03:29:00` = **1200 s** exactly
- **aggregate seat seconds** = 2382 + 618 = **3000**
- **dead-seat seconds** = **618**
- **timeout** = **420**

## 2. The clean fixture is accepted

```
check_l3(REPO, "f4492f1b92") -> (True, [], {"aggregate_seat_seconds": 3000,
    "dead_seat_seconds": 618, "timeout_seconds": 420, "wall_clock_seconds": 1200})
```

Empty note list; re-derived wall clock is the integer 1200, and the accounting artifact's 1200
matches. The same fixture through the shipped entry point:

```
python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root /tmp/c51fix/repo --revision f4492f1b92 --json
-> L1 false ("dispatch payload absent"), L2 false ("route map absent"),
   L3 true  (facts: 3000 / 618 / 1200 / 420), ledger_checks_passed=1, met=false, exit 1
```

L3 passing while L1 and L2 fail on the same revision is direct evidence that L3 reads only its own
five paths — the separability the contract asserts for C1 is visible at check granularity.

## 3. Off by one — it rejects

Same fixture, `settledAt` moved by one second, accounting artifact and LOG left at 1200:

| Mutant | `settledAt` | re-derived wall | accepted | notes emitted |
|---|---|---|---|---|
| `offby1_plus` (`8c8018cb25`) | `03:49:01Z` | **1201** | **False** | `time accounting wall clock 1200 != re-derived 1201`; `LOG.md does not name the re-derived wall-clock figure 1201` |
| `offby1_minus` (`f255ee25ba`) | `03:48:59Z` | **1199** | **False** | `time accounting wall clock 1200 != re-derived 1199`; `LOG.md does not name the re-derived wall-clock figure 1199` |

Both directions reject, and each rejection is double-signed: the artifact comparison and the LOG
naming check fire independently. A one-second shift in either direction is caught.

## 4. Attack: what L3 does not pin down

Four mutants are **accepted** by `check_l3`. Each is a real hole in the condition as worded, not a
fixture artefact — I re-ran each through the imported function and the notes list was empty.

| Accepted mutant | rev | what it shows |
|---|---|---|
| `offby1_fully_consistent` — timing `03:49:01`, accounting `1201`, LOG `1201 s` | `a7eee97f28` | **The sharpest result.** L3 has no absolute anchor: an off-by-one wall clock is rejected only while it is *inconsistent*. Shift timing, artifact and LOG together and a wrong clock passes. L3 constrains mutual agreement among three committed bytes, not the elapsed time of the wave. |
| `absurd_but_consistent` — 6 settled seats at `999999 s` each, accounting aggregate `6000612`, dead `618`, wall `1200` | `b9e323fa84` | `aggregate`/`dead` are re-**summed** from the same `settlement.json` the artifact is compared against. Nothing cross-checks a seat's seconds against the wall clock, so any self-consistent absurd triple passes. "Re-derivable" here means re-summed, not independently measured. |
| `zero_length` — `startedAt == settledAt`, accounting wall `0`, LOG names no figure at all | `3f18e1df27` | The LOG condition is guarded by `if wall > 0`; a zero-length wave skips it entirely, and `0 == 0` satisfies the artifact comparison. Accepted with a LOG that names no wall-clock figure. |
| `backwards_timing` — `settledAt` *before* `startedAt`, wall `-600`, accounting `-600`, LOG names no figure | `979689fe99` | Same guard: negative wall also skips the LOG condition, and a negative wall clock is accepted as a value. No ordering check on the timestamp pair. |
| `log_superstring` — timing/artifact at 1200 but LOG says only `11200 s` | `12d93e59a3` | The LOG check is `str(wall) not in log_text`: a substring test, so `1200` is satisfied by `11200`, `31200`, or a page number. Not a token or field match. |

The complement of §3, for symmetry: `offby1_log_lags` (`9e0fed7fb6`) — timing and accounting both
`1201`, LOG still `1200` — **rejects** with `LOG.md does not name the re-derived wall-clock figure
1201`. So the LOG check is live, and it is the *only* thing that catches a fully-consistent bad
clock's missing prose; it does not catch a wrong clock that is also named.

## 5. Dead-seat reason rule — behaviour confirmed at the boundary

| Mutant | `dead` seat | accepted | notes |
|---|---|---|---|
| `dead_timeout_mismatch` (`390119c2e0`) | `timeout-420` seat at `419 s` | **False** | `dead seat dead-timeout records reason timeout-420 but 419s != 420s` (+ the two sum notes, since the 1 s flowed into the aggregate) |
| `exit_at_timeout` (`061d306d51`) | `exit-3` seat at `420 s` == timeout | **True** | none — `==` is allowed; rule is `secs > timeout` |
| `exit_over_timeout` (`8d71167766`) | `exit-3` seat at `421 s` | **False** | `dead seat dead-exit3 ran longer than its timeout` |

`timeout-*` is an equality rule, `exit-*` a `≤` rule. Both behave as written. The 1-second `exit-*`
tolerance is defensible (a timeout fires, then the exit code arrives), but it is not stated in the
contract's L3 wording and a reader cannot derive it from the predicate.

## 6. Arithmetic-level checks

- `aggregate_offby1` (`31da41ca01`) — artifact `2999` vs derived `3000` → rejected:
  `time accounting aggregate 2999 != 3000`.
- `dead_offby1` (`a54b929214`) — artifact `619` vs derived `618` → rejected:
  `time accounting dead-seat seconds 619 != 618`.
- `grant_missing` (`29fcd0178f`) — empty grant file → rejected:
  `wave grant file does not carry a kake grant line`.

Both scalar comparisons are exact-integer and catch a one-unit error. The guard line
`granted lane=kake` is a substring test, the same shape as the LOG check.

## 7. Real lane, read-only

To ground the fixture in the shipped instrument's actual state, `check_l3` was called against the
lane itself (read-only `git show`; no index, worktree, `jj`, or commit touched):

| revision | L3 | note |
|---|---|---|
| `007d66e4e8` (base) | false, `facts={}` | `settlement receipt absent at the measured revision` |
| `9d13768c4f` (lane tip at dispatch) | false, `facts={}` | `settlement receipt absent at the measured revision` |

This matches the dispatch measurement of `C1 ledger 0/3 met=False`: the wave evidence does not exist
at either revision, so L3 fails at its first bound path and cannot be scored yet. It says nothing
about whether L3 will pass once the L1 lands the settlement — that is the open question, and §4 is
what to look at when it does.

## 8. Verdict for the L1

- **L3 is a real instrument.** It reads exactly five committed paths, re-derives the wall clock from
  the timing pair with integer truncation, compares against the accounting artifact, and rejects a
  one-second shift in either direction, a one-unit error in either scalar sum, a mismatched
  timeout-reason duration, an over-timeout exit seat, and a missing grant line. The clean fixture is
  accepted with all figures as constructed.
- **L3 is a consistency check, not a measurement.** Every input it re-derives from is itself a
  committed self-report. Three items in §4 (`offby1_fully_consistent`, `absurd_but_consistent`)
  pass with no note. So the correct claim is "the three committed figures agree with each other",
  not "the wave's elapsed time is 1200 s". The contract wording "re-derivable from the committed
  settlement and wave-timing bytes" is accurate and deliberately narrow; it should not be read as
  stronger.
- **Two guard holes** are worth a one-line fix in the L1's own bytes if operability is the axis:
  the `wall > 0` guard lets a zero-length or backwards timing skip the LOG condition entirely, and
  the `str(wall) in log_text` test is a substring match that `11200` satisfies. Neither is
  exploitable by an honest wave, and neither blocks C1 if the settlement is committed with sane
  figures.

## Retained evidence

- Fixture repo: `/tmp/c51fix/repo`, base `b0e7624a94`; commits `f4492f1b92` (clean, accepted),
  `8c8018cb25`, `f255ee25ba`, `3f18e1df27`, `12d93e59a3`, `390119c2e0`, `31da41ca01`, `a54b929214`,
  `29fcd0178f`, `b9e323fa84`, `979689fe99`, `a7eee97f28`, `9e0fed7fb6`, `061d306d51`, `8d71167766`.
- Module import root: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-51/c51_wave_ledger.py`,
  bound paths `SETTLEMENT`, `TIMING`, `ACCOUNTING`, `GRANT`, `LOG` as listed in §1.
- CLI transcript of the clean fixture: §2.

## Risks and blockers

- None blocking. The fixture is synthetic: it proves what `check_l3` accepts and rejects, not that
  the round's real settlement will agree with itself. If the L1 commits a settlement whose
  `seconds` fields are rounded per seat, aggregate drift is the likely first failure.
- No tools were installed or upgraded; no package manager was invoked. No file outside this report
  was written in the lane. `considerthese/`, the round-46 residual and round-48 validate copies,
  and the external read-only roots were not touched.
