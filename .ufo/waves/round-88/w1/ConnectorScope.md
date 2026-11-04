# ConnectorScope — Sibling-Overlap, Province, Knowledge & Assimilation Scan (Round 88)

- **Seat:** `ConnectorScope`
- **Role:** UFO-FSD Connector
- **Round:** kake round 88 (attempt 1; campaign target: round 100)
- **Base commit:** `f4479c14813037ad993a49a3dee4028763470f7a`
- **Freeze v2:** `8063739791e21a8d7966fd968913e552e1433881`
- **Axes:**
  1. **Calibration** (lowest owned axis, 2 HOLD): C1 defect queue closure (D1 ledger companion, D2 diagnostic type, D3 recheck path).
  2. **Freshness** (10 HOLD): C2 conservative Vary-match reader capability (20 frozen + 200 random cases, S463 RFC 9111 §4.1).

---

## 1. Sibling-Overlap Scan (Read-Only)

Grep sweep across all 20 sibling lane repositories named in `/home/vgpnk/Projects/shokunin/shokunin.conf`:
`tabi-shokunin`, `chousa-shokunin`, `kama-shokunin`, `kumitate-shokunin`, `kaidoku-shokunin`, `kasegi-shokunin`, `kengaku-shokunin`, `kotoba-shokunin`, `kagi-shokunin`, `lore-shokunin`, `revenger-shokunin`, `tameshi-shokunin`, `mado-shokunin`, `tsukuroi-shokunin`, `mori-shokunin`, `kotodama-shokunin`, `souji-shokunin`, `audio-shokunin`, `game-dev-2d-shokunin`, `game-dev-3d-shokunin`.

### 1.1 `vary_match`
- **Result:** **Exact absence** across all 20 sibling lane repositories. No hits found (`grep` returncode 1).

### 1.2 `secondary cache`
- **Result:** **Exact absence** across all 20 sibling lane repositories. No hits found (`grep` returncode 1).

### 1.3 `cache key` / `cache-key`
- **`tabi-shokunin`:**
  - `tabi-shokunin/.ufo/waves/round-27/assimilation/rfc9110.txt:1165, 2442, 5706` — RFC 9110 upstream specification text retained as assimilation source material.
  - `tabi-shokunin/.ufo/waves/round-57/reviewer/fixtures/independent-sample/S142-rfc9110.bin:1165, 2442, 5706` — Same RFC 9110 text retained as test fixture.
  - `tabi-shokunin/.ufo/waves/round-31/w1-dispatch.json:331, 421`, `w1-spec.json:89, 197`, `a2w1/MutC1Rows.md:116`, `w1/MutC1Counter.md:5, 25, 47, 61`, `w1/RevCountersCode.md:84`, `w1/MutC1Counter/MUTANTS.md:63, 87`, `round-32/w2-results.json:142`, `round-32/w1/ScribeErrataB.md:34`, `round-32/w1/ScribeErrataB/errata-B.md:31, 124-125`, `round-32/w2/CritErrataDispositions.md:52, 130` — All hits refer to `tabi`'s internal test-runner script cache key `(url, quote)` for offline test receipts in `scripts/check-selfassessment.mjs` and `check-decision-table.mjs`. Not HTTP caching ground.
  - `tabi-shokunin/.ufo/waves/round-35/w1/AdjKotoba1.md:40, 43`, `w1/AdjKotoba1/decisions.md:14, 15`, `w1/AdjKotoba1/screen.tsv:6, 7`, `w2/CritScreenKotobaMixed.md:34`, `w2/CritScreenKotobaMixed/verdicts.tsv:15, 16`, `round-39/assimilation/validate/corpus/adjacency-screen-browser.tsv:260, 261` — Adjacency screening hits evaluating kotoba's harness router description cache key `sha256(prompt_template \0 name \0 description)`.
  - `tabi-shokunin/.ufo/waves/round-38/w1-results.json:292` — "cache-keyed artifacts" in execution summary.
