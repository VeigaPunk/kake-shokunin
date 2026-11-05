# Round 97 freeze — kake (hyaku run 15, attempt 1, fresh start)

Frozen by the L1 (KakeR97) before any seat is dispatched and before the C1
repair or the C2 scored run. Round base (lane tip at round open, ahead=0):
`36d148f5c60100021304903c30e5663207c72f4f`. Instruments commits:
`74bda9b7d14a5108b1dfa119534ed4045a4b35a3` (v1) and
`a2208ac7b8ce6e1148e5069b4c884c78f97dfb3e` (v2, the frozen instruments; v1's
lookup-table forgery crashed inside the counter sandbox — receipt kept at
`controls/v1-forgery-crash/ctl-c2-slot-table-74bda9b7.txt`, mined as a
Mistake, never scored as a defense). Instrument digests:
`controls/instrument-sha256.txt`. Controls were executed and committed with
this file, at the v2 instruments revision, through each counter's public CLI
on committed revisions (`controls.sh a2208ac7…`).

## Fresh-start reads (Amendment 35; last three rejected closures)

| round | closure | root failure | what this round does differently |
|---|---|---|---|
| r94 | rejected-honest-stop (MANIFEST idx 1360) | C1 counter could not tell de-backtick gaming from repair (X4/X5 met=true); C2 target 40/40 unreachable (M11 equivalent) | C1 counter rejects a path-only junk row, a fenced or commented row and a prose row through the public CLI (receipts below); C2 target is one the positive control in the candidate slot already reaches, so it is attainable by construction |
| r95 | rejected-honest-stop (idx 1368) | C1 repairs real but uncertifiable under the frozen predicate; post-freeze amendment withdrawn | the C1 predicate is the counter line plus a row-review conjunct, both stated before data; no instrument byte changes after this commit |
| r96 | rejected-honest-stop (idx 1376) | C2 frozen counter crashed (`NameError: mutants`, line 624) on every candidate-present run; the green selftest ran another code path | R96-A: the successor's main path is proven end-to-end BEFORE freeze on committed revisions with the frozen positive control in the candidate slot (`ctl-c2-slot-pos.txt`, met=true exit 0) and two forgeries in the slot (met=false exit 1) |

The do-nothing control for each claim is named by instrument set (R96
Mistake 3): **the instruments the lane held at the round base, run on the
round base tree.** For C1 the lane held no coverage-index instrument; the
do-nothing tree is the base README scored by the successor counter
(`base-c1.txt`). For C2 the lane held `c96_reval.py`; it crashes on the base
and on the instruments revision (`c2-predecessor-at-base.txt`,
`c2-predecessor-at-instr.txt`).

## C1 — calibration (HOLD 2, lowest owned non-retired axis)

Surface: `corpus/README.md` coverage map, the lane's self-assessment of the
ground it holds (CORPUS.md: "An index row is a claim"), against the
committed `corpus/knowledge/*.md` population. Closure-routed R97-D1 names
one instance (revalidation-exchange.md has no row); the counter measures
the whole population.

- Counter: `python3 -B .ufo/waves/round-97/c97_index.py --root . --revision <REV> --work <scratch>`
  (sha256 in `controls/instrument-sha256.txt`).
- Before (do-nothing, base `36d148f5`): `entries=84 indexed=46 unindexed=38
  dangling=0 mismatches=38 met=false`, exit 1 (`controls/base-c1.txt`; same
  at the instruments revision, `controls/instr-c1.txt`).
