# ScribeSourceGate — S432 reopen, registry-free citation, exact Gate pointer

Seat: leaf scribe (advisory). Item: verify S432 was opened this round, that the correction
can cite S432 without adding a `SOURCES.md` row, and draft a Gate pointer at the exact source
location. No lane files, claims, counter, criteria or score were altered; every write below
happened in `/fast/scratch/hyaku/kake-r62/ScribeSourceGate/` (fixture + drafts), now deleted.

## 1. S432 was opened this round — supported, with one provenance gap

Live reopen performed by this seat on 2026-10-27 through `curl` (system binary, no installs):

```
$ curl -sS -D headers.txt -o live.html --max-time 60 https://fetch.spec.whatwg.org/
$ head -3 headers.txt
HTTP/2 200 
server: nginx/1.10.3
date: Tue, 27 Oct 2026 11:59:08 GMT
content-type: text/html; charset=utf-8
content-length: 1854393
$ sha256sum live.html
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  live.html
```

Pinned body is byte-identical to that response:

```
$ sha256sum .ufo/waves/round-61/sources/S432.html
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  .ufo/waves/round-61/sources/S432.html
$ wc -l .ufo/waves/round-61/sources/S432.html
18914 .ufo/waves/round-61/sources/S432.html
```

`.ufo/waves/round-61/sources/receipts.json` S432 entry: `url`/`effectiveUrl`
`https://fetch.spec.whatwg.org/`, `status` 200, `sha256` `63b0a018…bad911b`, `bytes` 1854393,
`fetchedAt` `2026-10-27T09:14:55Z`, `userAgent` `round61` — the pinned hash and byte count match
both the receipt and today's response.

**Gap (reported, not fixed).** `.ufo/waves/round-62/` contains no receipt or open-log artifact;
its contents are `c62_calibration.py`, `contract.md`, `w1/`, `w1-dispatch.json`, `w1-spec.json`,
`w1.ready`, `w1.ready.partial`. The wave's "opened this round … HTTP 200 from the web reader"
therefore rests on contract prose plus this seat's independent GET. Any lane text that asserts a
round-62 fetch receipt would be unbacked; either cite `contract.md` §Source grounding, or name this
seat's GET (channel `curl 8.23.0`, 2026-10-27T11:59:08Z, HTTP/2 200, sha256 as above). Because the
bytes are identical, the correction's citation of the pinned body is unaffected either way.

## 2. The correction needs no new `SOURCES.md` row

`corpus/SOURCES.md:178`:

```
| S432 | WHATWG Fetch — https://fetch.spec.whatwg.org/ | spec | A | X-Content-Type-Options nosniff value rule | Section 3.6 X-Content-Type-Options header and its value ABNF; WHATWG Living Standard accessed 2026-10-27 | The field has one defined value, nosniff, compared ASCII case-insensitively against the split field values, so a recorded value of anything else is outside the value rule | mined | 2026-10-27 | 180d | corpus/knowledge/response-header-expectations.md |
```

Row covers URL, §3.6, tier A, status `mined`, opened 2026-10-27, recheck 180d, `used-by` the entry
being corrected. Frozen counter needs only `"| S432 |" in SOURCES` (`source_row`), which this row
supplies; the counter-tested after-state (§5) leaves `corpus/SOURCES.md` untouched and still reports
`source_row=1`. Census unchanged:

```
$ ./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake
… 16 × W04 (incl. S433) … kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md   exit 0
$ ./scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kake
kake	rows	171
```

No E03 (duplicate id) for S432, no E11 (missing `used-by`). Adding a second row would move the 171
count and risk E03/E04 for no gain.

**Caveat (counter gap, §6.2):** `source_row` is presence-only. Marking the row `rejected` still
scores `met=true` (probe P4), so "kept, not rejected" is a reviewer check, not a counter check.

## 3. Exact source location — quote is unique, but not byte-contiguous in the HTML

`§3.6` paragraph, `.ufo/waves/round-61/sources/S432.html` (tags stripped per line, entities decoded):

