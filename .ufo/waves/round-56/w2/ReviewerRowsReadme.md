# ReviewerRowsReadme

Scope: `corpus/SOURCES.md` registry diff and `corpus/README.md` / `PROVINCE.md` index edits, base
`e48354b7` → tip `a450e43e`. Verified against retained bodies `.ufo/waves/round-56/sources/S367.html`
(002852), `S419.html` (002856), `S420.html` (002857), `receipts.json`, the three new entries, and
`corpus/lessons/round-56.md`.

## ROW DEFECTS:

- **LOW — S419 scope headline drops the page's possibility hedge** (`corpus/SOURCES.md`, S419 row,
  scope cell): "**A deleted URL answered with 200 OK stays in the crawl**" asserts certainty; the
  page states it as a possibility — `そのウェブページを巡回し続ける可能性があります`
  (`S419.html:104`), and the entry itself keeps the hedge (`yahoo-japan-deleted-url-recrawl.md`
  §The-condition: "stated as 可能性があります, a possibility; the page does not say the crawl always
  continues"). The teaches cell right below it is weaker ("may keep being crawled" is not written —
  it says "a 200 OK on a removed page leaves it crawled"), so the headline is also slightly
  stronger than its own row. The README coverage cell for the same entry does carry the
  "possibility" qualifier, so the defect is confined to this one cell's bold headline.
- **LOW — S419 teaches "leaves it crawled" is also unhedged** (same row, teaches cell): "a 200 OK
  on a removed page leaves it crawled" reads the possibility as outcome; the page's stated outcome
  is non-recognition plus possible continued crawl. Same root cause as above; severity stays LOW
  because the substance (200 OK hides deletion from the crawler) is on the page.

## README DEFECTS:

- none.

## PROVINCE DEFECTS:

- **LOW — round-56 section conflates S419's check-request with S420's set-request**
  (`PROVINCE.md:414-415`): "the page asks that the server return `HTTP 404 Not Found`" describes
  S419, but the page asks the publisher to *confirm whether* the server returns 404
  (`確認してください`, `S419.html:105`); setting it is S420's request (`設定を行ってください`,
  `S420.html:105`). The very next clause reads "(…) the same 404 request and fallback" for S420,
  erasing the check-vs-set distinction the entry and the lesson both preserve. The retained
  unedited round-55 sentence (crawler-address, user-agent-list, deleted-URL pages "not adopted this
  round", `PROVINCE.md:398-399`) is correct as history and is explicitly superseded for the
  deleted-URL page by the new section — no defect there.

## CLEAN CHECKS:

SOURCES.md (per checklist):
- S367: byte-level diff is confined to the used-by cell
  (`+ corpus/knowledge/yahoo-japan-link-target-crawl-restriction.md`); cells 2–11 verified identical
  base↔tip; the in-place change is the class rule 2 permits and it is logged old→new in
  `corpus/lessons/round-56.md` §Registry changes.
- S419/S420: 11 cells each (NF=13 under `-F'|'`), so no unescaped `|` inside any cell; both
  appended after S418, ids unused at base (base registry 156 rows, max id S418).
- Title cells: text between the row's first and last ` — ` is `削除したウェブページが巡回され続ける`
  and `存在しないウェブページが巡回される`; both occur verbatim inside the retained pages'
  `<title>` (`S419.html:33`, `S420.html:33`); canonical URLs `…/002856.php`, `…/002857.php` match
  the receipts and the pages' own 個別リンクURL fields.
- Anchor headings: both `§` cells name the page h2 (`S419.html:100`, `S420.html:100`) with the
  printed 更新日 2010年11月24日 (`:101`); locators, within the span ceilings.
- teaches grounded: S420's cell matches `S420.html:104-105` exactly including the flat
  `巡回を続けます` (no hedge on this page), the 404 request, and "names no crawler, no interval and
  no index outcome"; S419's substance (recognition failure, 404, unnamed head meta-tag fallback)
  is on the page — only the hedging defect above.
- Tier A: `docs` rows for the operator's own crawl documentation are primary-for-scope, consistent
  with the held sibling rows S367/S372/S373/S374/S418; kind `docs` + tier `A` pass the frozen
  census enum (no community-A inflation).
- status `mined` + real used-by: all three used-by paths exist at tip and each entry's `source:`
  header names its row (S367, S419, S420 respectively). Sibling rows' used-by cells were correctly
  not extended: the established convention lists only the entry a row primarily grounds (S372's
  used-by already omits `robots-txt-rules.md` and `crawl-scope-per-host.md`, which cite it, at
  base).
- recheck `180d`: matches the uniform cadence of the held Yahoo! JAPAN rows; the operative curl
  recheck lives in each entry's `recheck:` front-matter line, verified against `receipts.json`
  sha256s and 2026-10-25 fetch stamps.
- CORPUS rule 1 gate records exist for all three rows (URL, access date, ≤25-unit located quote
  with sha256): S419 quote `クローラーは削除されたウェブページと認識できず、` is a raw substring at
  `S419.html:104`; S420 quote `クローラーはエラーページとみなさず、` at `S420.html:104`; S367 quote
  `インデックスへの登録を許可する` present in `S367.html`. The S367 re-open also logs the fresh-GET
  equality and the 31→≤24-unit quote re-cut.

README.md:
- Three coverage rows (lines 70–72) each carry 3 fields, no pipes; every clause verified against
  the entry: "meta tag and server routes, page-vs-link-target indexing split, two glossed values"
  = S367 entry's three sections; "status 200 OK vs 404 Not Found check, error-page head meta tag
  with unnamed value, possibility and cannot-be-configured qualifiers" = S419 entry including its
  preserved hedges; S420 row's prose = the entry's stated content verbatim in compression.
- Ground-map row (`README.md:100`): 4 fields; the three entry paths equal the new files; the row
  set `S367 S419 S420` equals the union of the used-by cells of those three entries at tip;
  "r56 (lands this round)" matches the round-55 row's convention.
- Intro edit: "the round-56 row at the round-56 final revision (158 rows, S419 and S420 added),
  not at base `e48354b7…`" — tip count 158 and base count 156 both verified by grep; the added
  sentence "the round-56 row's three entry paths are absent at its base … and S419 and S420 are
  not in that registry" verified against the base tree (all three `git show` fail; zero matches).
- "the nine per-engine entries" + cites: round-52 section spans `PROVINCE.md:367-384` so `:382`
  resolves inside it; round-55 spans `:385-407` so `:397` resolves inside it; `:408` is exactly the
  new round-56 heading line. Other cites in the paragraph (`:25-26`, `:344`, `:361`) are unchanged
  and still resolve.

PROVINCE.md:
- New section opens at line 408; factual claims verified: re-grounded fetch date matches
  `receipts.json` (2026-10-25T22:02Z, HTTP 200); the S367 description (index,nofollow leaves own
  registration permitted; noindex,nofollow refuses both; `X-Robots-Tag: NOFOLLOW` server route)
  matches page and entry; the "no URL was served under test and no crawl was observed" disclaimer
  matches the entries' scope notes.
- Superseded-sentence handling: the round-55 "not adopted this round" sentence is untouched and
  remains true for the two pages not adopted; the round-56 paragraph declares supersession for the
  deleted-URL page and carries the S387/S388/S389 rejects to
  `corpus/lessons/round-56.md` §Gate, where each staged rejection indeed records reason + flip.

VERDICT: registry and index edits are structurally sound and grounded; only wording-grade defects — the S419 scope/teaches cells drop the page's possibility hedge, and PROVINCE.md:414-415 conflates S419's 404-check with S420's 404-set — both LOW, no structural or provenance failures.
