# Pair S013 × crawl-scope-per-host — round-26 freshness re-check

- Entry: `corpus/knowledge/crawl-scope-per-host.md` (53 lines; not edited)
- Source: S013, Google Search Central "Build and submit a sitemap", `corpus/SOURCES.md:21`
- Retained bytes: fetchIndex 1 (`fetched/manifest.json`, row S013). HTTP 200; `url` = `finalUrl` = `https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap`; fetchedAt 2026-10-21T15:10:40Z; Last-Modified Wed, 08 Jul 2026 15:47:49 GMT; 191,341 bytes. No retry record for S013 in `manifest-retry.json`.
- Integrity: `gzip -dc fetched/S013-1.raw.gz | sha256sum` = `492e22cf133333d6202bbfd6c47370eac981612d7952b1e851d31e06dd78920b` (matches manifest); decompressed size 191,341 bytes (matches manifest).
- Text judged: `fetched/text/S013-1.txt` (19,388 B, single line). Every quote below was located by literal match in that file.
- Base-commit check: `git cat-file -t cb807bc` → `commit`. Read-only `git diff -U0 cb807bc` and `git show cb807bc:corpus/knowledge/freshness-sweep.md` used to measure anchor drift.

## Scope

Judged as S013-dependent: every line that names S013 or Google's sitemap guidance, or that states a Google sitemap-scope, robots-discovery, or date fact the entry relies on (direct or indirect).

Excluded as not S013 (other pairs): L3 recheck and L7–13 (RFC 9309 / S011); L14–15 sitemaps.org "requires same-host URLs" (S012); L37–42 lane population and RFC recheck; L49, L52–53 (QUALITY bullets with no S013 reliance).

No `r20-correction` tail exists in this entry (no "r20", "correction", or "append" marker). The only appended material is the L20–24 refinement paragraph and the L44–53 named-debt and QUALITY sections, all covered below.

## Verdict table

| # | entry file:line | statement (abridged) | verdict | S013 quote key | S013 anchor observed / note |
|---|---|---|---|---|---|
| 1 | crawl-scope-per-host.md:1 | `source:` header lists S013 | HOLD | Q1 | "Sitemap best practices" → "Sitemap file encoding and location"; SOURCES.md:21 row and URL unchanged |
| 2 | :2 | "Google docs updated 2026-07-08" | HOLD | Q2 | page footer; HTTP Last-Modified 08 Jul 2026 agrees |
| 3 | :2 | `verified-at: 2026-10-19` (S013 clause) | HOLD · superseded date (advisory F1) | Q2 | round-26 re-fetch 2026-10-21 supersedes this stamp for S013; content unchanged |
| 4 | :15–17 | "For Google, unless submitted through Search Console, a sitemap affects only URLs under its parent directory" | HOLD | Q1 | "Sitemap file encoding and location" |
| 5 | :17 | "a site-root sitemap can cover all paths on that site" | HOLD | Q3 | same section; S013 says "can affect all files on the site" |
| 6 | :18 | "A `Sitemap:` line in the host-root robots file is a supported discovery route" | HOLD | Q4 | "Submit your sitemap to Google" (robots sub-part, not under "Sitemap best practices"); host-root example in "Sitemap cross-submission with robots.txt" |
| 7 | :20–21 | "Refines at base `cb807bc`. Makes host/path scope explicit for …" (rests on rows 4–5) | HOLD | Q1 | base commit exists; S013 scope basis holds |
| 8 | :21–23 | cited anchors `sitemap-orphan-audit.md:40-47`, `freshness-sweep.md:58`, `publish-queue.md:88-93` | **STALE (anchor only)** → C1 | Q1 | S013 part holds; all three base-commit line anchors now resolve 4 lines lower (see C1) |
| 9 | :26 | "Source checks (quotes reopened 2026-10-19)." | HOLD · superseded date (advisory F2) | Q1 | S013 quote re-checked 2026-10-21 and still verbatim |
| 10 | :33–34 | S013 bullet quote "unless you submit your sitemap…" | HOLD | Q1 | exact literal match in S013-1.txt |
| 11 | :35 | "It also describes listing a full sitemap URL in robots.txt." | HOLD | Q5 | "Submit your sitemap to Google"; the sentence names no anchor |
| 12 | :44–46 | Named debt: status of `veigapunk.github.io/robots.txt` and whether it lists project sitemaps "remain unknown" | HOLD (dependency on rows 6 and 11; live state not judged) | Q4 | S013 still documents the robots.txt route; no property probed (bounds) |
| 13 | :50 | "current host-root robots and sitemap contents remain named debt" (indirect) | HOLD (dependency) | Q6 | "Sitemap cross-submission with robots.txt" |
| 14 | :51 | "Admission authority: … Google's scoped guidance" | HOLD | Q7 | "Sitemap file encoding and location" |

