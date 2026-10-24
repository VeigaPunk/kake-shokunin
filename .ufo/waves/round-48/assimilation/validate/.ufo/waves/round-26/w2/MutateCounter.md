# Round-26 counter mutation probe — MutateCounter

## Scoped verdict

**DISAGREE — medium: `--selftest` does not protect all assigned load-bearing counter rules.** Twelve independent one-line mutations were tested: **6 killed, 6 survived, 0 inconclusive**. All twelve pristine runs and all twelve restored runs passed the same 14 existing fixtures (exit 0). The surviving boundary, maximum-word, document-group-distinctness, aggregate-statement-count, and manifest-SHA mutations are coverage findings, not evidence that the unmodified candidate receipts are stale or permission to weaken the contract. This report does not accept/reject the whole round or change any production rule.

**Axes:** freshness (quote boundaries/length/specificity and retained-byte integrity); operability (correct counts, retry selection, exit status, and reproducible restoration).

**Target:** `.ufo/waves/round-26/measure.py`, task-supplied candidate `e28312b14b076584fedd696fae2a684e460bd11e`, base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`. Findings are bound to the exact working-file SHA-256 below; commit identity was supplied by tasking and was not independently re-run through Git.

## Method and hard-bound accommodation

The assignment requests in-memory mutations and `python3 -B <copy> --selftest`. Its stronger lane bounds permit **only this report as an on-disk write**. Stock `run_case` creates a temporary directory (`measure.py:726`), calls `commit_fixture` (`:728`), and writes fixture files/Git indexes (`:632-641`). Therefore running the stock filesystem backend verbatim would violate the bounds.

Each child instead executed the **exact pristine or single-line-mutated target bytes** from a Linux anonymous `memfd`, using the literal command shape `python3 -B /proc/self/fd/<fd> --selftest`. A second inherited, anonymous memfd contained a `sitecustomize.py` ZIP that adapts only fixture filesystem/Git I/O to dictionaries. The target's 14 `CASES`, `fixture_files`, `commit_fixture`, `run_case`, `evaluate`, `score`, `Git` object-reader/parser methods, all load-bearing checks, expected outcomes, and `main` remain otherwise unchanged. There are no extra detector cases. The adapter also installs a Python audit hook rejecting real filesystem mutations and real subprocess launches in every detector child. Fixture Git operations are synthetic in-memory protocol responses, **not executions of Git**.

**Limitation:** these are results for the existing selftest logic with its fixture-I/O boundary adapted to memory. They do not verify native Git/filesystem operability or claim an unadapted on-disk selftest run. The common adapter is reproduced below and is identical for pristine, mutated, and restored executions. A passing baseline is required for every mutant.

The twelve independent pristine→mutated→restored triads were run concurrently (up to 12 workers); phases inside a triad were ordered. Every mutation starts from the original source, changes exactly the single line shown, and is not combined with any other mutation. No corpus, script, index, sibling lane, host service, website, or other runtime was mutated or invoked. No network requests were made. Only round-26 material was inspected. No tools were installed or upgraded; the Eval harness reported Python 3.14.8. Child commands invoked `python3` exactly as recorded below.
## Hash and restoration evidence

- Original: **38337 bytes, 780 lines**.
- Before SHA-256: `061bd2438470bf4c85204fb836917e3d0fccf773c882e1ccb96d31f2fefd1c83`.
- After all probes, re-read real target SHA-256: `061bd2438470bf4c85204fb836917e3d0fccf773c882e1ccb96d31f2fefd1c83`.
- Real target bytes equal original: `true`. The real target was never edited.
- Every restored in-memory subject has SHA-256 `061bd2438470bf4c85204fb836917e3d0fccf773c882e1ccb96d31f2fefd1c83` and passed 14/14, exit 0.
- Common in-memory adapter ZIP SHA-256: `637362c7a416ec701e57e6f06729b9a8d843597b23c6b7b5a587464196e28eb4`.
- Every source/adapter memfd was closed in `finally`; virtual fixture dictionaries were cleared by context exit. No disposable directory or script was created, so no on-disk scratch remains to delete. All 36 detector stderr streams were empty.

## Exact mutations and detector outcomes

All paths/line numbers in this table refer to `.ufo/waves/round-26/measure.py`. `P/M/R` means pristine/mutated/restored process exit.

| ID | Line / rule | Exact old → new expression | Expected detector | Actual P/M/R; mutated fixture result | Verdict |
|---|---|---|---|---|---|
| M01 | 276 / quote left boundary | `return re.search(r"(?<!\w)" + re.escape(needle) + r"(?!\w)", text) is not None` → `return re.search(re.escape(needle) + r"(?!\w)", text) is not None` | survives: no embedded-left-boundary fixture | 0/0/0; 14 passed / 0 failed | **SURVIVED** |
| M02 | 276 / quote right boundary | `return re.search(r"(?<!\w)" + re.escape(needle) + r"(?!\w)", text) is not None` → `return re.search(r"(?<!\w)" + re.escape(needle), text) is not None` | survives: no embedded-right-boundary fixture | 0/0/0; 14 passed / 0 failed | **SURVIVED** |
| M03 | 389 / minimum alphanumeric tokens | `if tokens < 6 or words > 25:` → `if tokens < 5 or words > 25:` | killed: short_quote becomes accepted | 0/1/0; 13 passed / 1 failed | **KILLED** |
| M04 | 389 / maximum whitespace words | `if tokens < 6 or words > 25:` → `if tokens < 6 or words > 26:` | survives: no 26-word fixture | 0/0/0; 14 passed / 0 failed | **SURVIVED** |
| M05 | 421 / distinct quotes inside document groups | `if hits or twins:` → `if hits:` | survives: no document-group twin fixture | 0/0/0; 14 passed / 0 failed | **SURVIVED** |
| M06 | 447 / statement ledger total | `output["statements"] += n` → `output["statements"] += stale` | survives: run_case does not assert statement totals | 0/0/0; 14 passed / 0 failed | **SURVIVED** |
| M07 | 452 / correction tag multiplicity | `if tags < stale:` → `if tags == 0:` | killed: statement_correction_absent loses its finding | 0/1/0; 13 passed / 1 failed | **KILLED** |
| M08 | 208 / population SHA pin | `if hashlib.sha256(raw).hexdigest() != pin:` → `if False:` | killed: tampered_population becomes accepted | 0/1/0; 13 passed / 1 failed | **KILLED** |
| M09 | 320 / decompressed fetch SHA pin | `if hashlib.sha256(raw).hexdigest() != expected_sha:` → `if False:` | killed: bad_sha loses fatal fetch_sha_mismatch | 0/1/0; 13 passed / 1 failed | **KILLED** |
| M10 | 309 / manifest SHA pin | `if field(entry, "sha256") != expected_sha:` → `if False:` | survives: no manifest-SHA mismatch fixture | 0/0/0; 14 passed / 0 failed | **SURVIVED** |
| M11 | 304 / retry precedence | `entry = self.retry[key] if key in self.retry else self.base.get(key)` → `entry = self.base.get(key)` | killed: effective S008 falls back to failed base fetch | 0/1/0; 2 passed / 12 failed | **KILLED** |
| M12 | 468 / findings influence on exit status | `return 0 if output["decided"] == EXPECTED and not output["findings"] else 1` → `return 0 if output["decided"] == EXPECTED else 1` | killed: ledger-only findings incorrectly exit zero | 0/1/0; 12 passed / 2 failed | **KILLED** |

### Per-mutant SHA-256

All before/restored hashes are the original hash above; each mutated subject hash is:

| Mutant | Mutated SHA-256 |
|---|---|
| M01 | `ef50ce20a8ed55098d397ebd7de0f29057eaa7c4bdb49fb4c4331ae1f3fb23a0` |
| M02 | `514bcbbea9db0d360b69e1d759374f6fabac8c1c48c049fe93df9e57ae99833b` |
| M03 | `e488982db76bec9bdf101c768c518337cc80b89200a2f637f94d8d148f40ac63` |
| M04 | `43de10cf5252930d9d83f0dad8d9414bce2a4dc03cc179d4effc3a4892f02602` |
| M05 | `28113287bb2ce2284a60479eadff0ac744906dd219a6db6e1e7b78e457815ba4` |
| M06 | `72d9bdc1d8a27e9fa19708ee978ac62a020f0f1cb371a5386e324298fa7e10dd` |
| M07 | `5eea78a1f0ded7aac6ea82922400f20c6aede33cee7cc5e0fbda894c70369e94` |
| M08 | `537dfebf2b512d36864771b40c1f459ab5e8264fe4a05b8de924576fb18a7b67` |
| M09 | `3a5c895232098d028b1495b382ebb8317d86c8891c872bd92fd07717a040f909` |
| M10 | `125ebccab5dbf950246ccab6afaf1b7b0016bc394794ec974f355d37cef2fe50` |
| M11 | `f3b10d8e1892fa2039de734c8df9d128dba0731a838110caaf57bd3c7e795bb1` |
| M12 | `b484aa8d5022f8fba8022c5f41435dd9cb86dac6ad29c0044231e4df774fa9c8` |

## Criterion-specific evidence and minimal corrections

### Six surviving mutations: gaps in the detector, not changes to the contract

- **M01 / M02 — word boundaries.** `measure.py:273-276` says “no word character on either side” and implements both lookarounds. Removing either lookaround still produced 14/14, exit 0. The cases at `:685-715` contain no quote that is only a suffix/prefix of a source word. **Minimal correction:** add two receipt fixtures using, for example, `fixture_quote("S004")[2:]` and `fixture_quote("S004")[:-1]`, respectively. Each should retain valid token/word counts but require `quote_not_in_text`, decided 31, exit 1. These proposed fixtures were not executed in this probe.
- **M04 — maximum words.** Contract amendment `contract-amendment.json:12` requires “>=6 alphanumeric tokens and <=25 whitespace words.” The single `words > 25` → `words > 26` defect at `measure.py:389` survived. The existing `short_quote` case at `:694-695` exercises only the lower token bound. **Minimal correction:** add a 26-whitespace-word quote fixture and assert the specific `quote_word_count` finding, not merely a failing exit; a not-in-text fallback must not mask removal of the length check.
- **M05 — distinct quotes inside a document group.** Amendment `:13` requires the `{S010,S028,S033}` group to use distinct quotes. `measure.py:419-422` computes `twins`, but changing `if hits or twins:` to `if hits:` survived. `boilerplate_quote` at `:708-710` exercises cross-row hits outside the group, not identical in-group quotes. **Minimal correction:** construct a fixture in which two grouped rows have the same, group-only source text and identical normalized quotes, with consistent raw bytes/manifest/population pins; require `quote_not_row_specific` for both. Include a distinct-quote control so the documented group exemption itself remains allowed.
- **M06 — statement ledger count.** `measure.py:447` accumulates the total `n`; the mutant accumulated `stale` instead and still passed 14/14. The existing ledger explicitly differs (`:683`: `"statements": 2, "stale": 1`). `run_case` only checks exit, finding IDs, decided rows, and local-population source (`:733-740`); it does not assert any of the three statement counters. **Minimal correction:** make the clean fixture assert `statements == 2`, `statementsStale == 1`, and `statementCorrections == 1`, and provide appropriate expected totals for the altered-ledger/absent-ledger/baseline cases. [INFERENCE] The mutated clean evaluation's statements total would be 1 instead of 2; that numeric field is not emitted by the current selftest JSON, so the observed result here is the escaped assertion, not a separate runtime observation of that field.
- **M10 — manifest/population SHA consistency.** `measure.py:309-310` rejects a manifest digest that differs from the pinned population digest. Bypassing that check survived 14/14. Existing `bad_sha` (`:689-690`) mutates decompressed bytes, and `tampered_population` (`:706`) changes population bytes; neither isolates this check. **Minimal correction:** change only the base-manifest `sha256` for a non-retry row such as S003, preserving correct population and raw bytes. Require fatal `manifest_population_mismatch`, decided 31, exit 2.

These are six independently surviving defects across five missing coverage areas (left/right boundaries count as one area). Do not remove or relax the existing checks. The minimal correction is detector coverage at these exact boundaries/counters, followed by replay of these mutations by the integration owner.

### Six killed mutations: specific successful detector protections

- **M03:** the five-token `short_quote` became accepted: observed exit 0 / decided 32 / no findings versus expected exit 1 / decided 31 / `quote_word_count`. Selftest failed 1/14 and exited 1.
- **M07:** the one-tag/two-STALE-statement `statement_correction_absent` fixture lost its finding under `tags == 0`: observed exit 0 / decided 32 / no findings versus expected exit 1 / `statement_correction_absent`. Selftest failed 1/14 and exited 1.
- **M08:** `tampered_population` became accepted: observed exit 0 / decided 32 / no findings versus expected exit 2 / decided 0 / `population_tampered`. Selftest failed 1/14 and exited 1.
- **M09:** `bad_sha` lost fatal digest classification: observed exit 1 / `quote_not_in_text` versus expected exit 2 / `fetch_sha_mismatch`; decided remained 31. Exact finding/exit comparison killed the mutant rather than mistaking an unrelated rejection for protection of SHA integrity. Selftest failed 1/14 and exited 1.
- **M11:** replacing retry precedence with base-only lookup made the clean fixture use S008's failed initial fetch (`:604-608`), yielding `manifest_entry_invalid`, exit 2, decided 31 instead of clean exit 0, decided 32. All affected cases are included verbatim in its output below. This checks effective retry selection, not a live refetch.
- **M12:** both ledger-only finding cases (`statement_correction_absent`, `statements_absent`) kept their expected finding IDs/32 decided but incorrectly exited 0. Selftest failed 2/14 and exited 1, verifying findings must affect exit status even without undecided rows.

## Actual commands and output references

Each command below was executed, not merely suggested. Numeric FD paths are ephemeral inherited memory handles and are now closed. Output blocks are deduplicated by exact stdout bytes; shared references mean byte-identical actual output, not an omitted run. All listed stderr values are the empty string. The backend-adapter environment for every command was `PYTHONPATH=/proc/self/fd/<adapter-fd>`, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONHASHSEED=0`, with the adapter ZIP inherited via `pass_fds` and the lane as cwd.

