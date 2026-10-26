# ScoutFreshnessBaidu

Fresh single GET per page on 2026-10-25 (host UTC ~23:48 +/-; saved under `ScoutFreshnessBaidu.files/`). Command: `curl -sS -L --compressed -m 60 -A kake-shokunin-round57-scout -o <file> -w '%{http_code} %{url_effective} %{num_redirects}'`. No redirects (num_redirects 0 for all three). No tool installed.

FETCHES:
| id | url | http | final url | bytes | sha256 | equal to retained |
|---|---|---|---|---|---|---|
| S421 | https://ziyuan.baidu.com/college/articleinfo?id=3458 | 200 | same (no redirect) | 34750 | 2effedc7af5eea8aca8a4271fcc91e51587462f3d3d30e120ac4b347ac9d947c | NO (byte-different, same length) |
| S422 | https://ziyuan.baidu.com/wiki/867 | 200 | same (no redirect) | 27327 | 393409dabbe6ba77bfdcfbf472c54bfebfb107f74229158340f3bf21637a7756 | NO (byte-different, same length) |
| robots | https://ziyuan.baidu.com/robots.txt | 200 | same | 672 | (not compared) | n/a |

Retained (recomputed with sha256sum, matches `sources/receipts.json`): S421 34750 B `32eaf8b74012c99dff8ae6cc3db0658d3f7520b04045336b8228461dab447182`; S422 27327 B `7cf2e27dc7e6dcba4e7bbeba09ed6f23a7c6322dc2a377e3cd36dee8c1de71ff`. Byte counts equal receipts.json (34750, 27327); hashes differ from the fresh ones. Saved copies: `fresh-S421.html`, `fresh-S422.html`, `robots.txt`.

DIFFS: `diff` + `cmp -l` (changed bytes: S421 8, S422 5). Every changed line lies AFTER `class="footer"` (S421 footer at line 319, diffs at 346/347/361; S422 footer at line 290, diffs at 318/319), i.e. in the trailing script block, not the article block (S421 `class="article-info"` line 271 to footer 319; S422 `zz_dldes_content` line 275 to footer 290), and not header/nav/sidebar. Changed text is only passport.baidu.com script cache-busters:
- S421 l.346 `uni_login_wrapper.js?cdnversion=202610260738` -> `...202610260748`; l.347 `wrapper.js?cdnversion=1792971513` -> `1792972122`; l.361 `passreg` URL port `%3A8054%2F` -> `%3A8109%2F` (login-widget config).
- S422 l.318 same `uni_login_wrapper.js` cdnversion `...0738` -> `...0748`; l.319 `wrapper.js?cdnversion=1792971515` -> `1792972124`.
Article block, title, header, nav, sidebar: byte-identical to retained. The page therefore has no content drift; only per-request script tokens differ, so retained-body sha256 will not be reproducible by a re-fetch (a sha-equality recheck would false-alarm; a substring recheck holds).

DATES: S421 `<p class="info-item-time">发布日期：2022-09-09</p>` (line 273, fresh and retained identical). S422 `发布日期：2016-06-30` (line 274, fresh and retained identical). Both match the staged entries' `发布日期` values.

RENDERING: plain GET body (no JS execution, `--compressed`) contains the article text; not client-rendered for these quotes. The two staged `recheck:` strings, counted with `grep -F -o` on the fetched body (and equally on the retained body):
- `死链一般是指页面已经无效，无法对用户提供任何有价值信息的页面。` in fresh S421: 1 (line 275, inside the article block, inside a `<section powered-by="xiumi.us"`); in fresh S422: 0.
- `启用了全新的死链识别模型，能识别协议死链，以及大多数内容死链、跳转死链等低质网页` in fresh S422: 1 (line 276, inside the `zz_dldes_content` block, in the article text); in fresh S421: 0.
Each staged recheck count is therefore 1 on its own page, matching the staged `-> 1` claims. Note both occurrences sit on very long single lines (article body is one HTML line each).

ROBOTS: `https://ziyuan.baidu.com/robots.txt` -> HTTP 200, 672 bytes. Group 1 `User-agent: *` has only `Disallow: /app/` and `Disallow: /webapp/` (neither `/college/` nor `/wiki/`). Named bots (Baiduspider*, Googlebot, MSNBot, YoudaoBot, Sogou*, Sosospider, ...) have `Allow: /`. A SECOND, final `User-agent: *` group (line 50) has `Disallow: /`. Fact for the scope note: with the two `*` groups read as one merged group (RFC 9309 behaviour), `*` is disallowed from `/college/` and `/wiki/` (and everything); read as first-group-only it is not. Our UA `kake-shokunin-round57[-scout]` matches no named group. The pages were fetched by a single non-crawler GET; nothing further was fetched.

VERDICT: bodies not byte-equal (only trailing login-script cdnversion/port tokens differ, after `class="footer"`); article blocks, dates (2022-09-09, 2016-06-30), HTTP 200 with no redirect, and both staged recheck strings (1 each) all hold; robots.txt has a final `User-agent: *` / `Disallow: /` group.
