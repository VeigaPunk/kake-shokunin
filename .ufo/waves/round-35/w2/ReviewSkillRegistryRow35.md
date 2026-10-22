# ReviewSkillRegistryRow35 — SKILL.md link-preview-audit gate registry row vs PROTOCOL Gate standard

Attacks: the `link-preview-audit` gate registry row in `SKILL.md` ("Link-preview audit gate registry — round 35", added at `fd0d53b2`, present at `7deacc4629c1d05a34fb919d8095e99efc7b712f`) against `PROTOCOL.md` "Gate standard" (§Registry fields, Verdict, Self-test, Two evidences). Verdict: **no actionable finding; row conforms**.

## Method (all in sandbox clone at 7deacc; TMPDIR exported; no lane mutation)

- PROTOCOL gate standard read: `PROTOCOL.md:388-435` (`[PROTOCOL.md#3BE2]`).
- Row read: `SKILL.md:1035-1064` (`:raw`, clone at 7deacc). Self-test runner read in full (`scripts/link_preview_selftest.py:1-202`); audit tool read in full (`scripts/link_preview_audit.py:1-340`).

## Field-by-field verdict

1. **Required fields present — PASS.** name, kind `gate`, entry command, verdict map, self-test command + spelling (`--tool`, `--fixtures`), pinned-value path, write scope, owner `kake` — all eight Registry fields present (`SKILL.md:1045`).
2. **Verdict map == code exits & reasons — PASS.** Code constants `EXIT_CLEAN=0 / EXIT_POLICY=1 / EXIT_INPUT=2 / EXIT_USAGE=64` (`link_preview_audit.py:65-68`); JSON verdicts `clean` / `failed-policy` / `could-not-evaluate`. Exit-1 reasons are exactly the five declared: `og_required_missing`, `og_type_multiple`, `og_url_not_absolute`, `og_url_not_canonical`, `og_url_multiple` (map at `SKILL.md:1045`; emitting code at `:228-269`). Exit-2 reasons exactly `input_invalid` (manifest-level, audits nothing) and `page_unreadable` (per page, readable pages still audited, `pagesChecked` counts readable) — matches the appended correction paragraph. Exit 64 usage: stderr message, no stdout JSON. Live spot runs at 7deacc confirmed: clean manifest → exit 0 + `verdict:clean`; missing og props → exit 1 + `failed-policy` with `og_required_missing`; two `og:url` → exit 1 + `og_url_multiple`; bad manifest → exit 2 + `input_invalid`; missing page → exit 2 + `page_unreadable`; no args → exit 64, stdout 0 bytes, message on stderr.
3. **Self-test command runs — PASS.** `python3 -B scripts/link_preview_selftest.py` at 7deacc: exit 0, verdict `clean`, `45/45` passed, zero failures. Runner asserts exit code, verdict, `pagesChecked`, finding ids, and (reason, property) projections per fixture against committed `expected.json` (independent of recomputation), runs with `PYTHONDONTWRITEBYTECODE=1`; 45 fixture dirs ≥ `MIN_FIXTURES=20`; `--tool`/`--fixtures` spelling implemented. Scripts identical between `b1cbbc39` and `7deacc4` (git diff 0 lines), so the pinned b1cbbc39 selftest receipt remains valid.
4. **Pinned proof files exist — PASS.** `.ufo/waves/round-34/c1-matrix.json` sha256 `246a6a3b…14f7` matches the row's pin exactly; `verification/c1-at-76fac3b.json` present (28/28, `byKind` 6/6+13/13+7/7+2/2, `constantGatesAllRejected:true`); `verification/selftest-link-preview-at-76fac3b.txt` present; `verification/c1-at-b1cbbc39.json` present (`met:true`, `passed:24`); `verification/control-c1-*.json` present (base-tool 14, constant-clean 7, declaration 14, lookup-dcef39b5 7, all `met:false`); `verification/selftest-link-preview-at-b1cbbc39.txt` present. Criterion check re-ran: `registry_row_check.py` exit 0 at 7deacc (`missing tools: none`), matching receipt `criterion-registry-row-at-fd0d53b2.txt` (exit 0) and the pre-row fail receipt at `318561ef` (exit 1).

## Observations (non-defects)

- At 7deacc the sealed C1 counter refuses with `error: "key visible at the measured revision"` (exit 2) — by-design post-reveal guard (reveal `4c6be2bd` precedes 7deacc). Re-run at `b1cbbc39` (pre-reveal) reproduces the receipt: exit 0, `passed:24`, `met:true`, target 22.
- Residual: the row pins the round-34 matrix digest but not a digest for the sealed-case snapshot; the C1 seal/reveal workflow (sha256-pinned keys since `81d9fd74`) supplies that constraint. No Gate-standard violation found.

## Not verified

- Did not compare the 45 fixture `expected.json` bodies against matrix cases (selftest receipt + 45/45 green and committed fixtures checked by existence only).
- Did not probe resource-limit edges (16 MiB page / 4 MiB manifest bounds) or `--help` exit path.

Tools used: none installed (plain python3/git; no new packages).
