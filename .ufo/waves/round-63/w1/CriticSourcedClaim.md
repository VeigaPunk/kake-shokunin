# CriticSourcedClaim — round 63 w1

Seat: CriticSourcedClaim (critic, leaf; no subagent dispatch). Date: 2026-10-27.
Frozen claims, counters, receipts and corpus left untouched; only this report written.
No tools installed; no pacman; no git/jj mutations.

## Item

Attack the §2b sourced-claim duty: is re-opening a row that already exists (S432,
mined since round 61) genuinely "a SOURCES.md row opened this round"? Compare with
how rounds 61/62 recorded re-opens. Conclude whether the duty is met or whether the
round needs a genuinely new row.

## Verdict

**Duty met in substance — under a lane convention that a genuine re-open counts as
"opened this round" — but the textual conformance is genuinely vulnerable, and that
vulnerability must be named, not waved through.** The round does **not** need a
genuinely new row: the frozen contract's own no-harm clause precludes adding one,
and a forced row would be its own kind of violation. The smallest safe correction
is explicit naming of the convention in the round report plus ratification (or text
amendment) at non-author closure — detailed in §5 below.

This is a fixable defect (unwritten rule-reading), not yet a kill: nothing in the
frozen C1/C2 predicates or kill rules references §2b, and the evidentiary substance
the duty exists to guarantee is fully present and independently verified this round.

## 1. The duty text (unchanged across rounds)

`/home/vgpnk/Projects/shokunin/.ufo/prompts/kake-round-63.md:73-75` (byte-identical
in `kake-round-61.md` and `kake-round-62.md` — verified by diff; only the lesson
filename in §2b.3 differs):

> 4. **At least one sourced claim** — one of the round's claims rests on a
> `SOURCES.md` row **opened this round**: the knowledge entry or evidence it
> lands cites that `S###`.

The registry contract it binds to, `/home/vgpnk/Projects/shokunin/CORPUS.md`:

- line 105: `opened` — "ISO date the row's author opened the source."
- lines 112-115, rule 1: "A row is a claim. Write it only after **opening the
  source in the round that writes the row**. The round lesson's `## Gate` records,
  **for every new row**, the URL, the access date, and a ≤25-word quote …
  Non-author verification re-opens a sample."

## 2. The counterexample (strongest form of the attack)

S432's registry row was written in round 61, commit `d2da25de` ("round-61: integrate
sourced header audit…"). Command:

    git -C /home/vgpnk/Projects/shokunin/kake-shokunin log -S "S432" --oneline -- corpus/SOURCES.md
    → d2da25de round-61: integrate sourced header audit, rechecks, and w2 hardening; C1 withheld

`corpus/SOURCES.md:178` — the row exists with `opened 2026-10-27`, status `mined`,
used-by `corpus/knowledge/response-header-expectations.md`. Round 63 adds and
changes no row (frozen contract, "No-harm": "no registry row added or changed; the
S432 row's status/recheck/used-by cells untouched").

So on the strict reading of §2b.4 — "a `SOURCES.md` row **opened** this round" —
the row's one and only open, the act rule 1 couples to "the round that writes the
row", happened in round 61. Round 63's act on S432 is, by the lane's own vocabulary
in every artifact that describes it, a **re-open**, a different word for a different
act:

- `corpus/lessons/round-63.md` Gate: "**S432 re-open record (rule 1):**
  https://fetch.spec.whatwg.org/ opened 2026-10-27 …" — the header itself
  distinguishes re-open from the open rule 1 governs.
- `corpus/knowledge/response-header-expectations.md` [r63-correction]:
  "The source was **re-opened live this round**".
- The orchestrator's own dispatch (`.ufo/waves/round-63/w1-dispatch.json:276`)
  calls it "exactly one sourced claim resting on a row opened this round
  (**the S432 re-open**)" — the parenthetical concedes the two phrases are not
  synonyms and asserts the equivalence under attack here.

Two reinforcing points:

1. **Rule 1's coupling.** The contract ties "opening the source" to "the round
   that writes the row". Round 63 writes no row, so the round-63 open authorizes
   nothing; it verifies currency. Applying rule 1's header to the Gate record is
   the lane's interpretive claim, not the contract's text.
2. **No accepted precedent for a sole-re-open landing claim.** Every round where
   re-opened rows grounded a sourced claim also opened at least one genuinely new
   row in the same round (rounds 55, 56 — §3). The one round that cited an
   already-mined row with zero new rows was round 62 — whose claim never landed
   (unprovable). Round 63 is the first round in which a **landing, score-bearing**
   claim rests solely on a re-opened row. If "opened this round" means first-open,
   this is the lane's first outright §2b.4 failure, and the frozen contract
   contains no hedge against that reading (contrast the round-55 contract, §3).

## 3. Comparison with rounds 61/62 (and the 55/56 convention)

**Round 61** — the unambiguous case. S432 was a new row written after a fresh open;
the lesson Gate records it under "S432 — opened 2026-10-27 — §3.6 — quote …"
(`corpus/lessons/round-61.md:43`). Claim C1/C2 rested on new rows S430–S433.
§2b.4 satisfied on any reading.

**Round 62** — the same S432 re-open, claim failed. `corpus/lessons/round-62.md:3`:
"Source S432 was **re-opened** this round at https://fetch.spec.whatwg.org/ on
2026-10-27"; line 23: "No SOURCES row was added or changed; the already-mined S432
row was **opened again** and cited by the claim." The round-62 report
(`/home/vgpnk/Projects/shokunin/.ufo/reports/round-62/kake.md`, Sources & frontier)
repeats "S432 was **reopened** and cited by the round's claim evidence". Because C1
was ruled unprovable (marker-only false-green), §2b.4 never had to carry a landing
claim, and the report recorded the re-open neutrally — it is precedent for the
*record-keeping*, not for re-open = opened on a scoring round.

**Rounds 55/56 — the convention's source, and its limit.** These are the only
rounds where re-opened rows were explicitly counted toward the sourced-claim duty:

- `corpus/lessons/round-55.md:24`: "These are the sourced claim's rows: C2 rests on
  S418 (**opened this round**) and on S372/S373 (**re-opened this round**)."
  Round-55 contract line 62: "C2 rests on three rows opened this round (S372, S373
  re-opened; S418 new)". Note both phrasings keep "opened" and "re-opened"
  *distinct* and lean on the genuinely new S418.
