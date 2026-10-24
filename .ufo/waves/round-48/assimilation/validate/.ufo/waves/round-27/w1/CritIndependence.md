# KakeR27.CritIndependence — critic report (r27-full-citing-set, judged on operability)

Seat: read-only critic, leaf. I did not run the unfinished gate `scripts/citing_set.py`.
Every witness below comes from the **frozen** counters (blobs at `be375d9`), run against synthetic
candidate commits in a scratch clone: `/fast/scratch/hyaku/kake-r27/CritIndependence/repo`.
The harness is `/fast/scratch/hyaku/kake-r27/CritIndependence/probe.py` and its output is `probe-out.json`.
No live lane, repo, index or jj state was mutated. No tools were installed.

## Inputs (sha256)
- contract.json `6d2d7f51371650c2d7535c401ead613355135d18b44762c41f385d05ee7582da`
- count_c1.py `a1e46d19b438fc254689dc42f474664864b7fd7fecc6a992ad70f5d5da44a14c`
- c2_count.py `93f39b0f7187fa084abd220d8c3734ce02b11b64cd940a1953347f37fa304686`
- c2-oracle.json `1d038205473180c7cb57895c2d480a8b52debe3bf08ab0a2f58ca7b1f67bc7dd`
- frozen/expected.json `628b7a054b3eb95370cb6716bf5fe8e87a9c9ab7caaadafad9797b726ec170c2`
- live fetched/manifest.json, uncommitted: `d3b0b1ca215bfa6d89edf639b2b87475d668fdf73cbf0ddf089c87e11d043781`

## Verdict summary
| Question | Verdict |
|---|---|
| Expected outcomes frozen before implementation? | YES for ordering, NO for independence (see I-1, I-2) |
| Zero or UNVERIFIABLE can be green? | YES: zero-denominator green, and r27 UNVERIFIABLE is masked by r26 carry (C1-1, C1-2, C1-6) |
| Stale corrections evade checks? | YES: a marker-only STALE passes (C1-8) |
| Inherited ledger launders the missing set? | YES: the r26 ledger is read at the candidate revision, unpinned (C1-3) |
| Real source support vs substring shape | The counter checks substring shape only. 10/16 pairs are not source-attributions at all (S-1) |
| C2 improved solely by C1 ledger additions? | NO with frozen bytes. YES only via a self-attested oracle rewrite (C2-2, C2-3) |
| C2 16/16 implies capability? | NO: a hard-coded, logic-free gate passes (C2-1) |

## Independence / freezing
- **I-1 Ordering holds.** At `be375d9`, `scripts/citing_set.py`, `pairs.json` and `discovered-pairs.json` are all absent (`c2-before.json`: `gate_absent`). The frozen corpus, population and ledger are byte-identical to base `83528f7` for all 26 knowledge files, `population.json` (`16330e1e…`) and `statements.json` (`c2026376…`). The r27 fetch `fetchedAt` is `2026-10-21T19:59:53Z`, 16 s after the freeze commit (`16:59:37 -0300`). So the sources were opened this round, after the oracle.
- **I-2 Duplicate authority.** `c2-oracle.json.expectedPairs == c1-before.json.missing`, with identical order (checked programmatically: `True`). The C2 "independent" oracle is `count_c1.py`'s own regex output, not a second derivation, so both claims share one token grammar. Any grammar defect is invisible to both, and a gate that follows the contract's literal wording can be scored a false positive. Concrete case: P-1.
- **I-3 Unfrozen provenance.** `fetched/`, `fetch_group.py` and `c2-before.json` are untracked (`git status`). `count_c1.py` reads `fetched/` at the measured revision, so the source bytes enter history only at the candidate commit, with candidate-written hashes (see C1-7).

