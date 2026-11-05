# Round 95 — kake: self-assessment repair under a frozen instrument, and conditional_eval contract v2

Round base `fdd5fdbeb8a2ba6c18f0f23135d1bee98068dca3`; instruments commit
`43cdd9fc899a2613d8ba7b55edf820825e57b4d1`; freeze
`8f638b591e739e1863f5fa22334d5e15178189ed`; integrity-ruling restoration commit
`4f443b3fd79f88fc75cfe46005c01d3ecd85c16f`. Wave `w1`: 12 seats
(`.ufo/waves/round-95/w1-dispatch.json`). Freeze and its govern rule: the
round's counters, predicates and targets were frozen before any seat scored;
`Amendment A` (below) was withdrawn from scoring on the orchestrator integrity
flag and the frozen bytes were restored.

## Gate

Candidates considered and their decisions.

- **Row S479 (RFC Editor errata search for RFC 9110) — admitted.** One GET
  (2026-11-05T16:32:51Z, HTTP 200 after one 302, 97 741 bytes, sha256
  `e6ddebb240b522f36acf0ccc9b6a52030a35ff77d17203dbd1fcf6d1339c0911`,
  `w1/ScoutErrata/fetch.txt`); located quote (21 words, exact substring of the
  raw body at line 863, inside EID 9164): "Each is semantically equivalent
  ABNF, so no interoperability question arises: the collected grammar and the
  body define the same language throughout." No verified or reported erratum
  targets sections 5.6.1.2, 5.6.3, 8.8.3 or 13.1.x at fetch. Census with the
  row: exit 0 (`w1/ScoutErrata/census-validate-with-s479.txt`). The row's
  first-drafted `used-by` (freeze.md only) was **rejected** and corrected: the
  census's E11 needs the used-by paths to exist, and the row's real consumers
  are the knowledge entry and this lesson.
- **Knowledge entry `corpus/knowledge/conditional-list-membership.md` —
  admitted.** Quotes verified byte-exact against the retained RFC 9110 body
  (`w1/ScribeEntry/verify-quotes.py`: violations 0); ground: contract v2
  clauses C1–C5 with RFC-exact and lane-convention clauses labeled; cites
  S478, S455, S034 and S479.
- **ExecC1Repair's 15-row file choices (R94-5) — admitted with recorded
  deviations.** Every chosen token is a committed non-empty regular blob at
  base (`w1/ExecC1Repair/repairs.md`, cat-file evidence per row). Deviations:
  the seat-spec candidate `.ufo/waves/round-85/w1/ExecRegistry/registry-rows.mjson`
  does not exist at base, replaced by `c1-base.json`; row 1588's brace group
  was collapsed to one blob token with the directory moved to prose. The
  freeze requires a non-author review of the rows: CriticClaims' X-route
  receipts (below) plus the outside closure carry it; a residual row-by-row
  re-read is owed by the closure.
- **ExecC2V2's v2 candidate diff — rejected for landing, kept as
  corroborating evidence.** The L1 had landed its own v2 candidate
  (`scripts/conditional_eval.py`, selftest 99/99, hand 66/66, generated
  120/120, forgeries 7/7, mutants 40/40) before the seat's diff arrived;
  the seat's independent implementation reached the same population verdict
  (`w1/ExecC2V2/scoring-v2.txt`: `DRIVER VERDICT met=true`), which stands as
  the second implementation agreeing with the frozen reference. One
  implementation lands; both are wave evidence.
- **Amendment A — rejected by the integrity flag.** CriticClaims-67 and
  SentinelScope-30 F1 flagged that after the freeze the C1 counter and
  surfaces had changed digest (commit d9be693f). Ruling: a post-freeze
  instrument edit cannot score C1. Option (b) chosen, with option (a)'s
  mechanics: the frozen bytes (counter `8fd27d62…`, surfaces `00a04c9a…`,
  `controls/base-c1.txt`, `controls/ctl-c1-selftest.txt`,
  `controls/instrument-sha256.txt`) were restored byte-exact at
  `4f443b3f`, verified (`controls/restore-verify-c1-selftest.txt`: selftest
  13/13, battery 20/20, admit 5/5; `controls/restore-verify-c1-base.txt`: the
  base control reproduced line-1-identical at `fdd5fdbe`), and no receipt
  produced with the amended counter is integrated anywhere.
- **considerthese: `considerthese/2026-11-05.md` proposal 3 (held-out vs
  frozen divergence column) — admitted** as QUALITY.md criterion R95-D below,
  grounded by the round-90/92 divergence record the proposal itself cites
  (frozen 4/4 and 57/57 beside held-out 14/23, 6/20, 7/7 at the carrier), with
  the criterion shown able to fail on that historical record.
- **Assimilation: none.** `merge/kake/SOURCES.append.md` was not adopted; the
  id-collision guard was re-derived this round
  (`.ufo/waves/round-95/assimilation/{reg-ids,staged-ids,collisions}`:
  129 staged ids, 8 collisions, unchanged from rounds 92–94). Note:
  ConnectorScope looked for `merge/kake/doctrine` under the fleet root; the
  package lives under `/home/vgpnk/Projects/shokuknow/merge/kake/` — no
  adoption turned on it either way.

Spot-check: the outside non-author closure of this round is owed; the lane
does not self-certify. Attack seats are lane seats (ReviewC1, ReviewC2,
CriticClaims, MutC1, SentinelScope) and are not the closure.

## Mistakes

