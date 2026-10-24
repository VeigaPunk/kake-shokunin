# SourceOpenS006 — S006 live reopen (r27, freshness)

Seat: KakeR27.SourceOpenS006 (leaf, read-only). Base 83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba; declarations be375d90afc6fc7aca369ab3cf5247bf460aeed2. Only lane write: this report. No corpus/index/git/fleet mutation, no subagents.

## Verdict

- Row `corpus/SOURCES.md:14` (S006) carries exactly **one** public URL. Reopened **live** once at 2026-10-21T20:02:19Z: HTTP 200, 138,096 bytes, sha256 `8b026e93…68da`. Body content is identical to the r27 retained fetch (19:59:56Z) and the r26 retained fetch (15:09:35Z); the three raw digests differ only in Next.js `buildId`/`_next` chunk names. **Teaching HOLD.**
- Inference at `corpus/knowledge/static-canonical-preflight.md:52-54` (seat cites `:53-54`): S006 is an **indirect contribution**, not direct support and not contradiction. It shows the built site is a configuration-filtered subset of the checkout on the Jekyll branch path; it says nothing about Actions artifacts, a deployable HTML tree, or canonical manifests. The preflight sentence cites S001–S006 plus `ghp-served-set.md` as a group; this row alone does not entail it.
- S006 citing set unchanged: 4 pairs at base, 2 decided in r26, 2 open for r27. No discovered pair found.

## Live reopen evidence

- Exact command (one GET, no recursion, no mirrors):
  `curl -sS --max-time 90 -o live-S006-1.html -D live-S006-1.headers -w 'http_code=%{http_code} size=%{size_download} url_effective=%{url_effective} time=%{time_total}' -H 'User-Agent: kake-r27-freshness-check/1 (+one public GET)' https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll`
- Access window 2026-10-21T20:02:19.103Z → 20:02:19.125Z UTC (`date -u` before/after). `http_code=200`, `size_download=138096`, `url_effective` = the SOURCES URL (no redirect), `time_total=0.017458`.
- Response headers: `content-type: text/html; charset=utf-8`, `content-length: 138096`, `date: Wed, 21 Oct 2026 20:02:19 GMT`, `cache-control: public, max-age=60`, `age: 11630`, `x-cache: MISS, HIT`, `via: 1.1 varnish, 1.1 varnish`, `x-github-edge-region: iad`, `x-github-request-id: A91C:285EAC:1F8E993:230A894:6AD8ECDC`. No `etag`, no `last-modified`.
- Live raw sha256: `8b026e939d9ca4af7dbd52d7c8b765015f388886457ff5f477b73f02a89668da` (138,096 bytes).
- r27 retained (`fetched/manifest.json`, row S006 index 1): `fetchedAt 2026-10-21T19:59:56.112484+00:00`, 138,096 bytes, sha256 `f0318abe7e63ecded4e7294484bd8cb68721e920b46d0b85399acb2a187742b6`; `gunzip -c fetched/S006-1.raw.gz | sha256sum` reproduces that digest and byte count.
- r26 retained: `fetchedAt 2026-10-21T15:09:35.317006+00:00`, 138,096 bytes, sha256 `71a698604486380c05ca092adbc863dc653fc175eecea5a675891651cd3bdfbd`.
- Byte diff live vs r27: 90 bytes in 10 runs; every run lies inside `/_next/static/...` asset URLs or `"buildId":"..."`. r26 vs r27: 105 bytes, 10 runs, same context. Examples: `webpack-89a39c7f16baf9b8.js`→`webpack-b9cf62b415b3e197.js`; `2137-9829586ffe393b57.js`→`2137-5c2598d434944693.js`; `"buildId":"tKruMSpttzVE7ytzANYAL`→`"buildId":"AZNqItOm5dutcdHoWp04P`.
- Content-normalized HTML (every `/_next/static/...` URL and every `"buildId"` value replaced): sha256 `60d33f739c389a62a92b07b10934f139ca96ce76d9e20b42d43ba68ca55dea4d` for live, r27 and r26 — identical.
- Visible text (scripts/styles stripped, tags removed, entities decoded, whitespace collapsed; 7,690 chars): sha256 `5e79c92c2df7d1c337106580c6039e73af9b3fc821e5b8a7aa05b5b47ebdae4d` for live, r27 and r26 — identical.
- r27 text view `fetched/text/S006-1.txt`: 7,677 bytes, sha256 `2d953b39b80cab8f7a51496dbbc627882d5b2451faa0567e0a1008e1bb5aa1f8`. Reading: documentation content has not changed across three retrievals spanning 4 h 53 min (15:09Z → 20:02Z); raw-byte identity is unstable on this host because the Next.js build rotates buildId/chunk names while the served content stays fixed.