- **`mori-shokunin`:**
  - `mori-shokunin/corpus/SOURCES.md:375` (S594): RFC 9111 §4.1: `"the Vary-selected representation and the cache-key rule: a stored response whose Vary value nominates request header fields is reused only when those presented fields match the original request's, and * never matches"`.
  - `mori-shokunin/corpus/evidence/sources-r79/rfc9111.txt:82, 261, 526` — RFC 9111 text pinned for S594: line 526 heading is `"4.1.  Calculating Cache Keys with the Vary Header Field"`.
  - `mori-shokunin/corpus/lessons/round-79-verifier-spotcheck.md:61` — Spot-check note quoting line 526.
- **Other 18 sibling lanes:** Exact absence of HTTP cache-key ground.

### 1.4 `Vary`
- **`tabi-shokunin`:**
  - `tabi-shokunin/corpus/evidence/round-29/release-pins/bytes/154.0.8037.97/third_party/blink/public/mojom/frame/frame.mojom:1211`
  - `tabi-shokunin/corpus/evidence/round-29/release-pins/bytes/156.0.8078.47/third_party/blink/public/mojom/frame/frame.mojom:1171`
  Both are Blink mojom code comments: `"// Updates the URL for a prerender ready to be activated via No-Vary-Search matching."`
- **`tameshi-shokunin`:**
  - `tameshi-shokunin/corpus/lessons/round-75.md:50` — Test fixture header hygiene note: `"the only authorization occurrence is the Vary: Authorization,Accept-Encoding request directive, not a credential value."`
- **`tsukuroi-shokunin`:**
  - `tsukuroi-shokunin/corpus/lessons/round-32-verifier-spotcheck.md:138`, `round-39-verifier-spotcheck.md:185` — Plain English verb ("vary every counted class", "vary device").
- **`kotodama-shokunin`:**
  - `kotodama-shokunin/corpus/knowledge/myth-symbol/binding-speech-complex.md:241` — Plain English verb ("Vary the formula's parts").
- **`mori-shokunin`:**
  - `mori-shokunin/corpus/README.md:861, 865`: `"## Round-79 knowledge addition — the Vary-selection ground"`.
  - `mori-shokunin/corpus/SOURCES.md:375`: Row S594 for RFC 9111 §4.1.
  - `mori-shokunin/corpus/knowledge/ua-serving-normative-r79.md:1, 3, 13, 14, 18, 22, 26, 40`: Entry titled `"Vary-selected representations: grounding the ua-serving class (round 79)"`. Grounding only: used to explain why observed per-User-Agent byte deltas at the same URL during fleet observability sweeps do not constitute content drift. The entry explicitly disclaims vendor header inspection, cache traversal, RFC compliance, and cache execution.
  - `mori-shokunin/corpus/lessons/round-79.md:45, 46, 64`, `round-79-verifier-spotcheck.md:61, 62, 72, 92`.
  - Pinned specification texts in mori evidence: `sources-r37/S221.src` (RFC 9110 text, 20+ lines), `sources-r37/S225.src` (Fetch spec, 6 lines), `sources-r79/rfc9111.txt` (10 lines).

### 1.5 Ownership Verdict
**No sibling lane owns Vary-match, cache-key, or conditional-request-selection ground.**
`tabi` owns client-side browser automation and navigation. `mori` owns fleet/host observability, and cited RFC 9111 §4.1 (S594) purely as normative justification for an observability classification (`ua-serving` vs `content-drift`), with an explicit disclaimer against cache mechanics. HTTP caching and response-header evaluation for web properties remain squarely in `kake`'s domain.

---

## 2. Province Boundary vs Adjacency Debt (`LANE/PROVINCE.md`)

