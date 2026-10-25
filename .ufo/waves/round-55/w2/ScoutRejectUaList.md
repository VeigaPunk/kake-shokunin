# ScoutRejectUaList

ATTACKS: unadopted staged candidate `corpus/knowledge/yahoo-japan-user-agent-list-unreadable.md` (staged id S364) — https://support.yahoo-net.jp/PccSearch/s/article/H000007955 — judged against the lane bar and province.

## CANDIDATE:

File: `/home/vgpnk/Projects/shokuknow/merge/kake/knowledge/corpus/knowledge/yahoo-japan-user-agent-list-unreadable.md`.
`source:` line: `S364 — https://support.yahoo-net.jp/PccSearch/s/article/H000007955 — § the served document's title element (the document carries no article heading and no section title) — fetched 2026-10-24`.
`ground:` line: per-host crawl hygiene — the operator's own crawler user-agent list, and why the lane cannot hold it.
Staged registry row (shokuknow merge `SOURCES.append.md` line 84): S364, tier A docs, locator "§ the served document's title element"; gloss claims the operator publishes the crawler user-agent list "only through a page delivered as its generic help shell".
Unadopted in round 55 (not in the collision/adoption set; `assimilation/staged-ids` lists S364; only staged S380 → S418 was adopted).

## FETCH:

Command (one plain GET of the cited URL):
`curl -sS -L --max-time 60 -o <tmp>/page.html -w 'http_code=%{http_code} url_effective=%{url_effective} size_download=%{size_download}\n' 'https://support.yahoo-net.jp/PccSearch/s/article/H000007955'`
Observed: `http_code=200`, `url_effective=https://support.yahoo-net.jp/PccSearch/s/article/H000007955` (no redirect), `size_download=22864`.
sha256 (file bytes): `51f2b54fe741a8e3f9012582ee509a040ef9547083fa9e76ce861acca9a53f64`; bytes: 22,864; state: raw save of the 200 body.
Size cross-checks (two additional plain GETs of public docs, sizes only): article path again → 22,864; sibling path `https://support.yahoo-net.jp/SccSearch/s/article/H000007955` → 23,792 (HTTP 200). Campaign's earlier r9 raw at the same article path was 22,866 bytes (`sha256 da0444dedbb82dbf…`) — a ~2-byte run-to-run delta from per-request chrome (session/version fields, verified opcodes: `'o'→'webki'`, inserts/deletes around user-agent/version). So the candidate's exact "22,866-byte" figure is one fetch's snapshot, not a stable property.
Recheck argv reproduced on my saved bytes: `grep -F -c '<title>Yahoo!検索ヘルプ'` → 1.
Content observed (raw substrings): `<title>Yahoo!検索ヘルプ</title>` present once; `ユーザーエージェント` 0 ×; `クローラー` 0 ×; `H000007955` 0 ×; row title `ウェブページにアクセスするシステムのユーザーエージェントについて` 0 ×; 0 `<h1>`–`<h6>` tags; one `<noscript>` region containing the img alt `このページの閲覧はJavaScriptをオンにする必要あります。` and the text run `このページを閲覧するにはJavaScriptをオンにする必要があります。`.

## VERDICT TABLE:

| check | result |
|---|---|
| Claim on the page? | Partially. Title element, absence of UA/crawler strings, noscript notice: all reproduce on my fetch. Headline "operator publishes the UA list" is not on the page — only absence is verifiable. |
| Duplicate of held row by URL? | No. URL absent from `corpus/SOURCES.md` at a7a548e (grep -c = 0). Id S364 also absent. |
| Over-ceiling quote? | No. Candidate quote 5–6 units; my quotes ≤25. |
| Out-of-scope? | Partial. Topic is operator crawler-UA/hygiene (kake Frontier), but the content at stake needs rendered capture = tabi's instrument; the lane's quotable alternative is the operator's server-rendered page, which the lane does not hold. |
| Unreadable body / no content block? | Yes. Document has no `<h2>` at all → no span satisfies the counter's located-quote content-block rule; the only quotable strings are site chrome + JS-boilerplate. |
| Citations resolve? | No. Candidate cites lane holdings S192, S193, S195, S200 — none exist in `corpus/SOURCES.md` at a7a548e (grep -c = 0 each; S193/S195 appear in the lane tree only as quarantine `payload-absent` rows; campaign scope-7 file assigns S200 to a *merge duplicate-id record*, not a DNS-refusal rule; the operator's actual DNS-refusal page 002855 is not in the lane registry either). |
| Numbers reproduce? | No. "drop-noscript extraction yields 95 characters": measured 58 collapsed / 63 raw chars (95 is the keep-noscript collapsed count). "the lane's own extractor yields 162 characters": the lane's own `scripts/source_recheck.py` `html_text`→`normalize` yields 111 chars / 86 normalized; 162 is the *byte* length of the campaign extractor's keep-output (99 chars). |

Verdict: REJECT (as written) — reason: unreadable body (client-rendered shell; only chrome/boilerplate quotable; no content block/no h2, so the lane's located-quote discipline cannot bind any span), plus unresolved S192/S193/S195/S200 premises and reversed/misattributed mechanism numbers. Flip (ADMIT-LATER) requires: (a) restate as a dated lane-owned measurement (tier B own-work) with numbers re-derived from a pinned fetch (report: HTTP 200, 22,864 bytes, sha256 `51f2b54f…`) and a receipt; or (b) re-ground on the operator's quotable server-rendered page 002855 (`https://info-search.yahoo.co.jp/archives/002855.php`; my GET: HTTP 200, 8,703 bytes, sha256 `9ce5a4ab…`) with an in-scope, ≤25-unit quote about the DNS-lookup/crawler-name check method; in both cases drop/correct the S192/S193/S195/S200 references and dedupe against sibling staged candidate S368 (same URL, same recheck command).

## QUOTES:

(≤25 units per counter `units()`; raw substrings of my fetch; the document carries no HTML heading, so locators are structural.)

1. § document `<title>` element — `Yahoo!検索ヘルプ` — 5 units.
2. § `<noscript>` img `alt` — `このページの閲覧はJavaScriptをオンにする必要があります。` — 22 units.
3. § `<noscript>` text run — `このページを閲覧するにはJavaScriptをオンにする必要があります。` — 25 units (at ceiling).

## REGISTRY COLLISION CHECK:

- `git show a7a548e102b71bd16b0a6ddafa469393a2c98b69:corpus/SOURCES.md | grep -c 'support.yahoo-net.jp'` → 0.
- `grep -c 'S364'` in same registry dump → 0 (id free; row would be new).
- Whole corpus/ tree at build rev: `git grep -c 'support.yahoo-net.jp' a7a548e -- corpus` → 0 files (URL appears only inside retained wave sources as the operator's own nav link `https://support.yahoo-net.jp/PccSearch/s/`).

VERDICT: REJECT the staged candidate as written — unreadable client-rendered body with only chrome/boilerplate quotable and no content block, unresolved S192/S193/S195/S200 premises, and reversed numeric claims; ADMIT-LATER only after restating as a pinned measurement or re-grounding on the operator's quotable server-rendered 002855 page with corrected citations and dedupe vs S368.
