# Held-out fixture manifest — ReviewerC1, kake round 74 w1

Ten held-out `SKILL.md` fixtures attacking the `c74_registry_gap.py` parser design, authored
before the counter exists in the lane. Each is a mini registry table plus prose. Expected
verdicts are derived from the frozen round-74 contract predicate only (conjunct 1: >=1
gate-registry table row whose cells contain the exact filename; conjunct 2: the counter path
named by *each* such row resolves at the measured revision; conjunct 3: own row names
`c74_registry_gap.py`).

| Fixture | Target counter | Contract-required result | Naive implementation likely shows | Kill-rule anchor |
|---|---|---|---|---|
| f01-kind-cell.md | c71_calibration.py | registered (filename in Kind cell — any cell counts) | unregistered (first-cell-only matcher) | f2 |
| f02-prose-only.md | c70_pointer_audit.py | NOT registered (prose mention only) | registered (whole-file substring matcher) | f3 |
| f03-command-path-other-counter.md | c69_recorded_counts.py | NOT registered for it (row's cells name c69_tmp_honour.py only); the row does register c69_tmp_honour.py | cross-credits the row to the round-69 sibling via `c69_`/path proximity | — (conjunct 1 scope) |
| f04-prefix-collision.md | c72_tmp_v2.py | NOT registered (only row names `c72_tmp.py`, a file absent from the tree; exact-filename rule) | registered via stem/prefix normalization; or false conjunct-2 failure on the dead out-of-population v1 path | — (exact filename; conjunct-2 scope) |
| f05-fenced-row.md | c69_tmp_honour.py | NOT registered (row is inside a fenced code block — documentation, not a rendered registry table) | registered (fence-unaware line matcher) | f3 spirit; AMBIGUITY A3 — must be pinned in `--selftest` either way |
| f06-duplicate-rows.md | c71_tmp.py | registered (conjunct 1) but overall NOT met: the second registering row's entry-command path `c71_tmp_pre_rename.py` is dead and conjunct 2 says "each such row" | met (first-matching-row-only conjunct 2) | f4 |
| f07-dead-path.md | c73_wave_pointers.py | registered (Name cell) but overall NOT met: the row's only path `c73_wave_pointers_missing.py` is dead | met (conjunct 2 skipped or matched against the Name-cell filename) | f4 |
| f08-leading-dot-slash.md | c69_tmp_honour.py | registered; conjunct 2 must resolve `./.ufo/waves/round-69/c69_tmp_honour.py` to the same blob. `git cat-file -e <rev>:./path` resolves only with the process cwd at the repo root (probed: exit 0 from lane root); cwd elsewhere fails | environment-dependent verdict; normalize the path or run from `--root`, and pin the choice in `--selftest` | — (conjunct 2 mechanics; AMBIGUITY A5) |
| f09-outside-population.md | none (rows name c56_selftally.py, c66_gate_status_hostportable.py, and never-committed c99_absent_probe.py) | no effect on the frozen population verdicts; no crash; the permanently dead c99 path must be ignored (conjunct 2 quantifies over population rows only) | false conjunct-2 failure from scanning dead out-of-population rows | — (population quantifier) |
| f10-alias-command-cell.md | c70_pointer_audit.py | registered (filename appears only in the Entry-command cell — the real alias-row shape of base lines 1253/1396) | unregistered (first-cell-only matcher) | f2 |

## Assertion protocol

`run-against-fixtures.sh` builds a throwaway git repo per fixture (fixture as `SKILL.md` plus
stub files at the eight frozen population paths so conjunct 2 is decidable per row), commits
with a throwaway identity inside the fixture only (`git rev-parse --show-toplevel` asserted
first), and runs the counter with `--root <fixture-repo> --revision <head> --json`.

- Overall exit is 1 for every fixture (at most one of eight counters is ever registered and
  no fixture carries an own row); the observable is the **per-counter registration** of the
  target, plus the **conjunct-2 finding on the dead row path** for f06/f07.
- f08: record which normalization the counter applies; both choices are contract-live until
  pinned, but the choice must be deterministic and exercised by `--selftest`.
- f05: record whether the fenced row counts; the choice must be pinned and selftested (A3).

Status at authoring time (2026-11-03, lane HEAD b35dd4d7): `c74_registry_gap.py` is absent
from the tree (`test -f` exit 1), so every fixture run is `NOT_RUN`; rerun the harness once
the counter lands.
