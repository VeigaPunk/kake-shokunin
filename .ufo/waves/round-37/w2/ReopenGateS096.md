# ReopenGateS096 — S096 (google/robotstxt) re-opened live at current master

Seat KakeR37.ReopenGateS096, leaf, wave 2 (falsify). Item: re-open the S096 Gate line live; test the
knowledge entry's S096 claims (caller-side normalization; no unreserved decoding) against README and
robots.cc at current master. Sandbox `/fast/scratch/hyaku/kake-r37w2/ReopenGateS096/`; no sealed or
private tree read, no lane state touched, no tooling installed.

## Access (freshness axis)
- `timeout 120 curl -sSL -o live.html https://github.com/google/robotstxt` → exit 0, HTTP 200, 0
  redirects, 321357 B, body sha `4c158ffa24a1…`; a second GET gave body sha `f98c5a2f4b10…`
  (per-response chrome only).
- Visible text re-extracted with the lane's exact rule (`fetch_sources.py:36-41`, copied locally):
  sha256 `d17aa81d51ba5fa3e030f24697a95bc50b864545bd90ba9db5228008a8615574`, 8703 B, 1274 words;
  `live_text == retained S096.txt` → **True** (python exit 0). Retained `S096.html.gz` decompresses
  to body sha `fe4b5e3a0ec7…`, matching `sources/receipts.json`; `sha256sum fetch_sources.py` =
  `3677e42f14390c3c…0f08` = receipt `fetcherSha256`.
- `curl .../git/ref/heads/master` → exit 0, `refs/heads/master =
  22b355ff855419e6a3ff8ff09c0ad7fdb17116f9` (committer 2026-04-01). Raw files there, all HTTP 200 /
  exit 0: README.md 5282 B `3bc73ffbf6ba…1050`, robots.cc 24644 B `d05a7fa74c0e…d473`, robots.h
  11034 B `912f3a5c6821…0bd5` — identical to wave-1's cited hashes (`w1/ScoutReopenS096.md:74`)
  and to 50a0dace (`diff -q` exit 0 ×3), so seats citing 50a0dace are not stale.
→ **Freshness holds**: the page did not move and the code bytes are unchanged since round-37's fetch.

## Gate quote / section / row
- Quote “production code used by Googlebot” (README, About the library; 5 words) — **holds**:
  `README.md:20`, inside `## About the library` (`:7`); exact substring, 1 occurrence in retained
  text (`grep -oF | wc -l`). Full sentence at `README.md:19-20`: “…slightly modified (i.e. some
  internal headers and equivalent symbols) production code used by Googlebot”.
- Row sections “Google Robots.txt Parser and Matcher Library”, “About the library”, “Notes” —
  **hold**: `README.md:2`, `:7`, `:118`.
- Row teaches/scope (“modified production code used by Googlebot”; “not all crawler policy outside
  parsing and matching”) — **holds**: `README.md:19-20`, `:128-130`.
- Row retention clause — **overstated**: the row anchors only the *page* text. That text holds the
  README passages (once each) but **zero code bytes** — `MaybeEscapePattern` 0, `kHexDigits` 0,
  `NeedEscapeValueForKey` 0; `robots.cc`/`robots.h` occur 4× each only in the files table
  (`S096.txt` offsets 3109–3256). The entry's line-63 claims rest on the code, which no lane
  artifact retains — only wave-1 hashes plus this live re-fetch (hashes match at 22b355ff). Entry
  line 2 “S096 retained round-37 retrievals” therefore covers README, not the cited code.
- Gate method “quotes verified … with `grep -cF` (1 match each)” — result holds for S096, but
  `grep -c` counts lines and the retained text is one line, so it cannot detect duplicates;
  `grep -oF | wc -l` still gives 1. Evidence note, not a wrong claim.

## Entry claims (corpus/knowledge/robots-txt-rules.md)
1. Line 63 “decodes no unreserved escape” — **holds**. Only `%` handling in robots.cc is
   `MaybeEscapePattern` (`robots.cc:167-212`): scan `:174-185`, rewrite `:194-206`; an existing
   `%XX` is copied with hex uppercased (`:196-199`; `kHexDigits` `:120`). No decode table or
   helper, none in `GetPathParamsQuery` (`:96-153`), and `Matches` is byte-exact (`:95-115`).
2. Line 63 “(it only uppercases hex)” — **overstated/partial**. It also percent-escapes raw
   high-bit bytes (`robots.cc:200-205`), and escaping covers only allow/disallow
   (`NeedEscapeValueForKey`, `:284-292`; user-agent and sitemap return false). No decoding
   consequence; the “only” is wrong as written.
3. Line 63 “leaves path normalization to the caller” — **holds**: `README.md:123-126` “this
   library will not perform full normalization of those URI parameters”; `robots.cc:539-541` “The
   url is not normalized (escaped, percent encoded) here…”; `robots.h:153`, `:159` “'url' must be
   %-encoded according to RFC3986”. Minor: the entry hangs this on “ScoutReopenS096 K1”, which is
   the decoding finding; caller-normalization is the report's “Gaps” item (`w1/…S096.md:69-70`).
4. Line 73 “local single-URL/user-agent command”; URIs must follow RFC 3986; no full URI
   normalization (Quickstart, Notes) — **holds**: `README.md:32-33`, `:26`, `:118`, `:123-126`.
5. Line 81 “S096 explicitly excludes crawler implementation logic outside parsing and matching”
   (Notes) — **holds**: `README.md:128-130`.
6. Gate summary “settles how a production parser treats BOM, rule priority and normalization”
   (`corpus/lessons/round-37.md:50-53`) — **overstated for “normalization”**: S096 settles
   *pattern* canonicalization and expressly declines URL normalization (`README.md:123-126`,
   `robots.cc:539-541`). The entry gets this right; the lesson sentence is looser.

## Verdicts
- Page/code freshness: **holds**. Gate quote/section/row content: **holds**.
- Row retention of code evidence: **overstated** (page text only, no code bytes).
- Entry “no unreserved decoding”: **holds**; “only uppercases hex”: **overstated**;
  “normalization left to caller”: **holds**; lesson “normalization”: **overstated**, no executable
  difference.

## Not run / limits
No C++ build or execution (code-reading plus live bytes at 22b355ff); no C1 counter, no sealed tree,
no sibling files; network only to the S096 URLs. No processes left running.