## C1 witnesses (`count_c1.py` from `be375d9`; base reproduces 57/41/16, exit 1)
| id | candidate input | exit | citing/decided/missing | issue |
|---|---|---|---|---|
| C1-1 | `round-26/population.json` rows → `[]` | **0** | 0/0/0 | zero-denominator green |
| C1-2 | `git mv corpus/knowledge corpus/kb` | **0** | 0/0/0 | zero-denominator green; no ≥57 floor |
| C1-3 | append 16 bare `{row,file}` rows to `round-26/statements.json` | **0** | 57/57/0, newDecided 0 | r26 ledger laundering; no r27 work at all |
| C1-4 | delete the 6 knowledge files holding the missing pairs | **0** | 11/11/0 | denominator shrinks silently below baseline 57 |
| C1-5 | 16 rows `kind:artifact, evidence:.ufo/waves/round-27/pairs.json, contains:"HOLD"` | **0** | 57/57/0 | self-referential evidence accepted |
| C1-6 | C1-5 plus r27 `UNVERIFIABLE` on all 41 r26 pairs | **0** | 57/57/0 | fresh UNVERIFIABLE masked by r26 carry |
| C1-7 | append an invented sentence to `fetched/text/S002-1.txt`, quote it | 1 (other pairs) | S002 row valid, no finding | text not bound to the raw hash |
| C1-8 | STALE row plus only `<!-- [r27-recheck S003 STALE] -->` appended | 1 (other pairs) | S003 row valid, no finding | marker-only correction accepted |
| C1-9 | r27 HOLD rows for all 41 r26 pairs | 0 (with C1-5) | newDecided **57** | r26 carry relabelled as r27-fresh |
| C1-10 | grouped-six source rows, quote `"the"` (or `"name:"`), anchor `"-"` | 1 (S008/S022/S023) | newDecided 10 | one-token quote grounds all 10 grouped-row pairs |

Mechanisms (count_c1.py line numbers):
- L18: the population is read at the revision, and the result is never compared to the frozen `population.json` or the 57-pair floor.
- L19: `ls-tree corpus/knowledge` returns empty after a move, with no error.
- L31–32: `decided` is the set of every r26 row regardless of content. r26 rows carry no `verdict`/`kind` fields at all; I counted all 41 with `verdict` = `None`.
- L60: `decided|new_decided` lets r26 dominate a fresh UNVERIFIABLE.
- L46–50: the raw sha is checked against a candidate-written manifest, the `text` file is trusted unhashed, and `status`/`fetchedAt` are ignored.
- L53: artifact `evidence` may be any blob, including `pairs.json` or the citing file itself.
- L56: STALE requires only the marker substring anywhere in the file. Nothing checks that a correction is appended at EOF or that the wrong attribution is addressed.
- `discovered-pairs.json` is read at the revision with no prior-revision comparison, so entries can be deleted and "monotone" is unenforced (by inspection; no witness run).

Current honesty (not a defect): the live `fetched/text/*.txt` files all regenerate byte-exactly from raw via `round-26/source_text.py`, and all 8 raw shas match the manifest. So C1-7 is a future-tamper surface, not a present corruption.

## Source support vs substring shape (S-1)
Contexts of the 16 frozen pairs, located in `frozen/corpus/knowledge`:
- **Substantive grouped attribution (6 pairs): static-canonical-preflight.md:54**, S001–S006. Located: "Prepare the manifest over actual built/deployable HTML when that artifact exists, not over an assumed checkout served set (S001–S006, `ghp-served-set.md`)." This is local synthesis. Per the contract, each source's contribution must be labelled. The counter accepts one ≤25-word quote per pair, with no check that it bears on the claim (C1-10).
- **Historical metadata (4 pairs):**
  - sitemap-orphan-audit.md:2, S003 and S005 by range expansion: "r20 S001-S006 quote corrections 2026-10-19, base cb807bc".
  - publish-channels.md:2, S004 and S006 by range expansion: "(S001-S007 opened that day)".
  - These are date/event claims. Support must be a round-20 artifact. A fetched-page quote would be shape, not support.
- **r26 EOF provenance (4 pairs): S008 in crawl-scope-per-host:57, ghp-custom-domain:62, ghp-etag-anatomy:60 and static-canonical-preflight:184**: "(`.ufo/waves/round-26/fetched/manifest.json`, S008 via `manifest-retry.json`)". The evidence artifact exists at base: `.ufo/waves/round-26/fetched/manifest-retry.json` and `S008-1-retry.raw.gz`.
- **Metadata range (2 pairs): S022 and S023 at static-canonical-preflight.md:2**: "verified-at: 2026-10-20 (S020-S027) and 2026-10-21 (S028-S029), documentation opened this round". The entry's `source:` line omits S022/S023, so they enter only through range expansion. UNVERIFIABLE here whether the r22 receipts cover these two rows; the pair seats must decide it.
- Consequence: the counter cannot tell these four classes apart. `kind:source` with a one-token quote passes for a date claim (C1-10 covers S003/S005 sitemap and S004/S006 publish-channels). Grading these pairs is a parent-judge/review job. The `count_c1` PASS alone is not evidence of support.

