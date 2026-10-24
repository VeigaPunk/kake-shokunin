# Scout — S071 (X Cards markup page): confirm or overturn rejection

**Question.** Does a current official X "cards markup" page exist, and should S071 as opened stay rejected?
**Answer (high confidence).** No current page was found on any X docs host reachable by ordinary GET; S071 **should stay rejected as a current source**. S071 as retained is the generic docs landing page (`https://docs.x.com/overview`), not card markup.

## Requests run (sandbox `/fast/scratch/hyaku/kake-r34/w1/ScoutXCardsLocation/`, `curl -sS -L --max-time 25..60`, all exit 0)

| URL requested | status | final URL | bytes |
|---|---|---|---|
| `https://developer.x.com/en/docs/x-for-websites/cards/overview/markup` **(the S071 URL)** | 200 (2 redirects) | `https://docs.x.com/overview` | 622081 |
| `https://docs.x.com/x-for-websites/cards/overview/markup` | **404** | same | 120210 |
| `https://docs.x.com/x-for-websites/cards` | **404** | same | — |
| `https://docs.x.com/x-for-websites/cards/overview/creating-cards` | **404** | same | — |
| `https://docs.x.com/x-for-websites/cards/overview/player-card` | **404** | same | — |
| `https://docs.x.com/x-for-websites/cards/overview/abouts-cards` | **404** | same | 120228 |
| `https://docs.x.com/x-for-websites/cards/overview/markup.md` | **404** | same | — |
| `https://developer.x.com/en/docs/x-for-websites/cards/overview/{creating-cards,player-card}` | 200 (2 redirects) | `https://docs.x.com/overview` | — |
| `https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/{markup,abouts-cards}` | 200 (2 redirects) | `https://docs.x.com/overview` | 622081 |
| `https://developer.x.com/en/docs/twitter-for-websites/cards/overview/markup` | 200 (2 redirects) | `https://docs.x.com/overview` | 622081 |
| `https://dev.x.com/cards` (linked from docs as the Cards home) | 200 (2 redirects) | `https://developer.twitter.com/` (title "X Developer Platform") | 12005 |
| `https://docs.x.com` | 308 | `/overview` | — |
| `https://help.x.com/en/using-x/x-cards` | **403** | same (not bypassed) | — |

Raw redirect hop for the S071 URL (`curl -D -`, no `-L`): `HTTP/2 307` → `location: https://docs.x.com`, then `308` → `/overview`.
Reproduction check: body of today's GET of the S071 URL hashes `sha256 aa5753ceb077f42e1b75da178c7f49146213b3fd9355d4ecaa425cfb682cbdc3`, byte-identical to `receipts.json` S071 `bodySha256` (finalUrl `https://docs.x.com/overview`, status 200, accessed 2026-10-22T20:57:41Z); canonical in that body is `<link rel="canonical" href="https://docs.x.com/overview"/>` and its own `og:url` is `https://docs.x.com/overview`. So the retained S071 text is the landing page, not cards content.

## Index and corpus searches (all exit 0)

- `https://docs.x.com/llms.txt` (200, 3467 B): areas are Overview, X API, Enterprise, Ads, SDKs, fundamentals, Chat, changelog, tutorials — **no Cards area**.
- `https://docs.x.com/sitemap.xml` (200, 167661 B): 1150 `<loc>` entries; 40 under `/x-for-websites/`; **zero URLs containing "card"**.
- `https://docs.x.com/llms-full.txt` (200, 4718502 B, whole doc set): **zero** occurrences of `open graph`, `og:title`, `og:image`, `twitter:card`, `summary_large_image`, `Card Validator`, `post preview`; the only surviving cards traces are embed parameters (`cards=hidden`, "link previews powered by Cards" pointing at `https://dev.x.com/cards`, line 82669) and unrelated Ads API card endpoints.
- `https://docs.x.com/changelog.md` (200, 109512 B): zero hits for `card markup`, `twitter:card`, `open graph`, `card validator`.
- `https://docs.x.com/x-for-websites/webpage-properties(.md)` (200, 3673 B) is widget theming only (`twitter:widgets:*`, `twitter:dnt`, canonical link) — no card markup tags. It is the closest remaining `x-for-websites` page and is **not** a substitute.

## Historical evidence (why the URL looks like it should work)

Wayback CDX for the exact S071 URL (`http://web.archive.org/cdx/search/cdx?...`, exit 0): last `200` capture `20260201012312`, first `307` capture `20260227105036` — the page died between those two dates, during the move to docs.x.com.
Archived body (`https://web.archive.org/web/20251208131832id_/https://developer.x.com/en/docs/x-for-websites/cards/overview/markup`, 200, 71694 B) is titled "Cards markup | Docs | X Developer Platform" and states, 14 words: **"The table in this section explains the OpenGraph fallback behavior for each Twitter tag."** Its table covers `twitter:card` plus `og:type`/`og:title`/`og:description` fallback ("if twitter:card is absent, then a summary card may be rendered"). This is the content S071 was expected to supply — archived, not current, so it is not a citation for a 2026-10 freshness claim.

## Verdict

- **Confirm the rejection.** S071, as opened on 2026-10-22, resolves to `https://docs.x.com/overview` (622081 B, hash-matched above). Basing a "current X card markup requirements" claim on it would attribute landing-page text to a page that no longer exists.
- No current official cards markup page was found at: developer.x.com cards paths, developer.twitter.com cards paths, docs.x.com cards paths (incl. `.md`), the docs sitemap, the docs `llms.txt` index, the docs `llms-full.txt` corpus, or the changelog; `dev.x.com/cards` now bounces to the developer.twitter.com root.
- If the round wants X-side card guidance at all, the only honest options are (a) drop the X/`twitter:card` requirement from the knowledge doc, or (b) cite the archived 2025-12 snapshot explicitly as historical, with its capture date.

## Not verified / gaps

- `help.x.com/en/using-x/x-cards` returned 403 to plain curl; I did **not** retry with a browser user agent or any challenge bypass, so X Help Center absence is unproven.
- I did not exhaustively enumerate other X subdomains (e.g. business.x.com, publish.x.com) — none is referenced by the live docs set as card-markup documentation.
- Two earlier questions are outside this item and were not touched: whether cards content exists on operator-owned sites, and any counter/selftest trust question.

## Provenance

Sandbox artifacts: `/fast/scratch/hyaku/kake-r34/w1/ScoutXCardsLocation/tmp/{x1.html,x2.html,llms.txt,sitemap.xml,llms-full.txt,ch.md,wb2.html,cdx.json,overview.md,a3d8edaa}`. No tools installed or updated; no pacman used. All requests were ordinary GETs to public X/GitHub-adjacent hosts and web.archive.org; no owned-property hosts touched.
