# Falsify S007 — round-26 C1 freshness recheck (receipt HOLD)

Seat: KakeR26-2.FalsifyS007 (leaf member — no subagent dispatch). Milestone r26-recheck-falsify. Axis: **freshness**.
Target: `.ufo/waves/round-26/rechecks/S007.json` (verdict HOLD) + SOURCES row S007 (`corpus/SOURCES.md:15`).
Goal: try to show the receipt is WRONG — quote does not ground the row's `teaches`, anchor mislocated in the raw bytes, or a content/version change the receipt missed.

**Verdict: AGREE** — the receipt survives every falsification attempt I ran. Severity: **low** (three non-blocking observations, two of them inherited-by-design from the round's own method; **no correction to the receipt is warranted**, see “Non-blocking observations”).

---

## 1. What the row claims (the ground truth to attack)

`corpus/SOURCES.md:15` (byte-identical at base `97404de4` and at candidate `e28312b1`; `git diff 97404de4 e28312b1 -- corpus/SOURCES.md` touches only the appended round-26 search-log paragraph, +2 lines, no registry cell):

```
| S007 | GitHub REST API: GitHub Pages endpoints — https://docs.github.com/en/rest/pages/pages | docs | A | Pages API fields describing build mode and custom-domain state | Get a GitHub Pages site response schema and Update information about a GitHub Pages site body parameters; fetched 2026-10-19 | The Pages API exposes build_type, cname, and protected_domain_state as distinct fields | mined | 2026-10-19 | 90d | corpus/knowledge/ghp-custom-domain.md |
```

- teaches: *“The Pages API exposes build_type, cname, and protected_domain_state as distinct fields”*
- anchor: *“Get a GitHub Pages site response schema **and** Update information about a GitHub Pages site body parameters; fetched 2026-10-19”*

Receipt under attack (`.ufo/waves/round-26/rechecks/S007.json`; byte-identical to the w1 draft `w1/RowS007.md`, sha256 `32b8d1da243471cb9d307dd1d1281f9543bd8f6afa5e1c12d33aff9365817e38` at commit and in the worktree):

```json
{"id":"S007","verdict":"HOLD","fetchIndex":1,
 "quote":"build_type string The process by which the GitHub Pages site will be built.",
 "anchorObserved":"Update information about a GitHub Pages site -> Parameters for \"Update information about a GitHub Pages site\" -> Body parameters (text view line 1; the HTML-to-text view is one line)",
 "reason":"Living unpinned docs re-fetched 2026-10-21, status 200, sha256 4f4449ba…: build_type is still a body parameter with values legacy|workflow, cname is still defined in the Update body as string-or-null and appears in the Get 200 response example, and protected_domain_state still appears in that response example beside pending_domain_unverified_at; both named anchor sections persist under unchanged headings, so scope, anchor and teaches still hold.",
 "correction":null}
```

---

## 2. Attack 1 — Does the quote ground THIS row’s `teaches` (not page chrome, not a neighbouring clause)? → **NO DEFECT**

Retained raw bytes `fetched/S007-1.raw.gz` (gz container 38 354 B; decompressed **453 447 B**; decompressed sha256 `4f4449ba997276df8acfb9a04aad7dc31c8f95b263ef56c6c7a4aac892097ce0`).

**a) The quote is a real parameter row, not chrome.** In the visible DOM the Update endpoint’s body-parameter table row is at raw offset **255 064**:

```
<code class="text-bold f5">build_type</code> <span class="color-fg-muted pl-2 f5">string</span> </div>
<div class="pl-1 f5 pt-2"><div><p>The process by which the GitHub Pages site will be built.
<code>workflow</code> means that the site is built by a custom GitHub Actions workflow.
<code>legacy</code> means that the site is built by GitHub when changes are pushed to a specific branch.</p></div>
<div class="pt-2"><p><span>Can be one of<!-- -->:<!-- --> </span><span><code>legacy</code>,<!-- --> </span><span><code>workflow</code> …
```

This is the **Update** table: the section `<h2 id="update-information-about-a-github-pages-site">` is followed by the `<caption …>Body parameters</caption>` at raw **253 960** (the Create table’s caption is at **240 362**), and the row at 255 064 follows the Update caption. The quoted sentence ends at a real sentence boundary (“… will be built.”), so the quote is a complete clause, not a truncating prefix.

