# Round 50, wave 1 — ScoutReopenS286

Scope: re-open the S286 source and class the frozen quote per the C1 instrument.
This is a leaf-seat scout report only; no lane state was mutated. The fetched
body lives at `/tmp/c50_s286.html` and was not written into the lane repo.

## Instrument baseline (counting commands, run verbatim)

C1 — `c50_quote_class.py`

- revision `9619af67c52939daac502ca7a24c9d714f3f51db` (base): `classed 0/3 met=False`
  - S273: class ledger absent, lesson absent
  - S274: class ledger absent, lesson absent
  - S286: class ledger absent, retained blob absent, lesson absent, no live
    registry row, entry absent
- revision `33eec7f2cecfdbb9c7a1f85c3d8efae8dacd7dd1` (pre-append):
  `classed 0/3 met=False`
  - S273: lesson absent
  - S274: lesson absent
  - S286: lesson absent, no live registry row, entry absent
  - (class ledger and retained blob now present for S286 — the pre-append
    mirror step landed; only the lesson/registry-row/entry append-side
    artifacts are missing)

C2 — `c50_durable.py`

- revision `9619af67c52939daac502ca7a24c9d714f3f51db`: `durable 0/1 met=False`
  - order proof absent; wave-cite proof absent; LOG.md at measured revision
    does not cite the wave; settlement absent

## Live re-fetch of the S286 source

One public GET, executed 2026-10-24:

```
curl -sS -L -o /tmp/c50_s286.html -w ... \
  'https://developers.google.com/search/docs/crawling-indexing/troubleshoot-crawling-errors'
```

- HTTP status: **200**
- Byte size (`size_download`, after redirects): **193271 bytes**
- Final URL: `https://developers.google.com/search/docs/crawling-indexing/troubleshoot-crawling-errors` (no cross-host redirect observed)

Frozen quote under test:

> `Googlebot will scale back its crawling if it detects that your servers are having trouble`

- **RAW substring of the fetched body:** YES — the 103-byte needle is present
  verbatim at byte offset ~143462 of the decoded body, inside
  `<li><a href="#availability_issues">Check that you're not running out of
  serving capacity</a>. Googlebot will scale back ... responding to crawl
  requests.</li>`. In the rendered page the sentence continues
  "…trouble responding to crawl requests." across a newline+indent; the
  frozen needle ends at "trouble" and does not span that whitespace.
- **Survives whitespace collapse** (body run through `' '.join(body.split())`
  before matching): YES.
- Surrounding context (verbatim slice):
  `...improve your site's crawling efficiency</a>.</li><li><a href="#availability_issues">Check that you're not running out of serving capacity</a>.\n  Googlebot will scale back its crawling if it detects that your servers are having trouble\n  responding to crawl requests.</li>`

## Derived class

**Class A — live-verbatim.** The frozen quote is a raw substring of a body
fetched fresh today from the canonical URL with a single GET; it also
survives whitespace collapse. No archive fetch, no redirect chain, no
normalization beyond whitespace needed. This is the strongest freshness
class and it corroborates the retained blob recorded by the pre-append
mirror (`S286` blob present at `33eec7f2`).

Note for the L1's verdict math: the C1 instrument at both revisions still
reports `met=False` for S286 — the missing pieces are the append-side
artifacts (lesson row, live registry row, entry), which are L1-owned files.
This report supplies the independent live-source evidence for the quote
itself; it does not close the instrument's gaps.

Report: .ufo/waves/round-50/w1/ScoutReopenS286.md
