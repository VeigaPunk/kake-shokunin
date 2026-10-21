# Rejection06S012: falsify attempt against the L1 rejection of the S012 seat STALE

Lane: kake-shokunin · Milestone: r26-recheck-falsify · Axis: freshness · Candidate `e28312b14b076584fedd696fae2a684e460bd11e` · Base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`

**Verdict: AGREE.** The L1 rejection is correct. The pointer `corpus/knowledge/freshness-sweep.md:58` in `crawl-scope-per-host.md` was true at its stated base. It maps exactly to the current A4 row under the round-21 register. The scope it cites still holds in the retained S012 bytes. No staleness is hidden.

## What was attacked

- Ledger: `statements.json` lists S012 with `seatStale: 1`, `stale: 0`, and `l1Disposition` "same base-scoped pointer as PairS011." The S011 disposition reads: "freshness-sweep.md:58 pointer is base-scoped (\"Refines at base cb807bc\"); +4 rule covers current coordinates."
- Seat finding: `w1/PairS012CrawlScopePerHost.md` row 7 says STALE (anchor). Its reason is that current `:58` is the H4 `scripts/probe-delta.mjs` row, and that the sitemap rows are now `:62-63`.
- Rule: `corpus/QUALITY.md:217-221`: "a pointer explicitly scoped to a base revision … is not a stale claim; record it as a note. A statement whose attribution was false even at its base revision is STALE."

The strongest counterexample is that the attribution was already false at `cb807bc`, or that the +4 mapping does not land on sitemap or host text. Both were tested. Both fail.

## Evidence

1. **The pointer is explicitly base-scoped.** Base entry lines 20–22 read: "**Refines at base `cb807bc`.** Makes host/path scope explicit for `corpus/knowledge/sitemap-orphan-audit.md:40-47` and `corpus/knowledge/freshness-sweep.md:58`".

2. **The attribution was true at the base.** Output of `git show cb807bc:corpus/knowledge/freshness-sweep.md | sed -n 58p`:
   `| A4 | armed | ds4cc sitemap/robots pre-push state | \`sitemapStatus\` 404 | \`200\` → \`LISTED-LIVE\` |`
   This is a sitemap/robots row. Line 58 is the same A4 row at 02b6dd0 (the round-20 commit that wrote the entry), at 9639ec7, and at the register baseline 5009ecaa.

3. **The attribution is in scope.** A4 probes `sitemapUrl: 'https://ds4cc.com/sitemap.xml'` (base `scripts/freshness-sweep.mjs:85`, with the verdict at :907–913). The bullet's job is exactly to say that ds4cc.com is a different host from `veigapunk.github.io`. So "host/path scope explicit for" A4 is a correct attribution, not a false one.

4. **The +4 mapping is exact.** In base `corpus/lessons/round-21.md`, line 127 reads `| freshness-sweep.md | N → N+4 |`, and lines 116–117 read "old line N at baseline `5009ecaa` is current line N+4". The pointer predates round 21 (02b6dd0 is an ancestor of 5009ecaa). Byte-identity check:
   - `cb807bc` freshness-sweep lines 1–58: sha256 `7ff58b3f…a2134`
   - `5009ecaa` lines 1–58: sha256 `7ff58b3f…a2134`
   - base `97404de` lines 5–62: sha256 `7ff58b3f…a2134`

   So base line 62 is the A4 row, the same bytes as old :58. The seat's own "sitemap rows are now :62-63" is exactly what the +4 rule yields. The seat read current coordinates for a pre-round-21 pointer, which `QUALITY.md:69-73` forbids.

5. **The source still supports the scope.** Retained `fetched/S012-1.raw.gz` decompresses to sha256 `5e7570590fcb92d473d7015c88940a830383b6a61bc6c16be4df51e97f471654`, 45,292 bytes, HTTP 200 (`manifest.json:244-250`). In `text/S012-1.txt`, each of these occurs exactly once:
   - "The location of a Sitemap file determines the set of URLs that can be included in that Sitemap."
   - "all URLs in a Sitemap must be from a single host"

6. **The candidate's appended note is consistent with this.** It says: "Pointers labelled `at base cb807bc` stay base-scoped (QUALITY.md round-21 coordinate rule), so current-tree line movement is not a stale claim." Because `cb807bc` and `5009ecaa` have byte-identical lines 1–58 of the target, the `cb807bc` label and the register baseline name the same coordinates.

## Adjacent observations (these do not overturn the rejection)

- **Seat row 6 used the wrong coordinates, but its HOLD verdict stands.** The seat read current `sitemap-orphan-audit.md:40-47`, which includes the listing-coverage tail and puts "## Procedure" at :44. Under the register (the same file is listed N → N+4), the base `:40-47` bytes are current `:44-51`. Those lines hold "## Procedure" and the per-host live `sitemap.xml` list, and they are identical to `cb807bc:40-47`. The HOLD verdict is unchanged. The seat applied the +4 rule to neither pointer, which is the same root error as its row-7 STALE.
- **Seat text-view provenance predates the committed file.** The seat cites `text/S012-1.txt` as 21,172 B with sha256 `3dac1076…`. The committed file is 21,212 B, sha256 `3008775c…cf5b`, last touched in `e28312b`. So the seat's byte offsets (for example 12127) do not index the committed view. In the committed view, after the BOM, the quote sits at byte 12167. The quotes still occur exactly once, so no verdict changes. This is low severity and belongs to the seat or the text-view owner, not this rejection.

## Minimal correction

None required for the rejection. Optionally, the row-7 seat finding could be recorded as a note: "old :58 ≡ current :62 (A4) per the round-21 register", rather than leaving it as a downgraded STALE.

## Commands run (read-only)

`git show`, `git log`, `git grep`, `git merge-base --is-ancestor`, `git diff 97404de..e28312b -- corpus/knowledge/crawl-scope-per-host.md`, `sha256sum`, plus Python stdlib (gzip, hashlib) on the retained bytes. There was no network GET, no `measure.py` run, and no edits outside this report. Installs or updates: none. Round-24 material: not read.

```json
{"target":"S012 L1 rejection (crawl-scope-per-host.md freshness-sweep.md:58 base-scoped pointer)","verdict":"AGREE","severity":"none"}
```
