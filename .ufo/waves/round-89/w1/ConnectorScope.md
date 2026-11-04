# ConnectorScope — Sibling-Overlap, Province, Knowledge & Assimilation Scan (Round 89)

- **Seat:** `ConnectorScope`
- **Role:** UFO-FSD Connector
- **Round:** kake round 89 (one v1 wave, 14 seats; campaign target: round 100)
- **Base revision:** `76225160d0dff8d2042fbcd037bd08b0971d5e07`
- **Freeze commit:** `08ab46a130a6355a7b19e2bfa83ffb7e116db803`
- **Axes:**
  1. **Calibration** (lowest owned non-retired axis, 2 HOLD): C1 defect queue closure (R88-A selftest number, R88-B gate sample counts, R88-C unbacked re-run claim, R88-D unpinned count, R88-E freeze-after-dispatch, R88-F lesson shape), measured by `.ufo/waves/round-89/c89_defect_queue.py`. Base: `items=6 open=6 closed=0 met=false`, exit 1.
  2. **Freshness** (10 HOLD, bounded capability): C2 conservative Vary-nominated cache-key constructor (`scripts/cache_key.py`), measured by `.ufo/waves/round-89/c89_key.py` against `.ufo/waves/round-89/c2-contract.md`. Base: candidate absent, `frozen=0/16 props=0/200 refuse=0/9 controls=5/5 met=false`, exit 1.

---

## 1. Sibling-Overlap Scan (Read-Only Sweep across 20 Sibling Lanes)

A comprehensive read-only search was conducted across all 20 sibling lane repositories located in `/home/vgpnk/Projects/shokunin/`:
`tabi-shokunin`, `chousa-shokunin`, `kama-shokunin`, `kumitate-shokunin`, `kaidoku-shokunin`, `kasegi-shokunin`, `kengaku-shokunin`, `kotoba-shokunin`, `kagi-shokunin`, `lore-shokunin`, `revenger-shokunin`, `tameshi-shokunin`, `mado-shokunin`, `tsukuroi-shokunin`, `mori-shokunin`, `kotodama-shokunin`, `souji-shokunin`, `audio-shokunin`, `game-dev-2d-shokunin`, `game-dev-3d-shokunin`.

Search targets: `*-shokunin/corpus/knowledge` and `*-shokunin/SKILL.md`.
Search patterns: `cache key`, `cache-key`, `Vary`, `9111`, and `stored-response-key`.
Raw receipts captured and preserved in `.ufo/waves/round-89/w1/ConnectorScope/`:
- `receipt-cache-key-space.txt` (8,419 B, sha256 `9840614ed545109beca18a8fb54e23514a5ff86f365507aea53061cf92c924f0`)
- `receipt-cache-key-hyphen.txt` (1,082 B, sha256 `58643f77504cb89de6e390e9c8b28e22e913c65921e77b5e08e1761bf8c25f5d`)
- `receipt-vary.txt` (9,517 B, sha256 `84993018fb10046d128d63f6b6c2c98e15c30950b32e57ffebaae131db24b45d`)
- `receipt-9111.txt` (24,770 B, sha256 `cd26f93acaa2819298a5ecb76440f5182965bdcd5f1eb16425a3d618851c64ad`)
- `receipt-stored-response-key.txt` (47 B, sha256 `05826f7ff744f4133e56bf72eea3179ae7c7c372418b35ac5aeafbf491f14db1`, 0 hits, exit 1)
- `receipt-cache-key-space-i.txt` (8,955 B, sha256 `f4d24cfeae8b3770e12e5ba014b3157b265e0b9cc9ed6f92062ac2f78a419efb`)
- `receipt-cache-key-hyphen-i.txt` (1,099 B, sha256 `5108c1eea6aa0da63d8a61bd86a2172f0863b9695b63e777700e3e7bf93db00d`)
- `receipt-vary-i.txt` (97,538 B, sha256 `87bcf503cc4c4eaafad575b320a6300d5a3eba3c67a9f3070e442a8c3ea33435`)

