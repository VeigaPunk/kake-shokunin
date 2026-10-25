# ExecRegress

Seat: regression surface of round 56 (W2, leaf). Round date 2026-10-25.
Revisions measured: base `e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6` (lane master tip at round open) and tip
`a450e43e696d032e3ac308383f6b3394e0c92860` (revision under attack). Every run in a private clone
(`git clone -q --no-checkout /home/vgpnk/Projects/shokunin/kake-shokunin $D && git -C $D checkout -q <rev>`;
`git -C $D rev-parse --show-toplevel` == `$D` verified), `python3 -B`, cwd = the clone root. Lane untouched; no git or
jj mutation in the lane. No tool installs were needed (host python3 only); nothing was run under pacman.

Blob identity first, because it decides how to read the selftest rows: all six scripts below are byte-identical at the two
revisions (`git rev-parse <rev>:<path>` equal at base and tip): `.ufo/waves/round-55/c55_readme_index.py`
`1a65be474aab`, `.ufo/waves/round-55/c55_quote_truth.py` `1c4688c75028`, `.ufo/waves/round-52/c52_quote_truth.py`
`1bd6e78f80e6`, `.ufo/waves/round-52/c52_wave_ledger.py` `93891e1fe252`, `scripts/citation_lint.py` `87252709fc65`,
`scripts/base_path_selftest.py` `d4e054f359c0`. So a differing result between the two columns is caused by tree content,
never by a code edit.

## TABLE:

`base` = exit / tally at `e48354b`, `tip` = exit / tally at `a450e43`. Eight assigned commands, each run at both revisions.

| # | command | base `e48354b` | tip `a450e43` |
|---|---|---|---|
| 1 | `python3 -B .ufo/waves/round-55/c55_readme_index.py --root $D --revision <rev>` | **exit 0**, `index_mismatches=0 knowledge_files=49 met=True`, `coverage_rows=51`, all seven components 0 | **exit 0**, `index_mismatches=0 knowledge_files=52 met=True`, `coverage_rows=54`, all seven components 0 |
| 2 | `python3 -B .ufo/waves/round-55/c55_readme_index.py --selftest` | **exit 0**, `44/44` | **exit 0**, `44/44` |
| 3 | `KAKE_R55_SELFTEST_REV=64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6 python3 -B .ufo/waves/round-55/c55_quote_truth.py --selftest` | **exit 0**, `54/54 (fixture revision 64c0ce12ffe3)` | **exit 0**, `54/54 (fixture revision 64c0ce12ffe3)` |
| 4 | `KAKE_R52_SELFTEST_REV=1ae8de5d4dee python3 -B .ufo/waves/round-52/c52_quote_truth.py --selftest` | **exit 0**, `18/18 (fixture revision 1ae8de5d4dee)` | **exit 0**, `18/18 (fixture revision 1ae8de5d4dee)` |
| 5 | `python3 -B .ufo/waves/round-52/c52_wave_ledger.py --selftest` | **exit 0**, `19/19` | **exit 0**, `19/19` |
| 6 | `python3 -B scripts/citation_lint.py --selftest` | **exit 0**, `9/9 passed` (all nine named checks PASS, incl. mutants E/F/G/H) | **exit 0**, `9/9 passed` |
| 7 | `python3 -B scripts/base_path_selftest.py` | **exit 0**, `45/45 fixtures passed` | **exit 0**, `45/45 fixtures passed` |
| 8 | `python3 -B .ufo/waves/round-55/c55_quote_truth.py --root $D --revision <rev>` | **exit 0**, `8/8 met=True` (C1–C8 all PASS) | **exit 1**, `6/8 met=False`; C1–C6 PASS, **C7_validate_before_append FAIL**, **C8_mirror_bytes FAIL** |

Two live (non-selftest) gates run on the same trees as extra regression surface, since a green selftest beside a red live
run would be exactly this seat's failure class:

| command | base `e48354b` | tip `a450e43` |
|---|---|---|
| `python3 -B scripts/citation_lint.py --root $D --revision <rev> --json <out>` | **exit 0**, `verdict clean`, `violations 0`, `adjudicated 31`, `population 2` | **exit 0**, `verdict clean`, `violations 0`, `adjudicated 31`, `population 2` |

Supporting facts read from the lane with read-only git: `SCORECARD.md` and `LOG.md` are unchanged between the two
revisions (`git diff --name-status` prints nothing), so gate 9's population is byte-identical and the 31 adjudications are
the same set.

## REGRESSIONS:

**None.** Every row that is green at `e48354b` is green at `a450e43` except row 8, which is the frozen-counter drift
below, not a regression of round-56's own surfaces. Nothing that was red at base became green by accident, and nothing
green at base went red for a reason the round-56 build did not declare.

Two positive (green-at-both, i.e. no-harm) results worth naming, because they are the load-bearing ones for the round-56
build:

- Row 1: the round-55 README coverage-map counter stays green across the three new knowledge files. Its predicate is
  revision-relative (`c55_readme_index.py:58-60`: base rev `fcaf4b85`, floor 46), and the round-56 build carried the
  coverage map with the tree: `corpus/knowledge/` 49 → 52 files and `coverage_rows` 51 → 54, with
  `unindexed=multi=thin=duplicate=head_changed=deleted=dangling=0` at the tip.
