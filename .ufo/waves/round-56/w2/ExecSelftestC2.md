# ExecSelftestC2

Seat scope: attack the C2 selftest — `.ufo/waves/round-56/c56_quote_truth.py --selftest` (blob identical at
`a450e43` and lane tip; `git diff a450e43 -- …/c56_quote_truth.py` empty). All runs in my own clone
`/tmp/tmp.CxF0Ug6E2j` (`git clone --no-checkout` + checkout `a450e43e696d032e3ac308383f6b3394e0c92860`,
`rev-parse --show-toplevel` = that dir). Lane, index and jj untouched; instrumented/mutated copies live only
under `/tmp/probe56/`.

## RUNS:

| # | env | stdout tail | exit | wall |
|---|---|---|---|---|
| 1 | `KAKE_R56_SELFTEST_REV=a450e43e696d` | `c56 quote-truth selftest: 67/67 (fixture revision a450e43e696d)` | 0 | 3.33 s |
| 2 | `KAKE_R56_SELFTEST_REV=d5afc48acd72` | `… 67/67 (fixture revision d5afc48acd72)` | 0 | 3.05 s |
| 3 | no pin, cwd tip = `a450e43` | `… 67/67 (fixture revision a450e43e696d)` | 0 | 3.00 s |

Supplementary (same clone): `KAKE_R56_SELFTEST_REV=3691e9689a03` (the pin named in `SKILL.md:1254`) → 67/67,
exit 0, 3.08 s. Pin sensitivity: `REV=e48354b` (base, no round-56 evidence) → exit 2, 0.04 s,
`selftest: missing round-56 evidence corpus/lessons/round-56.md`; `REV=deadbeef` → exit 2,
`… corpus/SOURCES.md`; unpinned from non-git `/tmp` → exit 2, `… corpus/SOURCES.md`.

Hostile env (pin `a450e43`, each run from the clone):
- `TZ=Asia/Tokyo` → 67/67, exit 0. `LC_ALL=C LANG=C` → 67/67, exit 0. (UTC date checks are TZ-immune.)
- `GIT_CONFIG_GLOBAL` with `core.autocrlf=true` → **66/67, exit 1**, `FAIL fail_mirror_crlf: expected 1, got 0`
  (+ ~1.7 kl warning lines): `_build()` (line 593) commits fixture files without `-c core.autocrlf=false`, so
  git normalises the CRLF mutation back to LF and the fixture becomes a no-op.
- `GIT_CONFIG_GLOBAL` with `commit.gpgsign=true` → **uncaught `subprocess.CalledProcessError`**, exit 1 (not the
  documented 2), ~245 KB of output. `_build()` passes only `-c user.name/-c user.email`, never
  `-c commit.gpgsign=false`, so a host-level signing policy aborts the selftest instead of reporting.

## COUNT DERIVATION:

- `grep -c '@case('  .ufo/waves/round-56/c56_quote_truth.py` → **63**.
- Plus the undecorated `pass` baseline seeded at line 655 (`cases = {"pass": (variant(lambda f: None), 0)}`) →
  **64 fixtures**.
- Plus **3** unit checks (lines 913-915: halfwidth kana one-per-char, non-BMP CJK, latin tokens per word) →
  **67**.
- Counter's own denominator: `total = len(cases) + len(unit_checks)` (line 931). An instrumented run enumerated
  **64 case names** and 3 unit labels — independent agreement.
- `SKILL.md:1254` registry row ("67 checks: 64 sandbox-repo fixtures … plus 3 unit-rule checks"): **exact** in
  arithmetic. Two caveats: (a) "64 fixtures" is not reachable by counting `@case(` — it needs the undecorated
  `pass` baseline; (b) the pin the row names is `3691e9689a03`, while this wave's dispatch names `d5afc48` —
  both produce 67/67, so the row's claim survives either pin.

## FIXTURE -> CONDITION TABLE:

Format `fixture (observed failing checks)`. "Observed" comes from a patched copy that prints every failing
check per case (`/tmp/probe56/c56p.py`, same 67/67); "meant" is the grouping label read from the counter.

