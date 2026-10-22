# ConnectCorpusLinks — C2 placement (round 28, attempt 3, wave 1)

Seat: KakeR28a3.ConnectCorpusLinks (connector, leaf). Axis judged: freshness. Read-only; the only file written is this report.
Lane HEAD b5d423fc02057f67a6f3a255808313ce40d29069. The working tree already holds the L1 draft: `corpus/knowledge/field-performance-cwv.md` (untracked, sha256 a52b8a66…c887c) and `corpus/SOURCES.md` (+7 lines, sha256 7d979a82…87dd). The SOURCES line numbers below are working-tree numbers (the S036–S039 rows add 4 lines before the Paths section). No installs. No network.

## Commands (all run from the lane root unless noted)
- `rg -n -i 'core web vitals|\bINP\b|\bLCP\b|\bCLS\b|crux|pagespeed|field[- ]performance|field data|web vitals|debugbear|lighthouse|\bTTFB\b|\bFCP\b' --glob '!.ufo/**' .` exit 0 (first run before the draft appeared)
- `rg` over S036–S039 visible text in `.ufo/waves/round-28/sources/` (Firefox, Safari, interactionId, robots.txt: zero hits; eligibility, status, rate-limit and 04:00 passages: hits), exit 0
- `git diff corpus/SOURCES.md`; `git status --short`; `python3 -c` read of `.ufo/waves/round-23/live-summary.json` and `.ufo/waves/round-28/sources/receipts.json`, all exit 0
- `grep -c 'INP : Stable' /fast/scratch/hyaku/kake-r28/sources/S036.html` gave `0`, exit 1. `grep -c 'INP</a>: Stable'` on the same file gave `1`, exit 0. The file's sha256 cbbfb174…b838 matches the S036 receipt.

## Existing mentions (path:line; there are none in SKILL.md and none in tracked corpus/knowledge/*.md)
- PROVINCE.md:24-26 lists field performance (Core Web Vitals, CrUX eligibility) as Frontier: "Ground moves to Core only with source-backed entries and a gate."
- PROVINCE.md:77 (round 25): "The remaining field-performance, Jekyll and Render frontier is unchanged."
- corpus/README.md:102-104 lists "field performance (CWV/CrUX)" as open ground and points to `../PROVINCE.md` §Frontier.
- corpus/SOURCES.md:26 holds the S018 DebugBear row (rejected). :70 is the round-20 search log saying S018 is retained as rejected. :112 says "No source ids are void: all S001-S018 were opened."
- corpus/SOURCES.md:99 (W3C Event Timing), :100 (web.dev Optimize INP) and :101 (Chromium speed metrics changelog) are related leads that remain unopened.
- corpus/lessons/round-20.md:186-189 is the gate rejection of S018. :220 is S018's quote row. :263 is adjudication A4: "S018 rejection retained; no lane claim depends on the number."
- corpus/lessons/round-20-verifier-spotcheck.md:13 records non-author agreement with the S017/S018 rejections.
- SCORECARD.md:586 is the C2 claim row.
- Draft additions: SOURCES.md:44-47 (rows), :60 (Paths), :90 (search log), and field-performance-cwv.md:1-123.

## S018: what it is and why it was rejected
DebugBear's "Firefox And Safari Now Support Two Core Web Vitals Metrics" is a community source, tier C. Its scope is the Firefox version and date for interactionId and INP support. It says "Mozilla released version 114 of Firefox on the 14th of October 2025", but Firefox's 144.0 release notes (released 2025-10-14) are the ones that carry `PerformanceEventTiming.interactionId` (round-20.md:220). The row flips only if a tier-A source confirms DebugBear's number. Recheck cadence is 180d from 2026-10-19.

None of S036–S039 mention Firefox, Safari or interactionId (zero rg hits), so C2 cannot flip S018. The draft handles this correctly at field-performance-cwv.md:121-123 and SOURCES.md:90: no browser-support claim.

## Contradiction risks and how the draft stands
1. **Core admission (PROVINCE.md:26).** C2's counter is a wave counter, not a lane gate. Neither the entry nor the frontier lines may say field performance moved to Core. The draft is clean on this.
2. **Adjacent ownership (PROVINCE.md:30-35).** S038 recommends Lighthouse audits, which are browser execution and belong to tabi. S039 requires a Google Cloud API key; kagi holds credential custody and kake records no secrets. Draft lines 113-114 and 122-123 are consistent.
3. **robots.txt versus discoverability (crawl-scope-per-host.md:7-12, :44).** S038's three disqualifying conditions are a non-200 final status, `X-Robots-Tag: noindex`, and meta robots noindex. robots.txt is not among them (zero hits). The entry must not tie robots.txt status to CrUX inclusion, or claim that the named robots.txt debt at :44 is settled. The draft is silent on this, which is correct.
4. **Soft 404 at status 200 (SKILL.md:64-66).** That passage says "Raw `200` is not proof: kimi-pro serves `200 + 5995B preview-404 body`." S038 says pages fail discoverability "if any of the following conditions are met" and judges discoverability by "the same indexability criteria as search engines." The three conditions are sufficient for exclusion, not a complete list.
   - **Risk at draft line 105-107.** "If those hold, the likely cause is traffic below the undisclosed popularity minimum" over-reads S038 on a soft-404 surface.
   - **Proposed fix:** "If those hold, low traffic is the likely but unconfirmed cause; a 200 soft-404 (SKILL.md:66) can still be non-indexable under search-engine criteria."