| Mutant | Phase | Actual command | Exit | Actual stdout | stderr |
|---|---|---|---|---|---|
| M01 | pristine | `python3 -B /proc/self/fd/9 --selftest` | 0 | O01 | `""` |
| M01 | mutated | `python3 -B /proc/self/fd/9 --selftest` | 0 | O01 | `""` |
| M01 | restored | `python3 -B /proc/self/fd/9 --selftest` | 0 | O01 | `""` |
| M02 | pristine | `python3 -B /proc/self/fd/11 --selftest` | 0 | O01 | `""` |
| M02 | mutated | `python3 -B /proc/self/fd/11 --selftest` | 0 | O01 | `""` |
| M02 | restored | `python3 -B /proc/self/fd/11 --selftest` | 0 | O01 | `""` |
| M03 | pristine | `python3 -B /proc/self/fd/15 --selftest` | 0 | O01 | `""` |
| M03 | mutated | `python3 -B /proc/self/fd/15 --selftest` | 1 | O02 | `""` |
| M03 | restored | `python3 -B /proc/self/fd/15 --selftest` | 0 | O01 | `""` |
| M04 | pristine | `python3 -B /proc/self/fd/23 --selftest` | 0 | O01 | `""` |
| M04 | mutated | `python3 -B /proc/self/fd/18 --selftest` | 0 | O01 | `""` |
| M04 | restored | `python3 -B /proc/self/fd/18 --selftest` | 0 | O01 | `""` |
| M05 | pristine | `python3 -B /proc/self/fd/35 --selftest` | 0 | O01 | `""` |
| M05 | mutated | `python3 -B /proc/self/fd/14 --selftest` | 0 | O01 | `""` |
| M05 | restored | `python3 -B /proc/self/fd/14 --selftest` | 0 | O01 | `""` |
| M06 | pristine | `python3 -B /proc/self/fd/22 --selftest` | 0 | O01 | `""` |
| M06 | mutated | `python3 -B /proc/self/fd/22 --selftest` | 0 | O01 | `""` |
| M06 | restored | `python3 -B /proc/self/fd/22 --selftest` | 0 | O01 | `""` |
| M07 | pristine | `python3 -B /proc/self/fd/32 --selftest` | 0 | O01 | `""` |
| M07 | mutated | `python3 -B /proc/self/fd/26 --selftest` | 1 | O03 | `""` |
| M07 | restored | `python3 -B /proc/self/fd/26 --selftest` | 0 | O01 | `""` |
| M08 | pristine | `python3 -B /proc/self/fd/19 --selftest` | 0 | O01 | `""` |
| M08 | mutated | `python3 -B /proc/self/fd/19 --selftest` | 1 | O04 | `""` |
| M08 | restored | `python3 -B /proc/self/fd/19 --selftest` | 0 | O01 | `""` |
| M09 | pristine | `python3 -B /proc/self/fd/47 --selftest` | 0 | O01 | `""` |
| M09 | mutated | `python3 -B /proc/self/fd/28 --selftest` | 1 | O05 | `""` |
| M09 | restored | `python3 -B /proc/self/fd/28 --selftest` | 0 | O01 | `""` |
| M10 | pristine | `python3 -B /proc/self/fd/53 --selftest` | 0 | O01 | `""` |
| M10 | mutated | `python3 -B /proc/self/fd/35 --selftest` | 0 | O01 | `""` |
| M10 | restored | `python3 -B /proc/self/fd/31 --selftest` | 0 | O01 | `""` |
| M11 | pristine | `python3 -B /proc/self/fd/44 --selftest` | 0 | O01 | `""` |
| M11 | mutated | `python3 -B /proc/self/fd/25 --selftest` | 1 | O06 | `""` |
| M11 | restored | `python3 -B /proc/self/fd/25 --selftest` | 0 | O01 | `""` |
| M12 | pristine | `python3 -B /proc/self/fd/56 --selftest` | 0 | O01 | `""` |
| M12 | mutated | `python3 -B /proc/self/fd/17 --selftest` | 1 | O07 | `""` |
| M12 | restored | `python3 -B /proc/self/fd/17 --selftest` | 0 | O01 | `""` |

