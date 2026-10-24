# Round 27 W2 — ReviewInputSafety

Axes: **operability** (judged), **freshness**. Target: frozen candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`.

## Scope and source binding

Static review plus real fixture/privacy selftests and harmless local scratch boundary cases. No network request was made, no actual URL or fetched body was opened, no raw form/session/header state was retained or printed, and no production source was edited. No `resume_continuity_v1` occurrence exists in the five assigned sources.

Before source reads, each working file matched the Git blob at the explicit candidate hash. Working SHA-256 / candidate Git blob: `scripts/citing_set.py` `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228` / `352a471abec08daa56a0fb7ef23fe78f2930d773`; `scripts/citing_set_selftest.py` `3c167895c7f3a4acf531886816bffcbf189d299d6137ca12096265855dd62a1c` / `c69b09b2e47f4115aa4e8ff286aa7cfe0e171a64`; `count_c1.py` `8d4c22efa884468daead75aa4b9d6143d38986a83c3069747d146ee0daf942a5` / `e1ebd5767cf152b3b01b4d041be0ac3c2dbea25d`; `c2_count.py` `913a797fdfcbd25d328c2291a14cb84620f4ebfe348d6fd1016415674b8ca055` / `bca4e649187f54128f06c294c8f7a6d256f9f817`; `fetch_group.py` `538c616faea2d05b1e1fde2978970b16ecf12921d82ab66398d6715b35c2a54c` / `1c4b8672790072999fa934b19d854a392f8769ba`.
Git boundary: normal `citing_set.py` uses argv-based `rev-parse` to canonicalize the revision before `show`/`ls-tree`; inspected gate commands are reads, not Git mutations. C1/C2 also use argv arrays (no shell), but interpolate caller `--revision` directly into Git object/log arguments (`count_c1.py:11,20,26,39`; `c2_count.py:10`) without first resolving an OID or `--end-of-options`. Treat those as trusted measurement inputs, not general arbitrary-revision readers; canonicalize as the gate does. No malicious revision was run.

The exact candidate also binds `round-26/source_text.py` (SHA-256 `55ae7abc52a5acfd95a86d96c27f12898c30e33ab63cfa7f383640120f57b7d6`) and `fetch_sources.py` (`de43a2a814cfb8a85348a2641d0d91ef7b3756a1319b247ba5b85218288c7820`), which were read as fetch_group dependencies.

## Findings

### 1. High, conditional — fetch and retained metadata do not enforce public destinations

**Exploit path:** a selected S001–S006 source row can supply any `http(s)` URL; `urllib` follows HTTP redirects without a public-host/destination check. Running the ordinary fetch mode can therefore request a private/loopback destination or retain a response not actually public. URLs (including userinfo/query text) and final URLs are copied verbatim into the manifest; exception text is also recorded. Code/config URL suffixes keep received bytes verbatim; other responses retain visible/normalized text, which is not a publicness or sensitivity test.

**Evidence:** `round-26/fetch_sources.py:24-42` extracts any `http(s)` URL and calls `urlopen`; `fetch_group.py:193-210,164-183` filters only by row ID, fetches, and stores `url`, `finalUrl`, `error`, status/time and digests. `count_c1.py:72-92` checks committed manifest history, recorded HTTP status/time and retained-byte hashes, not HTTP provenance or publicness. No actual URL was inspected, so this does not assert that a current row is private.

**Impact:** the documented public-only scope is a caller/source-list convention, not enforced by the fetch path; private response content or secret-bearing URL text could be persisted. `receivedSha256` for filtered HTML is an observation only, not a recoverable/authenticated raw response.

**Smallest remediation:** allowlist permitted public hosts and revalidate each redirect destination (reject private/loopback/link-local addresses); redact URL userinfo/sensitive query values and exception strings before manifest/log output. Treat manifest status/date/digests as self-reported unless backed by separate transport evidence.

### 2. High — sanitize-existing can write/delete outside the requested root via symlinked ancestors

**Exploit path:** point `root/.ufo/waves/round-27/fetched` (or an ancestor) at another writable directory containing a plausible manifest and run `--sanitize-existing`. `manifest_path.is_file()` follows the link. `_safe_child()` compares the child parent to `directory.resolve()`—the same outside target—so it does not establish containment beneath `root`. The migration then writes retained files/sidecars/manifest and unlinks listed old names there. Normal fetch mode also writes through `out` without validating its ancestors.

**Evidence:** `fetch_group.py:247-269,294-324`, especially `_safe_child:233-244`; normal writes at `187-213`. The stated round-27-only boundary at module lines 16-21 is not enforced against these directory links. No such path was exercised.

**Impact:** offline mode can modify or delete files outside the selected project even though it makes no network request.

**Smallest remediation:** reject symlinks/non-directories at every root-relative ancestor and establish containment under a canonical root before all reads, writes and deletes; use directory-fd/no-follow operations to avoid check/open races.

### 3. High, conditional — sanitizer trusts a self-asserted “already filtered” marker

**Exploit path:** provide a gzip payload containing raw HTML and a manifest entry whose `sha256` matches those raw bytes, whose `retainedRepresentation` is any object (even `{}`), and whose received digest/byte fields exist. At `fetch_group.py:274-283`, matching `sha256` plus a dict marker selects the already-filtered branch and retains the payload without calling `classify`; it then writes that payload as the retained representation.

**Impact:** stale, malformed or edited manifest metadata can make `--sanitize-existing` preserve exactly the hidden inputs, attributes or script bodies that the migration claims to remove. Current privacy selftest exercises a raw entry without this marker and the generated idempotent entry, not a forged marker.

**Smallest remediation:** always reclassify input payload bytes before retention (or verify an authenticated prior-retention record); do not let a caller-controlled dict plus matching caller-controlled digest establish that filtering occurred.

### 4. Medium — population/ledger nonregular inputs can hang; corpus checks are stronger

**Evidence:** `WorkingTreeSource.read_document()` uses realpath containment then plain `open()` and catches only `OSError` (`citing_set.py:184-215`); unlike `corpus_files()`/`_walk()` (`217-259`), it does not `lstat`, reject symlinks, or require a regular file. An outside-root input symlink is rejected; an in-root symlink is followed. A FIFO population/ledger path blocks indefinitely waiting for a writer. Corpus symlink and special-file entries fail closed.

**Impact:** a malformed local population/ledger path can hang the gate; concurrent replacement between realpath and open also leaves a TOCTOU boundary. This is not an outside-root escape in the observed symlink case.

**Smallest remediation:** `lstat` and require regular non-symlink population/ledger files, then open relative to a root directory fd with no-follow and `fstat` the opened descriptor.

### 5. High if inputs are not trusted — helper/test paths are executable, not data-only

**Exploit path/evidence:** `fetch_group.py:64-77` imports `source_text.py` and, for fetching, `fetch_sources.py` from caller-supplied `--root` using `spec.loader.exec_module`; `.is_file()` follows symlinks and there is no content hash check. Thus even `--sanitize-existing` executes code from the selected root before sanitizing. Separately, `citing_set_selftest.py:214-235` runs the caller-selected `--gate` as Python without a sandbox; `c2_count.py:24-29` extracts the gate from the selected revision and executes it. The fixture child environment copies the caller environment (`102-117`). These are intentional code-running workflows, not the normal gate’s data-reading path. By contrast, `count_c1.py:83-92` hashes its source-text dependency before import.

**Impact:** using these workflows on an untrusted root, revision, helper or gate grants arbitrary Python execution with the caller’s filesystem/network permissions and inherited environment. Do not represent them as safe arbitrary-root readers.

**Smallest remediation:** hash-pin and reject symlinked helper code before import; restrict executable gate/revision to an independently trusted binding; otherwise run the test/counter process in an actual sandbox with a scrubbed environment and no network/secrets.

### 6. Medium — default fixture selftest can report clean below the required fixture floor

**Evidence:** `CONTRACT_MINIMUM_CASES` is 12, but `args.min_cases` defaults to 0; a short case list only adds a note and `main()` returns 0 when its remaining cases pass (`citing_set_selftest.py:49-70,351-380`). `citing_set.py --selftest` forwards no minimum by default (`586-628`).

**Impact:** deleting most/all fixture directories can still produce `verdict=clean`, so the reusable selftest does not enforce the contract’s >=12-case operability criterion unless invoked with `--min-cases 12`.

**Smallest remediation:** enforce 12 by default and make below-floor cases return failure.

### 7. Low — C2 counter scratch is outside the assigned seat boundary

`c2_count.py:17` hardcodes `TemporaryDirectory(..., dir='/fast/scratch/hyaku/kake-r27')`, ignoring `TMPDIR`; that writes outside `/fast/scratch/hyaku/kake-r27/ReviewInputSafety/`. I did not run this counter because doing so would violate the seat’s write isolation. Make its scratch root caller-selectable or honor a seat-scoped environment path.

## Executed checks (expectations declared before each run)

- **Fixture runner:** expected exit 0 only if every fixture’s exact exit and sorted finding-ID multiset matches and the 12-case floor is met. Command: `TMPDIR=/fast/scratch/hyaku/kake-r27/ReviewInputSafety/fixture-runner-f2txuvoo/tmp python3 -B scripts/citing_set_selftest.py --tmpdir /fast/scratch/hyaku/kake-r27/ReviewInputSafety/fixture-runner-f2txuvoo/tmp --min-cases 12`; actual exit 0; stdout summary `clean`, 29 cases, 0 failed, minimum met; stdout SHA-256 `fdbc51cd663bfba3f9b3d3cc284757d708727d7e40ab93913cd41de8f2808f33`; exact stdout: `/fast/scratch/hyaku/kake-r27/ReviewInputSafety/fixture-runner-f2txuvoo/stdout.json`.
- **Privacy selftest:** expected exit 0 for the 9 declared synthetic filtering/migration/idempotence cases. Command: `TMPDIR=/fast/scratch/hyaku/kake-r27/ReviewInputSafety/fetch-selftest-4_d8b_x_ KAKE_R27_SCRATCH=/fast/scratch/hyaku/kake-r27/ReviewInputSafety/fetch-selftest-4_d8b_x_ python3 -B .ufo/waves/round-27/fetch_group.py --selftest`; actual exit 0, 9/9 passed; stdout SHA-256 `4acde372567f9b7d081501b1359483442ccb3e589703ad04add7af8a7a090110`; exact stdout: `/fast/scratch/hyaku/kake-r27/ReviewInputSafety/fetch-selftest-4_d8b_x_/stdout.json`.
- **Outside-root symlink:** expected exit 2/path escape. Command: `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/citing_set.py --root /fast/scratch/hyaku/kake-r27/ReviewInputSafety/gate-boundary-norel0zm/outside-symlink --population population-link.json --ledger ledger.json --json` (cwd that root). Actual exit 2; stdout JSON `{"verdict":"could-not-evaluate","citingPairs":0,"ledgerPairs":0,"findings":[{"id":"input_invalid","reason":"path_escapes_root","scope":"document","path":"population-link.json"}]}`; raw stdout SHA-256 `a0a74288ac5f48fdc6619bc75044b3c8a3b7f96647d46f4d056f91f35aaadcef`.
- **Corpus symlink:** expected exit 2/symlink rejection. Command: `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/citing_set.py --root /fast/scratch/hyaku/kake-r27/ReviewInputSafety/gate-boundary-norel0zm/corpus-symlink --population population.json --ledger ledger.json --json` (cwd that root). Actual exit 2; stdout JSON `{"verdict":"could-not-evaluate","citingPairs":0,"ledgerPairs":0,"findings":[{"id":"input_invalid","reason":"symlink_rejected","scope":"corpus","path":"corpus/knowledge/link.md"}]}`; raw stdout SHA-256 `be681479121a1f4a5f73bfa48237cf63fc9b6ff573148d672a422e351473e8c2`.
- **Corpus FIFO:** expected exit 2/nonregular rejection. Command: `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/citing_set.py --root /fast/scratch/hyaku/kake-r27/ReviewInputSafety/gate-boundary-norel0zm/corpus-fifo --population population.json --ledger ledger.json --json` (cwd that root). Actual exit 2; stdout JSON `{"verdict":"could-not-evaluate","citingPairs":0,"ledgerPairs":0,"findings":[{"id":"input_invalid","reason":"not_a_regular_file","scope":"corpus","path":"corpus/knowledge/not-regular"}]}`; raw stdout SHA-256 `554f14e928e91e2977f947e91f1c4940a6e590dd476e896b8241d53947351dc6`.
- **Population FIFO:** expected prompt invalid-input exit 2, not a block. Command: `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/citing_set.py --root /fast/scratch/hyaku/kake-r27/ReviewInputSafety/gate-boundary-norel0zm/population-fifo --population population.json --ledger ledger.json --json` (cwd that root, 2s timeout). Actual timed out at 2s; stdout empty, raw stdout SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. All probe inputs/output were under the owned seat scratch.

## Retention receipt check

Read a safe-field projection of the current manifest only: 8 entries, all status 200; 2 `received_code_bytes` entries retain received bytes verbatim, 6 `public_visible_text` entries have distinct retained/received sizes and hashes. `retention-migration.json` records exit 0, 8 records, 8 superseded raw names removed, `observationsPreserved=true`, no network. `retention-shape-after.json` records all retained checks true and explicitly limits the claim: filtered received HTML is not retained/reconstructable. These checks establish local representation integrity/shape, not public URL authenticity or immunity to the manifest-marker bypass above.