**b) The quote is endpoint-discriminating.** The page has *two* `build_type` body parameters. The Create one reads “The process **in which the Page** will be built” (raw 240 618); the Update one reads “The process **by which the GitHub Pages site** will be built” (raw 255 200). The receipt’s quote matches **only** the Update wording:

```
$ grep -c -F "build_type string The process by which the GitHub Pages site will be built." .ufo/waves/round-26/fetched/text/*.txt
.ufo/waves/round-26/fetched/text/S007-1.txt: 1
```
(the Create variant `build_type string The process in which the Page will be built.` is at text index 7495, i.e. a different string). So `anchorObserved` and `quote` agree on the same section — no neighbouring-clause slippage.

**c) All three taught fields are grounded, each at a checked location.**
- `build_type` — Update body parameter, values `legacy|workflow`: raw 255 064 ff. (“Can be one of: legacy, workflow”).
- `cname` — Update body parameter, `string or null`: raw **254 216** `<code class="text-bold f5">cname</code> <span …>string or null</span>` (inside the same Update table: caption 253 960 < 254 216 < 255 064), and in the **Get 200 response example** JSON at raw **235 345** `"cname": "developer.github.com"`.
- `protected_domain_state` — **Get 200 response example** JSON at raw **235 714** `"protected_domain_state": "verified"`, immediately after `"pending_domain_unverified_at": "2024-04-30T19:33:31Z"` (raw 235 636) — i.e. literally “beside pending_domain_unverified_at” as the receipt says. The example block opens at raw 235 022 (`<code>Status: 200</code>`) and the Create-201 example is the *second* occurrence (raw 249 143), so the receipt's “Get 200” attribution is the right one.
- The typed **response schema** (the row anchor's other half) carries all three as distinct properties: `cname` type `["string","null"]` (raw 369 853), `protected_domain_state` type `["string","null"]` enum `pending|verified|unverified|null` (raw 369 935), `build_type` type `["string","null"]` enum `["legacy","workflow",null]` (raw 370 449). The Get-200 `required` list is `["url","status","cname","custom_404","public"]` (raw 371 686).

**d) Cross-row specificity (the counter’s own rule).** The quote occurs in exactly one of the 31 retained text views; the fragment “The process by which the GitHub Pages site will be built” likewise occurs nowhere else. No twin quote among rows sharing a document group.

**e) Nothing in the page undercuts the teaches.** `normalize(text_of(raw))` contains **0** occurrences of “deprecat” (case-insensitive) — no deprecation or removal of `build_type` / `cname` / `protected_domain_state` anywhere in the document.

---

## 3. Attack 2 — Is the anchor observed correct in the raw bytes? → **NO DEFECT**

- Heading structure in the visible DOM (before the `<script id="__NEXT_DATA__">` payload at raw 367 746): `h1 title-h1 | Get a GitHub Pages site`, `h2 update-information-about-a-github-pages-site | Update information about a GitHub Pages site`, plus `Create` / `Delete` / builds / deployments. The Get section’s `Response schema` label and its 200 example are at text index 5802 ff.; the Update section’s `Parameters for "Update information about a GitHub Pages site"` is at text index 9926 and its `Body parameters` caption at 103 27, with the quote at **10 647** — inside that table. ✓
- Text-view fidelity: applying the committed extractor `.ufo/waves/round-26/source_text.py` to the retained raw bytes reproduces the committed text file exactly:
  `normalize(text_of(raw,'text/html')) == text_file.rstrip('\n')` → **True** (35 496 chars each). The retained text file is genuinely the view of the retained bytes, not a separately produced artifact. The receipt’s parenthetical “(text view line 1; the HTML-to-text view is one line)” is literally true: the file holds 1 newline (EOF) and 0 CR bytes.
