# ConnectorSiblings

Round-55 W1 sibling-overlap scan (read-only). Lane: kake-shokunin. Base
fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d. Scanned 20 sibling lanes
(checked /home/vgpnk/Projects/shokunin/<id>-shokunin; kake itself excluded):
audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kama, kasegi,
kengaku, kotoba, kotodama, kumitate, lore, mado, mori, revenger, souji,
tabi, tameshi, tsukuroi.
Each sibling swept over `corpus/knowledge`, `corpus/SOURCES.md`, `PROVINCE.md`
(existence checked per lane; all three existed in every one of the 20 lanes).
No tools installed (RULES.md record: none).

## COMMAND LOG:

All sweeps: `grep -rln [flags] -F -- <pattern> corpus/knowledge corpus/SOURCES.md PROVINCE.md`
run per sibling with cwd = sibling root; counts are file-hits summed across the
20 lanes (per-lane details in HITS where nonzero).

- `grep -rln -F -- 'info-search.yahoo.co.jp'` — 0 hits (all 20 lanes: 0 each).
- `grep -rln -F -- 'robots.txt'` — 3 hits, all tabi:
  corpus/knowledge/external-class-fixture-v2.md, arc-synthesis.md, closeout-r11.md.
- `grep -rln -F -- 'Disallow'` — first run: 1 hit (kotodama
  java-majapahit.md). Re-run for tabi (same pattern, same paths) returned rc=0
  with external-class-fixture-v2.md. Concurrent W1 edits in live sibling lanes
  raced the first pass; grounded final tally: 2 files (kotodama
  java-majapahit.md line 200 "Disallowed shortcuts" — civilization-methodology
  prose, unrelated; tabi external-class-fixture-v2.md).
- `grep -rln -F -- 'wildcard'` — 15 hits: chousa 2, game-dev-2d 1, kagi 2,
  kama 4, kasegi 1, kotoba 1, kotodama 2, kumitate 2, tabi 1. Only robot
  co-occurrence: tabi external-class-fixture-v2.md (line 550, U5).
- `grep -rln -F -- 'placement'` — 156 hits (kotodama linguistics/civilizations
  137, others 1–19). Only robots co-occurrence: tabi closeout-r11.md.
- `grep -rln -F -- 'consult'` — 111 hits (kotodama 108, others 1–6). Zero
  robots co-occurrence.
- `grep -rlin -F -- 'yahoo'` — 5 hits, all kasegi (intake-surface.md,
  mission-control.md, operator-queue.md, submitted-registry.md,
  ufo-workspaces.md): all `intigriti-yahoo` bug-bounty program references.
- `grep -rlin -F -- 'robots'` (case-insensitive) — 7 hits, all tabi:
  interaction-approval-table.md, external-class-fixture-v2.md,
  packet-readiness-r7.md, layer-routing-synthesis.md,
  carried-debt-closure-r8.md, arc-synthesis.md, closeout-r11.md.
- `grep -rln -F -- '002849'` — 0 hits. `'002850'` — 0 hits.
  `'002885'` — 0 hits.
- `grep -rln -F -- 'archives'` — 100 hits; reviewed across lanes: archive-file
  formats (zip/asar/apk byte evidence, revenger/kaidoku), audit/queue
  directories, AUR package archives (tsukuroi). None reference Yahoo info-search
  archives.
- `grep -rln -w -F -- 'Allow'` — 12 hits; sampled: kama consumer-registry.md
  (CORS header `Access-Control-Allow-Origin`), mori SOURCES.md (OpenTelemetry
  allow-list), kotodama calibration-registry.md (prose "Allow blanks"). None
  robots-related; zero robots co-occurrence.
