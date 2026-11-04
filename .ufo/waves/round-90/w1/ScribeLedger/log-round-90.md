## Round 90 — 2026-11-04, three routed round-89 defects and a cache-key conformance gate

Motivation: the round-89 outside spot-check (`corpus/lessons/round-89-verifier-spotcheck.md`)
routed three defects (D89-1 untracked `baseclean.out` at the lane root, D89-2 the unreceipted
round-89 C1 statement at `f62e7954` whose item list contradicts its count, D89-3 the S463
scope cell against its construction use) and the instrument-calibration lesson: two
first-draft `met` verdicts in round 89 were falsified by the round's own attack seats.
Calibration is the lowest owned axis (2 HOLD); the round also takes an operability
capability move that answers R89-2, a counter that admitted non-conforming stubs.

Claims (frozen, `.ufo/waves/round-90/freeze.md`, freeze `4ee62b18`):
- C1 calibration: D89-1, D89-2, D89-3 close, counter `c90_defects.py`. Base `209027f4`
  `open=3 closed=0 met=false`, exit 1 (`controls/base-c1.txt`); carrier `e50c9566`
  `open=0 closed=3 met=true`, exit 0 (`controls/after-c1-carrier.txt`). D1's live
  working-tree conjunct makes that reading time-bound, not revision-bound.
- C2 operability (capability): `scripts/cache_key_conformance.py`, counter `c90_gate.py`
  over 4 pinned positives and 57 pinned negatives (15 round-89 ExecControls stubs,
  5 round-89 shortcut controls, 35 non-equivalent MutKey mutants, 2 round-90 sandbox
  negatives). Base `gate=absent … met=false`, exit 1 (`controls/base-c2.txt`); carrier
  `7f6c68f1` `positives=4/4 negatives_refused=57/57 false_admits=0 errors=0
  anti_table=ok population=ok seed=923161196 met=true`, exit 0
  (`controls/after-c2-carrier.txt`).

Controls before the freeze (`controls/run_controls.sh`): C1 do-nothing `open=3`, seven
forgeries (D1a, D1b, D2a, D2b, D2c, D3a, D3b) each `open=3 … met=false`, positive fixture
`open=0 closed=3 met=true` (`controls/ctl-c1.txt`). The first run is kept as
`controls/ctl-c1-v0-before-parse-fix.txt`: its positive fixture read `open=1 closed=2
met=false` because the counter took the quoted superseded `open=5 closed=1` as the
reading, and its D2b forgery was refused for that wrong reason ("receipt first line
disagrees") instead of the re-run; fixed before the freeze (round-90 lesson, Mistakes
row 3). C2 do-nothing, blanket-refuse (`positives=0/4`), blanket-admit, hash-table and
name-table gates (`false_admits=57` each), all `met=false`, exit 1 (`controls/ctl-c2.txt`).

Counter integrity, disclosed: the gate was developed after the freeze and before its
carrier commit; two gate defects were fixed in that window (sandbox denied stdlib
listing; a non-UTF-8 hand case decided a point the contract leaves open, moved to the
advisory line; lesson Mistakes rows 4 and 5). Counter, pin and frozen-negative bytes are
unchanged from `4ee62b18` to `79e1aac2`. Wave finding (`w1/ScribeLedger.md`): the frozen
`c90_gate.py` also returns `met=true`, exit 0, for a 16-line gate with no conformance
logic that strips the nonce trailer and admits the first four hashes in the pins file
read at run time (`w1/ScribeLedger/receipts/forgery-c2-pin-reading-gate.txt`). C2's
behavioural support is therefore the per-subject gate lines (four positives
`clauses=6/6 hand=70/70 generated=120/120 sandbox=ok`) and two held-out subjects outside
the pins (`w1/ScribeLedger/receipts/heldout-*.txt`), not the counter verdict.

Fixes on committed bytes: `baseclean.out` relocated byte-exact to
`.ufo/waves/round-90/inherited/baseclean.out`; appended correction tails in `SCORECARD.md`
and `LOG.md` cite `controls/r89-c1-at-f62e7954.txt` (the frozen round-89 counter, blob
`0dee1dc8`, re-run on a scratch clone at `f62e7954`: `open=5 closed=1`, only item E closed;
the count stands, the words "items B, C, D, E, F closed" do not); S463 stays byte-identical
and S467 opens `supersedes S463 —`.

Registry: S466 (RFC 9110 §5.5), S467 (RFC 9111 §2, §4.1; supersedes S463 for construction
ground), S468 (RFC 8259 §7, §8.1), all tier A, mined; 202 → 205 rows; knowledge 77 → 78
(`corpus/knowledge/cache-key-conformance-gate.md`). Census `validate --root … kake` exit 0
before (`controls/census-before.txt`, 26 × W04) and after (`controls/census-after.txt`,
29 × W04; the three new W04 are S466–S468). Mistake row 1 rejects the round-89 MutKey
claim that M37 is equivalent: `%` is a `tchar` (S465); the gate case `name-percent-absent`
refuses M37 (`clauses=5/6 hand=69/70`).

Wave shape: one v1 wave, 13 seats (ScoutGround, ScoutSources; ExecStubs, ExecSandbox,
ExecReplay, ExecTrial; MutGate, MutC1; ReviewC1, ReviewGate; CriticClaims; ScribeLedger;
ConnectorScope). Attack seats: mutation-tester 2, reviewer 2, critic 1 = 5/13. Dispatch:
`.ufo/waves/round-90/w1.ready`, dispatched `2026-11-04T19:14:24`, after the freeze commit
(`18:54:29 -0300`) and both carriers.

Routed: R90-1 non-UTF-8 input undecided by the contract; R90-2 NUL in a field value
(S466) kept by the candidate; R90-3 contract example 5 "raw" separators versus RFC 8259 §7;
R90-4 the key omits the request method (S467 §2). Carried: RC-1…RC-10 for the frozen
round-89 C1 counter; the round-89 L0 questions (lesson §Operator-decision queue).

Tools: none installed or upgraded (no pacman; no network beyond the three named RFC GETs
recorded in `corpus/lessons/round-90.md` §Gate).
