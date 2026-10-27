# ExecC2Counter

Wrote `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/c61_header_cases.py` (new file,
the only lane path I touched; no git/jj mutation). It is the C2 counter for § Claim C2: it scores
`scripts/header_audit.py` on the 18 frozen H-fixtures, plus R3 (real-manifest shape, run-recorded) and
R4 (do-nothing at base) as printed gate lines. I did not score any after-state; the only lane-revision
execution was the contract base `9f07731a`, where the tool is absent (read-only, R4).

## DESIGN:

- **Extraction.** `git show <rev>:scripts/header_audit.py` into `--work`; absent tool ⇒ 0/18 (exit 1),
  never a crash. `GIT_*` scrubbed from every subprocess env; `--work` removed on exit.
- **CLI.** `python3 -B c61_header_cases.py --root <lane> --revision <rev> [--work D] [--seed N] [--json]`,
  hidden `--tool` for the selftest. Exits 0/1/2/64 per contract; `PREDICATE = "met: cases_passed == 18 of 18"`.
- **Fixtures.** Each fixture is a directory under `--work` holding `manifest.json` at its root and
  captured responses at `.ufo/waves/round-61/capture/<id>/response.json` (+ `body.bin`), so root-relative
  and manifest-relative `source` resolution coincide. Ids, hosts and directory names are drawn from
  `--seed` (printed) so a fixture-keyed tool cannot recognise them. Recorded responses use the landed
  capture shape `{"url","finalUrl","method","status","headers":[{"name","value"}],"headerCount",
  "contentType","bytes","sha256","truncated","fetchedAt","userAgent","redirects","error","bodyFile"}`
  (confirmed by ExecC2Capture-2); the counter accepts no other shape as "the" shape.
- **Tool argv.** `--manifest <fx>/manifest.json`, plus `--root <fx>` only when the tool's own `--help`
  output advertises `--root` (contract fixes no tool CLI; `.ufo/waves/round-61/w1/ExecC2Counter.files/`
  carries no copy of the tool). `--json` is never passed to the tool.
- **Exactness.** Finding lines `^(\\S+) ([a-z_]+) (.+)$` restricted to the six policy classes +
  `could_not_evaluate`; summary `^checks=(n) findings=(k)$`. Clean case = exit 0, no finding line, one
  summary `checks=<fixture n> findings=0`. Finding case = exit 1, exactly one line `<id> <class>`,
  summary `findings=1` with the fixture's check count. H13 = exit 1, exactly one `could_not_evaluate`
  line for the faulty check, zero policy lines, summary `checks=2`. H14/H15 = exit-only.
- **Sub-fixtures.** A case may hold several manifests and passes only if all meet their expectation;
  the extras pin the contract's boundaries: H2 (204 as well as 200), H3 (`https:false` ⇒ no HSTS
  finding), H4 (`max-age=0` present), H6 (`NOsniff ` and `nosniff\t`), H7 (`sniff`, `nosniff; preload`),
  H9 (uppercase singleton declaration; two `X-Frame-Options`; single field clean), H10 (Set-Cookie twice
  with and without the declaration), H11 (404 and 304), H12 (token name clean), H13 (missing receipt,
  non-numeric status, `null` status — each with one evaluable check beside it), H16 (undeclared duplicate
  `Vary` is not a finding), H17 (space- and tab-padded values). Every expected-clean 2xx fixture also
  carries headers that are clean under the *literal* class prose (Content-Type present, XCTO `nosniff`
  wherever a field exists), so no case decides the under-specified expectation-flag gating
  (ambiguity 10) either way.
- **R3.** Materialises the committed round-61 capture tree at `<rev>` (every `.json` plus every file
  under a capture dir, via `git ls-tree` + `git show`) into `--work`, so only committed bytes are read.
  Requires exactly one version-1 manifest with a `checks` array (prefers `manifest.json`), 12 checks,
  12 distinct `source`s each present in the materialised tree; then runs the tool and requires one
  summary `checks=12 findings=<k>` with exit 0 iff k==0. The k value is recorded, not asserted.