```
6149 | 3.6. `X-Content-Type-Options` header
6150 | The
6151 | `X-Content-Type-Options`
6152 | response header can be used to require checking of a response’s
6153 | `Content-Type` header against the destination of a
6154 | request.
6158 | To determine nosniff, given a header list list, run
6164 | Let values be the result of getting, decoding, and splitting `X-Content-Type-Options` from list.
6174 | If values[0] is an ASCII case-insensitive match for
6175 | "nosniff", then return true.
6183 | Web developers and conformance checkers must use the following value
6184 | ABNF for `X-Content-Type-Options`:
6187 | X-Content-Type-Options           = "nosniff" ; case-insensitive
6229 | 3.7. `Cross-Origin-Resource-Policy` header
6232 | response header can be used to require checking a request’s
6233 | current URL’s origin against a request’s origin when request’s mode is
6235 | "no-cors".
```

- The paragraph is lines **6150–6154**; the counter's quoted characters are lines **6152–6154** and
  begin after the closing backtick of the field-name code element on 6151. The contract's
  "§3.6 body lines 6151–6154" is correct only if the pointer means "the quotation plus the field-name
  code element"; a pointer that claims the quoted words start on 6151 is off by one word.
- Uniqueness: with inline `<code>` backticks stripped and whitespace normalized, the 120-character
  quoted string occurs **once** in the whole 18 914-line body; with backticks kept it occurs **zero**
  times (the body interleaves literal backticks and `<a>`/`<code>` markup). The quote is therefore a
  *rendering-normalized* contiguous substring, exactly like the entry's other S432 spans, and any
  pointer must say so rather than imply a raw-byte match.
- Apostrophe is literal U+2019 (`response’s`), matching the counter's `QUOTE` and the contract text.
- Near-miss to name in the Gate: **§3.7 lines 6229–6235** repeats the phrasing for
  `Cross-Origin-Resource-Policy` ("…checking a request’s current URL’s origin…"). It is a different
  field; the frozen `QUOTE` matches it 0 times, so a careless pointer here would be visibly wrong.
