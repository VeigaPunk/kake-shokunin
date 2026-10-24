source: S067 https://ogp.me/; S068 Facebook “A Guide to Sharing for Webmasters” https://developers.facebook.com/docs/sharing/webmasters/; S069 Slack Robots https://api.slack.com/robots; S070 Mastodon PreviewCard https://docs.joinmastodon.org/entities/PreviewCard/ (ids in corpus/SOURCES.md)
verified-at: 2026-10-22 (each of the four opened with one public GET at 2026-10-22T20:57:39Z–20:57:41Z, HTTP 200; S068 answered on developers.facebook.com/documentation/sharing/webmasters; retained visible text and receipts under .ufo/waves/round-34/sources/, text sha256 S067 0174794e…, S068 2c9a5d3c…, S069 e39bdc3d…, S070 81f99a9d…)
recheck: 90d, or on an Open Graph, Facebook sharing, Slack unfurl or Mastodon PreviewCard change — re-open each page once (the logic of `.ufo/waves/round-34/fetch_sources.py`, run in a sandbox) and compare the visible-text sha256 with `.ufo/waves/round-34/sources/receipts.json`; the counter `python3 -B .ufo/waves/round-34/c2_source_census.py --root . --revision <commit>` replays the retained text only and cannot see a page change
scope: The link-preview metadata a social or chat platform reads from a static page — the Open Graph required properties, Facebook and Slack crawler behaviour, the Mastodon PreviewCard entity — plus one offline census of Open Graph tags in the ds4cc source tree at 7fc6aa2f. No live request to an operator-owned property; nothing here says what ds4cc.com serves or what any platform actually renders.
ground: The four retained pages named above, plus the retained `git archive` of the 102 ds4cc `.html` paths at commit 7fc6aa2fc12451dd451fed5a9ee7125f3a90e884 (`tree.txt` and `html.tar.xz` under .ufo/waves/round-34/sources/ds4cc-7fc6aa2f/). Every factual sentence about a platform carries a curly-quoted span that is an exact substring of one retained text, with the source id in parentheses; census sentences are read from that archive and the matching receipt.
coverage: The four required properties and what each means, arrays and structured-property order, the website type fallback, the declared URL form; Facebook's undecorated canonical og:url, one og:type per URL, image caching by URL and the Sharing Debugger re-scrape; Slack's range-limited fetch, tag preference and global cache; the Mastodon card entity and its type enumeration; one commit-pinned ds4cc census.
falsifier: A fresh fetch of one of the four pages that contradicts a quoted sentence below, or a blob-exact recount of the retained archive that disagrees with the census line below.
counter: python3 -B .ufo/waves/round-34/c2_source_census.py --root . --revision <commit> — five conditions: four registry rows mined and dated 2026-10-22, each id cited in this entry, one 6–25-word quote per id in the round-34 gate, each quote an exact substring of the retained text, and the census line equal to the counter's own blob-exact recount; exit 0 only when all five hold and the one-letter control fails.

# Link-preview metadata (Open Graph)

Coverage-map ground: operability and freshness of the web properties — the
metadata a shared URL exposes before anyone clicks it. `static-canonical-
preflight.md` owns the canonical link and publisher selection; this entry
treats that link as one input to a preview and does not repeat its analysis.
`publish-channels.md` owns where a page is published, not what a preview shows.

## What a link preview reads (S067)

- The protocol names four required properties, not a recommended set: “The
  four required properties for every page are:” (S067), namely `og:title`,
  `og:type`, `og:image` and `og:url`.
  - `og:title` is “The title of your object as it should appear within the
    graph” (S067).
  - `og:type` is “The type of your object” (S067), and the requirements do not
    stop there: “Depending on the type you specify, other properties may also
    be required.” (S067).
  - `og:image` is “An image URL which should represent your object within the
    graph.” (S067).
  - `og:url` is “The canonical URL of your object that will be used as its
    permanent ID in the graph” (S067).
- A page without markup is not untyped at the consumer: “Any non-marked up
  webpage should be treated as og:type website.” (S067).
- Repeated tags form an array, and order is preference: “If a tag can have
  multiple values, just put multiple versions of the same <meta> tag on your
  page.” (S067) and “The first tag (from top to bottom) is given preference
  during conflicts.” (S067). Structured properties follow their root tag:
  “Put structured properties after you declare their root tag.” (S067).
