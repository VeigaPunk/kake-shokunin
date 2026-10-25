# ScribeGateQuotes — round 49 Gate quote lengths

Axes: operability, freshness. Lesson not edited. Only this report was written.

## Source

- File: `corpus/lessons/round-49.md` section `## Gate` (lines 5–19; next heading `## Mistakes` is line 21).
- Worktree blob `c833ff1910addc1e13b87baccf2bc7e6ffde2558` equals `HEAD:corpus/lessons/round-49.md`.
- `git status --porcelain -- corpus/lessons/round-49.md` printed nothing.
- HEAD `1c846ed2d67b1692ea966be064f0fc04542763c6` (2026-10-24 21:34:41 -0300). Count is of that committed Gate, not a dirty worktree.

## Method

Whitespace tokens, same rule as `len(quote.split())` in `.ufo/waves/round-49/c49_quote_truth.py` (6–25 inclusive). Apostrophes do not split (`won't`, `site's`). A period inside the quotes stays on the last token and does not add a word.

Extraction: every `"..."` span in the Gate, and the counter regex `quote:\s*"([^"]+)"`. Both found the same two strings. Backtick spans (`180d`, paths, `mined`, dates) are not quotes and were not counted.

## Counts

| Id | Line | Tokens | 6–25 | Quote |
|---|---|---|---|---|
| S273 | 9 | 21 | yes | Google won't shift this newly available crawl budget to other pages unless Google is already hitting your site's crawl capacity limit. |
| S274 | 10 | 10 | yes | It reduces your site's crawl rate across the whole hostname |

S273 tokens: Google, won't, shift, this, newly, available, crawl, budget, to, other, pages, unless, Google, is, already, hitting, your, site's, crawl, capacity, limit.

The closing period is inside the S273 quotes, so the 21st token is `limit.` Either way the count is 21.

S274 tokens: It, reduces, your, site's, crawl, rate, across, the, whole, hostname.

No period inside the S274 quotes.

## Result

Both Gate quotes are inside 6–25 words. S273 is 21. S274 is 10. No other double-quoted span is in the Gate.
