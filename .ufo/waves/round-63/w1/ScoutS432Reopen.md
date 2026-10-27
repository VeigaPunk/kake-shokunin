# ScoutS432Reopen — round 63 w1

Seat: ScoutS432Reopen (leaf; no subagent dispatch). Date: 2026-10-27.
Frozen claims, counters, receipts and corpus left untouched; only this report written.

## Verdict

1. **The round-61 retained body is current.** One fresh GET of
   https://fetch.spec.whatwg.org/ returned bytes byte-identical (sha256) to
   both `.ufo/waves/round-61/sources/S432.html` and the round-63 live receipt
   `.ufo/waves/round-63/sources/S432.live.html`.
2. **The lesson Gate's S432 re-open record matches CORPUS rule 1.** It records
   the URL, the access date (2026-10-27), and a 19-word located quote
   (≤25 words), grounding the S432 row's §3.6 anchor. Independent re-open
   (this seat) confirms every field.

## Evidence — the one live GET

Command (single GET, 30 s timeout, from cwd /fast/scratch/hyaku/kake-r63/ScoutS432Reopen):

    curl -sS --max-time 30 -o fetch-live.html -w 'HTTP %{http_code} bytes=%{size_download} url=%{url_effective}\n' https://fetch.spec.whatwg.org/

Output:

    HTTP 200 bytes=1854393 url=https://fetch.spec.whatwg.org/

Received body retained at `/fast/scratch/hyaku/kake-r63/ScoutS432Reopen/fetch-live.html` (scratch, outside the repo).

## sha256 comparison (exact command/output)

Command:

    sha256sum /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/sources/S432.html \
              /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/sources/S432.live.html \
              /fast/scratch/hyaku/kake-r63/ScoutS432Reopen/fetch-live.html

Output:

    63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  .../round-61/sources/S432.html
    63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  .../round-63/sources/S432.live.html
    63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  .../fetch-live.html

Size check (`stat -c '%s %n'`, all three): `1854393` bytes each.

The Gate record's digest prefix `63b0a018…911b` expands to exactly this value,
and its byte count (1,854,393) and HTTP 200 match the fresh GET. The retained
body is therefore current as of 2026-10-27.

## Gate re-open record vs CORPUS rule 1

Rule 1 (`~/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md`,
SOURCES.md "Rules" item 1, lines 112–115 of the canonical file): a row is a
claim written only after opening the source in the round; the round lesson's
`## Gate` records, for every new row, the URL, the access date, and a
≤25-word quote with its location grounding `teaches`; non-author verification
re-opens a sample.

The round-63 Gate record (`corpus/lessons/round-63.md`, "S432 re-open record
(rule 1)") contains:

- **URL** — `https://fetch.spec.whatwg.org/` ✓ matches the S432 registry row
  (`corpus/SOURCES.md:178`, source cell) and this seat's effective URL.
- **Access date** — `2026-10-27` ✓ matches today and the round-63 `opened`
  cell of row S432.
- **Quote, ≤25 words** — "response header can be used to require checking of
  a response's Content-Type header against the destination of a request" ✓
  19 words by `wc -w` on the exact string (command output above).
- **Location** — "raw lines 6150–6154". Verified against the freshly fetched
  bytes: `sed -n '6150,6154p' fetch-live.html` returns the sentence
  "The `X-Content-Type-Options` response header can be used to require
  checking of a response's `Content-Type` header against the destination of
  a request." (spanning raw lines 6150–6154). ✓ The quote grounds the row's
  anchor (§3.6 X-Content-Type-Options header) — the located proposition named
  by the C1 criterion (`X-Content-Type-Options` / `Content-Type` /
  `destination`).

Notes on conformance:

- S432 is a held row re-opened, not a new row, so rule 1's "for every new row"
  clause is satisfied vacuously for row creation; the record nonetheless
  supplies all three rule-1 fields plus digest evidence. No registry cell was
  added or changed (S432 stays `mined`; no-harm holds — read-only inspection
  only).
- The quote is a whitespace-collapsed span of a multi-line raw-HTML sentence;
  that is exactly the `collapsed-only` class the round-63 correction admits
  under the round-50 quote-class rule, consistent with
  `.ufo/waves/round-63/quote-class/quote-classes.json` and the
  `markup_collapsed_only` / `s432_real` selftest cases.
- This seat is the rule-1 "non-author verification re-opens a sample" step for
  S432: independent of the round-63 author-side Gate record, with matching
  result.

## No installs, no mutations

No tools installed; no pacman; no git/jj mutations; no writes outside this
report path and the scratch fetch body.
