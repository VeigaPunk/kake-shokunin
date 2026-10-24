# CitingSweep09 — blind source-id census, mirror-pitfalls.md + ops-automation.md

Seat: KakeR27.CitingSweep09 (leaf, read-only). Target repo /home/vgpnk/Projects/shokunin/kake-shokunin.
Measured at frozen base 83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba and declared HEAD be375d90afc6fc7aca369ab3cf5247bf460aeed2.
No production edits, no other file writes. Scratch: /fast/scratch/hyaku/kake-r27/CitingSweep09/ (c1-base.json, c1-head.json, c1-base.err empty).
No tool install/update needed this seat.

## Verdict

- Inherited32-population citing pairs contributed by these two files: **0**.
- Additional obligations against the 57-pair citing set: **none** — neither file contains any inherited-population id (S001–S013, S015–S018, S020–S034) in literal, grouped, range, alternate, header or EOF form.
- Out-of-population references found, recorded separately and **not dismissed as metadata**: `S019` once in each file, line 1 provenance header, scope "metadata authority only". S019 is a real SOURCES.md row (own-work, Tier A) but is excluded from the frozen 32-row population.
- S014 / S035: zero occurrences in either file (all citation-shaped scans below).
- Parser/counter agreement after the manual census: 57 citing pairs / 41 decided / 16 missing at both revisions; the 16 list is byte-equal (ordered) to the frozen C2 oracle; neither target file appears in any pair, outcome, or missing row.

## Files measured (byte identity)

| file | lines | bytes | sha256 | base=HEAD | worktree |
|---|---|---|---|---|---|
| corpus/knowledge/mirror-pitfalls.md | 72 | 6790 | 5372649953bb8d9b737726f97cbdf6331be6577a613e14a7bb56555aba5b2ccd | yes (diff base..HEAD empty) | same |
| corpus/knowledge/ops-automation.md | 141 | 13393 | 843d779d09c2118ca4a320130e65b43bd6f7fbda37b537bf12eb04f849fddac7 | yes (diff base..HEAD empty) | same |

Both hashes equal the frozen C2 snapshot pins in .ufo/waves/round-27/frozen/expected.json.

## Manual census (done before touching the counter/oracle comparison)

Method: read each file end-to-end; then an independent scanner over the base-revision blobs using (a) the contract's literal/range regexes, (b) six permissive alternates (case-insensitive, optional separators, unicode digits, `S0NN` placeholders, descending/`to`/`through`/`..` ranges, comma/slash/`&` groups), (c) a capital-S token dump of every line, (d) an incidental `S<digits>` context dump.

Every source-id reference found, with line and scope:

| # | file:line | form | exact text (≤25 words) | id | scope | population | C1 pair |
|---|---|---|---|---|---|---|---|
| 1 | corpus/knowledge/mirror-pitfalls.md:1 | literal, single | "Metadata authority only: S019 in corpus/SOURCES.md, not platform verification." | S019 | entry `source:` provenance header; metadata authority only, explicitly not platform verification | NOT in 32-row pop | none |
| 2 | corpus/knowledge/ops-automation.md:1 | literal, single | "Metadata authority only: S019 in corpus/SOURCES.md, not live automation verification." | S019 | entry `source:` provenance header; metadata authority only, explicitly not live automation verification | NOT in 32-row pop | none |

That is the complete list. No grouped lists (`S001, S002…`), no ranges (`S001–S006`, `S001..S006`, `S001 to S006`, `S001 through S006`, hyphen/en-dash/em-dash), no slash/`&`/`+` groups, no descending or >200-span ranges, no `S0NN` placeholders, no lowercase/unicode-digit variants, no ids in HTML comments or EOF prose. Both EOF tails were read in full:
- mirror-pitfalls.md:68–72 "## Round-24 path reconciliation" — no source id. Contains a self-coordinate `corpus/knowledge/mirror-pitfalls.md:63` (line 72), `corpus/knowledge/freshness-sidecar.json`, and checkout prefix `1fbdb8ed`; none is an S-id.
- ops-automation.md:130–141 "## Live re-verification — round 23 (2026-10-21)" and c1–c7 (lines 134–141) — no source id; only local paths, systemctl/journalctl surfaces and claim labels.

Non-source citation-shaped material enumerated (checked so absence is not inferred from a skipped region):
- mirror: line 1 named paths `kimi-surface-ops.md`, `fleet.dedupe-report.md`, `ufofsdbeta`; line 3 `recheck:` git-show command; line 7 `Sources:` named-path list; fire-target ids `1a0c20ea-6372…`/`1a049cb5-47d2…`; claim labels `[mirror-pitfalls:c1]`…`[c6]` (lines 60–65).
- ops: line 1/3/7 named systemd units, `probe-history.jsonl`, `webzites.mjs`, HTML comment `r18 re-census` at line 7; question labels `PQ-12` (line 53) and `PQ-7` (line 65); history-row numbers `77`/`78` (lines 27–28) and "rows 2–12" (line 61), "lines 73–75" (line 103) — probe-log rows, not source ids; claim labels `[ops-automation:c1]`…`[c7]` (lines 134–141).
- Incidental case-insensitive `S<digits>` regex hits were context-classified: `ds4cc` path fragments (`s4`, mirror:36/63/72, ops:114), `--ttl-ms 900000` (mirror:40), ISO dates (`s 2026`, ops:2/7/8/50), and plural-word endings before numbers (`rounds 1–4`, `median is 0.26h`, `rows 2–12`, `ws 3`, `lines 73–75`, `across 26`, `52 events`). None is a source-id reference.

## Parser / counter comparison (only after the census above)

