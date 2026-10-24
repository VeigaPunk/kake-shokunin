# Round 34 wave 1 — ScribeSourcesRows (leaf): SOURCES rows S067–S072 and the round-34 `## Gate` lines

Built six registry rows and six lesson Gate lines for the link-preview-metadata frontier from the
retained, already-opened texts; nothing was fetched live and no lane file other than this report was written.

Draft artifacts (sandbox):
- `/fast/scratch/hyaku/kake-r34/w1/ScribeSourcesRows/draft-rows.md` (header + six rows)
- `/fast/scratch/hyaku/kake-r34/w1/ScribeSourcesRows/quotes.py` (substring checker)

## Commands and outcomes

- `python3 -B quotes.py` (sandbox) — exit 0. Output:
```
S067: substring=YES words=8 in_6_25=yes offset=955
S068: substring=YES words=23 in_6_25=yes offset=1382
S069: substring=YES words=13 in_6_25=yes offset=671
S070: substring=YES words=14 in_6_25=yes offset=3020
S071: substring=YES words=15 in_6_25=yes offset=45
S072: substring=YES words=16 in_6_25=yes offset=3016
ALL_OK
```
- `awk -F'|' … NF!=13` on `draft-rows.md` — exit 0, printed `0` malformed rows; row count 6.
- Contract enum / duplicate-id / tier-inflation awk over `draft-rows.md` — exit 0, printed nothing;
  status histogram `mined=4 rejected=2`.
- Per-row cell split in python — exit 0; every row 11 columns, status/opened/recheck/used-by as written.
- `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` — printed `66`; table ends at
  line 74, `## Paths` starts line 76, so the rows belong after S066 at line 75.
- `ls corpus/lessons/round-34.md` — exit 2, file absent; Gate lines below are a paste-ready draft.
- Offline text probes over retained `S071.txt`/`S072.txt` — `card` 1/0, `meta` 0/0, `og:` 0/0; the single
  S071 "card" is the payment-card sentence, so neither page carries card/meta markup.

## Six rows (place after S066; `used-by` path is the C2 entry, not yet written)

| S067 | The Open Graph protocol — https://ogp.me/ | spec | A | The protocol's own statement of the metadata a page carries: the four required properties and the structured-property rules; not a statement about how any platform builds or renders a preview card | Basic Metadata section, the four required properties list and the og:url definition; ogp.me fetched 2026-10-22T20:57:39Z, HTTP 200, retained text sha256 0174794e…675581 | The protocol requires og:title, og:type, og:image and og:url on every page, and defines og:url as the canonical URL that serves as the object's permanent graph ID | mined | 2026-10-22 | 90d | corpus/knowledge/link-preview-metadata.md |
| S068 | Meta for Developers: A Guide to Sharing for Webmasters — https://developers.facebook.com/docs/sharing/webmasters/ | docs | A | Meta's own description of how the Facebook crawler reads a page's Open Graph markup for a shared link and what it does when the tags are absent; not a statement about other platforms and not a guarantee of a rendered card | Open Graph Markup section and the og:title, og:description, og:image and og:type tag table; page states "Updated : Jun 30, 2026", requested URL redirected to https://developers.facebook.com/documentation/sharing/webmasters, retained text sha256 2c9a5d3c…5baa72 | The Facebook crawler builds a shared link's title, description and preview image from Open Graph tags and falls back to internal heuristics when a page carries none | mined | 2026-10-22 | 90d | corpus/knowledge/link-preview-metadata.md |
| S069 | Slack: Robots — https://api.slack.com/robots | docs | A | Slackbot-LinkExpanding's documented link-unfurl fetch and the tag families it reads; not a statement about other crawlers and not a statement about how Slack renders a card | Meet the Robots section, the Slackbot-LinkExpanding entry and the following response-cache paragraph; fetched 2026-10-22T20:57:41Z, HTTP 200, retained text sha256 e39bdc3d…b2c722 | Slack's link robot fetches as little of a page as it can and extracts oEmbed and Twitter Card or Open Graph tags to unfurl a posted link | mined | 2026-10-22 | 90d | corpus/knowledge/link-preview-metadata.md |
| S070 | Mastodon documentation: PreviewCard entity — https://docs.joinmastodon.org/entities/PreviewCard/ | docs | A | Mastodon's own definition of the PreviewCard entity and the attributes it carries; not a statement about tag precedence and not a statement about how any instance renders a card | PreviewCard entity, the opening definition and the Attributes list; fetched 2026-10-22T20:57:41Z, HTTP 200, retained text sha256 81f99a9d…1df9539 | Mastodon builds a PreviewCard from a URL's OpenGraph tags, and its attributes include url, title, description, type, image and provider_name | mined | 2026-10-22 | 90d | corpus/knowledge/link-preview-metadata.md |
| S071 | X Developer Platform: Cards markup — https://developer.x.com/en/docs/x-for-websites/cards/overview/markup (final URL https://docs.x.com/overview) | docs | C | The content served at the requested X Cards markup URL on 2026-10-22 | Requested URL redirected to https://docs.x.com/overview, 2026-10-22T20:57:41Z, HTTP 200; the retained text is the documentation-index navigation and holds no meta or og: property and one "card" in a payment sentence, text sha256 05206565…b2cd31b | REJECTED: the cards markup URL now redirects to a generic docs.x.com overview whose retained text carries no cards markup and no meta or og: property, so it cannot ground any card-tag rule; flip: a GET of the cards markup path serves the markup documentation | rejected | 2026-10-22 | 90d | — |
| S072 | GitHub Docs: Customizing your repository's social media preview — https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview | docs | A | GitHub's repository-level social preview image setting only; not page-level Open Graph metadata that a published page carries | Adding an image to customize the social media preview of your repository section and the Settings > Social preview steps; fetched 2026-10-22T20:57:42Z, HTTP 200, retained text sha256 c248a847…7bd289b | REJECTED: GitHub documents a repository Settings > Social preview image upload, and the retained text names no meta or og: property, so this is not page metadata the lane's properties publish; flip: the page documents Open Graph tags a page's head carries | rejected | 2026-10-22 | 90d | — |

