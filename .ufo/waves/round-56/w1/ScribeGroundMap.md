# ScribeGroundMap

Seat: round-56 W1 scribe (leaf). Target: `corpus/README.md` §`### Frontier ground map (round 55)`,
lines 71–134 at base `e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`; those bytes are identical at lane
HEAD `6b3df99d` (`git diff --stat e48354b7..HEAD -- corpus/README.md PROVINCE.md corpus/knowledge`
empty), so the diff applies at either revision. Only this report was written in the lane.

## CURRENT SECTION:

```
### Frontier ground map (round 55)

One row per `PROVINCE.md` §Frontier ground that a held entry can be dated to
(`PROVINCE.md:22-30`): the round it entered, the entry, and the `used-by` rows
that entry names in `corpus/SOURCES.md` at base `fcaf4b85…` (155 rows); the round-55 row is
measured at the round's final revision (156 rows, S418 added), not at base. Ranges
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
the six per-engine entries (the round-52 trio `PROVINCE.md:382`, the round-55 Yahoo! robots trio
`PROVINCE.md:397`). The "Untouched ground" lines about crawler-specific extensions and robots
`Sitemap:` cross-submission predate round 55: one operator's own pattern-syntax and sitemap-location
statements are now held (`knowledge/yahoo-japan-robots-pattern-syntax.md`,
`knowledge/yahoo-japan-robots-txt-basics.md`), as documentation only, not observed crawler behaviour.
```

## PROPOSED EDIT:

Measured diff (read-only clone, `git diff --unified=1 e48354b7..98db18a4 -- corpus/README.md`;
`git apply --check` against base exits 0). Five hunks touch lines 71, 76, 92, 109 and 131–134;
every other line is unchanged — the "Untouched ground" bullets (115–127) are byte-identical:

```diff
diff --git a/corpus/README.md b/corpus/README.md
index 24a2209..d649d10 100644
--- a/corpus/README.md
+++ b/corpus/README.md
@@ -70,3 +70,3 @@ mirrors, Pages deploys).
 
-### Frontier ground map (round 55)
+### Frontier ground map (round 55; round-56 update)
 
@@ -75,3 +75,4 @@ One row per `PROVINCE.md` §Frontier ground that a held entry can be dated to
 that entry names in `corpus/SOURCES.md` at base `fcaf4b85…` (155 rows); the round-55 row is
-measured at the round's final revision (156 rows, S418 added), not at base. Ranges
+measured at the round's final revision (156 rows, S418 added), the round-56 row at the
+round-56 final revision (158 rows, S419 and S420 added), not at base `e48354b7…`. Ranges
 are inclusive and each id was checked individually; a row set is the entry's
@@ -91,3 +92,3 @@ are inclusive and each id was checked individually; a row set is the entry's
 | Crawl-error status | r50 | `knowledge/crawl-error-status-table.md` | S286 |
-| Yahoo! JAPAN link attribute (`rel`) | r52; S374 re-read r54 | `knowledge/yahoo-japan-rel-nofollow-semantics.md` | S367 S372 S373 S374 |
+| Yahoo! JAPAN crawl handling (link attribute `rel`; link-target crawl restriction, deleted URL, non-existent URL) | r52; S374 re-read r54; crawl-handling trio r56 | `knowledge/yahoo-japan-rel-nofollow-semantics.md` `knowledge/yahoo-japan-link-target-crawl-restriction.md` `knowledge/yahoo-japan-deleted-url-recrawl.md` `knowledge/yahoo-japan-nonexistent-url-recrawl.md` | S367 S372 S373 S374 S419 S420 |
 | Baidu crawl guidance | r52; locators superseded r53 | `knowledge/baidu-friendly-crawl-guidance.md` | S329 S373 S390 S409 |
@@ -108,3 +109,4 @@ Two dated row sets hold no entry of their own: the round-39 sitemap-file audit
 locators). The round-55 row's three entry paths are absent at base by design,
-and S418 is not in the base registry.
+and S418 is not in the base registry; the round-56 trio's three paths are
+absent at the round-56 base `e48354b7…`, and S419 and S420 are not in it.
 
@@ -129,6 +131,8 @@ observed): field performance `PROVINCE.md:25-26`, crawl budget
 `PROVINCE.md:344`, canonical selection and crawler identity `PROVINCE.md:361`,
-the six per-engine entries (the round-52 trio `PROVINCE.md:382`, the round-55 Yahoo! robots trio
-`PROVINCE.md:397`). The "Untouched ground" lines about crawler-specific extensions and robots
-`Sitemap:` cross-submission predate round 55: one operator's own pattern-syntax and sitemap-location
-statements are now held (`knowledge/yahoo-japan-robots-pattern-syntax.md`,
+the nine per-engine entries (the round-52 trio `PROVINCE.md:382`, the round-55 Yahoo! robots trio
+`PROVINCE.md:397`, the round-56 crawl-handling trio `.ufo/waves/round-56/contract.md` claim C2 —
+`PROVINCE.md` carries no round-56 block at base `e48354b7…`). The "Untouched ground" lines about
+crawler-specific extensions and robots `Sitemap:` cross-submission predate round 55: one operator's
+own pattern-syntax and sitemap-location statements are now held
+(`knowledge/yahoo-japan-robots-pattern-syntax.md`,
 `knowledge/yahoo-japan-robots-txt-basics.md`), as documentation only, not observed crawler behaviour.
```

