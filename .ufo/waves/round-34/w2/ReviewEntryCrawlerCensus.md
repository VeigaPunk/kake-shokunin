# Wave-2 review — C2 entry: S069/S070 sections, ds4cc census, fixing-the-source, limits

Seat: KakeR34.ReviewEntryCrawlerCensus · 2026-10-22 · target `corpus/knowledge/link-preview-metadata.md` at 24a16474ee73e20453f3e1be9d2f33573c5196d9.
No findings of substance: every assigned claim reproduces. One precision note on "exact substring" wording.

## Commands (all exit 0)

- `git show 24a1647:corpus/knowledge/link-preview-metadata.md > entry.md` (sandbox /fast/scratch/hyaku/kake-r34/w2/ReviewEntryCrawlerCensus/)
- `tar -xJf …/sources/ds4cc-7fc6aa2f/html.tar.xz -C archive; find archive -name '*.html' | wc -l` → 102
- `grep -c '\.html' …/tree.txt` → 102; `sha256sum sources/S069.txt sources/S070.txt` → e39bdc3d98…, 81f99a9dbe…
- Python recount + quote check over the 102 extracted pages (regex meta/link parse, `urljoin('https://ds4cc.com/'+relpath, href)`, trailing `index.html` stripped, whitespace-collapsed quote match)

## Sentence table

| Entry claim (section) | Verdict | Evidence |
|---|---|---|
| S069 quotes: range-fetch, oEmbed/Twitter/OpenGraph tags, media re-fetch, ~30-min global cache, ≤1 request per URL, no robots.txt (6 spans) | TRUE — all 6 verbatim vs S069.txt after whitespace-collapse + curly-apostrophe norm | check output 6/6; S069.txt sha256 e39bdc3d… equals entry `verified-at` and receipts.json |
| S070 quotes: PreviewCard generated from OpenGraph tags; url/title/description/image/width/height/type field rows; link/photo/video/rich enumeration; "Last updated October 8, 2026" (10 spans) | TRUE — all 10 verbatim vs S070.txt under same norm | check output 10/10; S070.txt sha256 81f99a9d… matches |
| Census line `pages=102 og:title=87 og:type=87 og:image=1 og:url=87 all-four=1 og-url-equals-canonical=87` (census) | TRUE — my independent recount returns the identical seven numbers | Python recount, exit 0; archive extracted from retained html.tar.xz, 102 .html = tree.txt 102 |
| "15 pages carry none of the title/type/url triple" (census) | TRUE — 15 found: 11 `burnerchrome/*.html`, `burnerchrome.html`, `bloat.html`, `exa.html`, `benchmarks/benxshitter-frontier.html` | recount page list |
| "14 of those still carry a canonical link without an og:url" (census) | TRUE — 14/15 have a canonical; globally 14 pages have canonical and no og:url | recount |
| "benchmarks/benxshitter-frontier.html has no canonical link at all" (census) | TRUE — canonical None for that page | recount |
| "all 87 pages that declare og:url point it at their canonical link" (census) | TRUE — zero og:url≠canonical mismatches; 87=87 | recount |
| "single image-bearing page is omegag/index.html … website / https://ds4cc.com/omegag/ / …/masterpiece.png; only all-four page" (census) | TRUE — exactly 1 page with og:image, values match verbatim; all-four=1 is that page | recount |
| "all 87 typed pages declare website" (census) | TRUE — og:type distribution {website: 87}, no second value, no page with two og:type values found | recount |
| Census numbers copied from `census.derived` in c2-at-d08d8de.json (census) | TRUE — receipt `derived` = {102,87,87,1,87,1,87}, `derivedWhy: ok` | verification/c2-at-d08d8de.json |
| "census recipe in the counter reproduces the same source-byte check without a network call" (fixing) | TRUE — counter docstring condition e recounts tree.txt+html.tar.xz offline with the same non-empty-stripped-content rule and the same canonical resolution I re-implemented | `git show 24a1647:.ufo/waves/round-34/c2_source_census.py` docstring, condition e |
| Limits: Facebook "Updated : Jun 30, 2026" (S068), Mastodon "Last updated October 8, 2026" (S070) | TRUE — both exact substrings (S068 verbatim byte-exact) | normalized check 2/2 on S068.txt+S070.txt |
| Limits: S071 "now redirecting to a generic docs overview", S072 GitHub social-preview docs, final URLs in receipts.json | TRUE — receipts S071 finalUrl https://docs.x.com/overview (generic overview), S072 social-media-preview page, both status 200 | sources/receipts.json |

## Precision note (minor, not a defect)

The entry's `ground` line says each quoted span "is an exact substring of one retained text". Against the raw single-line source files most spans are NOT byte-exact substrings — the entry hard-wraps lines, and "page's" uses a straight apostrophe where S069 has the curly glyph. The C2 counter (condition d) compares whitespace-collapsed, and under that rule 18/18 match with zero content divergence, so the contract's arbiter defines "exact" consistently. Byte-literal readers of the entry alone could see this as overstated wording; no change required.

## Residual risk / not verified

- I did not re-fetch S069/S070 live (not told to open URLs; freshness of the retained texts is the recheck header's job, not this seat's).
- I trusted the retained tar's integrity: I extracted `html.tar.xz` as-is and recounted, but did not myself re-verify per-member Git blob ids against `tree.txt` (counter condition e does; a corrupted-tar scenario would need that check to be wrong too).
- Wave-1 additions section, Registry rows, and the round-34 gate line are out of my assigned scope (other seats).
- No tools installed; no live requests; sandbox only, lane untouched except this report.
