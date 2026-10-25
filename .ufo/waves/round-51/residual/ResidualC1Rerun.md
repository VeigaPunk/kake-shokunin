# ResidualC1Rerun — C1 ledger re-run and independent L1 re-derivation (round 51, residual wave 2)

Seat `L1Kake51.ResidualC1Rerun` (reviewer) · lane `/home/vgpnk/Projects/shokunin/kake-shokunin` (read-only) ·
measured revision `907790c78008819fc95c988431188f90b81f0d5f` · do-nothing base `007d66e4e8360a5f88d29a93eeedd8066dad4434` ·
`python3 -V` → `Python 3.14.8`. `HEAD` at run time equals the measured revision
(`git rev-parse HEAD` → `907790c78008819fc95c988431188f90b81f0d5f`), and the base is an ancestor of it
(`git merge-base --is-ancestor 007d66e 907790c` → exit 0).

Bytes the rerun is bound to, hashed from the commit (not from the worktree):

| path at `907790c` | sha256 |
|---|---|
| `.ufo/waves/round-51/c51_wave_ledger.py` | `714c1017886dcace5e06123853e442dd5363b9cf35fb81e20d2f2b9ef60eba7c` |
| `.ufo/waves/round-51/settlement.json` | `30a5cc46ca8ed4c511c50e2d798d4dacced36adcbac1440589761a6e55fc3d6b` |
| `.ufo/waves/round-51/w51-taskcall.json` | `135364c5dae91b86344082a9f2ebb4e65957d08f350da428bdb630a0a5cdd9a2` |

Read-only except this file. Scratch lived in `/tmp/r51-residual-c1`. **No tool was installed or upgraded**
(no pacman/uv/npx/cargo transaction was run, so the host-wide pacman pause was never exercised).

**Verdict on the two things I was asked to re-run and re-check:** C1's counter prints `3/3 met=True`, exit 0 at
`907790c` and `0/3 met=False`, exit 1 at the base; every note list is empty; and an independent listing of the
committed reports gives **48** seat-report files against the settlement's `reports_written: 48`, with the
**same 48 names on both sides**. No defect that falsifies the frozen predicate was found.

---

## 1. C1 re-run — plain mode

```
$ python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-51/c51_wave_ledger.py \
    --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 907790c78008819fc95c988431188f90b81f0d5f
C1 ledger 3/3 met=True  (met: ledger_checks_passed == 3 of 3)
  L1 pass
  L2 pass
  L3 pass
  revision: 907790c78008819fc95c988431188f90b81f0d5f
EXIT=0
```

**Notes printed: none.** The plain renderer emits a `    - <note>` line for every note
(`c51_wave_ledger.py:290-291`); none appeared, which agrees with `"notes": []` for all three checks below.

## 2. C1 re-run — `--json`

```
$ python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-51/c51_wave_ledger.py \
    --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 907790c78008819fc95c988431188f90b81f0d5f --json
{
  "schema": "kake-r51-c1-wave-ledger-v1",
  "predicate": "met: ledger_checks_passed == 3 of 3",
  "revision": "907790c78008819fc95c988431188f90b81f0d5f",
  "checks": {
    "L1": {
      "passed": true,
      "notes": [],
      "facts": {
        "payload_spawn": 48,
        "settlement_spawn": 48,
        "payload_seats": 48,
        "settlement_seats": 48,
        "settlement_reports_written": 48,
        "seats_marked_with_report": 48,
        "committed_report_files": 48
      }
    },
    "L2": {
      "passed": true,
      "notes": [],
      "facts": {
        "roles": 10,
        "receipts": 2
      }
    },
    "L3": {
      "passed": true,
      "notes": [],
      "facts": {
        "aggregate_seat_seconds": 23554,
        "dead_seat_seconds": 0,
        "wall_clock_seconds": 897,
        "timeout_seconds": 3600
      }
    }
  },
  "ledger_checks_passed": 3,
  "met": true
}
EXIT=0
```

The two invocations are independent processes over the same committed bytes and agree figure for figure; the
`--json` `revision`, `predicate` and `met` fields match the plain header line.

### The three facts blocks, restated

- **L1 — seat accounting:** `payload_spawn` 48 = `payload_seats` 48; `settlement_spawn` 48 = `payload_seats` 48;
  `settlement_seats` 48; `settlement_reports_written` 48 = `seats_marked_with_report` 48 =
  `committed_report_files` 48.
- **L2 — route receipts:** `roles` 10, `receipts` 2 (the two `.json` probe receipts under
  `.ufo/waves/round-51/route-probes/`; the seven `.txt` probes are not receipts and are not parsed).
- **L3 — time accounting:** `aggregate_seat_seconds` 23554, `dead_seat_seconds` 0, `wall_clock_seconds` 897,
  `timeout_seconds` 3600.

## 3. Do-nothing control at the base

