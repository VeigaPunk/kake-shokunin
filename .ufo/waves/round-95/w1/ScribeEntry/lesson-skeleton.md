# Round 95 — kake: contract v2 for the conditional-request counter, and the strict self-assessment counter's own battery

Lane HEAD at round open: `fdd5fdbeb8a2ba6c18f0f23135d1bee98068dca3`. Round freeze
commit: `8f638b591e739e1863f5fa22334d5e15178189ed` (`.ufo/waves/round-95/freeze.md`).
Instruments commit: `43cdd9fc899a2613d8ba7b55edf820825e57b4d1`. Wave `w1`, 12 seats,
dispatch `.ufo/waves/round-95/w1-dispatch.json`.

> **SKELETON — the L1 finalizes this file.** The `## Gate` decisions below are
> `DRAFT` lines carrying the candidate entries; the L1 turns each into an
> admit/reject decision with its evidence and replaces the `DRAFT` marker. The
> two `## Mistakes` rows are seeded from what the round has already produced
> and are already in final wording; the L1 appends the remaining rows as the
> wave's seats report. Nothing here is a verdict of the lane's gate.

## Gate

Candidates considered and their decisions.

- **DRAFT — knowledge entry `corpus/knowledge/conditional-list-membership.md` — admit.** The entry
  grounds contract v2's clauses C1–C5 on rows S478 (RFC 9110 §5.6.1.2 and §5.6.3),
  S455 (RFC 9110 §8.8.3), S034 (RFC 8259 §4) and the round's own pending row S479
  (the RFC Editor errata page for RFC 9110). Every quoted fragment is an exact
  byte substring of a retained body, verified with `grep -F` against
  `.ufo/waves/round-94/w1/ScoutRFC/rfc9110.txt` (sha256 `21c1cdce6ab0e550…`, 502 941 bytes)
  and `.ufo/waves/round-90/L1/src/rfc8259.txt` (sha256 `61a5378f4255c720…`, 28 360 bytes);
  the receipt is `w1/ScribeEntry/verify-quotes.py` (run `python3 -B verify-quotes.py`,
  exit 0, `violations 0`) and the per-fragment output is `w1/ScribeEntry/quotes-verified.txt`.
  The entry labels clauses C3 (`"role": null` is origin) and C4 (duplicate object keys are
  refused) as **lane conventions**, not RFC requirements: RFC 8259 §4 says only that object
  names SHOULD be unique, and the refusal is local receipt-integrity policy. The entry's
  `source:` line names **S479, which is a pending row** — the L1 must admit the S479 row
  (drafted by `ScoutErrata`, `w1/ScoutErrata/S479-row.md`) into `corpus/SOURCES.md` **in the
  same integration commit as this entry**, or the frozen C1 counter's E3 rule reports
  `unresolved row id S479` for the new entry and the C1 target becomes unreachable through
  the declared repair route. The probe that measures this is
  `w1/ScribeEntry/entry_probe.py` (Q1/Q1b).
- **DRAFT — row S479 — admit, drafted by `ScoutErrata`.** RFC Editor errata search for RFC
  9110, one GET on 2026-11-05T16:32:51Z (302 → `https://errata.rfc-editor.org/search/?rfc_number=9110`
  → 200), 97 741 bytes, sha256 `e6ddebb240b522f3…`, retained at
  `w1/ScoutErrata/errata-9110.html`. The page lists 14 records under Verified (6),
  Reported (2) and Rejected (6), and **no** record targets §5.6.1.2, §5.6.3, §8.8.3 or
  §13.1.x — so the row supports the C2 claim's anchors rather than contradicting them.
  Census receipts: `w1/ScoutErrata/census-validate-with-s479.txt` (rc 0).
- **DRAFT — QUALITY.md criteria for round 95 — admit.** Three new sections, each naming
  `corpus/lessons/round-95.md` and each with an able-to-fail witness measured this round
  (`w1/ScribeEntry/quality-criteria.md`). The L1 must land this lesson file **in the same
  commit as the QUALITY sections**: the frozen C1 counter's E2 rule requires every criteria
  section to cite a `corpus/lessons/…` path that is a non-empty blob at the measured
  revision, and `corpus/lessons/round-95.md` does not exist at the round base.
