# ReviewerC3Derive

Reviewed `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-58/derive_c58_quote_truth.py` and the generated `c58_quote_truth.py` (lane tip cc8da16; working tree clean except untracked w1 dispatch files, not touched). Counter runs executed at base `044048597d62f3199494b63b36e90dd57825e350` and at the freeze commit `fff3eea6aa349c8635fd84a791cc32de350ee1c2` (read-only `git show` + counter run from the lane; no lane/git mutation).

## FINDINGS

No actionable defect found in the derive script or the generated counter. Ordered observations:

1. (Doc-only, cosmetic) The c58 docstring says the condition code is "unchanged except the round constants, the S424 article-block end marker and the page-named subject". The derive also replaced the selftest block with a stub and swapped the `description`/`schema` strings; the docstring understates the change set. No code impact.
2. (Expected, documented) `--selftest` is a version-1 stub returning 2; the contract states wave 1 ports it before data. Run `python3 -B c58_quote_truth.py --selftest` now returns 2 (unevaluable) — intended pre-port state.
3. Assertion hygiene of the derive script is good: it asserts the round-57 blob is readable at BASE, asserts each body's sha256 equals its receipt before substitution, asserts each `sub()` target exists, and asserts no `S421`/`S422`/`round-57`/`round57`/`死链` token survives in the generated body — all asserts hold on the emitted file.

## BLOCK CHECK

Marker occurrences and windows computed on the retained bodies with the counter's own `content_window` (where `hi = find(ARTICLE_END[sid], lo+1)`, `hi > lo`):

- S423 (`sources/S423.html`, 29007 bytes):
  - start marker `class="article-info"`: offset 9367, exactly 1 occurrence. It is the article container inside `div.list-left`, after the breadcrumbs and sidebar wrapper — header/nav/sidebar precede it and are excluded.
  - end marker `往期回顾`: offset 14801, exactly 1 occurrence, strictly after start. It opens the back-issue list paragraph (`往期回顾：…`, then the `【第N集】` links); the whole back-issue list and the page tail are excluded.
  - window (9367, 14801); 159 text-node segments (some whitespace-only captures, a regex artifact).
  - first meaningful text node: `搜索问答剧场 【五】“百度蜘蛛”全面解析` (h3 title); last meaningful text node: `【搜索问答剧场】是资源平台基于…运营知识库。` (the article's closing summary). The window includes the whole article, including the in-article reference to S424's URL.
- S424 (`sources/S424.html`, 22476 bytes):
  - start marker `class="article-info"`: offset 9352, exactly 1 occurrence, after breadcrumbs/sidebar wrapper.
  - end marker `推荐阅读`: offset 11025, exactly 1 occurrence, strictly after start. It is the `h2.recommand-news-title` header of the recommended-reading list; the list (`ul.news-list`) and footer follow and are excluded.
  - window (9352, 11025); 44 text-node segments.
  - first meaningful text node: `开发者如何解除封禁百度蜘蛛` (h3 title); last meaningful text node: `【建议方案】解除百度IP封禁：查看网站反爬虫策略，进行策略调整。` (final article paragraph). The whole article fits inside the window.
- S424 contains no `往期回顾` at all (count 0) — no stale round-57 end-marker assumption. S423's single `推荐阅读` (offset 15538) lies after its window, outside the article block.
- `TOPIC = "百度蜘蛛"` appears inside both blocks (26× S423, 7× S424) and in both page `<title>`s (S423 `…_搜索学堂_百度搜索资源平台` → row-title prefix `搜索问答剧场 【五】“百度蜘蛛”全面解析`; S424 → `开发者如何解除封禁百度蜘蛛`).

## NO-DEFECT CHECKS

- sha256 triple-equality: body files == `sources/receipts.json` == `BODY_SHA256` (S423 `8b8aef60…`, S424 `3ef1275b…`); freeze-commit blobs hash identically; receipts bytes 29007/22476 match `wc -c` and the bodies.
- `ROW_URL` matches receipts/sour URLs (S423 `?id=3457`, S424 `?id=3028`); `ADOPTED` and `STAGED_ABSENT` (`corpus/knowledge/baidu-crawler-identification.md`) match contract.md.
- Round tag: receipts `userAgent` = `kake-shokunin-round58` carries `round58`; the C6 check line was rewritten round57→round58 (diff hunk at c58:481 confirms).
- Constants: `ROUND_DATE=2026-10-26`, `BASE_REV=0440485…`, `LESSON=corpus/lessons/round-58.md`, `WAVE=.ufo/waves/round-58` — all match contract.
- Counter at base: `0/8`, exit 1, revision 0440485; output matches the committed `controls/base-c3-quote-truth.txt` verbatim. Counter at freeze fff3eea: `0/8`, exit 1, with only expected-absence notes (entries/rows absent; C6 fails solely on registry-URL comparison, the receipt pins themselves pass; C8 notes mirror add-commit == measured revision). Both do-nothing states behave as designed.
- Diff of round-57 counter v2.1 (at base) vs c58 shows only the intended substitutions (docstring, constants, round-tag lines, ADOPTED/NEW_ROWS/ROW_URL/STAGED_ABSENT/BODY_SHA256/TOPIC/ARTICLE_START/ARTICLE_END, selftest→stub, description, schema). No hardcoded ids, no two-row/死链/round-57 assumption survived in code (grep hits are only docstring provenance mentions).
- File identity: `c58_quote_truth.py` sha256 `0dde4d649d9b455025badd3f2c5260a4026e53cde24a53d61c7a8b01d3abbeed` == contract.json `C3.counterSha256v1`; freeze blob `1358df90…` matches the workspace file.
- `span_tools.py` imports and interoperates with the generated counter (smoke: `spans`/`check`/`window` run against both bodies).

Unrun/not applicable: no live data exists at base or freeze, so C1..C8 pass-state was not exercised (nothing to pass yet); the selftest is unevaluable until ported.

VERDICT: derive script and generated c58_quote_truth.py are sound — substitutions, receipts/body digests, round tag, block locators and freeze/base do-nothing runs all verified; no defect found.
