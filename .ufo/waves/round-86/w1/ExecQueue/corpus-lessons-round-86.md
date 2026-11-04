# Round 86 — routed dispositions (C1) and bounded Cache-Control reading (C2)

Author-side candidate for L1 integration only; not an after receipt or independent
closure. Base `376ac5dcdf86457ef1f8dd490dada735dad81f68`; frozen contract
`.ufo/waves/round-86/contract.md` at `efc2ad654f1ee56a86ecb57b3b709c18cd1323b5`.
Angle-bracket values are measured and filled at integration, never assumed by this seat.

## R1–R4 disposition table (C1: open=4 → open=0)

| Item | What it closes | Evidence (paths exact; values filled at integration) |
|---|---|---|
| R1 late-controls sequence | The round-85 routed defect that shortcut controls were captured after the ready-file handoff: this round's controls commit pre-freeze and the after receipts pin the carrier, so ordering is provable from bytes, not timestamps | Freeze: `.ufo/waves/round-86/controls/base-c1.txt` + `controls/base-c2.txt` read `met=false`; no `controls/after-c{1,2}-carrier.txt` at freeze. Carrier `<carrier-rev>`: `controls/after-c1-carrier.txt` + `controls/after-c2-carrier.txt` read `met=true`. Measured by `python3 -B .ufo/waves/round-86/count.py --root . --claim c1 --freeze 376ac5dcdf86457ef1f8dd490dada735dad81f68 --revision <carrier-rev> --work <work>`; counter selftest re-run red/green/junk/missing at freeze (seat receipt: `.ufo/waves/round-86/w1/ExecQueue/receipts/receipt-selftest.txt`) |
| R2 D84-4 operator routing | The literal-L2-planner vs validator-prohibition conflict is routed to the operator — a route-around, never a silent settlement; D84-4 itself stays operator-owned open | `.ufo/l0-questions.md` (fleet root, operator-owned) carries a `kake \| round-86 \|` line naming D84-4 and the planner/validator conflict; present and read by this seat at candidate time; counter conjunct `c1_item_r2` re-checks it at `<carrier-rev>` |
| R3 counterexample preservation | The round-85 false-row / canned-discriminator counterexamples stay resolvable and cited, so any finite green count remains a bounded disclosure, not proof of gate soundness | `.ufo/waves/round-85/w1/CriticClaims.md` (81 lines, 11806 bytes) and `.ufo/waves/round-85/controls/late-shortcut-c1.txt` (7 lines, 298 bytes) resolve at candidate; existence receipts: `.ufo/waves/round-86/w1/ExecQueue/receipts/receipt-existence.txt`; this lesson preserves the `round-85/w1/CriticClaims.md` path reference |
| R4 D84-2/D84-3 retained-open debt | The routed retention instruction is recorded as debt, not closure: both defects stay open with explicit `flip:` re-open conditions | `corpus/README.md` "Open instrument debt (round 86)" block names D84-2 and D84-3 with `flip:` conditions, citing `corpus/lessons/round-85.md` and `corpus/lessons/round-85-verifier-spotcheck.md` (candidate bytes: `.ufo/waves/round-86/w1/ExecQueue/corpus-README-debt-block.md`) |

Disclosed limit: R1–R4 are textual conjuncts over committed bytes; a records-only
tree with the right sentences opens nothing — transcription is the non-author
closure's catch. `open=4 → open=0` is claimed only from the counter's committed
after receipt; a nonzero after measurement is unprovable, and the population is
never narrowed after scoring.