- Image detail is optional and additive: “og:image:url - Identical to og:image”
  and “A MIME type for this image.” (S067) for `og:image:type`, plus
  “og:image:alt - A description of what is in the image (not a caption).”
  (S067).
- The declared URL type is restricted to web schemes: “All valid URLs that
  utilize the http:// or https:// protocols” (S067). [INFERENCE] A relative
  `og:url` therefore fails the declared type before any canonical comparison
  is made.
- Types are shared, not invented per page: “When the community agrees on the
  schema for a type, it is added to the list of global types.” (S067), and
  “The global types are grouped into verticals.” (S067). [INFERENCE] Picking a
  type outside that list, or a second type, buys nothing a platform is obliged
  to understand.

## Platform guidance (S068)

- `og:url` is the clean address of record: “The canonical URL for your page.”
  (S068), and “This should be the undecorated URL, without session variables,
  user identifying parameters, or counters.” (S068), because “Likes and Shares
  for this URL will aggregate at this URL.” (S068).
- Exactly one type per URL: “Each URL should be a single object, so multiple
  og:type values are not possible.” (S068). [INFERENCE] A second `og:type` is a
  markup error, not an alternative value.
- The image cache is keyed by address: “Images are cached based on the URL and
  won’t be updated unless the URL changes.” (S068), so a replacement needs a
  new address: “To update an image after it’s been published, use a new URL for
  the new image.” (S068).
- A missing tag is guessed, not skipped: “Without these Open Graph tags, the
  Facebook Crawler uses internal heuristics to make a best guess about the
  title, description, and preview image for your content.” (S068).
  [INFERENCE] An incomplete page still produces a card; the card is just not
  the one the author chose.
- The debugger both inspects and refreshes: it will “show which meta tags the
  crawler scrapes as well as any errors or warnings” (S068), and “The debugger
  also triggers a scrape of your page” (S068).
- Sharing is URL-first and compression-sensitive: “Most content is shared to
  Facebook as a URL, so it’s important that you mark up your website with Open
  Graph tags to take control over how your content appears on Facebook.”
  (S068), and “your server must also use the gzip and deflate encodings”
  (S068).

## How chat crawlers fetch (S069)

- The Slack link robot reads a range, not a document: “It fetches as little of
  the page as it can (using HTTP Range headers) to extract meta tags about the
  content.” (S069).
- Two tag families are accepted: “Specifically, we are looking for oEmbed and
  Twitter Card / Open Graph tags.” (S069).
- Referenced media is fetched as well: “If a page's tags refer to an image,
  video, or audio file, we will fetch that file as well to check validity and
  extract other metadata.” (S069).
- The cache is global and short-lived: “Responses to these requests are cached
  globally across the service for around 30 minutes.” (S069) and “You should
  not be seeing more than one request for the same URL from us more frequently
  than that.” (S069). [INFERENCE] A corrected scrape can persist for about half
  an hour and then expire without any action.
- robots.txt is not the gate: “We do not currently honor robots.txt files.”
  (S069). [INFERENCE] A disallowed page can still be unfurled, so robots
  policy is not a substitute for leaving preview tags out.

## How Mastodon builds a preview card (S070)

- The card is derived from the page's markup: “Represents a rich preview card
  that is generated using OpenGraph tags from a URL.” (S070).
- The entity carries the address, title, description and image: “url
  Description: Location of linked resource. Type: String (URL)” (S070),
  “title Description: Title of linked resource. Type: String” (S070),
  “description Description: Description of preview. Type: String” (S070) and
  “image Description: Preview thumbnail. Type: nullable String (URL)” (S070).
- Dimensions are first-class fields: “width Description: Width of preview, in
  pixels. Type: Integer” (S070) and “height Description: Height of preview, in
  pixels. Type: Integer” (S070).
- The card type is an enumeration: “type Description: The type of the preview
  card. Type: String (Enumerable, oneOf)” (S070), with values “link = Link
  OEmbed photo = Photo OEmbed video = Video OEmbed rich = iframe OEmbed.”
  (S070). [INFERENCE] A missing image degrades the card rather than suppressing
  it, because the entity's image field is explicitly nullable.
