# ScoutMisrootPattern — fleet-root misroot sweep

## Finding
**Axis:** operability. **Attack outcome: FAIL (not reproduced).** The fleet working-tree status contained no fleet-root path named for `kake` or `r46`, and no apparent kake-r46 seat-note-style file at the fleet root. The sole status path containing `kake` was `.ufo/state/kake.report-baseline`, which is nested under `.ufo/state/`, not at the fleet root. No files were moved or otherwise changed by this sweep.

This establishes the observed working-tree filename result only; `git status` does not establish authorship of unrelated/generically named root files.

## Evidence
Command run in `/home/vgpnk/Projects/shokunin`:

```text
git status --porcelain
```

Verbatim decisive output:

```text
 M .ufo/state/chousa.report-baseline
 M .ufo/state/kagi.report-baseline
 M .ufo/state/kaidoku.report-baseline
 M .ufo/state/kake.report-baseline
 M .ufo/state/kama.report-baseline
 M .ufo/state/kengaku.report-baseline
 M .ufo/state/kumitate.report-baseline
 M .ufo/state/mado.report-baseline
 M .ufo/state/mori.report-baseline
 M .ufo/state/souji.report-baseline
 M .ufo/state/tameshi.report-baseline
 M .ufo/state/tsukuroi.report-baseline
 M .ufo/watchdog.log
 M SCORECARD.md
?? .omp/mcp.json
?? .ufo/state/kotoba.report-baseline
?? .ufo/state/kotodama.report-baseline
?? .ufo/state/revenger.report-baseline
?? .ufo/waves/hyaku/inline-run-20261023.md
?? AGENTS.md
?? bm.json
?? live.html
?? live_s228.html
?? nama.html
?? s395.txt
?? scripts/hyaku/append-closure.py.bak-20261023T040735Z
?? scripts/hyaku/fleet-commit.sh.bak-20261023T040735Z
?? tf_bavelas.html
?? unblob.log
?? wb2.html
?? write
?? xc.xml
```

## Files written
- `.ufo/waves/round-46/w1/ScoutMisrootPattern.md` (this report)

## Blockers
None for the requested working-tree filename sweep. No installation or verification checks were run.