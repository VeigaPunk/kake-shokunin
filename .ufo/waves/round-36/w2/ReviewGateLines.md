# Round 36 wave 2 — ReviewGateLines (falsify: Gate lines S088–S094)

Axis: freshness. Attacked `corpus/lessons/round-36.md` `## Gate` → `### Source openings` (lines 35–44).
Result: CLEAN — all 7 lines verified; no mismatches. One future-date observation flagged.

## Verifying commands (all exit 0 unless noted)

Per-row whitespace-normalised substring checks, run verbatim in
`.ufo/waves/round-36/sources/` (quote taken byte-exact from the lesson line via `re.search(r'quote “(.+?)” \(',l)`):

```
SID=S088 Q='the target resource has been assigned a new permanent URI' python3 -Bc 'import os,re,sys
t=re.sub(r"\s+"," ",open(os.environ["SID"]+".txt",encoding="utf-8").read())
ok=re.sub(r"\s+"," ",os.environ["Q"]) in t
print(("PASS" if ok else "FAIL"),os.environ["SID"]); sys.exit(0 if ok else 1)'   # exit 0 → PASS S088
SID=S089 Q='For each URI reference (R), the following pseudocode describes an algorithm for transforming R into its target URI (T):' … # exit 0 → PASS S089
SID=S090 Q='A byte order mark has priority over a label' …                          # exit 0 → PASS S090
SID=S091 Q='If two strings are compatibility equivalents, then toNFKC(x) = toNFKC(y)' … # exit 0 → PASS S091
SID=S092 Q='Raw text elements script' …                                             # exit 0 → PASS S092
SID=S093 Q='the HTTP status code used for permanent redirecting' …                  # exit 0 → PASS S093
SID=S094 Q='These redirections are meant to last forever.' …                        # exit 0 → PASS S094
```
(S092 survives normalisation only because the retained text renders "Raw text elements script , style" — the extraction inserts spaces around punctuation; the raw HTML reads "Raw text elements: script, style". The claim is only "whitespace-normalised substring", so PASS stands.)

Word counts: `len(qn.split())` → 10, 19, 9, 10, 4, 8, 7 — each equals the stated count, all ≤ 25.

Locations (context printed before each quote index): S088 `15.4.2. 301 Moved Permanently` precedes quote (S088.txt idx 320694); S089 `5.2.2 . Transform References` precedes (idx 71114); S090 `8.1.1. UTF-8 decoder` precedes (idx 53233); S091 uniqueness/Normalization-Forms prose precedes (idx 39003); S092 §13.1.2 category list context (idx 4398); S093 lead paragraph (idx 1770); S094 `Permanent redirections` heading immediately precedes (idx 3181). Every line names a location that matches the retained text.

Decisions vs SOURCES rows: `awk -F'|' 'NR>=96&&NR<=102{print $2" -> "$9}' corpus/SOURCES.md` →
S088–S092 `mined` (Gate: admit/status mined), S093 `rejected`, S094 `rejected` (Gate: reject/status rejected). MATCH all 7.

Receipts: `receipts.json` `accessedUtc`/`status`/`url`/`textSha256` — all HTTP 200, URLs and timestamps byte-equal to the Gate lines (S088 01:08:56Z … S094 01:09:01Z); recomputed sha256 of each `S0XX.txt` equals `textSha256` (7/7).

## S094: scribe-draft vs L1 reject

- Scribe draft proposed admit: `w1/ScribeSourcesRows.md` ("S094 admitted at tier B…"), `w1/ScribeGateLines.md` ("S094 admit / B / docs / mined").
- Gate line rejects and cites `ScoutReopenS094`. Support verified: scout's "Recommendation: reject (tier B if kept, narrowly scoped)" rests on the blanket-3xx claim, which I re-located in `S094.txt` idx 2711 — "Redirect responses have status codes that start with 3 , and a Location header…" — immediately under the `Principle` heading (heading at 2605), and on S088 §15.4.5/§15.4.1 contradictions (304 has no Location; 300 Location SHOULD). Both quotes the Gate line says are "located there" are indeed located in `ScoutReopenS094.md` (offsets 3317 and 2711). The Gate prose faithfully mirrors the scout; the L1's reject is supported.
- SOURCES.md S094 status cell carries the same REJECTED rationale — consistent.

## Observations / not verified

- `receipts.json` timestamps are 2026-10-23T01:08:56Z–01:09:01Z and the scout's live `date:` header is Fri, 23 Oct 2026 — one day in the future relative to today (2026-10-22). All artifacts agree with each other; the Gate lines faithfully mirror the receipts. Flagged for the L1; not a Gate-line defect.
- Did not re-open any source live (no URL named for this seat; no network requests made). Quote checks are against retained snapshots only — the Gate claim "byte-identical to the scout's fetch" is separately supported for S094 by scout body sha256 `4c73d89c…` = `receipts.json` `bodySha256`; ScoutReopenS088–S093 byte-identity reports were read only at title level, not re-verified.
- No tools installed; no processes left running; only this file written in the lane.

Report path: `.ufo/waves/round-36/w2/ReviewGateLines.md`