- `corpus/lessons/round-56.md:12`: Gate header "Rows **opened or re-opened** this
  round" — again with two new rows (S419, S420) alongside the re-opened S367.
- Non-author acceptance: `corpus/lessons/round-55-verifier-spotcheck.md:49`
  records "freshness (C2) | improved | three new/re-verified entries on rows
  opened or re-opened this round, quotes true, digests equal live today" — the
  outside verifier treated "opened or re-opened" as conformance language.

So the lane convention is real and was accepted once by a non-author verifier —
but in both accepted cases a new row existed, and the convention was always spelled
out ("opened or re-opened"), never asserted as "re-open = opened". The strict
counterexample of §2 has not been rebutted by precedent; it has been avoided by
never before resting a sole re-open under a landing claim.

## 4. What round 63 actually has (the substance the duty protects)

The evidentiary content §2b.4 exists to guarantee — that the claim's source was
genuinely opened this round and the landed entry cites the row — is fully present
and independently verified:

- Fresh open this round: `curl -sS --max-time 30 https://fetch.spec.whatwg.org/`
  → `HTTP 200 bytes=1854393` (`.ufo/waves/round-63/w1/ScoutS432Reopen.md`,
  independent seat evidence). Committed receipt
  `.ufo/waves/round-63/sources/S432.live.html` sha256
  `63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b` — verified
  byte-identical to the round-61 retained body (`sha256sum` run above, both files).
- Gate record supplies all three rule-1 fields plus digest evidence; quote
  ("response header can be used to require checking of a response's Content-Type
  header against the destination of a request") verified at raw lines 6150–6154 of
  the retained HTML (`sed -n '6150,6154p'`, run above).
- The landed knowledge entry's [r63-correction] cites the S432 row's retained blobs
  and records the live re-open; C1's frozen `source_row` component requires the S432
  registry row and reads it at the measured revision (after receipt:
  `source_row=1`).
- Mechanical reading: the registry's only machine-checkable expression of "opened"
  is the `opened` cell, which reads `2026-10-27` — today's date. By the column's
  own semantics S432 displays as opened this round; the failure only appears when
  "this round" is read as round-number rather than date, and the duty text does not
  say which.

## 5. Conclusion and smallest safe correction

**Conclusion.** On the lane's recorded convention — accepted by the round-55
non-author verifier — the duty is **met**: C1 rests on S432, the entry and evidence
cite S432, and S432's source was genuinely (re-)opened this round with committed,
digest-verified evidence. On the strict textual reading — "opened" = the act rule 1
couples to writing the row, which for S432 happened in round 61 — the duty is
**not met**, and no precedent saves it, because every prior acceptance included at
least one genuinely new row.

**The round does not need a genuinely new row**, for two independent reasons:
(i) the frozen contract's no-harm clause ("no registry row added or changed")
precludes adding one this round; (ii) CORPUS.md rule 2's correction shape (`a new
row whose teaches opens supersedes S0NN`) does not apply — the S432 row is not
wrong, so a supersede row would be deadweight and a same-URL duplicate row would
trip the census W04 duplicate-URL class the registry already warns about.

**Smallest safe correction (fixable defect):**
1. The round-63 report's Sources & frontier section must state the reading
   explicitly — "C1's sourced claim rests on S432, re-opened this round (fresh GET
   2026-10-27, digest-verified), under the round-55/56 convention that re-opened
   rows satisfy §2b.4" — rather than the dispatch's bare parenthetical.
2. The non-author closure must ratify or reject that convention for sole-re-open
   rounds. If rejected, record a §2b conformance defect against round 63 (the C1/C2
   verdicts stand on their own frozen predicates; §2b is conformance, not a claim
   leg) and route the text fix to a future round: amend §2b.4 to "opened **or
   re-opened** this round", which is what rounds 55/56 already assumed.
3. No retroactive registry edit, no new row, no counter change.

## Impacted axes

- **Conformance/report integrity** (the §2b frontier-step duty): the attack's
  target; vulnerable as shown, fixable by naming + ratification.
- **Calibration (C1)**: conformance context only. C1's frozen predicate, kill rule
  and receipts contain no §2b reference; a §2b defect does not make C1 unprovable
  and does not affect the `met=true` after-receipt or the marker-fixture controls.
- **Operability (C2)**: untouched; the claim rests on the committed tool, not on
  the registry.
- **Expansion trend**: round 63 admits no new row and no new entry; expansion is
  unchanged, consistent with the round-62 precedent for correction-only rounds.
