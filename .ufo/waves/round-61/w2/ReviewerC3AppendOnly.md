# ReviewerC3AppendOnly

## Findings

- **SOURCES.md row diff:** base `9f07731` has 167 rows; working-tree after-state has 171. Exactly 9 base rows changed, each only in the `recheck` cell: S002–S010. S001 is unchanged. No base row is missing; original base-row order is preserved. New rows S430–S433 are appended in order. Diff numstat is 14 insertions / 9 deletions (13 added registry rows including four new rows; 9 replaced due rows). The changed due rows' other ten columns are unchanged.
- **Due-set semantics:** S002–S010 have concrete pins matching the frozen dates: S002–S007 → 2027-01-17; S008–S010 → 2027-10-19. S001 remains `on-release`; the lesson Gate line records `anchor_moved`, an observed state and honest carry with no pin. Thus the absent S001 recheck-cell change is consistent with the contract's non-pinning rule.
- **Retained rechecks:** receipts and bodies for S001–S010 are present in the working tree; each body matches its recorded SHA-256 and byte count, with HTTP 200, `round61` user-agent, and 2026-10-27 fetchedAt. S001's Gate note states the anchor moved and its second URL was not fetched. S002's second URL likewise was not fetched; this is disclosed in the Gate, but the contract's source-recheck rule uses one fresh GET per due row.
- **Lesson logging:** the populated `## Gate` logs each changed recheck cell old → new (S002–S010) and records S001's observed `anchor_moved` carry. The four new-source Gate records identify S430–S433 and retained-body provenance. The S433 line says the W04 duplicate-URL warning is census output and S088's row is unchanged.
- **W04 / S088:** the S088 registry row is byte-identical to base; there is no S088 change in the SOURCES.md diff. The observed W04 note is in the S433 lesson Gate line. No round-61 after-census output is present under `.ufo/waves/round-61/controls/` at review time, so the required census-after exit-0 result remains unverified.

## Diff tally

`corpus/SOURCES.md`: 14 insertions, 9 deletions; 9 changed base rows (S002–S010), all recheck-cell-only; 4 appended rows (S430–S433); 0 removed/reordered base rows; row count 167 → 171.

## Residual risk / verification gap

The after-census result is not yet available in the controls directory, so W04 being census-only is supported by the unchanged S088 row and lesson record, but the final census exit status is not verified. Review used the working-tree after-state because `corpus/SOURCES.md` and `corpus/lessons/round-61.md` were uncommitted at inspection; no lane content was changed by this review.

VERDICT: SOURCES.md changes satisfy the append-only and due-cell constraints; final W04 census exit status remains unverified.
