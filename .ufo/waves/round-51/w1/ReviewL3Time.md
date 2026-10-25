# ReviewL3Time — adversarial read of `check_l3` (C1 / L3, time accounting)

Scope: `.ufo/waves/round-51/c51_wave_ledger.py:200-257` (committed at `19a99bd`, still the
lane tip's ledger), with `build_wave_evidence.py` read as the producer of the artifacts the
check consumes. Every probe below was run against a byte-identical copy of the committed
counter in `/tmp/l3probe` (own git repo, synthetic wave bytes, commit per mutant); no lane
file was touched except this report.

Real-state run (read-only, no fixtures):

```
$ python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root . --revision 9d13768c4fdd0e9a2688d2ecf1616b539cf57658
C1 ledger 0/3 met=False  (met: ledger_checks_passed == 3 of 3)
  L1 FAIL
    - settlement receipt absent at the measured revision
  L2 FAIL
    - route map absent at the measured revision
  L3 FAIL
    - settlement receipt absent at the measured revision
rc=1
```

At the frozen tip `git cat-file -e` answers **absent** for `settlement.json`,
`wave-timing.json`, `round-time-accounting.json`, `wave-grant.txt`, `w51-taskcall.json`,
`route-map.json`; `ls-tree` counts 0 files under `w1/` and 0 under `route-probes/`
(all exist only untracked in the worktree). The real artifacts therefore cannot be
exercised yet, which is why every L3 finding below is demonstrated on a synthetic fixture
that the check accepts.

---

## 1. Is the wall clock re-derived from the timing pair, or copied from the accounting artifact?

**Re-derived.** `c51_wave_ledger.py:218-220`:

```
started = parse_ts(str(timing.get("startedAt", "")))
settled = parse_ts(str(timing.get("settledAt", "")))
wall = int((settled - started).total_seconds()) if started and settled else None
```

`parse_ts` (`:86-95`) normalizes `Z` to `+00:00`, treats a naive stamp as UTC, and returns
`None` on a parse failure. The accounting artifact is read only afterwards (`:239-241`) and
`wall` is used as the *left* operand of the comparison (`:240`), so the accounting figure can
never become the derived value. Probe 09 (accounting consistent with the pair, but
`wave-timing.json.wallClockSeconds = 999999` while the pair says 600) still passes L3,
confirming the paired field is not the source.

Two qualifications that matter for "re-derived":

- **The pair is the only source, and nothing corroborates it.** The settlement carries no
  per-seat start/finish stamps (`build_wave_evidence.py:55-66`: name, role, model, exit,
  seconds, report only), and L3 never compares the pair to `wave-start-utc.txt` /
  `settled-utc.txt` — the builder's declared inputs (`build_wave_evidence.py:14-15`), which
  are themselves uncommitted at the tip. Two self-declared timestamps in one JSON are the
  whole derivation.
- **`wallClockSeconds` (`build_wave_evidence.py:97`) is written and never read.** A grep of
  `c51_wave_ledger.py` for `wallClockSeconds` returns nothing, so the timing artifact
  carries a fourth figure that may silently disagree with the pair it ships beside (probe 09
  passes with a 999999-vs-600 disagreement).

Monotonicity is unguarded: `:220` computes a signed difference, so `settledAt < startedAt`
yields a negative wall, and `:242` gates the LOG check on `wall > 0`, so a negative wall skips
the LOG condition outright.

| Probe (fixture) | Derived wall | L3 | Note printed |
|---|---|---|---|
| 05 `settledAt` 06:10Z, `startedAt` 06:00Z, LOG names nothing | **-600** | **pass** | none |
| 06 `startedAt == settledAt`, LOG names nothing | **0** | **pass** | none |
| 09 timing pair 600, `wallClockSeconds` 999999 | 600 | **pass** | none |

A wave that reports -600 s or 0 s passes the time-accounting check with no LOG figure and no
note.

## 2. Is every figure the accounting carries cross-checked?

**No — 3 of 10.** `round-time-accounting.json` as the builder writes it
(`build_wave_evidence.py:107-117`) carries: `schema`, `round`, `wave`,
`wall_clock_seconds`, `aggregate_seat_seconds`, `dead_seat_seconds`, `settled_seats`,
`dead_seats`, `seatDefinition`, `spawn`. `check_l3` compares only `wall_clock_seconds`
(`:239-241`), `aggregate_seat_seconds` (`:244-247`) and `dead_seat_seconds` (`:248-251`).

Unchecked and therefore free: `round`, `wave`, `settled_seats`, `dead_seats`, `spawn`,
`schema`, `seatDefinition`.

| Probe 08 | Value in accounting | Value implied by settlement | L3 |
|---|---|---|---|
| `round` | 7 | 51 | **pass** |
| `wave` | `"r99-w9"` | `"r51-w1"` | **pass** |
| `settled_seats` | 99 | 2 | **pass** |
| `dead_seats` | 42 | 1 | **pass** |
| `spawn` | 999 | 3 | **pass** |
| `seatDefinition` | `"garbage"` | — | **pass** |

A stale or foreign accounting artifact passes as long as its three seconds fields match.

More structurally, the three checked fields are not independent observations. The builder
computes them from the same two lists the checker re-sums:

```
builder :104  aggregate   = sum(int(e["seconds"]) for e in settled_seats + dead_seats)
ledger  :215  aggregate   = sum(int(e.get("seconds", 0)) for e in seats)
```

with `seats = settlement.get("settled", []) + settlement.get("dead", [])` (`:214`). Both
encodings come from one derivation, so L3's accounting comparisons verify that a copy equals
its source, not that the source is true. Nothing in L3 — or in L1/L2 — binds a seat's
`seconds` to a committed per-seat timestamp; the builder derives them from filesystem mtimes
(`build_wave_evidence.py:53-54`), which are not committed bytes and are not reproducible from
the revision.

Adjacent: a seat present in both `settled` and `dead` is summed twice, unremarked (probe 10:
`C` in both lists → aggregate 1500 for a 600 s wave, L3 pass). L1's
`settled_count + dead_count != len(seats)` test (`:128`) cannot catch it, because the builder
sets both counts from the list lengths.

## 3. Can a dead seat record an impossible duration?

**Yes, on every route the producer can emit.** `:227-235` is the whole dead-seat rule:

```
reason = str(seat.get("reason", ""))
secs   = int(seat.get("seconds", 0))
if reason.startswith("timeout-") and secs != timeout:  note
if reason.startswith("exit-")    and secs >  timeout:  note
```

- **The builder's own reason is never validated.** `build_wave_evidence.py:61-66` emits
  `"reason": "no-report"` for every dead seat, with `"seconds": wall`. Neither prefix test
  fires, so no duration check applies to any dead row the committed producer can write.
  Probe 01b: `no-report` seat charged **999999 s inside a 600 s wave**, accounting mirroring
  it → **L3 pass**, no note.
- **No non-negativity.** Probe 02: dead seat at **-500 s** (aggregate -200) → **pass**.
- **A missing `seconds` key counts as 0 and passes.** Probe 03 (`:229` default `0`) → **pass**.
- **`timeout-` is checked only against a self-declared timeout.** `:217` reads
  `settlement.timeout_seconds`; the settlement is the artifact under test. Probe 04: a
  `timeout-3600` seat charged 3600 s inside a 600 s wave → **pass**. Probe 12: declare
  `timeout_seconds: 999999` and charge **999999 s** → **pass**. Probe 14: omit the field
  entirely (`timeout` defaults to 0) and a timeout death at **0 s** is the passing value →
  **pass**.
- **`reason: null` bypasses both prefixes** (`str(None) == "None"`). Probe 15: 999999 s →
  **pass**.
- **No upper bound against the wave, dead or settled.** Probe 13: a *settled* seat charged
  5000 s inside a 600 s wave → **pass**. Probe 16: 48 dead seats each charged the full 600 s
  wall clock (aggregate 28800 s) → **pass**. That is not an exotic fixture: it is exactly
  what `build_wave_evidence.py:64` writes per dead seat, so the builder's own semantics
  produce an aggregate up to `spawn × wall` with nothing to flag it.
- **Malformed durations crash instead of failing cleanly.** Probe 11 (`"seconds": "abc"`)
  raises `ValueError: invalid literal for int()` at `:215` — no notes, no JSON report, exit 1
  (Python's uncaught-exception status). The docstring advertises exit **2** for "the evidence
  cannot be evaluated" (`:31-32`), but `main` (`:262-290`) only ever returns 0 or 1, so a
  crash is indistinguishable by exit code from an honest `met=False`.

## 4. "LOG.md names the wall-clock figure"

Implemented as `if wall > 0 and str(wall) not in log_text` (`:242`) over the **repository-root**
`LOG.md` (`LOG = "LOG.md"`, `:53`), not the wave's. `LOG.md` at the tip is 169,386 bytes /
2,083 lines of prose, dates and sha fragments, so the test asks whether a decimal string
occurs anywhere in 169 KB, not whether the figure is named.

| Probe | LOG.md content | L3 |
|---|---|---|
| 07a | no wall figure, only `turn 1600 of the frontier` | **pass** (600 ⊂ 1600) |
| 07c | no wall figure, only `commit deadbeef600f` | **pass** (600 ⊂ hash) |
| 17 | wall 2026, only `- 2026-10-25 - round 51 opened` | **pass** (year) |
| 07b | `wall clock: 10 minutes` — the true figure, stated in minutes | **fail** |

Against that real log, 603 of the 6,601 integer wall values in a plausible 48-seat range
600..7200 s already satisfy the test today (9.1%); only 164 of them appear as a whole numeral
— the rest are substring hits inside other numbers (`602`, `605`, `609`, `610`, …). The check
therefore fails both ways: it accepts digits that name nothing, and rejects a correct figure
written in any unit but seconds.

## Findings by severity

**High**

1. **H1 — the producer's only dead-seat reason is exempt from duration checking.** `:227-235`
   validates `timeout-`/`exit-`; `build_wave_evidence.py:65` emits only `no-report`. L3's
   stated condition "every dead seat's duration matches its recorded reason" is unimplemented
   for every artifact the committed builder can produce. Evidence: probe 01b (999999 s in a
   600 s wave, pass).
2. **H2 — no duration is bounded by the wave.** Negative, absent (`:229` default), and
   greater-than-wall values all pass for dead seats; settled seats are unbounded too
   (`:214-216` has no per-seat or aggregate ceiling). Evidence: probes 02, 03, 04, 12, 13,
   16.
3. **H3 — the LOG check is a raw substring over a 169 KB repo-wide log.** 9.1% of plausible
   wall values already pass accidentally; a correct figure in minutes fails. Evidence: probes
   07a, 07b, 07c, 17 and the numeral census of `LOG.md@9d13768`.

**Medium**

4. **M1 — 3 of 10 accounting figures are cross-checked**, and those three are re-derivations
   of the same settlement lists the builder serialised (`:215-216` vs
   `build_wave_evidence.py:104-105`), so they test serialisation agreement, not measurement.
   A foreign accounting (`round=7`, `wave=r99-w9`, `spawn=999`) passes. Evidence: probe 08.
5. **M2 — the timing pair has no monotonicity guard**, and `:242`'s `wall > 0` gate silently
   disables the LOG condition for negative and zero walls. Evidence: probes 05, 06.
6. **M3 — `wave-timing.json.wallClockSeconds` is written at
   `build_wave_evidence.py:97` and never read**, so the timing artifact can ship a wall figure
   that contradicts its own pair without L3 noticing. Evidence: probe 09.
7. **M4 — malformed evidence crashes** (`:215`, `:229`), producing exit 1 with a traceback and
   no notes, while the docstring's exit 2 for "cannot be evaluated" (`:31-32`) is never
   returned by `main`. Evidence: probe 11.
8. **M5 — a seat in both `settled` and `dead` is double-counted** (`:214`) with no
   disjointness note; L1's count test (`:128`) is tautological against builder output.
   Evidence: probe 10.

**Low**

9. **L1 — absent and corrupt are conflated.** `show_json` (`:69-77`) returns `None` on
   `JSONDecodeError`, and `:206-213` then reports "artifact absent at the measured revision"
   for bytes that exist but do not parse. Evidence: probe 18.
10. **L2 — a non-object artifact crashes** (`accounting = []` → `AttributeError: 'list'
    object has no attribute 'get'` at `:239`). Evidence: probe 19.
11. **L3 — `timeout_seconds` defaulting to 0 (`:217`)** turns an omitted field into a
    requirement that a timeout death record 0 s, so the omitted-field state makes an
    impossible duration the passing one. Evidence: probe 14.
12. **L4 — timestamp semantics diverge between tools for naive stamps.**
    `build_wave_evidence.py:35-37` (`stamp`) interprets a naive value as host-local via
    `astimezone(timezone.utc)`; `c51_wave_ledger.py:86-95` (`parse_ts`) treats a naive value
    as UTC. Hand-written evidence without an offset means the producer and the checker disagree
    about the same bytes. The builder itself always emits `+00:00`, so this only bites
    hand-authored artifacts.

## Residual risk and verification gaps

- **No real-state verification of L3 was possible.** At `9d13768` four of L3's five inputs
  (settlement, timing, accounting, grant) plus all of L1's and L2's inputs are uncommitted;
  only the root `LOG.md` exists, so the counter's only true statement about the real wave is
  `0/3 met=False`. The evidence for every finding above is synthetic
  and self-built; none of it depends on the yet-to-be-written settlement.
- **`build_wave_evidence.py` cannot run against the frozen bytes:** `settled-utc.txt` (its
  second measured input, `:15`) is absent from `9d13768`. The C1 "after" state therefore
  requires a new input file, not just a re-run at the same tip.
- **The core L3 claim is narrower than the contract reads.** The contract's L3 sentence
  ("re-derivable from the committed settlement and wave-timing bytes") is literally true —
  the bytes suffice — but the settlement's `seconds` are themselves mtime-derived and not
  committed, so the re-derivation proves internal consistency of one operator-authored JSON,
  not the wave's elapsed time. A reader who takes L3 as a wall-clock certificate is
  over-reading it; an operator who wants one needs per-seat committed timestamps and a
  `seconds >= 0` / `seconds <= wall` bound, neither of which exists in the frozen counter.
- **Not verified:** the LOG.md that will exist at the measured commit (the check reads the
  root log at that revision, which does not exist yet for this wave); the real
  `timeout_seconds` value the builder will emit (env `KAKE_R51_TIMEOUT`, default 3600); and
  whether the wave will contain any dead seat at all.
- No tools were installed or upgraded for this review.
