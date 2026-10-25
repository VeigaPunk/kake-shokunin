# MutC2Counter
ATTACKS: .ufo/waves/round-55/c55_quote_truth.py --selftest (47 fixtures + 3 unit checks) at a7a548e102b71bd16b0a6ddafa469393a2c98b69

## METHOD
- Scratch: `git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kake-shokunin /tmp/mutc2.o3VO5J`; `git -C /tmp/mutc2.o3VO5J rev-parse --show-toplevel` → `/tmp/mutc2.o3VO5J` (verified). Clone HEAD was `78963ae…` (worktree had moved), so the counter was pinned to committed bytes: `git -C /tmp/mutc2.o3VO5J show a7a548e…:.ufo/waves/round-55/c55_quote_truth.py > .ufo/waves/round-55/c55_quote_truth.py`; file sha256 == `git show | sha256sum` == `300fb426f9d4cfcde93b7c18d50adef66a65fe33908f039582db1f0ce8813ce5` (observed equal).
- Baseline: `cd /tmp/mutc2.o3VO5J && KAKE_R55_SELFTEST_REV=a7a548e… python3 -B .ufo/waves/round-55/c55_quote_truth.py --selftest` → `c55 quote-truth selftest: 50/50 (fixture revision a7a548e102b7)`, rc=0, 2.6 s. Detector valid on pristine bytes.
- 52 single-point mutants (floor was 18): each = one exact-string replacement (count==1 asserted on pristine bytes), `py_compile` gate, then the same selftest command from inside the scratch; pristine bytes restored + sha256 re-verified after every run (all restores clean).
- Mutant validity disclosure: first forms of S02/S04/S07 replaced 2–3-line blocks and broke indentation (IndentationError, rc=1, empty stdout) — discarded as invalid, re-run as corrected single-line mutants; all verdicts below come from compiling mutants.
- Kill-fixture protocol: fixture inserted before the `unit_checks = {` anchor of `selftest()`; valid iff pristine+fixture → selftest rc=0 (no false alarm); kills iff mutant+fixture → rc=1. Harness-level survivors (S39/S42/S43) killed via sandbox drivers building the required git shape (throwaway `selftest` identity inside the scratch only).
- No tool installs (system python3 3.14.8 + git only); no pacman; no lane git-state commands.

