# ScoutRetainedLines — round-63 w1 seat report

**Item:** Verify from committed bytes that WHATWG Fetch §3.6 raw lines 6150-6154 of
`.ufo/waves/round-61/sources/S432.html` carry the field-purpose sentence, that the
ledger's `locatedRawLines` value is accurate, and that the frozen quote string equals
the located rendering (backticks and U+2019 apostrophe included).

**Verdict: CONFIRMED on all three points** (high confidence, byte-level evidence below).

Fleet root for all paths: `/home/vgpnk/Projects/shokunin/kake-shokunin`
Measured commit: `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`

---

## 1. Exact raw lines 6150-6154 (byte-exact, from committed bytes)

Command:

```sh
cd /home/vgpnk/Projects/shokunin/kake-shokunin && python3 - <<'EOF'
import pathlib
raw = pathlib.Path('.ufo/waves/round-61/sources/S432.html').read_bytes()
lines = raw.split(b'\n')
print("total raw lines:", len(lines))
for i in range(6149, 6155):
    print(i+1, repr(lines[i]))
EOF
```

Output:

```
total raw lines: 18915
6150 b'   <p>The'
6151 b'`<dfn class="dfn-paneled" data-dfn-type="http-header" data-export id="http-x-content-type-options"><code>X-Content-Type-Options</code></dfn>`'
6152 b'response <a data-link-type="dfn" href="#concept-header" id="ref-for-concept-header\xe2\x91\xa3\xe2\x91\xa4">header</a> can be used to require checking of a <a data-link-type="dfn" href="#concept-response" id="ref-for-concept-response\xe2\x91\xa3\xe2\x91\xa0">response</a>\xe2\x80\x99s'
6153 b'`<code>Content-Type</code>` <a data-link-type="dfn" href="#concept-header" id="ref-for-concept-header\xe2\x91\xa3\xe2\x91\xa5">header</a> against the <a data-link-type="dfn" href="#concept-request-destination" id="ref-for-concept-destination\xe2\x91\xa0\xe2\x93\xaa">destination</a> of a'
6154 b'<a data-link-type="dfn" href="#concept-request" id="ref-for-concept-request\xe2\x91\xa0\xe2\x93\xaa\xe2\x91\xa6">request</a>.'
6155 b''
```

Pasted exactly as rendered text (UTF-8 decoded; the `\xe2\x80\x99` byte sequence on
line 6152 is U+2019 RIGHT SINGLE QUOTATION MARK):

```
6150    <p>The
6151 `<dfn class="dfn-paneled" data-dfn-type="http-header" data-export id="http-x-content-type-options"><code>X-Content-Type-Options</code></dfn>`
6152 response <a data-link-type="dfn" href="#concept-header" id="ref-for-concept-header④⑤">header</a> can be used to require checking of a <a data-link-type="dfn" href="#concept-response" id="ref-for-concept-response④①">response</a>’s
6153 `<code>Content-Type</code>` <a data-link-type="dfn" href="#concept-header" id="ref-for-concept-header④⑥">header</a> against the <a data-link-type="dfn" href="#concept-request-destination" id="ref-for-concept-request-destination①⓪">destination</a> of a
6154 <a data-link-type="dfn" href="#concept-request" id="ref-for-concept-request①⓪⑦">request</a>.
```

The §3.6 heading (`<h3 ... data-level="3.6" id="x-content-type-options-header">…3.6. …
`X-Content-Type-Options` header…</h3>`) is the immediately preceding line 6149, so the
five-line span 6150-6154 is precisely the field-purpose paragraph of Fetch §3.6.

## 2. Ledger `locatedRawLines` accuracy

`.ufo/waves/round-63/quote-class/quote-classes.json` records
`"locatedRawLines": "6150-6154"`. Measured against the committed bytes:

- The sentence opens on line 6150 with `   <p>The` and closes on line 6154 with
  `<a ...>request</a>.` — the five-line span is exact; no off-by-one. Line 6155 is blank.
- Line numbering was indexed with `raw.split(b'\n')` (0-based index 6149 ⇒ line 6150),
  and the total line count 18915 matches the file's actual structure.

**`locatedRawLines` is accurate.**

## 3. Frozen quote == located rendering (backticks and U+2019 included)

Ledger `classes[0].quote` (and the counter's `FROZEN_QUOTE` at
`.ufo/waves/round-63/c63_calibration.py:47-51`) is:

```
The `X-Content-Type-Options` response header can be used to require checking of a response’s `Content-Type` header against the destination of a request.
```

Byte-level checks (same Python session as §1):

