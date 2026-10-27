# ScribeCorrectionReview — skeptical-editor review of the round-63 correction block

Seat: `ScribeCorrectionReview` (leaf, read-only). Round 63, wave 1.
Measured commit under review: `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`; base
`13d4519818db28cd0aa912e49020659140d7b9fa`.

## Target

`/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/response-header-expectations.md`
lines 222–250 (heading `## Round-63 correction — S432 field-purpose span admitted
as collapsed-only`, tag `[r63-correction 2026-10-27]`). The file was **not edited**.

## Verdict

The block's factual substrate verifies: the quoted span, both digests, the
`collapsed-only` derivation, the ledger contents, rendering reproducibility, the
4/4 selftest at the lane root, append-only no-harm, and "no registry cell changed"
all re-derive from committed bytes. There are **8 concrete defects** — none
falsifies the admitted quote or moves the class, but four of them (D1, D2, D5, D6)
would mislead a reader who tries to re-derive the claim from the block alone, and
three (D3, D4, D7) are provenance/precision overstatements. Two observations below
are cross-file inconsistencies the block inherits rather than creates.

## Evidence — commands run and outputs

All read-only; no git/jj mutation anywhere; cwd `/home/vgpnk/Projects/shokunin/kake-shokunin`.

1. Digests of the artifacts the block names:
```
$ sha256sum .ufo/waves/round-63/quote-class/S432.txt .ufo/waves/round-61/sources/S432.html \
    .ufo/waves/round-63/quote-class/quote-classes.json scripts/quote_class.py .ufo/waves/round-63/c63_calibration.py
8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69  .ufo/waves/round-63/quote-class/S432.txt
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  .ufo/waves/round-61/sources/S432.html
5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d  .ufo/waves/round-63/quote-class/quote-classes.json
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  scripts/quote_class.py
bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91  .ufo/waves/round-63/c63_calibration.py
```
   Both digests printed in the block (lines 233–236) match byte-for-byte; the tool
   and counter shas match the contract and the measured-revision blobs
   (`git show 05b0d7f:scripts/quote_class.py | sha256sum` → same
   `431e75e8…1f14`; same for `S432.txt`, `S432.live.html`, `quote-classes.json`).

2. Substring facts (line 232–237 claim):
```
in_txt True
in_raw False
txt_char_offset 100584   (S432.txt is one line, 286 933 chars)
```
   `S432.html` does contain `response’s` and `destination</a> of a`, but not the
   span as a byte sequence — the span crosses `<a>…</a>`/`<dfn>…</dfn>` markup.

3. Line range 6150–6154 (line 225–226 claim): `sed -n '6145,6160p'
   .ufo/waves/round-61/sources/S432.html` maps 6149 = `<h3 … data-level="3.6"
   id="x-content-type-options-header">`, 6150 = `   <p>The`, 6151 = `<dfn …><code>X-Content-Type-Options</code></dfn>`,
   6152 = `response <a…>header</a> can be used … response</a>’s`, 6153 = `` `Content-Type` `` …
   `destination</a> of a`, 6154 = `<a…>request</a>.`. The cited range is exact.

4. Quote identity: the block's blockquote at line 230 is **byte-identical** (152
   chars each) to `quote-classes.json` `classes[0].quote`; both carry U+2019 in
   `response’s`, backticks around the two field names, and the terminal period.
   It is also the `FROZEN_QUOTE` in `.ufo/waves/round-63/c63_calibration.py:51-55`.

5. Class derivation and tool (line 240–242 claim), run from the lane root:
```
$ python3 -B scripts/quote_class.py --selftest
case inline_raw_substring: derived=raw-substring expected=raw-substring pass
case markup_collapsed_only: derived=collapsed-only expected=collapsed-only pass
case absent_everywhere: derived=absent expected=absent pass
case s432_real: derived=collapsed-only expected=collapsed-only pass
selftest 4/4        (exit 0)
$ python3 -B scripts/quote_class.py classify --quote "<the block's span>" \
    --raw .ufo/waves/round-61/sources/S432.html --text .ufo/waves/round-63/quote-class/S432.txt
derived=collapsed-only   (exit 0)
```
   Same result from a foreign cwd, however, fails — see D5.

