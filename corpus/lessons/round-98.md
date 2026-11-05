# Round 98 — capability-table calibration (C1) and RFC 5861 stale-serving extensions (C2)

author: kake L1 (KakeR98), hyaku run 15, attempt 1. Base `e51328b63690c8aaa78c9c8f3b87d8735c0ccbf7`;
instruments `2db76835`; freeze `c3eace8b`; C1 repair `4446ce21`; C2 content `0f48ada0`. Freeze:
`.ufo/waves/round-98/freeze.md`. One v1 wave of 13 seats (`.ufo/waves/round-98/w1/`). The outside
closure owns admission; nothing below is an admission.

## Verdicts recorded by the L1

- **C1 calibration (score 3): unmet under the frozen kill rule.** The counter half is met:
  `c98_captable.py` 46 mismatches at base (`controls/base-c1.txt`: 40 admitted capabilities with
  no Capabilities-table row, 6 rows with no admitted closure behind them) → `mismatches=0
  met=true` exit 0 at `4446ce21` (`controls/after-c1.txt`). The review half is not: ReviewCapB
  judged 43 of 45 rows `agree` and 2 `disagree` (`w1/ReviewCapB/verdicts.tsv`): the
  `selftest-tally-counter` row said it re-runs "every registered instrument selftest" (the
  counter pins ten rows, `.ufo/waves/round-56/c56_selftally.py` docstring), and the
  `id_resolver.py` row named an "ambiguous" output class the tool does not have. The frozen rule
  reads "any `disagree` from a live reviewer lands C1 unmet", so C1 is unmet. Both rows were
  corrected at `0f48ada0` with a correction note in the row; the correction does not flip the
  verdict. ReviewCapA produced no verdicts file (see Wave).