---

## 2. Hit-by-Hit Decision Table (Lane, File, Line, Sentence, Decision)

### 2.1 Hits for `cache key` and `cache-key`

| # | Lane | File & Line | Sentence verbatim | Decision |
|---|---|---|---|---|
| 1 | `chousa` | `corpus/knowledge/japanese-prisma-item-wording-r40.md:15` | `"The cache key is sha256(url)[:24]: the archive URL maps to 'e84bfe97808591d23fe3266f' (a '.txt' and a '.raw'), while the original URL maps to 'f3dbe2fe59a684b1b94cfadc', whose only file is 'f3dbe2fe59a684b1b94cfadc.fail', 6 bytes, holding 'rc=28' — no '.txt' and no '.raw'."` | **Complements.** Documents local disk caching of captured web/PDF documents via SHA-256 URL truncation. Does not touch HTTP caching or Vary. |
| 2 | `chousa` | `corpus/knowledge/quality-control-guideline-issued-text-r48.md:5` | `"verified-at: 2026-10-26 — both captures re-opened read-only from the campaign cache; every quoted phrase re-located with 'text.find' (count 1 each); each cache key recomputed as the first 24 hex of sha256 of its URL"` | **Complements.** Re-verifies local file cache retrieval keys (`sha256(url)[:24]`). Unrelated to HTTP header-nominated keys. |
| 3 | `chousa` | `corpus/knowledge/quality-control-guideline-issued-text-r48.md:18` | `"...the cache key of the PDF URL is 16fe8487aa97b98576a0dbac and of the notice URL cfa080b4046592eb9490a82c, each the first 24 hex of sha256 of its URL."` | **Complements.** URL hash indexing for offline files. Unrelated to Vary cache keys. |
| 4 | `kotoba` | `corpus/knowledge/harness-router-models-round9.md:23` | `"The cache key is 'sha256(prompt_template ‖ 0x00 ‖ name ‖ 0x00 ‖ description)' where the description is hashed exactly as the YAML loader yields it: the scalar style decides — plain/'>-' → ws-collapsed, no trailing newline (11 of 17 here); '>' → ws-collapsed + '\"\n\"' (5); '\|' → literal with newlines + '\"\n\"' (1) — i.e. 6 of 17 keys are newline-bearing (omarchy, wwkd, xbrd-ask, sekhmet-l3, kimi-webbridge, ufo)."` | **Complements.** Documents SQLite database cache key formula for omp agent prompt routing in `~/.omp/agent/skill-descriptions.db`. Completely distinct domain; zero collision. |
| 5 | `kotoba` | `corpus/knowledge/harness-router-models-round9.md:155` | `"The cache key includes the description; expect a truncator render until a new row lands, so a front-loaded draft must survive the cliff before the compressor catches up. [r9]"` | **Complements.** Invalidation dynamics of omp prompt description cache. Distinct domain. |
| 6 | `kotoba` | `corpus/knowledge/instruction-surface-census-round13.md:57` | `"(recorded, not check-enforced: the enforced pin there is the 273-byte compression-template sha256, which is what invalidates every cache key when it moves)."` | **Complements.** Compression template invalidation of omp router cache keys. Distinct domain. |
| 7 | `kotoba` | `corpus/knowledge/render-mechanism-round7.md:105` | `"The cache key includes the description, so editing a description invalidates its row and reverts the skill to the truncator until the compressor rewrites it."` | **Complements.** omp agent router cache key lifecycle. Distinct domain. |
| 8 | `kumitate` | `corpus/knowledge/remaining-scripts-census.md:555` | `"'lean_frozen_cache_digest' (':128-175') supplies a stat-based cache key for the frozen preflight; a matching successful cache entry skips revalidation (TTL defaults to 0), so this is not a guarantee that a workspace which needs the network is never frozen."` | **Complements.** Build-system filesystem stat caching for `cargo-shim`. Distinct domain. |
| 9 | `mado` | `corpus/knowledge/hyprland-synthetic-dispatch-r52.md:23` | `"\| P11 \| The resolution cache key combines the keyboard object's address and raw key text. \| S370 \| Hyprland-legacy-DispatcherTranslator.cpp:557 \| 'const auto KEYPAIRSTRING = std::format(\"{}{}\", rc<uintptr_t>(KB.get()), KEY);' \| direct \| Both components are formatted into the cache key. \|"` | **Complements.** C++ GUI window manager keybind resolution cache key formatting. Distinct domain. |
| 10 | `chousa` | `SKILL.md:143` | `"C1 'REAL' = five cache keys with sha256[:20] prefixes 'd341c133e37d65f02f8f' ('54fe0734c01f699e735b4b0a', byte twin '74ced3e9311594a8cc3f1f42')..."` | **Complements.** Test fixture gate criteria referencing document cache keys. Distinct domain. |

