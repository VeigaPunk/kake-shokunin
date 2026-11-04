# Round 76 — Amendment 5 (terms-only, recorded before the final after-state)

Motivation (two independent seats, same finding): `w1/MutationTesterGates.md` and
`w1/ScribeKnowledge.md` both measured that at the round's own working revision the v0 counter prints
`findings=0` while the base is red — the eight spans it reports as absent are quoted verbatim inside the
round's own artifacts (the base receipt's finding lines and the seats' receipts), so the round's
diagnostics become the evidence for the defects they diagnose. Amendment 4 excluded the counter's own
files by name; that is too narrow: a seat's receipt or a later control can launder a quote the same way.

## D1 — the receipt universe excludes the measured round's seat working tree
A receipt is a committed file under a **receipt directory** of any round (`controls/`, `verification/`,
`resid/`, `receipts/`, `frozen/`, `fixtures/`, `cases/`, `sources/`, `live/`). Files under
`.ufo/waves/round-<N>/w1/` are **never** receipts when N is a round whose claim rows are being measured —
a seat's working tree is process evidence, not observation data. Data-extension files outside a receipt
directory are not receipts (this supersedes the v1 clause that admitted them).

## D2 — diagnostic lines are never evidence
Before matching, every receipt is stripped of any line matching `^\s*(T1|T2|T4|A1)\s+\S+:\d+\s`. A
diagnostic line reports that a quote is absent; it can never make that quote contiguous. This applies in
every receipt file, including files the counter did not write.

## D3 — Amendment 4 stands
`base-c1-quote-truth*.txt` and `ctl-*.txt` under `.ufo/waves/round-76/controls/` stay excluded by name.
The ledger's admissible evidence is therefore: receipts committed for earlier rounds (including that
round's own controls) and this round's **controls** — never this round's seat tree and never a diagnostic
line.

## D4 — the base count is unchanged
`findings=7` at `a0491fcd` (Amendments 3 §B6 and 4), and the target stays `findings=0 append_only=true
met=true`, exit 0. A run at the round's working revision that turns green without the repair rows is a
counter defect, not the after-state; the delivered instrument must be able to fail on the round's own
controls.

## D5 — the delivered counter's selftest must be green
`w1/MutationTesterGates.md` found the hardened build's `--selftest` aborts before any case: its fixture
helper is invoked twice with a byte-identical payload, so the second `git commit` exits 1 and the harness
raises. A counter whose selftest cannot run has not passed it (PROTOCOL §Gate standard); the delivered
`scripts/doc_quote_truth.py` must ship a selftest that exits 0 with every case executed, and the tally is
the evidence.