- **DRAFT — the two round-95 errata and gate-registry work items — admit.** R94-9's five
  registry rows and the R94-8 erratum (`w1/ExecReceipts/erratum-r94-8.md`) are round work
  outside the two claims' predicates; the L1 decides their placement.
- **DRAFT — amendment A's instrument correction — rejected, and the frozen bytes restored.**
  Amendment A (commit `d9be693fdb61dd080ae8cf6c007871d3a118c1d2`) would have re-pinned the
  knowledge entries' identity from head-8-line digests to presence, so that the C1 claim's own
  declared repair route (the three E3 entry repairs) could change those lines. The lane's
  integrity ruling (commit `4f443b3fd79f88fc75cfe46005c01d3ecd85c16f`, "option (b)") restored the
  frozen instrument bytes and the amendment was withdrawn from scoring, so the round's digests
  are again `c95_selfassess.py` sha256 `8fd27d626883f2b6852ea2ee425706a77a72eeaee10ef740b8e0fc15ac03b193`
  and `c95_conditional.py` sha256 `f09f84090fdda405992d7b51191be8838549e3df402b0898eb2ca00c4c3ff312`
  — the values the seat brief pins. **The L1 must note that `.ufo/waves/round-95/freeze.md` at
  `HEAD` still carries the Amendment A section (lines 144–173) even though the amendment was
  withdrawn**, so a reader who hashes the values named in that section will compute a mismatch
  against the restored bytes; the authoritative digests are the ones in
  `.ufo/waves/round-95/controls/instrument-sha256.txt` at `HEAD`, and this seat measured both
  counters against them.
- **DRAFT — assimilation — none.** The `merge/kake` package still collides on 8 ids; no
  package row is appended this round.
- **DRAFT — the two claims' verdicts — not the L1's to draft here.** C1 (`mismatches=18 → 0`)
  and C2 (contract v2) are scored by the wave's attack seats against the frozen instruments;
  this file records the lesson material, not the claims' admission.

## Mistakes

