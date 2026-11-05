# ConnectorScope — round 96 sibling-overlap scan (read-only)

Method: committed trees only. Reads were `git -C <lane> show HEAD:<path>`, `git -C <lane> grep … HEAD`, `git -C <lane> ls-tree HEAD`, and plain `grep`/`cat` over the lane's read-only views. No sibling file was written; no git mutation was run.

Sibling HEADs at scan time:
- `kumitate-shokunin`: `0bff4bab` (`0bff4babeec90dd57ea36efeaa94b66db9af381d`)
- `kotodama-shokunin`: `d41eb594` (`d41eb594d27fa71869c0c28d9c2dc051fda40079`)
- `chousa-shokunin`: `378fda82` (`378fda82dc2cbcc555a0565052cc408121813cef`)
- `tabi-shokunin`: `58d84eda` (`58d84eda992ffc11d77d76a2c1019bfe061f9241`)
- `souji-shokunin`: `8b393b19` (`8b393b1911558932eab29e74635361256afdd6e3`)
- `kake-shokunin`: freeze `049e8eca` (`049e8eca2f0fa5e981232eb4efe367357dce578c`), base `bde9869144f69c5a459c0d2c93f5135922fe3a8d`.

Instrument digests verified before reading (`sha256sum`, rc 0):
- `c96_selfassess.py` = `a282da654d5ee6af923abb2cae4bd0a4fd6e4309db81de5a67999ed7b25ad134` (match)
- `c96_reval.py` = `ec40aec19d0b4563ad21d79b398c7aaa65a99806984dbca55086c099571eebb9` (match)
- `c95_selfassess.py` = `8fd27d626883f2b6852ea2ee425706a77a72eeaee10ef740b8e0fc15ac03b193` (frozen round-95 counter, match)
All match `controls/instrument-sha256.txt` exactly.

---

## 1. Sibling Scan for RFC 9111 §4.3 / revalidation / 304 handling ground

Scan command executed across all local sibling lanes:
`git -C /home/vgpnk/Projects/shokunin/<lane>-shokunin grep -il 'revalidat\|304\|if-none-match' HEAD -- corpus/ SKILL.md`

### Per-Hit Findings

