# Seat ScoutS432Reopen — round-64 S432 live re-open and CORPUS rule-1 audit of the Gate re-open record

**Verdict: the retained body IS current** — one independent GET on 2026-10-30 returns bytes
byte-identical to the round-61 retained body (sha256 `63b0a018…911b`, 1 854 393 bytes), to the
round-64 live receipt file, and to the raw blob pinned at the measured revision; the round-64
receipt's every field is confirmed by my own observation. **The round-64 lesson Gate re-open
record satisfies rule 1's *record elements*** (URL ✓, access date ✓, ≤25-word quote ✓ = 19 words,
location ✓ = raw lines 6150-6154, re-derived independently) — but with **two qualifications**:
(i) it is a *non-author re-open* record, not rule 1's new-row record, and the rule-1 requirement
that a quote *ground `teaches`* is **not** met for the S432 row by this span (the located span
grounds the field-purpose proposition; the row's `teaches` cell states the `nosniff` value rule
and is cited by location only); (ii) the 19-word string **as printed** in the lesson is a
normalized short form that is `absent` under the lane's own round-50 quote-class rule — it is a
substring of neither the retained HTML nor the extracted flat text (ASCII `'` vs source U+2019,
backticks dropped, leading `The \`X-Content-Type-Options\`` dropped); the class-able verbatim
span lives in the knowledge entry's `[r63-correction]` block. No C1/C2/C3 kill rule is engaged by
either qualification (see §8).

- Lane repo (read-only): `/home/vgpnk/Projects/shokunin/kake-shokunin`
- Base revision (round-63 tip): `1a48131577ba82c967650561be34e8dba909432a`
- Measured T0: `4c8295fa5e3b628f1fdf3840299ae415c01849fb`; receipts commit: `cc8add1fa740b920ea5179a71152680ab220c70c`
- Scratch tree (created, used, deleted): `/fast/scratch/hyaku/kake-r64/ScoutS432Reopen/`
- Report path: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/w1/ScoutS432Reopen.md`

---

## 1. What I attacked

The factual core of the round-64 lesson's Gate re-open record
(`/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-64.md:84-91`):

```
84: **S432 re-open record (rule 1):** https://fetch.spec.whatwg.org/ opened
85: 2026-10-30 (one GET, HTTP 200, 1,854,393 bytes; receipt
86: `.ufo/waves/round-64/sources/receipts.json`), sha256 `63b0a018…911b`
87: byte-identical to the round-61 retained body, so the retained body is
88: current. Located quote (raw lines 6150–6154, 19 words): "response header can
89: be used to require checking of a response's Content-Type header against the
90: destination of a request". No registry row added or changed; the S432 row
91: stays `mined`.
```

Attack surface, in order:

1. **Re-open independently** — one GET of `https://fetch.spec.whatwg.org/` from my own scratch,
   30 s timeout, no inherited `TMPDIR`, no cookies, and compare the received bytes' sha256 against
   (a) the round-61 retained body, (b) the round-64 live receipt body, (c) the raw blob committed
   at the measured revision.
2. **Re-derive the located range from *my* bytes** — not from the committed blob — so the location
   claim "raw lines 6150–6154" is tested against independently fetched bytes.
3. **Audit the record against CORPUS rule 1** (`/home/vgpnk/Projects/shokunin/CORPUS.md:112-115`):
   URL, access date, ≤25-word quote, location, and *grounding `teaches`*.

I edited nothing in the lane. The frozen claims, counters, receipts, contract and lesson are
untouched.

---

## 2. The one GET

```
$ cd /fast/scratch/hyaku/kake-r64/ScoutS432Reopen
$ curl -sS --max-time 30 -A 'round64-scout/ScoutS432Reopen' -D headers.txt -o S432.scout.html \
    -w 'http_code=%{http_code}\nsize_download=%{size_download}\ntime_total=%{time_total}\nurl_effective=%{url_effective}\n' \
    'https://fetch.spec.whatwg.org/'
http_code=200
size_download=1854393
time_total=2.025274
url_effective=https://fetch.spec.whatwg.org/
curl_exit=0
```

