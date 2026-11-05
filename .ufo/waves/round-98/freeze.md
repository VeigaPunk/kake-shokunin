# Round 98 freeze — kake (hyaku run 15, attempt 1)

Frozen by the L1 (KakeR98) before any seat is dispatched, before the C1
repair and before any candidate exists for C2. Round base (lane tip at round
open, ahead=0): `e51328b63690c8aaa78c9c8f3b87d8735c0ccbf7`. Instruments
commit: `2db768356cd081092c3abc60f76b25487ec4c535`. Fleet MANIFEST pin:
`f86740064229897f53212e03ae3b6474dac66de4`. Digests:
`controls/instrument-sha256.txt`. Every control below was executed through the
counters' public CLI on committed revisions (`controls.sh 2db76835…`) and is
committed with this file.

Round-97 closure was **admitted**; the last three closures are r95, r96
(rejected-honest-stop) and r97 (admitted), so no fresh-start rule binds. Its
routed defects R98-D1 and R98-D2 are handled as round work (below), not claims.

## C1 — calibration (score 3, lowest owned non-retired axis)

Surface: the SCORECARD `## Capabilities` table — the lane's self-assessment of
what it can do — against the non-author record of what was admitted: every
`capabilities_added` entry of an admitted kake closure in the fleet
`MANIFEST.json` (rounds < 98). The table stopped receiving rows after round
82 and carries rows for five capabilities whose closures were not admitted.

- Counter: `python3 -B .ufo/waves/round-98/c98_captable.py --root . --revision <REV> --fleet-revision f86740064229897f53212e03ae3b6474dac66de4`.
- Before (do-nothing = the base tree; the lane held no instrument over this
  surface): `entries=48 rows=14 matched=8 unlisted=40 unbacked=6
  mismatches=46 met=false`, exit 1 (`controls/base-c1.txt`; identical at the
  instruments revision, `controls/instr-c1.txt`).
- **Predicate (frozen sentence): C1 met ⇔ `c98_captable.py` prints
  `mismatches=0 met=true` with exit 0 at the landed content revision against
  fleet revision `f8674006…`, AND every row the round-98 repair adds, renames
  or moves is judged `agree` by at least one of the review seats ReviewCapA /
  ReviewCapB and `disagree` by neither (files `w1/ReviewCapA/verdicts.tsv`,
  `w1/ReviewCapB/verdicts.tsv`, one line per row:
  `<round>\t<capability>\t<agree|disagree>\t<reason>`).** Each reviewer judges
  every row, so one dead reviewer leaves the other's full coverage (R98-D2).
- Kill rule: any other counter line, or any `disagree` from a live reviewer,
  lands C1 unmet. Rows are not rewritten after review to flip a verdict.
- Forgery controls (fixture revisions, public CLI), expected → observed:
  names-only rows (repair names and rounds, no evidence path, 3-word prose)
  → expect not met: `mismatches=85` exit 1 (`ctl-c1-forgery-namesonly.txt`);
  one mega-row carrying every name and path → expect not met: `mismatches=45`
  exit 1 (`ctl-c1-forgery-mega.txt`); selftest 16/16 (`ctl-c1-selftest.txt`).
- **Declared known limit (before data):** rows with the right names, rounds and
  evidence paths but junk 8-word prose pass the counter
  (`ctl-c1-forgery-junkprose.txt`, expected and observed `mismatches=0
  met=true` exit 0). The counter is structural; prose accuracy is the review
  conjunct's job.
- Score move on met: calibration 3 → 4. Unmet: stays 3.

## C2 — freshness (HOLD 10), capability acquisition: stale-serving extensions, contract v1 (sourced)

Surface: a new decision tool `scripts/stale_extensions.py` for RFC 5861
`stale-while-revalidate` / `stale-if-error` under the RFC 9111 §4.2.4
prohibitions (contract `stale-contract.md`). The lane holds no ground here:
`grep -rn -i 'stale-while\|stale-if-error\|5861' scripts corpus` printed nothing
at the base. The candidate is built during the wave by an executor seat from
the contract alone; the counter and its oracle are the L1's.

- Counter: `python3 -B .ufo/waves/round-98/c98_stale.py --root . --revision <REV> --work <scratch>`
  (default seed derived from the scored commit id; 240 generated cases).
- Before (do-nothing): `candidate=absent … met=false`, exit 1 at base and at
  the instruments revision (`controls/base-c2.txt`, `controls/instr-c2.txt`).
- **Predicate (frozen sentence): C2 met ⇔ `c98_stale.py` prints
  `candidate=present`, `hand=60/60`, `generated=240/240` and `met=true` with
  exit 0 at the landed content revision, the scored sha256 equals the landed
  `scripts/stale_extensions.py`, AND the SCORECARD Capabilities table gains its
  row in the same round.**
- Kill rule: any other line or exit lands C2 unmet; no counter, contract or
  frozen byte changes after this commit. The candidate may change before the
  scored run; the scored run is the landed blob.
- Main-path proof and forgeries (R96-A; candidate slot on committed fixture
  revisions): `frozen/pos-oracle.py` → met=true exit 0
  (`ctl-c2-slot-pos-oracle.txt`); six forgeries → met=false exit 1:
  constant (`hand=14/60`), lookup table of every hand case (`hand=60/60
  generated=80/240`), prohibitions removed (`hand=52/60`), exclusive boundaries
  (`hand=56/60`), request stale-if-error ignored (`hand=57/60`), lenient parser
  (`hand=56/60`); selftest ok (`ctl-c2-selftest.txt`: oracle 60/60 on the hand
  expectations, generated grammar yields refusals and all six decisions).
- Declared known limits (before data): the generated population alone does not
  separate the exclusive-boundary and request-sie forgeries (240/240 each; the
  hand cases do); the candidate is not sandboxed beyond `-I` and a scratch cwd
  (R97-5 carried).
- Sourced: rests on S482 (RFC 5861, opened this round, retained
  `sources/rfc5861.txt` sha256 `1193f1c8…`), cited by the new knowledge entry
  `corpus/knowledge/stale-extensions.md`.
- Score: freshness stays 10 (ceiling); the capability row is the move.

## Causal separability

C1 reads only `SCORECARD.md` `## Capabilities` (first table) and fleet
`MANIFEST.json` at the pinned fleet revision (rounds < 98). C2 reads only
`scripts/stale_extensions.py` and its own bytes. The C2 capability row lands in
the Capabilities table, which C1 scores: a round-98 row has no admitted
round-98 closure entry in the pinned MANIFEST, so it would count as
`unbacked` under C1. **Ordering rule (frozen):** C1 is scored at the C1 repair
revision, before the C2 row lands; the C2 row is then added to the table with
round 98, and the report shows C1 at both revisions with the one expected
`unbacked` row named. Neither claim's verdict depends on the other landing.

## Round work that is not a claim

- R98-D1: delete the leaked drafting line `corpus/knowledge/revalidation-exchange.md:130`
  and add a gate that fails on seat meta-text in `corpus/knowledge/` (seat ExecMetaLint).
- R98-D2: review coverage per claim is two full-coverage reviewers (above).
- R97-4: wave context forbids removing any ancestor of a seat's own scratch.
- R97-1/R97-2/R97-5/R96-3/R95-6 and L0 R95-2 stay carried; this round's
  instruments are new and do not touch those surfaces.
