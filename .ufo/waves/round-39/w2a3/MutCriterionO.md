# MutCriterionO — criterion (o) mutation probe
Axes: operability; freshness of committed byte-level evidence. Synthetic fixtures only; no frozen counter was invoked.
Paths below: `S=/fast/scratch/hyaku/kake-r39a3w2/MutCriterionO`; `U=/fast/scratch/hyaku/kake-r39a3w1/ScribeQualityCriterion`; `C=check_control_inventory.py`; sample paths are `$S/samples/<name>/SCORECARD.md`.
Source checker before/after SHA-256: `26f0911bf7866fc678d4180076ff1df2da3aa78c94f52f7293a9f08a1fa0fb30`; criterion before/after: `cf54466958cb8ade07cf98c8eb3655a9f8867476e69d5c218a2bc634b4c4b798`.
Prepared 15 SCORECARD samples and eight isolated checker copies. Public pre-summary contributed only label/hash fields; its source SHA-256 was `98e44fe613c85b660f3b12cd60ecc8973fe989114bcd1eb758fff56d2d16998b`.
## Executed commands and outputs
Commands are shown with the path aliases above; every subprocess had timeout ≤15s and AS ≤4,000,000,000 bytes; detector concurrency was two workers.
`timeout 120s prlimit --as=4000000000 -- python3 -B $S/probe.py prepare` → exit 0; `PREPARED: 15 SCORECARD samples; 8 isolated pristine checker copies; chronology_exit=0`.
`timeout 120s prlimit --as=4000000000 -- python3 -B $S/probe.py pristine` → exit 0; all eight detectors exit 0, checker exits `(valid,negative)=(0,1)`.
`timeout 20s prlimit --as=4000000000 -- cp -R probes/. mutants/` (cwd `$S`) → exit 0; preserved all eight mutant byte sets before restoration.
`timeout 120s prlimit --as=4000000000 -- python3 -B $S/probe.py mutated` → exit 0; all eight detectors exit 1, checker exits `(0,0)`, verdict `killed`.
`timeout 20s prlimit --as=4000000000 -- cp $U/$C $S/probes/<id>/$C` → exit 0 for each of the eight IDs below; restored exact original bytes.
`timeout 120s prlimit --as=4000000000 -- python3 -B $S/probe.py restored` → exit 0; all eight detectors exit 0, checker exits `(0,1)` again.
`timeout 120s prlimit --as=4000000000 -- python3 -B $S/probe.py adversarial` → exit 0 (observations collected, not a conformity pass); five unexpected accepts.
P39 was the actual stdout for every mutant negative: `PASS: 39/39 byte-bearing pre-declaration scores SHA-pinned and classed; absent baseline explicit; post-declaration scope explicit`. P40 below is the identical message with `40/40`. All checker stderr was empty.
## Eight single-point mutants and expected detectors
Each fixed detector requires the valid inventory to exit 0 and its listed negative to exit 1, unchanged across pristine/mutated/restored phases. Results: **8 killed, 0 survived, 0 inconclusive**; no baseline failed. Preserved paths: `$S/mutants/<id>/$C`.
| ID | Mutant path:line and defect | Negative sample | Mutant SHA-256 |
|---|---|---|---|
| M01_missing_guard | `$C:81`, drop missing-row guard | missing_row | `7279c466506efb7b69669dba850a3097443af0db931d4d70dcdaf7f5460e9c50` |
| M02_hash_compare | `$C:74`, compare class but not digest | hash_typo | `7f120da6aef15c10aa008dbab658f52184ac3bfa3086c3dad29f0e802a174275` |
| M03_extra_guard | `$C:81`, drop extra-label guard | extra_label | `04bc2041488479e482b8acf850bbebbcdcca96f26cb417e961b68ecbb6a3f3f1` |
| M04_duplicate_guard | `$C:81`, drop duplicate-label guard | duplicate_label | `09da5b5ec6cd8bdf68006bc5879598fffd95c3e92bd85ae1210039cf7e04e023` |
| M05_policy_guard | `$C:80`, force policy_ok=True | missing_policy | `16095f22e6e4a0656820b7b0aef5a396890894725ea1f787ed0ec13c19697ed1` |
| M06_baseline_omission | `$C:74`, exempt base from missing checks | missing_baseline | `8773e1e2f5afcb7de291bc2d5d8dbd3dc29bd272b8dbf09114f10a3e917ce986` |
| M07_class_compare | `$C:74`, compare digest but not class | wrong_class | `776bf3177d366c589f5de6fe2f02b2a05e9de031e33cb88fdfc21f8d8c0a559e` |
| M08_worktree_read | `$C:29-30`, read worktree instead of Git revision | worktree_bait | `ff64447138523a6c61800037f85c87151d3090f3109d2da25eee282b375f05c5` |
Restoration evidence: all eight `$S/probes/<id>/$C` have pristine/restored before-and-after SHA-256 `26f0911bf7866fc678d4180076ff1df2da3aa78c94f52f7293a9f08a1fa0fb30` in `results/pristine.json` and `results/restored.json`; mutant before/after hashes match the table. Exact child commands, exits, stdout and stderr are retained in phase JSON.
## Adversarial SCORECARD findings on the unmodified checker
All seven negatives below should reject under criterion (o), independently of whether the narrower matcher intentionally omits those checks. No synthetic score is represented as a real frozen-counter result.
| Sample path:line | Actual checker output/exit | Finding | SCORECARD SHA-256 |
|---|---|---|---|
| `code_only/SCORECARD.md:1-57` | P39 / 0 | Accepts inventory and policy entirely in a fenced, explicitly rejected example; operative declaration inventories nothing. | `76c7195715a9b9742570c7336b07d8dc9b3e4e96bfa60b8f6dd9e138d9115afe` |
| `hash_typo/SCORECARD.md:7` | FAIL, `1 of 39 byte-bearing scores missing/wrong` / 1 | Correctly rejects a one-hex-digit typo. | `7af21b5d29bfb309285713fde4976e19e8aa1e3307f0dfcb0658b263d33f9737` |
| `after_declaration/SCORECARD.md:3,8,53` | P40 / 0 | Accepts a post-declaration score as pre-declaration when supplied a later descendant summary, despite the scorecard citing the older summary. | `0d056a6eafdcdd6996d93d5a3c05c4ce86123918e3e53ccb2efd0f445ed4b8df` |
| `empty_inventory/SCORECARD.md:5-9` | FAIL, `39 of 39 byte-bearing scores missing/wrong`, `absent_baseline=missing` / 1 | Correctly rejects an empty table. | `534b4143440fe6ddbe425db46e898f7adf4f1ad2b59308590241adaf2bba0801` |
| `no_summary_revision/SCORECARD.md:1-5` | P39 / 0 | Accepts no source/revision citation whatsoever; regex `^Source:|\b[0-9a-f]{40}\b` had no matches. | `eea6a0d2bacce70c0e81c2497316933f7c793526dc210d0921659db3226b423a` |
| `comment_only/SCORECARD.md:1-54` | P39 / 0 | Accepts inventory and policy hidden in an explicitly non-operative HTML comment. | `4bc5a3e7c88681dccf8135a380095c38d67565b0239e9c03a686331ded563ef2` |
| `quoted_policy/SCORECARD.md:48-52` | P39 / 0 | Accepts the required sentence as rejected quotation while operative text explicitly adopts the opposite policy. | `e196783f6702e57ddb752dc0ae4809a6edf4bf9d397711f393603535b9f59bcd` |
Exact fence command: `timeout 15s prlimit --as=4000000000 -- python3 -B $U/$C --repo $S/fixture-repo --revision d8682c3911684d9fca431b20cdae673e6177f27d --summary-revision 62338ef348d434e088bad391724304c9c9f2a845` → exit 0, P39.
Exact late-score command: `timeout 15s prlimit --as=4000000000 -- python3 -B $U/$C --repo $S/fixture-repo --revision 0c870068e8a7204bbd0943c8b676c4a5dd88d5c7 --summary-revision d6f148a7aa2a2512d087ad697abae15473432909` → exit 0, P40.
`timeout 15s prlimit --as=4000000000 -- git -C $S/fixture-repo merge-base --is-ancestor 0c870068e8a7204bbd0943c8b676c4a5dd88d5c7 d6f148a7aa2a2512d087ad697abae15473432909` → exit 0. This temporal attack requires the explicit later-summary override; no default-mode chronology guarantee is claimed.
## Per attacked statement
**holds (tested cases):** `criterion-o.md:11` label/digest/class equality, exactly-once rows and absent baseline; typo, missing/extra/duplicate rows, wrong class and omitted base rejected, with corresponding mutants killed (`$U/$C:70-81`).
**holds (tested case):** `criterion-o.md:11` reads committed bytes, not worktree; committed-empty/worktree-valid bait rejected, M08 killed (`$U/$C:28-31`).
**overstated as complete criterion coverage:** `criterion-o.md:5` declaration's control-class text; raw scanning at `$U/$C:57-72` treats rejected code/comment examples as the actual declaration.
**wrong if PASS is used to certify this requirement:** `criterion-o.md:5` identify committed summary revision; `$U/$C:37-44,74-81` neither requires a scorecard citation nor binds that citation to the selected summary.
**overstated:** `criterion-o.md:5,11` explicit operative post-declaration distinction; substring membership at `$U/$C:80` accepts rejected/opposed wording and `$U/$C:41-44` admits a later summary. This is checker coverage failure, not a proposal to weaken (o).
## Evidence artifacts (SHA-256; all paths under S)
`probe.py`: `fbb29bc7826c3310a89876a7b5f8b0be8b0bc82f16c7d926c3b12cb23d164643`; `manifest.json`: `2b7daef9de29eacc08b789e8fc1ce68be3ef3d81a90559abdc5d500aab438b8d` (every sample path/hash/tree and summary revision).
`results/pristine.json`: `d56812b53bf9a8feb425ea2eec043c9341dde78537303d1cbba24f6706689654`; `results/mutated.json`: `57fee5c7140300cd043a5040ab7b6bbf0d4cf610361c0e540f02adb039aecc6c`.
`results/restored.json`: `5597300a7063a50655d6f5b2568af17fd6074b0303d3e465fe56fb49be8beb10`; `results/adversarial.json`: `34b020c5e50e79797c1102c6b3eb6e1afb5b7d19d011ff006857ae1e47a7d144`.
Hash command (cwd S): `timeout 20s prlimit --as=4000000000 -- sha256sum $U/$C $U/criterion-o.md probe.py manifest.json results/pristine.json results/mutated.json results/restored.json results/adversarial.json mutants/*/check_control_inventory.py` → exit 0, hashes above.
Only sandbox artifacts and this report were written. No sibling/lane source, lane Git index/state, sealed paths, keys, counter, network, other agent runtime, package install/update or live property was touched; all bounded child processes completed and were reaped. No round verdict or integration performed.
