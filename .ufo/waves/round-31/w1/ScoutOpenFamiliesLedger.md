# ScoutOpenFamiliesLedger — round-30 routed defect 2 (carried open items) at base `f1ffb81738c92c0537b99b30970143ab9419f990`

Leaf scout, no subagents, no installs. Lane read only; all runs in `/fast/scratch/hyaku/kake-r31/w1/ScoutOpenFamiliesLedger/`.
Base identity: gate `dbfade45e59351fb5edc010dfc45a4e15e1213fdb6fad9ec1668ffd3b77b7f02` (identical to `71c6bfa`), runner `9f2d1ecb280b7dc314886c79264fb5461c400d8f7c762ea62bb4018fc49e14d3`, strict checker `96e7bbcd…500f`, counter `be2a1287…c53e`, 45 committed fixture cases.

## Commands (exit codes)

| Command | Exit | Observed |
|---|---|---|
| `git clone -q <lane> clone`; `python3 -B clone/scripts/citing_set_selftest.py --root clone --tmpdir tmp/control` | 0 | 45 cases, `failed: 0`, runner sha `9f2d1ecb…`, gate sha `dbfade45…` (`out_control.txt`) |
| `TMPDIR=… python3 -B mutate_and_run.py` | 0 | base runner + re-derived m2/m4/m5 each `failed: 0` over 45 fixtures; separators: pristine 1, mutant 0 (`mutants_result.json`) |
| `TMPDIR=… python3 -B probe_identity.py gate_base.py work_base` | 0 | I1 `["19"]` exit 1; I2/I3 two findings each; R1 `document_unreadable`; R2 holds |
| `python3 -B gate_base.py --root deep … --json` (1000-deep corpus) | 0 | `verdict: clean`, empty findings, empty stderr |
| in-process `os.open` spy over population/ledger/corpus docs | 0 | flags `0x80900` (526592) on all three, `O_NOCTTY` bit true, `verdict: clean` |

## Carried open items — definition and status at base

| Item | Defining pointer | Status at base | Evidence |
|---|---|---|---|
| IDENTITY-PATHS | `.ufo/waves/round-27/unresolved-acceptance.json` `failures[ID]` ("Outside-population ids lose S prefix; literal backslash filenames and duplicate slash ledger refs cannot match"); sources `w2/AttackCase15.md`, `w2/AttackCase17.md`, `w2/CliGitNames.md`, `w2/AttackCase11.md` | **OPEN**, nothing closed it | gate blob at base = `71c6bfa` blob; probes reproduced at base: `row: "19"` (S lost), `back/slash.md` + `back\slash.md` for one file, `corpus/knowledge//a.md` + `corpus/knowledge/a.md` for one file; causes at base `scripts/citing_set.py:246-253` (`normalize_ledger_file`), `:713` (`key[1]` fallback) |
| RETENTION-FRAGMENT | same JSON `failures[RETENTION-FRAGMENT]` ("Unrecognized HTML fragment can retain attributes while metadata claims visible text"); source `.ufo/waves/round-27/w2/ReviewRetentionBoundary.md` F1; lesson `corpus/lessons/round-27.md:112` | **OPEN**, nothing closed it | `.ufo/waves/round-27/fetch_group.py` git blob at base `1c4b8672…` equals blob at freeze `ac46a74`; last commits touching `.ufo/waves/round-27/` are round-27 (`62aeddf`, `cd2e95b`, `ac46a74`) |
| RETENTION-TRUST-BOUNDARY | same JSON `failures[RETENTION-TRUST-BOUNDARY]` ("Symlinked ancestors, self-asserted filtered marker, caller-root executable helpers and unrestricted source/redirect destinations"); source `.ufo/waves/round-27/w1/InputSafety.md` §1–§2 | **OPEN**, nothing closed it | same untouched `fetch_group.py` blob; round-28/29/30 do not name the label (label first appears in round-30 `SCORECARD.md`/spot-check) |
| C1-UNIT-OVERRIDE | same JSON `failures[C1-UNIT-OVERRIDE]` ("Three artifact HOLD rows erase all 7 known unknown units"); sources `w2/AttackC1Target.md` §F1 (`count_c1.py:94-125` at `ac46a74`), `w2/AttackOracleFreeze.md`; carried unchanged at `corpus/lessons/round-28.md:125-126` | **OPEN**, nothing closed it | `.ufo/waves/round-27/count_c1.py` blob at base `e1ebd576…` equals blob at `ac46a74`; `decided.discard(key)` at :95 and `unknown.pop(key, None)` at :124 still present |
| Socket `document_unreadable` label | `corpus/lessons/round-28.md:111-115`; `.ufo/waves/round-28/w1a3/ReviewNonBlockingRead.md:18,25,67` | **OPEN**, nothing closed it | base gate opens before `S_ISREG` (`scripts/citing_set.py:289-300`); probe R1 on base gate: exit 2, reason `document_unreadable` |
| 12 of 25 reason codes without a fixture | `SKILL.md:766` ("Citing-set reason-code registry — round 30"); carried `SCORECARD.md:792-793` | **OPEN**, still 12/25 | AST + fixture scan below; fixtures 42–45 assert exit 64 with `findings: []` and name no reason |
| Deep corpus (no committed fixture) | `corpus/lessons/round-28-verifier-spotcheck.md:216-220`; `.ufo/waves/round-28/w1a3/ReviewCorpusMissingEmpty.md:22`; carried `SCORECARD.md:793-795` | **CODE REPAIRED, STILL UNGUARDED**: nothing at base closed the fixture gap | iterative walk at base `scripts/citing_set.py:329-349`; my 1000-deep run exits 0 clean with JSON, no traceback; no `case.json` builds nesting (only ops used: `fifo`, `git_init`, `git_commit`) |
| `O_NOCTTY` (no committed fixture) | `corpus/lessons/round-28.md:114-115`; `ReviewNonBlockingRead.md:31` | **CODE REPAIRED, STILL UNGUARDED**: fixture gap not closed | flags at base `scripts/citing_set.py:283-291`; observed `0x80900` with `O_NOCTTY` on all three document opens; only non-regular fixture is case 30 (FIFO), no tty case |
| Four strict-checker holes | `.ufo/waves/round-30/w2/CriticStrictChecker.md` holes 1–4 | **OPEN**, nothing closed it | checker blob at base = round-30 blob `96e7bbcd…`; hole 1 `:283` records `declaredCounterSha256` and never compares it (no `be2a1287` literal); hole 2 `:142` `expected_failing <= failing`, no baseline run; hole 3 `:166-176`, single-use control only in space form; hole 4 `:191`, one overflow site (population top level) |
| Runner mutants m2, m4, m5 | `.ufo/waves/round-30/w2/MutRunnerCompare.md:55-67` ("SURVIVED"), contract at `.ufo/waves/round-30/w2/MutRunnerCompare.md:11-18` | **OPEN at the base runner** (not only at the older `0fc87d5b` blob the report measured) | semantic re-derivation on base runner `9f2d1ecb`: m2 (missing-reason wildcard), m4 (exit ignored for object oracles), m5 (mixed oracle accepted) each pass 45/45, `failed: 0`; separators prove liveness (pristine exit 1, mutant exit 0) for each |