Why each hunk: (1) the table holds a round-56 row, so the heading's date must not say round 55 only;
(2) the measurement rule needs the round-56 row's revision and count — 158 = the contract's After
value, 156 measured at base and HEAD (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` on
`git show <rev>:corpus/SOURCES.md`); (3) the per-engine row gains three entries — `used-by` S367,
S419, S420 — its cell being the union with the existing S367 S372 S373 S374; (4) the base-absence
note extends to the trio; (5) "six per-engine entries" becomes nine, dated to the committed contract
because `PROVINCE.md` has no round-56 block at base. The last hunk re-wraps unchanged words only.

## ORDERING:

`c55_readme_index.py` collects `dangling` from the whole `## Coverage map` section (`coverage_sections`
stops at the next `## `), so frontier-table paths are resolved against `git ls-tree` **at the measured
revision**: this diff alone is red. Measured in a read-only clone (`D=$(mktemp -d)` →
`/tmp/c56-readme-4dzsaq8s`, `git clone` of the lane, toplevel == `$D`, commits
`-c user.name=selftest -c user.email=selftest@local`; the lane was never written):

| state | revision | output |
|---|---|---|
| lane HEAD, untouched | `6b3df99d` | exit 0, `index_mismatches=0 knowledge_files=49 coverage_rows=51` |
| this diff only, entries absent | `98db18a4` | exit 1, `dangling=3` — exactly the three new paths |
| stubs + 3 index rows after a blank line (second table) | `4322d1ee` | exit 1, `unindexed=3 dangling=0` |
| stubs + 3 index rows inside the first contiguous table | `60259f73` | exit 0, `coverage_rows=54 knowledge_files=52` |

Order for the L1:

1. Land the three entry files, the S419/S420 rows, the S367 `used-by` extension **and** one index row
   per entry inside the *first contiguous* table of `## Coverage map` — no blank line before them, or
   the block becomes a second table and indexes nothing (row 3 above). Shape per `corpus/QUALITY.md`
   round-55 criterion 1: Entry cell exactly `` `knowledge/<path>` ``, ≤2 knowledge paths per row
   (`multi`), Coverage cell ≥5 tokens sharing a non-common word with the entry head (`thin`), no
   repeated normalized cell (`duplicate`).
2. Then this diff, or both in one commit — the counter reads a single revision.
3. Measure: `python3 -B .ufo/waves/round-55/c55_readme_index.py --root . --revision <rev>` →
   `index_mismatches=0`; never measure the edit at a revision without the three files.