- **C1** (2): `fail_missing_entry` (C1+C2+C7); `fail_staged_name_survives` (C1)
- **C2** (4): `fail_no_source_header` (C2+C7); `fail_no_cite_below_header` (C2+C7); `fail_verified_at_wrong_date` (C2+C7); `fail_recheck_junk_cadence` (C2+C7)
- **C3** (5): `fail_row_short` (C3+C4+C7); `fail_new_row_wrong_url` (C3+C6+C7); `fail_held_row_cell_changed` (C3+C7+C8); `fail_new_row_junk_kind_tier` (C3+C7); `fail_new_row_already_in_base` (**C8 only**)
- **C4** (2): `fail_used_by_dropped_prior` (C3+C4+C5+C6+C7+C8); `fail_used_by_not_extended` (C4+C7)
- **C5** (22): `fail_lesson_quote` (C5); `fail_lesson_no_date` (C5); `fail_gate_first_quote_fabricated` (C5); `fail_gate_second_quote_not_unique` (C5); `fail_gate_quote_shared_with_sibling` (C5); `fail_body_swapped` (C5); `fail_held_body_edited` (C5); `fail_entry_quote` (C5+C7); `fail_entry_quote_over_ceiling` (C5+C7); `fail_boilerplate_quotes` (C5+C7); `fail_inference_line_fabricated` (C5+C7); `fail_header_fabricated_quote` (C5+C7); `fail_long_span_fabricated` (C5+C7); `fail_curly_quote` (C5+C7); `fail_anchor_heading_not_in_body` (C5+C7); `fail_short_span_fabricated` (C5+C7); `fail_entry_only_sibling_shared_spans` (C5+C7); `fail_entity_span_decoded` (C5+C7); `fail_long_single_token_fabricated` (C5+C7); `fail_char_ceiling_44_chars_25_units` (C5+C7); `fail_entry_only_spans_shared_with_unadopted_body` (C5+C7); `fail_empty_body` (C5+C6)
- **C6** (9): `fail_receipt_sha`, `fail_receipt_status`, `fail_receipt_status_bool`, `fail_receipt_stale_date`, `fail_receipt_url`, `fail_receipt_offset_stale`, `fail_receipt_offset_nonutc`, `fail_receipt_useragent_untagged` (all C6 only); `fail_bad_receipts` (C6 only, `unevaluable`, wants exit 2)
- **C7** (8): `fail_validate_exit`; `fail_validate_e04`; `fail_validate_root_argv`; `fail_validated_row_differs`; `fail_validated_entry_differs`; `fail_census_forged_shape`; `fail_census_wrong_file_argv`; `fail_validated_doc_differs` (all C7 only)
- **C8** (7): `fail_mirror_contaminated`; `fail_mirror_not_base`; `fail_pin_sha`; `fail_pin_empty`; `fail_pin_null`; `fail_mirror_crlf` (C8 only); `fail_not_append_only` (C7+C8)
- **C3+C8** (1): `fail_registry_row_dropped` (C3+C4+C5+C6+C7+C8)
- **expect-0 baselines** (4): `pass` (clean); `pass_gate_extra_short_quote` (clean); `pass_census_relative_argv` (clean); `pass_entity_span_raw` (clean)

Total 64. 40 of the 60 failing fixtures trip at least one check outside their intended condition — every C2,
C3 and C4 fixture is in that set.

## UNTRIPPED CONDITIONS:

**Top level:** no condition C1–C8 is untripped; each appears in at least one fixture's observed failure set.
**Net detection power is another matter** (mutation test: `add("Cx_…", [] and var)` in a `/tmp` copy, pin
`a450e43`):

| neutered check | selftest result | verdict |
|---|---|---|
| `C1_entries_exist` | 66/67 (`FAIL fail_staged_name_survives`) | detected |
| `C2_entry_provenance` | **67/67** | **undetected** |
| `C3_row_shape` | **67/67** | **undetected** |
| `C4_used_by` | **67/67** | **undetected** |
| `C5_quote_truth` | 60/67 | detected |
| `C6_receipt_pins` | 59/67 | detected |
| `C7_validate_before_append` | 59/67 | detected |
| `C8_mirror_bytes` | 60/67 | detected |

Cause: the harness compares only the exit code (`if code == want`, line 917) and most C2/C3/C4 fixtures mutate
the landed registry/entry without mirroring the change into `validate/`, so `C7_validate_before_append` fails as
collateral and the case still "passes". A regression that silently disables C2, C3 or C4 keeps the selftest at
67/67.

**Sub-condition branches that never fire** (23 `append` sites in `run_checks`, none reached by any fixture;
verified by absence from the instrumented note dump):
- C3: L290 escaped pipe; L292 `status != mined`; L296 registry `recheck` not ISO/NNd/on-release; L302 scope or
  teaches cell < 20 chars; L305 "already in the base registry"; L309 "no base-revision row".
- C5: L332 retained body absent; L337 body not UTF-8; L390 no `- SID ` Gate line; L393 curly quotes **in the
  Gate line** (only entry-level curly is tripped); L396 Gate line has no 6+ unit quote; L399 Gate quote outside
  6..25 units; L404 Gate line missing the URL.
- C6: L440 no receipt for an id; L443 no retained body to hash.
- C7: L474 incomplete validation receipt; L480 `--root` in argv (unreachable behind the `--file` branch at L476,
  which is what `fail_validate_root_argv` hits).
- C8: L528 "mirror bytes already carry the row"; L553 no commit adds the mirror; L557 add-commit not an
  ancestor; L559 add-commit == measured revision; L562 mirror blob unreadable at its add-commit; L568 mirror
  blob at its add-commit carries the row.

**Two fixtures are aimed at branches that cannot fire.** `fail_new_row_already_in_base` appends the S419 row to
the end of the base registry, and `fail_mirror_contaminated` appends the S420 row to the end of the mirror;
`parse_registry` (L124) and `row_lines` (L140) only count rows inside a `## Registry` section, so L305 and L528
are unreachable for those mutations. Both cases pass on C8 collateral ("mirror bytes differ from the
base-revision registry") — evidence that the intended C3/C8 sub-checks are not exercised at all.

**Risks:** (1) exit-code-only comparison hides collateral failures (above); (2) the sandbox `_build` is not
hermetic against host git config — `core.autocrlf=true` costs one case, `commit.gpgsign=true` crashes with a
traceback and exit 1 instead of 2; (3) 67/67 is reproducible under both named pins and under TZ/locale changes,
so the headline number itself is stable.

VERDICT: Selftest reproduces 67/67 exit 0 in all three mandated configurations (3.0–3.3 s), the "64 fixtures +
3 unit checks" arithmetic is exact, but C2, C3 and C4 have zero net detection power (neutering any of them
still yields 67/67) and 23 sub-condition branches — including the two the fixtures claim to target — never fire.
