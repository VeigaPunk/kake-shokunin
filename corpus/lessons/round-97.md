# Round 97 — kake (hyaku run 15, attempt 1, fresh start)

Base `36d148f5c60100021304903c30e5663207c72f4f`; instruments `74bda9b7` (v1) →
`a2208ac7` (v2, frozen); freeze `5d5f608f3cd9aa9a73136cf05f81bef38bea40cb`; C1 repair
`9e27ce0b2a8d168e032ab79ea11471b36eaceedf`. Claims, predicates, counters and controls:
`.ufo/waves/round-97/freeze.md`. One v1 wave of 13 seats (`.ufo/waves/round-97/w1-results.json`).

Fresh-start reads (Amendment 35): the round-94, round-95 and round-96 non-author spot-checks
(`round-9{4,5,6}-verifier-spotcheck.md`), summarised with what changed in the freeze's first table.

## Verdicts recorded by the L1 (the outside closure owns admission)

- **C1 calibration — met on the frozen predicate.** `c97_index.py` at `9e27ce0b`:
  `entries=84 indexed=84 unindexed=0 dangling=0 mismatches=0 met=true`, exit 0
  (`controls/repair-c1.txt`) against `mismatches=38` at base (`controls/base-c1.txt`);
  row-review conjunct `agree=19/19` (`w1/ReviewIndexA/verdicts.tsv`) + `agree=19/19`
  (`w1/ReviewIndexB/verdicts.tsv`), 38/38 rows, 0 disagree. An independent second
  implementation written from the docstring only agrees per entry 84/84 at base and at the
  repair (`w1/ExecIndexTwin/`). The attack seats falsified the counter's discrimination
  beyond the declared shuffle limit (Mistake 4, routed R97-1); the predicate's review leg is
  what certifies the 38 rows.
- **C2 freshness capability — met on the frozen predicate.** `c97_reval.py` at `9e27ce0b`:
  `candidate=present hand=37/37 generated=104/104 heldout=56/56 forgeries_refused=7/7
  positive=admitted mutants=14/14 survivors=none anti_table=ok population=ok seed=97 met=true`,
  exit 0, candidate sha256 `192b3bf7…` (`controls/repair-c2.txt`; reproduced by ExecScoreC2,
  CriticClaims, MutReval and SentinelScope). The predecessor `c96_reval.py` still crashes
  (`controls/c2-predecessor-at-base.txt`). CriticClaims K1–K4 show the frozen population
  cannot see four contract-v1 clauses (Mistake 5, routed R97-2); the real candidate decides
  every K-probe correctly (`w1/CriticClaims/receipts/direct-probes.txt`).

## Gate

- **Row S481 (RFC Editor errata search for RFC 9111) — admitted.** One GET by ScoutErrata
  2026-11-05T21:07:55Z: 302 → `https://errata.rfc-editor.org/search/?rfc_number=9111`, HTTP 200,
  40 374 bytes, sha256 `b906ce97f132718b55c846639bb1ffdfcd0da387c7988fc7c055066bea3b7395`
  (`w1/ScoutErrata/fetch.txt`, body `w1/ScoutErrata/errata-9111.html`). Four records
  (`records.tsv`): EID 9004 Reported §3.5, EID 9185 Reported §4.3.4, EID 9166 Held §5.2.3,
  EID 7695 Rejected §4.3.2. Located quote "Section 4.3.4 says:" at body line 260
  (`quotes-verified.txt`, substring_ok). Census-schema 11 cells, no pipe in a cell; status
  `mined`; recheck `90d` (two records unresolved).