- `grep -rln -F -- 'User-agent'` — 1 hit: tabi external-class-fixture-v2.md
  (line 181, fixture's 2-line sample robots body).
- `grep -rln -F -- 'Crawl-delay'` — 1 hit: tabi external-class-fixture-v2.md
  (line 550, U5).

Negative claims carry their sweep command above (info-search.yahoo.co.jp,
002849/002850/002885: 0 file-hits per lane).

## HITS:

| Sibling | File | Same document? | Ground | Touch |
|---|---|---|---|---|
| tabi | corpus/knowledge/external-class-fixture-v2.md | No | Adjacent | Loopback fixture: `/robots.txt` first-request "conventional permission probe"; `Disallow:` prefix matching (`path.startsWith(p)`); fixtures `User-agent: *` (line 181); U5 (line 550): real robots semantics — wildcards, per-agent groups, `Crawl-delay` — unmeasured; explicitly "not a robots-semantics study", instrument only |
| tabi | corpus/knowledge/interaction-approval-table.md | No | Adjacent | Policy stance: "corpus holds no measured ToS/robots datum; asserting one is forbidden; default-deny follows" (rows C3; lines 92-93) |
| tabi | corpus/knowledge/layer-routing-synthesis.md | No | Adjacent | RT15 trip classes: robots-disallow stop-before-issuing; "2-line robots document does not generalize" (line 156) |
| tabi | corpus/knowledge/arc-synthesis.md | No | Adjacent | Recaps robots-disallow stop-before-issuing; loopback instrument never a C6 datum |
| tabi | corpus/knowledge/closeout-r11.md | No | Adjacent | Recaps robots-first probe and trip instruments; placement discussion is SCORECARD-related (line 131), not robots placement |
| tabi | corpus/knowledge/packet-readiness-r7.md | No | Adjacent | U1 stands: rate/ToS/robots unmeasured for real surfaces; loopback half new |
| tabi | corpus/knowledge/carried-debt-closure-r8.md | No | Adjacent | Evidence-dir inventory for the loopback fixture (`probe-robots/` sets) |
| kotodama | corpus/knowledge/civilizations/java-majapahit.md | No | None | "Disallowed shortcuts" methodology prose (line 200) — false positive |
| kasegi | corpus/knowledge/{intake-surface,mission-control,operator-queue,submitted-registry,ufo-workspaces}.md | No | None | `intigriti-yahoo` bounty-program references — not crawler/robots ground |

## ADJACENCY CALLS:

1. Same-document ground: NONE. No sibling file contains `info-search.yahoo.co.jp`
   or any of the doc ids 002849/002850/002885; no sibling holds S372/S373/S418.
   Kake's three re-opened/new rows have no sibling twin.
2. tabi holds the only robots-touching sibling ground, and it is adjacent, not
   duplicative: (a) a loopback fixture that treats `/robots.txt` as a
   permission probe and matches `Disallow:` prefixes — it explicitly disclaims
   being a robots-semantics study; (b) a standing recorded absence (U1/U5,
   interaction-approval-table): real-surface robots/ToS semantics, wildcards,
   per-agent groups, `Crawl-delay` are unmeasured in tabi's corpus. It does NOT
   touch: Yahoo! JAPAN pages, Allow-vs-Disallow precedence, `*`/`$` wildcard
   syntax, or robots.txt placement/consult order.
3. ADJACENCY RULE: report, do not absorb. Kake must leave tabi's ground as
   tabi's; kake's entries (Yahoo operator-authored refusal rules + robots.txt
   basics) are orthogonal — they supply measured real-surface content that tabi
   explicitly marks absent. No absorption, no copy; a one-way cross-reference in
   the report (not in entries) is optional.
4. kasegi's Yahoo hits are bug-bounty program bookkeeping; no adjacency call
   (no touch on any declared topic).
5. Duplication check: kake's three candidate entries would duplicate NO sibling
   entry. No sibling has an entry on Yahoo info-search pages; tabi has no
   robots-semantics entry (only a fixture and an anti-claim/absence). The two
   candidate entries neither duplicate nor conflict with any sibling row; the
   only reported sibling mentions are internal to tabi's own corpus.

VERDICT: No sibling holds same-document ground for S372/S373/S418; only tabi
touches robots (loopback instrument + recorded absence), which is adjacent and
non-duplicative — report, do not absorb; kake's three entries duplicate no
sibling entry.
