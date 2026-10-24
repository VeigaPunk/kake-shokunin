# MutFamilyR — five surviving R-only controls
Survivors first: `m02_file_gate.py`, `m03_url_gate.py`, `m04_empty_id.py`, `m05_ascii_id.py`, `m06_last_id.py`.
Axes: operability (attacked); freshness (preserved frozen inputs). Ten single-line R-only mutants; five survived, five killed, none inconclusive. No round verdict issued.
Paths: `R=/home/vgpnk/Projects/shokunin/kake-shokunin`; `S=/fast/scratch/hyaku/kake-r40w1/MutFamilyR`; `C=$R/.ufo/waves/round-40/c1_count.py`. Every table tool is `$S/mutants/<name>`; `N` below is its basename without `.py`.
Expected detector: a weakened R repair should lose at least one witness or regression, making `met=false` (counter exit 1); a failing pristine/restored baseline would be inconclusive instead.

## Mutants and actual counter outputs (survivors first)
All rows: E=9/9, U=13/13, selftest exit=0 / `PASS 150/150`. Columns supply the remaining per-tool counter fields; SHA256 is the scored artifact's full digest.
| Tool:line | Exact replacement line | SHA256 | passed/30; R; met; exit; verdict |
|---|---|---|---|
| m02_file_gate.py:338 | `if isinstance(ident, str) and (not isinstance(raw.get("file"), str) or not _file_value_invalid(raw["file"])):` | f7e1e4be1c845b28124badf8e3cb93fe0e4cdefc80debe0e6a0aa88a70a2fd63 | 30; 8/8; true; 0; survived |
| m03_url_gate.py:338 | `if isinstance(ident, str) and (not isinstance(raw.get("sitemapUrl"), str) or _parse_url(raw["sitemapUrl"]) is not None):` | 54d2272bd0e9beefb5f69929bbd499616e55b4d3b993dddcebcd043c0ab51750 | 30; 8/8; true; 0; survived |
| m04_empty_id.py:338 | `if isinstance(ident, str) and ident:` | 59d1295b611d942b08b765c8b4e81bde32f2e8be47f820f19242425749c17c7d | 30; 8/8; true; 0; survived |
| m05_ascii_id.py:338 | `if isinstance(ident, str) and ident.isascii():` | 87ae2a3ad2aea4c15a32a74a641981d68f1309a10b9c9f0d1f0156afe5a061b4 | 30; 8/8; true; 0; survived |
| m06_last_id.py:340 | `seen_ids.clear(); seen_ids.add(ident)` | 27ca212009a47e7e124c7e79ea56f83edeb1494f6bf65ead8782039cc7e6b5ec | 30; 8/8; true; 0; survived |
| m01_type_gate.py:338 | `if isinstance(ident, str) and isinstance(raw.get("file"), str) and isinstance(raw.get("sitemapUrl"), str):` | 2517b407b60c62d1b14c69a3bba1c3aac610ef42a226c25d2ff39cd7a11590cf | 25; 3/8; false; 1; killed |
| m07_folded_id.py:340 | `seen_ids.add(ident.casefold())` | e8ef375c532790b925e14cf4d6b90478d02f2fce06d341a9ac7508a3897f954b | 29; 7/8; false; 1; killed |
| m08_second_id.py:339 | `duplicate = ident in seen_ids and len(seen_ids) < 2` | f27a059c0ae84c952aa512409e0bc7284f85c741c66bb60fa32f102598081f59 | 29; 7/8; false; 1; killed |
| m09_file_type.py:338 | `if isinstance(ident, str) and isinstance(raw.get("file"), str):` | 6ae27d8de8888421d71a2aada964c620911938202f45f722f9451caf4d89135d | 27; 5/8; false; 1; killed |
| m10_url_type.py:338 | `if isinstance(ident, str) and isinstance(raw.get("sitemapUrl"), str):` | 2360a5b53654dde4264634a615698a3f69c1a674e790c388ea6ad76e799bb6de | 28; 6/8; false; 1; killed |
Killed rows: m01 fails R1–R5; m07 R8; m08 R5; m09 R1/R3/R5; m10 R2/R4. False negatives output `clean/None/[]` instead of `error/check_invalid/[]`; m07's R8 outputs that error where clean was required.

