# C1 wave-ledger counter — mutant exercise (ExecLedgerMutants)

Seat: `L1Kake51.ExecLedgerMutants-2`. Scope: exercise `c51_wave_ledger.py` (C1, operability) with
named mutants and report what the counter admits vs. rejects. Read-only in the lane; all scratch
under `/tmp/r51-mut-l1/`. Only lane file written: this report.

## Axes

1. **Admission** — does a well-formed ledger reach `3/3` (exit 0)?
2. **Rejection discrimination** — does a single named defect always produce exit 1 *and* a note that
   names the defect property (not just "something failed")?
3. **Locality** — does the mutation cost only the check that owns the invariant, leaving the other
   two checks `pass` (i.e. the three checks are not accidentally coupled)?
4. **Vacuity** — can `3/3` be earned by degenerate evidence (zero seats, zero reports, phantom seats)?

## Evidence state at the measured revision (measured, not assumed)

`git cat-file -e 9d13768c…:.ufo/waves/round-51/<path>` at the lane tip:

| path | state |
|---|---|
| `settlement.json` | ABSENT |
| `wave-timing.json` | ABSENT |
| `round-time-accounting.json` | ABSENT |
| `route-map.json` | UNCOMMITTED (on disk, not in the revision) |
| `w51-taskcall.json` | UNCOMMITTED |
| `wave-grant.txt` | UNCOMMITTED |
| `route-probes/commandcode_deepseek_deepseek-v4.1-flash.json` | UNCOMMITTED |
| `w1/*.md` seat reports | 0 committed |

Pristine counter against the lane tip, verbatim:

```
$ python3 -B .ufo/waves/round-51/c51_wave_ledger.py \
    --root /home/vgpnk/Projects/shokunin/kake-shokunin \
    --revision 9d13768c4fdd0e9a2688d2ecf1616b539cf57658
C1 ledger 0/3 met=False  (met: ledger_checks_passed == 3 of 3)
  L1 FAIL
    - settlement receipt absent at the measured revision
  L2 FAIL
    - route map absent at the measured revision
  L3 FAIL
    - settlement receipt absent at the measured revision
  revision: 9d13768c4fdd0e9a2688d2ecf1616b539cf57658
exit=1
```

This is correct and honest behaviour for a committed-bytes reader: the whole wave-51 wave evidence
is worktree-only at the lane tip, so the counter reports `0/3`. It also means **the real evidence has
never been scored** by this counter — the five mutants below therefore run against a fixture I built
under `/tmp`, not against the wave's own bytes. That is a limitation of the measurement, not a pass.

## Fixture (constructed; stated as constructed)

Wave evidence absent at the revision, so I built the minimal passing fixture the counter's own code
requires, at `/tmp/r51-mut-l1/fixture` (a scratch git repo; `--revision` = its commit):

- `.ufo/waves/round-51/settlement.json` — `spawn:1`, `timeout_seconds:120`, `settled_count:1`,
  `dead_count:0`, `reports_written:1`, `settled:[{name:"seat-alpha",seconds:55,report:true}]`, `dead:[]`
- `.ufo/waves/round-51/w51-taskcall.json` — `counts.spawn:1`, one task (payload seats = 1)
- `.ufo/waves/round-51/route-map.json` — role `scout` with `kimiModel:"route/alpha"` and a `probe`
  string naming both `route/alpha` and the failing `route/omega`
- `.ufo/waves/round-51/route-probes/alpha.json` — `alias:"route/alpha"`, integer `httpStatus:200`, `ok:true`
- `.ufo/waves/round-51/route-probes/omega.json` — `alias:"route/omega"`, `httpStatus:403`, `ok:false`, body excerpt
- `.ufo/waves/round-51/wave-timing.json` — `2026-10-25T03:00:00Z` → `2026-10-25T03:01:00Z` (wall 60)
- `.ufo/waves/round-51/round-time-accounting.json` — `wall_clock_seconds:60`, `aggregate_seat_seconds:55`, `dead_seat_seconds:0`
- `.ufo/waves/round-51/wave-grant.txt` — `granted lane=kake …`
- `.ufo/waves/round-51/w1/seat-alpha.md`, `LOG.md` naming `60`

