# ScribeS432QuoteFix — round-62 w1 (advisory)

## Assignment

Leaf seat, no subagent dispatch. Draft an append-only correction paragraph for
`corpus/knowledge/response-header-expectations.md` that replaces the
verifier-rejected generic S432 lead-in with a located substantive quote; verify the
quoted span in the committed S432 body; explain claim limits; do not edit lane
files. Report-only output. I did not alter the claim, the frozen counter, the
criteria, the lesson, `SOURCES.md`, or any score.

## Lane state observed before any work

- `git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse --show-toplevel` →
  `/home/vgpnk/Projects/shokunin/kake-shokunin`
- `HEAD` → `c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13` (the contract base)
- `git status --porcelain` → only `?? .ufo/waves/round-62/` (untracked wave data)
- Frozen counter sha256:
  `ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d`
  (matches the ticket's freeze)
- Base control re-run (read-only; counter reads committed blobs only):

```
python3 -B .ufo/waves/round-62/c62_calibration.py --root . \
  --revision c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13
revision=c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13 disagreements=1 unresolved=1 \
quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false
exit=1
```

This reproduces the ticket's pre-wave base-control exactly (`unresolved=1
quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false`, exit 1).
`disagreements=1` is the single S432 `Disagree` row at
`corpus/lessons/round-61-verifier-spotcheck.md:33`
(`grep -c Disagree` on the committed blob → `1`).

## Verification of the quoted span in the committed S432 body

Retained body: `.ufo/waves/round-61/sources/S432.html` at `HEAD`.
Committed sha256 `63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b`,
18,914 lines. `receipts.json` binds id S432 to the same sha256, 1,854,393 bytes,
fetched `2026-10-27T09:14:55Z`, user agent `round61`.

Located structure (`git show HEAD:.ufo/waves/round-61/sources/S432.html | nl -ba`):

| Line | Content |
|---|---|
| 6149 | `<h3 … data-level="3.6" id="x-content-type-options-header">` |
| 6150 | `<p>The` |
| 6151 | `` `<dfn … id="http-x-content-type-options"><code>X-Content-Type-Options</code></dfn>` `` |
| 6152 | `response <a …>header</a> can be used to require checking of a <a …>response</a>’s` |
| 6153 | `` `<code>Content-Type</code>` <a …>header</a> against the <a …>destination</a> of a `` |
| 6154 | `<a …>request</a>.` |
| 6156 | `</p>` |

Normalization test (tags stripped, backtick wrappers dropped, whitespace collapsed):

```
NORMALIZED: '3.6. X-Content-Type-Options header The X-Content-Type-Options response
header can be used to require checking of a response’s Content-Type header against the
destination of a request.'
QUOTE_SUBSTRING: True
RAW_CONTAINS_QUOTE: False
ASCII_APOSTROPHE_QUOTE: False
```

So the frozen counter's `QUOTE` string is present in the *running text* of the
§3.6 opening paragraph, spanning the sentence words at lines 6151–6154 (the
contract's citation is exact for the sentence; the enclosing `<p>` opens at 6150
and closes at 6156). It is **not** a byte-contiguous slice of the retained HTML:
line 6152 splits `… of a` from `response’s`, and the code elements carry backticks
and newlines. The apostrophe in the source is U+2019 (`’`), which is what the
frozen counter's `QUOTE` uses; an ASCII-apostrophe variant does not occur.

The rejected lead-in is at line 6183 (`Web developers and conformance checkers
must use the following`), and it introduces the ABNF production at line 6187
(`X-Content-Type-Options = "nosniff" ; case-insensitive`). The `nosniff`-only
claim therefore comes from lines 6158–6181 (`determine nosniff`, ASCII
case-insensitive comparison at 6174–6175) plus 6183–6187, not from the
substantive sentence. The verifier's characterization of the lead-in as generic
is sustained by the body's own placement.

## Draft (append-only; NOT applied by this seat)

Append after the current final line of
`corpus/knowledge/response-header-expectations.md` (216 lines, ends with `\n`).
First appended line is `[r62-correction 2026-10-27]`, which matches
`append_guard.py`'s `TAG_RE` (`\[r[0-9]+-correction [0-9]{4}-[0-9]{2}-[0-9]{2}\]`)
and the round-60 tag criterion; the append is at EOF, which `append_guard.py`
already allows untagged, so the tag is house style rather than a gate need.
The quote must stay on **one physical line**: the counter tests a substring, so
markdown soft-wrapping the blockquote would break `quote_correction`.

```markdown
[r62-correction 2026-10-27]

## Round-62 correction — the S432 §3.6 sentence is quotable in full

Supersedes the two short spans quoted under `xcto_nosniff_value` above. The
second of them — “Web developers and conformance checkers must use the
following” — is a generic lead-in: in the retained body it opens the sentence
that introduces the ABNF value block (`.ufo/waves/round-61/sources/S432.html`,
line 6183, leading to the production at line 6187), so it says nothing about
what the field does and cannot ground a response-header expectation. The
round-61 non-author verifier sustained that objection
(`corpus/lessons/round-61-verifier-spotcheck.md`, S432 `Disagree` row, line
33). The first span, “can be used to require checking of a”, is not generic
but stops mid-sentence at a markup boundary.

The same S432 §3.6 body carries the substantive sentence in its opening
paragraph: heading line 6149 (`data-level="3.6"`,
`id="x-content-type-options-header"`), paragraph lines 6150–6156, sentence
words at lines 6151–6154. Its subject is `The X-Content-Type-Options`, whose
field name is the `<dfn>` code element on line 6151; the quoted span begins
after it, at `response header`. Read as running text, the sentence is:

> "response header can be used to require checking of a response’s Content-Type header against the destination of a request"

The span is a transcription of the rendered sentence, not a byte-contiguous
slice of the retained HTML: the field name on line 6151 sits in a `<dfn>`
node, `response` and `request` on lines 6152–6154 are link nodes, and the code
elements are wrapped in backticks, so a raw search of the body for the quote
returns no match. Normalising the paragraph — tags removed, backtick wrappers
dropped, whitespace runs collapsed to one space — yields the sentence
contiguously, and the quote above is that normalised running text, checked
against sha256 `63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b`
at 1,854,393 bytes, the retained body named in the front matter. The line
numbers are pinned to those bytes; a later revision may move them.

What the sentence grounds: the field's declared job is to have a recipient
check the response's `Content-Type` against the destination of the request.
That is a statement about the field's effect, which is what the
`xcto_nosniff_value` class reads. What it does not ground: that the field's
only value is `nosniff` (that comes from the ABNF production at line 6187 and
the `determine nosniff` algorithm at lines 6158–6181, including the ASCII
case-insensitive comparison at lines 6174–6175); that any surface sets the
field; that a browser will behave in a particular way; or anything about a
property's live headers. The entry's policy stays bounded to the
Fetch-defined `X-Content-Type-Options` field; this appendix changes no source
row and no verifier record, and the superseded prose above is left in place.
```

## Checks run on the draft (scratch simulation, no lane write)

Concatenated `base + "\n" + draft` in
`/fast/scratch/hyaku/kake-r62/ScribeS432QuoteFix/` and asserted:

```
QUOTE_in_merged: True
QUOTE_on_one_line: True
S432_section: True
Round62_correction: True
old_generic_kept: True
old_truncated_kept: True
base_lines_ordered_subsequence: True (217/217)
tag_line: '[r62-correction 2026-10-27]' matches: True
```

This is a simulation of the counter's `correction` expression
(`QUOTE in knowledge AND "S432 §3.6" in knowledge AND "Round-62 correction" in
knowledge`) plus an append-only line check. It is **not** a run of the frozen
counter against a commit, and no score is implied.

## Counter-compatibility facts for the integrating seats

Read off the frozen `c62_calibration.py` (no predicate changed):

- `corpus/knowledge/response-header-expectations.md` must contain, in the
  committed blob: the exact one-line `QUOTE`, `S432 §3.6`, and
  `Round-62 correction`.
- `corpus/QUALITY.md` must contain `substantive located quote` and
  `round-61-verifier-spotcheck.md` (the criterion seat's surface).
- `corpus/lessons/round-62.md` must contain `## Gate`, `S432`, `Agree`, `Reject`
  (the lesson seat's surface; the file does not exist at base).
- `corpus/SOURCES.md` must keep the `| S432 |` row; it does at base
  (line 178) and the draft does not touch it.
- `unresolved` is derived from the spot-check blob's S432/`Disagree` line count,
  so the verifier record must be preserved verbatim; the draft preserves it and
  cites it.

## Findings and limits

1. **The quote is normalized text, not a raw byte slice.** `RAW_CONTAINS_QUOTE:
   False`. Any later counter or verifier that greps the HTML for the quote must
   apply the same normalization (strip tags, drop backticks, collapse
   whitespace); a raw grep will return 0 and could be mistaken for drift.
2. **Line numbers are body-specific.** They hold for sha256
   `63b0a018…bad911b` (1,854,393 bytes). A live re-open this round (user agent
   `round62-recheck`, no receipt written, `curl` over https) returned
   1,839,728 bytes — a different byte count from the retained body — yet the
   same normalized sentence occurs exactly once and sits inside the
   `id="x-content-type-options-header"` §3.6 section. I use that only as
   corroboration that the citation has not drifted; it is **not** receipted
   evidence and must not be cited as such. The draft deliberately cites the
   committed, sha256-pinned body only.
3. **The rejected lead-in is generic for a locating reason, not a taste
   reason.** It sits at 6183 and introduces the ABNF at 6187; that placement is
   the argument the draft carries.
4. **Scope stays bounded.** The draft grounds only the field's declared effect.
   It explicitly withholds the `nosniff`-only claim (sourced separately at
   6183–6187/6174–6175), any per-site claim, any browser-behavior claim, and any
   claim about live headers.
5. **Append-only is preserved.** The old prose, both old span quotes, the source
   row and the verifier row are untouched; the correction supersedes by
   reference. Heading level `##` keeps it a sibling of the entry's top sections
   rather than nesting under `## Limits`.
6. **S432 row is not rejected or edited.** `corpus/SOURCES.md:178` remains the
   tier-A mined row with the 180d recheck.

## Out of scope / not done

- No edit to any lane file; no git/jj mutation; no commit; no scoring run
  against a new revision; no change to the claim, counter, criteria or lesson.
- I did not draft the QUALITY criterion or the round-62 lesson gate (other
  seats). The counter-compatibility facts above are provided so those surfaces
  can be checked without re-deriving them.
- No pacman transactions and no installs; nothing was needed.
- Scratch `/fast/scratch/hyaku/kake-r62/ScribeS432QuoteFix/` was created for the
  base copy and draft validation and deleted before yield. The durable draft is
  the fenced block above.

## Artifacts

- This report: `.ufo/waves/round-62/w1/ScribeS432QuoteFix.md`
  (written at `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-62/w1/ScribeS432QuoteFix.md`)
- Source verified: `.ufo/waves/round-61/sources/S432.html` at `HEAD`
  (sha256 `63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b`)
- Rejected quote record: `corpus/lessons/round-61-verifier-spotcheck.md:33`
- Target of the draft: `corpus/knowledge/response-header-expectations.md`
  (216 lines at `HEAD`, append at EOF)
