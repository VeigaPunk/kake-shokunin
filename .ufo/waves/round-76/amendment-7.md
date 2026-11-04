# Round 76 — Amendment 7 (terms-only, recorded before the final after-state)

Motivation: Amendment 5 §D1 excludes "the measured round's" seat tree, and the delivered counter read that
as **every** round in `--rounds` (75 and 76). Measured consequence at `a0491fcd` on build `eae3ce48`:
`findings=9` instead of 7, because two legitimate round-75 observations fell out of the receipt universe —
S443's retained-body digest `cbe684a1…` (retained under `.ufo/waves/round-75/w1/ScoutSources/`) at
`corpus/lessons/round-75.md:56`, and `source=uncommitted` (a round-75 tool receipt) at line 103. A closed
round's seat receipts are observation data, the same class as its `controls/`; only the round under
construction has an untrusted working tree.

## F1 — the seat-tree exclusion applies to the newest measured round only
`.ufo/waves/round-<M>/w1/` is never a receipt when **M is the largest round in `--rounds`** (the round under
construction). Seat trees of older measured rounds are ordinary receipt sources. All other Amendment 5
rules (D2 diagnostic-line stripping, D3 name exclusion, D4 base/target, D5 selftest) stand unchanged.

## F2 — the before-state
Under F1 the base at `a0491fcd` is the seven findings of Amendments 3 §B6 and 4 (`findings=7 met=false`,
exit 1); the two extra findings the D1 reading produced are a receipt-universe artifact, not defects of the
round-75 ledger. The after-state target is unchanged: `findings=0 append_only=true met=true`, exit 0, at a
revision that carries this round's claim rows and the repair rows.
