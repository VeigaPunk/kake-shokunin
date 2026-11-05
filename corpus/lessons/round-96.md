# Round 96 — kake: the R95-1 successor self-assessment counter, and a revalidation-exchange instrument whose frozen counter crashed before scoring

Round base `bde9869144f69c5a459c0d2c93f5135922fe3a8d`; instruments commit
`7ae3e9b07e2435f7fde6e73838d9fa14488b8dda`; freeze commit
`049e8eca2f0fa5e981232eb4efe367357dce578c` (frozen before the wave);
integration commit `7dc9bf43b6bd6ddae741f5b3af1d7e4224990428`. One v1 wave,
12 seats, dispatched 2026-11-05T15:16:55 through the inline spawn handoff
(`.ufo/waves/round-96/w1-dispatch.json`, results `w1-results.json`): all 12
seats settled, no dead seats.

## Gate

Candidates considered and their decisions.

- **Row S480 (RFC 9111 §4.3.1/§4.3.3 validation exchange) — admitted.**
  One GET by ScoutRFC (2026-11-05T18:17:11Z, HTTP 200, 84 477 bytes, sha256
  `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`,
  `w1/ScoutRFC/fetch.txt`) — byte-identical to the retained round-93 body
  (`cmp` rc 0). Six clause quotes located at the named plain-text lines
  (848, 852, 861, 935, 938, 944; `w1/ScoutRFC/s480-row.md`). The row lands
  `mined` with used-by naming the knowledge entry and this lesson; census
  exit 0 at the final tip (216 → 217 rows; the W04 duplicate-URL warning
  class is pre-existing and named in the report).
- **Knowledge entry `corpus/knowledge/revalidation-exchange.md` —
  admitted.** Provenance trio first (source: S480 + anchor lines 812-949;
  verified-at 2026-11-05; recheck 180d); 13 located quotes verified by the
  seat's `verify-quotes.py` (violations 0; `w1/ScribeEntry/quotes-verified.txt`);
  cites S480 plus the re-read rows S456 and S476; exclusions paragraph names
  storage, keys, freshness lifetimes, serving, the merged 304 field set and
  every live-cache claim as out of scope.
- **Gate-registry rows for `c96_selfassess.py` and `c96_reval.py` —
  admitted** (R94-9 pattern; append-only after the `c95_conditional.py`
  row, SKILL.md lines 219-220). ExecRegistry resolved every named path at
  the freeze tip (`w1/ExecRegistry/resolution-receipts.txt`; rows=2,
  resolved=8/8).
- **`scripts/reval_exchange.py` (the C2 candidate, authored by ExecReval) —
  admitted as landed work, credit withheld.** The tool runs and decides
  correctly: the seat's own scoring reached the selftest receipt
  (`selftest 7/7 … 14/14 … anti_table=ok`, rc 0), and ReviewReval's
  independent 24-case grid agrees 24/24 with zero tool, contract or
  reference defects (`w1/ReviewReval/grid.md`, non-overlapping cases
  receipted). The frozen counter could not score it this round: the
  candidate-present path crashes with `NameError: name 'mutants' is not
  defined` (Mistake 1), so C2 reports unmet and the Capabilities row does
  NOT enter this round (the round-64 precedent: the tool first ran in
  round 63 and credit was withheld until a counter pass). The candidate's
  digest is `192b3bf7596abad8ef76a7a8262ecc29c0d565587153547ee61b5ee7566c7212`.
