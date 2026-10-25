# ScribeGroundMap

Seat: leaf scribe, round-55 kake W1, base `fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d`; draft only — no product file, registry row, PROVINCE line or README byte edited.

## SECTION

```markdown
### Frontier ground map (round 55)

One row per `PROVINCE.md` §Frontier ground that a held entry can be dated to
(`PROVINCE.md:22-30`): the round it entered, the entry, and the `used-by` rows
that entry names in `corpus/SOURCES.md` at base `fcaf4b85…` (155 rows). Ranges
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
and S418 is not in the base registry.

**Untouched ground** — PROVINCE frontier items no entry holds yet:

- Accessibility conformance (WCAG 2.2) — `PROVINCE.md:29`. Only the round-25
  preparation packet exists, its cards are `not-assessed`, and
  `PROVINCE.md:78-79` says the packet is not conformance and no website was
  evaluated.
- JS-rendered canonical and rendered-DOM observation — `PROVINCE.md:23`
  ("canonical/JS rendering open"); `PROVINCE.md:361-362` keeps JS rendering open
  and leaves anything that executes a browser to tabi.
- Render live deploy facts (plan, region, domains, deploy trigger) —
  `PROVINCE.md:29`; `PROVINCE.md:120` records they stay unknown from the file.
- Sitemap parsing/scope, crawler-specific extensions, live fetch, redirects and
  caching — `PROVINCE.md:302`.
- Sitemap gzip, text/RSS sitemaps, robots `Sitemap:` cross-submission —
  `PROVINCE.md:336`.

Held, but ungated or unmeasured (an entry exists; no gate, no owned property
observed): field performance `PROVINCE.md:25-26`, crawl budget
`PROVINCE.md:344`, canonical selection and crawler identity `PROVINCE.md:361`,
the three per-engine entries `PROVINCE.md:382`.
```

## PATH CHECK

Entry paths — `test -e <path>` and `git cat-file -e fcaf4b85:<path>`:

```
$ for e in <20 entries>; do test -e corpus/knowledge/$e.md; git cat-file -e fcaf4b85:$p; done
# condensed two per line, values verbatim
corpus/knowledge/crawl-scope-per-host.md test -e=yes base=yes ; corpus/knowledge/robots-txt-rules.md test -e=yes base=yes
corpus/knowledge/sitemap-orphan-audit.md test -e=yes base=yes ; corpus/knowledge/static-canonical-preflight.md test -e=yes base=yes
corpus/knowledge/canonical-selection.md test -e=yes base=yes ; corpus/knowledge/crawler-identity.md test -e=yes base=yes
corpus/knowledge/js-rendering-queue.md test -e=yes base=yes ; corpus/knowledge/dynamic-rendering-workaround-limits.md test -e=yes base=yes
corpus/knowledge/crawl-budget-consequences.md test -e=yes base=yes ; corpus/knowledge/crawl-error-status-table.md test -e=yes base=yes
corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md test -e=yes base=yes ; corpus/knowledge/baidu-friendly-crawl-guidance.md test -e=yes base=yes
corpus/knowledge/baidu-mobile-matching-error-causes.md test -e=yes base=yes ; corpus/knowledge/field-performance-cwv.md test -e=yes base=yes
corpus/knowledge/pages-base-path.md test -e=yes base=yes ; corpus/knowledge/render-static-sites.md test -e=yes base=yes
corpus/knowledge/render-web-services.md test -e=yes base=yes ; corpus/knowledge/link-preview-metadata.md test -e=yes base=yes
corpus/knowledge/security-txt-publishing.md test -e=yes base=yes ; corpus/knowledge/accessibility-review-packet.md test -e=yes base=yes
```

Future paths of the round-55 row (absent at base and in the worktree, as expected):

```
corpus/knowledge/yahoo-japan-robots-txt-refusal-rules.md test -e=NO base=NO
corpus/knowledge/yahoo-japan-robots-pattern-syntax.md test -e=NO base=NO
corpus/knowledge/yahoo-japan-robots-txt-basics.md test -e=NO base=NO
```

S-ids — `git show fcaf4b85:corpus/SOURCES.md > /tmp/reg55.md`, then
`grep -cE '^\| <id> \|' /tmp/reg55.md` for each id in the table (ranges expanded):

