# Round 80 — lessons (kake, attempt 1)

Base `9998dc7a586b9fe76379014c8123aa3606f2d8b9`; frozen contract `.ufo/waves/round-80/contract.md`
at the freeze commit `f20163c1`; grammar amendment `amendments/amendment-1.md` (written before any
round-80 case was scored and before the tool was touched); counter correction
`amendments/amendment-2.md` at `de65ec21` (before any after-state). One v1 wave, fifteen requested
seats. Axes: calibration 2 (the lowest non-retired axis) and operability 10, with freshness 10 held.
Scores are held; a claim moves evidence, not a scalar.

## Claims

**C1 — calibration: the round-79 routed-defect queue closes.** Population: the six report/receipt
items R79-1, R79-2, R79-3, R79-4, R79-5, R79-8 of
`corpus/lessons/round-79-verifier-spotcheck.md` §6 (the two medium items R79-6/R79-7 are C2's and the
harness's). Counter `python3 -B .ufo/waves/round-80/c80_defect_queue.py --root <tree> [--revision
<rev>]`; frozen predicate `met <=> open == 0`. At the base every item is open (`open=6 met=false`,
exit 1, `controls/base-c80-defect-queue.txt`). Each condition is decided from bytes: a registry row
whose `used-by` resolves to a file that cites it and whose shape passes the census's cell/enum rules;
a guard whose selftest shows a non-prefix append failing; a selftest receipt compared to a re-run; a
fixture harness that kills its three mutants through their own conjuncts; a withdrawal that no
self-assessment file contradicts; a defect record whose seat bytes are re-derived from the round-79
results. The counter ships `--selftest` (`selftest: 3/3 passed`, `controls/ctl-c80-queue-selftest.txt`)
and two controls — base (`open=6`) and a junk tree that fabricates closure in words
(`open=5 closed=1 met=false`, `controls/ctl-c80-junk-queue.txt`).

**C2 — operability: `unavailable_after` accepts the date shapes its source names.** The round-79 tool
splits every field value on ASCII comma before parsing, so both comma-bearing `HTTP-date` shapes are
unreachable and S452's own example — `unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT` — is decided
as `xrt_invalid_value` plus `xrt_unknown_directive`. Amendment 1 makes a comma that follows the
leading weekday token of an `unavailable_after` value part of the value, and adds the asctime shape.
Counter `python3 -B .ufo/waves/round-80/c80_measure.py --root <lane> --revision <rev>` runs the frozen
round-79 matrix over 31 cases and this round's 12-case set over the same tool bytes; frozen predicate
`met <=> frozen wrong=0 and a2 wrong=0 and constants_failed=4/4 in both runs and selftest_ok=true in
both runs`. At the base: `frozen wrong=0 a2 wrong=10 met=false`, exit 1 (`controls/base-c80-a2.txt`).
The four frozen constants fail every case they should on both sets (`controls/ctl-c80-constants.txt`).

## Gate

Admit **S453** — RFC 9110, *HTTP Semantics*, §5.6.7 *Date/Time Formats*,
`https://www.rfc-editor.org/rfc/rfc9110.txt`, opened 2026-11-04 by three independent seats (the wave
scout, the knowledge seat and this L1) with byte-identical results: HTTP 200, final URL identical,
502,941 bytes, sha256 `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a`, retained at
`.ufo/waves/round-80/sources/rfc9110.txt` and
`.ufo/waves/round-80/w1/ScoutSources/S453-rfc9110.txt`. The digest equals the one the lane registered
in 2026-10-21 for S028, so the document identity is not in doubt. Located quote, retained text
`:1855-1856`:

> A recipient that parses a timestamp value in an HTTP field MUST accept all three HTTP-date formats.

Tier A: a Standards Track document with a normative `MUST` on the recipient. The row is
`corpus/SOURCES.md:201` (kind `spec`, tier `A`, status `mined`, opened 2026-11-04, recheck `365d`,
`used-by corpus/knowledge/http-date-grammar.md`). It is a second scoped row on a URL the registry
already holds five times (S010, S028, S033, S088, S433), so the census reports a `W04` warning rather
than an error — measured, not assumed: `W04 19 → 20`, the new line
`W04 S453 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes`, exit 0.

Also admitted: the knowledge entry `corpus/knowledge/http-date-grammar.md` — the three ABNF shapes,
which of them carry a comma, the §5.5 sentence that a comma which is data inside a member must not be
read as a separator, the per-carrier divergence table, and five `[INFERENCE]` marks.

Not written, with reasons:

- **A rejected `S453` row for RFC 9309.** The round-79 report claimed one; no such row was ever
  written and none is written now (§Corrections R79-1). RFC 9309 stays held as S099 for robots.txt.
