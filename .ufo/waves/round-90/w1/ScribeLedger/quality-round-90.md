## Round 90 — a counter's `met` is admitted only for the refusals it has been seen to make

Grounding: `corpus/lessons/round-89-verifier-spotcheck.md` (routed item: two first-draft
`met` verdicts in round 89 were falsified by the round's own attack seats — RC-1…RC-10 on
the C1 counter, and seven non-conforming stubs scoring `met=true`,
`.ufo/waves/round-89/w1/ExecControls/scoring-receipt.txt`); `corpus/lessons/round-90.md`
Mistakes row 3. Admit a counter's `met` only when receipts committed before the freeze
show: (1) a do-nothing control at the base scored `met=false`; (2) for every item, at
least one forgery whose printed reason for that item names the conjunct the forgery
targets — a forgery refused for some other reason is not a witness; (3) a positive
fixture reaching `met=true`, so blanket refusal is not read as rigour. When the only
positive is the claimed artifact itself (a capability counter), (3) becomes a blanket-refuse control that fails on the
positive subjects, plus a forgery that knows the scored population (names, hashes,
pins, labels) but holds no domain logic; if that forgery reaches `met=true`, the `met`
is reported as not discriminating and the claim rests on per-subject behaviour and
held-out subjects, never on the verdict. List every conjunct with no forgery as an
unwitnessed limit beside the `met`; do not call the counter sound beyond its witnesses.
Able-to-fail witnesses: `.ufo/waves/round-90/controls/ctl-c1-v0-before-parse-fix.txt`
(the positive fixture stayed `open=1 closed=2 met=false` and exposed the quoted-value
parse defect before freeze; its D2b forgery was refused as "receipt first line
disagrees", the wrong reason, which (2) rejects) and
`.ufo/waves/round-90/controls/ctl-c1.txt` (do-nothing `open=3`, seven forgeries
D1a–D3b each `met=false` with their own reason, positive `open=0 closed=3 met=true`).
Unwitnessed C1 conjuncts in that receipt: `baseclean.out` tracked at the lane root, an
untracked correction receipt, the `LOG.md` prefix check, the retained RFC 9111
digest, and each separate condition on the superseding row (rfc9111 URL, `mined`, scope
cell) beyond the do-nothing reading. The capability clause is grounded on
`.ufo/waves/round-90/w1/ScribeLedger/receipts/forgery-c2-pin-reading-gate.txt`: a
pin-reading gate with no conformance logic reaches the frozen C2 counter's
`met=true` (exit 0); the hash-table control in `controls/ctl-c2.txt` hashed the
nonce-altered bytes and failed with `false_admits=57`, so it never tested a forgery that
undoes the nonce.
