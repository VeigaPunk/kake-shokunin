# ReopenGateS101 — WHATWG URL Standard (r38 w2, falsify)

Attacked `corpus/lessons/round-38.md:47-51` (S101 Gate line) and `corpus/SOURCES.md:109` (row).
Independent GET of the named public URL, 14m54s after the recorded access; no owned hosts, no
installs, no lane mutation. Sandbox `/fast/scratch/hyaku/kake-r38w2/ReopenGateS101/`; two intermediate
extractors exited 1 on bad regexes, every fact below is from the exit-0 rerun.

## Access facts — HOLD
`curl -sS -o url.html -w 'status=%{http_code} size=%{size_download}' https://url.spec.whatwg.org/`
exit 0, `status=200 size=703601` at 2026-10-23T04:45:11Z; `content-length: 703601`,
`last-modified: Mon, 19 Oct 2026 11:58:10 GMT`, `etag: "6ad605d2-abc71"`.
sha256 `08cb42a9a8575dab006676378c846fdd8a72d06897c27929aa51eaf099656be4` = the row's full hash, not
merely its `08cb42a9…` prefix. `cmp` vs retained copy
`/fast/scratch/hyaku/kake-r38w1/ScribeSourcesRows/sources/whatwg-url.html` → exit 0, same hash.
Page text "URL Living Standard — Last Updated 19 October 2026" supports "last updated 2026-10-19"
beyond the header.

## Quote — present verbatim; section tag wrong
§4 "4. URLs" (h2 offset 144629) lead-in bullet, offset 145327, rendered:
"The URL parser takes an arbitrary scalar value string and returns either failure or a URL. It might
also record zero or more validation errors." Normalized against the lesson's line wrap: exact prefix,
**1 occurrence** in the rendered document, sentence sha256
`a96756e08aa95870cacab9efea7900e07d388377d7c04ed67a6b42cbfa0f60fc`.
§4.4 ("4.4. URL parsing", offset 190432) does **not** hold it; §4.4 opens "The URL parser takes a
scalar value string input, with an optional null or base URL base (default null) and an optional
encoding encoding (default UTF-8), and then runs these steps:". The contiguous string is absent from
the HTML because "scalar value string" is an `<a>` to Infra — verbatim in rendered text only.

## "WHATWG strips and removes the characters (i) rejects" — OVERSTATED
(i) set = `[\x00-\x20\x7f"<>\\^`{|}]` (`scripts/robots_audit.py:149`), 43 code points. Node v24.21.0
`new URL` matrix (`excl.js`, exit 0), each cp mid-path: removed anywhere **3** (U+0009/000A/000D);
stripped at input boundaries **33** (U+0000–U+0020; `edge3.js` leading and trailing lists);
percent-encoded **38** (C0 00–08/0B/0C/0E–1F, space→%20, U+007F→%7F, `"` `<` `>` `^` `` ` `` `{` `}`);
`\`→`/` (1); preserved raw **1** (`|`); leading U+007F **throws** `TypeError`. Spec sets match: path set =
query set + `? ^ ` ` { }`, query set = C0 set + space `"` `#` `<` `>`, `|` only in userinfo. §1.1: "A
validation error does not mean that the parser terminates." WHATWG normalizes and reports non-fatal
errors; it does not strip or remove (i)'s set.

## Row cells
Scope — accurate: parsing, non-fatal validation errors, encode sets, "not RFC 3986 URI syntax".
Anchor "Sections 1.2 Parsers and 4.4 URL parsing" — §1.2 exists but is only EOF/pointer vocabulary;
the scope cell's validation-error lives in §1.1 *Writing* and percent-encoding in §1.3 *Percent-encoded
bytes*, neither cited, and the lesson's quote is §4.
Teaches — both prongs hold: `scripts/robots_audit.py:104` is `from urllib.parse import urlsplit`, no
WHATWG dependency; the spec defines no RFC 3986 character-set rejection rule.

## Verdicts
| Statement | Verdict |
|---|---|
| Quote present verbatim | holds |
| Quote is at §4.4 | **wrong** — it is §4 lead-in; §4.4's sentence differs |
| HTTP 200 / sha256 `08cb42a9…` / last updated 2026-10-19 | holds |
| "WHATWG strips and removes the characters (i) rejects" | **overstated** — 3 of 43 removed anywhere, 33 boundary-stripped, 38 encoded + `\`→`/`, `\|` kept, one hard throw |
| Row scope cell | holds |
| Row anchor "1.2 Parsers and 4.4 URL parsing" | **overstated** (omits §1.1/§1.3 and the §4 quote site) |
| Row rejection rationale | holds |

Collateral: `w1/ScoutWhatwgUrl.md:5` says "no build date in text" — the page states it; the row is right.

## Evidence
- `/fast/scratch/hyaku/kake-r38w2/ReopenGateS101/url.html` `08cb42a9…656be4`
- `…/excl.out` `082de377daa14024bcb75e81a9286582f3a2ae34797a6b7b7e2b3d69e306df0a`,
  `…/edge3.js` `898ab4bdb448d168087a7dc9f92f517e5b30bfd22a5a1e10d6e828b0e6998a99`, `…/hdrs.txt`, `…/excl.js`, `…/edge.js` `79366f53…1d1697`
- `…/runs.txt` `9aba430e6edb4f8f847a24f5752e245b4aa2f78a88c02312d4ad467eb9f1f78b` (commands, exits)

Confidence: access facts, quote site, §4.4 defect and strips/removes verdict high; anchor-cell defect
medium (judged against the row's own scope cell). Node conformance itself `[INFERENCE]`.

Report: `.ufo/waves/round-38/w2/ReopenGateS101.md`
