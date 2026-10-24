# ExcludedPopulation — inherited 32-row population, excluded ids, freshness scope

Seat `KakeR27.ExcludedPopulation` (read-only leaf). Axis judged: freshness. Milestone: r27-full-citing-set.
Frozen base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`; declarations `be375d90afc6fc7aca369ab3cf5247bf460aeed2`.
Everything here is author-side peer evidence; the parent judges independently. No production/oracle/ledger/gate edits,
no tool installs, no r24 stopped work opened. Scratch: `/fast/scratch/hyaku/kake-r27/ExcludedPopulation/`.

## Verdicts (summary)

- V1 population: CONFIRMED exactly 32 rows = S001–S034 minus S014/S019; S035 absent; byte-identical to the r26 population at base.
- V2 excluded ids in `corpus/knowledge`: 25 occurrences in 17 files, forming 18 excluded `(row,file)` pairs (§2).
- V3 universal freshness: NO — population-scoped, pair-scoped, knowledge-file-scoped (§3).
- V4 omitted inherited-population citations: NONE under the frozen grammar (57 exact at base and HEAD); one wider-grammar
  pair exists and is already registered `discovered` 57→58 (§4).

## 1. Population audit

- `.ufo/waves/round-27/frozen/population.json` sha256 `16330e1effd5ee52665f8f31738e9423c6ec387e5d4a1404c5bcc35f69d01b03`,
  byte-equal to `git show 83528f7c:.ufo/waves/round-26/population.json`. `rows` = 32, sorted, unique; exact ids:
  S001–S013, S015–S018, S020–S034. `baseline` field is `97404de4…f006` (r26 pre-round), not the r27 base.
- Absent ids: S014, S019, S035. `SOURCES.md` has 35 registry rows, so the population is 32 of 35.
- Provenance of the rule: `.ufo/waves/round-26/contract.json:14` “`.ufo/waves/round-26/population.json` — S001..S034
  minus own-work S014/S019; S035 (opened r25) excluded” (15 words); `.ufo/waves/round-26/fetch_sources.py:20`
  “`EXCLUDED = {'S014', 'S019', 'S035'}  # own-work rows and the source opened last round`” (14 tokens);
  `.ufo/waves/round-26/w1/LessonScribe.md:63` “Excluded from this gate: S014 and S019 (own-work), S035 (opened round
  25; its round-25 Gate stands unchanged unless a later round rechecks it)” (23 words).
- Included-but-uncited rows: S015/S016 `status=queued`, S017/S018 `status=rejected`, all four `usedBy='—'`
  (population.json). They are in the 32 but have zero knowledge citing pairs, so only **28 population rows** carry pairs.
- Registry facts for the three excluded rows (`corpus/SOURCES.md:22,27,43`): S014 kind `own-work`, tier A, scope
  “Lane citation-local filesystem-path freshness gate” (6 words); S019 kind `own-work`, tier A, scope “Local
  provenance-field and lesson-heading census only; no verification of historical platform claims” (13 words),
  canonical input an absolute path outside this repo; S035 kind `spec`, tier A, scope “Publisher-side manual-review
  preparation for WCAG 2.2 Level A and AA, not website conformance” (15 words), “opened 2026-10-21; saved source
  SHA256 `6e3c5fe3…7057`”, recheck `on-release`.
- Reproduced C1 (`count_c1.py`, working-tree hash `7489865d…160d`; committed hash `a1e46d19…a14c`): base 83528f7 and
  declarations be375d9 both → 32 population / **57 citingPairs** / 41 decided / 16 missing; `c1-before.json`
  (`af55d0a4…6e3c`) states the same 57/41/16.
- Pair set did not move inside r26: at r26 landing `e28312b` 57/25/32; at `b44daed` 57/41/16; at `a2be0dc` and base
  57/41/16. The 16 were never adjudicated in r26; r27's “before” is accurate, not an artifact of a shrinking scan.

## 2. Where the three excluded ids occur in `corpus/knowledge` — complete enumeration