Exactly one request was issued (no `-L` redirect follow needed; `url_effective` equals the
requested URL). Response headers (same response, `-D`):

```
HTTP/2 200
server: nginx/1.10.3
date: Fri, 30 Oct 2026 11:08:44 GMT
content-type: text/html; charset=utf-8
content-length: 1854393
last-modified: Mon, 19 Oct 2026 12:03:15 GMT
vary: Accept-Encoding
etag: "6ad60703-1c4bb9"
access-control-allow-origin: *
```

`Last-Modified: Mon, 19 Oct 2026 12:03:15 GMT` predates both the round-61 fetch (2026-10-27) and
the round-64 fetch (2026-10-30): the served document has not been edited upstream in between, so
byte-identity across the three fetches is expected rather than lucky.

---

## 3. sha256 comparison — the retained body is current

```
$ sha256sum S432.scout.html \
    /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/sources/S432.html \
    /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/sources/S432.live.html
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  S432.scout.html
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  .../round-61/sources/S432.html
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  .../round-64/sources/S432.live.html

$ cmp S432.scout.html .../round-61/sources/S432.html   → IDENTICAL r61
$ cmp S432.scout.html .../round-64/sources/S432.live.html → IDENTICAL r64live
```

And the **committed** body at the measured revision:

```
$ git -C /home/vgpnk/Projects/shokunin/kake-shokunin show \
    cc8add1fa740b920ea5179a71152680ab220c70c:.ufo/waves/round-61/sources/S432.html | sha256sum
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  -
```

| Blob | sha256 | Bytes | Source |
|---|---|---|---|
| my one GET (2026-10-30 11:08:44Z) | `63b0a018…911b` | 1 854 393 | `S432.scout.html` (scratch) |
| round-61 retained body | `63b0a018…911b` | 1 854 393 | `.ufo/waves/round-61/sources/S432.html` (tracked) |
| round-61 retained body at receipts commit | `63b0a018…911b` | 1 854 393 | `git show cc8add1:…` |
| round-64 live receipt body | `63b0a018…911b` | 1 854 393 | `.ufo/waves/round-64/sources/S432.live.html` |
| counter's frozen pin `RAW_SHA` | `63b0a018…911b` | — | `.ufo/waves/round-64/c64_calibration.py:74` |

**All five agree.** The retained body is current.

### 3.1 The round-64 receipt, field by field

`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/sources/receipts.json` (single
row, `id` S432) against my own observation:

| Receipt field | Receipted value | My observation | Match |
|---|---|---|---|
| `url` | `https://fetch.spec.whatwg.org/` | same URL requested, `url_effective` identical | yes |
| `fetchedAt` | `2026-10-30T10:40:35Z` | my GET: `date: Fri, 30 Oct 2026 11:08:44 GMT`; file mtime `Oct 30 07:40` local (= −03:00 → 10:40Z) | consistent |
| `method` | `GET` | one GET | yes |
| `httpStatus` | `200` | `http_code=200` | yes |
| `bytes` | `1854393` | `size_download=1854393`, `content-length: 1854393` | yes |
| `sha256` | `63b0a018…911b` | `63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b` | yes |
| `retainedRound61Sha256` | `63b0a018…911b` | round-61 body sha (above) | yes |
| `byteIdenticalToRetained` | `true` | `cmp` reports no difference | yes |

The receipt file **is committed** at the receipts commit (`git show cc8add1:.ufo/waves/round-64/sources/receipts.json`
→ sha256 `95c5109787d375b559f9c025ce564b407691cf6e86be655989e4ab5fc2333bb1`; `git ls-files
--error-unmatch` succeeds), so its claims are backed by committed bytes plus the committed
round-61 body, which is byte-identical to the live body.

**Note (evidence, not a defect):** the *live body* file `.ufo/waves/round-64/sources/S432.live.html`
is **not tracked** (`git ls-files --error-unmatch` → "did not match any file(s) known to git";
`git status --porcelain` lists it as `??`). The committed evidence for the round-64 re-open is
therefore the receipt row plus the committed round-61 body (identical bytes), not a committed copy
of the live body. The receipt's `byteIdenticalToRetained` claim is verifiable from committed bytes
alone, so nothing in the round-64 record depends on the untracked file.