```
$ python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root . --revision 007d66e4e8360a5f88d29a93eeedd8066dad4434
C1 ledger 0/3 met=False  (met: ledger_checks_passed == 3 of 3)
  L1 FAIL
    - settlement receipt absent at the measured revision
  L2 FAIL
    - route map absent at the measured revision
  L3 FAIL
    - settlement receipt absent at the measured revision
  revision: 007d66e4e8360a5f88d29a93eeedd8066dad4434
BASE_EXIT=1
```

Base failure is by absence, not by a wrong number: L1 and L3 stop on the missing settlement
(`c51_wave_ledger.py:101-102`, `:206-207`), L2 on the missing route map (`:148-149`). The counter's exit convention
(`0` met / `1` not met, `:293`) is what the frozen claim's `met=True` rests on.

## 4. Independent L1 re-check (my own code, not the counter's)

I did not reuse `check_l1`. I listed the tree myself and compared it with the settlement's typed count and
with its per-seat `report` flags.

```
$ git -C . ls-tree -r --name-only 907790c78008819fc95c988431188f90b81f0d5f -- .ufo/waves/round-51/w1
```
→ **49 files**, of which **48 end in `.md`** and one does not:
`.ufo/waves/round-51/w1/swarm-registry.json` (the dispatch registry the payload names as
`registry.path`, not a seat report).

The 48 committed seat reports, as listed by git:

```
ConnectorSiblingOverlap  CriticAbsence            CriticCapability        CriticGateCriterion
CriticHarm               CriticIds                CriticQuarantine        CriticShape
CriticStaleRows          CriticTautology          CriticZeroControl       ExecAccountingPrototype
ExecCensusMirrorValidate ExecLedgerMutants         ExecQuoteCounterMutants ExecQuoteRawScan
ExecRegistryDiff         ExecRowShape             ExecSourceDigest        ExecSpecLint
MutationDropReport       MutationRoute            MutationSourceSha       MutationSwapIds
MutationWallClock        RevengerR50              ReviewAppendOnly        ReviewC1Predicate
ReviewC2Conditions       ReviewEntryScope         ReviewL1Accounting      ReviewL2Routes
ReviewL3Time             ReviewQualityBar         ReviewReportContract    ReviewShonen
ScoutCensusBefore        ScoutCounterC1Base       ScoutCounterC2Base      ScoutCounterC2Tip
ScoutMisroot             ScoutQuarantineSlice     ScribeEntryAudit        ScribeLessonShape
ScribeReportSources      ScribeSourcesCells       SentinelWriteScope      SimplifierCounters
```

Set comparisons I ran (`/tmp/r51-residual-c1/l1_indep.py`):

| check | result |
|---|---|
| committed `.md` count vs `settlement.reports_written` | **48 = 48** (`settlement.json:399`) |
| seats with `report: true` vs committed `.md` basenames, both directions | equal; missing `[]`, extra `[]` |
| settlement `spawn` (`settlement.json:8`) vs payload seat count | 48 = 48 (`w51-taskcall.json:17`, `counts.total` 48, `resume` 0) |
| payload `taskCall.tasks` names, 48 entries, uniqueness | 48 unique names, no duplicate |
| payload names vs settlement `settled`+`dead` names | identical sets; payload-only `[]`, settlement-only `[]` |
| `settlement.seats` name list vs `settled` names | identical, same order |
| per-seat `role` vs the payload task's `agent` field | 0 mismatches across 48 |
| `settled_count`+`dead_count` vs entry counts | 48+0 = 48 settled entries, 0 dead entries |
| seat `exit` codes | all 48 are `0`; no non-zero |
| Σ seat `seconds` | **23554**, re-derived independently and equal to L3's `aggregate_seat_seconds` |
| report bodies: empty / duplicate blobs / `TODO` markers | none empty (min **5020** bytes, max 41299, median 12376.5), **48 distinct** blob hashes, no `TODO` |

Timing pair, to check 897 is re-derived and not copied: `wave-timing.json` carries
`startedAt 2026-10-25T06:32:17+00:00` → `settledAt 2026-10-25T06:47:14+00:00` = **897 s**, which equals both
`round-time-accounting.json.wall_clock_seconds` and the figure named in `LOG.md:2088`
("48 seats, 48 settled, 0 dead, 48 committed reports, wall clock **897 s**").

## 5. Findings

No HIGH finding: nothing I ran contradicts the frozen predicate, and the L1 equality is not boilerplate —
the count equality is falsifiable and would break on any single missing, renamed or extra `.md`.