- **R4.** Resolves the literal contract base, asserts `git cat-file -e <base>:scripts/header_audit.py`
  fails, and runs `measure()` with an absent tool path (0/18, exit 1). Base unresolvable ⇒ printed
  `unverified`, does not withhold `met`.
- **met** = 18/18 AND R3 shape ok AND R4 not violated. Exit 1 otherwise; 2 when `--root` is not a
  repository toplevel or `--revision` does not resolve.
- **Interface pin.** Sent to ExecC2Audit, ExecC2Audit2, ExecC2Manifest and ExecC2Capture-2: tool CLI
  `--manifest` [+`--root`], repo-root-relative `source` = the `response.json` only, manifest shape,
  `field_name_syntax` as a required class, per-check `could_not_evaluate` (exit 1) vs manifest-level
  exit 2, and the real capture header/status shape. ExecC2Audit's reply matches the pin (`--help`.
  exits 64, which `probe_root()` tolerates by reading the text).

## SELFTEST: (tally)

`python3 -B .../c61_header_cases.py --selftest` → **ok, 7 controls, exit 0** (evidence:
`ExecC2Counter.files/selftest.txt`):

| control | score | expected |
|---|---|---|
| missing_tool | 0/18 | 0 |
| always_clean (`checks=<n> findings=0`) | 9/18 | 9 (H1,H4,H5,H6,H10,H11,H16,H17,H18) |
| always_exit_1, no output | 0/18 | 0 |
| manifest_sniffing composite | 9/18 | 9 (must fail every finding/exit case) |
| reference_impl (contract rule, inside the counter) | 18/18 | 18 |
| R3 shape control, 12-check synthetic tree | pass | pass |
| R3 shape control, 11-check synthetic tree | fail | fail |

Discrimination probe (13 mutants of the reference, `ExecC2Counter.files/mutants.txt`) — **13/13 killed,
each by its intended case**: header names case-sensitive → 6/18 (H1,H3–H10,H12,H13,H17); no OWS trim →
H6,H17; nosniff case-sensitive → H6; 2xx read as 200-only → H2; Content-Type rule applied to all statuses
→ H11; singleton declaration case-sensitive → H9; Set-Cookie treated as singleton → H10; no
`field_name_syntax` → H12; findings exit 2 → H2,H3,H7,H8,H9,H12,H13; summary counts `evaluated` →
H13; cne silently dropped → H13; HSTS ignores the `https` gate → H3; every duplicate is a finding → H16.

Other exercised controls: base-revision do-nothing run `--revision 9f07731a` → 0/18, `R4 PASS`, exit 1
(`do-nothing-base.txt`); exit 64 for absent `--revision` and for an unknown flag; exit 2 for a
non-toplevel `--root` and for an unresolved revision; and a synthetic committed repo (12 capture
receipts + 12-check manifest over 8×200/4×404) → 18/18, `R3 PASS exit=0 checks=12 findings=0`, exit 0.

R3 shape probe over the **real** round-61 manifest (read-only copy of `.ufo/waves/round-61/capture/`,
run with the counter's own reference implementation — not the landed tool, so no after-state is
scored; `r3-real-manifest.txt`): discovery finds exactly one version-1 checks manifest
(`capture/manifest.json`), 12 checks, 12 distinct root-relative sources all present, and
`r3_check → (True, 'exit=1 checks=12 findings=13')`. The 13 findings are recorded, not asserted clean,
and match ExecC2Manifest's independent audit count.

**Unrun:** the counter was not executed against the lane after-state or against the landed
`scripts/header_audit.py` (seat instruction); that 18/18 + R3 run belongs to the L1 after the freeze.
`[INFERENCE]` the landed tool passes if it reads header objects, keeps `--manifest`/`--root`, and
implements per-check `could_not_evaluate`, `field_name_syntax`, OWS/case rules and the Set-Cookie
exemption — its own selftest report and reply match the pinned interface, but I have not measured it.

## CONTRACT AMBIGUITIES:

