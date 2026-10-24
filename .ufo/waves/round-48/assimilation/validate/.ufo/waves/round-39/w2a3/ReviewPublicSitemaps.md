# ReviewPublicSitemaps — provenance + hand-derived verdicts (axes: operability, freshness)

Attacked report: `.ufo/waves/round-39/w1a3/ScoutPublicSitemaps.md`. Target dir `/fast/scratch/hyaku/kake-r39a3w1/ScoutPublicSitemaps/realrun/` (manifest + sitemaps/*.xml + robots/*.robots.txt). Commands run (cwd /home/vgpnk/Projects/shokunin): `sha256sum` + `wc -c` over manifest/sitemaps/robots (exit 0); `head -c 110` each .xml; `iconv -f UTF-8` + `grep -o '<sitemap>'|wc -l` + `grep -o DOCTYPE|wc -l` on the two smallest; grep `^HTTP/|^date:` and `content-length` over sitemaps/*.hdr. No sitemap tool run. No installs.

## Provenance

- **sha256: holds.** All 7 reported digests match exactly: manifest `dfb8a1b6…9035` 832B; fsf `9dabd65a…d9373` 38342; mdn `9ea170a…8b907` 1282; nodejs `4625ce3…9efb` 1652267; postgresql `92f7bd8…e4585` 4620210; rfc-editor `f1e3904…5698` 259; ruby-lang `c3fb0e3…e98d` 873987. Six cited robots digests also match (rfceditor `df052cf3…3827` 135B; mdn `8f2712e1…273a` 119B; fsf `989306ca…20fa` 3037B; postgres `44d41cd5…e308` 273B; nodejs `cbcd5e7d…8f32` 199B; ruby `1a7910b1…993` 71B). Content-Length in 4 hdrs equals on-disk bytes (nodejs/rfc-editor hdrs omit it — chunked, not a defect).
- **robots line citations: holds.** Verified verbatim: `robots/rfceditor.robots.txt:5` `Sitemap: https://www.rfc-editor.org/sitemap.xml`; `mdn.robots.txt:2` `Sitemap: https://developer.mozilla.org/sitemap.xml`; `fsf.robots.txt:15` `Sitemap: https://www.fsf.org/sitemap.xml`; `postgres.robots.txt:12`; `nodejs.robots.txt:8`; `ruby.robots.txt:2` `Allow: /`. Each `User-agent: *` group permits `/sitemap.xml` for the named UA (nodejs Disallow only `/dist/`,`/docs/` at :5-6 — verbatim). NOTE: `Sitemap:` is a non-group directive — it publishes the sitemap URL; the fetch allowance comes from the `*` group (no matching Disallow in all six). Report's phrasing "robots allow line" is fair.
- **manifest: holds.** version 1, six checks, `sitemapUrl` identical to the report table for all six; `file` relative paths resolve; every check would satisfy contract §4.
- **freshness/operability: holds.** All six `sitemaps/*.hdr` show `HTTP/…200` and `date: Fri, 23 Oct 2026` (fsf `01:45:30`, mdn `06:55:23`, nodejs `06:56:05`, postgresql `06:11:39`, rfc-editor `06:55:23`, ruby-lang `06:56:05` GMT). All six files start with an XML declaration; four large ones confirmed `urlset` root start (postgresql decl is lowercase `utf-8` — legal, contract §7 case-insensitive).
- **Held-out claims: holds where checkable.** `openssl.robots.txt:1-2` `User-agent: *`/`Disallow: /` verbatim; `godev.robots.txt` `Allow: /` verbatim (its `/sitemap.xml` 404 not artifact-verifiable, consistent with absence of godev.xml); `ietf.robots.txt` Disallow only `/admin/`+`/search/` verbatim; ietf sitemap absent = "set stays at six" consistent. MDN index children are `.xml.gz` and unfetched — consistent, no stray files. kernel/debian/gnu/python/w3/docs.github.com failure claims have no on-disk artifacts either way — not falsifiable, not contradicted.

## Hand-derived verdicts (contract sentences 1–34 only; no tool run)

- **rfc-editor.xml (259B, index) → status `clean`, zero findings.** (a) UTF-8 valid, no BOM, decl `UTF-8` §6-7. (b) well-formed `sitemapindex` doc, no doctype §8-9. (c) root `{http://www.sitemaps.org/schemas/sitemap/0.9}sitemapindex` §10. (d) 2 `sitemap` entries §11-13. (e) each entry: exactly one `loc`, no other child §15-17. (f) 259<52,428,800; 2<50,000 §19-20. (g) both locs `https://www.rfc-editor.org/sitemap-{1,2}.xml` absolute https §22, 41-43 chars <2048 §23. (h) index: scheme+host+port (443) match sitemapUrl §24,27. (i) no `lastmod` present — allowed §15.
- **mdn.xml (1282B, index) → status `clean`, zero findings.** (a)-(c) same as above (decl `UTF-8`). (d) 10 `sitemap` entries §11-12. (e) each entry: one `loc` + one `lastmod`; both permitted in index entries §15-16; no `changefreq`/`priority` §17. (f) in limits. (g) all locs `https://developer.mozilla.org/sitemaps/<locale>/sitemap.xml.gz` — absolute https §22; contract has no gzip/extension rejection, `.gz` suffix irrelevant §22-23. (h) index scope: scheme+host+default port match `https://developer.mozilla.org/sitemap.xml` §27 — `.gz` and deeper paths don't trigger `loc_out_of_scope`. (i) all `lastmod` `2026-10-23` = `YYYY-MM-DD` level, valid Gregorian date §28-29.
- File-level `input_invalid`/`file_unreadable` n/a: manifest parses, all `file`s readable §3-5.

## Per attacked statement

| Statement | Verdict |
|---|---|
| Manifest v1, sitemapUrl = fetched URL | **holds** |
| All six sha256 + byte counts | **holds** |
| Six robots citations verbatim + allow the fetch | **holds** |
| 200 responses, Date 2026-10-23, XML decls | **holds** |
| index-vs-urlset typing, postgresql < 5 MB cap | **holds** |
| Held-out set (openssl Disallow /, godev Allow+404, ietf allowed, MDN .gz unfetched) | **holds** |
| Suggested-host failures (kernel 404, debian 404, gnu timeout) | **unverifiable** — no artifacts, nothing contradicts |
| Expected verdicts rfc-editor/mdn = clean | derived `clean`/`clean` — report makes no claim to attack |

Residual risk: HTTP 200/Date prove responses were captured 2026-10-23 but I did not re-fetch (item scopes me to realrun inputs; network restricted to item-named URLs). robots `Sitemap:`-vs-Allow semantic reading is mine but does not change the allow outcome.
