# RowSiblingMteLedger — SOURCES row and Gate line for the sibling MTE ledger (round 30, wave 1)

Lane: /home/vgpnk/Projects/shokunin/kake-shokunin. Seat: scribe, axes operability, milestone r30-build. Scope: draft only. Nothing landed in the lane except this report; no network request of any kind; no Git or jj write in the lane.

## What I built

1. A `corpus/SOURCES.md` registry row S056 (11 cells) for the admitted sibling source `tameshi-shokunin/corpus/knowledge/mte-report-interop.md` at revision `f4e8f7d8`, opened read-only.
2. The `corpus/lessons/round-30.md` Gate line for that row, with a located quote of 9 words.
3. Three sentences on what the sibling's ledger shape implies for recording killed and surviving mutants of the citing-set runner.
4. A frozen-census check of the drafted row (CORPUS.md census commands) on a sandbox copy.

## The row (draft text, to be appended after the S048 row)

| S056 | Sibling lane tameshi, MTE report interop — tameshi-shokunin/corpus/knowledge/mte-report-interop.md at commit f4e8f7d8 | docs | B | The record shape of a sibling lane's mutation ledger: one verdict per defect id plus a separate aggregate count check, and the rule that a score derived from that same ledger is a sanity check; not a primary source for any fact about kake's citing-set gate | commit f4e8f7d835a8e33c64a87ff93e79da32264f031c, sections "What the interop does" (lines 10-22) and "Decision table - exporting a tameshi sweep as a report" (lines 159-164), file sha256 b173e3e549d0227e0d37df92956b652084290955bdcb6a0a7cbf2a9ad29c0fac | A mutation ledger records one verdict per defect id and checks the killed and survived counts separately, and any score computed from that same ledger is a sanity check rather than an independent measurement | queued | 2026-10-22 | on-release | - |

Cell notes: id S056 is free in the lane registry (S001-S048 today). `kind` `docs` and `tier` `B` follow the fleet precedent for a sibling lane's corpus entry (tsukuroi-shokunin/corpus/SOURCES.md S125, S127: "Sibling lane mori, ..." at a pinned commit, kind `docs`, tier B, scope "not a primary source for any kernel fact"). CORPUS.md tier A covers "the lane's own re-runnable gate output", so a sibling lane's prose account of its own gate is not A for kake. `status` `queued`, not `mined`, with the reason in the Gate line: the source is opened and quoted this round, but no landed kake corpus entry cites it yet, so `used-by` stays "-" until one does (the rule the round-29 rows S047 and S048 follow). `recheck` `on-release` because the sibling file changes with that lane's releases, as in tsukuroi S125.

## The Gate line (draft, for `## Gate` of corpus/lessons/round-30.md)

- S056 - tameshi-shokunin/corpus/knowledge/mte-report-interop.md at commit f4e8f7d8 (sibling lane tameshi, read-only `git show`) - opened 2026-10-22, section "What the interop does", line 21: "`score` is a sanity check that holds by construction." - queued: the source is opened and quoted this round, but no landed kake corpus entry cites it yet, so the row stays queued until the citing-set mutant-ledger entry lands and names it in `used-by`.

## Quote substring check

Primary quote "`score` is a sanity check that holds by construction." - 9 words (limit 25), no pipe, exact substring of the file at `f4e8f7d8`, first occurrence on line 21. Two supporting quotes, both exact substrings and both under 25 words, carry the implication sentences: line 18-19 (the file wraps this sentence over two lines, so the exact substring contains the newline) "`per_mutant` compares every emitted\nstatus with the committed recorded verdict of the same defect id in the" - 17 words; and line 169 "`balanced-flip-same-counts` (counts agree but ids are swapped: only the" - 9 words.

## The implication sentences (for the lesson body)

1. Tameshi's ledger keeps one record per seeded defect id and then checks two things separately - the aggregate killed, survived, invalid and total counts against the runner's own table line, and every individual status against the recorded verdict of the same id - so kake's citing-set mutant ledger should carry a per-mutant id to verdict record next to a separate count cross-check, because a balanced flip (counts agree, ids swapped) is invisible to the aggregate alone.
2. A mutant that the fixture runner could not evaluate is not a survivor: the runner exits 2 for could-not-evaluate and 64 for a usage error, so those mutants must be recorded as inconclusive and excluded from the kill denominator killed/(killed+survived), the way tameshi maps its INCONCLUSIVE verdict out of the valid set instead of into survived.
3. Any rate computed from kake's own ledger is by construction, because the same recorded table feeds both sides of the comparison, so it is a sanity check on the ledger's internal consistency and not an independent measurement of the citing-set gate's strength.

## Commands run, exit codes, observed output

