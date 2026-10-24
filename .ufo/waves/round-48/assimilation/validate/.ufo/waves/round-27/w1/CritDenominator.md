# CritDenominator — attack on the frozen C1 denominator and grammar

Seat `KakeR27.CritDenominator` (critic, read-only leaf). Axis judged: freshness (C1). Milestone: r27-full-citing-set.
Base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`; declarations `be375d90afc6fc7aca369ab3cf5247bf460aeed2`.
Everything here is author-side peer evidence. The parent judges independently. No production, oracle, or ledger edits were made.

## Verdicts (summary)

| # | Target | Verdict |
|---|---|---|
| F1 | Frozen grammar vs contract prose: `(S013, corpus/knowledge/ghp-served-set.md)` | CANDIDATE 58th pair; needs explicit L1 disposition (corroborates CritFailOpen) |
| F2 | Range / group expansion in all 26 base knowledge files | HOLD: every range at base is expanded; 57 is reproduced exactly |
| F3 | Metadata / EOF inclusion | HOLD for inclusion; verdict-kind risk on 4 S008 boilerplate pairs |
| F4 | Exclusion of S014 / S019 / S035 | HOLD at the stated scope; 18 excluded knowledge pairs must be disclosed, not described as "full" |
| F5 | Denominator can shrink: committed `count_c1.py` (a1e46d19) | FAIL: witness 57→55 |
| F6 | Ledger tamper: committed and working-tree counters both | FAIL: false PASS, exit 0, 57/57 |
| F7 | Frozen counter edited after the freeze (working tree, 7489865d) | IDENTITY CHANGE; must be disclosed |
| F8 | r26 carried pairs that contain seat-UNVERIFIABLE statements | DISCLOSURE GAP (2 pairs) |
| F9 | Latent grammar holes (not present in base corpus) | Latent; fixture-worthy |

Tool installs: none.

## Evidence base

- Population: `git show 83528f7c:.ufo/waves/round-26/population.json`, sha256 `16330e1e…1b03`. 32 rows: S001–S034 minus S014 and S019.
- r26 ledger: `statements.json` sha256 `c2026376…95ce`, 41 pairs. `frozen/ledger.json` equals the same 41 pairs. `frozen/population.json` is byte-equal to base.
- Frozen snapshot: `frozen/expected.json` sha256 `628b7a05…70c2`, 28 entries. All 28 recompute, and all 26 knowledge files are byte-equal to the base blobs. No base knowledge file is missing from the snapshot.
- Oracles at the commit: `count_c1.py` `a1e46d19…a14c`, `c2_count.py` `93f39b0f…4686`, `c2-oracle.json` `1d038205…c7dd`, `contract.json` `6d2d7f51…82da`, `c1-before.json` `af55d0a4…6e3c`. The working-tree `c1-before.json` equals the committed one.
- Independent enumeration: scratch `pairenum.py` scans all 26 base knowledge blobs.
  - Frozen grammar: 57 in-population pairs, equal to `c1-before.json` (41 decided + 16 missing).
  - The SOURCES.md `used-by` column yields 27 in-population knowledge pairs. All 27 are inside the 57, so the registry discovers nothing new.
  - JSON knowledge files (`accessibility-review-cards.json`, `freshness-pins.json`, `freshness-sidecar.json`) contain 0 `S\d` tokens and 0 `\u00` escapes, so their inclusion is vacuous.
  - Population rows with zero knowledge pairs: S015, S016, S017, S018 (queued or rejected rows). This is correct and gives no obligation.

## F1 — the contract's prose grammar is wider than the counter, the oracle, and the gate

- The contract denominator says "literal S +3-or-more digits", with no word-boundary requirement.
- The implementations all add a boundary:
  - `count_c1.py` uses `LITERAL = re.compile(r'\bS(\d{3,})\b')`.
  - The gate draft (`writer-gate/scripts/citing_set.py` `a165b779…`, line 105) uses `(?<!\w)S([0-9]{3,})(?!\w)`.
- Witness: `ghp-served-set.md:95` (blob `405b8587…a1e7`) ends with "name the round's retry, not a source of this entry (w2/Rejection01S001.md, w2/Rejection07S013.md)."
- A boundary-free `S(\d{3,})` scan over all 26 files gives the frozen 57 plus exactly one extra pair: `(S013, corpus/knowledge/ghp-served-set.md)`.
- Every other attached-prefix token is already in the 57: Correction3S010, Correction4S010, Rejection13S009, Rejection02S001, UncoveredS024S025, Correction6S026, Correction7S030, Correction8S030, Rejection10S021.
- What the token is: `w2/Rejection07S013.md` (`c31e10a4…6fa1`) has the target "row S013, `crawl-scope-per-host.md`". So `S013` is a seat or evidence filename label, not a source attribution for ghp-served-set. That is the same kind of round-provenance mention that F3 deliberately includes for S008.
- Impacted axes:
  - Freshness: the denominator is under-counted by 1 against the contract text.
  - Operability: if the gate followed the contract prose literally, it would emit 17 findings, and `c2_count.py` requires `len(findings)==16`. So the C2 oracle silently encodes the boundary rule.
- Smallest safe correction:
  - Add `{"row":"S013","file":"corpus/knowledge/ghp-served-set.md"}` to `discovered-pairs.json` (monotone, 57→58).
  - Adjudicate it as `kind: artifact`, verdict HOLD: the label points at evidence, not at a source.
  - Evidence: `.ufo/waves/round-26/w2/Rejection07S013.md`, which contains "row S013, `crawl-scope-per-host.md`".
  - State in the report that the token grammar is word-bounded, so that C2's 16 stays valid at that stated scope.
  - Do not rewrite `c2-oracle.json`.

## F2 — every range and group at base is expanded

These are all the range forms in the base corpus. Each is caught by `RANGE` and expanded, and each produced pair is in the 57.

| File:line | Form | Pairs added beyond the r26 41 |
|---|---|---|
| publish-channels.md:2 (metadata) | `S001-S007 opened that day` | S004, S006 |
| sitemap-orphan-audit.md:2 (metadata) | `r20 S001-S006 quote corrections` | S003, S005 |
| static-canonical-preflight.md:2 (metadata) | `S020-S027`, `S028-S029` | S022, S023 |
| static-canonical-preflight.md:54 (body) | `served set (S001–S006, ...)` (en-dash) | S001–S006 (grouped) |

- I searched for other forms: single-ended (`S001–6`), `/`, `~`, `…`, `...`, `thru`, U+2010/2011/2212 dashes, 2-digit ids and 4+-digit ids. None occur.
- `S0NN` placeholders appear in receipt paths. Every line carrying one also lists its rows literally, so they add no pair.
- Lists such as `S001, S002, S004 and S006` are fully caught by `LITERAL`.
- The metadata range claims are consistent with the SOURCES `opened` column: S001–S007 opened 2026-10-19, S020–S027 opened 2026-10-20, S028–S029 opened 2026-10-21. Artifact HOLD is available against `corpus/SOURCES.md` for S022 and S023 (static-canonical-preflight) and for S004 and S006 (publish-channels). S003 and S005 (sitemap) are dated r20 "quote corrections", which need their own evidence.

## F3 — metadata and EOF prose inclusion

- Inclusion is honest and matches the contract's "INCLUDE historical metadata/r26 EOF prose".
- Four of the 16 obligations exist only because of the r26 boilerplate "S008 via `manifest-retry.json`":
  - crawl-scope-per-host.md:57
  - ghp-custom-domain.md:62
  - ghp-etag-anatomy.md:60
  - static-canonical-preflight.md:184
- r26 already ruled on these words. `ghp-served-set.md:95` says they "name the round's retry, not a source of this entry".
- Risk of false provenance: a `kind: source` HOLD with a quote from the GNU tar manual would assert a support relation the text never claims.
- Correct form: `kind: artifact` against `.ufo/waves/round-26/fetched/manifest-retry.json`. Pair11B, Pair12A, Pair13B and Pair14A already draft this.

## F4 — exclusion of S014, S019 and S035

Under the frozen grammar there are 18 knowledge pairs outside the population:

- **S014, own-work:** 1 pair, `freshness-sweep.md`.
- **S019, own-work:** 16 pairs, mostly `source:` metadata lines. Files: drift-detection, fire-journal-codes, fleet-registry, free-read-verbs, freshness-sweep, ghp-subpath-spotcheck, keeper-timer-inert, kimi-subpath-audit, mirror-pitfalls, ops-automation, origin-repos, probe-delta-alerting, publish-channels, publish-queue, speedrun-pipeline, vault-properties.
- **S035, external W3C WCAG 2.2:** 1 pair, `accessibility-review-packet.md`.

Assessment:

- The r26 contract scopes the population as "S001..S034 minus own-work S014/S019; S035 (opened r25) excluded". SOURCES marks S014 and S019 as kind `own-work`.
- Excluding S014 and S019 is honest: they are local tools, not external sources.
- S035 is an external tier-A spec. Its exclusion is a population-scope tradeoff, not a defect, because C1 says "intersect r26 inherited32-row population".
- The milestone name "full citing-set" is overstated unless the report states that it covers 57 or 58 of 75 or 76 knowledge citing pairs, and names the 18 excluded pairs.
- Probe E: the working-tree counter raises `citing obligation outside frozen population` (exit 2) for a discovered S035 pair. It fails closed, not silently, but it means C1 cannot absorb S035. Disclose that.

## F5 — the committed counter lets the denominator shrink

- Committed `count_c1.py` recomputes pairs only from the measured revision. It never reads `c1-before.json`, even though the contract says "Baseline57 minimum, not maximum".
- Probe A, in a scratch clone at be375d90: rewrite `publish-channels.md:2` from `S001-S007 opened` to `S001 and S007 opened` and commit.
  - Result: `citingPairs 57→55`, `missing 16→14`, no finding.
  - The two obligations (S004 and S006 × publish-channels) disappear silently.
- Impacted axis: freshness (premature saturation).
- The working-tree edit (F7) fixes probe A: the same probe gives 57 / 16.

## F6 — false PASS from an unpinned r26 ledger, in both counter versions

- Both versions read `.ufo/waves/round-26/statements.json` and `population.json` from the measured revision, without any hash pin. The expected hashes are `c2026376…` and `16330e1e…`.
- Probe B: append the 16 oracle pairs as bare `{row,file}` rows, with no verdict, to r26 `statements.json`.
  - Committed counter: `decided 57/57`, `missing 0`, exit 0.
  - Working-tree counter: the same, exit 0.
- Probe D, working-tree counter: apply probe A and also drop the publish-channels rows from `c1-before.json`. Result: 55 pairs and 14 missing. The floor itself is mutable at the measured revision.
- Impacted axes: freshness (false PASS) and duplicate authority (the r26 ledger acts as an r27 credit source).
- Smallest safe correction, without rewriting expected outcomes:
  - Pin the sha256 of r26 `statements.json`, r26 `population.json` and `c1-before.json`. Compare blob hashes, or read them from `frozen/` with the `expected.json` digests, as `c2_count.py` already does.
  - On mismatch, return exit 2 `snapshot_tampered`.

## F7 — the frozen counter was edited after the freeze

- `git diff be375d90 -- count_c1.py`: the working tree is `7489865d…160d`, while the committed file is `a1e46d19…a14c`. The mtime is 17:05:14 -0300, after the W1 spawn.
- The edit makes four changes:
  - Union of the baseline floor (pairs from `c1-before.json` plus the r26 pairs).
  - Out-of-population pairs now raise an error.
  - `decided.discard(key)`, so a fresh override removes the old credit.
  - A `group_source_required` rule for S001–S006 × static-canonical-preflight.
- `c2_count.py` was also edited (`e5b6fa7f…`) to add `--selftest`, which calls the new untracked `oracle_selftest.py`.
- Each change strengthens the counter or adds tooling. None of them changes `c2-oracle.json` or the expected 16.
- However, the docstring still says the file was "written before adjudication or gate implementation". The measured authority is now ambiguous between the committed hash and the working-tree hash. CitingSweep08:133 observed the same edit.
- Impacted axes: identity change and false provenance.
- Correction: the parent should measure with an explicitly named counter hash. If the edited version is kept, land it as a disclosed post-freeze oracle amendment with its own hash, and keep `a1e46d19` as the declared original.

## F8 — r26 carried pairs that contain UNVERIFIABLE statements

- Two r26 pairs carry `seatUnverifiable>0`:
  - `S001 × ghp-served-set.md`: 3. The L1 disposition says "4 v3.0.1 statements UNVERIFIABLE", and EOF line 94 corrects that to 3.
  - `S033 × static-canonical-preflight.md`: 3, with no `l1Disposition` field.
- Both counters count both pairs as decided with no surfaced count.
- The counter's `scope` string discloses "not proof of truth of every underlying statement". That is a pair-granularity tradeoff, not a rounding defect.
- Correction: the report should name both pairs and their UNVERIFIABLE statement counts next to the decided total.

## F9 — latent grammar holes (absent from the base corpus, so 57 stands)

- Probe C appends `S001–S003–S006 and S020...S023` to a knowledge file and runs the committed counter.
  - The chained range loses S004 and S005, because `finditer` is non-overlapping.
  - The `...` form loses S021 and S022, because `\.\.` is immediately followed by `.`.
- A 4+-digit form `S0012` would map to S012 through `int()`. No occurrence at base.
- Fixture-worthy for the C2 selftest. This is not a C1 obligation today.

## Uncertainties

- F1's validity as a "citing pair" depends on how the contract is read. The tokens are literal, but the semantics are an evidence-file label. It is UNDECIDED here; the parent decides. I recommend the monotone addition because it costs one artifact row and removes the contract-versus-counter divergence.
- I did not identify the author of the F7 edit. The timestamps are from the filesystem.
- I ran the probes only in a scratch clone: `/fast/scratch/hyaku/kake-r27/CritDenominator/clone`, with `--shared` alternates, local commits only, and TMPDIR under scratch. No lane repository mutation.

## Witness commands

Run from `/fast/scratch/hyaku/kake-r27/CritDenominator`:

- `python3 -B pairenum.py` gives frozen 57, wide-minus-frozen `[S013 ghp-served-set]`, 18 excluded, and used-by ⊂ 57.
- Probes A–E: scratch clone at be375d90, running `count_c1.py` (committed) and `count_c1_worktree.py` (copy of 7489865d).