5. **Not-served is coverage, not a verdict (lessons/round-23.md:44-45).** "No field data" is the CrUX analogue of not-served: report it apart from pass or fail. The draft's lines 13-14 and 107-108 follow this.
   - The connection is non-obvious. Four surfaces in `.ufo/waves/round-23/live-summary.json` returned 404 on 2026-10-21: plazir27-kimi, lucario-kimi, plazir15-kimi and charter-kimi. Under S038 they would fail page-level discoverability. [INFERENCE] This is dated and not a current observation.
6. **Signal versus verdict (SKILL.md:399).** The canonical entry reads "signals, not guarantees". Similarly, none of S036–S039 support a search-ranking effect of Core Web Vitals. The draft makes no ranking claim; keep it that way.
7. **No measurement (pattern of PROVINCE.md:75).** "No actual website accessibility is evaluated" has a parallel at draft lines 118-120 (no property measured). Frontier lines must say the same.
8. **Unopened leads (SOURCES.md:99-101).** These must not be cited in the entry. The draft cites none of them.
9. **Recheck command (draft line 3) is false-stale. This is a defect.**
   - Raw HTML carries `<a href="/articles/inp">INP</a>: Stable`, so `grep -c 'INP : Stable'` prints 0 and exits 1 against the very bytes that were opened (receipt sha256 cbbfb174…).
   - **Fix:** `curl -fsSL https://web.dev/articles/vitals | grep -c 'INP</a>: Stable'`, which prints 1 on the retained bytes.
   - This affects freshness replay, not the C2 counter, which only checks that the line starts with `recheck:`.
10. **Access-time mismatch.**
    - Draft verified-at (line 2) and SOURCES.md:90 say "2026-10-22T09:29Z", and :90 cites `.ufo/waves/round-28/sources/` as its receipts.
    - receipts.json in that directory records S036–S039 at 08:30:34Z through 08:30:36Z.
    - The 09:29Z times come from the attempt-3 seat reports (`w1a3/Src*.md`; for example SrcS036Lifecycle.md:7 gives 09:29:06Z, with the same byte count as the receipt).
    - **Fix:** cite both times, or point the 09:29Z time to `w1a3/Src*.md`.

## Proposed one-line updates (text only, append-only like the round-22 and round-25 sections; PROVINCE.md:24 and README.md:102-104 stay as they are)
- **PROVINCE.md**, new section `## Round-28 field-performance knowledge`:
  `` `corpus/knowledge/field-performance-cwv.md` (S036–S039) moves Core Web Vitals thresholds and CrUX eligibility into held knowledge only — no lane property was measured, no CrUX or PageSpeed API was called, Core still needs a gate, and the Jekyll and Render frontier is unchanged. ``
- **corpus/README.md**, new section `## Round-28 field-performance frontier step`, coverage row:
  `` | Field performance (r28) | `knowledge/field-performance-cwv.md` (S036–S039) | LCP/INP/CLS good and poor bounds at the 75th percentile, CrUX discoverability and popularity eligibility, 28-day API window; no property measured | ``
- **corpus/README.md**, frontier line:
  `` Field performance (CWV/CrUX) from the round-20 open-ground list now has sourced held knowledge; field measurement of owned properties, key-holding CrUX API access (operator/kagi) and Lighthouse runs (tabi) remain open. ``

## Axes
- Freshness improves: the entry is connected to crawl scope, the soft-404 rule and round-23 not-served coverage, and its recheck becomes replayable.
- Operability is unchanged: no script, gate or counter changes.
- Risks from the fixes: none to the C2 counter, since its header check only matches line prefixes. The edits are the L1's to apply.

## Not verified
- I ran no c2_source_count.py run on any revision.
- I did not fetch anything from the network; the corrected recheck was tested only on retained bytes.
- I did not read corpus/lessons/round-28.md; it does not exist yet.
- I did not check the draft's S038 "20% ineligible traffic" or "lowercase origins" statements. The S037 10–30% target, the S039 150 queries per minute, the S039 04:00 UTC update time and the S036 "INP : Stable" lifecycle text were confirmed in the visible text.