- The page is dated: “Last updated October 8, 2026” (S070).

## ds4cc at 7fc6aa2f — Open Graph census

Population: the 102 `.html` paths of the retained `git archive` of
ds4cc-marketplace at commit `7fc6aa2fc12451dd451fed5a9ee7125f3a90e884`. The
count is over source bytes: a `<meta property="og:…">` counts when its content
is non-empty after stripping whitespace, and `og:url` is compared with the
first `<link rel="canonical">` href resolved against `https://ds4cc.com/`
(trailing `index.html` removed). It is not a measurement of what any platform
renders, and it says nothing about the live site.

ds4cc-7fc6aa2f-og-census: pages=102 og:title=87 og:type=87 og:image=1 og:url=87 all-four=1 og-url-equals-canonical=87

- The seven numbers are copied from `census.derived` in
  `.ufo/waves/round-34/verification/c2-at-d08d8de.json` and were reproduced
  independently from the retained archive.
- The gap is absence, not disagreement: 15 pages carry none of the
  title/type/url triple, 14 of those still carry a canonical link without an
  `og:url`, and all 87 pages that declare `og:url` point it at their canonical
  link (the equality count equals the `og:url` count). The fifteenth page,
  `benchmarks/benxshitter-frontier.html`, has no canonical link at all.
- The single image-bearing page is `omegag/index.html` (`og:type` `website`,
  `og:url` `https://ds4cc.com/omegag/`, image
  `https://ds4cc.com/omegag/assets/masterpiece.png`), and it is the only page
  with all four required properties; all 87 typed pages declare `website`.
- [INFERENCE] On these counts a shared ds4cc link would arrive typed and
  canonically addressed but almost always without an author-chosen image, so
  the preview falls back to platform heuristics (S068) or a text-only card
  (S070). That inference is about markup, not about a rendered result.

## Fixing the source (offline, operator-gated)

- Add all four required properties to the 15 unmarked pages before touching
  anything already shared; choose `og:type` from the global type list (S067)
  and keep exactly one (S068).
- Keep `og:url` equal to the canonical link and undecorated (S068), and add a
  genuinely new image URL where an image is wanted, because the cache follows
  the URL (S068).
- Validate offline against a manifest of local pages — the census recipe in
  the counter above reproduces the same source-byte check without a network
  call — then hand the change to the operator. Kake seats do not push or
  deploy; the Sharing Debugger re-scrape (S068) is an operator action on a
  live URL and is outside this entry's evidence.

## Limits

- No platform rendered anything here: the four pages are documentation, and
  no card was requested for a ds4cc URL.
- Facebook's guidance is dated “Updated : Jun 30, 2026” (S068) and Mastodon's
  page “Last updated October 8, 2026” (S070); both can change without notice,
  which is why the recheck above replays the retained bytes and then re-fetches.
- S069 speaks for Slack's robots only; it says nothing about other chat
  crawlers, and its no-robots.txt statement is a current behaviour, not a
  contract.
- S070 documents an API entity; it does not guarantee that any instance fetches
  or displays a given page.
- The census is one commit of source bytes. Commit 7fc6aa2f is the retained
  upstream head, not proof of what is deployed, and cached previews (S068,
  S069) mean a correct source fix may not show immediately.
- S071 (X cards markup URL, now redirecting to a generic docs overview) and
  S072 (GitHub repository social-preview docs) were opened for screening and
  are not used here; see `.ufo/waves/round-34/sources/receipts.json` for their
  final URLs.

## Round-34 wave-1 additions (appended after the declaration; not counted toward C2)

These come from wave-1 seat reports and one source (S073) opened after the
declaration. The C2 counter does not read them; they are knowledge, not
claim evidence.

- One more consumer contract (S073, Discord): the tags must be in what the
  server sends — “No code is executed, so tags added by a client-side script
  after load are never seen.” (S073) — and Discord's Tag Reference says “The
  key comes from name if present, otherwise from property” (S073). So a
  `<meta name="og:image">` counts on Discord although the protocol's own markup
  uses `property` (S067). The lane's audit counts only `property` (lane
  policy, stated in `scripts/link_preview_audit.py`); a page relying on
  `name=` would be flagged there and could still preview on Discord.
