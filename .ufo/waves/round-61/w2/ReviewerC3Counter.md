# ReviewerC3Counter

## Conditions and verdict

L1's after-state is **not committed** at review time. Lane HEAD is `f5a9b8acc8e4d0995e8ba849c4a9d56ba1ab0a8f` (`round-61: w2 falsification spec and 36-seat dispatch`); `corpus/SOURCES.md` is modified and the round-61 lesson, S010 recheck body, and other integration artifacts are untracked. Per assignment, an official measured-after-state verdict is **PENDING**; no measured lane revision is invented.

Ran the frozen counter as committed at HEAD against HEAD: `conditions_passed=4 of 6`, exit 1. C1, C3, C4, C6 passed; C2 failed because there are zero pinned dates, and C5 failed because the lesson Gate notes are not present in committed bytes. This is the expected pre-integration state, not a score of L1's after-state.

For falsification only, copied the currently visible integration artifacts into a `git clone --shared` under this seat's scratch, asserted its toplevel before committing there, and ran the committed counter against that provisional scratch commit (`ec35c5c37e18f1033fa0b9187a0bd2ed3e04878b`). Result: C1–C6 passed, `conditions_passed=6 of 6`, exit 0. This is explicitly provisional, not the lane's measured revision. It derived the frozen due set S001–S010; found nine pins and S001 carried with a Gate observation. C6 reported 167 base rows, 171 measured rows, and appended ids S430–S433. The nine pins were within their frozen cadence bounds; the on-release pin was exactly opened+90d.

## C6 and evidence checks

C6's provisional pass establishes that base rows outside S001–S010 are byte-identical under the counter's row-line comparison, due rows changed only in the recheck cell, every base row remains, and the four additions are S430–S433. Independent working-tree diff inspection likewise showed the expected S001–S010 recheck-cell edits plus S430–S433 additions, with no edit to S001's source-row fields. New ids are contiguous after S429.

The counter's selftest passed `56/56` in seat scratch. Independently checked the ten working-tree recheck body files against the receipt population: all S001–S010 bodies exist, and the displayed body byte counts/hash prefixes match the corresponding receipt values; provisional counter C4 fully validated the selected receipts. No tool was installed.

## Review notes / limits

The counter is committed-bytes-only and its provisional run used a scratch commit, so it does not establish that the lane has integrated or committed these bytes. Re-run against the actual L1 integration revision before recording the official C3 result. No `lsp` device/server was available in the provided tool inventory; code review used the committed counter source and its selftest instead.

VERDICT: PENDING — L1 after-state is uncommitted; provisional scratch measurement passes C1–C6 (6/6).