6. Rendering reproducibility (implied by line 238–240): re-running the cited recipe
   reproduces the committed rendering byte-exactly:
```
$ python3 -B .ufo/waves/round-63/quote-class/extract_text.py \
    --raw .ufo/waves/round-61/sources/S432.html --out /tmp/r63-scribe-S432.txt
extracted 1854393 bytes -> 286933 chars
8b90d096…2a69  /tmp/r63-scribe-S432.txt
8b90d096…2a69  .ufo/waves/round-63/quote-class/S432.txt
```
   (temp file deleted; `extract_text.py --selftest` prints `selftest 1/1`).

7. Registry (line 249–250 claim): `git diff <base> <measured> -- corpus/SOURCES.md | wc -l`
   → `0`. Row `corpus/SOURCES.md:178` is identical at base and measured:
   `… | X-Content-Type-Options nosniff value rule | Section 3.6 X-Content-Type-Options
   header and its value ABNF; … | The field has one defined value, nosniff, … | mined | 2026-10-27 | 180d | corpus/knowledge/response-header-expectations.md |`.

8. Append-only / no-harm: `git diff --stat <base> <measured>` for the knowledge
   file is `+29 −0`; the file's digest is identical at measured and in the worktree
   (`a4f0f228…31cb`). Later commits (`7f77d12b`, `15eb965c`) touch only the two
   after-receipts and the w1 spec/dispatch, not this file.

9. Earlier spans (line 245–246 claim): the `xcto_nosniff_value` section (lines
   69–91) carries exactly two blockquotes — `"can be used to require checking of a"`
   (line 78) and `"Web developers and conformance checkers must use the following"`
   (line 80) — matching "fragment ending before its object" and "generic lead-in".

10. Round-62 criterion (line 243–244 claim): `corpus/QUALITY.md:1412` exists at
    base, says "keep a field's purpose separate from claims about its exact value or
    algorithm", and its falsifier ("does not identify the `X-Content-Type-Options`
    response header or its check of `Content-Type` against request destination, or
    the `nosniff`-only claim is attributed to that purpose sentence") is passed by
    the admitted span. Consistent.

## Defects