---

### 2.2 Hits for `Vary`

| # | Lane | File & Line | Sentence verbatim | Decision |
|---|---|---|---|---|
| 1 | `kotodama` | `corpus/knowledge/myth-symbol/binding-speech-complex.md:241` | `"Vary the formula's parts (§4) rather than its fixity."` | **Neither duplicates, complements, nor contradicts.** Natural English verb at sentence start; entirely orthogonal to HTTP. |
| 2 | `mori` | `corpus/knowledge/ua-serving-normative-r79.md:1` | `"# Vary-selected representations: grounding the ua-serving class (round 79)"` | **Complements.** Mori references RFC 9111 §4.1 Vary representation selection purely to distinguish User-Agent representation variants from content drift during host observability sweeps. |
| 3 | `mori` | `corpus/knowledge/ua-serving-normative-r79.md:3` | `"A changed body at one URL is not, by itself, evidence that the source's content changed. RFC 9111 §4.1 makes request-header matching part of cache selection when a stored response names those fields in Vary. This grounds the distinction the lane already makes empirically for S591/S592/S593: compare the same served variant before interpreting byte drift. The RFC supplies the cache-selection mechanism, not proof of why those particular vendor responses differed."` | **Complements.** Cites RFC 9111 §4.1 conceptually for observability; explicitly disclaims cache key construction, traversal, and execution. |
| 4 | `mori` | `corpus/knowledge/ua-serving-normative-r79.md:18` | `"The operative sentence spans :528–534: absent revalidation, a cache MUST NOT reuse the stored response unless the request fields nominated by its Vary value match the original request's fields."` | **Complements.** Locates normative text in RFC 9111 §4.1. |
| 5 | `mori` | `corpus/knowledge/ua-serving-normative-r79.md:22` | `"Vary is carried by the stored response; its value nominates the request-header fields whose matching matters for reuse. RFC 9111 §4.1 (:528–534) therefore distinguishes stored responses for the same target by more than URL alone. Matching permits the normalization listed at :536–550; an absent field only matches another absence (:552–554), and a Vary member of '*' never matches (:556–557). Where several stored responses match, the cache chooses among them (:559–565); where none matches, it cannot satisfy the request from those stored responses (:576–579). This is a conditional cache rule, not a claim that every origin varies on User-Agent."` | **Complements.** Summarizes RFC 9111 §4.1 rules for representation selection; no cache key constructor is built or claimed. |
| 6 | `mori` | `corpus/knowledge/ua-serving-normative-r79.md:26` | `"If a response nominates User-Agent in Vary, changing that request field can select a different representation. A byte difference between two User-Agent fetches of the same URL is therefore compatible with legitimate representation selection; it does not establish content drift by itself."` | **Complements.** Applies Vary concept to explain observed telemetry differences. |
| 7 | `mori` | `corpus/knowledge/ua-serving-normative-r79.md:40` | `"RFC 9111 §4.1 governs cache reuse and matching, not a vendor's origin-side negotiation or bot-management algorithm. It does not specifically name User-Agent in this section and does not prove that S591/S592/S593 emitted 'Vary: User-Agent', traversed a cache, complied with the RFC, or held identical underlying content. No response-header capture or new vendor fetch was performed for this entry. A cache-selection mechanism supports the distinction; it cannot certify the cause of a historical byte delta."` | **Complements.** Explicitly disclaims cache execution and key construction. |