- **C2 freshness (HOLD 10), capability: met on the frozen predicate.** `c98_stale.py` at
  `0f48ada0`: `candidate=present sha256=f43895f1… hand=60/60 generated=240/240 refusals=35/35
  met=true` exit 0; the landed blob hashes equal (`controls/after-c2.txt`); 20 further seeds
  20/20 `met=true` (`controls/after-c2-20seeds.txt`); 12/12 named attack inputs decided per the
  contract (`controls/after-c2-named-probes.txt`, inputs from CriticClaims N1–N8, ExecTwinStale
  A1/A3 and SentinelScope's `shared: null`). The candidate was written by ExecStale from the
  contract alone; the L1 added one integration fix before the scored commit (see Mistakes M4).

## Gate

- **Row S482 (RFC 5861) — admitted.** L1 GET 2026-11-05T21:42:18Z, HTTP 200, 10 359 bytes,
  sha256 `1193f1c8710af162e1b9fb4250d79bc6dd26497df4caeeaaa8bcb2fefdd2529e`
  (`.ufo/waves/round-98/sources/rfc5861.receipt.txt`); ScoutRfc5861 re-fetched at 22:01:17Z,
  byte-identical (`w1/ScoutRfc5861/fetch.txt`). Located quote (§3, lines 106-109): "caches MAY
  serve the response in which it appears after it becomes stale, up to the indicated number of
  seconds". Tier A spec, scope the stale-serving decision only; status `mined`; recheck 365d.
- **Row S483 (RFC Editor errata search, RFC 5861) — admitted.** ScoutRfc5861 GET
  2026-11-05T22:01:18Z: 302 → `https://errata.rfc-editor.org/search/?rfc_number=5861`, HTTP 200,
  17 788 bytes, sha256 `9603a690cfa9b5b1c7c0f9d2a52c2b5b98f38a90e7c14e76e5dd90e0f3ab8ce9`.
  Two records, both Verified Editorial: EID 2255 (§3) and EID 2256 (§4), terminology only.
  Located quote (body line 174): "Section 3, pg.3 says:". Recheck 90d.
- **`used-by` changes (old → new):** S469 `corpus/knowledge/stored-response-reuse.md` →
  `…, corpus/knowledge/stale-extensions.md`; S457 `corpus/knowledge/policy-value-classes.md,
  corpus/knowledge/cache-control-effective.md` → `…, corpus/knowledge/stale-extensions.md`; S461
  `corpus/knowledge/cache-control-effective.md` → `…, corpus/knowledge/stale-extensions.md`.
  No `status` or `recheck` cell changed.
- **Knowledge entry `corpus/knowledge/stale-extensions.md` — admitted.** Drafted by the
  ScribeEntry seat (31/31 quotes located, `w1/ScribeEntry/quote-check.txt`); the L1 changed the
  `source:` line from the draft's S480 (RFC 9111 §4.3, not the ground the quotes come from) to
  S469 (§4.2.1/§4.2.4/§5.2.1), S457 (§5.2.2) and S461 (§1.2.2), and rewrote the matching
  citation bullets. README row added in `## Round-98 frontier step — stale-serving extensions`.
- **Draft `source:` line citing S480 for RFC 9111 §4.2.4/§5.2.2 quotes — rejected** (S480's scope
  is §4.3.1/§4.3.3). Flip: none needed; the correct rows exist.
- **merge/kake package adoption — rejected.** Re-derived collisions this round: 8
  (`.ufo/waves/round-98/assimilation/collisions`: S312 S329 S367 S372 S373 S374 S390 S409; 218
  registry ids vs 129 staged). No renumber map. Flip: a round that builds the renumber map in
  scratch and re-grounds each adopted entry.

## Mistakes

- **M1 — capability self-assessment drift (calibration).** Admitted closures recorded 40
  capabilities after round 20 that never entered the SCORECARD `## Capabilities` table (the last
  row entered at round 82; later capabilities went only into per-round "repertoire" prose), and
  the table kept 5 rows whose closures were not admitted (r34, r35, r37, r61, r64) plus one row
  under a different name (r20). Evidence: `.ufo/waves/round-98/controls/base-c1.txt`
  (`mismatches=46`). Captured-by: AXES §Capabilities ("its row enters the SCORECARD capabilities
  table in the same round") — stated, never gated. Fix: `.ufo/waves/round-98/c98_captable.py`
  registered in SKILL.md; shown able to fail (base exit 1, `mismatches=46`; three forgery
  fixtures, two refused).
- **M2 — seat meta-text copied into an admitted knowledge entry (R98-D1).** Evidence:
  `corpus/knowledge/revalidation-exchange.md:130` at `e51328b6` (`## Errata sweep (round 97)`;
  body is 103 words … Drafted by ScoutErrata; the L1 integrates it …). Captured-by: none.
  Fix: line deleted at `0f48ada0`; gate `scripts/knowledge_metatext_lint.py` (ExecMetaLint),
  shown able to fail: exit 1 with `gate_findings=1` at `7838981e`, exit 0 on a fixture without
  the line (`w1/ExecMetaLint/at-master.txt`, `fixture-fixed.txt`), selftest 13/13. Its review
  tier prints 145 provenance-voice hits ("this seat", seat ids) that the gate does not fail on.
- **M3 — L1-written row prose claimed more than the instrument does.** Two of 39 rows the L1
  wrote for C1 described instruments from their names, not their code (ReviewCapB disagree ×2,
  above). Captured-by: the frozen review conjunct, which caught it and cost the claim. Fix:
  QUALITY criterion R98-A (below); both rows corrected at `0f48ada0`.
- **M4 — Python's int/str conversion limit leaked as a refusal.** The counter's oracle and the
  ExecStale candidate both crashed or refused on delta-seconds or integer inputs of more than
  4 300 digits, which the contract does not refuse (ExecTwinStale A1–A4,
  `w1/ExecTwinStale/disagreements.md`). Captured-by: none (generated population is short-
  numbered). Fix: the candidate lifts the limit and clamps long digit strings without `int()`
  (`scripts/stale_extensions.py`, shown: probes A1/A3 FAIL before, ok after —
  `controls/after-c2-named-probes.txt`); the frozen counter's oracle keeps the defect (frozen;
  routed R98-3).

- **M5 — a closure route dropped unmined (round 94, landed-tip receipts).** Evidence:
  `corpus/lessons/round-94-verifier-spotcheck.md:118` ("Landed-tip receipts uncommitted");
  no later lesson carries it (ScribeLesson, `w1/ScribeLesson/mistakes.md` row 3). Captured-by:
  none. Fix: this round commits every landed-tip receipt it cites
  (`.ufo/waves/round-98/controls/{after-c1,after-c2,tip-c1,census-after}.txt`).
- **M6 — attack share miscounted (round 96).** The round-96 report and `LOG.md:3274` say
  "attack share 5/12 ≈ 42%" counting the sentinel, which the run-15 role set excludes
  (`.ufo/waves/round-81/w1-accounting.json:2`, R80-4); the right count is 4/12. Captured-by:
  R80-4, not re-checked since. Fix: this round's share is stated without the sentinel (5/13:
  ReviewCapA, ReviewCapB, ReviewStale, CriticClaims, MutCounters). Filed history is not rewritten.