**MEDIUM-1 — `reports_written` and the reports it counts were committed in the same commit, so L1 cannot show
the number was written before the files it certifies.** `settlement.json:399` (`"reports_written": 48`) and all
48 reports enter the tree at `907790c` (`git log --oneline` puts "land the wave evidence, the ledger verdict and
the mirror repair" at that commit; its single parent is `9d13768`). L1 crosses the typed number against git's
listing — that is a real cross-check, since a settlement claiming 47 or 49 fails — but it is a *consistency*
check, not an *ordering* check: a settlement authored after the reports, with the count read off the tree, is
indistinguishable from one authored before. This is the same self-attestation property
`.ufo/waves/round-51/w1/ReviewL1Accounting.md` records from the adversarial side; the residual seat confirms it
holds at this revision rather than adding a new hole. Nothing in the frozen predicate asks for ordering
evidence, so this is a limitation to carry forward, not a miss.

**LOW-2 — the report directory holds 49 files while `reports_written` is 48, and the difference is only visible
if the reader applies the same `.md` filter as the counter.** `c51_wave_ledger.py:110-114` builds its report list
with `if p.endswith(".md")`. A reader who runs `git ls-tree … | wc -l` (49) against `reports_written` (48) sees a
one-file gap that is `swarm-registry.json`, the dispatch registry. The contract sentence ("the committed
seat-report count under `.ufo/waves/round-51/w1/`") is satisfied, because a registry is not a seat report; the
hazard is documentation-only — a future census that counts files rather than `.md` files would report a phantom
missing report.

**INFO-3 — L1 never opens a report body, so body-level evidence is outside its reach; measured, no defect.**
A report could in principle be empty or a byte-copy of another seat's report and still satisfy L1's name equality.
At this revision: 48 distinct blobs, minimum 5020 bytes, no empty file, no `TODO`. As a further spot check,
47 of the 48 bodies contain their own seat name as a string; the one exception is
`w1/ReviewC2Conditions.md` (22627 bytes), whose title is prose ("Review — C2 (freshness) conditions vs. counter,
round 51 wave 1") and whose head quotes the C2 counter's own `8/8 met=True` output at `9d13768`. Benign — self-naming
is not an L1 condition — but recorded so the absence is not later read as a misattributed report.

**INFO-4 — one canonical runtime, no same-identity rerouting (checked because the L2 facts are thin: 10 roles,
2 receipts).** All ten role bindings in `route-map.json` carry `kimiModel: commandcode/deepseek/deepseek-v4.1-flash`
— the set of used aliases has exactly one member — and all 48 settlement seats record that same model. Its receipt
is `route-probes/commandcode_deepseek-v4.1-flash.json`: `alias` matches, `httpStatus` is the integer `200`,
`ok: true`, excerpt 82 bytes. The only other receipt is `xai-oauth/grok-4.7-fast`, `httpStatus` integer `403`,
`ok: false`, excerpt 200 bytes, `boundToRoles: []`, and it is recorded as a deviation in
`route-map.json.deviations[0]` with `resolution: "no role bound; every role routes @m_flash per the operator role map"`.
So the two-receipt fact is honest: nine probes were taken, one route was used, one failed and was excluded.
Residual note: the declared fallback `devin/swe-2-max` has a probe `.txt` but no `.json` receipt, which L2 does
not require while it is unused — but the moment a role is bound to it, L2 will fail until a receipt exists.

**INFO-5 — the worktree is not the tree the counter reads, and I did not confuse them.** At run time
`git status --porcelain` shows five committed w1 reports as `M` (`CriticZeroControl`, `ExecRegistryDiff`,
`ReviewAppendOnly`, `ReviewC2Conditions`, `SentinelWriteScope` — wave-2 seats appending to them) plus untracked
wave-48/round-51 assimilation paths. `c51_wave_ledger.py` reads only `git show`/`git ls-tree` (`:56-81`), so the
`48` I report is the count in `907790c`, not the count in the working tree; a reader who re-runs the same command
gets the same 48 until those edits are committed, at which point the count stays 48 but the bodies change.

## 6. Residual risk and verification gaps

- **Unrun checks: none of the ones I report.** Every number above came from a command whose output is quoted.
  I did not run any mutant settlement against L1 (mutation seats own that); my falsifiability evidence is
  structural — 49 files vs 48 `.md`, and a name-set comparison that reports `missing`/`extra` explicitly
  (`c51_wave_ledger.py:135-141`).
- **What C1 still cannot prove:** that the 48 named seats actually executed. L1 certifies the accounting shape of
  the wave (counts, names, receipts, time arithmetic), not the execution trace — no transcript sha, exit receipt
  or per-seat artifact is bound in. That is the frozen predicate's own scope, and the base control shows the
  counter is not trivially true; a reader must not read `3/3` as "the wave ran".
- **Not re-derived here:** L2's `.txt` probe bodies (nine probe files exist; only the two `.json` ones are
  receipts and only those were parsed) and the C2 half of the round. Both are other residual seats' items and
  C1's counter does not read C2's inputs (`contract.json.separability`), which my run respects: nothing I ran
  touched the registry, the two entries, the retained bodies or the mirror.
