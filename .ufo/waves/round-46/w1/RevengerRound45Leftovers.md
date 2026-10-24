# Seat report — kake-r46 / RevengerRound45Leftovers

**Item**: sweep for round-45 leftovers (untracked/uncommitted files, stray `__pycache__` under `.ufo/waves/round-45/`, files newer than r45 tip outside `.ufo/waves/round-46/`, seat reports missing from `w1|w2` against their registries). Delete nothing. Deliver `.ufo/waves/round-46/build/r45-leftovers.md`.

**Axes** (godspeed): operability, freshness. **Tools installed/updated**: none (none needed).

**Result: PASS** — sweep executed on all four probes; exactly one true leftover found (stale gitignored `__pycache__`); zero missing seat reports; zero uncommitted r45 bytes.

## Commands + decisive output (verbatim)

Baseline: r45 tip `7cdbaefd3ecbbc8814eca1f013fcee101a6157b0` (committer epoch `1792816643`, 2026-10-24T01:37:23-03:00), tree at HEAD `ded938d2`.

1. Untracked/uncommitted:
```
$ git status --porcelain=v1 --untracked-files=all
?? .ufo/waves/round-46/w1/swarm-registry.json
```
Only the live round-46 harness registry — not an r45 leftover.

2. Stray pycache — **FINDING**:
```
.ufo/waves/round-45/__pycache__/
  c45_audit.cpython-314.pyc     (mtime 2026-10-24 01:01:38)
  c45_count.cpython-314.pyc     (mtime 2026-10-24 00:39:36)
  c45_freshness.cpython-314.pyc (mtime 2026-10-24 00:59:29)
$ git check-ignore -v …
.gitignore:2:__pycache__/	.ufo/waves/round-45/__pycache__/c45_audit.cpython-314.pyc
$ git ls-files .ufo/waves/round-45/__pycache__/   → (nothing tracked)
```
Stale r45 byproduct, invisible to `git status` (ignored), untracked, all mtimes pre-date the r45 tip. Not deleted (bounds); flagged to L1.

3. Files newer than r45 tip, outside `.ufo/waves/round-46/`:
```
$ find . -path ./.git -prune -o -path ./.ufo/waves/round-46 -prune -o -type f -newermt "@1792816643" … | grep -v '^\./\.jj/'
./LOG.md                       2026-10-24 01:45:59
./corpus/lessons/round-46.md   2026-10-24 01:45:59
./SCORECARD.md                 2026-10-24 01:45:59
$ git log -1 --format='%h %s' -- <each>   → bd86ee8 round-46: freeze claims (…)
$ git status --porcelain -- <each>        → (clean)
```
All three are round-46 freeze writes, committed at `bd86ee8` — classified, not stray. Remaining newer entries are only `.jj/` VCS internals.

4. Registries vs reports:
```
[w1] registry=32 reports=32   missing reports: NONE   orphan reports: NONE
[w2] registry=32 reports=32   missing reports: NONE   orphan reports: NONE
```
Registries: `.ufo/waves/round-45/w1|w2/swarm-registry.json`; diff via python3 (`json` members vs `*.md` in each wave dir).

## Files written
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-46/build/r45-leftovers.md` (deliverable)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-46/w1/RevengerRound45Leftovers.md` (this report)

## Blockers / dependencies
None. Scratch created and unused: `/fast/scratch/hyaku/kake-r46/RevengerRound45Leftovers/`. Nothing deleted; no commits made.
