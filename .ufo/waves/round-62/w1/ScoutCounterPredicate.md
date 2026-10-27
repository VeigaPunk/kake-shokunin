# ScoutCounterPredicate — frozen counter review

## Findings

**Mismatch: `unresolved` is a proxy for four marker checks, not a count of the disagreement(s) actually resolved.** In `c62_calibration.py:31`, `disagreements` counts every spot-check line containing both `S432` and `Disagree`. But `:39-40` sets `resolved` from correction/criterion/lesson/source markers and then forces `unresolved=0` whenever those markers are all present, regardless of `disagreements` (including zero, or multiple rows). This does not implement a direct `unresolved_round61_spotcheck_disagreements == 0` predicate; it assumes those markers prove resolution.

**Mismatch: the correction and criterion tests do not establish their substantive content.** `:33-34` tests only for the literal quote, `S432 §3.6`, and `Round-62 correction` somewhere in the knowledge blob; it does not check that the correction is appended, explains support, or preserves the prior knowledge prose. `:35` tests only for `substantive located quote` and the verifier filename anywhere in QUALITY.md, not that the appended criterion states the intended rule or cites/follows the verifier finding. Thus unrelated/decoy occurrences can satisfy both bits without the requested change.

**Mismatch: purported lesson/source guards are token-presence checks.** `:36-38` accepts `## Gate`, `S432`, `Agree`, `Reject`, and `| S432 |` anywhere in their respective files; it does not verify a meaningful gate, retained old disagreement/source row, or row identity/content. The contract explicitly says old-row preservation (`contract.md:7`) and describes the counter as verifying old-row preservation and pointers (`:19`), but the implementation has no base-blob comparison or preservation check.

**Observed contract difference:** the frozen claim asks for a substantive correction and grounded QUALITY criterion, and explicitly preserves the existing S432 row and verifier record (`contract.md:7-9`). The implementation's boolean gates can report `met=true` without proving those semantics. Also, its printed fields include `lesson_gate` and `source_row` (`counter.py:42`) beyond the three named frozen predicate terms; those extra gates do not repair the semantic gaps.

## Evidence / exact commands

Read-only source inspection (no lane files modified):

- `read /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-62/contract.md:7:raw`
- `read /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-62/c62_calibration.py`

Observed source lines: `contract.md:7-9,19`; `c62_calibration.py:31-43`. No counter execution or score was performed.

## Confidence / gaps

High confidence in the implementation/contract mismatch: all findings are direct readings of the frozen files. I did not independently verify the base-control run or hash, and did not inspect corpus blobs beyond the supplied contract grounding; semantic correctness of any later claim remains unassessed.