| Lane | Sibling artifact (path @ HEAD) | Section | Verdict | Holds RFC 9111 §4.3 decision ground kake does not? |
|---|---|---|---|---|
| `tabi` | `SKILL.md` | §4 "network (wire capture)" (lines 374, 403, 423, 433); §Approval table / notes (lines 889, 891, 1052, 1146) | **PROVINCE-LOCAL** | **NO.** Observes client CDP `responseReceived` (200) vs wire `responseReceivedExtraInfo` (304) in browser loopback tests; explicitly records at line 891 that protocol semantics remain unexamined ("why client status reads 304 only for the revalidated style.css ... still unlanded"). |
| `tabi` | `corpus/knowledge/network-evidence-rung.md` | §4 "Byte equation", §6 "Layer routing" (D7 "wire 304 vs client 200"), §9 "Network-rung capture rules" | **PROVINCE-LOCAL** | **NO.** Loopback test harness observing browser network events under ThreadingHTTPServer; measures live wire responses without evaluating RFC 9111 §4.3 precondition or decision logic. |
| `tabi` | `corpus/knowledge/multi-step-journey.md` | §2, §6, §7 (effective status post-revalidation, wire 304 vs client 200) | **PROVINCE-LOCAL** | **NO.** Empirical browser loopback journey log documenting that the browser client reports 200 while the wire received 304. |
| `tabi` | `corpus/knowledge/async-step-evidence.md` | §3 "Cache, revalidation and the second journey" | **PROVINCE-LOCAL** | **NO.** Measures warm cache fetch lines in Chromium loopback runs; no decision engine. |
| `tabi` | `corpus/knowledge/carried-debt-closure-r8.md` | §2 "Round-6 L1 matrix — the wire-class / cache-revalidation decision for repeats" | **PROVINCE-LOCAL** | **NO.** Notes open debt regarding browser loopback repeat-fetch categorization. |
| `tabi` | `corpus/knowledge/layer-routing-synthesis.md` | §2 (RT3 wire status 304, RT10 cache revalidation staging) | **PROVINCE-LOCAL** | **NO.** Synthesizes CDP layer arbitration rules for GET journeys; no RFC 9111 cache validation engine. |
| `tabi` | `corpus/evidence/w4-t41-network/` (`driver-warm.sh`, `journey.mjs`, `run6-reval/*`, `summary.txt`) | Fixture logs and JSON traces | **PROVINCE-LOCAL** | **NO.** Raw loopback server and client traces recording HTTP/1.0 304 Not Modified wire lines. |
| `tabi` | `corpus/evidence/round-31/decision-table/bytes/S122.html` | Retained doc snapshot (lines 64, 78, 79) | **PROVINCE-LOCAL** | **NO.** External documentation capture of GitHub REST API best practices describing client use of `etag` and `if-none-match`; does not implement or decide cache validation rules. |
| `tabi` | Incidental hits: `corpus/README.md`, `corpus/SOURCES.md` (S081, S085, S122), `corpus/adjacency-*.tsv`, `corpus/evidence/**/*.json` | Bibliography, adjacency tables, trace metadata | **PROVINCE-LOCAL** | **NO.** Lexical coincidences (PIDs, sha256 substring "304", or line number 304 citations). |
| `kumitate` | `corpus/knowledge/receipt-age-on-the-compare-path.md` | "## The one asymmetry to RFC 9111" (lines 37–46; cites S237 = RFC 9111 §4.2.3 and §4.3.4) | **PROVINCE-LOCAL** | **NO.** Compares RFC 9111 §4.3.4 (304 updates stored response headers, resetting apparent age per §4.2.3) with kumitate's local static snapshot age gate (`omp-census.mjs --max-age`), which lacks a revalidation event. Does not evaluate conditional requests or revalidation exchanges. |
| `kumitate` | `corpus/lessons/round-38.md` | `## Mistakes` Check21 (line 105) | **PROVINCE-LOCAL** | **NO.** Refers to internal build artifact stat cache skipping revalidation; no HTTP or RFC 9111 semantics. |
| `kumitate` | `corpus/knowledge/distill-and-l3.md` | l3 swarm tests (lines 204, 268) | **PROVINCE-LOCAL** | **NO.** Rust harness lane startup validation. |
| `kumitate` | Incidental hits: `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/knowledge/cost-and-profile.md`, `kimi-residue-files.md`, `live-surface-probe.md`, etc. | Various sections | **PROVINCE-LOCAL** | **NO.** Lexical non-overlaps (line number 304, commit hash `165b8304`, byte counts, general validation). |
| `kotodama` | `corpus/SOURCES.md` (S304: Pazuzu), `corpus/knowledge/` (vessel-container, persia-sasanian, worldbible), `corpus/lessons/` | Various sections | **PROVINCE-LOCAL** | **NO.** All hits are source row S304 (Sarah Graff 2014, "Pazuzu: Beyond Good and Evil"), page number 304, or linguistic/worldbible validation. Zero HTTP or RFC 9111 content. |
| `chousa` | `corpus/SOURCES.md` (row S025, RFC 9111 §4.2 Freshness) | Row S025 (rejected) | **PROVINCE-LOCAL** | **NO.** Chousa explicitly REJECTED RFC 9111 in round 25 as inapplicable to research-record validity ("REJECTED: a standard for HTTP-cache freshness, not authority for research-record validity"). |
| `chousa` | Incidental hits: `SKILL.md`, `corpus/captures/*.raw`, `corpus/evidence/**/*.json`, `corpus/lessons/round-25.md` | Captures, evidence, lessons | **PROVINCE-LOCAL** | **NO.** Lexical coincidences: date stamps (`20230420`), street address (`3049`), page numbers (`1293–1304`, `6288–6304`), or binary byte sequences. |
| `souji` | `corpus/lessons/round-9.md` | Line 14 | **PROVINCE-LOCAL** | **NO.** Refers to git worktree cache revalidation under git 2.55; no HTTP semantics. |
| `souji` | Incidental hits: `corpus/README.md`, `corpus/SOURCES.md`, `corpus/lessons/` | Commit hashes | **PROVINCE-LOCAL** | **NO.** Hex commit hashes containing `304` (`778747eb…30467c`, `ca7fc1cb…304686`, `8376f442389f304340db…`). |

**Conclusion on Scan (1):**
Across all 5 sibling lanes, **zero sibling lanes hold RFC 9111 §4.3 decision ground**. Kake's C2 instrument (`scripts/reval_exchange.py`, contract `reval-contract-v1.md`, scored by `c96_reval.py`) is the sole capability in the fleet evaluating the RFC 9111 §4.3 revalidation exchange over supplied values.

---

## 2. Refreshed Sibling Overlap Matrix (Round 96)

Refreshed from round 95 (`overlaps.md` rows 1–12) at current sibling HEADs:

| # | Sibling artifact (path @ HEAD) | Class touched | Overlap in principle | Province-local or contested | One-line verdict |
|---|---|---|---|---|---|
| 1 | `tabi-shokunin/scripts/check-selfassessment.mjs` (SKILL.md:2627 registry row; `corpus/evidence/round-24/c2-measurements.json`) | A (C1 calibration) | Frozen-CASES calibration counter with zero-mismatch predicate, self-test asserting exit and finding id, and counter sha256 pinned in registry. Same AXES.md calibration axis. | **Contested.** Tabi compares SCORECARD/LOG tallies against git state; kake's E1–E5 audits corpus structure and integrity. | CONTESTED: report, do not absorb; distinct surfaces under shared fleet axis. |
| 2 | `chousa-shokunin/corpus/evidence/round79/selfcheck-v2.py` (registry row SKILL.md:175; QUALITY.md criteria 83 at :880 and 146 at :1054) | A (C1 audit / repair naming) | S1 registry cell-count and S3 Mistakes-row erratum with digest are closest match to kake E4/E5 and R94-3. QUALITY.md line 1054 criterion 146 documents the exact defect class: repair accepted as set membership with no content check. | **Contested.** Reads fleet-template documents shared across lanes. | CONTESTED: cite chousa criterion 146 (line 1054 confirmed) as prior art for R94-3/R95-3; do not port code. |
| 3 | `chousa-shokunin/corpus/evidence/round62/controls/null-counter.py`, `path-keyed-counter.py`, `c1v2-before.txt`; `corpus/evidence/round79/forge-battery.py` | A/B (battery & falsification) | Do-nothing and label-keyed controls, forgers that must be refused. Same admission rule as kake QUALITY "Round 90" (do-nothing control, one forgery per conjunct, positive fixture). | **Contested** (method rule). Both lanes independently adopted the same testing discipline. | CONTESTED: cite as independent discovery; no code shared. |
| 4 | `kumitate-shokunin/scripts/gate-mutants.mjs` (contract `kumitate-gate-mutants-v2`, kill predicate K43; registry row SKILL.md:617) | B (mutant kill) | Frozen mutant population, kill predicate over self-test run. Kill requires an immediate rerun with identical sorted failing case names. Re-verified at `0bff4bab`. | **Contested.** Kumitate K43 requires rerun stability and says nothing about equivalence. Kake C2 requires digest-pinned equivalence receipts for survivors. | CONTESTED: a fleet-level kill-predicate arbitration is needed (R95-2). Kake must not adopt either silently. |
| 5 | `tabi-shokunin/scripts/check-gate-mutants.mjs` + `scripts/gate-mutants.json` (fault vs benign catalogue; 12 self-test cases) | B (equivalence) | Benign-mutant class = equivalence declared at catalogue authoring time (must survive). Kake R94-4 = equivalence checked after survival via empirical receipt. Re-verified at `58d84eda`. | **Contested** (conflicting default vs row 4 and kake). | CONTESTED: conflicting fleet defaults; operator arbitration needed (R95-2). |
| 6 | `tabi-shokunin/scripts/check-measurement-binding.mjs` (SKILL.md:1836 "Measurement-binding gate registry") | Instrument pinning | Binds counted claim to counter blob sha256 at measured revision, ancestry, and counted-input drift. | **Contested** (instrument-binding discipline shared across lanes). | CONTESTED: candidate for instrument governance discipline; do not import. |
| 7 | `kumitate-shokunin/scripts/counter-pins.mjs` (contract `kumitate-counter-pins-v1`; `.ufo/pins/counter-pins.json`; SKILL.md:627) | Registry of frozen counters | Machine check that registered counter bytes match pins. Kake registers counters in SKILL.md without a standalone machine check script. | **Contested** (registry-of-counters pattern). | CONTESTED: note for SKILL.md gate registry rows; do not port. |
| 8 | `kotodama-shokunin/corpus/knowledge/verification/gate-frozen-run-standard.md` + `tools/check-gate-battery.py` | Frozen-run pins | Digest-pinned frozen runs with committed expected verdict; "a digest proves the bytes, never the tool". | **Fleet standard, not contested.** Governed by fleet PROTOCOL.md §Gate standard "Two evidences". Kake complies. | FLEET-STANDARD: cited, no overlap action. |
| 9 | `chousa-shokunin/tools/quote-reopen.py` + `corpus/evidence/round29/c1-count.py` (registry SKILL.md:91–92; ≤25 words verbatim rule) | Source hierarchy (quote verification) | Located-quote check: exact substring of retained or fetched body, ≤25 words. Kake's S477/S478/S479/S480 quote checks use the same ≤25-word rule. | **Contested.** Chousa owns source-hierarchy verification; kake executes per-round quote checks over RFC bodies. | CONTESTED: keep kake quote checks scoped to lane sources; do not build duplicate fleet verifier. |
| 10 | `tabi-shokunin/scripts/check-freshness.mjs` (SKILL.md:1559 `closeout-pin-witness` row; `scripts/freshness-witness.mjs`) | Freshness gate | Pinned-expected freshness gate with witness and expected-file table. | **Province-local.** Tabi checks local kimi-webbridge plugin files. Kake's `freshness-sweep.mjs` checks publisher-side web properties, sitemaps, GHP subpaths. | PROVINCE-LOCAL: no absorption. |
| 11 | `tabi-shokunin/corpus/knowledge/network-evidence-rung.md` & `SKILL.md:374,433` (wire 304 vs client 200 observation) | Conditional request / revalidation (C2 adjacency) | Both touch 304 responses. Tabi captures live CDP browser/wire divergence in loopback runs. Kake decides precondition header construction and response handling over supplied values (RFC 9111 §4.3). | **Province-local.** Live browser telemetry observation versus publisher-side contract decision engine. Zero RFC 9111 §4.3 decision ground held by tabi. | PROVINCE-LOCAL: no absorption. |
| 12 | `kumitate-shokunin/corpus/knowledge/receipt-age-on-the-compare-path.md` (+ `scripts/omp-census.mjs --max-age`; cites RFC 9111 §4.2.3 as S237, §4.3.4) | Conditional / cache age (C2 adjacency) | Cites RFC 9111 §4.2.3 and §4.3.4 for 304 age-refresh asymmetry. Kumitate uses wall-clock snapshot age in days for receipt compare staleness. Kake executes RFC 9111 §4.3 revalidation exchange. | **Province-local.** Different subject; no shared code. Kumitate holds no RFC 9111 §4.3 decision ground. | PROVINCE-LOCAL: no absorption. |