- **Knowledge-entry paragraph `## Errata sweep (round 97)` in
  `corpus/knowledge/revalidation-exchange.md` — admitted.** States EID 9185 targets §4.3.4
  (the 304 update set, which the entry's exclusions already leave out) and that §4.3.1/§4.3.3,
  the ground contract v1 decides, carry no verified, reported or held erratum at that fetch;
  §4.3.2's only record is Rejected. The entry's `source:` line is unchanged (S480) so the C1
  index row stays exact; the paragraph cites S481 in its body.
- **38 coverage-index rows (`corpus/README.md` `## Coverage index — round 97 (calibration
  repair)`) — admitted** on the review conjunct (38/38 agree). 26 are corrected rows (earlier
  Area/Coverage text kept, id set completed from the entry's `source:` line); 12 are new rows
  written from the entry's title, ground and scope lines. Earlier rows stay above as filed
  history (29 of them still fail the counter's per-row test — CriticClaims F-C1-4, routed R97-1).
- **SKILL.md gate-registry rows for `c97_index.py` and `c97_reval.py` — admitted** (R94-9
  pattern; SKILL.md lines 221–222).
- **Capabilities row "Revalidation exchange, contract v1" — admitted with caveats named**:
  first counter pass this round (the r96 flip condition), on a candidate landed in round 96;
  the row says the credited move is the instrument that can score it plus the attacked
  demonstration (CriticClaims F-C2-8), and carries the K1–K4 population gaps.
- **merge/kake package adoption — rejected.** ExecCensus re-derived 8 id collisions
  (`w1/ExecCensus/assimilation/collisions`; guard proof nonempty on an indented `  | S002 |`
  fixture, `guard-proof.txt`). No renumber map and no re-grounding this round. Flip: a round
  that re-opens each staged entry's sources and renumbers by document in scratch.
- **CriticClaims' proposed per-entry predicate ("no judged row names more than one entry") —
  not adopted in-round** (an instrument change after freeze; routed R97-1).
- **ConnectorScope A1 (chousa `corpus/evidence/round25-measure.sh`, an earlier unindexed
  counter that uses path-substring membership) — cited as prior art, not ported**
  (`w1/ConnectorScope/overlaps97.md` row A1). B2 (kumitate S237, RFC 9111 §5.1/§4.3.4) is
  neighbouring ground, no conflict with §4.3.1–§4.3.3.

SOURCES row changes (old → new): S481 absent → `mined` (new). No other row touched.

## Mistakes

| # | Class | Evidence | Captured-by | Fix (shown able to fail) |
|---|---|---|---|---|
| 1 | Instrument governance: a frozen forgery that cannot run inside the counter's sandbox scores as a crash, so its "refusal" proves nothing about the defense it was built to test | `.ufo/waves/round-97/controls/v1-forgery-crash/ctl-c2-slot-table-74bda9b7.txt`: the v1 lookup table imported `hashlib`, which the sandbox (`sys.path=[root]`, `-I`) cannot import; `hand=20/37 generated=0/104 heldout=0/55 … met=false` | none at build time; caught by the L1 reading the truncated traceback before freeze | v2 forgery imports only modules the sandbox has loaded; `controls/ctl-c2-slot-table.txt` passes hand 37/37 and generated 104/104 and fails only `heldout=22/57` → met=false exit 1 (reproduced by ExecScoreC2 `22/52` and MutReval `20/58` on their own commit ids). A forgery control now counts only when it passes every population except the one under test |
| 2 | Self-assessment drift: the coverage map under-claimed the corpus — 38 entries had no index row or a row omitting ids the entry cites; one was named from outside (R97-D1) | `controls/base-c1.txt` `mismatches=38`; `corpus/lessons/round-96-verifier-spotcheck.md` §6 R97-D1; CORPUS.md index-row rule | CORPUS "An index row is a claim"; no live lane instrument | `c97_index.py` shown able to fail: base 38, path-only junk 38, fenced table 38 (`controls/ctl-c1-forgery-{pathonly,fenced}.txt`); repair 0 |
| 3 | Stale premise: the freeze says "for C1 the lane held no coverage-index instrument"; it held the historical `readme-index-counter` (`.ufo/waves/round-55/c55_readme_index.py`, SKILL.md line 1242, red by design since round 59) | ScribeLesson `receipt-c55-counter-base-and-tip.txt`: `index_mismatches=29 … met=False` at base, the same 24 unindexed after the repair (it reads only `## Coverage map`) | round-96 Mistake 3's rule (name the do-nothing instrument set) was applied but the lane's gate-status ledger was not consulted | Not repaired in-round (frozen text). The do-nothing conclusion holds under both instrument sets (29 and 38, both red). Routed R97-3: freezes name every registered instrument over the surface, historical ones included, from SKILL.md's registry |
| 4 | Instrument discrimination: the C1 counter admits a one-row mega-index (all 84 tokens, all ids, two entry words each) and per-entry scope copies; it is per-entry, so older failing rows stay invisible | CriticClaims F-C1-1 (`met=true`, `index_rows 130`), F-C1-3, F-C1-4 (29 older rows fail the per-row test), F-C1-2 (review unit row vs entry); MutIndex survivors M01/M02/M06/M12/M13 (`w1/MutIndex/mutants.tsv`: selftest and base/repair lines do not distinguish them; the committed fenced control kills M01) | the freeze declared only the shuffle limit | Routed R97-1: successor requires one entry per judged row, a per-row test over every Entry-table row, and selftest fixtures whose fence/comment rows would otherwise be visible table rows |
| 5 | Population coverage: the frozen C2 population cannot see four contract-v1 clauses (5xx range beyond 500/503/599, etagc DQUOTE/DEL, boolean `last_modified`, 1xx above 100); the mutant clause scores the frozen positive control, not the candidate; refused generated inputs drop out of the denominator | CriticClaims F-C2-1…F-C2-7, K1–K5 `met=true` (`w1/CriticClaims/receipts/variants-results.json`); MutReval survivors M4a/M4b/M5/M6/M7 (`w1/MutReval/mut.md`) | none (round-96 population inherited unchanged by design) | Routed R97-2: successor adds hand cases 501/502/504/599-edge, etag DQUOTE/DEL, bool lastmod, 101/199, scores refused generated inputs as refusals, and labels `mutants=` a harness check |
| 6 | Seat hygiene: ConnectorScope deleted the round's parent scratch (`rm -rf /fast/scratch/hyaku/kake-r97`) mid-wave, killing sibling scratch trees | ConnectorScope-23 broadcast and `w1/ConnectorScope.md` §7; ExecScoreC2 `compare.md` incident note (first slot attempt died as checkout-fail shells, re-derived) | wave context said "delete your scratch tree" without forbidding the parent | Routed R97-4: wave context names the exact seat path to remove and forbids removing any ancestor; the L1's own scratch is not shared with seats |

## Routed to round 98

- **R97-1** (Mistake 4): C1 successor — one entry per judged index row; per-row test over
  every Entry-table row, or retire superseded rows explicitly; selftest fence/comment fixtures
  that are complete tables; CriticClaims' per-entry predicate.
- **R97-2** (Mistake 5): C2 successor population — CriticClaims K1–K4 cases; refused generated
  inputs scored as refusals; `mutants=` relabelled as a harness self-check; MutReval M4a/M4b/
  M5/M6/M7 discriminating fixtures (pins read at HEAD or working tree, lookup pin dropped,
  anti-table narrowed, git from PATH). The anti-table blacklist is not the defense: the
  held-out cases are (`controls/ctl-c2-slot-table.txt`, `anti_table=ok heldout=22/57`).
- **R97-3** (Mistake 3): name every registered instrument over a claim surface in the freeze;
  reconcile or retire `readme-index-counter` against `c97_index.py`.
- **R97-4** (Mistake 6): wave contexts forbid removing any ancestor of the seat's own scratch.
- **R97-5** (SentinelScope): the C2 sandbox admits in-tree writes, stdout-fd shadowing,
  outside `listdir`/`stat`, reads under `/usr` (prefix rule wider than the stdlib) and
  `kill(ppid, 0)`; carried with R96-4 (effectful shadow).
- **Carried unchanged**: R96-3 (round-96 C1 self-assessment counter false-greens; that
  instrument is untouched this round), R95-2 L0 kill-predicate arbitration (line 371 of the
  fleet `.ufo/l0-questions.md` still unanswered), R95-6.
- **Dead seat**: ReviewReval ended without a report or verdict (`w1-results.json` output ends
  mid-investigation: "Checking what landed where."); its diff review is partly covered by
  MutReval, ExecScoreC2 and CriticClaims; a full successor-diff review is owed next round.
