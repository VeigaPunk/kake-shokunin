# FalsifyS021 — author-side FALSIFY wave, row S021 (round 26, C1, freshness)

Target: receipt `.ufo/waves/round-26/rechecks/S021.json` (verdict `HOLD`, `fetchIndex` 1) and the
SOURCES row `corpus/SOURCES.md:29` (teaches «Head placement matters; absolute URLs are recommended
while relatives work; the signal is not a selection guarantee», anchor «The rel=canonical link
element, Use rel=canonical link annotations, Best practices; updated 2026-07-10, opened
2026-10-20»).

Attacks run: (a) does the recorded quote ground *this* row's teaches, or only page chrome / a
neighbouring clause; (b) is the anchor *observed* location correct in the retained raw bytes; (c)
did content/version change in a way the receipt missed; (d) one plain GET of the row URL compared
against the retained text view.

Bounds respected: no subagent dispatch; no corpus/script/fleet/lane-Git mutation; only the one
documented plain public GET of the row URL (nothing saved); no round-24 material read, run,
rephrased or rerouted. No file was written outside this report (a scratch decompress to `/tmp` was
created once and deleted in the same command; a later `/tmp` path was never created).

## Verdict

**AGREE** — the `HOLD` verdict, the recorded quote, and the recorded anchor location are all
correct against the retained bytes *and* against the live page re-fetched today. No freshness
defect found. One immaterial imprecision in the receipt's prose `reason` (a supporting sentence that
belongs to a different method on the page) is recorded below as a low-severity note; it does not
change the verdict, the anchor, the quote, or any corpus byte.

## Evidence

### 1. Anchor as claimed in the receipt is correct in the retained raw bytes

Receipt `anchorObserved`: *"Text view single flattened line 1, offset 15071, inside H3 \"The
rel=\"canonical\" link element\" under H2 \"Use rel=\"canonical\" link annotations\"; footer \"Last
updated 2026-07-10 UTC\""*.

- Text view geometry (`fetched/text/S021-1.txt`, 21019 bytes): exactly one newline → one flattened
  content line; the quote starts at **character offset 15071**, line index 0 — the receipt's
  "line 1, offset 15071" is exact.
