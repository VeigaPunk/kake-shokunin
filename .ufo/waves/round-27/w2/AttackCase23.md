# AttackCase23 — consumer fixture `23-glued-to-range-separator` (r27 fresh falsification, axis: operability)

Attacked item: `scripts/fixtures/citing-set/23-glued-to-range-separator/` consumed by
`scripts/citing_set.py` (gate) + `scripts/citing_set_selftest.py` (fixture runner).
Frozen candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`; HEAD == candidate, tree `7a20eeae…`
== candidate tree. Gate blob at candidate == worktree `352a471abec08daa56a0fb7ef23fe78f2930d773`,
runner blob `c69b09b2e47f4115aa4e8ff286aa7cfe0e171a64`; fixture blobs corpus `c25fe589…`, expected
`b741e718…`, ledger `24fecc53…`, population `6cd6a1f7…`; `git diff ac46a747 -- scripts/fixtures/
citing-set/23-glued-to-range-separator scripts/citing_set.py scripts/citing_set_selftest.py` →
empty (frozen inputs not rewritten). Python 3.14.8. No source, live fixture, index, MANIFEST or
fleet writes; no tool installs. TMPDIR/HOME confined to `/fast/scratch/hyaku/kake-r27/AttackCase23/`.

## P1 — base run on scratch copy, from unrelated cwd
Input (one corpus file `corpus/knowledge/publish-queue.md`): front-matter
`source: S001toS006 (corpus/SOURCES.md) - https://example.test/publish/queue-rows §Queue rows`;
body/EOF prose carries no other `S###`. Population = S001…S006 (6 rows). Ledger = 3 pairs
(S001, S003, S006) on that file.

**Declared expectation, derived from input + contract grammar before running** (contract C1
denominator: literal `S`+≥3 digits and ranges with `S` at both ends separated by
hyphen/en-dash/em-dash/`..`/`to`/`through`; gate docstring: separator may abut the digits):
`S001toS006` is ONE range (declared `to` separator, glued) expanding inclusively to S001–S006; the
literal-token rule matches neither endpoint (each digit abuts a word char), so the citing set is
exactly {S001…S006} × {the one file} = 6 pairs; the ledger adjudicates S001/S003/S006, so
S002/S004/S005 are unadjudicated → exit **1**, findings = **3 × `unadjudicated_citing_pair`** with
rows **S002, S004, S005** and file **corpus/knowledge/publish-queue.md**; verdict `failed`,
citingPairs 6, ledgerPairs 3, outsidePopulation 0, no `ledger_pair_not_cited`.

Command (cwd `/fast/scratch/hyaku/kake-r27/AttackCase23`, scratch copy, not the live fixture):
`python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/citing_set.py --root
/fast/scratch/hyaku/kake-r27/AttackCase23/case23 --population population.json --ledger ledger.json
--json` → EXIT=1, stdout `verdict failed, citingPairs 6, ledgerPairs 3, populationRows 6,
corpusFiles 1, outsidePopulation 0, source working-tree, revision null`; findings
`unadjudicated_citing_pair/S002/corpus/knowledge/publish-queue.md`, `…/S004/…`, `…/S005/…`.
Scratch corpus sha256 `55f48681fbcfce4c4c4d30a99565e229065a051944fcca5a24adc41e043f863d`.

**Result: exact agreement with the independently declared expectation** (exit, id multiset,
per-finding row identity, file identity, citingPairs/ledgerPairs). It also agrees with the fixture's
`expected.json` (`exit 1`, 3× `unadjudicated_citing_pair`) — but the oracle values were read only
after the derivation above. No row/file disagreement found.

Consumer path, same scratch copy (`citing_set_selftest.py --fixtures <scratch>/fixtures-only`):
verdict `clean`, passed true, exit 0, case `ok: true`. Live suite (29 fixtures, `--min-cases 12`):
verdict `clean`, passed true, cases 29, failed 0, meetsContractMinimum true, exit 0; case 23 ok.

## P2 — one causally meaningful input change (scratch only)
Change (scratch copy `case23-mut`; live fixture untouched, `git hash-object` still `c25fe589…`): the
glued range separator `to` → `+` (`S001toS006` → `S001+S006`), the only altered bytes; mutated
corpus sha256 `1b73096094130b67f968398e23a10bab511a81e1353eac37fbb4f1398e994273` (pristine `55f48681…`).

