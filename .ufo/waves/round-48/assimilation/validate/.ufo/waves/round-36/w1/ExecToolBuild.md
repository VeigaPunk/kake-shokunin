# Round 36 w1 — ExecToolBuild seat report

Seat: KakeR36.ExecToolBuild. Built `scripts/source_recheck.py` to the C1 public contract at cd3212796cab7a2afa03b638dbfafe7194df9629. No sealed-case tree was touched (nothing under /fast/scratch/hyaku/kake-r36/ was listed or read).

## Deliverables (sandbox)

- `/fast/scratch/hyaku/kake-r36w1/ExecToolBuild/source_recheck.py` (sha256 `577b2d7d028964e06152f5a7b792141e586045eaa8ec9262ee7f416ba5510d48`) — identical to the landed file in `clone/scripts/source_recheck.py`.
- `/fast/scratch/hyaku/kake-r36w1/ExecToolBuild/patch.diff` (sha256 `7ca525cdcca832bd28892fede44dcd1d7e5c58b8f8357d16642e755c26437121`) — `git diff` vs cd321279 adding only `scripts/source_recheck.py` (1 file, +629). Verified applies cleanly (`git apply --check`) on a fresh clone at cd321279.
- Tool: python3 stdlib only (json, os, re, sys, unicodedata, html). Reads only the manifest and the body files it names; no network, no writes, no subprocess, no environment reads.

## Self-checks (all in `/fast/scratch/hyaku/kake-r36w1/ExecToolBuild/cases/`)

Ran `python3 -B scripts/source_recheck.py --manifest <case>/manifest.json` for 43 cases (28 + 15 extras). Every bullet (a)–(g) covered plus verdict/exit-64/output-shape. Summaries (exit code / verdict / findings, `check` projected):

- `c01_clean_html` clean text/html + entity + comment + script → **0/clean/[]** (HTML rules hold; quote "Hello world" found after NBSP→NFKC strip).
- `c02_quote_missing` → **1/failed-policy/[quote_missing]**.
- `c03_gone` (404), `c39_410` → **1/failed-policy/[gone]**; `c04_http_error` (500), `c26_204` (other 2xx) → **1/failed-policy/[http_error]**.
- Redirects: `c05_moved` (301→301→200) → **1/[moved target=https://example.com/new2]**; `c06_tmp_first` (302 first) → **0/clean/[]** (no moved); `c07_perm_then_tmp` (301→308→302→200) → **1/[moved target=https://example.com/two]** (leading permanent run); `c31` absolute location → target `https://other.com/x`; `c32` `../c` → `https://example.com/c`; `c33` `//host/path` → `https://host/path`; `c34` fragment kept in target, base fragment not inherited → `https://example.com/c#new`; `c35` `?y=2` → `https://example.com/a/b?y=2`. RFC 3986 §5.2 resolution verified against all 23 RFC 3986 §5.4.1 normal examples (23/23 match).
- Media types: `c08_plain_ref` (text/plain, `&amp;` not decoded) → **0/clean**; `c09_unsupported_type` (application/json) → **1/[unsupported_type]**; `c10_charset_unsupported` (shift_jis) → **2/could-not-evaluate/[charset_unsupported]**; `c40` quoted charset `"utf-8"` → clean; `c11_bom` (UTF-8 BOM overrides shift_jis) → clean; `c13_utf16le` (FF FE BOM) → clean; `c12_iso88591` → `c42_latin1` (windows-1252 labels) → clean; `c43_default_utf8` → clean.
- HTML text: `c22_xhtml_script`, `c24_title` (title text kept), `c25_template_style` (mixed-case raw elements), `c30_entity_quote` (`&lt;` quote), `c36_attr_script` (attrs + uppercase end tag), `c37_lt` (literal `<` kept), `c41_num_entities` (decimal/hex) → all clean. Unterminated `<script>` drops the rest (HTML raw-text semantics), `c37`-style hostile bodies fine.
- (d) `c23_nfkc` (fullwidth quote) → clean; `c28_ws` (whitespace-run quote) → clean; matching is case-sensitive (c01 original lowercase quote → quote_missing, corrected fixture "Hello world" → clean).
- (g): `c14_not_json`, `c15_version`, `c16_checks` → **2/input_invalid, checksEvaluated 0, check null**. `c17_escape` (body `../escape.txt` + a second good check) → **2/check_invalid (check "a"), checksEvaluated 1** — other checks still evaluated. `c18_abs`, `c19_missing` → check_invalid; `c20_badcheck` (missing id, bad url, empty quote, empty hops, last-hop-redirect, non-object) → 6× check_invalid with null id where id unusable. Body path `sub/../b.html` (inside) valid; `sub/../nope.html` invalid; symlink-to-file counts as regular file (ospath.isfile).
- Verdict mix: `c27_mixed` (one clean + one quote_missing) → **1/failed-policy, checksEvaluated 2**; combo case (moved + unsupported_type + charset_unsupported) → **2/could-not-evaluate** per contract.
- Exit 64 usage: no args, unknown flag, missing `--manifest` value, extra positional → all `exit=64` with usage on stderr, nothing on stdout.
- Performance: 5 MB+ HTML body (repeated script/entities/comments) → 0.34 s; hostile body of 2.5M `<` without `>` → 0.48 s; unterminated script case → 0.07 s. No quadratic scans (linear `str.find`/regex-based processing; html.unescape per contract).

## Open-point choices (contract silent or ambiguous)

1. **RFC 3986 §5.2 strict** (not urllib.urljoin's non-strict variant): a reference with a defined scheme wins wholesale (`http:g` → `http:g`); dot segments removed during resolution; target keeps the reference's own fragment; base fragment never inherited (matches "Fragment inheritance out of scope"). Validated against RFC 3986 §5.4.1 normal examples.
2. **`moved` target** = resolved location of the last hop of the leading permanent run only (resolution chain stops at the first temporary hop), in addition to the final-status finding (e.g. moved+gone both present).
3. **Media-type check before charset**: unsupported media type → exactly one `unsupported_type` finding, no charset read/`charset_unsupported` (bullet e short-circuits f).
4. **windows-1252 decoded with Python codec `cp1252` + errors="replace"** (WHATWG's index windows-1252 actually maps undefined bytes 0x81/0x8D/0x8F/0x90/0x9D to C1 controls; contract's "invalid bytes → U+FFFD" and python3-stdlib-only reading favor the codec; divergence only on those 5 bytes).
5. **Unterminated comment/raw element runs to end of document** (HTML semantics per S092: `<!--`/`<script>` without a closer consume the rest); a `<` not followed by an ASCII letter/`/`!` is kept as text; a tag without a closing `>` is left as text.
6. **`location` required non-empty string on redirect hops**; last hop's `location` (if any) must be a string but is not read; last hop must not be a redirect status; status must be a JSON integer in 100–599 (booleans rejected).
7. **Manifest `version` accepted when numerically 1 (int or float), booleans rejected**; manifest read as strict UTF-8 JSON (BOM → input_invalid).
8. **Body containment by lexical normpath** (absolute, `..` escape, missing, non-regular-file → `check_invalid`); symlinks followed (isfile); only read when final status is 200.
9. **`checksEvaluated` counts non-`check_invalid` checks; `input_invalid` → 0**; findings order not significant (counter compares multiset).

## Not verified

- Sealed cases themselves (outside lane, no key) and the counter run — parent owns scoring.
- `actions`/publishing tooling; only the tool was written.
