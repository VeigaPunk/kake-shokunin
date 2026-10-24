# ScoutPublicSitemaps — real-run inputs only

Axes: operability (robots-allowed GET, bytes on disk, manifest v1) and freshness (live responses, Date 2026-10-23). No `sitemap_audit` run. No packages installed.

Manifest: `/fast/scratch/hyaku/kake-r39a3w1/ScoutPublicSitemaps/realrun/manifest.json` (832 bytes, sha256 `dfb8a1b6d4d3dfa824361afa06d9ab89d6365453e72f6aa1061d88f8047b9035`). `version` 1, six checks, `file` relative to that directory.

Suggested hosts did not yield a sitemap: `www.kernel.org/robots.txt` and `www.debian.org/robots.txt` HTTP 404; `www.gnu.org/robots.txt` timeout (curl 28); `www.python.org`, `www.w3.org`, and `docs.github.com` robots HTTP 200 but `/sitemap.xml` HTTP 404. Replacements below are public and non-operator. Each URL was one GET (`curl -sS -A KakeR39A3-ScoutPublicSitemaps/1.0`, sitemap calls also `-H 'Accept-Encoding: identity' --max-filesize 5242880`). Sitemap curls exited 0.

| id | sitemap URL | HTTP | bytes | sha256 | robots allow line |
|---|---|---|---|---|---|
| rfc-editor | https://www.rfc-editor.org/sitemap.xml | 200 | 259 | `f1e39049738f8f08b566dc76b8a8a7b0746da080a17048de2bcefb355d135698` | `robots/rfceditor.robots.txt:5` `Sitemap: https://www.rfc-editor.org/sitemap.xml` |
| mdn | https://developer.mozilla.org/sitemap.xml | 200 | 1282 | `9ea170a078ee7c503e2f8c57b22299c602ef6f30e426184e4ca665e26338b907` | `robots/mdn.robots.txt:2` `Sitemap: https://developer.mozilla.org/sitemap.xml` |
| fsf | https://www.fsf.org/sitemap.xml | 200 | 38342 | `9dabd65a74cc40a83ff14f8c83b9fffe25654f867fbc3cafd3ed09780c0d9373` | `robots/fsf.robots.txt:15` `Sitemap: https://www.fsf.org/sitemap.xml` |
| postgresql | https://www.postgresql.org/sitemap.xml | 200 | 4620210 | `92f7bd8d2ac8fa415c9ebfd6b17def5c146ffc332df13b248b0103654b4e4585` | `robots/postgres.robots.txt:12` `Sitemap: https://www.postgresql.org/sitemap.xml` |
| nodejs | https://nodejs.org/sitemap.xml | 200 | 1652267 | `4625ce3aa24e1627e726c1acf743ce5486fe065dd9c9b19df4f6e38230249efb` | `robots/nodejs.robots.txt:8` `Sitemap: https://nodejs.org/sitemap.xml` |
| ruby-lang | https://www.ruby-lang.org/sitemap.xml | 200 | 873987 | `c3fb0e360084a14dd0dd58b09f79959aa62a15088bff35e24243f18f81bee98d` | `robots/ruby.robots.txt:2` `Allow: /` |

Bytes are `sitemaps/<id>.xml` next to the manifest (`rfc-editor.xml` is a sitemap index; `mdn.xml` is a sitemap index; the other four are `urlset`). All six start with an XML declaration. postgresql is under the 5 MB cap (4620210 < 5242880).

Robots (same UA, curl exit 0, HTTP 200): `rfceditor.robots.txt` 135 `df052cf390448ea2916ce4d3b5f6e42880cd246ea2bf1d5efce5596b1b2e3827`; `mdn.robots.txt` 119 `8f2712e11105e549aa4fa1ea4de6a9fd5292ee805d773d669ca98a9e0e54273a`; `fsf.robots.txt` 3037 `989306caede851fa29fa5e111d5a8481154b5ffc72d79df21058ba74d4bb20fa`; `postgres.robots.txt` 273 `44d41cd563a231327036a3b84ea0c78a05c66807b5f62c43158213448d28e308`; `nodejs.robots.txt` 199 `cbcd5e7d85caf581c61f7c0ffb148868b73ffa32e8426b37e08a21d145ce8f32`; `ruby.robots.txt` 71 `1a7910b1ee54f2ac9c48b4df9714ecbaa76a812b1933d991c46c9face563b993`. For `User-agent: *` / `User-Agent: *`, no Disallow matches `/sitemap.xml` (nodejs disallows only `/dist/` and `/docs/`, `nodejs.robots.txt:5-6`).

Held out: `www.ietf.org/sitemap.xml` was HTTP 200 XML and robots allows it (`Disallow` only `/admin/` and `/search/`), but the set stays at six. `www.openssl.org` `Disallow: /`. `go.dev` has `Allow: /` but `/sitemap.xml` was 404. MDN index children are `.xml.gz` and were not fetched.