---

## 4. The located range re-derived from *my* bytes, not the committed blob

Recipe taken from the measured revision, raw input = **my fetched bytes**:

```
$ git -C … show cc8add1:.ufo/waves/round-63/quote-class/extract_text.py > extract_text.py
$ sha256sum extract_text.py
6b0a88cddfa3b712e8fdbe69c4c2803c816490cd43893972dfe0d39d5f362405   (== the counter's RECIPE_SHA)

recipe over MY fetched bytes : sha256 8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69
committed flat text S432.txt  : sha256 8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69
recipe output == committed S432.txt : True
```

I then re-implemented the counter's own minimal-window algorithm
(`c64_calibration.py:178-194`, `LOCATED_WINDOW=(6100,6200)`, `LOCATED_SPAN_MAX=15`, minimal
`b-a` whose recipe rendering contains `FROZEN_QUOTE`) and ran it over **my** bytes:

```
counter-equivalent derive_located over FETCHED bytes: 6150-6154  (width 4)
same over r61 retained blob                          : 6150-6154
```

The five raw lines (from my fetched copy; identical in the committed blob), 1-based:

```
6150:    <p>The
6151: `<dfn class="dfn-paneled" data-dfn-type="http-header" data-export id="http-x-content-type-options"><code>X-Con…
6152: response <a data-link-type="dfn" href="#concept-header" id="ref-for-concept-header④⑤">header</a> can be used t…
6153: `<code>Content-Type</code>` <a data-link-type="dfn" href="#concept-header" id="ref-for-concept-header④⑥">heade…
6154: <a data-link-type="dfn" href="#concept-request" id="ref-for-concept-request①⓪⑦">request</a>.
```

**The lesson's location claim "raw lines 6150–6154" is confirmed against independently fetched
bytes.** (Global minimality over the whole 18 915-line file was established by the sibling seat
`w1/ScoutRecipeReproduce.md`; my run reproduces the same value from an independent fetch.)

---

## 5. CORPUS rule 1 — the rule and what it demands

`/home/vgpnk/Projects/shokunin/CORPUS.md:112-115`:

> 1. **A row is a claim.** Write it only after opening the source in the round that writes the
>    row. The round lesson's `## Gate` records, for every new row, the URL, the access date, and a
>    ≤25-word quote with its location grounding `teaches`. Non-author verification re-opens a
>    sample.

Rule 1 has three parts: (i) *write the row only after opening the source in the writing round*;
(ii) *the writing round's `## Gate` records, for every new row:* URL + access date + a ≤25-word
quote **with its location** + the quote must **ground `teaches`**; (iii) *non-author verification
re-opens a sample*.

### 5.1 Record elements of the round-64 Gate re-open record — all present

| Rule-1 element | In `corpus/lessons/round-64.md:84-91` | Verified |
|---|---|---|
| URL | `https://fetch.spec.whatwg.org/` (line 84) | yes — matches the receipt row and the SOURCES row source cell |
| access date | `2026-10-30` (line 85) | yes — matches my fetch date (server `date:` Fri, 30 Oct 2026) and the receipt's `fetchedAt` |
| ≤25-word quote | lines 88-90, declared "19 words" | yes — collapsed, whitespace-split count = **19**; length 120 chars (round-61 convention: 6..25 units, ≤160 chars) |
| location | "raw lines 6150–6154" | yes — re-derived from independently fetched bytes (§4) |
| page-uniqueness (round-61 convention) | — | yes — "can be used to require checking of" occurs **1×** in the extracted text |

Word-count check (exact):

```
declared: 19   actual whitespace-split count: 19
collapsed quote: "response header can be used to require checking of a response's
                   Content-Type header against the destination of a request"   (120 chars)
```

### 5.2 The record is a *re-open* record, not a new-row record

