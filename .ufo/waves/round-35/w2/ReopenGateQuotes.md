# ReopenGateQuotes — round-35 Gate re-verification (falsify)

Item attacks: the round-35 Gate in `corpus/lessons/round-35.md:44-54` — every quote as an
exact substring of the retained text with the right word count, plus live re-open of S086 and
S087.

## Verdict

The Gate is substantively truthful on all 11 rows today. One low-severity factual error:
S087's quoted word count (11 stated, 12 actual). Live S086 and S087 both still hold — S086
changed, S087 is still the identical 404 body.

## 11-row table (substring of retained `.txt` + word count, whitespace tokenization)

| Row | Exact substring of retained text | Claimed words | Actual words | Pass |
|---|---|---|---|---|
| S078 | yes | 13 | 13 | yes |
| S079 | yes | 13 | 13 | yes |
| S080 | yes | 11 | 11 | yes |
| S081 | yes | 22 | 22 | yes |
| S082 | yes | 15 | 15 | yes |
| S083 | yes | 6 | 6 | yes |
| S084 | yes | 8 | 8 | yes |
| S085 | yes | 6 | 6 | yes |
| S086 | yes | 19 | 19 | yes |
| S087 | yes | 11 | **12** | **no** |
| S006 | yes | 20 | 20 | yes |

## Findings

1. LOW — S087 word count wrong. `round-35.md:53` claims the quote is "11 words"; the quote
   `404 - GitHub Docs GitHub Docs Page not found. Return to home.` tokenizes to 12 words on
   plain whitespace split (same method that validates the other ten rows). The quote itself IS
   an exact substring of the retained body (`sources/S087.txt:1`, which is the whole served
   body). Substance unaffected: the row is a genuine 404 reject and still live. The count
   error originates with the L1 (wave-1 `ScribeGateLines.md` contains no S087 row).
2. Confirmed OK — the ten other quotes are exact substrings with correct counts, including the
   S086 quote (19 words) and S006's re-open quote (20 words).

## Live results (2026-10-22, fetched now, GET only)

- S086 `https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site`
  → HTTP 200, final URL unchanged, 151,259 bytes, sha256 `5f4762d64fdfd165440255f918df048d5443aef92950bdb85ccfce7717f727ec`
  — byte-identical to the retained body (receipt `receipts.json:112-116`). Extracted text
  (HTML minus script/style/tags, entities decoded, whitespace collapsed; 1395 words) contains
  the quote verbatim: "disable the Jekyll build process by creating an empty file called
  .nojekyll in the root of your publishing source". Quote holds, status holds.
- S087 `https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/bypassing-jekyll-with-nojekyll`
  → HTTP 404, final URL unchanged, 502 bytes, sha256 `979615bad4719ae23bf76385ee60de8b1b05c785ce74497dee80ecb54c69c522`
  — byte-identical to the retained body (receipt `receipts.json:124-128`). Extracted text (20
  words) contains the quote verbatim. Still 404, no redirect; reject stands.

## Commands run (all exit 0 unless noted)

- `python3 -B .../verify_quotes.py` — retained substring + word-count check; exit 1 (the S087
  mismatch), per-row table above.
- `python3 -B .../check_live.py` — live HTML text extraction + substring check; exit 0.
- `curl -sS -o live_s086.html -w ... -L --max-time 60 <S086 url>` — status=200, exit 0.
- `curl -sS -o live_s087.html -w ... -L --max-time 60 <S087 url>` — status=404, exit 0.
- `sha256sum live_s086.html live_s087.html` — matches receipt bodySha256 values exactly.

## Evidence pointers

- Quotes under test: `corpus/lessons/round-35.md:44-54`; S087 word-count claim at `:53`.
- Retained texts: `.ufo/waves/round-35/sources/S078.txt` … `S087.txt`, `S006.txt`.
- Receipts: `.ufo/waves/round-35/sources/receipts.json` (S086 at :110-121, S087 at :122-133).
- Sandbox artifacts: `/fast/scratch/hyaku/kake-r35/w2/ReopenGateQuotes/{verify_quotes.py,check_live.py,live_s086.html,live_s087.html}`.

## Residual risk / gaps

- I re-fetched only S086/S087 (item scope); the other nine rows were verified against retained
  text only, not live.
- S087 "11 words" may have been counted excluding the standalone hyphen; the quoted string's
  count is 12 under the split used by all other rows.
- No tools installed/updated (none needed); no git/jj used; no owned-site traffic; no subagents.
