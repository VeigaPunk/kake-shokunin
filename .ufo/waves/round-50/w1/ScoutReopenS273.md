# ScoutReopenS273 — live re-open of the S273 source page

Round 50 wave 1 scout item. Re-opened the declared source URL once to
cross-check the frozen S273 quote against live bytes.

## Frozen quote (from `.ufo/waves/round-50/c50_quote_class.py`)

> Google won't shift this newly available crawl budget to other pages unless Google is already hitting your site's crawl capacity limit.

(20 whitespace tokens — inside the 6–25 bound.)

## Fetch

- URL: `https://developers.google.com/crawling/docs/crawl-budget`
- Command: `curl -sS -o /tmp/kake-r50-w1/s273.html -w '...' <url>` (single GET, `200`)
- HTTP status: **200**
- Fetched body size: **74,323 bytes**
- Body stored at `/tmp/kake-r50-w1/s273.html` — not in the lane.

## Substring checks

- Quote is a RAW substring of the fetched body: **false** (expected false)
- Quote is a substring of the whitespace-collapsed body
  (`' '.join(body.split())`): **true** (expected true)

The frozen quote is already whitespace-normalized (its own collapsed form
is identical), so no quote-side normalization affected the check.

## Derived class

Per the counter's `classify()` rule — `raw-substring` when the quote is a
substring of the raw blob, `collapsed-only` when it appears only after
whitespace collapse — the live page yields the same class as the committed
round-49 blob:

**S273 class: collapsed-only**

This matches the frozen ledger row and the derivation note in
`c50_quote_class.py` ("S273 is collapsed-only"). The label stays derived
from measured bytes, not assumed: a live page where the quote had become a
raw substring would have flipped the derived class to `raw-substring`.

## Note

The live fetch is a freshness cross-check only. The C1 counter reads
committed blobs (`git show <rev>:<path>`) exclusively; nothing in this
report enters the lane's scored surface, and no lane file was written
other than this report.
