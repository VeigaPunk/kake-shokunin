# ReviewEntryCoreSections — C2 entry core sections (r34 falsify, wave 2)

Target: `corpus/knowledge/link-preview-metadata.md` @ 24a16474 — header (lines
1–16) and sections "What a link preview reads (S067)" (18–51) and "Platform
guidance (S068)" (53–78). Axes: operability, freshness. Leaf seat; worked in
sandbox `/fast/scratch/hyaku/kake-r34/w2/ReviewEntryCoreSections/clone` (clone
checked out at 24a1647); no lane file touched except this report.

## Commands run (exit codes)

- `git clone -q <lane> clone && git -C clone checkout -q 24a16474…` — 0.
- `sha256sum .ufo/waves/round-34/sources/S06[78].txt` — 0; `S067
  0174794e…`, `S068 2c9a5d3c…` (both equal the `verified-at:` prefixes and
  receipts.json `textSha256`; S069/S070 prefixes also re-hashed equal).
- Python (eval) substring audit of every `“…”` span in scope against the
  whitespace-collapsed retained texts, with `(S0xx)` attribution — 28 spans.
- `grep -nE 'urllib|requests|socket|urlopen|fetch' c2_source_census.py` —
  hits only `from urllib.parse import urljoin` and the `git -C … show`
  subprocess; no HTTP read path (counter truly cannot see a page change).
- `git -C /fast/scratch/hyaku/kake-r33/ds4cc-upstream cat-file -t
  7fc6aa2fc12451dd451fed5a9ee7125f3a90e884` → `commit` (header's archive
  commit exists upstream). `tree.txt`: 1 commit line + 102 `.html` rows.
- `head -6` of `static-canonical-preflight.md`, `publish-channels.md` — both
  exist and own the scopes the header attributes to them.

## Quoted-span check — 28/28 pass

Every curly-quoted span in scope is an exact substring (whitespace collapsed)
of its attributed source: 18 spans → S067.txt, 9 spans → S068.txt, 0
mis-attributed, 0 missing. One span has no `(S0xx)` parenthetical: the L1
`source:` line's “A Guide to Sharing for Webmasters”, a bibliographic title
(directly precedes the URL; it is a substring of S068.txt). No single-curly
quote spans exist in scope; curly apostrophes (`won’t`, `it’s`) match the
retained bytes exactly.

## Sentence table (scope: lines 1–78)

| # | Lines | Sentence (abridged) | Verdict |
|---|-------|--------------------|---------|
| H1–H8 | 1–8 | source/verified-at/recheck/scope/ground/coverage/falsifier/counter fields | supported — every concrete claim re-verified above (receipts, sha256, docstring, 102 paths, commit exists) |
| H9 | 12–15 | "metadata a shared URL exposes before anyone clicks it"; canonical link owned by `static-canonical-preflight.md`; channels by `publish-channels.md` | supported |
| S1 | 20–22 | four required properties (title/type/image/url), "not a recommended set" | supported — source: "The four required properties for every page are:" + list |
| S2–S5 | 23–31 | per-property definitions | supported (4 spans) |
| S6 | 32–33 | unmarked page treated as `og:type website` | supported ("Any non-marked up webpage should be treated as og:type website.") |
| S7 | 34–38 | repeated tags form an array; first wins; structured after root | supported (source heading is literally "Arrays") |
| S8 | 39–42 | image detail optional/additive (url/type/alt) | supported ("The og:image property has some optional structured properties:") |
| S9 | 43–44 | declared URL type = http/https schemes | supported (source's `URL` datatype row) |
| S10 | 45–46 | relative `og:url` fails the declared type | inference — labelled `[INFERENCE]` correctly |
| S11 | 47–49 | "Types are shared, not invented per page" | **unsupported gloss** — see F1 |
| S12 | 50–51 | off-list/second type buys nothing | inference — labelled |
| P1 | 55–58 | `og:url` canonical, undecorated, aggregates likes | supported (3 spans) |
| P2 | 59–60 | one `og:type` per URL | supported |
| P3 | 61 | second `og:type` is a markup error | inference — labelled |
| P4 | 62–65 | image cache keyed by URL; new image → new URL | supported (2 spans) |
| P5 | 66–68 | missing tags → crawler heuristics | supported |
| P6 | 69–70 | incomplete page still produces a card | inference — labelled |
| P7 | 71–73 | debugger shows scraped tags/errors and triggers re-scrape | supported (2 spans) |
| P8 | 74–78 | sharing is URL-first; gzip+deflate required | supported (2 spans; context: "to be shared correctly by our crawler") |

## Findings by severity

- **LOW (unsupported gloss) — L47 "Types are shared, not invented per page."**
  The quoted support covers "shared", but S067 immediately after says "All
  other objects in the type system are CURIEs of the form …
  `my_namespace:my_type`" — namespaced types *are* invented per namespace.
  The framing denies a mechanism the source sanctions. Harm is low: the
  operative claim is the following labelled inference (off-list types buy
  nothing a platform must understand). Recommend "listed, not guaranteed"
  phrasing, or quoting the CURIE sentence.
- **NOTE (borderline, not a defect) — L32 "at the consumer"**: S067 says
  "should be treated as" without naming who treats; reading it as consumer
  behaviour is fair but is the only unquoted gloss of its kind.
- No missing, altered, or mis-attributed quotes; no inference presented as
  fact; no straight-quote substitution; the `verified-at` header matches the
  receipts byte-for-byte (timestamps 20:57:39Z/20:57:41Z, all status 200,
  S068 final URL = `developers.facebook.com/documentation/sharing/webmasters`).

## Residual risk / not verified

- I did not re-fetch ogp.me or the Facebook doc; freshness rests on the
  receipts (opened 2026-10-22, HTTP 200) — the entry itself warns the counter
  cannot see a page change.
- Registry rows in `corpus/SOURCES.md` and the lesson `## Gate` quotes are
  checked by the counter (L1 receipts 5/5 @ 24a1647), not re-run here.
- Out of scope per assignment: S069/S070 sections and the census lines
  (only their header references were sanity-checked).

## Tooling

None installed; Python 3 + git already present. No pacman transactions.
