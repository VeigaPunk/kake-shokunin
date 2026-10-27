# ConnectorPattern

Cross-axis pattern scan across round 61's three claims: receipt-lineage watch (C1, calibration), offline response-header expectation audit (C2, operability), and live source re-verification with cadence date pins (C3, freshness). Evaluated against base `9f07731a`, w1 outputs, committed tools in `scripts/`, prior round instruments (c58, c60, robots/sitemap audits, freshness sweep), and w2 falsification findings. RULES.md channel record: zero tools installed or updated.

## 1. Named Axes

1. **Calibration (C1)**: Lowest non-retired axis (score 2, sat at 10/10/2). Self-assessment quality, integrity of reported measurement results, resistance to undisclosed retroactive tampering or mislabeling.
2. **Operability (C2)**: Capability acquisition (score 10). Offline deterministic verification of external publisher artifacts and contract compliance.
3. **Freshness (C3)**: Drift detection, empirical re-verification of external groundings, and scheduling maintenance lifecycles (score 10).

---

## 2. Comparison 1: C1 Receipt Calibration vs Prior c58 / Round-60 Patterns

### Prior Art
- **Prior c58 (`.ufo/waves/round-58/c58_receipt_rewrites.py` + `receipt-rewrites.json`)**:
  - *Scope & Population*: Dynamic git walk of any path matching `\.ufo/waves/round-[0-9]+/controls?/` on the first-parent line of the measured tip.
  - *Event Trigger*: Raw byte-level git blob inequality (`fromBlob != toBlob`) across first-parent commits (`M`, `D`, `A`).
  - *Granularity*: Byte-level classification (`pin-only`, `pending-fill`, `content`, `append`, `format`, `delete`, `readd`).
  - *Disclosure Ledger*: Strict 40-character SHA1 blob IDs (`fromBlob`, `toBlob`), path, commit, status, kind, and a note pointing to an existing file (`unpointed == 0`).
  - *Form*: One-off wave fixture counter, un-parameterized for ongoing general lane use.
- **Prior Round-60 (`c60_gate_truth.py` / `corpus/lessons/round-60-verifier-spotcheck.md`)**:
  - *Scope*: SKILL.md gate-registry status labels for 28 counters from rounds 48–59 (`live`, `historical`, `never met`).
  - *Grounded Convention*: R60-D3 introduced the strict receipt-grammar convention (`# receipt: <name>`), single-commit immutability rule under `.ufo/waves/round-<N>/controls/`.
- **Round-61 C1 (`scripts/receipt_lineage.py` + `.ufo/receipt-disclosures.json` + `c61_lineage_cases.py`)**:
  - *Scope & Population*: Statically frozen 144 files (`population-144.txt`) with strict membership predicates (`member_changed`, `member_missing`, `extra_member`).
  - *Event Trigger*: Semantic result-span mutation (`# receipt:`, `revision:`, `EXIT=`, `met=`, etc.) and `pending`-fill transitions, ignoring non-result lines.
  - *Disclosure Ledger*: Permanent, repo-level `.ufo/receipt-disclosures.json` (schema `kake-receipt-disclosures-v1`), matching simply on `(path, commit)`.
  - *Form*: Permanent CLI tool in `scripts/` with `--selftest` (68/68 passed), `--json`, `--root`, `--revision`, `--disclosures`.

### Overlaps & Duplication
- **Motivating Incidents Overlap Exactly**: The motivating incidents in `contract.md` (round 56 relabel at `ad06cb8a1` and round 57 pending-fill at `20217f23e`) are already captured by c58's ledger (`receipt-rewrites.json` events 16 and 19) and verified clean at base by `c58_receipt_rewrites.py`.
- **Historical Event Strict Subset**: As demonstrated by `CriticC1C58Overlap`, C1's 12 historical events are a strict subset of c58's 19 events (`events=12` vs `events=19`). C1 misses 7 historical rewrite events detected by c58 because C1 gates on receipt grammar and result spans. C1 does not expand historical rewrite detection coverage.

