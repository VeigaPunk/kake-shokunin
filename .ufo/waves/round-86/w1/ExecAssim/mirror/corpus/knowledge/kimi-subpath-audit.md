source: own-work, no SOURCES.md S### row — kimi subpath baseline 2026-09-28 ~21:15Z: read-only GETs of same-origin links on 10 live kimi rows; ds4cc sitemap.xml parity (93 locs; sitemap commit f3d2ecd); git log --diff-filter=A miss classification; transient /tmp/kimi_audit.py + /tmp/kimi-subpath-audit.json (absent at round-21 audit)
verified-at: 2026-09-28 ~21:15Z baseline, sitemap source revision f3d2ecd — historical-not-live-reverified; no GET repeated this round
recheck: on kimi index, sitemap, or ds4cc source change — git -C ds4cc-marketplace show f3d2ecd:sitemap.xml | grep -c '<loc>https://ds4cc.com' (expect 93 per entry evidence); source vanished: ds4cc-marketplace checkout, kimi_audit.py and kimi-surface tooling absent at round-21 audit — operator must restore at f3d2ecd or retire this recheck; metadata contract S019

# kimi subpath audit — per-path freshness & link integrity

First baseline: 2026-09-28 ~21:15Z, read-only GETs, `/tmp/kimi-subpath-audit.json`
(transient artifact). Method + results below. Covers the README residual
"kimi subpaths (byte compare meaningless — needs per-path title+marker)".

## Why bytes are meaningless but paths aren't

`sync-check` proves identity+markers on the index only; kimi rewrites bytes
(sdk-seed.js ~+157B, cfemail, entities), so subpath comparison is status/title,
never digest. Enumerate candidate paths two ways:

1. **Live index link sweep** — same-origin `href`/`src` → GET each.
   Blind spot: JS-rendered link surfaces. veigapunk-page / ufo-fsd.kimi.page
   render PROPERTIES[] client-side (`${p.url}` literal appears in markup but
   resolves nowhere) — static sweep sees ~1 link, real rot (vault PQ-1 stale
   rows) needs rendered DOM or source inspection.
   Template-literal hrefs inside inline JS (`${esc(...)}`) are sweep noise —
   filter `[$`{]` before classifying.
2. **Canonical URL-list parity** — ds4cc.com's `sitemap.xml` (93 locs) is the
   "should-serve" set for ds4cc.kimi.page. Map `dir/` → `dir/index.html`
   (kimi serves no directory indexes — see mirror-pitfalls).

## Baseline results (2026-09-28)

### ds4cc-kimi-mirror — 93 canonical locs → 19 served, 74 missing

| Miss class | Count | Meaning |
|---|---|---|
| `git log --diff-filter=A` after 2026-08-29 | **74** | staleness, not rot |
| file added on/before 2026-08-29 | **0** | zero true rot |
| not in source | 0 | — |

Add-date decomposition: 63 files 09-23 (magga/ tree), 10 files 09-22
(burnerchrome/), 1 file 09-08 (omarchy-usage or omegag). Live index's own
embedded max date is 2026-08-21 → published build predates ~Aug-29, matching
the dedupe-report vintage. PQ-2 quantify: **the republish delta is 74
canonical paths** — every one of them post-dates the last publish. No
pre-publish file is missing. **Errata (round-9 review):** the source-side
sitemap commit `f3d2ecd` adds **75** `<url>` entries (18→93 locs); the true
republish delta is 75 paths — the live-GET count of 74 reflects the sweep
run, and the dedupe report's cited 477-line revenger diff has no on-disk
artifact. Prefer the in-repo number (75) when briefing the operator.

### `dir/` hrefs are live-dead on the mirror

ds4cc.kimi.page index links `omarchy-usage/`, `omegag/`, `speedrun/` — all
404 on kimi while `*/index.html` serves 200 (`speedrun/index.html` = 200,
11 153B). GHP serves the same links fine (`/dir` → 301 → `/dir/`). On kimi
this class is **permanent until a zip-time href rewrite or source fix** —
the mirror can't redirect its way out.

### Other live rows — link sweep clean

| Row | Same-origin links GET | Non-200 |
|---|---|---|
| burnerchrome-kimi | 15 | 0 |
| plazir27-kimi-page | 1 | 0 |
| plazir27runs-on | 6 | 0 |
| ufofsd-charter | 1 | 0 |
| plazir27runson | 6 | 0 |
| ufo-fsd-kimi-pro | 2 | 0 |
| veigapunk-page | 1 (`${p.url}` template) | 1 — noise, not rot |
| ufo-fsd.kimi.page (vault) | 1 (same) | 1 — noise |
| ufofsd | 0 | — |

Index embedded dates double as vintage evidence: plazir27.kimi.page max
2026-09-18 (its 09-18 scribe beat, vs canonical 09-28), plazir27runs-on max
2026-09-02, ufofsd-charter max 2026-09-05 — all confirmed stale-but-intact.

## Procedure (re-run recipe)

```bash
# link sweep (per live kimi row)
curl -sS <url> | extract same-origin href/src → GET each, record status
# canonical parity (ds4cc mirror)
grep -o '<loc>https://ds4cc.com[^<]*' ds4cc-marketplace/sitemap.xml |
  sed 's|ds4cc.com|ds4cc.kimi.page|; s|/$|/index.html|' → GET each
