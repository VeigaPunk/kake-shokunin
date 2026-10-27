# MutC3Counter

Mutation test of the round-57 C3 condition code (`c57_quote_truth.py` at base `044048597d62f3199494b63b36e90dd57825e350`, hash `959b12e94621d49658857b3b9f739ba86377b7f0493b1a7d3728ff9539a521a8`) using its own selftest (`--selftest`, `KAKE_R57_SELFTEST_REV=044048597d62f3199494b63b36e90dd57825e350`, run from a shared `git clone --shared` of the lane in scratch). Baseline: 120/120, exit 0, baseline conditions 8/8, 105 fixtures in the kill matrix.

Shared-code check: the condition code (C1..C8, `units`, `used_by`, `content_window`, `text_segments`, `in_content`, `CHAR_CEILING`, `TOPIC` compares) of `c58_quote_truth.py` (round-58, on disk in the lane) is identical to c57 except round constants, row/body dicts, `TOPIC` value, `ARTICLE_START/END` locators and the `round57`→`round58` receipt tag. Every mutation below therefore applies verbatim to the c58 code.

Tooling: no tools installed (python3/git stock; RULES.md read; no pacman).

## MUTANTS:
24 single-point mutants (mutant → one line in the pristine copy; sha256 = after-mutation file). Run in the same selftest harness; killed = selftest exit 1 (or crash), survived = exit 0 with 120/120.

| # | mutant | point mutated | sha256(12) | verdict |
|---|--------|---------------|------------|---------|
| M01 | units_drop_non_cjk | `units()`: drop non-CJK token term | 6a95aa4137b8 | killed (unit rule: latin tokens / long URL) |
| M02 | units_all_tokens_cjk | `units()`: `if not CJK_RE.search(t)` → `if True` | 86a6211ac84d | killed (unit rule: non-BMP / entity) |
| M03 | units_cjk_zero | `units()`: `len(CJK_RE.findall(text))` → `0` | bc1bcd6793f0 | killed (unit rule) |
| M04 | units_every_char_cjk | `units()`: `CJK_RE.findall(text)` → `re.findall(r".", text)` | 943590b069df6 | killed (fixture assert crashes selftest) |
| M05 | in_content_any_to_all | `in_content()`: `any` → `all` | aacd98f7c488 | killed (发布日期 / anchor-heading checks go red) |
| M06 | in_content_reversed | `in_content()`: `span in seg` → `seg in span` | 996d6eaa4dc6 | killed (content-block quotes go red) |
| M07 | segments_keep_style_script | `text_segments()`: style/script strip removed | 95a10ed316a3 | killed (fail_style_css_span goes green) |
| M08 | segments_tag_interiors | `text_segments()`: `>([^<>]+)(?=<)` → `<([^<>]+)>` | f30e4f3bcbbc | killed (article-block checks go red) |
| M09 | char_ceiling_400 | `CHAR_CEILING` 40 → 400 | 484cdc61c30a | killed (fail_m408_char_ceiling_41_chars goes green) |
| M10 | char_ceiling_10 | `CHAR_CEILING` 40 → 10 | 1ab89be877c0 | killed (normal quotes exceed 10 chars) |
| M11 | topic_empty | `TOPIC` "死链" → "" | 24e019b4f873 | killed (fail_gate_quote_off_topic goes green) |
| M12 | topic_dead_link_longer | `TOPIC` "死链" → "死链接" | 454c630ef37ca | killed (topic-carry fixtures go red) |
| M13 | c3_row_len_lt11 | C3: `len(row) != 11` → `len(row) < 11` | 2bc8cef30f80 | SURVIVED |
| M14 | c3_status_mined_or_queued | C3: `row[7] != "mined"` → `not in ("mined","queued")` | 90671c2c0bcf | SURVIVED |
| M15 | c4_used_by_order_insensitive | C4: `got != want` → `sorted(got) != sorted(want)` | e8dee0eac101 | masked (equivalent, see below) |
| M16 | c5_unit_ceiling_boundary | C5: `u > UNIT_CEILING` → `u >= UNIT_CEILING` | 49375c06474c | killed (pass_m408_char_ceiling_boundary_40 dies: 25-unit span) |
| M17 | c5_entry_unique_ge1 | C5: `text.count(span) == 1` → `>= 1` | 8df8bf6658fe | SURVIVED |
| M18 | c7_e03_dropped | C7: loop `("E03","E04")` → `("E04",)` | 4d9acae0c472 | SURVIVED |
| M19 | c7_exit_substring | C7: `exit_text.strip() != "exit=0"` → `"exit=0" not in exit_text` | 7e2e300ba0ff | SURVIVED |
| M20 | c8_pin_rows_lt | C8: `pin.get("rows") != len(mirror_rows)` → `<` | 41c7f6786e2d | SURVIVED |
| M21 | c8_registry_rows_lt | C8: `len(rows) != len(mirror_rows)+len(NEW_ROWS)` → `<` | ed893c67dc151 | SURVIVED |
| M22 | used_by_comma_only | `used_by()`: split `[,;]` → `[,]` | 0304456c3ef0 | masked (equivalent, see below) |
| M23 | used_by_keep_dash | `used_by()`: "—" exclusion removed | 5de0d2e5b808 | masked (equivalent, see below) |
| M24 | used_by_no_strip | `used_by()`: returned tokens not stripped | eff8245b5d3b | masked (equivalent, see below) |