- Word-bounded quote match under the counter’s own semantics (`measure.py:273-277`): `re.search(r'(?<!\w)'+re.escape(normalize(quote))+r'(?!\w)', text)` → match, count 1.
- Counter limits for the quote: 14 alphanumeric tokens (≥6 required), 13 whitespace words (≤25 required). ✓
- Fetch identity: `fetchIndex 1` is the only fetch for S007 in `population.json`; `fetched/manifest.json` row S007 index 1 records `status 200`, `finalUrl == url`, `bytes 453447`, `sha256 4f4449ba…`, `file S007-1.raw.gz`, `fetchedAt 2026-10-21T15:09:35.741177+00:00`; recomputing sha256 over the decompressed retained bytes gives the same `4f4449ba…` (the gz container hashes to `1179bd16…`, i.e. the manifest pins the *decompressed* body). ✓
- Receipt schema: keys are exactly `RECEIPT_KEYS = {id, verdict, fetchIndex, quote, anchorObserved, reason, correction}`; `verdict HOLD` ⇒ `correction: null` ✓.
- Downstream corpus attribution still holds against these bytes (`corpus/knowledge/ghp-custom-domain.md:25-27`): “`cname` is string-or-null and `build_type` is `legacy`, `workflow`, or null; the update endpoint accepts both fields” — cname type `["string","null"]` (369 853), build_type enum `["legacy","workflow",null]` (370 449), Update body `cname` (378 454) and `build_type` (379 031) both present. The r20 erratum at :52-58 (“the rendered page reads ‘cname string or null’”) is still exact: raw 254 216 renders `cname … string or null`, and “required” survives only inside the embedded schema lists (371 686 / 377 248). ✓

---

## 4. Attack 3 — Did content or version change in a way the receipt missed? → **NO DEFECT** (a byte-level test would have produced a FALSE STALE)

One plain public GET of the row URL this session (2026-10-21; `curl -sS -L --max-time 60`), decoded body **453 447 B** — identical length to the retained body:

```
live body sha256 (two consecutive GETs) : c013892cac789e1333257cb1f9717652bcdb7d9cbeb8255583d668a872867e64
retained body sha256                    : 4f4449ba997276df8acfb9a04aad7dc31c8f95b263ef56c6c7a4aac892097ce0   (differs)
```

The whole-body difference is **Next.js build churn only** — five diff regions, all build identifiers:

```
RAW : /_next/static/chunks/webpack-091b7f339815a268.js     LIVE : /_next/static/chunks/webpack-5e180f68666d859a.js
RAW : /_next/static/chunks/4480-c44ed77ff5c225dc.js        LIVE : /_next/static/chunks/4480-18dd60aa177d969c.js
RAW : /_next/static/chunks/2137-42872f32ebc7ccb0.js        LIVE : /_next/static/chunks/2137-5c2598d434944693.js
RAW : /_next/static/ndrfAHwVnt-w5Yffjl7If/_buildManifest.js LIVE : /_next/static/3ojI2I6G4IdChWRIRpj5c/_buildManifest.js
RAW : "buildId":"ndrfAHwVnt-w5Yffjl7If"                    LIVE : "buildId":"3ojI2I6G4IdChWRIRpj5c"
```

Decisive content checks against the live body:

| check | result |
|---|---|
| `normalize(text_of(live)) == normalize(text_of(retained))` (committed extractor) | **True** — 35 496 chars, byte-identical |
| visible DOM head, chunk names + `buildId` normalized | **equal** (367 114 B each) |
| `<script id="__NEXT_DATA__">` payload, `buildId` normalized | **equal** (85 657 B each) |
| Get-200 schema property set (live vs retained) | identical: `url, status, cname, protected_domain_state, pending_domain_unverified_at, custom_404, html_url, build_type, source, public, https_enforced, https_certificate` |
| occurrences of `build_type` / `protected_domain_state` / `pending_domain_unverified_at` / `cname` (live) | 6 / 6 / 6 / 36 — identical counts to the retained bytes |

So there is **no content change and no version change**: same API version banner (`API Version: 2026-03-10 (latest)`), same headings, same field set, same enum values, same descriptions. The receipt judged content and is right to; a byte-sha equality test on this URL is the wrong instrument and would have manufactured a false STALE.

---

## 5. Attack 4 — Does HOLD leave a stale claim behind? → **NO DEFECT**

