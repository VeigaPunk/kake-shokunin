# ScribeGroundMap

Scope: `corpus/README.md` §Coverage map / §Frontier ground map (lines 74-141) as it must record round 57;
read `PROVINCE.md` §Frontier (20-30) and the round-49..56 frontier-step blocks (340-427),
`corpus/knowledge/` (53 names), `corpus/lessons/round-5{4,5,6}.md`, `corpus/SOURCES.md` (158 rows),
`.ufo/waves/round-55/c55_readme_index.py`, `.ufo/waves/round-57/contract.md`, retained `sources/S421.html`
and `S422.html` (headings only). Lane revision read: `f7c98ff` (base `28fa0b23`). No lane file, index or jj
state was touched; every probe ran in a `mktemp -d` clone (`/tmp/r57-scribe-map-6x8zpuz7`, toplevel verified,
`-c user.name=selftest -c user.email=selftest@local` inside it).

## CURRENT SECTION: (verbatim, `corpus/README.md:74-141`)

### Frontier ground map (round 55; round-56 update)

One row per `PROVINCE.md` §Frontier ground that a held entry can be dated to
(`PROVINCE.md:22-30`): the round it entered, the entry, and the `used-by` rows
that entry names in `corpus/SOURCES.md` at base `fcaf4b85…` (155 rows); the round-55 row is
measured at the round's final revision (156 rows, S418 added), the round-56 row at the round-56
final revision (158 rows, S419 and S420 added), not at base `e48354b7…`. Ranges
are inclusive and each id was checked individually; a row set is the entry's
`used-by` cells, not a re-adjudication of any source.

| Frontier ground | Entered in round | Entries | Rows |
|---|---|---|---|
| Crawl hygiene per host (robots.txt location, sitemap scope) | r20 | `knowledge/crawl-scope-per-host.md` | S011–S013 |
| robots.txt rule semantics, offline expectation audit | r37; repaired r38 | `knowledge/robots-txt-rules.md` | S011 S034 S095 S096 S098–S101 |
| Sitemap and orphan parity | r7; r33 source pin | `knowledge/sitemap-orphan-audit.md` | S001–S006 S065 S066 |
| Static canonical declaration | r22 | `knowledge/static-canonical-preflight.md` | S001–S006 S020 S021 S024–S034 |
| Canonical selection | r51 | `knowledge/canonical-selection.md` | S262 |
| Crawler identity (Googlebot subtypes) | r51 | `knowledge/crawler-identity.md` | S263 |
| JS rendering queue | r48 | `knowledge/js-rendering-queue.md` | S137–S139 |
| Dynamic rendering limits | r48 | `knowledge/dynamic-rendering-workaround-limits.md` | S249 |
| Crawl budget | r49 | `knowledge/crawl-budget-consequences.md` | S273 S274 |
| Crawl-error status | r50 | `knowledge/crawl-error-status-table.md` | S286 |
| Yahoo! JAPAN link attribute (`rel`) | r52; S374 re-read r54 | `knowledge/yahoo-japan-rel-nofollow-semantics.md` | S367 S372 S373 S374 |
| Baidu crawl guidance | r52; locators superseded r53 | `knowledge/baidu-friendly-crawl-guidance.md` | S329 S373 S390 S409 |
| Baidu mobile matching | r52; locators superseded r53 | `knowledge/baidu-mobile-matching-error-causes.md` | S312 S390 S409 |
| Yahoo! JAPAN robots refusal file, pattern syntax, basics | r55 (lands this round) | `knowledge/yahoo-japan-robots-txt-refusal-rules.md` `knowledge/yahoo-japan-robots-pattern-syntax.md` `knowledge/yahoo-japan-robots-txt-basics.md` | S372 S373 S418 |
| Yahoo! JAPAN crawl handling (link-target restriction, deleted URL, non-existent URL) | r56 (lands this round) | `knowledge/yahoo-japan-link-target-crawl-restriction.md` `knowledge/yahoo-japan-deleted-url-recrawl.md` `knowledge/yahoo-japan-nonexistent-url-recrawl.md` | S367 S419 S420 |
| Field performance (CWV, CrUX) | r28 | `knowledge/field-performance-cwv.md` | S036–S039 |
| Jekyll/base-path build tooling | r29 | `knowledge/pages-base-path.md` | S040–S043 |
| Render static sites | r30 | `knowledge/render-static-sites.md` | S049–S052 S061 |
| Render web services and Blueprint | r31 | `knowledge/render-web-services.md` | S057–S060 S062 |
| Link-preview metadata | r34 | `knowledge/link-preview-metadata.md` | S067–S070 S073 |
| security.txt publishing | r35 | `knowledge/security-txt-publishing.md` | S001 S002 S006 S078–S080 S082–S086 |
| Accessibility review preparation | r25 | `knowledge/accessibility-review-packet.md` | S035 |

