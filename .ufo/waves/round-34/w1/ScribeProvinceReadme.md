# KakeR34.ScribeProvinceReadme — round-34 PROVINCE and corpus README drafts
Status: drafts only; neither target was modified and I ran neither counter. The
only execution evidence read is the before state at d08d8de (C1 0/28,
constants rejected; C2 met 0/5); insert only with both receipts at the
integrated revision.

Insertion: PROVINCE.md after line 156 (`operator-owned property.`, close of
`## Round-33 frontier step`; 156 lines); corpus/README.md after line 311
(`re-pinned (needs the sweep's armed section).`; 311 lines).

## Draft 1 — PROVINCE.md, verbatim

```markdown
## Round-34 link-preview frontier step

Link-preview metadata — the Open Graph properties a platform reads to build a
card for a shared URL — enters the Frontier as held ground with a source-backed
entry and an offline gate. The entry,
`corpus/knowledge/link-preview-metadata.md`, is grounded in S067 ogp.me, S068
Meta's sharing guide for webmasters, S069 Slack's robots page and S070
Mastodon's PreviewCard entity, and states the ds4cc Open Graph census of the
retained upstream tree at `7fc6aa2f`: 102 pages, 87 with `og:title`, 87 with
`og:type`, 87 with `og:url`, 1 with `og:image`, 1 with all four, and 87 whose
`og:url` equals the page canonical. The gate, `scripts/link_preview_audit.py`,
reads a version-1 manifest of local HTML pages and absolute page URLs and,
network-free, reports a missing one of the four required properties (S067),
more than one `og:type` (S068), a non-absolute `og:url`, and an `og:url`
differing from the first `<link rel=canonical>` resolved against the page URL.
Exit, verdict and finding shapes and the 28 frozen cases are in
`.ufo/waves/round-34/c1-matrix.json`; the counters are
`.ufo/waves/round-34/c1_matrix_count.py` and `c2_source_census.py`.

The Frontier paragraph at line 30 says ground moves to Core only with
source-backed entries and a gate. Both conditions are supplied: the entry's
quotes are exact substrings of the retained text, and the gate has a frozen
case matrix and a counter that rejects four constant implementations. The
round takes this ground from open to held Frontier ground, not Core; no Core
line is added and no older line is rewritten.

Nothing live was observed: the gate reads local files only, and the sources
were opened with one public GET each at 20:57Z (`sources/receipts.json`). No
operator-owned property was fetched. Open: live platform rendering (no card
was requested or observed; Slack's link robot reads tags over HTTP Range and
fetches referenced media, S069; Mastodon generates a PreviewCard from Open
Graph tags, S070); X card tags, whose markup URL S071 now redirects to a
generic documentation index and so grounds nothing; image checks beyond a
non-empty `og:image` (no fetch, MIME, dimension, HTTPS or reachability test);
`name=` meta forms, the other `og:*` properties and per-type extra required
properties (S067). The census observes source bytes and repairs nothing: 101
of 102 pages carry no non-empty `og:image`.
```

## Draft 2 — corpus/README.md, verbatim

```markdown
## Coverage — round 34 (2026-10-22)

| Area | Entry | Coverage |
|---|---|---|
| Link-preview metadata (r34) | `knowledge/link-preview-metadata.md` (S067–S070) | The Open Graph properties a platform reads to build a card for a shared URL: the four required properties and their meanings (S067); each URL is a single object, so multiple `og:type` values are not possible, and `og:url` is the canonical URL without session variables or counters (S068); Slack's link-expanding robot reads oEmbed and Twitter Card / Open Graph tags with HTTP Range requests and fetches referenced media to check validity (S069); Mastodon's PreviewCard is generated from Open Graph tags (S070). States the ds4cc census of the retained `7fc6aa2f` tree: 102 pages, `og:title` 87, `og:type` 87, `og:url` 87, `og:image` 1, all four 1, `og:url` equal to canonical 87. Platform rendering, X card tags and image validity are not covered |
| Offline link-preview audit (r34) | `scripts/link_preview_audit.py` and `.ufo/waves/round-34/c1-matrix.json` | A version-1 manifest of local HTML pages and absolute page URLs is audited network-free for a missing required property, more than one `og:type`, a non-absolute `og:url` and an `og:url` differing from the first canonical link resolved against the page URL; clean exits 0, policy findings 1, input findings 2, usage 64. 28 frozen cases, four constants each required to fail at least one case; counters `c1_matrix_count.py` and `c2_source_census.py` |

`corpus/SOURCES.md` gains rows S067–S070 (mined, opened 2026-10-22). S071 (X
card markup) and S072 (GitHub social preview) were opened for screening and
are rejection candidates (S071 redirects to a generic documentation index),
so neither grounds an entry and X card tagging stays open. The census is
source-side: no operator-owned property was fetched, no card was rendered and
no page was repaired.
```
## Evidence read (exit 0 each)

- `c1-matrix.json`: 28 cases; per-case comparison on exit, verdict and projected findings.
- `verification/c1-at-d08d8de.json`: passed 0/28, constantGatesAllRejected true, constantGatesPassed 6/28, 0/28, 6/28, 1/28.
- `verification/c2-at-d08d8de.json` `census.derived`: pages 102, og:title 87, og:type 87, og:image 1, og:url 87, all-four 1, og-url-equals-canonical 87; met 0/5, controlBroken false.
- `c2_source_census.py` conditions a-e; `sources/S067-S070` phrase probes; `receipts.json` all six 200, S071 finalUrl docs.x.com/overview.
## Limits

- Census numbers are the before receipt's derived recount; the entry must state that exact line for condition (e). "28 frozen cases" is matrix size, not a pass count.
- PROVINCE.md:22-30 and the round-33 sections are untouched; no network reads, no installs, no lane writes beyond this report.
