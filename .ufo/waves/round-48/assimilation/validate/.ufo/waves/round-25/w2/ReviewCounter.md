# ReviewCounter — independent code review of `.ufo/waves/round-25/measure.py`

Scope: code review only of `measure.py` (blob `46b8319f…`, identical in the working tree and in candidate
`9f62cda0a6b71a9c0c86d2088f01673f25787715`), cross-read against `scripts/accessibility_packet.py` (blob
`b4ef3def…`) at the same revision. I did not run `measure.py`, the packet tool, the selftests or the suite.
Read-only facts gathered: `git ls-tree`/`cat-file`/`log`/`for-each-ref`, `sha256sum`. No r24 artifacts read.
No tool installs/updates.

## Verdict

**Agree on the current candidate. The counter is not admission-unsafe for 9f62cda.** Revision blobs equal working-tree bytes for
measure.py, population.json, source-wcag22.html, the tool, cards and packet doc. Both pinned fixtures hash to
the constants (population `4751dc24…`, source `6e3c5fe3…`; frozen copies identical). `refs/replace` is empty.
Four fixable defects remain. None changes the result for 9f62cda, but each one can produce a wrong or
mislabelled result for another revision. Details follow under D1–D4.

## Axis judgments

| Point | Judgment |
|---|---|
| Revision snapshot | Tool + cards read as blobs at the resolved commit (`resolve` L100-110, `read` L112-114); tool runs `-I -B` in a temp snapshot with minimal env (L274-306). Sound, except D1/D2. |
| Baseline absent | 6883f1d has none of the round-25 paths (ls-tree empty) → fixtures via fallback → `tool is None` → `capability_absent`: verdict `failed`, accepted 0, exit 1 (L339-340, L311-314). Correct outcome; finding label is `input_invalid` (see D3). |
| Numerator per card | `accepted` = sum of per-criterion acceptance computed by the counter itself (L203-241); the tool's number is never trusted, only strict-compared (L363). Agree. Hazard: a stray unknown-id 56th card yields `accepted: 55`, `verdict: failed` (global `metadata_mismatch`, L199-200) — admission MUST key on `verdict == clean` and exit 0, never `accepted` alone. |
| Aggregate cross-checks | Full-document `strict_equal` (type-exact, key-exact, ordered lists) plus exit-code equality (L250-259, L363). Aggregates are derived, so internally consistent by construction. `len(cards) == EXPECTED` (L245) is redundant given no findings, harmless. Agree. |
| Oracle pinning | Population and source pinned by SHA-256 at the revision or in the fallback, `population.sourceSha256` cross-checked (L163-165). Caveat (tradeoff, not defect): constants, population and measure.py were all introduced in the same commit as the deliverable (`git log` shows only 9f62cda); there is no pre-candidate registration of the pins. The counter does not re-derive `normativeText` from the source HTML; the population hash is the oracle. |
| websiteConformance | Counter output is always `not-assessed` (`packet_result` L52-60); tool output must strictly equal it. Per-card `status != "not-assessed"` → finding. Agree. Residual: card prose is not screened for conformance assertions; that is a documentation boundary (packet.md decision table), not a counter defect. |
| Old receipt counters | No r24/round-24/receipt reference in measure.py (`rg` rc=1). Agree. |

## Defects

### D1 — The working-tree fixture fallback can grade a revision whose own checkout cannot run (snapshot handling; operability)
`pinned_bytes` (L117-147) falls back to the working tree whenever the revision has no blob for the fixture.
The comment calls the fixtures "not candidate deliverables", but the production tool hard-codes and loads them
from `--root` (`accessibility_packet.py` L16-21, L96-101), so they are runtime dependencies of the deliverable.
**Counterexample:** a revision R that keeps `scripts/accessibility_packet.py` and the cards but deletes
`.ufo/waves/round-25/population.json`. The counter takes the working-tree copy, injects it into the snapshot
(L286-290), and reports `clean`/exit 0. But `python3 -B scripts/accessibility_packet.py --root .` at R returns
`could-not-evaluate`/`input_invalid`/exit 2 (its `load` hits OSError). The fallback also walks every
`root.parents` up to `/` (L129). A stale mismatching file found before the right copy raises
`snapshot_tampered`, and a matching copy outside the repo is silently trusted.
**Smallest fix:** allow the fallback only on the capability-absent path. When `tool` exists at the revision,
require both fixture blobs at that revision; if one is missing, return the packet's `input_invalid`/exit 2.
Limit fallback candidates to `root/path` and the measure.py checkout, not every ancestor up to `/`.

