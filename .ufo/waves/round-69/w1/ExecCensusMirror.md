# ExecCensusMirror — SOURCES append guard (round 69, W1)

Base: `4d188f9477b4301a2c93c8ef5c13bc6c6f4bb6e4`. `corpus/SOURCES.md` at base: 289 lines, sha256 `aa6d76f7…59df8caa`, 173 registry rows (S001–S435). Lane HEAD during the work: `dbcfef0b` (contract commit). Validator: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, sha256 `3fb72615…d4a64e30`. Guard: `guard.sh`, sha256 `ea374f58…52469cd8f`.

## Delivered

| File | What it is |
|---|---|
| `guard.sh` | `guard.sh <registry.md> <staged-rows.md> <outdir>` — id-collision guard. Writes `registry.ids`, `staged.ids`, `collisions`; prints `registry_ids=<n> staged_ids=<n> collisions=<n>`; exit 0 clean, 1 on collision, 2 on usage/missing input. |
| `measure.txt` | Every command, its stdout/stderr and its exit code, sections 0–8. |
| `run-measure.sh` | Rebuilds `measure.txt` from scratch (idempotent; all state under `/fast/scratch/hyaku/kake-r69/ExecCensusMirror`). |
| `fixtures/registry.indented.md` | The attack fixture: base registry with the real S435 row prefixed by two spaces. |
| `fixtures/staged.dup435.md` | Staged file with one row whose id is S435. |
| `fixtures/staged-rows-placeholder.md` | The two placeholder staged rows used for the mirror (see "Staged rows"). |

## guard.sh

```bash
LC_ALL=C grep -oE "^ {0,3}\|[[:space:]]*S[0-9]{3,}" -- "$REG"   | grep -oE 'S[0-9]+' | LC_ALL=C sort > registry.ids
LC_ALL=C grep -oE "^ {0,3}\|[[:space:]]*S[0-9]{3,}" -- "$STAGED" | grep -oE 'S[0-9]+' | LC_ALL=C sort > staged.ids
comm -12 registry.ids staged.ids > collisions
```

0–3 leading spaces is deliberate: it is exactly `sources-census.sh`'s own row acceptance (`^ {0,3}\|`, 4+ spaces = indented code, ignored there and therefore ignored here). `LC_ALL=C sort` on both sides keeps `comm` consistent. The scan is whole-file and lexical (as specified), not section-scoped; section 7 of `measure.txt` records that the base file has no `| S###` row outside `## Registry`, so the two readings coincide today.

## Attacks and verdicts (all exercised; see measure.txt sections 2, 4, 5, 6)

| # | Attack | Expected | Observed | Verdict |
|---|---|---|---|---|
| A1 | Indented real row (two spaces before `\| S435 \|`) + staged S435 | collisions nonempty, exit 1 | `registry_ids=173 staged_ids=1 collisions=1`, `collisions` = `S435` (5 bytes, 1 line), exit 1 | **KILLED** — guard fails as required |
| A2 | Anchoring attack: a column-0-only pattern (`^\|`) against the same fixture | a naive guard misses it | naive: `naive_registry_ids=172`, `naive_collisions_bytes=0`; shipped pattern: `collisions=1`, `S435` | **KILLED** — the 0-3-space anchor is what makes the guard catch the indented row |
| A3 | Legitimate append S436+S437 against the base registry | no collision, exit 0 | `registry_ids=173 staged_ids=2 collisions=0`, exit 0 | PASSED (no false positive) |
| A4 | Unmodified base copy through the validator | exit 0 | `file ok …` + 16 W04 warnings, exit 0 | PASSED |
| A5 | Staged mirror through the validator | exit 0, warnings only | `file ok …` + 16 W04, exit 0 | PASSED |
| A6 | Validator red: staged row with a literal `\|` inside its `teaches` cell (12 cells) | nonzero | `file E01 S436 fields=12`, exit 1 | **KILLED** — validator fails as required |
| A7 | Empty staged file / missing staged file / wrong arity | no false alarm / exit 2 | `staged_ids=0 collisions=0 exit 0`; `staged rows not found … exit 2`; `usage: … exit 2` | PASSED |

