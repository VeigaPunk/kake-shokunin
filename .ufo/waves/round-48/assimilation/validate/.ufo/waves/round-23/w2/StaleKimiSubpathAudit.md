## Verdict

None — no counterexample found. The three stored claims are genuinely stale at their old values/pointer, and their round-23 corrections match the independent read-only checks below. No wrong correction (P1) found.

## Findings

None (P0–P3). No fix required.

## Checked and held

- **c1 — STALE confirmed; correction is true and not overclaiming.** Expected from the correction: a live GET of the canonical sitemap should parse to 96 `<loc>` entries. Ran `curl --max-time 30 -sS https://ds4cc.com/sitemap.xml` (GET; parsed the returned XML). Output: `sitemap_status=200 bytes=7565`, `loc_count=96 unique_locs=96`. Thus 93 is stale and the 96-entry correction is current. “Should-serve inventory” is the documented parity-set designation, not an assertion that all entries currently serve on Kimi; the c2 status check below confirms that many do not.

- **c2 — STALE confirmed; correction is true and complete for the stated GET/status observation.** Re-fetched and parsed the same sitemap, mapped each `<loc>` path to `https://ds4cc.kimi.page`, appending `index.html` only to paths ending in `/`, then issued GETs with `curl --max-time 30 -sS -o /dev/null -w '%{http_code}' "$url"` (five concurrent workers; no `-L`, so these are response statuses without following redirects). Output: `loc_count=96 unique_locs=96`; `mapped_count=96 invalid_locs=[]`; `status_counts={'200': 19, '404': 77}`; `curl_errors=[]`; `non_200_count=77`. This reproduces the correction exactly and contradicts the old 19/74 count.

- **c5 — STALE confirmed; correction is true and complete for the identified history change.** The live `GET https://github.com/VeigaPunk/ds4cc-marketplace/commits/main/sitemap.xml` history lists `0b1116766de2d9895a3673c88678049b4946cf3c` (Sep 30, 2026) with title “sitemap: list all 75 missing servable canonical URLs…”. `GET https://github.com/VeigaPunk/ds4cc-marketplace/commit/f3d2ecd` returned `HTTP 404`. The replacement commit page reports `1 parent 2b5fd57`; its sitemap diff reports `+75` and `0` deletions. Independent raw-file GETs returned HTTP 200 and counts `2b5fd57/sitemap.xml: 18` and `0b1116766de2d9895a3673c88678049b4946cf3c/sitemap.xml: 93`. The commit `.patch` also returned HTTP 200 and parsed to `patch_loc_additions=75 patch_loc_deletions=0`. This supports the correction’s parent/count/diff facts and identifies the stale `f3d2ecd` pointer.

## Limits

- These are point-in-time public GET observations on 2026-10-21; they do not guarantee later sitemap or mirror state.
- The c1 “should-serve” designation is a parity interpretation of the canonical sitemap, not independently verified hosting policy. The checks establish the sitemap inventory and its current Kimi response distribution, not who guarantees mirror completeness.
- An initial Python-urllib parity attempt failed partway on DNS resolution; it was not used as evidence. The full 96-path check was rerun through curl with the mapping rule above, with zero curl errors.