**Declared expected consequence before running:** `+` is not a declared separator, so the range
rule no longer matches; but `+` is a non-word delimiter, so both endpoints become *literal* tokens
→ the citing set collapses to {S001, S006} (2 pairs), interior rows S002/S004/S005 are cited
nowhere, the ledger's S003 is no longer cited → exit **1** with exactly **one**
`ledger_pair_not_cited` (row S003, same file) and **zero** `unadjudicated_citing_pair`; citingPairs
2, ledgerPairs 3, outsidePopulation 0.

Actual (same CLI, `--root …/case23-mut`): EXIT=1, stdout `verdict failed, citingPairs 2, ledgerPairs
3, outsidePopulation 0`; findings = `ledger_pair_not_cited/S003/corpus/knowledge/publish-queue.md`
(1). **Matches the declared consequence exactly.** Causal reading: the three base findings are
produced *solely* by range expansion over the glued `to` separator, not by literal-token scanning;
the interior rows are reachable only through the range reading, exactly as the fixture's prose
asserts. Same mutated copy through the consumer runner: verdict `failed`, passed false, exit 1,
reason `finding-id mismatch: expected [unadjudicated_citing_pair ×3], observed
[ledger_pair_not_cited]` → the oracle is not vacuous.

## Findings (severity order)
1. **MEDIUM — the fixture oracle is blind to row/file identity (contract-level weakness, not a
   breach).** `expected.json` carries only `exit` + finding-id multiset (the contract's
   `fixtureInterface` says exactly that), and `run_case` in `scripts/citing_set_selftest.py`
   compares only exit and sorted ids. Runtime witness: fixtures `12-noncited-ledger-pair`,
   `17-ledger-row-outside-population`, `26-ledger-pair-file-absent` have byte-identical
   `expected.json` (`{"exit":1,"findings":["ledger_pair_not_cited"]}`) while their real findings
   differ — observed `S002/corpus/knowledge/probe-delta-alerting.md`,
   `19/corpus/knowledge/sitemap-orphan-audit.md`, `2/corpus/knowledge/retired-channels.md`. A gate
   regression that mislabels the row or file of a finding keeps all 29 fixtures green. For *this*
   case the identity is correct (verified above), so no disagreement; the exposure is future-
   proofing of the fixture layer only — the production C2 oracle `.ufo/waves/round-27/c2_count.py`
   does compare `(row,file)` sets, so the 16-pair C2 measurement is not exposed.
2. **LOW–MEDIUM — the gate's `--revision` (GitSource) path is exercised by neither the 29 fixtures
   nor the C2 counter.** The runner never passes `--revision` and no fixture contains a `.git`;
   `c2_count.py` materialises the frozen snapshot into a temp root and runs the extracted gate in
   working-tree mode. My read-only probe at the frozen revision (`citing_set.py --root
   /home/vgpnk/Projects/shokunin/kake-shokunin --revision ac46a7472d945a6d7ff135e4d7f07b0b6913d835
   --population/--ledger <fixture 23 json>`) → EXIT=1, `source git`, `revision ac46a747…`,
   `corpusFiles 26`, verdict `failed` — the git path works, but a regression there turns no
   fixture red.
3. **INFO — no defect found in the attacked fixture.** Behaviour, id multiset, per-finding row and
   file identity, runner verdict and full-suite state all match independent derivation; the single
   mutation is causally decisive and the oracle reacts.

## Residual risk / verification gaps
- `expected.json` cannot itself pin row/file identity, so P1's identity result is author-side
  observation, not oracle-enforced (finding 1); git-mode behaviour rests on my single read-only
  probe (finding 2). Pre-fix failing gate, C1 counters and r24/r26 material were not re-run.
- `[INFERENCE]` the C2 layer as a whole still looks consistent with the frozen oracle, but that
  layer was not my seat's target and was not independently re-derived here.
- Disclosure: the shared worktree gained an untracked `scripts/__pycache__/citing_set.cpython-314.pyc`
  at 19:03:01 — a module-import artifact, not produced by my invocations (verified: running the
  gate as a script, with or without `-B`, creates no `__pycache__`); I neither created nor removed it.
