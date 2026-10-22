# ReviewRenderPrimary — re-open S049–S052 (Render docs), freshness check

Seat: KakeR30.ReviewRenderPrimary, round 30 wave 1. Date: 2026-10-22.
Assignment: one ordinary GET each of S049–S052; compare sha256 with receipts; compare visible
text with the fetcher's rule; confirm primary and current; find any "last updated" marker;
note script-JSON content the visible-text rule drops.

## Verdict

All four sources are **primary** (Render's own documentation, served on render.com, no
redirect, self-canonical) and **current** (fresh visible text byte-identical to the retained
`.txt`, across a mid-round Render site redeploy). None of the four pages carries any
per-page "last updated" marker; currency rests on content equality, not a page-stated date.

## Baseline integrity (lane repo, read-only; all exit 0)

1. `sha256sum .ufo/waves/round-30/sources/S04{9}.txt S05{0,1,2}.txt` — each equals its
   `textSha256` in `sources/receipts.json`. Retained text is what the receipts describe.
2. `gunzip -c sources/S0NN.html.gz | sha256sum` — S049 `841b8311…`, S050 `a57b515f…`,
   S051 `7ba689dc…`, S052 `59469467…`, each equals its `bodySha256`.
3. `fetcherSha256` `b9431a5f349c7b85…` in receipts equals `sha256sum .ufo/waves/round-30/fetch_sources.py`
   — the opening fetcher is unchanged. (`scripts/live_snapshot.py` is a different tool,
   `3638891d…`, and has no text-extraction rule; the wave-local fetcher is canonical here.)

## Fresh GETs (one each, no retries, no browser)

`python3 fetch_raw.py` (sandbox, exit 0), plain urllib GET, no redirect occurred
(`finalUrl == url` for all four), 2026-10-22T12:05:32–33Z:

| id | url | status | bytes retained→fresh | bodySha256 retained→fresh |
|----|-----|--------|----------------------|---------------------------|
| S049 | render.com/docs/static-sites | 200 | 320167→320210 | 841b8311…→ef584032… |
| S050 | render.com/docs/redirects-rewrites | 200 | 348130→348130 | a57b515f…→0414da13… |
| S051 | render.com/docs/static-site-headers | 200 | 280291→280377 | 7ba689dc…→0e4241b2… |
| S052 | render.com/docs/custom-domains | 200 | 371923→371966 | 59469467…→6161526f… |

All four content types: `text/html; charset=utf-8`. **Every raw body hash differs from the
receipts** — as the declared claim anticipates for dynamic pages — so the visible-text rule
is the decisive comparison, and it matches (below).

## Drift localization (why bodies differ; `inspect.py`, exit 0)

- S049, S051: Next.js chunk renamed with new deploy id — `…3uk1ctqk7kwib.js?dpl=zcqt4` →
  `…3j_8orpbhrw6y.js?dpl=8b4d78f7c` — Render redeployed its site between 11:49Z and 12:05Z.
  Head also swapped `<meta name="next-size-adjust">` for `<meta name="color-scheme" content="light dark">`.
- All four: fresh per-request `sentry-trace`/`baggage` ids (S050's only difference — same
  byte count, different hash).
- S052: re-hashed `/docs-assets/26bc1c68…` → `2c7b8c48…` etc. inside the RSC flight payload.
- No content-bearing difference in any body.

## Visible-text rule comparison (`compare.py`, exit 0)

Rule copied byte-for-byte from the fetcher (`fetch_sources.py:34-40`: script/style elements
removed, comments removed, tags removed, entities decoded, whitespace collapsed):

1. Fidelity: applying the rule to the **retained** html.gz reproduces every retained `.txt`
   byte-for-byte — 4/4 (`rule_reproduces_retained_txt: True`). The rule is deterministic.
2. Currency: applying the rule to the **fresh** body gives text byte-identical to the
   retained `.txt` — 4/4 (`text_equal: True`); fresh textSha256 equals receipts textSha256
   (S049 `3604f8f5…`, S050 `1c413643…`, S051 `e98982ce…`, S052 `6c1616f8…`); word counts
   equal `textWords` (983 / 854 / 539 / 1488); difflib word-opcodes: 0 changes, 4/4.

## Primary-source confirmation

Each page: title "… – Render Docs", `<link rel="canonical" href="https://render.com/docs/<slug>"/>`
(self-canonical), h1 matches the topic (Static Sites / Static Site Redirects and Rewrites /
HTTP Headers for Static Sites / Custom Domains on Render), and an `application/ld+json`
Organization block naming "Render" (founder Anurag Goel, url render.com). Served from
render.com itself, status 200, no redirect chain.

## Last-updated markers: none

Swept every fresh body (exit 0): zero `<time>` elements, zero `datetime=` attributes, no
"last updated"/"updated on/at" wording, no month-year or ISO dates anywhere (head, text, or
scripts), and the ld+json has no `dateModified`/`datePublished`. The only currency signals
the pages offer are indirect: the live `dpl=` deploy id (site actively redeployed today) and
the markdown preload links below. **The declared C2 "current" claim cannot be evidenced by
an on-page date; today's text-equality is the evidence, and it holds.**

## Dropped script JSON and other invisible content

The visible-text rule removes, per page:

- Two JSON script blocks (identical on all four pages):
  1. `application/ld+json` (708 B): Organization schema — `foundingDate: "2018"` is the
     company founding, **not** a page-update date; no per-page timestamps.
  2. `id="webmcp"` (1 014 B): an agent-tools manifest — notably `render.docs.get-markdown`
     → `GET /docs/{slug}.md`, `render.docs.search` → `/api/agent/docs-search`,
     `render.llms.get-index` → `/llms.txt`. A canonical markdown twin of each docs page exists.
- 12–17 non-JSON script blocks (~173–231 KB total) and 5–6 `self.__next_f` RSC flight
  blocks that duplicate the page content as escaped JSON plus asset hashes (S052's flight
  embeds the changed `/docs-assets/…` ids).
- Also dropped, in `<head>`: `<link rel="preload" as="fetch" href="https://render.com/docs/<slug>.md">`
  on every page. I did **not** fetch the `.md` twins or `/llms.txt` — the mandate was one
  GET per URL — but they are within this documentation site and could give a fresher,
  cleaner currency probe for a future seat.

## Residual risk and gaps

- My GET's User-Agent differed from the opening fetcher's (`kake-shokunin-readonly-preflight/1
  (+GET only)` vs `kake-shokunin-round-30-source-opening (one GET per page)`, `fetch_sources.py:31`);
  harmless here because bodies differed anyway (redeploy) and text matched byte-for-byte.
- No response headers captured (Date/ETag/Last-Modified/Cache-Status): single-GET mandate
  and my fetcher didn't record them, so cache-currency (like round-29's ReopenS042 caveat)
  is unverified; the body drift observed is stronger than headers would be.
- Text equality cannot detect attribute- or script-only content changes; that limitation is
  inherent to the receipts' `textRule` and shared by the declared claim's own comparison.
- I did not re-run the C2 counter itself (not my scope).

## Artifacts (sandbox, absolute paths)

- `/fast/scratch/hyaku/kake-r30/w1/ReviewRenderPrimary/fetch_raw.py` (one-GET fetcher),
  `fetch-meta.json` (status/finalUrl/contentType/bytes/sha256/fetchedAt), `S049.html`–`S052.html`.
- `compare.py` + `compare-out.json` (rule fidelity, text equality, word diffs, marker scan,
  script inventory); `inspect.py` (drift windows, title/canonical/ld+json/webmcp dumps).

No tooling was installed or upgraded (none needed; pacman untouched).