Exit code of the guard itself is the collision signal (`[ "$col_n" -eq 0 ]`), so a caller can gate the append on `guard.sh` directly; the `collisions` file is the receipt.

## Mirror validation (measure.txt section 4)

`git -C <lane> archive 4d188f94 corpus | tar -x -C <scratch>/mirror` gives a corpus-only tree; validating it **exits 1** with 17 E11 `used-by` findings (`scripts/source_recheck.py`, `SCORECARD.md`, `SKILL.md`, …) because `--file` resolves used-by paths against `dirname(file)/..` and those siblings are not in a corpus-only archive. That is a property of the mirror slice, not of the append. Re-run against a full base archive (`git archive 4d188f94 | tar -x`), the unmodified base copy is **exit 0** with 16 W04 warnings and `file ok`, which is the required control.

Staged mirror = full base tree + the two staged rows inserted after the last `| S` row of `## Registry` (line 181, before the blank lines and `## Paths`): 173 → 175 rows, S436 at line 182, S437 at 183.

`validate` on the staged mirror **as-is exits 1** with two E11 rows: `S436 missing used-by corpus/lessons/round-69.md` and the same for S437. `corpus/lessons/round-69.md` does not exist at base (`git ls-tree 4d188f94 corpus/lessons/` has no `round-69.md`). With a stub of that path added to the mirror, `validate` is **exit 0** with 16 W04 warnings and `file ok`.

**Integration consequence for the L1:** the SOURCES append and `corpus/lessons/round-69.md` must land in the same commit (or the lesson first). Appending the rows alone turns the lane gate red on E11.

## Staged rows

`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-69/w1/ScoutSources/rows-draft.md` **did not exist** when step 3 ran (`ls` exit 2, recorded in measure.txt section 3), so the two placeholder rows mandated by the seat spec were used: S436 (Node.js `os`, `https://nodejs.org/api/os.html`) and S437 (Python `tempfile`, `https://docs.python.org/3/library/tempfile.html`), each with the registry's 11-column schema, `status=mined`, `used-by=corpus/lessons/round-69.md`, cells marked `PLACEHOLDER`. They are rehearsal rows only — **not** opened sources, and they must be replaced by ScoutSources' real rows before the append. They are retained at `fixtures/staged-rows-placeholder.md`.

## Behaviour, retained evidence, risks

Behavior: `guard.sh <registry> <staged> <outdir>` → three sorted id files, a `comm -12` intersection, one summary line, exit 0/1/2. Nothing is written outside `<outdir>`.

Evidence retained: `measure.txt` (299 lines, full command/exit transcript), `run-measure.sh`, the three fixtures, `guard.sh`. Scratch tree `/fast/scratch/hyaku/kake-r69/ExecCensusMirror` removed after the final run.

Lane untouched: `git -C <lane> status --porcelain` shows only the pre-existing untracked `.ufo/waves/round-69/` wave files; the base `SOURCES.md` blob sha256 still equals the base tree's (`aa6d76f7…`). No tracked file in the lane was edited, nothing was committed, and no fleet-root path was written.

Risks / limits:
1. The guard scans the whole file lexically, per spec; a `| S###` row outside `## Registry` (the census's E12 class) would count as an id. Base has none; after the append this remains true (section 7a), but a future row misplaced below `## Paths` would be caught by the census (E12) and not specially by this guard.
2. Duplicate ids inside the staged file itself are not reported (only registry∩staged); the census E03 catches those at integration.
3. W04 warnings (16) are pre-existing and identical before and after the append; they do not affect exit status.

Tooling: nothing installed or upgraded; no package manager was run.
