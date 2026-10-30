# ScoutLedgerIntegrity — round-64 w1 seat report

Item: verify `.ufo/waves/round-63/quote-class/quote-classes.json` at T0
(`4c8295fa5e3b628f1fdf3840299ae415c01849fb`) against committed bytes.

**Verdict: VERIFIED — all four checks pass on committed bytes at T0. No
discrepancy found. No edits made to the lane.**

All evidence below is from `git show T0:<path>` (committed bytes), not the
working tree, unless explicitly marked. Scratch used:
`/fast/scratch/hyaku/kake-r64/ScoutLedgerIntegrity/` (deleted before yield).

## 1. sha256 of raw and text blobs vs ledger fields — MATCH

Ledger fields (`classes[0]`, file
`.ufo/waves/round-63/quote-class/quote-classes.json` at T0):
`rawSha256=63b0a018…bad911b`, `textSha256=8b90d096…f542a69`.

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ git show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-61/sources/S432.html | sha256sum
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  -     == ledger.rawSha256  ✓
$ git show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-63/quote-class/S432.txt | sha256sum
8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69  -     == ledger.textSha256 ✓
```

Fields are not swapped (`textPath`=S432.txt carries the `8b90…` digest,
`rawPath`=`.ufo/waves/round-61/sources/S432.html` carries the `63b0…`
digest). The ledger blob itself hashes to
`5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d`,
equal to the counter's `LEDGER_SHA` pin
(`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py:33`).

## 2. Ledger quote byte-identical to FROZEN_QUOTE — MATCH

`FROZEN_QUOTE` (`c64_calibration.py:71-75` at T0) imported from the frozen
module, compared byte-for-byte with the ledger's `classes[0].quote`:

```
ledger quote   sha256 = 465711f70cf80c77458639aebaf13963277f50086b8ccd907fe7e12bb54a6e2d  (154 bytes)
FROZEN_QUOTE   sha256 = 465711f70cf80c77458639aebaf13963277f50086b8ccd907fe7e12bb54a6e2d
LEDGER == FROZEN (byte-identical): True
```

Both carry U+2019 (`response’s`); no homoglyph/whitespace divergence.

## 3. Quote byte-identical to the [r63-correction] block quote — MATCH

`corpus/knowledge/response-header-expectations.md` at T0, the
`[r63-correction 2026-10-27]` block (starts line 224), quoted span at
line 230 (`> "The \`X-Content-Type-Options\` response header …"`).
Stripping only the markdown `> ` prefix and the surrounding ASCII double
quotes gives bytes sha256 `465711f7…6e2d` — byte-identical to both the
ledger quote and FROZEN_QUOTE. The block also names the ledger path
(`…quote-classes.json`, line 240) and both digests (lines 233-236).

## 4. matchClass collapsed-only — CONFIRMED (independently derived)

Round-50 rule (`corpus/QUALITY.md` round-50 criteria, line ~1103): substring
of retained HTML ⇒ `raw-substring`; survives only whitespace collapse ⇒
`collapsed-only`.

- `quote in raw_bytes` = False (checked at byte level on the committed blob).
- `quote in text_bytes` = True.
- ⇒ derived class `collapsed-only`, equal to ledger `matchClass`. Also
  reproduced by the lane tool `scripts/quote_class.py` (`s432_real`:
  derived=collapsed-only, selftest 4/4, exit 0).

## 5. locatedRawLines 6150-6154 — CONFIRMED (independently re-derived)

Re-executed the committed recipe
(`.ufo/waves/round-63/quote-class/extract_text.py` at T0, sha
`6b0a88cddfa3b712e8fdbe69c4c2803c816490cd43893972dfe0d39d5f362405`) over the
retained raw blob:

- `extract(raw)` output sha256 `8b90d096…f542a69` — byte-equal to the
  committed text blob (recipe reproduces the retained rendering).
- Independent minimal-range derivation (no window pin): the full-file
  brute force over all 18,915 raw lines found the unique global minimum
  span 6150-6154 (span 4); a complementary scan for any span ≤3 lines
  containing the quote over the whole file returned `[]`, so no smaller
  range exists anywhere in the blob.
- A separate implementation (regex tag-strip + `html.unescape` +
  whitespace collapse) of raw lines 6150-6154 renders to exactly the
  ledger quote (sha256 `465711f7…6e2d`).
- `awk NR` line numbering confirms raw line 6150 = `   <p>The`, 6151 =
  the `<dfn>` X-Content-Type-Options markup, 6154 ends `…request</a>.` —
  1-based inclusive, same convention the counter uses
  (`raw_lines[a-1:b]`, `c64_calibration.py:169-183`).
- Frozen counter agreement (run read-only at T0):
  `revision=4c8295fa… … recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 … met=true`, exit 0.

## Cross-checks

- Ledger unchanged across the round: `git diff --stat
  1a481315…4c8295fa -- .ufo/waves/round-63/quote-class/
  .ufo/waves/round-61/sources/S432.html
  corpus/knowledge/response-header-expectations.md` is empty; the round-63
  tip, T0 and the working tree all carry the same ledger sha `5f48e26b…`.
- Working tree tracked files match T0 byte-for-byte for the ledger, both
  blobs, the recipe and both frozen counters.
- Frozen instrument shas at T0 match the contract:
  `c64_calibration.py` = `5489eb2f…088adf`,
  `c64_quote_tool.py` = `96fd64e9…7ee2b`.
- Ledger is single-row (`classes` length 1, id `S432`); its top-level
  `recipe` field points at the committed recipe, whose sha equals the
  counter's `RECIPE_SHA` pin.
- Note-field claim ("raw lines 6150-6154 carry the field-purpose sentence
  across inline markup; the span is a substring of the committed
  flat-text rendering only") is accurate per §4/§5.

## Observed facts / inference / gaps

- Observed: everything in §1-§5 and Cross-checks (commands and outputs
  above, run at T0 committed bytes).
- Inference: none needed beyond the round-50 class rule text quoted from
  `corpus/QUALITY.md`.
- Gaps: none for this item. Note (out of scope, informational): the lane
  working tree carries an untracked
  `.ufo/waves/round-64/sources/S432.live.html`; it does not affect the
  ledger or any pinned path.

## Tooling installs

None. No pacman/uv/npm installs were needed; used system `python3` and
`git` only.
