# SentinelScope — round-44 worktree scope audit

Axes: **operability** (scope cleanliness) and **freshness/provenance** (round boundary and frozen hashes).

## Result

- **Scope attack: FAIL.** The worktree contains one untracked path outside round 44: `.ufo/waves/round-43/w1/CtlPrefixCache.md`. Its contents identify it as the `kake-r43-w1-CtlPrefixCache` report, with round-43 evidence. This is not round-44 work. No change was made to it.
- The other compact-status entries are `SCORECARD.md`, `.ufo/waves/round-44/`, `corpus/lessons/round-44.md`, and `scripts/ledger_latest_check.py`. The scoreboard diff begins with “Round 44 — C1 and C2 declared”; the checker is named by C2; the remaining paths are explicitly under the round-44 tree or named round-44 lesson. They are consistent with round-44 work. Authorship is inferred from these paths/context; status alone does not establish author identity.
- **Frozen hash attack: PASS** for all three expected hashes. G6 source hash is recorded below. The initial G6 lookup at repo-root `classes/g6_fold_pairs.py` failed because that path does not exist; the wave's actual file is `.ufo/waves/round-44/classes/g6_fold_pairs.py`.

## Exact commands and decisive output

```text
$ git status --porcelain
 M SCORECARD.md
?? .ufo/waves/round-43/w1/CtlPrefixCache.md
?? .ufo/waves/round-44/
?? corpus/lessons/round-44.md
?? scripts/ledger_latest_check.py
```

Additional commands used for classification and required scratch setup:

```text
$ git status --porcelain --untracked-files=all
[expanded the round-44 directory; the non-round-44 status entry is shown above]

$ git diff -- SCORECARD.md
w/SCORECARD.md | 183 +++++++++++++++++++++++
1 file changed, 183 insertions(+), 0 deletions(-)
+## Round 44 — C1 and C2 declared (frozen before any claim receipt is produced)

$ sha256sum .ufo/waves/round-44/classes/g6_fold_pairs.py && mkdir -p /fast/scratch/hyaku/kake-r44/SentinelScope
f4f13a7682ad27117e398f8b987aab68c92f34ccfa82813c0dd3636b8d2a536d  .ufo/waves/round-44/classes/g6_fold_pairs.py
```

`git status --porcelain --untracked-files=all`'s complete output was the expanded inventory used for classification.
Expanded inventory command: `git status --porcelain --untracked-files=all`. It expanded the `round-44/` directory into its untracked files; the sole expanded path outside that directory was the round-43 report above. The report contents identify its provenance:

```text
8:Seat kake-r43-w1-CtlPrefixCache. Base `scripts/sitemap_audit.py` @020bc457 (sha `914ebdee…`),
9:counter `c43_count_v4.py` sha `1c3b9661…`. Command (no --seed; os.urandom seed in receipt):
```

Hash command and output:

```text
$ sha256sum .ufo/waves/round-44/c44_count_v5.py .ufo/waves/round-44/c44_placebo.py .ufo/waves/round-44/c44_audit.py classes/g6_fold_pairs.py
5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc  .ufo/waves/round-44/c44_count_v5.py
9ce3acd4c4c72de0b3c26a31bd1101307b71b2174100eb260b8b04fa5fc77a27  .ufo/waves/round-44/c44_placebo.py
8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75  .ufo/waves/round-44/c44_audit.py
sha256sum: classes/g6_fold_pairs.py: No such file or directory (os error 2)

$ sha256sum .ufo/waves/round-44/classes/g6_fold_pairs.py
f4f13a7682ad27117e398f8b987aab68c92f34ccfa82813c0dd3636b8d2a536d  .ufo/waves/round-44/classes/g6_fold_pairs.py
```

## Files written / checks

- Wrote only `.ufo/waves/round-44/w2/SentinelScope.md`; created the required empty scratch directory `/fast/scratch/hyaku/kake-r44/SentinelScope/`.
- `git status` scope checks: **FAIL** due to the out-of-round report above. Frozen artifact hashes: **PASS** (all expected hashes match). G6 hash observed: `f4f13a7682ad27117e398f8b987aab68c92f34ccfa82813c0dd3636b8d2a536d`.
- Smallest remediation: lane owner should resolve the provenance/scope of `.ufo/waves/round-43/w1/CtlPrefixCache.md` (remove it from this worktree if unrelated). I did not modify it. No tests or other checks were run.