---

### 2.3 Hits for `9111`

| # | Lane | File & Line | Sentence verbatim | Decision |
|---|---|---|---|---|
| 1 | `chousa` | `corpus/knowledge/capture-bash-pin-r39.md:43-44` | `"- After (landed gate): '8/8' on seeds 39011/39111 ('receipts/c1-after-s39011.json', 'receipts/c1-after-s39111.json'), both"` | **Neither.** PRNG seed number substring; unrelated. |
| 2 | `kaidoku` | `corpus/knowledge/2026-10-13-r2-doctor-reverify-r2.md:22` | `"...tools_sha256 25802f6de8c14ba736dc61ff1cbc7c5cd738fd74426aa01338f2dd03e0911166..."` | **Neither.** Hexadecimal substring in SHA-256 digest; unrelated. |
| 3 | `kumitate` | `corpus/knowledge/receipt-age-on-the-compare-path.md:1` | `"source: S237 — IETF RFC 9111, §4.2.3 *Calculating Age* (https://www.rfc-editor.org/rfc/rfc9111.html, opened 2026-11-04; row S237 labels it 'Section 5.1 (Age)' — the quoted sentence stands in §4.2.3, capture '.ufo/waves/round-81/build/L1/captures/rfc9111.html:2295-2297', 'sha256 ce91ee98…f3d7'); own-work — 'scripts/omp-census.mjs' ('compareShape', 'receiptAgeDays', 'validateShape'), '.ufo/pins/omp-shape.json', 'pin.omp-shape'"` | **Complements.** Cites RFC 9111 §4.2.3 Age calculations to compute receipt age in days for build shape governance. Does not touch §4.1 Vary cache keys. |
| 4 | `kumitate` | `corpus/knowledge/receipt-age-on-the-compare-path.md:39-40` | `"- \"The Age field value is the cache's estimate of the number of seconds since the origin server generated or validated the response.\" (§4.2.3; capture '.ufo/waves/round-81/build/L1/captures/rfc9111.html', lines 2295-2297).\n- A cache measures from generation or validation: a 304 updates the stored response's headers (RFC 9111 §4.3.4...)"` | **Complements.** Evaluates HTTP Age arithmetic and 304 revalidation header updating for offline shape comparison. |
| 5 | `kumitate` | `corpus/knowledge/self-asserted-instants.md:1` | `"source: S242 https://www.rfc-editor.org/rfc/rfc3339.html; S237 https://www.rfc-editor.org/rfc/rfc9111.html"` | **Complements.** Source citation for timestamp and caching specs. |
| 6 | `kumitate` | `corpus/knowledge/self-describing-shape-receipt.md:1, 34` | `"RFC 9111 gives the reusable shape: \"The Age field value is the cache's estimate of the number of seconds since the origin server generated or validated the response.\""` | **Complements.** Quoting §5.1 / §4.2.3 Age for receipt metadata. |
| 7 | `mori` | `corpus/knowledge/userspace-oom-killers-r26.md:1` | `"...sha256 abc2fc1f3d6f10d0f01b4d1ff18689eb5561a98fd71fde911117ce16c50ed72f..."` | **Neither.** Hexadecimal substring in SHA-256 digest; unrelated. |
| 8 | `tabi` | `corpus/knowledge/rate-signal-decision-table.md:211, 230` | `"September 2022 (June 2022 belongs to the RFC 9110/9111 references)... with the header date at line 11 (September 2022) and June 2022 only inside the RFC's own RFC 9110 and RFC 9111"` | **Complements.** Chronological cross-reference to RFC 9110 / RFC 9111 publication dates for date reconciliation. |

