# MutationWallClock — C1/L3 wall-clock mutant (A9)

Seat: `L1Kake51.MutationWallClock-2` (mutation-tester, leaf).
Target of attack: C1's L3 condition — "the wave wall clock is re-derivable from the committed
settlement and wave-timing bytes, the committed time-accounting artifact carries the same
figures, LOG.md names the wall-clock figure".

## 1. Measured starting state (lane, read-only)

Commands run against the lane, nothing written:

```
$ python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root /home/vgpnk/Projects/shokunin/kake-shokunin \
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

Lane HEAD is still `9d13768c4fdd0e9a2688d2ecf1616b539cf57658`. The wave evidence
(`settlement.json`, `wave-timing.json`, `round-time-accounting.json`) is uncommitted/absent at
the lane tip, so a mutant applied to the lane could not be distinguished from the missing-evidence
failure. The probe therefore runs on a fixture built in `/tmp` — this is the stated prerequisite,
not a substitute for the real evidence.

## 2. Fixture (built, not assumed)

Builder: `/tmp/r51mut/build_fixture.py` → `/tmp/r51mut/pristine`, one git commit.

| Input | Provenance |
|---|---|
| `.ufo/waves/round-51/w51-taskcall.json` | copied verbatim from the lane (48 seats, `counts.spawn == 48`) |
| `.ufo/waves/round-51/route-map.json` | copied verbatim from the lane (10 roles, all on `commandcode/deepseek/deepseek-v4.1-flash`) |
| `.ufo/waves/round-51/route-probes/*` | copied verbatim from the lane (9 files: 200-ok route + the 403 deviation receipt) |
| `.ufo/waves/round-51/wave-grant.txt` | copied verbatim from the lane (`granted lane=kake wave=r51-w1 seats=48 …`) |
| `LOG.md` | real lane `LOG.md` at `9d13768…` (1924 lines) + one appended wave line naming the wall clock |
| `w1/<Seat>.md` (48) | synthesized one-line fixture reports so L1's report-count condition holds |
| `settlement.json`, `wave-timing.json`, `round-time-accounting.json` | synthesized to the shapes emitted by the lane's own `build_wave_evidence.py` |

Fixture figures: `startedAt 2026-10-25T06:32:17+00:00`, `settledAt 2026-10-25T07:32:17+00:00`
→ wall 3600 s; 48 settled seats, 0 dead, `reports_written 48`; seat seconds `600+i` →
`aggregate_seat_seconds 29928`, `dead_seat_seconds 0`, `timeout_seconds 3600`.

Real `LOG.md` at the tip contains neither `3600` nor `3660` (`git show …:LOG.md | grep -n '3600\|3660\|wall'` matched only unrelated "wall" prose), so the appended line is the only carrier of the figure and cannot mask the mutant.

**Pristine detector run — the fixture genuinely passes, so a later failure is attributable to the mutant:**

```
$ python3 -B <lane>/.ufo/waves/round-51/c51_wave_ledger.py --root /tmp/r51mut/pristine --revision 86a7f4123ed695f2c579fccd604cfd9c6424e74f
C1 ledger 3/3 met=True  (met: ledger_checks_passed == 3 of 3)
  L1 pass
  L2 pass
  L3 pass
PRISTINE_EXIT=0
```

## 3. The mutant

Smallest behavior-bearing point in the L3 derivation: the timing pair's second member.

```
--- a/.ufo/waves/round-51/wave-timing.json
+++ b/.ufo/waves/round-51/wave-timing.json
@@ -2,7 +2,7 @@
   "wave": "r51-w1",
   "startedAt": "2026-10-25T06:32:17+00:00",
-  "settledAt": "2026-10-25T07:32:17+00:00",
+  "settledAt": "2026-10-25T07:33:17+00:00",
   "wallClockSeconds": 3600,
   "source": "L1 pre-dispatch and post-batch timestamps, UTC"
 }
 .ufo/waves/round-51/wave-timing.json | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

`settledAt` moved +60 s; `startedAt`, `wallClockSeconds` and **every other artifact** untouched
(`round-time-accounting.json`, `settlement.json`, `LOG.md` byte-identical to pristine — see §5).
Mutant revision `aa7498598aaecc4c28e86612c6d552eeabbe9566`.

Expected detector: L3 fails on the re-derived 3660 against the recorded 3600 and on LOG.md not
naming 3660; L1 and L2 must be unaffected (they read disjoint inputs).

## 4. Result — mutant KILLED

```
$ python3 -B <lane>/.ufo/waves/round-51/c51_wave_ledger.py --root /tmp/r51mut/pristine --revision aa7498598aaecc4c28e86612c6d552eeabbe9566
C1 ledger 2/3 met=False  (met: ledger_checks_passed == 3 of 3)
  L1 pass
  L2 pass
  L3 FAIL
    - time accounting wall clock 3600 != re-derived 3660
    - LOG.md does not name the re-derived wall-clock figure 3660
  revision: aa7498598aaecc4c28e86612c6d552eeabbe9566
MUTANT_EXIT=1
```

`--json` L3 block on the same revision:

```json
{"L3": {"passed": false,
        "notes": ["time accounting wall clock 3600 != re-derived 3660",
                  "LOG.md does not name the re-derived wall-clock figure 3660"],
        "facts": {"aggregate_seat_seconds": 29928, "dead_seat_seconds": 0,
                  "wall_clock_seconds": 3660, "timeout_seconds": 3600}},
 "passed": 2, "met": false}
```

**Verdict: killed.** Two independent notes fire, `L3` flips pass→FAIL, the aggregate goes 3/3 → 2/3,
and the process exit goes 0 → 1. L1 and L2 stay green, confirming the L3 wall-clock check is not
riding on a side effect in another check. The specific note the mutant produces is
`time accounting wall clock 3600 != re-derived 3660`.

## 5. Restoration evidence

`wave-timing.json` restored with `git show <BASE>:… > …` (pristine bytes, not a re-render).

```
BEFORE (pristine)   fe2b6ea63c5c77db18375c4d8eeeaea5e48c1c14f6b87d4ff971a4593cbed27c  wave-timing.json
MUTANT              21fa3e7fa363d092bb242521af87292a0170276515415922ab43fe99c141fa14  wave-timing.json
AFTER (restored)    fe2b6ea63c5c77db18375c4d8eeeaea5e48c1c14f6b87d4ff971a4593cbed27c  wave-timing.json   ← identical to pristine
untouched, all three states:
  d381c340eea53a2f0fc347692ff8962e293edeee68c480fb0111b7e1a3bfd428  round-time-accounting.json
  2c565e0a52b72b736423ead6c16a9cde9b924ed17623147bcf373cf4f8be90f4  settlement.json
  25146860d25682a51b977d9fa426beef7b8b6767aed1683c2b9283aa490115dd  LOG.md
restored revision 06f16bb9870509e7cdab7e57b6cb3b857d5d00e4
$ git diff --stat 86a7f41 06f16bb   → empty, DIFF_RC=0   (trees identical)
$ python3 -B … --revision 06f16bb9870509e7cdab7e57b6cb3b857d5d00e4
C1 ledger 3/3 met=True    (met: ledger_checks_passed == 3 of 3)   RESTORED_EXIT=0
```

The accounting artifact was never touched across all three states, so the kill is attributable to
the timing mutation alone.

## 6. Coverage finding (surviving mutant, not a contract change)

`wave-timing.json` carries its own `wallClockSeconds` field and L3 never reads it
(`check_l3` derives `wall` from `startedAt`/`settledAt` and compares only
`accounting["wall_clock_seconds"]` and the `LOG.md` text).

Confirmed by execution on a second `/tmp` copy off the same fixture:

```
mutant: "wallClockSeconds": 3600 -> 3660, settledAt untouched
revision 4b50fb0bb8be97237f828a03c0bb13367207fed7
C1 ledger 3/3 met=True  → SECOND_EXIT=0     SURVIVED
```

So L3 certifies internal consistency of a wall clock re-derived from the pair; it does not
certify that the timing artifact is self-consistent. A fabricated-but-coherent triple
(`settledAt`, accounting figure, LOG line all moved together) would also survive — inherent to a
re-derivation check, and out of scope for this probe. Recorded as a coverage observation only; the
contract's L3 text is not challenged by it.

## 7. Bounds and tooling

- Read-only against the lane: only `git show`, `git ls-tree`, `git rev-parse`, `git status`,
  `git log`-class reads and the counter itself were run there. Lane HEAD is still
  `9d13768c4fdd0e9a2688d2ecf1616b539cf57658`; nothing was staged, committed, checked out or stashed.
- All mutation and git writes happened in `/tmp/r51mut/{pristine,second}` (disposable scratch).
- No file in the lane was written except this report.
- No package was installed or upgraded (no pacman/uv/npx invocation), so there is no tool record to report.
