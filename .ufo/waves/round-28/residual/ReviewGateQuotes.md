# ReviewGateQuotes — Gate quote re-opening check (Kake r28 attempt 3, residual)

Axes: evidence exactness (quote/section/digest fidelity), coverage (all 15 Gate quotes checked, none skipped).

## Target
`## Gate` of `corpus/lessons/round-28.md` at e57f601: 4 S036–S039 opening lines + 11-row
further-support table = 15 quotes. Working tree verified identical to e57f601 (`diff -q`
clean; clone HEAD `5a83d13b28024cef461c0ef497e28681684555ac`, `cat-file -t e57f601…` = commit).

## Method (per receipts-a3.json "method")
"curl -sL GET; visible text = HTML minus script/style and tags, entities unescaped,
whitespace collapsed; quotes checked as exact substrings of that text."
Recipe validation: my reimplementation applied to the L1's retained raw HTML
(`/fast/scratch/hyaku/kake-r28a3/sources/S036–S039.html`, whose sha256 equal receipts
`sha256` 4/4) reproduces the retained `S036–S039.txt` byte-for-byte (4/4), and those .txt
digests equal receipts `visibleSha256` 4/4. So my derivation is the receipts' derivation.

## Re-opening — one GET per URL (GET only; no API, no keys; TMPDIR in scratch)
`curl -sS -L --max-time 90 -D $TMPDIR/S0xx.hdr -o $TMPDIR/S0xx.html -w ... <url>` exit=0 ×4.
- S036 https://web.dev/articles/vitals — 200, redirects=0, 143742 B, sha256 `ca8c9b821fff…a98a52`
- S037 https://web.dev/articles/defining-core-web-vitals-thresholds — 200, redirects=0, 149326 B, sha256 `d7069a128052…f48f648`
- S038 https://developer.chrome.com/docs/crux/methodology — 200, redirects=0, 109250 B, sha256 `96c5f02dd25e…0a2d3`
- S039 https://developer.chrome.com/docs/crux/api — 200, redirects=0, 167991 B, sha256 `dedc50be3fe6…5128 8c` (exact: `dedc50be3fe6375ed3f518d3dba55db32797b17ae0025f13c09dc9e4c351288c`)

## Digest comparison vs receipts-a3.json
All four received-body sha256 differ from receipts (44aee957…, f6608980…, 2b896aa2…,
6ebcdcf7…). Cause: request-scoped tokens — first divergent byte on every page is a
`<script nonce="…">` CSP nonce; S036/S039 byte-equal length, S037/S038 +4 B elsewhere.
Consequence: derived visible text is byte-identical to receipts for all four
(my visibleSha256 == receipts visibleSha256 4/4; word-level diff 0 opcodes).
**The digest difference changes no quote.**

## Per-quote results (all 15: found, words, section)
Section check = quote occurs under the named heading in my derived text (offsets in
collapsed text; identical to receipts' text). "PASS" = exact heading match; quote inside.
| # | Src | Gate section label | Found | Words (≤25) | Section |
|---|-----|--------------------|-------|-------------|---------|
| 1 | S036 open | Core Web Vitals | 1x | 18 | PASS (h2 @3924, quote @5082) |
| 2 | S036 tbl | Core Web Vitals lifecycle | 1x | 9 | PASS* composite: h3 "Lifecycle" @5514 under h2 "Core Web Vitals"; quote @6246 |
| 3 | S036 tbl | Lab tools to measure Core Web Vitals | 1x | 19 | PASS (@11738; quote @12620) |
| 4 | S036 tbl | Stable | 1x | 12 | PASS (@7543; quote @7782) |
| 5 | S037 open | opening section | 1x | 23 | MISMATCH — see F1 (quote @4741 under h2 "Refresher:…" @3673; lead @2981–3673 lacks it) |
| 6 | S037 tbl | Core Web Vitals thresholds table | 1x | 23 | MISMATCH — see F1 (flattened table @4427 under "Refresher:…"; no such heading) |
| 7 | S037 tbl | Core Web Vitals thresholds | 1x | 19 | MISMATCH — see F1 (quote @9048 under h2 "Whether to have the same or different criteria per device" @8610) |
| 8 | S038 open | Publicly discoverable | 1x | 15 | PASS |
| 9 | S038 tbl | Publicly discoverable | 1x | 14 | PASS |
| 10 | S038 tbl | Sufficiently popular | 1x | 6 | PASS |
| 11 | S038 tbl | Origin | 1x | 19 | PASS (literal h-section "Origin" exists) |
| 12 | S039 open | The rolling average | 1x | 15 | PASS |
| 13 | S039 tbl | CrUX API Key | 1x | 17 | PASS |
| 14 | S039 tbl | Rate limits | 1x | 19 | PASS |
| 15 | S039 tbl | UrlNormalization | 1x | 8 | PASS |

- All 15 quotes are exact substrings of the derived visible text (1 occurrence each).
- All word counts ≤25 and equal receipts `words` field per quote.
- Gate quote texts == receipts `lessonQuotes` texts, per source (sorted-set equal, 4/4).

## Findings
- F1 (Low, advisory): three S037 locator labels do not resolve to page headings.
  The quotes are genuine, but "opening section" / "Core Web Vitals thresholds table" /
  "Core Web Vitals thresholds" are not headings on the page; the text lives under
  "Refresher: Core Web Vitals metrics and thresholds" (rows 5,6) and "Whether to have the
  same or different criteria per device" (row 7). Suggest precise labels in a follow-up.
- F2 (Info): S036 row "Core Web Vitals lifecycle" is a composite (h2→h3 path) that
  resolves uniquely; optionally rename to "Lifecycle".
- No fabrication, digest, word-count, or substring defect found.

## Gate narrative cross-checks
- "HTTP 200, 09:29:23Z to 09:29:26Z": receipts accessedUtc = 09:29:23/24/25/26 ✓.
- "Received-body digests are in receipts-a3.json" ✓ (and L1 scratch copies match them 4/4).
- "all 16 of its quotes were found again": receipts inheritedQuotesFound 4+3+5+4 = 16 ✓.

## Not verified / residual risk
- The L1's "one public GET" per source is not provable from here (no fetch logs); I confirm only my own one-GET re-opening.
- Wave-1 seats' re-opening (`w1a3/Src*.md`) and attempt-2 receipts not re-verified (out of target);
  S037/S038 +4-byte body delta not pinpointed beyond "not in visible text" (irrelevant to quotes).
- Checks are against server-rendered HTML as fetched; no JS-rendered variant probed.
- Tooling: no installs (pacman untouched); curl 8.23.0 and Python 3.14.8 preinstalled.
- Sandbox: clone + fetches under /fast/scratch/hyaku/kake-r28a3/res/ReviewGateQuotes/; lane untouched except this report.
