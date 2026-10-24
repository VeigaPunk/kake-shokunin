# ReopenFlagS065 — S065 re-opened by hand (real-input `quote_missing`)

**Verdict: real on the recorded (url, quote) pair, but both causes are record-level — an extraction
miss (the quote is a Markdown code span) plus a container-page URL. Not a tool miss, not page
drift, not a paraphrase.** The quote is verbatim in the commit's material and the retained copy.

## What I attacked
`.ufo/waves/round-36/realrun/input.json` S065: url `https://github.com/VeigaPunk/ds4cc-marketplace/
commit/7fc6aa2fc12451dd451fed5a9ee7125f3a90e884`, quote
`` `<link rel="canonical" href="https://ds4cc.com/magga/frostbite/">` `` (`from`: round-33.md),
recorded fetch `200`, `text/html; charset=utf-8`; `audit.json` finding `quote_missing`. Row
`corpus/SOURCES.md:73`: "read through a sandbox clone … retained byte-identical at
.ufo/waves/round-33/sources/ds4cc-7fc6aa2f/".

## Live fetch (ordinary GET, GET only, no challenge, no auth)
- `timeout 120 curl -sS -D live-noredirect.headers -o live-noredirect.html -w … <commit url>` — exit 0,
  `status=200 type=text/html; charset=utf-8 size=325106`; **no redirect** (`curl` without `-L`,
  `url_effective` = requested URL, one hop), so `moved` does not apply. Body sha256
  `398d8cb4f2549ddfd395a7a0fc087d83f17d93c6ee6d5c858795c349f568fea1`.
- Recorded snapshot `S065.body` (from `snap-bodies.tar.xz`) sha256
  `6f5982ca6b11de85251bbee649ecfcf11fb90df7ae608f8eeec996ffcd8130e9`, 325106 bytes; differs from live
  only in volatile bytes. **Both page texts contain zero `canonical`** — not page drift since 22:57Z.

## What the live page actually serves
Text of the live body through the tool's own extractor (`source_recheck.html_text`, bullet c): 6776
chars, `index.html` 5, `sitemap.xml` 1, `Frostbite` 3, **`canonical` 0**. Quoted page
text: `magga: Frostbite — Classic & Remastered at /magga/frostbite/ · VeigaPunk/ds4cc-marketplace@
7fc6aa2 · GitHub` … `12 files changed+3,734`. The commit route's own JSON
says `"moreDiffsToLoad":true,"asyncDiffLoadInfo":{"startIndex":1,"truncated":false,"byteCount":1350,
"lineShownCount":22}` — GitHub inlines **22 diff lines** (the `magga/README.md` hunk) and loads the
rest by JavaScript. File *names* appear (`magga/frostbite/index.html` among 12 paths); no content does.

## Where the quote really lives (same commit, github.com)
- `curl -o commit.diff <commit url>.diff` — exit 0, `status=200 type=text/plain; charset=utf-8
  size=171919`, sha256 `fd3c76a28d1ef12aaea10d744881877e0b386c0d5207b801255dcc8d8af689cf`.
  Line 1380: `+<link rel="canonical" href="https://ds4cc.com/magga/frostbite/">`. Hunk
  `@@ -0,0 +1,262 @@`, `new file mode`; the 262 added lines equal the lane's retained copy
  `.ufo/waves/round-33/sources/ds4cc-7fc6aa2f/magga/frostbite/index.html` line for line
  (sha256 `b7f5380afe0744849af76f8b82ef253d8ef80a696869be15d844268ca1c0d94f`; line 9 is the quote).
  The quoted text is verbatim at the cited commit — not a paraphrase, not stale.

## Four-way replay of the landed tool (build 4d5b3d55, unedited)
Body copied next to each manifest (relative `body` per bullet g); `hops:[{status:200}]`; exit below.

| manifest | url | quote | exit | verdict / finding |
|---|---|---|---|---|
| n1 | commit page | as recorded (with backticks) | 1 | `failed-policy`, `quote_missing` — reproduces the audit |
| n2 | commit page | backticks stripped | 1 | `failed-policy`, `quote_missing` — page alone is enough to fail |
| n3 | commit page `.diff` | backticks stripped | 0 | `clean` — the commit material does carry the quote |
| n4 | commit page `.diff` | as recorded | 1 | `failed-policy`, `quote_missing` — backticks alone break even correct material |

## Two independent causes, both record-level
1. **Extraction miss (input layer).** The recorded quote is the Markdown code span, backticks
   included (`repr` starts and ends with `` ` ``). A backtick is not `str.isspace()`, so contract (d)
   keeps it and no page text can contain it, even where the quote otherwise matches (n4). The
   wave-1 extractor documents this deliberately
   (`w1/ExecGateQuoteExtractor.md:59-61`: quote from "a `quote “…”` … or a non-command backtick
   span"), i.e. it strips the “ ” delimiters and keeps the inner backticks. Census of
   `input.json`: **7 of 90 quotes contain a backtick (S004, S005, S006, S007, S008, S017, S065) —
   exactly the 7 backtick-bearing ids among the 8 `quote_missing` findings** (S025 is the eighth,
   no backtick). The real-input run therefore measures input hygiene for those 7, not drift.
2. **Container-page URL.** The row cites a commit *page*; that route renders 22 diff lines inline and
   fetches the rest client-side (`moreDiffsToLoad`). Extracted page text has 0 `canonical` (n2, exit
   1), so no quote from a file body can ever hold against this URL.

## Actionable, for the L1 to decide (no lane change made here)
Re-anchor S065's re-checkable source to material that serves the text (`…/commit/<sha>.diff`,
`…/commit/<sha>.patch`, or `…/raw/<sha>/magga/frostbite/index.html`) and record the quote without
code-span delimiters; a re-check that must stay on the HTML page is unmeetable by construction.
The same fix removes 7 of the 14 real-input findings.

## Not verified / limits
- I did not open `raw.githubusercontent.com` (outside this seat's hosts) nor any operator host, and did
  not test the JS fragment endpoint; only the server-rendered page and the `.diff` endpoint were fetched.
- Row edits, `SOURCES.md`/lesson corrections and extractor changes are outside this seat; no lane file
  was written except this report. No tool installed or upgraded (none needed).

Evidence in `/fast/scratch/hyaku/kake-r36w2/ReopenFlagS065/`: `live-noredirect.html`, `live-noredirect.headers`,
`S065.body`, `commit.diff`, `live-page-text.txt`, `snapshot-page-text.txt`, `n1…n4/{manifest.json,body.bin}`.
