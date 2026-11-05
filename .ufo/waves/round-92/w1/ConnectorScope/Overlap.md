# Sibling-Overlap Scan and Registry Duplicate Analysis — Round 92 (kake)

**Seat:** ConnectorScope  
**Lane Root:** `/home/vgpnk/Projects/shokunin/kake-shokunin`  
**Base / Freeze Revision:** `a5640ca02c20f94a0fa03af41b977b46ae99808e`  
**Date:** 2026-11-04  

---

## 1. Executive Summary

This scan evaluated sibling repository overlap across the 20 sibling shokunin lanes under `/home/vgpnk/Projects/shokunin/*-shokunin/` for round 92's C2 capability ground (RFC 9111 §4.2.2 heuristic freshness), analyzed all RFC 9111 registry rows in kake's own `corpus/SOURCES.md`, evaluated within-scope duplicate rules under `CORPUS.md` rule 2, and rendered adjacency and non-absorption boundaries.

Key findings:
1. **Sibling Repositories:** Exactly 0 sibling repositories implement or ground RFC 9111 §4.2.2 heuristic freshness lifetime calculation. The exact phrases `"heuristic freshness"`, `"RFC 9111 §4.2.2"`, and `"stale-while-revalidate"` yield 0 hits across all sibling `corpus/knowledge/` and `corpus/SOURCES.md` files.
2. **Relevant Sibling Touchpoints:**
   - **`chousa-shokunin`** explicitly **REJECTED** RFC 9111 §4.2 (row `S025`) as authority for research-record metadata or validity.
   - **`tabi-shokunin`** empirically observed browser stylesheet revalidation variance in automated Playwright journeys (`async-step-evidence.md:264`) and noted that *"the mtime/heuristic-freshness candidate is correlational only"*.
   - **`kumitate-shokunin`** uses RFC 9111 §5.1 / §4.2.3 (row `S237`) strictly for self-describing shape receipt age tracking.
   - **`mori-shokunin`** uses RFC 9111 §4.1 (row `S594`) strictly for Vary-selected representation variation across User-Agents in web crawling.
   - **`kasegi-shokunin`** references `Expires` in RFC 9116 `security.txt` (row `S063`), an entirely distinct vulnerability disclosure format.
3. **LANE Registry Duplicate Verdict:** A new `SOURCES.md` row for RFC 9111 §4.2.2 (lines 686–720) is **NOT a within-scope duplicate** under `CORPUS.md` rule 2. It opens previously unmined, uncovered specification ground distinct from S456, S461, S462, S463, S467, and S469.

---

## 2. Exact Search Commands & Receipt Artifacts

All sibling searches were executed in read-only mode using `grep -rn` against `corpus/SOURCES.md` and `corpus/knowledge/` across all 20 sibling directories:
`audio-shokunin`, `chousa-shokunin`, `game-dev-2d-shokunin`, `game-dev-3d-shokunin`, `kagi-shokunin`, `kaidoku-shokunin`, `kama-shokunin`, `kasegi-shokunin`, `kengaku-shokunin`, `kotoba-shokunin`, `kotodama-shokunin`, `kumitate-shokunin`, `lore-shokunin`, `mado-shokunin`, `mori-shokunin`, `revenger-shokunin`, `souji-shokunin`, `tabi-shokunin`, `tameshi-shokunin`, `tsukuroi-shokunin`.

### Commands Executed:

