# ScoutReasonCoverageMap — C1 reason-code coverage (base 0356681)

Scope: every reason `scripts/citing_set.py` can emit at base
`035668132250b75b38d399e86e540b0a0371efbc`, what reaches it, what the C1 plan
leaves unasserted. Leaf seat: no subagents, lane read-only, one report written.

## Evidence
- Sandbox clone `…/w1/ScoutReasonCoverageMap/clone` at base (`git checkout -q
  0356681…`, exit 0). Gate sha256 `d7e79ba102ff…479d48`, runner
  `3c167895c7f3…62a1c` — match SCORECARD.md:714.
- Ran that gate once per committed fixture (29 subprocesses, TMPDIR in sandbox):
  the reached-by reasons below are observed, not inferred.
- Ran 18 probe trees (`…/probe`, `probe2`…`probe7`) for codes nothing names, and
  reproduced round-28 cases A1–A7, U1, U3 from source (that counter records
  `findingReasons` but asserts only the `input_invalid` id).
- Read `c1_reason_count.py` (170–470) and `c1-before-0356681.json` (R01–R08
  behaviour=true, fixture=false, compared=false; F01/F02 behaviour=false). Not
  run: both counters (round-30 needs a landed commit). No network.

## Table A — `input_invalid` reason codes at base (21) and after the plan
| # | code | lines | reached at base by | after C1 plan |
|---|---|---|---|---|
| 1 | empty_path | 180, 188 | none; probe `--population ./` → 2 | unasserted |
| 2 | absolute_path_not_allowed | 183 | none; probe `--population /etc/hostname` → 2 | unasserted |
| 3 | path_escapes_root | 186 (argument), 226 (document) | none; probes `../x.json` and `population.json -> ../outside.json` → 2 | unasserted (document form fixture-able) |
| 4 | document_unreadable | 234, 244 | none; probe missing `population.json`, chmod-000 doc → 2 | unasserted |
| 5 | document_not_regular_file | 238 | r30 R01 (FIFO population), F06 (pty); r28 U1/U2 (id only); no fixture | R01, F06 assert; R01 fixture still needed |
| 6 | corpus_directory_missing | 255, 382 | r28 A1/A2 (id only), r30 R03 | R03 asserts |
| 7 | corpus_directory_unreadable | 258, 280 | none; probe chmod-000 subdir of `corpus/knowledge` → 2 | unasserted; counter-only |
| 8 | symlink_rejected | 264, 288, 375 | none; probe corpus file symlink → 2 | unasserted |
| 9 | not_a_directory | 266, 379 | r28 A4 tree and Git (id only), r30 R05 (Git) | R05 asserts |
| 10 | corpus_empty | 270 | r28 A3 (id only), r30 R04, probe | R04 asserts |
| 11 | not_a_regular_file | 294, 372, 377 | none; probe FIFO in `corpus/knowledge` → 2 | unasserted; counter-only |
| 12 | git_unavailable | 323, 339, 353 | none; probe `PATH=/nonexistent --revision HEAD` → 2 | unasserted; counter-only |
| 13 | root_not_repository_top_level | 325 | r28 A7 (id only), r30 R08 | R08 behaviour only; **fixture blocked, gap 1** |
| 14 | revision_not_found | 330, 341 | r28 A6 blank revision (id only), r30 R07 | R07; **fixture blocked, gap 1** |
| 15 | git_command_failed | 355 | none; probe `--revision HEAD` with population/ledger absent from the commit → 2 | unasserted; counter-only |
| 16 | document_not_utf8 | 415 | none; probe invalid bytes in population → 2 | unasserted |
| 17 | document_not_json | 419 | fixture `15-invalid-json-population` (truncated), r28 U3/U4, r30 R02 | R02 asserts; fixture 15 needs object form |
| 18 | document_shape_invalid | 421, 428, 433, 436, 449, 453, 457, 459 | fixture `16-invalid-population-shape` (`rows` object → the 428 site) | **reason unnamed, gap 2** |
| 19 | population_id_unreachable | 439 | r28 A5 `X001`, r30 R06 `X001`, F03 `S01`/`S1` | R06, F03; base is clean for `S01`/`S02` (probe) |
| 20 | corpus_file_not_utf8 | 496 | none; probe invalid bytes in a corpus entry → 2 | unasserted |
| 21 | root_not_a_directory | 711 | none; probe absent `--root` → 2 | unasserted |