- **A second row on S449's Google URL with a header scope.** Carried from round 79 and still deferred:
  mechanically admissible (a `W04`), but outside the frozen terms; the drafted row stays at
  `.ufo/waves/round-79/w1/ScoutSources/row-deferred-google-xrt.txt`.
- **The `merge/kake` staged package.** Eight id collisions at the base blob (S312, S329, S367, S372,
  S373, S374, S390, S409) and 27 staged URLs the registry already holds
  (`w1/ConnectorC/collision.out`, exit 0). Adoption stays closed; the collision count is unchanged
  from round 79.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| **unsatisfiable predicate conjunct**: the C1 counter read `used = row[11]` on an eleven-cell row, so `used-by` was always empty and R79-1 could never close | `c80_defect_queue.py` at the freeze `f20163c1` (sha256 `90649c08…`), `used = row[11] if len(row) > 11` under `row_shape`'s eleven-cell rule; masked at the base because the row is absent and the function returns at the earlier branch (`controls/base-c80-defect-queue.txt:2`) | the wave's `ScoutSources` seat, at the freeze bytes and before any after-state (`w1/ScribeKnowledge/r79-1-counter-probe.txt`: freeze `(False, 'S453 used-by resolves to no file that cites S453')` vs `de65ec21` `(True, …)`) | cell index corrected and a `--selftest` added so the conjunct is shown able to pass and to fail (`amendment-2.md`, `controls/ctl-c80-queue-selftest.txt`); the predicate sentence did not change |
| **own-round receipt rewrite**: the base and junk control receipts were re-cut in place by that fix, one added `exit=` line each | `git diff f20163c1..de65ec21 -- .ufo/waves/round-80/controls/`: blobs `d46bd610` → `dad8fb81` and `a265d23a` → `b72e4af0`; the verdicts did not move | this L1's own diff discipline, checked by the round's scribe seat | disclosed in `.ufo/waves/round-58/receipt-rewrites.json` with true blob pairs, `kind=content` and notes pointing at this lesson, and in §Corrections below; the append is byte-spliced so the prior ledger bytes are preserved |
| **frozen-premise**: the round-79 contract called the RFC 822/850 `unavailable_after` branches case-pinned when no case carried one | `corpus/lessons/round-79.md` §Limits; the frozen set holds exactly two `unavailable_after` values, both ISO or invalid, and `grep -c GMT` over `round-79/expect/expect.json` prints `0` | the round-79 scout's grammar read, routed before the tool existed; the defect is measured this round: `controls/base-c80-a2.txt` prints `a2: cases=12 decided=12 wrong=10` | a branch is never called covered without a case carrying it; c32-c43 carry the comma-bearing IMF-fixdate, RFC 850 and asctime shapes |
| **spec-tool mismatch**: the grammar split every field value on ASCII comma first, so the source's own example was rejected | `corpus/lessons/round-79.md` §Limits and §Post-attack settlement; the round-80 base receipt `a2 wrong=10`, exit 1; `w1/ScoutRecon.md` §1 enumerates the six consequences with probes | ReviewC2 F1 named it after the round-79 green matrix; the frozen case set could not see it | amendment 1 (A1 comma after the weekday token belongs to the value, A2 asctime joins the shapes, A3 no new finding id), written before any case was scored; the frozen 31-case set stays a no-regression conjunct of the predicate |
| **control expectation contradicted by the committed control**: the contract says the junk tree "must still print `open=6`"; it prints `open=5 closed=1` | `contract.md` §Controls vs `controls/ctl-c80-junk-queue.txt:8`; R79-5 closes in the junk tree because its predicate is textual — a lesson line quoting the withdrawn sentence satisfies it | the round's record seat, reading the frozen control | reported, not edited: R79-5 is a wording defect whose closure *is* a recorded withdrawal, so a fabricated withdrawal is indistinguishable at that conjunct; the control still gates (`met=false`, exit 1) and the limit is stated below |
| **contract named a control that was never shipped** (`controls/ctl-c80-consts.txt`) | `contract.md` §Controls; the receipt now exists as `controls/ctl-c80-constants.txt` (`ctl constants_failed=4/4 cases=12`, exit 0) | the record seat's inventory | the named receipt is shipped (the filename differs from the contract line, which is frozen); the constants conjunct is decided by the C2 predicate on both sets regardless |

## Corrections

1. **R79-1 — erratum: the rejected `S453` row was never written.** The round-79 report says "One
   rejected row is kept (`S453`, RFC 9309, tier A, `status=rejected` …)"
   (`.ufo/reports/round-79/kake.md`); the non-author closure measured `grep -c 'S453' corpus/SOURCES.md`
   = 0 and filed R79-1. Erratum: no rejected row was written and none is owed — RFC 9309 stays held as
   S099. `S453` is this round's RFC 9110 §5.6.7 row (Gate above). The conjunct that closes the item
   also required the counter's `used-by` index repair (amendment 2).
