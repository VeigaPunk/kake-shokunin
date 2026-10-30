# Seat ScribeRule1Audit — S432 re-open record vs CORPUS.md SOURCES rule 1

Date: 2026-10-30. Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`.
HEAD = `cc8add1fa740b920ea5179a71152680ab220c70c` (green-after receipts), parent
`4c8295fa5e3b628f1fdf3840299ae415c01849fb` (measured T0), parent
`1a48131577ba82c967650561be34e8dba909432a` (round-63 base). Read-only seat:
no lane file outside this report was created, modified or deleted; no git/jj
mutation anywhere; no subagent dispatched; no tools installed; no pacman use.

Audited surface:

- `.ufo/waves/round-64/sources/receipts.json` (committed at T0;
  `git show 4c8295fa:.ufo/waves/round-64/sources/receipts.json | cmp - <worktree file>`
  → identical).
- `corpus/lessons/round-64.md` lines 84–90, the "**S432 re-open record (rule 1):**"
  paragraph inside `## Gate` (heading at line 46, next `##` at line 103). The lesson
  blob is byte-identical at T0, at green-after and in the worktree
  (sha256 `b4ac2fbd4ca77fdb66c54ce514719d743127b1c895b2d044e564609a796b1271`).

Rule text (fleet `CORPUS.md` "### Rules", item 1, fleet-root `/home/vgpnk/Projects/shokunin/CORPUS.md:125-127`):
"A row is a claim. Write it only after opening the source in the round that writes the row.
The round lesson's `## Gate` records, for every new row, the URL, the access date, and a
≤25-word quote with its location grounding `teaches`. Non-author verification re-opens a sample."

## Clause-by-clause

### A. receipts.json