### Distinctness
- **Semantic Result Spans vs Raw Blobs**: c58 required disclosures for cosmetic whitespace or comment changes. C1 isolates verdict-bearing lines (`# receipt:`, `revision:`, `EXIT=`, `met=`), allowing harmless non-result edits (case L4).
- **Closed-World Population Boundary**: c58 only audited paths present in git diffs; it could not detect the silent deletion of unmentioned controls or the addition of rogue controls. C1's `population-144.txt` freezes base members explicitly (`member_missing`, `extra_member`).
- **Reusable Production CLI Tool**: C1 transitions from a disposable wave acceptance script to a hardened, permanent lane tool with strict CLI argument handling, environment scrubbing (`GIT_*`), and regression suites.
- **Scorecard Invariant Check**: C1 bundles `scores_held == 3` (operability 10, freshness 10, calibration 2), preventing unearned score inflation.

---

## 3. Comparison 2: C2 Response-Header Audit vs Robots / Sitemap Tools

### Prior Art
- **`scripts/robots_audit.py` (Round 37 C1 / Round 38 C2)**:
  - *Domain*: Offline publisher expectation audit for `robots.txt` under RFC 9309 (S011) and Google spec (S095).
  - *Architecture*: Strictly offline, manifest-driven (`--manifest <path>`), reads local files, bounded file sizes (64 MiB manifest, 500 KiB robots), 4 exit codes (0 clean, 1 failed-policy, 2 could-not-evaluate, 64 usage).
- **`scripts/sitemap_audit.py` (Round 39 C1)**:
  - *Domain*: Offline publisher sitemap protocol validation under sitemaps.org (S102) and W3C Schema (S103).
  - *Architecture*: Strictly offline, manifest-driven (`--manifest <path>`), XML validation, bounded file sizes (50 MiB), 4 exit codes (0/1/2/64).
- **`scripts/header_audit.py` (Round 61 C2)**:
  - *Domain*: Offline publisher HTTP response-header expectation audit under RFC 9110 (S433), RFC 6797 (S430), W3C CSP3 (S431), WHATWG Fetch (S432).
  - *Architecture*: Strictly offline, manifest-driven (`--manifest <path> [--root <dir>]`), reads pre-recorded `response.json` capture receipts, bounded file sizes (8 MiB), 4 exit codes (0/1/2/64).

### Overlaps & Duplication
- **Shared Architecture (The Offline Manifest-Driven Publisher Audit Archetype)**:
  All three tools implement identical design patterns:
  1. *Decoupled Acquisition*: Live network fetches are banished from the audit engine; a separate capture phase (`response_snapshot.py`, `live_snapshot.py`, or curl) writes immutable local fixtures.
  2. *Declarative Expectation Manifest*: A version-1 JSON manifest specifies check IDs, target identifiers, and boolean policy expectations.
  3. *DoS & Memory Hardening*: Explicit file size ceilings (500 KiB to 64 MiB) enforced before read/parse to prevent runaway allocations.
  4. *Deterministic 4-State Exit Protocol*: 0 (clean), 1 (policy violation or per-check failure), 2 (unreadable/invalid manifest), 64 (CLI usage error).
  5. *Hermetic Self-Test Suites*: Standalone `--selftest` executing comprehensive fixture cases without filesystem side effects (64/64 passed for `header_audit.py`).

### Distinctness
- **Payload Level**: `robots_audit` and `sitemap_audit` parse body document payloads (directive syntax trees and XML hierarchies). `header_audit` operates at the HTTP wire transport layer (field-line token syntax, case-insensitive header name matching, OWS trimming, singleton cardinality, and security policy headers HSTS/CSP/XCTO).
- **Output Interface**: `robots_audit` and `sitemap_audit` serialize a single top-level JSON object. `header_audit.py` produces streamable, whitespace-free 3-column finding lines (`<check-id> <class> <detail>`) followed by `checks=<n> findings=<k>`, matching the standard unix pipe convention of `scripts/receipt_lineage.py` and `scripts/append_guard.py`.

---

## 4. Comparison 3: C3 Cadence Pins vs Freshness Sweep

### Prior Art
- **`scripts/freshness-sweep.mjs` (Rounds 16, 18, 20)**:
  - *Domain*: Whole-repo operational health battery covering filesystem paths (`§paths`), probe history telemetry (`§history`), and external service endpoints (`§armed`).
  - *Mechanism*: Evaluates standing pins stored in a centralized configuration file (`corpus/knowledge/freshness-pins.json`). Compares live system observations against pinned scalar thresholds, hashes, and sets.
  - *Execution*: Monolithic execution (`node scripts/freshness-sweep.mjs [--section=...]`), returning binary clean/drift status.