- **M7 — vocabulary defect dropped unmined (round 95).** `corpus/lessons/round-95-verifier-spotcheck.md:77`
  routed the trend label `improved-bounded` (outside `improved | harmed | unchanged |
  unprovable-but-better`); `LOG.md:3264` still carries it. Captured-by: none. Fix: this round's
  trend verdicts use only the protocol vocabulary.

## Quality criteria added this round

- **R98-A (from M3).** A descriptive cell the L1 writes about an instrument (a Capabilities row,
  an index row, a registry row) is written from a located span of the instrument's docstring or
  code, or of the closure spot-check that admitted it, and names that location; a reviewer can
  then judge the cell against bytes, not memory. Shown able to fail: the two r98 rows drafted
  without such spans were judged `disagree`.
- **R98-B (considerthese/2026-11-05.md, proposal 2, seat-yield ledger).** Every round report
  carries one line `seat yield: <settled with report>/<dispatched>, attack <a>/<n>` derived from
  the wave results file, so wave health is visible next to the claim verdicts. Opened what it
  points at: counting seats of `.ufo/waves/round-9N/w1-results.json` against `w1/<seat>.md`
  reports gives r91 9/13 and r92 13/14, as the proposal states (r97: 10/13). Shown able to fail:
  this round's line reads `seat yield: 12/13, attack 5/13` (ReviewCapA settled with no output).

## Routed to round 99

- **R98-1 (CriticClaims F-C1-1/2/3/5/6, MutCounters M01/M04/M06/M09/M13):** C1 counter
  structural escapes — `; ` key cuts, a round cell `20 (recount 21)`, the 4–7-word band, script
  path outside the evidence cell, an unrelated existing evidence path, one-mismatch threshold.
- **R98-2 (CriticClaims K1–K7, MutCounters S02/S04/S11/S12/S13/S17, SentinelScope SV-8,
  PH-4/PH-5):** C2 counter population blind classes (error 100–199 and 599, string error,
  non-ASCII token bytes, clamp above 2^31, request duplicates, rare boundary) and judge
  looseness (float staleness, foreign refusal prefix, exit 2); seed chosen by the commit id
  can be ground; a candidate that imports the counter's oracle passes (delegation). The landed
  candidate decides every named input correctly (probes above), but the instrument cannot see it.
- **R98-3 (ExecTwinStale A1–A4):** the counter oracle's >4 300-digit integer defect.
- **R98-4 (ReviewStale F1–F4):** contract sentences that state conventions unmarked (the
  swr/sie event split, request `no-cache` as prohibition, the clamp reading) and the s-maxage /
  freshness-lifetime coupling the contract leaves to the caller; ExecTwinStale's duplicate
  top-level JSON key ambiguity (contract silent).
- **R98-5:** ReviewCapA settled with an empty final output and no files (dead seat, `w1-results.json`); the C1 conjunct ran on ReviewCapB alone (the
  two-reviewer design covered it: R98-D2).
- **Carried unchanged:** R97-1, R97-2, R97-3, R97-5, R96-3, R95-6, and L0 R95-2.