1. **Case arithmetic.** §C2 says "18 fixture cases" but its table has 20 rows (H1–H18 + R3 + R4), and the
   predicate reads "18 of 18 (H-fixtures plus R3's run-recorded shape check)". Resolution taken: the
   scored denominator is H1–H18; R3's *shape* gates exit 0 (its verdict value is recorded), R4 is the
   do-nothing control also gating exit 0. If the L1 meant H1–H17 + R3 as the 18, only the printed
   denominator changes — say so before freeze and I will re-cut the constant.
2. **Sixth class.** H12 requires `field_name_syntax`, absent from the prose list of five classes. Table
   governs; the counter asserts it (and the landed tool implements it).
3. **Tool CLI is unfrozen.** No `--manifest`/`--root`/`--json` is specified for `header_audit.py`. Pinned
   as `--manifest` + optional `--root` probed from `--help`; the manifest sits at each fixture root so
   both plausible `source` bases coincide.
4. **`source` referent.** "capture receipt path" could mean a receipt file or the recorded
   `response.json`; the counter binds it to `response.json` (12 distinct).
5. **Recorded-response schema.** The contract names "final status … ordered header name/value pairs" but
   not the JSON encoding; the landed capture uses `status` (int) and header objects and `sha256`. Fixtures
   follow the capture, so a tool built against pair-arrays or `body_sha256` would fail all 18 — record
   that the capture schema is now the de facto one.
6. **H6 vs "exactly nosniff".** The class prose says "not exactly `nosniff`", H6 requires `NOsniff ` to be
   clean. Table governs: OWS span-trim, case-insensitive token compare.
7. **All-checks-non-evaluable.** "per-check `could_not_evaluate`" (H13, exit 1) vs "exit 2 only when NO
   check is evaluable" collide for a valid manifest whose every check is cne. Avoided: every cne fixture
   carries one evaluable check, so H13 asserts exit 1 unambiguously; that shape is untested and left to
   the L1/tool author (the landed tool chooses exit 1, which is compatible).
8. **R3 manifest location and uniqueness.** Not fixed; the counter discovers any version-1 manifest with a
   `checks` array under `.ufo/waves/round-61` and fails on ambiguity, preferring `manifest.json`.
9. **`body.bin`.** R3 materialises retained bodies too, but the audit is header-only; a tool that
   dereferences `bodyFile` must not require it at audit time (the counter provides it, the contract does
   not require it).
10. **Expectation flags vs literal class prose.** `content_type_present` and `xcto_nosniff_value` are
   defined by their sentences without naming the manifest flag, while manifest v1 carries the flags:
   read literally, any 2xx without Content-Type and any non-`nosniff` XCTO is a finding regardless of the
   declared flag; read as a declared expectation, the flag gates the class. The counter decides neither —
   every expected-clean 2xx fixture carries Content-Type and (where XCTO exists) `nosniff`, so its clean
   cases pass under both readings, and no finding case turns on a false flag (raised by ExecC2Audit2).
   Untested by design; a w2 critic may want the L1 to freeze the gated reading explicitly.

## RISKS

- R3 can fail on a real manifest whose `source`s are not repo-root-relative, or if a second version-1
  `checks` manifest lands in the tree (both messaged to ExecC2Manifest).
- H13's `null`-status sub-fixture is an inference from the capture schema, not a contract row; it is one
  sub of three and cannot alone fail H13 for a tool that treats `null` as unparseable (the landed tool
  does).
- Flag-gated vs literal expectation semantics (ambiguity 10) is deliberately not discriminated; a tool
  that gets it wrong in either direction still passes the 18.
- No blocker; no tool installs were needed.

VERDICT: C2 counter landed at `.ufo/waves/round-61/c61_header_cases.py`; selftest 7/7 controls ok (0/18, 9/18, 0/18, 9/18, 18/18 + two R3 controls), 13/13 mutants killed on their intended cases, base do-nothing 0/18 with R4 PASS, R3 shape validated against the real manifest (12 checks, 12 sources, findings=13 recorded); the 18/18 after-state run over the landed tool remains for the L1 after freeze.
