# ScoutCorpusRobots — every corpus robots claim against the round-37 C1 contract

Seat: kake-r37-w1, build wave, leaf. Read-only; no sandbox clone, no network, no counter run, sealed key untouched. Contract read from `git show 4b089da:SCORECARD.md` §“Round 37 — declared claims”; base 621fb528, declared 202d625.

## Commands (all offline)
1. `git -C <lane> show 4b089da699cfaaf5ebeb6a0746b7e4238602e20a:SCORECARD.md | sed -n '/^## Round 37 — declared claims/,$p'` → exit 0.
2. `git -C <lane> ls-tree 4b089da -- scripts/robots_audit.py` → exit 0, empty output (no tool at the receipt revision).
3. `grep -oF 'top-level path of the service' .ufo/waves/round-37/sources/S011.txt | wc -l` → 1; same for `MAY access any resources on the server` → 1 and `MUST assume complete disallow` → 1. `grep -cF` on the first phrase → 1, i.e. the entry’s own replay command reproduces its stated count; retained S011.txt is a single line, so the `-o` occurrence count is the stronger check and it is also 1.
4. `grep -n -i robots` over `corpus/`, `PROVINCE.md`, `LOG.md`, `corpus/lessons/` → the claim set below.
5. Offline reads of retained S011/S095/S097 text (`.ufo/waves/round-37/sources/`, sha256 S011 `8e632e48…59cf3`, S095 `a9094853…ddbbc6`, S097 `a42aee4e…be3801`).

## Claims and verdicts (path:line — claim — verdict vs C1 contract)
| # | claim | verdict |
|---|---|---|
| 1 | `corpus/knowledge/crawl-scope-per-host.md:7-9` — rules discovered at the service root `/robots.txt`, not per project subpath | AGREE (S011 §2.3 “top-level path of the service”), but OUT OF C1 SURFACE: the manifest names the file; C1 asserts nothing about where it is fetched from |
| 2 | `crawl-scope-per-host.md:9-10` — the three `veigapunk.github.io/<repo>/` sites share the one host-root policy | Compatible with RFC authority scope, untested by C1 (no URL→robots mapping); also the entry’s unprobed part (`:44-46`) |
| 3 | `crawl-scope-per-host.md:10-11` — 4xx robots response means crawlers MAY access resources | AGREE: C1 (a) 400–499 → allowed whatever any file says. C1 turns the MAY into a definite allow (stronger than the source, no conflict) |
| 4 | `crawl-scope-per-host.md:11-12` — 5xx/network-unreachable means MUST assume complete disallow, subject to the long-outage allowance | PARTIAL: C1 (a) 500–599 → disallowed, incl. `/robots.txt`; no time dimension (allowance unmodeled), and “network-unreachable” cannot be expressed (status must be an integer in 200–299/400–499/500–599). C1’s `/robots.txt`-disallowed reading resolves an RFC tension: §2.2.2 says “The /robots.txt URI is implicitly allowed” (verified in S011), §2.3.1.4 says complete disallow |
| 5 | `crawl-scope-per-host.md:13-18` — sitemaps get a path-based boundary; a `Sitemap:` line in the host-root file is a supported discovery route | AGREE with C1 (b): other keys (`sitemap`, `crawl-delay`) are ignored and do not end a group, matching S011 §2.2.4 “a ‘Sitemaps’ record MUST NOT terminate a group”. C1 does not audit sitemap scope or discovery — claim unmodeled |
| 6 | `crawl-scope-per-host.md:27-29` — quotes §2.3, §2.3.1.3, §2.3.1.4 | VERIFIED exactly, one occurrence each in retained S011 (command 3) |
| 7 | `crawl-scope-per-host.md:44-46` — named debt: status of `veigapunk.github.io/robots.txt` and its sitemap listing unknown; no property probed | UNCHANGED by C1: the tool is offline and fetches nothing; the debt survives the new gate |
| 8 | `crawl-scope-per-host.md:50` — “missing substrate stays visible” | CONFIRMED (7) |
| 9 | `corpus/README.md:40` — “robots.txt only at the host root; sitemap scope by location; project sites share the user-site robots policy” | Restatement of 1–5; same verdicts |
| 10 | `corpus/README.md:106-108` — “the user-site robots.txt” listed among checks needing an operator-authorized free read | Unchanged: C1 does not clear it |
| 11 | `PROVINCE.md:22-23` — frontier “Crawl hygiene per host … first entry …; canonical/JS rendering open” | C1 is the frontier’s first gate, but only for rule evaluation; sitemap scope, canonical and JS rendering stay open. `PROVINCE.md:30` requires “source-backed entries and a gate” — see gap |
| 12 | `PROVINCE.md:34-35` — kake owns publisher-side placement (robots/sitemap at the host it serves) | AGREE: C1 audits a publisher-side file and claims no crawler behaviour (its Limits say so) |
| 13 | `corpus/knowledge/freshness-sweep.md:62` (A4, pin `sitemapStatus` 404) + `corpus/knowledge/freshness-pins.json:36` (`sitemapStatus` 404) + `scripts/freshness-sweep.mjs:85-86,907-913` vs `corpus/knowledge/publish-queue.md:293` (200, 7,565 B on 2026-10-21) | CONTRADICTS — corpus-internal, not C1. Same URL (`https://ds4cc.com/sitemap.xml`) pinned 404 and recorded 200. Also A4’s label says “sitemap/robots” but the code fetches only the sitemap; robots.txt has no executable pin. File rule `publish-queue.md:286` (“this section is newer”) makes the pin stale — or the site regressed; unadjudicated offline |
| 14 | `corpus/knowledge/publish-queue.md:93,209,259` — ds4cc `sitemap.xml`/`robots.txt` live 404, working-tree-only/unpushed | Historical under the same in-file rule; superseded by `:293`; no protocol claim |
| 15 | `corpus/knowledge/ghp-subpath-spotcheck.md:62` — `robots.txt` among files served live-404 because unpushed | Historical, consistent with `publish-queue.md:93` |
| 16 | `corpus/knowledge/link-preview-metadata.md:95-96` — Slack’s link robot does not honour robots.txt; [INFERENCE] a disallowed page can still be unfurled | NOT REP; C1 says nothing about unfurlers, no conflict |
| 17 | `corpus/knowledge/field-performance-cwv.md:81-83` — `X-Robots-Tag: noindex` / `<meta name="robots" content="noindex">` as discoverability failures | Different mechanism (indexing directives, not crawl rules); C1 silent |
| 18 | `corpus/SOURCES.md:19-21` — S011 teaches host-root + unreachable disallow; S012/S013 teach sitemap location scope | S011 AGREE (verified). S012/S013 not re-opened this round (retained set has S011/S095/S096/S097 only); last HOLD is r26 (`crawl-scope-per-host.md:57-61`) — UNVERIFIED, not contradicted |
| 19 | `corpus/SOURCES.md:108,124` — reading sequence S010→S013 | No claim; consistent |
| 20 | `LOG.md:8,106,157,165,270,367` — ds4cc robots/sitemap live-404 and unpushed-set accounting; `LOG.md:204` — `final-{root,sitemap,robots}.html` artifact names | Ops record, no protocol claim; consistent with 14 |
| 21 | `corpus/lessons/round-20.md:213`, `round-20-verifier-spotcheck.md:12`, `round-6.md:21`, `round-34.md:36`, `round-34-verifier-spotcheck.md:131,154` | Admission quotes/verdicts and historical 404 sets; agree with S011; round-34 rows are S069 Slack (not REP) |

