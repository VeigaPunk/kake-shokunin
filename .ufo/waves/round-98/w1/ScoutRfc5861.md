# ScoutRfc5861 — round 98 w1 report (2026-11-05)

Seat: ScoutRfc5861 (leaf scout; no subagents). Scope: open RFC 5861 and its errata record once;
deliver fetch receipts, errata inventory, located quotes and two draft SOURCES rows supporting
S482/S483 for C2's `corpus/knowledge/stale-extensions.md`. Writes confined to
`.ufo/waves/round-98/w1/ScoutRfc5861/` and scratch `/fast/scratch/hyaku/kake-r98/ScoutRfc5861/`
(deleted before yield; receipts copied out first). No git/jj mutation anywhere; no tool installs.

## Pre-flight

- Lane tip: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse master` →
  `7838981e4e40280176085e8aa1f6827eb7133a69`, rc 0.
- Frozen instrument digests: `sha256sum -c controls/instrument-sha256.txt` inside
  `.ufo/waves/round-98/` → all 11 lines OK, verify_rc=0. No mismatch; nothing to route.
- Retained RFC 5861 body sha256 (sha256sum): `1193f1c8710af162e1b9fb4250d79bc6dd26497df4caeeaaa8bcb2fefdd2529e`
  — equals the freeze-named `1193f1c8…` prefix.
- Read first: freeze.md, stale-contract.md, controls/ inventory (committed receipts reproduced by
  the L1, not re-stamped here), corpus/lessons/round-97-verifier-spotcheck.md §6 (R98-D1 meta-text
  gate, R98-D2 reviewer coverage, R97-4 scratch rule honored).

## 1. Fetches (once each; full receipts in w1/ScoutRfc5861/fetch.txt)

| URL | hops | final URL | bytes | sha256 | UTC |
|---|---|---|---|---|---|
| https://www.rfc-editor.org/rfc/rfc5861.txt | 1 response, 0 redirects, HTTP/2 200 | same | 10359 | 1193f1c8710af162e1b9fb4250d79bc6dd26497df4caeeaaa8bcb2fefdd2529e | 2026-11-05T22:01:17Z |
| https://www.rfc-editor.org/errata_search.php?rfc=5861 | 2 responses, 1 redirect: HTTP/2 302 (Location errata.rfc-editor.org/search/?rfc_number=5861) then HTTP/2 200 | https://errata.rfc-editor.org/search/?rfc_number=5861 | 17788 | 9603a690cfa9b5b1c7c0f9d2a52c2b5b98f38a90e7c14e76e5dd90e0f3ab8ce9 | 2026-11-05T22:01:17→18Z |

curl rc 0 both. Bodies + per-hop headers copied to w1/ScoutRfc5861/ (rfc5861.txt,
rfc5861.headers.txt, errata-5861.html, errata.headers.txt).

**RFC body sha match: yes.** Live `rfc5861.txt` sha256 equals the retained
`.ufo/waves/round-98/sources/rfc5861.txt` byte-for-byte (same sha256sum output line, and equal
file size 10359).

## 2. Errata inventory (errata-5861.md)

Exactly 2 errata, both in the page's only status card "Verified (2)" (line 108 of the retained
page); no Reported / Held for Document Update / Rejected card exists. Body-line-numbered records:

| EID | status | type | section | evidence lines |
|---|---|---|---|---|
| 2255 | Verified | Editorial | 3 (pg.3) | header 129; badge 135; Type 138/141; "Section 3, pg.3 says:" 174; notes → 198 |
| 2256 | Verified | Editorial | 4 (pg.4) | header 205; badge 211; Type 214/217; "Section 4, pg.4 says:" 250; cf. EID=2255 note 274 |

Both are the same editorial Age/Warning-header-field rewording; EID 2255's notes state the issue
recurs in the last paragraph of Section 4. Neither touches the §3 window, the §4 bound, the §4
error set, or the §4 scope sentence — i.e. nothing C2's decision tool encodes.

## 3. Quotes (quotes.md) — 5/5 located

| target | file | lines |
|---|---|---|
| §3 "up to the indicated number of seconds" | sources/rfc5861.txt | 105-108 (phrase 107-108; heading 104) |
| §4 "more stale than the indicated amount" | sources/rfc5861.txt | 180-182 (phrase 181) |
| §4 500/502/503/504 error definition | sources/rfc5861.txt | 184-185 |
| §4 request-directive scope | sources/rfc5861.txt | 175-178 |
| RFC 9111 §4.2.4 prohibition | .ufo/waves/round-96/w1/ScoutRFC/rfc9111.txt | 790-793 |

Each quote is ≤25 words and a verbatim substring (line joins only; no hyphen wrap crossed).
Retained RFC 9111 body sha256: aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e.

## 4. Draft rows (rows-draft.md) — 2 rows

S482 (spec, tier A, RFC 5861 body, recheck 365d) and S483 (dataset, tier A, errata search page,
recheck 90d), exact 11-column contract-v1 shape, status mined, opened 2026-11-05, no literal `|`
in any cell. Registry check: S481 at corpus/SOURCES.md:227 is the last row; S482/S483 unused, so
the ids are collision-free. Flagged for L1: seat-spec used-by cell is `knowledge/stale-extensions.md`
while existing rows carry a `corpus/` prefix; kept as specified.

## Observations (findings routed, nothing repaired)

- `corpus/knowledge/stale-extensions.md` does not exist at the lane tip (glob: path not found) —
  expected: the contract says the executor seat builds it this wave. The draft rows' used-by cells
  point at it; the C2 predicate requires both to land.
- No defect found in the frozen instruments, the retained RFC body, or the errata page relative to
  the freeze; nothing to route.

## Deliverables (all in .ufo/waves/round-98/w1/ScoutRfc5861/)

fetch.txt, errata-5861.md, quotes.md, rows-draft.md, rfc5861.txt, rfc5861.headers.txt,
errata-5861.html, errata.headers.txt, four .fetch.start/.end UTC receipts, and this report.

Verdict evidence: fetch receipts rc=0 both; `sha256sum` retained vs live rfc5861.txt equal;
`sha256sum -c controls/instrument-sha256.txt` → 11/11 OK rc 0; errata records read from retained
page lines 108/129/135/141/174/198/205/211/217/250/274; quotes at the lines tabled above.

SCOUT-5861 rfc_sha_match=yes errata=2 quotes_located=5/5 rows=2
