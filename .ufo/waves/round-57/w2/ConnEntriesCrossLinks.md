# ConnEntriesCrossLinks

Seat: ConnEntriesCrossLinks — cross-source pattern check for the two entries' cross-links.
All reads at the build under attack, lane revision `4b8c73050470ada9e6583f3b12d659d1bed6a17f` (`git show 4b8c730…:<path>`); verified at 2026-10-25.

## ATTRIBUTIONS:

### Entry baidu-dead-link-types.md (S421), line 95 (§ Cross-engine contrast)

| entry line | claim | held sentence (file:line) | verdict |
|---|---|---|---|
| S421:95 | Yahoo! JAPAN deletion entry holds `クローラーは削除されたウェブページと認識できず、` (the crawler cannot recognise the deleted web page) (S419) | yahoo-japan-deleted-url-recrawl.md:18 (block quote `> "クローラーは削除されたウェブページと認識できず、"`; rendered at :21) | TRUE — quote matches verbatim, confirmed by running `git show 4b8c730…:corpus/knowledge/yahoo-japan-deleted-url-recrawl.md` |
| S421:95 | its nonexistent-URL sibling holds `巡回を続けます` (it continues the crawl) (S420) | yahoo-japan-nonexistent-url-recrawl.md:36 (block quote `> "巡回を続けます"`; rendered at :38) | TRUE — quote matches verbatim, confirmed by running `git show 4b8c730…:corpus/knowledge/yahoo-japan-nonexistent-url-recrawl.md` |
| S421:95 | Both Yahoo pages concern a URL that answers `HTTP 200 OK`, and each asks that the server return 404 | S419: lines 12-14 quote `「HTTP 200 OK」のステータスを返すように` (200 OK condition); lines 25-27 quote the request to confirm the server is configured to return `「HTTP 404 Not Found」` (`確認してください`). S420: line 18 quotes `サーバーが「HTTP 200 OK」`; lines 46-50 quote the request to configure `「HTTP 404 Not Found」` (`設定を行ってください`) | TRUE — both pages state a 200 OK answer and ask for a 404 return; nuance: S419 asks to *check* the 404 setting, S420 asks to *make* it (S420:54 states the division), so the attribution's "each asks that the server return 404" is fair, confirmed by running the same two `git show` reads |
| S421:95 | The Google-side entry `corpus/knowledge/crawl-error-status-table.md` (S286) admits one sentence (Googlebot scales back when servers are detected to have trouble) | crawl-error-status-table.md:10 — "Google's crawl-errors page says Googlebot will scale back its crawling if it detects that your servers are having trouble (S286)." | TRUE — one admitted sentence, confirmed by running `git show 4b8c730…:corpus/knowledge/crawl-error-status-table.md` |

### Entry baidu-spider3-dead-link-model.md (S422)

| entry line | claim | held sentence (file:line) | verdict |
|---|---|---|---|
| S422:8 | the lane holds what an error status does to a crawl on Googlebot's side (`corpus/knowledge/crawl-error-status-table.md`, S286) | crawl-error-status-table.md:10 (same sentence as above) | TRUE — confirmed by running `git show 4b8c730…:corpus/knowledge/crawl-error-status-table.md` |
| S422:8 | another operator's pages say about a deleted URL and about a URL that never existed (`corpus/knowledge/yahoo-japan-deleted-url-recrawl.md`, S419; `corpus/knowledge/yahoo-japan-nonexistent-url-recrawl.md`, S420) | S419 title line 6: "A deleted URL that still answers 200 OK may keep being crawled"; S420 title line 6: "The crawler does not treat a 200 OK error page for a nonexistent URL as an error page" | TRUE — confirmed by running `git show 4b8c730…:corpus/knowledge/yahoo-japan-deleted-url-recrawl.md` and `…:corpus/knowledge/yahoo-japan-nonexistent-url-recrawl.md` |
| S422:70 | Status-code layer: `corpus/knowledge/crawl-error-status-table.md` (S286) | crawl-error-status-table.md:6,10 — the entry is the status layer (title "An error status is its own crawl layer") | TRUE — entry exists and matches the label, confirmed by running `git show 4b8c730…:corpus/knowledge/crawl-error-status-table.md` |
| S422:70 | Other operator, deleted URL and never-existent URL: `corpus/knowledge/yahoo-japan-deleted-url-recrawl.md` (S419) and `corpus/knowledge/yahoo-japan-nonexistent-url-recrawl.md` (S420) | S419:6, S420:6 (titles as above) | TRUE — confirmed by running `git show 4b8c730…:` on both paths |
| S422:70 | Other Baidu statements held by the lane: `corpus/knowledge/baidu-friendly-crawl-guidance.md` (S329) and `corpus/knowledge/baidu-mobile-matching-error-causes.md` (S312) | baidu-friendly-crawl-guidance.md:1 (`source: S329 … 百度搜索资源平台` — Baidu course page); baidu-mobile-matching-error-causes.md:1 (`source: S312 … 百度搜索资源平台` — Baidu manual page) | TRUE — both entries exist at the revision and are Baidu-operator statements; no specific held sentence is claimed, only the pointer, confirmed by running `git show 4b8c730…:` on both paths |
| S422:55 | the staged candidate this entry replaces (shokuknow `merge/kake/`, the staging row for this page) attached a 10-day-to-40-80% improvement to dead-link handling; its staged Gate quote is 37 units, over the 25-unit ceiling | the staging row is not a held lane entry named in this seat's scope (it is the replaced candidate artifact); the claim is a factual statement about that candidate, not an attribution of content to a held entry — recorded here, not judged | N/A (out of scope) |