2. **R79-2 — the append guard, and this round's own append.** `scripts/ledger_append_guard.py` checks
   that a receipt ledger's base bytes are preserved as a prefix when the file grows; its `--selftest`
   makes a non-prefix in-place edit fail and a pure append pass. The round's own disclosure append to
   `.ufo/waves/round-58/receipt-rewrites.json` was made by byte-splicing before the array's closing
   `]`, so every prior byte survives — the guard's own subject, exercised by this round's work.
3. **R79-4 and R79-6 — the survivors, isolated.** k4 (the mutator that zeroes `malformed`) survived the
   round-79 battery because the cheap-note entry is counted as both `undisclosed` and `malformed`, so
   dropping `malformed` flipped nothing; the battery's cheap-note fixture never isolated the mechanism.
   `R79-4`'s closure condition is now `c80_ledger_fixtures.py` reporting `killed == 3` with k3
   (`wrong_kind`), k4 (cheap-note) and k5 (`symlinks`) each red through its own conjunct and the
   cheap-note fixture red through `undisclosed == 1`, recorded at `controls/c80-cheap-note.txt`.
   `corpus/QUALITY.md` gains the criterion clause naming `R79-4` with `undisclosed=1`.
4. **R79-5 — the sentence is withdrawn.**
   R79-5 withdrawal: `passed 31/31 before the tool existed` is withdrawn for want of a committed reference run.
   The round-79 report's sentence has no committed pointer and its scratch tree is gone; what the
   round rests on is unaffected (amendment 1's terms, the frozen case set, the matrix receipt). No
   lane self-assessment file repeats the sentence; the only lane occurrence is the non-author closure
   quoting it as the routed defect.
5. **R79-8 — the empty-output seats, and what the results file cannot say.**
   `.ufo/waves/round-79/w1-results.json` carries 14 records of four fields each (`agent`, `name`,
   `note`, `output`) with `note: null` everywhere; exactly two outputs are empty — `ExecC2Tool`
   (executor) and `CriticC` (critic), 0 bytes, sha256 `e3b0c442…b855`. The file records no status,
   exit or error text, so a "last error" cannot be recovered from committed bytes;
   `.ufo/waves/round-80/defect-queue.json` records the two seats with re-derived `output_bytes` and
   `output_sha256` and states that limit rather than inventing a message. Three further seats returned
   short reading notes with no deliverable (`ExecC1Ledger`, `ExecR2R3`, `ReviewC1` in round 79); they
   are thin, not empty.
6. **Per-carrier scope (connector finding).** After this round the lane holds two instruments that read
   an `unavailable_after` value from different carriers and disagree on the same literal: the header
   tool accepts RFC 850 and asctime; the round-78 meta tool rejects both and expects
   `[invalid_value, unknown_directive]` for `Sunday, 06-Nov-94 08:49:37 GMT` (its frozen case `m25`).
   Observed in `w1/ConnectorC/meta-date-probe.out`; recorded in `corpus/knowledge/http-date-grammar.md`
   §Per-carrier scope and in `PROVINCE.md`; harmonization is routed, not done — round-78's grammar,
   matrix and receipts are frozen.
7. **Adopted from `considerthese/2026-10-23.md:36`** (one proposal, not implemented before this round):
   seat failures split by cause rather than a single dead count. R79-8 is the class this scores, and
   the record above splits the two empty seats from the three thin ones and names what the results
   file does not record; the durable fix (a failure-cause field in the wave registry) is routed to the
   next wave, because this round's registry is frozen.

## Limits

- **R79-5's predicate is textual.** A fabricated withdrawal sentence satisfies it; only the "no
  self-assessment file repeats it" conjunct is state-bound. The junk control shows this (`open=5`, not
  `open=6`); it still gates, because the other five items are state-bound.
- **`unavailable_after` calendar validity is not decided.** `31 Feb 2025` matches the IMF-fixdate shape;
  the tool decides grammar, never whether a date exists. RFC 9110's 50-year window for the two-digit
  RFC 850 year is not implemented.
- **A2 widens RFC 9110 by one branch.** `date3` requires `month SP ( 2DIGIT / ( SP 1DIGIT ))`; the
  amendment also accepts a single space before a one-digit day (`Nov 6`), a lenient reading chosen so a
  space-collapsed transcript does not flip a value to invalid. No frozen case uses that branch (c34 is
  `Nov  6`, c43 is `Nov 16`). Marked `[INFERENCE]` in the knowledge entry.
- **A1 is a lane segmentation rule, not a source statement.** S452 never says the comma belongs to the
  date; RFC 9110 §5.5 is an `ought` on field definers (line 1629-1631 uses "ought to"), and
  `X-Robots-Tag` is defined by no specification. The rule is the lane's, grounded in both.
