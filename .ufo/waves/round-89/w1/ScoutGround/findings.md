# ScoutGround — round-89 wave-1 scoped findings

Seat: ScoutGround (recon + bounded planning data-walk). Lane root
`/home/vgpnk/Projects/shokunin/kake-shokunin` (LANE). Base revision
`76225160d0dff8d2042fbcd037bd08b0971d5e07`. Scratch:
`/fast/scratch/hyaku/kake-r89/ScoutGround/` (deleted after receipts were
copied here).

No production file was written by this seat. No commit, no push, no mutating
git or jj command. No subagent dispatch (lane bounds: leaf member).

Tools: no install or upgrade was needed. Everything ran on the host's
pre-existing `git` and `python3` 3.14 (`/usr/lib/python3.14`); no new tool was
added, so no channel/reason record is owed.

---

## 1. Existing cache-key / key-construction / Vary / request-header-selection material

Search scope, exactly as assigned: `corpus/`, `scripts/`, `SKILL.md`,
`PROVINCE.md`. Two regex families were run over each path:
`(?i)\bvary\b` and
`(?i)cache[-_ ]key|key[-_ ]construct|stored[-_ ]response|primary[-_ ]key|secondary[-_ ]key|key[-_ ]form`.

### 1a. The three named files

**`scripts/vary_match.py`** (294 lines) — round-88 C2 candidate, the *match*
half of RFC 9111 §4.1.

| line | hit |
|---|---|
| 2 | docstring: "Conservative Vary-match reader — round 88 C2 candidate (seat ExecReader)" |
| 5–6 | stdin contract `{vary, stored, presented}` — two header maps, not one |
| 7–10 | verdict map `match` / `mismatch` / `invalid_input:` |
| 13–25 | the three permitted transformations; `*` always fails; refusal conventions |
| 32–34 | **explicit scope fence**: "This reader performs no cache-key construction, storage, revalidation, freshness or serving behaviour" |
| 41–42 | `OWS = ' \t'`, `TCHAR` = RFC 9110 token set |
| 50–52 | `is_token()` — RFC 9110 token |
| 56–58 | `ascii_lower()` — ASCII-only A–Z lowering |
| 60–77 | `parse_vary()` — split on `,`, OWS-strip, `*` → star, token check, ASCII-lowercase, **dedupe** (not refuse) |
| 79–99 | `normalise_request()` — case-insensitive lookup map, case-variant duplicate refused, list values combined with `, ` |
| 101–131 | `decide()` — both-absent matches, one-sided absence mismatches, values compared byte-exact after OWS trim |

**`corpus/knowledge/vary-matching.md`** (323 lines) — round-88 knowledge entry
(S463, RFC 9111 §4.1).

| line | hit |
|---|---|
| 1 | source: S463, §4.1 *Calculating Cache Keys with the Vary Header Field*; retained body `.ufo/waves/round-88/w1/ScribeVary/rfc9111.html` (178573 B, sha256 `999f4013…`) |
| 4 | ground: freshness — round-88 C2 |
| 5 | scope: "**not** cache-key construction, storage, revalidation, freshness, serving or any browser behaviour" |
| 9–13 | the match half: two header maps (stored / presented) |
| 40–49 | the MUST NOT quote (24 words) |
| 95–99 | the wildcard sentence |
| 125–133 | the R1–R9 decision table |
| 137–141 | ASCII case-insensitive name comparison; duplicate members redundant (dedupe, not refuse) |
| 183–186 | R4/R5 checked before R6 |
| 223–248 | the runnable checklist (stdin JSON shape) |
| **262–264** | **"No cache-key claim.** Nothing here constructs, derives or compares a cache key. §4.1 paragraph 1 governs which stored response may be considered; the key itself is a separate construction." |
| 265–266 | "No storage claim." |

**`corpus/knowledge/cache-current-age.md`** (79 lines) — round-87 entry (S462).

| line | hit |
|---|---|
| 8 | scope excludes "header extraction, cache policy, storage/reuse authorization or browser" |
| 52 | "A computed age, including zero, does not prove freshness or reuse permission." |
| 53–54 | "RFC §4.2 also requires `freshness_lifetime > current_age`; §4 adds URI/method, **Vary**, directives, validation and other applicable reuse conditions." |

### 1b. Every other hit in scope (file:line)

`corpus/README.md`
- 666–669 — round-86 frontier: "General policy equivalence, the independent changed-row oracle, full HTTP extraction, **Age/Vary/Pragma**, browser/runtime cache behavior and live property repair remain frontier."
- 693–697 — round-87 supersession: "Date/Age header extraction, missing-Date support, **Vary/Pragma**, general policy equivalence … remain frontier."
- 701–713 — **"## Round-88 frontier step — Vary match semantics"** (heading at 701): the round-88 frontier row. 703–707 name `corpus/knowledge/vary-matching.md` (S463) and `scripts/vary_match.py`; 708–709 state it "does not claim **cache-key construction**, storage, revalidation, freshness, serving or browser behaviour"; 709–711 name the remaining frontier: "field-specific normalisation (the third permitted transformation the reader declines), the CR/LF/NUL rule, and a population the candidate cannot read"; 711–713 record the `mori-shokunin` S594 adjacency.

`corpus/SOURCES.md`
- 202 S455, 203 S456, 204 S457 — RFC 9111/9110 rows, scopes explicitly exclude cache-key construction.
- 209 S462 — RFC 9111 §4.2.3 age arithmetic; "not header extraction, storage/reuse or browser behavior".
- **210 S463** — "RFC 9111 — HTTP Caching, **Calculating Cache Keys with the Vary Header Field**" — the RFC section title itself is the key-construction section; scope cell reads "**not cache-key construction**, storage, revalidation or serving".

`corpus/knowledge/cache-control-effective.md` — 69–70: "No browser cache model; no **Vary**, Age calculation, Pragma, heuristic freshness, raw HTTP extraction, request/response cache interaction …"

`corpus/knowledge/header-change-classes.md`
- 11–13, 18–21, 39–48, 78–87 — RFC 9111 stored-response semantics (merge on update, validators).
- **92–96** — "`vary` is the instructive member: it does not describe bytes, but §4.1 makes it the field that selects a stored response for a request, so a moved `vary` changes the object-to-request mapping the capture is evidence about. It stays decisive."
- 118–129 — "the stored response is therefore not body plus a known list of headers".

`corpus/knowledge/vary-matching.md` — see 1a.

`corpus/knowledge/publish-queue.md` — 347–350: no publishing/deploy action taken.

`corpus/knowledge/hreflang-declaration.md` — 158–163: "No HTTP headers, no `Vary`."

