# ReviewDeclarationOrder — declaration-before-data check (round 32, wave 1)

Scope: verify that declaration commit 5b32cc7 precedes the before receipts and
the build, and that no counter file changed after the declaration. All commands
were read-only (`git log`/`diff`/`merge-base`) in the lane; no repo state mutated.

## Commands run (all exit 0)

1. `git -C <lane> log --format='%H %cI %s' a0b0dff..285abca`
   Output (newest first):
   - 285abcad632e3c1c57bb402232e7d218054db383 2026-10-22T15:55:47-03:00 "S062 recheck 90d (census E09 fix), after receipts at 2f2f12d"
   - 2f2f12deb0fe33d8fa7d9bd14c75d855f005f71a 2026-10-22T15:55:33-03:00 build (P6 spec+reason_contains, C2 retained blobs, S062, entry)
   - 5b32cc7c4f6494a92912df5a19f589f04f7160a8 2026-10-22T15:54:19-03:00 "declared claims C1 ... with counting commands, before measurement" (aI=15:50:53)
   Order: 5b32cc7 (declaration) -> 2f2f12d (build + before receipts) -> 285abca (tip).

2. `git -C <lane> diff 5b32cc7 285abca -- .ufo/waves/round-32/c1_m3_probe.py .ufo/waves/round-32/c2_retained_count.py`
   Empty output, exit 0: both counters byte-identical to the declaration commit.

3. `git -C <lane> log --format='COMMIT %H a=%aI c=%cI %s' --name-only a0b0dff..285abca`
   - 5b32cc7 added: c1_m3_probe.py, c2_retained_count.py, SCORECARD.md (declared claims).
   - 2f2f12d added: c1-before-a0b0dff.json, c2-before-a0b0dff.json (before receipts) plus the build files.
   - 285abca added: c1-after-2f2f12d.json, c2-after-2f2f12d.json, SOURCES.md recheck.
   Before receipts first appear only in the build commit, after the declaration.

4. `git -C <lane> merge-base --is-ancestor 5b32cc7 2f2f12d` = 0; `... 285abca` = 0.
   Declaration is a strict ancestor of build and tip (linear chain).

5. `git -C <lane> log --name-only -- <counter files>` (full history, no range bound):
   only 5b32cc7 ever touched either counter, so the unchanged-after-declaration
   result also holds through master tip 7e05aa8.

## Observation beyond the assigned tip (master = 7e05aa8, c=15:59:13)

Post-tip commit 7e05aa8 adds `.ufo/waves/round-32/declared_time_check.py` and
`verification/declared-time-check.txt`, whose receipt reads:
`stated 2026-10-22T18:58:00+00:00 commit 2026-10-22T18:54:19+00:00 /
violation: stated declaration time is later than the declaring commit / exit=1`.
The same commit appends a SCORECARD correction: the "Declared at 18:58Z" line in
5b32cc7 was estimated, not read; the commit was made at 18:54:19Z. 7e05aa8 does
not touch the counters or any receipt JSON (name-status: check script, receipt,
w1 spec/dispatch/registry, LOG.md, SCORECARD.md, QUALITY.md, lessons/round-32.md).

## Findings

- PASS (commit order): declaration 5b32cc7 (c=15:54:19-03:00) strictly precedes
  the build commit 2f2f12d (15:55:33) that contains both before receipts and the
  C1/C2 repair, and precedes tip 285abca (15:55:47) with the after receipts.
- PASS (counter immutability): diff 5b32cc7..285abca for both counters is empty;
  file history shows no later modification, including post-tip 7e05aa8.
- DEFECT (self-flagged, corrected): the declaration's own stated time "Declared
  at 18:58Z" postdates the declaring commit (18:54:19Z) — literally impossible;
  the L1's check fails on it (exit=1) and 7e05aa8 appends the correction. Git
  order is honest; the stated timestamp was not.
- Note: the before receipts measure base a0b0dff but were committed together with
  the repair in 2f2f12d, so "before measurement" is proven only by the counter
  output embedded in the receipts, not by commit-time separation from the build.
  The declaration still precedes both.

## Not verified

- Receipt content correctness (killed/met field values) — other seats' scope.
- Whether counter code was developed/tested against live data before being
  committed in 5b32cc7; git history cannot show pre-commit iteration.
- No tools installed; pacman pause irrelevant (no installs needed).
