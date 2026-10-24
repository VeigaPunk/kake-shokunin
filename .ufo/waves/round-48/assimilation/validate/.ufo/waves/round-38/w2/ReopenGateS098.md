# ReopenGateS098 — S098 Gate line and SOURCES row vs the RFC 3986 text

Attacked: `corpus/lessons/round-38.md:31-35` (S098 source-opening line) and `corpus/SOURCES.md:106`
(S098 row) at tip `adab4c7`. Everything below is from a fresh GET plus the lane's read-only git and
sandbox artifacts; no lane file, index or jj state was touched. Sandbox
`/fast/scratch/hyaku/kake-r38w2/ReopenGateS098/`.

## Commands (all from the sandbox; `TMPDIR` set, no clone needed)
- `curl -sS -o rfc3986.txt -w 'http_code=%{http_code} size=%{size_download}' https://www.rfc-editor.org/rfc/rfc3986.txt`
  → `http_code=200 size=141811`, exit 0; `sha256sum rfc3986.txt` →
  `3102dae4b68cebe40337730312fcb612297b8928547267e8b3d1ee6002b2d683`, exit 0.
- Second GET with headers → 200, same 141811 bytes, same digest (`rfc3986_2.txt`), exit 0. Headers:
  `etag: W/"45bc1160a280c34b923309ae91ff283a"` = md5 of the body (checked, exit 0),
  `cache-control: public, max-age=86400`. `headers.txt` sha256 `4bbb1380d30567b25a2f97f2…b06ac8`.
- `python3 verify_quote.py` exit 0: quote found after whitespace unwrap at byte 33093, line 720;
  section headers at lines 634/656/718/745 with titles `Percent-Encoding`, `Reserved Characters`,
  `Unreserved Characters`, `When to Encode or Decode`; ABNF at 647 (`pct-encoded = "%" HEXDIG
  HEXDIG`), 679/681/683 (reserved/gen-delims/sub-delims), 724 (unreserved).
- `python3 recompute_i.py` exit 0: parsed the RFC ABNF and the *declared* rule (i) paragraph out of
  `SCORECARD.md` at `2dab7f31` (`$ git show 2dab7f31:SCORECARD.md`, sha256
  `b7432d69ffc4302bf0f5f660…d7b31841`), swept U+0000–U+007F → declared set == RFC set, **85
  allowed, 43 excluded, MISMATCHES: 0**; excluded printable = space + `" < > \ ^ `` ` `` { | }`
  (9 named) and 32 C0 + DEL.
- `gzip -dc .ufo/waves/round-26/fetched/S029-1.raw.gz | sha256sum` → same digest;
  `| cmp - rfc3986.txt` → BYTE-IDENTICAL (exit 0).
- Cross-check of the wave-1 artifact `…/kake-r38w1/ScoutReopenRFC3986s2/charset_table.tsv`
  (sha256 `ebb2da200fd4238ce0242182…d0884a6`): 128 rows, 0 disagreements with my independent ABNF
  parse on either the `rfc3986_s2.2_2.3_plus_pct` or `rule_i` column, 0 rows with `relation != OK`;
  class counts unreserved 66, reserved 18, pct-% 1, excluded 43.

## Verdicts

| # | Statement attacked | Verdict |
|---|---|---|
| 1 | Quote is present verbatim at §2.3 | **holds** — `rfc3986.txt:720-721`, broken only by the RFC's own line wrap: `…do not have a reserved\n   purpose are called unreserved.` Same bytes with whitespace collapsed (`verify_quote.py`). |
| 2 | `HTTP 200` at access | **holds** — 200 twice today, 141811 bytes both times. |
| 3 | `sha256 3102dae4…b2d683` | **holds** — full digest reproduced; row's full-length pin `3102dae4…02b2d683` is 64 hex chars and matches. |
| 4 | `(same bytes as S029)` | **holds, stronger than claimed** — not just digest equality against S029's recorded string: the in-lane 2026-10-21 retention `.ufo/waves/round-26/fetched/S029-1.raw.gz` decompresses byte-identically to today's fetch (`cmp` exit 0). |
| 5 | `accessed 2026-10-23T04:30:17Z` | **holds, ordering-only** — wave 1 was dispatched `2026-10-23T04:29:52Z` (`.ufo/waves/round-38/w1-dispatched-at.txt`) and the tip commit is `04:43:03Z`; 04:30:17Z sits between. No server-side receipt exists, so the exact second is corroborated only by sequence. The identical second in `w1/ScoutWhatwgUrl.md:3` is a concurrent seat's start time (`04:30:17Z–04:31:49Z`), not evidence of a copy-paste. |
| 6 | Row `anchor` cell | **holds** — the three section titles/numbers are exact (`rfc3986.txt:634,656,718`), footer says `January 2005` (61 occurrences), digest as above. |
| 7 | Row `scope` cell | **holds** — §§2.1–2.3 are precisely character classes and percent-encoding; `SOURCES.md:37` (S029) is scoped to §3 authority-vs-path and `:97` (S089) to §5.2–5.3; those are the only other `rfc3986` rows and no other row claims unreserved/percent-encoding (`grep -i unreserved\|percent-encod` → S098 and S101 only). |
| 8 | Row `teaches` cell | **holds** — §2.2 defines reserved characters as `delimiting characters … distinguishable from other data`; §2.3 defines unreserved; neither is browser URL normalization. |
| 9 | Row metadata `mined / 2026-10-23 / 365d / used-by` | **holds** — S098 absent at base `af43a50f` (base ends at S097), so the lesson's `` `—` → mined`` is right; the two `used-by` paths do cite it (`corpus/knowledge/robots-txt-rules.md:1,89,103`; `corpus/lessons/round-38.md:31`); 11 columns like every other row. |
| 10 | `Per-character check of rule (i) against §§2.2/2.3: 85 allowed, 43 excluded, 0 mismatches` | **holds numerically, overstated in provenance** — 85/43/0 reproduced independently **but the reference set is §2.2 + §2.3 + `%` from §2.1** (`pct-encoded`, line 647): 84 of the 85 come from §§2.2/2.3. The wave-1 table itself names the column `rfc3986_s2.2_2.3_plus_pct`; the lesson's one-liner drops `+§2.1`. |

## Remaining unknowns
- RFC 3986 **errata** for §§2.1–2.3 were not examined: the errata page is a second URL, outside the
  item's one named URL, and wave 1 declined it the same way. This is the only untested freshness
  surface; if a verified erratum touches §2, the row's `anchor` would need it.
- `retained text SHA256` in the row names no in-lane path — the wave-1 copy is a sandbox artifact
  (`/fast/scratch/hyaku/kake-r38w1/…/rfc3986.txt`, still present, digest matches). The identical
  bytes do exist in-lane (round-26 copy), so the wording is materially true; no fix required.
- Nothing here tests the rule's implementation at `3ed8e15c`; this item judged the Gate text and row only.

Net: the S098 Gate line and row survive falsification. One real (small) overstatement — the `+§2.1`
provenance of the 85th allowed character — and one wording nit.

Tool installs: none.