25 occurrences, 17 distinct files, 18 excluded `(row,file)` pairs (freshness-sweep carries two ids).

| id | file:lines | occurrences | role |
|---|---|---:|---|
| S014 | `freshness-sweep.md`:1,2,3,182 | 4 | source header, verified-at run record, recheck command, round-20 resume note |
| S019 | 16 files, 17 occurrences (list below) | 17 | metadata-authority header / metadata contract |
| S035 | `accessibility-review-packet.md`:1,3,88,155 | 4 | source header, recheck, one normative §5.2.1 statement, recheck comparison |

S019 files and lines: `drift-detection.md`:1, `fire-journal-codes.md`:1, `fleet-registry.md`:1, `free-read-verbs.md`:1,
`freshness-sweep.md`:1, `ghp-subpath-spotcheck.md`:1,2, `keeper-timer-inert.md`:1, `kimi-subpath-audit.md`:3,
`mirror-pitfalls.md`:1, `ops-automation.md`:1, `origin-repos.md`:1, `probe-delta-alerting.md`:1,
`publish-channels.md`:1, `publish-queue.md`:1, `speedrun-pipeline.md`:2, `vault-properties.md`:1.

Located support, each ≤25 words:

- `freshness-sweep.md:182`: “Source row: S014 in `corpus/SOURCES.md` (own-work, tier A for lane citation resolution only).” (15)
- `keeper-timer-inert.md:1`: “Metadata authority only: S019 in corpus/SOURCES.md, not current service-state verification.” (13)
- `ghp-subpath-spotcheck.md:2`: “S019 in corpus/SOURCES.md governs metadata only.” (7)
- `free-read-verbs.md:1`: “metadata contract S019 (corpus/SOURCES.md, metadata authority only, not platform authority)” (10);
  `fire-journal-codes.md:1`: “metadata format per S019 (metadata authority only, not a platform source)” (11);
  `origin-repos.md:1`: “metadata contract S019 (format authority only; entry evidence is the wz-repos reports)” (13).
- `kimi-subpath-audit.md:3` and `speedrun-pipeline.md:2`: “metadata contract S019” (3 each);
  `publish-channels.md:1`: “Metadata authority only: S019, not live platform verification.” (8)
- `accessibility-review-packet.md:1`: “source: S035 — https://www.w3.org/TR/2024/REC-WCAG22-20241212/
  (success criteria 1.1.1–4.1.3; conformance requirements §5.2)” (13 tokens); `:88`: “S035 §5.2.1 requires all A
  and AA criteria for Level AA” (12); `:155`: “compare its This version URL with S035; the offline gate cannot
  observe a new online release” (19).

Pair accounting: `count_c1.py` scans these literals but keeps a pair only when the row is in the population
(`if f'S{i:03d}' in pop`), so they are visible, named exclusions — not scan misses. Widening to all registry rows gives
57 + 18 = **75** knowledge pairs (S014×1, S019×16, S035×1); with the registered discovery the inclusive figure is 76.
Excluded-id files that also carry population pairs: `ghp-subpath-spotcheck.md` (2), `publish-channels.md` (7),
`speedrun-pipeline.md` (3); the other 14 files carry none.

## 3. Why this round is not universal freshness

N1. **Population scope, not registry scope.** Denominator = 32 inherited rows ∩ knowledge pairs, per the frozen
contract: “All corpus/knowledge files at measured revision; literal S +3-or-more digits and ranges with S at both
ends” … “intersect r26 inherited32-row population” (`contract.json:12`). 35 registry rows exist; 3 are excluded;
S015–S018 have no citation. C1’s “all frozen/discovered pairs” is 57(→58) pairs, not 35 rows.

N2. **Own-work rows are not public, re-fetchable sources.** S014 is a local script; S019 is a local corpus-contract
audit whose canonical input lives in another checkout. r26 itself recites the scope: “the 32 previously opened
external rows (S001–S034 minus own-work S014/S019)” (`corpus/SOURCES.md:79`). No GET can HOLD/STALE them; their
freshness is file/commit existence, which C1 does not adjudicate.

