# ConnectorSiblingOverlap — round 50 wave 1

Axis: adjacency. Advisory read-only scan; no source-truth verdict, no gate, no writes into any sibling repo or the lane Git index.

## Round-50 theme under test

The frozen contract (`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-50/contract.json`) declares C1 on three source ids already in `corpus/SOURCES.md` lines 149–150 plus the staged row S286:

- S273 — `https://developers.google.com/crawling/docs/crawl-budget` (crawl-budget reallocation sentence)
- S274 — `https://developers.google.com/crawling/docs/crawlers-fetchers/reduce-crawl-rate` (hostname-wide backoff sentence)
- S286 — `https://developers.google.com/search/docs/crawling-indexing/troubleshoot-crawling-errors` (Googlebot scales back when servers have trouble)

All three are publisher-side crawl-hygiene rows: what an error status or a throttle decision does to Google's crawl of a host the lane serves. The lane's existing entries already hold this ground: `corpus/knowledge/crawl-error-status-table.md` (S286), `corpus/knowledge/crawl-budget-consequences.md` (S273, S274), `corpus/knowledge/crawl-scope-per-host.md` (S011–S013), `corpus/knowledge/robots-txt-rules.md`, `corpus/knowledge/sitemap-orphan-audit.md`.

## Sibling scan — paths checked

Per lane: `PROVINCE.md`, `SKILL.md`, `corpus/knowledge/` listing, and a content grep for `crawl.error|soft.?404|crawl.rate|crawl.budget|Googlebot|troubleshoot.crawling|error.?status|429.*retry|5xx|Search.Console`. Sibling repos scanned:

