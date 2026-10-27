# ScoutC1Population

ATTACKS: C1 population completeness at B1; frozen path/blob correspondence; extra regex matches; rounds 40–47 and round-60 registry coverage; disclosure accuracy.

POPULATION:
- Contract § C1 (contract.md:47–52, 214–216) defines exactly the population regex for rounds 48–59, same N twice, and says 28 members at base. Counter implementation uses the same regex/range at `c60_gate_status.py:89,213–216`.
- Exact B1 tree query: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin ls-tree -r 8b33fd248d126b48d838af5c38bc175850f41a09 -- .ufo/waves/round-48 ... .ufo/waves/round-59 | <regex/regular-object filter>` returned `28` matching entries and `nonregular=[]`. The 28 paths and OIDs match the counter’s `FROZEN` dictionary (`c60_gate_status.py:104–135`): round counts 48:2, 49:2, 50:2, 51:2, 52:4, 53:1, 54:2, 55:2, 56:2, 57:3, 58:3, 59:3. No extra same-regex path is present in those ranges; a direct path enumeration with the exact regex also returned 28.
- B1 all-wave `ls-tree -r --name-only ... -- .ufo/waves | grep -E '/c[0-9]+_'` did list many historical copies/fixtures under assimilation and reports, plus round-60 counters. Those paths are not extra members: the declared population regex anchors directly under `.ufo/waves/round-N/` with at most one allowed lowercase subdirectory, requires `cN_` and N in 48–59. The three production round-60 files `c60_gate_status.py`, `c60_guard_cases.py`, `c60_quote_truth.py` are excluded by the contract’s upper bound and by code. The C1 counter itself is additionally excluded by `SELF_PATH`.

UNREGISTERED:
- The C1 population check found no committed population member missing from the SKILL registry. B1 `SKILL.md` round-60 ledger has the C1 registry description and entries, including all three round-60 counters (lines 1311–1358); those C60 entries are not C1 population members.
- Rounds 40–47 include 17 top-level counter-like paths from the assigned broad listing: 40:1, 41:2, 42:4, 43:1, 44:4, 45:4, 46:1, 47:3. Contract explicitly excludes them at line 52 and stated limits line 244 (“not claimed”). They are not silently asserted as part of the 28-member C1 result. `SKILL.md` contains older references to some of these counters (e.g. round-47 registry-count in existing prose); they are historical/context references rather than new round-60 registry rows. The requested test was registry coverage accuracy, not re-evaluation of those historical counters.
- No population/unregistered defect observed. No counter was run in this seat; C1 verdict/selftest status is not assessed here.

FINDINGS:

| severity | target file:line | issue | evidence command | fix |
|---|---|---|---|---|
| none | — | No C1 population, frozen-blob, extra-member, registry-coverage, or disclosure inaccuracy found in the scoped attack. | `git -C /home/vgpnk/Projects/shokunin/kake-shokunin ls-tree -r ...` plus exact regex/regular-object enumeration; inspect contract.md:47–52, 239–244 and SKILL.md:1311–1358. | None. |

VERDICT: C1’s declared 28-member population at B1 is complete, its frozen path/blob set matches, no extra regex member exists, and the stated exclusion of rounds 40–47 is accurate; no scoped finding.