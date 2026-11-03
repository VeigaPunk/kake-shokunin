# ReviewerC2 — round 74 / attempt 1 / w1

## Axes and scope
Freshness; historical fidelity; binding correctness; host-error discrimination; no-harm compatibility. Review recommendation only, not admission. Measured committed base `ced2878a1e77f57afb4ee3baebf1021e5130399b`; no after-state exists for this review. Contract read first. No production files edited, no installations, no subagents.

## Findings by severity

### High — delivered counter reports met=true / exit 0 for forbidden notes and lost history
Delivered `.ufo/waves/round-74/w1/ExecC2Counter/c74_sidecar_reobserve.py:79–90` computes met/exit solely from stat contradictions; `:117–123` appends annotation findings afterward without changing verdict. Independently exercised all 18 fixtures through its real `measure` function, replacing only `read_entries` with the fixture and its prior preimage (no os.stat mock). Every forbidden-vocabulary fixture and missing/changed-history fixture returns **exit_code=0, met=true**, even while `annotation_findings` identifies the violation. `bad-date` also returns 0 without findings. Its g4/g5 selftests at :151–158 inspect only the helper and never assert rejection by the actual verdict. This cannot establish the frozen kill rule at contract :112–118. Recommendation: make annotation failures affect the verdict and test that actual path, not just diagnostic production. Receipts and executable driver: `ReviewerC2-heldout/counter-heldouts.{py,json}`. This is a recommendation, not admission.

### Medium — standing sweep cannot certify history preservation
`scripts/freshness-sweep.mjs:359–394` validates current binding, date, kind and prose but never reads `history`. Heldouts `missing-history` and `changed-history` both exit **0** despite violating frozen C2 clauses 2 / kill rule. An after-state green sweep alone is insufficient evidence; the delivered counter also fails to reject these, as shown above.

### Medium — permission errors are absence to the standing sweep, not to C2
Heldout `permission-denied` successfully constructs `PermissionError` via a chmod-000 directory under scratch; sweep exits **0**, classifying its annotated token as declared absent. Frozen counter rule requires **exit 2, unevaluable**, and repair must refuse flip. Broken symlink produces FileNotFoundError and parent-file child produces NotADirectoryError: both are legitimate absent states under this contract, and both sweep exits are 0. Do not implement the new counter using exists/existsSync.

### Low — restoration is not an assertion used by the standing sweep
Contradicted absent fixture exits 0; restored-but-absent fixture exits 1. This confirms the disclosed blindness and the need for the new counter, rather than a new after-state regression.

## Independent base recount
174 entries; kind counts absent=148, restored=26. absent_present=144, absent_absent=4, restored_absent=0; restored_present=26; unevaluable=0. Independently implemented os.stat loop and SHA-256-ranked deterministic 20-entry sample, not a copied L1 sample. Full code and output: `ReviewerC2-heldout/recount.py`, `recount.json`; executed program exit 0.

The four remaining entries / three distinct tokens:

| Entry index (zero based) | Citation | Token |
|---|---|---|
| 0 | corpus/knowledge/drift-detection.md:77 | ~/Projects/plazir-15-site |
| 1 | corpus/knowledge/fleet-registry.md:57 | ~/Projects/plazir-15-site |
| 2 | corpus/knowledge/free-read-verbs.md:321 | ~/Projects/webzites/bin/webzites.mjs |
| 3 | corpus/lessons/round-6-aggregator-audit.md:48 | ~/Projects/webzites/scripts/kimi-surface.mjs |

Independent sample (index, kind, stat result, token):

- 166: absent / present — `~/Projects/shokunin/scripts/sources-census.sh` (corpus/lessons/round-64.md:106)
- 90: absent / present — `~/Projects/shokunin` (corpus/lessons/round-34-verifier-spotcheck.md:189)
- 115: absent / present — `~/Projects/shokunin` (corpus/lessons/round-62-verifier-spotcheck.md:44)
- 23: restored / present — `~/Projects/ds4cc-marketplace/burnerchrome` (corpus/knowledge/fleet-registry.md:51)
- 94: absent / present — `~/Projects/shokunin` (corpus/lessons/round-37-verifier-spotcheck.md:25)
- 40: absent / present — `~/Projects/ds4cc-marketplace` (SKILL.md:517)
- 12: restored / present — `~/Projects/ds4cc-marketplace` (corpus/knowledge/fleet-registry.md:50)
- 71: absent / present — `~/Projects/ds4cc-marketplace/speedrun` (corpus/knowledge/speedrun-pipeline.md:93)
- 39: absent / present — `~/Projects/ds4cc-marketplace` (SKILL.md:516)
- 5: restored / present — `~/Projects/ds4cc-marketplace` (SKILL.md:19)
- 15: restored / present — `~/Projects/ds4cc-marketplace` (corpus/knowledge/origin-repos.md:19)
- 102: absent / present — `~/Projects/shokunin` (corpus/lessons/round-49-verifier-spotcheck.md:72)
- 120: absent / present — `~/Projects/shokunin` (corpus/lessons/round-64.md:106)
- 157: absent / present — `~/Projects/shokunin/scripts/sources-census.sh` (corpus/lessons/round-49-verifier-spotcheck.md:72)
- 173: absent / present — `~/Projects/ufo-fsd-alpha` (corpus/lessons/round-22-verifier-spotcheck.md:94)
- 52: absent / present — `~/Projects/ds4cc-marketplace` (corpus/knowledge/render-web-services.md:108)
- 88: absent / present — `~/Projects/shokunin` (corpus/lessons/round-32-verifier-spotcheck.md:100)
- 21: restored / present — `~/Projects/ds4cc-marketplace/burnerchrome` (SKILL.md:424)
- 140: absent / present — `~/Projects/shokunin/kake-shokunin/corpus/SOURCES.md` (corpus/lessons/round-26-verifier-spotcheck.md:99)
- 171: absent / present — `~/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-33/w1/ReviewFreeze.md` (corpus/SOURCES.md:139)

