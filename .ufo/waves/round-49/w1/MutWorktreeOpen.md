# MutWorktreeOpen — one-line reintroduction of the round-48 worktree read

Seat: mutation-tester. Not applied. Lane counters were not edited.

Axes: operability, freshness.

## Mutation (one line, not applied)

In `.ufo/waves/round-49/c49_quote_truth.py` line 174, replace the committed-byte read

```python
            blob = git_show(root, revision, rel)
```

with the worktree open

```python
            blob = open(os.path.join(root, rel), "rb").read()
```

`rel` is already `.ufo/waves/round-49/sources/{textPath}` (line 173). That is the same path round 48 built and opened:

```python
path = os.path.join(root, os.path.dirname(RECEIPTS), receipt["textPath"])
with open(path, "rb") as fh:
```

at `.ufo/waves/round-48/c48_quote_truth.py:205` and `:207` (`RECEIPTS` dirname is `.ufo/waves/round-48/sources` there; the round-49 equivalent is the `rel` above). A dirty worktree file at that path can change the R4 sha256 and substring result. The rest of R4 still consumes `blob`.

Live blob at `1c846ed2d67b1692ea966be064f0fc04542763c6` does not contain `os.path.join(root`. Worktree `git hash-object` of `.ufo/waves/round-49/c49_quote_truth.py` equals that revision's blob `0808c865234a4a2bc95905622871807c5c77ee1d`. Same for `.ufo/waves/round-49/c49_order.py` (`7ca940160ed4b0729e5cf110ca00b5acd807ab58`).

## Check that rejects that blob

`.ufo/waves/round-49/c49_order.py:167-175`. The quote-counter blob is `git show <measured>:.ufo/waves/round-49/c49_quote_truth.py`, not the worktree file. The rejecting arm is:

```python
        if "os.path.join(root" in source:
            reasons.append("quote counter still joins a worktree path")
```

Any reason forces `order = 0` at line 176, so C1 is not met (exit 1). The mutant still contains `COMMITTED_BYTES_ONLY` and `git show` (docstring and `git_show()`), so the sibling arm at lines 172-173 does not fire. A worktree-only edit of the counter is invisible at `1c846ed2`; the check rejects the blob only when `git show` returns the mutated line.

## Scratch execution (lane untouched)

Scratch repo, deleted after the run. Clean commit held the `1c846ed2` quote-counter blob. Mutant commit held only the one-line swap. Neither commit had `order-proof.json`, so both fail the proof arm; only the mutant adds the join arm.

```
python3 -B .ufo/waves/round-49/c49_order.py --root <scratch> --revision c44a9123d7b086063789e9872b09c0ded60dd3c4
C1 order 0/1 met=False
  FAIL proof absent
exit=1

python3 -B .ufo/waves/round-49/c49_order.py --root <scratch> --revision 9296a0da75f5ae79f974c7f451b9a0f1617be9ad
C1 order 0/1 met=False
  FAIL proof absent
  FAIL quote counter still joins a worktree path
exit=1
```

After the run, lane `git hash-object .ufo/waves/round-49/c49_quote_truth.py` was still `0808c865234a4a2bc95905622871807c5c77ee1d`, and `git status --porcelain` on both counters was empty.

## Coverage limit

The arm is a source-text needle, not a behavioral ban on opening `root`. A one-line read that avoids the spelling `os.path.join(root` — for example `blob = open(f"{root}/{rel}", "rb").read()` — reintroduces the same dirty-tree score move and this check would not add `quote counter still joins a worktree path`. That bypass was not applied either. The assigned mutant is the round-48 spelling, and that blob is rejected.

Report: .ufo/waves/round-49/w1/MutWorktreeOpen.md