### Verbatim stdout payloads

#### O01

SHA-256 of actual stdout (including its final newline): `f1ea1874a68c234dc5c93095883d4ad06e746ba2ab47a97cf9296c70172a8832`.

```json
{"cases": [{"case": "complete_clean", "decided": 32, "exit": 0, "expectedDecided": 32, "expectedExit": 0, "expectedFindings": [], "findings": [], "passed": true, "populationSource": "revision"}, {"case": "missing_receipt", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["receipt_missing"], "findings": ["receipt_missing"], "passed": true, "populationSource": "revision"}, {"case": "bad_sha", "decided": 31, "exit": 2, "expectedDecided": 31, "expectedExit": 2, "expectedFindings": ["fetch_sha_mismatch"], "findings": ["fetch_sha_mismatch"], "passed": true, "populationSource": "revision"}, {"case": "quote_not_in_text", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["quote_not_in_text"], "findings": ["quote_not_in_text"], "passed": true, "populationSource": "revision"}, {"case": "short_quote", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["quote_word_count"], "findings": ["quote_word_count"], "passed": true, "populationSource": "revision"}, {"case": "stale_without_correction", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["correction_missing"], "findings": ["correction_missing"], "passed": true, "populationSource": "revision"}, {"case": "stale_marker_absent", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["stale_marker_absent", "statement_correction_absent"], "findings": ["stale_marker_absent", "statement_correction_absent"], "passed": true, "populationSource": "revision"}, {"case": "unverifiable_undecided", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["row_unverifiable"], "findings": ["row_unverifiable"], "passed": true, "populationSource": "revision"}, {"case": "duplicate_json_key", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["receipt_json_invalid"], "findings": ["receipt_json_invalid"], "passed": true, "populationSource": "revision"}, {"case": "tampered_population", "decided": 0, "exit": 2, "expectedDecided": 0, "expectedExit": 2, "expectedFindings": ["population_tampered"], "findings": ["population_tampered"], "passed": true, "populationSource": null}, {"case": "baseline_without_receipts", "decided": 0, "exit": 1, "expectedDecided": 0, "expectedExit": 1, "expectedFindings": ["receipts_absent"], "findings": ["receipts_absent"], "passed": true, "populationSource": "local"}, {"case": "boilerplate_quote", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["quote_not_row_specific"], "findings": ["quote_not_row_specific"], "passed": true, "populationSource": "revision"}, {"case": "statement_correction_absent", "decided": 32, "exit": 1, "expectedDecided": 32, "expectedExit": 1, "expectedFindings": ["statement_correction_absent"], "findings": ["statement_correction_absent"], "passed": true, "populationSource": "revision"}, {"case": "statements_absent", "decided": 32, "exit": 1, "expectedDecided": 32, "expectedExit": 1, "expectedFindings": ["statements_absent"], "findings": ["statements_absent"], "passed": true, "populationSource": "revision"}], "failed": 0, "passed": 14, "schema": "kake-source-recheck-selftest-v1"}
```

