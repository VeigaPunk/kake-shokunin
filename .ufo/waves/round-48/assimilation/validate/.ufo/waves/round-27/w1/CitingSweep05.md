# CitingSweep05 — r27 citing-set completeness data-walk (freshness files)

Seat: KakeR27.CitingSweep05 (leaf, read-only findings). Round 27, wave 1, milestone r27-full-citing-set.
Targets, exactly: `corpus/knowledge/freshness-sidecar.json`, `corpus/knowledge/freshness-sweep.md`.
Revisions: frozen base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`; declarations `be375d90afc6fc7aca369ab3cf5247bf460aeed2`.
No source/public-site evaluation; no tool installs; no production edits; scratch only `/fast/scratch/hyaku/kake-r27/CitingSweep05/`.

## Method and ordering

1. Manual census of both files (grep plus broader `S[+digits]` and case-insensitive form scans) — completed before any parser run.
2. Parser probe: `count_c1.py:4-5` LITERAL/RANGE regexes applied to exactly these two files.
3. Independent full-corpus pair recomputation under the contract grammar, intersected with the frozen 32-row population.
4. Only then compared with `count_c1.py`, `c1-before.json` (16 missing), `c2-oracle.json`, `frozen/ledger.json`.

## 1. Manual census — every source-id reference

`freshness-sweep.md` (15,358 bytes, 201 newline-split lines):

| line | form | id | scope | located support (≤25 words) |
|---|---|---|---|---|
| 1 | literal, provenance header | S014 | principal source of the whole entry; script/pins/round-20 proof method | `source: S014 in corpus/SOURCES.md` (4w) |
| 1 | literal, provenance header | S019 | metadata authority only; explicitly not platform verification | `Metadata authority only: S019 in corpus/SOURCES.md, not platform verification.` (9w) |
| 2 | literal, `verified-at` header | S014 | historical round-20 correction/run; “historical, not live-reverified” | `round-20 citation-local correction and S014 run` (6w) |
| 3 | literal, row-reference alternate (“the S014 row”) | S014 | conditional recheck: retire entry and SOURCES row if script absent | `retire this entry and the S014 row` (7w) |
| 182 | literal, appended Round-20 resume note | S014 | own-work source row, tier A, lane citation resolution only | ``Source row: S014 in `corpus/SOURCES.md` (own-work, tier A for lane citation`` (11w) |

All five tokens are on these four lines; no other `S`+digit token exists in the file.

EOFs/notes checked explicitly:
- Final EOF block, `## Round-24 reconciliation and preservation` lines 191–201: **zero** S-ids. It references the sidecar path at line 197, `.ufo/waves/round-24/c1-population.json` at 193, and `w1/ScoutMistakeSweep.md` at 201 — path/artifact references only.
- Line 182 is inside the earlier appended Round-20 resume note (180–188), not the final EOF block; scope differs from the header (lane citation resolution only).

`freshness-sidecar.json` (15,616 bytes, 275 lines): **zero** S-id tokens. A regex probe of every line for `\bS(\d{3,})\b` returned no match; `lineSha256` keys and lowercase hex hashes produce none.

Form sweep over both files — every `S`+digit token found was exactly `S014` (4×) and `S019` (1×). Absent by observation: ranges with S at both ends (hyphen/en-dash/em-dash/`..`/`to`/`through`), grouped or slash lists, `S-014`/`S 014`/`S014a`, lowercase, and any `S035`.

## 2. Population intersection and pair result

- Frozen `population.json` (r26 and round-27 frozen copy): 32 ids = S001–S034 minus own-work S014/S019. `corpus/SOURCES.md:79` states: `the 32 previously opened external rows (S001–S034 minus own-work S014/S019)`.
- Membership test on all five tokens: S014 ∉ population, S019 ∉ population. Therefore **both target files contribute 0 citing pairs**, 0 inherited32 pairs, and **no additional obligation** under the frozen denominator. `freshness-pins.json` also contributes 0.
- Independent recomputation with the contract grammar reproduces **57 pairs** across nine files: crawl-scope-per-host 4, ghp-custom-domain 4, ghp-etag-anatomy 3, ghp-served-set 6, ghp-subpath-spotcheck 2, publish-channels 7, sitemap-orphan-audit 6, speedrun-pipeline 3, static-canonical-preflight 22. No freshness file appears.
- Decided 41 = r26 `statements.json` pair set = frozen ledger pair set (verified set-equal). Missing 16 = independent (pairs − decided) = `c1-before.json` missing = `c2-oracle.json` `expectedPairs`; 41 + 16 = 57.
- Outside-population references, recorded separately (not counted in 57): `(S014, corpus/knowledge/freshness-sweep.md)` with the four distinct scopes above, and `(S019, corpus/knowledge/freshness-sweep.md)` at line 1. If own-work rows were admitted, the denominator would grow 57→59, one pair per file/id regardless of occurrence count.
- `S035`: zero references in either target. Corpus-wide, S035 is cited only by `corpus/knowledge/accessibility-review-packet.md` (lines 1, 3, 88, 155) — outside these files and outside the population.

