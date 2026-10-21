# PairS011CrawlScopePerHost: S011 x corpus/knowledge/crawl-scope-per-host.md

Round 26 · C1 freshness · knowledge pair seat · milestone r26-recheck-build · leaf seat (no dispatch)

## Result

- Statements attributed to S011 in the entry: **20**. HOLD **19**, STALE **1**, UNVERIFIABLE **0**.
- The retained RFC 9309 text supports every S011 quote and every S011-derived rule in the entry. Nothing S011 says is contradicted.
- The one STALE is an anchor. `crawl-scope-per-host.md:22` cites `corpus/knowledge/freshness-sweep.md:58` for host/path scope, but line 58 is now the H4 history row. The host-scoped robots/sitemap row is line 62. Correction C-1 is below.
- Row teaches (`corpus/SOURCES.md:19`, "Robots rules are located at the service's top-level /robots.txt; an unreachable robots file requires crawlers to assume complete disallow"): **HOLD**. Quotes K04 and K15 are verbatim in the retained text.

## Retained bytes (checked this run)

- Source: RFC 9309, Robots Exclusion Protocol, Standards Track, Published September 2022, ISSN 2070-1721. URL `https://www.rfc-editor.org/rfc/rfc9309.html`.
- Manifest row (`fetched/manifest.json`, index 1): HTTP 200, `fetchedAt` 2026-10-21T15:10:38.867462+00:00, 82,367 bytes, sha256 `bbaa280636d3e38f0a1a130a5ce40e9753db1ed18c860945b0bf795ff8dc1a87`. Decompressing `fetched/S011-1.raw.gz` gives the same size and sha256.
- Text view `fetched/text/S011-1.txt`: 21,232 characters, sha256 `1364638f387475ef2c09dcdc39e3db09a43ebe14e8faf4db1064dec0179d904c`. Every quote below is a contiguous substring of this view.
- The raw HTML breaks some phrases across newlines and `<span class="bcp14">` tags. Raw substring counts are 0 for "top-level path of the service", "MAY access any resources on the server" and "MUST assume complete disallow". The visible text is the same sentence, so the text view is the quote authority.

## Entry under test

- `corpus/knowledge/crawl-scope-per-host.md`: 53 lines, 3,160 bytes, **no trailing newline**. Any EOF append must begin with a newline. sha256 prefix `669d9da571383edf`.
- No `r20` tag, no correction tail, and no appended section exists in this file. The closest block is "Refines at base cb807bc" (lines 20-24), judged below. The round-20 S011 record is `corpus/lessons/round-20.md:213`, outside this entry, not judged.
- Not S011-dependent, excluded: lines 14-17 and 30-35 (S012/S013 sitemap statements), line 2's Google date (S013), lines 37-41 (population count; the "three" count is not judged), lines 52-53 (QUALITY labels), and the headings at lines 5 and 48 (titles only). Line 26's "quotes reopened 2026-10-19" header is a dated S011 claim, flagged on K-13.

## Statement table

Verdicts: HOLD = supported at its anchor against retained text. STALE = wrong or incomplete now. UNVERIFIABLE = retained bytes cannot decide (none).