#### O02

SHA-256 of actual stdout (including its final newline): `2e05776671f4168fdcab475b7406f442e3e4caa9c6f9de388d350b822675b374`.

```json
{"cases": [{"case": "complete_clean", "decided": 32, "exit": 0, "expectedDecided": 32, "expectedExit": 0, "expectedFindings": [], "findings": [], "passed": true, "populationSource": "revision"}, {"case": "missing_receipt", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["receipt_missing"], "findings": ["receipt_missing"], "passed": true, "populationSource": "revision"}, {"case": "bad_sha", "decided": 31, "exit": 2, "expectedDecided": 31, "expectedExit": 2, "expectedFindings": ["fetch_sha_mismatch"], "findings": ["fetch_sha_mismatch"], "passed": true, "populationSource": "revision"}, {"case": "quote_not_in_text", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["quote_not_in_text"], "findings": ["quote_not_in_text"], "passed": true, "populationSource": "revision"}, {"case": "short_quote", "decided": 32, "exit": 0, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["quote_word_count"], "findings": [], "passed": false, "populationSource": "revision"}, {"case": "stale_without_correction", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["correction_missing"], "findings": ["correction_missing"], "passed": true, "populationSource": "revision"}, {"case": "stale_marker_absent", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["stale_marker_absent", "statement_correction_absent"], "findings": ["stale_marker_absent", "statement_correction_absent"], "passed": true, "populationSource": "revision"}, {"case": "unverifiable_undecided", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["row_unverifiable"], "findings": ["row_unverifiable"], "passed": true, "populationSource": "revision"}, {"case": "duplicate_json_key", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["receipt_json_invalid"], "findings": ["receipt_json_invalid"], "passed": true, "populationSource": "revision"}, {"case": "tampered_population", "decided": 0, "exit": 2, "expectedDecided": 0, "expectedExit": 2, "expectedFindings": ["population_tampered"], "findings": ["population_tampered"], "passed": true, "populationSource": null}, {"case": "baseline_without_receipts", "decided": 0, "exit": 1, "expectedDecided": 0, "expectedExit": 1, "expectedFindings": ["receipts_absent"], "findings": ["receipts_absent"], "passed": true, "populationSource": "local"}, {"case": "boilerplate_quote", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["quote_not_row_specific"], "findings": ["quote_not_row_specific"], "passed": true, "populationSource": "revision"}, {"case": "statement_correction_absent", "decided": 32, "exit": 1, "expectedDecided": 32, "expectedExit": 1, "expectedFindings": ["statement_correction_absent"], "findings": ["statement_correction_absent"], "passed": true, "populationSource": "revision"}, {"case": "statements_absent", "decided": 32, "exit": 1, "expectedDecided": 32, "expectedExit": 1, "expectedFindings": ["statements_absent"], "findings": ["statements_absent"], "passed": true, "populationSource": "revision"}], "failed": 1, "passed": 13, "schema": "kake-source-recheck-selftest-v1"}
```

