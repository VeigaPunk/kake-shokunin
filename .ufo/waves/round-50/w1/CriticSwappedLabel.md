# CriticSwappedLabel — can a WRONG class be met?

Scope: C1 (`met: classed == 3 of 3 declared ids`) under label swap of S286
`matchClass` raw-substring → collapsed-only, with the lesson's S286 class
sentence swapped to match. Counter: `.ufo/waves/round-50/c50_quote_class.py`.

## Method

`c50_quote_class.py` reads committed bytes only (`git show <rev>:<path>`), but
the lesson, SOURCES registry row, and entry are staged-uncommitted in the lane
worktree. To attack the *committed* end-state the claim will be judged at, I
drove the frozen counter's `run()` directly with `git_show` monkeypatched so
exactly four paths serve local bytes — `.ufo/waves/round-50/quote-classes.json`
(committed version with only S286 `matchClass` flipped to `collapsed-only`,
sha pins untouched), `corpus/lessons/round-50.md` (worktree bytes with only the
`- S286 quote class is …` line flipped to `collapsed-only`), `corpus/SOURCES.md`
and `corpus/knowledge/crawl-error-status-table.md` (worktree bytes as staged).
Every other path (S273/S274/S286 retained blobs, etc.) resolved via real
`git show` at the pre-append mirror revision `33eec7f`.

## Verbatim counter output

Swapped-label attack run (exit code 1):

```
C1 classed 2/3 met=False
  ok S273: all rules hold
  ok S274: all rules hold
  FAIL S286: recorded class collapsed-only != derived raw-substring, lesson lacks the derived class sentence, lesson states the opposite class, no live registry row
```

Honest-label control (same harness, unswapped ledger at `33eec7f` + worktree
lesson/SOURCES/entry as staged — exit code 1):

```
C1 classed 2/3 met=False
  ok S273: all rules hold
  ok S274: all rules hold
  FAIL S286: no live registry row
```

Frozen counter on the real lane for reference:

```
$ python3 -B .ufo/waves/round-50/c50_quote_class.py --root . --revision 9619af6…  (base)
C1 classed 0/3 met=False    [exit 1]
$ python3 -B .ufo/waves/round-50/c50_quote_class.py --root . --revision 33eec7f…  (pre-append)
C1 classed 0/3 met=False    [exit 1]
  FAIL S286: lesson absent, no live registry row, entry absent   (+ ledger/lesson absent at base)
```

## Verdict

A WRONG class cannot be met. Swapping S286's label to `collapsed-only` trips
three independent rules on that row: R2 recorded-vs-derived mismatch
(`recorded class collapsed-only != derived raw-substring`), R3 missing
required sentence (`lesson lacks the derived class sentence` — it requires the
*derived* string, not the recorded one), and R3 opposite-sentence ban
(`lesson states the opposite class`). `classed` tops out at 2/3, `met=False`,
exit 1. Flipping only the ledger or only the lesson would still fail on the
untouched half, so no single-file forgery meets the predicate.

## Caveat (not a swap hole)

The fourth S286 failure — `no live registry row` — also fires in the honest
control: the staged worktree `SOURCES.md` predates the S286 append, so that
rule's verdict is a staging artifact, not a label-swap consequence. R4's
registry/entry/gate checks are orthogonal to the label attack and were not
exercised by it.
