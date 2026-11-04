# Round 76 — Amendment 4 (terms-only, recorded before the final after-state)

Motivation: `w1/ExecQuoteRepair.md` measured that committing this round's own C1 control receipts makes the
counter print `findings=0` with **no repair at all**: each diagnostic line in
`.ufo/waves/round-76/controls/base-c1-quote-truth.txt` ends with the very span it reports as absent
(`  T1 SCORECARD.md:4892 files=18 mismatches=0 append_only=true met=true missing_frozen=0`), so the counter's
own output satisfies the contiguity test it applies to the ledger. That is a tautology: the diagnostic file
would be the evidence for the defect it diagnoses. The round's do-nothing control must stay red.

## C1 — the counter's own diagnostics are never receipts
For the C1 counter, files under `.ufo/waves/round-76/controls/` whose name matches
`base-c1-quote-truth*.txt` or `ctl-*.txt` are excluded from the receipt universe. The exclusion is by path
and name and applies on every measured revision (base, carrier, tip), so the before- and after-states are
measured on the same universe minus the same files.

Nothing else changes: receipts from earlier rounds (`round-75/controls/*`, including that round's own
`ctl-*` files) remain receipts, because they are the round-75 counters' outputs, not this round's, and the
repair legitimately quotes them.

The re-measured before-state under amendments 3 and 4 stays `findings=7` at `a0491fcd` (the exclusion cannot
change the base count: no round-76 control file exists in the base tree). The C1 target stays
`findings=0 append_only=true met=true`, exit 0, closed by the whole-line correction rows — now reachable
only with the repairs in place.
