# ExecProbeUnescape — does `html.unescape` decode character references as the HTML parser does?

Leaf executor. Lane `kake-shokunin` @ `cd3212796cab7a2afa03b638dbfafe7194df9629`. Scope: C1 bullet (c) — *"character references decoded as HTML does (named, decimal and hexadecimal; Python `html.unescape` conforms)"*. Lane read-only; sealed tree `/fast/scratch/hyaku/kake-r36/` never listed/read/statted/searched. Work in `/fast/scratch/hyaku/kake-r36w1/ExecProbeUnescape/`.

**Verdict: true for named references and for numeric references outside one narrow band; FALSE for numeric references naming 94 codepoints, where `html.unescape` deletes the character the HTML tokenizer emits. The false part is material for bullet (d): it flips a quote-match verdict in both directions.**

**Oracles.** A = `html5lib` 1.1 `HTMLTokenizer` (spec-conformant, §13.2.5.77–13.2.5.84; a separate spec-driven implementation). B = my re-implementation of the spec's reference states, written from the spec text and driven by the spec's own table fetched by GET. C = real Chromium (headless, `about:blank` + `setContent`) — a browser, i.e. what "the HTML parser does" means. D = `html.unescape` (CPython 3.14.8; identical on 3.9–3.15), the subject. A/B/C agreed on every case below, on 8000/8000 randomized fuzz inputs (seed 20261022), and all 97 curated cases.

**Sources.** S092 `.ufo/waves/round-36/sources/S092.txt` sha256 `2fb98770463f89d127d4f02bc92c9306164a530498bc78db61e8875f4496adb3` §13.1.4; `named-characters.html` sha256 `5809624955c439562238d9e9af997c1d4c916ff0f1d90942072dc152bd43d463` (217 529 B); `parsing.html` sha256 `3e839e6fc96e9cf08eb3e3d87cb689c61c04d392f9d60c228f78acca5f44fd68` (826 255 B); both GET 2026-10-22.

## Test table ("spec" = A=B=C; rows group equivalent inputs)

| inputs | class | `html.unescape` | spec | agree |
|---|---|---|---|---|
| `&amp;` `&amp` `&AMP;` | named, semicolon / legacy / case | `&` | `&` | yes |
| `&copy` `&notin;` `&notin` `&notit;` | named, no-semi / longer / longest-prefix | `©` `∉` `¬in` `¬it;` | same | yes |
| `&noti;` `&notindot;` `&notinva;` `&CounterClockwiseContourIntegral;` | named | `¬i;` `⋵̸` `∉` `∳` | same | yes |
| `&NotEqualTilde;` vs `&notEqualTilde;` | case sensitivity | `≂̸` vs `¬EqualTilde;` | same | yes |
| `&nosuchentity;` `&ampfoo` `&` `&&` | unknown / prefix+junk / bare | `&nosuchentity;` `&foo` `&` `&&` | same | yes |
| `&#65;` `&#65` `&#0000065;` `&#65abc` `&#x41zz;` | decimal, no-semi, zeros, junk | `A` `A` `A` `Aabc` `Azz;` | same | yes |
| `&#150;` `&#x96;` `&#128;` `&#x80;` `&#159;` `&#x9F;` `&#153;` | C1 range | `–` `€` `Ÿ` `™` | same | yes |
| `&#x81;` `&#x8D;` | C1 not in spec table | `\x81` `\x8d` | same | yes |
| `&#xD800;` `&#55296;` `&#0;` `&#x0;` `&#x110000;` `&#1114112;` | surrogate / null / >U+10FFFF | `\ufffd` | `\ufffd` | yes |
| `&#X41;` `&#x41;` `&#x4a;` | hex case | `A` `A` `J` | same | yes |
| `&#x;` `&#;` `&#xZZ;` `&#-1;` `&#+1;` | malformed | literal, unchanged | same | yes |
| `&amp;amp;` `&lt;script&gt;` `a &amp; b` | no double decode / encoded markup / plain | `&amp;` `<script>` `a & b` | same | yes |
| `&#x10FFFF;` `&#xFFFE;` | noncharacter, plane edge | **`''` dropped** | `U+10FFFF` `U+FFFE` | **NO** |
| `&#1;` `&#x7F;` | control 0x01 / 0x7F | **`''` dropped** | `U+0001` `U+007F` | **NO** |
| `&#xFDD0;` | noncharacter | **`''` dropped** | `U+FDD0` | **NO** |

**Named: 0 divergences.** Exhaustive sweep of all 2231 spec names x 5 suffixes (11 155 inputs) and all 106 legacy no-semicolon identifiers x 5 suffixes: 0 divergences. `html.entities.html5` in CPython is identical to the spec table fetched today: 2231 entries each, no entry on one side only, no value differences.

**Numeric: 188 divergences.** Every value 0..0x110010 in `&#N;` and `&#xN;` form (2 228 258 inputs): 188 divergences over **94 distinct codepoints** — exactly CPython's `_invalid_codepoints` set minus the C1 entries the C1 table claims: controls `U+0001–0008`, `U+000B`, `U+000E–001F`, `U+007F` (28 values), noncharacters `U+FDD0–FDEF` (32) and `U+xFFFE/U+xFFFF` for planes 1..16 (34). `/usr/lib/python3.14/html/__init__.py` `_replace_charref` does `if num in _invalid_codepoints: return ''`. The spec's end state (parsing.html §13.2.5.84, extracted to `spec-end-state.txt`) never deletes: a noncharacter is a *parse error only*, and "Append a code point equal to the character reference code" still happens. Chromium agrees with the spec text on all of them. Fuzz (8000 inputs, seed 20261022, no `<`/`>` so only reference handling varies): 1550 divergences, **every one contains at least one dropped codepoint** — 0 unexplained.

