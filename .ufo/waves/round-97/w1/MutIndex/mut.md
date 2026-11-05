# MutIndex — mutation test of the frozen C1 counter (`c97_index.py`)

Seat: MutIndex (leaf member, no subagent dispatch). Lane tip at start: `9e27ce0b2a8d168e032ab79ea11471b36eaceedf`.
Round base `36d148f5c60100021304903c30e5663207c72f4f`. Instrument digest verified before any run:
`8535150e91bd610bd42186b3ad8be23477b0386a1f8d14b95aba8375788aa008` (matches `controls/instrument-sha256.txt`).

## Method

- Pristine copy taken from the lane instrument into scratch (`/fast/scratch/hyaku/kake-r97/MutIndex/pristine/`); the
  lane copy was never edited. Pristine hash re-verified before every mutant run.
- 14 single-point mutants, each built as exact unique-anchor string replacements (asserted count == 1) on the pristine
  bytes. Patches are in `mutants.diff`; per-mutant sha256 in `mutants-results.json`.
- Detectors per mutant (frozen rule, verbatim): **killed iff selftest fails or a base/repair line differs from the frozen counter's.**
  1. `python3 -B <mutant> --selftest --work <scratch>` (public CLI fixtures, 14 declared).
  2. `python3 -B <mutant> --root LANE --revision 36d148f5… --work <scratch>` (base).
  3. `python3 -B <mutant> --root LANE --revision 9e27ce0b… --work <scratch>` (repair).
- Baseline (pristine) reproduced the controls before scoring: selftest `rc=0 selftest 14/14`; base `rc=1 mismatches=38 met=false`;
  repair `rc=0 mismatches=0 met=true`. Baseline was not inconclusive.
- Tools installed: none. Lane writes: none (counter reads committed bytes via `git show`/`ls-tree`/`rev-parse`, read-only).

## Results

| id | patch | killed_by | rc (selftest, base, repair) |
|---|---|---|---|
| M01-no-fence-skip | delete fence open/close handling | none | 0, 1, 0 |
| M02-no-comment-skip | delete HTML comment open/close handling | none | 0, 1, 0 |
| M03-no-entry-header-required | header-less tables fall back to column 1 | selftest+base+repair | 1, 1, 0 |
| M04-ids-from-entry-cell-only | id coverage checked against Entry cell only | base+repair | 0, 1, 1 |
| M05-no-range-expansion | delete S###-S### range expansion | base+repair | 0, 1, 1 |
| M06-min-words-8to1 | MIN_WORDS 8 -> 1 | none | 0, 1, 0 |
| M07-min-shared-2to0 | MIN_SHARED 2 -> 0 | selftest | 1, 1, 0 |
| M08-readme-from-worktree | README from working tree, not `git show REV:` | selftest+base | 1, 0, 0 |
| M09-no-empty-pop-exit2 | delete empty-population GitError | selftest | 1, 1, 0 |
| M10-dangling-not-counted | dangling excluded from mismatches | selftest | 1, 1, 0 |
| M11-unmet-exit-2 | unmet exit 1 -> 2 | selftest+base | 1, 2, 0 |
| M12-no-git-no-replace-objects | drop `GIT_NO_REPLACE_OBJECTS=1` pin | none | 0, 1, 0 |
| M13-git-from-path | `GIT = "/usr/bin/git"` -> `"git"` | none | 0, 1, 0 |
| M14-no-range-zero-padding | range expansion drops zero padding | base+repair | 0, 1, 1 |

**Score: killed=9/14. Survivors: M01, M02, M06, M12, M13.** Full rows in `mutants.tsv`.

## Survivor analysis (supplementary probes; scratch only; verdict unchanged)

`probe_survivors.py` builds fixture repos in scratch and runs pristine vs. mutant through the public CLI. These probes
explain *why* each survivor survived; they are not part of the frozen selftest and do not change the verdict.
Output in `probe-results.txt`.