---

### 2.4 Hits for `stored-response-key`

- **Result:** **Exact absence** across all 20 sibling lane repositories (0 hits, exit 1). Captured in `receipt-stored-response-key.txt`.

---

## 3. The Overlap Rule Applied

The rule governing cross-lane domain boundaries is declared in `kake-shokunin/PROVINCE.md:6`:
> **Refuses:** anything outside this domain; report cross-domain evidence back to the orchestrator rather than absorbing it.

And in `kake-shokunin/PROVINCE.md:465`:
> Adjacency (reported, not absorbed...)

Consistent with this operational rule:
1. **Report, Do Not Absorb:**
   - Sibling lanes maintain their own specialized cache key definitions: `chousa` hashes URLs for local capture retrieval (`sha256(url)[:24]`); `kotoba` hashes prompt templates and descriptions for LLM model routing (`sha256(prompt ‖ 0x00 ‖ name ‖ 0x00 ‖ desc)`); `kumitate` hashes filesystem stats for build shims (`lean_frozen_cache_digest`); and `mado` formats window manager pointer addresses and keycodes.
   - `mori` references RFC 9111 §4.1 strictly as normative justification to distinguish User-Agent representation variants from content drift in observability telemetry, explicitly disclaiming cache execution and key derivation (`ua-serving-normative-r79.md:40`).
   - `kumitate` references RFC 9111 §4.2.3 and §5.1 Age calculations for receipt age tracking in `scripts/omp-census.mjs`.
2. **Kake's Exclusive Ground:**
   - HTTP response header evaluation, publisher caching directives, and RFC 9111 §4.1 Vary-nominated cache-key construction belong exclusively to `kake-shokunin`.
   - In round 88, `kake` built `scripts/vary_match.py` (C2), which explicitly disclaimed cache-key construction (`vary-matching.md:262`: *"Nothing here constructs, derives or compares a cache key"*).
   - In round 89, `kake` advances from pairwise matching to canonical stored-response key construction (`scripts/cache_key.py`, C2). This capability is new, bounded, and operates entirely within `kake`'s province.

---

## 4. Contested Scope & Canonical Key Form Assessment

- **Check:** Does any sibling lane hold a *different* canonical key form (a normalisation, a sort order, an escaping scheme) that would make kake's contract inconsistent with the fleet?
- **Finding:** **ZERO CONTESTED SCOPE.**
  - No sibling lane defines or uses an HTTP cache-key form.
  - No sibling lane specifies header name normalisation, member sorting, OWS value trimming, or delimiter escaping for HTTP headers.
  - Kake's declared canonical layout in `c2-contract.md`:
    ```
    key = ESC(uri) + US + join(US, [ESC(name) + RS + (ESC(value) if present else GS)])
    ```
    with:
    - ASCII lowercasing and lexicographical sorting of nominated header names;
    - Delimiter escaping: `%` → `%25`, `GS` (U+001C) → `%1C`, `FS` (U+001D) → `%1D`, `RS` (U+001E) → `%1E`, `US` (U+001F) → `%1F`;
    - Absent fields encoded as `GS`; present-empty values encoded as empty string;
    - Strict refusal of malformed JSON, missing/non-string URI, non-object headers, invalid RFC 9110 tokens, CR/LF in values, `*` wildcard, and case-insensitive duplicates;
    is **unique across the fleet**, introduces zero cross-lane contradictions, and establishes a clean, conflict-free standard.

---

## 5. UFO-FSD Connector Move: Ingestion-Boundary Multi-Line Normalization & Candidate Self-Test Anchor

### 5.1 Evidence

