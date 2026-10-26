# MutC1PinsV2

Round-57 W2 mutation test of the version-2 C1 counter. Target: `.ufo/waves/round-57/c57_receipt_pins.py` read at lane
revision `4b8c73050470ada9e6583f3b12d659d1bed6a17f` (`git show <rev>:<path>`), copied byte-identical to scratch
`/tmp/mutc1pins.VCphGS/` (sha256 `955c7abae1e5057b53f7ad8e1a9a07056ec7027bf57bf317d5f7a364c1531ee1`; blob hash matches).
The lane working-tree copy (`8cf3c36e…`, differs — L1 repairs) was never read for the mutation work and never written.
44 single-point mutants were generated (one exact-once string replacement each, all compiling, each a one-line diff);
detector = the mutant's own `--selftest` (48 checks, ~5 s). Pristine baseline: **48/48, exit 0, confirmed by running**.
Verdict rule: selftest exit ≠ 0 ⇒ KILLED; exit 0 ⇒ re-run against a fixture-augmented 73-check suite (25 added fixtures,
pristine baseline **73/73, exit 0, confirmed by running**). All runs in mktemp scratch; the lane repo received only this
report and `MutC1PinsV2.files/`. Restoration: nothing to restore — the source at `4b8c730…` is immutable and its scratch
copy is hash-unchanged; all mutants live under `/tmp`.

## MUTANTS:

| # | mutant | point (line at 4b8c730) | single-point change | killed by | verdict |
|---|--------|------------------------|---------------------|-----------|---------|
| 1 | walk-topo | 119 | drop `--topo-order` | fx_backdated_side | KILLED (fixture) |
| 2 | walk-reverse | 119 | drop `--reverse` | old relabel disclosed…; rename plus relabel… | KILLED |
| 3 | walk-M | 119 | drop `-M` | fx_renames_off (`diff.renames=false`) | KILLED (fixture) |
| 4 | rec-status | 128 | `parts[0][0]`→`parts[0]` | rename plus relabel in one commit… | KILLED |
| 5 | rename-pop | 152 | `last.pop(old,…)`→`last.get(…)` | fx_rename_reuse | KILLED (fixture) |
| 6 | rename-carry | 161 | `cur or prev`→`cur` | fx_rename_strip_repin | KILLED (fixture) |
| 7 | rename-latch | 153 | move-out `if prev:`→`if True:` | fx_moveout_unpinned | KILLED (fixture) |
| 8 | compare-empty-target | 143 | drop `or [""]` | stripped then re-pinned yields two relabels | KILLED |
| 9 | compare-same-pin | 144 | `if a != b:`→`if a:` | fx_second_pin_old | KILLED (fixture) |
| 10 | delete-uncond | 168 | `if last.get(path):`→`if True:` | fx_delete_unpinned | KILLED (fixture) |
| 11 | delete-gone-filter | 179 | drop `if p not in present` | — (see SURVIVORS) | SURVIVED |
| 12 | shortfall-drop-gone | 219 | drop `- len(gone)` | receipt deleted; a receipt moved out… | KILLED |
| 13 | outside-all-present | 218 | `len([p … not startswith])`→`len(present)` | fx_shortfall | KILLED (fixture) |
| 14 | exclude-never | 74 | EXCLUDE_RE→never-match | fx_ladder_pretty | KILLED (fixture) |
| 15 | rev-colon | 75 | `[:=]`→`:` | …= form relabel detected | KILLED |
| 16 | rev-quote | 75 | `"?revision"?`→`revision` | quoted JSON key relabel detected | KILLED |
| 17 | rev-bound | 75 | drop `\b` after `{40}` | fx_hex41 | KILLED (fixture) |
| 18 | firstadd-oldest | 189 | `lines[0]`→`lines[-1]` | fx_readd_draft_c2 | KILLED (fixture) |
| 19 | firstadd-alltouches | 188 | drop `--diff-filter=A` | fx_counter_touched | KILLED (fixture) |
| 20 | intro-noancestor | 235 | drop `is_ancestor(counter_intro, measured)` | measured revision predates the counter | KILLED |
| 21 | intro-eq | 257 | `measured_rev != intro`→`==` | honest, no relabel (+4 more) | KILLED |
| 22 | claim-extra2 | 249 | `paths[1:]`→`paths[2:]` | second receipt for claim 2 | KILLED |
| 23 | newre-digit | 72 | `([123])`→`(\d)` | fx_c4_valid | KILLED (fixture) |
| 24 | body2-metany | 78 | `met=True`→`met=(True\|False)` | fx_body2_metfalse | KILLED (fixture) |
| 25 | body2-4of5 | 78 | `5 of 5`→`4 of 5` | honest, no relabel (+4 more) | KILLED |
| 26 | body-crlf | 260 | drop `\r\n` normalisation | fx_c2_crlf | KILLED (fixture) |
| 27 | tip-eq-allowed | 272 | drop `t0 != lc` | — (see SURVIVORS) | SURVIVED |
| 28 | tip-anc-dropped | 272 | drop `is_ancestor(t0, lc)` | fx_side_copy | KILLED (fixture) |
| 29 | tip-all3 | 273 | `("1","2","3")`→`("1","2")` | — (see SURVIVORS) | SURVIVED |
| 30 | tip-multitip | 267 | `len(tips) == 1`→`tips` | fx_two_tips | KILLED (fixture) |
| 31 | tip-rerunmet | 279 | drop `rerun["met"] and` | new receipt missing claim 3… | KILLED |
| 32 | tip-cbtrue | 277 | recursion `check_bodies=True` | honest, no relabel (+4 more) | KILLED |
| 33 | sc-section | 287 | `^## Round 57\b`→`…$` | honest, no relabel (+4 more) | KILLED |
| 34 | sc-nobullet | 288 | drop `(?:[-*][ \t]+)?` | fx_bullet_pin | KILLED (fixture) |
| 35 | sc-any | 289 | `all(x == measured…)`→`any(…)` | SCORECARD names a second measured revision | KILLED |
| 36 | base-ancestorgone | 222 | guard→`if False:` | history without the base revision is flagged | KILLED |
| 37 | basepop-45 | 64 | `BASE_POPULATION = 44`→`45` | fx_base_population | KILLED (fixture) |
| 38 | errata-dupok | 205 | duplicate check→`if False:` | errata duplicate entries are malformed | KILLED |
| 39 | errata-3keys | 202 | drop `"commit"` key check | fx_errata_int_commit | KILLED (fixture) |
| 40 | measured-prefix | 230 | `HEX40.fullmatch`→`HEX40.match` | — (see SURVIVORS) | SURVIVED |
| 41 | exit-flip | 664 | met/exit polarity swap | CLI met repo exits 0; CLI unmet repo exits 1 | KILLED |
| 42 | usage-zero | 652 | argparse `else 64`→`else 0` | fx_unknown_flag (`--no-such-flag`) | KILLED (fixture) |
| 43 | uneval-1 | 662 | unevaluable exit 2→1 | CLI malformed errata exits 2 | KILLED |
| 44 | newpaths-noafter | 238 | basename filter→`True` | fx_nonclaim_quiet | KILLED (fixture) |