Baseline, verbatim: `C1 ledger 3/3 met=True … exit=0`. Each mutant is a fresh copy of that repo,
one defect applied, committed, then the pristine counter is run with `--revision <mutated commit>`.
Counter under test: `/tmp/r51-mut-l1/c51_wave_ledger.py`, sha256
`714c1017886dcace5e06123853e442dd5363b9cf35fb81e20d2f2b9ef60eba7c`, 12364 bytes, Python 3.14.8.

## Required mutants — all five rejected

| # | mutation | exit | other checks | notes printed (verbatim) |
|---|---|---|---|---|
| a | settlement `reports_written` 1 → 2 (inflated by one) | **1** | L2 pass, L3 pass | `settlement reports_written 2 != committed report files 1` |
| b | add settled seat `seat-beta` with `report:true`, no file (counts kept consistent: `settled_count:2`, `reports_written:1`, `seconds:0`) | **1** | L2 pass, L3 pass | `seats marked with a report but no committed file: ['seat-beta']` |
| c | used route's receipt `httpStatus` `200` → `"200"` (string) | **1** | L1 pass, L3 pass | `probe receipt for route/alpha carries no integer httpStatus` (emitted twice — once from the used-route loop, once from the receipts loop) |
| d | used route `route/alpha` receipt `ok:true` → `false` (excerpt kept) | **1** | L1 pass, L3 pass | `route route/alpha was used but its receipt is not ok`; `failing route route/alpha was used by a role`; `failing route route/alpha is not recorded as a deviation in the route map` |
| e | accounting `wall_clock_seconds` 60 → 61 (off by one from the timing pair) | **1** | L1 pass, L2 pass | `time accounting wall clock 61 != re-derived 60` |

All five: exit 1, `2/3`, the owning check alone flips to `FAIL`, and the note names the exact
quantity and both of its values (expected/actual), not a generic "mismatch". Axis 2 and axis 3 hold
for the required set. Mutant commit ids: a `6156f0e4…`, b `a6eda300…`, c `eeb4cbaf…`,
d `5e001d6a…`, e `54e13ec8…`.

## Extra mutants — also rejected (cheap, same harness)

| # | mutation | exit | notes |
|---|---|---|---|
| f | committed report file for a seat the settlement does not list (`w1/seat-ghost.md`) | **1** | `settlement reports_written 1 != committed report files 2`; `committed report files for unknown seats: ['seat-ghost']` |
| g | failing `route/omega` receipt dropped from every role's `probe` string | **1** | `failing route route/omega is not recorded as a deviation in the route map` |
| h | `LOG.md` stops naming the wall-clock figure | **1** | `LOG.md does not name the re-derived wall-clock figure 60` |
| i | settlement `spawn` 1 → 2 | **1** | `settlement spawn 2 != payload seats 1` |

## Gap probes — mutations the counter ADMITS at 3/3 (exit 0)

These are not in the required five; they are the axis-4 result and they are defects in the counter,
not in the fixture.

| # | evidence planted | exit | verdict |
|---|---|---|---|
| j | **phantom seat** — `settled` gains `{name:"seat-phantom",seconds:0,report:false}`, `settled_count:2`, `spawn` stays 1, `reports_written` stays 1 | **0** | `3/3 met=True` — admitted |
| k | **zero reports** — the single seat set `report:false`, `reports_written:0`, its report file deleted | **0** | `3/3 met=True` — admitted |
| l | **empty wave** — `spawn:0`, `settled:[]`, `dead:[]`, payload `tasks:[]`/`counts.spawn:0`, accounting all zero, no report files | **0** | `3/3 met=True` — admitted |