### D2 — `GitStore.read` turns any git failure into "path absent" (snapshot handling; operability)
`read` returns `None` on any nonzero exit (L112-114). A corrupt or missing object, a partial clone or a
permission error on the tool blob therefore reaches `tool is None` → `capability_absent` → `failed`/exit 1.
That is the baseline-absent verdict, but the honest result is `could-not-evaluate`/exit 2. For fixtures, the same failure
silently switches to the working-tree fallback. Lesser hardening gap: `git cat-file`/`rev-parse` honour
`refs/replace` (only `GIT_*` env is stripped, L89-90). None exist today.
**Smallest fix:** distinguish absence (for example `git ls-tree -z <rev> -- <path>` returns empty) from failure (nonzero
exit → `InputFailure("input_invalid")`). Add `--no-replace-objects` to the git argv.

### D3 — A tool disagreeing with the counter is reported as `input_invalid`, the same as unavailable input (false provenance; operability)
Mismatch returns `invalid_input("input_invalid")`, exit 2 (L363-364). That is byte-identical to genuine input
unavailability, and identical to the expected result when cards are absent (L359-361), so a reader cannot tell
"candidate tool lies" from "input missing". Concrete divergence that exists today: the production tool parses
cards with plain `json.loads` (`accessibility_packet.py` L104), which keeps the last duplicate member.
**Counterexample:** a card containing `"status": "passed", …, "status": "not-assessed"`. The tool reports
`clean`/exit 0, but a first-wins JSON consumer reads `passed`. The counter's `strict_json` rejects it
(expected exit 2), so the counter correctly withholds admission. Its finding, however, blames input instead of
naming the tool divergence. Baseline absence also reuses `input_invalid` per criterion (L311-314).
**Smallest fix:** emit a distinct stable finding for tool/counter disagreement (for example `tool_mismatch`) and
for capability absence (for example `capability_absent`). Separately, the production tool should reject duplicate
members with the same `object_pairs_hook` the counter uses. That is a production change and is not made here.

### D4 — Deeply nested JSON crashes the counter without the stable JSON output (operability)
`strict_json` callers catch only `UnicodeError`/`ValueError` (L161, L266, L351), and `main` catches only
`OSError` (L380). Deeply nested cards (for example `[` repeated 10⁵ times) or deeply nested tool stdout raise
`RecursionError` in CPython's json decoder. [INFERENCE: known CPython behaviour, not executed here.]
That error escapes `evaluate`, so the counter prints a traceback, emits no JSON and exits 1, which the contract
reads as "packet failed". Admission is still withheld because the exit is not 0.
**Smallest fix:** inside `strict_json`, convert `RecursionError` to `ValueError`.

## Minor (maintainability, no axis harm)
- L359-361 is unreachable: `derive_packet(rows, None)` raises `InputFailure` (L188-189) before the `else` branch.
  Delete it.
- `input_invalid_rows(rows)` ignores `rows` (L317-318). It is the same as `invalid_input("input_invalid")`.
- The production tool reads its population from a wave-scoped `.ufo/waves/round-25/` path. The deliverable's runtime
  data lives in a round workspace, which is what makes D1 possible.

## Impacted axes
operability (D1–D4), freshness (none: pins match the dated REC 2024-12-12 snapshot, and there is no r24/receipt reuse).