#### O03

SHA-256 of actual stdout (including its final newline): `7b478ee2c228932f58f2dcb44179eead77c03a89174823ee023f3c1d9b56e401`.

```json
{"cases": [{"case": "complete_clean", "decided": 32, "exit": 0, "expectedDecided": 32, "expectedExit": 0, "expectedFindings": [], "findings": [], "passed": true, "populationSource": "revision"}, {"case": "missing_receipt", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["receipt_missing"], "findings": ["receipt_missing"], "passed": true, "populationSource": "revision"}, {"case": "bad_sha", "decided": 31, "exit": 2, "expectedDecided": 31, "expectedExit": 2, "expectedFindings": ["fetch_sha_mismatch"], "findings": ["fetch_sha_mismatch"], "passed": true, "populationSource": "revision"}, {"case": "quote_not_in_text", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["quote_not_in_text"], "findings": ["quote_not_in_text"], "passed": true, "populationSource": "revision"}, {"case": "short_quote", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["quote_word_count"], "findings": ["quote_word_count"], "passed": true, "populationSource": "revision"}, {"case": "stale_without_correction", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["correction_missing"], "findings": ["correction_missing"], "passed": true, "populationSource": "revision"}, {"case": "stale_marker_absent", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["stale_marker_absent", "statement_correction_absent"], "findings": ["stale_marker_absent", "statement_correction_absent"], "passed": true, "populationSource": "revision"}, {"case": "unverifiable_undecided", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["row_unverifiable"], "findings": ["row_unverifiable"], "passed": true, "populationSource": "revision"}, {"case": "duplicate_json_key", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["receipt_json_invalid"], "findings": ["receipt_json_invalid"], "passed": true, "populationSource": "revision"}, {"case": "tampered_population", "decided": 0, "exit": 2, "expectedDecided": 0, "expectedExit": 2, "expectedFindings": ["population_tampered"], "findings": ["population_tampered"], "passed": true, "populationSource": null}, {"case": "baseline_without_receipts", "decided": 0, "exit": 1, "expectedDecided": 0, "expectedExit": 1, "expectedFindings": ["receipts_absent"], "findings": ["receipts_absent"], "passed": true, "populationSource": "local"}, {"case": "boilerplate_quote", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["quote_not_row_specific"], "findings": ["quote_not_row_specific"], "passed": true, "populationSource": "revision"}, {"case": "statement_correction_absent", "decided": 32, "exit": 0, "expectedDecided": 32, "expectedExit": 1, "expectedFindings": ["statement_correction_absent"], "findings": [], "passed": false, "populationSource": "revision"}, {"case": "statements_absent", "decided": 32, "exit": 1, "expectedDecided": 32, "expectedExit": 1, "expectedFindings": ["statements_absent"], "findings": ["statements_absent"], "passed": true, "populationSource": "revision"}], "failed": 1, "passed": 13, "schema": "kake-source-recheck-selftest-v1"}
```

#### O04

SHA-256 of actual stdout (including its final newline): `d962f6435482cbe92b1597bb476be1253e63a7dc0f1a8025e0dfd38c09df6f6d`.

```json
{"cases": [{"case": "complete_clean", "decided": 32, "exit": 0, "expectedDecided": 32, "expectedExit": 0, "expectedFindings": [], "findings": [], "passed": true, "populationSource": "revision"}, {"case": "missing_receipt", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["receipt_missing"], "findings": ["receipt_missing"], "passed": true, "populationSource": "revision"}, {"case": "bad_sha", "decided": 31, "exit": 2, "expectedDecided": 31, "expectedExit": 2, "expectedFindings": ["fetch_sha_mismatch"], "findings": ["fetch_sha_mismatch"], "passed": true, "populationSource": "revision"}, {"case": "quote_not_in_text", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["quote_not_in_text"], "findings": ["quote_not_in_text"], "passed": true, "populationSource": "revision"}, {"case": "short_quote", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["quote_word_count"], "findings": ["quote_word_count"], "passed": true, "populationSource": "revision"}, {"case": "stale_without_correction", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["correction_missing"], "findings": ["correction_missing"], "passed": true, "populationSource": "revision"}, {"case": "stale_marker_absent", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["stale_marker_absent", "statement_correction_absent"], "findings": ["stale_marker_absent", "statement_correction_absent"], "passed": true, "populationSource": "revision"}, {"case": "unverifiable_undecided", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["row_unverifiable"], "findings": ["row_unverifiable"], "passed": true, "populationSource": "revision"}, {"case": "duplicate_json_key", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["receipt_json_invalid"], "findings": ["receipt_json_invalid"], "passed": true, "populationSource": "revision"}, {"case": "tampered_population", "decided": 32, "exit": 0, "expectedDecided": 0, "expectedExit": 2, "expectedFindings": ["population_tampered"], "findings": [], "passed": false, "populationSource": "revision"}, {"case": "baseline_without_receipts", "decided": 0, "exit": 1, "expectedDecided": 0, "expectedExit": 1, "expectedFindings": ["receipts_absent"], "findings": ["receipts_absent"], "passed": true, "populationSource": "local"}, {"case": "boilerplate_quote", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["quote_not_row_specific"], "findings": ["quote_not_row_specific"], "passed": true, "populationSource": "revision"}, {"case": "statement_correction_absent", "decided": 32, "exit": 1, "expectedDecided": 32, "expectedExit": 1, "expectedFindings": ["statement_correction_absent"], "findings": ["statement_correction_absent"], "passed": true, "populationSource": "revision"}, {"case": "statements_absent", "decided": 32, "exit": 1, "expectedDecided": 32, "expectedExit": 1, "expectedFindings": ["statements_absent"], "findings": ["statements_absent"], "passed": true, "populationSource": "revision"}], "failed": 1, "passed": 13, "schema": "kake-source-recheck-selftest-v1"}
```