## The 25 gate reason codes at base (23 literals + 2 module constants)

Covered by a committed fixture (13), with case names:

| Code | base line(s) | Fixture case(s) |
|---|---|---|
| `document_not_regular_file` | 299 | 30 |
| `document_not_json` | 577 | 15, 31 |
| `corpus_directory_missing` | 316, 460 | 32 |
| `corpus_empty` | 356 | 33 |
| `not_a_directory` | 327, 457 | 34 |
| `population_id_unreachable` | 599 | 35, 40 |
| `revision_not_found` | 408, 419 | 36 |
| `root_not_repository_top_level` | 403 | 37 |
| `document_duplicate_key` | const 162 | 38 |
| `document_nonfinite_number` | const 163 | 39, 41 |
| `descending_range` | 678 | 13 |
| `span_too_large` | 690 | 14 |
| `document_shape_invalid` | 579, 589, 594, 597, 610, 614, 618, 620 | 16 |

No fixture names these 12 (unchanged count):

`absolute_path_not_allowed` (237), `corpus_directory_unreadable` (318, 366), `corpus_file_not_utf8` (657), `document_not_utf8` (564), `document_unreadable` (294, 304), `empty_path` (234, 242), `git_command_failed` (433), `git_unavailable` (401, 417, 431), `not_a_regular_file` (352, 450, 455), `path_escapes_root` (240, 280), `root_not_a_directory` (895), `symlink_rejected` (325, 344, 453).

Fixture oracle shapes: 20 string-form cases, 16 object-form cases, 9 empty; none mixed, none object-form missing `reason` — the exact separators m5/m2/m4 would need.

## Not verified / notes for the L1

- I ran semantic equivalents of m2/m4/m5, not `MutRunnerCompare`'s exact patch files; the property measured (survival over the 45 committed fixtures) is the same.
- I did not run `.ufo/waves/round-30/c1_reason_count.py` or `c1_strict_checks.py` at base; the strict holes are read from the base blob.
- The labels RETENTION-FRAGMENT / RETENTION-TRUST-BOUNDARY are minted in round-30 text; I mapped them to their round-27 evidence pointers (`ReviewRetentionBoundary.md`, `InputSafety.md`), which is inference on naming, not on status.
- Lane tip moved mid-scout: at my first read it was `a16602a` with an uncommitted `M scripts/citing_set_selftest.py`; it is now `b801ac8` (`c88b97e` landed that runner containment, `b801ac8` the C2 supplement). All measurements above used the committed base runner blob `9f2d1ecb`, so they are base-relative and unaffected; I did not measure the new `b801ac8` runner.
- Sandbox artifacts: `out_control.txt`, `mutants_result.json`, `mutate_and_run.py`, `probe_identity.py`, `gate_base.py`, `runner_base.py`, `strict_base.py`, `deep/`, `flagprobe/`, `ttyprobe/`, `trees/`.
