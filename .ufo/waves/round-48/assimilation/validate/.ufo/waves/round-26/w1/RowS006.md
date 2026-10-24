# S006 — FRESHNESS recheck (round 26)

Row: `corpus/SOURCES.md:14` · tier A · kind docs · scope "Default file exclusions in GitHub Pages Jekyll branch builds" · anchor "Configuring Jekyll in your GitHub Pages site; fetched 2026-10-19" · used-by `corpus/knowledge/ghp-served-set.md`.

Fetched #1: `https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll` → HTTP 200, 138096 bytes, sha256 `71a698604486380c05ca092adbc863dc653fc175eecea5a675891651cd3bdfbd`, fetched 2026-10-21T15:09:35Z (response `date: Wed, 21 Oct 2026 15:09:35 GMT`; no etag/last-modified); text view `fetched/text/S006-1.txt` (7676 chars). Living, unpinned docs: availability plus content drift test.

```json
{"id":"S006","verdict":"HOLD","fetchIndex":1,"quote":"Jekyll doesn't build files or folders that: Are located in a folder called /node_modules or /vendor Start with _,., or # End with ~","anchorObserved":"H2 'Configuring Jekyll in your GitHub Pages site' (id configuring-jekyll-in-your-github-pages-site), exclusion list immediately after the locked-settings list and before the 'Front matter' H2","reason":"All five exclusion classes named by the teaches remain verbatim in that section: folders /node_modules and /vendor, names starting with _, . or #, names ending with ~, plus the exclude-setting clause. The page still documents branch publishing ('If you are publishing from a branch ...'), so scope, anchor and teaches hold unchanged; the page's added GitHub Actions advisory does not alter Jekyll's branch-build defaults.","correction":null}
```

Caveats:
- Living, unpinned docs: no commit/tag pin to freeze; HOLD rests on today's bytes still carrying the teaches, not on a version match.
- No earlier S006 fetch is retained under `.ufo/waves`, so drift since 2026-10-19 cannot be byte-diffed; the current payload independently supports the row.
- Digest verified: decompressed body sha256 `71a69860…bdfbd` matches population/manifest byte counts; the gz container hash (`d0474010…180dd8`) differs only because the manifest hashes decoded body bytes.
- Raw HTML exposes no dateModified/lastUpdated field, consistent with an unpinned living page.
- Knowledge claim at `corpus/knowledge/ghp-served-set.md:30-33` (node_modules/vendor, `_ . #` prefixes, `~` suffix) matches the re-fetched text; no knowledge correction needed from this row.
- The Actions note ("github-pages gem remains supported for some workflows, GitHub Actions is now the recommended approach") is advisory; branch Jekyll builds and their defaults are still documented, so it does not narrow the scope.
- No tool installs or upgrades were performed.
