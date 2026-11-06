# ScoutRfc9111 — kake round 99 w1 — re-open of the two C2 sources (S484, S485)

Date: 2026-11-05. Lane root: /home/vgpnk/Projects/shokunin/kake-shokunin (LANE).
Observed lane tip: `git -C LANE rev-parse master` = `7f5b1b7b8dbfdae74dfe6d487bbf5406c478b916`
(differs from round base `cde408e5817bf1376c701d8decc5469fa82b2985` — expected mid-wave state; observation, not a defect).
Scratch root used: /fast/scratch/hyaku/kake-r99/ScoutRfc9111 (deleted before yield; see §7).

## 1. Frozen-instrument verification (before attacking)

Command: `( cd LANE && sha256sum -c .ufo/waves/round-99/controls/instrument-sha256.txt )`, rc=0.
All 11 entries print OK: c99_registry.py, c99_fresh304.py, fresh304-contract.md, frozen/neg-constant.py,
frozen/neg-copyall.py, frozen/neg-firstmatch.py, frozen/neg-lenient.py, frozen/neg-lookup.py,
frozen/neg-mustnot.py, frozen/neg-weakstrong.py, frozen/pos-oracle.py. No mismatch found; no repair made.
Note: the list does not cover the two source bodies; the contract carries the rfc9111.txt digest inline
(`aeb52adb…`), freeze.md names `sources/eid9185.html` without a digest. Digests for both retained bodies
are recorded in §2 below; the S485 row draft (rows.md) carries the eid9185 digest.

## 2. Fetch receipts (three URLs, one GET each; curl 8.x, -L, --max-redirs 10)

| # | URL | start UTC | end UTC | observed chain | final URL (observed) | final code | bytes (size_download = on-disk size) | sha256 |
|---|-----|-----------|---------|----------------|----------------------|-----------|--------------------------------------|--------|
| 1 | https://www.rfc-editor.org/rfc/rfc9111.txt | 2026-11-05T23:16:07Z | 2026-11-05T23:16:07Z | REDIRS=0 (no redirects) | https://www.rfc-editor.org/rfc/rfc9111.txt | 200 | 84477 | aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e |
| 2 | https://www.rfc-editor.org/errata/eid9185 | 2026-11-05T23:16:07Z | 2026-11-05T23:16:08Z | REDIRS=2 | https://errata.rfc-editor.org/eid9185/ | 200 | 10655 | 83c3b795290e09842d1af973f73b52c98fd661bf77cafc17658eb5ac4df63dd3 |
| 3 | https://www.rfc-editor.org/errata_search.php?rfc=9111 | 2026-11-05T23:16:08Z | 2026-11-05T23:16:08Z | REDIRS=1 | https://errata.rfc-editor.org/search/?rfc_number=9111 | 200 | 40374 | b906ce97f132718b55c846639bb1ffdfcd0da387c7988fc7c055066bea3b7395 |

All three curls exited rc=0. Bodies copied to this directory: `rfc9111.txt`, `eid9185.html`,
`errata_search_rfc9111.html` (flat filenames).

**RFC body vs retained copy:** `cmp -s fetched rfc9111.txt LANE/.ufo/waves/round-99/sources/rfc9111.txt`
→ equal (RFC_MATCHES_RETAINED=yes); sha256 `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`
equals the digest recorded in fresh304-contract.md and freeze.md. **rfc9111-sha = match.**
EID page vs retained copy: `cmp -s` → equal as well (same digest as in the table above); retained
`sources/eid9185.html` sha256 = `83c3b795…` (no frozen digest exists for it; supplied here).

**Per-hop statuses — process defect and honest reconstruction.** The single GET pass ran without
`curl -v`, so per-hop status lines were NOT captured; only REDIRS counts, final URL, final code and
byte count are GET-observed. Reconstruction used separate method-HEAD probes (labeled; not the GETs):
- URL 1: HEAD `HTTP/2 200` directly (no hops) — consistent with REDIRS=0.
- URL 2: HEAD www.rfc-editor.org/errata/eid9185 → `HTTP/2 302`, `location: https://errata.rfc-editor.org/eid9185`;
  then HEAD (REDIRS=0) https://errata.rfc-editor.org/eid9185 → `HTTP/2 301`, `location: /eid9185/`.
  Reconstructed chain: 302 → 301 → 200 at https://errata.rfc-editor.org/eid9185/ (matches REDIRS=2 and final URL).
