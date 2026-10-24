# BuildFixtures — r27 citing-set fixture corpus (author-side findings)

Seat: `KakeR27.BuildFixtures` (executor, axis: operability, milestone r27-full-citing-set).

## What was authored

- Worktree: `/fast/scratch/hyaku/kake-r27/writer-fixtures`, branch `kake-r27-fixtures`, base `be375d90afc6fc7aca369ab3cf5247bf460aeed2` (worktree pre-created by the dispatcher; observed HEAD == base, `git status` shows only `?? scripts/fixtures/`).
- Authored path (only): `scripts/fixtures/citing-set/**` — 29 case directories, 118 files.
- No commit made (L1 integrates). No other repo path, no live lane, no `scripts/` file, no gate/selftest file touched.
- Authoring scratch (outside the worktree): `/fast/scratch/hyaku/kake-r27/fixtures-scratch/gen_fixtures.py` (content generator; holds the authored corpus/ledger/population text and the authored expected values).
- Tree digest (sorted `path\0sha256\n` over all 118 files): `dcbb40d576e78f1cc55c1e63ba189ae34a12b93c35ad415e030355215ad99bd4`.
- Tool installs: none (no install needed or performed).

Fixture layout per case: `corpus/knowledge/<entry>.md|.json`, `population.json` (`{"round":27,"baseline":...,"rows":[{"id","kind","tier","scope"}]}`), `ledger.json` (`{"round":27,"pairs":[{"row","file","statements","stale","report"}]}`), `expected.json` (`{"exit":int,"findings":[<finding-id>,...]}`). `expected.json` carries **ids only**, sorted ascending, duplicates retained — the frozen contract's fixture interface. No extra keys, no extra files inside a case dir, nothing referenced outside the case dir.

## Interface facts the expectations encode (frozen contract + author confirmations)

Contract `gateInterface.fixtureInterface` + `gateInterface.output` (`.ufo/waves/round-27/contract.json`), confirmed in writing by the gate author `KakeR27.BuildGate` and the runner author `KakeR27.BuildSelftest`:

- CLI per case: `python3 -B scripts/citing_set.py --root <case-dir> --population population.json --ledger ledger.json --json`; runner compares exit + sorted multiset of finding ids.
- Exits: 0 clean, 1 failed, 2 could-not-evaluate, 64 usage. Ids exactly: `unadjudicated_citing_pair`, `ledger_pair_not_cited`, `ledger_duplicate_pair`, `citation_range_invalid`, `input_invalid`.
- Multiplicity is per distinct object: one `unadjudicated_citing_pair` per distinct (row,file); one `ledger_pair_not_cited` per distinct ledger pair absent from the citing set; **one** `ledger_duplicate_pair` per distinct pair even if repeated; a duplicated pair still counts as adjudicated.
- `input_invalid` (missing/unreadable/malformed document, wrong document shape, rows without id, symlinked/non-regular knowledge file, path escaping root) → exit 2.
- `citation_range_invalid` (descending, or span > 200 ids) → exit 1, verdict failed; the range is **not** expanded; its endpoints stay literal pairs only when they are standalone tokens.
- Token rule: `S` + ≥3 ASCII digits delimited by non-word chars; ids intersected with population rows (a cited id outside the population is not a citing pair and yields no finding).
- Range separators: hyphen, en dash U+2013, em dash U+2014, `..`, `to`, `through`; any whitespace (newlines included) may surround the separator and the separator may abut the digits (grammar correction relayed by BuildGate during this wave, interface unchanged).
- Scan set: every regular file under `<root>/corpus/knowledge/` recursively, `.md` and `.json` alike, whole-file text — front-matter metadata lines and trailing EOF prose count like in-body citations. `population.json`/`ledger.json` at the case root are read as documents, never scanned as corpus.

## Case matrix (29) — expectation and rationale

`cited` = the citing set the gate must derive; `missing` = pairs the ledger lacks (each ⇒ one `unadjudicated_citing_pair`).