## MUTANTS
|id|site|single-point mutation|result|killer (observed)|
|---|---|---|---|---|
|K01|C1|drop `add("C1_entries_exist",…)`|SURVIVED/unkillable|C2 shadows (att: 1/1)|
|K02|C2|drop `add("C2_entry_provenance",…)`|KILLED|mutc2_hdr_keyless (new)|
|K03|C3|drop `add("C3_row_shape",…)`|KILLED|mutc2_att_opened_shifted (new)|
|K04|C4|drop `add("C4_used_by",…)`|KILLED|mutc2_usedby_short (new)|
|K05|C5|drop `add("C5_quote_truth",…)`|KILLED|fail_body_swapped|
|K06|C6|drop `add("C6_receipt_pins",…)`|KILLED|fail_receipt_offset_nonutc|
|K07|C7|drop `add("C7_validate_before_append",…)`|KILLED|fail_census_forged_shape|
|K08|C8|drop `add("C8_mirror_bytes",…)`|KILLED|fail_mirror_contaminated|
|S01|C1|drop existence-append inside C1 loop|SURVIVED/unkillable|C2 shadows (att: 1/1)|
|S02|C2|header-keys loop → `for key in ():`|KILLED|mutc2_hdr_keyless (new)|
|S04|C2|cite-below-header check → `if False:`|KILLED|mutc2_cite_below_only (new)|
|S05|C3|11-cell check → `if False:`|SURVIVED/unkillable|C4 `len<11` guard (att: 0/0)|
|S06|C3|status `!= "mined"` → `==`|KILLED|pass (baseline)|
|S07|C3|row-URL check → `if False:`|SURVIVED/unkillable|C6 receipt-vs-row URL (att: 0/0)|
|S08|C3|held-row `row[:10]!=base[:10]` → `elif False:`|SURVIVED/unkillable|C8 restored-bytes (att: 0/0)|
|S09|C3|held-row `!=` → `==`|KILLED|pass (baseline)|
|S10|C4|`if got != want:` → `if False:`|KILLED|mutc2_usedby_short (new)|
|S11|C4|order-insensitive `sorted(got)!=sorted(want)`|KILLED|mutc2_usedby_reordered (new)|
|S12|C5|Gate range `<=UNIT_CEILING` → `<=40`|SURVIVED/unkillable|verify() ceiling (att: 0/0)|
|S13|C5|entry ceiling `u > UNIT_CEILING` → `u > 40`|KILLED|mutc2_entry_26u (new)|
|S14|C5|Gate page-unique check → `if False:`|KILLED|mutc2_gate_shared_quote (new)|
|S15|C5|entry page-unique gate → `if True:`|KILLED|mutc2_unique_two_plus_shared (new)|
|S16|in_content|`h2 = text.find("<h2")` → `h2 = 0`|KILLED|mutc2_precontent_only_quote (new)|
|S17|C5|Gate-line curly check → `if False:`|KILLED|mutc2_gate_curly_tail (new)|
|S18|C5|entry-line curly check → `if False:`|KILLED|mutc2_entry_curly (new)|
|S19|C5|`MIN_UNIQUE_SPANS = 3` → `0`|KILLED|mutc2_unique_exactly_two (new)|
|S20|C5|title-in-body check → `if False:`|KILLED|mutc2_title_stripped (new)|
|S21|C5|URL-field-in-body check → `if False:`|KILLED|mutc2_urlfield_stripped (new)|
|S22|C5|Gate-URL check → `if False:`|KILLED|mutc2_gate_url_swapped (new)|
|S23|C5|Gate-date check → `if False:`|KILLED|fail_lesson_no_date|
|S24|C6|receipt sha check → `if False:`|KILLED|fail_receipt_sha|
|S25|C6|receipt bytes check → `if False:`|KILLED|mutc2_receipt_bytes_off (new)|
|S26|C6|drop `isinstance(status, bool)` guard|SURVIVED/equivalent|`True != 200` still flags|
|S27|C6|drop UTC-suffix clause on fetchedAt|KILLED|fail_receipt_offset_nonutc|
|S28|C6|receipt-URL check → `elif False:`|KILLED|fail_receipt_url|
|S29|C7|`--file` presence → `if False:`|KILLED|mutc2_argv_no_file_flag (crash: exit 2)|
|S30|C7|`--root` rejection → `elif False:`|KILLED|mutc2_argv_root_plus_file (new)|
|S31|C7|sources-census.sh token check → `if False:`|KILLED|mutc2_argv_not_census (new)|
|S32|C7|exit check → `if False:`|KILLED|fail_validate_exit|
|S33|C7|E03/E04 scan → `for code in ():`|KILLED|mutc2_e04_midstream (new)|
|S34|C7|stdout tail-shape check → `if False:`|KILLED|fail_census_forged_shape|
|S35|C7|registry compare → adopted-rows-only|KILLED|fail_validated_doc_differs|
|S36|C7|scratch-entry equality → `if False:`|KILLED|fail_validated_entry_differs|
|S37|show_bytes|`git show` → worktree read|KILLED|pass (baseline: base_rev read returns tip bytes)|
|S38|C8|mirror==base check → `if False:`|KILLED|mutc2_att_mirror_usedby (new)|
|S39|C8|pin sha check → `if False:`|KILLED|DRV-B′ (pin points at add-blob)|
|S40|C8|pin rows check → `if False:`|KILLED|mutc2_pin_rows_plus1 (new)|
|S41|C8|`merge-base --is-ancestor` → `if False:`|SURVIVED/tautology|DRV-D demo: all rc=0|
|S42|C8|`add_commit == rev` → `if False:`|KILLED|DRV-A (mirror in tip batch)|
|S43|C8|add-blob hash → `elif False:`|KILLED|DRV-B (blob ≠ tip mirror)|
|S44|C8|restored-bytes check → `if False:`|KILLED|mutc2_append_only_cell_edit (new)|
|S46|C8|trailing-newline clause dropped|KILLED|mutc2_landed_no_trailing_nl (new)|

## SURVIVORS
37 mutants survived the stock selftest; 29 were then killed by new fixtures (table above). 8 remain unkillable — each is a coverage finding, contract unchanged:
- K01, S01 (C1 existence): C2's `entry absent` note fires for any absent entry. Attempt mutc2_att_entry_gone (delete S373 entry + its validate copy): pristine rc=1, K01 rc=1, S01 rc=1 — no flip. C1 is redundant with C2.
- S05 (11-cell check): any <11-cell row also trips C4's `len(row) < 11` guard. Attempt mutc2_att_row_ten_cells (10-cell S418 row, validate synced): pristine rc=0, mutant rc=0 (both flag). Redundant with the C4 guard.
- S07 (row-URL): C6 compares `receipt.url` with the row's own URL. Attempt mutc2_att_row_url_shifted: pristine rc=0, mutant rc=0. Redundant with C6.
- S08 (held-row cells 0–9): C8's restored-bytes check compares those cells against the mirror. Attempt mutc2_att_held_cell_edited: pristine rc=0, mutant rc=0. Redundant with C8.
- S12 (Gate range upper bound): `verify()`'s `u > UNIT_CEILING` ceiling also applies to Gate quotes, and the `units(q) >= 6` filter shadows the lower bound. Attempt mutc2_gate_26u (26-unit Gate quote): pristine rc=0, mutant rc=0 (both flag via ceiling). Redundant with verify().
- S26 (bool guard): with the guard dropped, `True != 200` still flags; fail_receipt_status_bool passes under the mutant (matrix rc=0). Equivalent mutant.
- S41 (is-ancestor): `git log <rev> -- <path>` output is reachable from `<rev>` by definition, so `merge-base --is-ancestor` cannot fail in a healthy repo. DRV-D demo: 3 sandbox commits, is-ancestor rc=0 for each. Strictness lives in `add_commit == rev` (S42, killable).