| # | Class | Evidence | Captured-by | Fix (shown able to fail) |
|---|---|---|---|---|
| 1 | Instrument governance: the C1 identity surface was edited after the freeze commit and the round's own seats flagged it | `4f443b3f` ancestors: d9be693f changed `c95_selfassess.py` 8fd27d62…→04be4a7d… and `frozen/c1-surfaces.json` 00a04c9a…→9eff04c5… after freeze `8f638b59`; flag relayed by the orchestrator from CriticClaims-67 + SentinelScope-30 F1 | the wave seats' digest verification against the freeze (and the orchestrator integrity flag); none of the frozen controls caught it, because the controls were re-stamped with the amended bytes | option (b): frozen bytes restored byte-exact (`4f443b3f`), restore-verification receipts committed, amended receipts never integrated; the restore-verify base control reproduces the frozen base control line-1-identical, which is the check that can fail again |
| 2 | Instrument design: the frozen identity pinned each knowledge entry's first-eight-line digest, but the declared E3 repair route (in-file head corrections) changes exactly those lines, so the frozen C1 counter cannot certify its own claim's repair | `controls/restore-verify-c1-base.txt` (mismatches=18 under frozen bytes); the landed-tip receipt shows `pins=identity` with `entry-content` findings once the three E3 repairs land — `met=false` either way | none at freeze time: found by claim rehearsal after the wave was dispatched; the freeze's own do-nothing control could not distinguish the two designs | the successor C1 counter must pin entries by presence and freeze BEFORE dispatch (round 96); this round reports C1 unmet honestly under the frozen rule instead of widening the instrument |
| 3 | Inherited (R94-8): the round-93 mutant driver's `base_rev 191dd0ed…` names an uncommitted worktree state that is absent from the lane (`git cat-file -t` fatal) | `.ufo/waves/round-93/w1/recovered-partial/MutConditional/posgood-out/mutants.json` line 7; also cited in round-94 wave evidence (`w1-results.json`, `CriticClaims/git-and-digests.out`) — historical files, not edited | none in rounds 93–94; surfaced by the round-94 closure item 5 and ExecReceipts' sweep | the erratum (`w1/ExecReceipts/erratum-r94-8.md`): the pointer is unrecoverable from this lane; the scored bytes are pinned exactly in `frozen/c2-population.sha256` (pos-good blob `e78f2845…`, `mutants-posgood.json` `f15c99f4…`), and the round-95 counter exits 2 on any digest drift — QUALITY criterion R95-B |
| 4 | Seat-spec defect: a named candidate file did not exist at the base revision | `w1/ExecC1Repair/repairs.md` note 2 (`registry-rows.mjson` absent at `fdd5fdbe`) | the seat's own `git cat-file` evidence command | choices re-anchored to existing blobs (`c1-base.json`); spec authors must cat-file candidate paths before naming them |

## Routed to round 96

- **R95-1**: the successor C1 counter pins knowledge entries by presence
  (heads are correctable surfaces), freezes BEFORE dispatch, and re-declares
  the E3 repair route so the frozen predicate and the frozen pins agree.
- **R95-2**: the kill-predicate definitions differ across lanes (kumitate K43
  requires rerun stability; tabi declares equivalence at catalogue time; kake
  requires digest-pinned equivalence receipts) — `w1/ConnectorScope/overlaps.md`
  rows 4–5; a fleet-level decision is owed; kake adopts neither silently.
- **R95-3**: chousa criterion 146 (round-79) is the prior art for R94-3's
  repair-naming rule — cite, do not port (`overlaps.md` row 2).
- **R95-4**: the row-by-row non-author re-read of the 15 repaired SKILL.md
  rows beyond CriticClaims' X-route coverage is owed by the round closure.
- **R95-5** (ReviewC1): 27 routes refused; three new false-green shapes —
  NG01, NG08, NG11 (`w1/ReviewC1/ReviewC1.md`, `route_runs.txt`) — are
  admitted-shape on synthetic lanes (refused there only by cardinality pins,
  which are `ok` on the real lane). The successor counter must close them as
  class rules.
- **R95-6** (ReviewC2): the frozen C2 reference has two RFC-exact deviations
  unobservable in the frozen population — R1 the reference over-refuses a
  comma inside an opaque-tag where the candidate is RFC-exact, R2
  If-Unmodified-Since under OPTIONS evaluates 412 against the §13.2.1 ignore
  reading; contract C5 must pin the reading (`w1/ReviewC2.md`, grid 30/30).
- **R95-7** (SentinelScope): the C2 sandbox is escapable — in-tree symlinks
  are trusted (`abspath`, not `realpath`) and `os.execv` is unaudited, so a
  candidate can read the counter reference end-to-end (`sentinel.md` x01–x03);
  the C2 counter has no effectful-shadow defense (R94-2 was implemented for
  C1 only); C1's sys.path sanitization does not cover PYTHONPATH shadows from
  a non-script directory; and the frozen C1 docstring's "python3 -I" sentence
  is false for the frozen `-B` command. All four are successor-counter items.
- **R95-8** (CriticClaims): the C2 anti-table digests hand inputs only — a
  memorizing lookup-table candidate over hand + generated cases passes met;
  the successor anti-table must digest generated inputs too. The mutant-kill
  rule is circular as validation (v2 semantics kill v1-semantics mutants;
  M11, M19, M20, M33, M40) — the RFC grounding and digest pinning stand
  against it, and both sides are recorded.
