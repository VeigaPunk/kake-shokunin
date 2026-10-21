# Rejection07 × S013 — attack on the L1 rejection of the seat's anchor-drift finding

- Target: `.ufo/waves/round-26/statements.json:128-136` (row S013, `crawl-scope-per-host.md`): `"seatStale": 1, "stale": 0`, `"l1Disposition": "same base-scoped pointers (+4 four-line provenance prefix, QUALITY round-21)."`
- Seat finding rejected: `w1/PairS013CrawlScopePerHost.md` row 8 / C1. It says the cited anchors `sitemap-orphan-audit.md:40-47`, `freshness-sweep.md:58` and `publish-queue.md:88-93` are STALE because they now resolve 4 lines lower.
- Candidate `e28312b14b076584fedd696fae2a684e460bd11e`, base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`.
- Axis judged: freshness.

## Verdict: AGREE (the rejection is correct and hides no staleness)

I tried three counterexamples. None holds.

### Counterexample 1: the pointers are wrong at their own stated scope

The statement scopes itself explicitly. At base, `git show 97404de:corpus/knowledge/crawl-scope-per-host.md`, lines 20-24 read:

> `**Refines at base `cb807bc`.** Makes host/path scope explicit for`
> `corpus/knowledge/sitemap-orphan-audit.md:40-47` and
> `corpus/knowledge/freshness-sweep.md:58`; the historical ds4cc.com 404 at
> `corpus/knowledge/publish-queue.md:88-93` is a different host …

`cb807bc` is a commit (2026-10-17, "kake: ignore interactive session logs") and an ancestor of base (`git merge-base --is-ancestor` succeeds). At `cb807bc`, each window contains exactly the content the sentence describes:

- `sitemap-orphan-audit.md:40` = `## Procedure (the wedge: a URL list independent of the source tree)`, through `:47` = `inside base path) or use `docs/FLEET-MAP.md` path tables.` This is the sitemap-sourcing procedure that the entry refines.
- `freshness-sweep.md:58` = `| A4 | armed | ds4cc sitemap/robots pre-push state | `sitemapStatus` 404 | `200` → `LISTED-LIVE` |`
- `publish-queue.md:88` = `- **Canonical side (r14 scout, new):** `ds4cc.com/sitemap.xml` and`, through `:93` = `PQ-2's canonical reference set is local-only by construction.` This is the historical ds4cc.com 404.

Result: correct at the stated scope. There is no false attribution at base revision, so the QUALITY round-26 exception ("A statement whose attribution was false even at its base revision is STALE", `corpus/QUALITY.md:220-221`) does not apply.

### Counterexample 2: the +4 rule maps from a different baseline

This was the strongest lead. `corpus/lessons/round-21.md:116-117` defines the register as "old line N at baseline `5009ecaa` is current line N+4". That baseline is not `cb807bc`. If any of the three files had shifted above the cited window between `cb807bc` and `5009ecaa`, the L1 disposition's "+4" would point at the wrong bytes.

`git diff -U0 cb807bc 5009ecaa` hunk headers:

- sitemap-orphan-audit: `@@ -112,0 +113,11 @@` (EOF append only)
- freshness-sweep: `@@ -93,0 +94 @@` and `@@ -174 +175,10 @@` (both below line 58)
- publish-queue: `@@ -262,0 +263 @@` (below line 93)

`git diff -U0 5009ecaa 97404de` shows `@@ -0,0 +1,4 @@` (the round-21 prefix) plus tail-only hunks for all three files. All three files are in the register (`round-21.md:127`, `:136`, `:137` → `N → N+4`). The rule covers the entry: it was authored in round 20 (`02b6dd0`), so its pointers are pre-round-21 (`QUALITY.md:69-71`).

I checked byte identity with `sed -n` windows piped through `sha256sum` (first 16 hex digits):

| window | cb807bc | base +4 | candidate +4 |
|---|---|---|---|
| sitemap-orphan-audit 40-47 → 44-51 | 2e99136e79baae18 | 2e99136e79baae18 | 2e99136e79baae18 |
| freshness-sweep 58 → 62 | 9207a3727db72e25 | 9207a3727db72e25 | 9207a3727db72e25 |
| publish-queue 88-93 → 92-97 | dc6105acfa2a4b1b | dc6105acfa2a4b1b | dc6105acfa2a4b1b |

Result: `cb807bc` and `5009ecaa` give the same coordinates for these windows. The register recovers the exact bytes in both the base tree and the candidate tree, so a reader is never sent to the wrong content.

### Counterexample 3: the S013 premise behind the pointer paragraph has gone stale

- Retained bytes: `gzip -dc fetched/S013-1.raw.gz | sha256sum` → `492e22cf133333d6202bbfd6c47370eac981612d7952b1e851d31e06dd78920b`; `wc -c` → `191341`. `manifest-retry.json` has no S013 record (its only row is S008).
- Literal counts in `fetched/text/S013-1.txt`:
  - "unless you submit your sitemap through Search Console, a sitemap affects only descendants of the parent directory": 1
  - "can affect all files on the site": 1
  - "Last updated 2026-07-08 UTC": 1
  - "Sitemap: https://example.com/my_sitemap.xml": 1
- Offsets: "Sitemap best practices" @8213 < "Sitemap file encoding and location" @8886 < quote @9094. The entry's anchor "Sitemap best practices" (L33) contains the quote.

Result: the host/path-scope claim that the pointer paragraph rests on (L15-18) holds. The "historical … not a current observation" wording is self-labelled history, not a live claim.

## Impacted axes

- freshness: none. The rejection is correct; the seat's C1 is a coordinate convenience the register already provides, not a correction of a wrong statement.

## Low-severity adjacent observations (not the target; no correction required for this verdict)

1. **Two different baselines, not stated together.** The candidate append (`e28312b:corpus/knowledge/crawl-scope-per-host.md`, "Round-26 source recheck" bullet) says "Pointers labelled `at base cb807bc` stay base-scoped (QUALITY.md round-21 coordinate rule)". The register it relies on is defined from `5009ecaa`. The two coincide here only because the `cb807bc..5009ecaa` changes fall below every cited window, and nothing records that. Smallest optional fix: a ledger or lesson note that says "cb807bc ≡ 5009ecaa for these windows (all intervening hunks below the cited lines)".
2. **Copied boilerplate provenance.** That same appended bullet includes "(S008 via `manifest-retry.json`)", but this entry cites only S011, S012 and S013. The same wording appears in 5 knowledge files (`git grep -c` at e28312b: crawl-scope-per-host, ghp-custom-domain, ghp-etag-anatomy, ghp-served-set, static-canonical-preflight). It is true of the round but irrelevant to this entry. This is a provenance-precision nit, not staleness.

## Commands run

Read-only only: `git show`, `git log`, `git diff -U0`, `git merge-base --is-ancestor`, `git grep -c`, `gzip -dc | sha256sum | wc -c`, `grep -oF | wc -l`, and an inline python offset search over `fetched/text/S013-1.txt`. No network GET. Nothing written except this report.

## Tooling

I read `/home/vgpnk/.omp/agent/RULES.md`. No tools were installed or upgraded.

```json
{"target":"statements.json S013 l1Disposition (rejection of PairS013 C1 anchor drift)","verdict":"AGREE","severity":"none"}
```
