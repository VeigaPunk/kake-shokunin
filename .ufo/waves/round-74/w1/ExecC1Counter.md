# ExecC1Counter — round 74, wave w1 — C1 registry-gap counter

Seat: `ExecC1Counter` (executor, kake lane, round 74, wave w1, attempt 1). Date: 2026-11-03.
Base: `ced2878a1e77f57afb4ee3baebf1021e5130399b`; freeze commit `b35dd4d7`
(= `b35dd4d7d6a0a633d7c950bf641d3f948e680448`). Lane was read-only for this seat: git reads
only (`rev-parse`, `cat-file -e`, `show`, `ls-tree`, `diff --stat`), no mutation anywhere.

## Deliverable

- Counter: `.ufo/waves/round-74/w1/ExecC1Counter/c74_registry_gap.py`
- sha256: `5dbc8124356e1386e083430e557a4ac9e65cd7eaa3762e97bc132f5e09e5e840`
- Report: `.ufo/waves/round-74/w1/ExecC1Counter.md` (this file)
- Receipts: `.ufo/waves/round-74/w1/ExecC1Counter/receipts/` (9 files, listed below)

## Axes

- **Calibration** (the claim's owned axis): the lane's self-assessment (`SKILL.md` gate
  registry) vs observed repo state at a revision — is every frozen counter registered with a
  row whose named path resolves, and does the round register its own counter?
- **Reproducibility** (sub-axis): the counter's base run must byte-match the frozen control
  receipt. Achieved (cmp exit 0).
- **Kill power** (sub-axis): `--selftest` must kill every contract fixture f1–f5. Achieved
  (5/5).

## Implementation contract (as built, per frozen C1)

- Args: `--root <lane>` (default `.`), `--revision <rev>` (default `HEAD`), `--json`,
  `--selftest`, `--work <scratch dir>` (selftest fixture repos; else one under `TMPDIR`).
- Population: the 8 contract counters hard-coded, repo-relative, in contract order
  (c69_recorded_counts, c69_tmp_honour, c70_pointer_audit, c71_calibration, c71_tmp,
  c72_tmp_v2, c73_tmp_v3, c73_wave_pointers).
- Row detection: line starts with `'| '` and carries `>= 6` `'|'`; a row names a counter iff
  the exact filename appears in one of its cells; prose outside such a row never counts.
- Conjunct 2: per naming row, the first backticked token ending `.py` is extracted and
  resolved with `git -C <root> cat-file -e <rev>:<path>`; a naming row with no such token
  (`no_path`) or an unresolved one (`path_unresolved`) is a finding.
- Conjunct 3 `own_row`: any table row naming `c74_registry_gap.py`.
- `met` = unregistered==0 ∧ no path findings ∧ own_row, with every population file resolvable.
- Exits: `0` met · `1` not met · `2` unevaluable (revision unresolvable, `SKILL.md` missing,
  population file missing/renamed → never silently met) · `64` usage.
- Stdlib only; Python 3 (host: 3.14.8); runs with `-B`; honours `TMPDIR`; no `/tmp` literal
  (`grep -c '/tmp'` → 0 matches).

## Verification — exact commands and exit codes

All runs from fleet-root cwd with absolute paths; counter invoked as
`python3 -B <counter> --root /home/vgpnk/Projects/shokunin/kake-shokunin …`.

1. **Base reproduction** (`--revision ced2878a1e77f57afb4ee3baebf1021e5130399b`):
   exit **1**; stdout `cmp` against `.ufo/waves/round-74/controls/base-c1-registry.txt` →
   **CONTROL-IDENTICAL** (0 bytes differ, 386 bytes). Base run line: `unregistered=7 met=false`.
   Receipt: `receipts/base-run.txt`.
2. **Freeze commit** (`--revision b35dd4d7`): exit **1**, tail `unregistered=7 met=false`;
   only the mandated revision line differs from base (`…revision=b35dd4d7d6a0a633d7c950bf641d3f948e680448…`).
   Expected: the `SKILL.md` blob is byte-identical base↔b35 (`diff` empty) and all 8 population
   files exist at both revisions (`git cat-file -e` → 0 for 8/8 at each). Receipt:
   `receipts/b35-run.txt`.
3. **Selftest** (`--selftest --work <scratch>/selftest-work`): stdout `selftest 5/5`, stderr
   empty, exit **0**; fixture repos removed in-finally (work dir left with 0 entries). Re-run
   with `TMPDIR` pointed at a scratch dir: `selftest 5/5`, exit 0. Receipt: `receipts/selftest.txt`.
4. **JSON** (`--json` at base): valid JSON (`python3 -m json.tool` ok); fields
   `unregistered=7 own_row=false met=false exit=1 path_findings=0 unevaluable=[]`; c73 row
   resolves (`path_unresolved` absent). Receipt: `receipts/base-json.txt`.
5. **Usage**: `--bogus` → **64**; `--root` without value → **64**.
6. **Unevaluable**: `--revision 0000000000000000000000000000000000000000` → exit **2**, tail
   line `unevaluable=revision`. Receipt: `receipts/uneval.txt`.
7. **Syntax/hygiene**: `py_compile` → `syntax-ok` (receipt `receipts/syntax-ok.txt`);
   `find <w1> -name '__pycache__' -o -name '*.pyc'` → 0; `sha256sum` receipt `receipts/sha256.txt`.
8. **TMPDIR honour**: concurrent watcher during 4 back-to-back `--selftest` runs with `TMPDIR`
   set observed the fixture dir appear under it (`fixture_dir_observed_under_TMPDIR=1`), and
   `tempfile.mkdtemp()` under that `TMPDIR` asserts under it. Receipt: `receipts/tmpdir-proof.txt`.

### Selftest fixtures (kill table)

| Fixture | Seeded defect | Assertion that kills it |
|---|---|---|
| f1 | one population counter absent from the registry | exit 1 ∧ `unregistered_names == [s3_counter.py]` ∧ rows `[1,1,0]` ∧ not met |
| f2 | counter named only in a non-first (alias) cell — positive control | exit 0 ∧ unregistered 0 ∧ `own_row=true` ∧ `met=true` ∧ no findings |
| f3 | counter mentioned only in prose (incl. a backticked command outside any row) | exit 1 ∧ rows(s1)==0 ∧ `unregistered_names == [s1_counter.py]` |
| f4 | naming row whose entry-command path is not committed | exit 1 ∧ `path_unresolved` finding on that row ∧ not met |
| f5 | population counter file missing from the repo (renamed case) | exit **2** ∧ `unevaluable == [s3_counter.py]` ∧ never met |

f2 doubles as the after-state rehearsal: exactly the landing shape (8 rows resolvable, one
counter named in a non-first cell, own row present) yields `met=true`, exit 0.

## Deviation from the control

**None.** Base run is byte-identical to `controls/base-c1-registry.txt`; exit 1 as frozen. The
b35dd4d7 run differs only in the revision line, which the measured revision change requires.

## Tooling installs

None. `~/.omp/agent/RULES.md` was read; nothing installed or upgraded (python3 3.14.8 and git
preexisting); pacman guard respected (no pacman transactions).

## Risks / notes for the L1

- Path extraction takes the **first** backticked `.py` token in a row. In the current registry
  the entry-command cell is the first `.py` span, so this is exact at base and b35. A future
  row placing another `.py` backtick earlier than the entry command would resolve that token
  instead (deterministic, and any miss surfaces as a `path_unresolved` finding, fail-closed).
- Unevaluable runs append an `unevaluable=<names>` line after the control-shaped tail; the
  control case itself stays byte-exact (unevaluable empty there).
- Per the frozen kill rule, `own_row` requires only a row naming `c74_registry_gap.py`; its
  entry-command resolution is reported in `--json` (`row_paths`) but does not gate `met`.
- After-state expectation for the landing tip: with the 8 rows added (or alias rows) each
  carrying a resolvable entry-command path, plus a round-74 row naming `c74_registry_gap.py`,
  the counter returns `unregistered=0 own_row=true met=true`, exit 0 (see f2 rehearsal).

## Scope and cleanup

- Writes: counter, this report, `receipts/` — all under `.ufo/waves/round-74/w1/ExecC1Counter/`.
- Scratch `/fast/scratch/hyaku/kake-r74/ExecC1Counter/` deleted before yield (`rm_exit=0`,
  verified `scratch-gone`); receipts copied out first. No scratch residue; no defect to report.
- No commits/pushes/stashes, no fleet-repo or sibling-lane writes, no `.ufo/state/`,
  `MANIFEST.json`, `.scratch/` or templates touched; no subagents spawned.

Report: .ufo/waves/round-74/w1/ExecC1Counter.md