- `/home/vgpnk/Projects/shokunin/audio-shokunin` — PROVINCE, `corpus/knowledge/` (17 entries)
- `/home/vgpnk/Projects/shokunin/chousa-shokunin` — PROVINCE, `corpus/knowledge/` (40+ entries)
- `/home/vgpnk/Projects/shokunin/game-dev-2d-shokunin` — PROVINCE, `corpus/knowledge/` (5 entries)
- `/home/vgpnk/Projects/shokunin/game-dev-3d-shokunin` — PROVINCE, `corpus/knowledge/` (6 entries)
- `/home/vgpnk/Projects/shokunin/kagi-shokunin` — PROVINCE, `corpus/knowledge/` (25 entries)
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` — PROVINCE, `corpus/knowledge/` (50+ entries)
- `/home/vgpnk/Projects/shokunin/kama-shokunin` — PROVINCE, `corpus/knowledge/` (28 entries)
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin` — PROVINCE, `corpus/knowledge/` (30+ entries)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin` — PROVINCE, `corpus/knowledge/` (35+ entries)
- `/home/vgpnk/Projects/shokunin/kotoba-shokunin` — PROVINCE, `corpus/knowledge/` (50+ entries)
- `/home/vgpnk/Projects/shokunin/kotodama-shokunin` — PROVINCE, `corpus/knowledge/` (5 subtrees)
- `/home/vgpnk/Projects/shokunin/kumitate-shokunin` — PROVINCE, `corpus/knowledge/` (40+ entries)
- `/home/vgpnk/Projects/shokunin/lore-shokunin` — PROVINCE, `corpus/knowledge/` (28+ entries)
- `/home/vgpnk/Projects/shokunin/mado-shokunin` — PROVINCE, `corpus/knowledge/` (35+ entries)
- `/home/vgpnk/Projects/shokunin/mori-shokunin` — PROVINCE, `corpus/knowledge/` (40+ entries)
- `/home/vgpnk/Projects/shokunin/revenger-shokunin` — PROVINCE, `corpus/knowledge/` (17 entries)
- `/home/vgpnk/Projects/shokunin/souji-shokunin` — PROVINCE, `corpus/knowledge/` (10 entries)
- `/home/vgpnk/Projects/shokunin/tabi-shokunin` — PROVINCE, `corpus/knowledge/` (40+ entries)
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin` — PROVINCE, `corpus/knowledge/` (40+ entries)
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` — PROVINCE, `corpus/knowledge/` (40+ entries)
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, `/home/vgpnk/Projects/shokunin/kotoba-shokunin`, `/home/vgpnk/Projects/shokunin/kotodama-shokunin`, `/home/vgpnk/Projects/shokunin/kumitate-shokunin`, `/home/vgpnk/Projects/shokunin/souji-shokunin`, `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, `/home/vgpnk/Projects/shokunin/tabi-shokunin`, `/home/vgpnk/Projects/shokunin/lore-shokunin`, `/home/vgpnk/Projects/shokunin/mado-shokunin`, `/home/vgpnk/Projects/shokunin/mori-shokunin`, `/home/vgpnk/Projects/shokunin/kama-shokunin`, `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, `/home/vgpnk/Projects/shokunin/kagi-shokunin`, `/home/vgpnk/Projects/shokunin/chousa-shokunin`, `/home/vgpnk/Projects/shokunin/revenger-shokunin`, `/home/vgpnk/Projects/shokunin/audio-shokunin`, `/home/vgpnk/Projects/shokunin/game-dev-2d-shokunin`, `/home/vgpnk/Projects/shokunin/game-dev-3d-shokunin`

## Findings — no contested ground

No sibling holds the crawl-error-status, soft-404, 5xx-crawl-rate, or crawl-budget surface as its own ground. Only two lanes touch the same vocabulary, and both splits are already declared and stable:

- **tabi** owns *client-side* crawler discipline — browser-side rate/ToS/rights instruments (loopback fixtures serving `429 + Retry-After`, `403`, robots-shaped body, CAPTCHA interstitial as 200) at `corpus/knowledge/external-class-fixture-v2.md` and `corpus/knowledge/interaction-approval-table.md`. The publisher-side vs client-side split is already recorded both directions: kake `PROVINCE.md:34` ("`tabi` drives browsers and owns client-side crawler discipline; kake owns publisher-side placement") and tabi `corpus/adjacency.tsv:6` (disposition `split-declared`, kake_ref `PROVINCE.md:30`). Tabi's `429`/`403`/robots instruments are loopback fixtures that explicitly are not real rate/rights data (`SKILL.md:329` — "a loopback 429 is an instrument, never a C6 datum"), so they do not overlap Google's documentation about what those status codes do to a publisher's crawl.

- **kasegi** mentions crawl-budget vocabulary in passing in `corpus/knowledge/intake-surface.md` and similar VDP/CVE-intake files, but the lane owns vulnerability-disclosure intake, not Googlebot. No crawl-status knowledge entry exists under `kasegi-shokunin/corpus/knowledge/`.

- **kama** owns local model-serving endpoints (its boundary rule, quoted from kake `PROVINCE.md:41`: "`kama` owns local model-serving endpoints; kake owns remote web properties"). The round-49 prompt already routed an Ollama OpenAPI row to kama as out-of-province — that row was refused, not contested.

- **kengaku** mentions "crawler" only as a benchmark-side term (WebArena task spec) and lists kake as the web-properties owner in its own adjacency table (`corpus/knowledge/benchmark-saturation-and-lifecycle.md`).

- All other lanes (audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kotoba, kotodama, kumitate, lore, mado, mori, revenger, souji, tameshi, tsukuroi) return zero hits for the pattern on `corpus/knowledge/` and declare domains (audio, research method, game engines, secrets, RE artifacts, skill-file linguistics, worldbuilding, dispatch/OMP substrate, narrative canon, desktop config, host observability, RE method, hygiene/trash, mutation testing, host repair) that do not include crawl-error-status ground.

## Boundary status

The round-50 theme (publisher-side meaning of crawl error statuses, soft-404 classification, Googlebot's 5xx and crawl-rate response) is **not contested**. Kake's existing adjacency declarations already place it inside the lane: `PROVINCE.md:22` ("Crawl hygiene per host — robots.txt, sitemap scope, canonical signals") and `PROVINCE.md:34–36` (tabi client-side vs kake publisher-side; chousa research method vs kake domain findings). The S286 staged row extends that held ground; no sibling's `PROVINCE.md` claims an overlapping surface.

The one adjacent-but-distinct seam is with tabi's loopback client-side instruments. If the wave later wants a citation for what a client-side 429 fixture measures versus what Google's S286 publisher-side documentation asserts, the pair is `tabi corpus/knowledge/external-class-fixture-v2.md` (client-side shape) + `kake corpus/knowledge/crawl-error-status-table.md` (publisher-side meaning). The two entries are complementary, not duplicative.

## Instrument baseline (frozen commands re-run)

- `c50_quote_class.py --revision 9619af67…` → `classed 0/3 met=False` (no class ledger, no S286 row).
- `c50_quote_class.py --revision 33eec7f2…` → `classed 0/3 met=False` (committed mirror has class ledger + S286 retained bytes; live registry still missing S286 row and lessons for all three ids).
- `c50_durable.py --revision 9619af67…` → `durable 0/1 met=False` (no order proof, no wave-cite, LOG lacks wave cite, settlement absent).

## Gaps and caveats

- This scan is name- and keyword-shaped; a sibling that holds an HTTP-status surface under different vocabulary (for instance as "HTTP response code" or "fetch outcome" rather than `crawl.error`, `error status`, `5xx`, `429`, `Googlebot`, `soft.404`, `crawl.rate`, `crawl.budget`, `Search.Console`, `troubleshoot.crawling`) would not appear. A second pass on a wider vocabulary is cheap if the L1 wants fuller coverage.
- Wave-file evidence (`.ufo/waves/**`) inside siblings was not exhaustively opened — only `corpus/knowledge/` and `PROVINCE.md` were enumerated. Titles and PROVINCE self-descriptions were used as the province signal; a sibling could hold stray crawl evidence inside wave evidence trees without it rising to a province claim.
- The kake-side frontier entry `corpus/knowledge/crawl-error-status-table.md` already exists; C1's predicate is about quote-class ledgering and lesson rows for S273/S274/S286, not about admitting new sibling-contested ground.
- No live property, Search Console, or external host was touched; only the three committed knowledge entries and the two frozen counting commands were used.
