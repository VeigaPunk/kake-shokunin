# BuildBasePathSelftest — committed regression fixtures for the C2 base-path gate

Seat `KakeR29.BuildBasePathSelftest` (leaf executor), axis: operability, milestone r29-build.
Purpose: the round-28 routed defect 1 lesson — a gate's reason codes must be asserted by
committed fixtures, not only by a round counter. This seat commits a fixture tree plus a
runner that fails on any exit, verdict or reason mismatch. No lane file other than this
report was written; no git/jj command was run in the lane.

## 1. Sandbox paths

Root `/fast/scratch/hyaku/kake-r29/w1/BuildBasePathSelftest/`:

- `deliverable/scripts/base_path_selftest.py` — the runner (sha256 `c60377d3d34d8b12a19259a21d04b6d7c81ca641d871b7eafb6277f472bbc006`)
- `deliverable/scripts/base_path_fixture_gen.py` — regenerates the tree from the pinned matrix (sha256 `6fb44d4f6f8f504f50528585b21149547eed4b1e13cd657734fefb70f41c512c`)
- `deliverable/scripts/fixtures/base-path/<case-id>/` — **30** fixture directories, 89 files:
  the case files of `.ufo/waves/round-29/c2-matrix.json` verbatim plus `expected.json`
  (exit, verdict, expected finding tuples with their reason codes, argv override).
  Tree sha256 `2f20fd9d9b90e40f6352f9637c93be7cdfdeff56cd781937fed67585522b0c66`.
- `stubs/constant_clean.py`, `stubs/refuse_everything.py` — the two required stubs.
- `stubs/renamed_reason.py` — extra stub: correct exits/verdicts, renamed reason codes.
- `tools/reference_base_path_audit.py` — local reference tool used only to prove the harness
  accepts a correct tool (not a deliverable; the C2 tool is `scripts/base_path_audit.py`).
- `tools/gen_fixtures.py`, `tools/verify_fixtures.py` — build and check helpers.
- `c2-matrix.json` — copy of the pinned matrix, sha256 `75c08f64…c2e84a` (matches the digest
  pinned in `.ufo/waves/round-29/c2_matrix_count.py`).

## 2. Commands run (sandbox) with exit codes and observed output

```
$ python3 -B tools/gen_fixtures.py c2-matrix.json deliverable/scripts/fixtures/base-path   # exit 0
wrote 30 fixtures under deliverable/scripts/fixtures/base-path
$ python3 -B tools/verify_fixtures.py c2-matrix.json deliverable/scripts/fixtures/base-path   # exit 0
verdict clean, casesChecked 30, casesInMatrix 30, problems [], treeSha256 2f20fd9d…
$ python3 -B deliverable/scripts/base_path_selftest.py --tool tools/reference_base_path_audit.py   # exit 0
30/30 fixtures passed
$ python3 -B deliverable/scripts/base_path_selftest.py --tool stubs/constant_clean.py   # exit 1
7/30 fixtures passed   (23 failed; first: D1-root-relative-stylesheet, exit mismatch 1 != 0)
$ python3 -B deliverable/scripts/base_path_selftest.py --tool stubs/refuse_everything.py   # exit 1
7/30 fixtures passed   (23 failed; first: D1-root-relative-stylesheet, exit mismatch 1 != 2)
$ python3 -B deliverable/scripts/base_path_selftest.py --tool stubs/renamed_reason.py   # exit 1
8/30 fixtures passed   (22 failed; first reason mismatch: missing ('outside_base_path','link','href','/style.css'))
$ python3 -B deliverable/scripts/base_path_selftest.py --tool /fast/scratch/hyaku/kake-r29/w1/BuildBasePathAudit/base_path_audit.py   # exit 0
30/30 fixtures passed   (the sibling executor's real tool, sha256 e3264615…65aa, commit 90d5c82)
$ python3 -B .ufo/waves/round-29/c2_matrix_count.py --root <sibling clone> --revision 90d5c82305a92d3f991ac52e85ac7432b306f4b8   # exit 0
C2 30/30 at 90d5c82305a92d3f991ac52e85ac7432b306f4b8
$ python3 -B tmp/defaulttest/scripts/base_path_selftest.py   # exit 0, default tool path = base_path_audit.py next to the runner
30/30 fixtures passed
$ python3 -B deliverable/scripts/base_path_selftest.py --tool tools/nonexistent.py   # exit 2
could-not-evaluate: tool not found
```

Fixture tree digest before and after all four stub runs was identical
(`2f20fd9d…b0c66` both times) and no `__pycache__`/`.pyc` file appeared: the runner never
writes inside a fixture (`PYTHONDONTWRITEBYTECODE=1`, `-B`).

## 3. What the runner asserts

Per fixture: exit code equal; for exits 0/1/2 one JSON object on stdout with `verdict` equal
and the finding multiset equal. Each expected finding selects the observed keys it names
(always `reason`, plus `element`/`attribute`/`value` when pinned), so a renamed or dropped
reason fails even when exit and verdict are right. Exit 64 (usage) needs no JSON. The tool
runs with the fixture directory as cwd, exactly like `.ufo/waves/round-29/c2_matrix_count.py`,
so both observe the same behaviour. Stdout is one JSON summary object (lane convention, as in
`scripts/citing_set_selftest.py`); stderr carries per-case lines and the `N/M` line. Exit
status: 0 all matched, 1 some mismatch, 2 harness unusable.

## 4. Notes and risks for the L1

- The fixture expectations are the matrix expectations, unmodified: no case, exit, verdict or
  reason was invented or relaxed. `tools/verify_fixtures.py` re-checks the tree against the
  matrix byte for byte.
- Cross-check: the sibling executor's real tool (`BuildBasePathAudit` clone, commit 90d5c82,
  sha256 `e3264615…65aa`) passes this fixture tree 30/30, so the committed expectations agree
  with the shipped tool as well as with the frozen matrix. The official counter reports
  `C2 30/30` at the same commit. The runner compares on `reason`/`element`/`attribute`/`value`
  only and ignores the tool's finding `id`, as the tool owner specified.
- The shipped tool requires the exact manifest key set `{version, basePath, pages}` and
  `{file, url}` per page; the fixtures use exactly those keys, so no fixture is rejected for
  key shape. The usage fixture runs the tool with no arguments, which is the tool's exit 64
  path (it prints usage JSON on stdout, which the runner does not require).
- `scripts/base_path_fixture_gen.py` is included so the tree can be regenerated from the
  pinned matrix; drop it if the L1 prefers a fixtures-only change.
- The runner depends on the frozen interface only (`--manifest <file>`, JSON on stdout); if
  the shipped tool changes its CLI, the runner's `--manifest` call must be adjusted.
- Not verified here: the selftest was not run inside the lane repo (the lane has no
  `scripts/base_path_audit.py` at commit `9e541a1`, and I may not write lane files besides
  this report), and no build, lint or test tooling was installed or run. No packages were
  installed this seat, so there is nothing to record for the tooling directive.