- URL 3: HEAD → `HTTP/2 302`, `location: https://errata.rfc-editor.org/search/?rfc_number=9111`;
  chain: 302 → 200 (matches REDIRS=1 and final URL).
The hop statuses above are HEAD-probe reconstructions, not GET-pass captures; recorded as such.

## 3. Located quotes (plain-text line numbers of the fetched/retained rfc9111.txt body)

All line numbers refer to that file (1956 lines). Section boundaries: §3.1 = 338-366, §3.2 = 369-414, §4.3.4 = 951-988.

| Q | Section | Lines | Quote (≤25 words) |
|---|---------|-------|-------------------|
| 1 | §3.2 add/replace sentence | 375-377 | "the cache MUST add each header field in the provided response to the stored response, replacing field values that are already present" (22 words) |
| 2 | §3.2 Content-Length exception (bullet 4 of the §3.2 exception list) | 387 | "*  The Content-Length header field." |
| 3 | §4.3.4 strong-validator MUST NOT | 971-972 | "the cache MUST NOT use the new response to update any stored responses" (13 words) |
| 4 | §4.3.4 weak "most recent" sentence | 976-977 | "then the most recent of those matching stored responses is identified for update" (13 words) |
| 5 | §4.3.4 no-validator sentence | 979-984 | "If the new response does not include any form of validator … then that stored response is identified for update" (19 words, elided parenthetical) |
| 6 | §3.1 Proxy-Authenticate sentence | 361-363 | "Effectively, this is limited to Proxy-Authenticate (Section 11.7.1 of [HTTP]), Proxy-Authentication-Info (Section 11.7.3 of [HTTP]), and Proxy-Authorization (Section 11.7.2 of [HTTP])." (21 words) |

Context, verified against the body:
- Q1 full sentence (375-377): "When doing so, the cache MUST add each header field in the provided / response to the stored response, replacing field values that are / already present, with the following exceptions:"
- Q3 full sentence (969-972): "…validators are identified for update.  If none of the initial set / contains at least one of the same strong validators, then the / cache MUST NOT use the new response to update any stored / responses." — this is bullet 1 of the §4.3.4 first-match filter; matches contract decision `must-not-update`.
- Q4 full sentence (973-977): "If the new response contains no strong validators but does contain / one or more "weak validators", and those validators correspond to / one of the initial set's stored responses, then the most recent of / those matching stored responses is identified for update." — supports LC2/LC3 (largest `received`; single most recent).
- Q5 full sentence (979-984): "If the new response does not include any form of validator (such / as where a client generates an If-Modified-Since request from a / source other than the Last-Modified response header field), and / there is only one stored response in the initial set, and that / stored response also lacks a validator, then that stored response / is identified for update." — supports the `no-validator` rule (sole response, itself validator-less).
- Q6 sits inside §3.1 bullet 4 (358-363), whose MUST NOT clause ("Header fields that are specific to the proxy … MUST NOT be stored, unless the cache incorporates the identity of the proxy into the cache key", lines 358-360) grounds the contract's proxy-authenticate / proxy-authentication-info / proxy-authorization update exclusions.
- §3.2 bullet 1 (379-380) says "Header fields excepted from storage in Section 3.1", tying §3.1's exclusions (Connection list, connection-specific fields, qualified no-cache/private args, proxy-specific fields) into every 304 update — the contract's update-exclusion chain.

quotes = 6/6 located and verified.

## 4. Errata touching §3.1, §3.2 or §4.3.4