New codes, absent at base (grep for both names, `parse_constant`,
`object_pairs_hook`: exit 1) and silently grandfathered:

| # | code | base behaviour (probe) | after C1 plan |
|---|---|---|---|
| 22 | document_duplicate_key | repeated `rows` → last wins, exit 1 `unadjudicated_citing_pair` | F01 (population member, ledger pair member) |
| 23 | document_nonfinite_number | `NaN` accepted, exit 1 | F02 (`NaN`, `Infinity`, `-Infinity`) |

## Table B — reason fields outside `input_invalid`
- `citation_range_invalid` (id 114): `descending_range` 517 ← fixture 13
  (`S006–S001`, observed); `span_too_large` 529 ← fixture 14 (`S001..S900`). Both
  assert only the id; sub-reasons unasserted. Not findings: `"error": "usage: "…`
  632, exit 64 (636; F04 covers four repeats); `"error": "selftest_runner_missing"`
  660 (exit 2).

## Gaps after the C1 plan
1. **R07/R08 `fixture`+`compared` are unsatisfiable as declared.** The runner's
   gate argv is fixed (`scripts/citing_set_selftest.py:214-226`) with no
   `--revision`, and `GitSource` exists only when `--revision` is given (gate
   714–717), so no fixture can emit `revision_not_found` or
   `root_not_repository_top_level`; one naming either would mismatch, make the
   runner non-zero and fail `compared` (`c1_reason_count.py:448-450` needs
   baseline 0). The export never `git init`s (counter 470–477), so R08 would hit
   `revision_not_found` first (gate 304–305). Needs a case-local revision input
   plus runner-side repo synthesis; neither is in the plan.
2. **`document_shape_invalid` stays unnamed.** Case 16 reaches the 428 site only;
   seven raise sites (421, 433, 436, 449, 453, 457, 459) are reached by nothing.
   Converting 16 to object form freezes one site — state whether the rest are out
   of scope.
3. **R01's fixture artifact.** A FIFO cannot ship: `tarfile … filter="data"`
   raised `SpecialFileError` on a FIFO and `AbsoluteLinkError` on an absolute
   symlink, aborting the export (`tarprobe`, `tarprobe2`). A relative directory
   symlink works: `population.json -> .` → `document_not_regular_file`, exit 2
   (`probe6`); a `path_escapes_root` fixture needs a relative link inside the
   exported tree (`-> ../outside.json`, `probe7`).
4. **Unasserted after the plan (13 of 21 base codes).** Fixture-reachable but
   unbuilt (5): `document_unreadable` (omit population), `symlink_rejected`
   (relative symlink under `corpus/knowledge`), `document_not_utf8`,
   `corpus_file_not_utf8`, `document_shape_invalid` (naming only). Counter-only
   (8): `empty_path`, `absolute_path_not_allowed`, `path_escapes_root` (argument
   form), `corpus_directory_unreadable` (modes do not survive export),
   `not_a_regular_file` (special files do not survive), `git_unavailable` (needs
   stripped PATH), `git_command_failed`, `root_not_a_directory` — all probed at
   exit 2, none planned.
5. **Base runner rejects object-form expectations** (`expectation_problem`, runner
   167–181: "must contain only strings"), so converting 15/16 and every new named
   fixture depends on the runner change landing in the same commit. Duplicate-key
   detection needs `object_pairs_hook` at parse time: base `json.loads` drops the
   evidence, and F01's population case repeats `rows`.

## Not verified
- Neither counter executed here; Git-mode `not_a_regular_file` sites (372/377,
  non-blob entry, submodule) need a hand-built repository; runner post-change
  behaviour is the executor's build.