Round 64 adds **no** registry row: `git diff 1a48131577ba82c967650561be34e8dba909432a
cc8add1fa740b920ea5179a71152680ab220c70c -- corpus/SOURCES.md` is **empty**; the S432 row
(`corpus/SOURCES.md:178`) still reads `status = mined`, `opened = 2026-10-27`, `recheck = 180d`;
the lesson says so itself ("No registry row added or changed; the S432 row stays `mined`", lines
90-91). So the round-64 Gate text is the *non-author verification re-opens a sample* record
(rule 1's third sentence), not the "every new row" record. The rule-1 new-row obligation for S432
sits in the round-61 Gate (`corpus/lessons/round-61.md:43`):

```
- S432 — https://fetch.spec.whatwg.org/ — opened 2026-10-27 — §3.6 — "Web developers and
  conformance checkers must use the following" (9 units; …)
```

— a record that satisfies rule 1's *elements* but whose quote the round-61 non-author spot-check
rejected (`corpus/lessons/round-61-verifier-spotcheck.md:33`): *"is only a generic lead-in, not
substantive evidence for a response-header expectation."* Rule 1's own design (a sample re-opened
by non-author verification) is what caught it; rounds 63/64 respond with the located span.

### 5.3 The "grounding `teaches`" clause — **not** met for the S432 row by this span

The S432 row's `teaches` cell (`corpus/SOURCES.md:178`) is:

> "The field has one defined value, nosniff, compared ASCII case-insensitively against the split
> field values, so a recorded value of anything else is outside the value rule"