Score: 40/44 killed (18 by the shipped selftest, 22 only after the fixtures below). All KILLED/SURVIVED verdicts confirmed by running.

## SURVIVORS:

Four surviving mutants; each is a coverage finding about the selftest, not a licence to change the contract.

1. **delete-gone-filter (line 179) — equivalent mutant.** `deleted` is only appended in the D branch (167-169) and the
   move-out branch (153-156); every re-entry path executes `deleted.discard(path)` (add/M branch) or
   `deleted.discard(new)` (R branch, 157-163), so a path latched *and* present at the tip cannot exist — the
   `p not in present` filter is dead code. No fixture can kill it while `discard` covers re-entry.
   Confirmed by running: passed both the 48-check and 73-check suites.
2. **tip-all3 (line 273) — equivalent while the rerun gate exists.** `rerun = measure(root, t0, check_bodies=False)`
   with `ok = rerun["met"] and first == want` (277-279): `met` requires `new_receipts == 3` *at t0*, which already
   implies all three receipts exist at t0. The explicit all-three blob check is strictly weaker (defense-in-depth).
   Fixture `fx_late_c3` (claim 3 landing after t0) was validated on pristine and run against the mutant: the mutant
   still rejects the receipt via `rerun['met']=False`, i.e. the check is subsumed, confirmed by running.
3. **tip-eq-allowed (line 272) — equivalent by construction.** `lc` is the last commit that wrote after-c1; the `tip:`
   line names a commit whose 40-hex hash must be fixed before the body text exists, so `t0 == lc` is unreachable
   (a commit cannot embed its own hash) and `t0 != lc` is always true when the check runs.
   [INFERENCE] for the hash-impossibility argument; the survival itself is confirmed by running.
4. **measured-prefix (line 230) — equivalent at the counter's observable surface.** `fullmatch`→`match` accepts a
   41-hex `revision`, but the code assigns the **full string** (`measured_rev = mdata["revision"]`), which then
   mismatches every 40-hex receipt pin and scorecard pin — the same counters result (new_unpinned +1 either way,
   scorecard_pin 0, new_receipts < 3). Distinguishing it would require asserting the note *text*
   ("revision is not 40-hex" vs "does not descend from the commit that added the counter"), which the selftest's
   assertion surface (`met` + the seven KEYS) cannot express. `fx_measured_41` was validated on pristine and run
   against the mutant: identical verdicts, confirmed by running.

