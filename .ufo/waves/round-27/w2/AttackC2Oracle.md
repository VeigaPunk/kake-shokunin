# KakeR27.AttackC2Oracle — C2 causal separability / consumer evidence (falsification, not a judge)

Candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`. All source reads by explicit hash. Hashes of the files I read in the working tree equal the candidate blobs: `c2_count.py` 913a797f…, `c2-oracle.json` 1d038205…, `frozen/expected.json` 628b7a05…, `pairs.json` f1fa20ca…, `scripts/citing_set.py` 3a361a00…. No source/docs/registry edits; main repo tracked tree clean after the run, and HEAD is still the candidate. Scratch only: `/fast/scratch/hyaku/kake-r27/AttackC2Oracle/` (TMPDIR there). Scratch commits exist only in a `--shared` scratch clone there (not the project repo; L1 may delete). No installs. No network.
Expectations were written to `scratch/expected-declared.json` (sha256 79616ec9…) before each probe ran. Harness: `scratch/probe.py` (162c0f9a…).

## 1. Frozen rerun on the unchanged 28 inputs
`python3 -B .ufo/waves/round-27/c2_count.py --root . --revision ac46a74…` → exit 0, stdout sha256 4666151c…, `expected 16, detected 16, falsePositive 0, passed true, gateExit 1`, gate `failed`, citingPairs 57, ledgerPairs 41, 16 findings, all `unadjudicated_citing_pair`, stderr empty.
**Identities, not just the count:** the multiset of (row, file, id) equals the 16 oracle pairs exactly (set size 16, no other finding ids).
**Independent trace from the frozen corpus text** (rg over the frozen blobs, not gate output), 16 total:
- `static-canonical-preflight.md`, 9 pairs: S001–S006 via the en-dash group on line 54 (no S001..S006 literal elsewhere in that file); S008 as an r26 EOF-prose literal on line 184; S022/S023 via the metadata range `S020-S027` on line 2.
- `sitemap-orphan-audit.md`, 2 pairs: S003/S005 via the metadata range `S001-S006` on line 2.
- `publish-channels.md`, 2 pairs: S004/S006 via the metadata range `S001-S007` on line 2.
- S008 literal in r26 EOF prose, 3 pairs: `crawl-scope-per-host.md:57`, `ghp-custom-domain.md:62`, `ghp-etag-anatomy.md:60`.
Every one of the four declared mechanisms is load-bearing: en-dash group, hyphen range in metadata, EOF prose, and literals.

## 2. New harmless changed inputs (not W1-authored; frozen blobs copied to scratch; candidate gate run in working-tree mode)
| probe | change | declared | actual exit / unadj / other / citingPairs | match |
|---|---|---|---|---|
| P0 | none | 1 / 16 oracle / 0 / 57 | 1 / 16 identical / 0 / 57 | yes |
| P1 | remove grouped `S001–S006` from static:54 | oracle minus S001–6×static = 10, citing 51 | 1 / 10, exactly those 6 removed / 0 / 51 | yes |
| P2 | `S001–S006` → `S001 through S003` | minus S004–6×static = 13 | 1 / 13 / 0 / 54 | yes |
| P3 | sitemap:2 `S001-S006` → literal list S001,S002,S004,S006 | minus S003,S005×sitemap = 14 | 1 / 14 / 0 / 55 | yes |
| P4 | crawl-scope:57 drop `S008` | minus S008×crawl = 15 | 1 / 15 / 0 / 56 | yes |
| P5 | append `S017 and S014 and S999` to free-read-verbs | +S017×free-read = 17; outsidePopulation +2 | 1 / 17 / 0 / 58; outside 18→20 | yes |
| P6 | append `S015..S018` to free-read-verbs | +4 pairs = 20 | 1 / 20 / 0 / 61 | yes |
| P7 | ledger add `{S0022, ./corpus/…/static…}` | minus S022×static = 15 | 1 / 15 / 0, ledgerPairs 42 | yes |
| P8 | ledger add uncited `{S007, free-read-verbs}` | 16 + 1 `ledger_pair_not_cited` | 1 / 16 / that 1 exact | yes |
Stdout sha256 of each gate run: P0 5216c7d8…, P1 5eb5790b…, P2 f21b3398…, P3 4d2d9113…, P4 1080f1f8…, P5 e1111f54…, P6 7c02a983…, P7 ddcf20ff…, P8 2317c5b3…. `ALL_MATCH True`.
Result: the gate output changes causally and exactly under removal, narrowing, range-to-list, new literal, new range, numeric spelling with `./`, and ledger fill/uncited inputs. It is not a fixed print of the 16 pairs.

## 3. Can C1 ledger additions rescue frozen C2?
- **P9a**, gate level: frozen ledger ∪ all 18 `pairs.json` pairs (one already present). Declared: 0 unadjudicated + 1 `ledger_pair_not_cited` (S013, ghp-served-set.md, which the frozen corpus does not cite). Actual: exit 1, exactly that. Match.
- **P9b**: frozen ledger ∪ only the 16 C1 oracle pairs. Declared and actual: exit 0, `clean`, ledgerPairs 57. **So the gate itself is rescuable by C1 data. Separability rests entirely on `c2_count.py`'s pins.**
- **P10**, scratch-clone commit `23d99eac…` with frozen/ledger.json replaced by the P9b ledger: exit 2 `snapshot_tampered` ledger.json (out 15060203…). Match.
- **P11**, P10 plus a rehashed `frozen/expected.json` (`fedde109…`): exit 2 `frozen_input_changed` expected.json (c04ad8d3…). Match.
- **P14**, P11 plus `c2-oracle.json` rewritten to expectedPairs [] / exit 0 (`a9f72a92…`): exit 2 `frozen_input_changed` c2-oracle.json (cd677705…). Match.
- **P14o**, the ORIGINAL declared counter bytes (be375d9 `c2_count.py`, sha256 93f39b0f…) on the same commit: exit 0, `passed true`, expected 0, gate clean (d3d7dcb7…). Match with declaration.
**Conclusion:** the original counter could be turned green by co-rewriting oracle, expected file and ledger. The correction 08014ce (pin to DECLARATIONS) is load-bearing and closes that path. With the corrected counter, C1 ledger additions cannot rescue frozen C2. Every rescue path I tried ends in exit 2, never green.
- **P15**: the original counter on the candidate → exit 0, 16/16, byte-identical stdout to the corrected run (4666151c…). The correction changed no verdict on the real candidate.

## 4. Discrepancies / residual weaknesses (author-side findings)
- **D1, my declared expectation was wrong; this is not a candidate defect.** P12: `c2_count` at original base 83528f7 → exit 2 `git_input_unavailable` (6c1160cd…), not the `gate_absent` exit 1 I declared. The base lacks the round-27 frozen inputs, so the `gate_absent` branch is reachable only at the declarations commit. P12b at be375d9 → exit 1 `gate_absent`, detected 0 (5f74a2dd…), which matches `c2-before.json`. The "0/16 on base" claim is evidenced by the separate r26 measure (`r26-fail-open-before.json`), not by `c2_count` at base. Wording should not imply `c2_count` ran on 83528f7.
- **D2, a tradeoff the judge must weigh: the finite oracle is not semantic proof.** P13: scratch commit `a725a915…` replaces `scripts/citing_set.py` with a 3-line stub that prints the 16 hard-coded findings and exits 1. `c2_count` → exit 0, `passed true`, 16/16 (012d9135…). `c2_count` alone accepts a stub. Mitigations observed:
  - The gate fixture selftest at the stub commit gives `passed false`, 29/29 failed, exit 1.
  - At the candidate the same selftest gives 29/29 passed, exit 0.
  - The changed-input probes P1–P8 above.
  But `c2_count` does not bind the selftest or any changed input to its verdict. The C2 green claim MUST cite `c2_count` plus the selftest (or the probes) at the same revision, never `c2_count` alone. Smallest safe correction (for L1, not done here): have `c2_count` also run the candidate's `scripts/citing_set_selftest.py` (or one built-in perturbation, e.g. P1) and require that it pass.
- **D3, trust boundary:** `c2_count.py` executes from the working tree, not from the measured revision. Its DECLARATIONS pin protects only if the operator runs the pinned bytes (913a797f…, recorded in frozen-candidate.json). Keep that hash check in admission.
- The C2 selftest (`c2_count.py --selftest`) → exit 0 (765f90a0…).
- Pair presence ≠ semantic support. Nothing here bears on C1 strict status: C1 remains UNPROVABLE at 55 strictly decided of 58 reviewed. P9 used `pairs.json` only as ledger rows, not as verdict support.

## Verdict for the operability axis (falsification only)
C2 frozen detection reproduces with exact identities. The gate responds correctly to 9 new changed inputs plus 2 C1-union inputs, and the corrected counter blocks every C1/oracle rescue I attempted. Open item: D2. A green based on the finite oracle alone would be false provenance; it must be paired with the same-revision selftest or perturbation evidence.
