# AttackOracleFreeze — r27 W2 fresh falsification (critic, axis: operability)

Attacked item: oracle freeze across declaration `be375d9` → amendment `08014ce` → strict `9ba102d` → candidate `ac46a74`, plus whether the stricter counters only enforce frozen targets or move them.
Scratch: `/fast/scratch/hyaku/kake-r27/AttackOracleFreeze/` (TMPDIR there; disposable clone `clone/`, shallow clone `shallow/`). No live source/index/commit writes. No installs.

## Verdict
- **Freeze holds for the named immutable inputs.** The amended C2 counter turns the declaration-era blessed-oracle rewrite into could-not-evaluate (exit 2).
- **Counterexample (fixable defect):** the strict and candidate C1 counters reach exit 0 at 58/58 with 0 unknown units after three shape-only ledger rows. Strictness is enforced only on carried ledger fields. A fresh artifact override restores green with no semantic check (probe R8).
- **Minor gaps:** a deleted `c1-before.json` and a rewritten `contract.json` are not could-not-evaluate for any C1 counter (R3, R7). The target still comes from the declaration blob, so the target is not shifted.

## Byte identity (sha256 prefix; same at be375d9 / 08014ce / 9ba102d / ac46a74 / working tree; absent at base 83528f7)
contract.json `6d2d7f51…`, c1-before.json `af55d0a4…`, c2-oracle.json `1d038205…`, frozen/expected.json `628b7a05…`, frozen/population.json `16330e1e…`, frozen/ledger.json `c2026376…` (equal to declaration blob of round-26/statements.json).
`git diff --stat 83528f7 ac46a74 -- .ufo/waves/round-26` is empty. Only untracked `__pycache__` is present in the r26 directory.

## Code hashes (full sha256)
| version | count_c1.py | c2_count.py |
|---|---|---|
| decl be375d9 | a1e46d19b438fc254689dc42f474664864b7fd7fecc6a992ad70f5d5da44a14c | 93f39b0f7187fa084abd220d8c3734ce02b11b64cd940a1953347f37fa304686 |
| amend 08014ce | 26fd8bbb96dad961bd3378ebe8bb59fd572b590502eca7ceb06f523fae4b457f | 913a797fdfcbd25d328c2291a14cb84620f4ebfe348d6fd1016415674b8ca055 |
| strict 9ba102d | f2632131c5dc72c0cb7b79d1da3eac651d59a80386ef20f360766eb7eb894664 | = amend |
| cand ac46a74 | 8d4c22efa884468daead75aa4b9d6143d38986a83c3069747d146ee0daf942a5 | = amend |

Dependencies are read from the code directory, not from `--revision`, and are hash-pinned: carry-errata.json `236d9e79…`, round-26/source_text.py `55ae7abc…`.
Provenance drift: `oracle-implementation-corrections.json` names 26fd as the corrected C1 hash, and `strict-c1-source-hashes.json` names f263. The candidate hash 8d4c (which adds the carry-errata block, +10/−1 lines) appears only in frozen-candidate.json and integration-receipt.json. It is disclosed, but the corrections chain is not one closed record.

## Run matrix (`python3 -B <code>/round-27/<k>.py --root <repo> --revision <rev>`)
Every row below matched its declared expectation.
| code→target | C1 exit / decided/citing (unknown units) | C2 exit / result |
|---|---|---|
| decl→base | 1 / 41/57; stdout sha `af55d0a4…` = c1-before.json bytes | 1, uncaught CalledProcessError traceback (crash, conflated with "failed") |
| amend→base | 1 / 41/57 | 2 could-not-evaluate git_input_unavailable |
| strict→base | 1 / 39/57 (reviewed 41) | — |
| cand→base | 1 / 38/57 (7 units, 3 pairs) | 2 git_input_unavailable |
| decl,amend,cand→decl | C1 same as on base | 1 gate_absent, 0/16 |
| decl→cand | 0 / 58/58 | 0, 16/16, false positives 0, gateExit 1 |
| amend→cand | 0 / 58/58 | 0, 16/16 (stdout sha `4666151c…`, identical to decl) |
| strict→cand | 1 / 56/58 (S001 ghp-served-set and S033 preflight, 3+3 units) | — |
| cand→cand | 1 / 55/58 (+S007 ghp-custom-domain, 1 unit) | 0, 16/16 |

Shift versus enforcement:
- Citing denominator is identical across all four versions (57 on base, 58 on candidate).
- Per-row validity of the 18 pairs.json rows is identical across versions (18/18 valid; diff empty). No observed loosening from the re-derived `text_of` view.
- The only movement is decided falling 58→56→55, from the contract's existing C1 rule ("UNVERIFIABLE explicit, never counted decided").
- Unit check: 7 = S001 3 + S033 3 + S007 1 is correct. r26 `Rejection02S001.md` moved row 17 to STALE (4→3). The ledger's l1Disposition prose still says "4"; that is stale text, not an undercount.
- Carry-errata is a post-declaration input that changes the outcome (56→55). Code inspection shows it can only add unknown pairs (a negative `units` value still leaves the key unknown). It is monotone-strict and does not shift the target.

