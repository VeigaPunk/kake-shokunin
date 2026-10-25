# ExecRerunC1 — C1 counting command re-run

Seat: executor. Axes: operability, freshness.
Milestone: Round 49 v1 wave: attack the frozen order proof and crawl-budget quote truth.
Bound: counter not edited. Only this report written. No `--json`. No checkout.

## Command

Frozen counting command (`.ufo/waves/round-49/contract.json`):

```
python3 -B .ufo/waves/round-49/c49_order.py --root . --revision <commit>
```

Run from `/home/vgpnk/Projects/shokunin/kake-shokunin` at 2026-10-24 21:37:43 -0300.
Worktree `c49_order.py` matches `1c846ed2` (`git diff --exit-code 1c846ed2 -- .ufo/waves/round-49/c49_order.py` exit 0). Blob `7ca940160ed4b0729e5cf110ca00b5acd807ab58`. After both runs, `git status --porcelain -- .ufo/waves/round-49/c49_order.py` was empty.

## At 1c846ed2

Resolved: `1c846ed2d67b1692ea966be064f0fc04542763c6`

stdout:

```
C1 order 1/1 met=True
```

exit code: **0**
stderr: 0 bytes

## At base 090ce8f1

Resolved: `090ce8f1cfbae2dfb8bfa65dedd2c72861c48166`

stdout:

```
C1 order 0/1 met=False
  FAIL proof absent
  FAIL quote counter absent at measured revision
```

exit code: **1**
stderr: 0 bytes

## What the two runs show

The do-nothing control does not meet `met: order == 1 of 1`. The measured revision does. A second separated run printed the same stdout and the same exit codes.

Base has neither the counter nor the proof (`git cat-file -e 090ce8f1:.ufo/waves/round-49/c49_order.py` and `.../assimilation/order-proof.json` both exit 128). The command still used the worktree counter with `--revision 090ce8f1`, which is the frozen do-nothing form. The counter file at that revision was not executed, because it is absent.
