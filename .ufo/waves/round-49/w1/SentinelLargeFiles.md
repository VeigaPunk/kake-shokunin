# Sentinel — large untracked copies (round-49, wave 1)

- seat: SentinelLargeFiles · role: sentinel · axes: operability, freshness
- lane: `/home/vgpnk/Projects/shokunin/kake-shokunin` · HEAD `1c846ed2d67b1692ea966be064f0fc04542763c6`
- measured: 2026-10-24T21:38:39-03:00
- bound: this seat wrote only this report. No `git add`, no `git commit`, no `jj`. The seventeen paths below were not staged and were not modified.

## Verdict

Still untracked. Nine `>1MiB` copies under `.ufo/waves/round-48/assimilation/validate/` and eight residual reports under `.ufo/waves/round-46/residual/` are absent from the index and from `HEAD`. Porcelain for those paths is seventeen `??` lines and nothing else. They were not added.

Severity for the frozen score: informational. These bytes are not an input to C1 or C2. Severity for a later sweep: low — they are not ignored, so a pathspec `git add` of a parent would stage them. That add was not run.

## Porcelain

Command: `git status --porcelain --` plus the seventeen paths. Exit 0. `git diff --cached --name-status --` on `.ufo/waves/round-46/residual` and `.ufo/waves/round-48/assimilation/validate` printed nothing (exit 0).

```
?? .ufo/waves/round-46/residual/CriticCitationOverreach.md
?? .ufo/waves/round-46/residual/CriticMatrixBlindness.md
?? .ufo/waves/round-46/residual/MutationSemanticsGap.md
?? .ufo/waves/round-46/residual/ReviewQualityCriterion.md
?? .ufo/waves/round-46/residual/ReviewReceiptIdentity.md
?? .ufo/waves/round-46/residual/ReviewWitnessOracle.md
?? .ufo/waves/round-46/residual/ScoutSiblingOverlap.md
?? .ufo/waves/round-46/residual/SentinelBounds.md
?? .ufo/waves/round-48/assimilation/validate/.ufo/waves/round-21/anchors-fixed.json
?? .ufo/waves/round-48/assimilation/validate/.ufo/waves/round-36/realrun/snap-bodies-run2.tar.xz
?? .ufo/waves/round-48/assimilation/validate/.ufo/waves/round-36/realrun/snap-bodies.tar.xz
?? .ufo/waves/round-48/assimilation/validate/.ufo/waves/round-37/sealed/cases.json
?? .ufo/waves/round-48/assimilation/validate/.ufo/waves/round-39/sources/xmlschema11-2.html
?? .ufo/waves/round-48/assimilation/validate/.ufo/waves/round-40/sources/xmlschema11-2.html
?? .ufo/waves/round-48/assimilation/validate/.ufo/waves/round-41/realrun/sitemaps/nodejs.xml
?? .ufo/waves/round-48/assimilation/validate/.ufo/waves/round-41/realrun/sitemaps/postgresql.xml
?? .ufo/waves/round-48/assimilation/validate/.ufo/waves/round-42/controls/w1/CtlCache/ctl_accept_table_seed4242.py
```

`??` is untracked, not staged. A staged add would have been `A `, not `??`.

## Counts, re-measured

Threshold: a file is `>1MiB` when its size is greater than 1048576 bytes.

| set | count | in index | in HEAD | notes |
|---|---|---|---|---|
| validate copies `>1MiB` | 9 | 0 | 0 | sum 19325862 bytes; smallest 1283159 |
| residual reports | 8 | 0 | 0 | regular files, 1335–18737 bytes; mtimes 2026-10-24 03:26–03:37 -0300 |

`find .ufo/waves/round-48/assimilation/validate -type f -size +1048575c` returned exactly those nine. `find .ufo/waves/round-46/residual -type f` returned exactly those eight; no subdirectory. `git status --porcelain --untracked-files=all` on each parent returned the same 9 and 8 lines. `git ls-files` on the seventeen paths printed nothing. `git cat-file -e HEAD:<path>` was absent for all seventeen. `git check-ignore -v` printed nothing: they are untracked because they were never added, not because an ignore rule hides them.

Each copy is a regular file, mode 644, not a symlink. `cmp -s` against the path with `.ufo/waves/round-48/assimilation/validate/` stripped was identical for all nine. Each twin is tracked (`git ls-files -v` flag `H`). Adding the copies would duplicate blobs already in history. It would not create a second source of truth.

## Attack on the frozen score

Mutating or adding these worktree copies cannot move C1 or C2 at `1c846ed2d67b1692ea966be064f0fc04542763c6`.

- Both counters are clean against HEAD (`git diff --quiet HEAD --` the two scripts, exit 0).
- Reads are `git show <revision>:<path>` (`c49_order.py` `git_show`, `c49_quote_truth.py` `git_show`). The only `open(` in either committed script is the optional `--json` writer, not a read of retained text or of these copies.
- `git grep` of HEAD copies of both counters for `round-46/residual`, `anchors-fixed.json`, `snap-bodies`, `xmlschema11-2`, `ctl_accept_table_seed4242`, `postgresql.xml`, `nodejs.xml`, and `sealed/cases.json` returned no hits.

So a dirty edit of an untracked copy is invisible to the frozen counters. Leaving the copies untracked is the state that keeps them out of a later commit. The failure mode that would put them in history is a later `git add` of a parent path: they are not ignored, and directory-track's 1MiB skip is not a git ignore. This seat did not run that add. The 1MiB skip itself was not re-measured here; running `jj` is outside this seat's bound. The untracked status was.

## Impact

No index change. No new blob. The frozen order proof and the crawl-budget quote check still see only committed paths, and these seventeen paths are not among them. The residual reports stay orchestrator-owned and uncommitted. The nine copies stay duplicate worktree files, byte-identical to tracked twins.

## Smallest remediation

Do not add them. Any later lane commit must exclude these seventeen paths. Do not force-add them to beat a size skip. This seat's remediation is the non-action: they were left untracked.

Report: .ufo/waves/round-49/w1/SentinelLargeFiles.md