- `grep -rn "S007" corpus/` → `corpus/SOURCES.md:15` (the registry row) and `corpus/knowledge/ghp-custom-domain.md:1` (source list), `:25` (the S007 bullet), `:52-58` (the r20 quote-format erratum), `:62` (the round-26 recheck block). Every S007-attributed statement in that entry is re-verified above and holds against the 2026-10-21 bytes.
- The appended round-26 block (`ghp-custom-domain.md:60-62`) states: “Rows S003, S005 and S007 were re-fetched by one public GET each … and judged HOLD at their anchors against the retained bytes; receipts `.ufo/waves/round-26/rechecks/S0NN.json`”. The three receipts exist and all say HOLD (`rechecks/S003.json`, `S005.json`, `S007.json`). ✓
- Statement ledger `.ufo/waves/round-26/statements.json` → S007 pair: `statements 20, seatStale 0, stale 0, seatUnverifiable 0`, report `w1/PairS007GhpCustomDomain.md`. The seat report additionally lists **1 statement as UNVERIFIABLE and not counted** (the L54-55 Markdown-representation statement, whose artifact is not retained) — consistent with the contract’s rule that UNVERIFIABLE is reported separately and never counted decided. The ledger’s `seatUnverifiable: 0` is the count of *adjudicated-unverifiable* entries; the seat report’s line 8 (“1 statement UNVERIFIABLE and not counted”) matches the JSON’s `stale: 0` and the 20 decided statements. **No S007 STALE marker is required** (the counter requires the `[r26-recheck S007 STALE]` tag only for STALE receipts) and none is present — consistent.
- Counter at candidate `e28312b1` (read-only run): `decided 32, hold 32, stale 0, unverifiable 0, statements 276, statementsStale 8, statementCorrections 8, findings []`, exit **0**. At base `97404de4`: `decided 0`, finding `receipts_absent`, exit **1**. The S007 row record is decided with no findings.

---

## 6. Non-blocking observations (no correction required)

- **N1 (completeness of `anchorObserved`, low).** The row anchor names **two** locations — “Get a GitHub Pages site response schema **and** Update information about a GitHub Pages site body parameters”. The receipt’s `anchorObserved` string names only the Update body-parameters half (where the quote sits); the Get half is evidenced only in the `reason` prose, and there it is grounded in the Get 200 response **example** (raw 235 345 / 235 714) rather than in the response **schema** the row names. Both renderings exist and are unchanged — the example shows the three fields as distinct keys, the typed schema shows them as distinct properties (369 853 / 369 935 / 370 449) — so the substance is unaffected and HOLD stands. Optional `anchorObserved` enrichment for future receipts: name the Get-200 schema location (or both halves) so a reader can resolve the row’s first anchor half from the receipt alone. **Not a falsification**: nothing in the receipt is false.
- **N2 (method observation, low).** The receipt’s `reason` cites the sha256 of the round-26 retained bytes (`4f4449ba…`), which is what the manifest pins; today’s live body hashes to `c013892c…`. The difference is exclusively Next.js build-ID/chunk-hash churn (proved in §4), so this URL is **not** byte-reproducible across requests. Any future freshness gate that compares a live sha256 against a pinned sha for `docs.github.com/en/rest/pages/pages` will report a false STALE; the content-level method used here is the correct one.
- **N3 (registry bookkeeping, low).** `corpus/SOURCES.md:15` still reads “fetched 2026-10-19” in the anchor cell although the row was re-fetched 2026-10-21. The contract allows status/recheck/used-by cell updates (logged) but does not require them, and the re-check *is* logged twice outside the cell: the round-26 search-log paragraph in `corpus/SOURCES.md` (“Re-fetched every recorded URL with one public GET … HOLD 32, STALE 0 … receipts `.ufo/waves/round-26/rechecks/S0NN.json`”) and the `## Round-26 source recheck` block in `corpus/knowledge/ghp-custom-domain.md:60-62` (naming S003, S005, S007 explicitly). The w1 seat flagged the same cell as superseded with “L1 **may** log the recheck in the allowed recheck cell” — discretionary, and the counter imposes no such requirement. Leaving the historical opening-read date in the anchor cell is not a false statement.

---

## 7. Residual risk / verification gaps