Two dated row sets hold no entry of their own: the round-39 sitemap-file audit
(S102–S109, `used-by` only `corpus/lessons/round-39.md`; tool
`scripts/sitemap_audit.py`) and the round-53 superseding rows S416/S417
(`used-by` only `corpus/lessons/round-53.md`, correcting the S329/S312
locators). The round-55 row's three entry paths are absent at base by design,
and S418 is not in the base registry; the round-56 row's three entry paths are
absent at its base `e48354b7…`, and S419 and S420 are not in that registry.

**Untouched ground** — PROVINCE frontier items no entry holds yet:

- Accessibility conformance (WCAG 2.2) — `PROVINCE.md:29`. Only the round-25
  preparation packet exists, its cards are `not-assessed`, and
  `PROVINCE.md:77-78` says the packet is not conformance and no website was
  evaluated.
- JS-rendered canonical and rendered-DOM observation — `PROVINCE.md:23`
  ("canonical/JS rendering open"); `PROVINCE.md:361-362` keeps JS rendering open
  and leaves anything that executes a browser to tabi.
- Render live deploy facts (plan, region, domains, deploy trigger) —
  `PROVINCE.md:29`; `PROVINCE.md:120` records they stay unknown from the file.
- Sitemap parsing/scope, crawler-specific extensions, live fetch, redirects and
  caching — `PROVINCE.md:302-303`.
- Sitemap gzip, text/RSS sitemaps, robots `Sitemap:` cross-submission —
  `PROVINCE.md:335-336`.

Held, but ungated or unmeasured (an entry exists; no gate, no owned property
observed): field performance `PROVINCE.md:25-26`, crawl budget
`PROVINCE.md:344`, canonical selection and crawler identity `PROVINCE.md:361`,
the nine per-engine entries (the round-52 trio `PROVINCE.md:382`, the round-55 Yahoo! robots trio
`PROVINCE.md:397`, the round-56 crawl-handling trio `PROVINCE.md:423`). The "Untouched ground" lines about
crawler-specific extensions and robots `Sitemap:` cross-submission predate round 55: one operator's own
pattern-syntax and sitemap-location statements are now held
(`knowledge/yahoo-japan-robots-pattern-syntax.md`,
`knowledge/yahoo-japan-robots-txt-basics.md`), as documentation only, not observed crawler behaviour.

## PROPOSED EDIT: six replacements, each a unique one-occurrence match

E1 — header (line 74):
- old: `### Frontier ground map (round 55; round-56 update)`
- new: `### Frontier ground map (round 55; round-57 update)`

E2 — intro paragraph (lines 77-80):
- old:
  `measured at the round's final revision (156 rows, S418 added), the round-56 row at the round-56`
  `final revision (158 rows, S419 and S420 added), not at base `e48354b7…`. Ranges`
- new:
  `measured at the round's final revision (156 rows, S418 added) and the round-56 row at the round-56`
  `final revision (158 rows, S419 and S420 added), not at base `e48354b7…`; the round-57 row at the`
  `round-57 final revision (160 rows, S421 and S422 added), not at base `28fa0b23…`. Ranges`

E3 — ground-map table, insert one row directly after the r56 row (line 100):
- new:
  `| Baidu dead-link handling (dead-link types, Spider 3.0 recognition model) | r57 (lands this round) | `knowledge/baidu-dead-link-types.md` `knowledge/baidu-spider3-dead-link-model.md` | S421 S422 |`
- Precedent: the r55 and r56 trios each took their own row on the per-engine ground (`PROVINCE.md:22`,
  read through the round-52 block at `PROVINCE.md:374-382`), so the r57 pair takes a row and is not folded
  into the r52 "Baidu crawl guidance" row. Both r57 rows are new (no re-opened id like S367).

E4 — "Two dated row sets…" paragraph (lines 113-115), replace its last sentence:
- old: `absent at its base `e48354b7…`, and S419 and S420 are not in that registry.`
- new:
  `absent at its base `e48354b7…`, and S419 and S420 are not in that registry; the`
  `round-57 row's two entry paths are absent at its base `28fa0b23…`, and S421 and`
  `S422 are not in that registry.`

E5 — "Held, but ungated or unmeasured" paragraph (lines 136-137):
- old:
  `the nine per-engine entries (the round-52 trio `PROVINCE.md:382`, the round-55 Yahoo! robots trio`
  `` `PROVINCE.md:397`, the round-56 crawl-handling trio `PROVINCE.md:423`). ``
- new:
  `the eleven per-engine entries (the round-52 trio `PROVINCE.md:382`, the round-55 Yahoo! robots trio`
  `` `PROVINCE.md:397`, the round-56 crawl-handling trio `PROVINCE.md:423`, the round-57 Baidu pair ``
  `` `PROVINCE.md:433`). ``
