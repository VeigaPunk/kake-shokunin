# ExecRunnerReasonFixtures — wave-1 report (Kake round 30, C1 R01-R08)

Seat: leaf executor for C1 runner + fixtures. Sandbox: `/fast/scratch/hyaku/kake-r30/w1/ExecRunnerReasonFixtures/`. Clone: `clone/` (HEAD `9bf6896`).

## What I built

1. **Runner** (`clone/scripts/citing_set_selftest.py`, rewritten in place):
   - `expected.json` findings accept two forms, never mixed within a case: legacy strings (compare sorted multiset of ids) and objects `{"id": ..., "reason": ...}` (compare sorted multiset of `(id, reason)` pairs; a missing reason compares as `null`). Exit code compared exactly as before. Mixed lists are a malformed oracle and fail that case.
   - Per-case setup mechanism via optional `case.json` (`root`, `argv`, `setup`): ops `mkdir`, `fifo`, `git_init`, `git_commit`. Every case runs from a scratch copy under `--tmpdir/citing-set-selftest/cases/<case>/`; committed fixtures are never mutated. Git steps use an isolated env (drops inherited `GIT_*`, sets author/committer, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`).
   - Summary JSON rows carry both `ok` and `passed` booleans plus `case`, `expected`, `actual`, `argv` (strict checker S2 reads `passed`).
   - Scratch case root resolved to an absolute path (fix commit `9bf6896`; without it the counter's `--scratch`-relative `tree` double-prefixed paths).

2. **Fixtures 30-37**, one per round-28 reason code, all `{"exit": 2, "findings": [{"id": "input_invalid", "reason": "<code>"}]}`:
   - `30-document-not-regular-file`: committed regular `population.json`; setup makes it a FIFO in the scratch copy (no FIFO committed; copytree-safe).
   - `31-document-not-json`: committed malformed `ledger.json`.
   - `32-corpus-directory-missing`: no corpus directory at all.
   - `33-corpus-empty`: setup `mkdir corpus/knowledge` in the scratch copy (Git cannot store an empty dir).
   - `34-not-a-directory`: `corpus/knowledge` committed as a regular file.
   - `35-population-id-unreachable`: population row id `X001` (non-S id; does not collide with gate-seat case 40).
   - `36-revision-not-found`: setup `git_init`+`git_commit`; argv `--revision no-such-revision`.
   - `37-root-not-repository-top-level`: payload under `sub/`, repo created at scratch root, root `sub`, argv `--revision HEAD`.

3. **Converted fixtures 13-16 to object form** (they already carried reasons): `13` -> `("citation_range_invalid","descending_range")`, `14` -> `("citation_range_invalid","span_too_large")`, `15` -> `("input_invalid","document_not_json")`, `16` -> `("input_invalid","document_shape_invalid")`, verified against the gate's emitted findings.

## Commands run (all in my sandbox)

- `python3 -B clone/scripts/citing_set_selftest.py --root clone --tmpdir <sandbox>/tmp` -> exit 0, verdict clean, 37 cases, 0 failed.
- Mutation loop: for each of the 8 codes, `shutil.copytree` of the clone, replace `"<code>"` -> `"<code>_mutated"` in `scripts/citing_set.py`, run the runner with `--tmpdir <sandbox>/mutwork/<code>`. All 8: exit 1, exactly the fixture naming that code failing (S2 shape holds). E.g. `document_not_json` -> failures `15-invalid-json-population`,`31-document-not-json`.
- `c1_reason_count.py --root <sandbox>/clone --revision HEAD --scratch <sandbox>/count4` -> exit 1, **8/14: R01-R08 all pass** (behaviour, fixture, compared); F01-F06 fail (gate seat's unlanded changes). Controls K1-K3 hold, constant gates rejected. Baseline runner: exit 0, 37 cases, 0 failed.
- Note: the counter requires an absolute `--scratch`; a relative scratch path makes its own export tree relative and the runner invocation fails (observed exit 2 / empty summary).
- `c1_strict_checks.py --root <sandbox>/clone --revision HEAD --scratch <sandbox>/strict` -> exit 1 overall (gate-seat families S3-S6 and F01/F02 fixtures still unlanded), but **S1 and S2 pass for all eight round-28 codes**: every code renamed exits 1, exactly the fixtures naming that code fail (e.g. document_not_json fails 15 and 31).

- Mutation seat (MutC1CounterStubs) measured my runner + gate seat's gate + both fixture sets on base 4580c78: counter **14/14**, 41 cases, runner baseline exit 0 / 0 failed. Mutants all killed; a runner skipping setup cases drops to 10/14 losing exactly R01/R04/R07/R08 (the four fixtures with setup ops), confirming the setup mechanism is load-bearing.

## Changed files (my two commits, vs parent 4580c78)
`scripts/citing_set_selftest.py`; `scripts/fixtures/citing-set/13..16/expected.json`; new fixture dirs `30..37` (39 files, +506/-38). Commit hashes: `4ceafb9` (runner + fixtures), `9bf6896` (absolute scratch root). Full diff vs base `0356681` includes the pre-existing round-30 declaration commit 4580c78 files (SCORECARD.md, `.ufo/waves/round-30/...`); my own changes are only under `scripts/`.

## Handoff notes

- Gate seat `KakeR30.ExecGateFamilies` owns fixtures 38-41; no number collisions. My runner accepts their object-form plain files; they confirmed no legacy fixture conversions on their side.
- Baseline runner exit 0 requires the gate seat's fixtures to be present or absent consistently; after integration, re-run the counter baseline first.