Totals: 14 statements · 13 HOLD · 1 STALE.

### Quote key (verbatim from `fetched/text/S013-1.txt`)

- **Q1** (17 words): unless you submit your sitemap through Search Console, a sitemap affects only descendants of the parent directory.
- **Q2** (4 words): Last updated 2026-07-08 UTC.
- **Q3** (15 words): Therefore, a sitemap posted at the site root can affect all files on the site
- **Q4** (12 words): We will find it the next time we crawl your robots.txt file
- **Q5** (15 words): Insert the following line anywhere in your robots.txt file, specifying the path to your sitemap.
- **Q6** (9 words): reference the sitemap in the robots.txt file at https://example.com/robots.txt.
- **Q7** (23 words): Therefore, a sitemap posted at the site root can affect all files on the site, which is where we recommend posting your sitemaps.

## Findings

**STALE (row 8): superseded anchors in the L20–24 refinement paragraph.** The paragraph cites base-commit line numbers. `git diff -U0 cb807bc` hunk headers show each of the three cited files gained a 4-line front-matter block at line 1 (`@@ -0,0 +1,4 @@`). The same content now sits lower: sitemap-orphan-audit.md base 40–47 → now 44–51; freshness-sweep.md base 58 → now 62 (row A4); publish-queue.md base 88–93 → now 92–97. Content is unchanged, and the S013 path-scope claim is unaffected.

**Superseded dates (advisory, not STALE):**
- F1 (row 3, `verified-at` at L2): optional append-only note — "r26 re-check 2026-10-21: S013 re-fetched (fetchIndex 1, HTTP 200, sha256 492e22cf…78920b); S013-dependent statements HOLD."
- F2 (row 9, heading at L26): optional append-only note — "S013 quotes re-checked 2026-10-21 against the round-26 re-fetch: verbatim, HOLD."

## Corrections (append-only; STALE only)

**C1 — append after the last line (L53) of `corpus/knowledge/crawl-scope-per-host.md`; do not edit L20–24:**

```
**r26 anchor re-pin (2026-10-21; appended — original lines unchanged).** Lines 20–24 cite base `cb807bc` line numbers. Each cited file has since gained a 4-line front-matter block at its top, so the same content now sits at `corpus/knowledge/sitemap-orphan-audit.md:44-51` (base 40-47: `## Procedure` through the `docs/FLEET-MAP.md` path tables), `corpus/knowledge/freshness-sweep.md:62` (base 58: row A4, ds4cc sitemap/robots pre-push state), and `corpus/knowledge/publish-queue.md:92-97` (base 88-93: Canonical side, ds4cc.com 404 observation). The S013 path-scope claim above is unchanged.
```

## Adjacent observations (outside this entry; not judged)

- `corpus/SOURCES.md:21` (S013 row): date column still reads 2026-10-19, before the 2026-10-21 fetch. Teaches and anchor both hold. Owner: SOURCES row.
- `corpus/lessons/round-20.md:215` quotes the same S013 sentence with anchor "page last updated 2026-07-08 UTC". HOLD on the same evidence; not judged here.
- `corpus/knowledge/freshness-pins.json:144` lists the entry; not judged.
- Operability: the entry's `recheck:` line (L3) covers RFC 9309 only. S013 has no replayable check. Suggested (not applied): `curl -fsSL https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap | grep -cF 'descendants of the parent directory'` (expect 1).

## Tooling

No tools installed or upgraded. Read-only git (`cat-file`, `diff -U0`, `show`) on kake-shokunin; `gzip`, `sha256sum`, `wc` for byte checks. No network fetch, no site or property probing, no writes outside this report.

## Verification gaps

- The live `veigapunk.github.io/robots.txt` status is not probed (bounds). Rows 12–13 are judged on the S013 dependency only.
- Other corpus files are judged only at the three anchor windows in row 8.

```json
{"pair":"S013xcrawl-scope-per-host","statements":14,"hold":13,"stale":1,"corrections":["r26 anchor re-pin (2026-10-21; appended — original lines unchanged). Lines 20–24 cite base cb807bc line numbers. Each cited file has since gained a 4-line front-matter block at its top, so the same content now sits at corpus/knowledge/sitemap-orphan-audit.md:44-51 (base 40-47: ## Procedure through the docs/FLEET-MAP.md path tables), corpus/knowledge/freshness-sweep.md:62 (base 58: row A4, ds4cc sitemap/robots pre-push state), and corpus/knowledge/publish-queue.md:92-97 (base 88-93: Canonical side, ds4cc.com 404 observation). The S013 path-scope claim above is unchanged."]}
```
