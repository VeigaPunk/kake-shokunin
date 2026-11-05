# ConnectorScope — Round 93 Sibling-Overlap, Script Duplication, and Registry Scan

VERDICT: C1 holds; C2 holds; no sibling overlap, internal script boundaries clean, 0 within-scope duplicate URLs, census advisories 31 → 37 (W04 ok, exit 0).

Seat: `ConnectorScope` (leaf connector, kake round 93, wave 1).
Scope: Read-only scan across sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin` and inside `kake-shokunin`; registry audit of `w1/ScribeSources/rows.append.md`.

---

## 1. Sibling-Overlap and Duplication Scan

Scanned across 20 sibling lane repositories under `/home/vgpnk/Projects/shokunin/*-shokunin` (excluding `kake-shokunin`) in `corpus/knowledge/` and `scripts/` for seven target terms:
`conditional-request`, `ETag`, `entity-tag`, `If-None-Match`, `If-Modified-Since`, `304`, `revalidation`.

Receipt: `.ufo/waves/round-93/w1/ConnectorScope/receipts/sibling-scan.txt`.

### Findings by Sibling Lane

1. **Non-HTTP False Positives (19 lanes)**:
   - `audio-shokunin`, `chousa-shokunin`, `game-dev-3d-shokunin`, `kaidoku-shokunin`, `kama-shokunin`, `kasegi-shokunin`, `kengaku-shokunin`, `kotoba-shokunin`, `kotodama-shokunin`, `kumitate-shokunin`, `lore-shokunin`, `mado-shokunin`, `mori-shokunin`, `revenger-shokunin`, `tameshi-shokunin`, `tsukuroi-shokunin`:
     - Every hit for `304` is a line number (e.g. `c1:304`), source ID (e.g. `S304`), byte count (e.g. `98,304 B`), process PID, timestamp millisecond, or commit/hash fragment (e.g. ZIP signature `504b0304` in `revenger-shokunin`).
     - Hits for `ETag` in `kumitate-shokunin` and `kengaku-shokunin` refer to task/session "retagging" (`route-probe-cluster.md:117`, `bench-arena-round8-horizon.md:87`), not HTTP entity tags.
     - Hits for `revalidation` in `kama-shokunin` (`free-tier-provider-limits.md:75`) and `kumitate-shokunin` (`remaining-scripts-census.md:555`) refer to periodic recheck scripts and shell wrapper execution, not HTTP revalidation.
     - `game-dev-2d-shokunin`, `kagi-shokunin`, `souji-shokunin`: 0 hits across all terms.

2. **Adjacent Empirical Fragment: `tabi-shokunin` (81 raw hits)**:
   - `tabi-shokunin` holds empirical browser-wire observation records from rounds 6–9 using Chrome DevTools Protocol (`Network.responseReceivedExtraInfo`) and Playwright:
     - `corpus/knowledge/network-evidence-rung.md:24`: wire status observation of `HTTP/1.0 304 Not Modified`.
     - `corpus/knowledge/network-evidence-rung.md:69`: a test fixture server (`server.py`, 1,800 B, sha256 `a5ceef29fae5`) implementing Python's stock `ThreadingHTTPServer` with a mock `If-Modified-Since` 304 path and `Cache-Control: no-cache` mode.
     - `corpus/knowledge/network-evidence-rung.md:94, 214, 311, 410`: browser cache revalidation staging, documenting that Chrome's CDP reports client status 200 or 304 while wire status is 304, and that CDP cache flags (`fromDiskCache`/`fromMemoryCache`) evaluate to `false` during wire revalidation.
     - `corpus/knowledge/layer-routing-synthesis.md:73, 80`: wire status vs client status under revalidation.
     - `corpus/knowledge/carried-debt-closure-r8.md:17, 68`: wire-class / cache-revalidation matrix.

### Fleet-Wide Novelty Assessment

- **Duplicate**: None. No sibling lane implements RFC 9110 §13.2.2 precedence, RFC 9110 §13.1.1–13.1.4 precondition evaluation, RFC 9110 §8.8.3.2 entity tag comparison functions, or RFC 9111 §4.3.2 cache role evaluation.
- **Adjacent**: `tabi-shokunin`'s empirical observation of browser CDP wire-304 behavior with a Python test server is adjacent at the HTTP protocol layer, but strictly observational from the client/browser perspective.
- **Genuinely New**: `kake-shokunin`'s round-93 C2 candidate (`scripts/conditional_eval.py`) is the **first and only** normative HTTP precondition evaluation engine in the shokunin fleet, implementing the formal 6-step recipient precedence order and comparison functions over structured representations.

---

## 2. Internal LANE Script Boundary and Duplication Check

Inside `kake-shokunin`, `scripts/conditional_eval.py` was evaluated against all seven existing caching/inspection scripts:
`scripts/stored_reuse.py`, `heuristic_freshness.py`, `cache_current_age.py`, `cache_key.py`, `vary_match.py`, `cache_control_effective.py`, `capture_delta.py`.

Receipt: `.ufo/waves/round-93/w1/ConnectorScope/receipts/script-boundaries.txt`.

### Boundaries by Script

1. **`scripts/stored_reuse.py` (Round 91)**:
   - *Decision*: Stored response reuse permission (`reuse`, `revalidate`, `serve-stale`, `must-revalidate-fail`, `not-storable`, `heuristic-undecided`, `only-if-cached-miss`).
   - *Boundary Line Quote* (`scripts/stored_reuse.py:28-29`):
     `"* no network, no revalidation exchange (RFC 9111 4.3), no cache store, and no statement about any live property;"`
   - *Relation*: `stored_reuse.py` decides *whether* a cache must revalidate. When it returns `revalidate`, it hands off without evaluating precondition headers or computing 304/412. `conditional_eval.py` evaluates the resulting conditional request without deciding storage or reuse.

2. **`scripts/heuristic_freshness.py` (Round 92)**:
   - *Decision*: Heuristic freshness lifetime calculation (`explicit`, `heuristic`, `not-heuristically-cacheable`, `heuristic-undecided`, `not-storable`).
   - *Boundary Line Quote* (`scripts/heuristic_freshness.py:26-28`):
     `"It reports the lifetime and the heuristic flag; it does not store, reuse, serve or revalidate anything, and it does not re-decide what scripts/stored_reuse.py (round 91) already decides beyond the freshness lifetime."`
   - *Relation*: Decides time intervals; `conditional_eval.py` evaluates precondition match/status.

3. **`scripts/cache_current_age.py` (Round 87)**:
   - *Decision*: Conservative 6-term current-age arithmetic.
   - *Boundary Line Quote* (`scripts/cache_current_age.py:6-7`):
     `"This is not a Date parser, clock, network client, freshness lifetime calculator, or storage/reuse permission model."`
   - *Relation*: Disjoint numerical clock arithmetic.

4. **`scripts/cache_key.py` (Round 89)**:
   - *Decision*: URI and Vary-nominated secondary key generation.
   - *Boundary Line Quote* (`scripts/cache_key.py:5-7`):
     `"The key is built from exactly three ingredients: the request URI, the field names nominated by Vary, and those fields' presented values."`
   - *Relation*: Key hashing only; no precondition evaluation.

5. **`scripts/vary_match.py` (Round 88)**:
   - *Decision*: Request matching over Vary-nominated header names (`match` vs `mismatch`).
   - *Boundary Line Quote* (`scripts/vary_match.py:7-9`):
     `"exit 0, stdout exactly \"match\" -> the stored response may be considered to match the presented request; exit 0, stdout exactly \"mismatch\" -> it may not"`
   - *Relation*: Compares presented request headers to stored request headers for cache-key lookup; does not evaluate preconditions or representation state.

6. **`scripts/cache_control_effective.py` (Round 85)**:
   - *Decision*: First-occurrence parsing of Cache-Control response directives.
   - *Boundary Line Quote* (`scripts/cache_control_effective.py:2`):
     `"Bounded RFC 9111 response Cache-Control reader; not a cache permission model."`
   - *Relation*: Header token extraction; does not evaluate preconditions.

7. **`scripts/capture_delta.py` (Round 82)**:
   - *Decision*: Capture tree comparison using SHA-256 and header mapping.
   - *Boundary Line Quote* (`corpus/knowledge/capture-drift-validators.md:87-88`):
     `"A further consequence of the mapping rule: the gate never reads ETag as a validator. If an ETag differs it shows up as one more field=etag change=changed entry with body=same..."`
   - *Relation*: Drift detection over static capture archives; ignores validator comparison semantics.

**Conclusion**: `scripts/conditional_eval.py` duplicates zero decisions made by existing lane scripts.

---

## 3. Census Audit of Draft SOURCES Rows

Audited `w1/ScribeSources/rows.append.md` (drafted by `ScribeSources`): 6 rows (S471–S476) appending to `corpus/SOURCES.md`.
Receipts:
- `.ufo/waves/round-93/w1/ConnectorScope/receipts/new-rows.txt`
- `.ufo/waves/round-93/w1/ConnectorScope/receipts/testlane-census.txt`

### Audit Results

1. **Row Count and ID Sequence**:
   - Rows added: 6 (S471, S472, S473, S474, S475, S476).
   - Base registry: 216 rows, highest ID S470.
   - ID sequence is strictly continuous without gaps or collisions: S470 → S471..S476.

2. **Within-Scope Duplicate URL Check (E04)**:
   - `sources-census.sh validate` defines E04 as duplicate `(normalized_url, scope)`.
   - Each row defines an explicit, non-overlapping `scope` cell:
     - S471: `scope: The order in which a recipient evaluates...`
     - S472: `scope: Which entity-tag comparison function an origin server applies to If-Match...`
     - S473: `scope: Which entity-tag comparison function a recipient applies to If-None-Match...`
     - S474: `scope: The conditions under which a recipient must ignore a date-based precondition...`
     - S475: `scope: The two entity-tag comparison functions as defined...`
     - S476: `scope: Which conditional header fields a cache must not evaluate...`
   - **Result: E04 count = 0 (clean)**.

3. **Tier Inflation Check (E06, E10)**:
   - S471–S475 cite RFC 9110 (`kind=spec`, `tier=A`).
   - S476 cites RFC 9111 (`kind=spec`, `tier=A`).
   - Under SOURCES-CONTRACT-v1, normative IETF standards-track specifications are canonical Tier A.
   - **Result: Tier inflation = 0 (E06=0, E10=0)**.

4. **Census Validation and Advisory Count**:
   - Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate <lane>`
   - Result: `ok /.../corpus/SOURCES.md`, **exit code 0**.
   - Advisory Count: **37 advisories** (all `W04 duplicate url ... across scopes`).
     - Base had 31 advisories (`assimilation/census-before.txt`).
     - Exactly 6 new advisories emitted (one for each new row citing the existing RFC URLs with a distinct scope).
     - Informational warnings only; does not fail validation.

---

## 4. UFO-FSD Connector Synthesis: One Non-Obvious Move

### Evidence
1. **Attack Seat Findings**:
   - `CriticClaims` demonstrated in `w1/CriticClaims/build_attacks.py` that `A_cache_lazy.py` (which defers or skips validation of `If-Match` and `If-Unmodified-Since` when `role == "cache"`) is accepted by the frozen counter `c93_conditional.py` because the frozen test population lacks a malformed field case under `role: "cache"`.
   - `ReviewC2` independently built 160 cases from `c2-contract.md` alone (`w1/ReviewC2/ReviewC2.md`) and specifically generated refusal cases `R46–R48` testing malformed skipped fields under `role: "cache"`.
   - `CriticClaims` also demonstrated in `repair_minimal.py` that C1's predicate `c93_selfassess.py` can be structurally satisfied with empty headings, dummy file citations, and arbitrary file replacements while remaining semantically vacuous.
2. **Cross-Claim Coupling**:
   - C2 deliverables (`scripts/conditional_eval.py`, `corpus/knowledge/conditional-request-evaluation.md`, and its `SKILL.md` probe entry) expand the measured surfaces evaluated by C1's self-assessment counter (`c93_selfassess.py`).
   - If C2's knowledge entry omits or misformats the 3-line metadata header (`source:`, `verified-at:`, `recheck:` within first 8 lines), C1 class E3 immediately fails.
   - If C2's lesson entry (`corpus/lessons/round-93.md`) introduces a blank line in Mistakes or omits `## Gate`, C1 classes E4/E1 fail.
   - If `SKILL.md` row additions cite a non-existent path, C1 class E5 fails.

### Affected Axes
- `C1 calibration` (score 2 HOLD, lowest owned non-retired axis)
- `C2 freshness` (score 10 HOLD, capability acquisition)

### Proposed Move
**Pre-Carrier Cross-Claim Conformance Binding**:
1. In `scripts/conditional_eval.py`, strictly execute Clauses 1–4 validation eagerly on all supplied fields *before* branching on `role == "cache"`, satisfying Contract Clause 6 ("No evaluation before validation"). This closes the semantic hole identified by `CriticClaims` (`A_cache_lazy.py`) and ensures 100% agreement with `ReviewC2`'s 160-case contract battery.
2. In the C2 integration pipeline, run `python3 -B .ufo/waves/round-93/c93_selfassess.py --root . --revision HEAD` inside the pre-carrier fixture before committing C2 deliverables, verifying that C2's newly introduced files adhere to C1 classes E1–E5.

### Risks
- Eager validation could inadvertently reject valid edge cases if field parsing is overly rigid; mitigated by matching `frozen/pos-good.py`'s parser structure which achieves 160/160 on `ReviewC2`'s battery.
- Minor overhead during self-assessment replay; mitigated by in-memory AST and regex checking.

### Verification
- Run `c93_conditional.py` with eager candidate: `hand=44/44 generated=120/120 forgeries_refused=6/6 positive=admitted anti_table=ok population=ok met=true`, exit 0.
- Run `c93_selfassess.py` over integrated carrier: `mismatches=0 E1=0 E2=0 E3=0 E4=0 E5=0 pins=ok met=true`, exit 0.
