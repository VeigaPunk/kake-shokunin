# ScribeRegistry — round 84 wave w1

## Delivered

- Appended one registry row, **S457**, as the last row of `corpus/SOURCES.md` (after S456, line 204, inside `## Registry`, before `## Paths`). Cells, in order: `S457` · `RFC 9111: HTTP Caching, §4.2 Freshness, §5.2 Cache-Control and §5.2.2 Response Directives — https://httpwg.org/specs/rfc9111.html` · `spec` · `A` · scope naming policy-header value semantics · anchor naming §4.2/§5.2/§5.2.2/§5.2.2.1 with HTML line numbers and the RFC revision · teaches · `mined` · `2026-11-04` · `180d` · `corpus/knowledge/policy-value-classes.md`. Eleven cells, 13 `|`-delimited parts, no `|` inside any cell, no embedded newline (verified with the census’s own `registry_rows` splitter).
- Added exactly one row to the coverage map in `corpus/README.md` (line 86): `policy-value-classes.md` (S457) plus the one-line coverage. Nothing else in that file changed.
- Took the after-census and wrote `controls/census-after.txt` (full stdout plus `census_exit=0`).

## Re-derived counts (not carried over from the brief)

- Registry rows at base: **194**; highest id **S456**; next free id **S457**. After the append: **195** rows, ids unique, S457 is last.
- Tier/status deltas: `tier.A` 170 → 171, `status.mined` 164 → 165; `tier.B` 7, `tier.C` 17, `queued` 8, `rejected` 22 unchanged (`sources-census.sh census`, exit 0).
- `W04` count: **22 before, 22 after**. `census-after.txt` is byte-identical to the frozen `controls/census-before.txt` (both sha256 `5c5a3da2c253c38058c43d6c562f5c0cb0e8f1daaec7dbac1216e9148c168ac0`).

## Commands and exit codes

| command | exit |
|---|---|
| `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` (before, to `w1/ScribeRegistry/census-before-run.txt`) | 0 |
| same command (after, to `controls/census-after.txt`) | 0 |
| `sources-census.sh census --root /home/vgpnk/Projects/shokunin kake` (before) | 0 |
| same command (after) | 0 |
| `python3 -B .ufo/waves/round-84/c84_defect_queue.py --root <lane>` (after append) | 1 (D4 closed; D1–D3 open on other seats) |
| `node scripts/corpus-contract.mjs --root .` (`node` reports exit 1; shell wrapper echoed its own `$?`) | 1 (3 pre-existing findings) |
| `git diff --stat -- corpus/SOURCES.md corpus/README.md` | 0 (2 files, 2 insertions, 0 deletions) |
| `grep -cF <quote> <retained html>` over seven fragments | 0, each `count=1` |

## Append-only proof and mutable-cell changes

`git diff -U0 -- corpus/SOURCES.md` is exactly one hunk: `@@ -203,0 +204 @@`, one added line, zero removed. No existing registry cell was touched, so the old→new list for ScribeLesson/the L1 is **empty**:

> Registry changes (ScribeRegistry, r84): none — no existing `status`, `recheck` or `used-by` cell changed. S457 is a new row: `mined`, `2026-11-04`, `180d`, `corpus/knowledge/policy-value-classes.md`. Census: rows 194→195, tier.A 170→171, mined 164→165, W04 22→22, exit 0→0.

## D4 coupling (why the HTTPWG URL)

`c84_defect_queue.py::item_d4` compares the W04 tuples in the frozen `controls/census-before.txt` against `census_w04()` re-derived from the **measured tree’s** `corpus/SOURCES.md`. S456 already registers `https://www.rfc-editor.org/rfc/rfc9111.txt`, so a second row on that URL with a new scope cell would derive a 23rd W04 and reopen D4. S457 therefore cites `https://httpwg.org/specs/rfc9111.html`, which no registry row carries; ScoutSources-17 actually fetched and retained that URL (`fetch-meta-httpwg.txt`: `http_code=200`, `size_download=178573`; sha256 `999f401328ed8991d172aeb1cd4ab048630928437af2401d3e39552c4a073f64`), so the citation is the retained object, not a substitute for it. Measured after the append: `item=D4 closed=1 state=1 row=1 receipt_w04=22 derived_w04=22`.

## Findings