N3. **S035 is a public tier-A spec that r27 never re-opens.** It is excluded solely because it was opened in r25
(“S035 excluded as opened in round 25”, `corpus/lessons/round-26.md:6`; same clause at
`round-26-verifier-spotcheck.md:37`). Its four knowledge occurrences include a normative statement at
`accessibility-review-packet.md:88`; the only freshness basis is round-25 retained bytes (`6e3c5fe3…7057`) and a
round-25 W2 identical-bytes report. The round-27 `fetched/manifest.json` has 8 entries, all S001–S006; no S035.
Hence r27 makes no freshness claim about the newest public source in the registry.

N4. **Pair granularity, not statement or row truth.** r26 was row-level (32 rows HOLD); r27 is pair-level. The frozen
counter discloses “Pair adjudication is not proof of truth of every underlying statement,” and UNVERIFIABLE is
explicitly not decided (`contract.json` C1 `sourceVerdict`), so a green C1 does not certify every cited sentence.

N5. **File scope.** Only `corpus/knowledge` is read. All 57 pairs live in 9 of 26 knowledge files; 17 knowledge files
cite no population id. Every corpus citation outside that directory is out of denominator by contract; e.g.
`corpus/lessons/round-26.md:6` literally contains “S001–S034” (a 34-id range if scanned). Peer `PeripheralScope.md`
reports 219 expanded outside-knowledge pairs at declarations across 22 files; I did not re-run that census.

N6. **Evidence scope: 6 of the 16 missing pairs have no round-27 fetched bytes.** Missing rows: S001×1, S002×1,
S003×2, S004×2, S005×2, S006×2, S008×4, S022×1, S023×1. `count_c1.py` resolves `kind:"source"` only from
`.ufo/waves/round-27/fetched/manifest.json`, whose rows are S001–S006. So S008×4, S022, S023 (6 pairs) cannot be
source-adjudicated now; a HOLD there must be `kind:"artifact"` (r26 bytes / SOURCES row), not a round-27 re-fetch.

N7. **Denominator/settlement identity.** `count_c1.py` reads `.ufo/waves/round-26/population.json` and
`statements.json` from the measured revision with no hash pin, while `frozen/expected.json` pins the population sha
only for C2. A candidate that edits those r26 files changes the denominator without a finding. Also disclose the
measurement identity: working-tree counter `7489865d…160d` vs committed `a1e46d19…a14c`; worktree `c2_count.py`
`e5b6fa7f…` vs committed `93f39b0f…`. My numbers use the working-tree counter; closing language should name the
counter hash and verify population sha `16330e1e…` plus ledger sha `c2026376…`.

Scope sentence the round should use: “r27 C1 freshness covers 58 population/discovered knowledge-file citing pairs
(frozen floor 57) out of 76 population-inclusive knowledge pairs; it excludes own-work S014/S019, re-opened S035, the
16-pair r26 tail, statement-level truth, and all citations outside `corpus/knowledge`.”

## 4. Omitted inherited-population citations — checked, none under the frozen grammar

- Independent strict enumeration (`\bS\d{3,}\b`, five range forms) over all 26 base knowledge blobs gives **57**
  pairs, exactly `c1-before.json` (41+16) and the 16 `c2-oracle.json` `expectedPairs`. Per-file counts: crawl-scope 4,
  ghp-custom 4, ghp-etag 3, ghp-served 6, ghp-subpath 2, publish-channels 7, sitemap-orphan 6, speedrun 3,
  static-canonical 22 = 57.
- Five ranges exist, all expanded by the frozen regex: `publish-channels.md:2` S001-S007; `sitemap-orphan-audit.md:2` S001-S006; `static-canonical-preflight.md:2` S020-S027 and S028-S029; `:54` S001–S006.
- Alternate forms probed and absent: bare-number lists (`S001, 002`), abbreviated ranges (`S001-6`), 1–2 digit ids,
  ellipsis/`thru`/U+2010-2011-2212 ranges, spaced ids, lowercase, 4+-digit ids. The three JSON knowledge files contain
  0 `S\d` tokens; `S0NN` placeholders carry no digits and add no pair.