Owed before landing: re-derive the Rows cell from the landed `used-by` cells
(`git show <rev>:corpus/SOURCES.md | grep -E '^\s*\|\s*S(367|419|420)\s*\|'`; if an entry also names
S372/S373 the cell grows) and the 158 with the census command, writing what it prints.

## UNTOUCHED FRONTIER:

Round 56 touches none of these; the diff leaves lines 113–127 byte-identical. Verified by reading each
line (`grep -n "" PROVINCE.md | sed -n ...`):

| Item | PROVINCE ref | Why still untouched |
|---|---|---|
| Accessibility conformance (WCAG 2.2) | `PROVINCE.md:29` | only the r25 preparation packet; `:78` "not WCAG conformance" |
| JS-rendered canonical / rendered-DOM | `PROVINCE.md:23`, `:361-362` | browser execution stays tabi's |
| Render live deploy facts (plan, region, domains, trigger) | `PROVINCE.md:29`, `:120` | unknown from the file |
| Sitemap parsing/scope, crawler-specific extensions, live fetch, redirects, caching | `PROVINCE.md:302-303` | r56 opens none of them |
| Sitemap gzip, text/RSS sitemaps, robots `Sitemap:` cross-submission | `PROVINCE.md:335-336` (text at 336–337, see findings) | unchanged |

Field performance (Core Web Vitals) and Jekyll/base-path are **held, not untouched** — the map lists
them under "Held, but ungated" (`PROVINCE.md:25-26`); r56 adds nothing to either. The three new entries
join that list, taking the per-engine count from six to nine.

## FINDINGS (routed, not fixed here)

1. **Ref off by one.** "Sitemap gzip, text/RSS sitemaps, robots `Sitemap:` cross-submission —
   `PROVINCE.md:335-336`": the "Still open:" list is on `PROVINCE.md:336-337` (336 ends "Still open:
   gzip, live"; 337 "fetch, text/RSS sitemaps, robots cross-submission, and a key that kills those 15
   breaks"). Round-55 residue, so left in place; fix: `-  \`PROVINCE.md:335-336\`.` →
   `+  \`PROVINCE.md:336-337\`.`.
2. **`PROVINCE.md:398` is superseded.** The round-55 block ends "…and deleted-URL pages in the staging
   package are not adopted this round" — true for r55, but r56 adopts the deleted-URL page (002856 →
   S419). The L1's round-56 PROVINCE block or a dated note must say so; the README map cannot.
3. **Variant, same counter effect.** If one row per ground is preferred over a 4-entry row, add after
   line 92, leaving the round-52 row byte-identical:
   ```
   | Yahoo! JAPAN crawl handling (link-target restriction, deleted URL, non-existent URL) | r56 (lands this round) | `knowledge/yahoo-japan-link-target-crawl-restriction.md` `knowledge/yahoo-japan-deleted-url-recrawl.md` `knowledge/yahoo-japan-nonexistent-url-recrawl.md` | S367 S419 S420 |
   ```
   Same three tokens, so `dangling` behaves identically. The primary diff follows the assignment's
   "the row gains the three entries".

## Limits

- The three entry files exist nowhere (`ls` → no such file at base or HEAD), so claims about their
  content are planned, not read; the Rows cell is arithmetic on the contract's row mapping plus the
  existing set. The clone's fixture entries are two-line stubs: they prove path resolution and
  index-row placement only, never quote truth or entry fidelity.
- `158` is the contract's declared After value; only `156` was measured (base and HEAD).
- No tool installed, no network read, no lane/sibling/jj/Git-index mutation; only this report written.

VERDICT: Diff drafted and proven order-sensitive — the README edit alone makes `c55_readme_index.py`
report `dangling=3` (exit 1); with the three entries plus three index rows inside the first coverage
table it reports `index_mismatches=0` (exit 0).
