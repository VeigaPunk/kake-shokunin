# ScoutOperatorLessons

## OPERATOR LESSONS:

The seat item reads `corpus/lessons/operator-*.md` (newest three). That file set is EMPTY at base
9f07731a — verified three independent ways:

- Filesystem sweep: `find /home/vgpnk/Projects/shokunin -name 'operator-*'` matches only
  `.ufo/scopes/*/operator-demand.md`, `game-dev-3d-shokunin/reports/*/operator-*.md` and
  `kasegi-shokunin/corpus/knowledge/operator-queue.md`; no `corpus/lessons/operator-*` exists in any
  lane corpus, the fleet corpus, or shokuknow (read-only).
- Lane git: `git ls-files corpus/lessons/` lists only `round-*.md`; `git log --all` over
  `corpus/lessons/operator-*` is empty at every ref (nothing deleted, nothing ever committed).
- The reference is template text: `.ufo/prompts/kake-round-61.md:480` ("Also honor any
  `corpus/lessons/operator-*.md` teaching not yet reflected") and
  `.ufo/waves/round-61/make_spec_w1.py:346-348` generate this item generically; the template
  presumes a file set the operator never committed.

So there are no operator-*.md teachings to enumerate and nothing unreflected from that channel to
list. The operator-authored teaching channel that DOES exist — the round-60 outside-verifier
spot-check — is fully reflected: all six routed defects (R60-D1..R60-D6) appear in the contract's
"Routed defects of the round-60 spot-check" section (D1 relabel-count process note; D2 erratum
note keeping the 22-unit measurement; D3 `# receipt:` header rule; D4 C1/C2/C3 causal
decoupling; D5 quarantine hold + calibration L0 carry; D6 SHONEN boxes stay `[~]` with pointers).

## L0 ROWS:

All three rows the item names are open in the append-only fleet queue
`/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` (read-only; unmodified):

1. **Quarantine hold** — `kake | round-58` (line 180): the §10 quarantine/frozen-claim conflict.
   The 12-row absent-defect slice was re-opened; six registered payloads are now present (S142,
   S156, S161, S193-S195) while C3's frozen mirror predicate permits only S423/S424; the round-58
   assimilation theme (Baidu crawler identity) does not cover them. Question: should present
   quarantine rows stay candidates for a later round's theme/claim, or may they be adopted as a
   separate §10 duty without widening a frozen claim?
   Routing in round-61: contract "Routed defects" R60-D5 and "Frontier step and assimilation" —
   the slice is re-derived byte-identical to the round-58/59/60 record (12 rows), still held,
   nothing appended, `Assimilation: none` ("no staged theme matches the claims; the slice stays
   operator-held"). The round declines to adopt any present row, so the frozen-claim conflict is
   never triggered; the question is deferred, not answered.

2. **Calibration-ownership ruling** — `kake | round-59` (line 181): rounds 54-59 declare a claim
   on the `calibration` sub-axis (AXES.md: SCORECARD/SHONEN vs observed state) while the mission
   prompt names kake's axes as operability + freshness. Should calibration stay a scored kake
   sub-axis (the lowest-axis rule keeps landing on it), be folded into operability, or be dropped
   from the SCORECARD? Raised in the round-54 spot-check, filed round-59; the round-59 lesson
   Considerthese row 8 records it open, named for the operator.
   Routing in round-61: contract "Axis declaration" — the scorecard still carries the round-54
   bounded sub-axis calibration (score 2, lowest non-retired), so the lowest-axis obligation
   lands on C1, with ownership expressly "still open for the operator, L0 row of round 59". The
   round declares no score change: the C1 counter carries a `scores_held == 3` term (operability
   10, freshness 10, calibration 2), shown able to fail by a score-only mutant per R59-D2. The
   round continues the status quo without deciding ownership.

3. **S367 CJK unit rule** — `kake | round-59` (line 182): which reading of the ≤25-word quote
   rule binds — kake's count (one unit per CJK character, one per non-CJK whitespace token) or a
   plain whitespace-token count under which a whole Japanese/Chinese sentence is one token. It
   blocks re-grounding the staged Yahoo! JAPAN 002855 entry (w1/ScoutRejectYahooUA flip).
   Evidence named: `c59_quote_truth.py units()`; round-59 lesson Considerthese row 7 records the
   convention open and notes the S367 quote was re-cut to ≤24 units in r56 so no committed quote
   exceeds 25 units. S367 is the Yahoo!検索 インフォセンター Japanese row
   (`corpus/SOURCES.md:157`, opened round 53).
   Routing in round-61: the contract's quote rule is stated in plain whitespace units ("6..25
   whitespace units, ≤160 chars, ASCII", C3 condition C3; seat-level rule: "6..25 whitespace
   tokens"), but no round-61 quote depends on the CJK reading: the four new C2 rows S430-S433 are
   RFC 6797, W3C CSP3, WHATWG Fetch and RFC 9110 — all English; the ten C3 due rows S001-S010
   are GitHub docs, GNU tar, nginx source and RFC 9110 rows — all English (checked
   `corpus/SOURCES.md`). The staged S367/Yahoo! entry is not re-grounded this round, so the
   unresolved rule binds nothing and no quote sits near the ambiguity.

## INHERITED:

- The three L0 rows above, inherited as open operator questions; round-61 routes around each
  (assimilation none; no score change; no CJK-dependent quote) rather than answering any.
- Round-60 spot-check routed defects R60-D1-R60-D6, carried into the contract's Routed defects
  section (all six reflected there — see OPERATOR LESSONS).
- Seat constraints from the wave context: the L0 queue is read-only/append-only; write scope is
  this report file and `ScoutOperatorLessons.files/` only; every quote here obeys the round quote
  rule (6-25 whitespace tokens, ≤160 chars, ASCII double quotes, page-unique, substring of one
  whitespace-collapsed text node); no fabrication — the empty operator-lesson file set is
  reported as observed, and template-generated expectations that match no committed file are
  named as such.
- Round facts: base 9f07731a873585e655a6518233ea39f5d9fb8204; access date 2026-10-27 (UTC);
  counters are frozen by the L1 after this wave, before any measurement — this seat scores no
  after-state; this item was produced from a generic template whose `operator-*.md` premise has
  no committed referent.

VERDICT: operator-*.md lesson files are absent fleet-wide (nothing unreflected to list; the
round-60 spotcheck teachings are all reflected in the contract); the three named L0 rows —
quarantine hold (kake r58), calibration-ownership ruling (kake r59), S367 CJK unit rule (kake
r59) — remain open and the round-61 contract routes around each without resolving it.
