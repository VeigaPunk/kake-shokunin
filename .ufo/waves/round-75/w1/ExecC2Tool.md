# ExecC2Tool — C2 receipt tool (round 75, wave w1)

Seat: executor. Lane checkout `kake-shokunin`, measured base `c9c5e484c533aa65f4374b841a3edcf572ed19a9`
(freeze `88f2e05f` carries contract + amendment 1). Deliverable: this directory's
`instrument_receipts.py` (the L1 lands it as `scripts/instrument_receipts.py`) plus the receipts
below. No lane file was edited; every measurement ran in `git clone --shared` trees under
`/fast/scratch/hyaku/kake-r75/ExecC2Tool/`, each clone outside its scratch root.

- tool: `instrument_receipts.py`, 48,868 B, sha256 `162dd6852cd5f6adbf278405365464f0b2f5c5d66100883a0974c32b0e6a68e7`
- `--selftest`: **17/17**, exit 0 (`selftest.txt`, sha256 `13016087d729d8023be27d61b83cd70b2a74bde662ce251664edd904c626ef90`)
- self-entry at a simulated 18-file tip: `{"path":"scripts/instrument_receipts.py","sha256":"162dd685…","bytes":48868,"selftest_mode":true}`

## 1. Population derivation (independent of the C1 counter)

Frozen rule (contract §C1) implemented without importing `c75_row_truth.py`: a row is an 8-column
table row (unescaped-pipe split) inside a section matching `^### Round \d+ gate registry additions`;
live = Kind cell without `historical` (case-insensitive; no Kind cell in the tree carries a capital,
so this is identical to the C1 counter's lowercase test); instrument = Name cell when it is itself a
`.py`/`.mjs` path, else the first path token of the Entry-command cell, else of the Self-test cell,
else of the first cell in order carrying one; population = sorted distinct instruments.

Observed at `c9c5e484`:

```
$ python3 -B instrument_receipts.py --root <clone> --revision c9c5e484… --emit-population
16 lines; set-equal to the contract §C1 list (diff empty)          exit 0
```

Cross-check against the C1 counter's own derivation (imported `c75_row_truth.parse_rows`,
`.effective`, `.instrument` over the same `SKILL.md` text):

```
c1_files=16 c2_files=16 equal=True  only_c1=[]  only_c2=[]           (cross-check.txt)
```

Amendment 1 (population is a floor): `--check`/`--json` report `missing_frozen` (paths of the frozen
16 that no longer derive; gating) and `beyond_frozen` (live-row instruments beyond the 16; in-population).
Simulated landing commit with the round-75 section's two rows (`c75_row_truth.py`,
`scripts/instrument_receipts.py`): `population=18 … missing_frozen=0 beyond_frozen=2`, receipt covers
18, carrier check `bound=18 mismatches=0 met=true` (`i-sim-carrier.txt`).

## 2. `--selftest` registration — the exact detection rule

`.py`: the committed source must parse; it registers `--selftest` iff the AST contains
(a) a call `<expr>.add_argument(...)` with a positional string-literal argument exactly
`--selftest`, or (b) an `ast.Compare` in which one operand is the string literal `--selftest` and at
least one operator is `==`, `!=`, `in` or `not in`. Docstrings, comments, help text and subprocess
argv lists are bare `ast.Constant` nodes and never count. `.mjs`: `includes('--selftest')`,
`indexOf('--selftest')`, or `[!]==`/`!==` against the literal (fallback; no `.mjs` in this
population). Undecidable (non-UTF-8, syntax error, unknown extension) is `unparsable`, never `false`.

Measured at base: 15 of 16 derive `selftest_mode=true`; `c69_tmp_honour.py` derives `false` (it only
passes `--selftest` to `scripts/freshness-sweep.mjs` in a `run([...])` argv list), which is the row
contract §C1 demotes. Classifier unit check covers add_argument, `in`/`==` comparisons, docstring,
argv list, `.mjs` includes, comment, syntax error.

## 3. Receipt and `--write` idempotence

`corpus/knowledge/instrument-receipts.json`, `{"schema":"instrument-receipts/v1","revision","date",
"host","files":[{path,sha256,bytes,selftest_mode}]}`, sorted by path, 2-space indent, ASCII-safe,
one trailing newline. Digests/byte counts are of the committed blob (`git ls-tree` modes +
`git cat-file --batch`); never the worktree.

