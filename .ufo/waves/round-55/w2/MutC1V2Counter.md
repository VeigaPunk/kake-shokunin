# MutC1V2Counter
ATTACKS: .ufo/waves/round-55/c55_readme_index.py @ a7a548e102b71bd16b0a6ddafa469393a2c98b69 (version 2) and its `--selftest` (35 fixtures)

## Method (commands + observed outputs)
- Target bytes: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show a7a548e...:.ufo/waves/round-55/c55_readme_index.py` → 398 lines. Scratch copy: `git -C <lane> archive a7a548e... .ufo/waves/round-55/c55_readme_index.py | tar -x -C $D/wt`; pristine sha256 `0ffb8d31cfe5e1483a19a7913321ff6ee0af8ee12280d529d4b6e10d4ace5091`.
- Baseline detector: `python3 /tmp/mutc1v2.nqtWyj/pristine.py --selftest` → `c55 readme-index selftest: 35/35`, rc=0 (observed). Detector green before any mutant ran.
- Each mutant = exact single-occurrence string replacement in a scratch copy (`count == 1` asserted by the driver; no repo file touched), then `python3 <mutant>.py --selftest`, rc + stdout recorded. Driver: `/tmp/mutc1v2.nqtWyj/driver.py`.
- Result: 22 mutants → 18 KILLED, 4 SURVIVED; all 4 survivors killed by new fixtures below.

## MUTANTS:
| id | single-point change | observed `--selftest` | verdict |
|---|---|---|---|
| M01 | `FLOOR = 46` → `45` | 34/35 rc1; `FAIL fail_floor_literal: expected 1, got 0` | KILLED (exit) |
| M02 | drop `- common` in `shared = ...` | 34/35 rc1; `FAIL fail_common_words_only: expected 1, got 0` | KILLED (exit+fact thin) |
| M03 | `MAX_FILES_PER_ROW = 2` → `99` | 34/35 rc1; `FAIL fail_mega_row: fact multi expected 1, got 0` | KILLED (facts only; exit still 1 via thin) |
| M04 | drop `elif lines: break` (first-table rule) | 34/35 rc1; `FAIL fail_second_table_does_not_index: expected 1, got 0` | KILLED (exit) |
| M05 | `deleted = [...]` → `[]` | 35/35 rc0 | SURVIVED |
| M06 | `if not new.startswith(old[:1500]):` → `if False:` | 34/35 rc1; `FAIL fail_head_edited_to_fit: expected 1, got 0` | KILLED (exit+fact) |
| M07 | `if key in seen:` → `if False:` | 34/35 rc1; `FAIL fail_duplicate_cell: fact duplicate expected 1, got 0` | KILLED (facts only; exit still 1 via thin) |
| M08 | `len(row["cov"].split()) < 5` → `< 4` | 35/35 rc0 | SURVIVED |
| M09 | `show()` reads `open(root/path)` instead of `git show` | 33/35 rc1; `FAIL fail_head_edited_to_fit: expected 1, got 0`; `FAIL pass_head_only_committed_bytes: expected 0, got 1 {'thin': ['e1.md']}` | KILLED (exit) |
| M10 | `if name in PROTOCOL_NAMES or not has_ext:` → `if not has_ext:` | 34/35 rc1; `FAIL pass_protocol_name_exempt: expected 0, got 1 {'dangling': ['robots.txt', 'security.txt']}` | KILLED (exit) |
| M11 | `know` excludes paths containing `/` | 34/35 rc1; `FAIL fail_nested_unindexed: expected 1, got 0` | KILLED (exit+facts) |
| M12 | header lookup removed (`e_idx = 1; c_idx = -1`) | 34/35 rc1; `FAIL pass_columns_by_header: expected 0, got 1 {'unindexed': [all 46 e-files], 'duplicate': ['S900' ×45]}` | KILLED (exit) |
| M13 | remove `if len(sections) != 1: return 2` guard | rc1, no stdout; stderr: `IndexError: list index out of range` at `section = sections[0]` (case fail_no_section) | KILLED (crash: exit-2 contract lost) |
| M14 | drop `len(multi)` from `mismatches` sum | 35/35 rc0 | SURVIVED |
| M15 | drop `len(duplicate)` from `mismatches` sum | 35/35 rc0 | SURVIVED |
| M16 | drop `len(unindexed)` from sum | 30/35 rc1; 5 FAILs incl `FAIL fail_unindexed: expected 1, got 0 {'unindexed': ['e0.md']}` | KILLED (exit) |
| M17 | drop `len(dangling)` from sum | 31/35 rc1; 4 FAILs incl `FAIL fail_dangling_md: expected 1, got 0 {'dangling': ['knowledge/nope.md']}` | KILLED (exit) |
| M18 | drop `len(thin)` from sum | 29/35 rc1; 6 FAILs incl `FAIL fail_swap_population: expected 1, got 0 {'thin': ['stub0.md'..'stub9.md']}` | KILLED (exit) |
| M19 | drop `(?!\.[A-Za-z0-9])` lookahead from REF_RE | 34/35 rc1; `FAIL fail_prefix_name: expected 1, got 0` | KILLED (exit) |
| M20 | `len(know) >= FLOOR` → `>` | 24/35 rc1; all 11 `pass*` cases `expected 0, got 1` | KILLED (exit) |
| M21 | `MAX_FILES_PER_ROW = 2` → `1` | 34/35 rc1; `FAIL pass_two_files_one_row: expected 0, got 1 {'multi': [...]}` | KILLED (exit) |
| M22 | `new.startswith(old[:1500])` → `new != old` | 34/35 rc1; `FAIL pass_entry_appended_correction: expected 0, got 1 {'head_changed': ['e1.md']}` | KILLED (exit+fact) |

## SURVIVORS:
- **M05 `deleted` dropped.** Root cause observed, not inferred: `_fixture()` commits every knowledge file of `files` at base and the tip commit only adds, so no fixture can express a base→tip deletion — `deleted` is `[]` in all 35 fixtures (first pristine-harness run confirmed: `fact deleted expected 1, got 0` even with a base-only extra file, because `git add -A` resurrects it). `fail_swap_population`'s exit 1 comes from thin, not deleted (M18 output lists `stub0..stub9` thin).
- **M08 `< 5` → `< 4`.** No fixture has a 4-token Coverage cell; the tested boundary values are 1 token (`fail_thin_short` "TBD") and 5 tokens (`pass_five_tokens`).
- **M14 `multi` out of sum.** `fail_mega_row`'s exit 1 is over-determined: the mega row's 45 non-matching files go thin, so exit stays 1 without `multi`; the case's facts assert only `len(multi) == 1` (detection intact). Sum contribution untested.
- **M15 `duplicate` out of sum.** Same masking: in `fail_duplicate_cell`, row a3/e3 is also thin (cov names Widget1/Widget2, head is Widget3 → no shared word beyond `common`), so exit stays 1; facts assert only `len(duplicate) == 1`.

## KILL FIXTURES:
Test-only harness extension applied identically to pristine and each mutant (`/tmp/mutc1v2.nqtWyj/driver2.py`): `gone` param on `_fixture`/`case` — files committed at base, then `os.remove`d before the tip commit (4 patches P1–P4; the `os.remove` is required because `commit()` runs `git add -A`; the un-removed first attempt was caught by the pristine check, `deleted expected 1, got 0` on pristine).

1. `kill_m05_deleted` — base gets extra `corpus/knowledge/zz-old.md`, absent at tip → tip know=46 (floor still met in mutant), base=47, `deleted=['zz-old.md']`; expect `1, {"deleted": 1}`. Mutant cannot reach exit 0.
2. `kill_m08_lt4` — row a1 Coverage `Widget1 cache invalidation rules` = 4 tokens, shared word `widget1` with e1's head beyond `common` → pristine: `4 < 5` → thin, exit 1; mutant: not thin → exit 0.
3. `kill_m15_dupsum` — rows a1(e1)/a2(e2) share Coverage `Widget1 and Widget2 cache invalidation rules described in full` (valid for both: shared {widget1}/{widget2}, 9 tokens) → pristine: duplicate=1, exit 1; mutant: mismatches=0, exit 0. Facts pin `duplicate:1, thin:0`.
4. `kill_m14_multisum` — row m Entry names `knowledge/e1.md` `knowledge/e2.md` `knowledge/e3.md` (3 refs > 2), Coverage `Widget1 Widget2 Widget3 cache invalidation rules described in full` valid for all three → pristine: multi=1, exit 1; mutant: exit 0. Facts pin `multi:1, thin:0`.

Observed runs (`python3 /tmp/mutc1v2.nqtWyj/kill.py --selftest`):
- pristine + harness + 4 cases → `c55 readme-index selftest: 39/39`, rc=0 (fixtures kill nothing on pristine).
- M05 + fixtures → 38/39 rc1: `FAIL kill_m05_deleted: expected 1, got 0` — KILLED.
- M08 + fixtures → 38/39 rc1: `FAIL kill_m08_lt4: expected 1, got 0` — KILLED.
- M15 + fixtures → 38/39 rc1: `FAIL kill_m15_dupsum: expected 1, got 0 {'duplicate': [...]}` — KILLED.
- M14 + fixtures → 38/39 rc1: `FAIL kill_m14_multisum: expected 1, got 0 {'multi': [...]}` — KILLED.
Each mutant failed exactly its own fixture; no cross-failures.

## Exit-code-equivalent mutants (facts a facts-asserting fixture pins)
- M07 and M03: case exit stays 1 (thin co-fires), killed only by existing facts assertions — pin `len(duplicate) == 1` / `len(multi) == 1`.
- M14/M15 (survivors): case-level exit AND asserted facts identical; pinned only by fixtures 3–4, which make the target term the sole mismatch so the exit itself flips 1→0.
- M13: crash changes the failure mode from clean exit 2 to rc=1 traceback; existing `fail_no_section` pins the exit-2 contract.
- M06/M11/M22: killed by exit and facts jointly; facts give attribution (`head_changed` / `unindexed`+`knowledge_files` / `head_changed`).

## Restoration and bounds
- Restoration: after both drivers, work-path sha256 `0ffb8d31cfe5e1483a19a7913321ff6ee0af8ee12280d529d4b6e10d4ace5091` == pristine (`RESTORE ... match=True`, observed in both driver runs).
- Lane access: read-only `git show`/`log`/`archive` only; scratch under `/tmp/mutc1v2.nqtWyj` (`mktemp -d`); fixture commits only inside selftest `mktemp` dirs; no lane write except this report; no `git add/commit/stash/checkout/reset` on the lane; no jj mutation; no subagents; no pacman (no installs needed).
VERDICT: 22 single-point mutants — 18 killed by the existing 35-fixture selftest, 4 survivors (deleted-term inexpressible by harness; `<5` boundary; multi/duplicate sum contributions masked by co-firing thin) all killed by 4 new fixtures with pristine 39/39 green.