#### O05

SHA-256 of actual stdout (including its final newline): `992179de09bd2ee1cb61e336be71a2f7ab7e343eb3cbf19fc871c837aa3d1089`.

```json
{"cases": [{"case": "complete_clean", "decided": 32, "exit": 0, "expectedDecided": 32, "expectedExit": 0, "expectedFindings": [], "findings": [], "passed": true, "populationSource": "revision"}, {"case": "missing_receipt", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["receipt_missing"], "findings": ["receipt_missing"], "passed": true, "populationSource": "revision"}, {"case": "bad_sha", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 2, "expectedFindings": ["fetch_sha_mismatch"], "findings": ["quote_not_in_text"], "passed": false, "populationSource": "revision"}, {"case": "quote_not_in_text", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["quote_not_in_text"], "findings": ["quote_not_in_text"], "passed": true, "populationSource": "revision"}, {"case": "short_quote", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["quote_word_count"], "findings": ["quote_word_count"], "passed": true, "populationSource": "revision"}, {"case": "stale_without_correction", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["correction_missing"], "findings": ["correction_missing"], "passed": true, "populationSource": "revision"}, {"case": "stale_marker_absent", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["stale_marker_absent", "statement_correction_absent"], "findings": ["stale_marker_absent", "statement_correction_absent"], "passed": true, "populationSource": "revision"}, {"case": "unverifiable_undecided", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["row_unverifiable"], "findings": ["row_unverifiable"], "passed": true, "populationSource": "revision"}, {"case": "duplicate_json_key", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["receipt_json_invalid"], "findings": ["receipt_json_invalid"], "passed": true, "populationSource": "revision"}, {"case": "tampered_population", "decided": 0, "exit": 2, "expectedDecided": 0, "expectedExit": 2, "expectedFindings": ["population_tampered"], "findings": ["population_tampered"], "passed": true, "populationSource": null}, {"case": "baseline_without_receipts", "decided": 0, "exit": 1, "expectedDecided": 0, "expectedExit": 1, "expectedFindings": ["receipts_absent"], "findings": ["receipts_absent"], "passed": true, "populationSource": "local"}, {"case": "boilerplate_quote", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["quote_not_row_specific"], "findings": ["quote_not_row_specific"], "passed": true, "populationSource": "revision"}, {"case": "statement_correction_absent", "decided": 32, "exit": 1, "expectedDecided": 32, "expectedExit": 1, "expectedFindings": ["statement_correction_absent"], "findings": ["statement_correction_absent"], "passed": true, "populationSource": "revision"}, {"case": "statements_absent", "decided": 32, "exit": 1, "expectedDecided": 32, "expectedExit": 1, "expectedFindings": ["statements_absent"], "findings": ["statements_absent"], "passed": true, "populationSource": "revision"}], "failed": 1, "passed": 13, "schema": "kake-source-recheck-selftest-v1"}
```

#### O06

SHA-256 of actual stdout (including its final newline): `da266b4254a47b078c98b6898f846c817a3eb81ee8a8aaf58806af8bd0f1bc9e`.

```json
{"cases": [{"case": "complete_clean", "decided": 31, "exit": 2, "expectedDecided": 32, "expectedExit": 0, "expectedFindings": [], "findings": ["manifest_entry_invalid"], "passed": false, "populationSource": "revision"}, {"case": "missing_receipt", "decided": 30, "exit": 2, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["receipt_missing"], "findings": ["manifest_entry_invalid", "receipt_missing"], "passed": false, "populationSource": "revision"}, {"case": "bad_sha", "decided": 30, "exit": 2, "expectedDecided": 31, "expectedExit": 2, "expectedFindings": ["fetch_sha_mismatch"], "findings": ["fetch_sha_mismatch", "manifest_entry_invalid"], "passed": false, "populationSource": "revision"}, {"case": "quote_not_in_text", "decided": 30, "exit": 2, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["quote_not_in_text"], "findings": ["manifest_entry_invalid", "quote_not_in_text"], "passed": false, "populationSource": "revision"}, {"case": "short_quote", "decided": 30, "exit": 2, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["quote_word_count"], "findings": ["manifest_entry_invalid", "quote_word_count"], "passed": false, "populationSource": "revision"}, {"case": "stale_without_correction", "decided": 30, "exit": 2, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["correction_missing"], "findings": ["correction_missing", "manifest_entry_invalid"], "passed": false, "populationSource": "revision"}, {"case": "stale_marker_absent", "decided": 30, "exit": 2, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["stale_marker_absent", "statement_correction_absent"], "findings": ["manifest_entry_invalid", "stale_marker_absent", "statement_correction_absent"], "passed": false, "populationSource": "revision"}, {"case": "unverifiable_undecided", "decided": 30, "exit": 2, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["row_unverifiable"], "findings": ["manifest_entry_invalid", "row_unverifiable"], "passed": false, "populationSource": "revision"}, {"case": "duplicate_json_key", "decided": 30, "exit": 2, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["receipt_json_invalid"], "findings": ["manifest_entry_invalid", "receipt_json_invalid"], "passed": false, "populationSource": "revision"}, {"case": "tampered_population", "decided": 0, "exit": 2, "expectedDecided": 0, "expectedExit": 2, "expectedFindings": ["population_tampered"], "findings": ["population_tampered"], "passed": true, "populationSource": null}, {"case": "baseline_without_receipts", "decided": 0, "exit": 1, "expectedDecided": 0, "expectedExit": 1, "expectedFindings": ["receipts_absent"], "findings": ["receipts_absent"], "passed": true, "populationSource": "local"}, {"case": "boilerplate_quote", "decided": 30, "exit": 2, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["quote_not_row_specific"], "findings": ["manifest_entry_invalid", "quote_not_row_specific"], "passed": false, "populationSource": "revision"}, {"case": "statement_correction_absent", "decided": 31, "exit": 2, "expectedDecided": 32, "expectedExit": 1, "expectedFindings": ["statement_correction_absent"], "findings": ["manifest_entry_invalid", "statement_correction_absent"], "passed": false, "populationSource": "revision"}, {"case": "statements_absent", "decided": 31, "exit": 2, "expectedDecided": 32, "expectedExit": 1, "expectedFindings": ["statements_absent"], "findings": ["manifest_entry_invalid", "statements_absent"], "passed": false, "populationSource": "revision"}], "failed": 12, "passed": 2, "schema": "kake-source-recheck-selftest-v1"}
```