`corpus/lessons/round-84.md` — 88–96: "§4.1 is *Calculating Cache Keys with the Vary Header Field*, and the sentence lists the normalisations under which two **request** header sets match … Flip: if the lane ever compares request-header values across captures — a `Vary`-key drift check — this sentence becomes the correct anchor for that new row, and the tool would then need a request-side grammar." (This is the lane's own pre-registered flip condition for a key-shaped tool.)

`corpus/lessons/round-83.md` — 158–161, 179–183: stored-response reuse preconditions; §4.2.3 scope fence.

`corpus/lessons/round-87.md` — 37–46: S462 registry row; "Frontier advances only supplied-time Age arithmetic; Date/Age extraction, **Vary/Pragma**, generic equivalence/changed-row oracle, runtime and publishing remain open."

`corpus/lessons/round-88.md` — 32–36 (Gate: admits RFC 9111 §4.1 and RFC 9110 §12.5.5; rejects the counter-pass proposition and the empty-`Vary` proposition), 44–46 ("Frontier advances only the supplied-header-map field-match half of §4.1; **cache-key construction**, storage, revalidation, freshness, serving and browser behaviour remain open"), 149–152, 258–259.

`corpus/lessons/round-88-verifier-spotcheck.md` — 113–150 (C2 evaluation), 181–187 (the §4.1 text anchors), 203–217 (the four Gate decisions), 255–259 (R88-B/R88-C routed).

`corpus/lessons/round-82.md` — 246–249: mori's `Vary` rule is *adjacency*, "not content drift".

`corpus/lessons/round-82-verifier-spotcheck.md` — 102–106: mori `Vary`/cache-selection adjacency, cited not absorbed.

`corpus/lessons/round-83-verifier-spotcheck.md` — 135–138: S456 anchor decisions.

`corpus/lessons/round-84-verifier-spotcheck.md` — 73–76: §4.1 "reordering field values when order is not significant" — "Request-key normalization does not prove arbitrary response policy equivalence."

`corpus/lessons/round-81-gate/rfc9110.txt` / `.html` — RFC 9110 §12.5.5 (Vary grammar at txt line 5675, html 9360–9373), §12.1.6, §12.2.4, §12.4.3, §4.2.3 ("a cache key might be compared as a simple string …", txt 1164–1167), §7.2 (txt 2441–2444), §12.5.5 ¶1 (txt 5699–5707: "**Vary expands the cache key** required to match a new request to the stored cache entry"), §8.8.1, §9.3.4–5, §13.1.2, §15.3.7.3.

`scripts/header_change_class.py` — 15–19, 51–53: `vary` sits in the `REPRESENTATION` class; 92–96 mirrors the knowledge entry.

`scripts/hreflang_audit.py` — 53–56: no `Vary`, no HTTP headers.

`scripts/capture_delta.py` — 15–18, 72–77, 114–117: `header_map()` — lower-cased name → values in wire order; the lane's only existing *header-map normalisation* helper.

`scripts/response_snapshot.py` — 121–181: the capture recorder (`fetch()`), which is what writes the `headers: [{name,value}]` shape consumed by `header_audit.py` and `capture_delta.py`.

`SKILL.md`
- 1597–1615 — **"## Round 88 — conservative Vary matching and the r87 defect queue"** (heading at 1597): the registry table (rows at 1607 `vary_match`, 1608 `c88 defect queue`, 1609 `c88 vary capability`), and 1611–1615 the note that only `scripts/cache_current_age.py`'s message changed. Line 1607's verdict cell states "a decision **is not a cache-key**, storage, revalidation or serving permission".
- 1577–1595 — round-87 registry block (`cache_current_age`, `c87 finite claims`).

`PROVINCE.md`
- 668–672 — round-82/83 classification ground, `vary` inside the `representation` class.
- 692–701 — **"## Round 87 — Age arithmetic only"** (heading at 692): "This advances only the Age-arithmetic slice: Date/Age header extraction, missing-Date handling, cache storage/reuse permission, **Vary/Pragma**, browser/runtime behavior and publication remain outside this capability."
- 20–37 — the `## Frontier` section (crawl hygiene, field performance, publisher response-header expectations) and `## Core` (10–18).
- 660–682 — round-83 header-change classification ground.

### 1c. Which ground the new C2 constructor *covers*, and which it *duplicates*

**Covers (new ground, not held anywhere in the lane):** the *construction* of the
stored-response key from (URI, `Vary` members, presented values). The lane holds
the **match** half only. Three independent pieces of lane text say so
explicitly and are the anchors this claim rests on:

- `corpus/knowledge/vary-matching.md:262–264` — "Nothing here constructs, derives or compares a cache key … the key itself is a separate construction."
- `corpus/knowledge/vary-matching.md:5` and `corpus/SOURCES.md:210` — scope cells ending "**not cache-key construction**".
- `corpus/lessons/round-88.md:44–46` — "cache-key construction, storage, revalidation, freshness, serving and browser behaviour remain open."
- `corpus/README.md:708–709` — same fence for the round-88 frontier row.

The `Vary` *grammar* and the *RFC 9111 §4.1* source are already held (S463,
RFC 9110 §12.5.5 at `corpus/lessons/round-81-gate/rfc9110.txt:5675`), so C2
**reuses the ground and adds the construction operation on top of it** — it is
an expansion of the same axis, not a second source claim.

**Duplicates (must not be re-claimed):**

| duplicated element | where it already lives | consequence for C2 |
|---|---|---|
| RFC 9110 `token` alphabet | `scripts/vary_match.py:41–52`; `scripts/c89_key.py` `TCHARS` | C2's name-validity rule is the *same* rule; it is a reuse, not a discovery |
| ASCII-only A–Z lowercasing | `scripts/vary_match.py:56–58` (`ascii_lower`) | same |
| OWS (SP/HTAB) edge trimming | `scripts/vary_match.py:41`, `:62`, `:126` | same |
| `Vary` split on `,` + member token check | `scripts/vary_match.py:60–77` | same |
| case-insensitive header-name lookup, case-variant duplicate refused | `scripts/vary_match.py:79–99` | same |
| `*` wildcard handling | `scripts/vary_match.py:67–68`, `:117–118`; `corpus/knowledge/vary-matching.md:95–99` | same *decision*, different *output* (C2 refuses `*`; the r88 reader returns `mismatch`) |
| the `invalid_input:` refusal convention | `scripts/vary_match.py:139`, `:274–276`; `corpus/knowledge/vary-matching.md:125–129` | same convention, different refusal list |
| the §4.1 source body | `corpus/knowledge/vary-matching.md:1` (sha256 `999f4013…`) | C2 must not re-fetch and re-claim S463 as a new source row; S464/S465 (already filed by L1) are the *new* rows for the construction ground |

**Two deliberate behavioural divergences from the r88 reader, both required by
the C2 contract and both worth naming in the lesson so the next reader does not
read them as contradictions:**

1. **Duplicate `Vary` member.** r88 *dedupes* (`scripts/vary_match.py:73–75`,
   `corpus/knowledge/vary-matching.md:137–138`, case 13 in its table). C2
   *refuses* (`c2-contract.md` §Refusals). Different outputs for the same
   input — a reader who runs both tools on `Vary: a, A` gets `match` from one
   and exit 1 from the other. That is the contract's call, not a contradiction.
2. **Empty `Vary` value.** r88 refuses it as `invalid_input:` (case 14);
   C2 treats `vary: ""` and absent `vary` as the same thing and emits the bare
   URI key (`c2-contract.md` §Input, worked example 2). Also a deliberate split.

**The `mori-shokunin` adjacency** (S594) is recorded in
`corpus/README.md:711–713` and `corpus/lessons/round-88.md` as a sibling note
to be *reported, not absorbed*. Round-88's own LOG entry
(`LOG.md:3019–3021`) records the same. C2 is the publisher-side key
*constructor*; it should be reported against mori's one-line §4.1 rule the same
way, not merged.

---

## 2. Base absence at `76225160`

Proven by `git cat-file -e` against the lane repo (read-only). Receipt copied
to `base-absence.txt` in this directory.

```
$ git -C /home/vgpnk/Projects/shokunin/kake-shokunin cat-file -e 76225160d0dff8d2042fbcd037bd08b0971d5e07:scripts/cache_key.py
fatal: path 'scripts/cache_key.py' exists on disk, but not in '76225160d0dff8d2042fbcd037bd08b0971d5e07'
exit=128

$ git -C /home/vgpnk/Projects/shokunin/kake-shokunin cat-file -e 76225160d0dff8d2042fbcd037bd08b0971d5e07:corpus/lessons/round-89.md
fatal: path 'corpus/lessons/round-89.md' does not exist in '76225160d0dff8d2042fbcd037bd08b0971d5e07'
exit=128
```

Both paths are **absent at base**. Neither is a rename or a deletion: neither
path exists in the base tree at all. This is consistent with the C1 base
receipt (`controls/base-c1.txt`, copied here as `base-c1.txt`), whose every
item fails with "round-89 lesson missing" / "no commit adds
`.ufo/waves/round-89/c89_key.py`".

---

## 3. Real recorded header data a domain trial could map to C2 inputs

C2's input is `{uri, request_headers, vary}`. A domain trial needs: a real URI,
a real `Vary` value from a real response, and real request-header values.

**Round-23 — no recorded response headers.** `round-23/live/*/fetch.json` (12
surfaces) carry the keys `bytes, contentType, error, fetchedAt, finalUrl,
method, redirects, sha256, status, truncated, url` and **no `headers` key**.
`round-23/live/*/manifest.json` carries only `pages[]` and `version` (a static
canonical-URL manifest, not a capture manifest). `round-23/live/*/audit.json`
carries `exit`, `result.findings`, `result.pagesChecked`, `result.verdict`. The
only header prose in round 23 is narrative, in
`round-23/receipts/drift-detection.json:39,42` (an observation string naming
`location` and `x-request-id` for `statics.kimi.ai`). **Round 23 therefore
contributes no C2-mappable header data.** The r26 lesson
(`corpus/lessons/round-26`/`round-26/w1/FetchCritic.md:51,105,120–122`) already
records the cause: "the fetcher sends no `Accept-Encoding` … `HEADERS` omits
`content-encoding` and `vary`, so the manifest cannot show which encoding was
served", with the fix listed as "Add `content-encoding` and `vary` to `HEADERS`"
— which `scripts/response_snapshot.py` now does.

**Round-61 — the primary C2-mappable corpus.** `round-61/capture/manifest.json`
is the capture manifest (`version: 1`, `checks[]` with `id`, `url`, `https`,
`expect`, and a `source` path per check). Twelve
`round-61/capture/<id>/response.json` files sit beside it, each with a
`headers` array of `{name, value}` objects (duplicates preserved, wire order),
`headerCount`, `url`, `finalUrl`, `method`, `status`, `contentType`, `bytes`,
`sha256`, `fetchedAt`, `userAgent`, `redirects`, `error`, `bodyFile`.

Every header key they hold, and the `Vary` value:

| file | header keys | `Vary` |
|---|---|---|
| `round-61/capture/burnerchrome-kimi/response.json` | Date, Content-Type, Transfer-Encoding, Connection, Server, **vary, vary**, x-internal-adhoc-canary, access-control-allow-headers, access-control-allow-methods, access-control-allow-origin, Cache-Control, x-content-type-options, strict-transport-security, cf-cache-status, CF-RAY | `Accept-Encoding` + `Origin` (two members) |
| `round-61/capture/charter-ghp/response.json` | Connection, Content-Length, Server, Content-Type, Last-Modified, Access-Control-Allow-Origin, Strict-Transport-Security, ETag, expires, Cache-Control, x-proxy-cache, X-GitHub-Request-Id, x-github-edge-region, Accept-Ranges, Date, Via, Age, X-Served-By, X-Cache, X-Cache-Hits, X-Timer, **Vary**, X-Fastly-Request-ID | `Accept-Encoding` |
| `round-61/capture/charter-kimi/response.json` | Date, Content-Type, Transfer-Encoding, Connection, Server, **vary, vary**, x-internal-adhoc-canary, access-control-allow-headers, access-control-allow-methods, access-control-allow-origin, strict-transport-security, cf-cache-status, CF-RAY (status 404) | `Accept-Encoding` + `Origin` |
| `round-61/capture/ds4cc-kimi/response.json` | Date, Content-Type, Transfer-Encoding, Connection, Server, **vary, vary**, x-internal-adhoc-canary, access-control-allow-headers, access-control-allow-methods, access-control-allow-origin, Cache-Control, x-content-type-options, strict-transport-security, cf-cache-status, CF-RAY | `Accept-Encoding` + `Origin` |
| `round-61/capture/ds4cc-primary/response.json` | Connection, Content-Length, Server, Content-Type, Last-Modified, Access-Control-Allow-Origin, ETag, expires, Cache-Control, x-proxy-cache, X-GitHub-Request-Id, x-github-edge-region, Accept-Ranges, Date, Via, Age, X-Served-By, X-Cache, X-Cache-Hits, X-Timer, **Vary**, X-Fastly-Request-ID | `Accept-Encoding` |
| `round-61/capture/lucario-ghp/response.json` | same 23-key shape as charter-ghp | `Accept-Encoding` |
| `round-61/capture/lucario-kimi/response.json` | Date, Content-Type, Transfer-Encoding, Connection, Server, **vary, vary**, … cf-cache-status, CF-RAY (status 404) | `Accept-Encoding` + `Origin` |
| `round-61/capture/plazir15-ghp/response.json` | same 23-key shape as charter-ghp | `Accept-Encoding` |
| `round-61/capture/plazir15-kimi/response.json` | Date, … **vary, vary**, … (status 404) | `Accept-Encoding` + `Origin` |
| `round-61/capture/plazir27-kimi/response.json` | Date, … **vary, vary**, … (status 404) | `Accept-Encoding` + `Origin` |
| `round-61/capture/ufo-fsd-kimi-pro/response.json` | Date, Content-Type, Transfer-Encoding, Connection, Server, access-control-expose-headers, Cache-Control, x-fc-request-id, x-proxy-by, strict-transport-security, cf-cache-status, CF-RAY | **no `Vary` at all** |
| `round-61/capture/vault-index-kimi/response.json` | Date, … **vary, vary**, … Cache-Control, x-content-type-options, strict-transport-security, cf-cache-status, CF-RAY | `Accept-Encoding` + `Origin` |

Full dump: `capture-header-inventory.txt` in this directory.

**Round-81 — the same shape, three surfaces.** `round-81/capture/manifest.json`
carries `version: 1`, `allowlist: ["ds4cc.com", "www.ds4cc.com"]` and three
`checks[]` (`ds4cc-primary` → `https://ds4cc.com/`, `ds4cc-robots` →
`https://ds4cc.com/robots.txt`, `ds4cc-sitemap` →
`https://ds4cc.com/sitemap.xml`), each with `expect` and a `source` path.
`round-81/capture/<id>/response.json` holds the header arrays:
`ds4cc-primary` and `ds4cc-robots` carry the 22-key GitHub-Pages shape;
`ds4cc-sitemap` carries the same plus `x-origin-cache` (23 keys). All three
carry `Vary: Accept-Encoding`.
`round-81/population/<id>/fetch.json` is **not** a capture manifest — it holds
only `{id, url}`.

**The round-88 trial capture is the best C2 input, because it is the only place
in the lane that recorded the *request* side too.**
`.ufo/waves/round-88/w1/ExecTrial/`:
- `capture.json` — `url: https://ds4cc.com/`, `method: GET`,
  `access_date_utc: 2026-11-04T18:52:27Z`, `http_status: 200`,
  `size_download: 78897`, `body_sha256: f2c5d2b3ab34e8e1…`,
  `vary_observed_verbatim: "Accept-Encoding"`,
  `vary_extraction` states the value is 15 bytes with no leading/trailing SP or
  HTAB, `credentials_or_cookies_sent: false`,
  `content_encoding_header_present: false`, and
  `selected_header_lines_verbatim` (16 lines).
- `response-headers.txt` — the raw `HTTP/2 200` response headers, `vary:
  Accept-Encoding` among them.
- `loopback-request.txt` — **the request header set**, captured on loopback with
  the same curl flags: `Host:`, `User-Agent:
  kake-r88-ExecTrial/1.0 (capability observation)`, `Accept: */*`, and the
  explicit consequence: "no Accept-Encoding field was sent … no Cookie,
  Authorization or other credential/cookie field was sent".
- `payload-identical.json`, `payload-perturbed.json`,
  `payload-probe-dupkey.json`, `payload-supplementary-ua.json` — four payloads
  already shaped for the r88 reader (`{vary, stored, presented}`).

**Mapping to C2's input shape.** From `loopback-request.txt` +
`response-headers.txt` a C2 trial payload is directly derivable:
`uri = "https://ds4cc.com/"`, `vary = "Accept-Encoding"`,
`request_headers = {"Host": "ds4cc.com", "User-Agent":
"kake-r88-ExecTrial/1.0 (capability observation)", "Accept": "*/*"}`. The
nominated field `accept-encoding` is **absent** from that request, so the
contract's absent-marker (`GS`) branch is the one exercised by the real
surface — that is the single most valuable trial case available, and it is
exactly the distinction the r88 reader cannot make (it only answers
match/mismatch). The kimi.page captures supply the **two-member** `Vary`
case (`Accept-Encoding, Origin`), which the frozen case set does not cover as a
*real* surface; and `ufo-fsd-kimi-pro` supplies the **no-`Vary`** case. All
three shapes are real, recorded, and currently unclaimed by any round-89
receipt.

**Caveat, stated honestly:** none of these captures records the request header
map. `round-61/capture/*/response.json` records `userAgent: "round61"` and
`method: "GET"` and nothing else about the request; the r61 fetcher's request
headers are therefore **not** recoverable from the capture files. The only
recorded request header set in the lane is round-88's `loopback-request.txt`.
Any r89 domain trial that needs a request map must either reuse that file or
record its own; it must not present `userAgent: "round61"` as a request header
map.

---

## 4. LANE files that will need a round-89 edit, with base anchor line numbers

All line numbers are at base `76225160`. Receipt:
`round-89-edit-anchors.txt` in this directory.

| # | file | base total lines | anchor | what round 89 needs |
|---|---|---|---|---|
| 1 | `SCORECARD.md` | 5504 | insert **after** line 5504 (the last line, "behaviour, revalidation and serving remain frontier. No round 89 is started here."). Nearest heading `### Planned — after round 88` at **5496** | a new `## Round 89 — …` section. The round-88 block is 5459–5504 (`## Round 88 — bounded committed measurements` at **5459**, `### Demonstrated repertoire — round 88` at **5490**, `### Planned — after round 88` at **5496**). Two C1 obligations land *inside* the existing round-88 block: line **5469** and line **5488** each still carry the stale `22/22` and must carry a `[r89-correction …]` tag (this is exactly C1 item A's `STALE='22/22'` / `TAG='[r89-correction'` test). A new `integrated-selftest: <n>/<n>` marker line must appear exactly once — `SCORECARD.md` currently has **zero** such markers (the `marker()` regex requires the line to *start* with `integrated-selftest:`). |
| 2 | `LOG.md` | 3027 | insert **after** line 3027 (last line: "overlap is reported rather than absorbed (`w1/ConnectorScope.md`)."). Nearest heading `## Round 88 — 2026-11-04, three routed r87 defects and a conservative Vary-match reader` at **2963** | a new `## Round 89 — 2026-11-04, …` entry |
| 3 | `SKILL.md` | 1615 | insert **after** line 1615 (last line: "behaviorally (exit, message, six-term arithmetic, selftest), not by prose."). Nearest heading `## Round 88 — conservative Vary matching and the r87 defect queue` at **1597** | a new `## Round 89 — …` registry section with a row for the new `cache_key` tool (the round-88 table shape is at 1605–1609) |
| 4 | `corpus/README.md` | 713 | insert **after** line 713 (last line: "adjacency, not absorbed."). Nearest heading `## Round-88 frontier step — Vary match semantics` at **701** | a new frontier/coverage row for the key-construction ground (the r88 row is 701–713) |
| 5 | `PROVINCE.md` | 701 | insert **after** line 701 (last line: "calibration metadata, not new province ground or domain knowledge."). Nearest heading `## Round 87 — Age arithmetic only` at **692** | a new ground section (the r87 one is 692–701). Note the file has **no** round-88 section, so r89's is the first round-88-or-later ground section there; PROVINCE's `## Frontier` list at 20–37 is the other place a frontier sentence may need to move |
| 6 | `corpus/lessons/round-89.md` | — | **absent at base** (proved in §2); **created during the wave** (commit `28532540`, markers added at `d9c972da`, wave-review sections at `a225647f`) | new file. C1 items B, C, D and F all read it: it needs `## Mistakes` with a table whose header columns include exactly `class`, `evidence`, `captured-by`, `fix`, `witness` (F_COLS) and ≥1 data row; a `gate-sample:` marker and an `r88-gate-summary-correction:` marker, both reading `admits=2 rejects=2` (see §5); an `r88-c-rerun:` marker reading `receipt=<path>` (that path must resolve) or `retracted`; a `controls-count:` marker of the form `<n>@<rev>` whose recount at `<rev>` equals `<n>`. At HEAD the four markers read `admits=2 rejects=2`, `admits=2 rejects=2`, `retracted`, `1604@21770586` (recount verified = 1604) |
| 7 | `corpus/lessons/round-88.md` | 327 | line **265** ("- Integrated tool selftests: `vary_match` 22/22, `cache_current_age` 61/61,") is the stale line item A targets; lines **329–336** already carry two `[r89-correction 2026-11-04]` blocks (appended, append-only) | item A requires line 265 to carry the `[r89-correction …]` tag or the stale `22/22` to go; item F requires a line containing **both** `[r89-correction` and `L1 mistakes` — line 329 already satisfies that half |

Additional integration touch points the counters imply but do not name
directly: `corpus/SOURCES.md` (S464/S465 rows — already added by L1 in
`fcb615c6`) and the new `corpus/knowledge/cache-key-construction.md` (already
added by L1 in `fcb615c6`).

---

## 5. Defects found — in the round's own counters, contract and case set

These are the counter-level findings this seat is asked to report. Each was
measured, not inferred.

### 5a. C2's counter has five uncovered contract rules (mutants survive to `met=true`)

The counter's own reference is correct on every case below (I re-derived each
against `.ufo/waves/round-89/c89_key.py`'s `key_of`, the committed candidate
`scripts/cache_key.py`, and `c2-contract.md`). The defect is in the **scored
population**: the frozen 16 cases, the 9 refusal items and the 200 seeded
properties do not discriminate five rules the contract states. I built
thirteen mutants of the shipped candidate and scored them with the counter's
own `score_candidate(source, work, SEED)`:

| mutant | contract clause broken | counter result | survives? |
|---|---|---|---|
| **M1** — drop the CR half of the CR/LF check | "a header value … contains CR or LF" must be refused | `frozen=16/16 props=200/200 refuse=9/9` → **met=true** | **survives** |
| **M2** — dedupe duplicate `Vary` members instead of refusing | "two `Vary` members are equal case-insensitively" must be refused | `frozen=16/16 props=200/200 refuse=9/9` → **met=true** | **survives** |
| **M4** — treat a missing `request_headers` as `{}` | "`request_headers` is missing or not an object" must be refused | `frozen=16/16 props=200/200 refuse=9/9` → **met=true** | **survives** |
| **M7** — do not escape the URI | §4: "In the URI, each name and each value, `%` becomes `%25` …" | `frozen=16/16 props=200/200 refuse=9/9` → **met=true** | **survives** |
| **M11** — do not escape the `Vary` member *name* | §4: escaping covers "each name" | `frozen=16/16 props=200/200 refuse=9/9` → **met=true** | **survives** |
| M3 — accept an empty header name | "a header name … is empty" must be refused | `frozen=15/16 refuse=8/9` → met=false | killed |
| M5 — no OWS trim on the value | §3 edge trim | `frozen=14/16 props=180/200` → met=false | killed |
| M6 — no sort of `Vary` names | §5 "the pairs sorted by the lowercased name" | `frozen=15/16 props=180/200` → met=false | killed |
| M8 — escape `%` last instead of first | §4 escaping order | `frozen=15/16` → met=false | killed |
| M9 — treat `*` as an ordinary token member | "`Vary` member is `*` … refused" | `frozen=15/16 refuse=8/9` → met=false | killed |
| M10 — case-fold header values | §3 "otherwise compared byte-exactly: no case folding" | `frozen=15/16 props=180/200` → met=false | killed |
| M12 — reverse-sort the `Vary` names | §5 sorted order | `frozen=13/16` → met=false | killed |
| **M13** — sort by the *raw* member text instead of the lowercased name | §1 "Members are compared case-insensitively and sorted"; §5 "sorted by the lowercased name" | `frozen=16/16 props=200/200 refuse=9/9` → **met=true** | **survives** |

Direct demonstrations of the survivors:

```
M1 on {"uri":"https://e.test/a","request_headers":{"a":"x\ry"},"vary":"a"}
  -> exit 0, stdout {"key": "https://e.test/a\x1fa\x1ex\ry"}
  contract: must refuse (CR is named explicitly)

M7 on {"uri":"https://e.test/50% x","request_headers":{"a":"1"},"vary":"a"}
  reference key : 'https://e.test/50%25 x\x1fa\x1e1'
  M7 candidate  : 'https://e.test/50% x\x1fa\x1e1'
  (M7 emits an unescaped '%' in the URI, and the two keys differ)

M11 on {"uri":"https://e.test/a","request_headers":{},"vary":"x%y"}
  reference key : 'https://e.test/a\x1fx%25y\x1e\x1c'
  M11 candidate  : {"key": "https://e.test/a\x1fx%y\x1e\x1c"}
  (M11 leaves the member name unescaped)

M13 on {"uri":"https://e.test/a","request_headers":{"aB":"1","Ac":"2"},"vary":"aB,Ac"}
  reference key : 'https://e.test/a\x1fab\x1e1\x1fac\x1e2'
  M13 candidate  : {"key": "https://e.test/a\x1fac\x1e2\x1fab\x1e1"}
  (M13 orders the pairs by the raw member text, so two distinct logical
   requests can land on different keys than the contract's order says)
```

**Cross-check with the peer seats.** ExecControls scored the same class of
mutants independently against the same counter
(`.ufo/waves/round-89/w1/ExecControls/scoring-receipt.txt`): `adv-cr-only`,
`adv-missing-headers`, `adv-no-dup-vary`, `adv-no-uri-escape`,
`adv-no-name-escape` and `adv-raw-sort` all reach `cand_met=true`. My M1, M4,
M2, M7, M11 and M13 are the same six gaps, re-derived independently from the
committed candidate. The two seats agree; the gaps are real and reproducible.
ConnectorScope reached the same root cause from the source side
(`.ufo/waves/round-89/w1/ConnectorScope.md:144`: "the frozen counter's
`REFUSALS` list … omits tests for duplicate Vary members and CR/LF values …
`_props` never generates URIs containing `%` or separators").

**Why each survives** (the precise gap, for a fix that is not a rewrite):

- **M1 (CR):** the only CR/LF case in the whole population is the frozen case
  `lf-value-refused`, whose value is `x\ny` (LF). No case anywhere carries a
  bare CR, and the seeded `VALS` list contains no control characters. `REFUSALS`
  has no CR item either. A candidate that checks only `\n` is indistinguishable.
- **M2 (duplicate `Vary` member):** the frozen set has `duplicate-header-name-refused`
  (case-variant duplicate in `request_headers`) but **no** duplicate-`Vary`-member
  case. `REFUSALS` has none. The seeded generator draws `names` by
  `rng.sample(NAMES, …)` — a sample without replacement — so a duplicate
  member is never generated either.
- **M4 (missing `request_headers`):** `REFUSALS` has `headers-not-object`
  (`request_headers: []`) but **not** `request_headers` absent. The contract
  lists "missing or not an object" as one bullet; only the second half is
  scored. (`uri-missing` is scored; the parallel `headers-missing` is not.)
- **M7 (URI escaping):** every frozen and generated URI is
  `https://e.test/` + one of `a, b, c/d, p?q=1, r#f` — **no `%` and no
  separator character ever appears in a URI**. The frozen case `percent-escaped`
  puts `%` in a *value*, and `separator-in-value-escaped` puts separators in a
  *value*. The contract's §4 sentence covers "the URI, each name and each
  value"; only the value half is exercised.
- **M11 (`Vary` member name escaping):** §4 says escaping covers "the URI, each
  name and each value". The `Vary` member name is the one component that is
  both a *name* and derived from the input, and it is never exercised: every
  frozen and generated member name is drawn from `NAMES`
  (`accept, accept-encoding, accept-language, x-probe, user-agent`) — all
  lowercase, all `%`-free, all separator-free. Only the *value* half of the
  name is escaped in a scored case, and no frozen case puts a `%` in a `Vary`
  member at all.
- **M13 (sort by the raw member text):** §1 and §5 both say the members are
  sorted by the **lowercased** name. The seeded generator emits `vary` as
  `', '.join(names)` where `names` is a sample of the already-lowercase `NAMES`
  list — so raw text and lowercased text coincide in every generated case, and
  the sort order is untestable from the population. A candidate that sorts the
  raw member text instead is indistinguishable, and produces a *different* key
  for `vary: "aB,Ac"` (raw order `Ac, aB`; lowercased order `ab, ac`).

**Severity.** This is the round-88 R88-1 shape recurring one axis later: R88-1
was "a table over the committed seed or an oracle-import stub passes C2". The
mitigation then was "the property population is generated at scoring time". But
a *generated* population is only as strong as the value and name alphabets it
draws from — `VALS` and `NAMES` are fixed lists that contain no CR, no
duplicate member, no `%`-bearing URI and no mixed-case member. M1/M2/M4/M7/M11/M13
are not tables or oracle imports; they are honest, plausible candidate
implementations that violate the contract and reach `met=true`. The counter's
own selftest only checks five mutants (`no-escape`, `no-trim`, `casefold-values`,
`no-sort`, `absent-equals-empty`) — none of which is M1, M2, M4, M7, M11 or M13.

**Recommended disclosure** (the counter is frozen and must not be repaired after
scoring): route these four as instrument limits in `corpus/lessons/round-89.md`
§Routed defects, naming each mutant, the contract clause it breaks, and the
population gap that lets it through. Do **not** add cases to the frozen set and
do **not** re-score.

### 5b. The freeze was amended after dispatch — a live R88-E recurrence

`git log` on the lane shows the C2 counter was amended **after** the wave was
dispatched:

```
08ab46a1  ct=1793826745  18:12:25  freeze — two claims, counters, contract, frozen cases, base controls
2e700b9a  ct=1793826784  18:13:04  wave-1 dispatch evidence (spec, validated payload, ready marker)
46a43e94  ct=1793826978  18:16:18  freeze v2 — shortcut guard no longer refuses a docstring …
f62e7954  ct=1793827181  18:19:41  evidence receipts
9784ad54  ct=1793827214  18:20:14  scripts/cache_key.py — C2 candidate
```

`46a43e94` is 194 seconds **after** the dispatch commit `2e700b9a` and 334
seconds after the freeze commit `08ab46a1`. It changed `.ufo/waves/round-89/c89_key.py`
(the `FORBIDDEN` tuple and the guard body) and re-derived
`.ufo/waves/round-89/controls/base-c2.txt`.

**This is R88-E again, in the same shape the round claims to close.** R88-E was:
"v3 `52e41d2d` landed at 15:58:05, six minutes after the 15:52:15 dispatch,
while the wave was live … it moved validation ahead of the wildcard rule and
flipped three seeded labels. … keep the freeze-then-dispatch order next
round." (`corpus/lessons/round-88-verifier-spotcheck.md:268–273`.)

The amendment was **substantively justified** — I measured it. Under the v1
guard the correct L1 candidate was falsely refused:

```
v1 guard(.ufo/waves/round-89/w1/L1/cache_key.py) = shortcut guard: source names '.ufo/waves'
   (that file names '.ufo/waves', 'round-89' and 'frozen' in its docstring)
v2 guard(same file)                                   = None
```

The v1 `FORBIDDEN` tuple was `('c89_key', '.ufo/waves', 'round-89', 'frozen',
'c2-cases', 'oracle')` — it matched any candidate whose *docstring* mentioned
the wave path, `round-89` or the word `frozen`. That is a real false positive
on a correct candidate (the freeze-v2 commit message says exactly this). The
v2 tuple `('c89_key', 'c89_defect_queue', 'c2-cases')` plus the `open(`/`.ufo`
line check is materially tighter against the actual shortcuts while no longer
refusing a docstring.

**But C1 item E does not catch it.** Item E measures `git log --diff-filter=A`
— the commit that *first adds* `c89_key.py` — against the commit that first
adds `w1.ready`, and compares committer times. Because `c89_key.py` was
*added* at `08ab46a1` (before dispatch), item E reads `[]` (passes) and is
blind to the later **amendment** at `46a43e94`. Item E's own selftest asserts
"E passes when the freeze commit precedes dispatch" and "E fails when dispatch
is committed first" — it has no case for *amend-after-dispatch*.

**Consequence for the claim.** C1's predicate is "the six defects … close,
re-derived from committed bytes by one counter". R88-E's substance — the frozen
instrument must not move after the wave is live — is **not** what item E
measures, and the round-89 instance of it actually happened, at 18:16:18, with
the wave live (the `w1/` seat directories are timestamped 18:13–18:15 and the
`ExecKey` candidate directory 18:15). This must be disclosed in the round-89
lesson; it is not a reason to withhold the claim, because the amended counter
is strictly better and its selftest is 43/43, but it is the honest reading.

**Recommended disclosure** (not a counter repair): in `corpus/lessons/round-89.md`,
record that the C2 counter was amended at `46a43e94` (194 s after dispatch),
that the amendment was a false-positive fix with a measured witness (v1 guard
refuses the correct L1 candidate, v2 guard does not), and that item E's
`--diff-filter=A` formulation cannot see an amendment. Name it as the round-89
instance of R88-E, and state that the amended bytes are the ones scored.

**Corroboration by the peer reviewer (independent).** `ReviewCounterC1` reached
the same conclusion from the counter's side, in the lane's committed
`corpus/lessons/round-89.md` §"Wave review — routed C1 counter defects"
(line 158 onward): **RC-2 (high) — "E ignores post-dispatch edits to the frozen
counter"**, and **RC-1 (high) — "E reads HEAD, not `--revision`"**. My
measurement (the `--diff-filter=A` first-add semantics and the 194-second
post-dispatch amendment at `46a43e94`) is the receipt for RC-2; the two seats
agree independently. The lesson's own verdict line already reflects it: "Verdicts
after the wave review: C1 unadmitted (item A open; B, C, D, F decided by prose
and not behaviour; E not revision-pinned)."

I also checked the counterpart claim: the v1 counter's own selftest is 43/43
against its own `controls/` (I ran it from a scratch copy with the `controls/`
directory present — the committed stub set — and it passed). So v1 was not
broken; it was over-broad. The amended counter is the one scored.

### 5c. `freeze.md` was not updated with the freeze-v2 amendment — *now partly routed*

`git show --stat 46a43e94` touches only `c89_key.py` and `controls/base-c2.txt`.
`freeze.md` is unchanged at `46a43e94` and still describes the v1 guard
("Committed shortcut stubs … are each rejected in that same receipt
(`controls=5/5`)"). The base receipt's own text changed under it: the
`ctl-table` line moved from `met=false (shortcut guard: source names
'.ufo/waves')` to `met=false (shortcut guard: source names 'c2-cases')`. The
freeze document is the round's statement of what was frozen before data; it now
understates what changed.

**Status at HEAD `acc69ba5`:** the *receipt* half of this is now routed — the
lane's committed `corpus/lessons/round-89.md:60` and `:227–229` record that
"`21770586` overwrote `controls/base-c2.txt` with the v2 re-run, so the
freeze-time bytes were lost from the working tree", and the freeze-time bytes
are restored as `controls/base-c2-freeze-v1.txt` (from `08ab46a1`) with the
v2 re-run kept and labelled. **The `freeze.md` half is still open**: the
freeze document itself is unchanged and does not name the v2 amendment. The
honest repair is a one-line erratum in the round-89 lesson (not a silent edit
of frozen bytes) — the lesson already names the amendment's substance, so only
the pointer to `freeze.md` is missing.

### 5d. A base receipt was truncated in the worktree and restored

`git status` during this seat's run showed
`M .ufo/waves/round-89/controls/c2-selftest.txt` with the file at 0 bytes,
against a committed 44-line version. The committed bytes are intact at
`08ab46a1`; a copy of the committed 43/43 receipt is in this directory as
`c2-selftest-v1-committed.txt`. By the end of the seat's run the file was
restored (2139 bytes, `selftest: 43/43 passed`, and still so at HEAD).
Recorded because a momentarily-empty committed receipt is exactly the R88-C
failure shape ("a claim with no committed receipt"), and the committed receipt
is the authority.

### 5e. Minor: the C1 counter's `## Round 88` window in `SCORECARD.md` has no closing `## ` heading

`item_a` scans the `## Round 88` section of `SCORECARD.md` and closes the
window at the next line starting with `## `. At base there is **no** such line
after 5459 (the file ends at 5504). So the window runs to EOF, and any
`22/22` a future round-89 section writes into `SCORECARD.md` would be caught by
the same stale-claim test. This is benign here (r89's section should not quote
`22/22`), but it means the r89 section must be appended **after** a `## `
heading of its own or the window will swallow it — and item A's STALE check
would then require a `[r89-correction …]` tag on any `22/22` inside it.
Worth knowing before editing.

### 5f. Minor: `item_a` requires a marker format the lane has never used

`marker()` matches `^integrated-selftest:[ \t]*(...)$` — the line must **start**
with `integrated-selftest:`. `SCORECARD.md` at base contains the string
`integrated-selftest` only inside prose (`controls/integrated-selftests.txt` at
lines 5469 and 5494), and the base receipt confirms the marker count is 0. The
value must equal the tool's own printed `selftest: N/N passed`, which for
`scripts/vary_match.py` is **35/35** (I ran the base-committed tool: exit 0,
`selftest: 35/35 passed`), *not* the `22/22` the current SCORECARD and lesson
claim. The correct marker value is therefore `35/35`. This is exactly R88-A,
and item A re-derives it behaviourally — the marker must state what the tool
prints.

### 5g. The `controls-count` marker is revision-pinned, and the count moves

`item_d` requires a `controls-count: <n>@<rev>` marker whose `<n>` equals a
recount at `<rev>`. I measured the recount with the counter's own method
(`git ls-tree -r --name-only <rev>` filtered on `/controls/`):

| revision | controls count |
|---|---|
| `76225160` (base) | **1590** |
| `08ab46a1` (freeze) | 1600 |
| `2e700b9a` (dispatch) | 1600 |
| `46a43e94` (freeze v2) | 1600 |
| `f62e7954` (evidence receipts) | 1602 |
| `21770586` / HEAD at this seat's last read | 1602+ (rising as this wave files controls) |

The count is **not stable across the wave** — every new `controls/` file moves
it. R88-D was exactly this: the "1,577 tracked files" number named no revision
("The count is exact at `f60a852a` (1577), but at filing HEAD `741fb728` it is
1590"). The marker must name a revision **and** a count that is true at that
revision, and the count must be re-derived after the last control file lands.
The base revision `76225160` → 1590 is the safest pin available now; any
later revision must be recounted at the moment of filing.

### 5h. C1 items B/C/F at base, and what the lesson must contain

I re-derived the `## Gate` table of `corpus/lessons/round-88.md` at base with
the counter's own parsing logic: **admits=2, rejects=2** (admits: RFC 9111
§4.1; RFC 9110 §12.5.5 — rejects: the counter-pass proposition; the
empty-`Vary` proposition). So the round-89 lesson's `gate-sample:` and
`r88-gate-summary-correction:` markers must both read `admits=2 rejects=2`.

Item C: the round-88 `controls/` paths named in `SCORECARD.md` and
`corpus/lessons/round-88.md` all resolve at base — I expanded the brace forms
and checked each with `git cat-file -e`:
`after-c1-carrier.txt`, `after-c2-carrier.txt`, `base-c1.txt`, `base-c2.txt`,
`integrated-trial.txt` — **all present** at `76225160`. So the R88-C failure
("Re-run at `edcb2980` with identical results" named no receipt) is now
repairable either by pointing at a real receipt (`receipt=<path>`) or by
`retracted`. Note the round-89 wave has already committed
`.ufo/waves/round-89/controls/r88-c1-rerun-at-55d67f15.txt`, whose content is
`C1v1 revision=55d67f15… items=3 open=0 closed=3 met=true` — a genuine
receipt for the r88 C1 re-run, and the natural `receipt=` target.

Item F: `F_COLS = ('class', 'evidence', 'captured-by', 'fix', 'witness')` and
the header row's joined text must contain all five column names, with ≥1 data
row; `corpus/lessons/round-88.md` must contain a line with **both**
`[r89-correction` and `L1 mistakes` — line 329 already does.

---

## 6. Planning data for the integrator (bounded; no production edit)

Facts, in the order an integrator needs them. **The lane moved while this seat
was working** — the numbers below are re-measured at HEAD `acc69ba5`
(2026-11-04 18:27:48 -0300), the state this seat last observed.

1. **C2's candidate is committed and scores green.** At HEAD `acc69ba5`,
   `python3 -B .ufo/waves/round-89/c89_key.py --root . --revision <HEAD>
   --candidate scripts/cache_key.py --work <explicit-scratch>` prints
   `C2v1 … frozen=16/16 props=200/200 refuse=9/9 controls=5/5 met=true`, exit 0.
   (Measured by this seat against the committed bytes.) The candidate is
   `scripts/cache_key.py` (committed at `9784ad54`).
2. **C1 is at open=1 closed=5 at the same revision.** The counter prints
   `items=6 open=1 closed=1 → now open=1 closed=5 met=false`, exit 1. Only
   **item A** is still open, and only on the stale `22/22` claims:
   `SCORECARD.md:5469`, `SCORECARD.md:5488` and
   `corpus/lessons/round-88.md:265` each still carry `22/22` without a
   `[r89-correction …]` tag. Items B, C, D, E and F now pass: the lesson
   `corpus/lessons/round-89.md` exists with the four markers
   (`gate-sample: admits=2 rejects=2`,
   `r88-gate-summary-correction: admits=2 rejects=2`,
   `r88-c-rerun: retracted`, `controls-count: 1604@2177058662d8778f1d1a685613f57deccb51ef01`),
   the `## Mistakes` table carries the five `F_COLS` columns, and
   `SCORECARD.md:5514` carries `integrated-selftest: 35/35`.
3. **The `controls-count` pin re-derives.** `git ls-tree -r --name-only
   2177058662d8778f1d1a685613f57deccb51ef01 | grep -c '/controls/'` = **1604**,
   matching the lesson's `1604@21770586`. Item D is closed on a pinned,
   re-derivable number.
4. **The three remaining item-A edits are additive tags.** Each of the three
   `22/22` lines needs `[r89-correction …]` on the same line (or the stale
   number removed). Per the lane's own rule — "correct the number in a new
   entry, never by rewriting filed bytes" (R88-A,
   `corpus/lessons/round-88-verifier-spotcheck.md:248–252`) — the honest form
   is to **append** a tagged correction and to tag the stale line itself, which
   is what the counter's `STALE`/`TAG` test accepts. The number to state is
   **35/35**, which is what `scripts/vary_match.py` prints (measured at base
   and at HEAD: exit 0, `selftest: 35/35 passed`).
5. **My §5a mutant findings are already corroborated by two peer seats** and
   are in the lane's own wave-review sections — `corpus/lessons/round-89.md`
   §"Wave review — C2 counter, contract and axis" (line 200 onward) records
   the URI-escape and whitespace mutants, the refusal-coverage gap and the
   reference-copy shortcuts; §"Wave review — routed C1 counter defects" (line
   158 onward) records RC-1 (E reads HEAD, not `--revision`) and RC-2 (E
   ignores post-dispatch edits to the frozen counter), which are **the same
   finding as my §5b**. My independent re-derivation confirms both.
6. **The lesson already reached the verdicts my §5b and §5a imply**: "Verdicts
   after the wave review: C1 unadmitted (item A open; B, C, D, F decided by
   prose and not behaviour; E not revision-pinned). C2 unadmitted (its target
   certifies the instrument's sample, not the declared capability; the axis is
   mislabelled)." The three remaining item-A edits are what stands between the
   current state and `met=true` for C1 — and per the same lesson's reasoning,
   closing item A does not by itself admit C1.

**Remaining items I did not cover** (stated so the integrator knows the
boundary): I did not re-derive the wave-review verdicts themselves, the
critic's axis-mislabelling claim, or the `mori-shokunin` S594 adjacency
analysis beyond naming the lane's own record of it.

---

## 7. Honest limits of this seat

- I did **not** score the C2 counter against the candidate myself as a verdict;
  §6.1 is the counter's own output, run read-only against committed bytes at
  a stated revision. The frozen counter's selftest (43/43) was run from a
  scratch copy with its `controls/` present.
- The four surviving mutants in §5a are my constructions, not the lane's. They
  are reproducible from `scripts/cache_key.py` by the single-line substitutions
  listed, scored with the counter's own `score_candidate`.
- **No live network request was made.** Every capture cited in §3 is read from
  committed bytes already in the lane; no URL was fetched, no credential or
  cookie was sent, no account state was touched.
- `round-23`'s absence of recorded headers is a statement about the *committed
  files*, not about what the r23 fetcher could have recorded. The cause is in
  the lane's own r26 lesson (`round-26/w1/FetchCritic.md:120–122`).
- I did not read the full body of `corpus/lessons/round-81-gate/rfc9110.txt`
  (44 KB) — only the `Vary`-relevant regions cited.
- The §4 anchor table gives the *insertion* point and the nearest heading for
  each file. It does not dictate section wording; the round's own conventions
  govern that.
- The count in §5g is the counter's method (`/controls/` in the path), which
  includes the round-89 wave's own controls. It will keep moving as this wave
  files more; the pin must be taken at filing time.
- I made no edit to `scripts/`, `corpus/`, `SKILL.md`, `PROVINCE.md`,
  `LOG.md` or `SCORECARD.md`. My only writes are this directory and
  `.ufo/waves/round-89/w1/ScoutGround.md`.