## Commands, receipts, and restoration
Executed: `timeout 1200 prlimit --as=4000000000 python3 -B /fast/scratch/hyaku/kake-r40w1/MutFamilyR/run_family.py` → exit 0; two workers, each child counter bounded to 1200 seconds and inheriting the 4 GB address-space limit.
Each mutated argv: `python3 -B "$C" --root "$R" --tool-file "$S/mutants/$N.py" --label "MutFamilyR-$N" --seed 400401 --out "$S/receipt-$N.json"` → exits in table.
For each `STAGE=pristine,restored`: `python3 -B "$C" --root "$R" --tool-file "$S/probes/$N.py" --label "MutFamilyR-$N-$STAGE" --seed 400401 --out "$S/receipt-$N-$STAGE.json"` → all twenty exit 0; each passed=30, byClass={E:9/9,R:8/8,U:13/13}, selftest={exit:0,summary:"PASS 150/150"}, met=true.
Initial independent baseline: `timeout 1200 prlimit --as=4000000000 python3 -B "$C" --root "$R" --tool-file "$S/pristine.py" --label MutFamilyR-pristine --seed 400401 --out "$S/receipt-pristine.json"` → exit 0 with those same complete results.
Exact expanded argv, exit codes, stdout/stderr, receipts and before/mutated/after hashes: `$S/logs/$N.json`; aggregate `$S/family-results.json`. Retained mutants are intentional control artifacts; every isolated `$S/probes/$N.py` was restored byte-for-byte, including after counter failure.
Every probe's before/after SHA256, and reference/pristine SHA256: `03a8fba4930ad7628a569e7aa30b3ece728fbb6eb3fa4ac7c9a78dfbeb07b22b`; every `restoredExact=true`. Mutated probe hashes equal the corresponding retained artifact hashes above.
Frozen counter SHA256: `6d73b8f498a29a5a86c9a7f1ce5d87cd135c40f1b634d869d14659cc10bee8d8`. Hash command: `timeout 30 prlimit --as=4000000000 sha256sum /fast/scratch/hyaku/kake-r40/shared/ref_fix.py "$S/pristine.py" "$C"` → exit 0.

## Independent confirmation that survivors are real defects
Executed: `timeout 1200 prlimit --as=4000000000 python3 -B /fast/scratch/hyaku/kake-r40w1/MutFamilyR/contract_probe.py` → exit 0. Uses the frozen counter's unchanged bubblewrap launcher and exact-output judge; six contract-derived cases, not replacement scoring witnesses.
Cases: m02 earlier absolute file and earlier `..` segment; m03 earlier relative sitemapUrl; m04 earlier missing-file check with id `""`; m05 same with id `"κ"`; m06 missing-file id `left`, valid id `right`, then repeated valid `left`.
All six pristine/restored CLI runs: exit 2, exact expected JSON matches. Every mutant CLI run also exits 2 but incorrectly reports the repeated check clean: `check 1: got clean/None/[] want error/check_invalid/[]` (m06: `check 2`). Thus exit-only detection would miss these defects.
All six supplemental probe targets restored exactly, with the same reference hash above. Full commands, actual stdout/stderr, expected JSON and stage hashes: `$S/contract-results.json`.

## Attacked statements
**Wrong:** “the eight R witnesses kill every weakening.” `$C:127-139` covers missing/wrong-type members, non-object/non-string exclusions and case distinction, but not invalid path values, invalid URL values, empty/Unicode ids, or an intervening distinct id. Five demonstrated partial repairs meet the full frozen predicate.
**Holds for these probes:** reference registration at `/fast/scratch/hyaku/kake-r40/shared/ref_fix.py:335-340` honors contract sentence 4 (`$R/.ufo/waves/round-39/c1-contract.md:22-25`); six supplemental pristine/restored cases match.
**Holds:** the counter kills the tested type-gated registration, case-folded storage and two-id duplicate weakening; exact failed witness ids are recorded above.
These survivors skip R sub-shapes while retaining E/U; they fit the frozen partial-repair control definition (`$R/SCORECARD.md:2608-2616`). This reports measurements and coverage findings only; integration/scoring remains with KakeR40.
No network, installs, runtime switching, lane source/index/jj mutations, or sibling/shared writes. Child process groups were killed/reaped by both harnesses; all started jobs completed. Only this report was written in the lane.
