# RevengerStaged

ATTACKS: the three staged candidates in `/home/vgpnk/Projects/shokuknow/merge/kake/knowledge/corpus/knowledge/` — `yahoo-japan-link-target-crawl-restriction.md` (staged id S367, page 002852), `yahoo-japan-deleted-url-recrawl.md` (S375, 002856), `yahoo-japan-soft-404-recrawl.md` (S376, 002857) — against the landed entries at `a450e43e696d032e3ac308383f6b3394e0c92860`: `corpus/knowledge/yahoo-japan-link-target-crawl-restriction.md`, `yahoo-japan-deleted-url-recrawl.md`, `yahoo-japan-nonexistent-url-recrawl.md`, plus rows 157/165/166 of `corpus/SOURCES.md` and the staged rows `SOURCES.append.md:87,95,96`. Staged file names below: **LT** (link-target), **DU** (deleted-url), **S4** (soft-404).

## Evidence (commands run, output as observed)

1. `git show <rev>:corpus/knowledge/<each>.md` for the three landed bodies; the staged files read whole. Staged ids at the landed rev: S367 kept; S375→**S419**; S376→**S420**; the staged path `yahoo-japan-soft-404-recrawl.md` does not exist at the rev (`git ls-tree` on `corpus/knowledge` lists `yahoo-japan-nonexistent-url-recrawl.md` instead).
2. `python3 -B .ufo/waves/round-56/span_tools.py window {S367,S419,S420}` → article text 550 / 317 / 291 characters. Each page carries 2–3 sentences; S367 carries five body lines (framing sentence, two sub-headings, two examples, two glosses).
3. **Quote-coverage map** (this seat's own script): every `> "…"` span and every fenced example in a landed entry was located in its page's article window, the matched characters marked, and the maximal uncovered runs printed. Result: S419 and S420 have **no uncovered substantive run** except the title, `更新日`, the date, and `。`/`また、` punctuation. S367 leaves exactly four substantive runs uncovered: `のほかに、`, `上記の例は、「`, `」という意味を持ちます。`, and the two entity-escaped `<meta …>` lines.
4. `span_tools.py check` on ten spans: staged DU quote = **46 units**, staged S4 quote = **29 units** (both raw, unique, in-content) — over the 25-unit ceiling as single spans; landed splits them into 2 and 3 spans.
5. Token absence in the article windows: S367 `個別リンク` = 0 in article, 1 in the whole body — in the `<div class="tag-area">` URL field (`<strong>個別リンクURL</strong>：`), i.e. boilerplate. S419 `コスト`/`予算`/`アプリケーション`/`恒久`/`永久` = 0. S420 `タイポ`/`ルーティング`/`キャンペーン`/`改名`/`永久`/`スタイル`/`誤り` = 0.
6. `git show <rev>:corpus/SOURCES.md` → 158 rows; `grep -E '\| S(192|199|200|201) \|'` → **0** (the four ids the LT entry cites as lane ground do not exist at the rev); S367/S372/S374/S419/S420 present at rows 157/158/154/165/166.
7. Staged rows vs landed rows: LT row says "the meta tag, the server header **and the per-link form**"; landed row 157 says "the meta tag and the server header, **beside the per-link attribute S374 holds**". DU row says "the operator's **remedy is a not-found response**"; landed row 165 says "**the 404 check it asks for**". S4 row says "**a routing mistake**"; landed row 166 says "a URL that has no page".
8. `MERGE-REPORT.md:75,83,84` → all three staged paths are `new-file` with no duplicate-target note and no folding instruction.

## OBSERVATION TABLE:

| # | staged observation (file:line) | page support / landed state | verdict |
|---|---|---|---|
| 1 | LT:9-11 lane ground = S201, S192, S199, S200 | landed L8-9 cites S374 + S372; none of those four ids is a row at the rev (158 rows, 0 hits) | dropped on purpose — lane bookkeeping (stale cross-ref ids) |
| 2 | LT:11-13 "the lane did not hold the other half: how a page refuses the crawl of its links … separate from whether the page itself is indexed" | landed L8-10 "This page states a third surface … without refusing itself" | carried |
| 3 | LT:15 "The operator names three routes for it." | page line 5 names three methods; landed L8-9 + L14-29 | carried |
| 4 | LT:15 "The page's own links can carry the attribute form." | landed L27-29: pointer to 002851, "states no semantics for the attribute" | carried (sharpened) |
| 5 | LT:15-16 "The page's head can carry a meta tag." | landed §The meta tag, L31-57 | carried |
| 6 | LT:16 "And the server can carry a header:" | landed §The server route, L80-99, `X-Robots-Tag` quoted, delivery marked [INFERENCE] | carried |
| 7 | LT:18 quote `X-Robots-Tag: NOFOLLOW` | landed L92 verbatim | carried |
| 8 | LT:20 "The meta-tag form is the one that carries the distinction …" | landed L45-57, both glosses quoted raw in pieces | carried |
| 9 | LT:20-24 the two values `index,nofollow` / `noindex,nofollow` | landed L41-43, L72-78 (fences entity-decoded — see LOST (d)) | carried |
| 10 | LT:24-25 "the same refusal can be applied to an individual link URL rather than to the page's whole link set" | **not on the page**: `個別リンク` 0× in the article, 1× in the tag-area URL field; landed L103-105 denies it by name | dropped on purpose — unsupported |
| 11 | LT:27-30 "three documented ways … the choice changes whether the page itself stays in the index" | landed L76-78: the two glosses separate exactly that | carried |
| 12 | LT:30-31 "A blanket `noindex` on such a page is the wrong instrument, and the operator's own page says so." | page line 11 offers `noindex,nofollow` as a case (`という場合には`), evaluates nothing; landed L69-70 keeps も as addition, not preference | dropped on purpose — unsupported |
| 13 | LT:33-34 scope note | landed L124 | carried |
| 14 | LT:7 title "…a separate decision from refusing the page" | landed L6 retitled; L10 keeps "without refusing itself" | carried (wording) |
| 15 | DU:9-10 "The operator explains a recurring complaint in one page …" | page line 5 states a condition; no complaint, no history | dropped on purpose — unsupported framing |
| 16 | DU:10 "The diagnosis is the response status:" | landed §The condition, L10-21 | carried |
| 17 | DU:12 quote (46 units) | landed L18-19, split into `クローラーは削除されたウェブページと認識できず、` + `そのウェブページを巡回し続ける可能性があります` | dropped on purpose — over ceiling (as one span) |
| 18 | DU:14-15 "no way to tell the page is gone, so it keeps crawling it" | landed L21 keeps 可能性があります | carried |
| 19 | DU:15-16 "The operator's remedy is to answer with a not-found status instead" | page says `確認してください` (confirm); landed L29 renders check-not-change | dropped on purpose — inflation |
| 20 | DU:16-17 "where the server cannot be configured that way, … meta tag in the error page's head" | landed L31-38, three qualifiers | carried |
| 21 | DU:19-20 "a deletion is only a deletion if the server stops answering with success" | landed L6 title + L21 | carried |
| 22 | DU:20-21 "one the **application** still serves with a 200 … **crawl cost** … still being paid" | page's subject is サーバー; `アプリケーション`/`コスト`/`予算` = 0; landed L53-54 denies both; also 可能性 → certainty | dropped on purpose — unsupported + inflation |
| 23 | DU:23-24 scope note | landed L56, L62 | carried |
| 24 | DU:7 title "…cannot delete" | landed L6 "…cannot drop" | carried (wording) |
| 25 | S4:9-10 "sibling of the deleted-URL case" | landed L55, L72-74 | carried |
| 26 | S4:9-10 "a typo in a link, a route that was renamed, a campaign page that was retired" | **not on the page**: `タイポ`/`ルーティング`/`キャンペーン`/`改名` = 0; landed L16 "the page names no cause such as a typo or a renamed route" | dropped on purpose — unsupported |
| 27 | S4:10-12 "an error page served with a success status is not read as an error page, so the crawler keeps coming" | landed L28-34 | carried |
| 28 | S4:12 "the remedy is the same status the deletion case asks for" | landed L50 sharpens it: S419 asks to check, S420 asks to set | carried (sharpened) |
| 29 | S4:14 quote (29 units) | landed L42-48, split into three spans | dropped on purpose — over ceiling (as one span) |
| 30 | S4:16-17 index-refusal meta tag in the error page's head | landed L52-70, `インデックス拒否` kept distinct from S419's `インデックスへの登録拒否` (L74) | carried |
| 31 | S4:19-20 "one rule in two places: the crawl loop follows what the server answers, not what the site intends" | landed L74 keeps the shared-statement list, not the maxim | dropped on purpose — editorial synthesis |
| 32 | S4:20-21 "a **styled** error page … converts every mistake into a **permanent** crawl target" | page says `巡回を続けます`; `スタイル`/`永久` = 0 | dropped on purpose — inflation |
| 33 | S4:21-23 "the two … are the same defect with different triggers" | landed L74 states what the two bodies share and what differs, without asserting defect identity | dropped on purpose — editorial synthesis |
| 34 | S4:25-26 scope note | landed L94 | carried |
| 35 | S4:7 title "A routing mistake served with success …" | landed L6 retitled to the page's own subject; "routing mistake" unsupported (see #26) | dropped on purpose — unsupported (title) |

Front matter, all three files (not counted as body observations): section cell `→ サーバーで設定する方法` (LT:2) → landed names both sub-headings = **dropped, correction**; staged id S375/S376 → S419/S420 = **dropped, pre-renumber id**; staged file name `soft-404-recrawl` → `nonexistent-url-recrawl` = **dropped, correction** (the page never uses the term; landed marks it [INFERENCE] at L34); `fetched 2026-10-24` / `verified-at` / `-> 1 (ran 2026-10-24)` on all three → landed `2026-10-25` + retained bodies and `receipts.json` = **dropped, 2026-10-24 date** (3); `ground: per-host crawl hygiene` on all three → landed `per-engine` on all three = **dropped, taxonomy** (3, consistent this round); recheck probes re-pointed in all three (LT `X-Robots-Tag: NOFOLLOW`, DU/S4 the full sentences) → landed narrower probes, still `-> 1` against curl arm and retained body = **carried**.

Tally: 35 body observations — **22 carried, 13 dropped on purpose, 0 lost**.

## LOST POINTS:

**Zero staged observations are LOST.** Every staged observation that is page-stated is present in the landed entry: the coverage map (Evidence 3) leaves no substantive page sentence uncovered in S419 or S420, and in S367 only the connective and the gloss frame, both of which the landed prose renders. The round-55 result (five page-stated losses) **does not reproduce on these three files** — the reason is mechanical: these pages carry 2–3 sentences each and the landed entries quote all of them, while the round-55 pages (S372/S373/S418) carried worked examples the landed text skipped.

Four page-text gaps remain; none is a staged loss, and (a) is a landed defect:

**(a) S367 — the connective the landed gloss mis-places (landed defect).** Landed L21 says "ほかに (besides) **opens** the sentence"; the raw body is `…<a href="…002851.php">rel=&quot;nofollow&quot;属性を使った指定方法</a>のほかに、HTMLのメタタグで指定する方法と、…` — ほかに closes the rel=nofollow clause, it does not open the sentence. The connective is also unquoted: the landed span is `HTMLのメタタグで指定する方法と、` (13 u). Located span, verified `check S367` = 17 units, raw substring, in-content, count 1:
> `のほかに、HTMLのメタタグで指定する方法と、`
Proposed sentence (replacing landed L21-22's "opens the sentence"): "のほかに、 closes the rel=nofollow clause: the two methods that follow are additional to it, and 巡回制限は governs all three." Note `属性を使った指定方法のほかに、` is **not** a raw substring — the `</a>` sits between — so the 17-unit span above is the only single-span carrier.

**(b) S420 — the status is quoted but its return is not.** Landed quotes `サーバーが「HTTP 200 OK」` (L18) and then jumps to `エラーページを表示する設定にしていると、` (L22); the coverage gap is `のステータスを返して`. The rendering at L20 says "the server answers with the status", but no span carries 返して — on an entry whose thesis is that the status is what the crawler reads. Located span, `check S420` = 12 units, raw, in-content, count 1:
> `「HTTP 200 OK」のステータスを返して`
Proposed: quote it as the second span of §The condition, before `エラーページを表示する設定にしていると、`.

**(c) S367 — the gloss frame.** `check S367`: `上記の例は、` (5 u) and `という意味を持ちます。` (10 u), both raw, unique, in-content. Landed L55-56 describes them in prose ("上記の例は in front of the gloss and という意味を持ちます after it mark it as the example's meaning") but quotes neither. Optional restore; the prose carries the meaning.

**(d) S367 — the two examples are entity-decoded, so the Quote-classes claim overreaches.** Landed L41-43 and L72-74 print `<meta name="robots" content="index,nofollow">` / `…noindex,nofollow">`; the retained body writes `&lt;meta name="robots" content=&quot;index,nofollow&quot;&gt;`, and both fence strings return `raw_substring: False`. Landed L119-121 nevertheless states "Each quotation is a raw substring of … S367.html". The staged text wrote the same examples unescaped inline, so this is carried-through, not a staged loss — but the landed claim needs scoping to the `> "…"` spans, or the fences need the escaped form.

## DROPPED ON PURPOSE:

13 body observations, by primary reason:

| reason | count | rows |
|---|---|---|
| unsupported — the page states nothing of the kind | 6 | LT#10 (per-link URL: `個別リンク` only in the tag-area URL field), LT#12 (blanket noindex "wrong"), DU#1 (recurring complaint), DU#22 (application attribution), S4#26 (typo/renamed route/campaign page), S4#35 (title "routing mistake") |
| inflation — page-stated fact overstated | 2 | DU#19 (`確認してください` → "remedy is to answer with a not-found status"), S4#32 (`巡回を続けます` → "styled" / "permanent"); DU#22 also carries the 可能性 → "still being crawled" inflation |
| over ceiling (25 units) as a single span | 2 | DU#17 (46 u), S4#29 (29 u) — both landed as 2 and 3 spans |
| editorial synthesis, no page sentence | 2 | S4#31 ("the crawl loop follows what the server answers"), S4#33 ("the same defect with different triggers") |
| lane bookkeeping — stale cross-ref ids | 1 | LT#1 (S192/S199/S200/S201: 0 rows at the rev) |

Front matter, by reason: pre-renumber id **2** (S375→S419, S376→S420); 2026-10-24 date **3 files** (plus the three `ran 2026-10-24` recheck annotations); ground taxonomy per-host→per-engine **3**; under-labelled section cell **1**; filename correction `soft-404`→`nonexistent-url` **1**. Carried unchanged: the three recheck probes (re-pointed, still `-> 1`), the three scope notes, the per-page `更新日 2010年11月24日`.

## What the staged author was doing, and whether the landing serves it

`MERGE-REPORT.md:75,83,84` lists all three as `new-file` — no folding instruction, so the adopt step was a straight copy. All three staged entries share one posture: state the page's mechanism, then state what the page does *not* say. The landing keeps that posture and strengthens it (retained bodies + `receipts.json`, the [INFERENCE] marks on `X-Robots-Tag` delivery and on the term "soft 404", the S419-vs-S420 verb split at landed S420 L50, the S419/S420 `インデックスへの登録拒否` vs `インデックス拒否` split at L74). What the landing did **not** keep is exactly the staged text that went past the pages: the per-link route (LT#10), the "wrong instrument" verdict (LT#12), the "remedy" verb (DU#19), the application attribution and crawl cost (DU#22), the invented URL causes (S4#26) and the styled/permanent framing (S4#32). Every one of those is a staged overreach, not landed attrition — the staged text is the weaker side of the three.

VERDICT: The landed three drop 13 staged observations and lose **zero** page-stated ones — all 22 page-supported staged points survive, and the 13 drops are six unsupported claims, two inflations, two ceiling splits, two editorial syntheses and one stale cross-ref; the only real defects found are landed-side: a mis-placed ほかに gloss at S367 L21, an unquoted 返して at S420 L18-22, and a Quote-classes claim at S367 L119-121 that the entity-decoded fences do not satisfy.

Writes: this report only. Lane repo, lane jj state and lane git index untouched; every git call was read-only (`show`, `ls-tree`, `ls-tree -r`); no selftest or counter was run; the staged tree and `/home/vgpnk/Projects/shokuknow` were read only.