```sh
# (1) Six required search terms across sibling targets
targets=$(for s in /home/vgpnk/Projects/shokunin/*-shokunin; do
  [ "$(basename "$s")" != "kake-shokunin" ] && echo "$s/corpus/SOURCES.md $s/corpus/knowledge"
done)

# Term 1: heuristic freshness
grep -rn "heuristic freshness" $targets > .ufo/waves/round-92/w1/ConnectorScope/receipts/query-heuristic-freshness.txt
# exit 1, 0 hits

# Term 2: RFC 9111 §4.2.2
grep -rn "RFC 9111 §4.2.2" $targets > .ufo/waves/round-92/w1/ConnectorScope/receipts/query-rfc9111-sec422.txt
# exit 1, 0 hits

# Term 3: Last-Modified
grep -rn "Last-Modified" $targets > .ufo/waves/round-92/w1/ConnectorScope/receipts/query-last-modified.txt
# exit 0, 48 hits across 9 lanes

# Term 4: heuristic
grep -rn "heuristic" $targets > .ufo/waves/round-92/w1/ConnectorScope/receipts/query-heuristic.txt
# exit 0, 142 hits across 14 lanes

# Term 5: stale-while-revalidate
grep -rn "stale-while-revalidate" $targets > .ufo/waves/round-92/w1/ConnectorScope/receipts/query-stale-while-revalidate.txt
# exit 1, 0 hits

# Term 6: Expires
grep -rn "Expires" $targets > .ufo/waves/round-92/w1/ConnectorScope/receipts/query-expires.txt
# exit 0, 11 hits across 2 lanes (kasegi, tabi)

# Extended discovery checks:
grep -rn "heuristic-freshness" $targets
# exit 0, 1 hit in tabi-shokunin

grep -rn -i "rfc9111" $targets > .ufo/waves/round-92/w1/ConnectorScope/receipts/query-rfc9111.txt
# exit 0, 11 hits across chousa, kumitate, mori, tabi

grep -rn "RFC 9111" $targets > .ufo/waves/round-92/w1/ConnectorScope/receipts/query-rfc-9111.txt
# exit 0, 16 hits across chousa, kumitate, mori, tabi

# (2) Registry scan in LANE
grep -rn "rfc9111" /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
# exit 0, 8 hits (7 table rows: S456, S457, S461, S462, S463, S467, S469, plus 1 lead bullet)
```

Receipt directory: `.ufo/waves/round-92/w1/ConnectorScope/receipts/`

---

## 3. Sibling Overlap Hit Table