1. **No retained 2026-10-19 bytes for S007.** The round-26 fetch set contains only 2026-10-21 bytes, so change between the opening read (2026-10-19) and the recheck cannot be shown differentially. HOLD rests on today’s bytes supporting the row’s scope/teaches at the anchors, corroborated indirectly by the corpus entry’s 2026-10-19 quotes (all still matching), not on a byte-identity proof against the original read.
2. **The response-schema half of the anchor is invisible to the committed text view.** `source_text.py` skips `<script>`, and the typed schema lives in the `<script type="application/json">` payload (raw 367 746–453 381). Nullability, the `required` lists and the `protected_domain_state`/`build_type` enums are therefore observable only in raw bytes — any future recheck that greps only `fetched/text/*.txt` will miss them (the w1 seat recorded the same gap as its observation 1).
3. **Unpinned, unversioned, un-datable document.** The manifest carries `last-modified: null`, `etag: null`; the page shows only “API Version: 2026-03-10 (latest)”. Freshness can be asserted only at the observed instant (2026-10-21), never guaranteed forward; and the API version string itself is not pinned by the row.
4. **Not exercised (out of scope):** no browser rendering of the client-side “Response schema” tab (its content was read from the embedded payload instead); no live `api.github.com` call (the row forbids it — “No API call was made” is true of the retained artifact); no non-English locale of the page; no check of the `Create`/`Delete` endpoints’ behaviour.

---

## 8. Reproduction commands (read-only)

```
# quote + anchor in the committed text view
grep -c -F "build_type string The process by which the GitHub Pages site will be built." .ufo/waves/round-26/fetched/text/*.txt
grep -bo -F "build_type string The process by which the GitHub Pages site will be built." .ufo/waves/round-26/fetched/text/S007-1.txt

# raw-bytes locators (decompressed offsets)
gzip -dc .ufo/waves/round-26/fetched/S007-1.raw.gz | grep -bo -F 'The process by which the GitHub Pages site will be built'
gzip -dc .ufo/waves/round-26/fetched/S007-1.raw.gz | grep -bo -F '&quot;protected_domain_state&quot;: &quot;verified&quot;'
gzip -dc .ufo/waves/round-26/fetched/S007-1.raw.gz | grep -bo -F '<caption class="mt-3 mb-3 h5 float-left">Body parameters</caption>'

# extractor fidelity + live-vs-retained content equality
python3 - <<'PY'
import gzip,re,importlib.util
spec=importlib.util.spec_from_file_location('st','.ufo/waves/round-26/source_text.py')
st=importlib.util.module_from_spec(spec); spec.loader.exec_module(st)
raw=gzip.decompress(open('.ufo/waves/round-26/fetched/S007-1.raw.gz','rb').read())
tf=open('.ufo/waves/round-26/fetched/text/S007-1.txt',encoding='utf-8').read()
print(st.normalize(st.text_of(raw,'text/html'))==tf.rstrip('\n'))
PY
curl -sS -L --max-time 60 https://docs.github.com/en/rest/pages/pages | sha256sum

# counter, base vs candidate (read-only)
python3 -B .ufo/waves/round-26/measure.py --root . --revision 97404de4ff73d6c8a4f87385cf5fdf36dca7f006   # exit 1, decided 0
python3 -B .ufo/waves/round-26/measure.py --root . --revision e28312b14b076584fedd696fae2a684e460bd11e   # exit 0, decided 32
```

---

## 9. Bounds note (full disclosure)

No corpus file, script, fleet repo, sibling lane, lane Git index or jj state was mutated. **Only this report file was written in the lane.** Per the operator tooling directive, no package transaction was performed (host-wide pacman pause respected); `curl`, `python3`, `gzip`, `grep`, `sha256sum`, `git` were already present — **no tool was installed, upgraded or updated**.

Two scratch deviations to disclose: (i) I wrote the fetched live body to `/dev/shm/live-S007.html`, `/dev/shm/live2.html`, `/dev/shm/live3.html`, `/dev/shm/live4.html`, `/dev/shm/cur.html` as scratch rather than keeping it in memory — each was deleted immediately after use (`rm -f`), and no `/tmp` path was written; (ii) importing the committed `.ufo/waves/round-26/source_text.py` created `.ufo/waves/round-26/__pycache__/source_text.cpython-314.pyc`, which I deleted (`rm -f`). `.ufo/waves/round-26/__pycache__/measure.cpython-314.pyc` was already present from the wave’s own counter runs and was left untouched. `git status --porcelain` shows no tracked-file modification and no new path outside `.ufo/waves/round-26/w2/`.

```json
{"target":".ufo/waves/round-26/rechecks/S007.json","verdict":"AGREE","severity":"low"}
```
