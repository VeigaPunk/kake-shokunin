# SimplifyScripts

YAGNI review of round 56's committed scripts (read-only; no lane file edited, no lane jj/Git state touched).
Measured revision: the attack revision `a450e43e696d032e3ac308383f6b3394e0c92860` (lane tip at wave dispatch), plus
`7ad7db51dfcff2eccea9f7f73726f2437b2ed8de` for the one file that exists only there (`make_spec_w2.py`, added by
`7ad7db5`). All runs in my own clones: `/tmp/simp-FHzEL6` (a450e43) and `/tmp/simp2-p4s3wd` (7ad7db5). No tool installed
(`pyflakes 4.0.3` already at `~/.local/bin/pyflakes`, python 3.14.8; `python3 -m pyflakes` is not available, the binary is).

Baselines (my clones, clean):
- C1 `python3 -B .ufo/waves/round-56/c56_selftally.py --root . --revision a450e43…` → `tally_mismatches=0 rows_checked=10 met=True`, exit 0, 26.2 s.
- C2 `python3 -B .ufo/waves/round-56/c56_quote_truth.py --root . --revision a450e43…` → `8/8 met=True`, exit 0, 0.07 s.
- Both identical at `7ad7db5` (revision line aside): C1 exit 0, C2 exit 0.

## DEAD CODE:

1. `c56_quote_truth.py:57` — `from datetime import datetime, timezone`: `timezone` is never read (pyflakes: `'datetime.timezone' imported but unused`; `parse_iso` at :205 only uses `datetime.fromisoformat`). Deleting it changes no counter output (proved, SAFE DELETIONS 1).
2. `derive_c56_quote_truth.py:8` — `import re, subprocess, sys`: `re` and `sys` are unused (pyflakes). The script only uses `subprocess.run` and `body.replace`.
3. `derive_c56_quote_truth.py:56,59` — `def sub(old, new, count=1)` with `body.replace(old, new, count) if count else body.replace(old, new)`: all seven call sites (:60, :62, :63, :81, :82, :83, :84) pass two arguments, so the `count` parameter and the `if count else` arm are unreachable. (The file is a deletion candidate anyway — REDUNDANT FILES 1.)
4. `make_spec_w2.py:156` — `f"YAGNI review of round 56's committed scripts: …{{…}}"`: the braces are escaped (`{{`/`}}`), so the string has no placeholder; the `f` prefix is inert (pyflakes: `f-string is missing placeholders`). One-character fix, no behaviour change.
5. **Negative result — constants:** every module-level constant in both counters is read by code. `c56_quote_truth.py` 27/27 constants and `c56_selftally.py` 11/11 have ≥2 occurrences (AST + occurrence count), and each maps to a live condition: `UNIT_CEILING`/`CHAR_CEILING`/`MIN_UNIQUE_SPANS`/`CURLY`/`HELD_BODY_SHA256`/`STAGED_ABSENT`/`ROW_KINDS` → C5, `NEW_ROWS`/`ROW_URL` → C3/C5/C6, `PRIOR_USED_BY`/`NOFOLLOW` → C4/C8, `MIRROR_PIN`/`VALIDATE*` → C7/C8, `POP`/`TALLY_RES`/`PIN_RX`/`TIMEOUT`/`EXPECTED_ROWS` → the C1 measure loop. `landed_check.py`'s six constants (:50-58) are all read. No constant is dead.
6. **Negative result — functions:** no module-level function in `c56_selftally.py` (22 defs), `c56_quote_truth.py` (30), `span_tools.py` (6), `landed_check.py` (35), `make_spec_w1.py`/`make_spec_w2.py` is uncalled; pyflakes reports no other unused import. The two counters are not carrying a dead condition block — each `add("C…")` is reached in `run_checks` and each is exercised by ≥1 selftest fixture.

## REDUNDANT FILES:

1. `derive_c56_quote_truth.py` — **stale generator; still runs, does not reproduce the committed counter.** Run from `/tmp/der1`: exit 0, writes `c56_quote_truth.py` (28 862 B, 0 `@case(`). That output is byte-equal to `git show 2d308e8:.ufo/waves/round-56/c56_quote_truth.py` (v1) and differs from the committed file (45.7 KB, 63 `@case(`) by 427 diff lines. Re-running it today would silently revert version 2.1 (Gate uniqueness, 40-char ceiling, `verified-at`/`recheck` checks) and the whole 67-check selftest. Its only value is reproducing v1, which git already holds at `2d308e8`. It still resolves its round-55 source (`e48354b7:.ufo/waves/round-55/c55_quote_truth.py`) — the bytes exist.
2. `derive_c56_selftest.py` — **stale generator; still runs, regresses the committed counter.** Run from `/tmp/der2` on the committed file: exit 0, 47-line diff, `@case(` count 63 → 55 (drops 8 v2 fixtures, e.g. `fail_held_body_edited`, `fail_char_ceiling_44_chars_25_units`, `fail_staged_name_survives`, `fail_verified_at_wrong_date`). Its output equals no committed revision (`3691e96`, `a450e43`: no); applied to the v1 file (`/tmp/der3`) it also equals none (`d5afc48` differs by 95 lines). The contract calls the selftest "generated" by it, but the shipped 67-check block is not its output — re-running it now would falsify `SKILL.md:1254`'s "67 checks" claim.
3. `make_spec_w1.py`, `make_spec_w2.py` — **redundant but reproducible** (contra the "no longer reproducible" hypothesis). Run from `/tmp/sp1`, `/tmp/sp2`: exit 0, `w1-spec.json` (43 seats) and `w2-spec.json` (41 seats) are **byte-equal** (`cmp`) to the committed files. They read no repo bytes (only `json.dump` to their own directory). The two files share the `LANE`/`W`/`add()` scaffolding and the lane-bounds `CONTEXT` boilerplate (0.54 char-level similarity; not a verbatim copy). Their output is already committed and no counter reads them; keep for provenance or drop at round close — counter-neutral either way (SAFE DELETIONS 3).
4. `span_tools.py` — **duplicated logic, drifted copy.** `units()` (:24), `window()` (:29), `in_content()` (:34) and the CJK regex (:18) are copies of `c56_quote_truth.py:160,165,174,97` (identical regex; identical unit rule), and the drafting ceiling `6 <= units(piece) <= 25` is hardcoded at `:69` instead of reading `UNIT_CEILING`. The copy has drifted: `window()`/`in_content()` have no `None` guard, so a body without the `<h2 … 個別リンクURL` block raises `TypeError` where the counter returns `False`. `SRC` (:16) hardcodes the live lane's absolute path, so the helper reads the lane, not the caller's clone. It is cited by ≥12 W1 reports as the check they ran (`w1/EntryLinkTarget.md:7`, `w1/EntryNonexistentUrl.md:116`, `w1/ReviewerStaged.md:7`, …), so deleting it during the round orphans those citations — keep until settlement, then drop.
5. `validate_append.sh` — not read by any counter (C7 reads its receipts, not the script), but `SKILL.md:1260` names it as the C7 regeneration path, so it is live documentation. Two sharp edges worth recording: it hardcodes `LANE` (cannot run against a clone) and `rm -rf`s the committed `assimilation/validate/` before regenerating.
6. `controls/base-c1-selftally.txt` vs `controls/base-c1-selftally-v2.txt` — **byte-identical** (`cmp`, no output). Two receipt files for one state; both are cited by `contract.md` §Counter versions, so keep, but the pair records no difference: C1 v1 and v2 print the same base control.

## SAFE DELETIONS: (proved)

Each proof is a commit **inside my own clone** with `-c user.name=selftest -c user.email=selftest@local`, then both counters at the new revision; "identical" means stdout equal to the baseline with only the `revision:` line masked.