## Six Gate lines (round-34 lesson `## Gate`, paste-ready)

- S067 — https://ogp.me/ — accessed 2026-10-22T20:57:39Z, HTTP 200 — admit, tier A, kind spec, status mined: the four required Open Graph properties; quote “The four required properties for every page are” (Basic Metadata section; 8 words; the list continues with og:title, og:type, og:image, og:url and the og:url definition).
- S068 — https://developers.facebook.com/docs/sharing/webmasters/ (redirects to …/documentation/sharing/webmasters) — accessed 2026-10-22T20:57:39Z, HTTP 200 — admit, tier A, kind docs, status mined: the Facebook crawler's use of Open Graph tags and its heuristic fallback; quote “Without these Open Graph tags, the Facebook Crawler uses internal heuristics to make a best guess about the title, description, and preview image” (Open Graph Markup section; 23 words).
- S069 — https://api.slack.com/robots — accessed 2026-10-22T20:57:41Z, HTTP 200 — admit, tier A, kind docs, status mined: Slack's link robot extracts oEmbed and Twitter Card / Open Graph tags; quote “Specifically, we are looking for oEmbed and Twitter Card / Open Graph tags.” (Meet the Robots, Slackbot-LinkExpanding entry; 13 words).
- S070 — https://docs.joinmastodon.org/entities/PreviewCard/ — accessed 2026-10-22T20:57:41Z, HTTP 200 — admit, tier A, kind docs, status mined: a PreviewCard is generated from a URL's OpenGraph tags; quote “Represents a rich preview card that is generated using OpenGraph tags from a URL.” (PreviewCard entity opening definition; 14 words).
- S071 — https://developer.x.com/en/docs/x-for-websites/cards/overview/markup (final https://docs.x.com/overview) — accessed 2026-10-22T20:57:41Z, HTTP 200 — reject, tier C, kind docs, status rejected: the URL now serves the generic documentation index with no cards markup; quote “Fetch the complete documentation index at: /llms.txt Use this file to discover all available pages” (page head, documentation index; 15 words).
- S072 — https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview — accessed 2026-10-22T20:57:42Z, HTTP 200 — reject, tier A for the repository setting but out of scope, kind docs, status rejected: a repository Settings > Social preview image upload, not page metadata; quote “You can customize the image displayed on social media platforms when someone links to your repository.” (page opening; 16 words).

## Limits and notes

- Not verified: the rows are a draft, not applied to `corpus/SOURCES.md` (leaf bound). `corpus/knowledge/link-preview-metadata.md` does not exist yet, so the contract census "mined rows whose used-by paths do not exist" will flag S067–S070 until the C2 entry lands; the four `mined` statuses depend on that entry actually citing all four rows.
- No live request was made by this seat; S068's redirect is read from `receipts.json` only and was not re-fetched.
- Rejection evidence (not a Gate line): S071 retained text has exactly one `card` (payment card), zero `meta`, zero `og:`; S072 has zero of each and only the Settings > Social preview image steps.
- Row changes logged old→new: all six are new (`—` → status above, opened `2026-10-22`, recheck `90d`); no existing row's cells change.
- Tools installed/updated: none.
