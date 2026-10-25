# ReviewerC2CounterCode

Scope: code review of `.ufo/waves/round-55/c55_quote_truth.py` (699 lines) before the C2 claim is
measured. Method: full read; ground truth from base revision fcaf4b8… (registry rows, receipts,
mirror pin) and staged wave evidence. Findings marked `confirmed by running` were demonstrated by
executing the counter's own code paths on throwaway `mktemp -d` fixture repos built through the
counter's own `_build` (identity confined to the fixture via `-c user.name=selftest`; no lane path
mutated; lane git used read-only: `show`/`log`/`grep` only). No `lsp` server is mounted in this
session (only `ast_edit`/`debug` under `xd://`), so caller/definition checks were done by direct
read — recorded per protocol. No tools installed (none needed; pacman untouched).

FINDINGS:

F1 HIGH — C8 vacuous pass on a falsy pin — line 407 `if mirror_text is not None and pin:` — confirmed by running
   Input: `mirror-pin.json` = `{}` (equally `[]`, `null`, `0`, `false`) with a contaminated mirror
   (junk row appended). The entire C8 block — mirror==base bytes, restored-bytes append-only check,
   row count, add-commit ancestor/strictness/blob-hash, and "measured revision carries the row"
   (lines 407-455) — sits inside the `pin` truthiness gate, so it is skipped and C8 passes.
   Run: fixture case C (`pin={}`) and D (`pin=null`): exit 0, 8/8 met on a contaminated mirror;
   control case B (same contamination, real pin): exit 1, C8=fail.
   Fix: after `pin = json.loads(pin_text)` require `isinstance(pin, dict)` with `sha256`/`rows`
   present (note otherwise), and gate on `mirror_text is not None and isinstance(pin, dict)`.