No STRETCHED or FALSE attribution found in either entry.

## ID RESOLUTION:

Command (run 2026-10-25):
`python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/id_resolver.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 4b8c73050470ada9e6583f3b12d659d1bed6a17f --fleet /home/vgpnk/Projects/shokunin`

Output (verbatim):
```
ids_cited=106 ids_resolved=106 dangling=0 owned_elsewhere=0 unowned=0
EXIT=0
```
All 106 cited ids in the corpus at the pinned revision resolve in the lane registry; zero dangling, zero owned elsewhere, zero unowned.

S### tokens in the two entries and their registry rows (registry = `corpus/SOURCES.md` `## Registry` at the pinned revision, row line numbers from `git show 4b8c730…:corpus/SOURCES.md | grep -n`):

| token | registry row (SOURCES.md line) | row id | resolves to (entry) |
|---|---|---|---|
| S421 (×16 in baidu-dead-link-types.md) | 167 | S421 | corpus/knowledge/baidu-dead-link-types.md |
| S419 (×1) | 165 | S419 | corpus/knowledge/yahoo-japan-deleted-url-recrawl.md |
| S420 (×1) | 166 | S420 | corpus/knowledge/yahoo-japan-nonexistent-url-recrawl.md |
| S286 (×1) | 151 | S286 | corpus/knowledge/crawl-error-status-table.md |
| S422 (×11 in baidu-spider3-dead-link-model.md) | 168 | S422 | corpus/knowledge/baidu-spider3-dead-link-model.md |
| S286 (×2) | 151 | S286 | corpus/knowledge/crawl-error-status-table.md |
| S419 (×2) | 165 | S419 | corpus/knowledge/yahoo-japan-deleted-url-recrawl.md |
| S420 (×2) | 166 | S420 | corpus/knowledge/yahoo-japan-nonexistent-url-recrawl.md |
| S329 (×1) | 155 | S329 | corpus/knowledge/baidu-friendly-crawl-guidance.md |
| S312 (×1) | 156 | S312 | corpus/knowledge/baidu-mobile-matching-error-causes.md |

(Counts from `grep -o -E 'S[0-9]{3}'` on each entry file at the pinned revision; all tokens resolve — no dangling token in either entry.)

## SUGGESTED BACK-LINKS:

Suggestions only; no edits made.

1. **crawl-error-status-table.md (S286)** → add pointers to baidu-dead-link-types.md (S421) and baidu-spider3-dead-link-model.md (S422). A reader of the status table (per-engine crawl hygiene) debugging dead links would want the Baidu content-kind-answers-200 entry and the Spider3.0 recognition-scope entry; S286 currently holds no cross-links at all.
2. **yahoo-japan-deleted-url-recrawl.md (S419) and yahoo-japan-nonexistent-url-recrawl.md (S420)** → add pointers to S421 (same class: a content dead link answers 200) and S422 (model recognises content/redirect dead links). Both Yahoo entries already contrast with the Google-side status entry; Baidu is the missing third-engine contrast for the same 200-OK dead-link surface.
3. **baidu-mobile-matching-error-causes.md (S312)** → names "a dead link" as one cause of an unmatchable mobile page but has no pointer to S421/S422, which define dead-link kinds for the same operator; a reader of S312 would benefit from a pointer.
4. **baidu-friendly-crawl-guidance.md (S329)** (optional) → same operator's crawler guidance; a pointer to S421/S422 would round out the Baidu crawl-hygiene cluster, but S329's topic (robots) is less directly adjacent.

VERDICT: All cross-links in S421 and S422 check out TRUE (7/7 judged, 1 out-of-scope staging-row note); resolver run reports 106/106 ids resolved with 0 dangling; all S### tokens in both entries resolve to their registry rows; suggested back-links listed (S286 → S421/S422, S419/S420 → S421/S422, S312 → S421/S422, optional S329).