| # | Class | Evidence | Captured-by | Fix (shown able to fail) |
|---|---|---|---|---|
| 1 | A counter's E5 path rule accepted a tree as a present path, so a SKILL.md row naming a directory read clean and the round recorded `met=true` while no blob was ever cited | round-93's counter accepted trees because its path check asked only "does this path exist"; the round-94 strict counter at base `0f7d9bbcdd6a9ed36f5bc62b2116ddd040e871a8` reports `E5=15` with every finding `names a tree, not a blob` (`.ufo/waves/round-94/controls/base-c1.txt`, line 1 and the JSON detail); the round-95 base control at `fdd5fdbeb8a2ba6c18f0f23135d1bee98068dca3` still reports `E5=15` with the same 15 tree findings (`.ufo/waves/round-95/controls/base-c1.txt`) | none in round 93 — `read()` on a tree returned rc 0 (R93-5); the strict counter from round 94 onward is what catches it | the round-95 counter's E5 rule requires a **non-empty regular blob** at the measured revision: a tree, a symlink (git mode 120000) and a 0-byte blob are each a finding (`.ufo/waves/round-95/c95_selfassess.py`, E5 block), and the battery plants one route per shape (`B08-tree-path`, `B09-empty-blob`, `B10-symlink-path`), each of which the base control records as `refused_ok=true`. The 15 rows are **not** repaired by this rule: the route that names a concrete committed non-empty blob for each of the 13 directory rows is R94-5, and it is still open. |
| 2 | A mutant population's `base_rev` pointed at an uncommitted worktree state, so the population's measured base could not be resolved at the revision the kill count was quoted at | the round-93 mutant-scoring receipt `.ufo/waves/round-93/w1/recovered-partial/MutConditional/posgood-out/mutants.json` line 7 declares `"base_rev": "191dd0ed0cf594a29668f5862f536a925998cadd"`; `git cat-file -t 191dd0ed0cf594a29668f5862f536a925998cadd` → `fatal: git cat-file: could not get object info`, rc 128 (the round-94 critic recorded the same rc at `.ufo/waves/round-94/w1/CriticClaims/git-and-digests.out` lines 3–4) | none — the population named a base the lane cannot resolve, and the round-94 critic had to find it (`w1/CriticClaims.md` D1/D14) | the round-95 freeze pins the population's base **by bytes**: the 40 mutants patch `.ufo/waves/round-93/frozen/pos-good.py` (content sha256 `0fe018a8e33ca82928a876f2b0d2e5b3f33befa00260f2fdf995418822a868e4`, byte-identical to the committed blob at `fdd5fdbe`), the population file itself pins that digest in `base.sha256`, and `.ufo/waves/round-95/frozen/c2-population.sha256` pins every fixture digest; the counter scores the population against the digest-pinned bytes and ignores the dead pointer by design (`.ufo/waves/round-95/c95_conditional.py`, `POPULATION BASE`). The erratum `.ufo/waves/round-95/w1/ExecReceipts/erratum-r94-8.md` names the pointer **unrecoverable from this lane** and records the correction text. |
| 5 | The round-95 C1 counter's `met` conjunct battery counts **routes**, not the finding shapes the counter enforces: 7 of the 23 finding shapes its audit can emit have no battery route that expects them, and a regression in any of those 7 is invisible to the battery the `met` line counts | `w1/ScribeEntry/battery_coverage.py` (exit 0): enumerates the 23 emitted shapes from the frozen bytes and maps the 19 defect routes with the counter's own `fragment in detail` rule; the uncovered shapes are E1 `vacuous Gate: no reject decision line (route R01)`, E2 `section … names no corpus/lessons/ file`, E2 `section … cites missing <lesson>`, E3 `missing source:`, E3 `missing verified-at:`, E3 `missing recheck:`, E3 `vacuous source: no row id, URL or path locator`. `w1/ScribeEntry/branch_mutation.py` (exit 0) proves the gap: one surgical mutation per uncovered branch, each in a lane-shaped side tree so every battery field stays comparable, each leaving the mutated counter's own battery reading `battery=20/20 admit=5/5 shadow_absent=1 predecessor_admits=10/19` — byte-for-byte the pristine verdict — while the mutated branch stops firing | none: the class-level reading holds (E1–E5 each have a route) and the base control reads `battery=20/20`, so no route count, selftest or base run distinguishes the mutated counter from the pristine one. MutC1's survivor M03/M03b (E1-vocabulary) is a **separate** mechanism in the same family — it mutates the `admit` half of the disjunction and is invisible to battery *and* base run because every fixture satisfies both alternatives at once | the successor C1 counter must assert a **named finding per emitted shape**, not a route count: one route per shape the audit can emit, each expecting that shape's own detail string, so a branch that stops firing drops the battery count. The QUALITY criterion "a counter's `met` conjunct battery covers every rule class the counter enforces" is already landed as R95-A; this finding refines it to shape level and is the round-96 routing input. |

## Routed

- **R94-1 … R94-9** were read before the round's declaration (`.ufo/waves/round-95/freeze.md`,
  "Fresh-start duty"). C1 implements R94-1, R94-2, R94-3 and R94-7; C2 implements R94-6,
  R93-10, R94-4 and the R94-8 population-base pin; the round's non-claim work covers
  R94-9 (registry rows) and the R94-8 erratum plus the landed-tip receipts.
- **New this round (the L1 records the final routing):** the battery-coverage gap measured
  by `w1/ScribeEntry/battery_coverage.py` — 7 of the 23 finding shapes the frozen C1
  counter can emit have no battery route that expects them, and all 7 are reachable
  (E1 `vacuous Gate: no reject decision line`; E2 `section … names no corpus/lessons/ file`;
  E2 `section … cites missing <lesson>`; E3 `missing source:`; E3 `missing verified-at:`;
  E3 `missing recheck:`; E3 `vacuous source: no row id, URL or path locator`). The
  round-95 QUALITY criterion "a counter's `met` conjunct battery covers every rule class
  the counter enforces" is the rule this gap is measured against; the L1 decides whether the
  gap routes to round 96.
- **Spot-check:** the non-author closure of this round is owed. The attack seats
  (`ReviewC1`, `ReviewC2`, `CriticClaims`, `MutC1`, `SentinelScope`) falsify; they are not
  the outside closure.

Assimilation: none (see Gate). considerthese: nothing mined from
`considerthese/2026-11-05.md` fits a frozen claim's surface this round.