Independent reconstruction from the base tree (same regex semantics as count_c1.py, population intersected):
- 57 citing pairs across 9 files: static-canonical-preflight.md 22, publish-channels.md 7, ghp-served-set.md 6, sitemap-orphan-audit.md 6, ghp-custom-domain.md 4, crawl-scope-per-host.md 4, speedrun-pipeline.md 3, ghp-etag-anatomy.md 3, ghp-subpath-spotcheck.md 2.
- Contribution of the two target files: **[] and []** (zero). Rows uncited in population: S015–S018 (unchanged by this sweep).
- sha256 of sorted `[[row,file],…]` for the 57: `8d97c0e29333d2c2829184c36ab6623233c86bd1522eecedfcbcea165669ce7f`.

Frozen counter run `python3 -B .ufo/waves/round-27/count_c1.py --root . --revision <rev>` (TMPDIR under seat scratch):
| revision | population | citingPairs | decided | missing | target outcomes | missing sha256 |
|---|---|---|---|---|---|---|
| 83528f7 (base) | 32 | 57 | 41 | 16 | [] | 90a90b3cc381760734a68bf26a4b95d0557caa987f1194e0dbbcc3b8c6512d54 |
| be375d9 (HEAD) | 32 | 57 | 41 | 16 | [] | same list, byte-identical |

- c1-before.json (af55d0a4…) matches both runs exactly: `missing` 16 rows, files = crawl-scope-per-host.md, ghp-custom-domain.md, ghp-etag-anatomy.md, publish-channels.md, sitemap-orphan-audit.md, static-canonical-preflight.md; neither target file present.
- c2-oracle.json `expectedPairs` compares equal as an ordered list to c1-before `missing` (16/16); hash of `[[row,file]]` for both = `90a90b3c…` (same as above). Oracle sha256 `1d038205…`.
- c2_count.py's reported pre-state (`c2-before.json`: revision be375d9, detected 0/16, `gate_absent`) is consistent with the frozen set; not re-run as a gate (no gate file in lane).

Agreement statement: parser and manual census agree that both files contribute zero inherited-population pairs. The parser does match the `S019` token (literal group `019`, line 1) in both files; exclusion is solely the population filter (`f'S{19:03d}' in pop` is false), not a missed form and not a metadata dismissal. No parser blind spot was found for these files.

## Out-of-population references (recorded separately, denominator not shrunk)

- `S019` × mirror-pitfalls.md:1 — metadata authority only; platform verification disclaimed.
- `S019` × ops-automation.md:1 — metadata authority only; live automation verification disclaimed.
- S019 provenance: corpus/SOURCES.md:27, kind own-work, Tier A, "Local provenance-field and lesson-heading census only; no verification of historical platform claims"; `usedBy` cell = `corpus/lessons/round-21.md` only.
- Population boundary: frozen 32 rows = S001–S013, S015–S018, S020–S034; S014, S019 and S035 are absent by construction (own-work exclusions S014/S019; S035 later). Therefore these two citations are outside C1's frozen denominator.
- Monotone-denominator disclosure: if L1 ever admits S019 to the population, the citing set would grow by exactly two named pairs — (S019, corpus/knowledge/mirror-pitfalls.md) and (S019, corpus/knowledge/ops-automation.md). Not counted now; named so the denominator cannot later shrink silently.
- Observed metadata asymmetry (no C1 effect): SOURCES.md S019's `usedBy` does not list either target file even though both cite S019; inverse usedBy is not a citing form under the frozen rule.

## Freshness notes (observed text only; no source/public-site evaluation performed)

- mirror-pitfalls.md:63 `[mirror-pitfalls:c4]` **STALE**: both /home/vgpnk/Projects/{plazir-15-site,ds4cc-marketplace}/speedrun "does not exist"; mirror-pitfalls.md:72 (Round-24 note, newer) says ~/Projects/ds4cc-marketplace/speedrun "present (test -e exit 0; checkout 1fbdb8ed)". Internal supersession contradiction recorded as text; not adjudicated here. No S-id involved.
- ops-automation.md:134–137 four **STALE** corrections (probe timer, keeper timer, probe-history.jsonl, webzites.mjs) and 138–141 three **UNVERIFIABLE**; no S-id involved.
- Both files' `source:`/`verified-at:`/`recheck:` headers (lines 1–3) carry no ids beyond the S019 note in `source:`.

## Inputs opened (sha256)

contract.json `6d2d7f51…`; count_c1.py `a1e46d19…`; c2_count.py `93f39b0f…`; c2-oracle.json `1d038205…`; c1-before.json `af55d0a4…`; frozen/expected.json `628b7a05…`; frozen/population.json `16330e1e…`; frozen/ledger.json `c2026376…` (41 pairs; key `verdict` absent — ledger uses stale/seat* fields; no target-file hits).

## Uncertainties / residual unknowns

- Whether S019 metadata citations should ever become obligations is an L1 population-admission decision; outside this seat's rule. If admitted, the two pairs above are the complete addition from these files.
- C1's frozen rule is S-id/regex-based by design; named-path evidence pointers (`kimi-surface-ops.md`, `fleet.dedupe-report.md`, `webzites` units, `probe-history.jsonl`) carry no S-id and are not pairs under that rule.
- `discovered-pairs.json` and `pairs.json` were absent at measurement time (count_c1 treats them as optional); this sweep found no discovery to add for these files.
- No build/lint/test/formatter run; no production or index/Git/jj mutation. Report is the only write.

## Checks L1 should run at integration

`python3 -B .ufo/waves/round-27/count_c1.py --root . --revision <candidate>` and confirm citingPairs stays ≥57, the two target files still have zero pairs (or exactly the two S019 pairs if population is deliberately widened), and the 16-row missing set is unchanged unless other seats adjudicate it.