## C2 witnesses (`c2_count.py` from `be375d9`)
| id | candidate input | c2 exit | passed | issue |
|---|---|---|---|---|
| C2-1 | `scripts/citing_set.py` = literal print of the 16 oracle pairs, exit 1, no reading of inputs | 0 | **true** | 16/16 with zero logic; single-point oracle |
| C2-2 | clean-printing gate plus `c2-oracle.json` rewritten to `expectedPairs:[]`, `expectedExit:0` | 0 | **true** | oracle read at the candidate revision, self-attested |
| C2-3 | C1-style 16 rows appended to `frozen/ledger.json`, no rehash | 2 | `snapshot_tampered` | tamper check works for one-file edits |
| C2-4 | same as C2-3 plus `frozen/expected.json` sha rehashed, oracle kept | 1 | false | circular hash accepted; oracle still rejects |
| C2-5 | gate imports a sibling module | 2 | JSONDecodeError | only `citing_set.py` is copied, so a multi-module gate cannot be evaluated |

- **Separability answer:** C2 cannot look improved from C1 ledger additions alone. With frozen bytes, additions are either detected (C2-3) or make a correct gate emit fewer than 16 findings, which fails (C2-4). The only route to a fake green is rewriting the oracle at the candidate revision (C2-2) or hard-coding (C2-1).
- By inspection, not run: keys in `expected.json['sha256']` are joined to the tempdir unsanitised, so `../x` writes outside the tempdir (L16). The gate subprocess also inherits the caller's cwd (the repo root), so a gate can read `c2-oracle.json` directly.
- The contract's other C2 "after" claims (clean positive fixture exits 0, selftest coverage, mutation probes) have **no frozen independent oracle**. They rest on candidate-authored fixtures and must not be credited from the c2_count PASS.

## Discovered pair (denominator grows; does not shrink)
- **P-1: (S013, corpus/knowledge/ghp-served-set.md)**, at line 95, through the glued filename token. Located: "not a source of this entry (w2/Rejection01S001.md, w2/Rejection07S013.md)."
- It is missed by `\bS(\d{3,})\b`, but matches the contract wording "literal S +3-or-more digits", which states no boundary.
- I derived it independently with a prefix-glued probe. It matches CritFailOpen's candidate. The other glued tokens (3S009, 3S010, 4S010, 1S001, 2S001, nS030, 4S025, 6S026, 7S030, 8S030, 0S021) all fall in already-counted pairs. `S404_SHA256` is outside the population. No case-variant ranges (`To`/`thru`), other dashes (U+2010–2012, U+2212), JSON-escaped dashes, or `S001-006` half-ranges exist in the frozen corpus.
- Impact: if L1 admits P-1 to the denominator (58 pairs), a gate that follows the contract's grammar reports 17 pairs on the frozen snapshot, and the C2 oracle (exactly 16, no false positives) rejects it. L1 must either pin the token grammar (word boundaries) in the contract or disclose the C2 oracle as UNPROVABLE for that grammar. It must not rewrite the expected outcome to match the candidate.

## Impacted axes
- **Freshness (C1):** C1-1 through C1-10 and S-1. The counter's green is not sufficient evidence for "every pair has a durable, supported adjudication".
- **Operability (C2):** C2-1, C2-2 and C2-5. A 16/16 result does not demonstrate gate capability. Path and cwd leakage are minor.
- **Both:** I-2, one regex authority behind both oracles.