```
$ python3 -B instrument_receipts.py --root <clone> --revision c9c5e484… --write --date 2026-11-03
wrote corpus/knowledge/instrument-receipts.json revision=c9c5e484… population=16 missing_frozen=0 \
  sha256=b37d1b09415e2e63816c701324cf53d86b5e8dcc150130609583dcc836d81a69 bytes=3397      exit 0
```

Second write at the same revision: byte-identical (`cmp`, `receipt.write1.json` =
`receipt.base.json`). Simulated 18-file tip: `population=18 … sha256=942dcf769af305e4df734f2e730542cef4e69c885fa447cafd6790fbeb8bb491 bytes=3793` (`h-sim-write.txt`).

`--write` refuses with exit 2 when a population path is absent, not a regular file (symlink/gitlink)
or unparsable — observed in the simulation before the C1 counter blob existed: `2 unevaluable:
cannot bind .ufo/waves/round-75/c75_row_truth.py: it does not resolve to a blob at …`.

## 4. `--check` semantics (contract §C2 + amendment 1 + L1 amendment A3)

- The receipt is read **only** from committed bytes at `--revision`
  (`git cat-file blob <rev>:corpus/knowledge/instrument-receipts.json`). A receipt that exists only in
  the worktree is `source=uncommitted` and a mismatch for every population file (exit 1); the detail
  names the worktree copy. `--write` writes the worktree file; the caller commits it.
- The receipt's declared `revision` must be a 40-hex id that `git cat-file -e <rev>^{commit}`
  resolves and that is an ancestor of (or equal to) the measured revision
  (`git merge-base --is-ancestor`); otherwise every population file is a
  `receipt_revision_invalid` mismatch. Declared revision = *subject* (the blobs it pins); measured
  revision = *carrier* commit holding the receipt (normally a child).
- Per population file: digest, byte length and static `--selftest` flag must match; a missing entry,
  duplicate entry, shape error, absent blob, non-regular mode or unparsable source is a mismatch.
  One finding per unbound file, so `mismatches == population - bound`.
- An entry for a path outside the population is reported separately (`outside:`), is not counted
  toward `bound`, and does not gate — the frozen kill rule says exactly that; fixture asserts
  `bound=16 mismatches=0 met=true` with one junk entry.
- `met = (bound == population) and (mismatches == 0) and missing_frozen == 0`.
- Output line (always): `C2v1 revision=<carrier> population=<n> bound=<b> mismatches=<m> met=<bool>`,
  then `population: derived= frozen=16 missing_frozen= beyond_frozen=`, `receipt: source=… worktree=…
  declared=… declared_match=… declared_valid=…`, then findings. `--json` prints the line plus the JSON
  document. Exit 0 met, 1 not met, 2 unevaluable (root not a toplevel, revision unresolved, SKILL.md
  or a population blob unreadable), 64 usage (argparse errors are remapped to 64).

## 5. Measured runs (clone at base; commands and verdicts)

| # | Command | Observed | Exit |
|---|---|---|---|
| A | `--check` at `c9c5e484` (no receipt) | `population=16 bound=0 mismatches=16 met=false`; `source=none` | 1 |
| B | `--write --date 2026-11-03` | `population=16 … sha256=b37d1b09… bytes=3397` | 0 |
| B2 | second `--write`, same revision | byte-identical | 0 |
| C | `--check` at `c9c5e484`, worktree receipt only | `bound=0 mismatches=16 met=false`; `source=uncommitted worktree=only-worktree` | 1 |
| D | commit receipt (carrier `480bdce5…`), `--check <carrier>` | `population=16 bound=16 mismatches=0 met=true`; `source=committed worktree=identical declared=c9c5e484… declared_valid=true` | 0 |
| E | `--check c9c5e484` in the carrier tree | `source=uncommitted`; `bound=0 mismatches=16` — a worktree copy at a revision that does not carry it is not evidence | 1 |
| F | fabricated committed receipt (all digests `0`×64, bytes 0) | `bound=0 mismatches=16 met=false`, finding class `digest` | 1 |
| G | committed receipt with one path dropped | `bound=15 mismatches=1 met=false`, class `missing` | 1 |
| H | committed receipt, one `selftest_mode` flipped | `bound=15 mismatches=1 met=false`, class `mode-flag` | 1 |
| I | restore real receipt, commit, `--check <carrier>` | `bound=16 mismatches=0 met=true` | 0 |
| J | simulated landing (18 instruments) → write, commit, `--check <carrier>` | `population=18 bound=18 mismatches=0 met=true`, `declared_valid=true` | 0 |
| K | usage: `--bogus`, `--write` without `--date`, `--date 2026-02-30`, `--selftest` without `--work` | `64 usage: …` | 64 |
| L | `--root` not a repository | `2 unevaluable: … is not a git repository` | 2 |
| M | landed tip `4e3fc159` (lane HEAD, receipt pinned `f1fc5d0a`), `--check <tip>` | `population=18 bound=18 mismatches=0 met=true`; `source=committed worktree=identical declared_valid=true` | 0 |

