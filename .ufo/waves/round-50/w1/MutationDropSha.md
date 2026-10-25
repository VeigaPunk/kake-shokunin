# Mutation test — C1 class ledger (w1 seat)

Scope: attack the frozen C1 counter `.ufo/waves/round-50/c50_quote_class.py` by mutating the committed class ledger `.ufo/waves/round-50/quote-classes.json` in a `/tmp` clone only. Lane repo untouched; mutants scored as committed bytes via `git show`, matching the counter's COMMITTED_BYTES_ONLY contract.

## Method

- Clone `/home/vgpnk/Projects/shokunin/kake-shokunin` → `/tmp/r50-mut-test`, checked out at pre-append `33eec7f2`.
- Control commit `70ef3fa3c5b4bf51f95631f3e05980980e62e875`: copies in the unmutated passing artifacts (mirror `SOURCES.md` with the S286 row, `corpus/lessons/round-50.md`, `corpus/knowledge/crawl-error-status-table.md`). Scores `met=True` 3/3 — a clean baseline each mutant is one commit on top of.

## Baseline (frozen counter, real lane revisions)

`python3 -B .ufo/waves/round-50/c50_quote_class.py --root . --revision 9619af67c52939daac502ca7a24c9d714f3f51db` → `C1 classed 0/3 met=False`, exit 1. Do-nothing: no class ledger, no retained S286 blob.
`python3 -B .ufo/waves/round-50/c50_quote_class.py --root . --revision 33eec7f2cecfdbb9c7a1f85c3d8efae8dacd7dd1` → `C1 classed 0/3 met=False`, exit 1 (lesson absent, S286 live row/entry absent — expected at pre-append).

## Mutant 1 — drop sha256 pins

Edit: removed `textSha256` and `rawSha256` from all three rows of `quote-classes.json`; committed as `e4bb0c77f3683369d31512c41534bf6c70092ebf`.

```
C1 classed 0/3 met=False
  FAIL S273: text sha256 differs, raw sha256 differs
  FAIL S274: text sha256 differs, raw sha256 differs
  FAIL S286: text sha256 differs, raw sha256 differs
```

Exit code: 1.

Rejected: yes. Rule that fired: **R1's pin check** — counter compares `row["textSha256"]` / `row["rawSha256"]` against `sha256` of the retained blobs read by `git show`; missing fields compare unequal → `text sha256 differs` / `raw sha256 differs` (c50_quote_class.py:191-194).

## Mutant 2 — drop `matchClass`

Edit: removed `matchClass` from all three rows (sha pins and `quote` intact); committed as `8d95e3ff8c4187568b8e1d3510e8162129d106cc`.

```
C1 classed 0/3 met=False
  FAIL S273: recorded class None != derived collapsed-only
  FAIL S274: recorded class None != derived raw-substring
  FAIL S286: recorded class None != derived raw-substring
```

Exit code: 1.

Rejected: yes. Rule that fired: **R2's recorded-vs-derived check** — `row["matchClass"]` is `None`, never equal to the class derived from the two retained blobs → `recorded class None != derived …` (c50_quote_class.py:187-190).

## Verdict

Both mutants are rejected, each by a distinct R1/R2 rule, exit code 1 in both cases. A ledger row cannot pass with its sha256 pins stripped (the pin is compared to the live blob digest, not merely required to exist), and cannot pass with `matchClass` stripped (the recorded label must equal the class the counter derives from both blobs, not just be present). The counter pins provenance (bytes) and label (derivation) independently.
