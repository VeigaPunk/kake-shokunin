# CriticC1Deletion

## CASES

Empirical probes ran the committed `scripts/receipt_lineage.py` at lane HEAD `f5a9b8acc8e4d0995e8ba849c4a9d56ba1ab0a8f` in four isolated scratch Git repositories (each verified as its own toplevel; no lane mutation). All produced exit 0 and no findings:

| Case | Tool output | A3 consequence / counter coverage |
|---|---|---|
| Receipt added, then deleted and absent at measured revision | `receipts=0 events=0 undisclosed=0 met=True` | A3 says absence in a later tree is a deletion event with empty result span. For a receipt with non-empty result span, this differs from the parent span and is a `rewrite`, hence absent disclosure should yield `undisclosed_rewrite`. Counter-level frozen-member check can separately yield `member_missing`; the lineage tool itself is silent. |
| Receipt deleted, then re-added byte-identically | `receipts=1 events=0 undisclosed=0 met=True` | A3 implies a deletion event (empty child span) and an add event (non-empty child span against absent parent): two `rewrite` events absent disclosure. |
| Rename-with-edit in one commit (`git mv` plus result-line edit) | `receipts=1 events=0 undisclosed=0 met=True` | Under A3 the old frozen receipt path's deletion is an undisclosed rewrite. New path is its own history; if newly introduced under the legacy population rule it is also counter-level `extra_member`. Tool misses the old-path event. |
| Pure rename | `receipts=1 events=0 undisclosed=0 met=True` | Same deletion omission; tool's built-in selftest L19 explicitly expects clean. |

The code explains the results: `walk_changes` records `D`, but `segments_of` closes the current segment and emits no deletion item; `path_events` compares only blobs within each segment, starting each segment from its own first blob. `evaluate` enumerates population from the measured revision tree, so a path absent at that revision is not evaluated at all. Tool selftest L20 also expects a delete/re-add to be clean.

## GAPS

1. **A3 conformance defect (C1 calibration axis):** A3 explicitly makes an absent path a deletion event with empty result span. The tool instead treats deletion as a segment boundary, not an event. This suppresses the deletion and makes delete/re-add and rename laundering clean. This is a fixable implementation defect, not merely a tradeoff: the tool's documented behavior and selftests L19/L20 contradict the binding amendment.
2. **Counter coverage gap:** contract C1's L1–L16 fixtures contain no delete, delete/re-add, rename-with-edit, or absent-at-revision deletion case. Thus the frozen 18-case predicate cannot detect this defect. The expected counter `.ufo/waves/round-61/c61_lineage_cases.py` is absent from committed HEAD (`git ls-tree` lists no such file); `w1/ExecC1Counter.md` likewise says the implementation was incomplete, L1–L16 were not implemented, and it must not be frozen/used. No counter run is claimed here.

## Smallest safe correction

Implement the A3 deletion event for a watched receipt path, comparing the empty span at deletion with the last present span; classify it by the frozen rewrite/pending-fill rules and pass it through normal disclosure matching. Treat a re-add as an event against the absent parent (do not silently reset the comparison baseline). Add explicit counter fixtures for deletion and delete/re-add, plus a rename case; assert the expected tool findings and counter `member_missing`/`extra_member` behavior where applicable. Update the tool's L19/L20 selftest expectations to match A3. Keep the existing frozen predicate unchanged.

## Axes

Impacted axis: **calibration** (C1). Finding: the specified measure does not detect a deletion-based manipulation, and its declared counter has no deletion test. No evidence of effect on operability or freshness.

VERDICT: C1 tool violates binding A3 and frozen counter coverage cannot catch deletion; reject this implementation on calibration until deletion semantics and fixtures are corrected.