- No carried pair is dropped: r26 `statements.json` 41 pairs and `frozen/ledger.json` 41 pairs are set-equal, all
  inside the 57; no r26 pair names a non-knowledge file.
- Wide-grammar check (contract prose omits a boundary): exactly **one** extra pair appears,
  `(S013, corpus/knowledge/ghp-served-set.md)`, from the evidence filename token “w2/Rejection07S013.md” (context:
  “entry (w2/Rejection01S001.md, w2/Rejection07S013.md)”). Other attached-prefix tokens (PairS0NN, CorrectionNS0NN,
  UncoveredS024S025, ReopenS030) already have their row in the same file’s strict set, so they add nothing.
- That pair is registered in `.ufo/waves/round-27/discovered-pairs.json` (sha256 `45e95683…03fb`, only S013), which
  says “C1 minimum obligation grows57→58 under the predeclared monotone discovery rule.” **Live denominator when
  landed = 58;** at committed HEAD it is 57 because the file is untracked and `count_c1.py` reads it via `git show`.
  No `pairs.json` exists yet, so the pair has no adjudication row and would remain in `missing` until authored.

## 5. Raises for L1 (none are production edits by this seat)

R1. Author the 58th pair as `kind:"artifact"` HOLD (or reject with reason) in `pairs.json`; a source-kind HOLD would
need an S013 fetch entry, which the round-27 manifest lacks.

R2. State excluded pairs explicitly wherever “full citing set” appears: 18 excluded pairs / 17 files (§2), and
`57`/`58` of `75`/`76` population-inclusive knowledge pairs. Do not describe 58 as all corpus citations.

R3. Do not let S035’s exclusion read as freshness coverage: it is the only excluded public spec, it has a normative
knowledge statement, and r27 has no fetch for it. Name it uncovered-by-construction or re-open it.

R4. The 6 S008/S022/S023 pairs need artifact-scoped HOLDs; a source-scoped HOLD with an S001–S006 quote would be
false provenance (`count_c1.py` flags `source_missing`).

R5. Pin r26 population/statements hashes at measurement (or read the frozen copies) so the denominator cannot shrink
silently; the frozen population sha is already recorded for C2.

## Uncertainties

- Whether `Rejection07S013.md` is a “citation” of S013 is semantic; the token is an evidence-file label. The
  discovered-pairs file already resolves it to include; I did not edit it.
- S035 exclusion is a population tradeoff, not by itself a defect; calling the round “universal freshness” would be.
- The outside-knowledge census (219) is peer-reported, not re-measured. I did not inspect writer drafts or their
  proposed verdicts; this report checks population, excluded-id enumeration, scope language, and pair completeness.

## Reproducibility

```bash
sha256sum .ufo/waves/round-27/frozen/population.json; git show 83528f7c:.ufo/waves/round-26/population.json | sha256sum
python3 -B .ufo/waves/round-27/count_c1.py --root . --revision 83528f7c   # 57/41/16
python3 -B .ufo/waves/round-27/count_c1.py --root . --revision be375d90   # 57/41/16
grep -n 'S014\|S019\|S035' corpus/knowledge/*
```
Hashes: population `16330e1e…1b03`; contract `6d2d7f51…82da`; count_c1 worktree `7489865d…160d`, committed
`a1e46d19…a14c`; c1-before `af55d0a4…6e3c`; c2-oracle `1d038205…c7dd`; frozen ledger `c2026376…95ce`; expected
`628b7a05…70c2`; discovered-pairs `45e95683…03fb`. Knowledge blobs: accessibility packet `4277f159…aab`,
freshness-sweep `c2728405…7dbe`, static-canonical `833b28f2…31bc`.

Report: .ufo/waves/round-27/w1/ExcludedPopulation.md
