# MutationWrongPath — C1 per-id binding mutation test

Seat: leaf, round 50 wave 1. Frozen counter:
`.ufo/waves/round-50/c50_quote_class.py`, predicate `met: classed == 3 of 3 declared ids` (S273, S274, S286). All mutants built in a `/tmp/kake-r50-mut` clone on top of pre-append revision `33eec7f2cecfdbb9c7a1f85c3d8efae8dacd7dd1`, scored with the frozen counter against that clone. The lane repo was not touched.

Key mechanism, read from the counter source: per-id blobs are resolved through the **hardcoded `BLOBS` dict** (`BLOBS[sid]`), not through the ledger row's `textPath`/`rawPath`. Those two ledger fields are never opened by the counter — `grep textPath|rawPath` over `c50_quote_class.py` returns no matches. The binding is therefore: fixed path → committed bytes → sha256 pin → frozen quote → derived class.

## Mutant 1 — S286 `textPath`/`rawPath`/`textSha256`/`rawSha256` repointed to S274's committed blobs

Ledger row claims S286's class is evidenced by S274's `.txt`/`.raw.html` bytes, with matching sha256 fields.

```
$ python3 -B .ufo/waves/round-50/c50_quote_class.py --root /tmp/kake-r50-mut --revision d4e3022a547346119b8c3402a7cfedad3348b2fa
C1 classed 0/3 met=False
  FAIL S273: lesson absent
  FAIL S274: lesson absent
  FAIL S286: text sha256 differs, raw sha256 differs, lesson absent, no live registry row, entry absent
exit code: 1
```

Rule that fired: **R1** — `text sha256 differs`, `raw sha256 differs`. The counter hashed the blob at the hardcoded `BLOBS["S286"]` path and compared it against the ledger's (now-S274) sha, so the pin caught the mismatch even though the ledger's path fields pointed elsewhere.

## Mutant 1b — S286 `textPath`/`rawPath` repointed to S274's blobs, sha256 left at S286's true values

```
$ python3 -B .ufo/waves/round-50/c50_quote_class.py --root /tmp/kake-r50-mut --revision d1672a9d880f6fef4031298864358718b027ccd9
C1 classed 0/3 met=False
  FAIL S273: lesson absent
  FAIL S274: lesson absent
  FAIL S286: lesson absent, no live registry row, entry absent
exit code: 1
```

No rule fired on the path mutation itself. The counter is **blind to `textPath`/`rawPath`** — the ledger can assert paths naming another id's blobs without detection. Only the fixed-path sha pin binds the id to bytes.

## Mutant 2 — S273 `textPath`/`textSha256` repointed to S274's committed `.txt` blob

```
$ python3 -B .ufo/waves/round-50/c50_quote_class.py --root /tmp/kake-r50-mut --revision 4502f1802d80c9bde288a4a426c422d0f88df236
C1 classed 0/3 met=False
  FAIL S273: text sha256 differs, lesson absent
  FAIL S274: lesson absent
  FAIL S286: lesson absent, no live registry row, entry absent
exit code: 1
```

Rule that fired: **R1** — `text sha256 differs`. Same mechanism as mutant 1: the recorded sha was compared against the bytes at the fixed `BLOBS["S273"]` path.

## Mutant 3 (control) — S286 blob bytes at the hardcoded path physically replaced with S274's committed bytes, ledger sha updated to match

This is the strongest form of "an id pointing at another id's bytes" — the id's own fixed path now contains the other id's bytes, and the ledger agrees.

```
$ python3 -B .ufo/waves/round-50/c50_quote_class.py --root /tmp/kake-r50-mut --revision c542e49b2673fd53dc437f39dcfc62a791d5769e
C1 classed 0/3 met=False
  FAIL S273: lesson absent
  FAIL S274: lesson absent
  FAIL S286: recorded class raw-substring != derived absent, lesson absent, no live registry row, entry absent
exit code: 1
```

Rule that fired: **R2** — `recorded class raw-substring != derived absent`. The frozen S286 quote is not a substring of S274's text blob, so `classify()` derives `absent` and the recorded `raw-substring` label is rejected. The sha pin passed (bytes at the fixed path matched the ledger), but the per-id frozen quote still bound the id to its own content.

## Answer to the posed question

**No — the counter cannot be met by an id that points at another id's bytes.** Every mutation path is caught:

- Repoint the ledger's `textPath`/`rawPath` + sha to another id → **R1** fires (`text/raw sha256 differs`), because the counter hashes the blob at the hardcoded per-id `BLOBS` path and ignores the ledger's path fields entirely.
- Repoint only the path fields, keep the true sha → silent on R1/R2 (the fields are unverified — a cosmetic ledger lie), but the id still cannot gain class credit from it; it simply leaves the real binding untouched.
- Replace the actual committed bytes at the id's fixed path with another id's bytes and update the sha to match → **R2** fires (`recorded class != derived absent`), because the id's frozen quote is not a substring of the borrowed bytes.

The per-id binding is the conjunction of (a) the frozen per-id `FROZEN_QUOTES`, (b) the hardcoded per-id `BLOBS` path, (c) the sha256 pin over bytes read at that fixed path, and (d) R2's derived-class equality. Borrowing another id's bytes breaks (c) at minimum, and even if (c) is satisfied by substitution, (a)+(d) still reject the row because the wrong bytes cannot yield the right quote's derived class.

One residual weakness worth noting for the L1: `textPath`/`rawPath` in the ledger are dead fields — a ledger can name any path at all without affecting the verdict. Harmless to the predicate, but a reader could mistake them for the binding mechanism.