## Quote (≤25 words) and anchor

- Quote (18 words; exactly one occurrence in live visible text, in r27 visible text and in the r27 text view):
  > By default, Jekyll doesn't build files or folders that: Are located in a folder called /node_modules or /vendor
- Anchor: H2 `Configuring Jekyll in your GitHub Pages site` (one raw occurrence of `id="configuring-jekyll-in-your-github-pages-site"`), immediately below the locked-settings code block. The quote joins that `<p>` lead-in and `<ul>` list item 1 with one space, as the r27 text view flattens them. Raw HTML: `<p>By default, Jekyll doesn&#x27;t build files or folders that:</p><ul><li>Are located in a folder called <code>/node_modules</code> or <code>/vendor</code></li>`.
- Code-line context (not the adjudicated quote): the same code block contains `source: [your repo's top level directory]` in raw HTML. The page names the repo top level as the build *input*, and the list names input entries the build *skips*. The text view renders that line as `[ your repo's top level directory ]` (extraction inserts spaces), so it is a poor verbatim ledger quote.

## Teaching check (row S006)

`SOURCES.md:14` teaches: "By default Jekyll skips paths starting with underscore, dot, or hash, paths ending in tilde, node_modules, and vendor." Live list, all items present: (1) `Are located in a folder called /node_modules or /vendor`; (2) `Start with _,., or #`; (3) `End with ~`; (4) `Are excluded by the exclude setting in your configuration file`, with "If you want Jekyll to process any of these files, you can use the include setting in your configuration file."

Verdict: **HOLD** at the row's own scope (default file exclusions in GitHub Pages Jekyll branch builds). No wording change vs the r26 receipt, anchor unmoved, and the page still exposes no version/last-updated field. No registry edit made or needed; the 90-day recheck cell is unaffected.

## Inference test — `static-canonical-preflight.md:52-54`

Text under test: "Prepare the manifest over actual built/deployable HTML when that artifact exists, not over an assumed checkout served set (S001–S006, `ghp-served-set.md`)."

**Classification: INDIRECT CONTRIBUTION.** Read at two levels: the quote is direct evidence for the row-scope statement "a Jekyll branch build does not serve the checkout tree", and indirect evidence for the preflight instruction, which concerns a manifest over a captured/deployable artifact. What S006 supplies is a concrete set difference between checkout tree and built site: defaults exclude `/node_modules` and `/vendor` folders, names starting `_`, `.` or `#`, names ending `~`, plus the configured `exclude` list, and `include` can re-admit any of them. Built-set membership is therefore a build-configuration decision, not a checkout property. That is the premise behind "not over an assumed checkout served set": a list enumerated from the checkout can name inputs that never become deployable HTML.

Why the preflight instruction is not directly supported:
- Scope: the page documents Jekyll branch builds. Its own note now says "GitHub Actions is now the recommended approach for deploying and automating GitHub Pages sites"; the corpus already scopes this ("not every workflow uses that build path", `ghp-served-set.md:30-33`).
- The live text never mentions Actions artifacts, upload steps, a deployable HTML tree, `_site`, `.nojekyll`, or canonical manifests (all absent). It does not show pages that exist only in output, and does not say a captured artifact equals the served set.
- The preflight sentence is a grouped citation (S001–S006 + `ghp-served-set.md`); the Actions-side mechanism is S001/S004 scope, not reopened here. S006 is one leg of that synthesis and is not presented as entailing it.

No contradiction: nothing in S006 says the checkout itself is served, and nothing says a manifest must be enumerated from source files.

## Citing pairs (denominator unchanged)

