# MutationRoute — C1/L2 mutant: used route's receipt flipped to `ok: false`

Seat: `L1Kake51.MutationRoute-2` (mutation-tester). Scope: one probe on C1's L2
(route receipts) of the committed counter `.ufo/waves/round-51/c51_wave_ledger.py`.
Lane read-only; everything below ran in `/tmp`. No subagents dispatched.

## Why a fixture and not the lane bytes

The lane tip `9d13768c4fdd0e9a2688d2ecf1616b539cf57658` scores **0/3**, so it cannot
serve as the mutation baseline (a baseline failure is inconclusive, not a killed mutant):

```
$ python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root . --revision 9d13768c4fdd0e9a2688d2ecf1616b539cf57658
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

Reason: `settlement.json`, `w51-taskcall.json`, `route-map.json`, `route-probes/`,
`wave-timing.json`, `round-time-accounting.json`, `wave-grant.txt` and `w1/*.md` are
still untracked in the lane worktree (`git status --porcelain` lists them as `??`).
So the baseline is a minimal fixture whose committed bytes make L1+L2+L3 pass.

## Fixture (`/tmp/mutroute-51/fixture`, plain git repo, 13 files, 3 commits)

Only the paths the counter reads, no invented semantics:

| path | role |
|---|---|
| `.ufo/waves/round-51/settlement.json` | spawn 3, settled 2 × report, 1 dead (`exit-1`, 40 s), `reports_written` 2, timeout 1800 |
| `.ufo/waves/round-51/w51-taskcall.json` | 3 tasks, `counts.spawn` 3 |
| `.ufo/waves/round-51/w1/ExecAlpha.md`, `ExecBeta.md` | the 2 committed seat reports |
| `.ufo/waves/round-51/route-map.json` | one role `executor`, `kimiModel` = the used alias; probe text records the xai 403 deviation |
| `.ufo/waves/round-51/route-probes/commandcode_deepseek-v4.1-flash.json` | **used** route, `httpStatus` 200, `ok: true`, body excerpt |
| `.ufo/waves/round-51/route-probes/xai-oauth_grok-4.7-fast.json` | unused failing route, `httpStatus` 403, `ok: false`, body excerpt |
| `.ufo/waves/round-51/wave-timing.json` | `03:00:00Z → 03:04:20Z` (260 s) |
| `.ufo/waves/round-51/round-time-accounting.json` | aggregate 260, dead 40, wall 260 |
| `.ufo/waves/round-51/wave-grant.txt` | `granted lane=kake …` |
| `LOG.md` | names the 260 s wall clock |

Detector copied byte-identically (never re-implemented):

```
counter lane sha256   714c1017886dcace5e06123853e442dd5363b9cf35fb81e20d2f2b9ef60eba7c
counter copy sha256   714c1017886dcace5e06123853e442dd5363b9cf35fb81e20d2f2b9ef60eba7c
```

Baseline revision `b2cc23dc6d795a52f1c76f6add27537a5ba93578`:

```
PRISTINE exit 0 passed 3 met True
  L1 passed [] {'payload_spawn': 3, 'settlement_spawn': 3, 'payload_seats': 3, 'settlement_seats': 3,
                'settlement_reports_written': 2, 'seats_marked_with_report': 2, 'committed_report_files': 2}
  L2 passed [] {'roles': 1, 'receipts': 2}
  L3 passed [] {'aggregate_seat_seconds': 260, 'dead_seat_seconds': 40, 'wall_clock_seconds': 260,
                'timeout_seconds': 1800}
```

## The mutant

One field, at the one behaviour-bearing point: the **used** route's probe receipt, with
the body excerpt left in place. Alias, status, endpoint, probe time untouched.

```
--- a/.ufo/waves/round-51/route-probes/commandcode_deepseek-v4.1-flash.json
+++ b/.ufo/waves/round-51/route-probes/commandcode_deepseek-v4.1-flash.json
@@ -4,3 +4,3 @@
   "httpStatus": 200,
-  "ok": true,
+  "ok": false,
   "bodyExcerpt": "{\"success\":true,\"message\":\"Command Code API\"}",
```

Revision `5ec21d2bd71d807bad7b70ad6729d8056a5ab5e5`.

## Detector output on the mutant

```
$ python3 -B /tmp/mutroute-51/c51_wave_ledger.py --root /tmp/mutroute-51/fixture --revision 5ec21d2bd71d807bad7b70ad6729d8056a5ab5e5
C1 ledger 2/3 met=False  (met: ledger_checks_passed == 3 of 3)
  L1 pass
  L2 FAIL
    - route commandcode/deepseek/deepseek-v4.1-flash was used but its receipt is not ok
    - failing route commandcode/deepseek/deepseek-v4.1-flash was used by a role
    - failing route commandcode/deepseek/deepseek-v4.1-flash is not recorded as a deviation in the route map
  L3 pass
  revision: 5ec21d2bd71d807bad7b70ad6729d8056a5ab5e5
exit=1
```

**Verdict: killed.** The mutant is rejected on the intended note (`used but its receipt is
not ok`, from `check_l2`'s `if receipt.get("ok") is not True` for every alias in the
`kimiModel` used-set) and independently by `failing route … was used by a role`. L1 and L3
stay `pass`, so the kill is localised to L2 and does not leak across checks. No hole to
name: the `ok` flag is load-bearing on a used route.

## Restoration evidence

Pristine bytes restored from the `rev0` blob, not re-typed:

```
used-receipt pristine sha256   db155eaff1372c52c41da0453a9b8516510ae841ad5dca3bfdbd2773deb04e16
mutant           sha256        868ee8dd2eb9d8bea5aabd983b094043341e23ac8f79afd9e2735896c31d0433
restored worktree sha256       db155eaff1372c52c41da0453a9b8516510ae841ad5dca3bfdbd2773deb04e16  (== pristine)
restored blob @ d0f1293 sha256 db155eaff1372c52c41da0453a9b8516510ae841ad5dca3bfdbd2773deb04e16  (== pristine)
```

Re-run on restored bytes `d0f1293999a300d9fefc27a7b9fddc02d1e43308`:

```
RESTORED exit 0
C1 ledger 3/3 met=True  (met: ledger_checks_passed == 3 of 3)
  L1 pass
  L2 pass
  L3 pass
```

and re-running the untouched `rev0` still gives `3/3 met=True`, so the pass/fail flip
tracks the mutated field and nothing in the fixture drifted.

## Observation from the actual output (diagnostic, not a verdict change)

The third note is a **cascade artifact**, not extra evidence: the deviation check joins
only `roles[*].probe` strings and asks whether the alias is a substring, and the fixture's
probe text names the receipt *path* (`commandcode_deepseek-v4.1-flash.json`, underscores)
rather than the alias (`commandcode/deepseek/deepseek-v4.1-flash`, slashes). A single
mutated field therefore produces a second, misleading claim that the used route is
unrecorded as a deviation. Rejection still holds on the first two notes, so this does not
weaken the kill; an operator reading only the last line could be misled about *why* it
failed.

Not exercised, therefore not claimed: no probe of a role that omits `kimiModel` (the
`used` set is built from `kimiModel` alone, so such a role never enters the receipt check),
and no probe of `httpStatus` 500 with `ok: true` (only `isinstance(status, int)` is
enforced, no 2xx requirement). Both are read-only observations of `check_l2`, unmeasured.

## Boundaries

- Lane: no `git`/`jj` mutation, no file written outside this report.
  `git status --porcelain` in the lane carries no `MutationRoute` entry.
- Everything else lives under `/tmp/mutroute-51/` (`fixture/`, `c51_wave_ledger.py`).
- No tool installed or upgraded this run.