Killed examples actually observed: M05 `C5_quote_truth: S421: the article block does not print 发布日期：2022-09-09 in a text node`; M07 `FAIL fail_style_css_span: expected 1 on C5_quote_truth, got 0`; M09 `FAIL fail_m408_char_ceiling_41_chars: expected 1 on C5_quote_truth, got 0`; M16 `FAIL pass_m408_char_ceiling_boundary_40: expected 0 on any condition, got 1`; M11 `FAIL fail_gate_quote_off_topic: expected 1 on C5_quote_truth, got 0`.

## SURVIVORS:
7 genuine holes (behavior-changing, undetected: selftest still 120/120, exit 0). All exist identically in c58.

- S1 (M13) C3: a registry row with 12+ cells (supernumerary pipe) is no longer flagged ("expected 11"). The `len(row) != 11` guard was the only check on the cell count.
- S2 (M14) C3: status `queued` is accepted as `mined`.
- S3 (M17) C5: an entry quote appearing more than once in its own body still counts as "page-unique" (`text.count(span) >= 1`), so duplicates can satisfy `MIN_UNIQUE_SPANS` and the topic-span requirement.
- S4 (M18) C7: an `E03` finding in census stdout is tolerated (only `E04` refused).
- S5 (M19) C7: the exit file only needs to *contain* `exit=0` (e.g. `exit=00` or trailing junk passes).
- S6 (M20) C8: pin `rows` larger than the actual mirror-row count is tolerated (`<` instead of `!=`), so a shrunk mirror passes.
- S7 (M21) C8: the measured registry may carry extra rows beyond mirror + new rows (`<` instead of `!=`).

Masked (behavior-changing but verdict-neutral under the current contract; NOT holes today — the C4 `want` list is always a singleton because `PRIOR_USED_BY={}` and `want = prior + [path]`, so order, separator and "—" parses can never change a verdict): M15, M22, M23, M24. The `used_by` parser is effectively untested beyond single-token parse; any of these becomes live the day a row has a multi-element used-by.

## PROPOSED FIXTURES:
Round-58 port fixtures (named for `c58_quote_truth.py`'s selftest; use the existing `dual()` helper wherever a landed file has a validated scratch twin, so the failure is the condition under test, not C7):

- S1 → `fail_new_row_extra_cell`: append a 12th cell (` | extra`) to S423's landed + validated registry row; want red on C3_row_shape, note "registry row has 12 cells, expected 11".
- S2 → `fail_new_row_status_queued`: dual-edit S423 row status `mined` → `queued`; want red on C3_row_shape, note "status 'queued'".
- S3 → `fail_entry_duplicate_unique_span`: `set_entry` S423 whose body quotes one real ≥6-unit page-unique span twice and no other unique span; want red on C5_quote_truth, note "< 3 page-unique quoted spans" (duplicates excluded).
- S4 → `fail_validate_e03`: append `file\tE03\tS423 …` to `census-stdout.txt`; want red on C7_validate_before_append, note "E03 finding".
- S5 → `fail_validate_exit_extra`: `census-exit.txt` = `exit=0\nspurious\n`; want red on C7, note "expected 'exit=0'".
- S6 → `fail_pin_rows_overstated`: pin `rows` = actual + 1; want red on C8_mirror_bytes, note "mirror rows … != pinned …".
- S7 → `fail_registry_extra_unstaged_row`: add an extra unrelated row (e.g. S999) to the landed registry only; want red on C8, note "registry rows … != mirror rows … + …".
- Masked group → unit checks for `used_by` in selftest's `unit_checks` (`used_by("a; b") == ["a","b"]`, `used_by("a, b") == ["a","b"]`, `used_by("—") == []`, `used_by(" a ") == ["a"]`), plus — if the round-58 port ever sets `PRIOR_USED_BY` — `fail_used_by_reversed` (used-by cell lists the prior uses + current path in reverse order; want red on C4_used_by).

No fixtures proposed for the killed mutants: the selftest already covers them.

VERDICT: 7 genuine survivors (C3 row-len/status, C5 duplicate-unique, C7 E03/exit-substring, C8 pin/registry-row comparisons) + 4 masked used_by/C4 equivalents; 7 fixtures + used_by unit checks proposed for the round-58 port.