## Semantics: committed sweep rule evidence
All line references below are to `git show ced2878a1e77f57afb4ee3baebf1021e5130399b:scripts/freshness-sweep.mjs`.

- Lines 374–377 require a calendar-valid YYYY-MM-DD date and a note including it: `Number.isNaN(Date.parse(e.date)) || new Date(e.date).toISOString().slice(0, 10) !== e.date` rejects bad dates.
- Lines 383–388: `const prose = e.note.replace(PATH_RE, '\u00abcite\u00bb');` then binding rejects `(e.kind === 'restored' && ABSENT_RE.test(prose))`; absent entries require absence vocabulary plus `historical record, not an executable instruction`.
- Lines 384 / 380–382 require matching source line digest and a normalized token on that line; a raw trailing-slash token fails binding, even though stat of the directory with slash succeeds.
- Lines 481–485: `if (erratum && erratum.kind === 'absent')` supplies an annotation from the sidecar. **Restored supplies none**; it does not erase absence language already present in source prose.
- Lines 517–520: `if (fs.existsSync(abs)) resolve.push(...)`; otherwise all cites annotated means declaredAbsent, else drift.

Thus flipping the 144 stat-present entries is semantically valid under loadPathSidecar provided the new notes avoid absence vocabulary and bindings remain unchanged. The sweep considers their present paths resolved regardless of annotation. If a restored token later disappears, it becomes drift only if at least one cite lacks its own prose annotation; if every source citation already carries absence language it can remain declaredAbsent. The new C2 counter must still reject restored_notes_absent independently. History is honest only when its `{date,kind,note}` preserves the old observation verbatim; unchanged corpus lines also preserve historical source text. History must not be treated as present-state absence prose.

## Heldouts
18 text JSON artifacts under `ReviewerC2-heldout/`, each containing sidecar bytes, contract expectation, actual os.stat category and observed sweep exit. Nine separate vocabulary fixtures cover every frozen absence-vocabulary phrase.

| Fixture | Contract expectation | Sweep expected / observed exit |
|---|---|---|
| absent-resolves | C2 exit 1: contradicted absent | 0 / 0 |
| restored-absent | C2 exit 1: stale restoration | 1 / 1 |
| vocab-absent | C2 exit 1 (or invalid input 2): forbidden vocabulary | 2 / 2 |
| vocab-gone | C2 exit 1 (or invalid input 2): forbidden vocabulary | 2 / 2 |
| vocab-vanished | C2 exit 1 (or invalid input 2): forbidden vocabulary | 2 / 2 |
| vocab-emptied | C2 exit 1 (or invalid input 2): forbidden vocabulary | 2 / 2 |
| vocab-no-longer | C2 exit 1 (or invalid input 2): forbidden vocabulary | 2 / 2 |
| vocab-dangling | C2 exit 1 (or invalid input 2): forbidden vocabulary | 2 / 2 |
| vocab-no-such-file | C2 exit 1 (or invalid input 2): forbidden vocabulary | 2 / 2 |
| vocab-never-published | C2 exit 1 (or invalid input 2): forbidden vocabulary | 2 / 2 |
| vocab-missing | C2 exit 1 (or invalid input 2): forbidden vocabulary | 2 / 2 |
| missing-history | C2 exit 1: missing prior observation | 0 / 0 |
| changed-history | C2 exit 1: historical note differs from base | 0 / 0 |
| bad-date | C2 not met; sweep invalid date exit 2 | 2 / 2 |
| trailing-slash | stat present; C2 contradiction; sweep rejects non-normalized token | 2 / 2 |
| broken-symlink | C2 absence is correct; stat FileNotFoundError | 0 / 0 |
| parent-file | C2 absence is correct; stat NotADirectoryError | 0 / 0 |
| permission-denied | C2 exit 2 unevaluable if PermissionError; repair must refuse flip | 0 / 0 |

