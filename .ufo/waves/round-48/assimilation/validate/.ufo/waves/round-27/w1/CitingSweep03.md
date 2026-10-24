# KakeR27.CitingSweep03 — blind citing census, two named knowledge files

Axes: **freshness** (C1 citing-set denominator completeness at frozen base) and
**operability** (can the frozen counter reproduce the before-state). This seat's
work exercises both; no production edits, no source/public-site evaluation.

Scope: exactly `corpus/knowledge/fire-journal-codes.md` (87 lines) and
`corpus/knowledge/fleet-registry.md` (112 lines).
Base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`; HEAD `be375d90afc6fc7aca369ab3cf5247bf460aeed2`.

Method order honoured: manual line-by-line census **first**, parser and
`c1-before.json`/16-missing comparison **after**.

## 1. Manual census (complete)

Every source-id reference in both files, found by whole-file scan for
`S` + 3-or-more digits, plus a broader separator/case sweep
(`S[ _.-]?digits`, case-insensitive), plus hand read of all 199 lines:

| file | line | token | form | syntactic scope | semantic scope |
|---|---|---|---|---|---|
| fire-journal-codes.md | 1 | `S019` | literal, single | `source:` provenance header | metadata-format authority only; primary sources are own-work |
| fleet-registry.md | 1 | `S019` | literal, single | `source:` provenance header | "Metadata authority only", explicitly not platform verification |

Exact support, <=25 words each:

- fire line 1: "own-work; no SOURCES.md id); metadata format per S019 (metadata authority only, not a platform source)"
- fleet line 1: "Metadata authority only: S019 in corpus/SOURCES.md, not platform verification."

Negative findings, same scan:

- **Grouped forms:** none (no `S001–S006`-style group anywhere in either file).
- **Ranges:** none (`-`, en/em dash, `..`, `to`, `through` with S at both ends).
- **Alternate spellings:** none (`S-019`, `S 019`, `s019`, `SO19`, "row 19").
- **EOF notes:** zero S-id tokens. fire 78–87 uses claim labels `[fire-journal-codes:c1..c6]`
  only; fleet 87–100 uses `[fleet-registry:c1..c9]`, and fleet 107–112 cites
  `fleet-registry.md:49/50/51/57/64/66` (self row coordinates, not S-ids).
- fire line 8 r20 note and line 3 recheck are citation-local annotations with no S-id.

Token frequency (`grep -oE 'S[0-9]{3,}' | sort | uniq -c`): fire `1 S019`;
fleet `1 S019`. Both are 3-digit literals; the parser's `{3,}` admits them.

## 2. Denominator impact (inherited 32-row population)

Frozen denominator rule: literals + S-both-ends ranges, **intersected with the r26
32-row population**. `S019` is not a population row
(`.ufo/waves/round-26/population.json`: 32 ids, S001–S034 excluding S014/S019;
`corpus/SOURCES.md:79` records "S001–S034 minus own-work S014/S019").

- Inherited-population citing pairs contributed by these two files: **0**.
- Ranges that could expand into population ids: **0**.
- Of the frozen 16 missing pairs: **0** involve either file.
- No additional inherited32-row obligation found: the only references are
  out-of-population `S019`, named separately below. Denominator 57 is not shrunk
  by this seat; nothing valid was dismissed as "just metadata" without the rule check.

## 3. Out-of-population citations — recorded separately (not obligations)

Named explicitly so the denominator can only grow visibly:

1. `(S019, corpus/knowledge/fire-journal-codes.md)` — line 1, metadata-format authority.
2. `(S019, corpus/knowledge/fleet-registry.md)` — line 1, metadata authority, not platform verification.

`S014` and `S035` do **not** appear in either assigned file (both absent from both
scans). Corpus context from the same base scan, outside my two-file scope:
`S019` cited by 16 knowledge files, `S014` by 1 (`freshness-sweep.md`), `S035` by 1
(`accessibility-review-packet.md`). If L1 ever admits own-work rows, this seat's
scope adds exactly **2** pairs, pending a separate adjudication basis.

## 4. Parser comparison (performed after §1)

`count_c1.py` at base, unchanged, exit 1 (missing) — output is **JSON-identical**
to `c1-before.json` (`2026-10-21`, this seat): `citingPairs 57`, `decided 41`,
`missing 16`, `findings 0`. Independent enumerator written to the contract rule
(3+ digits; hyphen/en/em/`..`/`to`/`through`; population intersection; 26 knowledge
files at base) also returns exactly 57, and its missing set equals
`c2-oracle.json.expectedPairs` (16) and `c1-before.json.missing` (set-equal).

Mechanism for these files, observed in the parser source:

- `LITERAL = \bS(\d{3,})\b` matches `S019` once per file, then
  `if f'S{i:03d}' in pop` is false → no pair. Matches manual census exactly.
- `RANGE` requires `S` at both ends; no match in either file.
- Scan domain is `corpus/knowledge` blobs at `--revision` only, so SOURCES.md's
  defining `S019` table row is not itself a pair.
- `pairs.json` / `discovered-pairs.json` were absent at measurement, so the
  before-state is purely r26-carried: 41 decided = 41 rows of
  `round-26/statements.json`, which contains **zero** rows naming either file.

Range forms observed corpus-wide at base (for cross-check only):
`publish-channels.md S001-S007`, `sitemap-orphan-audit.md S001-S006`,
`static-canonical-preflight.md S020-S027`, `S028-S029`, `S001–S006`.

## 5. Byte identity / hashes

- `git diff --stat base..HEAD -- <both files>`: empty; working bytes == base == HEAD.
- fire: git blob `03dad37cc33f89134fe5fa2890222ff926930ab1`,
  sha256 `7e74cb6346300b1b3a242d1a1c14c72f7932956f6f5a29055c78e6e26503a503`.
- fleet: git blob `a8997c920d29b408982068f8395095da576e2ffd`,
  sha256 `4bd960f082e43fd1a4d5e40c02503d304e72b983f8df2f4fef920a1d331a4cd1`.
- Working-tree `hash-object` equals base `rev-parse` for both.

## 6. Verdicts

- **Supported at base (author-side):** both files contribute 0 to frozen 57 and 0
  to the 16 missing; the frozen counter's exclusion is correct per the declared
  population-intersection rule, not an omission.
- **Freshness of bytes:** unchanged from frozen base, so no r27 content drift in
  either assigned file.
- No PASS claimed on any substantive content claim in these files; content is
  historical/own-work and was not re-observed this round.

## 7. Uncertainties

1. Whether own-work rows (`S019`) enter any denominator is an L1/contract decision;
   if admitted, +2 pairs here, and support basis is the `S019` metadata audit
   (`CORPUS.md` Layout, opened 2026-10-20), not platform truth.
2. No source/public-site evaluation performed by design; r23 claim verdicts and
   historical assertions untouched.
3. Alternate-form sweep is literal-pattern based; a purely verbal reference
   ("source nineteen") would evade it. None observed.
4. `c2-oracle`/`c1-before` equivalence proves agreement, not independent truth of
   the population itself; population membership was taken as frozen.

Evidence: base-revision `git show` reads, `count_c1.py` run (exit 1, JSON identical
to `c1-before.json`), independent enumerator, `sha256sum`/`git hash-object`.
Scratch: `/fast/scratch/hyaku/kake-r27/` (`CitingSweep03-count.json`, `-err.txt`).
No tool installs; pacman untouched. No edits outside this report.
