# ScribeEntryDraft — C2 entry draft, round 34 wave 1

Draft: `/fast/scratch/hyaku/kake-r34/w1/ScribeEntryDraft/link-preview-metadata.md` (179 lines, sha256 `336ef643ba7fd4054800e5ac09cf06726d414edc024b519f966d56ac22d3d1e0`). Land byte-identical as `corpus/knowledge/link-preview-metadata.md`. Header is exactly 8 lines (source, verified-at, recheck, scope, ground, coverage, falsifier, counter); census line sits alone at draft:128, after the header, unfenced.

## What I built

- Entry sections: link-preview reads (draft:18, S067), platform guidance (draft:53, S068), chat-crawler fetching (draft:80, S069), Mastodon PreviewCard (draft:99, S070), census (draft:118), offline operator-gated source fixes (draft:147), limits (draft:161).
- Census line at draft:128 is `ds4cc-7fc6aa2f-og-census: pages=102 og:title=87 og:type=87 og:image=1 og:url=87 all-four=1 og-url-equals-canonical=87`, copied from `census.derived` in `.ufo/waves/round-34/verification/c2-at-d08d8de.json` and independently reproduced from the retained `html.tar.xz` by `/fast/scratch/hyaku/kake-r34/w1/ScribeEntryDraft/recount.py` (sha256 `f5d59707cca4cab381ce92552c1a89d172308ae60b3e0dd38df2e8ebe08b2095`).
- Entry text says the census counts tags in source bytes and is not a rendering measurement.

## Gates run (own sandbox only)

1. `python3 -B recount.py` — exit 0; `pages=102 og:title=87 og:type=87 og:image=1 og:url=87 all-four=1 og-url-equals-canonical=87`, identical to `census.derived`.
2. `git clone -q <lane> clone && git -C clone checkout -q a2fe31b2d1d2bf67f832b31fb994869b83dbdb9f`; copied the draft in, plus sandbox-only stub registry rows and `## Gate` lines; commit `883b79bd6a0201f627f4bb6725483bc22acc70e6`; `python3 -B clone/.ufo/waves/round-34/c2_source_census.py --root clone --revision HEAD` — exit 0, `met 5 total 5`, `controlBroken false`, `derivedWhy ok`, `statedLines 1`.
3. Mutant `all-four=2` (commit `97fb26b05d5656c40a0e62a87904c74ec6f15274`) — counter exit 1, census condition fails.
4. Mutant duplicate census line (commit `86f8304b447c49d48e4b1bf434caf96c204fca7f`) — exit 1, `C2 4/5`, `statedLines` no longer 1.
5. Mutant dropping every `S069` citation (commit `9e01d4a24394da6797a6f45557cad989bbb5e92b`) — exit 1, `b_entry_body_cites:false` for S069 only.
6. Quote audit script over the draft: 46 curly-quoted spans, all exact substrings of the retained text after whitespace collapse; every span followed by `(Sxxx)` matched that same source (0 mismatches). Negative control `got a high quality preview in Feed` correctly MISS.
7. No lane command that mutates: only read-only `git ls-tree`/`git cat-file` in the lane; all writes under `/fast/scratch/hyaku/kake-r34/w1/ScribeEntryDraft/`.

## Sentence-to-quote table (claim → supporting phrase → source)