- The verifier-rejected span is a separate node: lines **6183–6184** ("Web developers and conformance
  checkers must use the following value ABNF for `X-Content-Type-Options`:"), which announces the
  ABNF block at 6187 and asserts nothing. The value rule the entry encodes is carried by 6187 and
  6158–6179, not by the purpose sentence — keep that distinction in the correction.

## 4. Deliverables (drafts, counter-tested in scratch only)

### 4.1 Gate pointer (for `corpus/lessons/round-62.md`; verbatim draft)

```markdown
## Gate — S432 §3.6 located quote

| Field | Value |
|---|---|
| Item | S432 non-author disagreement, `corpus/lessons/round-61-verifier-spotcheck.md:33` (registry verdict `Admit`, spot-check `Disagree`) |
| Opened | https://fetch.spec.whatwg.org/ — HTTP 200, 2026-10-27; body byte-identical to the pinned round-61 body, sha256 `63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b`, 1854393 bytes |
| Exact location | `.ufo/waves/round-61/sources/S432.html`, §3.6 paragraph lines 6150–6154; the quoted characters are lines 6152–6154 and begin after the field-name code element on line 6151 |
| Old quote | `Web developers and conformance checkers must use the following` (lines 6183–6184): Reject as grounding — it announces the following ABNF block and asserts nothing about the field |
| Source verdict | Agree with the spot-check on quote quality and keep the source admitted: the located sentence asserts the field's purpose, while the value rule is grounded separately by the ABNF (line 6187) and the algorithm (lines 6158–6179) |
| Near-miss | §3.7 lines 6229–6235 repeats the phrasing for `Cross-Origin-Resource-Policy`; it is not the cited span |
| Registry | `corpus/SOURCES.md:178` S432 row used unchanged (tier A, status `mined`, opened 2026-10-27, recheck 180d); no new SOURCES row |
| Non-author record | kept verbatim; this round appends a correction and a criterion, it does not erase the disagreement |
```

### 4.2 Knowledge correction (append-only tail; verbatim draft)

```markdown
## Round-62 correction — S432 §3.6 quote (r61 spot-check, line 33)

The xcto_nosniff_value quotations above are preserved unedited. The verifier
rejected `"Web developers and conformance checkers must use the following"` as a
generic lead-in, not evidence for a response-header expectation
(`corpus/lessons/round-61-verifier-spotcheck.md:33`). Appended correction:

> "response header can be used to require checking of a response’s Content-Type header against the destination of a request"

S432 §3.6, retained body `.ufo/waves/round-61/sources/S432.html`, paragraph at
lines 6150–6154: the quoted characters are lines 6152–6154, and the quote begins
after the backtick-wrapped code element naming the field on line 6151, as the
other S432 spans in this entry do.

Support. The sentence asserts the field's job: the response header exists so that
a response's `Content-Type` may be checked against the destination of the
request. It is a purpose statement, and it is the substantive claim the entry's
opening sentence about "response-processing steps" attributes to §3.6.

Limits. The value rule this entry encodes is asserted elsewhere in the same
section — the ABNF production on line 6187, whose comment is `; case-insensitive`,
and the algorithm at lines 6158–6179, which reads the first decoded value and
compares it to `nosniff` as an ASCII case-insensitive match. The purpose sentence
does not by itself ground the value rule, which stays cited by location. The
near-identical phrasing at S432 §3.7 lines 6229–6235 describes
`Cross-Origin-Resource-Policy` and is not the quoted span. The S432 row
`corpus/SOURCES.md:178` is unchanged: this correction adds no registry row, and
the only source-open evidence added is a 2026-10-27 HTTP 200 reopen of
https://fetch.spec.whatwg.org/ whose body is byte-identical (sha256
63b0a018…bad911b, 1854393 bytes) to the pinned round-61 body.
```

### 4.3 QUALITY criterion (append-only section; verbatim draft)

```markdown
## Substantive located quotes — round 62

Criterion: a **substantive located quote** names its source section and the lines
or anchors in the pinned body, and the quoted words themselves assert the
proposition attributed to them; where the normative content sits in a
neighbouring node, the entry says so and cites that node by location.

Reject a generic lead-in ("must use the following", "as described below")
offered as grounding; a quote whose assertion lives in an unquoted sibling node
but is read as if it were quoted; or a lookalike sentence from another section.

Grounding: `corpus/lessons/round-61-verifier-spotcheck.md:33` (S432 `Disagree`:
lead-in only); `corpus/lessons/round-62.md` §Gate; S432 §3.6 lines 6150–6154
versus §3.7 lines 6229–6235.
```

## 5. Frozen-counter test of the three drafts (scratch fixture, no lane writes)

Fixture: fresh `git init` at `/fast/scratch/hyaku/kake-r62/ScribeSourceGate/fixture`,
`git -C` asserted `--show-toplevel` = fixture dir, four base blobs restored with
`git -C <lane> show c341a7a…:<path>`, draft commit adds only knowledge tail, QUALITY section and
`corpus/lessons/round-62.md`. Counter invoked unchanged:

| State | Command | Output | Exit |
|---|---|---|---|
| Lane base (reproduction) | `python3 -B .ufo/waves/round-62/c62_calibration.py --root . --revision c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13` | `disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false` | 1 |
| Fixture base | same script, `--root <fixture> --revision bfb1228` | identical line | 1 |
| Fixture after drafts | `--revision a6f1993` | `disagreements=1 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true` | 0 |

Lane base control therefore reproduces the contract's `unresolved=1 quote_correction=0 criterion=0
lesson_gate=0 source_row=1 met=false exit 1` exactly, and the drafts flip it to `met=true` with
`corpus/SOURCES.md` untouched (fixture diff: QUALITY +15, knowledge +31, lesson +14 lines).

## 6. Findings

### 6.1 Gate traps the drafter must respect (probe-tested, exact literals)

| Probe | Change from the passing state | Counter line | Verdict |
|---|---|---|---|
| P1 | straight `'` instead of U+2019 in the knowledge quote | `unresolved=1 quote_correction=0 … met=false` | exact codepoint required |
| P2 | criterion phrase capitalised (`Substantive located quote`) | `criterion=0 … met=false` | literal is lowercase `substantive located quote` |
| P3 | `## Gate` heading renamed `## Decision` | `lesson_gate=0 … met=false` | exact `## Gate` heading required |
| P6 | marker renamed `Round-62 note` | `quote_correction=0 … met=false` | exact `Round-62 correction` required |

Also required and easy to miss: `S432 §3.6` verbatim (with the section sign) in the knowledge entry,
the strings `Agree` and `Reject` and `S432` in `round-62.md`, and the exact filename
`round-61-verifier-spotcheck.md` in QUALITY. A table-row criterion is equally acceptable to the
counter as long as it contains the lowercase phrase; the entry's own append-only precedent favours a
new section, which is what §4.3 drafts.

### 6.2 Counter gaps (reported; counter and score untouched)

1. **`unresolved` is not a measured disagreement count once gates pass.**
   `unresolved = disagreements if not resolved else 0`. Probe P5 appended a line containing both
   `S432` and `Disagree` to the spot-check file: `disagreements=2` but `unresolved=0 … met=true`.
   Conversely P8 deleted the verifier's `Disagree` row entirely: `disagreements=0 … met=true`.
   A reader of `unresolved=0` cannot tell whether the finding was learned or erased.
2. **No preservation check exists.** The contract says the counter "verifies old-row preservation";
   `measure()` only tests the quote, three markers, the criterion phrase and `"| S432 |"`. Probe P7
   replaced the two preserved S432 spans in the entry with a placeholder and still scored
   `met=true`. Append-only preservation of the knowledge prose, the verifier row and the registry
   row must be checked by diff (`git -C <lane> diff c341a7a… -- corpus/SOURCES.md` empty;
   `git show c341a7a…:corpus/knowledge/response-header-expectations.md` is a prefix of the new blob;
   spot-check blob byte-identical), not by the counter.
3. **`source_row` is presence-only.** P4 set the S432 row's status to `rejected` and the counter still
   reported `source_row=1 … met=true`. The contract's "do not mark it rejected" is therefore
   reviewer-enforced only; the review must also confirm the row is still `mined` with `opened
   2026-10-27`, `recheck 180d` and the knowledge `used-by`, since the row's bytes are the evidence
   that no second row was added.
4. **`criterion` is phrase-matching, not semantics.** P2 shows the counter reacts to case, not to
   whether the criterion is grounded; the reviewer must read §4.3's Grounding column against the
   verifier line.

These are advisory readings of the frozen counter. No change to `c62_calibration.py`, the claim, the
criteria, or any score was made or is proposed here.

### 6.3 Source-side notes for the correction

- The purpose sentence grounds *why the field is read in response processing*; it does **not** ground
  the `nosniff` value rule, which needs 6187 + 6158–6179. The entry already cites those by location;
  do not let the new quote absorb their warrant.
- The counter `QUOTE` omits the leading field-name code element and the literal backticks around
  `X-Content-Type-Options` and `Content-Type`. It is a rendering-normalized substring (1 occurrence
  after normalization, 0 raw). Say so, as the entry's other spans do, so the falsifier
  ("retained body no longer contains a quoted span") stays honest.
- Do not touch the entry's `fetches:` header line to claim a round-62 fetch; there is no round-62
  receipt (§1). Keep reopen evidence in the appended block or the Gate row.

## 7. Out of scope / not done

- No edits to `contract.md`, `c62_calibration.py`, `corpus/knowledge/response-header-expectations.md`,
  `corpus/QUALITY.md`, `corpus/lessons/round-62.md`, `corpus/lessons/round-61-verifier-spotcheck.md`,
  `corpus/SOURCES.md`, or any lane Git/jj/index state: `git status --porcelain` in the lane shows only
  `?? .ufo/waves/round-62/` (the wave directory, containing dispatch/ready files and this report).
- No post-integration score was run; the after-state figure in §5 is a scratch-fixture prediction of
  the frozen counter on the drafted pointers, not a measured lane revision.
- Not verified: browser-rendered appearance of the code spans (only extracted text), the census
  contract's 171-row derivation beyond the reported counter, and any statement about live header
  behaviour of any property (out of this lane's policy scope).

## 8. Artifacts

- Report: `.ufo/waves/round-62/w1/ScribeSourceGate.md`
- Scratch (deleted before yield): `/fast/scratch/hyaku/kake-r62/ScribeSourceGate/` —
  `live.html`, `headers.txt`, `draft-correction.md`, `draft-criterion.md`, `draft-gate.md`,
  `fixture/` (commits `bfb1228` base, `a6f1993` after-drafts, probes `p1`…`p8` reset away).
- Commands used: `curl 8.23.0` GET of the source; `sha256sum`; `python3 3.14.8` inline text
  extraction; `python3 -B .ufo/waves/round-62/c62_calibration.py` (unmodified); `scripts/sources-census.sh
  validate|census`; `git -C <fixture>` for fixture commits. No installs, no pacman, no tool downloads.
