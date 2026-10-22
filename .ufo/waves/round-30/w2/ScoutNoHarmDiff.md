# Wave 2, no-harm scan of 0356681..451e98f (Kake round 30)

Seat KakeR30.ScoutNoHarmDiff, leaf, axes operability and freshness. Item attacked: the round-wide no-harm premise wave 1 left unexamined, carried by one concrete wave-1 artifact. `.ufo/waves/round-30/w1/ExecGateFamilies.md:8` says "Diff stat vs base: 17 files changed, 297 insertions(+), 23 deletions(-)". The landed `71c6bfa` is **56 files, 803 insertions, 63 deletions**, and that note enumerates no deletion. All 63 are listed and judged below: 25 in `scripts/citing_set.py`, 34 in `scripts/citing_set_selftest.py`, 4 in fixtures 13 to 16. `git diff --numstat 03566813 451e98fc` totals 63 deletions, all inside `71c6bfa`; nothing else in the range deletes a line (`451e98f` is +11327/-0 over 83 files).

Sandbox `/fast/scratch/hyaku/kake-r30/w2/ScoutNoHarmDiff/` (clone at 451e98f, TMPDIR inside), Python 3.14.8, system Git. No installs, no network, read-only git in the lane, this file is my only lane write. Verdicts: CORRECTION (the removal is a repair or a truthful rewrite), NEUTRAL (no observable change), HARM (regression against base), MIXED.

## scripts/citing_set.py, 25 lines
- **35-38** Population docstring, "not S followed by digits" -> CORRECTION. Now names the scanner's own rule `^S[0-9]{3,}$`, matching the code. Caveat: "unreachable" is not literally true of `S01`, whose `id_key` equals `S001`'s and whose pair is citable; that caveat is absent from the text.
- **62** Findings docstring line -> CORRECTION, reflowed to name the two new reasons; the rest of the retained list is identical.
- **229** one-line `os.open` flags -> NEUTRAL, a 4-line expression adding `O_NOCTTY`; no change for regular files (fixture 30 and the 41/41 run below).
- **268, 273, 285-294** (12 lines) `self._walk(base, found)`, `def _walk`, its loop body -> CORRECTION. Recursion becomes an explicit stack: same sorted depth-first order, same three rejections, same final `sorted(found)`. Equivalence observed below.
- **417** `document = json.loads(text)` -> CORRECTION, strict parser for duplicate members, non-finite literals and float overflow. No committed input regresses, below.
- **437-438** `key = id_key(identifier)` then `if key[0] != "n":` -> CORRECTION. Validation now precedes keying and uses `fullmatch`, so `S1`, `S01` and `S001\n` are refused where `$` accepted the last; acceptance is unchanged for every id the scanner can produce.
- **641-644** four `add_argument` one-liners -> CORRECTION, 2-line forms with `action=StoreOnce`; a repeated valued option now exits 64 with the JSON usage object. No committed caller repeats one.

## scripts/citing_set_selftest.py, 34 lines
- **10, 16, 26** format line, comparison line, summary line -> CORRECTION, reflowed for the two oracle forms and the added `results` array. Wart: the docstring still calls `.ufo/waves/round-27/contract.json` "the contract under test" while the accepted oracle grammar is now a declared superset of its `fixtureInterface`.
- **144-164** (11 lines) `finding_ids` and its body -> MIXED. Legacy equivalence holds (cases 01 to 29 below); carries H2.
- **167-182** (9 lines) `expectation_problem`, including `return None` -> HARM H1: the clean malformed-oracle failure path becomes a comparison that raises `TypeError`.
- **188** `def run_case(...)` -> NEUTRAL, gains `cases_root`.
- **208, 209, 210, 212** problem capture, test, reason, `row["expected"]` -> HARM H1 for oracle validation; `row["expected"]` otherwise gains `mode`.
- **219, 230** `str(case_dir)` as `--root`, `cwd=str(case_dir)` -> MIXED. Each case is now copied to `<tmpdir>/citing-set-selftest/cases/<case>`, so the gate cannot mutate a committed fixture and Git-hostile setup is possible; HARM H3 below.
- **263** `observed = sorted(finding_ids(report))` -> NEUTRAL in ids mode (verified); carries H2.
- **272-274** id-only comparison, message, argument -> NEUTRAL; the message now says "finding mismatch", and `actual.mode` carries what the old wording implied.
- **338** `row = run_case(...)` -> NEUTRAL, passes `cases_root`.

## fixtures 13..16/expected.json, base line 4 in each
`"citation_range_invalid"` (13, 14) and `"input_invalid"` (15, 16) become `{id, reason}` -> CORRECTION. The gate does emit those reasons (`descending_range` `citing_set.py:678`, `span_too_large` `:690`, `document_not_json` `:577`, `document_shape_invalid` `:579`), so the object form pins an observable the string form discarded. Cases 01 to 12 and 17 to 29 stay in the string form, so both forms remain exercised.

