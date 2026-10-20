# Measure — round 22

Axis: operability.

## Implementation

Implemented `.ufo/waves/round-22/measure.py` in the required private clone `/tmp/kake-r22-Measure`. The clone's `master` was observed at the frozen base `7c61c8cc791bde36dd5e3688bdfea2678d90146c` before editing.

The counter resolves `--revision` to a commit and obtains the validator only from `scripts/canonical_audit.py` at that commit. It reads Git blobs for the validator and, when present, the full matrix instrument (`matrix.py`, `cases.json`, and fixture blobs), materializes them into a temporary root, then invokes `matrix.py --root <temp-root> --json`. If the target revision lacks a complete instrument, `--cases-root` supplies the instrument independently: it prefers complete blobs at that root's `HEAD` and otherwise snapshots its working-tree files, rejecting symlinks and non-regular inputs. The target validator is never taken from `--cases-root`.

Every materialized input is reported in `blobs` with its SHA-256 digest, Git object ID where available, and source. Output includes the resolved revision, availability, accepted/total counts, the complete results, the independent 32-name manifest, the instrument revision/source, and raw matrix stdout/stderr. The contract's 32 case IDs are fixed in the counter; duplicate, missing, or extra IDs in `cases.json` and matrix results invalidate the count. A missing validator returns `accepted: 0`, `total: 32`, and `unavailable: true`; only the frozen baseline's unavailable result exits 0. Matrix failures exit nonzero.

## Retained evidence

- Frozen contract read: `.ufo/waves/round-22/contract.json`; it specifies the base hash, the count command, and 32 matrix case names.
- Clone observation: `git rev-parse master` returned `7c61c8cc791bde36dd5e3688bdfea2678d90146c`.
- Matrix owner confirmed the `cases.json` schema (`version: 1`, `cases` rows with `caseId`, `manifest`, `expectedExit`, `expectedFindings`, and `rationale`), result-row `caseId` fields, and `--json` output with accepted/total/results.
- Population reviewer required checking the frozen name set rather than relying on a count or fixture glob; that check is implemented.
- Per the wave instruction, no builds, tests, lint, formatters, or measurement runs were performed. No tools were installed. No LSP route was available in the session; this change adds a standalone file and does not refactor existing symbols.

## Risks and blockers

No implementation blocker. The candidate-root working-tree fallback is deliberately distinguishable in the output (`source: working-tree`, no Git object ID) and SHA-256-pinned; use a committed instrument when available for repeatable measurements. The expected-case name set is frozen in this script, while the complete oracle bytes are exposed by the reported `cases.json` digest; L1's separate replay digest map remains the authority for checking expected instrument identity. Integration and the post-wave check gate remain for L1.