- Row 1's `head_changed=0` is corroborated independently: `git diff --name-status e48354b a450e43 -- corpus/knowledge
  corpus/lessons` shows three `A` (added) entries and no `M` — `corpus/knowledge/yahoo-japan-deleted-url-recrawl.md`,
  `corpus/knowledge/yahoo-japan-link-target-crawl-restriction.md`,
  `corpus/knowledge/yahoo-japan-nonexistent-url-recrawl.md`, plus `A corpus/lessons/round-56.md`. No existing entry was
  edited, so the append-only rule the round-55 counter encodes still holds on the knowledge tree.

## EXPECTED FROZEN-COUNTER DRIFT:

Row 8 is the only red-at-tip. It is the round-55 quote-truth counter, frozen for the round-55 append, and the failure is
structural rather than a defect of the round-56 tree.

Exact tip output of row 8:

```
C2 quote-truth 6/8 met=False  (met: conditions_passed == 8 of 8)
  C1_entries_exist PASS
  C2_entry_provenance PASS
  C3_row_shape PASS
  C4_used_by PASS
  C5_quote_truth PASS
  C6_receipt_pins PASS
  C7_validate_before_append FAIL
    - validated scratch registry is not byte-equal to the landed registry
  C8_mirror_bytes FAIL
    - registry rows 158 != mirror rows 155 + 1
    - append-only: measured registry minus new rows, used-by restored, != mirror bytes
  revision: a450e43e696d032e3ac308383f6b3394e0c92860
```

Why it fails, by pinned constant, not by guess (`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-55/c55_quote_truth.py`):

- `:74` `BASE_REV = "fcaf4b85ce32…"` (the round-55 base, not round-56's), `:94` `NEW_ROWS = ("S418",)`, `:95`
  `PRIOR_USED_BY = {"S372": …, "S373": …}`; `.ufo/waves/round-55/assimilation/mirror-pin.json:6` `"rows": 155`.
- C8 row count, `:513-514`: registry at tip has 158 rows (base 156 + the two rows this round appends), the counter
  expects `mirror rows 155 + 1 = 156` → mismatch.
- C8 append-only bytes, `:526-528`: the restore loop rewrites `used-by` only for `PRIOR_USED_BY` ids, so S367's
  round-56 `used-by` extension survives the restore and the byte comparison against the round-55 mirror fails.
- C7, `:477`: the round-55 validated scratch registry (`assimilation/validate/corpus/SOURCES.md`, 156 rows, S367 at its
  base `used-by`) is compared byte-for-byte to the landed registry (158 rows, S367 extended) → mismatch.

The registry delta that produces all three messages, measured row-by-row
(`git diff e48354b a450e43 -- corpus/SOURCES.md`, plus a row-map diff of the `## Registry` table):

- rows 156 → 158; added `S419`, `S420`; removed none; changed ids: `S367` only; the only differing cell is index 10
  (`used-by`), base `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md` → that path plus
  `corpus/knowledge/yahoo-japan-link-target-crawl-restriction.md`. This independently corroborates the contract's C2
  after-state clause that S367 differs from its base row in `used-by` only; it is not a judgment on C2.

Attribution experiments, run in two further private clones (commits made only inside those `mktemp -d` clones with
`-c user.name=selftest -c user.email=selftest@local`), to prove the drift is exactly the registry delta and to split it
between the two edits:

| fixture (clone at `a450e43` + one change) | row-8 result |
|---|---|
| `$E`: only `corpus/SOURCES.md` replaced by the round-56 pre-append mirror bytes (`sha256 cc402e4b559528170fe71ba09b6ad3be663a8f9d5ce9f36caeaed5ea45e6c50e`, byte-equal to the registry at `e48354b`); synthetic rev `04bc38481932a8be9268df64354dd77d57eb675d` | **exit 0, 8/8 met=True** (C1–C8 PASS) — the whole tip tree minus the registry delta is green under the round-55 counter |
| `$F`: only the `S419`/`S420` row lines deleted, S367 `used-by` extension kept; synthetic rev `ac0dbf3cdcd3407acb86a15fe08bc47f9635abb6` | **exit 1, 6/8**; C8 loses the row-count message (`156 == 155+1` holds) and keeps only the append-only message; C7 still FAIL — so the S367 `used-by` extension alone is sufficient to red the counter |

Conclusion for the L1: row 8's red is a frozen-counter property (its mirror, `NEW_ROWS` and validated scratch registry
are round-55 constants; any later registry append necessarily reds it), not a round-56 regression. The applicable
round-56 predicate is `c56_quote_truth.py`'s `met: conditions_passed == 8 of 8` with the round-56 mirror and `NEW_ROWS`;
its live measurement belongs to other seats and was **not** run here. No action is proposed for this wave beyond
reporting; re-pinning `c55_quote_truth` is not in scope and would falsify a frozen round-55 receipt.

Unrun by this seat (reported as unrun, not as pass): `c56_selftally.py`, `c56_quote_truth.py`, `sources-census.sh
validate`, `scripts/landed_check.py`, and any round-52 live counter. No credential material, session token or private URL
appears in this report.

VERDICT: No regression: 7 of 8 assigned checks green at both revisions (identical script blobs), and the single red-at-tip is the round-55 quote-truth counter's frozen round-55 pinning (158 vs 155+1 rows, S367 used-by unrestored), proven by reverting the registry delta alone, which restores 8/8.