| Claim (draft line) | Supporting phrase | Src |
|---|---|---|
| Four required properties (:20) | “The four required properties for every page are:” | S067 |
| og:title meaning (:23) | “The title of your object as it should appear within the graph” | S067 |
| og:type and extra required (:25) | “Depending on the type you specify, other properties may also be required.” | S067 |
| og:image meaning (:26) | “An image URL which should represent your object within the graph.” | S067 |
| og:url meaning (:28) | “The canonical URL of your object that will be used as its permanent ID in the graph” | S067 |
| website fallback (:30) | “Any non-marked up webpage should be treated as og:type website.” | S067 |
| arrays, first tag wins (:32) | “If a tag can have multiple values…” / “The first tag (from top to bottom) is given preference during conflicts.” | S067 |
| structured-property order (:34) | “Put structured properties after you declare their root tag.” | S067 |
| optional image fields (:36-38) | “og:image:url - Identical to og:image” / “A MIME type for this image.” / “og:image:alt - A description of what is in the image (not a caption).” | S067 |
| URL type restricted (:40) | “All valid URLs that utilize the http:// or https:// protocols” | S067 |
| shared global types (:43) | “The global types are grouped into verticals.” | S067 |
| og:url undecorated, aggregates (:55-57) | “This should be the undecorated URL, without session variables, user identifying parameters, or counters.” / “Likes and Shares for this URL will aggregate at this URL.” | S068 |
| one og:type per URL (:59) | “Each URL should be a single object, so multiple og:type values are not possible.” | S068 |
| image cache keyed by URL (:62) | “Images are cached based on the URL and won’t be updated unless the URL changes.” | S068 |
| new URL to replace image (:64) | “To update an image after it’s been published, use a new URL for the new image.” | S068 |
| heuristics without tags (:66) | “Without these Open Graph tags, the Facebook Crawler uses internal heuristics to make a best guess…” | S068 |
| debugger inspects and re-scrapes (:71-72) | “The debugger also triggers a scrape of your page” / “show which meta tags the crawler scrapes as well as any errors or warnings” | S068 |
| URL-first sharing, gzip (:74-77) | “Most content is shared to Facebook as a URL…” / “your server must also use the gzip and deflate encodings” | S068 |
| range-limited fetch (:82) | “It fetches as little of the page as it can (using HTTP Range headers) to extract meta tags about the content.” | S069 |
| tag families looked for (:85) | “Specifically, we are looking for oEmbed and Twitter Card / Open Graph tags.” | S069 |
| referenced media fetched (:87) | “If a page's tags refer to an image, video, or audio file, we will fetch that file as well to check validity…” | S069 |
| global 30-minute cache (:90-91) | “Responses to these requests are cached globally across the service for around 30 minutes.” / “You should not be seeing more than one request for the same URL…” | S069 |
| robots.txt not honored (:95) | “We do not currently honor robots.txt files.” | S069 |
| card generated from OpenGraph (:101) | “Represents a rich preview card that is generated using OpenGraph tags from a URL.” | S070 |
| card fields, nullable image (:103-108) | “url Description: Location of linked resource. Type: String (URL)” / “image Description: Preview thumbnail. Type: nullable String (URL)” | S070 |
| dimensions and type enum (:110-112) | “width Description: Width of preview, in pixels. Type: Integer” / “type Description: The type of the preview card. Type: String (Enumerable, oneOf)” | S070 |
| source dates (:116, :165-166) | “Last updated October 8, 2026” / “Updated : Jun 30, 2026” | S070, S068 |

## Findings

- 15 of 102 pages carry none of og:title/og:type/og:url; 14 of those have a canonical link without og:url, and `benchmarks/benxshitter-frontier.html` has no canonical at all.
- The only page with an og:image is `omegag/index.html`, which is also the only page with all four; all 87 typed pages declare `website`.
- S071 (now redirecting to a generic docs overview) and S072 (GitHub repository social preview) are not used; their receipts record both final URLs.

## Out of scope / not verified

- Condition a (registry rows) and condition c (round-34 gate lines) are sandbox stubs I wrote only to exercise the counter; they are not my deliverable and the real rows must come from the owning seats. The lane at a2fe31b2 still has no S067-S070 rows and no round-34 lesson.
- Nothing was landed in the lane; the draft is not committed there. No live request was made to any property; no platform rendered a card; deployment state of 7fc6aa2f is unknown.
- No tool installs or updates.

Artifacts: `/fast/scratch/hyaku/kake-r34/w1/ScribeEntryDraft/{link-preview-metadata.md,recount.py}` and sandbox clone `/fast/scratch/hyaku/kake-r34/w1/ScribeEntryDraft/clone`.