## Smallest safe corrections (for L1; do not rewrite expected outcomes)
1. Run both counters from frozen blobs (`git show be375d9:.ufo/waves/round-27/{count_c1,c2_count}.py`), never from the working tree.
2. In `c2_count.py`, read `c2-oracle.json` and `frozen/*` at `be375d9`, not at `--revision`. This closes C2-2 and C2-4.
3. In `count_c1.py`, read `population.json` and `round-26/statements.json` at `be375d9`. Union the frozen 57 (frozen ledger ∪ oracle pairs) and all discovered pairs into the denominator, and report removed references as findings (see the Addendum). This closes C1-1 through C1-4 and R1–R3.
4. Make an r27 row for an r26 pair override the r26 carry. UNVERIFIABLE or invalid must then count as missing. Report r26 carry and r27 rows separately. This closes C1-6 and C1-9.
5. Regenerate quote text from raw via frozen `round-26/source_text.py` instead of trusting `text/*.txt`. Require `status==200` and `fetchedAt` later than the freeze. Forbid artifact evidence under `round-27/pairs.json` and the citing file itself. This closes C1-5 and C1-7.
6. Grade quote relevance, STALE correction content (EOF, attribution fixed), and per-source contribution labels in the human/parent review. Do not credit them from the counter (C1-8, C1-10, S-1).
7. Before integrating the gate, freeze at least one independent positive C2 case: frozen ledger plus the 16 rows, expected exit 0 and 0 findings. This is derivable without candidate output. Then run the gate with `cwd=tempdir`. This closes C2-1.
8. Decide P-1 explicitly. Record it in `discovered-pairs.json` (adjudicate as an artifact pointer) and fix the token-boundary rule in the contract, or disclose UNPROVABLE.

## Addendum (parent request): baseline-57 shrink by reference removal — CONFIRMED
Witness: `probe2.py` / `probe2-out.json` in the scratch dir, run with the frozen `count_c1.py`. These are text-only edits: no file deletion and no ledger change.
| id | edit | exit | citing/decided/missing |
|---|---|---|---|
| R1 | static-canonical-preflight.md:54 `(S001–S006, `ghp-served-set.md`)` → `(`ghp-served-set.md`)` | 1 | 51/41/10 |
| R2 | R1, plus removing the S001-S006/S001-S007 metadata ranges, the 4 `S008 via manifest-retry.json` mentions, and S022/S023 from the `verified-at` range | **0** | **41/41/0** |
| R3 | R2, plus replacing r26-decided `S004` in speedrun-pipeline.md | **0** | **40/40/0** |

Cause: `count_c1.py` L19–28 enumerate pairs from the **current** revision's text only. The frozen original set is never unioned in, so "Baseline57 minimum" is unenforced. R3 shows that already-decided r26 pairs can also leave the denominator silently.

The frozen original-57 set can be rebuilt from `be375d9` bytes alone, with no candidate input:
- `frozen/ledger.json` pairs (41) ∪ `c2-oracle.json` expectedPairs (16) = 57. The two sets are disjoint, the oracle equals `c1-before.missing`, and the union equals an independent recount of `frozen/corpus/knowledge` with the frozen grammar (57).
- Correct denominator is `pairs(candidate) ∪ frozen57 ∪ discovered(every revision since be375d9)`. Report `removedReferences = frozen57 − pairs(candidate)` as a finding. Do not drop it.
- A removed reference is either a STALE correction to be appended (the r26 rule is append-only, with original lines unchanged) or a disclosed obligation. It is never an exclusion.

## Addendum 2 (parent request): r27 override of an r26 carried pair — FIXTURE FAILURE CONFIRMED
Witness: `probe3.py` / `probe3-out.json` (scratch), run with the frozen `count_c1.py`. Every case contains the same 16 valid artifact HOLD rows for the missing pairs. Each adds at most one r27 row for the carried pair `(S001, corpus/knowledge/ghp-served-set.md)`. Required outcome: the override removes the carried credit, the pair is listed in `missing`, decided = 56, and exit = 1.
| case | r27 override row | actual exit | actual decided / missing | required | verdict |
|---|---|---|---|---|---|
| O0 control | none | 0 | 57 / [] | 0, 57 / [] | ok |
| O1 | UNVERIFIABLE, valid artifact | **0** | **57 / []** | 1, 56 / [S001×ghp-served-set] | **FAIL: green** |
| O2 | HOLD, `kind:bogus` | 1 (finding `kind`) | **57 / []** | 1, 56 / [pair] + finding | FAIL: credit retained |
| O3 | UNVERIFIABLE, artifact `contains` absent | 1 (`artifact_support`) | **57 / []** | same | FAIL: credit retained |
| O4 | STALE, no `[r27-recheck S001 STALE]` | 1 (`correction_missing`) | **57 / []** | same | FAIL: credit retained |
| O5 | verdict `MAYBE` | 1 (`verdict`) | **57 / []** | same | FAIL: credit retained |

