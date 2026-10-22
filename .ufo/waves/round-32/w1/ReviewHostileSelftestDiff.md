# KakeR32 wave 1 — ReviewHostileSelftestDiff (C1 code review)

Scope: `git diff a0b0dff..285abca -- scripts/citing_set_hostile_selftest.py scripts/fixtures/citing-set-hostile/`
(21 changed lines in the selftest, +26-line new spec `P6-commit-before-init/hostile.json`).
Verdict: NO DEFECTS FOUND in the diff. Observations below are info/nit only.

## Findings by severity

- HIGH/MED/LOW: none.
- INFO (pre-existing, not diff-introduced): docstring "Output" line
  (scripts/citing_set_hostile_selftest.py:62-65) describes only
  `{"schema","passed","cases"}`; `main()` also emits `runner` and `error`
  keys. Unchanged by this diff.
- INFO (cosmetic): line 2 still says "(round 31)" although P6 is a round-32
  case; P6 spec `"gap": "m3"` diverges from siblings' N-series gap labels
  (N1,N2,N3,N5,N6) — gap is free-form and only recorded in `detail["gap"]`.
- INFO (cosmetic): `reason_contains` " " (whitespace-only) passes validation;
  substring check would then test for a blank — harmless.
- INFO (style): the new docstring paragraph at lines 38-43 is accurate but
  convoluted; meaning: deleting the load-time guard still leaves the shape
  refused by a later layer, so reason_contains pins the first refusing layer.

## Acceptance checks performed

1. `load_spec` validation (lines 142-144): requires non-empty str.
   Unit probe on the tip file: rejected int 5, "", null, ["a"], 0, false
   (LOAD_REJECT x5); accepted the committed spec (LOAD_OK). Rejected specs
   make `main` exit 2 (lines 246-250), consistent with existing validation.
   `CASE_KEYS` (line 84) extended in place; unknown-key rejection preserved.
2. Passed predicate (lines 218-221): `reasonChecks[n] = isstr(reason) and
   needle in reason`; missing/non-str reason -> False -> spec fails ->
   selftest exits 1. Conservative: a hostile case that fails with a
   different reason, or does not fail, both fail the spec. `all({})` on
   specs without the key is True — zero behavior change for P1-P5.
   Runner messages verified at tip AND base, identical:
   - load-time guard scripts/citing_set_selftest.py:365-366 raises
     ValueError "...setup op 'git_commit' needs an earlier 'git_init'" —
     contains P6 needle "needs an earlier 'git_init'".
   - apply-time re-check lines 491-493 raises RuntimeError "git_commit
     needs the repository created by git_init" — does NOT contain the
     needle, so mutant m3 (load-guard deleted) fails P6's reasonCheck.
     This is exactly the discrimination C1 claims.
3. Docstring: new key documented as optional (lines 38-43); pass criteria
   updated at line 53-55 to include reason_contains "when given" — matches
   the predicate. Runner/selftest usage text unchanged and still correct.
4. JSON output shape: `reasonChecks` is `dict[str,bool]` inside
   `cases[i].detail` (same level as `reasons`/`canary`/`victimUnchanged`),
   present on every spec run including `{}` for key-absent specs; absent
   only on the pre-existing `{"error": ...}` exception branch — acceptable.
   Probe `.ufo/waves/round-32/c1_m3_probe.py` reads only `cases[].case`/
   `.passed` — compatible.
5. Existing specs unchanged: diffstat shows only the new P6 file added under
   the fixtures dir; P1-P5 JSON files are byte-identical (no modifications
   in the diff). Their runtime behavior is gated by `"reason_contains" in
   case`, so they cannot observe the new field.

## Commands run (all in sandbox clone at tip 285abca)

- `git diff a0b0dff 285abca -- <paths>` — exit 0, artifact://9323.
- `git clone` + `checkout -q 285abca` to
  /fast/scratch/hyaku/kake-r32/w1/ReviewHostileSelftestDiff/clone — OK.
- `python3 -m py_compile scripts/citing_set_hostile_selftest.py` — OK.
- load_spec unit probe — UNIT2_EXIT=0, results above.
- `python3 -B scripts/citing_set_hostile_selftest.py --root . --tmpdir
  $TMPDIR/hostile` — exit 0; `passed: true`; all six specs passed;
  P1-P5 `reasonChecks {}`; P6 `reasonChecks {'h6': True}` and
  `reasons {'h6': "case.json setup op 'git_commit' needs an earlier 'git_init'"}`.
  Captured at /fast/scratch/hyaku/kake-r32/w1/ReviewHostileSelftestDiff/tmp/pristine.json.

## Residual risk / verification gaps

- Live-verified: pristine pass path, load_spec rejections, JSON shape.
- NOT live-verified by this seat (assigned to mutation-testers): mutant m3
  run producing RuntimeError reason -> reasonCheck False -> spec fail ->
  probe `killed: 1`. Static analysis + L1 receipt (c1-after-2f2f12d:
  killed 1, "mutant P6 fails only") support it; no defect mechanism found.
- No `lsp` device exists in this seat's tool inventory; review used
  rev-pinned source reads plus executed probes (stronger than grep).
- No tools installed this round; pacman paused, nothing needed.
