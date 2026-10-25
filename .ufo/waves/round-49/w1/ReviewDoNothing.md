# ReviewDoNothing — base control vs frozen targets

**Seat:** ReviewDoNothing (reviewer)
**Axes:** operability, freshness
**Milestone:** Round 49 v1 wave: attack the frozen order proof and crawl-budget quote truth
**Control revision:** `090ce8f1cfbae2dfb8bfa65dedd2c72861c48166`
**Receipt commit:** `1c846ed2d67b1692ea966be064f0fc04542763c6` (the receipts are not in the base tree)

Frozen targets, from the receipt `predicate` fields and `c49_order.py` / the wave spec:

- C1 operability: `met: order == 1 of 1`
- C2 freshness: `met: passed >= 2 of 2 declared ids` (S273, S274)

Rule applied: a control that meets the target is a bad counter. This control does not meet either target.

## Verdict

Not a bad counter. Base C1 is order 0. Base C2 is 0/2. Both `met` fields are false. A live re-run at the base revision exits 1 for both counters and its `--json` bytes match the committed before receipts.

The same counters at the treatment revision `1c846ed2d67b1692ea966be064f0fc04542763c6` do meet both targets (exit 0). That pass is the treatment, not the control. It shows the base miss is discrimination, not a counter stuck at fail.

## Before receipts

Only two before files exist under `.ufo/waves/round-49/verification/`. Both are committed at `1c846ed2` and byte-identical to the worktree (`git show <rev>:<path> | cmp - <worktree>` printed nothing, then `C1_BLOB_MATCH` / `C2_BLOB_MATCH`). `git ls-tree -r 090ce8f1 .ufo/waves/round-49/verification` printed no paths (`BASE_LS_EXIT:0`).

| Receipt | Blob at `1c846ed2` | sha256 | Score |
|---|---|---|---|
| `.ufo/waves/round-49/verification/c1-before-090ce8f1.json` | `dcf23dbb017b7414d2cec4bd23a61384a48e51bc` | `fa2360ac8c30612fbb4debb447e25fddadaa08e0d05af584f6577c54a51d0148` | `order` 0, `total` 1, `met` false |
| `.ufo/waves/round-49/verification/c2-before-090ce8f1.json` | `62f94c8de71d2a79ae13c50768cee1283bb69d4f` | `aabd263348670c6020f7eb9ec2bf15d5cf9216a5b2e7c0ef8023cdc4c2b23003` | `passed` 0, `total` 2, `met` false |

C1 reasons in the receipt: `proof absent`; `quote counter absent at measured revision`. `pre_rev` is null. `revision` is the base hash.

C2 detail: S273 and S274 each `ok: false`, `quote: null`, reasons `no source receipt file at this revision`, `no registry row`, `entry file absent`, `no gate quote`.

0 is not 1, so C1 does not meet `order == 1 of 1`. 0 is not >= 2, so C2 does not meet `passed >= 2 of 2`.

## Live re-run (read-only; `--json` went to `/tmp`, not the lane)

```
python3 -B .ufo/waves/round-49/c49_order.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 090ce8f1cfbae2dfb8bfa65dedd2c72861c48166
C1 order 0/1 met=False
  FAIL proof absent
  FAIL quote counter absent at measured revision
C1_EXIT:1

python3 -B .ufo/waves/round-49/c49_quote_truth.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 090ce8f1cfbae2dfb8bfa65dedd2c72861c48166
C2 passed 0/2 met=False
  FAIL S273: no source receipt file at this revision, no registry row, entry file absent, no gate quote
  FAIL S274: no source receipt file at this revision, no registry row, entry file absent, no gate quote
C2_EXIT:1
```

`cmp` of those `--json` files against the two before receipts printed `C1_RECEIPT_EQ_RERUN` and `C2_RECEIPT_EQ_RERUN`. The receipts are the counter's own output, not a hand-edited fail.

Absence at the base revision (`git cat-file -e`, exit 128 each): `.ufo/waves/round-49/assimilation/order-proof.json`, `.ufo/waves/round-49/c49_quote_truth.py`, `.ufo/waves/round-49/c49_order.py`. The fail is missing round artifacts, which is the do-nothing condition. `c49_order.py` documents that a missing proof is order 0, not a usage error (exit 2). Exit 1 is the not-met exit.

Contrast, not the control:

```
C1 order 1/1 met=True
C1_TIP_EXIT:0
C2 passed 2/2 met=True
C2_TIP_EXIT:0
```

at `--revision 1c846ed2d67b1692ea966be064f0fc04542763c6`.

## Attack

No false green on the control. Scoring `order` / `passed` / `met` / the process exit keeps the control on the fail side of both targets.

Two reading hazards, neither of which makes this control meet the target:

1. Each failing receipt still contains the target sentence in `predicate` (`met: order == 1 of 1`, `met: passed >= 2 of 2 declared ids`). A judge that greps verification JSON for that sentence would call this control met. That judge would be a bad counter. The counters themselves are not: they set `order` 0 and `passed` 0 and exit 1.
2. The worktree also has untracked `.ufo/waves/round-49/verification/c1-after-1c846ed2.json` and `c2-after-1c846ed2.json` (`git status --porcelain` showed `??` for both; `git ls-tree -r 1c846ed2 .ufo/waves/round-49/verification` lists only the two before blobs). Those after files are a treatment record. Do not score them as the do-nothing control. This seat did not use them for the base confirmation.

Operability: the negative control returns not-met, so the gates can fail. Freshness: the committed before receipts match a re-run in this seat; they are not a stale or worktree-only score. No axis harmed by treating this control as a valid fail.

Report: .ufo/waves/round-49/w1/ReviewDoNothing.md
