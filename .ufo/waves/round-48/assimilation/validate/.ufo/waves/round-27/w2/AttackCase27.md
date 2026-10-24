# AttackCase27 — fresh falsification of consumer fixture `27-range-endpoint-outside-population`

Seat: KakeR27.AttackCase27 · lane: leaf (no dispatch) · axis: **operability** · milestone: r27-fresh-falsification.
Frozen candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835` (HEAD == candidate); gate blob
`352a471abec08daa56a0fb7ef23fe78f2930d773` == candidate `scripts/citing_set.py`, file sha256
`3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228` == `frozen-candidate.json` `sourceFiles` entry;
runner sha256 `3c167895c7f3a4acf531886816bffcbf189d299d6137ca12096265855dd62a1c` == frozen entry. Python 3.14.8, no installs.

**Attacked item** (read-only in repo): `scripts/fixtures/citing-set/27-range-endpoint-outside-population/` —
corpus `fed5dd57497bae9e346bf3664aae3922470d60bc435fe0c5ddc700d7615d6221`, `expected.json`
`49d7286dd34a00ce88a31d473272e589cb5542e76d60505cd9591437ee353e81`, `ledger.json`
`7c79a345464cf2915b1d4f8b210d938a1a70368eb86be2981fa5bb99272d969b`, `population.json`
`407f994f83ab861e56d853a6de95205732e366c2eaa7248ce3d1bbaba803e61c` — all four == the `frozen-candidate.json`
entries (byte-identical to the frozen target; live fixture never edited).
Scratch only: `/fast/scratch/hyaku/kake-r27/AttackCase27/` (TMPDIR/TMP/TEMP set explicitly; no /tmp, no /dev/shm).

## Independent derivation — declared BEFORE any gate run

Own sweep of the fixture inputs (my own regex, not the gate's): literal tokens `['S090','S095']`; range spans
`['S090-S095']` (one file) expanding to S090…S095 inclusive; `population.json` rows `['S092']`; `ledger.json` pairs `[]`.
Hence expanded citing set ∩ population = `{(S092, corpus/knowledge/ops-automation.md)}`; S090/S091/S093/S094/S095 are
cited but outside the population (counted, never findings per contract C2 semantics); ledger empty ⇒ no
`ledger_pair_not_cited` / `ledger_duplicate_pair`; range ascending, span 5 ≤ 200 ⇒ no `citation_range_invalid`;
inputs well-formed ⇒ no `input_invalid`.
**Declared expected: exit 1, verdict `failed`, finding-id multiset {`unadjudicated_citing_pair` ×1},
identity row `S092` / file `corpus/knowledge/ops-automation.md`, citingPairs 1, outsidePopulation 5.**

## Probe A — real frozen gate CLI, scratch copy, unrelated cwd

Scratch copy `/fast/scratch/hyaku/kake-r27/AttackCase27/base` (four files sha256-identical to the live fixture).
Command (cwd `/home/vgpnk`, `$SEAT` = that scratch dir): `TMPDIR=$SEAT/tmp TMP=$SEAT/tmp TEMP=$SEAT/tmp python3 -B
/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/citing_set.py --root $SEAT/base --population population.json
--ledger ledger.json --json` (stdout+exit captured to `$SEAT/run4.json`).
Actual: `EXIT=1`; stdout `{"verdict":"failed","citingPairs":1,"ledgerPairs":0,"findings":[{"id":
"unadjudicated_citing_pair","row":"S092","file":"corpus/knowledge/ops-automation.md"}],"populationRows":1,
"corpusFiles":1,"outsidePopulation":5,"source":"working-tree","revision":null}`; stderr empty; identical output from
cwd `$SEAT/cwd` and cwd `/home/vgpnk`.
**Comparison with fixture `expected.json` (`exit 1`, `["unadjudicated_citing_pair"]`): exit agrees; id multiset agrees
1:1 (no disagreement).** Identity checked independently of `expected.json` (which carries no row/file): the reported
row `S092` is in `population.json` rows, the reported file exists under `corpus/knowledge/` and is the only corpus
file, and `outsidePopulation == 5` is only reachable if the range was expanded to S090…S095 (literals alone → 2).
No row/file disagreement.

## Probe B — ONE causally meaningful input change (population widened to the range endpoints)

Change (scratch variant only; corpus/ledger/expected untouched): `population.json` rows `['S092']` →
`['S090','S092','S095']` (sha256 `8961db81c45cd7be48f2c44cce11001ab57760e65e76b9399885ed306ae0559a`).
Declared before running: citingPairs 3; findings exactly 3 × `unadjudicated_citing_pair` with rows {S090,S092,S095} in
`corpus/knowledge/ops-automation.md`; outsidePopulation 3 (S091,S093,S094); ledgerPairs 0; no other finding ids;
verdict failed; exit 1. Falsify conditions declared: citingPairs 1 ⇒ endpoints not expanded; citingPairs 6 ⇒ population
intersection ignored; exit ≠ 1 ⇒ verdict logic wrong.
Actual: `EXIT=1`; `citingPairs 3`, `ledgerPairs 0`, findings rows `S090`,`S092`,`S095` all in
`corpus/knowledge/ops-automation.md`, `populationRows 3`, `corpusFiles 1`, `outsidePopulation 3`, verdict `failed`.
**Matches the declared expectation exactly; no falsify condition met.** Consequence: the baseline single finding is
causally attributable to population intersection of an expanded range — the fixture's expected count is a function of
the input, not a constant; a gate ignoring the population would report 6, one dropping ranges 0.

## Probe C — real consumer fixture runner over the scratch case

`python3 -B scripts/citing_set_selftest.py --root <repo> --fixtures $SEAT/cases --gate <repo>/scripts/citing_set.py
--tmpdir $SEAT/tmp --min-cases 1 --json` (case dir = copy of the fixture).
Actual: `EXIT=0`, `verdict clean`, `cases 1`, `failed 0`, per-case `expected` = actual (exit 1, ids
`["unadjudicated_citing_pair"]`); runner notes the 1-case directory is below the contract minimum of 12 (expected for a
single-case slice).

## Integrity / no-harm

Live fixture re-hashed after all runs: all four sha256 identical to the frozen-candidate entries above.
`git status --porcelain scripts/` → empty. No source, doc, registry, MANIFEST or sibling-file writes; only the report
and scratch under `/fast/scratch/hyaku/kake-r27/AttackCase27/`. No mutant source was built (leaf read-only seat).

## Findings by severity

1. **Medium — the fixture oracle is identity-blind (whole suite, not just case 27).** `scripts/citing_set_selftest.py`
   `run_case` compares only the process exit code and `sorted(finding_ids(report))`; the contract's fixture shape
   `{exit:int, findings:[finding-id,...]}` carries no row/file field. Consequence: a gate that reported the wrong row
   (e.g. `S091`) or a wrong file for case 27 — or for any of the 29 cases — would still be green, because the id
   multiset would be unchanged. My seat verified row/file identity for case 27 only (Probe A identity check, Probe B row
   set); the other 28 cases have no such assertion from me. This is a contract-level coverage gap, not a contract
   violation, and `expected.json`'s shape is contract-mandated, so I did not alter it. [INFERENCE] L1 decision needed if
   identity is to be enforced: extend the oracle with optional `rows`/`files` expectations, or accept identity as
   out-of-fixture scope.
2. **Low — case 27 exercises only the missing-pair side.** Its ledger is empty, so it can only ever express "cited but
   unadjudicated"; it does not show that a ledger entry for a range-derived pair is honoured. That direction is covered
   by other cases (03 en-dash, 04 hyphen, 05 dotdot, 06 to, 07 through carry ledger pairs for range rows and expect
   exactly one `unadjudicated_citing_pair`), so C2's range-aware claim is not read as resting on case 27. Recorded so
   the ledger side of case 27 is not double-counted as covered.
3. **Low — out-of-population ids are observable only as a count.** The report exposes `outsidePopulation` (5) but never
   the ids, so no fixture's assertion surface pins *which* ids are outside the population; a regression in the
   per-id accounting (e.g. counting only literal tokens, 2 instead of 5) would pass every fixture while still passing
   Probe B. Probe B constrains the citing-set expansion, not the counter's per-id content.

## Residual risk / verification gaps

- Only the working-tree source mode was exercised (`source: working-tree`); the `--revision` git-blob mode was not run for
  case 27 (the fixture interface is working tree; case 18 is the working-tree case).
- The suite-wide 29/29 claim rests on the author's run; this seat observed one case and one consumer-runner slice.
- No mutant gate was built (out of lane), so "a gate without population intersection would report 6 findings" is
  analytic; Probe B is the executed corroboration that the observed count tracks the population input.
- No policy/content refusal; no browser/account/auth/credential/publication operations; no network use.
