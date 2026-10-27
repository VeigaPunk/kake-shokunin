# CriticC1Before

Attack on C1 BEFORE value (calibration honesty): "19 events, 13 never disclosed". Method: ran `c58_receipt_rewrites.py --revision` at both the contract commit `fff3eea6` and base `04404859` — identical 19-event list. Cross-checked the round-57 errata, then for each of the 13 non-errata events grepped the round's own prose: lane `LOG.md`, `SCORECARD.md`, fleet reports `.ufo/reports/round-5[2-7]/kake.md`, settlements (round-53/55/56/57 `settlement.md`, round-54 `w1/ScribeC2Settlement.md`, round-55 `w2/ExecSeatSettlement.md`), lessons `corpus/lessons/round-5X.md` §Mistakes, and traced when each mention entered history (`git log -S`).

## PER EVENT:

1. `.ufo/waves/round-52/control/c1-mutation-ladder.json` @ `1ae8de5d` (M; relabel of internal `old_tail` revision strings) — **not disclosed**. Round-52 report/LOG/SCORECARD name the receipt only (`round-52/kake.md:43` `c1-mutation-ladder.txt` / `.json`).
2. `.ufo/waves/round-52/control/c1-mutation-ladder.json` @ `a4a890cf` (M; relabel again) — **not disclosed**.
3. `.ufo/waves/round-52/control/c2-quote-selftest.txt` @ `a4a890cf` (M; fixture revision pin `3a50ae43`→`1ae8de5d`) — **not disclosed** (`round-52/kake.md:46`, `SCORECARD.md:4248` list the receipt as a result, not a rewrite).
4. `.ufo/waves/round-52/control/c1-mutation-ladder.json` @ `fd91527a` (M; relabel) — **DISCLOSED at the time** (round-53, ~1.5 h later): `reports/round-53/kake.md:12` "The inherited dirty `round-52/control/c1-mutation-ladder.json` was committed…"; `:19` "dirty receipt committed"; `corpus/lessons/round-53.md:53,56` (§Mistakes items 8 and 11); `LOG.md:2104` ("inherited round-52 mutation-ladder receipt landed together at `fd91527a`…").
5. `.ufo/waves/round-54/controls/c1-selftest.txt` @ `8e408e00` (M; +2 checks: `correction_wrong_polarity`, `correction_before_render`) — **partial/unnamed disclosure**: `LOG.md:2145` "both base controls and the final C1 selftest were rerun after repair" (no filename, no before/after values).
6. `.ufo/waves/round-54/controls/base-c1-s374.txt` @ `a0a4fd48` (M; reworded PASS/FAIL lines, same met result) — **partial/unnamed disclosure**: same `LOG.md:2145` "both base controls … were rerun after repair".
7. `.ufo/waves/round-54/controls/base-c2-ops-debt.txt` @ `a0a4fd48` (M; rerun: `uncovered=4`→`uncovered=7`, cited set 4→7) — **partial/unnamed disclosure**: same `LOG.md:2145` sentence. (Post-event `w1/ScribeC2Settlement.md:67` still quotes `uncovered=4`, i.e. the rewrite was invisible to that seat.)
8. `.ufo/waves/round-54/controls/c1-selftest.txt` @ `a631cc02` (M; +2 checks: `unrelated_marker`, `correction_removed_render`) — **partial/unnamed disclosure**: `LOG.md:2145` as above.
9. `.ufo/waves/round-54/controls/sources-census.txt` @ `5826682b` (M; appended "After (round-end run, measured against lane tip a631cc0246…)" line) — **not disclosed** (`LOG.md:2156` names the file as evidence only).
10. `.ufo/waves/round-55/controls/c1-selftest-v2.txt` @ `64c0ce12` (M; tally `32/32`→`44/44`) — **not disclosed** (`SCORECARD.md:4310`, `round-55/kake.md:43` list final `44/44` only).
11. `.ufo/waves/round-55/controls/c2-selftest.txt` @ `955e3d7` (M; fixture revision pin `faf9abe8`→`64c0ce12`) — **not disclosed**; also **not in the round-57 errata** although it is the same relabel class the errata claims to cover.
12. `.ufo/waves/round-56/controls/c2-selftest.txt` @ `ad06cb8a` (M; tally `67/67`→`86/86`) — **not disclosed** (`SCORECARD.md:4339`, `round-56/kake.md:46` list final `86/86` only).
13. `.ufo/waves/round-57/controls/after-c1-receipt-pins.txt` @ `20217f23` (M; **fill**: `pending` → full receipt) — **DISCLOSED at the time** (same minute): `reports/round-57/kake.md:48-49` "T0 … placeholder C1 receipt" @ `31b61a4d` and "C1 receipt written after its run at T0" @ `20217f23`; commit messages `31b61a4d` ("placeholder C1 receipt") and `20217f23` ("C1 receipt written after its run at T0"); `w2/ExecC1Dryrun.md` documents the placeholder-carrying T0 sequence. Caveat: `SCORECARD.md:4366` simultaneously asserts "none is ever rewritten", so the scorecard contradicts the event while the report discloses it.

## CORRECTED COUNT:

- Claimed: 13 never disclosed. Verified explicit prose disclosures at the time: **2** (events 4 and 13). Strict corrected count: **11 never disclosed** (`reports/round-53/kake.md:12`, `corpus/lessons/round-53.md:53`; `reports/round-57/kake.md:48-49`).
- If the unnamed round-54 `LOG.md:2145` rerun sentence is accepted as disclosure, events 5-8 are also disclosed → lenient corrected count: **7 never disclosed**.
- So "13 never disclosed" is overstated by at least 2 (events 4 and 13), and possibly by 6.

## ERRATA OVERLAP:

- All 6 round-57 errata entries are distinct events among the 19 and match path+commit exactly: r52 `c1-ledger-real.txt`+`c2-quote-real.txt` @ `a4a890cf`; r55 `after-c1-readme-index.txt`+`after-c2-quote-truth.txt` @ `955e3d7`; r56 `after-c1-selftally.txt`+`after-c2-quote-truth.txt` @ `ad06cb8a`. Overlap = exactly 6/19.
- The errata is incomplete for its own class: revision-pin relabels `c2-quote-selftest.txt` (r52, event 3) and `c2-selftest.txt` (r55, event 11) are identical-class relabels not in the errata; the ladder-JSON relabels (events 1,2,4) are also outside it.

VERDICT: The "13 never disclosed" count is overstated — events 4 (round-53 report/lesson/LOG) and 13 (round-57 report/commit messages) were disclosed in prose at the time; corrected count 11 strict (7 if the unnamed round-54 LOG rerun sentence counts); the round-57 errata covers exactly 6 of 19 but misses same-class relabels (events 3, 11).
