# ReviewRetainedText — does the visible-text rule lose needed content? (r30 w1)

Seat: KakeR30.ReviewRetainedText (leaf). Date: 2026-10-22. Judged on: freshness.
Target: the four round-30 source snapshots `.ufo/waves/round-30/sources/S049..S052`
(.html.gz + retained .txt). Sandbox: `/fast/scratch/hyaku/kake-r30/w1/ReviewRetainedText/`.
No installs were needed; no live requests were made (saved snapshots only).

## Method
Copied the four snapshots into the sandbox and attacked them three ways, all with
Python 3 stdlib `html.parser` (convert_charrefs=True) plus direct greps:

1. Extracted `<main>`/`<article>` visible text and structured items (tables with
   per-cell text, `<pre>` blocks, callout blocks `class*=callout-block`, headings,
   inline `<code>`, `<img alt>`, `<ol>`) per source; checked each item against the
   retained .txt under (a) whitespace-collapsed exact match, (b) all-whitespace-removed
   match (glue detector), (c) per-cell/per-word split match.
2. Char-diffed every suspect row/callout against the actual .txt substring
   (difflib opcodes) to classify each mismatch as lost text vs inserted space.
3. Re-ran the fetcher's own `visible_text()` (copied `.ufo/waves/round-30/fetch_sources.py`)
   on each saved .html.gz and compared output and sha256 to the retained .txt and
   `receipts.json:textSha256`.

Key commands (all exit 0 unless noted):
- `python3 compare.py` (item presence; wrote `tmp/compare.json`)
- `python3 analyze2.py` (pre/ol/img-alt census; alt-in-txt checks)
- char-diff harness over `tmp/compare.json` rows/callouts (inline heredoc)
- `visible_text` replay: `rule(body)==retained` and sha match → True for S049-S052
- `grep -o 'curl -X PATCH…' S052.txt`, artifact counts `t.count(" ,")` etc.
Two early greps exited 1 (no-match): alt texts absent from .txt — that IS the finding.

## Headline
- The retained .txt is **exactly** the declared rule applied to the saved HTML:
  `visible_text(body) == <id>.txt` and sha256 == receipt `textSha256` for all four
  sources. The receipts are honest.
- **No word, number, table cell, sentence, heading, callout or code token is missing.**
  Every article sentence, all 9 tables (S049:1, S050:4, S051:1, S052:2 — 23 rows
  total), all 7 in-article callouts (S049:1, S050:1, S052:5), all headings and all
  3 `<pre>` blocks are present (split-match). Zero MISSING at every level tested.
- The rule replaces every tag with one space (`fetch_sources.py:40`
  `re.sub(r"(?s)<[^>]+>", " ", t)`), so nothing can run together; all my initial
  "RUNTOGETHER/glued" hypotheses dissolved under char-diff into *inserted* spaces.
- What the rule does lose or garble is below, per source.

## Per-source findings

### S049 (render.com/docs/static-sites)
- Table (Static site vs Web service compare?) and callout: intact.
- Missing: 1 `<img alt>` — "Selecting Static Site from the New menu" (absent from .txt).
- Garbled (cosmetic): 12 space-before-punctuation artifacts (` .` 8, ` ,` 3, ` :` 1).

### S050 (…/redirects-rewrites)
- Redirect/Rewrite table (3 rows) and header ("Action Description"): all words present,
  cells space-separated. Artifact only: rendered `…to /docs).` is retained as
  `…to /docs ).` (space injected by the closing `</code>` tag).
- Callout "You can't apply redirect/rewrite rules to your domain root." — intact,
  same artifact class ("(such as /blog , or even / ).").
- Missing: 1 `<img alt>` — "Setting redirect and rewrite rules in the Render Dashboard".
- Link targets dropped: 150 `<a href>` on page (mostly nav); in-article link
  "Rule matching and ordering" → `#rule-matching-and-ordering` (anchor only, low impact).
- 15 space-before-punctuation artifacts (` ,` 4, ` .` 5, ` )` 4, ` :` 2).

### S051 (…/static-site-headers)
- Path-pattern table (6 rows incl. header): all patterns and descriptions present,
  e.g. txt: `/blog/* Matches /blog/ , /blog/latest-post/ , and all other paths…` —
  rendered page has `/blog/, /blog/latest-post/,` (artifact, not glue).