No corpus claim contradicts C1. Claims 1–2 are outside C1’s test surface; 4 is partially modeled; 5, 13 and 16–17 are unmodeled by design.

## Contract vs its own sources (S095, and S097 opened this round)
- S095 gives Google a *crawler-specific* layer C1 does not model: “most specific user agent” precedence and “Only one group is valid” for different names, vs S011 §2.2.1 “the matching groups’ rules MUST be combined” (verified) — C1 follows the RFC, Google diverges; exact-token equality hides most of the difference.
- S095: follows ≥5 redirects then treats robots as 404 (S011 §2.3.1.2 SHOULD ≥5) — C1 has no 3xx path (a 3xx status makes the check `check_invalid`).
- S095: all 4xx except 429 treated as no file; 429 handled like a server error with retry/cache — C1 folds 429 into 400–499 “allowed” (RFC-correct, Google-divergent in decision source).
- S095: 24 h cache, 30-day last-good, then no restrictions if the site is generally available — C1 has no cache/time model; this is also the corpus’s unmodeled “long-outage allowance” (claim 4). S095 also confirms the 500 KiB cap C1 fixes at exactly 512000 bytes.
- S095 path scope “relative to the root of the website from where the robots.txt file was fetched (same protocol, port, host and domain names)” supports claim 1; the corpus’s “host-root” is shorthand for RFC authority.
- S097 (1994) is cited by no corpus entry (only `SCORECARD.md:1789`); its Method matches S011’s root placement — nothing to contradict.

## Frontier gap
- Filled: the corpus’s only executable robots/sitemap artifact today is the ds4cc sitemap fetch (claim 13); C1 adds the first offline evaluator of the REP *grammar* the frontier entry cites only for scope — grouping (§2.2.1), matching and specificity (§2.2.2), special characters (§2.2.3), other records (§2.2.4), access results (§2.3.1), 500 KiB (§2.5) — plus deterministic manifest fault handling. A publisher can test a local file plus a status code with no crawler.
- Corpus-side hole: no corpus entry states C1’s readings (b)–(e) — octet specificity counting `*`/`$`, decode-unreserved normalization, `/robots.txt` implicit allow only when 200–299, 512000-byte cap, BOM drop, U+FFFD replacement. So `PROVINCE.md:30`’s “source-backed entries and a gate” pair holds for scope only; append the readings (with S011/S095 anchors) to `crawl-scope-per-host.md` or a new entry before any Core promotion.
- Stays open: live fetch and any observed file (claim 7), redirects, caching/time incl. the long-outage allowance, Google’s UA precedence, 429 and sitemap discovery field, indexability directives (claim 17), sitemap scope (claims 5, 18), network-unreachable as a status, and whether the host-root policy covers the three project sites (claim 2).

## Not verified
- No live GET of any property: which side of claim 13 is current is unknown; C1’s behaviour was never observed (tool absent at `4b089da`, command 2). S012/S013 quotes not re-opened. S096 unread beyond size — no corpus claim rests on it.

## Advisory to L1
1. Claim 13 is a real operability defect independent of C1: pin 404 vs recorded 200 on the same URL; also A4’s “sitemap/robots” label overstates what the script fetches. Re-pin or re-label, and decide whether robots.txt deserves its own pin.
2. If C1 lands, the knowledge entry needs the grammar readings, otherwise the gate is source-backed for scope only.
3. The corpus never contradicts C1; the only open question C1 raises is the §2.2.2/§2.3.1.4 `/robots.txt`-under-5xx reading, which should be written down as a lane reading.