## KILL FIXTURES
All proven: pristine+fixture → selftest rc=0; mutant+fixture → rc=1 (drivers compare `run_checks` exit: pristine 1 / mutant 0).
1. mutc2_hdr_keyless — delete S418 `verified-at:` line, sync validate copy — K02, S02
2. mutc2_cite_below_only — rewrite below-header `S372` cites to `S937`, header kept, sync — S04
3. mutc2_usedby_short — S373 used-by → entry path only, sync VALIDATE_REG — K04, S10
4. mutc2_usedby_reordered — S373 used-by reversed (entry, NOFOLLOW, BAIDU), sync — S11
5. mutc2_att_opened_shifted — S418 opened 2026-10-25→2026-10-24, sync — K03
6. mutc2_entry_26u — append 26-unit in-content unique span to S418 entry, sync — S13
7. mutc2_gate_shared_quote — append S372's Gate quote into S373+S418 bodies, receipts re-pinned — S14
8. mutc2_unique_two_plus_shared — strip S372 entry quotes; 2 unique + 1 shared span, sync — S15
9. mutc2_precontent_only_quote — move S372 Gate quote into a `<head>` comment, receipts re-pinned — S16
10. mutc2_gate_curly_tail — append curly-quoted text to S372 Gate line — S17
11. mutc2_entry_curly — append curly-quoted line to S373 entry, sync — S18
12. mutc2_unique_exactly_two — strip S372 entry quotes; exactly 2 unique spans, sync — S19
13. mutc2_title_stripped — remove all `robots.txtとは？` from S418 body, receipts re-pinned — S20
14. mutc2_urlfield_stripped — replace S418 `value="…002885…"` field, receipts re-pinned — S21
15. mutc2_gate_url_swapped — S418 Gate-line URL 002885→002886 — S22
16. mutc2_receipt_bytes_off — S373 receipt bytes += 1 — S25
17. mutc2_argv_no_file_flag — argv without `--file` — S29 (mutant exits 2: `tokens.index("--file")` ValueError)
18. mutc2_argv_root_plus_file — argv carrying both `--root` and `--file` — S30
19. mutc2_argv_not_census — argv without sources-census.sh — S31
20. mutc2_e04_midstream — E04 line inserted before the final `file<TAB>ok` line — S33
21. mutc2_pin_rows_plus1 — mirror-pin rows 155→156 — S40
22. mutc2_append_only_cell_edit — S263 row cell edited (row regex preserved), sync — S44
23. mutc2_landed_no_trailing_nl — landed registry + validate copy without trailing newline — S46
24. DRV-A — mirror committed in the tip batch (add-commit == measured rev) — S42
25. DRV-B — add-commit blob ≠ tip mirror bytes — S43
26. DRV-B′ — pin sha256 points at the add-commit blob — S39
Failed attempt recorded: mutc2_gate_26u did not kill S12 (pristine rc=0, mutant rc=0 — see SURVIVORS).

## RESTORATION
- After every mutant and at the end: sha256(scratch counter) == `300fb426f9d4cfcde93b7c18d50adef66a65fe33908f039582db1f0ce8813ce5` (asserted per run; final check observed True).
- Lane repo: only `git show`/`clone` reads; no add/commit/stash/checkout/reset/pull/push; no jj commands. The only lane path written by this seat is this report file.
- Scratch `/tmp/mutc2.o3VO5J` holds restored pristine bytes only; disposable.

VERDICT: 52 mutants — 44 killed (15 by existing fixtures, 29 by new proven fixtures incl. 3 harness drivers), 8 unkillable survivors are redundant/shadowed checks (C1⊂C2, C3-cells⊂C4/C8, C3-URL⊂C6, Gate-range⊂verify-ceiling, bool-guard equivalent, is-ancestor tautology) — detector coverage findings, contract unchanged.
