# ReopenGateS100 — r38 w2 falsify seat (freshness)

Target: S100 Gate line (round-38.md:43-46) and SOURCES.md:108 vs the live page. HEAD `b7d821e3`;
ticket tip `adab4c7e`; both files identical between them (`git diff adab4c7e..HEAD -- …` empty,
exit 0). Hashes: round-38.md `8986f011…12b605`; SOURCES.md at my read `d666b4e4…1f42650`.
Concurrent (not mine): another seat edited SOURCES.md at 04:51:44Z (diff only S034/S101 `used-by`;
S100 row byte-identical). I wrote only this report and sandbox files.

## Fetch

`curl -sS -L -D headers.txt -o json.html -w '…' https://docs.python.org/3/library/json.html` at
2026-10-23T04:45:42Z → `http_code=200 num_redirects=0 bytes=115104`, exit 0. `sha256sum json.html`
→ `234b80bf…a07f792e` (full hash in Pointers), exit 0. Headers: HTTP/2 200, no Location,
`last-modified: Fri, 23 Oct 2026 01:40:01 GMT`, `age: 3624`, `x-cache: HIT, HIT`; byte-identical to
the w1 receipt (`/fast/scratch/hyaku/kake-r38w1/ScoutPythonJson/receipt-json.html.txt`,
`access_utc=2026-10-23T04:30:22Z`, same full hash).

## Verdicts

1. **Quote present verbatim — HOLDS.** Tag-stripped, whitespace-normalised page text contains the
   18-word sentence exactly once: “It also understands NaN, Infinity, and -Infinity as their
   corresponding float values, which is outside the JSON spec.” (json.html raw 599–600;
   `page_occurrences: 1`; byte-equal to round-38.md:44-45).
2. **Gate location `(json.loads)` — WRONG.** The sentence is inside `class json.JSONDecoder`
   (`<dt … id="json.JSONDecoder">` json.html:562; its `<dl class="py class">` spans 561–659; the
   sentence follows the `json-to-py-table` table at 566–598). The `json.loads` object is a separate
   `<dl class="py function">` (542–556) with **zero** `NaN`/`Infinity` occurrences (count over
   chars 58160–62060: 0/0); it only says “using this conversion table” (548). The Gate's own
   pointer `w1/ScoutPythonJson.md` says `json.load` — also wrong (that dl, 457–540, holds the
   `parse_constant` prose at 503, not this quote). CORPUS.md rule 1 requires the quote's location;
   the recorded one sends a verifier to a section that does not contain it.
3. **Access facts `HTTP 200`, sha256 `234b80bf…a07f792e`, accessed 04:30:22Z — HOLDS.** My
   independent GET 15 min later returned 200, 0 redirects, same full hash and byte count; the
   truncation matches (prefix `234b80bf`, suffix `a07f792e`). The 04:30:22Z wall clock is evidenced
   only by the w1 receipt plus byte identity.
4. **Row title/version “Python 3.15.1 documentation” — HOLDS.** `<title>json — JSON encoder and
   decoder — Python 3.15.1 documentation`; `3.15.1` is the page's only version string.
5. **Row scope/teaches/anchor — HOLD AS WRITTEN; lane use is over-scoped.** “Infinite and NaN
   Number Values” exists (json.html:877) and states “Despite that, by default, this module accepts
   and outputs Infinity, -Infinity, and NaN …”; `parse_constant` prose is at json.html:503. But
   `scope` limits S100 to non-finite constants and `parse_constant`, while the lane cites it for
   integer length: PROVINCE.md:315 (“robotsStatus of any length … unused long numbers change
   nothing (S034, S100)”) and corpus/knowledge/robots-txt-rules.md:100 (“4300-digit conversion
   limit … (S100 points to that limit)”). `grep -n '4300' json.html` → exit 1, no match; the page
   only links to `../builtins/stdtypes.html#int-max-str-digits` (533), and stdtypes has no SOURCES
   row. The 4300 figure has no in-registry source. The anchor cell also omits `json.JSONDecoder`,
   the object holding the Gate's quote.
6. **Row `status mined`, `used-by` — HOLDS.** corpus/knowledge/robots-txt-rules.md (S100 at 1, 89,
   94, 100) and corpus/lessons/round-38.md (43–46, 56–58) cite it; CORPUS.md:107 limits `used-by`
   to knowledge entries/lessons, so the absent PROVINCE.md:315 cite is per contract.
7. **Lesson “S098, S099, S100 `—` → `mined`” — minor imprecision, not falsified.** All four rows
   are absent at base (`git show af43a50:corpus/SOURCES.md | grep -c '^| S100 |'` → 0; tip → 1),
   so no committed old cell exists; the shorthand reads as new-row status, not a logged old→new.
## Pointers

- corpus/lessons/round-38.md:43-46; corpus/SOURCES.md:108 (docs/A, mined, opened 2026-10-23,
  recheck on-release, used-by `corpus/knowledge/robots-txt-rules.md, corpus/lessons/round-38.md`).
- json.html:542-556 `json.loads` (0 NaN/Infinity), 561-565 JSONDecoder start, 566 table id,
  599-600 quote, 877 section, 533 stdtypes link.
- Sandbox `/fast/scratch/hyaku/kake-r38w2/ReopenGateS100/json.html` sha256
  `234b80bf7385ea72e198521156d012cbe8997bab428740468f46f881a07f792e` (115104 B); `headers.txt`
  sha256 `5969f9b4c3ca5cf3b16f616dc3ecfd45b16c20ecc7320057778e4fd991db3d11`.
## Not done / unknowns

- 04:30:22Z cannot be re-observed; verified only by the w1 receipt + byte identity.
- Did not run counters/selftests; `scripts/robots_audit.py:464-465` passes `parse_int` and
  `parse_constant`, so the long-integer claim is implemented though its registry support stays
  outside S100's declared scope.
- No owned site opened; no mutating git/jj command; no tool installed or upgraded.
