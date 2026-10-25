# MutationOrderSwap — C2 order-rule mutation test

Item: mutation-test C2's pre-append order rule by swapping the roles of the
pre-append mirror and the live registry, then scoring with the frozen counter.

## Mutation

Built a scratch git repo at `/tmp/c50-mutation-order-swap/repo` with three
commits, using the lane's real pre-append artifacts (from
`33eec7f2cecfdbb9c7a1f85c3d8efae8dacd7dd1`) with the roles swapped:

- `c0e615bdf9e43b41302e0a997f884afc4dcc7923` (pre_rev): live
  `corpus/SOURCES.md` contains the S286 row (inserted after S274);
  `.ufo/waves/round-50/assimilation/pre-append/corpus/SOURCES.md` mirror has
  the S286 row removed. Census argv/stdout/exit blobs copied verbatim from the
  real pre-append revision (a passing `--file` validation of the mirror).
- `db2e81d3ae52678586294da5f76afd86e181d260` (grant_rev): `wave-grant.txt`
  (one granted line, seats=36), `dispatch-command.txt` (`kimi ... --prompt`,
  no `--auto`), `LOG.md` without `r50-w1`.
- `17c45e87c77522c7a4528dfa074fcdb7b58e1919` (measured): `order-proof.json`
  naming pre_rev and `adopted_ids: ["S286"]`, `wave-cite-proof.json` naming
  grant_rev, `settlement.json` (`spawn: 36`, `replacements: []`), `LOG.md`
  citing `r50-w1` and the grant_rev hash.

This models the inversion the order rule exists to catch: S286 was appended to
the live registry before the pre-append mirror was committed — i.e., the
mirror no longer proves the row was validated before adoption.

## Score (frozen counter, verbatim)

```
$ python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-50/c50_durable.py --root /tmp/c50-mutation-order-swap/repo --revision 17c45e87c77522c7a4528dfa074fcdb7b58e1919
C2 durable 0/1 met=False
  FAIL S286 already in live registry at pre_rev
  FAIL S286 missing from pre-append mirror
EXIT=1
```

## Conditions that fired

Both halves of counter condition 3 (c50_durable.py:149-152):

- `S286 already in live registry at pre_rev` — the "not yet live" half.
- `S286 missing from pre-append mirror` — the "mirror holds the candidate" half.

All other conditions (ancestor relations, census argv/exit, grant stdout,
dispatch shape, LOG citation ordering, settlement spawn/replacements)
evaluated clean — the swap isolates the order rule.

## Control

A same-shape control at `/tmp/c50-mutation-order-control/repo` with the roles
unswapped (live without S286 at pre_rev, mirror with it, S286 appended to live
at the measured revision) scores `C2 durable 1/1 met=True`, exit 0. The
counter is not simply failing on the scratch harness.

## Verdict

No — the counter cannot be met by a registry that was appended before the
mirror was committed. Both directions of the inversion are caught: appending
early fires `S286 already in live registry at pre_rev`, and a mirror without
the row fires `S286 missing from pre-append mirror`. The order rule requires
mirror-has-row AND live-lacks-row at pre_rev, plus live-has-row at the
measured revision; the mutation shows each conjunct independently gated.