| ID | file:line | statement (abridged) | verdict | verbatim quote from S011-1.txt | anchor, reason, flags |
|---|---|---|---|---|---|
| K-01 | :1 | header lists S011 for §2.3/§2.3.1.3/§2.3.1.4 | HOLD | "2.3. Access Method The rules MUST be accessible in a file named"; "2.3.1.3. "Unavailable" Status "Unavailable" means the crawler tries to fetch the robots.txt file"; "2.3.1.4. "Unreachable" Status If the robots.txt file is unreachable due to server or network errors" | All three headings exist with these titles. Flag: header URL has no `.html` (manifest and SOURCES use `rfc9309.html`). Same RFC, no verdict change. |
| K-02 | :2 | `verified-at: 2026-10-19` (RFC 9309 published September 2022) | HOLD + FLAG | "Category: Standards Track Published: September 2022 ISSN: 2070-1721" | Published date holds. Flag: the 2026-10-19 verified-at is superseded by the retained fetch above. Content unchanged, so no correction. The Google docs date belongs to S013. |
| K-03 | :3 | recheck command: curl of `rfc9309.txt`, then grep -cF for the phrase | HOLD + FLAG | "in the top-level path of the service" | Phrase occurs once in the retained text (count 1). The `.txt` endpoint is not retained, so the exact command was not re-run (see gaps). Flag: the command uses `.txt`; the retained bytes are `.html`. |
| K-04 | :7-8 | robots rules are discovered at the service root `/robots.txt`, not per project-page subpath | HOLD | "The rules MUST be accessible in a file named "/robots.txt" (all lowercase) in the top-level path of the service." | §2.3 holds. The URI is given as `scheme:[//authority]/robots.txt`, so the location is per authority. |
| K-05 | :8-10 | the three lane sites under `veigapunk.github.io/<repo>/` share one host-root robots policy | HOLD (S011 part) | "the URI of the robots.txt file is" | Same authority, so one robots file. The count "three" is not decided by S011 and is not judged here. |
| K-06 | :10-11 | 4xx robots response means crawlers MAY access resources | HOLD | "If a server status code indicates that the robots.txt file is unavailable to the crawler, then the crawler MAY access any resources on the server." | §2.3.1.3. The RFC gives the HTTP range as "such status codes are in the 400-499 range", so the 4xx paraphrase holds. |
| K-07 | :11-12 | 5xx or network-unreachable response means crawlers MUST assume complete disallow | HOLD | "in the context of HTTP, server errors are identified by status codes in the 500-599 range"; "the crawler MUST assume complete disallow" | §2.3.1.4. Both clauses are present. |
| K-08 | :12 | "subject to RFC 9309's long-outage allowance" | HOLD | "If the robots.txt file is undefined for a reasonably long period of time"; "crawlers MAY assume that the robots.txt file is unavailable as defined in Section 2.3.1.3 or continue to use a cached copy" | The allowance is in §2.3.1.4. The entry does not restate the example of 30 days, which is not a defect in the claim. |
| K-09 | :17-18 | a `Sitemap:` line in the host-root robots file is a supported discovery route | HOLD (S011 part) | "Crawlers MAY interpret other records that are not part of the robots.txt protocol" | S011 gives the host-root location (§2.3) and lists "Sitemaps" as an other record crawlers MAY interpret (§2.2.4). "Supported discovery route" is the S013 claim, not judged here. |
| K-10 | :20-21 | "Refines at base cb807bc": host/path scope made explicit for `sitemap-orphan-audit.md:40-47` | HOLD (anchor) | "The rules MUST be accessible in a file named "/robots.txt" (all lowercase) in the top-level path of the service." | Lines 40-42 (path coverage) and 44-47 (URL-list procedure, "Live `sitemap.xml`: plazir15-ghp ✓ (8 locs), charter-ghp ✓ (2 locs)") still carry host/path scope. Base content was not compared. |
| K-11 | :22 | same refinement: host/path scope made explicit for `freshness-sweep.md:58` | **STALE (anchor only)** | "The rules MUST be accessible in a file named "/robots.txt" (all lowercase) in the top-level path of the service." | Line 58 is now the H4 history row (`scripts/probe-delta.mjs`), not host or path scope. The only table row naming robots is A4 ("ds4cc sitemap/robots pre-push state"), now at line 62. A5 (line 63) is a sitemap row for another host and does not replace it. The S011 claim itself holds. Correction C-1. |
| K-12 | :22-24 | ds4cc.com 404 at `publish-queue.md:88-93` is a different host, not a current observation about veigapunk.github.io | HOLD | "The rules MUST be accessible in a file named "/robots.txt" (all lowercase) in the top-level path of the service." | Authority scope. `publish-queue.md:92-93` still carries the r14 "live 404" text for ds4cc.com sitemap and robots, inside the 88-93 range. |
| K-13 | :27 | S011 §2.3 quote "in the top-level path of the service" | HOLD | "in the top-level path of the service" | Verbatim. Flag: the header at line 26, "quotes reopened 2026-10-19", is superseded by the retained re-fetch; the quotes still match (count 1). |
| K-14 | :27-28 | S011 §2.3.1.3 quote "MAY access any resources on the server" | HOLD | "the crawler MAY access any resources on the server" | Verbatim, in §2.3.1.3 "Unavailable" Status. |
| K-15 | :28-29 | S011 §2.3.1.4 quote "MUST assume complete disallow." | HOLD | "this means the robots.txt file is undefined and the crawler MUST assume complete disallow" | Verbatim, in §2.3.1.4 "Unreachable" Status. |
| K-16 | :42 | RFC recheck from the header argv returned `1` occurrence | HOLD + FLAG | "in the top-level path of the service" | Retained-text count today: 1. Flag: the observation is dated 2026-10-19 and the count is unchanged. |
| K-17 | :44-46 | named debt: status of `veigapunk.github.io/robots.txt` and whether it lists sitemaps is unknown | HOLD | "The rules MUST be accessible in a file named "/robots.txt" (all lowercase) in the top-level path of the service." | Debt stays open. The retained bytes do not cover that host, and no property probe is permitted this round. |
| K-18 | :49 | replayable claim: states the RFC sections, exact command, and lane population | HOLD | "2.3.1.4. "Unreachable" Status If the robots.txt file is unreachable due to server or network errors" | The cited sections exist. The exact command is K-03. The lane population is not S011. |
| K-19 | :50 | missing substrate stays visible: current host-root robots and sitemap contents remain named debt | HOLD | "The rules MUST be accessible in a file named "/robots.txt" (all lowercase) in the top-level path of the service." | Host-root file still unfetched, so debt stays visible (see K-17). |
| K-20 | :51 | admission authority: cites RFC 9309 | HOLD | "Category: Standards Track Published: September 2022 ISSN: 2070-1721" | Standards Track. The retained page carries no "Obsoleted", "Updated by" or "Errata" text (census 0 each). |

