# SentinelLargeFiles — round-50 evidence-size census

Round 50 wave 1 leaf seat (calibration). Read-only census of evidence file
sizes under `.ufo/waves/round-50/`, plus confirmation of the inherited
uncommitted large-file sets that must stay uncommitted. Nothing was modified
or deleted. Surveyed 2026-10-24.

## Method

```
find .ufo/waves/round-50 -type f -printf '%s\t%p\n' | sort -n
find .ufo/waves/round-50 -type f -size +1048576c -printf '%s\t%p\n'
find .ufo/waves/round-48/assimilation/validate -type f -size +1M -printf '%s\t%p\n' | sort -n
find .ufo/waves/round-46/residual -type f -printf '%s\t%p\n' | sort -n
jj status                      # untracked-path confirmation (read-only)
git status --porcelain         # uncommitted confirmation (read-only)
```

Threshold used: 1 MiB = 1,048,576 bytes (`find -size +1048576c`). The nine
round-48 copies are also caught by `-size +1M` (find rounds to MiB); all nine
exceed 1,283,159 bytes so the choice of threshold does not change the set.

## Round-50 census result

- Total files under `.ufo/waves/round-50/`: **170**
- Total size: ~3.1 MiB (`du -sh` = 3.1M)
- Files **above 1 MiB: 0** — no oversized evidence in this round.

Largest five files (bytes, path):

| Bytes | Path |
|------:|------|
| 343,167 | `.ufo/waves/round-50/assimilation/pre-append/SCORECARD.md` |
| 193,275 | `.ufo/waves/round-50/sources/S286.raw.html` |
| 163,613 | `.ufo/waves/round-50/assimilation/pre-append/corpus/knowledge/accessibility-review-cards.json` |
| 154,245 | `.ufo/waves/round-50/sources/S286.txt` |
| 133,780 | `.ufo/waves/round-50/assimilation/pre-append/corpus/SOURCES.md` |

Full ordering by size was taken with `find -printf '%s\t%p\n' | sort -n`;
the smallest entries are 0-byte guards (`assimilation/guard/guard-col0`,
`assimilation/pre-append/census-stderr.txt`). No file approaches the 1 MiB
line — the largest is ~335 KiB.

## Inherited set 1: nine >1 MiB copies under round-48 validate

`find -size +1M` under `.ufo/waves/round-48/assimilation/validate/` returns
exactly **nine** files, matching the bound:

| Bytes | Path (relative to `.ufo/waves/round-48/assimilation/validate/`) |
|------:|------|
| 1,283,159 | `.ufo/waves/round-42/controls/w1/CtlCache/ctl_accept_table_seed4242.py` |
| 1,508,774 | `.ufo/waves/round-39/sources/xmlschema11-2.html` |
| 1,508,774 | `.ufo/waves/round-40/sources/xmlschema11-2.html` |
| 1,652,267 | `.ufo/waves/round-41/realrun/sitemaps/nodejs.xml` |
| 1,808,836 | `.ufo/waves/round-36/realrun/snap-bodies-run2.tar.xz` |
| 1,811,344 | `.ufo/waves/round-36/realrun/snap-bodies.tar.xz` |
| 2,355,487 | `.ufo/waves/round-21/anchors-fixed.json` |
| 2,777,011 | `.ufo/waves/round-37/sealed/cases.json` |
| 4,620,210 | `.ufo/waves/round-41/realrun/sitemaps/postgresql.xml` |

All nine are listed as `??` untracked in `jj status` / `git status
--porcelain` — present on disk, uncommitted. Left untouched.

## Inherited set 2: eight residual reports under round-46

`.ufo/waves/round-46/residual/` contains exactly **eight** files:

| Bytes | File |
|------:|------|
| 1,335 | `SentinelBounds.md` |
| 5,090 | `CriticMatrixBlindness.md` |
| 6,633 | `ScoutSiblingOverlap.md` |
| 10,722 | `CriticCitationOverreach.md` |
| 14,304 | `ReviewReceiptIdentity.md` |
| 14,369 | `MutationSemanticsGap.md` |
| 16,258 | `ReviewQualityCriterion.md` |
| 18,737 | `ReviewWitnessOracle.md` |

The whole directory is untracked (`?? .ufo/waves/round-46/residual/`),
`git ls-files` on it returns 0, and no ignore rule covers it — it is
orchestrator-owned and stays uncommitted. Left untouched.

## Other uncommitted round-50-adjacent paths seen in the same status sweep

For calibration context only (not part of either protected set, no action
taken): `?? .ufo/waves/round-50/append_s286.py`,
`?? .ufo/waves/round-50/w1/` (this report's own directory),
`?? corpus/knowledge/crawl-error-status-table.md`,
`?? corpus/lessons/round-50.md`, and `M corpus/QUALITY.md` (jj working-copy
change). All other round-50 instrument files (`contract.json`,
`c50_quote_class.py`, `c50_durable.py`, `route-map.json`, etc.) are already
tracked — `git ls-files` on `.ufo/waves/round-50` returns 157 paths.

## Calibration notes

- Both frozen instruments were run as controls during this seat's sweep.
  C1 at base `9619af67` → `classed 0/3 met=False` (ledger and S286 row
  absent); C1 at pre-append `33eec7f2` → `classed 0/3 met=False` (class
  ledger now present, lessons still absent — correct discrimination between
  the two revisions). C2 at base → `durable 0/1 met=False` with all four
  checks failing. The instruments discriminate; the do-nothing base reads
  unmet on both claims as declared in `contract.json`.
- No file under `.ufo/waves/round-50/` needs size quarantine; the wave's
  evidence footprint (3.1 MiB across 170 files) is dominated by the
  pre-append mirror tree, not by new blobs.

Report: .ufo/waves/round-50/w1/SentinelLargeFiles.md
