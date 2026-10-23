# ReopenGateS011 — re-open of the S011 Gate line and row used-by (freshness)

Item: verify the S011 quote, section, access claims and the S011 row's used-by change live; note drift since
02:50Z. Read-only against the lane; cloning and extraction in
`/fast/scratch/hyaku/kake-r37w2/ReopenGateS011/`. Measured tip `79d3c780`; `git diff --stat 79d3c780 --`
on `corpus/lessons/round-37.md`, `corpus/SOURCES.md`, `corpus/knowledge/robots-txt-rules.md`,
`scripts/robots_audit.py` is empty at live HEAD `a5ae0280` (exit 0), so every read below is the measured tip.

## Commands and observed output

1. `curl -sS -o rfc9309-live.html -w 'HTTP:%{http_code} SIZE:%{size_download} ...' --max-time 120
   https://www.rfc-editor.org/rfc/rfc9309.html` → exit 0, `HTTP:200 SIZE:82367 TIME:0.19`,
   at `2026-10-23T03:44:51Z`; `sha256sum` → `bbaa280636d3e38f0a1a130a5ce40e9753db1ed18c860945b0bf795ff8dc1a87`.
2. `gzip -dc .ufo/waves/round-37/sources/S011.html.gz | sha256sum` → the same `bbaa2806…1a87`.
   The retained body at 02:50:49Z and my 03:44:51Z body are the same bytes: **no body drift in 54 min.**
3. Re-applied the receipt's own `textRule` (`fetch_sources.py:38-43`) to the live body:
   `textSha256 8e632e483ba4c6c9808a1436d3912079b1856e77d52ba2ca7245dc8d39259cf3`, 3268 words —
   equals `receipts.json` S011 `textSha256`/`textWords`; `cmp` against `sources/S011.txt` → exit 0,
   `BYTES_IDENTICAL`. The gate line's "byte-identical to the scout's live extraction" is reproducible
   from the live page now, not just asserted.
4. `curl -sSI …` at `2026-10-23T03:45:34Z` → `HTTP/2 200`, `etag: W/"fb45b793cb4e0556a014c336d8121b5a"`
   — same etag wave-1 `ScoutReopenS011.md` recorded on its 03:23/03:26 GETs; no `Last-Modified`.
5. `grep -oF 'the crawler MUST assume complete disallow' sources/S011.txt | wc -l` → **1** (exit 0);
   offset 14857 in the extracted text, with `2.3.1.4.` at 14708 and `2.3.1.5.` at 15229 → the quote lies
   inside Section 2.3.1.4. Raw-HTML check: `id="section-2.3.1.4"` at byte 62334, `id="section-2.3.1.5"`
   at 63495; the tag-stripped segment contains the quote (`QUOTE IN SEGMENT: True`). Section heading is
   `2.3.1.4. "Unreachable" Status`. Words: **6**. Quote found: **yes, section 2.3.1.4, exactly once**.
6. Row check, `corpus/SOURCES.md:19` (one row: `grep -c '^| S011 '` → 1). `git log -p -3 -- corpus/SOURCES.md`
   (the `528a6d0` hunk) shows exactly:
   `-…| mined | 2026-10-19 | 365d | corpus/knowledge/crawl-scope-per-host.md |`
   `+…| mined | 2026-10-19 | 365d | corpus/knowledge/crawl-scope-per-host.md, corpus/knowledge/robots-txt-rules.md |`
   Status (`mined`), opened (`2026-10-19`) and recheck (`365d`) unchanged; anchor and teaches cells
   unchanged. Both used-by targets exist; the new one cites S011 28× (`grep -c`), including the row's own
   teaches at `corpus/knowledge/robots-txt-rules.md:19`.
7. Live text supports the anchor's remaining cells: `2.3. Access Method` occurs once (offset 13065);
   "in the top-level path of the service" at 13159; `Published: September 2022` in the header.

## Verdicts

| Attacked statement | Verdict |
|---|---|
| S011 quote `the crawler MUST assume complete disallow` is in Section 2.3.1.4 "Unreachable" Status, 6 words | **holds** (commands 5; `sources/S011.txt`, 1 occurrence) |
| S011 accessed 2026-10-23T02:50:49Z, HTTP 200, no drift since | **holds** (commands 1–4; body+etag identical across 02:50→03:45) |
| Retained visible text byte-identical to live extraction | **holds** (command 3; `cmp` exit 0) |
| S011 row used-by old→new exactly as logged; status/opened/recheck unchanged | **holds** (command 6; `SOURCES.md:19`) |
| "RFC 9309 grounds every rule of (a)–(e)" (`corpus/lessons/round-37.md:41`) | **overstated** — see below |

## Overstatement, reproducible

The unqualified "every rule" contradicts the same entry's own body on two rules:
- **(e)** Live 2.2.2 (offset 9492): octets "in the reserved range defined by [ RFC3986 ] , MUST be
  percent-encoded as defined by [ RFC3986 ] prior to comparison"; read literally `%2F` == `/`.
  Contract (e) `SCORECARD.md:1845` fixes the opposite as a *marked* lane reading, following Figure 4
  and the next sentence. A marked reading that reverses a normative MUST is not grounding.
  Recorded at `corpus/lessons/round-37.md:72`.
- **(a)** Contract (a) `SCORECARD.md:1815-1818` gives only 200–299/400–499/500–599; (f) makes any other
  status a `check_invalid`. Live 2.3.1.2 (offset 13883): crawlers SHOULD follow "at least five
  consecutive redirects"; a file reached within five MUST be "fetched, parsed, and its rules followed".
  A 3xx `/robots.txt` is therefore un-auditable by a rule the RFC defines. Recorded at
  `corpus/lessons/round-37.md:183`.
Neither deviation is hidden (both are carried in the entry), so this is a Gate-line wording defect, not a
fabrication: line 41 should say "grounds (a)–(e) except the two recorded deviations" or drop "every".
Note the wave-1 scout's D1 is itself narrower than the RFC: the 2.2.2 second sentence ("MUST be unencoded
… unless it is a reserved character") and its Figure 4 row already support the contract's reading, so the
RFC is self-conflicting there rather than one-sided against the contract.

## Minor, not defects

- `receipts.json.accessedUtc` is taken **before** the request (`fetch_sources.py:47`), so "accessed" is a
  request-start label; the body-hash chain (command 2) still pins the content at that end.
- The quote is not a contiguous substring of the raw HTML (markup splits it); the gate claim is against
  the retained text, which is where it was verified.

## Unchecked / remaining unknowns

- Post-publication **errata** for RFC 9309: the page carries only the boilerplate errata pointer
  (offset 1217), no errata banner. I did not fetch the errata endpoint (not named in this item), so a
  verified erratum that changes the operative text is unexamined — the one freshness surface left.
- The 365d recheck interval is not challenged here (body unchanged). Tooling installs: none this run.