| # | case | exit | findings | rationale / what it pins |
|---|---|---|---|---|
| 01 | single-literal-clean | 0 | — | One literal `S001` bullet; ledger adjudicates it. Baseline clean. |
| 02 | single-literal-missing | 1 | unadjudicated×1 | Two entries, ledger adjudicates only one; the other literal pair is unadjudicated. |
| 03 | en-dash-group-range-interior-omission | 1 | unadjudicated×4 | `S001–S006` group; ledger holds only the endpoints → interiors S002–S005 missing (the grouped-omission shape of the frozen S001–S006 group). |
| 04 | hyphen-range-omission | 1 | unadjudicated×1 | `S001-S007` (hyphen, mirrored on the verified-at line); S006 missing. |
| 05 | ascii-dotdot-range-omission | 1 | unadjudicated×1 | `S001..S006`; interior S003 missing. |
| 06 | to-range-omission | 1 | unadjudicated×1 | Whole-word `to` range; S004 missing. |
| 07 | through-range-omission | 1 | unadjudicated×1 | Whole-word `through` range; S002 missing. |
| 08 | comma-list-omission | 1 | unadjudicated×1 | Header comma list `S001, S002, S003`; S002 missing. |
| 09 | metadata-header-reference | 1 | unadjudicated×1 | Row id appears **only** in the front-matter `source:` line; metadata references are citing pairs. |
| 10 | eof-prose-reference | 1 | unadjudicated×1 | Row id appears **only** in the trailing round-recheck EOF prose; EOF prose is a citing pair. |
| 11 | duplicate-ledger-pair | 1 | ledger_duplicate_pair×1 | Same (row,file) listed twice; pair stays adjudicated, so no unadjudicated id. |
| 12 | noncited-ledger-pair | 1 | ledger_pair_not_cited×1 | Ledger pair (S002,file) that the file never cites. |
| 13 | descending-range | 1 | citation_range_invalid×1 | `S006–S001`; invalid range not expanded; both endpoints literal and adjudicated, so the range defect is the only id. |
| 14 | oversize-range | 1 | citation_range_invalid×1 | `S001..S900` (span 899 > 200); population carries S001 and S900, both adjudicated → only the range defect. |
| 15 | invalid-json-population | 2 | input_invalid×1 | Truncated `population.json` (deliberately malformed) → could-not-evaluate. |
| 16 | invalid-population-shape | 2 | input_invalid×1 | `population.json` is valid JSON but `rows` is an object, not a list of rows → wrong document shape. |
| 17 | ledger-row-outside-population | 1 | ledger_pair_not_cited×1 | Ledger row S019 is absent from the population; it is not a citing pair. |
| 18 | working-tree-input-no-revision | 0 | — | Revision-free input path: no `--revision`, files read from the working tree. |
| 19 | mixed-positive-negative-controls | 1 | ledger_duplicate_pair, ledger_pair_not_cited, unadjudicated_citing_pair | alpha cites `S001, S002–S005` + EOF `S006`; beta cites `S003`. Ledger duplicates (S001,alpha), adds a stale (S002,beta), omits (S006,alpha) → one id of each kind at once. |
| 20 | range-with-population-gap | 0 | — | `S001-S007` span with S003/S004 absent from the population: interior ids outside the population raise nothing. |
| 21 | no-citations-empty-citing-set | 0 | — | Entry naming no registry row → empty citing set, no false positive. |
| 22 | json-knowledge-file-citation | 1 | unadjudicated×1 | Row id inside a `.json` knowledge file (`freshness-pins.json`) → JSON knowledge files are scanned. |
| 23 | glued-to-range-separator | 1 | unadjudicated×3 | `S001toS006` glued: range recognised, endpoints are **not** standalone tokens, so only the expansion yields pairs; S002/S004/S005 missing. Discriminates the corrected range grammar from the old whole-word rule. |
| 24 | range-separator-across-linebreak | 1 | unadjudicated×1 | `S001\nto S006` across a line break; endpoints standalone and the span expands; S005 missing. |
| 25 | em-dash-range-omission | 1 | unadjudicated×1 | `S001—S006` (em dash); S004 missing. |
| 26 | ledger-pair-file-absent | 1 | ledger_pair_not_cited×1 | Ledger pair whose corpus file does not exist → absent from the citing set. |
| 27 | range-endpoint-outside-population | 1 | unadjudicated×1 | `S090-S095` span with only S092 in the population: the range stays valid, expands over its numeric span, and the interior row this registry carries becomes one pair. |
| 28 | ledger-row-numeric-spelling | 0 | — | Population lists S001 and S0001, ledger adjudicates the same row as `S0001` → numeric identity, no finding. |
| 29 | ledger-pair-two-numeric-spellings | 1 | ledger_duplicate_pair×1 | Same population, ledger lists (S001,file) and (S0001,file) → one distinct row adjudicated twice: one duplicate id, pair still adjudicated. |