1. **The Real Wire Header Combination Gap (`ExecTrial.md` Defect D1):**
   - In `ExecTrial.md`, execution of the C2 capability over authentic captured responses from `burnerchrome.kimi.page` (R2, R2b), `veigapunk.kimi.page` (R3), and `charter-kimi` revealed that real HTTP servers emit `Vary` across multiple lines (e.g. `Vary: Accept-Encoding\r\nVary: Origin`).
   - RFC 9110 §5.3 specifies that multiple field lines with the same field name are combined into a single comma-separated list (`"Accept-Encoding, Origin"`).
   - However, `c2-contract.md` only specifies an already-combined string input `{"vary": <string>}` and does not declare how an ingestion adapter should handle multi-line wire headers. The trial driver had to introduce an unpinned `", "` join.

2. **The Adversarial Blind-Spot Gap (`ExecControls/scoring-detail.txt`):**
   - Testing adversarial mutant stubs against the frozen counter `.ufo/waves/round-89/c89_key.py` revealed that **7 mutant stubs passed completely** (`cand_met=true`, 16/16 frozen, 200/200 properties, 9/9 refusals):
     - `adv-bad-json`: missing JSON validation in certain branches.
     - `adv-cr-only`: refusing LF but not CR in values.
     - `adv-missing-headers`: omitting strict type checks on headers.
     - `adv-no-dup-vary`: failing to refuse case-insensitive duplicate `Vary` members (e.g. `Vary: Accept, accept`).
     - `adv-no-name-escape`: failing to escape control characters in header names.
     - `adv-no-uri-escape`: failing to escape control characters or `%` in URIs.
     - `adv-raw-sort`: sorting before case-folding names.
   - **Root cause:** The frozen counter's `REFUSALS` list in `c89_key.py` contains only 9 cases, omitting tests for duplicate Vary members (contract line 64) and CR/LF values (contract line 59). Furthermore, `_props` never generates URIs containing `%` or separators (`f'https://e.test/{i}'`). Thus, the counter's test suite has blind spots that permit non-compliant implementations to score 100%.

3. **Candidate Self-Defense in `L1/cache_key.py`:**
   - Both `ExecKey/cache_key.py` and `L1/cache_key.py` correctly implement the full contract (including duplicate Vary member rejection and URI escaping).
   - Crucially, `L1/cache_key.py` includes a standalone `--selftest` mode (lines 157–209) that explicitly verifies duplicate header name rejection, newline rejection, case-insensitive sorting, and separator collision prevention.

### 5.2 Affected Axes

- **Calibration (lowest owned axis, 2 HOLD):** Closes the verification gap between declared contract invariants and counter coverage without mutating the frozen `c89_key.py` counter (preserving R88-E freeze integrity). Prevents future rounds from inheriting unverified blind spots.
- **Freshness (10 HOLD, bounded capability):** Unifies offline cache-key generation with real publisher response-header captures (`round-61`, `round-81`), providing an exact, RFC 9110 §5.3-compliant ingestion path from live wire headers to canonical keys.

### 5.3 Proposed Move

1. **Standardize the Ingestion Boundary in Round-89 Lesson / Knowledge:**
   - Formally document in `corpus/lessons/round-89.md` that while `scripts/cache_key.py` accepts a single canonical `vary` string, upstream wire-capture adapters MUST combine multiple `Vary` header lines using `", "` per RFC 9110 §5.3 before constructing the JSON payload.
2. **Anchor Invariant Coverage in `scripts/cache_key.py --selftest`:**
   - Retain L1's dual-mode CLI design: when invoked with `--selftest`, `scripts/cache_key.py` runs an in-memory regression battery that explicitly asserts the 7 contract invariants missed by the frozen counter:
     - Case-insensitive duplicate `Vary` member rejection (`Accept-Encoding, accept-encoding`);
     - Rejection of CR and LF in header values;
     - Rejection of case-colliding header names (`{"Accept": "1", "accept": "2"}`);
     - Escaping of `%`, `US`, `RS`, and `GS` within URIs and header names;
     - RFC 9110 §5.3 comma-combination equivalence.
3. **Route Counter Hardening to Round-90 Calibration Queue:**
   - Record the 7 blind spots in `corpus/lessons/round-89.md` as an outside-routed finding for the round-90 counter generator, ensuring that future counter properties expand URI and refusal coverage.

