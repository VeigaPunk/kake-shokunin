# DRAFT — LOG.md `## Round 89` entry (ScribeLedger, wave 1)

Measured at lane HEAD `acc69ba5`; L1 re-measures at its carrier. Replaces the landed entry at
`LOG.md:3029` (commit `28532540`) where the two differ. Corrections: the landed entry stated
the C1 result as `open=5 closed=1` (a pre-marker reading; the carrier reads `open=1 closed=5`);
it understated the C2 admitted set; it counted six real trial cases where the trial table has
seven; and its wave-shape line did not say what is on disk.

## Round 89 — 2026-11-04, six routed round-88 defects, a conservative cache-key constructor, and two unadmitted claims

Motivation: the round-88 outside spot-check routed six defects (R88-A…F: stale selftest count,
Gate sample miscount, unbacked re-run claim, unpinned count, freeze after dispatch, lesson shape).
Calibration is the lowest owned axis (2 HOLD). The round also takes a freshness capability step on
the Vary ground round 88 opened: construction of the stored-response key, the half of RFC 9111 §4.1
that round 88 left open.

Claims, as frozen in `.ufo/waves/round-89/freeze.md` (freeze `08ab46a1`):

- C1 calibration: six routed defects close, counter `c89_defect_queue.py`. Base receipt
  `controls/base-c1.txt` `open=6 closed=0 met=false`, exit 1. At `acc69ba5` the same counter prints
  `open=1 closed=5 met=false`, exit 1; item A stays open (untagged `22/22` at SCORECARD 5469 and 5488
  and round-88 lesson 265; the counter requires an in-line tag, which the append-only rule forbids
  on filed bytes; routed R89-1 and RC-5/RC-6/RC-7). Not admitted. Re-running the same counter at the
  base revision now prints `open=5 closed=1`, because item E reads HEAD rather than `--revision`
  (RC-1; `controls/c1-base-revision-control-at-acc69ba5.txt`). The frozen base line is reproducible
  only at freeze time.
- C2 freshness: conservative Vary-nominated cache-key construction, counter `c89_key.py`. Base
  candidate absent, `met=false`, exit 1. Integrated `scripts/cache_key.py` (sha256 `3a658326…`)
  `frozen=16/16 props=200/200 refuse=9/9 controls=5/5 met=true`, exit 0 under the committed v2 counter
  (`controls/c2-carrier-v2.txt`, re-run `w1/ScribeLedger/receipts/c2-v2-at-acc69ba5.txt`) and under
  the frozen v1 counter (`controls/c2-carrier-frozen-v1.txt`, re-run
  `w1/ScribeLedger/receipts/c2-frozen-v1-at-acc69ba5.txt`). Not admitted: the instrument accepts
  non-conforming candidates (seven of ten adversarial probes in `w1/ExecControls.md`; values
  stripped of all whitespace where the contract trims SP and HTAB only, and a URI without
  escaping, both at four seeds, and a 421-entry table, in `w1/CriticClaims.md`;
  runtime, alias, `file://` and environment imports, a hybrid literal table and a guard bypass in
  `w1/ReviewCounterC2.md`; 27 of 37 mutants killed with seven real survivors in `w1/MutKey.md`).

Counter integrity, disclosed: freeze v2 `46a43e94` changed the C2 shortcut guard after dispatch
`2e700b9a`, to remove a false positive on a correct candidate's docstring. The verdict holds under
both versions, but the frozen claim text "frozen before any after-state data" is true of the claim
and false of the counter file, and item E cannot see the change (RC-2). The C2 base receipt was
regenerated in place by that commit; the freeze-time bytes are restored as
`controls/base-c2-freeze-v1.txt`. The wave review's findings are in
`corpus/lessons/round-89.md` §Wave review.

Wave shape: one v1 wave, 14 seats (ScoutGround, ScoutRFC; ExecKey, ExecDefects, ExecTrial,
ExecControls; ScribeEntry, ScribeLesson, ScribeLedger; ReviewCounterC1, ReviewCounterC2; CriticClaims;
MutKey; ConnectorScope). Attack seats: reviewer 2, critic 1, mutation-tester 1 = 4/14 (28.6%). L1
holds the planner seat (the validator forbids a planner swarm role). Settlement is not verifiable from
the wave directory: there is no results JSON and no wave-done receipt; ten seat reports are on disk,
ScoutRFC has receipts only, ScribeEntry's directory is empty, and ScribeLesson has no output on disk
(its lesson text is in `corpus/lessons/round-89.md`, which names no seat author). L1 also drafted
the knowledge entry and the reference candidate before the seat reports landed; seat drafts were
compared, not silently adopted.

Actual domain work: recorded `Vary` values from the round-61 and round-81 captures through the
committed candidate (`w1/ExecTrial.md`). Seven real surfaces (R1, R2, R2b, R3, R4, R5, R6), no
recorded `*`, five synthetic refusals (X1–X5). The committed candidate reproduces the ExecTrial
reference on all twelve cases: key, exit and stderr identical (`w1/ScribeLedger/receipts/trial-committed-results.json`).
Real-data refusals: zero of seven. Keys establish construction over recorded header lines only; they
show nothing about what any server, CDN or browser stores. The driver joins duplicate `Vary` lines with
`, ` (RFC 9110 §5.3). The contract does not say so, and seven of the twelve round-61 captures carry
duplicate lines (D1, routed).

Assimilation: none — `merge/kake` still collides on eight ids (S312, S329, S367, S372, S373, S374,
S390, S409), re-derived in `.ufo/waves/round-89/assimilation/`. The round adds S464 (RFC 9111 §4.1) and
S465 (RFC 9110 §5.6.2, §5.6.1.2) as tier-A rows; registry 201→203 rows, no existing row edited.
`considerthese/2026-10-26.md` proposal 5 was already adopted at r66 (`corpus/knowledge/gate-status-ledger.md`
header); none of its other proposals is taken this round.

Adjacency: `mori-shokunin` holds a one-line RFC 9111 §4.1 Vary rule (round 88 S594) and a
`ua-serving-normative-r79` entry that cites §4.1 for observability and disclaims key construction
(`w1/ConnectorScope.md`). Twenty sibling lanes were searched read-only; the other cache-key hits are
local caches unrelated to HTTP. The overlap is reported, not absorbed.

Tools: none installed or upgraded in this round's scribe work (git and python3 only; no pacman, no
network GET beyond the two named RFC bodies in the lesson's §Gate).