```
S011=1 S012=1 S013=1 S034=1 S095=1 S096=1 S098=1 S099=1 S100=1 S101=1
S001=1 S002=1 S003=1 S004=1 S005=1 S006=1 S065=1 S066=1
S020=1 S021=1 S024=1 S025=1 S026=1 S027=1 S028=1 S029=1 S030=1 S031=1 S032=1 S033=1
S035=1 S036=1 S037=1 S038=1 S039=1 S040=1 S041=1 S042=1 S043=1
S049=1 S050=1 S051=1 S052=1 S057=1 S058=1 S059=1 S060=1 S061=1 S062=1
S067=1 S068=1 S069=1 S070=1 S073=1
S078=1 S079=1 S080=1 S082=1 S083=1 S084=1 S085=1 S086=1
S137=1 S138=1 S139=1 S249=1 S262=1 S263=1 S273=1 S274=1 S286=1
S312=1 S329=1 S367=1 S372=1 S373=1 S374=1 S390=1 S409=1
S102=1 S103=1 S104=1 S105=1 S106=1 S107=1 S108=1 S109=1 S416=1 S417=1
S418=0
```

The S102–S109 and S416/S417 ids are the ones the section names outside the
table (round-39 and round-53 note rows); S418 is the only cited id absent at
base.

Counts: base registry 155 rows (`grep -cE '^\| S[0-9]+' /tmp/reg55.md`); base
`corpus/knowledge` 46 files (43 `.md`, 3 `.json`), equal to the worktree.
`used-by` extraction: `grep -F "corpus/knowledge/<entry>.md" corpus/SOURCES.md`
per entry, id from the row head. Round dates: adding commit from
`git log --diff-filter=A --date=short --format='%h %ad %s' -- <entry>` (e.g.
`crawl-scope-per-host` `02b6dd0` r20, `canonical-selection`/`crawler-identity`
`5591557` r51, the three r52 entries `5422ff3`), cross-read against
`corpus/lessons/round-4[8-9].md` and `round-5*.md`.

## FINDINGS

- **Placement changes C1's measurement** [INFERENCE from `c55_readme_index.py`,
  not run]: `coverage_section()` slices `## Coverage map` to the next `^## `,
  every `|` line in that slice becomes a coverage row, and the coverage text is
  the row's **last** cell (`cells[-1]`). Inside that slice this map's rows read
  `thin` (<5 words) for entries no earlier row names, and its three future paths
  read `dangling` (+3); under a later `##` heading the slice excludes it.
- **S373 `used-by` spans two engines**: the Yahoo! JAPAN pattern-syntax row
  names both `knowledge/yahoo-japan-rel-nofollow-semantics.md` and
  `knowledge/baidu-friendly-crawl-guidance.md`. Recorded as the registry states
  it; not adjudicated here.
- **The round-55 row is false until C2 lands**: its three entry paths are absent
  at base (checked above), hence the `(lands this round)` mark.

## UNEVIDENCED

- **Round-39 sitemap-file audit has rows but no entry.** S102–S109 exist (all
  checked =1) and are dated to round 39, but their `used-by` is only
  `corpus/lessons/round-39.md`; the artifact is `scripts/sitemap_audit.py`. No
  knowledge entry entered that ground, so no entry can be dated to r39.
- **Rows added without a new entry.** S367 (r53) names only the r52 entry
  `knowledge/yahoo-japan-rel-nofollow-semantics.md`; S390/S409 (r53) name only
  the two r52 Baidu entries. Their rounds are datable, their entries are not
  new. S416/S417 (r53) are metadata-only superseding rows (`used-by`
  `corpus/lessons/round-53.md`).
- **Round dates for r48–r52 entries rest on commits and lessons, not on a
  frontier-step section.** `corpus/README.md` coverage sections stop at round 39
  and `PROVINCE.md` has no round-48 or round-50 block, so those dates come from
  the adding commit subject and the round lesson. Field performance (r28)
  likewise has no `## Round-28` PROVINCE block; its date is `PROVINCE.md:25`
  plus README §Round-28.
- **No round exists for live per-engine behavior or rendered DOM.** Neither was
  ever observed (`PROVINCE.md:361-362`, `PROVINCE.md:382`), so no round can be
  named for them.
- **Out of scope, not unevidenced.** The other 23 markdown entries hold ground
  `PROVINCE.md` §Frontier does not name (Core publishing/operability plus the
  r46 redirect-rewrite entry); this map does not date them.

VERDICT: frontier ground map drafted with 21 rows (20 dated to base-existing entries, 1 landing this round); 20 entry paths and 91 S-ids verified =1 at base, S418 and the three round-55 paths verified absent at base.