### Overlap Counts

- Overlap candidates with an opened sibling artifact: **12** (rows 1–12).
- Contested: rows 1, 2, 3, 4, 5, 6, 7, 9 = **8**.
- Province-local: rows 10, 11, 12 = **3**.
- Fleet standard, not contested: row 8 = **1**.

**Verdict line (for the L1):**
`CONNECTOR overlaps=12 contested=8`

---

## 3. Refresh of R95-2 Evidence & Verbatim-Ready L0 Question Draft

### Re-verification of Sibling HEADs
Re-inspected at current sibling HEADs (`kumitate-shokunin` `0bff4bab`, `tabi-shokunin` `58d84eda`, `kake-shokunin` `049e8eca`):
1. **Kumitate (K43 rerun stability):** `scripts/gate-mutants.mjs` implements contract `kumitate-gate-mutants-v2`. A mutant is killed iff its run exits non-zero with `VERDICT: FAIL`, confirmed by an immediate second rerun producing identical sorted failing case names. Equivalence is unrepresented.
2. **Tabi (catalogue-time equivalence):** `scripts/check-gate-mutants.mjs` and `scripts/gate-mutants.json` partition mutants at catalogue authoring time into `fault` (must be killed) and `benign` (must survive as semantic equivalence). Rerun stability is not checked.
3. **Kake (digest-pinned equivalence receipts):** `c96_reval.py` and `c95_conditional.py` score frozen mutant populations (`frozen/mutants-reval.json`, 14 mutants); surviving mutants are admitted only when proved semantically equivalent across exhaustive input spaces via digest-pinned receipts (`frozen/c2-equiv-receipts.json`, R94-4/R95 M11 precedent), with round 96 freezing `mutants=14/14 with no survivor`.

The three lane defaults remain distinct and unreconciled at current HEADs.

### Verbatim-Ready L0 Question Text (Two Sentences)

```text
Fleet mutation testing defines 'killed' across three conflicting lane defaults: kumitate's K43 requires immediate rerun stability of failing case names, tabi declares equivalence at catalogue authoring time via a fault/benign partition, and kake requires digest-pinned exhaustive input-equivalence receipts for surviving mutants. Should the fleet establish a unified mutant-kill standard across lanes, or should individual lanes continue to govern equivalence and rerun discipline under local provincial contracts?
```

---

## 4. Confirmation of Chousa Criterion 146 (R95-3 Citation)

Re-verified read-only at current chousa HEAD `378fda82dc2cbcc555a0565052cc408121813cef`:
- **File:** `corpus/QUALITY.md`
- **Line number:** `1054`
- **Heading/Text:**
  `146. **A self-assessment counter validates each resolution line against the bytes it claims to repair, and its audit window covers every block rather than the newest.** Round 78's selfcheck.py accepted correction: SKILL.md:168, supersedes: 142 and erratum: round-77.md:73 as set membership with no content check, so a scratch mirror carrying all three routed defects and three hollow repair lines printed SELFCHECK=PASS unresolved=0/3 at exit 0 (R78ReviewB/ALL-three-hollow.txt), and appending any newer ## Round-<n> addition block removed every earlier criterion from pointer auditing (R78ReviewB/atkB2-new-block-window.txt). Check before a successor freeze: every repair line carries a shape or digest assertion about the row, criterion or lesson …`

Line 1054 at chousa HEAD `378fda82` is confirmed. Kake's C1 QUALITY criterion citation of chousa round-79 criterion 146 as prior art for R94-3/R95-3 is verified accurate to line.
