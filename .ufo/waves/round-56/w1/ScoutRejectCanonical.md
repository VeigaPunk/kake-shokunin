# ScoutRejectCanonical

Candidate: `/home/vgpnk/Projects/shokuknow/merge/kake/knowledge/corpus/knowledge/yahoo-japan-canonical-notification.md` (staged row S388).
Body: `.ufo/waves/round-56/sources/S388.html` (archives/003036.php, 9681 bytes, HTTP 200, fetched 2026-10-25T22:02:43Z, sha256 `115b4353…7a56` per `receipts.json`).
All measurements are against that retained body, read-only (python via `span_tools.py` helpers; no live fetch, no fleet or lane mutation).

## TESTS:
T1. `source:` section label `§ 本文（内容が重複する複数のURLをまとめる方法）` — **FAIL, label not in body.**
 - Full label: 0 occurrences. The tail `内容が重複する複数のURLをまとめる方法`: 0 occurrences. `本文` occurs 3 times, only as skip-link image alt text (`このページの本文へ`, `ここから本文です`, `本文はここまでです`, offsets 1366/2308/6377), never as a heading.
 - Actual headings (byte offsets in body): h2 @2593 `内容が重複する複数のURLをまとめるよう、検索エンジンに通知` (page title; also in `<title>`, nav list); h3 @3867 `<link rel="canonical" href="">の記述方法と機能` (raw `&lt;link rel=&quot;canonical&quot; href=&quot;&quot;&gt;の記述方法と機能`).
 - The quoted span (offset 4266) sits under the h3 @3867, so the correct section is the h3, not the invented "本文（…方法）". The label looks synthesised from the title (`…まとめる方法` vs the real `…まとめるよう…`). Violates QUALITY r53 "A source locator points to the section containing its quote".
 - `更新日 2010年11月24日` occurs once (offset 2651): a page-header date, which r53 says is not a section date. Only acceptable as a header date, not as the section's.
 - `fetched 2026-10-24` / `verified-at: 2026-10-24` / `ran 2026-10-24`: the lane's retained fetch is 2026-10-25; the staged date is shokuknow's, not re-observed here. No contradiction, but nothing in the lane proves it.

T2. `recheck:` grep string `検索エンジンは、内容が重複するウェブページのクロール…自動的に判定します。` — **count PASS, length FAIL.**
 - `grep -F -c` on the retained S388.html: **1** (matches the staged `-> 1`). `str.count`: 1. It is on one line, so `-c` and occurrence count agree. Offset 4266, inside the article block (window 2593..4618). In none of S367/S419/S420 (page-unique vs adopted bodies).
 - Units: **98** (CJK chars + whitespace tokens by `span_tools.units`). Contract ceiling and QUALITY r55 "New quotes stay at or under 25 units": **98 > 25 → fails.** Not unit-compliant as a recheck string either; a page-unique <=25-unit tail (e.g. `最終的に重複とみなすかどうかを自動的に判定します`, 24 units, count 1, in-block, unique) exists, so the overrun is avoidable.
 - `--compressed` live replay: UNRUN (no network use authorised); count measured on the retained body only.

T3. Quoted spans in the entry prose — **only one quote exists and it is the 98-unit recheck string.** The prose has zero quoted spans, no `>`-block quote, no `[S388]` marker. QUALITY r55 requires >=3 page-unique spans per entry; entry has 1 (the recheck string, 98 units). Fail.
 - Candidate substitutes I measured (all raw substrings, single occurrence, in article block, absent from S367/S419/S420): `このタグの記述をほかの情報やデータとともに利用し` 24u; `最終的に重複とみなすかどうかを自動的に判定します` 24u; `参照してほしいウェブページを指し示す` 18u; `ほかの情報やデータとともに利用し` 16u. And `この記述は、Yahoo!検索だけでなくGoogle、Bingの検索エンジンにも共通の規格です。` is 28u (>25, unusable whole).