## 3. Parser comparison (after the manual census)

- `count_c1.py` regexes on the targets match the manual census exactly: line 1 `{S014,S019}`, line 2 `{S014}`, line 3 `{S014}`, line 182 `{S014}`; RANGE matches none. No false positive or false negative in these files.
- `count_c1.py` at base: population 32, citingPairs 57, decided 41, missing 16, findings `[]`. Rerun at `be375d9`: identical except the printed revision string; `git diff --stat 83528f7..be375d9 -- corpus/knowledge` is empty.
- `c1-before.json` 16-pair list equals `c2-oracle.json` `expectedPairs` exactly; oracle `expectedExit` 1, `expectedCount` 16, `falsePositives` 0; finding id `unadjudicated_citing_pair`.
- `scripts/citing_set.py` is absent at `be375d9`; `c2-before.json` records `gate_absent`, expected 16 / detected 0. C2 construction is not this seat's work.

## 4. Evidence integrity

- `git diff --stat 83528f7..be375d9 -- corpus/knowledge`: empty; both targets are byte-identical to the frozen revision.
- `freshness-sweep.md` sha256 `c272840537debc4ce3fdbc440642a857160b11dba8237560ec7b1a6e398a7dbe` — equals `frozen/expected.json` entry.
- `freshness-sidecar.json` sha256 `b09849f0698db1d81ca6218a316c3dde729c6a8294d209cb793868f6d0a974ac` — equals `frozen/expected.json` entry.
- `frozen/expected.json` sha256 covers all 26 knowledge files plus `ledger.json` and `population.json` (28 entries), matching the frozen tree.

## 5. Supplemental — sidecar’s own bindings (not source-id references)

- Schema `kake-paths-sidecar-v1`; 30 entries: 4 `absent`, 26 `restored`; all dated 2026-10-21; file distribution 17 corpus/knowledge, 10 SKILL.md, 3 corpus/lessons; no entry binds either target file.
- All 30 `lineSha256` digests match the bound line’s current text hashed **without** trailing newline; 0 out-of-bounds lines; 0 duplicate `(file,line,token)` keys; every file passes the validator’s path predicate.
- Token/line check: 21 entries contain the literal token; 9 bind a line spelling the path as `/home/vgpnk/...` while the entry token is `~/...`. The validator canonicalizes absolute→tilde before comparison (`scripts/freshness-sweep.mjs:340-346`, `367-373`), so these are accepted forms; a literal-substring checker would spuriously report 9 failures. This is code reading, not an executed gate.
- Kind vs local presence (`test -e`, no public site contacted): 4 absent tokens missing, 26 restored tokens present, 0 disagreements. Local filesystem observation only.

## 6. Uncertainties and residual gaps

- The S014/S019 exclusion is definitional (`SOURCES.md:79`), not evidence that those rows lack support. Whether own-work rows belong in C1 is a contract decision.
- `SOURCES.md:27` lists S019 `usedBy` as `corpus/lessons/round-21.md` only, while 16 knowledge files carry 17 S019 metadata-authority occurrences (16 on provenance-header lines 1–2; `kimi-subpath-audit.md:3` is the exception), including `freshness-sweep.md:1`; S014’s `usedBy` does name `freshness-sweep.md` (`SOURCES.md:22`). Observed metadata omission; no source-support verdict.
- Pair granularity is file-level: the four S014 scopes (principal / historical run / conditional retirement / resume note) collapse to one pair. Any later adjudication must cover the four scopes separately.
- Grammar boundary: literals require S + ≥3 digits and ranges require S at both ends. Neither file contains an out-of-grammar alternate, but no corpus-wide “no valid form missed” claim is made here; the full recomputation reused the same frozen grammar.
- No source or SOPS evaluation performed, per lane bounds.

## Verdict (scope-limited, factual)

- Census complete for both files: 5 S-id tokens, 2 unique ids, all in `freshness-sweep.md`; zero in `freshness-sidecar.json`; 0 ranges, 0 grouped/slash lists, 0 other spellings (`S-014`/`S 014`/`S014a`/lowercase), 0 S035.
- Inherited32 pairs from these two files: **0**. Frozen57 is not enlarged; no additional obligation is named from these files.
- S014 (4 scopes) and S019 (metadata-authority scope) are recorded as out-of-population references; admitting them would move 57→59, not silently change 57.
- Manual census, `count_c1.py`, `c1-before.json` 16-list, `c2-oracle.json`, and the frozen ledger agree within this scope; no discrepancy found to report.
- No production edits. This report is the only write: `.ufo/waves/round-27/w1/CitingSweep05.md`.