The landed `scripts/instrument_receipts.py` is byte-identical to this directory's file
(sha256 `162dd685…`), and the landed 18-entry receipt re-derives at the tip (`m-landed-tip.txt`).

Receipts: `a-base-absent.txt`, `b-write.txt`, `b2-write.txt`, `c-uncommitted.txt`,
`d-carrier-green.txt`, `e-ctl-fabricated.txt`, `e-ctl-dropped.txt`, `e-ctl-modeflip.txt`,
`f-restored.txt`, `g-sim-tip-before-write.txt`, `h-sim-write.txt`, `i-sim-carrier.txt`,
`m-landed-tip.txt`, `check-json.txt`, `cross-check.txt`, `population.txt`.

## 6. `--selftest` — 17 isolated fixtures under `--work`

Each fixture is its own `git init` repo (toplevel asserted equal to the fixture dir before the first
commit; `-c user.name/-c user.email/-c commit.gpgsign=false` on every commit). Fixture `SKILL.md`
carries the 16 frozen paths in a Round-900 section with all four name/entry/selftest/pinned
placements, a `historical` row naming a file that must be excluded, and a non-matching section whose
row must be ignored.

```
green: write, idempotent rewrite, committed, check at carrier, emit-population
missing receipt: bound=0 mismatches=16
uncommitted receipt: ignored, bound=0 mismatches=16
wrong digest: bound=15 mismatches=1
wrong byte count: bound=15 mismatches=1
wrong mode flag: bound=15 mismatches=1
duplicate path: bound=15 mismatches=1, class duplicate
path outside population: reported separately, bound=16 mismatches=0
declared revision of another commit, changed blob: bound=15 mismatches=1
receipt committed after its declared revision: unchanged bytes bind
declared revision that does not resolve: receipt_revision_invalid, bound=0
declared revision not an ancestor: receipt_revision_invalid, bound=0
fabricated receipt (16 paths): bound=0 mismatches=16
live row beyond the frozen 16: population=17 bound=17
missing_frozen=1 keeps met=false with bound=16 mismatches=0
classifier: add_argument, comparisons, docstrings, argv lists, .mjs
usage: --write without --date exits 64, --selftest without --work exits 64
selftest: 17/17                                                              exit 0
```

Fixtures stay under `<--work>/fx-*/` for inspection (the scratch tree that contains them is deleted
before yield; the transcript is `selftest.txt`).

## 7. Risks, limits and handoff

- **Carrier, not subject, is the check revision.** The admission command must name the commit that
  holds the receipt, e.g. `--check --revision <landing commit>`; `--check --revision <pinned base>`
  in a later tree is red by design (the receipt is not committed there). The declared revision must
  be an ancestor, so write at the landed row revision, commit the receipt as a child, check the child.
- **ExecC2Receipts flow change:** after `--write` the receipt must be committed in the clone before
  `--check`; a worktree-only receipt is `source=uncommitted`, `bound=0 mismatches=16`, exit 1. The
  write output gives the exact receipt sha256/bytes. Simulated 18-file flow: write at the landed
  subject, commit, check the child → `population=18 bound=18 met=true`.
- **Outside entries do not gate** (frozen kill rule: "not counted toward bound and is reported
  separately"). A reviewer wanting junk entries to fail must amend the contract, not the tool.
- `--write` exit 2 on an unreadable/unparsable population file; a registry row naming a file that
  does not exist at the measured revision makes a receipt impossible (and `--check` reports it as
  `absent`).
- No lane edits, no commits in the lane, no mutating git/jj in the lane; no tool installs were needed
  (git 2.56.0, Python 3.14.8 already present); scratch tree deleted after the receipts were copied.
