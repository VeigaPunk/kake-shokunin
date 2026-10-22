# Scout — og:url / canonical / sitemap loc consistency, ds4cc @ 7fc6aa2f

Verdict: on the 87 pages that carry `og:url`, the three signals are **exactly consistent**;
zero mismatches in every class. The only real divergence on the site is on two pages that
have **no** `og:url`, so neither the new audit rule nor an OG-only check can see it.

## Method (sandbox /fast/scratch/hyaku/kake-r34/w1/ScoutOgUrlCanonicalSitemap/work)
- `tar -xJf .ufo/waves/round-34/sources/ds4cc-7fc6aa2f/html.tar.xz` → exit 0, 102 `*.html`.
- `python3 -B audit.py . .ufo/waves/round-33/sources/ds4cc-7fc6aa2f/sitemap.xml` → exit 0.
  Parser = stdlib `HTMLParser`; `og:*` read from `property=` meta; canonical from `link[rel~=canonical]`.
  Mapping: `index.html`→`/`, `x/index.html`→`/x/`, else literal path.
- Faithfulness of the archive: for each of the 102 paths, `git hash-object -- <file>` vs
  `git ls-tree -r 7fc6aa2f` → exit 0, **0/102 mismatches**, none missing.
- Sitemap provenance: `git show 7fc6aa2f:sitemap.xml | sha256sum` =
  `sha256sum .ufo/waves/round-33/sources/ds4cc-7fc6aa2f/sitemap.xml` =
  `55cb947fa2d07f4a39f709b102f0133c94eb351501ec0b6d2263746f487006ef`. 100 `<url>`, 100 unique,
  all `https://ds4cc.com/`; 14 `.html`-style locs + 86 directory-style; no loc carries query/fragment;
  0 locs equivalent after normalising `.html`/`/index.html`/trailing slash.
- Raw cross-check: `grep -rhoiE '<meta[^>]*og:image[^>]*>' --include='*.html' .` → exit 0;
  `name="og:*"` forms: none, so the `property=` parse is complete for this corpus.

## Counts per class
Pages carrying `og:url`: 87 of 102 (each exactly one; 0 duplicate `og:url` values across pages;
all absolute `https://ds4cc.com/…`; all `og:type=website`, 0 pages with two `og:type`).

| comparison | scheme | host | path | trailing slash | query/fragment | total |
|---|---|---|---|---|---|---|
| `og:url` vs `canonical` (87) | 0 | 0 | 0 | 0 | 0 | **0** |
| `og:url` vs own sitemap `loc` (87) | 0 | 0 | 0 | 0 | 0 | **0** |

- `og:url` values not present in the sitemap: **0**. Pages whose `og:url` page is outside the sitemap: 0.
- Sitemap locs whose page lacks `og:url`: **13**, and all 13 also carry **zero** `og:*` tags
  (no title/type/image/url), each with a canonical equal to its loc:
  `bloat.html`, `exa.html`, `burnerchrome/index.html`, `burnerchrome/family.html`,
  `burnerchrome/install.html`, `burnerchrome/compare.html`, `burnerchrome/burner.html`,
  `burnerchrome/marketplace.html`, `burnerchrome/delegate.html`,
  `burnerchrome/adapters/{almanacker,kimiraikkoner,musketeer,puppeteer}.html`.
- Pages outside the sitemap: **2** — `burnerchrome.html` (meta-refresh stub + `canonical=/burnerchrome/`,
  no OG; :5-6) and `benchmarks/benxshitter-frontier.html` (no canonical, no OG, no inbound link; head :1-9).

## Defect found (class `extension`, invisible to the og:url rule)
| page | canonical | sitemap loc |
|---|---|---|
| `bloat.html:384` | `https://ds4cc.com/bloat` | `https://ds4cc.com/bloat.html` |
| `exa.html:393` | `https://ds4cc.com/exa` | `https://ds4cc.com/exa.html` |

Both pages' own nav links still use `./exa.html` (bloat.html nav), so the canonical names a URL
no internal link uses, while the sitemap advertises the other one. Both pages lack `og:url`, so
the declared rule "og:url differs from canonical" and any OG-scoped audit cannot flag this.
Mechanism: the sitemap is hand-maintained — `git grep -l -i sitemap 7fc6aa2f -- .` returns only
`CHANGELOG.md` (":21", gkeep gained "a sitemap entry") and `robots.txt`; no generator script
exists in the tree, so nothing keeps loc and canonical in sync.

## Freshness reading for this round
- Independent recount reproduces the frozen receipt `verification/c2-at-d08d8de.json`
  `census.derived` exactly: `pages=102 og:title=87 og:type=87 og:image=1 og:url=87 all-four=1
  og-url-equals-canonical=87`. So the C2 entry line, if it states those numbers, is truthful at
  7fc6aa2f.
- `og:image` exists on exactly one page (`omegag/index.html:15`, `assets/masterpiece.png`, 1920x840).
  Consequence: on ds4cc the new audit's dominant output is 86 missing-`og:image` pages plus 15
  missing-OG pages — not URL inconsistency. The S068 (multi `og:type`) and `og:url`≠canonical
  rules have **no witness** in this corpus, so passing them proves nothing about real data.

## Not verified
- Whether `https://ds4cc.com/bloat` and `/exa` (extensionless) resolve — owned host, no live
  requests; cannot say whether canonical or sitemap is the live truth.
- No JS/edge injection of OG tags was modelled (no browser); parse is static HTML only.
- Tool installs: none. Network: none. No lane or repo mutation; only this file written.
