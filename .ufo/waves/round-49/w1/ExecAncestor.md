# ExecAncestor — round 49 w1

Axes: operability, freshness.
Milestone: Round 49 v1 wave: attack the frozen order proof and crawl-budget quote truth.
Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`. Commands below were re-run in that repo this turn. No production file was edited. No `jj`. No fleet write.

## Ancestor check

```
git merge-base --is-ancestor 99fa9d3fcaafbdb6bb1a2518c21e27698199b4c9 1c846ed2d67b1692ea966be064f0fc04542763c6
```

Stdout empty. **Exit code: 0.**

Both names resolve to themselves (`git rev-parse --verify`). They are not the same commit (`sort -u | wc -l` → `2`), so the relation is strict, not the self-ancestor case.

Caveat, not a failure of this pair: `git merge-base --is-ancestor 99fa9d3fcaafbdb6bb1a2518c21e27698199b4c9 99fa9d3fcaafbdb6bb1a2518c21e27698199b4c9` also exits 0. Exit 0 alone does not prove a *strict* ancestor. `c49_order.py` adds `pre_rev == revision` before it treats exit 0 as strict. That extra guard holds here because the two hashes differ.

Subjects, for identity only:

- `99fa9d3fcaafbdb6bb1a2518c21e27698199b4c9` — `round-49: freeze counters and commit the pre-append census mirror` (2026-10-24 21:33:46 -0300)
- `1c846ed2d67b1692ea966be064f0fc04542763c6` — `round-49: append crawl-budget rows after the pre-append mirror` (2026-10-24 21:34:41 -0300)

`git log --oneline 99fa9d3fcaafbdb6bb1a2518c21e27698199b4c9..1c846ed2d67b1692ea966be064f0fc04542763c6` prints only the scored commit. Worktree `HEAD` is `1c846ed2d67b1692ea966be064f0fc04542763c6`.

## Live `SOURCES.md` at the pre revision lacks S273

"Live" here is the committed blob `99fa9d3fcaafbdb6bb1a2518c21e27698199b4c9:corpus/SOURCES.md`, the path `c49_order.py` reads with `git show`. It is not the worktree file and not the pre-append mirror.

- `git cat-file -t` → `blob`
- object id `cc6806d0cb39a66706ede871bd6174661137d932` (git id, not sha256)
- `git show 99fa9d3fcaafbdb6bb1a2518c21e27698199b4c9:corpus/SOURCES.md | sha256sum` → `7a4b75ccdda39207288bb04795b8176d8552496d44c050f19ab286d7b2acdb93`
- 253 lines, 132132 bytes
- substring `S273` count: **0**
- `grep -F -c -e S273` printed `0` and exited **1** (`PIPESTATUS` git=0, grep=1)
- no line contains `S273`
- registry heading `## Registry` at line 5; 140 registry rows; last id `S249` at line 148

Same blob also has substring `S274` count 0. That is the same scan, not a separate claim.

## What would give the opposite answer

These are not the live pre-revision file. Citing them as "lacks S273" would be false.

- Pre-append mirror at the same revision, `99fa9d3fcaafbdb6bb1a2518c21e27698199b4c9:.ufo/waves/round-49/assimilation/pre-append/corpus/SOURCES.md`: `grep -F -c -e S273` printed `1`, exit 0.
- Worktree `corpus/SOURCES.md` (HEAD is the scored commit): `grep -F -c -e S273` printed `1`, exit 0.
- Scored live blob `1c846ed2d67b1692ea966be064f0fc04542763c6:corpus/SOURCES.md`: substring count 1, registry row at line 149.

## Attack result

Condition 2 (pre_rev is an ancestor; hashes differ so it is strict) and condition 3 for S273 (no live registry row, and no substring at all) hold on re-execution. This pair does not falsify the frozen order proof. The check is only sound if the reader uses `git show <pre_rev>:corpus/SOURCES.md`. A worktree open or a mirror open finds S273 and would invert the absence claim.

Report: `.ufo/waves/round-49/w1/ExecAncestor.md`