- Heading ancestry, parsed from the retained raw HTML (`fetched/S021-1.raw.gz`, `HTMLParser`,
  heading chain at the quote's paragraph): `h1 "How to specify a canonical URL with rel=\"canonical\"
  and other methods"` → `h2 "Use rel=\"canonical\" link annotations"` → `h3 "The rel=\"canonical\"
  link element"`. The receipt names exactly the h3 and h2 it says the quote sits inside. Raw
  landmarks: h2 `id="use-rel=canonical-link-annotations"` at raw line 4125, h3
  `id="rel-canonical-link-method"` at raw line 4158.
- The quote's own paragraph (raw lines 4209–4212) is body prose, not site chrome:
  `"Use absolute paths rather than relative paths with the rel=\"canonical\" link element. Even though
  relative paths are supported by Google, they can cause problems in the long run (for example, if
  you unintentionally allow your testing site to be crawled) and thus we don't recommend them."`
- The third declared anchor still exists as a heading in the raw bytes: raw line 3956
  `<h2 id="best-practices" data-text="Best practices">Best practices</h2>`.
- Footer raw line 4441: `<p>Last updated 2026-07-10 UTC.</p>` — matches the row's
  `updated 2026-07-10`.

### 2. The quote grounds this row's teaches (not chrome, not a neighbouring clause)

- Teach "absolute URLs are recommended while relatives work" — the quote is inside the *same
  paragraph* as the recommendation, and the recommendation is the sentence immediately preceding it
  (raw line 4209: *"Use absolute paths rather than relative paths with the rel=\"canonical\" link
  element."*), followed by *"and thus we don't recommend them"* (raw line 4212). Text view: the
  absolute-path clause at text offset ~15030, quote at 15071, same paragraph.
- Teach "Head placement matters" — raw lines 4223–4225: *"The rel=\"canonical\" link element is only
  accepted if it appears in the `<head>` section of the HTML, so make sure at least the `<head>`
  section is valid HTML."* (text offset 15423, in the same h3 section, after the quoted paragraph).
- Teach "the signal is not a selection guarantee" — page lead (raw line 3888): *"rel=\"canonical\"
  link annotations: A strong signal that the specified URL should become canonical."* plus the lead
  sentence *"you can indicate your preference using a number of methods"* (text offset ~6847). A
  "strong signal" is not a guarantee; the row's summary is a reading, not a quote — the same
  qualification the wave's own w1 report already states (`.ufo/waves/round-26/w1/RowS021.md`,
  caveat 5).
- Quote provenance is internally consistent with the corpus's own pinned citation: the row's
  used-by lesson quotes the same sentence verbatim at `corpus/lessons/round-22.md:44`
  (*"The rel=canonical link element: \"Even though relative paths are supported by Google, they can
  cause problems in the long run\""*), so the receipt reuses the corpus's pinned fragment rather
  than a different string.
- Quote uniqueness (amendment rule "a decided quote must not occur in any other population row
  text outside its document group"): `grep -cF "Even though relative paths are supported by
  Google" fetched/text/*.txt` → only `S021-1.txt:1`; every other text view returns 0.

### 3. No content/version change the receipt missed (live GET vs retained bytes)

One plain GET of the recorded row URL, same UA and header set as `fetch_sources.py`
(`kake-shokunin-source-recheck/26 (+GET only)`), response compared in memory against
`fetched/S021-1.raw.gz`:

```
live status 200 final https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
live headers {'content-type': 'text/html; charset=utf-8', 'last-modified': 'Fri, 10 Jul 2026 10:12:15 GMT',
              'etag': None, 'date': 'Wed, 21 Oct 2026 16:29:19 GMT', 'content-length': '194799'}
live bytes 194799 sha256 33d3101fddcc818d2fbff65bf549e8f3fc2558c8797ada1b076a2eb68b082aa2
retained bytes 194799 sha256 4edda778243cee4a2138fa31541226d22fc7be155a1ee385ce11a26674c7e5c5
live text len 20846 retained text len 20846 text identical: True
quote in live text: 15071
'only accepted if it appears in the <head> section' live: 15423 retained: 15423
'strong signal' live: 6847 retained: 6847
'Google will decide which pages' live: 16773 retained: 16773
'Last updated 2026-07-10 UTC' live: 20075 retained: 20075
'The rel="canonical" link element' live: 13274 retained: 13274
'Use rel="canonical" link annotations' live: 12713 retained: 12713
'Best practices' live: 4572 retained: 4572
```

- Extracted text views are **byte-identical** (20846 chars each) — no content change.
- The raw-byte sha256 difference is *not* content: a line-level diff of the 5236-line raw HTML
  shows only (i) reordering of two footer-promo `data-label`/`data-category` attributes, (ii)
  reordered JSON keys in the analytics `<script type="application/json">` blob, (iii) a rotated
  `<script nonce="…">` value, and (iv) one reordered static-asset URL tuple. No prose changed.
- `Last-Modified` is byte-identical to the retained manifest
  (`fetched/manifest.json`: `"last-modified": "Fri, 10 Jul 2026 10:12:15 GMT"`, `sha256
  4edda778…c7e5c5`, 194799 bytes) — the document version has not moved since the 2026-07-10 update
  and since the 2026-10-20 opening recorded in the row.
- Manifest record for the receipt's `fetchIndex` 1: `{"row": "S021", "index": 1, "status": 200,
  "finalUrl": …/consolidate-duplicate-urls, "fetchedAt": "2026-10-21T15:10:43.417148+00:00",
  "sha256": "4edda778…c7e5c5", "file": "S021-1.raw.gz"}` — the receipt's index resolves to a real
  population fetch, and the receipt file at the candidate revision is byte-identical to the
  working tree (`git show e28312b14b076584fedd696fae2a684e460bd11e:.ufo/waves/round-26/rechecks/S021.json`).

### 4. The committed receipt and row are unchanged at the candidate revision

```
$ git show e28312b1:.ufo/waves/round-26/rechecks/S021.json   # identical to working tree
$ git show e28312b1:corpus/SOURCES.md | sed -n '29p'
| S021 | Google Search Central: How to specify a canonical URL — https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls | docs | A | Google's documented HTML canonical signals and limitations | The rel=canonical link element, Use rel=canonical link annotations, Best practices; updated 2026-07-10, opened 2026-10-20 | Head placement matters; absolute URLs are recommended while relatives work; the signal is not a selection guarantee | mined | 2026-10-20 | 90d | corpus/knowledge/static-canonical-preflight.md, corpus/lessons/round-22.md |
```

The row's three declared anchors and the `updated 2026-07-10` stamp are all still present in the
live page (offsets 13274 / 12713 / 4572 and 20075 above), so no anchor drift and no version drift.

## Findings by severity

**none (freshness criterion)** — no actionable freshness defect.

**low (immaterial, does not change the verdict)** — the receipt's prose `reason` attributes the
sentence *"Google will decide which pages (if any) are duplicates"* to the framing of the
rel="canonical" method. That sentence is in the page's **h2 "Use a sitemap"** section (raw line
4265: *"All pages listed in a sitemap are suggested as canonicals; Google will decide which pages
(if any) are duplicates, based on similarity of content."*), i.e. it describes *sitemap inclusion*,
not the rel="canonical" annotation. The correct rel="canonical" grounding for the row's third
teach is the page lead (raw line 3888: *"rel=\"canonical\" link annotations: A strong signal that
the specified URL should become canonical."*). Because the lead says "signal" and the row says
"not a selection guarantee", the row's teach still holds, and the w1 row report
(`.ufo/waves/round-26/w1/RowS021.md`, caveat 5) already lists the three fragments without binding
the sitemap sentence to the method — so this is prose imprecision inside one receipt's `reason`
string, not a row-, anchor- or quote-level error. Minimal optional correction (NOT required for
the HOLD to stand, and not applied here because receipts/corpus are out of my write scope):
replace the parenthetical in `reason` with the lead wording, e.g. *"the method is framed as 'A
strong signal that the specified URL should become canonical' — a stated preference, not a
selection guarantee"*.

### Related finding already handled by the wave (consistency check, not a defect)

The row is `HOLD`, but the *statement* citing it in the knowledge entry was judged STALE and
already carries an appended EOF correction at `corpus/knowledge/static-canonical-preflight.md:186`
(*"[r26-recheck S021 STALE] Line 25's 'Cross-domain canonical is likewise not intrinsically
invalid' is not stated by S021 …"*) — consistent with the round-26 lesson
(`corpus/lessons/round-26.md:51-60`, which lists "S021 cross-domain attribution" among the STALE
corrections and explicitly rejects re-flagging "verification-date stamps (… S021)" and "S021
fragment wording"). A `HOLD` row receipt with a statement-level STALE correction is coherent; no
inconsistency to report.

## Residual risk / verification gaps

- The row's third teach ("the signal is not a selection guarantee") is an *interpretation* of
  "strong signal" / "indicate your preference"; the page contains no literal "guarantee" wording
  and does not itself say Google may pick a different canonical for a rel="canonical" annotation
  (that is row S022's separate claim, `corpus/SOURCES.md:30`). The receipt correctly flags this as
  interpretation-level in the w1 caveats; a stricter reader could require the row's teaches cell to
  name the lead/`Reasons to specify a canonical URL` section rather than the three declared anchors
  (the "strong signal" sentence sits in the h1 lead, above every declared anchor).
- S021 is a living documentation page (no pinned commit/tag). This HOLD certifies today's bytes
  only; the row's 90d cadence remains the appropriate guard, exactly as `w1/RowS021.md` caveat 9
  states.
- One comparison command of mine (character-level `difflib.SequenceMatcher` over the 194 KB raw
  HTML) exceeded its 300 s budget and was replaced by the successful line-level diff quoted above;
  no evidence depends on the abandoned command.
- I did not re-run `.ufo/waves/round-26/measure.py` (main-agent verification job); my checks are
  independent of the counter and used only the retained bytes plus one live GET.

## Tooling

No tool installs, upgrades or system changes were needed or performed for this row (no
`pacman`/`uv`/`cargo`/`npm` transaction, no new binary). All commands used Python 3 from the base
system and the wave's own `source_text.py` extractor, unchanged.

```json
{"target":"S021","verdict":"AGREE","severity":"none"}
```