- **Round-61 C3 Cadence Pins (`c61_recheck_pins.py` + `corpus/SOURCES.md`)**:
  - *Domain*: Targeted citation lifecycle management for the repository's external knowledge base.
  - *Mechanism*: Selects the oldest opened rows (S001–S010), conducts live GET requests to verify HTTP 200 and verbatim anchor quotes, and converts symbolic intervals (`90d`, `365d`, `on-release`, `on-use`) directly into concrete calendar dates (`opened + cadence` or `opened + 90d`).
  - *Execution*: Embedded in-band in `corpus/SOURCES.md` recheck cells; audited offline by `c61_recheck_pins.py` across 6 strict conditions.

### Overlaps & Duplication
- **Shared Freshness Mechanics**: Both instruments advance the Freshness axis by replacing untracked temporal drift with falsifiable empirical pins. Both implement honest non-blocking degradation: `freshness-sweep` marks offline/missing checks as `skipped` rather than passing; C3 preserves existing cadences and logs Gate notes when quotes cannot be re-verified live, refusing to invent synthetic dates.

### Distinctness
- **Operational Telemetry vs Knowledge Grounding**: `freshness-sweep` verifies whether local repo files, systemd timers, and server deployments function. C3 verifies whether external academic, RFC, and vendor standards cited by the knowledge base remain valid and unchanged.
- **Centralized Config vs In-Band Table Cells**: `freshness-sweep` pins live in `freshness-pins.json`. C3 embeds dates directly into the markdown table of `corpus/SOURCES.md`, ensuring native compliance with fleet-wide syntax (`scripts/sources-census.sh validate`).
- **Batch Drift Check vs Staggered Maintenance Scheduling**: `freshness-sweep` evaluates drift at the instant of execution. C3 schedules future expiration dates (e.g. `2027-01-17`, `2027-10-19`), establishing a deterministic queue for subsequent review rounds.

---

## 5. Smallest Distinct Generalization: The Asymmetric Two-Stage Verification Pipeline

Across all three claims, round 61 converges on a single architectural archetype:
**Stage 1: Capture & Ledger (Stateful / Network / Git)** $\rightarrow$ **Stage 2: Deterministic Projection (Offline / Hermetic / Bounded)**.

| Claim | Stage 1: Capture / Ledger | Stage 2: Offline Projection & Verification | Invariant Enforced |
|---|---|---|---|
| **C1 (Calibration)** | Git first-parent history walk + `.ufo/receipt-disclosures.json` | `scripts/receipt_lineage.py` + `population-144.txt` | Closed-world historical population; semantic result span immutability |
| **C2 (Operability)** | `scripts/response_snapshot.py` $\rightarrow$ `capture/<id>/response.json` | `scripts/header_audit.py` $\rightarrow$ `manifest.json` | Declarative publisher header compliance; offline determinism |
| **C3 (Freshness)** | Live GET $\rightarrow$ `.ufo/waves/round-61/recheck/` sha256 receipts | `c61_recheck_pins.py` $\rightarrow$ `corpus/SOURCES.md` | Concrete calendar expiration deadlines; quote-truth preservation |

### Systemic Contradictions Identified
1. **Receipt Storage Silos Break C1 Lineage Coverage**:
   - C1 monitors only `.ufo/waves/round-<N>/control(s)/*.{txt,json}`.
   - C2 stores capture receipts in `capture/<id>/response.json`. C3 stores recheck receipts in `recheck/<id>.receipt.txt`.
   - *Contradiction*: C2 and C3 receipts live outside `controls/` and are completely unmonitored by C1. A future round could rewrite a `response.json` or recheck receipt after the fact, and C1 would be blind to it.
2. **Duplication of Capture Apparatus**:
   - C2 uses `response_snapshot.py` to GET 12 endpoints with sha256, 2 MiB bounds, and userAgent `round61`.
   - C3 uses a separate fetch mechanism to GET 10 endpoints with sha256, 2 MiB bounds, and userAgent `round61`.
   - Both perform identical network tasks under identical constraints, but emit fragmented receipt formats.
