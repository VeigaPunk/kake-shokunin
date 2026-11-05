VERDICT: RFC 9111 §4.2.2 opened and quoted on committed receipts; the frozen source is byte-identical to the fetched body; 10 % is supported as a hedged example, the 86400 cap is not in the RFC text; C2 contract has one unlabelled upper-endpoint choice and one unused input (`now`) for the routed list.

# ScoutSources — round 92 (kake)

Deliverable: `.ufo/waves/round-92/w1/ScoutSources/Sources.md` (receipt table, quotes, conventions).
Receipts: `.ufo/waves/round-92/w1/ScoutSources/{rfc9111-fetched.txt,errata9111.html,datatracker9111.html}`.

## Findings

### F1. Source opened; frozen copy identical
- `curl -sS -o rfc9111-fetched.txt -w 'HTTP %{http_code} bytes=%{size_download}\n' https://www.rfc-editor.org/rfc/rfc9111.txt` → `HTTP 200 bytes=84477`, exit 0.
- `sha256sum` → `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`.
- UTC access (observed) `2026-11-05T00:30:13Z` — 2026-11-04 local evening (UTC−03:00). Recorded as observed; the round is dated 2026-11-04.
- `cmp .ufo/waves/round-92/L1/src/rfc9111.txt <fetched>` → no output, exit 0. **Identical.**

### F2. Quotes (plain-text line numbers; each verified raw-substring of the cited lines, exit 0 from a Python check)
- (a) lines 689–690, 15 words: "a cache MAY assign a heuristic expiration time when an explicit time is not specified"
- (b) lines 695–696, 20 words: "A cache MUST NOT use heuristics to determine freshness when an explicit expiration time is present in the stored response."
- (c1) lines 697–699, 18 words: "heuristics can only be used on responses without explicit freshness whose status codes are defined as "heuristically cacheable""
- (c2) lines 700–701, 18 words: "on responses without explicit freshness that have been marked as explicitly cacheable (e.g., with a public response directive)."
- (d) lines 707–708, 22 words: "caches are encouraged to use a heuristic expiration value that is no more than some fraction of the interval since that time." and line 709, 9 words: "A typical setting of this fraction might be 10%."

A quote that survives only after whitespace collapse is not counted; the check joined the cited lines with one space and tested containment, and each quote's span is the exact cited lines.

### F3. Errata and obsoletion — none touches §4.2.2
- `curl -sS -o errata9111.html -w 'HTTP %{http_code}' https://www.rfc-editor.org/errata/rfc9111` → `HTTP 302 bytes=0`, exit 0 (empty body; not kept).
- Redirect followed with `curl -sSL` to `https://errata.rfc-editor.org/search/?rfc_number=9111&presentation=records` → `HTTP 200 bytes=40383` (3 redirects), exit 0.
- Four records: 9004 Reported §3.5; 9185 Reported §4.3.4; 9166 Held for Document Update §5.2.3; 7695 Rejected §4.3.2. None cites §4.2.x. Adjacent: 9004 and 9166 sit beside §3 (which §4.2.2 cites as "Section 3") but change no normative text in force.
- `curl -sSL https://datatracker.ietf.org/doc/rfc9111/` → `HTTP 200 bytes=120322`, exit 0. Status "Internet Standard (June 2022)"; "This document obsoletes RFC 7234". No "Obsoleted by"/"Updated by" relationship text (text search of saved HTML; not a rendered-view check).

### F4. Conventions
- **10 % fraction — supported as a hedged example.** Line 709: "A typical setting of this fraction might be 10%." Labelling it a lane convention is accurate.
- **86400 cap — not in the RFC.** `grep -c 86400` → `0`; `grep -ciE "24 hours|one day"` → `0`. The only constraint language is lines 692–693, "impose worst-case constraints on their results", unquantified. Labelling it a lane convention is accurate.

### F5. Defects in the round's own contract (routed, not edited)
1. **Unlabelled upper endpoint (clause 12).** The RFC says "the interval since that time" (line 708) and names no upper endpoint. The contract uses `Date`. The contract's "Everything else is a direct reading of the section" overstates; this choice is unlabelled.
2. **Unlabelled undecided rule (clause 13).** RFC lines 690–691 permit heuristics "employing algorithms that use other field values" with no Last-Modified, and are silent on Last-Modified > Date. `heuristic-undecided` is a lane choice, not labelled.
3. **`now` validated and unused.** Contract line 34 and 60 define and validate `now`. `c92_heuristic.py` line 137–139 validates it. The reference decision (line 186) computes from `Date` and `Last-Modified` only; no decision clause 9–13 reads `now`. The frozen counter therefore accepts a `now` that changes nothing; a candidate that reads `now` for a decision would not be caught by the reference's case set.
4. **Status set cited, not fetched.** Clause 11's 12-code set matches the 12 "is heuristically cacheable" sentences in the lane-retained RFC 9110 copy `.ufo/waves/round-81/w1/ScoutSources/rfc9110.txt` (lines 6953–7876). RFC 9110 was not re-fetched this round; the match rests on that retained copy, not on a fresh source open.

### F6. Deviations and honest limits
- **Deviation:** errata URL R2 was fetched twice (first without redirect-follow, then with `-L` to `errata.rfc-editor.org`, a host the item did not name). The item said "once each". Disclosed; the redirect target's body is kept as `errata9111.html`.
- **Access date:** the host UTC clock read 2026-11-05 at access; recorded as observed, not rewritten to the round date.
- Datatracker and errata checks are text searches of saved HTML.
- Only RFC 9111 and the two registry pages were touched on the network: four GETs total (R1, R2, R2b, R3).

## Tooling and writes
- No installs or upgrades. No pacman, no uv, no global tools changed.
- No git or jj command was run anywhere.
- Writes: `.ufo/waves/round-92/w1/ScoutSources/` (Sources.md and three receipts) and this report. Nothing else in LANE was written.
- Scratch `/fast/scratch/hyaku/kake-r92/ScoutSources/` removed after receipts were copied (see final command).

## Commands, exit codes
| Command | Exit |
|---|---|
| `curl -sS -o rfc9111-fetched.txt -w '...' https://www.rfc-editor.org/rfc/rfc9111.txt` | 0 (HTTP 200) |
| `cmp frozen fetched` | 0 (identical) |
| `curl -sS -o errata9111.html -w '...' https://www.rfc-editor.org/errata/rfc9111` | 0 (HTTP 302) |
| `curl -sSL -o errata9111.html -w '...' https://www.rfc-editor.org/errata/rfc9111` | 0 (HTTP 200, 3 redirects) |
| `curl -sSL -o datatracker9111.html -w '...' https://datatracker.ietf.org/doc/rfc9111/` | 0 (HTTP 200) |
| Python line-span containment check (7 quotes) | 0, all `True` |
| `grep -c 86400 rfc9111-fetched.txt` | 1 (`0` hits; grep printed 0) |
