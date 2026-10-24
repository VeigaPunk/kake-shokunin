# AttackCase17 — fixture `17-ledger-row-outside-population` (r27 W2, axis: operability)

## Authority / integrity of what was measured
- Frozen candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`.
- Gate `scripts/citing_set.py`: candidate blob `352a471abec08daa56a0fb7ef23fe78f2930d773`; worktree blob identical; sha256 `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228`.
- Consumer runner `scripts/citing_set_selftest.py`: sha256 `3c167895c7f3a4acf531886816bffcbf189d299d6137ca12096265855dd62a1c` (matches `frozen-candidate.json`).
- Fixture bytes at candidate: expected `502c20bb…`, ledger `9c964924…`, population `1705091e…`, corpus `aae803c6…`; worktree blobs identical.
- Live fixture untouched: all four fixture blobs still equal the candidate blobs; `git diff ac46a747… -- scripts/` empty (no tracked change anywhere under `scripts/`). Source read-only.
- Scratch: `/fast/scratch/hyaku/kake-r27/AttackCase17` (TMPDIR set there; no /tmp, no /dev/shm). No tool installs. Python 3.14.8.
- Unattributed artifact observed at 19:03:01 local: untracked `scripts/__pycache__/citing_set.cpython-314.pyc`. Not produced by this lane — every invocation here used `python3 -B` against scratch copies (`$S/citing_set.py` executed as `__main__` writes no bytecode), and no lane command referenced the repo copy as an import. Left in place (not mine to delete); flagged for L1 because it is an untracked write inside `scripts/`.

## Independently derived expectation (declared before any gate run)
From gate source semantics + fixture input bytes (not from expected.json):
- population rows → `{("n",1): "S001"}`; one corpus file; token scan yields exactly `S001` (only `S`+≥3-digit token); no range matches.
- citing set = `{(S001, corpus/knowledge/sitemap-orphan-audit.md)}`; `outsidePopulation = 0` (S019 is never cited).
- ledger: `(S001, file)` is in the citing set → adjudicated; `(S019, file)` is in no citing pair → one `ledger_pair_not_cited`.
- **Derived: exit 1, verdict `failed`, finding multiset {`ledger_pair_not_cited` ×1}, citingPairs 1, ledgerPairs 2, populationRows 1, corpusFiles 1, outsidePopulation 0.**
- Identity predicted from source (`citing_set.py:500`): the display map holds only `S001`, so the fallback yields the bare integer → finding `row` = `"19"`; finding `file` = `"corpus/knowledge/sitemap-orphan-audit.md"` (equal to the ledger `file` value).
- Disclosure: `expected.json` was visible in the same input-read batch (before any gate run). The derivation above was made from gate source + input bytes and predicts identity fields `expected.json` does not record, so it is not an echo of the fixture's expectation.

## Agreement with expected.json
`expected.json = {"exit":1,"findings":["ledger_pair_not_cited"]}` → **agrees** with the derived multiset and with the observed run. Finding-id tally agrees; finding **file** identity agrees; finding **row** identity **disagrees** (observed `"19"` vs ledger row id `"S019"`).

## Actual runs
- PROBE A — `python3 -B $S/citing_set.py --root $S/work/17-ledger-row-outside-population --population population.json --ledger ledger.json --json` (cwd `$S`, unrelated to the fixture): stdout `verdict failed, citingPairs 1, ledgerPairs 2, populationRows 1, corpusFiles 1, outsidePopulation 0, findings [{id ledger_pair_not_cited, row "19", file corpus/knowledge/sitemap-orphan-audit.md}]`; **exit 1** — identical to the derived expectation.
- PROBE B — real consumer runner over case 17 only (`--fixtures $S/fixtures-only`, `--gate` frozen gate): `verdict clean, passed true, cases 1, failed 0`; runner exit 0 (note: case count below the contract minimum of 12, so this is not a contract-level pass by itself).
- PROBE F — real consumer runner over scratch copies of **all 29** cases: `verdict clean, passed true, cases 29, failed 0, meetsContractMinimum true`; runner exit 0.

## One causally meaningful input change (scratch only), expectation declared before running
PROBE C — append one citation line to the scratch corpus copy (`corpus/knowledge/sitemap-orphan-audit.md`, sha256 `29069bc1…` → `56aceda2…`): `source: S019 (corpus/SOURCES.md) - https://example.test/sitemap/orphan-audit §Audit rows`. Population and ledger unchanged.
- Declared: exit 1 / `failed`; multiset **unchanged** {`ledger_pair_not_cited` ×1} because the citing set admits population ids only (S019 excluded), so the pair stays outside it; **no** `unadjudicated_citing_pair`; citingPairs stays 1; outsidePopulation 0 → 1; `row` stays `"19"`.
- Actual: exactly as declared — exit 1, `findings [{ledger_pair_not_cited, row "19", file corpus/knowledge/sitemap-orphan-audit.md}]`, citingPairs 1, outsidePopulation 1, populationRows 1.