| Term | Total Hits | Sibling Lanes with Hits | Representative Path & Line | What It Holds |
|---|---|---|---|---|
| **heuristic freshness** | 0 | None (0/20) | None | Zero hits for literal phrase across all 20 sibling repos. |
| **heuristic-freshness** | 1 | `tabi-shokunin` (1) | `tabi-shokunin/corpus/knowledge/async-step-evidence.md:264` | Empirical observation during browser testing: stylesheet revalidation variance across runs; notes *"the mtime/heuristic-freshness candidate is correlational only"*. |
| **RFC 9111 §4.2.2** | 0 | None (0/20) | None | Zero hits for exact section citation across all 20 sibling repos. |
| **RFC 9111 (general)** | 16 | `chousa-shokunin` (1)<br>`kumitate-shokunin` (8)<br>`mori-shokunin` (5)<br>`tabi-shokunin` (2) | `chousa-shokunin/corpus/SOURCES.md:35`<br>`kumitate-shokunin/corpus/SOURCES.md:191`<br>`mori-shokunin/corpus/SOURCES.md:375`<br>`tabi-shokunin/corpus/SOURCES.md:137` | **chousa S025:** Evaluated §4.2 and REJECTED it for research validity.<br>**kumitate S237:** Uses §5.1 / §4.2.3 for shape-receipt age on the compare path.<br>**mori S594:** Uses §4.1 for Vary-selected representation variation across User-Agents.<br>**tabi S123:** Cited in reference list of RFC 9309. |
| **Last-Modified** | 48 | `kaidoku-shokunin` (6)<br>`kasegi-shokunin` (3)<br>`kotoba-shokunin` (4)<br>`kotodama-shokunin` (1)<br>`kumitate-shokunin` (16)<br>`mori-shokunin` (5)<br>`tabi-shokunin` (3)<br>`tameshi-shokunin` (3)<br>`tsukuroi-shokunin` (7) | Multiple (see section 4) | **Passive metadata (45 hits):** Server HTTP header recorded during page/dataset capture.<br>**HTTP mechanism (3 hits):**<br>- `tabi`: `network-evidence-rung.md:556` (Last-Modified / IMS 304 in browser test passes).<br>- `tsukuroi`: `SOURCES.md:105` & `pause-lift-gate-r24.md:47` (pacman `libalpm` setting DB mtime from server's Last-Modified).<br>No sibling calculates heuristic freshness from Last-Modified. |
| **heuristic** | 142 | 14 sibling lanes | Multiple (see section 4) | Domain-specific heuristic logic: audio codec mapping (`audio`), text locator heuristics (`chousa`), binary disassembly (`kaidoku`, `revenger`), process listener inference (`kama`), triage gates (`kasegi`), evaluation theory (`kengaku`), linguistic patterns (`kotodama`), OOM killer (`tsukuroi`). |
| **stale-while-revalidate** | 0 | None (0/20) | None | Zero hits across all 20 sibling repos. |
| **Expires** | 11 | `kasegi-shokunin` (9)<br>`tabi-shokunin` (2) | `kasegi-shokunin/corpus/SOURCES.md:69`<br>`kasegi-shokunin/corpus/knowledge/rfc-9116-security-txt.md:1,13,21,42,43,51`<br>`tabi-shokunin/corpus/SOURCES.md:116`<br>`tabi-shokunin/corpus/knowledge/csrf-defense-shape-boundary.md:6` | **kasegi S063:** RFC 9116 `security.txt` `Expires` field (vulnerability disclosure clock).<br>**tabi S102:** IETF draft expiration date (`Expires 18 May 2024` for `draft-ietf-httpbis-rfc6265bis-13`).<br>Neither refers to HTTP `Expires` response header (RFC 9111 §5.3 / §4.2.1). |

---

## 4. Deep-Dive on Sibling Touchpoints

### 4.1 chousa-shokunin: S025 Rejection of RFC 9111 §4.2
In `chousa-shokunin/corpus/SOURCES.md:35`:
```markdown
| S025 | RFC 9111, HTTP Caching — https://www.rfc-editor.org/rfc/rfc9111 | spec | C | a general rule for research-record staleness or knowledge-entry metadata policy | section 4.2 Freshness; Standards Track, June 2022 | REJECTED: a standard for HTTP-cache freshness, not authority for research-record validity; flip: use as an explicitly labelled analogy and pair it with a directly relevant method source | rejected | 2026-10-21 | on-release | — |
```
- **What it holds:** chousa explicitly evaluated RFC 9111 §4.2 (Freshness) as potential methodology for research-record staleness, and rejected it. The stated reason is that HTTP-cache protocol rules are not epistemological authority for research validity.
- **Adjacency boundary:** chousa owns research method. This rejection is proper for chousa's meta-research domain, but does NOT constrain kake. Kake owns HTTP publishing freshness and cache control specifications.

### 4.2 tabi-shokunin: Browser Client Observation of Heuristic Freshness
In `tabi-shokunin/corpus/knowledge/async-step-evidence.md:264`:
```markdown
2. Why W-run1 and W-run2 (identical setup, fresh copies) differ in `style.css`
   revalidation count (4 vs 1), and why re-aged runs show 0 — mechanism
   unexamined; the mtime/heuristic-freshness candidate is correlational only.
```
And `tabi-shokunin/corpus/knowledge/network-evidence-rung.md:556`:
```markdown
the Last-Modified / If-Modified-Since 304 path used by the warm passes.
```
- **What it holds:** tabi automates user journeys in live browsers (Playwright, Firefox, Chromium). In measuring network request slices across page navigations, it observed variance in whether `style.css` was revalidated, hypothesizing that file mtime and browser heuristic freshness might correlate with the counts, but explicitly left the mechanism unexamined.
- **Adjacency boundary:** tabi owns live browser runtime and empirical client behaviour. Kake owns publisher-side placement and specification-conforming decision instruments over supplied integers. Kake's C2 contract explicitly isolates itself from browser runtime: *"It is not a clock, an HTTP-date parser, a network client, a cache store, a revalidation exchange, or a statement about any live property... browser behaviour stays frontier."*

### 4.3 kumitate-shokunin: S237 Receipt Age on the Compare Path
In `kumitate-shokunin/corpus/SOURCES.md:191`:
```markdown
| S237 | IETF RFC 9111 — HTTP Caching, Section 5.1 (Age) — https://www.rfc-editor.org/rfc/rfc9111.html | spec | A | A stored artifact can carry its own age, and the consumer decides freshness against a declared lifetime instead of assuming the artifact is current | *Age* and *Freshness* sections; fetched 2026-11-04; capture .ufo/waves/round-81/build/L1/captures/rfc9111.html (quote 22 words) | Disclose a receipt's age and make staleness an opt-in gate the consumer declares, never a silent score change | mined | 2026-11-04 | 180d | corpus/knowledge/self-describing-shape-receipt.md, corpus/knowledge/receipt-age-on-the-compare-path.md |
```
- **What it holds:** kumitate adopted RFC 9111's conceptual model of Age (§5.1 / §4.2.3) to stamp timestamps on artifact shape receipts so that comparing receipts can determine receipt age.
- **Adjacency boundary:** kumitate owns artifact assembly and build shape verification. Kake must not absorb kumitate's receipt-age tracking.

### 4.4 mori-shokunin: S594 Vary Representation Selection
In `mori-shokunin/corpus/SOURCES.md:375`:
```markdown
| S594 | HTTP Caching (RFC 9111) §4.1 — https://www.rfc-editor.org/rfc/rfc9111.txt | spec | A | the Vary-selected representation and the cache-key rule: a stored response whose Vary value nominates request header fields is reused only when those presented fields match the original request's, and `*` never matches | §4.1:528-534 (the reuse rule), :552-554 (absent field), :556-557 (`*`), :559 (choose among matches), :576 (no match); sha256 aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e; copy corpus/evidence/sources-r79/rfc9111.txt; 84477 bytes, 1956 lines | A per-User-Agent byte difference at one URL is compatible with legitimate representation selection and is not content drift | mined | 2026-11-04 | 180d | corpus/knowledge/ua-serving-normative-r79.md |
```
- **What it holds:** mori uses RFC 9111 §4.1 to explain why a crawler observing different response bytes for different User-Agent request headers is observing legitimate representation selection rather than site drift.
- **Adjacency boundary:** mori owns crawling and web representation tracking. Kake owns publisher cache-key construction and Vary matching for stored responses.

### 4.5 kasegi-shokunin: S063 RFC 9116 `security.txt` `Expires` Field
In `kasegi-shokunin/corpus/SOURCES.md:69`:
```markdown
| S063 | RFC 9116 — A File Format to Aid in Security Vulnerability Disclosure — https://www.rfc-editor.org/rfc/rfc9116.txt | spec | A | RFC 9116's own security.txt disclosure-channel discovery format: the machine-readable file a target publishes at /.well-known/security.txt, its eight defined fields with Contact and Expires the only REQUIRED ones, and the Expires staleness clock | RFC 9116 §2.5 field definitions ... §2.5.5 Expires ... |
```
- **What it holds:** kasegi grounds vulnerability disclosure discovery via RFC 9116, where `Expires` is a mandatory timestamp indicating when security contact data expires.
- **Adjacency boundary:** RFC 9116 `Expires` is not HTTP response caching `Expires`. Belongs strictly to kasegi's security triage domain.

---

## 5. LANE's RFC 9111 Registry Rows & Duplicate Analysis

### 5.1 Existing Registry Rows in `kake-shokunin/corpus/SOURCES.md`

`grep -rn "rfc9111" corpus/SOURCES.md` identifies 7 table rows:

| ID | URL | Tier | Scope Summary | Anchors | Used By | Status |
|---|---|---|---|---|---|---|
| **S456** | `https://www.rfc-editor.org/rfc/rfc9111.txt` | A | HTTP cache storage, freshness and validation bearing on reading two dated captures of one URI; Age clock estimate; ETag and Last-Modified validators compared for equivalence. | §3.1 heading 338, quote 340-342; §3.2 lines 369-388; §4 lines 466-490; §4.2 lines 581-599; §4.2.3 lines 719-738; §4.3.1 lines 812-850; §4.3.4 lines 986-988. | `corpus/knowledge/header-change-classes.md`<br>`corpus/knowledge/cache-control-effective.md` | mined |
| **S457** | `https://httpwg.org/specs/rfc9111.html` | A | Cache-Control response field value semantics: freshness vs freshness lifetime, max-age, ignoring unrecognized directives. | §4.2 heading and p.1-p.3 line 269; §5.2 heading and p.1 line 279; §5.2.2 heading and §5.2.2.1 max-age heading line 282; §5.2.3 p.1 line 282. | `corpus/knowledge/policy-value-classes.md`<br>`corpus/knowledge/cache-control-effective.md` | mined |
| **S461** | `https://httpwg.org/specs/rfc9111.html` | A | Response Cache-Control first-match lifetime and duplicate-value first-occurrence option, case-insensitive directive tokens, recipient quoted arguments, no-store and delta-seconds overflow. (Supersedes S457 for ordering rules). | Sections 1.2.2, 4.2.1 paragraphs 1 and 4, 5.2, 5.2.2.5 and 5.2.2.10. | `corpus/knowledge/cache-control-effective.md` | mined |
| **S462** | `https://httpwg.org/specs/rfc9111.html#age.calculations` | A | Conservative current-age arithmetic on supplied timestamps only. | Section 4.2.3; age_value definition and three equation blocks. | `corpus/knowledge/cache-current-age.md` | mined |
| **S463** | `https://httpwg.org/specs/rfc9111.html#caching.negotiated.responses` | A | Conservative Vary match profile: nominated-field matching, absence semantics, ordered line combination, wildcard member. (Superseded by S467). | Section 4.1; the MUST NOT sentence, three permitted transformations, absence sentence, wildcard sentence. | `corpus/knowledge/vary-matching.md`<br>`corpus/knowledge/cache-key-construction.md` | mined |
| **S467** | `https://www.rfc-editor.org/rfc/rfc9111.txt` | A | Cache key composition ingredients (method, target URI, Vary-nominated request fields) and section 4.1 title. (Supersedes S463). | Section 2 lines 251–262 and section 4.1 heading line 526. | `corpus/knowledge/cache-key-construction.md`<br>`corpus/knowledge/cache-key-conformance-gate.md` | mined |
| **S469** | `https://www.rfc-editor.org/rfc/rfc9111.txt` | A | Client request directives constraining reuse, first-match freshness-lifetime order, and when stale responses are forbidden or permitted. | Section 5.2.1 heading line 1111 (lines 1113-1201), section 4.2.1 heading line 652 (lines 654-684), section 4.2.4 heading line 784 (lines 786-799), section 1.2.2 (lines 214-217). | `corpus/knowledge/stored-response-reuse.md` | mined |

Note: Plain-text `rfc9111.txt` URLs are carried by **S456**, **S467**, and **S469**.

### 5.2 Duplicate Verdict for a New Row for §4.2.2 under CORPUS.md Rule 2

**VERDICT: NOT A DUPLICATE (Legitimate New Row Required).**

#### Legal & Structural Analysis under `CORPUS.md` Rule 2:
1. **Rule 2 Mandate:** `CORPUS.md` rule 2 states:
   > *"Append-only. Only status, recheck and used-by change in place... A correction is a new row whose teaches opens 'supersedes S0NN —'... Expansion is knowledge, not rows. The expansion trend counts admitted knowledge/ entries whose source: cites a mined row on uncovered coverage-map ground. There is no row quota; a short registry of opened, honestly tiered rows beats a long one."*
2. **Comparison with Round 91's Rejection of a Second Row for §4.2.3:**
   - In round 91, a proposed new row for §4.2.3 (Age Calculations) was **rejected** as a within-scope duplicate because **S462 already owned §4.2.3** on the same specification (`rfc9111.html#age.calculations`). The round-91 tool `scripts/stored_reuse.py` merely delegated age arithmetic to `scripts/cache_current_age.py` without modifying or respecifying the equation set. Citing S462 was sufficient.
3. **Absence of §4.2.2 in All Existing Rows:**
   - **S456** anchors §4.2 only at lines 581–599 (the high-level definitions of fresh and stale), jumping immediately to §4.2.3 (Age) and §4.3.1 (Validators). It does NOT anchor or scope §4.2.2 (lines 686–720).
   - **S457 / S461** anchor §4.2.1 (explicit freshness lifetime from Cache-Control / Expires).
   - **S462** anchors §4.2.3 (calculating age).
   - **S463 / S467** anchor §4.1 (Vary cache keys).
   - **S469** anchors §5.2.1 (request directives), §4.2.1 (explicit lifetime), and §4.2.4 (serving stale). In round 91, PROVINCE.md explicitly declared §4.2.2 out of scope: *"no heuristic freshness (§4.2.2 — with no explicit lifetime the answer is `heuristic-undecided`, never a guessed number)"*.
4. **Conclusion:**
   RFC 9111 §4.2.2 ("Calculating Heuristic Freshness", lines 686–720) is previously unmined, uncovered coverage-map ground. Drafting the C2 knowledge entry `corpus/knowledge/heuristic-freshness.md` requires grounding in a dedicated tier-A row (e.g. `S470`), anchored at `https://www.rfc-editor.org/rfc/rfc9111.txt` lines 686–720, with scope: *"Heuristic freshness lifetime assignment for responses without explicit expiration: status-code heuristically-cacheable set, public directive override, and fraction of interval since Last-Modified"*.
   Attempting to cite S456 or S469 for §4.2.2 would constitute false attribution (neither row anchors or teaches heuristic freshness calculation). Creating row S470 is therefore fully compliant with `CORPUS.md` rule 1 and rule 2.

---

## 6. Adjacency & Non-Absorption Verdict

### 6.1 Domain Boundaries

| Lane | Core Owned Domain | Scope Relative to HTTP Freshness |
|---|---|---|
| **`kake-shokunin`** | Publisher-side placement, cache-control policy, and freshness calculations/decisions on stored responses. | **OWNS** RFC 9111 §4.2.2 heuristic freshness lifetime calculation over supplied integer seconds (`scripts/heuristic_freshness.py`). Statically evaluated, stdlib only, no live browser execution. |
| **`chousa-shokunin`** | Research method: question → source hierarchy → citation chain → claim-vs-source check. | Evaluates information credibility and source validity. Does NOT own HTTP protocol mechanics. |
| **`tabi-shokunin`** | Browser automation, user journey execution, client-side runtime behavior. | Observes live browser behavior (Chromium, Firefox, Playwright). Does NOT specify cache protocol contracts. |
| **`kumitate-shokunin`** | Artifact assembly, shape verification, build reproducibility. | Uses RFC 9111 Age concepts for artifact receipt age. |
| **`mori-shokunin`** | Web crawling, mirror synchronization, representation selection. | Uses RFC 9111 Vary concepts for crawler request variation. |
| **`kasegi-shokunin`** | Vulnerability discovery, security disclosure channels. | Uses RFC 9116 `security.txt` fields. |

### 6.2 Prohibited Absorptions (What kake Must NOT Absorb)

1. **Must NOT absorb chousa's rejection of RFC 9111 §4.2 (S025):**
   - Chousa rejected RFC 9111 §4.2 because HTTP caching standards are not authority for research-record truth. Kake must NOT apply chousa's rejection to its own domain: for kake, RFC 9111 is tier-A normative ground.
2. **Must NOT absorb tabi's live browser journey observations (`async-step-evidence.md:264`):**
   - Tabi observed stylesheet revalidation variance in Playwright runs and called heuristic freshness "correlational only". Kake must NOT treat browser-engine implementation variance or network timing as specification truth. Kake's C2 capability evaluates pure mathematical functions over supplied header/integer inputs, explicitly decoupled from browser caching internals.
3. **Must NOT absorb kumitate's receipt-age metadata model (S237):**
   - Kumitate tracks age of test execution receipts. This is build-harness metadata, not HTTP response freshness.
4. **Must NOT absorb mori's crawler User-Agent negotiation findings (S594):**
   - Mori evaluates crawler representation selection across vendor endpoints. Kake evaluates cache-key matching and response freshness under declared contract rules.
5. **Must NOT absorb kasegi's RFC 9116 `security.txt` `Expires` logic (S063):**
   - RFC 9116 `Expires` is an absolute date for security vulnerability contact validity, not an HTTP response caching lifetime.
