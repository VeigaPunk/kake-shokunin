# ReviewerEntryBasics
ATTACKS: corpus/knowledge/yahoo-japan-robots-txt-basics.md @ a7a548e102b71bd16b0a6ddafa469393a2c98b69 (claim C2, row S418) — quote truth, renderings, contrasts, header trio + recheck, scope, unit counts.

Method: entry read via `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show a7a548e…:<path>` (line numbers from `| cat -n`); retained body `.ufo/waves/round-55/sources/S418.html` read in full (393 lines). No LSP server exists for markdown/HTML at a pinned revision; all checks are `git show` + literal `grep -F` text checks — text fallback used deliberately, not presented as semantic proof.

## QUOTES:
Units recounted by script (CJK chars incl. fullwidth punctuation + non-CJK whitespace tokens); Count = plain-text occurrences in the retained body.

| Entry L | Span | Units | Substring | Count | Rendering faithful |
|---|---|---|---|---|---|
| 13 | 検索エンジンに対する要求を伝えるファイルです | 22 | yes | 1 | yes — request + search engine preserved |
| 18 | クローラーに巡回してほしくないウェブページ | 21 | yes | 1 | yes — negation ほしくない kept; "administrator" is the adjacent sentence's actor, derived on entry L15–16 |
| 21 | やディレクトリ (inline fragment) | 7 | yes | 1 | yes, minor: や is the non-exhaustive "and/or"; "(or directories)" sheds only that nuance and entry L21–22 states the sharing correctly |
| 24 | サイトマップの位置 | 9 | yes | 1 | yes |
| 31 | クローラーはrobots.txtの記述に従って | 14 | yes | 1 | yes — 記述 = "what robots.txt says" |
| 35 | サイト内のウェブページを巡回します | 17 | yes | 1 | yes — scope サイト内 kept ("inside the site") |
| 40 | クローラーによる巡回の際は | 13 | yes | 1 | NO — "on the occasion of a crawl" is faithful, but entry L42 appends "— per crawl, not once per site lifetime", a frequency guarantee the page never states → DEFECT 1 |
| 44 | まずサイトのルートディレクトリ | 15 | yes | 1 | yes — まず = first |
| 48 | （サイトの一番上の階層）にあるrobots.txtを探します | 21 | yes | 1 | yes — 探します = looks for; parenthetical glosses root as topmost level |
| 55 | robots.txtが設置されていなかった場合には | 16 | yes | 1 | yes — negation and 設置=placement kept |
| 59 | そのサイトに対する巡回制限はないものとみなして | 23 | yes | 1 | yes — site-scoping and みなして (treatment, not finding) kept |
| 64 | robots.txtが設置されていた場合には | 13 | yes | 1 | yes |
| 68 | その内容に従って巡回します | 13 | yes | 1 | yes |

All 13 spans ≤ 25 units (max 23).

## UNTAGGED BEYOND-PAGE:
- Entry L42, repeated L97: "per crawl, not once per site lifetime" — beyond the page and untagged; the page says only that at crawl time the crawler first looks for the file. This is the sole instance found: every other non-quoted statement checked is page-stated, and the one lane-mapping inference (L90–91) carries [INFERENCE].

## CONTRAST CHECKS:
1. L73–76 RFC side — robots-txt-rules.md:19 at rev: "an HTTP 4xx “unavailable” response means crawlers MAY access server resources, while an unreachable file due to server or network errors requires a crawler to assume complete disallow" → SUPPORTED.
2. L78–79 service scope — robots-txt-rules.md:15: "with the protocol, authority and port determining the scope"; crawl-scope-per-host.md:7: "Robots rules are discovered at the service's root" → SUPPORTED.
3. L8–9 lane holds the protocol and the host-root scope — same two lines → SUPPORTED.
4. L87–88 per-link attribute — yahoo-japan-rel-nofollow-semantics.md header at rev: S374, "what a link attribute says … about crawling a link target", body on rel=nofollow of `<a>` → SUPPORTED.
5. L83–85 refusal-settings pages = rows S372/S373 — receipts.json: S372 = …/002849.php, S373 = …/002850.php, matching the page's link hrefs and link texts サイト単位、ディレクトリ単位での巡回の拒否設定 1 / 2 → SUPPORTED.

