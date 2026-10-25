# ExecCensusFile — re-run `validate --file` on the worktree pre-append mirror

Seat: executor (leaf). Axes: operability, freshness.
Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`. HEAD at re-run: `1c846ed2d67b1692ea966be064f0fc04542763c6`.
Clock: `2026-10-25T00:37:47Z` (`date -u`). No labrat. No production edit. No `jj`, no `git add`, no commit.

Report: .ufo/waves/round-49/w1/ExecCensusFile.md

## Required paste

Command, worktree path, not a `git show` blob:

```text
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-49/assimilation/pre-append/corpus/SOURCES.md
```

Exit code: **0**

Last line (tab-separated; `repr` = `'file\tok\t/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-49/assimilation/pre-append/corpus/SOURCES.md'`):

```text
file	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-49/assimilation/pre-append/corpus/SOURCES.md
```

**This is not a full-repo validation.**

## What the re-run actually printed

Two re-runs in this seat, both exit 0. The second stdout is byte-identical to the committed receipt `.ufo/waves/round-49/assimilation/pre-append/census-stdout.txt` (`cmp -s`; sha256 `35de84dad39539920ddf586f90bae81b696fab1ad1336aed4570fad2fa75efd4`). Stderr on the instrumented re-run was 0 bytes. 13 stdout lines: 12 `file\tW04\t… across scopes`, then the ok line. Zero `E` codes. One `ok` line. Lane column is the literal `file`, not `kake`.

Worktree mirror `git hash-object` = `4d9ca243e48593b9021d7851620363e9f682ad7d`, equal to both `HEAD:.ufo/waves/round-49/assimilation/pre-append/corpus/SOURCES.md` and `99fa9d3fcaafbdb6bb1a2518c21e27698199b4c9:.ufo/waves/round-49/assimilation/pre-append/corpus/SOURCES.md`. `git status --porcelain` on that path was empty. The re-run is the committed mirror bytes, not a dirty worktree drift. Raw sha256 of that file: `0a4aa38d098ef1e6a5ccd6b5c5d913673d7c25d7152c7a284975377e94811ceb` (133242 bytes). Live `corpus/SOURCES.md` is a different file (`46bb77e39229102ddc3c68a89c6a773f3e4629d3559b0372ced45f7d5724d3ad`, 133241 bytes).

## Why this is not a full-repo validation

`scripts/sources-census.sh` header (fleet script, read-only): default targets are child repositories; `--file` is "a specific registry." `resolve_targets` on a set `FILE` emits one TSV row `file<TAB><abs path><TAB><dirname>/..<TAB>` and returns. It does not call `build_roster`, does not read `shokunin.conf`, and does not emit a lane id. `FLEET` lines exist only in census mode. Validate prints findings, then one `ok` line per target that had no `E` code (`scripts/sources-census.sh` near the validate case: lane_errors from `E[0-9]+` only; W-codes do not set `findings`; header: exit 0 is clean or warnings).

used-by (`E11`) is checked under `dirname(SOURCES.md)/..`, which for this argv is `.ufo/waves/round-49/assimilation/pre-append/`, not the live lane root and not any sibling lane. `W04` here is the same URL in two scope cells of this one file (`url_seen` / `url_scopes` inside that file's awk pass), not a cross-lane shared-url scan.

`.ufo/waves/round-49/assimilation/order-proof.json` already says the same limit: "Mirror validation was sources-census.sh validate --file on that mirror only. It is not a full-repo validation." This re-run confirms that note. It does not widen it. This seat did not run `validate` with no `--file`, and did not run `validate --root /home/vgpnk/Projects/shokunin kake`. Those exits are not in this report.

## What exit 0 does not prove

Exit 0 means this one mirror file had no `E` code. It does not mean the fleet is clean, and it does not mean the live kake registry passed.

The passing mirror already contains an S273 row (worktree line 150). `git show 99fa9d3fcaafbdb6bb1a2518c21e27698199b4c9:corpus/SOURCES.md` has zero `S273` matches. So this ok line is not a census of the pre-append live registry. Citing it as "validate-before-append of `corpus/SOURCES.md`" would be a misread. The file that passed is the mirror named on the ok line.

## Bounds

Wrote only this file. Did not edit the census script, the mirror, `order-proof.json`, or any production path. Did not install tools.
