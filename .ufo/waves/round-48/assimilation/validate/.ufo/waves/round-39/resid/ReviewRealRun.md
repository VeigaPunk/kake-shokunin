# ReviewRealRun — Kake r39a3 residual, real run on six public sitemaps

Verdict: PASS — build output reproduced byte-identically on all six files; all sampled
findings are right per contract sentences 24–27; no actionable defect found.

## Reproduction

- Working-tree `scripts/sitemap_audit.py` at tip d8a20a99 is identical to build commit
  565ef4c9 (sha256 6d86c8ce…, `git show 565ef4c9:scripts/sitemap_audit.py` vs file).
- `sha256sum -c verification/realrun/inputs.sha256` → all 7 OK, exit 0.
- `python3 scripts/sitemap_audit.py --manifest manifest.json` (run from
  /fast/scratch/hyaku/kake-r39a3w1/ScoutPublicSitemaps/realrun) → exit 1, matching
  `build-565ef4c9.exit` (=1). `cmp` rerun vs `build-565ef4c9.json` → identical.
- `cmp build-565ef4c9.json reference-663e051e.json` → identical (build and reference
  agree on every check).
- Output: verdict `failed-policy`; rfc-editor, mdn, postgresql, ruby-lang `clean`;
  fsf 212× `loc_out_of_scope` (entries 1–212); nodejs 8× `loc_out_of_scope`
  (entries 1656–1663).

## Findings adjudication (contract sentences 24–27)

fsf.xml — urlset, sitemapUrl `https://www.fsf.org/sitemap.xml`. Sampled entries 1–5:
`http://www.fsf.org/`, `/about`, `/campaigns`, `/associate/`, `/resources`
(sitemaps/fsf.xml). Scheme `http` ≠ `https` → differs per sentence 25 →
`loc_out_of_scope` RIGHT for all 5. All 212 locs in the file are
`http://www.fsf.org/…` (urllib.parse scan: 212× scheme http, host www.fsf.org),
so the full count of 212 is consistent.

nodejs.xml — urlset, sitemapUrl `https://nodejs.org/sitemap.xml`. Sampled entries
1656–1660: `ai-coding-assistants-policy.openjsf.org`, `terms-of-use.openjsf.org`,
`privacy-policy.openjsf.org`, `bylaws.openjsf.org`, `code-of-conduct.openjsf.org`
— host ≠ `nodejs.org` → `loc_out_of_scope` RIGHT. Same holds for 1661–1663
(`trademark-policy`, `trademark-list` on openjsf.org; `www.linuxfoundation.org/cookies`).
Exactly these 8 of 1663 locs have a non-nodejs.org host — no other host misses.

## Clean files — spot-read 10 locs each (all in scope, clean RIGHT)

- rfc-editor (sitemapindex; sentence 27: scheme/host/port only): 2 entries,
  `https://www.rfc-editor.org/sitemap-{1,2}.xml` — same scheme+host.
- mdn (sitemapindex): 10 entries, `https://developer.mozilla.org/sitemaps/<locale>/sitemap.xml.gz` — same scheme+host.
- postgresql (urlset; sitemapUrl dir `/`): sampled 10 of 29,600 —
  e.g. entry 1 `https://www.postgresql.org/`, 2961 `…/docs/18/catalog-pg-attrdef.html`,
  26641 `…/docs/7.3/pltcl-description.html` — all https www.postgresql.org.
- ruby-lang (urlset): sampled 10 of 7,593 — e.g. entry 1
  `https://www.ruby-lang.org/de/news/2001/01/18/stable-snapshot-is-available/`,
  6832 `…/zh_tw/news/2022/12/` — all https www.ruby-lang.org.
- Whole-file scope scan confirms 0 out-of-scope locs in each clean file (schemes/
  hosts uniform per above).

## Residual risk / gaps

- Spot-reads cover loc scope only; lastmod/changefreq/priority values inside clean
  files not individually adjudicated (none were flagged; build==reference).
- No installs performed; stdlib python3 and coreutils sufficed.