- **Sanctioned behaviour changes with no case.** `unavailable_after: Wed, noindex` loses `noindex`
  (the comma belongs to the value, which then fails every shape), and a comma-bearing value with a
  wrong zone shrinks from `invalid + unknown` to `invalid` only (A3). Both are consequences of the
  amendment, not defects; `w1/ScoutRecon.md` §4 measures them.
- **The real-input population is unchanged and negative.** No live property was fetched (two public
  source GETs only); the round decides grammar and case behaviour, never a crawler outcome.
- **C1's item population is six of the eight routed defects.** R79-6 is decided by the fixture harness
  inside R79-4's condition and R79-7 by C2's third conjunct (frozen 31 plus the 12-case set); the
  round report states the per-item disposition of all eight.

## Post-attack settlement (appended 2026-11-04)

The wave's attacks and its own receipts changed the round's bytes before the report; the record is
corrected here rather than by rewriting an earlier line.

- **C1 measured at the carrier.** `C1v1 revision=aa44b9af2cdd146f287782f69888bf8b984187d8 items=6
  open=0 closed=6 exported=84 met=true`, exit 0 (`controls/after-c1.txt`); base `open=6 … met=false`,
  exit 1 (`controls/base-c80-defect-queue.txt`). Per item: R79-1 closed on the RFC 9110 row whose
  `used-by` resolves and the erratum; R79-2 closed on the append guard (selftest green through a
  failing non-prefix fixture, ledger prefix preserved); R79-3 closed on the selftest receipt matching a
  re-run at the measured revision; R79-4 closed on `killed == 3` with the cheap-note fixture red
  through `undisclosed == 1`; R79-5 closed on the withdrawal recorded above and unrepeated in every
  self-assessment file; R79-8 closed on the re-derived seat bytes. R79-6 is decided by the fixture
  harness inside R79-4's condition and R79-7 by C2's `frozen wrong=0` conjunct.
- **C2 measured at the carrier.** `C2v1 revision=aa44b9af… frozen_cases=31 frozen_wrong=0
  a2_cases=12 a2_wrong=0 constants=4/4+4/4 selftest=ok met=true`, exit 0 (`controls/after-c2.txt`);
  base `a2 wrong=10`, exit 1 (`controls/base-c80-a2.txt`). Tool `d1ea524f…` (23,677 B) with
  `selftest: 33/33 passed` (`controls/c80-selftest.txt`); the four frozen constants fail 12/12 each on
  the new set (`controls/ctl-c80-constants.txt`).
- **Three counter/instrument amendments, all before an after-state.** Amendment 2 (the `used-by` cell
  index, found by `ScoutSources`) and amendment 3 (`ExecGuard`'s finding that R79-2 could not be
  decided in revision mode: the guard gained `--base-file`, the counter exports the governed ledger and
  a base snapshot). The predicates, item conditions, case set and oracle are unchanged by both.
- **A1's strictness was ruled by the seat that wrote it.** `DATE_COMMA_RE` anchors the weekday at the
  end of the split piece without allowing trailing whitespace, so `Wed , 03 Dec …` (a space before the
  comma) keeps the round-79 split — A1 says the comma *immediately* follows the token. No frozen case
  discriminates; the reading is recorded here as the carriage rule.
- **Four receipt rewrites, all disclosed.** The round re-cut `controls/base-c80-defect-queue.txt` and
  `controls/ctl-c80-junk-queue.txt` (amendment 2, one added `exit=` line each, both `append`),
  refreshed `controls/c80-selftest.txt` after a post-freeze tool tweak so its pinned tool sha follows
  the carrier (`content`), and re-ran the base receipt after amendment 3 grew the revision export
  (`content`, `exported=76 → 77`). Each is an entry in `.ufo/waves/round-58/receipt-rewrites.json` with
  its true blob pair and kind, appended by byte-splice; the standing round-79 gate is green at the
  carrier (`events=36 undisclosed=0 … met=true`, `controls/after-c1-ledger-gate.txt`).
- **The wave's own seats changed the carrier.** `ExecGrammar` fixed the parse (its `$`-anchored
  `DATE_COMMA_RE` and the asctime shape), `ExecFixtures` built the survivor harness (its cheap-note
  kill criterion initially contradicted itself — `undisclosed == 1 and malformed == 1` while also
  requiring `malformed == 0` in the "others" set — and the L1 corrected that one condition after the
  seat reported `killed: 2`), `ExecGuard` routed the amendment-3 defect and its guard design informed
  the L1's implementation, `ExecQueue` wrote the re-derived seat record, `ScoutSources` found the
  unsatisfiable conjunct, `ScoutRecon` measured the 31/31 no-regression and the 12/12 predicted patch,
  and the two scribes produced the Gate, Mistakes, Corrections and criterion drafts this lesson lands.
