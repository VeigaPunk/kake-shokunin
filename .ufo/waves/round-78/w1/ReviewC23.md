C2 working-tree repair survives independent controls; two counter defects were fixed; C3 is unreviewed because all four required artifacts remain unavailable; carrier=pending.

## Scope and axes

Axes: calibration (C1, outside this seat), freshness (C2), operability/capability (C3). Reviewed frozen contract in full and amendment 1. No promotion, saturation, live-site correctness, remote freshness, or admission verdict is claimed. This is a recommendation only.

LSP unavailable: `read xd://lsp` returned “No such tool”; no semantic references/definition/diagnostics service was available. Source inspection and literal searches are fallback evidence, not semantic proof. No subagents, installs, git mutations, tool/case/counter edits, or external runtime dispatch were performed.

Evidence directory: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-78/w1/ReviewC23/`. Every command receipt retains exact absolute argv, cwd, stdout, stderr and exit. `receipt-sha256.json` hashes the selected retained receipts; its SHA256 is `9bd023c22b9be97a5ca93362c4944bf790b91fd7559b305d05620be3fac1fb6d`.

## Findings, by severity

1. **High — applied: C2 counter mislabeled working-tree measurements as revision measurements.** Original `c78_sweep_truth.py:100-108` ran `sweep(root)` while only its control archived `rev` (`:81-95`). Independent reproduction repaired a scratch snapshot, supplied the known-red base revision `fe50945399a386b48678b1f2051fdbe8a77b10bd`, and obtained exit 0 / `met=true`; original base archive independently returned exit 1 / drift 1 / newMissing 1. Read-only `GIT_DIR` let the scratch snapshot access lane object storage; no fixture commits were made. Receipt `counter-revision-mismatch.json`, SHA256 `b3ed978c6cad84e7c44e335d4bed4788bb176d1d0a6e9aa76204e167a33e1dcf`. Routed to KakeR78, who fixed the counter. Canonical repaired logic now archives the measured revision before sweeping (`c78_sweep_truth.py:124-138`). Reproduction against final digest `46acb450a2042249d0b589ed6614ab0c83e67e48da3eb5da69efd2ecbadb2821` exits 1, `sweep_exit=1 drift=1 new_missing=1 control_exit=1 control_drift=2 tree_identity=c07506acd9598bbe met=false`. Receipt `counter-revision-final.json`, SHA256 `c2bdcc17a4caa929d48552d324c504e6657111047b7f45e5866c19d945816870`.

2. **Medium — applied: first identity repair omitted decision inputs.** The intermediate `tree_identity():97-108` omitted both the sidecar and sweep source, although both affect the result. Routed and corrected: final `:101-109` includes `SKILL.md`, pins, sidecar, sweep source and all corpus Markdown. A sidecar-removal probe executed after the fix was already landing: it returned unequal identities and exits 1 versus 0, corroborating the corrected behavior, not reproducing the earlier collision. Receipt `identity-omits-sidecar.json` is retained with that honest distinction. Final counter digest is the one above.

3. **Verification blocker — routed: C3 artifacts absent.** Explicit reads/existence checks found none of `scripts/meta_robots_audit.py`, `.ufo/waves/round-78/cases/`, `.ufo/waves/round-78/consts/`, or `.ufo/waves/round-78/c78_meta_robots_matrix.py`. Producers and KakeR78 were notified. KakeR78 explicitly authorized a partial review rather than an invented verdict. No C3 case was executed or approved by this seat; no constant tally, matrix comparison implementation, or real-run site-correctness disclaimer could be checked.

## C2 independent citation census

`git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 78711a628ad7e1c23cefcb9f9e345a0cc240c25b:<file>` exited 0 for each enumerated source. This frozen-artifact revision carries the same original citation bytes as the base. Independent base JSON found **16 unannotated locations for one token**, not 16 absent paths. `citation-enumeration.json` retains each literal line and its ±2 window (SHA256 `32e1033afa9a3b6779516e88abd97877fc60d00a1d9d1d377f2d5aa5af87efa4`).

All locations below are under `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/`:

| File | Lines |
|---|---|
| round-66-verifier-spotcheck.md | 101, 102 |
| round-66.md | 69 |
| round-70.md | 119 |
| round-71.md | 73 |
| round-73.md | 59 |
| round-74-verifier-spotcheck.md | 36, 101, 137, 175 |
| round-74.md | 70 |
| round-75-verifier-spotcheck.md | 91 |
| round-76-verifier-spotcheck.md | 99 |
| round-76.md | 127 |
| round-77-verifier-spotcheck.md | 97 |
| round-77.md | 108 |

The 16 new sidecar entries (`freshness-sidecar.json:2578-2720`) match this set exactly. Every bound line hash matches; each token is exactly `~/projects`; current host observation finds `/home/vgpnk/projects` absent and `/home/vgpnk/Projects` present. Each note dates the observation 2026-11-03 and marks its citation historical/non-executable. The W6 consolidation history is supported by the pre-existing record `corpus/lessons/round-17.md:8-23` and `SKILL.md:308-312`; current existence tests do not independently prove a 2026-09-29 event or uninterrupted absence since then. The notes do not claim uninterrupted absence.

**Rejected: requiring these sidecar notes to sit in Markdown ±2 windows.** This is the existing line/hash-bound sidecar route, not new prose annotations. `freshness-sweep.mjs:358-393` validates the binding; `:481-485` attributes the note to the exact citing line. Ordinary windows are unchanged. The scanner reads SKILL and corpus Markdown (`:396-401`), not sidecar note text, so the notes introduce no new scanned path token. Original lesson bytes remain unchanged in the scoped diff. `sidecar-review.json` retains all sixteen bindings (SHA256 `1b119148abe86318a8e281a7dc9e8c61230f7b0682ea8a4d53aa2b7269f5be6f`).

## C2 exercised checks

All are working-tree measurements unless the row explicitly says base. Carrier remains pending; none is represented as a committed-carrier pass.

| Check | Result / exit | Receipt |
|---|---|---|
| `node /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/freshness-sweep.mjs --offline` | drift 0, no new miss; exit 0 | final-working-offline.json |
| Same plus `--json` | exit 0; independently `len(sections.paths.drift)=0`, `len(setDelta.newMissing)=0`, matching reported counts; paths.ok true | final-working-json.json |
| Sweep `--selftest`, isolated `KAKE_SELFTEST_DIR` and `TMPDIR` | 36/36; exit 0 | selftest.json |
| Independent base archive + only add `~/projects` to `pins.pathsMissSet` | drift 1, newMissing 0, paths.ok false; exit 1 | pin-only.json |
| Repaired scratch copy + new unannotated `~/ReviewC23-never-created-78` citation | drift 1, newMissing 1; exit 1; exact planted citation in drift | final-planted-unannotated.json |
| Repaired scratch copy + annotated genuinely present `~/Projects` citation | drift 0, newMissing 0; exit 0 | final-annotated-present.json |

Sweep source was not changed by the repair. Final sweep SHA256 `4bd99b04e1eb9ccad519edf185c16db860eb8e0f3e2f4f1a3e73eb4f07165f97`; pins `c3def789fda4bd94353e3197c9ce077e8ec0103fb92e9b960f7037669e2505c8`; sidecar `fc7f8b87835d4e67ba3545a3206cfc8ad455641ec88d28353d50de361c8624bf`. Armed checks were skipped and history suspended, not passed.

## C3 residual risk and required handoff

`independent-family-oracle.json` records derivations for all 29 amended family labels from contract sentences, without consulting a tool. It is a **partial family oracle**, not approval of absent `expect.json` files: null effective sets explicitly require actual fixture content; date rendering and g26's combined-versus-separate checks require inspection. Amendment A5 drops numeric video limits when nosnippet is present, so g26 must not expect both on the same check.

Three concrete adversarial mutations to test once the matrix exists (kill status **unknown**, not claimed):

- Choose the earliest `unavailable_after` by lexical timestamp rather than instant. An offset-crossing pair such as `2026-11-03T00:00:00+02:00` versus `2026-11-02T23:00:00Z` must choose the first instant. A matrix containing only one valid date would let this wrong implementation survive.
- Apply Unicode casefolding instead of ASCII case-insensitivity. A tag named `robotſ` must not match default agent `robots`; a casefold-based implementation would wrongly accept it. Ordinary uppercase g14 does not distinguish these algorithms.
- Treat `max-snippet:-1` as numerically smaller/more restrictive than `max-snippet:20`. Contract §C3 and amendment A5 require 20; g10 tests the video directive, not necessarily the snippet merge branch. A wrong snippet-only implementation survives unless a separate snippet-unlimited case exists.

These are proposed uncovered neighbors, **not** three proven surviving mutants: with no matrix files there is no honest way to establish survival. Likewise the four constants' failing case lists, finding-id **set** versus exit comparison, every concrete `expect.json`, tool selftest ≥40, and real-run disclaimer remain unverified.

After a carrier is committed, the L1 must repeat the offline/JSON sweep from that carrier, run the revised C2 counter with that carrier and an explicit scratch `--work`, then run/review the C3 matrix against the same tool revision and actual frozen cases/consts. The C3 recommendation remains withheld until those artifacts exist.

Scratch `/fast/scratch/hyaku/kake-r78/ReviewC23` was removed; existence check returned false. No tools installed or updated.

Self-evaluation: accuracy 4 (historical event grounded only in retained corpus); completeness 2 (C3 artifacts unavailable and carrier pending); clarity 4 (explicit partial-oracle qualifications); actionability 4 (named blockers and reruns); conciseness 4 (sixteen-location census retained rather than repeated source windows). Overall 3.6/5. Highest-impact improvement is a second independent C3 review after all producer artifacts and the carrier exist; this cannot be repaired by pretending pending checks passed. The user should agree that C2 is evidenced and C3 is not.
