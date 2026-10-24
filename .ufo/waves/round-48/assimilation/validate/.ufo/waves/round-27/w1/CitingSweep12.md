# CitingSweep12 — blind citing census: sitemap-orphan-audit.md, speedrun-pipeline.md

Seat: read-only scout (leaf), axis freshness. Revision HEAD `be375d90afc6fc7aca369ab3cf5247bf460aeed2`;
target bytes are identical at frozen base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`
(`git diff 83528f7 be375d9 -- <both files>` empty; worktree clean vs HEAD).
No source/public-site evaluation was performed; nothing fetched; no edits outside this report.

Method: (1) read both blobs line by line and hand-enumerated every S-id occurrence, form and scope,
including the `source:`/`verified-at:` provenance headers and the EOF round-26 recheck notes;
(2) independent token sweep `\bS\d+`, `[Ss]\s?\d{2,}`, `S\d+\s*(through|to|\.\.|…|/)\s*S?\d+`
and Unicode-dash inventory to surface any form the frozen regexes cannot see;
(3) only then compared with `count_c1.py` / `c1-before.json` / frozen16 / `c2-oracle.json`.

## Verdict (census, not source truth)

Population-intersecting citing pairs in these two files: **9** — `sitemap-orphan-audit.md` = S001,S002,S003,S004,S005,S006
(6); `speedrun-pipeline.md` = S001,S002,S004 (3). All 9 are inside frozen57 (57/41/16 partition reproduced exactly).
Frozen16 contains exactly 2 of the 9: `(S003, sitemap)` and `(S005, sitemap)`; the other 7 are carried by the r26 ledger.
**No valid inherited32-row pair exists in these files outside frozen57 → no additional population obligation from this seat.**
Out-of-population reference: `S019` (speedrun L2) recorded separately below; `S014`/`S035` do not appear.

## A. Occurrence inventory (1-based current lines; form; ids; scope)

sitemap-orphan-audit.md (149 lines, 13065 B):

| line | form | ids contributed | scope |
|---|---|---|---|
| 1 `source:` | literal list | S001,S002,S004,S006 | "for the r20 artifact-membership corrections"; header also cites a pinned raw action.yml URL (non-S artifact, not a pair) |
| 2 `verified-at:` | **range `S001-S006`** (ASCII hyphen) | S001–S006 (6, expansion adds S003,S005) | "r20 S001-S006 quote corrections 2026-10-19, base cb807bc"; header declares historical-not-live-reverified |
| 120 | literal pair | S001,S004 | correction to base line 14: zero-orphan must be checked against deployed artifact/build output |
| 121 | literal pair | S001,S004 | base line 18: no-orphan conclusion conditional on artifact comparison |
| 122 | literal list | S001,S002,S004,S006 | base line 21: upload-pages-artifact excludes .git/.github; v4 hidden-path default; v5 include-hidden-files |
| 123 | literal pair | S001,S004 | base line 25: deleted paths depend on deployed artifact |
| 124 | literal list | S001,S002,S004,S006 | base line 28: artifact can be subset/build output, served set ≠ origin/main |
| 125 | literal pair | S001,S004 | base line 32: [INFERENCE] listing-only residual unestablished |
| 126 | literal pair | S001,S004 | base line 38: [INFERENCE] artifact may include paths not in sourceDir |
| 127 | literal pair | S001,S004 | base line 112: [INFERENCE] workflow build output may differ from checkout |
| 149 EOF recheck | literal list (4 IDs twice in prose) | S001,S002,S004,S006 | round-26 recheck of lines 120-127; also `rechecks/S0NN.json` glob = placeholder, not an id |

Non-IDs: `S0NN` (receipt-path placeholder, both files), `S0` substring of it, and words `SHA256/SOURCES/STALE/Same/Sources/Surface`.
`s 2026` at L93/L138 is prose ending in "s" + year. Em dashes in this file are punctuation only; **no** en-dash/em-dash/`..`/`to`/`through` S-range exists.

speedrun-pipeline.md (99 lines, 10738 B):

| line | form | ids contributed | scope |
|---|---|---|---|
| 1 `source:` | literal list | S001,S002,S004 | "for the round-20 upload-artifact correction"; header also lists webzites paths and r18 absence flags (non-S) |
| 2 `verified-at:` | literal | S019 | "metadata contract S019" — **outside inherited32 population** (own-work row) |
| 70 | literal list | S001,S002,S004 | correction to base line 36: uploaded artifact is not the full checkout |
| 99 EOF recheck | literal list | S001,S002,S004 | round-26 recheck of line 70; `rechecks/S0NN.json` glob = placeholder |

Non-IDs: `S0NN`, `s 2026` (L7,8,13,15), `s 300000` (L19 `--interval-ms 300000`), `SIGINT`, `STALE`, `Stages`, `SPEEDRUN`.
En dash at L17 is the stage range "1–3 / 4–6", not an S-range.

## B. Pair disposition (manual census)

| pair | frozen57 | r26 ledger | frozen16 | occurrence lines |
|---|---|---|---|---|
| S001 × sitemap | yes | yes (8 statements, stale 0) | no | 1, 2(range), 120-127, 149 |
| S002 × sitemap | yes | yes (2) | no | 1, 2(range), 122, 124, 149 |
| **S003 × sitemap** | yes | **no** | **yes** | **2 only (range expansion)** |
| S004 × sitemap | yes | yes (8) | no | 1, 2(range), 120-127, 149 |
| **S005 × sitemap** | yes | **no** | **yes** | **2 only (range expansion)** |
| S006 × sitemap | yes | yes (2) | no | 1, 2(range), 122, 124, 149 |
| S001 × speedrun | yes | yes (1) | no | 1, 70, 99 |
| S002 × speedrun | yes | yes (1) | no | 1, 70, 99 |
| S004 × speedrun | yes | yes (1) | no | 1, 70, 99 |
| (S019 × speedrun) | n/a — S019 ∉ population | n/a | n/a | 2 |

Located support (each ≤25 words, exact current bytes):
- sitemap L1: `S001, S002, S004, S006 (corpus/SOURCES.md) for the r20 artifact-membership corrections`
- sitemap L2: `r20 S001-S006 quote corrections 2026-10-19, base cb807bc` — the only text grounding S003/S005
- sitemap L122: `check the deployed artifact/build output rather than assuming full-tree coverage — S001, S002, S004, S006`
- sitemap L149: `The round-20 correction lines in this entry cite S001, S002, S004 and S006 (lines 120-127)`
- speedrun L1: `S001, S002, S004 (corpus/SOURCES.md) for the round-20 upload-artifact correction`
- speedrun L2: `metadata contract S019`
- speedrun L70: `v4 excludes hidden paths by default (v5 adds include-hidden-files) — S001, S002, S004`
- speedrun L99: `The round-20 correction lines in this entry cite S001, S002 and S004 (line 70)`

## C. Additional-obligation check (explicit)

- No population pair from either file falls outside frozen57. My independent enumeration of the full blobs yields
  exactly 9 population pairs here and 57 corpus-wide; frozen `c1-before.json` reports `citingPairs 57`, `decided 41`,
  `missing 16`, `findings []`, and 16+41 = 57 with both sets ⊆ mine and disjoint.
- The metadata-dismissal trap: `(S003, sitemap)` and `(S005, sitemap)` exist **only** inside the `verified-at`
  header range `S001-S006`; no correction bullet names S003 or S005. They are already obligations (frozen16 items
  3 and 7) precisely because the contract denominator INCLUDES historical metadata/EOF prose. Do not re-file them as
  discovered pairs; do not drop them as "metadata".
- If any seat's denominator omits either header pair, that omission is the additional obligation. At base 83528f7,
  frozen57 does not omit them.

## D. Out-of-population references (separate ledger, not pairs)

- **S019** — speedrun-pipeline.md L2, scope "metadata contract S019" (`corpus/SOURCES.md:27`, own-work corpus-contract
  audit, mined 2026-10-20). Not in r26 population ("S001–S034 minus own-work S014/S019", SOURCES.md:79). Not a citing
  pair under the frozen denominator and not counted in 57. If L1 ever widens the population to full SOURCES.md, this
  becomes a discovered pair and the C1 denominator grows (57 → 58) — named, not admitted here.
- S014 and S035: **absent** from both files (token sweep `\bS\d+` and `S[A-Za-z0-9]+`).

## E. Parser comparison (performed after the manual census)

- `count_c1.py` at base 83528f7 reproduces `c1-before.json` byte-for-byte in its decision fields: citingPairs 57,
  decided 41, missing 16, findings 0; missing set == all 16 `c2-oracle.json` expectedPairs (exit 1).
- For these two files the parser's pair set equals the manual set: 6 (sitemap) + 3 (speedrun); the range expands
  S001..S006 and dedupes against the four literals on L1. The 16 missing list is exactly the frozen oracle, so the two
  header-range-only sitemap pairs are already detected.
- Parser limits observed, none biting here: `\bS(\d{3,})\b` cannot see placeholders (`S0NN`), lowercase/short ids,
  slash-separated ("S001/S006") or ellipsis ranges; the files contain no such citing form. Unicode dash support
  (en/em) is unused here — the only S-range is ASCII. Case sensitivity correctly excludes `SOURCES`, `SHA256`, `STALE`.
- Interpretation caveat: `S001-S006` is a *quote-correction set* statement, not an entailment that each of the eight
  correction bullets rests on all six sources (bullets cite only {S001,S004} or {S001,S002,S004,S006}).
  Any HOLD for S003/S005 must be scoped to set membership in the r20 quote corrections, never to the zero-orphan claim.

## F. Uncertainties

- Whether `(S019, speedrun-pipeline.md)` should be admitted is an L1 population decision; this seat records it and does
  not count it, so no denominator change is asserted.
- C1's after-state cannot be assessed from this seat: `.ufo/waves/round-27/pairs.json` and `discovered-pairs.json` were
  absent at measurement (0 newDecided), so author additions are not yet visible.
- Base-line labels inside correction bullets (`...md:14`, `:21`, `:112`, …) are base-commit coordinates, not current
  line numbers; conflating them would mis-locate the cited claim.

## G. Evidence

- `corpus/knowledge/sitemap-orphan-audit.md` SHA256 `553ad1006e9e5800668afb033cd655b5d938fe1736b769dd9d82a3019268a0ec`
  (13065 B; equals `frozen/expected.json`; blob `45648e9ddb6209edad04dc4882dc8ac88fdade0c`).
- `corpus/knowledge/speedrun-pipeline.md` SHA256 `ad7919efea94596bbcb1530bec694d050853511b1eee9cea2ea53165cf5114bd`
  (10738 B; equals `frozen/expected.json`; blob `ec8e4ba8e112c84232497e47aefd9a28e308fdf6`).
- Reproduced C1 output: `/fast/scratch/hyaku/kake-r27/CitingSweep12/c1-rerun.json` (scratch only).
- Ledger cross-check: `.ufo/waves/round-26/statements.json` (41 pairs, 9 files; 7 of them in these two files).
No install, no pacman, no service mutation, no network, no source/ledger edit.

Report: .ufo/waves/round-27/w1/CitingSweep12.md