### 2.1 Inside `kake`'s Province
1. **Publisher Response-Header Semantics:** Ground established in round 61 (`corpus/knowledge/response-header-expectations.md`, `scripts/response_snapshot.py`, `scripts/header_audit.py`) and refined in round 83 (`corpus/knowledge/header-change-classes.md`, `scripts/header_change_class.py`), where `vary` was designated the representative header that selects stored representations for incoming requests.
2. **Offline Conservative Vary Reader (C2):** `scripts/vary_match.py` and `corpus/knowledge/vary-matching.md` (grounded in RFC 9111 §4.1, new row S463). This is an offline, record-bound capability assessing pairwise request-header matching against a supplied `Vary` field value. It advances publisher-side representation auditing without making live network assertions.
3. **Calibration & Defect Queue Hygiene (C1):** D1 (`corpus/knowledge/gate-agreement-metadata.md`), D2 (`scripts/cache_current_age.py` diagnostic typing), and D3 (`corpus/knowledge/cache-current-age.md` recheck path). Maintaining strict gate integrity and provenance triples in `corpus/knowledge/` is core operational discipline.

### 2.2 Adjacency Debt (Reported, Not Absorbed)
1. **Full Cache-Key Construction & Secondary Indexing:** RFC 9111 §4.1 outlines how Vary expands the cache key. Building an actual multi-variant cache-key generator, URI normalization engine, or secondary cache index is complex caching middleware that exceeds kake's offline audit scope.
2. **Multi-Variant Cache Storage & Eviction:** Storing multiple representation variants per URI and selecting among matching variants based on freshness (RFC 9111 §4.1 lines 559–574) is proxy/server caching runtime ground. Kake evaluates pairwise matching only.
3. **Conditional Request Evaluation & Revalidation:** Generating conditional headers (`If-None-Match`, `If-Modified-Since`) or handling 304 Not Modified responses when a Vary mismatch occurs is browser/client runtime ground (adjacent to `tabi`) and origin server ground.
4. **Field-Specific Normalizations:** RFC 9111 §4.1 permits field-specific normalizations (e.g. reordering list members, case-folding values, collapsing internal whitespace). The declared profile explicitly refuses these and enforces byte identity after OWS trimming; claiming general semantic equivalence would be ungrounded overreach.
5. **Browser Cache Behavior:** Browser caching, service worker interception, and cache partitioning belong to `tabi`'s browser craft.
6. **Live Surface Certification & Deployment:** No live property (`ds4cc.com`, `kimi.page`) is certified compliant or modified; publication and DNS remain strictly operator-owned.
7. **Mori's Telemetry Scope:** Mori's S594 citation relates to host-level observation of vendor endpoints. Kake reports mori's existing citation of RFC 9111 §4.1 as adjacent ground, not absorbed telemetry.
8. **Calibration Ledger Decisions (D1):** `gate-agreement-ledger.json` is calibration metadata, not domain knowledge or new province ground (`PROVINCE.md:700–701`).

---

## 3. Existing Knowledge Scan (`LANE/corpus/knowledge`)

### 3.1 Hits for `Vary` in `kake-shokunin/corpus/knowledge/`
1. `corpus/knowledge/cache-control-effective.md:70`:
   `"No browser cache model; no Vary, Age calculation, Pragma, heuristic freshness, raw HTTP extraction, request/response cache interaction, or must-understand store-permission implementation."`
   *(Explicit disclaimer and refusal of Vary).*
2. `corpus/knowledge/cache-current-age.md:54`:
   `"RFC §4.2 also requires freshness_lifetime > current_age; §4 adds URI/method, Vary, directives, validation and other applicable reuse conditions."`
   *(Mentioned as an unhandled reuse condition in RFC 9111 §4).*