## PROPOSED FIXTURES:

25 fixtures, in `scenario(...)`/`honest(...)` style, inserted into a copy of the selftest
(`MutC1PinsV2.files/c57_receipt_pins_fx.py`; pristine passes **73/73, exit 0, confirmed by running**; scratch runs
also kept in `MutC1PinsV2.files/{battery_results,survivor_results,killed_details}.txt`). Each fixture below killed its
target mutant on first validation (single re-run each, no tuning loop), except #12/#17 which demonstrated the
equivalences above instead.

1. `fx_shortfall` — base population 2, one receipt present at tip ⇒ shortfall counts; kills `outside-all-present`.
2. `fx_moveout_unpinned` — unpinned receipt `git mv`'d out of the population; kills `rename-latch`.
3. `fx_delete_unpinned` — unpinned receipt deleted; kills `delete-uncond`.
4. `fx_rename_reuse` — old name re-added after a rename; kills `rename-pop`.
5. `fx_rename_strip_repin` — pin stripped via rename (200-line body for rename similarity), re-pinned; kills `rename-carry`.
6. `fx_second_pin_old` — receipt gains a second pin, then honest() re-pins ⇒ exactly 2 relabels; kills `compare-same-pin`.
7. `fx_hex41` — 41-hex revision line is not a pin; kills `rev-bound`.
8. `fx_readd_draft_c2` — receipt drafted at the measured commit, deleted, re-added at t0; kills `firstadd-oldest`.
9. `fx_counter_touched` — counter file edited after the run; kills `firstadd-alltouches`.
10. `fx_body2_metfalse` — claim-2 `met=False` report line carrying `EXIT=0`; kills `body2-metany`.
11. `fx_c2_crlf` — CRLF claim-2 body still matches; kills `body-crlf`.
12. `fx_late_c3` — claim 3 lands after the tip named by claim 1; validated (pristine passes, mutant survives) ⇒ proves `tip-all3` equivalence.
13. `fx_errata_late` — errata published after the t0 run; validated on pristine (target `tip-rerunmet` was already killed by the shipped suite, so the fixture is redundant but sound).
14. `fx_two_tips` — second `tip:` line voids the c1 body; kills `tip-multitip`.
15. `fx_side_copy` — t0 on a side branch, body written on main before a `-X ours` merge ⇒ `is_ancestor(t0, lc)` false; kills `tip-anc-dropped`.
16. `fx_bullet_pin` — bulleted `- Measured revision:` line counts; kills `sc-nobullet`.
17. `fx_measured_41` — 41-hex measured revision; validated ⇒ proves `measured-prefix` equivalence.
18. `fx_errata_int_commit` — errata entry with non-string `commit`; kills `errata-3keys`.
19. `fx_backdated_side` — backdated (2005) side-branch relabel merged at tip; kills `walk-topo`.
20. `fx_c4_valid` — valid-bodied `after-c4` receipt: malformed name, three claims stay; kills `newre-digit`.
21. `fx_ladder_pretty` — ladder JSON with bare revision lines; kills `exclude-never` (the shipped ladder scenario embeds the pin inside a JSON string `REV_RE` cannot match, so only the name exclusion is exercised today).
22. `fx_nonclaim_quiet` — quiet round-57 non-claim control is not an `after-*` receipt; kills `newpaths-noafter`.
23. `fx_renames_off` — move+relabel with `diff.renames=false` (`-M` must force detection; git ≥ 2.9 defaults it on, which is why `walk-M` survived the pristine battery); kills `walk-M`.
24. `fx_unknown_flag` — CLI `--no-such-flag` must exit 64 (the shipped "usage error exits 64" exercises the `if not args.revision` branch, not the argparse `SystemExit` handler); kills `usage-zero`.
25. `fx_base_population` — restores the counter's own default (`BASE_POPULATION = 44`) from its source and builds 43 out-of-57 receipts ⇒ shortfall 1 (pristine) vs 2 (mutant); kills `basepop-45`.

Findings for the selftest's owner (coverage, not contract changes): the population-shortfall formula, the rename
handling, the `tip:` body rules and the exit codes were the under-covered areas — 22 of 26 selftest survivors needed
new fixtures; three of the four remaining survivors mark dead or subsumed code (items 1-2 above), which the maintainer
may simplify or keep as defense-in-depth.

VERDICT: 44 single-point mutants of c57_receipt_pins.py@4b8c730: 40 killed (18 shipped selftest, 22 via 25 new validated fixtures, all confirmed by running), 4 equivalent survivors documented with arguments; source untouched (blob sha256 955c7aba… identical before/after).
