# ScoutLedgerIntegrity — round-63 quote-class ledger internal verification

Seat scope: verify `.ufo/waves/round-63/quote-class/quote-classes.json` internally —
recompute sha256 of the committed text/raw blobs and compare to the ledger's
`textSha256`/`rawSha256`; confirm the ledger `quote` is byte-identical to the quote in
`corpus/knowledge/response-header-expectations.md` (round-63 block) and to `FROZEN_QUOTE`
in `.ufo/waves/round-63/c63_calibration.py`.

Verdict: **PASS — ledger is internally consistent; all three quote copies are byte-identical.**
No tools installed; no fixtures created; read-only against the fleet repo.

## Evidence

Fleet root: `/home/vgpnk/Projects/shokunin/kake-shokunin` (all paths below relative to it).

### 1. Blob hashes match the ledger

Command:

```
sha256sum .ufo/waves/round-63/quote-class/S432.txt .ufo/waves/round-61/sources/S432.html
```

Output:

```
8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69  .ufo/waves/round-63/quote-class/S432.txt
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  .ufo/waves/round-61/sources/S432.html
```

Ledger (`.ufo/waves/round-63/quote-class/quote-classes.json`, class id `S432`):

- `textPath` = `.ufo/waves/round-63/quote-class/S432.txt`, `textSha256` = `8b90d096…6f542a69` — **match**
- `rawPath` = `.ufo/waves/round-61/sources/S432.html`, `rawSha256` = `63b0a018…bad911b` — **match**

(The raw sha256 `63b0a018…bad911b` also agrees with the round-61 fetch receipt recorded in
`corpus/knowledge/response-header-expectations.md` line 4: "receipts … sha256 S432 63b0a018…bad911b".)

### 2. Ledger quote is byte-identical in all three locations

Extraction method:

- Ledger: `json.load(...)["classes"][0]["quote"]` → exact JSON string bytes.
- Corpus: line 230 of `corpus/knowledge/response-header-expectations.md` (inside the
  "## Round-63 correction — S432 field-purpose span admitted as collapsed-only" block that
  begins at line 222); the blockquote content between the outer ASCII double quotes.
- Counter: `FROZEN_QUOTE` from `.ufo/waves/round-63/c63_calibration.py` lines 51–54,
  evaluated via `ast.literal_eval` (line 53 uses the `\u2019` escape for the right single quote).

Comparison (Python `==` on str, plus sha256 of the UTF-8 encoding):

```
ledger==corpus : True
ledger==frozen : True
corpus==frozen : True
ledger len 154 sha256 465711f70cf80c77458639aebaf13963277f50086b8ccd907fe7e12bb54a6e2d
corpus len 154 sha256 465711f70cf80c77458639aebaf13963277f50086b8ccd907fe7e12bb54a6e2d
frozen len 154 sha256 465711f70cf80c77458639aebaf13963277f50086b8ccd907fe7e12bb54a6e2d
```

Each copy is 154 UTF-8 bytes with exactly one non-ASCII code point, U+2019 (’) in
"response’s". The quote string is:

> The `X-Content-Type-Options` response header can be used to require checking of a response’s `Content-Type` header against the destination of a request.

### 3. Corroboration of the ledger's collapsed-only note (out of strict scope, cheap)

- The quote **is** a contiguous substring of the committed flat-text rendering
  `.ufo/waves/round-63/quote-class/S432.txt` (`q in txt` → True).
- The quote is **not** a contiguous substring of the raw HTML (`q in raw` → False);
  inline markup splits it. This is consistent with the ledger note "the span is a
  substring of the committed flat-text rendering only".
- Ledger `locatedRawLines: "6150-6154"` verified: `.ufo/waves/round-61/sources/S432.html`
  lines 6150–6154 (1-based) carry the sentence across `<dfn>`/`<a>`/`<code>` inline
  elements, ending "…request.</a>." at line 6154.

## Confidence and remaining unknowns

- Hash and byte-identity claims: **certain** (direct recomputation from committed bytes).
- `locatedRawLines` and substring claims: **certain** (direct file inspection).
- Out of scope, not checked here: sha256 of `c63_calibration.py` itself, the
  `extract_text.py` recipe, the `quote_class.py` selftest, and the round-61 S432
  disagreement adjudication logic — assigned to sibling seats.
