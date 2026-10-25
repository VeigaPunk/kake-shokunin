# Critic cross-wire probe — C1 quote-class counter

## What was attacked

The frozen C1 counter `.ufo/waves/round-50/c50_quote_class.py` reads
`.ufo/waves/round-50/quote-classes.json` at a committed revision. Hypothesis
under test: a critic could swap the per-id fields of two ledger rows — S273
(collapsed-only) and S274 (raw-substring) — and the counter would still
return `met` because the rows, quotes, and sha256 pins are all
internally consistent, just attached to the wrong ids.

## Method

1. Exported the real ledger at pre-append revision
   `33eec7f2cecfdbb9c7a1f85c3d8efae8dacd7dd1`.
2. Swapped `quote`, `matchClass`, `textPath`, `rawPath`, `textSha256`,
   `rawSha256` between the S273 and S274 rows, leaving `id` fields in
   place. S286 row untouched.
3. Minted probe commit `000eefb7583f308befdfc7022bf1e14c51a98440`
   (parent 33eec7f, only file changed:
   `.ufo/waves/round-50/quote-classes.json`) via `hash-object -w` /
   `commit-tree` against a `/tmp` index file — the lane index, worktree,
   and jj state were never touched.
4. Ran the frozen counting command against the probe revision.

## Frozen counter baseline (for context)

```
$ python3 -B .ufo/waves/round-50/c50_quote_class.py --root . --revision 9619af67c52939daac502ca7a24c9d714f3f51db
C1 classed 0/3 met=False
  FAIL S273: class ledger absent, lesson absent
  FAIL S274: class ledger absent, lesson absent
  FAIL S286: class ledger absent, retained blob absent, lesson absent, no live registry row, entry absent
EXIT=1

$ python3 -B .ufo/waves/round-50/c50_quote_class.py --root . --revision 33eec7f2cecfdbb9c7a1f85c3d8efae8dacd7dd1
C1 classed 0/3 met=False
  FAIL S273: lesson absent
  FAIL S274: lesson absent
  FAIL S286: lesson absent, no live registry row, entry absent
EXIT=1
```

## Probe result — counter stdout and exit code

```
$ python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-50/c50_quote_class.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 000eefb7583f308befdfc7022bf1e14c51a98440
C1 classed 0/3 met=False
  FAIL S273: ledger quote is not the frozen quote, recorded class raw-substring != derived collapsed-only, text sha256 differs, raw sha256 differs, lesson absent
  FAIL S274: ledger quote is not the frozen quote, recorded class collapsed-only != derived raw-substring, text sha256 differs, raw sha256 differs, lesson absent
  FAIL S286: lesson absent, no live registry row, entry absent
EXIT=1
```

## Verdict

**The swap is detected.** Both crossed ids fail four independent rules
each; `classed` drops to 0/3 and the predicate is unmet. No rule failed
to fire.

### Which rules fired, per crossed row

For S273 (row now carrying S274's bytes):

- `ledger quote is not the frozen quote` — the row's `quote` is S274's
  string; the counter compares it to `FROZEN_QUOTES["S273"]` (the
  hard-coded crawl-budget sentence), not to anything derived.
- `recorded class raw-substring != derived collapsed-only` — the
  counter re-derives the class from the *real* S273 blobs
  (`BLOBS["S273"]`, hard-coded paths under
  `.ufo/waves/round-49/sources/`): the frozen quote is a substring of
  `S273.txt` but not of `S273.raw.html` → `collapsed-only`. The swapped
  row says `raw-substring` → R2 fails.
- `text sha256 differs` / `raw sha256 differs` — the swapped pins are
  the S274 blob hashes; the counter hashes the S273 blobs it loaded via
  `BLOBS["S273"]`, so the digests mismatch.

For S274 the same four rules fire symmetrically (derived
`raw-substring` vs recorded `collapsed-only`).

### Residual surface worth naming

The counter **ignores the ledger's `textPath`/`rawPath` fields** — it
always opens `BLOBS[id]`, a hard-coded map. So the path swap itself is
inert: even if a row's paths pointed at the other id's files, the
counter would still derive class and sha from `BLOBS[id]`. The check
that actually fires is the sha256 pin plus the frozen-quote and
re-derived class comparisons, all anchored to constants in the counter,
not to ledger contents. Consequence: cross-wiring the ledger can never
succeed unless the attacker also rewrites the frozen constants in
`c50_quote_class.py` — which is committed at the base revision and out
of scope for a ledger-only edit.

`lesson absent` on all three rows and the S286 registry/entry failures
are pre-existing gaps at 33eec7f (the lesson and live-registry row land
later in the wave), not consequences of the swap.

## Lane-hygiene note

Probe objects live in the lane repo's object store as an unreferenced
commit (`000eefb…`), reachable by hash only — no branch, tag, index
entry, worktree file, or jj state was mutated. `git status` before and
after showed only pre-existing modifications/untracked paths unrelated
to this probe.

Report: .ufo/waves/round-50/w1/CriticCrossWire.md
