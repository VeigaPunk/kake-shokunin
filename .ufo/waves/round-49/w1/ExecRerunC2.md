# ExecRerunC2

Re-ran the frozen C2 counting command at `1c846ed2` and at base `090ce8f1`. Did not edit the counter. Did not pass `--json`. Score is this run's stdout, not `verification/c2-*.json`.

Predicate: `met: passed >= 2 of 2 declared ids`.
Contract exits: `0` met, `1` not met, `2` could-not-evaluate, `64` usage.

## Counter identity

- cwd: lane root
- command form: `python3 -B .ufo/waves/round-49/c49_quote_truth.py --root . --revision <commit>`
- HEAD: `1c846ed2d67b1692ea966be064f0fc04542763c6`
- script blob `HEAD:.ufo/waves/round-49/c49_quote_truth.py`: `0808c865234a4a2bc95905622871807c5c77ee1d`
- worktree sha256: `f9be4761aca237b8e94e13095357dbe768922ab3a3a2e9ea974ba5b36926fc8f`
- `git status --porcelain -- .ufo/waves/round-49/c49_quote_truth.py`: empty
- ran at: `2026-10-25T00:37:12Z`

## At 1c846ed2

Resolves to `1c846ed2d67b1692ea966be064f0fc04542763c6`.

```
python3 -B .ufo/waves/round-49/c49_quote_truth.py --root . --revision 1c846ed2
```

exit: `0`
stderr: empty

stdout:

```
C2 passed 2/2 met=True
  ok S273: all rules hold
  ok S274: all rules hold
```

## At base 090ce8f1

Resolves to `090ce8f1cfbae2dfb8bfa65dedd2c72861c48166`. Ancestor of HEAD (`git merge-base --is-ancestor` exit `0`).

```
python3 -B .ufo/waves/round-49/c49_quote_truth.py --root . --revision 090ce8f1
```

exit: `1`
stderr: empty

stdout:

```
C2 passed 0/2 met=False
  FAIL S273: no source receipt file at this revision, no registry row, entry file absent, no gate quote
  FAIL S274: no source receipt file at this revision, no registry row, entry file absent, no gate quote
```

## Reading

Both runs evaluated. `1c846ed2` meets the predicate (2/2, exit 0). Base `090ce8f1` does not (0/2, exit 1). The do-nothing control is not already at the target.

---
seat: ExecRerunC2
axes: operability, freshness
milestone: Round 49 v1 wave: attack the frozen order proof and crawl-budget quote truth
report: .ufo/waves/round-49/w1/ExecRerunC2.md
