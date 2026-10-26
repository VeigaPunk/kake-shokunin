# ReviewerStagedBaidu

Fidelity review of the two staged Baidu candidates against the retained bodies (`sources/S421.html`, sha256 `32eaf8b7…`, 34750 bytes = staged `baidu-dead-link-taxonomy.md`, row S403 -> lane S421 `baidu-dead-link-types.md`; `sources/S422.html`, sha256 `7cf2e27d…`, 27327 bytes = staged `baidu-spider3-dead-link-recognition.md`, row S408 -> lane S422 `baidu-spider3-dead-link-model.md`). All replacement quotes below were verified with `span_tools.py` (`units <= 25`, `len <= 40`, raw substring of the retained body, `in_content=True`, `count_in_page=1`, `in_other_adopted_body=False`, ASCII double quotes).

## DEFECTS:

### S421 — `baidu-dead-link-taxonomy.md` (staged S403 -> lane S421 `baidu-dead-link-types.md`)

1. **`baidu-dead-link-taxonomy.md:2` and `:19-28` (zero quoted spans >= 6u; non-occurring composite anchor; pre-renumber id/date)**
   - **Page text:** `<h2>一、了解死链</h2><div><br></div><div><span name="h2_article_title1"><h3>1、死链都有哪些类型？</h3>` (S421.html line 275). The composite string `一、了解死链 → 1、死链都有哪些类型？ A：` occurs 0 times in `S421.html`. The staged entry carries 0 double-quoted spans (C5 requires >= 3 distinct page-unique spans of 6..25u and <= 40 chars). Also staged `SOURCES.append.md:123` writes the title without the space before `【六】` (`搜索问答剧场【六】“死链”常见问题解析`, 0 hits in S421.html; actual `<title>` and `<h3 class="info-title">` have an ASCII space: `搜索问答剧场 【六】“死链”常见问题解析`, 3 hits).
   - **Fix:** Rename entry to `corpus/knowledge/baidu-dead-link-types.md`; set `source: S421 — https://ziyuan.baidu.com/college/articleinfo?id=3458 — § 1、死链都有哪些类型？ (发布日期 2022-09-09) — fetched 2026-10-25` and `verified-at: 2026-10-25`; use row title `搜索问答剧场 【六】“死链”常见问题解析`; embed >= 3 checked page-unique quotes from the list below.

2. **`baidu-dead-link-taxonomy.md:4` (recheck grep string is 29 units, over the 25-unit ceiling if quoted)**
   - **Page text:** `A：死链一般是指页面已经无效，无法对用户提供任何有价值信息的页面。` (`S421.html` line 275, § 一、了解死链 → `1、死链都有哪些类型？`). Full sentence is 29u / 31 chars.
   - **Fix:** Split into `"死链一般是指页面已经无效，"` (12u, 13 chars) and `"无法对用户提供任何有价值信息的页面。"` (17u, 18 chars); use one of those in `recheck:` and Gate so every span stays <= 25u and <= 40 chars.

3. **`baidu-dead-link-taxonomy.md:10-11` (dropped qualifier `一般是指` and `包括`)**
   - **Staged:** `A dead link is a page that has already become invalid and can give the user no valuable information; the taxonomy then splits it in two.`
   - **Page text:** `A：死链一般是指页面已经无效，无法对用户提供任何有价值信息的页面。包括协议死链和内容死链。` (§ 一、了解死链 → `1、死链都有哪些类型？`).
   - **Fix:** Preserve both qualifiers (`一般是指` = "generally refers to", `包括` = "includes"): `A dead link generally refers to ("死链一般是指页面已经无效，") a page that has already become invalid and can provide no valuable information to the user ("无法对用户提供任何有价值信息的页面。"), and includes protocol dead links and content dead links ("协议死链和内容死链", 9u, 9 chars).`

4. **`baidu-dead-link-taxonomy.md:13-14` (dropped qualifiers `明确表示` and `等`)**
   - **Staged:** `A protocol dead link is the familiar case — the TCP or HTTP status says so, and 403, 404 and 503 are the common ones.`
   - **Page text:** `（1）协议死链：页面的TCP协议状态/HTTP协议状态明确表示的死链，常见的如403、404、503状态等。` (§ 一、了解死链 → `1、死链都有哪些类型？`).
   - **Fix:** Preserve `明确表示` ("explicitly indicates") and `等` ("and the like"): `A protocol dead link is one explicitly indicated by the page's TCP or HTTP protocol status ("的TCP协议状态/HTTP协议状态明确表示的死链，", 16u, 25 chars), commonly 403, 404, 503 statuses and the like ("常见的如403、404、503状态等。", 7u, 19 chars).`

