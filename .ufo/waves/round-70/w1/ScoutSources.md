# ScoutSources — round 70, W1 (kake lane)

Seat duty: re-open one external source (the document staged row S352 rides on) with ONE GET,
retain it, receipt it, and locate three passages with an explicit class method and ≤25-word quotes.

## Source — one GET, retained

- URL `https://developer.chrome.com/docs/crux/bigquery`; final URL identical (no off-document redirect).
- status **200**, bytes **110697**, sha256 **dd17ea8cb30ec89af9eb6cbb16fcb0de3d04eb33143a3aa8ac19c9da6d5db420**,
  access date **2026-11-03** (2026-11-03T19:34:48Z UTC).
- command (one invocation, curl exit 0, stderr empty):
  `curl -sS -L --max-time 60 -o /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-70/w1/ScoutSources/sources/S438-crux-bigquery.html -w '%{http_code} %{size_download} %{url_effective}\n' https://developer.chrome.com/docs/crux/bigquery`
  → write-out `200 110697 https://developer.chrome.com/docs/crux/bigquery`
- retained body: `.ufo/waves/round-70/w1/ScoutSources/sources/S438-crux-bigquery.html`
- receipt: `.ufo/waves/round-70/w1/ScoutSources/sources/receipt.json` and an identical copy at
  `.ufo/waves/round-70/w1/ScoutSources/receipt.json` (both sha256
  `5572463d2ea68c2030dc41bb97837ff05bd2baf211bdfcf030245f9054f75fe1`), fields
  `url, final_url, status, bytes, sha256, access_date_utc, command`.

## Method (both classes exercised for every passage)

- raw class: `grep -cF '<quote>' <retained body>` → hit = `raw-substring`.
- collapsed class: retained `strip.py` (drop `<script>`/`<style>`/comments, drop tags,
  `html.unescape`, collapse whitespace) → `collapsed.txt` (10150 B, sha256
  `fc1d02f2015200b300e033a842039457b10b268bfbcfa8b41c2ab243cfd4c9a0`), then `grep -cF`.
- word count: `wc -w` on the quote text alone (printf to a file, no surrounding words).
- Every located passage was checked both ways; classes below are the observed outcomes.

## Q1 — the adoption quote (contract C2(c))

> The origin_summary table contains a list of all origins in the CrUX dataset

- class **collapsed-only** (raw `grep -cF` = 0, collapsed `grep -cF` = 1). Raw fails because the
  table name is marked up: `<code translate="no" dir="ltr">origin_summary</code> table`.
- **13 words** (≤25). Position: line 3146, byte offset 89743 of the retained body.
- Verdict: admissible under C2(c) (`raw-substring` or `collapsed-only`); not `absent`.

## Q2 — monthly refresh cadence of origin_summary

> it is updated monthly with the latest list of origins in the dataset

- class **raw-substring** (raw = 1, collapsed = 1). **13 words** (≤25).
- Position: line 3146, byte offset 89861 — the second clause (after the semicolon) of the same
  sentence as Q1; the whole sentence runs 32 words, so the clause is the ≤25-word record.

## Q3 — free-to-explore within the BigQuery free tier

> The CrUX dataset on BigQuery is free to access and explore up to the limits of the free tier

- class **collapsed-only** (raw = 0, collapsed = 1). Raw fails on two anchors:
  `<a …>CrUX dataset on BigQuery</a>` and `<a …>free tier</a>`.
- **19 words** (≤25). Position: line 2930, byte offset 78723.
- Truncation is explicit: the full sentence is 27 words (`…, which is renewed monthly and provided
  by BigQuery.`), over the cap; the recorded quote stops at the comma, nothing paraphrased or added.
- Collapsed-text artifact to be aware of: it reads `free tier ,` (space before the comma) because
  the closing tag became whitespace; the quote itself ends before the comma.

## Attacks and verdicts

| # | attack | verdict |
|---|---|---|
| A1 | claim Q1 as `raw-substring` | **FAIL** as raw (code element splits it) → recorded `collapsed-only` |
| A2 | word cap on every quote | Q1 13, Q2 13, Q3 19 pass; Q3 full sentence 27 would FAIL → truncated and marked |
| A3 | receipt ↔ body integrity | **PASS**: sha256 recomputed from retained bytes equals receipt; `bytes` = `stat -c%s` = 110697 |
| A4 | lane discipline | **PASS**: `git status --porcelain` shows only untracked `.ufo/waves/round-70/` paths; no commit/push/mutation |
| A5 | fetch honesty | **PASS**: one curl call, exit 0, empty stderr, `url_effective` = requested URL |

`absent` class was not needed: all three passages were located.

## Residual unknowns

- The retained page is Devsite HTML with client-side chrome; only the static `<article>` bytes were
  used. No second fetch was made, so the retained sha256 is the only evidence of the 2026-11-03 state.

## Tooling

- None installed or upgraded; pacman not invoked (host pause respected).

Scratch `/fast/scratch/hyaku/kake-r70/ScoutSources` removed on exit (stripper and collapsed text
retained under this seat directory).