Each sidecar is bound to a one-line `SKILL.md` fixture with its SHA-256; token resolution uses HOME set explicitly to the sole scratch tree. Permission denial was constructible for the current non-root process. The changed-history and missing-history fixtures assume prior base observation `2026-10-21 absent; historical record, not an executable instruction`, included in fixture metadata / peer history case; a candidate counter that requires committed fixtures must compare against that preimage rather than an unrelated production entry.

## Harm exercise on scratch-only proposed flip
Shared clone pinned to base, with only its sidecar locally rewritten: 144 flips, old `{date,kind,note}` appended unchanged, new date 2026-11-03 and `Linux reviewer host: stat ok; target present on direct re-observation.` Full proposed bytes retained as `ReviewerC2-heldout/proposed-sidecar.json`.

- `node scripts/freshness-sweep.mjs --selftest`: exit **0**, `selftest: 36/36 passed`.
- `node scripts/freshness-sweep.mjs --offline`: exit **1**, `VERDICT: DRIFT — §paths: 1 unannotated miss · 1 NOT in pins.pathsMissSet (exit 1, partial: offline)`.
- Named path remains `~/projects`; stdout identifies 6 of 27 cites unannotated. No `Error:` line or stderr. Full receipts retained.

These were run concurrently in the same base clone after the scratch-only proposed flip, not against an actual candidate after-state. The canonical selftest internally created and cleaned its transient HOME fixture as implemented at sweep lines 1286ff; all explicit TMPDIR/KAKE_SELFTEST_DIR paths were in scratch. This incidental HOME write is a seat-scope execution defect relative to the strict write-only-scratch requirement; no persistent HOME artifact is retained.

## Commands, exits, gaps
`ReviewerC2-heldout/commands.json` records exact argv, cwd, exit, stdout and stderr for every subprocess (git show, shared clone, root assertion, clone-only checkout, both harm commands, 18 fixture sweep commands, independent recount program). Clone root was asserted equal to its scratch path before checkout. No fixture commits were made. Recount uses only token field and HOME expansion, never file-field existence. Raw input fetched with mandated git-show command; no working-tree sidecar substituted.

LSP unavailable: `read xd://lsp` returned `No such tool`; therefore definition/references/diagnostics cannot be requested. Text/source checks above are literal evidence, not semantic LSP proof. No runtime routing/resume implementation is changed here; same-identity rerouting/saturation/resume_continuity_v1 claims are outside the frozen C2 scope, not inferred passed.

Counter arrived late and was exercised at base via CLI: exit **1**, entries=174, absent=148, restored=26, absent_present=144, absent_absent=4, restored_absent=0, unevaluable=0, met=false. All 18 heldouts were exercised at the measure-function boundary; permission correctly returns exit_code=2, broken symlink and ENOTDIR return 0, trailing-slash directory contradiction returns 1. The counter author acknowledged the high finding and reports its separate seat formula constrained met to host contradictions; frozen C2 acceptance is not established by that narrower formula.

Repair tool also arrived late at `ExecC2Tool/sidecar_reobserve.py`. Exercised all 18 fixtures through real `reobserve` in both check/write modes; `tool-heldouts.{py,json}` retains exact driver and output. Every check left bytes unchanged; permission-denied returned 2 in both modes with zero mutation. Invalid date raised ValueError at API boundary with zero mutation. Resolvable absent entry flipped; slash-terminated directory token also flipped (normalization/binding is not validated by this repair helper). Broken symlink and ENOTDIR remained absent unchanged. Existing invalid restored notes/history were neither repaired nor rejected: exit 0 unchanged, so it is an observation/repair tool, not the C2 gate. Stale restored entry likewise reports `restored_absent` without nonzero exit. These results must not be described as full predicate acceptance. No extra production change requested beyond the concrete counter verdict finding.

Raw CLI/driver commands and outputs are in commands.json. No actual after-diff reviewed. Residual risks: full committed-fixture CLI integration, repair's full-production candidate result, and actual landing-tip battery remain unverified. Do not admit C2 based on this pre-after review.

Self-evaluation: accuracy 4 (actual landing unavailable); completeness 4 (tool and counter exercised via API, not complete committed-fixture CLI integration); clarity 4 (raw receipts separated); actionability 4 (specific verdict bug identified); conciseness 4 (18-fixture detail retained in artifacts). Improvements: exercise actual landing tip and require end-to-end verdict rejection. User should agree these are explicit verification gaps, not passes.

Cleanup: removed `/fast/scratch/hyaku/kake-r74/ReviewerC2` with `shutil.rmtree`; subsequent existence observation was false. Receipts were copied first. No owned scratch tree remains.
