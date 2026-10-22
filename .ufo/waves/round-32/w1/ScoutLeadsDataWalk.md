# ScoutLeadsDataWalk — next freshness-claim ground (kake r32 w1)

Seat: KakeR32.ScoutLeadsDataWalk (scout, freshness). Read-only; no network request, no tool install.
Lane reading revision `7e05aa8` (`285abca` is its parent). Wrote only this report.
"Not on the citing-set gate" read as: the claim is verified by its own offline counter over committed
bytes (shape of `.ufo/waves/round-32/c2_retained_count.py`), not by `scripts/citing_set*.py` fixtures.
[INFERENCE: the round-27 citing-pair obligation still applies to a landed entry; that is review
input, not the claim's counter.]

Commands (exit 0): `grep -n "## Leads (unopened)" -A 80 corpus/SOURCES.md`; `grep -n "## Frontier"
-A 80 corpus/README.md`; `awk 'NR>=120&&NR<=139' corpus/SOURCES.md`; `grep -n "^## \|^### "` over
`corpus/QUALITY.md`, `PROVINCE.md`, `corpus/knowledge/publish-channels.md`; a python scan of
`~/Projects/*/.github/workflows/*.yml{,.yaml}` for `uses:` pins; `find ~/Projects -maxdepth 3
-regextype posix-extended -regex '.*/[0-9a-f]{32}\.txt'` (0 hits); `ls -lS`/`find -size +500k` over
`ds4cc-marketplace`, `stat`+`grep -c` on its `sitemap.xml`.

## Ranked (best first)

### 1. GitHub Actions workflow lockfiles, 2026-10-14 — SOURCES.md:124
Why best: newest dated platform change on the list (8 days), about the publish pipeline itself, and
it turns a frontier read that today needs operator authorization into an offline check.
README.md:106-108 names "each Pages repo's `build_type` and workflow action pins" as such a read;
the pin half is answerable from local workflow files. Measured now: 13 workflow files under
`~/Projects/*/.github/workflows`, 80 `uses:` entries, **0** SHA-pinned; Pages actions are mutable
tags — `burnerchrome/.github/workflows/pages.yml:59,62,66` (`configure-pages@v5`,
`upload-pages-artifact@v3`, `deploy-pages@v4`), `ds4cc-marketplace/.github/workflows/pages.yml:61,64,69`
(same), `kimi-code/.github/workflows/docs-deploy.yml:37,51` (`upload-pages-artifact@v5`,
`deploy-pages@v5`), and `ds4cc-marketplace/.github/workflows/validate.yml:27`
`dtolnay/rust-toolchain@stable` (branch-level).
Sharpest single claim: both Pages sites deploy with `upload-pages-artifact@v3`, whose bytes the
corpus says it does not hold — `corpus/knowledge/ghp-served-set.md:89` ("no v3.0.1 `action.yml`
bytes are retained") and `:94`; `corpus/knowledge/publish-channels.md:73` (c7) already names
`raw.githubusercontent.com/actions/upload-pages-artifact/v3/action.yml` as a surface. Resolve `v3`
to a commit today, retain the bytes, register a row, cite it: the UNVERIFIABLE drops.
Counter sketch: (a) retained blob id of that `action.yml` at the resolved commit, (b) SOURCES row
naming the commit, (c) entry citation, (d) pin census over named workflow files (tag vs SHA).
Risk: announcement prose — claim only what it states, and date it.

### 2. Google crawler file-size limits, moved February 2026 — SOURCES.md:133
Why: a dated platform change on crawl hygiene (`PROVINCE.md:21-23`) with a real local artefact
population to measure. Measured now: `ds4cc-marketplace` holds 6 HTML files of 1.98–2.03 MB
(`magga/grok47-high-on-cursor-cloud/games/{boxhead,cluck-horizon,chicken-invaders}/index.html` plus
the byte-near-identical `magga/zai-glm5.3-max-omp/...` set); its `sitemap.xml` is 97 `<loc>`,
7,614 bytes — far under the sitemaps.org 50,000-URL/50 MB limits already held in S012
(`corpus/knowledge/crawl-scope-per-host.md`), so any binding limit is the per-file one.
Counter sketch: quote the page's numbers, then compare named local files/sitemap against them.
Risk: the page states limits with qualifiers (fetch vs index); QUALITY round-31 F4 needs the
qualifier words inside the quoted sentence, and "2 MB page at a ceiling" is [INFERENCE] until read.

### 3. IndexNow protocol — SOURCES.md:137
Why: the only lead opening a publish verb the corpus lacks entirely. `publish-channels.md` sections
are GitHub Pages push (`:7`), Render (`:24`), Kimi surface (`:30`) plus corrections — no
search-engine notification channel; S012 covers only sitemap scope. Cheap and falsifiable offline:
an IndexNow key file is a 32-hex-named `.txt` at the host root; the scan above found **0** under
`~/Projects` at depth 3, and `ds4cc-marketplace` carries only `robots.txt`/`sitemap.xml`, so a claim
can state both the requirement and the measured absence. Counter: key-file presence per named root.
Risk: weakest freshness value of the three (no dated change); the site is protocol-community prose,
so tier B unless the page pins a spec. Host-root scope must be read with S011, not asserted.

## Next best, one line each
- Custom 404 page (SOURCES.md:123): cheapest GitHub-Docs item and offline-checkable (no `404.html`
  in `burnerchrome/` or `ds4cc-marketplace/` roots), but `ghp-subpath-spotcheck.md:62-63` already
  handles 404.html; its HTTPS half is settings/live and not checkable offline.
- Google canonicalization troubleshooting, July 2026 (SOURCES.md:134): best STALE-correction
  candidate, but canonical ground is heavily mined (S020/S021/S026/S027) and it is support-desk prose.
- WCAG 2.2 as ISO/IEC + SC 2.5.8 (SOURCES.md:130-132): accessibility is open, yet no local artefact
  to count, so the claim is read-only.
- Event Timing / Optimize INP / Chromium changelog (SOURCES.md:127-129): INP thresholds already land
  at `field-performance-cwv.md:3,11,22-28`; incremental only.

## Required in whichever claim is declared (r31 routed defects, still open)
- Truth sampling, not provenance only: `corpus/lessons/round-31-verifier-spotcheck.md:173-174`.
- Screen at least one non-primary candidate: same file `:179-180`.

## Not verified / unknown
- No lead URL was fetched by this seat (no network permission here): reachability, status and
  today's bytes of items 1-3 are unverified.
- The workflow census covers one host's checkouts at 2026-10-22 (`~/Projects/shokunin` excluded), not
  a fleet-wide or live statement; the DS4CC weights are repository files (no build was run).