Mechanical enumeration at base 83528f7 (literals + ranges, population S001–S034) finds S006 cited in 4 knowledge files:
- `ghp-served-set.md` — literals `:1`, `:30`, `:83`. r26-decided (6 statements HOLD, `round-26/w1/PairS006GhpServedSet.md`).
- `sitemap-orphan-audit.md` — literals `:1`, `:2`, `:122`, `:124`, `:149`; range `S001-S006` at `:2`. r26-decided (2 statements HOLD).
- `publish-channels.md` — metadata range `S001-S007` at `:2` only. Open; the C2 oracle expects this pair.
- `static-canonical-preflight.md` — literal `:54` and range `S001–S006` at `:54`. Open; the C2 oracle expects this pair.

No additional S006 citing form was found. `discovered-pairs.json` and `pairs.json` were absent when read (20:00–20:03Z), so there is nothing to append; the row's pair denominator stays 4.

Scope note for the open `publish-channels.md` pair: that file's body r20 corrections cite S001, S002, S003, S005 and S007 (lines 58-61); S006 reaches it only through the `verified-at` header range `S001-S007`. The pair adjudication should target that metadata statement ("S001–S007 opened 2026-10-19"), not a body claim about Jekyll defaults. This reopen supports the row's continued validity but cannot verify the 2026-10-19 opening event.

## Uncertainties and flags

- U1 Cache provenance: the live response was a CDN cache hit (`x-cache: MISS, HIT`, `age: 11630`, entry ≈16:48Z); I observed retrieval, not origin regeneration. Agreement across 15:09Z/19:59Z/20:02Z makes an origin content change very unlikely, not impossible.
- U2 Raw sha is not a stable page identity here: three fetches, three digests, identical 138,096-byte content modulo Next.js build IDs. The r27 manifest sha pins bytes, not content; freshness comparisons on this host should use the normalized-HTML or visible-text digest.
- U3 The r26 receipt `rechecks/S006.json` carries no hashes, but `round-26/w1/PairS006GhpServedSet.md` records text-view sha `847e8190…9063` / 7,676 bytes, while the retained r26 text view is now `2d953b39…aa1f8` / 7,677 bytes and byte-identical to the r27 text view. Cause unresolved (later regeneration vs receipt error); neither hash was used for my verdict.
- U4 The text view flattens the `<ul>` and pads brackets inside code spans; the chosen quote is verbatim in raw HTML and in the text view, the code-block line is not.
- U5 No JavaScript was executed; this docs page server-renders its body and the three fetched bodies agree, so no client-only content is relied on.
- U6 Policy: one public documentation GET, no accounts/auth/cookies/private URLs, no property/browser/publication action, no broad download (single 138,096-byte document). No tool installs or upgrades; no pacman transaction.

## Checks run

- `curl` one GET; `sha256sum`; `gunzip -c | sha256sum`; `python3 -B` stdlib (gzip, hashlib, re, html) for normalization, byte-diff runs and quote containment.
- Quote containment checked three ways (live visible text, r27 visible text, r27 text view): 1 occurrence each; 18 words ≤ 25.
- Scratch: `/fast/scratch/hyaku/kake-r27/SourceOpenS006/` (`live-S006-1.html`, `live-S006-1.headers` only). This report is the only file written inside the repo.
- No build/lint/test/formatter run (writer-only wave rule; this seat is read-only).

```json
{"row":"S006","urls":1,"live":{"at":"2026-10-21T20:02:19Z","status":200,"bytes":138096,"sha256":"8b026e939d9ca4af7dbd52d7c8b765015f388886457ff5f477b73f02a89668da"},"r27":{"fetchedAt":"2026-10-21T19:59:56Z","sha256":"f0318abe7e63ecded4e7294484bd8cb68721e920b46d0b85399acb2a187742b6"},"contentNormalizedSha256":"60d33f739c389a62a92b07b10934f139ca96ce76d9e20b42d43ba68ca55dea4d","visibleTextSha256":"5e79c92c2df7d1c337106580c6039e73af9b3fc821e5b8a7aa05b5b47ebdae4d","teaching":"HOLD","inference":{"file":"corpus/knowledge/static-canonical-preflight.md","lines":"52-54","class":"indirect-contribution"},"pairs":{"known":4,"new":0}}
```

Report: .ufo/waves/round-27/w1/SourceOpenS006.md
