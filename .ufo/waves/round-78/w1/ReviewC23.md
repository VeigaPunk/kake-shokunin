C2 working-tree repair survives independent controls; C3 artifacts reviewed clean against contract+amendments 1-4 with three matrix-surviving mutations found (casefold mutant unguarded by matrix AND selftest); carrier still pending so no matrix-level pass is claimed.

## Scope and axes

Axes: calibration (C1, outside this seat), freshness (C2), operability/capability (C3). Reviewed the frozen contract in full plus amendments 1-4. No promotion, saturation, live-site correctness, or admission verdict is claimed. This review is a recommendation only.

LSP unavailable: `read xd://lsp` returned "No such tool"; no semantic references/definition/diagnostics service was available. Source inspection and literal searches are fallback evidence, not semantic proof. No subagents, installs, git mutations, or edits to the tool/cases/counters were performed.

Evidence directory: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-78/w1/ReviewC23/`. Every command receipt retains exact absolute argv, cwd, stdout, stderr and exit. `receipt-sha256.json` (SHA256 `bd0c250498a9a0e3d5d981472baa65aceef7e579ff2993a2aa169c76b4d50392`) hashes the retained receipts; per-input digests in `reviewed-c3-input-digests.json`.

## Findings, by severity

1. **High — applied: C2 counter mislabeled working-tree measurements as revision measurements.** Original `c78_sweep_truth.py:100-108` ran `sweep(root)` while only its control archived `rev`. Reproduction: repaired scratch snapshot + known-red base `fe50945…` + read-only `GIT_DIR` → exit 0 / `met=true` while the base archive was red (exit 1, drift 1, newMissing 1). Receipt `counter-revision-mismatch.json`. Routed to KakeR78; the fixed counter archives the measured revision (`c78_sweep_truth.py:124-138`). Re-run at final counter digest `46acb450a2042249d0b589ed6614ab0c83e67e48da3eb5da69efd2ecbadb2821`: exit 1, `sweep_exit=1 drift=1 new_missing=1 control_drift=2 tree_identity=c07506acd9598bbe met=false`. Receipt `counter-revision-final.json`.

2. **Medium — applied: first identity repair omitted decision inputs.** The intermediate `tree_identity()` omitted the sidecar and sweep source; routed and corrected (`:101-109` now hashes SKILL.md, pins, sidecar, sweep source, all corpus *.md). A sidecar-removal probe run while the fix landed showed unequal identities and exits 1 vs 0, corroborating the corrected behavior. Retained in `identity-omits-sidecar.json` with that honest distinction.

3. **High — routed: casefold mutant survives every frozen C3 guard.** A one-line mutation of the tool (`ascii_lower` → `str.casefold()`) passes all 36 matrix cases (my harness, `mutation-audit.json`) **and its own selftest 94/94** (exit 0). Contract violation demonstrated: `<meta name="robotſ" content="noindex">` (U+017F) must not match under ASCII case-insensitivity (contract §C3: name "ASCII-case-insensitively equals one of `agents`"); real tool returns default `follow,index`, mutant returns `noindex`. No matrix case and no selftest case uses a non-ASCII name or token, so this whole class is unguarded. Cheapest close: one frozen case (or selftest case) with a non-ASCII agent name (e.g. `robotſ`) expecting the default set. Tool/cases/counters untouched by me per seat rules.

4. **Medium — routed: two more mutations pass all 36 matrix cases while violating the contract** (both caught one level down by the tool's selftest, not by the matrix):
   - **Lexical `unavailable_after` ordering** (`min` by literal instead of instant): survives the matrix — g12a/b/c each carry a single date. Violation: `2026-01-01T00:00:00+02:00` (instant 2025-12-31T22:00Z) vs `2025-12-31T23:00:00Z`; contract §C3 "the earliest valid `unavailable_after` wins" → real tool picks the `+02:00` one, mutant picks `2025-12-31T23:00:00Z`. Tool selftest m26 kills it.
   - **RFC 822 weekday-merge removal** (the audit_page comma-merge special case deleted): survives the matrix — g12c's value carries no weekday. Violation: `unavailable_after: Mon, 25 Jun 2010 15:00:00 PST` (amendment 2 B6 accepts `[EEE,] D Mon YYYY HH:MM:SS ZONE`) → real tool: effective date, no findings; mutant: default set + `meta_robots_invalid_value` + `meta_robots_unknown_directive`. Tool selftest m23 kills it.
   - **Killed control:** `-1` treated as most restrictive (min over raw values incl. −1) is killed by g10 (`max-video-preview:-1` + `30` must render `30`) — the frozen set does pin the no-limit ordering. Also confirmed killed by the frozen set: body-tag-ignored (pre-A1) by g19; date-only-rejected (pre-A2) by g12b; exit-0-on-findings (amendment-3 C4 exit column) by the 8 amendment-4 rows; `nosnippet` not dominating by g25; `index`-beats-`noindex` by g06/g28.

## C3 review (artifacts now exist; carrier pending)

Matrix-level run is blocked: at review time HEAD was `e409f6c1f16d…` and `scripts/meta_robots_audit.py` is not committed; the matrix correctly exits 2 (`tool_absent rc=128`). `controls/after-c3-matrix.txt` honestly records the same state — it matches my run byte-for-byte on the verdict line and `cases_sha256=2ee1dea3…`. **Real-run receipt** (`w1/ExecC3Tool/realrun.txt`, tool sha256 `886e8861…` — byte-identical to the blob I reviewed, so the harness results above apply to it verbatim): the receipt explicitly states the run "is the real-run smoke (audit output vs. what the page declares), not a correctness claim about any live property". Its population is named — 8 retained round-23 capture pages (sha256-verified against `fetch.json`, 8/8) plus four 404 surfaces reported as not retained, "never counted clean or as an error"; expectations were derived from the retained bytes independently of the tool; the run is offline over captures (no fetch); 8/8 pages `["follow","index"]`, findings empty, exit 0, plus selftest 94/94 and a 36/36 cross-check. The "does not claim site correctness" check **passes on the receipt's own text**, not vacuously. Carrier-committed rerun of the matrix itself is still pending.

Independently verified (harness replicates the matrix's B1 isolation: manifest copied to a random scratch dir, check id neutralized to `check`, `expect` stripped, page copied, tool run `--manifest --root --json`; receipts `case-audit.json`, `constants-audit.json`, `mutation-audit.json`):

- **Case oracle vs contract, not the tool:** I re-derived all 36 rows from §C4 + amendment-4 exit corrections before looking at outputs. All 36 `expect.json` match my independent table (0 mismatches) — including g19 (`noindex` + `tag_outside_head`, exit 1), g26 (`max-video-preview:-1,nosnippet`), g31 (missing content ≡ empty), g33 (lowercase `t`/`z` rendered as written), g34/g35 (`exit:2` + error codes). Case directory holds exactly 36 ids, no extras; g34's manifest names a nonexistent page, g35 duplicates one id.
- **Working-tree tool vs oracle:** 36/36 correct through the harness (working tree, not a carrier blob — not a matrix receipt).
- **Comparison semantics:** `judge()` compares exit code, version, single-check shape, check id, sorted `effective` and sorted `findings`; its selftest proves effective-only and findings-only wrongness each fail (`matrix-selftest.json`, exit 0). Finding-id **sets** are compared, not just exits.
- **Constants (run by me per case):** `always_clean.py` fails 32, `empty_findings_real_exits.py` fails exactly the 8 amendment-4 finding rows, `naive_substring.py` fails 25, `report_every_id.py` fails 36 → `constants_failed == 4` will hold. The matrix additionally runs a label-leak sibling adversary (`echo_sibling_expect.py`) and requires it to fail — a strengthened, not loosened, gate.
- **Tool selftest:** exits 0 (receipt `tool-selftest.json`); B5's `P == T ≥ 40` gate is implemented (`run_tool_selftest`).

## C2 exercised checks (working tree, carrier pending)

| Check | Result / exit | Receipt |
|---|---|---|
| `node …/freshness-sweep.mjs --offline` (and `--json`) | drift 0, newMissing 0, exit 0; JSON counts re-derived equal | final-working-offline/json.json |
| `--selftest` (isolated dir) | 36/36, exit 0 | selftest.json |
| Independent base archive + pin-only `~/projects` | drift 1, newMissing 0, exit 1 | pin-only.json |
| Repaired copy + planted unannotated cite | drift 1, newMissing 1, exit 1 | final-planted-unannotated.json |
| Repaired copy + annotated present `~/Projects` | drift 0, newMissing 0, exit 0 | final-annotated-present.json |
| Revised counter at base revision | exit 1, met=false (correct) | counter-revision-final.json |

Citation census: exactly 16 unannotated `~/projects` locations at the base (`citation-enumeration.json`); the 16 new sidecar entries (`freshness-sidecar.json:2578-2720`) cover them 1:1 with matching line hashes, dated 2026-11-03 notes, historical/non-executable markers, and no new scanned path token (the scanner reads SKILL/corpus Markdown, `freshness-sweep.mjs:396-401`, not sidecar notes). `/home/vgpnk/projects` is absent and `/home/vgpnk/Projects` present on this host; the W6 2026-09-29 event history rests on the retained r17 record (`corpus/lessons/round-17.md:8-23`, `SKILL.md:308-312`), which the notes cite rather than overclaim.

Sweep source digest `4bd99b04…`, pins `c3def789…`, sidecar `fc7f8b87…`. Armed checks skipped, history suspended — not passes.

## Residual risk and required handoff

1. Carrier replay: ~~C3 matrix~~ — closed by `controls/after-c3-matrix.txt` at `82c3d02c…` (`met=true`, byte-identical inputs, see the carrier update below). Still open for C2: rerun the sweep/JSON and the revised C2 counter against the committed revision (`--revision 82c3d02c…`); `controls/after-c2-sweep.txt` was cut on the lane worktree (input digests match my measured bytes exactly: sweep `4bd99b04…`, pins `c3def789…`, sidecar `fc7f8b87…`; exit 0, drift 0, newMissing 0) but is not itself a committed-revision measurement.
2. ~~Real-run receipt~~ — done: `realrun.txt` disclaims site correctness explicitly and names its population; carrier-committed replay of the matrix binary against `<carrier>` remains the open item.
3. The casefold guard gap (finding 3) survives the matrix predicate as frozen; until a case/selftest row pins a non-ASCII name, `met=true` does not exclude that class. Also consider an instant-vs-literal multi-date matrix case (M1) and a weekday-form case (M3) — both currently only selftest-guarded.
4. Minor doc rot, no action required: `meta_robots_audit.py:117` comments `EXIT_FINDING` as "unused by this interface" while `audit_manifest` uses it.

Scratch `/fast/scratch/hyaku/kake-r78/ReviewC23` removed; existence check false. No tools installed or updated. Self-check: accuracy 4 (all C3 claims executed; W6 history rests on retained corpus records), completeness 4 (C3 artifacts were reviewed this time; only the carrier-committed reruns remain), clarity 4, actionability 4 (three named mutation closes with concrete inputs), conciseness 4. Overall 4.0/5.

## Carrier update (appended 2026-11-03, after the carrier committed)

Carrier `82c3d02c39d16ae99c6cd34238fa3ec6ea089fb9` landed; `controls/after-c3-matrix.txt` now records the real matrix run: `met=true` — cases=36 decided=36 correct=36 wrong=0, constants_failed=4/4, selftest 94/94 exit 0, `sibling_expect_control_failed=true` (label-leak adversary rejected), case_set 36/36 with no missing/extra, `tool_blob=ff0a9df0…`, `tool_sha256=886e8861…` (byte-identical to the blob I reviewed), `cases_sha256=2ee1dea3…` (identical to the case tree I audited). The four constants' failing counts and first-failing ids in the receipt (32/8/25/36) match my independent harness exactly. This closes the "carrier-committed rerun" gap for C3; my earlier tool-absent observation was valid at `e409f6c…` and is superseded by this receipt. Residual, explicitly accepted by the producers as fixed-population limits (no widening after scoring): the casefold-agent, instant-vs-literal date-ordering and RFC822-weekday classes remain guarded only outside the frozen set (two by the tool selftest; the casefold class by nothing measured). That is a documented boundary of `met=true`, not a defect in the receipt.
