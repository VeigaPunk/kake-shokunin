# RecheckCounter: r26-recheck-build (C1 freshness)

Lane: KakeR25.RecheckCounter-6. Axes: freshness, operability. Milestone: r26-recheck-build.

Deliverable: `.ufo/waves/round-26/sandbox-counter/measure.py` (one file, standard library only).
Status: written, **not executed**. The item says "Do not run it", so neither the CLI nor `--selftest` was run. No build, test, lint or smoke run was performed.

## Identity
- Population pin `POPULATION_SHA256`: `16330e1effd5ee52665f8f31738e9423c6ec387e5d4a1404c5bcc35f69d01b03`
  (sha256 of `.ufo/waves/round-26/population.json` as read at drafting time). Any later edit to the population makes the run exit 2.
- Schema `kake-source-recheck-v1`, `expected` 32.
- Run: `python3 -B .ufo/waves/round-26/sandbox-counter/measure.py --root . --revision <40- or 64-hex commit>`
- Self-check: `python3 -B .ufo/waves/round-26/sandbox-counter/measure.py --selftest`

## Exit codes
- 0: decided == 32 and no findings.
- 1: rows undecided, or a non-fatal finding present.
- 2: input unavailable or tampered (any fatal id below).
- 64: usage. `--revision` must be a full 40- or 64-digit hex name. `--selftest` takes no root or revision.

## Finding ids
Fatal, exit 2: root_unavailable, revision_unavailable, git_unavailable, population_unavailable, population_tampered, population_invalid, manifest_unavailable, manifest_invalid, source_text_unavailable, manifest_entry_missing, manifest_entry_invalid, manifest_population_mismatch, fetch_bytes_unavailable, fetch_bytes_invalid, fetch_sha_mismatch.

Non-fatal, exit 1: receipts_absent, receipt_missing, receipt_unexpected, receipt_json_invalid, receipt_schema, receipt_id_mismatch, verdict_invalid, reason_missing, anchor_missing, quote_missing, fetch_index_invalid, quote_word_count, quote_not_in_text, correction_missing, correction_unexpected, stale_marker_absent, row_unverifiable.

Usage, exit 64: usage.

## Selftest fixtures (expected exit, finding ids, decided)
- complete_clean: 0, none, 32. Also covers retry supersession: S008's base TimeoutError entry is superseded by the retry entry.
- missing_receipt: 1, receipt_missing, 31.
- bad_sha: 2, fetch_sha_mismatch, 31.
- quote_not_in_text: 1, quote_not_in_text, 31.
- short_quote: 1, quote_word_count, 31.
- stale_without_correction: 1, correction_missing, 31.
- stale_marker_absent: 1, stale_marker_absent, 31.
- unverifiable_undecided: 1, row_unverifiable, 31.
- duplicate_json_key: 1, receipt_json_invalid, 31.
- tampered_population: 2, population_tampered, 0.
- baseline_without_receipts: 1, receipts_absent, 0, with the population taken from the exact local file.

Each case must match its exit, its finding-id set exactly, and its decided count. The fixture population is synthetic, so the selftest passes its own sha as the pin. The CLI always uses the constant above.

## How it reads
- Every input is a committed blob at REV, read with `git ls-tree` then `git cat-file blob REV:path`. Every git call runs with inherited `GIT_*` variables stripped, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `--no-replace-objects`, `--literal-pathspecs` and `core.hooksPath=/dev/null`.
  `cat-file blob` stands in for `git show REV:path` so that no textconv or filter can alter the bytes.
- Repository-relative paths use the `--show-prefix` of ROOT. kake-shokunin is its own git top level, so the prefix is empty (checked read-only).
- Effective fetch: the retry entry if one exists for the same row and index, otherwise the base entry. Its sha256 must equal the population sha256, and the gunzipped bytes must hash to that value.
- Quote: `normalize(text_of(raw, content_type))` from `.ufo/waves/round-26/source_text.py` at REV, executed in memory. `content_type` is the effective manifest `headers["content-type"]`, the same argument `sandbox-tests/text_selftest.py:137` passes.
- Word boundary: `(?<!\w)` and `(?!\w)` around the normalized quote, case-sensitive. Quote length is 6 to 25 whitespace words.
- Population: taken from REV when present. Otherwise the local file under ROOT is used, and only if its sha matches the pin.

## Decisions beyond the item text (please review)
1. Stricter than the item. Receipts must carry exactly the seven contract keys (receipt_schema). `reason` is required for every verdict. `anchorObserved` must be nonempty for HOLD and STALE. `correction` must be null for HOLD and UNVERIFIABLE (contract: "null or ... STALE only"). A non-null quote is word-checked even on UNVERIFIABLE.
2. Raw, manifest or population sha disagreement is treated as tampered input (exit 2), not as a row verdict, because the population pins those values.
3. Zero receipts gives receipts_absent (global). Some receipts missing gives receipt_missing per row. Any other entry under rechecks/ gives receipt_unexpected (exit 1).
4. A missing manifest-retry.json is read as "no retries". A missing manifest.json while receipts exist is exit 2.
5. Every UNVERIFIABLE row also emits row_unverifiable, so every undecided row is named.
6. Selftest scratch repos are created under `sandbox-counter/` as `.recheck-selftest-*` and removed on exit. Nothing is written to /tmp, per the round-25 disclosure at `LessonScribe.md:84`.

## Facts for L1 (not changed by me)
1. `.ufo/waves/round-26/contract.json` `claim.count` names `python3 -B .ufo/waves/round-26/measure.py --root . --revision <commit>`. This item places the file at `sandbox-counter/measure.py`. L1 must move or copy the file, or amend the contract. `ClaimCritic.md` item 9 flagged the same mismatch.
2. `population.json`, `fetched/`, `source_text.py` and `rechecks/` are not in HEAD. `git ls-tree HEAD -- .ufo/waves/round-26/population.json` returned nothing. A revision-bound run needs the inputs and the 32 receipts committed first. The baseline 97404de has none of them, so its expected result is decided 0, receipts_absent, exit 1.
3. Population: 32 rows, namely S001 to S013, S015 to S018 and S020 to S034. S014 and S019 are excluded, and S035 is absent. S001 and S002 each have two fetches. S008 index 1 pins `fetched/S008-1-retry.raw.gz` with sha256 `93281a63…`. Its base entry is a TimeoutError with an empty body and is superseded.
4. Expected full-run shape, not measured: decided = HOLD + STALE over the 32 rows.

## Verification
- None performed, per the item.
- Recommended gate for L1, in order: `--selftest` (expect exit 0 and 11 passing cases). Then, after committing the round-26 inputs and receipts, `--root . --revision <commit>`.

## Tooling
- No tool installed or updated. Read-only host observations: git 2.56.0 and Python 3.14.8.
- No pacman, uv or npm activity.

## Boundary note
- A repo-wide grep over `.ufo/waves` returned incidental snippets from `round-24/measure_c2.py` (lines 39–41), `round-26/w1/PacketCounter-draft.py` and `round-26/w2/ReviewCounter.md`. I did not open any round-24 file. I did not use those snippets as a source.