3. `corpus/knowledge/capture-drift-validators.md:223`:
   `"This is RFC 9111 cache-selection ground (S594 in mori, §4.1 Vary; S237 in kumitate, §4.2.3 Age) applied to this delta, reported as adjacency rather than re-taught."`
   *(Historical note citing mori's S594 as adjacent ground).*
4. `corpus/knowledge/header-change-classes.md:93-95`:
   `"accept-ranges, vary. For the first group a move is direct evidence that the payload metadata differs. vary is the instructive member: it does not describe bytes, but §4.1 makes it the field that selects a stored response for a request, so a moved vary changes the object-to-request mapping the capture is evidence about. It stays decisive."`
   *(Classifies Vary as a representation-class header for capture drift; does not state a match rule).*
5. `corpus/knowledge/hreflang-declaration.md:159`:
   `"- No HTTP headers, no Vary."` *(Exclusion of header-delivered hreflang).*
6. `corpus/knowledge/publish-queue.md:348`:
   `"raw shas vary per fetch"` *(English verb).*
7. `corpus/knowledge/x-robots-tag-header.md:112`:
   `"crawler's behavior is undefined and may vary"` *(English verb).*

### 3.2 Duplication & Cache-Key Assessment
- **Does a new entry duplicate an existing one?**
  **NO.** None of the existing entries states an RFC 9111 §4.1 Vary match rule, defines a matching algorithm, or provides a decision table for request matching. `corpus/knowledge/vary-matching.md` covers completely fresh ground.
- **Does any existing entry claim a cache-key guarantee that the conservative profile contradicts?**
  **NO.** `grep -i "cache[- ]key" corpus/knowledge/**` returns **zero hits**. No existing entry asserts any cache-key guarantee. The conservative profile (byte identity after OWS trim, ASCII case-insensitive field names, ordered array combining, wildcard mismatch, refusal of malformed inputs) is fully compatible with all held knowledge.

---

## 4. Assimilation Collision Status (`merge/kake`)

### 4.1 Extractor Command & Artifacts
Executed the exact id-collision extractor from `lane-addendum.md:470–473` (with `0-3 leading spaces` regex pattern):
```bash
S=/home/vgpnk/Projects/shokuknow
LANE=/home/vgpnk/Projects/shokunin/kake-shokunin
A=/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/w1/ConnectorScope

grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$LANE/corpus/SOURCES.md" \
  | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$S/merge/kake/SOURCES.append.md" \
  | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"
comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"
```

### 4.2 Counts & Results
- **Registry ID count (`reg-ids`):** **200** IDs.
- **Staged ID count (`staged-ids`):** **129** IDs.
- **Collision count (`collisions`):** **8** IDs.
- **Collision IDs:**
  ```
  S312
  S329
  S367
  S372
  S373
  S374
  S390
  S409
  ```

### 4.3 Staged ID List (`staged-ids`, 129 IDs)
```
S287 S288 S289 S290 S291 S292 S293 S294 S295 S296 S297 S298 S299 S300 S301 S302 S303 S304 S305 S306
S307 S308 S309 S310 S311 S312 S313 S314 S315 S316 S317 S318 S319 S320 S321 S322 S323 S324 S325 S326
S327 S328 S329 S330 S331 S332 S333 S334 S335 S336 S337 S338 S339 S340 S341 S342 S343 S344 S345 S346
S347 S348 S349 S350 S351 S352 S353 S354 S355 S356 S357 S358 S359 S360 S361 S362 S363 S364 S365 S366
S367 S368 S369 S370 S371 S372 S373 S374 S375 S376 S377 S378 S379 S380 S381 S382 S383 S384 S385 S386
S387 S388 S389 S390 S391 S392 S393 S394 S395 S396 S397 S398 S399 S400 S401 S402 S403 S404 S405 S406
S407 S408 S409 S410 S411 S412 S413 S414 S415
```

### 4.4 Registry ID List (`reg-ids`, 200 IDs)
```
S001 S002 S003 S004 S005 S006 S007 S008 S009 S010 S011 S012 S013 S014 S015 S016 S017 S018 S019 S020
S021 S022 S023 S024 S025 S026 S027 S028 S029 S030 S031 S032 S033 S034 S035 S036 S037 S038 S039 S040
S041 S042 S043 S044 S045 S046 S047 S048 S049 S050 S051 S052 S053 S054 S055 S056 S057 S058 S059 S060
S061 S062 S063 S064 S065 S066 S067 S068 S069 S070 S071 S072 S073 S074 S075 S076 S077 S078 S079 S080
S081 S082 S083 S084 S085 S086 S087 S088 S089 S090 S091 S092 S093 S094 S095 S096 S097 S098 S099 S100
S101 S102 S103 S104 S105 S106 S107 S108 S109 S110 S111 S112 S113 S114 S115 S116 S117 S118 S119 S120
S121 S122 S123 S124 S125 S126 S127 S128 S129 S130 S131 S132 S133 S134 S135 S136 S137 S138 S139 S249
S262 S263 S273 S274 S286 S312 S329 S367 S372 S373 S374 S390 S409 S416 S417 S418 S419 S420 S421 S422
S423 S424 S425 S426 S427 S428 S429 S430 S431 S432 S433 S434 S435 S436 S437 S438 S439 S440 S441 S442
S443 S444 S445 S446 S447 S448 S449 S450 S451 S452 S453 S454 S455 S456 S457 S458 S459 S460 S461 S462
```

### 4.5 Cause of Collision
In `kake-shokunin/corpus/SOURCES.md`, IDs S312, S329, S367, S372, S373, S374, S390, S409 were already committed in earlier rounds for Yahoo! and Baidu crawl documentation (e.g. S374 Yahoo! `rel=nofollow`, S329 Baidu robots, S312 Baidu mobile matching, S390 Baidu render UA). The external staged file `/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md` assigned those same numeric IDs to different documents.
- **Disposition:** Consistent with `contract.md:101–102`, the merge package cannot be appended without extensive renumbering; the round reports **`Assimilation: none`**.

---

## 5. UFO-FSD Connector Move: Input-Validation Precedence & Dual-Surface Wire Fixture

### 5.1 Evidence
1. **The Order-of-Validation Defect in C2:**
   - Testing the candidate `w1/ExecReader/vary_match.py` against `.ufo/waves/round-88/c88_vary.py` revealed failures on 3 seeded random cases (`r53`, `r150`, `r193`), scoring `197/200`.
   - **Root cause:** `ExecReader/vary_match.py` checked `if star: return 'mismatch', None` (lines 112–113) *before* calling `normalise_request()` on `stored` and `presented` (lines 114–119). When a response carried `Vary: *` or `Vary: accept, *`, but the request payload contained malformed data (such as `{"accept": 5}` or an empty list `[]`), the wildcard branch short-circuited and returned `mismatch` with exit 0 instead of failing closed with `invalid_input:` and exit 1.
   - In contrast, the reference in `c88_vary.py` (lines 81–85) explicitly specifies:
     ```python
     a, b = normalise(stored), normalise(presented)
     if a is None or b is None:
         return 'invalid'
     if star:
         return 'mismatch'   # input validation precedes the wildcard rule
     ```
   - Candidate `w1/L1/vary_match.py` normalized `stored` and `presented` before checking `star`, correctly scoring `20/20 frozen` and `200/200 random` (`met: true`).
2. **Coupling to C1's Diagnostic Discipline (D2):**
   - In C1, defect D2 occurred because `cache_current_age.py` emitted an inaccurate type name (`boolean` instead of `float`) when refusing invalid input.
   - In C2, `vary_match.py` must maintain the exact same diagnostic discipline: any malformed input type must fail closed with an explicit, unambiguous refusal naming the parameter.
3. **Live Wire Evidence from `ExecTrial`:**
   - `ExecTrial` captured headers from `https://ds4cc.com/`:
     ```http
     vary: Accept-Encoding
     age: 0
     cache-control: max-age=600
     date: Wed, 04 Nov 2026 18:52:27 GMT
     ```
   - Notice that the exact same wire response provides the live input parameters for **both** round tools:
     - `vary: Accept-Encoding` feeds `vary_match.py` (C2).
     - `age: 0`, `date`, `max-age: 600` feed `cache_current_age.py` (C1).
   - Under RFC 9111 §4, cache reuse requires evaluating *both* §4.1 Vary matching and §4.2 Age freshness. Currently, C1 and C2 are verified in complete isolation with no cross-tool fixture.

### 5.2 Affected Axes
- **Calibration (lowest owned axis, 2 HOLD):** Strengthened by locking down input-validation precedence across CLI tools and eliminating the schema-bypass defect where wildcards masked corrupt payloads.
- **Freshness (10 HOLD):** Improved by ensuring the new Vary-match capability is 100% compliant with the RFC 9111 §4.1 reference contract (`200/200 random`), while establishing a concrete offline path connecting response freshness lifetime to representation selection.

### 5.3 Proposed Move
1. **Lock Input-Validation Precedence into C2:** Enforce that in `scripts/vary_match.py`, payload structure and schema validation (`tokens(vary)`, `normalise(stored)`, `normalise(presented)`) strictly precede all match/mismatch heuristics (including `*` and absent-field comparisons).
2. **Standardize Diagnostic Type Reporting:** Mirror D2's precision in `vary_match.py` refusals (e.g. reporting the exact JSON type received, ensuring `invalid_input:` is emitted without stdout).
3. **Bind Live Observation into a Dual-Surface Offline Fixture:** Synthesize `ExecTrial`'s captured `response-headers.txt` into a committed offline integration test (`tests/test_caching_wire_fixture.py` or wave receipt) that runs both `cache_current_age.py` (C1) and `vary_match.py` (C2) against the identical recorded `ds4cc.com` response, proving both capabilities hold simultaneously over an authentic publisher wire capture without making live HTTP requests during test runs.

### 5.4 Risks
- **Over-constraining Stderr Messages:** `c88_vary.py` checks only `p.stderr.startswith('invalid_input:')`. Ensuring descriptive messages does not break the counter as long as the prefix remains exact.
- **Network Dependency:** Relying on live network fetches in verification would violate hermeticity; the move avoids this by consuming only the *retained* offline capture from `ExecTrial/response-headers.txt`.

### 5.5 Verification
1. **C2 Verification:**
   ```bash
   python3 -B .ufo/waves/round-88/c88_vary.py --tool scripts/vary_match.py --work <scratch>
   ```
   *Expected:* `frozen: 20/20, random: 200/200, met: true`, exit code 0.
2. **C1 Verification:**
   ```bash
   python3 -B .ufo/waves/round-88/c88_defect_queue.py --root . --revision HEAD --work <scratch>
   ```
   *Expected:* `items=3 open=0 closed=3 met=true`, exit code 0.
3. **Dual-Surface Offline Check:** Run both tools against `ExecTrial/payload-identical.json` and the captured `ds4cc.com` age/date values; assert exit 0 and mutual consistency (`match` for Vary, `current_age` computed).

---

## 6. Host & Environment Receipts
- **Scratch directory:** `/fast/scratch/hyaku/kake-r88/ConnectorScope/` (receipt files copied to wave directory; scratch purged prior to yielding).
- **Retained wave directory artifacts:**
  - `reg-ids` (200 IDs, sha256: `a92e45e46e11ed6db65cf37fb0291b43fa9341ba1f1ee985e020ae3639120d2a`)
  - `staged-ids` (129 IDs, sha256: `3938ec94ee29d52d27e6192603a9c30b9bfee3a8969600c7207478c3828f9deb`)
  - `collisions` (8 IDs, sha256: `a443d89dc53a6ad4d6c8d6c7204116f378bdd479620dcbb95a02a92def8ea9a0`)
- **External Network Requests:** 0 (read-only scan over local repositories and staged text).
- **Tools Installed / Modified:** None.