### 5.4 Risks & Mitigations

- **Risk of Breaking Frozen Counter:** `c89_key.py` invokes candidates via stdin JSON and checks stdout/stderr.
  *Mitigation:* The `--selftest` flag is triggered only via explicit CLI argument (`argv`). When invoked via stdin JSON without arguments, `cache_key.py` operates in pure filter mode, maintaining 100% compatibility with `c89_key.py`.
- **Risk of Over-Constraining Input Formats:**
  *Mitigation:* `cache_key.py` continues to require a single string for `vary`; the RFC 9110 §5.3 join rule is applied at the adapter layer, preserving the contract's simple interface.

### 5.5 Verification

1. **Frozen Counter Verification:**
   ```bash
   TMPDIR=$(mktemp -d) python3 -B .ufo/waves/round-89/c89_key.py \
     --root . --revision HEAD --candidate scripts/cache_key.py --work "$TMPDIR/work"
   ```
   *Expected output:* `C2v1 ... frozen=16/16 props=200/200 refuse=9/9 controls=5/5 met=true`, exit 0.
2. **Candidate Internal Self-Test:**
   ```bash
   python3 -B scripts/cache_key.py --selftest
   ```
   *Expected output:* `selftest: 21/21 passed` (or all checks passing), exit 0.
3. **Real-Data Capture Verification:**
   ```bash
   python3 -B .ufo/waves/round-89/w1/ExecTrial/driver/trial.py \
     scripts/cache_key.py /tmp/trial-out .ufo/waves
   ```
   *Expected output:* All 6 real-data cases (`R1`–`R6`) produce keys identical to the reference output, exit 0.

---

## 6. Host & Environment Receipts

- **Scratch directory:** `/fast/scratch/hyaku/kake-r89/ConnectorScope/` (all receipts generated locally and copied into `.ufo/waves/round-89/w1/ConnectorScope/`; scratch directory purged prior to yielding).
- **Retained wave directory artifacts (`.ufo/waves/round-89/w1/ConnectorScope/`):**
  - `receipt-cache-key-space.txt` (8,419 B, sha256 `9840614ed545109beca18a8fb54e23514a5ff86f365507aea53061cf92c924f0`)
  - `receipt-cache-key-hyphen.txt` (1,082 B, sha256 `58643f77504cb89de6e390e9c8b28e22e913c65921e77b5e08e1761bf8c25f5d`)
  - `receipt-vary.txt` (9,517 B, sha256 `84993018fb10046d128d63f6b6c2c98e15c30950b32e57ffebaae131db24b45d`)
  - `receipt-9111.txt` (24,770 B, sha256 `cd26f93acaa2819298a5ecb76440f5182965bdcd5f1eb16425a3d618851c64ad`)
  - `receipt-stored-response-key.txt` (47 B, sha256 `05826f7ff744f4133e56bf72eea3179ae7c7c372418b35ac5aeafbf491f14db1`)
  - `receipt-cache-key-space-i.txt` (8,955 B, sha256 `f4d24cfeae8b3770e12e5ba014b3157b265e0b9cc9ed6f92062ac2f78a419efb`)
  - `receipt-cache-key-hyphen-i.txt` (1,099 B, sha256 `5108c1eea6aa0da63d8a61bd86a2172f0863b9695b63e777700e3e7bf93db00d`)
  - `receipt-vary-i.txt` (97,538 B, sha256 `87bcf503cc4c4eaafad575b320a6300d5a3eba3c67a9f3070e442a8c3ea33435`)
  - `receipt-sweep-summary.json` (1,315 B, sha256 `6e80d488ea20e18630ac8f9c2ccd9d9f2b78a1591ff789702a397faf7d9b38b6`)
- **Tools installed / modified:** None. No pacman, no uv tool, no pip, no cargo, no npx.
- **External network requests:** 0 (strictly read-only scan over local sibling repositories and lane artifacts).