1. **The dispatch sentence “§5.2.2.2 max-age” is wrong.** RFC 9111 §5.2.2.1 is `max-age`; §5.2.2.2 is `must-revalidate`, in both the rfc-editor text (lines 1208/1222) and the HTTPWG HTML (line 282, columns 6944 and 7842). The row’s anchor names §5.2.2.1 for `max-age` and marks §5.2.2.2 as `must-revalidate, not max-age`, so no correction is needed. The L1 correction message repeated the slip; the knowledge seat reached the same conclusion independently.
2. **The before-output cannot be committed as `census-after.txt` alongside the after-output.** Item 3 says “commit both outputs as `controls/census-after.txt`”, but `controls/*` is frozen and `census-before.txt` is a frozen input to D4. I wrote only `census-after.txt`; the before run is preserved byte-identically at `w1/ScribeRegistry/census-before-run.txt` (same sha256 as the frozen receipt).
3. **Transient E11 is real and resolved by a sibling.** Between the append and the knowledge entry landing, the census reported `E11 S457 missing used-by corpus/knowledge/policy-value-classes.md` and exit 1 (`w1/ScribeRegistry/census-mid-e11.txt`). After ScribeKnowledge-19 wrote the 14,271-byte entry, the after-census is clean. Row order therefore couples to a sibling deliverable; the L1 should take the after-census only after `policy-value-classes.md` exists.
4. **`corpus-contract.mjs` grew from 69 to 70 knowledge entries with no new finding**: still the same three pre-existing `missing_metadata` findings on `corpus/knowledge/meta-robots-directives.md`, 0 errors. The new entry satisfies the provenance trio.
5. **Anchor line numbers are HTML lines of a 303-line, 178,573-byte file**, so several sections share a line (line 282 carries §5.2.2, §5.2.2.1, §5.2.2.2 and §5.2.3 p.1). I recorded section + line + paragraph id rather than a narrow line span, since a span would be misleadingly precise.
6. **Leads list untouched.** `## Leads (unopened)` still lists `https://www.rfc-editor.org/rfc/rfc9111.html`; that exact URL was not opened (the HTTPWG rendering was), so the lead remains accurate and the append-only rule needed no exception.
7. **The `equivalent`/`control` reorder leg has no ground in S457’s source.** RFC 9111 names no referrer field at all: `grep -c -F` is 0 for each of `referrer`, `Referrer`, `referer` and `Referer` in both renderings, and the only `refer`-containing tokens are `references`/`referring`/`reference` and `prefer*` (token census over both files: 25 `references`, 8 `referring`, 6 `prefers`, 4 `preferred`, 3 `reference`, 2 `preferences`, 2 `preference`, 2 `preferable`). That forecloses the counter-reading that a `Referer` mention somewhere supplies the missing grammar. `referrer-policy` is likewise absent from every registry row, while `contract.md:132-133` and `policy-expectations.json:16,21` exercise the `reordered` class with exactly that header. This is not a counter contradiction — the pairs are synthetic and the class table is lane policy — but the round lesson should carry it as the Gate’s reject: S457 grounds the `max-age` argument and the ignore-unrecognised rule, not the Referrer-Policy grammar; flip condition is the Referrer-Policy specification itself, which is outside this seat’s authorised URLs and was not opened. The coverage-map row does not claim otherwise.

## Limits

- I made no network call. The GET and the retained bytes are ScoutSources-17’s; the fetch time is recorded by that seat, not by me, and the row attributes the fetch to it rather than asserting a timestamp I did not observe.
- The `teaches` cell paraphrases RFC 9111; it does not claim an ordering rule the RFC does not state, and it says so.
- Verification of C1 as a whole is not mine: D1/D2 depend on `corpus/lessons/round-84.md` and D3 on `w1-results.json`, neither of which existed at my measurement.

## Receipts

`.ufo/waves/round-84/w1/ScribeRegistry/`: `census-before-run.txt` (byte-identical to the frozen receipt), `census-mid-e11.txt`, `census-diff.txt`, `row-parse.txt` (census-parser view of S457), `d4-equality.txt`, `c1-counter-after.txt`, `raw-checks.txt` (seven `grep -F` proofs over the retained HTML). Artifacts: `.ufo/waves/round-84/controls/census-after.txt`.

## Addendum (post-append independent verification)

ScoutSources-17 re-verified every anchor claim in the landed row against its own retained bytes and reports all `VERIFIED` (`w1/ScoutSources/row-anchor-check.txt`, evidence `raw-checks.txt`): §4.2 at HTML line 269 / byte 69398 (txt 581), §5.2 at 279 / 107517 (txt 1081), §5.2.2 at 282 / 115955 (txt 1203), §5.2.2.1 at 282 / 116325 (txt 1208), §5.2.2.2 at 282 / 117223 (txt 1222), §5.2.3 p.1 at 282 / 131205 (txt 1411), and the front-matter claims STD 98 (txt 7), obsoletes RFC 7234 (txt 8; HTML 233), June 2022 (txt 11). Its `fetch-receipt-httpwg.json` records the GET as `2026-11-04T14:06:43Z`, status 200, 178,573 bytes, sha256 `999f4013…f64`, `truncated=false`, no cookies and no credentials.

I did not edit the landed anchor cell to carry those byte offsets or the timestamp: a post-append edit would turn the single-line diff into an add-then-modify pair and weaken the append-only evidence. Both refinements stay recoverable from the scout’s receipt and this addendum, and the row’s factual claims are unchanged. The scout’s own draft row used `status=queued`; the assignment pins `mined`, and the landed row keeps `mined` — the only status difference, with no factual conflict.

## Verdict

**S457 appended correctly and the registry stayed append-only: 195 rows (+1), 22 W04 (unchanged), after-census exit 0 and byte-identical to the frozen before-receipt, D4 measured `closed=1` with `receipt_w04=22 derived_w04=22`; one dispatch numbering error (§5.2.2.2 is `must-revalidate`, `max-age` is §5.2.2.1) reported, not propagated.**