## Correction (append-only; STALE only)

**C-1** for K-11. Target `corpus/knowledge/crawl-scope-per-host.md`, appended at EOF after line 53, starting with a newline (the file has no trailing newline). Original lines are not rewritten.

```
[r26-recheck S011 STALE] Line 22 cites corpus/knowledge/freshness-sweep.md:58 for host/path scope. That line is now the H4 history row (scripts/probe-delta.mjs). The host-scoped robots/sitemap row is corpus/knowledge/freshness-sweep.md:62 (A4, "ds4cc sitemap/robots pre-push state"). The S011 host-root rule this refinement builds on still holds: RFC 9309 §2.3 states "in the top-level path of the service".
```

## Checks run

1. Manifest and population: S011 is index 1 in `fetched/manifest.json` and `population.json` `rows[10]` (0-based). The retained raw gzip decompresses to the manifest size and sha256.
2. Quote census on the text view: 18 candidate quotes, each present exactly once, all 6-25 words, none containing the paragraph marker.
3. Phrase census on the text view: "top-level path of the service" 1; "MAY access any resources on the server" 1; "MUST assume complete disallow" 1; "30 days" 1 (in §2.3.1.4); "Obsoleted", "Updated by", "Errata", "Erratum" 0 each; "2.3.1.3" and "2.3.1.4" headings present.
4. Anchors read at current line numbers: `sitemap-orphan-audit.md:36-50` (total 146 lines), `freshness-sweep.md:50-62` (total 202 lines), `publish-queue.md:85-95` (total 294 lines). `corpus/QUALITY.md` exists and contains the five labels the entry cites.
5. Entry scan: 53 lines; no `r20` or correction marker; S011 named at lines 1 and 27 and implicitly at 2-3, 7-12, 20-24, 42, 44-51.

## Verification gaps

- The recheck command in line 3 targets `rfc9309.txt`, which is not in the retained set. Re-running it is outside this lane's one-GET-per-recorded-URL fetch contract. The retained `.html` text carries the phrase exactly once, and the recorded 2026-10-19 run returned 1.
- Errata and obsolescence were checked only against the retained page. The RFC Editor errata list was not retained.
- Anchors for K-10 and K-11 were judged by subject on the current files. Base content at `cb807bc` was not compared, since no git history was read.
- `veigapunk.github.io/robots.txt` was not probed (no property probing this round). The named debt stays open.
- Not judged (other pairs): S012/S013 statements, the lane count "three", and the Google docs date.

## Tools

None installed or upgraded. Checks used the read tool and Python 3 standard library in eval (file reads, sha256, substring counts). No network access and no property probing.

```json
{"pair":"S011xcrawl-scope-per-host","statements":20,"hold":19,"stale":1,"corrections":[{"id":"C-1","statement":"K-11","file":"corpus/knowledge/crawl-scope-per-host.md","placement":"EOF after line 53; prepend a newline (file has no trailing newline)","text":"[r26-recheck S011 STALE] Line 22 cites corpus/knowledge/freshness-sweep.md:58 for host/path scope. That line is now the H4 history row (scripts/probe-delta.mjs). The host-scoped robots/sitemap row is corpus/knowledge/freshness-sweep.md:62 (A4, \"ds4cc sitemap/robots pre-push state\"). The S011 host-root rule this refinement builds on still holds: RFC 9309 §2.3 states \"in the top-level path of the service\"."}]}
```
