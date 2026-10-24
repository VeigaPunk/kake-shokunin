# CriticSymlinkCases — C1 N6, symlinked and odd fixture-directory entries

Seat: KakeR31a2.CriticSymlinkCases (critic, leaf). Axis: operability. Milestone r31-falsify.
Clone: /fast/scratch/hyaku/kake-r31/a2-w2/CriticSymlinkCases/clone at fde133ab48086bb9a06911b4ab045e2ad9086347.
Runner sha256 5371530d93ecb218b4607fb37de810fe7b7b2db869c65c8b65988b2f04c0ce6c; SKILL.md sha256 611c9274ede550a6d3f7c2793cd162643db90675363a73f4879a04b5247f9ef8.
`git diff --stat fde133a 92235a0 -- scripts SKILL.md` in the lane is empty, so the results hold at the lane tip 92235a0.

## Counterexample (main finding)

A symlinked case whose name starts with "." is still skipped silently. Discovery at
`scripts/citing_set_selftest.py:679-683` keeps `(path.is_symlink() or path.is_dir()) and not path.name.startswith(".")`,
so the dot-name filter applies to symlinks too. With one valid control case plus `.10-link -> <valid case>`,
the runner exits 0, verdict clean, cases=1: the symlink is never counted. The runner docstring
(`:77-78` "a symlink in the fixture directory (a symlinked case is a failed case, never a silent skip)")
and SKILL.md (`:851` "a symlink in the fixture directory (a failed case, never a skip)") both claim more than this.
This is the exact N6 harm (a symlinked case vanishes, `corpus/lessons/round-30-verifier-spotcheck.md:258`), narrowed to dot names.
Hostile spec P5 (`scripts/fixtures/citing-set-hostile/P5-symlinked-case/hostile.json`) only builds a case named `h5`, so the hostile selftest cannot see this.
Note: a real dot-named directory is also skipped silently (exit 0 with control, exit 2 alone). That predates round 31
(base runner `f1ffb81:scripts/citing_set_selftest.py:575` has the same filter) and neither doc mentions the dot skip.

## Commands (all in the sandbox, TMPDIR=/fast/scratch/hyaku/kake-r31/a2-w2/CriticSymlinkCases/tmp)

- `bash /fast/scratch/hyaku/kake-r31/a2-w2/CriticSymlinkCases/build_and_run.sh` exit 0. For each fixture directory under
  `.../CriticSymlinkCases/fx/<name>` it runs
  `python3 -B clone/scripts/citing_set_selftest.py --root clone --fixtures fx/<name> --tmpdir runner-tmp/<name>`.
  "<name>" holds a copy of `01-single-literal-clean` as `00-control` plus the odd entry; "<name>-only" holds the odd entry alone.
  Summaries: `.../CriticSymlinkCases/out/<name>.json`; one-line log: `.../CriticSymlinkCases/run.log`.

## Table: entry | runner result | documented?

| entry (top level of --fixtures) | runner result with control / alone | documented? |
|---|---|---|
| symlink to a valid case dir `10-link` | exit 1 failed, "symlinked case directory refused" / exit 1 same | yes, correct (docstring :77-78, SKILL :851) |
| dangling symlink `10-link` | exit 1, refused / exit 1, refused | yes, correct |
| symlink to a regular file `10-link` | exit 1, refused (same reason text) / exit 1 | yes, correct (the reason says "case directory" for a file target: cosmetic) |
| dot-named symlink `.10-link` to a valid case | exit 0 clean, cases=1, skipped silently / exit 2 "contains no case directories" | NO: both docs say any symlink is a failed case, never a skip |
| regular file `10-file` | exit 0 clean, skipped silently / exit 2 | not mentioned; harmless (not a case) and "absent or empty can never report success" (:91-92) holds |
| FIFO `10-fifo` | exit 0 clean, skipped, no hang (is_dir stats, never opens) / exit 2 | not mentioned; harmless |
| extra: real dot-named directory `.10-hidden` | exit 0 clean, skipped silently / exit 2 | not mentioned; predates round 31 |

Extra entries inside a case (outside the N6 wording, recorded because "a symlink in the fixture directory" can be read as any depth):

| entry inside case `10-*` | runner result | documented? |
|---|---|---|
| `population.json` symlink to a file outside the case | runner does not refuse; copytree keeps the link; the gate refuses it: exit 1, `exit mismatch: expected 0, observed 2`, finding `input_invalid/path_escapes_root` | docs are silent on nested symlinks; the gate, not the runner, contains it |
| `case.json` symlink to a hostile `{"argv":["--selftest"]}` | exit 1, "case.json must be a regular file of at most 65536 bytes" | consistent with `:315` |
| dangling `case.json` symlink | exit 0 clean: `path.is_file()` at `:312` is false, so the case runs as if it had no case.json | not documented; no harm seen (the target is unreadable), but a broken setup file is ignored, not refused |
| FIFO `case.json` | exit 1, "case copy failed ... is a named pipe"; no hang | not documented; refused as a failure |

## Impacted axes

Operability: the containment claim for N6 is wider than the guard (doc truthfulness, false provenance of "never a skip").
No exit-code regression found: every refused shape exits 1, and an all-odd fixture directory exits 2, never 0.

## Smallest safe correction (either one)

1. Code: change the discovery filter at `scripts/citing_set_selftest.py:681` to
   `path.is_symlink() or (path.is_dir() and not path.name.startswith("."))`, so every symlink reaches the refusal at `:521`;
   add a dot-named symlink case to hostile spec P5.
2. Docs only: say "a symlink whose name does not start with '.'" in the docstring (:77) and SKILL.md (:851), and state that
   dot-named entries, regular files and FIFOs at the top level are skipped.

## Not verified

- Did not run the C1 counter, the hostile selftest or the 45-case fixture suite (other seats own those).
- Did not test TOCTOU swaps (an entry replaced between discovery and `run_case`), or symlinks deeper than one level inside a case
  other than `population.json` and `case.json`.
- No installs, no network, no lane writes other than this report.