- Cause: L60, `decided=(decided|new_decided)&pairs`. The r26 carry is unioned in unconditionally, so any r27 row for the same key, whether UNVERIFIABLE or invalid, cannot subtract from it.
- O2–O5 are fail-closed on exit only, because `findings` is non-empty. The `decided`/`missing` metrics still report the pair as decided. So the C1 "every pair has durable HOLD or supported STALE" number would be overstated, and an UNVERIFIABLE override (O1) is fully green.
- Required semantics for the repair: the latest r27 row for a key supersedes the r26 carry. Only a valid HOLD or STALE (with correction) counts as decided. UNVERIFIABLE or invalid rows put the key in `missing`, and invalid rows also emit a finding.
- The target is unchanged: the denominator stays original-57 ∪ discoveries, and the repair touches the decision rule only.
- Source semantic support is still human-checked (next section). These fixtures prove record and credit logic only.

## Addendum 3 (SourceCensus report): uncommitted counter edits — target-preserving harness repair, not target drift; still undisclosed and incomplete
The live `count_c1.py` and `c2_count.py` are modified and uncommitted, and they changed while I was reviewing:
- `count_c1.py`: `d6e3b32b…`, then `c890a77003b3…` (mtime 17:09:51 -0300).
- `c2_count.py`: `e5b6fa7f…`, then `ac570237…`; I staged `913a797f…`.
- `c2-oracle.json` is unchanged (`1d038205…`).

I tested the `count_c1.py` snapshot `c890a77` and the `c2_count.py` snapshot `913a797`. Copies are in the scratch `new/` dir; witnesses are `probe4.py`/`probe4-out.json` and `probe5.py`/`probe5-out.json`.

**Drift verdict: harness extension.**
- On the base snapshot, the edited counter gives 57/41/16, exit 1, identical to `c1-before`. With `discovered-pairs.json` it gives 58/41/17.
- I found no case that the frozen counter rejects and the edited counter accepts. One exception: a raw-hash mismatch is now reported per fetch, not against the pair, so the pair keeps its credit. The exit is still 1.
- Disclosure is still required: the declared measuring command's bytes are no longer the frozen `a1e46d19` / `93f39b0f`.
- Commit the amendment, with its reason and hashes, before any candidate measurement. Report both frozen-counter and amended-counter outputs. Do not present the amended counter as the frozen counter written before adjudication.

Re-test against the edited counter (closed = the witness no longer passes):
| witness | frozen counter | edited counter | status |
|---|---|---|---|
| C1-1 empty population | exit 0 | exit 2 `frozen_input_changed` | closed |
| C1-2 moved corpus | exit 0, 0 pairs | exit 1, 57/41/16 | closed |
| C1-3 r26 ledger launder | exit 0 | exit 2 `frozen_input_changed` | closed |
| R1 reference removal | 51/41/10 | 57/41/16 | closed |
| R4 `c1-before.json` rewritten plus reference removed | n/a | exit 2 | closed |
| O1 UNVERIFIABLE override | green | override pair moves to `missing` | closed |
| C2-2 oracle rewritten | passed | exit 2 `frozen_input_changed` | closed |
| C1-5 self-ref `pairs.json` artifact, 10 non-grouped pairs | accepted | **accepted** | OPEN |
| **X2** grouped six with 6-token row-specific *page-chrome* quotes, plus self-ref artifacts for the other 10 | n/a | **exit 0, 57/57/0, no findings** | **OPEN: full C1 green with zero real support** |
| X3 fabricated `S001-1.raw.gz` plus re-sha'd manifest, matching quote | n/a | S001 grouped pair valid, no finding | OPEN |
| X4 manifest `status:503`, `fetchedAt:2020-01-01` | n/a | exit 0 | OPEN |
| C1-8 marker-only STALE | accepted | accepted | OPEN |
| X1 `discovered-pairs.json` deleted in a later commit | n/a | 58 → 57, exit unchanged, no finding | OPEN (monotone rule unenforced) |
| C2-1 hard-coded 16-pair gate | passed | **passed** | OPEN |
| Y consumer repo lacking `be375d9` | n/a | exit 2 `CalledProcessError` on `git show be375d9:` | NEW consumer failure |