Mechanism, read from the source (`check_l1`):

- `spawn` is compared only to `len(tasks)` from the dispatch payload; `len(seats)` is compared only
  to `settled_count + dead_count`. **Nothing ties `settlement.spawn` to the settlement's own seat
  list**, so a settlement can list more (j) or fewer seats than it claims to have spawned and stay
  silent — as long as the extra seat does not claim a report.
- `reported == committed` is an equality between two possibly-empty sets, and `reports_written` is
  compared to the file count without a floor. A wave that writes **no** seat report at all (k) and
  a wave with **no seats** at all (l) both satisfy L1/L3 exactly. There is no non-vacuity guard:
  no `reports_written > 0`, no `len(seats) > 0`, no `spawn > 0`.

Operability consequence: `met: ledger_checks_passed == 3 of 3` is currently satisfiable by evidence
that attests nothing. A reader re-deriving the round's "seat accounting" from such bytes would
re-derive zero and be told the ledger passed. This is the one finding I would want fixed before the
L1's own settlement is scored: add a vacuity floor (at minimum `spawn >= 1`, `len(seats) == spawn`,
`reports_written >= 1`) and it costs three lines in `check_l1`.

## Second finding — documented exit code 2 is unreachable

The module docstring declares `2 the evidence cannot be evaluated`, but `main()` returns only `0` or
`1`. Measured with a revision that does not exist (`0000000000000000000000000000000000000000`):

```
C1 ledger 0/3 met=False …  L1/L2/L3 FAIL "… absent at the measured revision"   exit=1
```

so an unreadable/absent revision is indistinguishable from evidence that was read and found
defective. For C1's counting command this matters: a typo in `--revision`, or a wave that never
committed its evidence, both print `0/3` and exit 1 — the same bytes a genuine failed ledger prints.
Either implement exit 2 for the "cannot evaluate" path or drop the claim from the docstring.

## Third finding — the counter's report directory is a shared naming surface

`check_l1` treats **every** committed `w1/*.md` as a seat report and fails any whose basename is not
a seat the settlement lists as `report:true`. Consequently this report
(`w1/ExecLedgerMutants.md`) will itself be a "committed report file for an unknown seat" once
committed, unless the L1's settlement names `ExecLedgerMutants` as a settled seat with `report:true`
and counts it in `reports_written`. `w1/swarm-registry.json` is safe (`.json`, filtered out). The L1
should either name every `w1/*.md` producer as a seat or narrow the counter to a seat-report naming
prefix — otherwise committing the wave's own review artifacts breaks L1 by construction.

## Reproduce

```
cp .ufo/waves/round-51/c51_wave_ledger.py /tmp/r51-mut-l1/
# fixture + mutants: built by an in-memory harness; each mutant is a fresh copy of
# /tmp/r51-mut-l1/fixture with one defect applied and committed, then:
python3 -B /tmp/r51-mut-l1/c51_wave_ledger.py --root /tmp/r51-mut-l1/mut-<tag> \
        --revision "$(git -C /tmp/r51-mut-l1/mut-<tag> rev-parse HEAD)"
```
Captured results for all twelve runs: `/tmp/r51-mut-l1/results.json` (tag, exit, passed, notes, rev).

## Tooling

No installs or upgrades were needed or performed (python3 3.14.8 and git only). Pacman untouched.

## Caveats

- The five required mutants prove the counter's **rejection logic** on a fixture I authored; they do
  not prove anything about the wave's real settlement, which is absent from the measured revision.
- The fixture satisfies the counter as written. I did not audit whether the fixture's shape matches
  what the L1's `build_wave_evidence.py` will emit; if the real settlement uses different key names
  (`settled`/`dead`/`spawn`/`reports_written`), L1 will fail for shape reasons no mutant here covers.
- Reading `LOG.md` via `git show <rev>:LOG.md` is the lane's live log; if the L1 edits it after the
  measured commit the wall-clock note must still be present in that commit's bytes.