#### O07

SHA-256 of actual stdout (including its final newline): `bbd6b37737085ae6543a9df7ae8b8d5f3e75d0f2f0c0af99fd3ea31e5df32e9c`.

```json
{"cases": [{"case": "complete_clean", "decided": 32, "exit": 0, "expectedDecided": 32, "expectedExit": 0, "expectedFindings": [], "findings": [], "passed": true, "populationSource": "revision"}, {"case": "missing_receipt", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["receipt_missing"], "findings": ["receipt_missing"], "passed": true, "populationSource": "revision"}, {"case": "bad_sha", "decided": 31, "exit": 2, "expectedDecided": 31, "expectedExit": 2, "expectedFindings": ["fetch_sha_mismatch"], "findings": ["fetch_sha_mismatch"], "passed": true, "populationSource": "revision"}, {"case": "quote_not_in_text", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["quote_not_in_text"], "findings": ["quote_not_in_text"], "passed": true, "populationSource": "revision"}, {"case": "short_quote", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["quote_word_count"], "findings": ["quote_word_count"], "passed": true, "populationSource": "revision"}, {"case": "stale_without_correction", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["correction_missing"], "findings": ["correction_missing"], "passed": true, "populationSource": "revision"}, {"case": "stale_marker_absent", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["stale_marker_absent", "statement_correction_absent"], "findings": ["stale_marker_absent", "statement_correction_absent"], "passed": true, "populationSource": "revision"}, {"case": "unverifiable_undecided", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["row_unverifiable"], "findings": ["row_unverifiable"], "passed": true, "populationSource": "revision"}, {"case": "duplicate_json_key", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["receipt_json_invalid"], "findings": ["receipt_json_invalid"], "passed": true, "populationSource": "revision"}, {"case": "tampered_population", "decided": 0, "exit": 2, "expectedDecided": 0, "expectedExit": 2, "expectedFindings": ["population_tampered"], "findings": ["population_tampered"], "passed": true, "populationSource": null}, {"case": "baseline_without_receipts", "decided": 0, "exit": 1, "expectedDecided": 0, "expectedExit": 1, "expectedFindings": ["receipts_absent"], "findings": ["receipts_absent"], "passed": true, "populationSource": "local"}, {"case": "boilerplate_quote", "decided": 31, "exit": 1, "expectedDecided": 31, "expectedExit": 1, "expectedFindings": ["quote_not_row_specific"], "findings": ["quote_not_row_specific"], "passed": true, "populationSource": "revision"}, {"case": "statement_correction_absent", "decided": 32, "exit": 0, "expectedDecided": 32, "expectedExit": 1, "expectedFindings": ["statement_correction_absent"], "findings": ["statement_correction_absent"], "passed": false, "populationSource": "revision"}, {"case": "statements_absent", "decided": 32, "exit": 0, "expectedDecided": 32, "expectedExit": 1, "expectedFindings": ["statements_absent"], "findings": ["statements_absent"], "passed": false, "populationSource": "revision"}], "failed": 2, "passed": 12, "schema": "kake-source-recheck-selftest-v1"}
```

## In-memory adapter reproduction

The following is the exact `sitecustomize.py` source stored in the anonymous adapter ZIP. The ZIP contained this one member (`ZIP_STORED`, timestamp `2026-10-21 00:00:00`). It makes fixture I/O virtual before the unmodified/mutated counter imports `Path`. Filesystem mutation/open-write/process-launch audit failures are not suppressed. No target check or selftest expectation is replaced.

