# ConnSiblingOverlap

Round-56 W1 sibling-overlap scan (read-only; contract section 3 / Claim C2).
Lane: kake-shokunin. Base: e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6.
Scanned 20 sibling lanes (/home/vgpnk/Projects/shokunin/*-shokunin, kake excluded):
audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kama, kasegi, kengaku,
kotoba, kotodama, kumitate, lore, mado, mori, revenger, souji, tabi, tameshi, tsukuroi.
Swept corpus/, SKILL.md, PROVINCE.md across all siblings. No tools installed.

Negative sweep results (0 hits across all 20 sibling lanes):
- `info-search.yahoo.co.jp`: 0 hits across all 20 sibling lanes.
- `archives/002856`, `archives/002857`, `archives/002852`: 0 hits across all 20 sibling lanes.
- `X-Robots-Tag`: 0 hits across all 20 sibling lanes.

OVERLAP TABLE:
| Lane | File:line | What | Same document? | Same crawl ground? |
|---|---|---|---|---|
| mori | corpus/SOURCES.md:103 | S097 proc_pressure(5) manpage candidate returned HTTP 404 Not Found (reject evidence) | No | No (filesystem/kernel docs) |
| chousa | corpus/SOURCES.md:71 | S061 RFC 9110 §15.5.5 "404 Not Found" status semantics at origin server | No | No (research hop resolution) |
| chousa | corpus/evidence/round30/qr_harness.py:219 | Mock server string `HTTP/1.1 404 Not Found` in QR test harness | No | No (test mock) |
| kama | corpus/knowledge/endpoint-identity.md:78 | Jetty `HTTP ERROR 404 Not Found` on port 8080 (endpoint identity false positive) | No | No (local LLM service triage) |
| kama | corpus/knowledge/consumer-registry.md:249 | Recorded probe header `HTTP/1.1 404 Not Found` from misdirected port | No | No (local LLM service triage) |
| kama | SKILL.md:71,175 | Triage table for foreign Jetty servlet returning 404 on port 8080 | No | No (local LLM service triage) |
| kama | corpus/lessons/round-1-citations.md:9 | Witness log for Jetty 404 on port 8080 | No | No (local LLM service triage) |
| tabi | corpus/knowledge/external-class-fixture-v2.md:181,550 | Loopback `/robots.txt` prefix test fixture; U5 disclaims real robots semantics | No | Adjacent (browser test harness) |
| tabi | corpus/knowledge/interaction-approval-table.md:92 | Stance: real-surface robots/ToS unmeasured; default-deny follows | No | Adjacent (browser policy stance) |
| tabi | corpus/evidence/w9-tabi-b91/runs/.../journey.json:164 | Loopback journey test fixture HTTP/1.0 404 Not Found status line | No | No (browser test run record) |
| kotodama | corpus/lessons/round-71.md:38 | External cite rejection for EFDSS Morris page returning 200 with 404 title ("soft-404") | No | No (myth/dance citation check) |
| kotodama | corpus/lessons/round-71-verifier-spotcheck.md:106 | Spotcheck agreeing EFDSS page is rejected soft-404 | No | No (myth/dance citation check) |
| kengaku | corpus/evidence/round28-calibration/.../audit-current.stdout:30586 | LLM benchmark evaluation prompt intent string "404 Not Found" | No | No (benchmark prompt data) |
| kasegi | corpus/knowledge/intake-surface.md:65 | Intigriti-yahoo bug bounty program reference | No | No (bounty bookkeeping) |

ID COINCIDENCES:
Target IDs: S367, S375, S376, S419, S420.
Swept all 20 sibling `corpus/SOURCES.md` registries. Only kotodama-shokunin has reached this registry height; all other 19 siblings hold fewer than 300 rows (max S015 to S282; mori has 257 rows up to S484 but skips 360-430).
Kotodama rows for these exact IDs:
- S367 (SOURCES.md:396): Batsîkama & Campelo 2011, "A Catedral de São Salvador de Angola..." (history paper, 1885 colonial Kongo division / 1913 insurrection).
- S375 (SOURCES.md:404): Bostoen & de Schryver 2018, "Seventeenth-Century Kikongo Is Not the Ancestor of Present-Day Kikongo" (linguistics chapter).
- S376 (SOURCES.md:405): MacGaffey 2003, "Crossing the River: Myth and Movement in Central Africa" (symposium paper on Kongo myth/social structures).
- S419 (SOURCES.md:448): College of Arms (London), "FAQs: heraldry" (heraldic rules on arms transmission and quarterings).
- S420 (SOURCES.md:449): Court of the Lord Lyon 2026, "Petitioning for a Coat of Arms..." (Scottish arms matriculation by proved relationship).

In kake-shokunin:
- S367 (SOURCES.md:157): Yahoo!検索 インフォセンター `archives/002852.php` (link-target crawl restriction via meta tag / X-Robots-Tag).
- Staged S375: `archives/002856.php` (deleted URL recrawl / 404 status), renumbered to S419 by round-56 contract to avoid colliding with kake's registered S418 base.
- Staged S376: `archives/002857.php` (non-existent URL recrawl / soft-404 status), renumbered to S420 by round-56 contract.
- S419: New kake row for `archives/002856.php`.
- S420: New kake row for `archives/002857.php`.

Assessment:
The coincidence is purely lexical homonymy arising from autonomous per-lane monotonic integer indexing (S001 upwards). As established in kake's round-53 lesson (`corpus/lessons/round-53.md:11-21,37`), the round-52 verifier's remark that staged IDs "resolve only in kotodama" was mistaken: source registries are strictly lane-local. The underlying documents and domains are completely disjoint (Yahoo! search crawl hygiene vs African linguistic history and British heraldry).

PROVINCE CLAIMS:
Swept `PROVINCE.md` across all 20 sibling lanes.
- Zero sibling PROVINCE files claim crawl hygiene, search engine crawler directives, robots.txt, sitemaps, soft-404 handling, or HTTP status codes for crawler guidance.
- `tabi-shokunin` (PROVINCE.md:15-16): Explicitly refuses "web *publishing* (→ kake)". Owns client-side browser driving, DOM evidence capture, and crawler interaction discipline.
- `kake-shokunin` (PROVINCE.md:34-35): Explicitly claims publisher-side placement and crawl hygiene ("tabi drives browsers and owns client-side crawler discipline; kake owns publisher-side placement (robots/sitemap at the host it serves)").
- `chousa-shokunin` (PROVINCE.md:1-16): Owns deep-research method, question framing, and source hierarchy; does not own web publishing or crawl hygiene.
- `kotodama-shokunin` (PROVINCE.md:19-20): Explicitly refuses "web publishing (kake)".
- `kotoba-shokunin` (PROVINCE.md:57): Explicitly records kake as adjacent: "web properties and publishing".
- `souji-shokunin` (PROVINCE.md:3-8): Owns workspace/repo hygiene (cleaning stray local files), not web crawl hygiene.
- Conclusion: No sibling PROVINCE claims or contests kake's crawl-hygiene ground.

ADJACENCY LINES FOR THE REPORT:
1. `tabi-shokunin` (Adjacent — report, do not absorb):
   Tabi owns client-side browser driving and crawler interaction discipline; kake owns publisher-side crawl hygiene (server response status codes like HTTP 404, response headers like X-Robots-Tag, and page-level meta directives). Tabi's loopback robots fixture is an instrumentation harness, not a crawl study; kake's entries supply real-operator documentation that tabi explicitly leaves unmeasured.
2. `chousa-shokunin` (Adjacent — report, do not absorb):
   Chousa holds RFC 9110 HTTP status semantics (S061) to govern research hop resolution. Kake uses operator documentation on HTTP 404/200 for search-engine crawl management. No absorption; the scopes are orthogonal.
3. `kotodama-shokunin` (Disjoint homonym):
   Registry IDs S367, S375, S376, S419, S420 coincide with kotodama rows only by independent per-lane monotonic integer counters. The referenced texts (Kikongo linguistics, Angolan history, British heraldry vs Yahoo! search crawler handling) share zero document or domain overlap. Kake's report should reaffirm that registries are autonomous.
4. Contested ground:
   NONE. Kake's round-56 Claim C2 entries (`yahoo-japan-link-target-crawl-restriction`, `yahoo-japan-deleted-url-recrawl`, `yahoo-japan-nonexistent-url-recrawl`) operate entirely within kake's declared Frontier ground (per-engine crawl hygiene) and duplicate no sibling document or entry.

VERDICT: Zero sibling overlap on retained Yahoo documents; ID coincidences with kotodama are disjoint lexical homonyms; tabi and chousa remain cleanly adjacent; no sibling PROVINCE claims crawl hygiene; zero contested scope.