- Where ds4cc's tags come from (wave-1 `ScoutDs4ccTemplateSource`): the 102
  pages are hand-authored static HTML; the Pages workflow uploads the
  directory as-is and no script emits Open Graph tags. The 15 pages without
  the title/type/url triple are the 11 `burnerchrome/` pages, `bloat.html`,
  `burnerchrome.html` (a zero-second refresh shim), `exa.html` and
  `benchmarks/benxshitter-frontier.html`. The tree has no site-wide default
  raster image, so adding `og:image` to the other 86 pages needs a new image
  asset as well as a tag per page.
- Canonical versus sitemap (wave-1 `ScoutOgUrlCanonicalSitemap`): all 87
  `og:url` values equal their canonical link and their own sitemap loc, but
  `bloat.html` and `exa.html` declare canonicals `https://ds4cc.com/bloat` and
  `https://ds4cc.com/exa` while the sitemap lists `…/bloat.html` and
  `…/exa.html`. Neither page has `og:url`, so an Open Graph audit cannot see
  this; it belongs to the canonical preflight (`static-canonical-preflight.md`).
  Whether the extensionless URLs resolve was not checked (owned host, no live
  request).
- The audit on real input (`.ufo/waves/round-34/real_input_run.py`, receipt
  `.ufo/waves/round-34/verification/real-input-at-5613071.json`): over the
  same 102 retained pages the landed tool exits 1 with 101 missing `og:image`
  and 15 each missing `og:title`, `og:type` and `og:url`, and no other
  finding — the census above, seen through the tool.
- Other owned properties, from the round-23 served snapshots of 2026-10-21
  (wave-1 `ScoutOwnedPropertiesOG`): the plazir-15 and charter-ufo-fsd GitHub
  Pages roots carry all four properties; the ds4cc.com root carries no
  `og:image`; the ds4cc kimi.page mirror has a relative `og:url` (`./`) and no
  canonical link; the burnerchrome and veigapunk kimi.page roots, the lucario
  Pages root and the ufo-fsd kimi.pro shell carry no Open Graph tags. These are
  one-day-old captured bytes, not today's live state.

## Round-34 wave-2 corrections (appended; the sections above stay as landed)

- The wave-1 additions preamble says "The C2 counter does not read them".
  That is wrong: the counter reads the whole entry. C2 was measured at
  `9ef758c`, before that section existed, and at later revisions those lines
  change no condition (wave-2 `CriticDeclarationTiming`).
- Header `coverage`: S069 states no "tag preference" between oEmbed and Open
  Graph; it says only that both families are read (wave-2
  `CriticC2Sufficiency`).
- Slack cache bullet: it is the old cached copy that can persist for about
  half an hour after a fix, not the corrected scrape.
- "Any non-marked up webpage should be treated as og:type website." (S067) is
  the protocol's instruction to consumers; that a given platform does so is
  [INFERENCE].
- "Types are shared, not invented per page" overstates S067, which also
  allows custom namespaced types; the operative point stays the labelled
  inference that an off-list type obliges no platform (wave-2
  `ReviewEntryCoreSections`).
- Fixing the source, first step (wave-2 `CriticFrontierValue`): fix the
  canonical-versus-sitemap split on `bloat.html` and `exa.html` before adding
  `og:url` there, or shares collect at `https://ds4cc.com/bloat` and
  `https://ds4cc.com/exa`, which no one has shown to resolve; the lane's
  `scripts/canonical_audit.py` already flags both against the sitemap URL.
  Other gaps it named: the 86 image-less pages need one new image asset; the
  tool does not check that an `og:image` file exists in the tree; the
  ds4cc.kimi.page relative `og:url` is not in the ds4cc source (a Kimi-side
  re-publish, operator-owned); the burnerchrome pages are also mirrored on
  Vercel; S068 lists `og:description` among its basic tags, which the census
  does not count; no freshness pin watches the ds4cc commit behind the census.
- The audit tool now counts `og:image:url` as `og:image` ("og:image:url -
  Identical to og:image", S067) and keeps the first of duplicated attributes
  (`76fac3b`); the census line above is unaffected (no ds4cc page uses either
  form; the real-input run at `76fac3b` gives the same 101/15/15/15).