- Predicate (frozen sentence; the same in the counter and the receipt):
  **C1 met ⇔ `c97_index.py` prints `mismatches=0 met=true` with exit 0 at the
  landed content revision AND every row of the round-97 index section is
  judged `agree` in `w1/ReviewIndexA/verdicts.tsv` + `w1/ReviewIndexB/verdicts.tsv`
  (one line per row: `<entry>\t<agree|disagree>\t<reason>`; agree count equals
  the section's row count, disagree count 0).**
- Kill rule: any other counter line, or any `disagree` on the reviewed bytes,
  lands C1 unmet. Rows are not rewritten after review to flip a verdict.
- Forgery controls (public CLI, committed fixture revisions in scratch clones
  of the instruments revision), expected → observed:
  path-only junk rows for all 38 entries → expect `unindexed=38` exit 1
  (`ctl-c1-forgery-pathonly.txt`); the same rows with ids and entry words
  inside a fenced block → expect `unindexed=38` exit 1
  (`ctl-c1-forgery-fenced.txt`); selftest 14/14 fixtures via the public CLI,
  incl. comment, prose, wrong-header table, token-outside-Entry-cell, one
  missing id, dangling row, uncommitted row, empty population (exit 2)
  (`ctl-c1-selftest.txt`).
- **Declared known limit (before data):** rows assembled from shuffled entry
  words with the right ids pass the counter (`ctl-c1-forgery-shuffle.txt`,
  expected and observed `mismatches=0 met=true` exit 0). The counter cannot
  judge prose accuracy; that is why the predicate carries the row-review
  conjunct. A row that quotes or reuses an entry's own scope text is an
  accurate index claim and is admitted by design.
- Score move on met: calibration 2 → 3 (one measured self-assessment
  mismatch population closed, 38 → 0). Unmet: stays 2.

## C2 — freshness (HOLD 10), capability acquisition: revalidation exchange, contract v1

Surface: the candidate `scripts/reval_exchange.py` (landed r96, sha256
`192b3bf7596abad8ef76a7a8262ecc29c0d565587153547ee61b5ee7566c7212`), scored
for the first time by a counter that runs; capability row enters the
SCORECARD Capabilities table only on met.

- Counter: `python3 -B .ufo/waves/round-97/c97_reval.py --root . --revision <REV> --work <scratch>`
  (successor of `c96_reval.py`: R96-1 binding, committed-bytes-only reads,
  `/usr/bin/git` with `GIT_NO_REPLACE_OBJECTS=1`, held-out cases seeded from
  the scored commit id, widened anti-table, seventh forgery
  `frozen/neg-lookup-table.py`; docstring lists every change).
- Before (do-nothing instrument set): `c96_reval.py` at base and at the
  instruments revision → `NameError: name 'mutants' is not defined`, exit 1,
  no verdict line (`c2-predecessor-at-base.txt`, `c2-predecessor-at-instr.txt`);
  SCORECARD Capabilities table has no revalidation-exchange row.
- Predicate (frozen sentence): **C2 met ⇔ `c97_reval.py` prints
  `candidate=present`, `hand=37/37`, `generated=G/G`, `heldout=X/X`,
  `forgeries_refused=7/7`, `positive=admitted`, `mutants=14/14`,
  `survivors=none`, `anti_table=ok`, `population=ok`, `met=true` with exit 0
  at the landed content revision, and the scored candidate blob's sha256
  equals the landed `scripts/reval_exchange.py`.**
- Kill rule: any other line or exit lands C2 unmet; no counter byte changes
  after this commit (round-95 Amendment-A rule).
- Main-path proofs and forgery controls (R96-A; public CLI on committed
  fixture revisions where the candidate slot holds the named subject):
  frozen positive control → expect met=true exit 0 (`ctl-c2-slot-pos.txt`);
  lookup-table forgery (memorized answers for every hand and seed-96/97
  input, keyed on a form the anti-table does not search) → expect met=false
  exit 1 via `heldout` (`ctl-c2-slot-table.txt`); oracle-import forgery →
  expect met=false exit 1 (`ctl-c2-slot-oracle.txt`); candidate deleted →
  expect `candidate=absent met=false` exit 1 (`ctl-c2-slot-absent.txt`);
  successor at the round-96 base → expect population drift exit 2 (the
  round-97 forgery is not in that tree: fails closed, never a zero count)
  (`c2-successor-at-r96base.txt`); selftest 8/8 with 14/14 mutants killed
  (`ctl-c2-selftest.txt`).
- The do-nothing control does not reach the target: the instrument the lane
  held cannot produce a verdict line at all. The work this claim is credited
  for is the successor instrument plus the demonstrated, independently
  attacked capability; the candidate's existence alone is not the claim.
- Sourced: the claim's evidence cites S480 (RFC 9111, r96) and a new row for
  the RFC 9111 errata search opened this round (ScoutErrata), whose sweep
  over §4.3.1–§4.3.3 lands in `corpus/knowledge/revalidation-exchange.md`.
- Score: freshness stays 10 (ceiling); the capability row is the move.

## Causal separability

C1 reads only `corpus/README.md` and `corpus/knowledge/*.md`; C2 reads only
the candidate, the frozen population and its own pins. Neither counter reads
a file the other claim changes (the S481 knowledge-entry paragraph adds no
source id to the C1-required set unless its `source:` line changes; if it
does, C1's counter will require that id in the entry's index row, which the
L1 adds in the same content commit — recorded, not hidden).