- **QUALITY criterion R96-A — admitted** (selftest/main code-path parity,
  with the chousa round-79 criterion 146 prior-art citation required by
  R95-3 — cited at the sibling's current HEAD, never ported). Grounded by
  the round's own crash receipts; shown able to fail by those receipts.
- **The C1 successor counter certifies the lane — admitted as the C1
  claim's working state.** At the integration tip the successor reads
  `pins=ok mismatches=0 battery=23/23 admit=5/5 shadow=absent
  predecessor_admits=6/22 ng_pred_admits=3/3 met=true` exit 0, while the
  frozen round-95 counter at the same revision reads
  `pins=identity met=false` — the routed R95-1 defect (a predicate whose
  entry-content pins forbade its own repair route) is closed: entries are
  presence-pinned from the freeze, the E3 repair route is reachable, and
  the NG01/NG08/NG11 shapes are refused as class rules with the predecessor
  admitting all three (liveness).
- **Assimilation: none.** The id-collision guard was re-derived this round
  (`w1/ExecReceipts/assimilation/{reg-ids,staged-ids,collisions}`: 217
  registry ids, 129 staged ids, 8 collisions — unchanged from rounds
  92-95); nothing adopted.
- **R95-2 — routed to the operator as an L0 question** (fleet
  kill-predicate arbitration; kumitate K43 rerun stability vs tabi
  catalogue-time equivalence vs kake digest-pinned receipts, re-verified at
  current sibling HEADs by ConnectorScope, `w1/ConnectorScope/overlaps96.md`).
  Kake adopts neither sibling default silently.
- **Spot-check:** the outside non-author closure of this round is owed; the
  lane does not self-certify. Attack seats (ReviewC1, ReviewReval,
  CriticClaims, MutReval, SentinelScope) are lane seats, not the closure.

## Mistakes

| # | Class | Evidence | Captured-by | Fix (shown able to fail) |
|---|---|---|---|---|
| 1 | Instrument governance: the frozen C2 counter's main scoring path crashes on every candidate-present run while its selftest passes | SentinelScope F1 (r08: five candidate variants incl. the frozen positive control, each rc=1 `NameError: name 'mutants' is not defined` at `c96_reval.py:624`) and CriticClaims C2-01 (committed candidate in a scratch clone; same crash); the selftest receipt `controls/ctl-c2-selftest.txt` is green because only `selftest()` binds the population list | none at freeze time: the pre-freeze selftest exercises a different code path than the main scoring path; the freeze's pre-scoring controls ran the counter only where the candidate is absent (base-c2.txt), so the crash was unreachable before data | Routed R96-1 (round 97: bind `mutants` in `main()` exactly as `selftest()` does). The criterion this lesson produces — `corpus/QUALITY.md` R96-A — demands the main path of the frozen counting command execute end to end on a committed positive-control candidate BEFORE the freeze; it fires on this round's r08/C2-01 receipts (the red state is this round itself). The frozen bytes are not amended (round-95 Amendment-A rule): C2 reports unmet honestly |
| 2 | Reference-drift: the round-95 freeze bytes still carry Amendment A's post-amendment digest instruction with the superseded digests | `.ufo/waves/round-95/freeze.md` (filed bytes, never rewritten) still says "every post-amendment check must hash the values above" over `04be4a7d…`/`9eff04c5…` (grep receipt `w1/ExecReceipts/freeze-supersession.md`); the authoritative scoring digests are `8fd27d62…`/`00a04c9a…` restored at `4f443b3f` | the round-95 closure routed it (spot-check item 6); no lane criterion covered filed-instruction drift | The supersession note in `w1/ExecReceipts/freeze-supersession.md` is integrated into this lesson: a reader is pointed to `.ufo/waves/round-95/controls/instrument-sha256.txt` and the `4f443b3f` ruling receipt set; filed bytes stay untouched |
| 3 | Stale-premise: the C1 freeze's do-nothing sentence ("the do-nothing lane stays uncertifiable") reads as contradicted by the committed successor-at-base control, because it does not name WHICH instrument set defines the do-nothing lane | CriticClaims C1-01 (`w1/CriticClaims/claims.md`): the predicate "successor met=true AND predecessor met=false" is satisfied at the base by the round's own work product; the committed `controls/c1-successor-at-base.txt` is the claimed work scoring itself, not a do-nothing lane | the §9 no-work-control rule names the control but not the instrument set that scores it; the critic's reading is recorded, not adopted | Round-97 freezes must state the do-nothing control as "the instruments the lane holds without this round's work, scored at the same revision" (here: the predecessor `met=false`), and name any self-scored control as claimed work. C1 is reported met on its frozen predicate with this wording defect recorded; the closure owns admission |

## Routed to round 97

- **R96-1** (Mistake 1): the successor C2 counter binds `mutants` in
  `main()` (the selftest's binding), and its freeze proves the main path
  end-to-end on a committed positive-control candidate (R96-A). The landed
  candidate `scripts/reval_exchange.py` (`192b3bf7…`) is ready to score.
- **R96-2** (CriticClaims C2-02..C2-07, counterfactual probe receipts): the
  anti-table misses raw-JSON-keyed lookup tables, base64-encoded digests,
  every-second-hex digests, minified-JSON digests and positional seed-order
  answer tables; the successor must digest canonical AND minified AND
  re-encoded input forms, and pin refusal diagnostics so one refusal cannot
  stand for another (MutReval N05/N06/N07/N08/N11 refusal-coarseness
  class; `w1/MutReval/new-mutants.json` carries the recipes).
- **R96-3** (ReviewC1, `w1/ReviewC1/routes.md`): four new false-green
  shapes on the C1 counter — RX01 decision tokens only inside HTML
  comments, RX02 only inside fenced code, RX03b an entire Gate inside a
  fence, RX09 a subdir lesson whose round number hijacks the >= 96 rule —
  plus the absence-annotation laundering route (CriticClaims C1-02), the
  two-token vocabulary-stuffing route (C1-03) and the `git replace`
  substitution route (C1-05; the counter must pin `GIT_NO_REPLACE_OBJECTS=1`
  for its git reads).
- **R96-4** (SentinelScope F2/F3/F4): the C1 counter resolves `git` from
  PATH (a PATH-shadowed wrapper executes); sandbox-unaudited vectors
  (`os.kill(ppid, 0)`, outside metadata listing) are named; the C2 sandbox
  has no effectful-shadow defense (R95-7's C2 side, now demonstrated).
  Carried with R95-6 and R95-7's remaining C2 items to the conditional and
  revalidation counter successors.
- **R95-2**: the L0 question is filed with this round's report; adoption
  waits for the operator's arbitration.
- **R95-6** (conditional_eval reference deviations R1/R2) and the rest of
  R95-7's C2 side stay routed to that counter's next successor; this round
  did not amend that frozen instrument.

Capability note: `scripts/reval_exchange.py` runs and is independently
verified (ReviewReval 24/24, reference_agree 22/22 on dict cases), but the
Capabilities row does not enter this round — no frozen-counter pass exists
(Mistake 1), and rows enter only through a demonstrated pass in the round
report. Round 97's successor counter scores the landed candidate.
