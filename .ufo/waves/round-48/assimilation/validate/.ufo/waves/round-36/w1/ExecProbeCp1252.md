# ExecProbeCp1252 — does contract (f)'s "invalid bytes decode to U+FFFD" agree with WHATWG windows-1252 for 0x00-0xFF?

Seat: KakeR36.ExecProbeCp1252 (leaf). Lane: kake-shokunin, round 36 wave 1. Sealed tree untouched.

## Verdict

**Refuted for any tool built on Python's `cp1252` codec; holds only when the tool uses the WHATWG index.** The WHATWG windows-1252 index is *total* over 0x80-0xFF (128 contiguous pointers, 0..127), so under WHATWG **no byte 0x00-0xFF is invalid** and contract (f)'s "invalid → U+FFFD" clause never fires for windows-1252. Python's `cp1252` codec leaves five bytes undefined; with `errors="replace"` each yields **U+FFFD** where WHATWG yields the matching C1 control character. 5 of 256 bytes differ.

## Table of differing bytes (both decodings)

| byte | WHATWG windows-1252 (index) | Python `b.decode('cp1252','replace')` | Python strict `cp1252` |
|---|---|---|---|
| 0x81 | U+0081 (`<control>`) | U+FFFD | `UnicodeDecodeError` |
| 0x8D | U+008D (`<control>`) | U+FFFD | `UnicodeDecodeError` |
| 0x8F | U+008F (`<control>`) | U+FFFD | `UnicodeDecodeError` |
| 0x90 | U+0090 (`<control>`) | U+FFFD | `UnicodeDecodeError` |
| 0x9D | U+009D (`<control>`) | U+FFFD | `UnicodeDecodeError` |

All other 251 bytes agree exactly (0x00-0x7F ASCII identity per S090 §9.1; 0xA0-0xFF Latin-1 order; the other 123 high bytes agree with WHATWG's index).

## Evidence

Commands run in `/fast/scratch/hyaku/kake-r36w1/ExecProbeCp1252`, `TMPDIR` set, each `timeout`-capped:

1. `timeout 60 curl -sS -o index-windows-1252.txt https://encoding.spec.whatwg.org/index-windows-1252.txt` → exit 0. sha256 `2c5fa192d566f92b8b9e6e116255b1f94016b4ece5b9dacb3b98be70b8c60795`; 5667 bytes; header `Identifier: e56d49d9176e9a412283cf29ac9bd613f5620462f2a080a84eceaf974cfa18b7`, `Date: 2024-09-18`. Non-comment entries: 128, pointers contiguous 0..127 (verified `set(m)==set(range(128))`); pointers 1/13/15/16/29 at lines 8/20/22/23/36 → bytes 0x81/0x8D/0x8F/0x90/0x9D.
2. Python compare over all 256 bytes (index vs `cp1252`/`replace`): **5 differences**, exactly the table. Captured at `table_and_probe.txt`, sha256 `e41296f6a9e7141dad567e146d07a7c7993d17a1f3fb93bc24e1ee2544d44c06`.
3. Independent cross-check, Node v24.21.0 `new TextDecoder('windows-1252')` over all 256 single-byte inputs → **0 differences** vs the index (`node_cp1252.json`, sha256 `68af8a946d866a753d270a7d274b58198e6d8ab79bda72194494df37cda7fc64`, exit 0). So the divergence is Python's codec, not my reading of the index.
4. Scope check — the U+FFFD clause is safe for the other three encodings (Python `replace` vs Node `TextDecoder`): all 65 536 two-byte UTF-8 inputs → 0 mismatches (`node_utf8_2b.json`); all 1 376 256 three-byte inputs with lead 0xE0-0xF4 → 1 mismatch, `EF BB BF`: Python `'\ufeff'` vs WHATWG `''`, the BOM case contract (f) already handles by dropping the mark (`node_utf8_3b.json`). UTF-16LE/BE lone surrogates (`d800`, `dc00`, `d80041`, `dc00d800`) agree (U+FFFD both sides).

## Which sentence of (f) is decisive

The decisive sentence is the label-table one, not the U+FFFD one:

> "Otherwise the `charset` parameter, trimmed, with surrounding double quotes removed and matched ASCII case-insensitively, picks the encoding by the WHATWG Encoding label table; the tool supports the labels of UTF-8, UTF-16BE, UTF-16LE and windows-1252 (so `iso-8859-1`, `latin1`, `ascii` and `us-ascii` mean windows-1252)."

It is decisive because it makes the **WHATWG Encoding standard the authority for what "windows-1252" *is***, i.e. for the byte→code point map. Only then does the closing sentence ("Bytes invalid in the chosen encoding decode to U+FFFD") have a defined subject: "invalid" means "absent from index-windows-1252.txt" per S090 §9.1 ("If codePoint is null, then return error"), and that set is empty for windows-1252. A closure reading the U+FFFD sentence as primary — or implementing the label table with Python's `cp1252` codec — silently mutates five byte values.

## Consequence for the build (and for case outcomes)

A `cp1252`-based decoder can flip contract (d) both ways, so this is not cosmetic:
- body bytes `41 81 42 81`, quote containing U+0081 → WHATWG holds, Python-cp1252 reports `quote_missing`;
- same body, quote containing U+FFFD → WHATWG reports `quote_missing`, Python-cp1252 holds;
- UTF-8 bytes under a windows-1252 label (the key-v2 case shape): text `'Â\x81'` → body `c382c281`; WHATWG decodes `'Ã‚Â\x81'` (quote `'Â\x81'` holds), Python decodes `'Ã‚Â�'` (miss).

Recommendation to the tool builder: do not call `bytes.decode('cp1252', ...)`. Use the WHATWG table (128-entry high half, ASCII identity below 0x80). Adjacent traps in the same sentence: Python `latin-1` differs from WHATWG windows-1252 on **27** bytes and Python `ascii` on **128**, so the `iso-8859-1`/`latin1`/`ascii`/`us-ascii` labels must not be routed to those codecs.

## Deliverables (sandbox; absolute paths)

- `/fast/scratch/hyaku/kake-r36w1/ExecProbeCp1252/whatwg_cp1252.py` — 256-entry WHATWG table + `whatwg_decode_cp1252()` + self-check asserting exactly the five differing bytes; sha256 `203dbfcf58cdee5cb3fa88b28ae631b5883c4b35733cf12f546b688114bf1267`; `python3 whatwg_cp1252.py` exit 0.
- `/fast/scratch/hyaku/kake-r36w1/ExecProbeCp1252/index-windows-1252.txt` (fetched source of truth).
- `/fast/scratch/hyaku/kake-r36w1/ExecProbeCp1252/{table_and_probe.txt,node_cp1252.json,node_utf8_2b.json,node_utf8_3b.json}`.

## Not verified / limits

- No sealed case was read, listed or scored; the counter was not run (no key). The predicate is untouched.
- Node's `TextDecoder` is ICU-backed, not normative; it corroborates, it does not prove. The proof of index content is the fetched `index-windows-1252.txt` plus S090 §5 and §9.1 text.
- Only UTF-8, UTF-16LE/BE and windows-1252 were probed; other WHATWG labels are out of contract scope.
- No build, lint, test or formatter was run for the tool; no packages installed (no tooling changes).
- `corpus/SOURCES.md` shows as modified in the lane; that change is not mine (the L1 is writing registry rows).
