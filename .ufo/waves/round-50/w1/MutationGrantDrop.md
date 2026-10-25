# MutationGrantDrop — C2 mutation test (round 50, wave 1)

Seat: leaf member (mutation-tester role), judged on operability.
Counter under test: `python3 -B .ufo/waves/round-50/c50_durable.py --root <repo> --revision <rev>`
Frozen predicate: `met: durable == 1 of 1`.

## Setup

Built a scratch git history in `/tmp/r50-mut/` (the lane is never mutated; `git clone` of the read-only lane). The lane's real commit layout maps onto the counter's revision model:

- `pre_rev` = `33eec7f2cecfdbb9c7a1f85c3d8efae8dacd7dd1` (pre-append mirror + census blobs committed; live registry has no S286).
- `grant_rev` = `89096c387622785af59312bd2ee3b169202f1d4e` (`wave-grant.txt`, `dispatch-command.txt` committed; LOG.md does not yet cite `r50-w1`).
- `measured` = a new commit that appends the S286 row to the live registry and lands `assimilation/order-proof.json`, `wave-cite-proof.json`, `settlement.json`, plus a LOG.md line citing `r50-w1` and the grant_rev hash.

For each mutant the grant/measured pair was rebuilt so only the named condition broke. Baseline (control) first verified MET so a rejection is attributable to the mutant, not the harness.

## Control (baseline) — MET

```
C2 durable 1/1 met=True
EXIT:0
```

Measured rev `1c8d5767978aac44204c076e0502b59fe7789feb` — all 11 counter conditions hold.

## Mutant 1 — wave-grant.txt absent at grant_rev

grant_rev rebuilt without `.ufo/waves/round-50/wave-grant.txt`; measured rev `ffbcaa8f3307f93cf269fdea4e87ce6137614cbc`.

```
C2 durable 0/1 met=False
  FAIL wave-grant stdout absent at grant_rev
EXIT:1
```

Rejecting condition: counter §8 — `git show <grant_rev>:wave-grant.txt` returns nothing (`grant is None`), so the grant stdout is absent. The exact-once `granted … seats=N` line can never be read.

## Mutant 2 — dispatch-command.txt contains `--auto` at grant_rev

grant_rev rebuilt with `kimi -m <MODEL> --auto --prompt …` in `dispatch-command.txt`; measured rev `f161ad6554da23bf691f9e92ea2967d3bce348c2`.

```
C2 durable 0/1 met=False
  FAIL dispatch command contains --auto
EXIT:1
```

Rejecting condition: counter §9 — the `kimi … --prompt` transport is still present (that sub-check passes), but the literal `--auto` flag is found in the dispatch blob and is forbidden.

## Mutant 3 — LOG.md cites the wave before the grant commit

grant_rev rebuilt with a premature `r50-w1` line already in `LOG.md` (the wave cited before the grant is durable); measured rev `049dcf73c6bfddaaf1de230756e504273fb673ff`.

```
C2 durable 0/1 met=False
  FAIL LOG.md at grant_rev already cites the wave
EXIT:1
```

Rejecting condition: counter §10 (first half) — `git show <grant_rev>:LOG.md` contains `r50-w1`, which violates the pre-append ordering invariant that the grant must be durable before any LOG entry cites the wave.

## Verdict

**C2 rejects all three mutants.** Each of the three targeted order/durability conditions (grant stdout present, dispatch transport free of `--auto`, and wave-not-cited-at-grant_rev) is independently enforced by the frozen counter — the mutant tripped exactly the intended `FAIL` reason and no other. The instrument is sensitive to each defect class it claims to guard.