The X2 quotes accepted as "row-specific support":
- S001: `name: "Upload GitHub Pages artifact" description:`
- S002: `Release v4.0.0 · actions/upload-pages-artifact · GitHub`
- S003: `Home GitHub Pages Get started Configure`
- S004: `Using custom workflows with GitHub Pages`
- S005: `Expand sidebar Home GitHub Pages Configure`
- S006: `Expand sidebar Home GitHub Pages Set`

These are titles and navigation text, not support for static-canonical-preflight.md:54. The ≥6-token and `quote_not_row_specific` rules narrow the shape test but do not make it semantic. This confirms the explicit limitation below.

Consumer-input notes:
- **Y:** any isolated fixture repo built by `git init` (as `oracle_selftest.py` appears to do) will exit 2, unless it also contains `be375d9`. By inspection, not run: the selftest's c1 cases expect exits 0/1. Seed `be375d9` into the fixture repo, or pass the reference blobs another way.
- The `source_text.py` helper is loaded from `__file__`'s working-tree location, not from the measured revision. It is hash-pinned (`55ae7abc…`, equal to base), so this is safe, but running the counter from an extracted blob elsewhere fails.

Smallest remaining repairs:
1. Pin `discovered-pairs.json` as union-monotone: entries at the measured revision ⊇ entries at every earlier r27 commit, or at a committed snapshot.
2. Reject artifact evidence under `.ufo/waves/round-27/` that the counter itself reads (`pairs.json`, `discovered-pairs.json`).
3. Pin `fetched/manifest.json` (live `d3b0b1ca…`) and the raw shas in a committed declaration. Require `status==200` and a `fetchedAt` later than the freeze.
4. Keep quote meaning and STALE-correction content as human review.
5. C2 still needs an independent frozen positive case, plus `cwd=tempdir`, before 16/16 can stand as evidence of capability.

## Explicit limitation: source quote validation checks shape, not meaning
`count_c1.py` L44–51 establish only that:
- the manifest row and index exist;
- the raw gzip hashes to the candidate-written manifest sha;
- the quote is 1–25 words and a whitespace-normalised substring of an unhashed text file;
- the anchor is a non-empty string.

It does **not** establish:
- that the quote bears on the cited statement, or entails it at the stated scope;
- that the anchor locates the quote;
- that each grouped source's contribution is labelled;
- that the fetch was 200 and post-freeze;
- that the text file derives from the raw bytes.

Witnesses: C1-10 (the one-token quote `"the"` validates all 10 S001–S006 pairs, including 4 date/metadata pairs that no page text can support) and C1-7 (an invented sentence is accepted).
A valid `count_c1` row therefore means "a well-formed record exists". Semantic HOLD/STALE must be judged by a reviewer who is not the pair author, against S-1's classes:
- 6 synthesis pairs need a per-source contribution label;
- 4 metadata pairs need artifact evidence;
- 4 S008 provenance pairs need `round-26/fetched/manifest-retry.json`;
- 2 S022/S023 range pairs need r22 receipt evidence.
Raising the quote minimum (for example, ≥5 words) would only narrow the shape test. It would not make it semantic.

## Uncertainties
- C1-7 and C1-8 were run against one pair each. Generalising to all pairs is by code reading ([INFERENCE], same code path).
- Whether S022/S023 "verified-at 2026-10-20" is supported: UNVERIFIABLE from this seat. Left to the pair seats.
- Whether P-1 is a "citing pair" is a contract-scope decision. The text says "not a source of this entry".

Checks for main/L1 after integration: rerun `probe.py` scenarios against the integrated candidate, and run `c2_count.py` from the `be375d9` blob.