# vintage classification per miss
test -f <sourceDir>/<rel> && git -C <sourceDir> log --diff-filter=A -1 --format=%as -- <rel>
```

Classification table: `in_source && added ≤ publish-vintage` = ROT;
`added > vintage` = expected staleness; `!in_source` = not-ours/noise.
Publish vintage per row: max embedded DOM date, kimi-map chat updateTime of
the bound chat, keeper logs — never `fleet.config.json.updatedAt`.

## Live re-verification — round 23 (2026-10-21)

Read-only live checks; receipt `.ufo/waves/round-23/receipts/kimi-subpath-audit.json` (claim, surface, method, observation). A HOLD is an observation on 2026-10-21, not a guarantee. Where this section and earlier text disagree, this section is newer.

- [kimi-subpath-audit:c1] **STALE** — The live canonical sitemap currently has 93 entries and is the should-serve inventory for the Kimi mirror. Surface: `GET https://ds4cc.com/sitemap.xml`. Correction: As of 2026-10-21, the live ds4cc.com sitemap contains 96 <loc> entries and remains the should-serve inventory for ds4cc.kimi.page.
- [kimi-subpath-audit:c2] **STALE** — Parity of the canonical list reports 19 served and 74 missing Kimi paths. Surface: `GET https://ds4cc.com/sitemap.xml; GET all 96 mapped paths on https://ds4cc.kimi.page (trailing / mapped to index.html)`. Correction: As of 2026-10-21, the live sitemap has 96 canonical locations and the 96 directory-mapped Kimi GETs return 19 HTTP 200 and 77 HTTP 404.
- [kimi-subpath-audit:c3] **HOLD** — The index-linked omarchy-usage, omegag, and speedrun directory URLs fail on Kimi while their index.html paths serve. Surface: `GET https://ds4cc.kimi.page/{omarchy-usage,omegag,speedrun}{/,/index.html}`.
- [kimi-subpath-audit:c4] **HOLD** — The burnerchrome Kimi index has 15 same-origin link targets and zero non-200 targets. Surface: `GET https://burnerchrome.kimi.page/ and its 15 unique same-origin non-fragment href/src targets`.
- [kimi-subpath-audit:c5] **STALE** — The source-history pointer f3d2ecd is the sitemap change adding 75 URLs to the 18-entry list, reaching 93. Surface: `GET https://github.com/VeigaPunk/ds4cc-marketplace/commits/main/sitemap.xml; GET https://github.com/VeigaPunk/ds4cc-marketplace/commit/f3d2ecd; GET raw sitemap at 2b5fd57 and 0b1116766de2d9895a3673c88678049b4946cf3c`. Correction: As of 2026-10-21, the reachable sitemap history shows commit 0b1116766de2d9895a3673c88678049b4946cf3c adding 75 locations (parent 2b5fd57: 18; new tree: 93), while the cited f3d2ecd URL returns 404.