1. `git -C .../tameshi-shokunin rev-parse f4e8f7d8` - exit 0: `f4e8f7d835a8e33c64a87ff93e79da32264f031c`.
2. `git -C .../tameshi-shokunin log -1 --format='%H %ad %s' --date=iso f4e8f7d8` - exit 0: `f4e8f7d835a8e33c64a87ff93e79da32264f031c 2026-10-22 06:40:33 -0300 round-25: retain late SiblingOverlap seat report`.
3. `git -C .../tameshi-shokunin show f4e8f7d8:corpus/knowledge/mte-report-interop.md > mte.md` (read-only, 170 lines) - exit 0; `git rev-parse f4e8f7d8:corpus/knowledge/mte-report-interop.md` gives blob `eb34dfaef6e086aee02ac40b7bfcf4782a4863c6`; file sha256 `b173e3e549d0227e0d37df92956b652084290955bdcb6a0a7cbf2a9ad29c0fac`.
4. `python3 -B check.py` in the sandbox - exit 0: `full hash matches row anchor: True`; `sha256 in row anchor: True`; primary quote `words=9 substring=True single_line=True pipes=False first_line=21`; per-mutant quote `words=17 substring=True single_line=False first_line=18`; balanced-flip quote `words=9 substring=True first_line=169`; row `cells: 11`, `kind in enum: True`, `tier in ABC: True`, `status in enum: True`, `no pipe inside cells: True`; `S056 present: False` against the lane registry.
5. Frozen census (CORPUS.md commands) on a sandbox copy of `corpus/SOURCES.md` with the row appended - all exit 0: `rows 49`, `malformed 0`, duplicate ids printed nothing, enum/tier check printed nothing.
6. Same enum check on the literal `kind` variant - printed `kind S056 sibling` (see the conflict below).
7. `git -C /home/vgpnk/Projects/shokunin/kake-shokunin status --porcelain` - exit 0; only the pre-existing untracked wave files (`.ufo/waves/round-30/w1-assignments.json`, `w1-dispatch.json`, `w1-spec.json`, `w1/`) plus this report. No tracked lane file changed.

## Conflict for the canonical judge (verbatim)

The assignment asks for "kind sibling". The frozen CORPUS.md v1 kind enum is `spec | docs | paper | code | tool | dataset | talk | book | community | own-work`, and its census prints for the literal variant: `kind S056 sibling`. My recommended row therefore carries `kind` `docs` with the sibling designation in the source cell ("Sibling lane tameshi, ..."), matching the fleet precedent (tsukuroi S125/S127). Landing the literal `sibling` kind would fail the lane's own registry census; the L1 chooses between the two cells, the rest of the row is identical. Second tier note: if the L1 would rather cite tameshi's tool itself (`tools/mte-interop.py`) than its prose, tameshi's own S033/S036 precedent applies - a sibling gate script is `kind` `code`, `tier` `A`, scoped to "the gate's own behavior at the measured revision". The prose row above stays B.

## Gates

- CORPUS.md rule 1 (a row is a claim; the Gate records the access date and a ≤25-word quote): the source was opened this round with one read-only `git show`, and the quote is an exact substring of that text.
- CORPUS.md rule 6 and the census: no credential material, no session URL, no `|` inside any cell.
- Lane bounds: only this report was written inside the lane; every other artifact is in the sandbox; the sibling repo was read with `git show`/`rev-parse`/`log` only; no owned web property was contacted.

## Touched surfaces

- Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-30/w1/RowSiblingMteLedger.md` (this report, the only file written in the lane).
- Sandbox: `/fast/scratch/hyaku/kake-r30/w1/RowSiblingMteLedger/` - `row.md` (draft row, Gate line, implication sentences), `check.py` (the verification script above), `mte.md` (the sibling file at the pinned revision), `census/corpus/SOURCES.md` (the census copy).

## Out of scope

- Landing the row and the Gate line; creating `corpus/lessons/round-30.md` or a citing-set knowledge entry; the C1 interface change and the C1 counter; the mutation-tester seat's stub work.
- Rows S053-S055: not assigned to this seat and not yet in the lane registry, so the L1 should confirm S056 does not collide when those rows land. Registry state re-read after my checks: the lane `corpus/SOURCES.md` now ends at S052 (the Render rows S049-S052 landed meanwhile, 4 insertions in the working tree); S056 is still free.

## Findings for the L1

1. The reason a reason-only mutant could survive the current oracle: `grep -rl reason scripts/fixtures/citing-set` returns 0 files, and `expected.json` carries only `exit` and a `findings` id list (checked in cases 01 and 02). A mutant that keeps the same exit code and the same finding ids but emits a wrong reason code is a survivor today, so the mutant ledger should record the per-case expected reason codes once the C1 fixtures carry them.
2. Corroboration from the mutation seat (reported by peer KakeR30.MutC1CounterStubs, not observed by me): its ledger row carries one row per mutant with the failed check ids plus a count cross-check, because a wrong-reason mutant was caught only through a coupled path (one wrong reason breaks the shared runner baseline, so the score fell 14 to 4 rather than by one check) and because the counter's compared condition can accept any runner failure after the rename (a false 14/14 on a reason-blind runner). Both are the sibling file's own warning in another shape: a leg whose setup is broken is refused as SETUP and not judged (lines 49-52, 21), and a score derived from the same table is by construction, not an independent measurement.
3. Promotion path for this row: while `corpus/lessons/round-30.md` and the citing-set knowledge entry do not exist, `status` must stay `queued` with `used-by` "-" (a `mined` row whose `used-by` path does not exist fails the census). When the L1 lands the lesson, promote with the old→new log that the append-only rule 2 requires.

## Artifacts

- /fast/scratch/hyaku/kake-r30/w1/RowSiblingMteLedger/row.md
- /fast/scratch/hyaku/kake-r30/w1/RowSiblingMteLedger/check.py
- /fast/scratch/hyaku/kake-r30/w1/RowSiblingMteLedger/mte.md
- /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-30/w1/RowSiblingMteLedger.md (this report)

Tooling: nothing installed or upgraded this seat; no install was needed.