Supplementary boundary probe (declared before running):
PROBE D — add `S019` to the scratch population rows (`population.json` sha256 `11942908…` → `12575416…`). Declared: exit 1; multiset {`ledger_pair_not_cited` ×1} with `row` now `"S019"` (population display spelling); citingPairs 1; populationRows 2; outsidePopulation 0; no `unadjudicated_citing_pair` minted for an uncited population row. Actual: exactly as declared.

PROBE E — consumer runner over the PROBE C fixture. Declared: still `clean/passed` (exit and id multiset unchanged). Actual: `verdict clean, passed true, cases 1, failed 0`.

## Findings by severity
**F1 — Medium — row identity of a ledger row outside the population is lossy.** `citing_set.py:500`/`:513` render `display.get(row, … str(row[1]))`; for a row absent from the population display map the integer is emitted, so the report says `row:"19"` while the ledger row id is `"S019"` (`id_key("19") = ("s","19") ≠ ("n",19)`); the offending row id is not recoverable from the report. Observed identically in fixture 26 (`row:"2"` for ledger `S002`) during the 29-case sweep. Bounded impact: C2's measurement (`c2_count.py:26`) consumes `(row,file)` only for `unadjudicated_citing_pair`, whose rows are population rows (correct spelling), and the fixture runner compares ids only — so no measured number changes; the defect is in the report a human/operator reads.

**F2 — Medium — `ledger_pair_not_cited` is emitted for a pair that IS literally cited.** PROBE C: with `source: S019 …` present in the corpus file, the gate still reports `ledger_pair_not_cited` for `(S019, corpus/knowledge/sitemap-orphan-audit.md)`. The id asserts non-citation; the true cause is population exclusion (the citing set is restricted to population ids, `citing_set.py:440/443`). The report carries no field separating the two causes (`outsidePopulation` is a count only). No fixture in the 29-case set covers this condition: the sweep shows `outsidePopulation>0` only in cases 20 (2) and 27 (5), neither of which has an outside-population ledger row.

**F3 — Medium — fixture 17 does not exercise the dimension its name claims.** In the pristine fixture S019 appears nowhere in the corpus, so `outsidePopulation=0` and the observable multiset is identical to fixture 12 (`ledger row merely uncited`). PROBE D shows the flag survives when S019 *is* in the population — i.e. the pristine red is attributable to non-citation alone and the population dimension is inert. Making the fixture genuinely discriminating requires citing S019, which then lands on F2's mislabel.

**F4 — Low — the consumer oracle cannot see row/file identity.** `citing_set_selftest.py:269,272` compares exit + sorted finding ids only; `expected.json` (`{exit, findings}`) has no room for identity fields. PROBE E: after the corpus was mutated so that the flagged pair became literally cited, the runner still reported `clean/passed` (exit 0). So F1/F2 are invisible to the whole fixture suite.

## Residual risk / verification gaps
- Per-case expected.json comparison for all 29 cases was executed only through the runner (PROBE F: 29/29 pass on scratch copies); I did not hand-audit each expected.json.
- The fixture interface is working-tree only (the runner never passes `--revision`), so git-blob mode is not covered by any fixture; it is exercised elsewhere (`c2_count.py`).
- Not executed: outside-population rows with duplicate spellings, alternative ledger `file` spellings, and the numeric-spelling path for an outside-population row; the shared fallback at `:500`/`:513` indicates they all render bare integers — [INFERENCE] from source reading, not measured.
- [INFERENCE] (not observed): a consumer that groups gate findings by row id would mis-group every outside-population ledger row; no such consumer exists in-repo today.
- Nothing in this lane bears on the wave's C1 numbers (58 reviewed / 55 strictly decided / 7 unknown units); C1 status is untouched here.