```python
import os, sys

def no_disk_or_process_side_effects(event, args):
    blocked = {'os.mkdir', 'os.remove', 'os.rmdir', 'os.rename', 'os.link', 'os.symlink',
               'os.truncate', 'os.chmod', 'os.chown', 'os.utime', 'subprocess.Popen',
               'os.system', 'os.exec', 'os.posix_spawn'}
    if event in blocked:
        raise RuntimeError('memory-only mutation probe blocked ' + event)
    if event == 'open':
        mode, flags = args[1], args[2]
        if isinstance(mode, str) and any(c in mode for c in 'wax+'):
            raise RuntimeError('memory-only mutation probe blocked writable open')
        if isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND):
            raise RuntimeError('memory-only mutation probe blocked writable open flags')
sys.addaudithook(no_disk_or_process_side_effects)

import pathlib, tempfile, subprocess, hashlib, itertools
_LOCAL = {}
_DIRS = set()
_REPOS = {}
_SERIAL = itertools.count(1)

class MemoryPath(pathlib.PurePosixPath):
    def resolve(self, strict=False):
        return self
    def mkdir(self, mode=0o777, parents=False, exist_ok=False):
        key = str(self)
        if key in _DIRS and not exist_ok:
            raise FileExistsError(key)
        if parents:
            _DIRS.update(str(p) for p in self.parents)
        _DIRS.add(key)
    def is_dir(self):
        return str(self) in _DIRS
    def write_bytes(self, data):
        if str(self.parent) not in _DIRS:
            raise FileNotFoundError(str(self.parent))
        _LOCAL[str(self)] = bytes(data)
        return len(data)
    def read_bytes(self):
        try:
            return _LOCAL[str(self)]
        except KeyError:
            raise FileNotFoundError(str(self)) from None

class MemoryTemporaryDirectory:
    def __init__(self, suffix=None, prefix=None, dir=None, **kwargs):
        self.name = str(MemoryPath(str(dir)) / ((prefix or '') + 'memory-' + str(next(_SERIAL)) + (suffix or '')))
        MemoryPath(self.name).mkdir(parents=True)
    def __enter__(self):
        return self.name
    def __exit__(self, *args):
        self.cleanup()
    def cleanup(self):
        for table in (_LOCAL, _REPOS):
            for key in list(table):
                if key == self.name or key.startswith(self.name + '/'):
                    del table[key]
        for key in list(_DIRS):
            if key == self.name or key.startswith(self.name + '/'):
                _DIRS.remove(key)

def memory_git_run(command, *, cwd=None, **kwargs):
    args = list(command)
    if args.pop(0) != 'git':
        raise RuntimeError('memory-only probe allows fixture Git protocol only')
    while args and args[0].startswith('-'):
        flag = args.pop(0)
        if flag == '-c':
            args.pop(0)
        elif flag not in ('--no-replace-objects', '--literal-pathspecs'):
            raise RuntimeError('unsupported Git global option ' + flag)
    verb, *rest = args
    root = str(cwd)
    def done(stdout=b'', code=0, stderr=b''):
        return subprocess.CompletedProcess(command, code, stdout, stderr)
    if verb == 'init':
        _REPOS[root] = {'commits': {}, 'head': None}
        return done()
    repo = _REPOS.get(root)
    if repo is None:
        return done(code=128, stderr=b'not a memory repository')
    if verb == 'add':
        return done()
    if verb == 'commit':
        files = {key[len(root) + 1:]: data for key, data in _LOCAL.items() if key.startswith(root + '/')}
        digest = hashlib.sha1()
        for key, data in sorted(files.items()):
            digest.update(key.encode() + b'\0' + data + b'\0')
        revision = digest.hexdigest()
        repo['commits'][revision] = files
        repo['head'] = revision
        return done()
    if verb == 'rev-parse':
        if rest == ['--show-toplevel']:
            return done((root + '\n').encode())
        if rest == ['--show-prefix']:
            return done(b'\n')
        selector = rest[-1].removesuffix('^{commit}')
        revision = repo['head'] if selector == 'HEAD' else selector
        return done((revision + '\n').encode()) if revision in repo['commits'] else done(code=128)
    if verb == 'ls-tree':
        dash = rest.index('--')
        revision = next(arg for arg in rest[:dash] if not arg.startswith('-'))
        files = repo['commits'].get(revision)
        if files is None:
            return done(code=128)
        path = rest[dash + 1]
        if path in files:
            entries = [(path, 'blob')]
        else:
            prefix = path.rstrip('/') + '/'
            if '-r' in rest[:dash]:
                entries = [(key, 'blob') for key in files if key.startswith(prefix)]
            else:
                children = {}
                for key in files:
                    if key.startswith(prefix):
                        tail = key[len(prefix):]
                        name, slash, _ = tail.partition('/')
                        children[prefix + name] = 'tree' if slash else 'blob'
                entries = list(children.items())
        data = b''.join((('100644' if kind == 'blob' else '040000') + ' ' + kind + ' ' + '0' * 40 + '\t' + name).encode() + b'\0'
                        for name, kind in sorted(entries))
        return done(data)
    if verb == 'cat-file' and rest[0] == 'blob':
        revision, _, path = rest[1].partition(':')
        files = repo['commits'].get(revision, {})
        return done(files[path]) if path in files else done(code=128)
    raise RuntimeError('unsupported fixture Git command ' + verb)

pathlib.Path = MemoryPath
tempfile.TemporaryDirectory = MemoryTemporaryDirectory
subprocess.run = memory_git_run
```

The parent delivery function used the following command/FD/environment setup (each subject is the exact source bytes hashed above):

```python
code_fd = os.memfd_create("round26-measure.py", flags=0)
zip_fd = os.memfd_create("round26-memory-io.zip", flags=0)
try:
    os.write(code_fd, subject_bytes)
    os.write(zip_fd, adapter_zip_bytes)
    os.lseek(code_fd, 0, os.SEEK_SET)
    os.lseek(zip_fd, 0, os.SEEK_SET)
    command = ["python3", "-B", f"/proc/self/fd/{code_fd}", "--selftest"]
    child_env = os.environ.copy()
    child_env["PYTHONPATH"] = f"/proc/self/fd/{zip_fd}"
    child_env["PYTHONDONTWRITEBYTECODE"] = "1"
    child_env["PYTHONHASHSEED"] = "0"
    proc = subprocess.run(command, pass_fds=(code_fd, zip_fd), env=child_env,
                          cwd="/home/vgpnk/Projects/shokunin/kake-shokunin",
                          capture_output=True, timeout=60, check=False)
finally:
    os.close(code_fd)
    os.close(zip_fd)
```

No production fix was applied; the assigned mutation probe is complete.

```json
{"target":".ufo/waves/round-26/measure.py --selftest","verdict":"DISAGREE","severity":"medium"}
```