- No images, no callouts. 136 hrefs dropped. 7 artifacts (` ,` 6, ` .` 1).

### S052 (…/custom-domains) — the one real garble
- DNS CNAME table: intact ("Name Value * Your service's onrender.com subdomain…" —
  the literal `*` cell survives, space-separated). Punycode/AAAA/CAA callouts: intact.
- **Garbled code example (copy-hostile, fact-preserving)** — the multi-line curl
  PATCH example is retained as ONE line with highlighted braces split by spaces:
  `curl -X PATCH https://api.render.com/v1/services/ { service-id } \ -H "Authorization: Bearer {api-key}" …`
  In the HTML the URL is `/v1/services/{service-id}` (prism `<span>` per brace);
  pasted from the .txt the URL and the `\` line-continuations are broken
  (`{ service-id }` spaced; ` \ -H` has the continuation backslash detached).
  Contrasting: `{api-key}` in the same snippet is NOT spaced — inconsistent fidelity.
  The CAA zone example retained cleanly: `example.com IN CAA 0 issue "letsencrypt.org" …`.
- Missing: all 6 `<img alt>`s — "Adding a custom domain in the Render Dashboard",
  "Added custom domain with DNS update needed" (×2), "Verified domains in the Render
  Dashboard", "Disabling the onrender.com subdomain", "Wildcard Custom Domain with
  DNS update needed". These describe the screenshots; the .txt has no trace.
- Ordered lists: 5 `<ol>` in the article; CSS-generated step numbers (1. 2. 3.) are
  absent — order survives only by sequence.
- Code-block chrome noise: `plaintext Copy to clipboard` appended after the curl body.
- 29 space-before-punctuation artifacts (` ,` 6, ` .` 14, ` )` 7, ` :` 2). 175 hrefs dropped.

## Cross-cutting facts
1. Attribute-only content is invisible to the rule by construction: 8 img alts,
   31 aria-labels (9/7/7/8), and every href (184/150/136/175) are absent. Alts are
   the only ones I'd call needed content (they describe the evidence screenshots).
2. S052's three `<pre>` examples sit AFTER `</main>` and `</article>` in the raw
   HTML (byte offsets: article ends 132,757; main 135,858; pres at 143,629/146,381/
   149,584 of 371,923). A reviewer who restricts parsing to main/article would
   wrongly report the curl and CAA examples as lost; the whole-page rule catches them.
3. Entities decode correctly (ëxample.com, xn--xample-ova.com present; no `&quot;`
   leakage anywhere in the four .txt).

## Judgment for the C2 retained-text claim
The retained bodies lose no textual fact on these four pages; quotes taken from the
.txt are exact substrings under the receipt's stated rule. Needed-content risk is
concentrated in: (a) the S052 curl example, unusable if copied from the .txt — quote
it from the .html.gz instead; (b) screenshot alt descriptions, absent — anyone citing
"what the screenshot shows" must go to the HTML. Both are cheap to note in the
knowledge file if a quote ever leans on them.

## Not verified / residual
- Rendered-page text beyond the SSR snapshot (JS-hydrated deltas) — out of scope, no
  live requests allowed for this seat.
- Whether the knowledge file `corpus/knowledge/render-static-sites.md` actually quotes
  any garbled region — I did not audit its quotes against the .txt (another seat's lane).
- The regex `<script|style>` strip could theoretically over/under-strip nested edge
  cases; none observed here (token streams matched the rule exactly, and article
  content showed no stray script text).
- Artifact counts (` .` etc.) include a few emphasis/link boundaries, not only code
  spans; treat them as upper bounds of the code-span artifact class.

## Artifacts (sandbox, absolute paths)
- `/fast/scratch/hyaku/kake-r30/w1/ReviewRetainedText/compare.py` (item extractor+checker)
- `/fast/scratch/hyaku/kake-r30/w1/ReviewRetainedText/analyze2.py` (pre/ol/alt census)
- `/fast/scratch/hyaku/kake-r30/w1/ReviewRetainedText/tmp/compare.json` (full results)
- decompressed `S049..S052.html` + copied .txt/.html.gz/receipts.json in the same dir