T4. Registry/index: `S388` is **not in `corpus/SOURCES.md`** (0 hits; lane max id is S418, S419/S420 are this round's new rows). Staged ids collide with nothing here but need a renumbered row (as S375→S419, S376→S420) before citation, per QUALITY r53 "source id resolves in this lane's own registry". No `corpus/README.md` Coverage-map row (r55 "an entry lands with its index row"). Both are fixable obligations, not merit failures.

T5. Held-style check: held Yahoo entries (e.g. `yahoo-japan-rel-nofollow-semantics.md`) quote in blockquote, mark `[S###]`, and use the real heading as locator; the staged one does none.

## CLAIMS:

(page = S388 body; line refs are entry lines)

- L9-10 "lane holds Google's canonicalization rules and its own static-canonical preflight" — SUPPORTED: `corpus/knowledge/canonical-selection.md` (S262, "a hint, not a rule") and `static-canonical-preflight.md` exist. "Not hold this operator's statement" — SUPPORTED (S388 unregistered).
- L10-11 "sharper than the practice guides tend to be" — editorial, no source; INFERENCE (the Yahoo page is not sharper than Google's own S262 "hint, not a rule", which the lane already holds).
- L13 "takes the tag as one piece of information among several, together with other data, and judges by itself whether duplicate" — SUPPORTED (`このタグの記述をほかの情報やデータとともに利用し、最終的に重複とみなすかどうかを自動的に判定します`), rendered in English.
- L14-15 "statement of intent, not an instruction that is obeyed" — INFERENCE (page says 通知 'notify' and 自動的に判定 'decides automatically'; "intent/obeyed" is the entry's gloss, not the page's words).
- L15-16 "exactly the question the lane's ledger kept open" — UNVERIFIED: no "ledger" in `canonical-selection.md`; PROVINCE.md says only canonical/JS rendering open. Presented as fact; I could not locate the ledger.
- L17 "Two supporting clauses matter" — SUPPORTED that both clauses exist on the page; relevance is editorial.
- L18-19 "specification shared with the other engines, so writing it once covers Google and Bing too" — **split:**
  - first half SUPPORTED: `この記述は、Yahoo!検索だけでなくGoogle、Bingの検索エンジンにも共通の規格です。` (offset 4378; sentence is the last of the 記述方法と機能 list).
  - "so writing it once covers Google and Bing too" — **INFERENCE, overreach: a behavioural guarantee the page does not make.** The page asserts a shared *format/規格* (the `<link rel="canonical">` syntax), not shared handling. The same page's preceding sentence says each engine weighs the tag with other data and decides itself, so the same tag can be honoured differently by each engine; the lane's own S262 says Google may select a different canonical. A 2010-11-24 page by one operator cannot attest Google's or Bing's current behaviour; S388 contains no quoted Google/Bing statement and the lane holds no Bing source (QUALITY r20 "Platform mechanism": platform behaviour needs a tier-A row for that platform; also `yahoo-japan-rel-nofollow-semantics.md:38` explicitly disclaims Google/Bing). The entry also contradicts its own L13-16 thesis (engine decides) with L18-19 (one write covers all).
- L19-21 "not the same as a 301 redirect: the redirected page keeps no content of its own" — SUPPORTED (`301リダイレクトの場合は、リダイレクト元のウェブページに内容がなく、自動的にリダイレクト先に遷移させられるという点が異なります`, 39u so unusable as a quote whole).
- L20-21 "a canonical page stays reachable and merely says which of the two the engine should prefer" — INFERENCE/partly WRONG in wording: page says the tag 指し示す ('points to') and 通知 ('notifies') that two URLs have the same content; the words "stays reachable" and "prefer" (優先/prefer: 0 occurrences) are not on the page. "Reachable" is a reasonable contrast to the redirect clause but unstated.
- Date/scope: entry never discloses the page is a 2010 tips page (only in the header line), and never states the "注意" recommendation (normalise URLs where possible) that the page itself ranks as the practical advice.

## DECISION:

**REJECT as staged.** (ADMIT/REJECT on merit under `corpus/QUALITY.md`.)

Merit grounds, independent of the theme limit:
1. Locator fails: the `source:` section label does not occur in the body (0 hits); the real section is the `…の記述方法と機能` h3. QUALITY r53 "A source locator points to the section containing its quote".
2. The only quote/recheck span is 98 units (> 25); QUALITY r55 ceiling and the round-56 contract ceiling; <3 page-unique quoted spans (1).
3. Headline practical claim "writing it once covers Google and Bing too" is unsupported inference stated as practice guidance, contradicting the entry's own thesis and the lane's S262 hint-not-rule; no Google/Bing tier-A row backs engine behaviour.
4. S388 unregistered in lane `corpus/SOURCES.md`; no README coverage-map row.

Theme: the entry (canonical notification) is outside round-56's single theme (Yahoo! JAPAN crawl handling: deleted URL, non-existent URL, link-target restriction) — a theme-limit rejection exists independently of items 1-4: not one of the three contract-named entries, and contract says only S367/S419/S420 are adopted. Merit rejection (1-4) also stands independently of theme: even in a canonical-themed round the staged file would fail the gate as written.

Flip condition (to ADMIT in a later, canonical-themed round): (a) register S388 as a new lane row with section `<link rel="canonical" href="">の記述方法と機能` and header date `更新日 2010年11月24日` labelled as page-header date; (b) replace the 98-unit recheck string with a <=25-unit page-unique span (e.g. 24u `最終的に重複とみなすかどうかを自動的に判定します`, count 1) and add >=2 more <=25u raw page-unique spans (e.g. `参照してほしいウェブページを指し示す`, `ほかの情報やデータとともに利用し`) in blockquotes with `[S###]` markers; (c) delete or rescope L18-19 to "the page says the format (規格) is common to Yahoo!, Google and Bing; it does not say the engines treat it identically", and drop unsupported "prefer/reachable/ledger" wording or source them; (d) add the README coverage-map row; (e) retained-body recheck counts 1.

VERDICT: REJECT — section label absent from body, 98-unit recheck string, 1 quoted span, unregistered S388, "covers Google and Bing too" is unsupported inference; also out of round-56 theme.