The located span at raw lines 6150-6154 is the **field-purpose** sentence ("… response header can
be used to require checking of a response's `Content-Type` header against the destination of a
request"). It does **not** state the value rule. The lane's own knowledge entry says so
explicitly (`corpus/knowledge/response-header-expectations.md:242-244`):

> "This span substantively states the proposition the `xcto_nosniff_value` section attributes to
> S432 (a field-purpose statement, **kept separate from the `nosniff`-only value rule** per the
> round-62 criterion)."

and the value rule itself is cited **by location, not by quote** (the §3.6 ABNF block "is not
quoted because it spans element boundaries" — knowledge entry, `xcto_nosniff_value` section).
The only two spans quoted in that section are the historical ones the r63 correction declares
"ground nothing".

**Consequence:** rule 1's clause "a ≤25-word quote with its location grounding `teaches`" is
satisfied for the *purpose* proposition (the knowledge entry's use of S432) but **not** for the
S432 row's `teaches` cell, which no recorded quote grounds. The round-61 spot-check's harm
("an admitted row's quote does not ground its teaching", spot-check §Discernment) is therefore
*narrowed*, not *closed*, at the registry-row level: the cited row still teaches a value rule that
no quoted span establishes. This is a rule-1 conformance observation about the corpus, not a
C1/C2/C3 kill-rule breach (§8).

### 5.4 Quote fidelity of the string as printed — `absent` under the lane's own class rule

The lane's quote-class taxonomy (round-50 semantics, inlined in the counter at
`c64_calibration.py:113-119`) is: `raw-substring` if the string is in the raw body, else
`collapsed-only` if it is in the extracted flat text, else `absent`. Applied to the 19-word
string **as printed in the lesson**:

```
lesson quote (collapsed): "response header can be used to require checking of a response's
                           Content-Type header against the destination of a request"
in raw html : False
in flat text: False
→ class: absent
```

Why: the source text uses the typographic apostrophe U+2019 (`response’s`), the source renders
the code span with backticks (`Content-Type`), and the printed quote drops the leading
`The \`X-Content-Type-Options\``. The verbatim, class-able span is the one frozen in the counter
(`FROZEN_QUOTE`, `c64_calibration.py:77-81`) and quoted in the knowledge entry's `[r63-correction]`
block (`corpus/knowledge/response-header-expectations.md:222-245`), whose class is
`collapsed-only` — that is the string the counter pins, derives and gates.

Two further facts about the printed string:

- The round-63 lesson printed the same short form with the **typographic** apostrophe
  (`corpus/lessons/round-63.md:56-58`); the round-64 lesson prints the **ASCII** apostrophe
  (`corpus/lessons/round-64.md:89`). One codepoint apart, and both differ from the source
  (which is U+2019).
- Under the counter's `classify()`, the round-63 string is likewise not in the raw and not in the
  flat text → also `absent` as written.

So: the *substance* the lane intends is correct and verified (§4), the *string it prints* in the
Gate is a normalized short form that is not verbatim from either retained blob. The
"collapsed-only" label in the Gate's admit paragraph (`corpus/lessons/round-64.md:64-70`) attaches
to the frozen span carried by the knowledge entry, not to the short form the Gate prints.

**Nothing gates this.** The counter's `lesson_gate` component
(`c64_calibration.py:253-260`) requires only that the Gate contain `"S432 / Fetch"`, the
round-61 verdict span, `"collapsed-only"`, `"c64_calibration.py"` and an author-side marker; the
`quote_correction` component (`:248`) checks `FROZEN_QUOTE` against the **knowledge** block, not
the lesson. A future drift of the lesson's own re-open quote, access date or URL — including
re-introducing the round-61 generic lead-in — would not turn `c64_calibration.py` red.

---

## 6. Findings

| # | Finding | Severity | Evidence |
|---|---|---|---|
| F1 | The retained round-61 body is **current**: my one GET on 2026-10-30 is byte-identical (sha256 + `cmp`) to the round-61 retained body, to the round-64 live receipt body, and to the raw blob committed at `cc8add1`; `Last-Modified: Mon, 19 Oct 2026` predates all three fetches | none (confirms the claim) | §2, §3 |
| F2 | Every field of the round-64 source receipt is independently confirmed (url, fetchedAt, method, httpStatus, bytes, sha256, retainedRound61Sha256, byteIdenticalToRetained) | none (confirms the claim) | §3.1 |
| F3 | The located range "6150-6154" re-derives from **independently fetched** bytes with the counter's own minimal-window algorithm (width 4), and the recipe over my bytes reproduces the pinned flat-text sha `8b90d096…2a69` byte-for-byte | none (confirms the claim) | §4 |
| F4 | Rule-1 record elements all present in `corpus/lessons/round-64.md:84-91`: URL, access date 2026-10-30, 19-word quote (≤25) with location, and page-unique span | conforms (form) | §5.1 |
| F5 | **Rule-1 scope:** the record is a non-author re-open record, not a new-row record (no registry row added or changed; `corpus/SOURCES.md` diff base→receipts-commit is empty). Rule 1's new-row obligation for S432 remains in the round-61 Gate (`corpus/lessons/round-61.md:43`), whose quote the spot-check rejected | observation | §5.2 |
| F6 | **Rule-1 "grounding `teaches`" not met for the S432 row:** the located span grounds the field-purpose proposition; the row's `teaches` cell (`corpus/SOURCES.md:178`) states the `nosniff` value rule, which no quoted span establishes (cited by location only, per `corpus/knowledge/response-header-expectations.md:242-244`) | observation | §5.3 |
| F7 | **Quote fidelity:** the printed 19-word string is `absent` under the lane's own class rule (`c64_calibration.py:113-119`) — ASCII `'` vs source U+2019, backticks dropped, leading `The \`X-Content-Type-Options\`` dropped — in both the raw body and the flat text; round-63 printed the same short form with U+2019, round-64 with ASCII `'` | observation | §5.4 |
| F8 | **Ungated surface:** `c64_calibration.py`'s `lesson_gate` (`:253-260`) does not read the lesson's re-open quote/date/URL at all, and `quote_correction` (`:248`) checks the knowledge block; drift in the Gate re-open record cannot turn the counter red | observation | §5.4 |
| F9 | The round-64 **live body** file `.ufo/waves/round-64/sources/S432.live.html` is untracked (not committed); the committed evidence is the tracked receipt row plus the committed, byte-identical round-61 body | observation | §3.1 |

---

## 7. What I did not attack (other seats' axes)

The C2 stub-proofing of `c64_quote_tool.py` and the C3 sidecar re-pin / `freshness-sweep.mjs`
outcome; the C1 counter's `pins`/`recipe`/`class`/`prose`/`unresolved` components beyond the
prose-binding cross-read I needed for §5.4; the committed control fixtures and their `met=false`
receipts. I did read the frozen instruments' shas only to confirm they match the contract:

```
5489eb2f3ac498e0383d841c677f036231fbf6933717d8da447f3193ff088adf  .ufo/waves/round-64/c64_calibration.py
96fd64e9a915468a32596e1560de4a71af5ba26fd7a6cc583d279add6327ee2b  .ufo/waves/round-64/c64_quote_tool.py
```

(both equal the contract's frozen pins at `.ufo/waves/round-64/contract.md`).

---

## 8. Kill-rule impact

**None.** The C1 kill rule (`.ufo/waves/round-64/contract.md` §C1) fires on: an after receipt that
does not print `met=true`; any pinned sha differing at the measured revision; any control printing
`met=true`; a counter crash; or a wave attack reproducing a marker-only / stub / do-nothing /
digest-consistent-fabrication green. My findings concern the *corpus prose* of the Gate re-open
record (F5/F6/F7) and an *ungated* surface (F8); they do not touch a pin, a control, a receipt or
the counter's predicate. The counter's own green-after receipt
(`.ufo/waves/round-64/controls/after-c1.txt`, `met=true`, exit 0) is unaffected by anything here,
and my re-open *supports* the C1 claim's factual substrate (the retained body is current; the
located range is 6150-6154; the recipe output is the pinned sha).

---

## 9. Commands, files, hygiene

**Lane artifacts read (all read-only, absolute paths):**

- `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-64.md` (lines 84-96)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-63.md` (lines 45-59)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-61.md` (line 43)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-61-verifier-spotcheck.md` (line 33)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md` (line 178; schema line 7)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/response-header-expectations.md` (lines 222-245)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/QUALITY.md` (§Round-62 criteria)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/contract.md`, `c64_calibration.py`, `c64_quote_tool.py`
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/sources/receipts.json`, `S432.live.html`
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/controls/after-c1.txt`
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/sources/S432.html`
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/quote-class/S432.txt`, `extract_text.py`
- `/home/vgpnk/Projects/shokunin/CORPUS.md` (lines 112-115)

**Scratch (created under the mandated path, deleted before yield):**
`/fast/scratch/hyaku/kake-r64/ScoutS432Reopen/` — `S432.scout.html`, `headers.txt`,
`extract_text.py`, plus ephemeral eval state. Deleted with `rm -rf` after all evidence was
captured into this report.

**Hygiene assertions:**

- **One** HTTP request to `https://fetch.spec.whatwg.org/` (the single `curl` in §2). No other
  network access; no retries.
- No mutating `git`/`jj` command anywhere. Only `git show`, `git rev-parse`, `git ls-files`,
  `git status`, `git diff` (all read-only) against the lane repo. No fixture repo was created, so
  the `rev-parse --show-toplevel` precondition never arose.
- The lane working tree was not modified except for **this report file**, the path my seat spec
  names. `git status --porcelain` in the lane shows only orchestrator-produced untracked paths
  (`.ufo/waves/round-64/sources/S432.live.html`, `.ufo/waves/round-64/w1*`), which pre-existed
  my seat.
- Nothing written to `~/.local/bin` or any PATH directory; no fleet-root tracked file
  (`LOG.md`, `SCORECARD.md`, `MANIFEST.json`) touched; nothing committed or pushed.
- **Tools:** no installs. `curl` and `python3` (pre-existing system interpreter) sufficed;
  `pacman` was not invoked (host-wide pause respected).

---

## 10. One-line verdict

**The round-64 S432 re-open is honest and independently reproducible — one GET on 2026-10-30
returns bytes byte-identical to the round-61 retained body, the round-64 live body and the pinned
raw blob (`63b0a018…911b`, 1 854 393 bytes, HTTP 200, `Last-Modified: Mon, 19 Oct 2026`), and the
lesson's located range 6150-6154 re-derives from those independent bytes — so the retained body IS
current; the Gate re-open record carries every element rule 1 names (URL, access date, 19-word
quote, location) and is therefore a conforming non-author re-open record, but rule 1's
"grounding `teaches`" is still unmet for the S432 row (the span grounds the field-purpose
proposition; the row teaches the `nosniff` value rule, cited by location only), the printed
19-word string is `absent` under the lane's own quote-class rule (ASCII `'` vs source U+2019,
backticks dropped), and no counter gates that Gate text.**