## Immutable-input rewrite probes (scratch clone commits on top of ac46a74)
| probe | rewrite | expected | actual |
|---|---|---|---|
| R1 `41434a9b` | C2 bless: c2-oracle expectedPairs=[], expectedExit 0; 16 pairs added to frozen/ledger.json; expected.json sha updated | decl blesses, amend/cand return 2 | decl C2 exit 0 passed (expected 0, detected 0, gateExit 0) = **blessed new expectation**; amend and cand C2 exit 2 frozen_input_changed |
| R2 `224ee07e` | c1-before.json missing=[] | amend+ return 2 | decl C1 0 (58/58; never reads it); amend, strict, cand exit 2 frozen_input_changed: c1-before.json |
| R3 `049bd695` | `git rm` c1-before.json | not caught | amend 0 58/58, strict 1 56/58, cand 1 55/58: **deletion accepted** (blob read with optional=True) |
| R4 `0944688b` | r26 statements seatUnverifiable→0 | amend+ return 2 | decl 0; amend, strict, cand exit 2 frozen_input_changed: round-26/statements.json |
| R5 `e71dcb84` | fetched/manifest.json entry appended | amend+ return 2 | decl 0; amend, strict, cand exit 2 fetched_manifest_changed |
| R6 `710cec4d` | discovered-pairs.json deleted | cand keeps 58 | all versions 58 citing (S013 also found literally, so this probe cannot discriminate) |
| R7 `33d3bd93` | contract "exactly16/16"→"exactly15/16" | C2 returns 2, C1 blind | amend and cand C2 exit 2 frozen_input_changed; decl C2 0; **all C1 counters ignore it** (decl 0, cand 1 55/58) |
| P1 | carry-errata uncertainties emptied in a copied code dir | 2 | cand exit 2 carry_errata_changed |
| P2 | shallow depth-1 clone without be375d9 | cand returns 2 | cand C1 exit 2 (CalledProcessError text), cand C2 exit 2 git_input_unavailable; decl C1 0 58/58 and decl C2 0 16/16 (no freeze check) |

## Counterexample R8 (`12a286a7`, scratch only): strict C1 green by shape
Added three pairs.json rows: `{kind:artifact, verdict:HOLD, reason:"probe"}` for S001/ghp-served-set, S033/static-canonical-preflight and S007/ghp-custom-domain. Their evidence is the r26 seat reports `PairS001GhpServedSet.md`, `PairS033StaticCanonicalPrefl.md` and `PairS007GhpCustomDomain.md`, which declare those very statements UNVERIFIABLE. The `contains` values are "21 HOLD" and "HOLD".
- Expected exit 0 (declared before running).
- Actual: strict exit 0 at 58/58; cand exit 0 at 58/58 with knownUnverifiableUnits 0, knownUnverifiablePairs 0, findings 0; all three outcomes valid.
- Cause: `decided.discard` followed by `unknown.pop` on any valid fresh row. `artifact_self_support` excludes only corpus/knowledge, the round-27 directory and the two r26 JSON files, so r26 reports and any other repo text count as support.
- The actual candidate pairs.json has no such rows (55/58 stands), so this is a latent hole, not a current false green. The C1 "UNPROVABLE, never green" claim depends on author discipline, not on the counter.
- Impacted axes: freshness (C1 strict status) and operability (the counter as a gate).
- Smallest safe correction: for any key in carried `unknown` or carry-errata, require `kind=='source'` (same mechanism as `group_source_required`), and extend `artifact_self_support` to the `.ufo/waves/` prefix. This adds no new expected outcome; it only closes the override route.

## Other discrepancies / uncertainties
- R3 fix: require `c1-before.json` to be present whenever `git merge-base --is-ancestor be375d9 <revision>` holds. Absence would remain tolerated only before the declaration (base).
- R7: C1 does not pin contract.json. C2 does, so the contract is guarded on one path only. Pinning it in count_c1 is a one-line `pinned_obj`-style check.
- The declaration C2 crash on base (exit 1 from an uncaught re-raise) is a real defect, corrected by 08014ce (exit 2). Any historical "C2 exit 1 on base" reading is a crash, not a measurement.
- Carry-errata and source_text are bound to the code checkout, not `--revision`. Running candidate code against base therefore applies post-declaration errata. This is disclosed by hash pinning but is not revision-bound.
- c2_count hardcodes its tempdir parent `/fast/scratch/hyaku/kake-r27`, ignoring TMPDIR. The directory is cleaned up; noted for isolation only.
- A session-shell job (bg_4698, rewrite loop using `source <(sed…)`) stalled before running any counter. It ended at the 3600 s timeout with no output and no `out/R*` files. All probes were rerun with explicit hashes in a fresh shell.

Checks for Main: rerun the run matrix and R1/R3/R7/R8 from the scratch clone; the fixes above stay L1-owned.
