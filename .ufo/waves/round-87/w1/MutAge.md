# MutAge — C2 fixed-oracle mutation probe

Axes: calibration (2 HOLD) and freshness (10 HOLD). No score change or admission claimed. Base supplied: `86ca7803fd964db7ae2a628c7e9048741c78a45f`; freeze supplied: `58fee726102aa89ad2c1fa9f697869de3a212510`. Read frozen contract, counter and all cases before probing. No frozen predicate, cases or expected output was changed.

## Detector and results

Expected detector: frozen `count.py` lines 73–80 semantics, using all 17 unchanged cases: actual CLI exit must equal expected exit; successful parsed complete JSON object must equal expected object. Every mutation independently starts from the same pristine candidate; exactly one arithmetic assignment changes. Same 17-case CLI detector runs pristine → mutated → restored for EACH mutant. These are actual subprocess CLI mutants, not merely abstract calculations.

| Isolated change | Independent abstract matched /17 | Actual CLI matched /17 | Missed case numbers | Verdict |
|---|---:|---:|---|---|
| corrected_age_value: age_value + response_delay → age_value | 11 | 11 | 4,5,6,7,9,10 | killed |
| corrected_initial_age: max → min | 8 | 8 | 2,4,5,6,8,9,10,11,12 | killed |
| current_age: corrected_initial_age + resident_time → corrected_initial_age | 10 | 10 | 5,6,7,9,10,11,12 | killed |
| apparent_age: max(0,response_time-date_value) → response_time-date_value | 16 | 16 | 3 | killed |
| corrected_age_value: age_value + response_delay → response_delay | 12 | 12 | 4,5,6,8,11 | killed |
| current_age → 0 (other five fields unchanged) | 7 | 7 | 2,4,5,6,7,8,9,10,11,12 | killed |

All six pristine runs and all six exact-restoration runs matched **17/17**. All six mutants retained **5/5 invalid exits**, actual exit1 for cases 13–17 (inverted request/response, inverted response/now, negative Age, boolean Date, missing Date); valid-case CLI exits remained 0 even when output mismatched. The independent abstract calculation likewise retained all five invalid exits. `constantzero` means only the final arithmetic assignment is replaced, not an implementation returning a malformed scalar or zeroing all six fields. Drop-response-delay and omit-resident likewise remove the term from its downstream sum, retaining the diagnostic delay/resident field.

**Missing mutant kill:** none among these six assigned mutants. No baseline failure, survivor or inconclusive mutant. This does NOT claim all plausible defects are killed; Age-only current_age is a distinct shortcut from ignore-Age and was not an additional actual mutation here.

## Execution and receipts

Evidence directory (all paths absolute): `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/MutAge/`.

- Independent abstract command: `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/MutAge/abstract_probe.py`; exit0, empty stderr. Retained source and full `abstract-results.json`; explicitly labeled abstract model, not candidate CLI execution.
- Actual candidate read from `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ExecAge/cache_current_age.py`, copied into six independent scratch files. No clone and no git/jj mutation.
- Actual commands: `python3 -B /fast/scratch/hyaku/kake-r87/MutAge/NAME.py`, NAME one of `drop_response_delay`, `min_initial`, `omit_resident`, `omit_clamp_apparent`, `ignore_Age`, `constantzero`. Each command receives the unchanged per-case input as stdin JSON, cwd `/fast/scratch/hyaku/kake-r87/MutAge`, timeout10 seconds. Total 306 CLI invocations: 6 mutants × 3 byte states ×17 cases. Every exact argv, stdin, stdout, stderr, exit and match is retained in `NAME-cli.json`; `cli-summary.json` indexes substitutions and hashes. Aggregate probe invocation completed successfully; no timeouts or exceptions.
- Setup: `mkdir -p /fast/scratch/hyaku/kake-r87/MutAge /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/MutAge`, exit0.
- Disposal after retaining receipts: `rm -r /fast/scratch/hyaku/kake-r87/MutAge`, exit0; `test ! -e /fast/scratch/hyaku/kake-r87/MutAge`, exit0.

## Hashes / restoration

Pristine source and every restored scratch copy SHA256: `d1b09ae17a54728a3b967cdc7436f19b62fc98e4304aab64324ee8969454331a`. Executor source remained this digest after probing. Every scratch file was restored to exact original bytes before restored CLI runs and before disposal.

| Mutant | Mutated SHA256 |
|---|---|
| drop_response_delay | `1471ee0076051e203443006d0583bbb95209301d35c1a87815a4cef0af27de6d` |
| min_initial | `a3ffdf83a98119d00a38e2853e8e7c3e60ed05d977c3399f7cc2b27d9f3c7860` |
| omit_resident | `74ebd14ea6b64503d7f60e10ecc5ec67277fef55907f3acd29bf6cdb9357958b` |
| omit_clamp_apparent | `fe630d10e23067385e9e5559f4e62560793a884d2d9f627fa4dae5ab0dc0fa41` |
| ignore_Age | `5ebd0aa25764964d14cd43442cda24f891bd0572a44956e0098f0143555dea4d` |
| constantzero | `f499afebbe3a93640232e72cef3a326c9173d3bd20f880b0d7cfd13648eeda02` |

Frozen cases SHA256 before/after: `cea987d4ce15d53f0f80f59c28b14d2978edde1f0f768daf8aadf900defad25e`. Frozen counter SHA256 before/after: `12b9e9045112ab9d6016731f4880c17912646b664b0dc6d683b6471372cd47e1`. Contract and expected-ledger digests also unchanged. Full before/after receipts: `input-hashes-before.json`, `restoration.json` in the evidence directory.

## Honest limitations / defects

- A fixed finite oracle cannot distinguish correct arithmetic from a lookup implementation hardcoding its 12 successful cases and five rejection exits. Killing these simple formula mutants does not resolve that overfit discriminator limitation or establish general RFC correctness. No new discriminator was added after freeze.
- Counter comparison uses Python dict equality, not exact output-value type validation; bool/int and integral float/int equality can evade its stated exact-integer output requirement. This is source-inspected detector weakness, not an executed additional mutant or claimed exploit result. Invalid-case scoring checks the exit only, not presence of a diagnostic or stdout cleanliness. No frozen counter edit made.
- This probe used the executor candidate bytes above, not an integrated revision and not `count.py --revision`; it reproduces the bounded per-case comparison while preserving the frozen counter. No production selftest, network request, provider probe, build, lint, install, service, browser, source-repository write or runtime delegation performed.
- No tools installed or updated. All created material was confined to this seat's permitted evidence/report paths and its now-deleted scratch.

Self-evaluation: accuracy4 (finite-oracle scope, not universal proof); completeness4 (all six assigned actual mutants and abstract calculations, no extra overfit mutant); clarity4 (raw receipts intentionally separate); actionability4 (exact replacements and commands retained, scratch intentionally disposed); conciseness4 (hash/command detail retained for audit). The highest-value remaining discriminator is an independently chosen off-table input, outside this frozen mutation assignment.