- The number in E5 is not free: it must be the line of the round-57 PROVINCE block's own
  `Frontier knowledge:` sentence (the convention every existing ref uses: 382, 397, 423 are those
  sentences, not headings). `433` is what my stub block measured; fill it with
  `awk '/^## Round-57/{f=1} f&&/Frontier knowledge/{print NR; exit}' PROVINCE.md` after that block lands.
  Appended after line 427 with one blank line, its heading lands at 429.

E6 — outside the ground-map section but required by the round-55 counter: two rows in the coverage-map
table, inserted directly after the S420 row (`corpus/README.md:77`):
- `| Baidu dead-link types and handling (r57) | `knowledge/baidu-dead-link-types.md` (S421) | dead-link types, how dead links arise, discovery and handling: a 404 page, a root-directory file and platform submission; submission-tool scope notes (403/500, directory wildcards, index sitemaps, effective period) |`
- `| Baidu Spider 3.0 dead-link recognition model (r57) | `knowledge/baidu-spider3-dead-link-model.md` (S422) | protocol dead links, content dead links and redirect dead links; what the new recognition model claims to identify; the submission-speed claim; no crawl observed |`

No other line of the section changes. In particular the "Untouched ground" list (lines 117-131) is left
byte-identical.

## ORDERING:

1. Entries, E6, E1-E5 and the PROVINCE block land in ONE revision. Both split orders are red at the
   intermediate revision, measured in the scratch clone: README first (`a628217`) → `exit 1, dangling=2`
   (the counter's `dangling` scans every backticked token in the whole `## Coverage map` section, ground-map
   table and prose included, `c55_readme_index.py:208-221`); entries first without E6 (`53f2847`) →
   `exit 1, unindexed=2` (`unindexed` = knowledge file with no row in the first contiguous table). The
   single landing with all of it (`3575d67`) → `exit 0, index_mismatches=0, knowledge_files=54,
   coverage_rows=56`. Round-57 measurement is taken at the tip.
2. PROVINCE before README: E5 needs the round-57 block's `Frontier knowledge:` line to exist. The counter
   does not police line refs (`PROVINCE.md:429` resolved while `PROVINCE.md` still had 427 lines), so a
   stale number is a reviewer catch, not a gate catch.
3. After the append, re-derive E3's Rows cell instead of copying it:
   `git show <rev>:corpus/SOURCES.md | awk -F'|' '/^\| S42[12] /{print $2, $12}'` must print S421→
   `corpus/knowledge/baidu-dead-link-types.md` and S422→`corpus/knowledge/baidu-spider3-dead-link-model.md`,
   and `git show <rev>:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` must
   print `160` (measured `158` at `f7c98ff` and at base `28fa0b23`).
4. Last: `python3 -B .ufo/waves/round-55/c55_readme_index.py --root . --revision <tip>` → expect
   `index_mismatches=0 … EXIT=0` with `knowledge_files=54`, `coverage_rows=56`. E6's cells clear the `thin`
   test with either a rich or a minimal entry head in my probes, but they were written against the entries'
   intended vocabulary; if the landed entries use none of `dead links`, `submission`, `spider`, `sitemaps`,
   re-word the cell rather than touching the entry head (`head_changed` is red for base files only, so a
   new file's head may be edited before landing, never after).

## UNTOUCHED FRONTIER:

No untouched item is claimed, moved or re-read this round; the list stays as written. Items and their
PROVINCE refs, all still open after round 57:

- Accessibility conformance (WCAG 2.2) — `PROVINCE.md:29`; packet-only, `not-assessed`,
  `PROVINCE.md:77-78`.
- JS-rendered canonical / rendered-DOM observation — `PROVINCE.md:23` ("canonical/JS rendering open"),
  `PROVINCE.md:361-362` (tabi's province for anything that executes a browser).
- Render live deploy facts — `PROVINCE.md:29`, `PROVINCE.md:120`.
- Sitemap parsing/scope, crawler-specific extensions, live fetch, redirects, caching — `PROVINCE.md:302-303`.
- Sitemap gzip, text/RSS sitemaps, robots `Sitemap:` cross-submission — `PROVINCE.md:335-336`.

Round 57 adds held, ungated ground only (two entries, no gate, no owned property observed), so it enters
the E5 sentence and not the untouched list; §Frontier (20-30) keeps its bytes.

## PROBE LIMITS

The base is counter-clean: `c55_readme_index.py --revision f7c98ff` → `exit 0, index_mismatches=0,
knowledge_files=52, coverage_rows=54`. The stub entries used in the scratch landings served only the
counter's file-existence and word-overlap tests — they are not the round-57 entries and no content claim
rests on them; the stub PROVINCE block put its `Frontier knowledge:` sentence at line 433 (heading 429).
No `span_tools.py` call was made and no quote is proposed in this report.

VERDICT: README ground map records round 57 with one new per-engine row (r57, S421 S422) plus header, intro, base-note and held-list edits and two required coverage rows; green only when entries, registry rows, PROVINCE block and README land in one revision, measured `exit 0` in a scratch clone.