5. **`baidu-dead-link-taxonomy.md:14-16` (dropped qualifier `等与原内容无关的信息页面`)**
   - **Staged:** `A content dead link is not: the server returns a normal status, but the content has changed to something that no longer exists, has been deleted, or needs a permission.`
   - **Page text:** `（2）内容死链：服务器返回状态是正常的，但内容已经变更为不存在、已删除或需要权限等与原内容无关的信息页面。` (§ 一、了解死链 → `1、死链都有哪些类型？`).
   - **Fix:** Preserve `等与原内容无关的信息页面` ("and similar information pages unrelated to the original content"): `A content dead link is one where the server return status is normal ("服务器返回状态是正常的，但", 12u, 13 chars), but the content has changed to non-existent, deleted, or permission-requiring ("内容已经变更为不存在、已删除或需要权限", 18u, 19 chars) and similar information pages unrelated to the original content ("等与原内容无关的信息页面", 12u, 12 chars).`

6. **`baidu-dead-link-taxonomy.md:16-17` (clause location & dropped `服务器端` / `状态码` precision; framing as "consequence")**
   - **Staged:** `The page states the consequence plainly: the content kind returns HTTP 200 and cannot be set to 404.`
   - **Page text:** Second sentence of item `（2）内容死链` under § 一、了解死链 → `1、死链都有哪些类型？`: `内容死链，服务器端返回HTTP状态码200，无法设置为404。` (Inside `<b>内容死链</b>` item (2) of Q1's answer, not a separate section).
   - **Fix:** Locate the clause explicitly as the second sentence of Q1 item (2) (`（2）内容死链`), drop "the consequence", and render: `In the second sentence of item (2), for a content dead link the server side returns HTTP status code 200 ("服务器端返回HTTP状态码200", 9u, 16 chars) and cannot be set to 404.`

7. **`baidu-dead-link-taxonomy.md:5, 7, 19-28` (inflated generalization, untagged inferences, and self-contradictory remedy)**
   - **Staged:** l.5 `that no status code reveals`; l.7 `# The dead link that answers 200`; l.19-25 `That single clause is why the taxonomy matters to a publisher. A page that is gone but still answers 200 is, by the operator's own definition, a dead link — and no crawler, monitor or link checker that reads status codes alone can see it. The symptom is a page that crawls cleanly, ranks as a live URL, and sends a visitor to an empty or permission-gated screen. The remedy is on the publisher's side and is not a status code: the path has to be removed from the site's internal links, or the route has to be made to answer a real 404.`; l.26-28 `The same distinction governs what to do with a link that points at such a page...`
   - **Page text:** S421 never mentions monitors, link checkers, "crawls cleanly", "ranks as a live URL", or removing internal links. In § 一 Q4 (`4、Q：如何发现网站中存在的死链接？`), the page lists `抓取异常工具` and `参考爬虫软件：此类工具可以爬取全站所有链接并分析页面状态` without saying they fail on content dead links. In § 二 (`教你如何处理死链页面`) and § 三 Q1 (`1、【死链提交】工具可以识别403、500等无效数据吗？`), every remedy on the page *is* setting HTTP 404 (`将需处理的页面设置404页面` / `"页面设置404，一定是404页面"` (9u, 16 chars) / `"请一定设置为404"` (6u, 9 chars)) and submitting via `【死链提交】工具`. Furthermore, saying the remedy for a content dead link is "the route has to be made to answer a real 404" directly contradicts Q1 item (2)'s defining clause `无法设置为404` quoted three lines earlier, while claiming "The remedy ... is not a status code" contradicts both the page's 404-only remedy and the staged sentence's own second half.
   - **Fix:** Delete lines 19-28 (or keep only the status-code checker contrast explicitly marked `[INFERENCE]`), and replace with what S421 § 一 Q2–Q4, § 二, and § 三 actually state: why dead links matter (§ 一 Q3: `"不能给浏览用户提供任何价值"` 13u, `"对网站本身的访问体验和造成负面影响"` 17u, `"影响网站整体评价"` 8u), how the page says to discover them (§ 一 Q4: `抓取异常工具` and `参考爬虫软件`), and how the page instructs handling them (§ 二 / § 三: setting pages to 404 — `"页面设置404，一定是404页面"` 9u — and submitting via `【死链提交】工具`, which `"请一定设置为404"` 6u and `"不支持目录级提交"` 8u, with `"生效周期为1-2周"` 6u), noting as `[INFERENCE]` that the page gives no separate submission path for a content dead link that `无法设置为404`.

---

### S422 — `baidu-spider3-dead-link-recognition.md` (staged S408 -> lane S422 `baidu-spider3-dead-link-model.md`)

1. **`baidu-spider3-dead-link-recognition.md:2` and `:9-28` (zero quoted spans >= 6u; non-occurring English anchor in `source:`)**
   - **Page text:** The heading in `S422.html` line 276 is `『死链处理更及时—被黑低质页面全屏蔽』` (16u, 19 chars, count=1). The English string `the article body's dead-link section` in `source:` (and `the article body's dead-link section (the passage headed 死链处理更及时)` in `SOURCES.append.md:128`) occurs 0 times in `S422.html` and fails C5's `anchor not in texts[sid]` check. The entry also contains 0 double-quoted spans (C5 requires >= 3 page-unique spans).
   - **Fix:** Rename entry to `corpus/knowledge/baidu-spider3-dead-link-model.md`; set `source: S422 — https://ziyuan.baidu.com/wiki/867 — § 『死链处理更及时—被黑低质页面全屏蔽』 (发布日期 2016-06-30) — fetched 2026-10-25` and `verified-at: 2026-10-25`; use row anchor `§ 『死链处理更及时—被黑低质页面全屏蔽』 (发布日期 2016-06-30)`; embed >= 3 checked page-unique quotes.

2. **`baidu-spider3-dead-link-recognition.md:4` (recheck grep string is 37 units / 40 chars, over the 25-unit ceiling)**
   - **Page text:** `在死链处理方面，<span lang="EN-US">Spider3.0</span>启用了全新的死链识别模型，能识别协议死链，以及大多数内容死链、跳转死链等低质网页，` (`S422.html` line 276). The string `启用了全新的死链识别模型，能识别协议死链，以及大多数内容死链、跳转死链等低质网页` is 37u (40 chars).
   - **Fix:** Split into two raw, page-unique spans: `"启用了全新的死链识别模型，能识别协议死链，"` (19u, 21 chars) and `"以及大多数内容死链、跳转死链等低质网页，"` (18u, 20 chars).

3. **`baidu-spider3-dead-link-recognition.md:5, 9-14` (chronology inversion & sibling-page mechanisms asserted onto S422)**
   - **Staged:** l.7 `# The crawler sees the dead link that answers 200`; l.9-12 `Round 15 staged Baidu's own taxonomy of dead links: a protocol dead link is one the status code says so — 403, 404, 503 — and a content dead link is one where the server answers normally while the content is gone, and the operator says that kind cannot be set to 404. Read on its own, that reads like a gap in what any checker can see.`; l.14 `The operator's spider-3.0 announcement closes the loop from the other side.`
   - **Page text:** `S422.html` is published `2016-06-30` (six years *before* `S421.html`'s `2022-09-09`), and never mentions `200`, `403`, `404`, `503`, status codes, or `无法设置为404`.
   - **Fix:** State the dates explicitly (`S422` is `2016-06-30`; `S421` is `2022-09-09`), attribute the status-code definitions (`403`/`404`/`503`, `HTTP状态码200`, `无法设置为404`) strictly to `[S421]`, and tag any cross-page synthesis connecting S421's HTTP-200 content dead link to S422's model as `[INFERENCE]`.

4. **`baidu-spider3-dead-link-recognition.md:14-18` and `SOURCES.append.md:128` (dropped items `跳转死链` and `等低质网页`; dropped `被黑低质页面全屏蔽`; dropped `大多数` in conclusion; "machine-learning model" and "10 days / 40–80%" attached from the wrong section of S422)**
   - **Staged:** Entry l.14-18: `It says the crawler runs a new dead-link recognition model that identifies protocol dead links and most content dead links, and the section's heading promises faster handling rather than mere detection. So the content dead link that answers 200 is visible to this crawler: it is invisible to a status-code check, not to the search engine.` And staged `SOURCES.append.md:128`: `the operator says its spider 3.0 recognises dead links with a machine-learning model that identifies protocol dead links and most content dead links, and that indexing display timeliness improved from about ten days to 40–80% faster`.
   - **Page text:**
     - Dead-link heading (`S422.html` line 276, para 8): `『死链处理更及时—被黑低质页面全屏蔽』` ("Dead-link handling is more timely — hacked low-quality pages fully blocked").
     - Dead-link paragraph (`S422.html` line 276, para 10): `在死链处理方面，<span lang="EN-US">Spider3.0</span>启用了全新的死链识别模型，能识别协议死链，以及大多数内容死链、跳转死链等低质网页，简单点说就是在之前的版本，站点通过站长平台提交死链，处理速度可能非常慢，甚至快照在一段时间内仍然存在，但是<span lang="EN-US">Spider3.0</span>更新后，大约几天内就可以处理掉了。`
     - Earlier section (`『抓取、建库更快—提交的内容更容易被抓取』`, `S422.html` line 276, para 6 — *not* the dead-link section): `链接抓取和建库方面，开发了更强大的机器学习模型，来进行链接的质量预测，对库中所有的链接进行全局排序，对有价值链接的召回率提高<span lang="EN-US">95%</span>！索引展现时效性提升，原来是<span lang="EN-US">10</span>天左右，现在提升<span lang="EN-US">40%~80%</span>不等！`
   - **Fix:**
     - Do **not** call the dead-link model a "machine-learning model" and do **not** attach the `10天左右` / `40%~80%` indexing-display-timeliness figure to dead-link recognition: both belong to the earlier `『抓取、建库更快—提交的内容更容易被抓取』` section (`链接抓取和建库方面`, link quality prediction and global ranking).
     - In the dead-link section (`"『死链处理更及时—被黑低质页面全屏蔽』"`, 16u, 19 chars), render the full list and keep every qualifier: Spider3.0 enabled a brand-new dead-link recognition model that can recognize protocol dead links (`"启用了全新的死链识别模型，能识别协议死链，"`, 19u, 21 chars) as well as **most** (`大多数`) content dead links, **redirect dead links** (`跳转死链`), **and similar low-quality web pages** (`"以及大多数内容死链、跳转死链等低质网页，"`, 18u, 20 chars).
     - Do not generalize `大多数内容死链` ("most content dead links") into the unqualified "the content dead link that answers 200 is visible to this crawler"; keep "most" (`大多数`) and mark the cross-reference to `[S421]`'s HTTP-200 definition as `[INFERENCE]`.
     - State the actual timing and mechanism in the dead-link paragraph: in earlier versions, when a site submitted dead links through the webmaster platform (`"简单点说就是在之前的版本，站点通过站长平台提交死链，"`, 24u, 26 chars), processing speed could be very slow and snapshots still remained for a period (`"处理速度可能非常慢，甚至快照在一段时间内仍然存在，"`, 23u, 25 chars), whereas after the Spider3.0 update they can be processed within about a few days (`"更新后，大约几天内就可以处理掉了。"`, 15u, 17 chars).

5. **`baidu-spider3-dead-link-recognition.md:20-23` (invented "404 vs 200" framing attributed to S422)**
   - **Staged:** `The same passage gives the operator's own preference — if you want the best processing result, a protocol dead link is the best choice — which is the practical form of the taxonomy. A 404 is not merely more honest than a 200 that lies; it is the kind the operator says its systems handle best.`
   - **Page text:** `当然，如果你要追求最佳处理效果，协议死链是最好的选择。` (`S422.html` line 276, para 10).
   - **Fix:** Quote and render the sentence directly: `"当然，如果你要追求最佳处理效果，协议死链是最好的选择。"` (24u, 27 chars) — if you pursue the best processing result (`最佳处理效果`), a protocol dead link (`协议死链`) is the best choice. Delete "A 404 is not merely more honest than a 200 that lies; it is the kind the operator says its systems handle best" (S422 never mentions `404` or `200`; any link to S421's 403/404/503 examples must be tagged `[INFERENCE]`).

6. **`baidu-spider3-dead-link-recognition.md:25-26` (imprecise negative claim on snapshots/ranking and ambiguous reference to "the timing it quotes")**
   - **Staged:** `Two things the page does not say, worth keeping apart: it does not say a recognised dead link is removed from the index, and the timing it quotes concerns handling, not ranking.`
   - **Page text:** In the dead-link section, the page says of submitted dead links that previously `甚至快照在一段时间内仍然存在` (snapshots even remained for a period of time) and after Spider3.0 `"更新后，大约几天内就可以处理掉了。"` (15u, 17 chars), and the section heading states `被黑低质页面全屏蔽` (hacked low-quality pages fully blocked). Elsewhere on S422 (under `『时效性内容更多—有内容站点的更多机遇』`), the page *does* discuss ranking (`收录时间越近的排名会越靠前`).
   - **Fix:** Specify the exact timings and sections: the dead-link section's timing (`大约几天内就可以处理掉了`) concerns processing of dead links submitted via the platform (contrasted with snapshots remaining for a period), whereas the `10天左右` / `40%~80%` figure in the earlier `链接抓取和建库方面` paragraph concerns index-display timeliness (`索引展现时效性`), and ranking (`排名`) is discussed only in the later timeliness section (`『时效性内容更多—有内容站点的更多机遇』`).

## SAFE-TO-REUSE LINES:

- **`baidu-dead-link-taxonomy.md` (for `baidu-dead-link-types.md`):**
  - `l.9`: "The operator's own definition of a dead link is wider than the HTTP status a server returns." (accurate summary of Q1 A).
  - `l.10-17` core structure (definition -> split into protocol vs content dead links -> protocol examples 403, 404, 503 -> content dead link normal status, changed to non-existent/deleted/permission -> returns HTTP 200 and cannot be set to 404), **after** restoring the dropped qualifiers (`一般是指`, `包括`, `明确表示`, `等`, `等与原内容无关的信息页面`) and adding the checked quotes (`"死链一般是指页面已经无效，"` 12u, `"无法对用户提供任何有价值信息的页面。"` 17u, `"协议死链和内容死链"` 9u, `"的TCP协议状态/HTTP协议状态明确表示的死链，"` 16u, `"服务器返回状态是正常的，但"` 12u, `"内容已经变更为不存在、已删除或需要权限"` 18u, `"服务器端返回HTTP状态码200"` 9u).
- **`baidu-spider3-dead-link-recognition.md` (for `baidu-spider3-dead-link-model.md`):**
  - `l.14-16` core observation that Spider3.0 enabled a new dead-link recognition model that recognizes protocol dead links and most content dead links, **after** restoring `跳转死链等低质网页` ("redirect dead links and similar low-quality web pages") and quoting `"启用了全新的死链识别模型，能识别协议死链，"` (19u) + `"以及大多数内容死链、跳转死链等低质网页，"` (18u).
  - `l.20-21`: "if you want the best processing result, a protocol dead link is the best choice" — accurate rendering of `"当然，如果你要追求最佳处理效果，协议死链是最好的选择。"` (24u).
  - `l.27`: "The scope of this finding is the crawler-side recognition and the operator's stated preference."

## VERDICT PER ENTRY:

- **`baidu-dead-link-taxonomy.md` (staged S403 -> lane S421 `baidu-dead-link-types.md`): RE-DRAFT (reusing l.9-17 skeleton with qualifier restorations).** Lines 9-17 need qualifier fixes and embedded <=25u quotes; lines 19-28 must be replaced because they contain zero quotes, assert ungrounded crawler/ranking claims, and state a remedy ("is not a status code ... or the route has to be made to answer a real 404") that contradicts both Q1's `无法设置为404` and § 二–三's 404-only submission workflow.
- **`baidu-spider3-dead-link-recognition.md` (staged S408 -> lane S422 `baidu-spider3-dead-link-model.md`): RE-DRAFT (reusing l.14-16 and l.20-21 renderings).** The staged file has zero quotes, a non-occurring English anchor in `source:`, a 37-unit recheck grep string, a reversed 2016-vs-2022 chronology, omitted categories (`跳转死链等低质网页` and `被黑低质页面全屏蔽`), and (in `SOURCES.append.md:128`) attaches the earlier section's machine-learning model and `10天`/`40%~80%` indexing-timeliness figure to the dead-link section.

VERDICT: Both staged entries require re-drafting under their lane names (`baidu-dead-link-types.md`, `baidu-spider3-dead-link-model.md`) with <=25u/<=40c raw quotes from S421/S422, restored CJK qualifiers (`一般是指`, `包括`, `明确表示`, `等`, `等与原内容无关的信息页面`, `大多数`, `跳转死链等低质网页`), corrected section attribution (S422's ML model and 10-day/40-80% figures belong to `链接抓取和建库方面`, not `死链处理方面`), and removal of S421's self-contradictory remedy prose.