Source: fetched errata search page (Presentation=Table view, default status filter; raw body retained).
Completeness basis: 4 `Errata-ID` occurrences in the body; status groups shown: Reported (2), Held for Document Update (1), Rejected (1); no Verified group appears. Full set for RFC 9111 = 4 errata.

| Errata-ID | Status | Type | Date reported | Section | Gist | Touches §3.1/§3.2/§4.3.4 |
|-----------|--------|------|---------------|---------|------|--------------------------|
| 9004 | Reported | Technical | 2026-06-11 | 3.5 | proxy-revalidate does not authorize shared-cache storage of authenticated responses; proposes clarifying note | no |
| 9185 | Reported | Technical | 2026-09-24 | 4.3.4 | proposes recasting the initial-set paragraph so a strong-ETag match can freshen a stored response across a selecting-header (Vary) mismatch, with re-keying text appended | **yes — §4.3.4** |
| 9166 | Held for Document Update | Technical | 2026-09-09 | 5.2.3 | Cache-Control extension text should not preclude other HTTP extensions modifying cache operation | no |
| 7695 | Rejected | Technical | 2023-11-07 | 4.3.2 | proposed If-Match/If-Unmodified-Since forwarding requirement; rejected 2024-01-16 by Francesca Palombini | no |

**errata-touching = 1** (EID 9185, §4.3.4). No erratum touches §3.1 or §3.2.

**EID 9185 status line, quoted from the fetched page:** `Status: Reported` (adjacent fields:
Errata-ID: 9185; Type: Technical; Reported By: Daniel Fox Franke; Date Reported: 2026-09-24).
Consistent with freeze.md ("EID 9185, Reported") and the S485 draft status.

Relevance guard (observation, no repair): EID 9185 proposes replacing the §4.3.4 initial-set paragraph;
fresh304-contract.md explicitly does not compute the initial set (caller-supplied `stored`), so the
erratum does not change the scored contract. Unverified status: not in force.

## 5. Registry row drafts

In `rows.md` (same directory), 11-column shape matching corpus/SOURCES.md
(id, source, kind, tier, scope, anchor, teaches, status, opened, recheck, used-by):
S484 (spec, tier A) and S485 (dataset, tier A), status `mined`, opened 2026-11-05,
recheck 365d / 90d, used-by corpus/knowledge/freshening-304.md, no literal `|` inside any cell.
Drafts only — L1 integrates.

## 6. Routed findings (reporter, not repaired)

- R1 (process, self-reported): my first GET pass omitted `curl -v`, so per-hop statuses of the three
  GETs were not captured. Reconstruction used labeled HEAD probes (§2). The GET-pass records
  (REDIRS, final URL, final code, bytes, sha256) are first-party; hop statuses are HEAD-derived.
- R2 (instruction conflict): the seat's `Report:` trailer names `.ufo/waves/round-99/w1/ScoutRfc9111.md`,
  but the hard bounds restrict writes to `w1/ScoutRfc9111/` and the seat spec item 4 names
  `w1/ScoutRfc9111/report.md` + `rows.md`. I followed the seat spec and bounds; the trailer-path file
  was not written. L1 should reconcile if it expects that exact filename.
- R3 (gap, instrument control): `controls/instrument-sha256.txt` covers counters/contract/frozen
  subjects but not the two retained source bodies; rfc9111.txt is pinned via the contract's inline
  digest, eid9185.html via nothing frozen. Digests supplied in §2; consider adding them if the
  freeze set is ever amended (not a repair I can make post-freeze).

## 7. Scratch hygiene

Tooling installed/updated: none. Host sysctls: untouched. Git/jj mutations in LANE or fleet repo: none
(read-only `rev-parse`, `sha256sum -c` only); no fixture commits were needed.
Scratch seat dir /fast/scratch/hyaku/kake-r99/ScoutRfc9111 (plus fetch logs and cleaned-text aids)
was deleted after copying the three bodies into this w1 directory; nothing else under
/fast/scratch/hyaku/kake-r99 was touched.

## 8. Verdict line

SCOUT rfc9111-sha=match eid9185=Reported errata-touching=1 quotes=6/6