### D1 — First sentence inverts the agency of the resolution (line 224)
Text: "The round-62 held correction above resolves this round."
The round-62 correction resolves nothing: `corpus/knowledge/response-header-expectations.md:220`
ends "…the S432 disagreement remains open. The row stays mined for the field's
separately supported value rule; no registry cell changed." The entity that does
the resolving is *this round's* correction (`corpus/lessons/round-63.md:63`: "it is
resolved by this round's correction"). As written, a reader takes the r62 held
correction as the resolver, which is the opposite of its own last sentence.
Fix: "The round-62 held correction above is resolved this round." (or "The
correction below resolves it.").

### D2 — "its two retained blobs" is false for the text blob (line 227)
Text: "classed by derivation from its two retained blobs".
Only one blob is retained from the source round: `.ufo/waves/round-61/sources/S432.html`.
The other, `.ufo/waves/round-63/quote-class/S432.txt`, did not exist before this
round; it is a **derived rendering** produced by `.ufo/waves/round-63/quote-class/extract_text.py`
(the block's own next clause says so, lines 238–239) and is reproducible byte-exactly
(evidence 6). Calling it "retained" overstates the independence of the derivation: a
class computed against an artifact authored in the same round is weaker evidence than
S273/S274, whose `.txt` blobs predate the classing. The class can still be right (it
is, and the S273 precedent has the identical shape: `S273 in raw False`, `S273 in text True`),
but the sentence's adjective is wrong.
Fix: "classed by derivation from the retained HTML and its committed flat-text rendering".

### D3 — The cited rule's wording does not support the derivation as written (line 228)
Text: "under the round-50 quote-class rule (`corpus/QUALITY.md`)".
`corpus/QUALITY.md:1102` defines the class as "a span that survives only whitespace
collapse". The admitted span does **not** survive whitespace collapse alone — the raw
body must have its inline markup removed:
```
$ python3 -c '<collapse whitespace of S432.html; test span>'  → whitespace-collapse-only contains span: False
```
The operational round-50 rule that does support it is R2 in
`.ufo/waves/round-50/c50_quote_class.py:16-18`: "collapsed-only when it is a substring
of the text blob only", which is exactly what `scripts/quote_class.py:32-37` and the
C1 counter's inline `classify` (`c63_calibration.py:59-67`) implement. So the label is
correct lane practice and matches the S273 precedent, but the block cites the prose
summary whose literal test fails while omitting the operational definition that passes.
Fix: cite the operational rule (c50 R2 / the round-63 tool's three-way test) or say
"the flat-text rendering's match" instead of "whitespace collapse".

### D4 — "textContent semantics" misdescribes the recipe (line 239)
`extract_text.py` does three things real DOM `textContent` does not: it skips
`script`/`style`/`noscript` (`extract_text.py:27,37-38,46-48,52-54`), it inserts
newline boundaries for block elements (`:21-26,39-40,49-50`), and it collapses every
whitespace run to one ASCII space (`:56-57`). A reader checking the claim "textContent
semantics" against the DOM will find a mismatch on all three. The recipe's own
docstring uses the same phrase, so the block is faithfully repeating its source; the
phrase is still inaccurate as a description a third party can rely on.
Fix: "textContent with script/style dropped, block boundaries, and whitespace collapsed".

### D5 — "selftest 4/4" is not reproducible without a cwd qualifier (lines 240–241)
The tool resolves its fixtures against `Path.cwd()` (`scripts/quote_class.py:24-25,79-80`),
which the contract records as a deliberate freeze note
(`.ufo/waves/round-63/contract.md:58-60`: "binds fixture resolution to the invoking
cwd (the lane root)"). From any other directory the claim fails:
```
$ cd /tmp && python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/quote_class.py --selftest
case inline_raw_substring: derived=unevaluable expected=raw-substring FAIL
… (four cases) …  selftest 0/4     (exit 1)
```
The block states "selftest 4/4" as an unconditional fact. A reader following the
block alone will very likely run it from elsewhere and conclude the block overclaims.
Fix: "(selftest 4/4 when run from the lane root; real case `s432_real`)".

### D6 — "with its existing scope" conflates cell-unchanged with scope-adequate (line 250)
"No registry cell changed" is true (evidence 7). "The S432 row stays `mined` with its
existing scope" is the risky half: `corpus/SOURCES.md:178` scopes the row as
"X-Content-Type-Options **nosniff value rule**", its description as "The field has
**one defined value, nosniff**", and the r62 correction (`…expectations.md:220`) spells
that out — the row "stays mined for the field's **separately supported value rule**".
The span now admitted is a **field-purpose** statement (the block says so two lines
earlier, 242–244), which that scope text does not name. A reader can therefore take
"existing scope" as confirmation that the row already covered the purpose proposition,
which the row's own cells deny. Since the contract forbids touching the row, the block
is the only place this can be said correctly.
Fix: "No registry cell changed; the S432 row stays `mined`, still scoped to the
nosniff value rule (`corpus/SOURCES.md:178`), and does not itself register the purpose
statement admitted here."

### D7 — The live-GET clause rests on an uncited record (lines 247–249)
"one GET of https://fetch.spec.whatwg.org/ on 2026-10-27 returned a body byte-identical
(sha256 `63b0a018…911b`) to the round-61 retained body."
Byte-identity is verifiable and correct — `.ufo/waves/round-63/sources/S432.live.html`
hashes to the full `63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b`
at 1 854 393 bytes, and the block's truncated `63b0a018…911b` is a correct 8+4
abbreviation. What is **not** re-derivable from the block is the process claim: "one
GET", the date, and the implicit status rest only on the lane's own lesson
(`corpus/lessons/round-63.md:53-55`: "one GET, HTTP 200, 1,854,393 bytes"). No request
receipt (status line, headers, fetch timestamp) is committed, and the block names
neither the live blob nor the lesson. So the clause asks the reader to trust an
author-side record for exactly the part that is not checkable from bytes.
Fix: cite `.ufo/waves/round-63/sources/S432.live.html` (sha + byte count) and mark the
"one GET / 2026-10-27" part as the lesson's record, not as an independently verified fact.

### D8 — "the proposition the section attributes to S432" has no single referent (lines 242–243)
The `xcto_nosniff_value` section attributes **two** things to S432: the purpose
statement (line 70, "gives the field its purpose in the response-processing steps") and
the value rule (lines 83–88, "one production whose only permitted value is the literal
`nosniff`"). The block's own parenthetical then says the span is "kept separate from
the `nosniff`-only value rule" — i.e. it does *not* state the section's headline
proposition. A skeptical reader can read the sentence as claiming the span grounds the
value rule, which the parenthetical contradicts. Name the proposition: "substantively
states the field-purpose proposition the section already attributes to S432 (line 70),
kept separate from the `nosniff`-only value rule".

## Observations (not counted as defects)

- **Line-range citations for the same span disagree across the corpus.** This block
  says 6150–6154 (correct for the sentence: `The` at 6150 … `request</a>.` at 6154),
  the r62 correction at `…expectations.md:220` says 6150–6156 (includes the blank line
  and `</p>`), and `corpus/QUALITY.md:1412` says 6151–6154 (starts at the code element).
  The block is the most precise of the three; a reader moving between them sees three
  ranges for one span.
- **The section body is not forward-linked to the correction.** Lines 69–91 still
  present the two short spans as the evidence and assert "the quotable pieces are short"
  (lines 74–77). Appending is this lane's correction convention (the r62 correction does
  the same), so this is a residual navigation risk rather than a violation: a reader who
  reads only the section reaches the false conclusion that no full-sentence quote exists.
  Worth one clause in the block: "(the section's 'quotable pieces are short' applies to
  raw substrings only)".

## Claims checked and verified as stated

| Block line | Claim | Verification |
|---|---|---|
| 225–226 | span is Fetch §3.6, retained body `S432.html:6150–6154` | line map, evidence 3 |
| 230 | quoted span | byte-identical to ledger quote, evidence 4 |
| 232–234 | substring of `S432.txt`, sha `8b90d096…2a69` | evidence 1, 2 |
| 234–236 | not substring of retained HTML, sha `63b0a018…911b` | evidence 1, 2 |
| 236–237 | derived class `collapsed-only` | evidence 5 |
| 238–240 | class, both digests, recipe recorded in `quote-classes.json` | ledger has `matchClass`, `textSha256`, `rawSha256`, `recipe` (`quote-classes.json` classes[0]); recipe reproduces the blob, evidence 6 |
| 240–242 | re-derivable by `scripts/quote_class.py`, selftest 4/4, case `s432_real` | evidence 5 (at lane root; see D5) |
| 243–244 | kept separate from `nosniff`-only value rule per r62 criterion | `QUALITY.md:1412`, evidence 10 |
| 245–246 | two earlier spans, historical, ground nothing | evidence 9 |
| 249 | no registry cell changed | evidence 7 |
| 250 | S432 row still `mined` | evidence 7 (scope wording: D6) |

Also read but not re-executed: `.ufo/waves/round-63/controls/after-c1.txt`
(`… derived=collapsed-only class_match=1 … met=true`, exit 0). The C1 counter was
not re-run for this review.

## Lane compliance

- Wrote only this report; the reviewed file was not edited; no change to any frozen
  claim, counter, receipt, ledger, registry, `.ufo/state`, `scripts/` or `templates/`.
- No git/jj mutation, no commits, no push, no subagent dispatch, no fixture repo
  created, no `pacman`, no tool installs, no PATH writes.
- One temp file `/tmp/r63-scribe-S432.txt` (286 933 bytes) created for the rendering
  reproduction and deleted in the same command.

## Artifacts

- Report: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/w1/ScribeCorrectionReview.md`
- Reviewed: `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/response-header-expectations.md:222-250`
- Evidence: `corpus/SOURCES.md:178`, `corpus/QUALITY.md:1100-1108,1410-1412`,
  `corpus/lessons/round-63.md:53-65`, `.ufo/waves/round-63/quote-class/quote-classes.json`,
  `.ufo/waves/round-63/quote-class/extract_text.py`, `scripts/quote_class.py`,
  `.ufo/waves/round-63/c63_calibration.py:51-67,118-150`,
  `.ufo/waves/round-63/controls/after-c1.txt`, `.ufo/waves/round-63/contract.md:51-63`