F2 HIGH — C7 `row_lines` last-match-wins lets the validated registry differ from the landed one —
   lines 124-133 (`row_lines`), 382-386 (comparison) — confirmed by running
   `row_lines` maps an id to the LAST line matching `^ {0,3}\| *Sxxx *\|` anywhere in the file,
   unlike `parse_registry` which scopes to `## Registry`. A validated scratch registry carrying two
   S418 rows (first altered, last byte-faithful) makes `vlines["S418"]` equal the landed row, so
   C7's byte-equality passes although the census-validated registry's S418 row differs from the
   landed one; no other check reads the validated registry's whole text.
   Run: case M → exit 0, 8/8 met. Fix: scope `row_lines` to the `## Registry` section (track the
   heading as `parse_registry` does), treat a duplicated id as a defect, compare first occurrences.
   (Landed-side exposure is backstopped by C8's whole-text restoration; the validated side has no
   backstop. C8's own `mlines` use is false-fail-only, guarded by mirror==base.)

F3 MEDIUM-HIGH — C5 quoted spans ≥401 chars are entirely invisible — line 309
   `re.findall(r'"([^"]{1,400})"', line)` — confirmed by running
   Input: an entry line with a 450-char fabricated quoted span: the regex cannot close, so the span
   matches nothing — no ceiling check, no substring check. Run: probe P3 (`[]` for a 450-char span)
   and case K (exit 0, C5=pass; control K2, 40-char fabricated span → C5=fail).
   Fix: use `"([^"]+)"` (as the Gate path already does) and enforce the ceiling in code.
   Note: the selftest's own span picker (line 579) shares this regex, so the selftest cannot catch
   this defect by construction.

F4 MEDIUM — C5 `[INFERENCE]` lines skip all quote checks — line 307 — confirmed by running
   Input: entry line `Note [INFERENCE] the operator says "<30 CJK chars>" here.` — the whole line is
   skipped, so neither the ceiling nor the raw-substring check applies.
   Run: case H → exit 0, C5=pass; control case I (same quote without the marker) → C5=fail with
   both notes. Fix: validate quotes on inference lines too (the ≤25-unit/substring rule is
   quote-scoped, not line-scoped), or skip only the marker token, not the line.

F5 MEDIUM — C5 never scans the first 8 entry lines — line 306 `body.splitlines()[8:]` — confirmed by running
   Input: a 30-unit fabricated quote appended to the `verified-at:` header line (line 2 of 8). C2
   only checks those lines for the three header keys; C5 starts at line 9.
   Run: case G → exit 0, C5=pass. Fix: scan all lines, exempting only lines that matched the
   `source:`/`verified-at:`/`recheck:` header pattern.

F6 MEDIUM — C5 Gate line validates only the LAST double-quoted span — line 293 `q = quotes[-1]` — confirmed by running
   Input: Gate line `- S372 <url> 2026-10-25 — "FABRICATED NOT IN BODY ANYWHERE XXXX" "<real>"` —
   the fabricated first quote gets neither the 6..25-unit check nor the substring check.
   Run: probe P4 (selection) and case J → exit 0, C5=pass. Fix: validate every span in `quotes`
   (each 6..25 units and a raw substring), or require exactly one quoted span per Gate line.

F7 MEDIUM — C6 compares the UTC-shifted date: stale receipts can pass, fresh ones can fail —
   line 167 (`parse_iso`) + lines 350-351 — confirmed by running
   Input: `"fetchedAt": "2026-10-24T20:00:00-05:00"` → 2026-10-25T01:00Z → date check PASSES (stale
   receipt accepted); `"2026-10-25T08:00:00+09:00"` → 2026-10-24T23:00Z → false FAIL.
   Run: probe P1. Live receipts are `+00:00` on the round date, so no live impact; latent.
   Fix: compare the calendar date in the recorded offset (drop `.astimezone(timezone.utc)`), or
   require `Z`/`+00:00` receipts and compare that date.

F8 MEDIUM-LOW — `units()` undercounts halfwidth kana and non-BMP CJK, defeating the ≤25 ceiling —
   lines 87, 96-98 — confirmed by running
   Input: `"ｱ"*30` → 1 unit (rule: 30; U+FF76… halfwidth kana are outside CJK_RE, the run is one
   non-CJK token); `"𠮷野家"` → 2 (rule: 3; U+20BB7 outside the BMP ranges).
   Run: probe P2. Fix: extend CJK_RE with `\uff65-\uff9f` and `\U00020000-\U0002ffff`; decide and
   document CJK punctuation (U+3000-303F, currently 1 unit per token-run).

F9 LOW — C7/C8 byte-equality claims are line-ending-blind — line 93 (`text=True` in `git()`) — confirmed by running
   `show()` decodes with universal newlines, so CRLF/CR blobs compare equal to LF text: the C8
   mirror==base check, the restored-bytes join, and C7's row/entry equality cannot see line-ending
   contamination; the pin sha256 is computed over the re-encoded normalized text, so a CRLF mirror
   with a pin hashed over normalized text passes all C8 checks.
   Run: probe P7 (CRLF blob → `show()` returns LF). Fix: use `show_bytes` + strict UTF-8 decode for
   registry/mirror/validated texts, or hash raw bytes for the pin comparison.

F10 LOW — C8 false-fail when the append introduces a trailing newline the mirror lacked —
   lines 421-431 — confirmed by running
   Input: mirror whose last line has no newline; measured registry = edited mirror + "\n" + S418
   row + "\n". Restoration drops the S418 element but keeps the trailing "" element → restored ends
   "\n" ≠ mirror → "append-only" false fail on a legitimate append. Run: case E. Live base ends
   with "\n" (verified), so latent. Fix: compare after normalizing a single trailing newline, or
   document that the append must preserve the mirror's trailing-newline state. Related latent:
   `set_used_by` canonicalizes the cell to `| value |` — byte-exact for the live mirror padding
   (probe P5: round-trip exact on the real S372/S373 lines), but a mirror with different cell
   padding would false-fail.

F11 LOW — C3's escaped-pipe check is dead code — line 235 `any("\\|" in cell for cell in row)` — confirmed by running
   `parse_registry` splits cells on `|`, so no cell can contain `|`, hence never `\|` (probe P8:
   cells from a `\|`-bearing line are `[' a \\', ' b ', ' x ']` — check False). The real
   `\|`-in-source case manifests as extra cells and is caught by the `len(row) != 11` gate. No
   wrong verdict possible; the check can never fire. Fix: delete it, or test `cell.endswith("\\")`.

F12 LOW — `selftest()` mutates the module global `BASE_REV` and never restores it — lines 498, 650 — [INFERENCE]
   After `selftest()` returns, `BASE_REV` holds the last fixture's base sha; any later `run_checks`
   call in the same process (module import + reuse) silently measures C3/C8 against a fixture
   base. Benign in the CLI flow (main exits after selftest). Fix: pass `base_rev` as a parameter to
   `run_checks`, or save/restore in a `finally`.

F13 LOW — selftest `rev` fallback misreports when cwd is not a git repo — line 499 — [INFERENCE]
   `git(os.getcwd(), "rev-parse", "HEAD")` failure yields `rev=""` → every evidence read fails →
   "missing round-55 evidence <first path>", exit 2, masking the real cause. Fix: check the rc and
   error with "not a git repository: run from the lane root".

NO-DEFECT CHECKS:

- C3 `row[:10] != base[:10]` is correct for the 11-cell schema: used-by is cell index 10 (verified
  against the base rows: 11 cells, used-by at [10]); the slice runs only after the `len(row) != 11`
  gate; stripped-cell drift inside cells 0-9 is backstopped by C8's byte-level restoration
  comparison. No unsatisfiable-contract defect: base S372/S373 already carry `opened=2026-10-25`,
  `mined`, `180d` (rows entered round 53, commit fd91527 dated 2026-10-25), so `opened ==
  ROUND_DATE` and "used-by only" are jointly satisfiable.
- C4 ordering: `want = PRIOR_USED_BY.get(sid, []) + [path]` enforces append-at-end order, matching
  the contract's "prior + entry" phrasing; base S373 used-by is exactly
  `yahoo-japan-rel-nofollow-semantics.md, baidu-friendly-crawl-guidance.md` (comma-separated,
  verified on real bytes), so `used_by`'s `[,;]` split reproduces PRIOR_USED_BY order; S418 want is
  exactly [entry 3]. A semantically-equal but reordered used-by would false-fail — intended
  strictness per the frozen contract, noted, not a defect.
- C7 `tail[-1].split("\t")[1:2] != ["ok"]` matches the census validator's real output format
  (`file\tok`; round-49 verifier lesson: stdout "ends `file ok`"; the identical check landed green
  in round 52's c52 counter). The `if code in stdout` E03/E04 scan is substring-based; clean
  validator stdout carries no such legend (round-49 evidence), so no live false-fail.
- C8 add-commit logic correct: `commits[-1]` takes the OLDEST add on a newest-first log;
  `merge-base --is-ancestor`, strict-earlier (`add_commit == rev`), blob-hash-vs-pin, and
  no-S418-in-blob are all right. Mirror verified byte-equal to the base registry (sha256 f4e6cc88…,
  144364 bytes, 155 rows — matches mirror-pin.json).
- `_build` fixture ordering correct: base-registry commit → pre-append evidence commit (mirror,
  pin, validated registry, argv/stdout/exit, scratch entries) → append commit (landed tree); C8's
  strict-ancestor and C7's validate-before-append semantics are exercisable; commit identity is
  confined to the fixture repo; toplevel verified against the tempdir. The 30 selftest mutation
  cases each target the intended condition (spot-audited: e.g. `fail_held_row_cell_changed`
  mutates cell 3 within the S372 line only; `fail_used_by_dropped_prior` uses `set_used_by`, so C3
  stays green and C4 fires).
- `row_lines` scoping exposure is latent today: 0 row-like `| Sxxx |` lines outside `## Registry`
  in the base tree (probe P6); `## Leads (unopened)` uses bullets, not table rows.
- `parse_iso` rejects naive timestamps (returns None → "not ISO 8601" note) — defensible, since
  receipts carry offsets; wording nit only. A receipts file without a `sources` key is treated as
  fail (exit 1) rather than unevaluable (exit 2) — semantic quibble.
- text-mode `git show` decodes UTF-8 in this environment (preferred encoding UTF-8, verified); a
  C-locale run would raise inside the try and exit 2 (unevaluable), not a wrong verdict.
- The selftest `pass` case requires landed evidence; pre-landing `selftest` exits 2 naming the
  first missing path — honest. Selftest itself was NOT run (no landed revision exists yet; W1 in
  flight; `assimilation/validate/` absent) — reported unrun; the fixture battery substitutes.

RESIDUAL RISK / VERIFICATION GAPS:
- The fixture battery used synthetic entries/lesson/rows built from real bodies, receipts, mirror
  and pin; case A (faithful fixture) passed 8/8, exit 0, which validates fixture fidelity — but the
  counter has not been run against a real landed revision (none exists yet).
- F1/F2 are reachable by a falsifier with commit access to the wave evidence; both are cheap to fix
  before measurement. F3-F8 are quote/date/ceiling bypasses; F9-F11 are false-fail/robustness;
  F12/F13 are selftest hygiene.
- Not verified: the census validator's exact current argv/stdout contract beyond the round-49/52
  precedent (round-55 `validate/` does not exist yet); the Gate line format the executor will
  actually write (round-52 precedent: `## Gate` heading, single quote per line).

VERDICT: 13 findings — 2 high false-pass defects (F1 C8 falsy-pin vacuous pass; F2 C7 row_lines last-match-wins), 5 medium quote/date bypasses (F3-F7), 6 low — each with line, failing input and fix; happy path verified sound on a faithful fixture (8/8, exit 0).