1. **`c56_quote_truth.py:57` → `from datetime import datetime`.** Clone `/tmp/simp-FHzEL6`, commit `ada7eef` ("probe: drop unused timezone import"): C2 exit 0, output identical; C1 exit 0, output identical (`tally_mismatches=0 rows_checked=10 met=True`).
2. **`derive_c56_quote_truth.py`, `derive_c56_selftest.py` (whole files).** Same clone, commit `e1451a4` deletes both plus `span_tools.py`, `make_spec_w1.py`, `validate_append.sh`: C1 exit 0, output identical (26.5 s); C2 exit 0, output identical; `KAKE_R56_SELFTEST_REV=e1451a4… python3 -B …/c56_quote_truth.py --selftest` → `67/67`, exit 0. No counter, no selftest and no pinned helper reads either file.
   Cost of the deletion (not free): two prose references dangle — `c56_quote_truth.py:5` ("`derive_c56_selftest.py`") and `:9` / `contract.md:54` ("generated by `derive_c56_quote_truth.py`"). The L1 would need one edit naming `2d308e8`/`d5afc48` instead. This is why I propose rather than perform.
3. **`make_spec_w2.py` (whole file).** Clone `/tmp/simp2-p4s3wd` at `7ad7db5`; baseline C1/C2 equal the a450e43 outputs (revision line aside); commit `5e44791` deletes it: C1 exit 0, identical; C2 exit 0, identical. `make_spec_w1.py` is covered by proof 2 (same clone/commit). Recommendation: keep both — they are the only re-derivation path for the seat prompts and they regenerate byte-exactly.

Not proved, therefore not claimed: deleting `span_tools.py` and `validate_append.sh` is counter-neutral (proof 2 covers both), but I do **not** recommend it before settlement (REDUNDANT FILES 4, 5).

## KEEP:

- `c56_selftally.py` (507 lines) and `c56_quote_truth.py` (979 lines) — no dead condition, no dead constant, pyflakes-clean except the one import above; each is a single self-contained file by design, because C1 pins a script **and every `*.py` beside it** to its base blob (`c56_selftally.py:216-224`). Factoring the shared helpers (`units`/`in_content`/`table parsing`) into a common module would put them outside the pinned directory — the disclosed v2 limit in `contract.md` ("a helper outside the pinned script's directory is not pinned") — so the duplication between the counters is load-bearing, not YAGNI debt.
- `--json` in both counters (`c56_selftally.py:484`, `c56_quote_truth.py:946`): live consumers this wave — `w1/ExecBaseControls.md:127,131` parse it, `w2/ExecRunC1.md:36`, `w2/ExecRunC2.md:17` report it. Not an unused surface.
- `landed_check.py` (487 lines) — pyflakes clean, all 35 defs reachable from `_fixtures`/`main` (`_ambiguous_blob_prefix`, `_write_blob`, `_object_format` are fixture builders at :260-294), no shell with report-derived input (`subprocess` only with fixed argv and `git -C`). It is the considerthese-1 deliverable cited in `SKILL.md`.
- `make_spec_w1.py` — byte-reproducible generator of a committed artifact; deleting it is safe (proof 2) but loses nothing to gain.
- `validate_append.sh` — the documented C7 regeneration path (`SKILL.md:1260`); C7 itself only reads receipts, so it is not on the counter's critical path.

Method note: `python3 -m pyflakes` is absent; I used `/home/vgpnk/.local/bin/pyflakes` (4.0.3). Dead-code claims about constants/functions are static (AST + occurrence count + manual read of both counters end to end), not executed proofs; the deletion claims above are executed proofs.

VERDICT: Two stale one-shot generators (`derive_c56_quote_truth.py`, `derive_c56_selftest.py`) and one unused import (`c56_quote_truth.py:57`) are proved deletable without changing either counter (C1 `0/10 met=True`, C2 `8/8 met=True` unchanged, C2 selftest still 67/67); everything else in the set earns its keep — the counters are dead-code-free and their duplicated helpers are pinned by C1's own helper-bytes rule.