## Does it matter in text content (outside attributes)?

Yes, for bullet (d). `html.unescape` removes the character; the parser keeps it. After (d)'s NFKC + `str.isspace()` deletion, 178 of the 188 divergent forms still differ and flip the verdict **both ways** (`probe5.py`): body `x&#x1;y` quote `xy` -> unescape holds / spec `quote_missing`; body `x&#x1;y` quote `x\x01y` -> unescape `quote_missing` / spec holds; same for `&#xFDD0;`. Only 10 of 188 forms are erased by the whitespace deletion (the `U+000B`, `U+001C–U+001F` band, where `str.isspace()` is true). **Attribute context is a separate divergence** (informational; (c) works on text): spec §13.2.5.78 does not decode a legacy name without `;` before `=` or an ASCII alphanumeric inside an attribute, while `html.unescape` always decodes (`&amp=1` -> `&=1`, `&ampx` -> `&x`; Chromium in an attribute keeps `&amp=1`).

## `html.parser.HTMLParser(convert_charrefs=True)` text vs `html.unescape`

Identical on all 97 curated cases and on the whole divergence set, because CPython's `HTMLParser` calls `html.unescape` internally for text data (`/usr/lib/python3.14/html/parser.py`: `self.handle_data(unescape(rawdata[i:j]))`). So `HTMLParser` is **not** an independent check on `html.unescape` — it inherits the same 94-codepoint defect. It differs in not decoding inside `script`/`style` (`x<script>&amp;</script>y` -> `x&amp;y`), which (c) handles by removing those contents.

## Judgement on the contract's "conforms" sentence

The bullet (c) sentence *"…decoded as HTML does (…; Python `html.unescape` conforms)"* is **overstated**. `html.unescape` conforms for every named reference and every numeric reference except 94 codepoints (188 of 2 228 258 numeric forms), where it deletes a character the HTML parser emits. It is safe as a shorthand only if callers accept `html.unescape`'s deletion as the definition of "HTML does" — but then the tool is not decoding as HTML does, "conforms" is false, and any registry row whose quote legitimately contains a control character, a noncharacter or a plane-edge `U+FFFE`/`U+FFFF` will be reported `quote_missing` although the source contains it. The L1 must pick one and state it: **(1)** keep `html.unescape` as the definition — then write "decoded as `html.unescape` decodes them", not "as HTML does", and accept that `U+0001`, `U+007F`, `U+FDD0–FDEF` and plane-edge noncharacters are erased from the text before the quote comparison; **(2)** decode as HTML does — then `html.unescape` cannot be used directly for the numeric branch: the C1 table (§13.2.5.84), the surrogate/null/>U+10FFFF -> U+FFFD rules, and the "keep the code point, only raise a parse error" rule for controls and noncharacters must be implemented explicitly. `html.unescape` stays usable for the *named* branch (verified 0 divergences over the whole table).

## Reproduction and artifacts

`cd /fast/scratch/hyaku/kake-r36w1/ExecProbeUnescape` — `python3 probe3.py` (97 curated cases, 3-way oracle table, exit 0), `probe4.py` (2 228 258 numeric + 11 685 named inputs, exit 0), `probe5.py` (contract (d) impact, exit 0), `probe6.py` (randomized fuzz, exit 0). sha256: `probe3.py` `c66f921efe23a84d228e0d759492369a8cd82c70773f98e8845d9bb13f0d1c42`; `probe4.py` `71c070e9d5d3cd8a28a2f4d62f80d18efad12f82508220dfc9d9f06dc5f3dac3`; `probe5.py` `6ce188dd735d5839ebc446f04fe9caaf51eaed68d716b63870d07ae8f8717cb0`; `probe6.py` `d71cf5e502cd06a4c89ab439198487e71afa552ddbf861e73bf63fa7b4e58906`.

## Tooling installed

`html5lib==1.1` (+ `six==1.17.0`, `webencodings==0.6.1`) into a local uv venv at `/fast/scratch/hyaku/kake-r36w1/ExecProbeUnescape/.venv` via `uv pip install` (PyPI, CPython 3.15.0); reason: an independent WHATWG-conformant tokenizer oracle. No system packages; no `pacman` transaction (host-wide pacman pause respected). Chromium was already present, driven headless against `about:blank` only — no requests to any operator-owned site. No process left running.

## Risks / not verified

- **Not verified: how the sealed cases were authored.** If generated with `html.unescape` (as the contract's parenthetical implies), a spec-faithful tool would fail them; if generated from a real parser, `html.unescape` fails them. The sealed tree was not touched, so this is unresolved from here — the L1 must check which.
- Not verified: CPython < 3.9; the drop-set was present unchanged on 3.9–3.15 (8 versions x 8 inputs). `html5lib` 1.1 is from 2020, but Chromium independently confirms the same answers, so the oracle is not the weak link. The divergence is invisible unless a body or quote contains one of those 94 codepoints; real-world text rarely does, but the claim is stated absolutely and a future case could probe it.