3. **Calibration Credit Ambiguity**:
   - As established by `CriticC1C58Overlap`, C1's rewrite detection duplicates c58 (12 events $\subset$ 19 events). Claiming calibration credit purely for detecting undisclosed rewrites is indefensible against existing in-lane art.
   - The *only* genuine calibration advance in C1 is **closed-world population enforcement** (`extra_member`, `member_missing`) and **scorecard invariant locking** (`scores_held == 3`).

---

## 6. Non-Obvious Move (Bounded Proposal): Unified Artifact Manifest & Closed-World Calibration Contract

### Evidence
1. `CriticC1C58Overlap`: c58 at base already detects both motivating incidents and covers 19 historical events (C1 covers 12).
2. `ConnCrossClaim` & `ReviewerCrossClaims`: Round-61 controls namespace collision required w1 amendments because C1's population path regex conflated historical measurement records with current-round execution artifacts.
3. Local inspection: `header_audit.py` (selftest 64/64) and `receipt_lineage.py` (selftest 68/68) run hermetically; `sources-census.sh` validates `corpus/SOURCES.md` cleanly with 16 W04 warnings.

### Affected Axes
- **Calibration (improved)**: Grounds C1's calibration claim strictly on closed-world population closure (`population-144.txt`) and scorecard tamper resistance (`scores_held == 3`), rather than redundant rewrite detection.
- **Operability (improved & protected)**: Formalizes the Two-Stage Verification pattern across publisher audits and eliminates capture receipt isolation.
- **Freshness (improved)**: Preserves concrete calendar date pins (`YYYY-MM-DD`) in `corpus/SOURCES.md` without triggering census syntax errors or overdue warnings.

### Proposed Move
Synthesize the round's findings into a bounded three-part contract refinement:
1. **Formalize C1's Calibration Grounding as Population Closure, Not Rewrite Novelty**:
   - Formally document in the round lesson that c58 already covers the historical rewrite detection class.
   - Explicitly ground C1's calibration defense on:
     (a) Closed-world population enforcement (`extra_member` prevents unmonitored measurement accumulation; `member_missing` prevents silent deletion); and
     (b) Hard scorecard invariant verification (`scores_held == 3`), which detects unearned self-assessment inflation.
2. **Unify Stage-1 Capture Receipts under a Generic Artifact Manifest Schema**:
   - In subsequent rounds, replace fragmented capture paths (`capture/`, `recheck/`, `controls/`) with a unified Stage-1 receipt schema (`ufo-capture-receipt-v1`) carrying `url`, `status`, `headers`, `sha256`, `bytes`, `fetchedAt`, and `userAgent`.
   - Extend C1's lineage watch to inspect the declared Artifact Manifest, ensuring C2 and C3 receipts cannot be silently rewritten post-commit.
3. **Establish In-Band Date Pinning as the Standard Expiration Model**:
   - Maintain C3's date-pin pattern (`opened + cadence`) in `corpus/SOURCES.md` as the authoritative scheduling queue for all non-rejected sources, phasing out monolithic ad-hoc pin files (`freshness-pins.json`).

### Risks & Mitigations
- *Risk*: Extending C1's population watch to capture/recheck directories could trigger false positives during wave execution.
  *Mitigation*: Apply the round-boundary partition established in Amendment A2: the frozen historical population covers only rounds $< N$; current-round receipts are verified by content-addressable hash equality until round settlement.
- *Risk*: Pinned dates in `corpus/SOURCES.md` could become overdue if the lane does not sweep them before `YYYY-MM-DD`.
  *Mitigation*: C3 pins dates to `2027-01-17` and `2027-10-19` (82 to 357 days in the future), providing ample operational runway before `sources-census.sh` flags overdue status.

### Verification
- `python3 -B scripts/receipt_lineage.py --selftest` (verifies 68/68 checks pass).
- `python3 -B scripts/header_audit.py --selftest` (verifies 64/64 checks pass).
- `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` (exits 0, confirming date pin syntax validity).
- `python3 -B .ufo/waves/round-58/c58_receipt_rewrites.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 9f07731a873585e655a6518233ea39f5d9fb8204` (exits 0, proving c58 baseline coverage).

VERDICT: C1 receipt calibration duplicates c58 rewrite detection (12 events ⊂ 19) but distinctively provides closed-world population guards and scorecard tamper checks; C2 and C3 share with prior tools an Asymmetric Two-Stage Verification architecture whose silos must be unified to prevent unmonitored receipt drift.
