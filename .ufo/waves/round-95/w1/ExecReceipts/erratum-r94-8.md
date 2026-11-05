# Erratum R94-8 — the round-93 `base_rev` pointer names an unrecoverable commit

Seat: ExecReceipts (kake round 95, wave w1, 2026-11-05). Measured in the lane at
HEAD `d9be693fdb61dd080ae8cf6c007871d3a118c1d2`; round base
`fdd5fdbeb8a2ba6c18f0f23135d1bee98068dca3`; round-94 freeze of reference
`ba667b245f26125c13885958498b3b4999756d04`. Read-only measurements only.

## What the pointer claimed

The round-93 mutant-scoring receipt
`.ufo/waves/round-93/w1/recovered-partial/MutConditional/posgood-out/mutants.json`
line 7 declares:

```json
"base_rev": "191dd0ed0cf594a29668f5862f536a925998cadd",
```

i.e. the round-93 receipts claim their 40-mutant kill measurements ran against
the round-93 base commit `191dd0ed0cf594a29668f5862f536a925998cadd`.

Note on the reading list: the seat brief pointed at `mutants-posgood.json` for
the `base_rev` line. Measured (below): that file carries **no** `base_rev`
field at all; the `base_rev` line lives in the sibling scoring output
`posgood-out/mutants.json`. The correction text below is written against the
measured reality.

## What is absent

- `git cat-file -t 191dd0ed0cf594a29668f5862f536a925998cadd`
  → `fatal: git cat-file: could not get object info`, rc 128
  (observed 2026-11-05, lane HEAD `d9be693f`; same fatal at the round base).
  The object is reachable from no lane ref, no remote ref, and no committed
  tree; round-94 critic receipts already record the same rc 128
  (`.ufo/waves/round-94/w1/CriticClaims/git-and-digests.out` lines 3–4) and the
  executor clone-only base `6d75ee0c` is likewise absent (CriticClaims D14).
- **The base commit `191dd0ed` is unrecoverable-from-this-lane.** The round-93
  kill counts are reproducible only from the committed patch list plus the
  frozen base bytes — never from that revision.

## What the measured bytes actually are

- The patch population
  `.ufo/waves/round-93/w1/recovered-partial/MutConditional/mutants-posgood.json`
  (git blob `f15c99f42ef250baaa21f2e3114b3b634de2734e`, mode 100644, at
  `fdd5fdbe`) contains no `base_rev`; it pins its base **by content**:

  ```json
  "base": {"file": "scripts/conditional_eval.py",
           "source": ".ufo/waves/round-93/frozen/pos-good.py",
           "sha256": "0fe018a8e33ca82928a876f2b0d2e5b3f33befa00260f2fdf995418822a868e4"}
  ```

- Measured: `git ls-tree fdd5fdbe -- .ufo/waves/round-93/frozen/pos-good.py`
  → blob `e78f28457fb6209bcdbac99aed0bfa56a289a4e4` (mode 100755);
  `git show fdd5fdbe:.ufo/waves/round-93/frozen/pos-good.py | sha256sum`
  → `0fe018a8e33ca82928a876f2b0d2e5b3f33befa00260f2fdf995418822a868e4` —
  **byte-identical** to the population's declared `base.sha256`.
- Digest correction to the seat brief's guess: `f15c99f4…` is the blob of
  `mutants-posgood.json` itself, **not** of `pos-good.py`; the full digests are
  the two recorded above (`e78f2845…` blob / `0fe018a8…` content sha256).
- The round-95 C2 counter consumes this file as `MUTANTS_JSON`, scores it
  against `MUTANT_BASE` (the digest-pinned `pos-good` bytes) and ignores the
  dead pointer by design (freeze.md "Population base" paragraph; the pointer is
  disclosed in the counter docstring, `c95_conditional.py` line 37).

## Other citers of `191dd0ed` in the committed trees

`git grep -n 191dd0ed <tree>` (rc 0, full trees):

- At round base `fdd5fdbe` and at freeze `8f638b59` (identical hit sets):
  - round-93: only the pointer itself, `posgood-out/mutants.json:7`. No other
    round-93 file cites the commit; `mutants-posgood.json` does **not**.
  - round-94: `w1-results.json:52` (embedded critic output, D1/D14),
    `w1/CriticClaims.md` lines 39, 83, 168, 174, 187, 208,
    `w1/CriticClaims/git-and-digests.out` lines 3–4 (the rc-128 receipts).
  - round-94 corpus/scorecard routing: `SCORECARD.md:5722` (R94-8 line),
    `corpus/lessons/round-94.md:94` (R94-8 row).
- At HEAD `d9be693f` additionally (by design, the erratum disclosures):
  `.ufo/waves/round-95/freeze.md:110` and
  `.ufo/waves/round-95/c95_conditional.py:37`.

No committed file treats `191dd0ed` as resolvable; every citer after the
round-93 receipt quotes it as absent.

## Correction text for the round lesson (two sentences)

> The round-93 mutant-scoring receipt `w1/recovered-partial/MutConditional/posgood-out/mutants.json`
> pinned its readings to `base_rev 191dd0ed0cf594a29668f5862f536a925998cadd`,
> a round-93 base commit no lane ref carries (`git cat-file -t` fatal, rc 128
> at round-95 base `fdd5fdbe`), so that revision is unrecoverable from this
> lane and the round-93 kill counts are reproducible only from the committed
> patch list plus the frozen base bytes. The patch target itself needs no
> revision: `mutants-posgood.json` (blob
> `f15c99f42ef250baaa21f2e3114b3b634de2734e`) pins
> `base.source = .ufo/waves/round-93/frozen/pos-good.py` by content sha256
> `0fe018a8e33ca82928a876f2b0d2e5b3f33befa00260f2fdf995418822a868e4`,
> byte-identical to the committed `pos-good.py` blob
> `e78f28457fb6209bcdbac99aed0bfa56a289a4e4` at `fdd5fdbe`, and the round-95
> counter correctly ignores the dead pointer, scoring the population against
> the digest-pinned pos-good bytes.

## Verdict

R94-8 is closed as an erratum: the pointer is recorded as claimed-and-absent,
the base commit is marked unrecoverable-from-this-lane, the measured bytes
(content-pinned pos-good base) are recorded, and the two-sentence correction
above is ready to carry into `corpus/lessons/round-95.md`. No lane file was
modified.
