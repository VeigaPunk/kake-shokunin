VERDICT: neither counter reads `met=true` at freeze `a5640ca02c20f94a0fa03af41b977b46ae99808e`.
Both exit 1. The targets are not trivially satisfiable, so the two claims are not dead on
arrival. One caveat survives: C1's `self` conjunct is already satisfied at the freeze, and C1's
item C does not measure the revision it is given (C1-D4).

# Controls — do-nothing at the freeze revision

## Setup (the prescribed scratch clone)

```
S=/fast/scratch/hyaku/kake-r92/CriticClaims
git clone -q --shared /home/vgpnk/Projects/shokunin/kake-shokunin "$S/clone"
git -C "$S/clone" checkout -q --detach a5640ca02c20f94a0fa03af41b977b46ae99808e
git -C "$S/clone" update-ref refs/heads/master \
  $(git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse refs/heads/master)
```

`git -C "$S/clone" rev-parse --show-toplevel` printed
`/fast/scratch/hyaku/kake-r92/CriticClaims/clone` before any run. Clone `master` = `f0b2dc63…`
(the LANE `master` tip at the time), which is what the C1 harness resolves as `CARRIER`.

## Do-nothing readings (first lines, verbatim)

```
$ python3 -B "$S/clone/.ufo/waves/round-92/c92_defects.py" \
    --root "$S/clone" --revision a5640ca02c20f94a0fa03af41b977b46ae99808e --work "$S/work-dn/c1"
C1v92 revision=a5640ca02c20f94a0fa03af41b977b46ae99808e items=3 open=3 closed=0 battery=hit differential=fail self=ok met=false
exit=1
```

```
$ python3 -B "$S/clone/.ufo/waves/round-92/c92_heuristic.py" \
    --root "$S/clone" --revision a5640ca02c20f94a0fa03af41b977b46ae99808e --work "$S/work-dn/c2"
C2v92 revision=a5640ca02c20f94a0fa03af41b977b46ae99808e candidate=absent hand=0/28 generated=0/120 forgeries_refused=0/5 anti_table=n/a population=n/a seed=92 met=false
exit=1
```

Receipts: `receipts/dn-c1.out` (both lines + JSON detail), `receipts/dn-c2.out`.

C1's JSON detail at the freeze: `open_items=["A","B","C"]`, reasons
`A="mutation receipt absent"`, `B="no registry row names c92_defects.py with its --revision
command and met predicate"`, `C="label set differs (missing=['carrier-open=0','carrier-met=true',
'carrier-exit=0'] extra=['carrier-open=2','carrier-met=false','carrier-exit=1'])`,
`battery="fixture FA could not be built"`, `self_pin="ok"`.

## Base cross-check (the committed controls are reproducible)

```
C1v92 revision=e143faff1b86aad172dd87696da900c70347b8b2 items=3 open=3 closed=0 battery=hit differential=fail self=hit met=false
C2v92 revision=e143faff1b86aad172dd87696da900c70347b8b2 candidate=absent hand=0/28 generated=0/120 forgeries_refused=0/5 anti_table=n/a population=n/a seed=92 met=false
```

Both exit 1 and match `.ufo/waves/round-92/controls/base-c1.txt` / `base-c2.txt` line for line.
The only difference between the base and freeze C1 readings is `self=hit` → `self=ok`, because
`frozen/c1-self.sha256` arrives in the freeze commit.

## Two notes that matter for the claim

1. **`self=ok` at the freeze is not wave work.** The pin file and the counter are committed in
   the same commit, and `self_ok` compares the pin *at the measured revision* to the counter *at
   the same revision* (`c92_defects.py` lines 399–402). The self conjunct therefore cannot move
   between the freeze and the carrier unless someone edits one without the other. It is a
   tamper check against accidental drift, not a pin to the frozen instrument (C1-D5/C1-D6).
2. **C1's item C is not a do-nothing control on the revision.** It is `open` at the freeze only
   because the clone's `master` (`f0b2dc63…`) also lacks the artifacts. Measured at fixture F4
   `d8affc1b…` — no C1 artifact present at all — item C **closed** because `master` was F1 at
   that moment (`open=2 closed=1`). So item C is satisfied without work whenever `master` is a
   revision where A and B hold; it does not measure the revision it is handed (C1-D4).

No counter reads `met=true` with no work at the freeze revision. The target is not wrong; the
predicates are under-bound (C1.md, C2.md), which is a different failure.