- **M01 (no fence skip) — coverage gap.** The frozen selftest fixture `row-inside-fence` places the data row after a
  fence opener with no header. Without fence skipping that row is read as a *table header* (no `entry` cell), so it is
  dropped and the fixture still scores 1. Probe PR-M01a (same shape) does not kill it; probe **PR-M01b** (fenced block
  carrying its own `| Area | Entry | Coverage |` header and data row) does: pristine `mismatches=1 met=false`, mutant
  `mismatches=0 met=true` exit 0. The selftest does not discriminate fence handling.
- **M02 (no comment skip) — coverage gap, same mechanism.** `row-inside-comment` has no header; PR-M02a does not kill,
  **PR-M02b** (comment carrying its own header + data row) does: pristine `met=false` exit 1, mutant `met=true` exit 0.
- **M06 (MIN_WORDS 8->1) — coverage gap.** Frozen fixtures with ids but few words also lack ≥2 shared long words, so the
  shared-word conjunct catches them first. **PR-M06** (ids present, 5 other-cell words, two shared long words with the
  entry) kills it: pristine `met=false` exit 1, mutant `met=true` exit 0. The row-coverage conjunct is untested in isolation.
- **M12 (drop GIT_NO_REPLACE_OBJECTS pin) — coverage gap.** No frozen fixture carries a `git replace` ref. **PR-M12**
  (`git replace` on the README blob to a version indexing `b.md`) kills it: pristine `mismatches=1` exit 1, mutant
  `mismatches=0` exit 0. Note `git_env()` passes an explicit env dict, so the pin is the only guard. The lane itself
  carries no replace refs (base and repair lines are unchanged), so the lane run cannot see this class.
- **M13 (`"git"` instead of `/usr/bin/git`) — equivalent mutant under the frozen environment.** `git_env()` pins
  `PATH=/usr/bin:/bin` for the child, so a bare `git` resolves to `/usr/bin/git` regardless. Probe PR-M13 put a
  `git` wrapper that logs its own execution first on the parent PATH: pristine and mutant both returned the identical
  line (`met=true` exit 0) and the wrapper **did not fire** (`shadow_fired=False`). The child-env PATH pin is the
  operative defense; the absolute path is belt-and-braces. A real shadowing hole would need the PATH pin removed too
  (a two-point mutant, outside the single-point protocol; not run).

## Observations (for the L1; not repairs)

1. The selftest's header-less fenced and commented fixtures pass M01/M02 by a parsing accident (the row becomes a
   header), not by discriminating fence/comment handling. A successor counter (not this round; the counter is frozen)
   would need header-bearing fenced/commented fixtures.
2. The MIN_WORDS 8 conjunct is not isolated by any frozen fixture; the MIN_SHARED conjunct is (M07 killed by selftest).
3. No frozen fixture covers `git replace` refs; the GIT_NO_REPLACE_OBJECTS pin is untested.
4. M08 kills at base because the lane working tree README equals the repair content (master = 9e27ce0b); the base
   revision therefore reads 84/84 from the worktree. Reported as observed, not as a counter defect.
5. The frozen `ctl-c1-forgery-fenced.txt` / `pathonly` receipts were NOT re-run by this seat (the committed fixture
   repos lived under the scratch tree that a sibling deleted; see the incident note in MutIndex.md). Re-running them is
   owed to whoever scores those controls.

## Incident disclosure

My scratch tree `/fast/scratch/hyaku/kake-r97/MutIndex` was deleted mid-run by a sibling's `rm -rf` of the round parent
(ConnectorScope-23 disclosed it). I recreated it, re-derived the pristine copy from the lane instrument (hash re-verified
`8535150e…` before use), rewrote the driver, and reran from scratch. No lane, sibling, or fleet bytes were affected by
me. The final run in this report is the post-recreation run.

## Restoration / cleanup

Scratch tree deleted before yield (see MutIndex.md). Lane tree: only `w1/MutIndex/` files added.