Coverage against the assignment list: single literal clean/missing (01, 02) · en-dash grouped omission (03) · hyphen / `..` / `to` / `through` ranges (04, 05, 06, 07; em dash 25; glued 23; line break 24) · comma list (08) · metadata / EOF references (09, 10) · duplicate ledger (11, 29) · non-cited ledger (12, 17, 26) · descending / oversize range (13, 14) · invalid JSON / population / revision-free input boundary (15, 16, 18) · mixed positive+negative controls (19) · range endpoint outside the population (27) · numeric row-id equivalence (28, 29). 29 ≥ 12 required cases.

## Judgement notes

- No source-text or mock-echo assertion: `expected.json` states only exit code and the frozen finding ids; the corpus files carry realistic entry content (front-matter, body bullets, trailing recheck prose) but no test asserts on their wording.
- Expected values were authored by hand from the contract semantics and the authors' written confirmations, not computed by a re-implementation of the gate; no fixture is derived from the gate's own output.
- Multiplicity is deliberate: 03 expects four identical ids, 23 three — the runner's multiset compare is what makes those distinguishable from a single missing pair.

## Verification actually performed

- Authoring hygiene only: the 87 authored JSON documents parse (the one deliberate exception is case 15's malformed `population.json`), and the file digest above was computed. **No gate execution, no fixture runner execution, no test/lint run** — the wave bounds place the gate run after integration (L1). Fixture-vs-gate agreement is therefore **unverified by me** and must be checked by the L1 with `scripts/citing_set_selftest.py` (or the gate's `--selftest`).
- Peer-side evidence (not mine): the gate author `KakeR27.BuildGate` reported in-channel that cases 27, 28 and 29 match its implementation after running its own gate over them, and that no gate change is needed for them. That is author-side evidence only; the whole 29-case set still needs the L1's post-integration run.
- Unverified-by-me risk points, in order: (a) case 16 depends on the gate treating a non-list `rows` as a wrong document shape (a missing `rows` key might be read as an empty population instead — that variant is deliberately not used); (b) cases 13/14 depend on invalid ranges keeping their endpoints as literal pairs (confirmed in writing, not executed by me); (c) case 23 depends on the corrected range grammar being the one in the integrated gate; (d) cases 28/29 depend on the ledger's row comparison and duplicate detection being numeric.

## Suggested behavioural boundaries still uncovered (for the L1 / gate author)

1. Ledger pair whose `row` is well-formed but whose `file` lies outside `corpus/knowledge/` (path escaping the scanned subtree).
2. Corpus subdirectory nesting under `corpus/knowledge/` (recursive scan) and a knowledge file that is a symlink (should be `input_invalid`, exit 2).
3. `--revision` mode against a git blob set: fixture cases are revision-free by construction, so blob-mode citation discovery (e.g. a range that only exists in the committed blob) is untested by this corpus.
4. A population row that is itself malformed (`id` not matching `S`+digits) — `input_invalid` vs silent drop.
5. An invalid range whose span crosses a row id absent from the population (`citation_range_invalid` plus interior rows) — cases 13/14/27 pin the endpoint and interior rules separately, not this combination.

## Boundaries respected

No live-lane writes, no modifications to `scripts/citing_set.py` or `scripts/citing_set_selftest.py`, no git commits, no second judge/admission/promotion/state operation, no subagent dispatch, no network or property/browser/account/publication operation, no reads of stopped r24 work, no tool installs.