```
QUOTE repr: 'The `X-Content-Type-Options` response header can be used to require checking of a response’s `Content-Type` header against the destination of a request.'
codepoints around apostrophe: ['0x2019']        # exactly one non-ASCII codepoint, U+2019 in "response’s"
quote in flat text rendering: True              # substring of .ufo/waves/round-63/quote-class/S432.txt
quote in raw html: False                        # NOT a substring of the raw HTML
text context: b'exclusively use UTF-8. 3.6. `X-Content-Type-Options` header The `X-Content-Type-Options` response header can be used to require checking of a response\xe2\x80\x99s `Content-Type` header against the destination of a request. To determine nosniff, given a header li'
```

Derivation of the located rendering from the raw span (round-50 collapsed-only class):

1. Raw lines 6150-6154 contain the sentence interleaved with inline markup
   (`<dfn>`, `<code>`, `<a>`, surrounding backticks), so the quote cannot be a raw
   substring — confirmed (`quote in raw html: False`).
2. The committed recipe `.ufo/waves/round-63/quote-class/extract_text.py` renders the
   retained HTML with textContent semantics: charrefs decoded once, script/style/noscript
   skipped, block elements → newline boundaries, inline content concatenated, every
   whitespace run collapsed to one ASCII space, output joined into a single line.
3. Under that rendering the §3.6 heading and the paragraph flatten to
   `… 3.6. \`X-Content-Type-Options\` header The \`X-Content-Type-Options\` response
   header can be used to require checking of a response’s \`Content-Type\` header against
   the destination of a request. To determine nosniff, …` — the frozen quote is a
   verbatim substring (context shown above), backticks and U+2019 included.
4. This is exactly the ledger's `matchClass: "collapsed-only"` (round-50 rule: a span
   present only in the collapsed flat-text rendering, not in the raw HTML).

**The frozen quote string equals the located rendering, byte for byte.**

## 4. Hash chain (committed bytes, measured commit)

```
$ sha256sum .ufo/waves/round-63/c63_calibration.py \
    .ufo/waves/round-63/quote-class/quote-classes.json \
    .ufo/waves/round-61/sources/S432.html \
    .ufo/waves/round-63/quote-class/S432.txt scripts/quote_class.py
bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91  .ufo/waves/round-63/c63_calibration.py   == frozen counter sha (contract) ✓
5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d  .ufo/waves/round-63/quote-class/quote-classes.json == frozen ledger sha (contract) ✓
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  .ufo/waves/round-61/sources/S432.html    == ledger rawSha256 ✓
8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69  .ufo/waves/round-63/quote-class/S432.txt == ledger textSha256 ✓
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  scripts/quote_class.py                    == frozen tool sha (contract) ✓
```

Same three artifact blobs re-derived from the measured commit directly:

```
$ git show 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f:.ufo/waves/round-61/sources/S432.html | sha256sum
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  -
$ git show 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f:.ufo/waves/round-63/quote-class/S432.txt | sha256sum
8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69  -
$ git show 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f:.ufo/waves/round-63/quote-class/quote-classes.json | sha256sum
5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d  -
```

`git status --porcelain` over the frozen paths shows no modifications (only the
in-flight untracked wave scaffolding `.ufo/waves/round-63/w1.ready*` / `w1/`, which this
report is part of).

## 5. Independent counter corroboration

```
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
```

The counter's inline `classify()` (round-50 semantics: `raw-substring` / `collapsed-only`
/ `absent`) re-derives `collapsed-only` from the committed blobs with `class_match=1`,
agreeing with the ledger's recorded class. The counter's `FROZEN_QUOTE` constant is the
same string as the ledger quote (verified by eye against §3 above; both use U+2019).

## 6. Findings summary

| Question | Answer | Evidence |
|---|---|---|
| Do raw lines 6150-6154 carry the field-purpose sentence? | Yes | §1 byte dump; §3.6 heading at line 6149; sentence spans 6150-6154 |
| Is `locatedRawLines: "6150-6154"` accurate? | Yes | §2 indexing check |
| Does the frozen quote equal the located rendering (backticks + U+2019)? | Yes, byte-for-byte substring of the flat-text rendering; absent from raw HTML | §3 membership checks + context dump |

Confidence: **high** — all claims are grounded in `sha256sum`-verified committed bytes at
the measured commit, with the derivation reproduced from the committed `extract_text.py`
recipe semantics.

Remaining unknowns: none for this item. (Out of scope, not evaluated: C1's other
components — criterion/lesson_gate/source_row content quality, and the C2 tool selftest;
this seat verified only the S432 quote-location claim assigned to it.)

## 7. Lane-bounds compliance

- Leaf seat: no subagent dispatch, no commits, no push, no mutating git/jj. Read-only
  against the fleet root.
- Wrote only this report at
  `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/w1/ScoutRetainedLines.md`.
- Frozen claim, counters, receipts, corpus/SOURCES.md, scripts/ and templates/ untouched.
- No fixture repos created; no tools installed (nothing new needed) — no installs to record.
- No pacman transactions.