## Harm
**H1, demonstrated.** `scripts/citing_set_selftest.py:269` sorts `(id, reason)` tuples and raises `TypeError` when one id appears twice and only one entry carries a reason, since `None` and `str` are not orderable. Probe A at `/fast/scratch/hyaku/kake-r30/w2/ScoutNoHarmDiff/probeA` with oracle `{"exit":1,"findings":[{"id":"unadjudicated_citing_pair"},{"id":"unadjudicated_citing_pair","reason":"x"}]}`: HEAD runner exit 1, **empty stdout**, stderr `TypeError: '<' not supported between instances of 'str' and 'NoneType'` at selftest:269. Base runner on the same fixture directory: exit 1, stdout `{"verdict":"failed","cases":1,"failed":1}`, row reason `expected.json "findings" must contain only strings`, 0 bytes stderr. The new docstring calls the comparison a sorted multiset, so a repeated id is a documented shape and a mixed-presence duplicate is a malformed oracle, which the runner's docstring says must fail the run rather than crash it. Cost: a broken oracle destroys the summary every receipt consumes. Scope is fixture authors, not gate input.
**H2, latent.** `scripts/citing_set_selftest.py:233` `return sorted(pairs)` in `finding_pairs` raises the same `TypeError` (observed by direct call). A real gate report cannot reach it: reason presence is uniform per id, since only `InputInvalid.as_finding()` (`citing_set.py:203`) and the two `citation_range_invalid` sites set a reason while `unadjudicated_citing_pair`, `ledger_pair_not_cited` and `ledger_duplicate_pair` never do. Reachable only via `--gate`.
**H3, demonstrated.** `scripts/citing_set_selftest.py:366-367` `shutil.rmtree` and `shutil.copytree` are unguarded while `main` guards only `cases_root.mkdir` (`:547`). Probe B at `/fast/scratch/hyaku/kake-r30/w2/ScoutNoHarmDiff/tmpB` with the cases directory present and mode 500: exit 1, **empty stdout**, `PermissionError` from `shutil._copytree`. Base ran cases in place, so the path is new. Related, not a crash: each run deletes and recreates `<tmpdir>/citing-set-selftest/cases/<fixture name>` inside an operator-supplied directory.
**Note, added code.** `_first_nonfinite` (`citing_set.py:539-557`) is unreachable for parsed documents: `parse_constant` refuses `NaN` and `Infinity` and `parse_float=_finite` refuses `1e999` first (observed; both yield `document_nonfinite_number` before the walk).

## Why the other 56 removals are not harm
- Runner over all 41 cases at HEAD in the sandbox: exit 0, `verdict clean, cases 41, failed 0`, 0 bytes stderr (`/fast/scratch/hyaku/kake-r30/w2/ScoutNoHarmDiff/base41.json`). Cases 01 to 29 use legacy string oracles and pass, so the `finding_ids` to `finding_pairs` substitution preserves the legacy form.
- Gate `--selftest` delegation: exit 0, 41 cases, failed 0, so the four replaced argparse lines did not break the gate's own path.
- Base gate against HEAD gate, same tree, round-27 frozen population and ledger, `--revision 03566813`: verdict failed, 59 citing pairs, 41 ledger pairs, 18 findings, **identical** `(id, reason)` multiset. At `--revision 451e98fc`: 62 pairs, 21 findings, identical. The 59 to 62 growth is `corpus/knowledge/render-static-sites.md`, added by this round.
- Population tightening: 184 of 187 committed population rows match `S[0-9]{3,}`; the three that do not are the new fixtures built to be refused (`35` `X001`; `40` `S01`, `S02`).
- Strict parser: of 220 checked-in JSON files, duplicate member names appear only in `scripts/fixtures/base-path/X01-duplicate-json-key/manifest.json` (another gate's fixture) and case 38; non-finite numbers only in `base-path/X02/manifest.json` and cases 39 and 41. `citing_set` never reads the base-path manifests.
- `StoreOnce`: `--root . --root .` exits 64 with the JSON usage object and abbreviated `--rev a --revision b` also exits 64. No committed caller repeats a valued option (`citing_set_selftest.py:214-225`, `round-27/git_name_selftest.py`, `round-27/c2_count.py`, `round-28/c1_interface_count.py`, `round-28/verification/c1_root_env_matrix.py`, `SKILL.md:609`).

## Docs: no pre-existing line removed or modified
`git diff --numstat` deletions are zero on every documentation path: SCORECARD.md +95, SKILL.md +83, PROVINCE.md +14, corpus/QUALITY.md +66, corpus/README.md +15, corpus/SOURCES.md +10, corpus/knowledge/publish-channels.md +24. Root `README.md` and `SHONEN.md` are unchanged. New: corpus/knowledge/render-static-sites.md +113, corpus/lessons/round-30.md +107. The documentation side is append-only, so it removes nothing and rewrites nothing.

## Commits in the range not made by round 30
`636dddd0a37b2e79ce3bc4e46f743ed1e363612c` "considerthese: 2026-10-22 daily reflection", author Joao Pedro Veiga <jpveigao10@gmail.com>, 2026-10-22T09:04:52-03:00, one file, +32/-0 (`considerthese/2026-10-22.md`), between the declaration `4580c78` and the notes `04637bd`. It deletes nothing and touches no lane file, so it harms no lane content, but `0356681..451e98f` is not a pure round-30 diff: 32 added lines are the operator's reflection, whose line 19 narrates round-30 provenance from inside the measured range. Every other commit in the range is by `kake-shokunin <kake@shokunin.local>`.

## Not verified
Whether appended prose contradicts retained prose (another seat's item; I only established that nothing was deleted). A corpus deeper than 1000 directories, a tty as an input document, and `O_NOCTTY` behaviour outside Linux; I relied on the counter receipts for F05 and F06 instead of re-running them. Whether H1 or H3 is reachable in any mode the round's counters use: both counters pass their own tmpdir and committed oracles, and both receipts show the runner baseline at 41 cases, 0 failed.