## RECHECK:
- Ran the grep half of L3: `grep -F -c '検索エンジンに対する要求を伝えるファイルです' .ufo/waves/round-55/sources/S418.html` → output `1` (one matching line; the sole occurrence). Prints what the entry claims.
- `sha256sum …/S418.html` → 2b146a723e5d417de24f7bc64ad7adda4efbf9c6251438d89cfa88839d69312c — matches L95 `2b146a72…`.
- `wc -c …/S418.html` → 7559 — matches L95–96.
- receipts.json S418: httpStatus 200, bytes 7559, sha256 full match, fetchedAt 2026-10-25T20:40:14+00:00 — matches "HTTP 200 in `receipts.json`" and the L1 fetched date.
- Header trio L1 matches the page: `<h2>robots.txtとは？</h2>`, `<p class="update">更新日 2010年11月24日</p>`, URL = https://info-search.yahoo.co.jp/archives/002885.php.
- Curl half of the recheck: unrun (live fetch is outside this seat's assigned checks; the grep half was the mandated run).

## DEFECTS:
1. Entry L42 (echoed L97): rendering inflates 巡回の際は with "— per crawl, not once per site lifetime", a lookup-frequency guarantee the page does not state (the page binds the lookup to crawl time; it says nothing about recurrence). Minimal fix: L42 → "(rendered: on the occasion of a crawl by the crawler)"; L97 → "巡回の際は (on the occasion of a crawl)"; or keep "per crawl" and tag it [INFERENCE].

## NO-DEFECT CHECKS:
- Quote mechanics: 13/13 raw substrings, each occurs exactly once, units 7–23 (script recount; a segmentation excluding fullwidth punctuation only lowers counts — conclusion invariant).
- Directive-token claim (L83–84): scan of the whole retained body found 0 occurrences of user-agent / Disallow / crawl-delay / Sitemap: / allow: / `$` / `*` — "the page carries no directive token" is true at raw-byte level. Only directive-like text is the boilerplate `<meta name="robots" content="index,follow,noarchive,noodp" />` (robots-meta boilerplate, not visible content, not a robots.txt directive) — claim stands.
- Negation/scope qualifiers preserved: ほしくない (L20), ない (L61), なかった (L57), サイト内 (L37), そのサイトに対する (L61–62), まず (L46), root-directory gloss (L50–51).
- Renderings' supplied subjects (administrator L20, crawler L61) are the adjacent page sentences' actors — not inflation.
- "No status code, no redirect, no fetch failure, no cached copy" (L72–73): none present in the page's visible text; confirmed by reading the retained body.
- L96 parenthetical "(one unit per CJK character)" understates the frozen unit rule (omits the non-CJK-token half), but every quote is ≤25 under the full rule, so the claim it supports is true — noted, no defect.
- L89 negative ("no robots.txt was served and no crawl was observed") is lane-side attestation restated in the scope note (L100–102); the scope note claims no more than the page about page content.
- Seat bounds respected: only this report file written; no lane git/jj state touched.

## RESIDUAL RISK / GAPS:
- Live curl half of the recheck unrun; grep half verified against retained bytes.
- verified-at: 2026-10-25 is a lane attestation consistent with receipts fetchedAt, not independently reproducible from artifacts alone.
- S372/S373 entry bodies were not audited in this seat (only their URLs/identity as contrast targets).

VERDICT: quote-truth holds (13/13 substrings, each once, ≤25 units; hash/size/HTTP-200/recheck verified; all five contrasts supported) — one minor defect: entry L42/L97 inflates 巡回の際は with an unstated "per crawl, not once per site lifetime" guarantee; drop it or tag [INFERENCE].
