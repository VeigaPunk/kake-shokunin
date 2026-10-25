# ExecRecheckInventory

Mechanical inventory of `corpus/knowledge/*.md`. No judgement, no edits outside this report.
Working tree HEAD at read time: `6b3df99d694f59d44504604da1a55a9fe1e9be75`;
`git status --porcelain corpus/knowledge` returned 0 lines, so the inventory describes the
unmodified working tree. All commands were run from
`/home/vgpnk/Projects/shokunin/kake-shokunin`.

COMMANDS:

1. File count — `ls corpus/knowledge/*.md | wc -l` → `46`
2. Files whose first 8 lines carry `source:`, `verified-at:` and `recheck:` (anchored at column 0) —
   ```
   for f in corpus/knowledge/*.md; do h=$(head -8 "$f"); if printf '%s\n' "$h" | grep -q '^source:' && printf '%s\n' "$h" | grep -q '^verified-at:' && printf '%s\n' "$h" | grep -q '^recheck:'; then echo "$f"; fi; done | wc -l
   ```
   → `46`
3. Files whose `recheck:` line holds a backticked command (rule: the recheck line contains at least
   one backtick-delimited span whose first character is `[A-Za-z0-9]` and which contains a space,
   i.e. a command plus at least one argument; a backticked bare token such as `` `CNAME` `` does not
   match) —
   ```
   for f in corpus/knowledge/*.md; do l=$(grep -m1 '^recheck:' "$f"); if printf '%s' "$l" | grep -oq '`[A-Za-z0-9][^`]* '; then echo "$f"; fi; done | wc -l
   ```
   → `20`
4. `verified-at:` dates and earliest/latest (rule: first `YYYY-MM-DD` match inside the value; the
   value's leading date) —
   ```
   for f in corpus/knowledge/*.md; do grep -m1 '^verified-at:' "$f" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -1; done | sort | uniq -c
   ```
   → earliest `2026-09-21` (1 file), latest `2026-10-25` (6 files); full distribution:
   `2026-09-21:1, 2026-09-26:1, 2026-09-28:11, 2026-09-29:3, 2026-10-19:5, 2026-10-20:1,`
   `2026-10-21:1, 2026-10-22:6, 2026-10-23:2, 2026-10-24:9, 2026-10-25:6`
5. Files with `verified-at` older than 2026-10-20 (strict `\<` on the leading date) —
   ```
   for f in corpus/knowledge/*.md; do d=$(grep -m1 '^verified-at:' "$f" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -1); if [ "$d" \< "2026-10-20" ]; then echo "$(basename "$f") $d"; fi; done | wc -l
   ```
   → `21` (listed in TOTALS)
6. Table source command —
   ```
   for f in corpus/knowledge/*.md; do h=$(head -8 "$f"); s=Y; v=Y; r=Y; printf '%s\n' "$h" | grep -q '^source:' || s=N; printf '%s\n' "$h" | grep -q '^verified-at:' || v=N; printf '%s\n' "$h" | grep -q '^recheck:' || r=N; va=$(printf '%s\n' "$h" | grep -m1 '^verified-at:' | sed 's/^verified-at:[[:space:]]*//'); d=$(printf '%s' "$va" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -1); t=$(printf '%s' "$va" | cut -c1-70); [ ${#va} -gt 70 ] && t="$t…"; printf '| %s | %s | %s | %s | %s | %s |\n' "$(basename "$f")" "$s" "$v" "$r" "$d" "$t"; done
   ```
   The last column is the `verified-at:` value truncated at 70 characters (`…` = truncated); the
   untruncated values remain in the files. The date column is the leading-date extraction of step 4.

TABLE:

Columns: file | source | verified-at | recheck | leading date | verified-at value (truncated 70)

| file | source | verified-at | recheck | date | value |
|---|---|---|---|---|---|
| accessibility-review-packet.md | Y | Y | Y | 2026-10-21 | 2026-10-21 — pinned Recommendation source opened; documentation pack… |
| baidu-friendly-crawl-guidance.md | Y | Y | Y | 2026-10-25 | 2026-10-25 |
| baidu-mobile-matching-error-causes.md | Y | Y | Y | 2026-10-25 | 2026-10-25 |
| canonical-selection.md | Y | Y | Y | 2026-10-24 | 2026-10-24 |
| claim-count-derivation.md | Y | Y | Y | 2026-10-23 | 2026-10-23 (kake round 43) — the r42-stated counts failed re-derivat… |
| commit-citation-hygiene.md | Y | Y | Y | 2026-10-24 | 2026-10-24 |
| crawl-budget-consequences.md | Y | Y | Y | 2026-10-24 | 2026-10-24 |
| crawl-error-status-table.md | Y | Y | Y | 2026-10-24 | 2026-10-24 |
| crawl-scope-per-host.md | Y | Y | Y | 2026-10-19 | 2026-10-19 (RFC 9309 published September 2022; Google docs updated 202… |
| crawler-identity.md | Y | Y | Y | 2026-10-24 | 2026-10-24 |
| drift-detection.md | Y | Y | Y | 2026-09-29 | 2026-09-29 (latest original evidence: r16 read-only re-verification, 2… |
| dynamic-rendering-workaround-limits.md | Y | Y | Y | 2026-10-24 | 2026-10-24 |
| field-performance-cwv.md | Y | Y | Y | 2026-10-22 | 2026-10-22 (pages last updated: S036 2024-10-31, S037 2025-05-07, S038… |
| fire-journal-codes.md | Y | Y | Y | 2026-09-28 | 2026-09-28 (die/throw sites in kimi-surface.mjs; journals 2026-09-26/0… |
| fleet-registry.md | Y | Y | Y | 2026-09-28 | 2026-09-28 (`len(sites)` = 21 and live probe of 2026-09-28 — origina… |
| free-read-verbs.md | Y | Y | Y | 2026-09-28 | 2026-09-28 (original read of the webzites tree and live runs 2026-09-2… |
| freshness-sweep.md | Y | Y | Y | 2026-10-19 | 2026-10-19 (round-20 citation-local correction and S014 run; r16 run 2… |
| ghp-custom-domain.md | Y | Y | Y | 2026-10-19 | 2026-10-19 (GitHub Docs and REST API opened 2026-10-19) |
| ghp-etag-anatomy.md | Y | Y | Y | 2026-10-19 | 2026-10-19 (nginx release-1.28.0; RFC 9110 published June 2022) |
| ghp-served-set.md | Y | Y | Y | 2026-10-19 | 2026-10-19 (v4.0.0 commit 7b1f4a7; current action commit 5f327015) |
| ghp-subpath-spotcheck.md | Y | Y | Y | 2026-09-28 | 2026-09-28 baseline audit and GHP fetches; webzites revision not recor… |
| js-rendering-queue.md | Y | Y | Y | 2026-10-24 | 2026-10-24 |
| keeper-timer-inert.md | Y | Y | Y | 2026-09-28 | 2026-09-28T22:18Z original read-only capture (r13 re-read 2026-09-28T2… |
| kimi-subpath-audit.md | Y | Y | Y | 2026-09-28 | 2026-09-28 ~21:15Z baseline, sitemap source revision f3d2ecd — histo… |
| link-preview-metadata.md | Y | Y | Y | 2026-10-22 | 2026-10-22 (each of the four opened with one public GET at 2026-10-22T… |
| mirror-pitfalls.md | Y | Y | Y | 2026-09-28 | 2026-09-28 (LOG.md rounds 1–4; ufofsdbeta absence event 2026-09-28T2… |
| ops-automation.md | Y | Y | Y | 2026-09-29 | 2026-09-29 (original evidence: r13 re-verification 2026-09-28T22:4x–… |
| origin-repos.md | Y | Y | Y | 2026-09-21 | 2026-09-21 (wz-repos terminal round r8, run gqab44994c06d7e7a4; origin… |
| pages-base-path.md | Y | Y | Y | 2026-10-22 | 2026-10-22 (all four opened this round with one public GET each, HTTP … |
| probe-delta-alerting.md | Y | Y | Y | 2026-09-28 | original evidence 2026-09-28 (round-10 final run, 76 rows, 6 events / … |
| publish-channels.md | Y | Y | Y | 2026-09-26 | 2026-09-26 (kimi-webbridge "not supported on Linux" check) and 2026-09… |
| publish-queue.md | Y | Y | Y | 2026-09-29 | 2026-09-29 (r16 re-verification 02:1x–02:3xZ, latest in-entry live r… |
| receipt-integrity.md | Y | Y | Y | 2026-10-24 | 2026-10-24 (kake round 45) — the three v1 defect sites re-read at th… |
| redirect-rewrite-rules.md | Y | Y | Y | 2026-10-24 | 2026-10-24 (S135 fresh GET this round; S050 retained text re-read) |
| render-static-sites.md | Y | Y | Y | 2026-10-22 | 2026-10-22 (all four opened this round with one public GET each at 202… |
| render-web-services.md | Y | Y | Y | 2026-10-22 | 2026-10-22 (all four opened this round with one public GET each at 202… |
| robots-txt-rules.md | Y | Y | Y | 2026-10-23 | 2026-10-23 (S011, S095 and S096 retained round-37 retrievals; `.ufo/wa… |
| security-txt-publishing.md | Y | Y | Y | 2026-10-22 | 2026-10-22, eleven public GETs 22:00:48Z–22:27:55Z, all HTTP 200 exc… |
| sitemap-orphan-audit.md | Y | Y | Y | 2026-09-28 | 2026-09-28 (orphan-check baseline ~20:20Z; r16 re-read 2026-09-29T02:2… |
| speedrun-pipeline.md | Y | Y | Y | 2026-09-28 | 2026-09-28 round-5 original evidence (commit 18537e9; LOG round-5); r2… |
| static-canonical-preflight.md | Y | Y | Y | 2026-10-20 | 2026-10-20 (S020-S027) and 2026-10-21 (S028-S029), documentation opene… |
| vault-properties.md | Y | Y | Y | 2026-09-28 | 2026-09-28 original baseline GETs and +157B seed finding, introduced i… |
| yahoo-japan-rel-nofollow-semantics.md | Y | Y | Y | 2026-10-25 | 2026-10-25 |
| yahoo-japan-robots-pattern-syntax.md | Y | Y | Y | 2026-10-25 | 2026-10-25 |
| yahoo-japan-robots-txt-basics.md | Y | Y | Y | 2026-10-25 | 2026-10-25 |
| yahoo-japan-robots-txt-refusal-rules.md | Y | Y | Y | 2026-10-25 | 2026-10-25 |

TOTALS:

- files: **46** (command 1)
- files with all three of `source:`, `verified-at:`, `recheck:` in the first 8 lines: **46** (command 2)
- files whose `recheck:` holds a backticked command: **20** (command 3) —
  claim-count-derivation.md, commit-citation-hygiene.md, drift-detection.md,
  dynamic-rendering-workaround-limits.md, fleet-registry.md, free-read-verbs.md,
  freshness-sweep.md, js-rendering-queue.md, keeper-timer-inert.md, link-preview-metadata.md,
  mirror-pitfalls.md, ops-automation.md, probe-delta-alerting.md, publish-channels.md,
  receipt-integrity.md, redirect-rewrite-rules.md, render-static-sites.md, render-web-services.md,
  speedrun-pipeline.md, yahoo-japan-robots-txt-refusal-rules.md
  (the one file with backticks but no backticked command is ghp-custom-domain.md, whose only
  backticked span is the bare token `CNAME`)
- earliest `verified-at` date: **2026-09-21** — origin-repos.md (command 4)
- latest `verified-at` date: **2026-10-25** — baidu-friendly-crawl-guidance.md,
  baidu-mobile-matching-error-causes.md, yahoo-japan-rel-nofollow-semantics.md,
  yahoo-japan-robots-pattern-syntax.md, yahoo-japan-robots-txt-basics.md,
  yahoo-japan-robots-txt-refusal-rules.md (command 4)
- files with `verified-at` older than 2026-10-20: **21** (command 5) —
  crawl-scope-per-host.md 2026-10-19; drift-detection.md 2026-09-29; fire-journal-codes.md 2026-09-28;
  fleet-registry.md 2026-09-28; free-read-verbs.md 2026-09-28; freshness-sweep.md 2026-10-19;
  ghp-custom-domain.md 2026-10-19; ghp-etag-anatomy.md 2026-10-19; ghp-served-set.md 2026-10-19;
  ghp-subpath-spotcheck.md 2026-09-28; keeper-timer-inert.md 2026-09-28; kimi-subpath-audit.md 2026-09-28;
  mirror-pitfalls.md 2026-09-28; ops-automation.md 2026-09-29; origin-repos.md 2026-09-21;
  probe-delta-alerting.md 2026-09-28; publish-channels.md 2026-09-26; publish-queue.md 2026-09-29;
  sitemap-orphan-audit.md 2026-09-28; speedrun-pipeline.md 2026-09-28; vault-properties.md 2026-09-28

VERDICT: 46 knowledge files, all 46 carry source:/verified-at:/recheck: in their first 8 lines, 20 recheck values hold a backticked command, verified-at spans 2026-09-21…2026-10-25, and 21 files predate 2026-10-20.
