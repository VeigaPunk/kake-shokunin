# ScoutFreshness

FETCHES: (UA `kake-shokunin-round56-scout`, `curl -sS -L`, one GET each, 2026-10-25 ~22:28 GMT; bodies saved in `.ufo/waves/round-56/w1/ScoutFreshness.md.files/`)
- https://info-search.yahoo.co.jp/archives/002852.php — HTTP 200, 8051 bytes, sha256 0188de9dae01e9088231098a9c6af3c8f5dc62a5982419a5f82fd98e86772a19 — equal to S367.html: yes (cmp byte-identical; sha256 equals receipts.json S367)
- https://info-search.yahoo.co.jp/archives/002856.php — HTTP 200, 7428 bytes, sha256 6172d5d108d0c31d25244659516fc7fc81472c924ef35a51afc964cdd3a4a5c8 — equal to S419.html: yes (cmp byte-identical; sha256 equals receipts.json S419)
- https://info-search.yahoo.co.jp/archives/002857.php — HTTP 200, 7332 bytes, sha256 a860d4f33181302d7ab467f5a0b21f2008916bb6dc6def69e69df5b54c630209 — equal to S420.html: yes (cmp byte-identical; sha256 equals receipts.json S420)
- Byte counts and sha256 also match the receipts.json entries (8051 / 7428 / 7332) for all three.
- https://info-search.yahoo.co.jp/robots.txt — HTTP 200, 141 bytes, sha256 14a529933f3395b7e9a333d3ba9812cfda613f171391969025b28be0f6acf044 (saved as robots.txt in the .files dir).

DIFFS:
- None. All three bodies are byte-identical to the retained files, so no region (article block, sidebar, footer) changed.

DATES: (printed `<p class="update">`, line 101 of each page)
- 002852.php (S367): 更新日 2010年11月24日
- 002856.php (S419): 更新日 2010年11月24日
- 002857.php (S420): 更新日 2010年11月24日
- Final URL: each equals the requested URL; `num_redirects=0` for all three, and for robots.txt.
- The pages' `<title>` values: 002852 リンク先のウェブページの巡回制限 ― ウェブページ内やサーバーでの設定; 002856 削除したウェブページが巡回され続ける; 002857 存在しないウェブページが巡回される (each followed by " - インフォセンター - Yahoo!検索").

NOTES:
- The robots.txt body is: `User-agent: *`, then `Disallow: /cgi-bin/`, `/images/`, `/*.css$`, `/*.js$`, then `Sitemap: https://info-search.yahoo.co.jp/sitemap.xml`. It does NOT mention `archives` (grep count 0), so `/archives/` is not disallowed for `User-agent: *` by the site's own robots.txt. Scope-note fact only.
- Extra request beyond the assignment: one HEAD request per page (3 total) to look for Last-Modified. Responses were HTTP/2 200 with only a `date:` header among date/etag/last-modified, so there is no HTTP-level revision date. The printed 更新日 is the only revision date.
- The pages are unchanged since the earlier round-56 fetch (22:02 GMT) and carry the 2010-11-24 printed date. Nothing in the retained evidence needs refreshing.
- No tools were installed. No pacman was run. No repo or VCS mutation; only this report and its `.files/` directory were written.

VERDICT: All three adopted pages re-fetched HTTP 200 with no redirect, byte- and sha256-identical to S367/S419/S420 and receipts.json; each prints 更新日 2010年11月24日; site robots.txt (200) does not mention `archives`.
