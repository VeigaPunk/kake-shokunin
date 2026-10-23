KILLED — counter v4's common-host and repeated-host detection survives every single-generator weakening I removed; the only MET verdicts are the acceptance-required population removal (m2) and a two-generator removal (m5, one survivor).

Sandbox /fast/scratch/hyaku/kake-r43/MutCounterHost/ only; lane sources never written. Frozen sources re-verified after all runs: `.ufo/waves/round-43/c43_count_v4.py` 1c3b9661…fe8eab and `scripts/sitemap_audit.py` 914ebdee…cd021 unchanged — no restore needed, no tool installs.

Controls (one-member weakenings of the build 914ebdee…, both kept byte-identical elsewhere):
- `/fast/scratch/hyaku/kake-r43/MutCounterHost/ctl_hosttable.py` sha256 d29cdc7f4616cd665fe683ca028f589b12dc2d78b566512abc0a5e6a99d392b8 — `_audit_loc` returns with no finding when the raw authority host is in a static table {localhost, example.invalid, sitemaps.invalid, test.invalid}.
- `/fast/scratch/hyaku/kake-r43/MutCounterHost/ctl_repeat.py` sha256 fe5803fd2198aeeb8b723ccb2310ed3781cea8bf903d8533bc91726803a99125 — `_audit_loc` memoizes per raw authority host: once one loc for a host is accepted, later locs of that host are accepted unvalidated.
Isolation check (`python3 -B smoke.py`, exit 0): ref41.py 50287ac6…dd7d flags `https://example.invalid/a bc` loc_not_absolute@2, ctl_hosttable clean; ref41 flags `https://rep.test/a bc` loc_not_absolute@3, ctl_repeat clean; build 914ebdee… output equals ref41 exactly.

Command per receipt (`--seed` never passed; each run draws os.urandom):
`timeout 900 prlimit --as=8000000000 -- python3 -B <counter> --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file <tool> --label <label> --out <label>.json` — exit 0 met / 1 not met / 2 cannot evaluate. All exits below as printed; ≤3 counters ran at once.

| counter (sha256[:12]) | one-member change (diff vs v4 is exactly this) | control | equalRuns | met | unequal runs | exit |
|---|---|---|---|---|---|---|
| v4.py (1c3b96610873) | none — frozen baseline | ctl_hosttable | 9/11 | false | F, T3 | 1 |
| m1_f_commonhost.py (52c4a4cdff03) | `range(150)`→`range(0)` on both F common-host loops (300 values) | ctl_hosttable | 10/11 | false | T3 | 1 |
| m6_t3_commonhost.py (ecb57d4a99b7) | `elif roll < 0.11:`→`elif False:` in shape_t3 (3% common-host) | ctl_hosttable | 10/11 | false | F | 1 |
| m2_table4.py (c93231433f7f) | the four tabled hosts deleted from COMMON_HOSTS (population removal) | ctl_hosttable | 11/11 | **true** | — | 0 |
| m5_all_commonhost.py (a8e2e4a83b81) | m1 + m6: all common-host generation removed (two generators) | ctl_hosttable | 11/11 | **true** | — | 0 |
| v4.py (1c3b96610873) | none — frozen baseline | ctl_repeat | 7/11 | false | B, E, F, T2 | 1 |
| m3_f_repeat.py (23b6631626a6) | `for _ in range(8):`→`range(0)` on the F repeated-host blocks (8×50) | ctl_repeat | 7/11 | false | B, E, F, T2 | 1 |
| m4_f_t3_repeat.py (35bf1addd976) | m3 + `elif roll < 0.08:`→`elif False:` (F and T3 repeated-host blocks) | ctl_repeat | 7/11 | false | B, E, F, T2 | 1 |
| m2_table4.py (c93231433f7f) | (same m2) | ctl_repeat | 8/11 | false | E, F, T2 | 1 |

Receipts: `v4-ctlhosttable.json`, `m2-ctlhosttable.json`, `m1-ctlhosttable.json`, `MutCounterHost-v4-ctlrepeat.json`, `MutCounterHost-m3-ctlrepeat.json`, `MutCounterHost-m4-ctlrepeat.json`, `MutCounterHost-m5-ctlhosttable.json`, `MutCounterHost-m2-ctlrepeat.json`, `MutCounterHost-m6-ctlhosttable.json` (seeds recorded in each). Witness probe `python3 -B witness.py` exit 0 (all four hosts, ref41 vs control): `https://localhost/a bc`, `https://example.invalid/a bc`, `https://sitemaps.invalid/a bc`, `https://test.invalid/a bc` → ref41 `loc_not_absolute@2`, ctl_hosttable `clean`; `https://rep.test/ok`, `https://rep.test/ok2`, `https://rep.test/a bc` → ref41 `loc_not_absolute@3`, ctl_repeat `clean`.

Survivors and their witness values:
- m2 (four tabled hosts removed): MET because no generated value carries those hosts any more; the witness that unweakened v4 uses to fail the control is `https://example.invalid/a bc` (F common-host loc, and T3's 3% branch; both vanish under m2).
- m5 (both common-host generators removed): MET, witness as above; removing either generator alone (m1, m6) still fails the control, so the class is doubly generated and loses only under a two-member removal — reported as a coverage bound, not a contract change.

Per checked statement (path:line):
- SCORECARD.md "Round 43 — C1 and C2 declared": v4 catches the F common-host skip — HOLDS (v4 vs ctl_hosttable unequal on F).
- c43_count_v4.py:775-777 (T3 docstring: "repeated-host blocks (8%), common-host values (3%…)"): the common-host half — HOLDS (v4 unequal on T3; with F's copy removed, m1 still fails via T3 at 10/11).
- The same docstring's repeated-host half is OVERSTATED for T3: v4, m3 and m4 all show T3 equal against ctl_repeat (unequal B, E, F, T2), so T3's 8% blocks are inert for this cache shape; the repeated-host class is caught elsewhere (T2's 1000-value same-host files, and B/E/F host reuse), which is why m3 and m4 are unchanged from baseline.
- Any claim that F's repeated-host blocks are a sole load-bearing guard is WRONG: m3 removes them and the unequal set matches baseline, and even m4 (F and T3 blocks gone) is still 7/11. Recorded as redundancy, not a contract change.

Bounds honoured: no subagents, lane read-only (`git -C … status --porcelain` shows only sibling untracked reports), all runs `timeout`-bounded ≤900 s and `prlimit --as=8000000000`, no network, no pacman, processes all exited before this report.
