# ReviewMirrorScope — the pre-append census argv is not a full-repo validation

Axes: operability, freshness.
Milestone: Round 49 v1 wave: attack the frozen order proof and crawl-budget quote truth.
Seat: reviewer. Leaf. No other file written. No `jj`. No fleet write. No commit.

## Verdict

**Not a full-repo validation.** The mirror claim that this census covered the fleet, or the live kake lane, does not survive the frozen argv. The narrower claim already written in `order-proof.json`, `LOG.md`, and `SCORECARD.md` — `--file` on that mirror only — matches the blob.

## Argv (pre revision, `git show` only)

Pre revision named by `order-proof.json`: `99fa9d3fcaafbdb6bb1a2518c21e27698199b4c9`.
`git merge-base --is-ancestor 99fa9d3fcaafbdb6bb1a2518c21e27698199b4c9 1c846ed2d67b1692ea966be064f0fc04542763c6` exited 0.
Blob at that path, at both revisions: `4fc2b0fafd0454947274456530a8d49ce70f2100` (178 bytes). Worktree `git status --porcelain` for the path was empty. The quote is not a dirty-tree read.

Command:

```
git show 99fa9d3fcaafbdb6bb1a2518c21e27698199b4c9:.ufo/waves/round-49/assimilation/pre-append/census-argv.txt
```

Argv, one line, trailing newline:

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-49/assimilation/pre-append/corpus/SOURCES.md
```

The string contains `validate` and `--file` and the pre-append `SOURCES.md` path. It does not contain `--root`. It does not name the lane `kake`. It names no other registry.

## Why that is not full-repo

`scripts/sources-census.sh` header (lines 10–15): default targets are child repositories from the conf; `repo "."` is excluded; `--file` or an explicit directory is how you pick one registry.

`resolve_targets` (lines 495–503) returns immediately when `FILE` is set. It does not call `build_roster`. The emitted lane token is the literal `file`. The used-by directory is `dirname(file)/..`, which for this path is `.../assimilation/pre-append`, not the live lane root and not the fleet root. E11 therefore cannot see a missing live `corpus/` path that the mirror happens to contain.

Same pre revision, stdout last line (`git show 99fa9d3:.../census-stdout.txt`):

```
file	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-49/assimilation/pre-append/corpus/SOURCES.md
```

Lane column is `file`, not `kake`, not `FLEET`. Exit blob is `0\n`. A roster `validate` would emit one row per child lane. A lane command is `validate --root <fleet> kake` and would ok `kake-shokunin/corpus/SOURCES.md`. Neither string is this argv.

Round 48's "gated on a full-repo mirror" sentence (`LOG.md` round-48 assimilation; `corpus/lessons/round-48.md` mistake 3) is a different artifact. Spot-check defect 3 already forbids calling that mirror full-repo. It must not be read onto this blob.

## What the attack does not break

The disclaimer in `assimilation/order-proof.json` ("validate --file on that mirror only. It is not a full-repo validation"), `LOG.md` round 49 ("The mirror is not a full-repo validation"), and `SCORECARD.md` round 49 holds against this argv.

`c49_order.py` check 5 requires `--file` and `pre-append/corpus/SOURCES.md` and rejects `--root`. This blob passes that check. Do not treat the returned field `fullRepoValidation: False` (`c49_order.py` return dict) as the evidence: that boolean is a constant, not a measurement. The argv blob is the evidence. Absence of `--root` alone would not prove "not full-repo" — a bare `validate` is the roster walk and also lacks `--root`. The positive `--file` plus the single mirror path is what settles it.

## Axis read

- **Operability:** exit 0 on this argv does not license a fleet census or a live-lane census. It licenses one mirror file, with used-by resolved inside the pre-append tree.
- **Freshness:** the quote is the ancestor blob `4fc2b0fafd0454947274456530a8d49ce70f2100`, identical at the measured revision `1c846ed2d67b1692ea966be064f0fc04542763c6`. A later worktree edit of `census-argv.txt` would not move this reading.

Report: .ufo/waves/round-49/w1/ReviewMirrorScope.md