| Clause | Verdict | Evidence |
|---|---|---|
| URL present | PASS | `receipts.json` field `"url": "https://fetch.spec.whatwg.org/"` — identical to the `source` cell URL of registry row S432 (`corpus/SOURCES.md:178`). |
| fetchedAt = 2026-10-30 | PASS | `"fetchedAt": "2026-10-30T10:40:35Z"` — the audit date; matches the lesson's access date "opened 2026-10-30". |
| method GET | PASS | `"method": "GET"`, `"httpStatus": 200` recorded alongside. |
| sha256 | PASS | `"sha256": "63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b"` equals: (1) the sha256 of the round-64 retained file `.ufo/waves/round-64/sources/S432.live.html` (`sha256sum` → same, 1854393 bytes = the receipt's `"bytes": 1854393` and `wc -c`); (2) the sha256 of the committed round-61 blob `.ufo/waves/round-61/sources/S432.html` at base, at T0 and green-after — the receipt's `"byteIdenticalToRetained": true` and `"retainedRound61Sha256"` are true; (3) the C1 counter constant `RAW_SHA` (`.ufo/waves/round-64/c64_calibration.py:66`); (4) the contract's raw-blob pin (`.ufo/waves/round-64/contract.md:28`); (5) the ledger `rawSha256` (`.ufo/waves/round-63/quote-class/quote-classes.json:13`). |
| One GET this round | consistent | receipt `note`: "one public GET; purpose: SOURCES rule-1 re-open of the S432 row for the round-64 sourced calibration claim". |

### B. Lesson Gate re-open paragraph (round-64.md:84-90)

| Clause | Verdict | Evidence |
|---|---|---|
| URL present | PASS | Line 84: `https://fetch.spec.whatwg.org/` — same URL as receipt and registry row. |
| Access date 2026-10-30 | PASS | Line 85: "opened 2026-10-30 (one GET, HTTP 200, 1,854,393 bytes; receipt `.ufo/waves/round-64/sources/receipts.json`)". |
| ≤25-word located quote, counted exactly | PASS, 19 words | Line 86-88 quote: `response header can be used to require checking of a response's Content-Type header against the destination of a request`. Whitespace tokenization gives exactly **19** tokens: response(1) header(2) can(3) be(4) used(5) to(6) require(7) checking(8) of(9) a(10) response's(11) Content-Type(12) header(13) against(14) the(15) destination(16) of(17) a(18) request(19) — matching the lesson's own "19 words". Even splitting the hyphenated `Content-Type` into two words gives 20 ≤ 25. |
| Location = raw lines 6150–6154 | PASS | Independently re-derived: loading the committed recipe `.ufo/waves/round-63/quote-class/extract_text.py` (sha256 `6b0a88cd…f362405`) and scanning raw lines 6100–6200 of the retained blob for spans of ≤15 lines whose rendering contains the ledger quote `The \`X-Content-Type-Options\` response header can be used to require checking of a response’s \`Content-Type\` header against the destination of a request.`, the minimal span is exactly **6150–6154**; rendering those five raw lines yields that sentence. The range equals the ledger's `"locatedRawLines": "6150-6154"` (quote-classes.json:14) and the counter constant `EXPECTED_LOCATED = "6150-6154"` (c64_calibration.py:70). Raw lines 6150–6154 are the §3.6 `<p>` element (6150–6151 carry "The `X-Content-Type-Options`"; 6152–6154 carry the words quoted). |
| "No registry row added or changed" statement | PASS and TRUE | Lesson lines 89–90: "No registry row added or changed; the S432 row stays `mined`." Verified: `git show <rev>:corpus/SOURCES.md | sha256sum` → `63af1594e2f8d0b499fbf2673424bf818cf93dd380232a8c8d546eef00f75ae2` at base, T0 and green-after (three identical hashes); `git diff 1a481315… 4c8295fa… -- corpus/SOURCES.md` → empty (0 lines); row count `grep -cE '^\|…S[0-9]{3,}\|'` → **171** at all three revisions; worktree `corpus/SOURCES.md` sha identical and `git status --porcelain --untracked-files=no` → empty (tracked tree untouched). Row S432 (`corpus/SOURCES.md:178`) retains `opened 2026-10-27`, `status mined`, `used-by corpus/knowledge/response-header-expectations.md`. The round-64 lesson is a new file this round (absent at base) — not a registry change. |

## Findings (caveats, none of the enumerated clauses fails)

1. **The located quote is a normalized rendering, not a byte-verbatim excerpt.** As
   literally quoted it is a substring of neither the raw HTML (inline markup, U+2019
   apostrophe in "response’s") nor the committed flat text
   `.ufo/waves/round-63/quote-class/S432.txt`: the flat text carries the sentence with
   backticks, the curly apostrophe, the leading subject "The `X-Content-Type-Options`"
   and a trailing period. The lesson's 19-word version drops those. Punctuation-stripped
   and lowercased it is contained contiguously in the flat text, so word order and
   content are faithful; only exact-byte fidelity fails. Rule 1 does not define a
   verbatim standard for collapsed-markup sources; the ledger itself records the same
   fact ("the span is a substring of the committed flat-text rendering only", the
   `collapsed-only` class). Reported, not scored as a breach.
2. **The quote does not by itself ground the row's `teaches`.** Row S432 `teaches` is the
   nosniff value rule ("The field has one defined value, nosniff, compared ASCII
   case-insensitively against the split field values…", SOURCES.md:178). The quoted
   sentence is the §3.6 field-purpose lead-in; the value-rule text ("To determine
   nosniff, …") starts on the next flat-text sentence. This is precisely the round-61
   non-author spot-check's `Disagree` reason — "is only a generic lead-in, not
   substantive evidence for a response-header expectation" — which the same Gate section
   quotes verbatim (round-64.md:95) and which the C1 counter deliberately binds
   (`SPOT_VERDICT_SPAN`, c64_calibration.py:78-81). The lesson therefore discloses the
   defect rather than hiding it; the resolution mechanism is the located-range
   re-derivation plus the round-63 non-author closure, not this quote.
3. **Rule-1 scope note.** The Gate-record duty ("for every new row") is vacuous this
   round — no row was added or changed (verified above). The re-open record is
   author-side; rule 1's "Non-author verification re-opens a sample" obligation is
   discharged by the verifier spot-check/closure mechanism, and the lesson says so
   (round-64.md:91-102: "This round's own gate decisions … are author-side
   self-assessment; the round-64 non-author closure decides agreement."). No claim is
   upgraded here.
4. **Consistency with the row-opening record.** The round-61 Gate record for the same
   row used a different quote — "Web developers and conformance checkers must use the
   following" (9 units; `corpus/lessons/round-61.md:43`) — with the same blob sha and
   byte count. The re-open quote is a different span of the same §3.6; no contradiction
   with rule 2 (append-only) since no registry cell changed.
5. **Blob commit state.** `.ufo/waves/round-64/sources/S432.live.html` is untracked
   (`?? ` in `git status --porcelain`), present on disk only; the receipt, lesson and all
   counter pins point at the committed round-61 blob (same sha), so no audit dependency
   rests on the untracked copy. `receipts.json` is committed at T0.

## Verdict

The S432 re-open record **complies with every enumerated clause of SOURCES rule 1**:
URL present (receipt + Gate, both `https://fetch.spec.whatwg.org/`), access date
2026-10-30 in both, located quote exactly 19 words (≤25), location raw lines 6150–6154
accurate and equal to ledger/counter pins, and the "no registry row added or changed"
statement present and true (SOURCES.md byte-identical, 171 rows, at base/T0/green-after
and in the untouched worktree). Two disclosed caveats stand: the quote is a normalized
rendering rather than byte-verbatim, and the span grounds the field's purpose, not the
row's `teaches` (nosniff value rule) — the pre-existing round-61 `Disagree` span the
round binds and resolves by other evidence. No conflict with the frozen contract was
found; nothing was edited, attacked or rerun beyond read-only verification.

## Commands and exact outputs

```
$ sha256sum .ufo/waves/round-64/sources/S432.live.html .ufo/waves/round-61/sources/S432.html
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  .ufo/waves/round-64/sources/S432.live.html
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  .ufo/waves/round-61/sources/S432.html
$ wc -l -c .ufo/waves/round-64/sources/S432.live.html
18914 1854393 … (receipt bytes: 1854393; httpStatus 200; fetchedAt 2026-10-30T10:40:35Z; method GET)
$ python3 (word count of the lesson's located quote) → 19 tokens, list as in table; hyphen-split variant → 20
$ python3 (lesson quote literal presence): in raw html False; in flat text False;
  ledger quote in flat text True; punctuation-stripped lowercase lesson quote in flat text True
$ python3 (minimal-span re-derivation over raw lines 6100–6200, recipe 6b0a88cd…): span 6150–6154;
  rendered slice: "The `X-Content-Type-Options` response header can be used to require checking of a
  response’s `Content-Type` header against the destination of a request."
$ for rev in 1a481315… 4c8295fa… cc8add1f…: git show $rev:corpus/SOURCES.md | sha256sum →
  63af1594e2f8d0b499fbf2673424bf818cf93dd380232a8c8d546eef00f75ae2 (×3); row count → 171 (×3)
$ git diff --stat 1a481315… 4c8295fa… -- corpus/SOURCES.md → (empty); diff | wc -l → 0
$ git rev-parse HEAD → cc8add1fa740b920ea5179a71152680ab220c70c
$ git show 4c8295fa…:corpus/lessons/round-64.md | sha256sum → b4ac2fbd4ca77fdb66c54ce514719d743127b1c895b2d044e564609a796b1271 (== worktree, == cc8add1f… blob)
$ git status --porcelain --untracked-files=no → (empty)
```

## Surfaces touched / scratch

- Wrote only: this report, `.ufo/waves/round-64/w1/ScribeRule1Audit.md`.
- Scratch `/fast/scratch/hyaku/kake-r64/ScribeRule1Audit/` (derived analysis only, all
  reproduced above) — deleted before yielding.
- Out of scope (not audited): C1/C2/C3 counters, controls, sweep, census, round-61/63
  artifacts beyond the S432-relevant blobs, non-author closure of this round.
