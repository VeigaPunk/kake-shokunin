## Verdict

C1 freshness recheck completed for five load-bearing claims in `kimi-subpath-audit` on 2026-10-21: three are STALE and two HOLD. This is a scoped freshness receipt, not an independent admission.

## Findings

### P2 — Canonical sitemap count is stale

- **Exact command:** `curl -sS https://ds4cc.com/sitemap.xml | python3 -c 'import sys; print("loc_count=" + str(sys.stdin.read().count("<loc>https://ds4cc.com")))'`
- **Exact observed output:** `loc_count=96`
- **Impacted claim/axis:** C1 freshness; the unit calls the current canonical inventory 93 locations.
- **Smallest fix:** Replace the live-count claim with 96 and date the observation; retain the sitemap as the should-serve source.

### P2 — Mirror parity count is stale

- **Exact probe:** GET `https://ds4cc.com/sitemap.xml`; for each of its 96 `<loc>` URLs, map a trailing `/` to `index.html` and GET the mapped `https://ds4cc.kimi.page` URL using `curl -sS -o /dev/null -w '%{http_code}'` (96 targets; eight concurrent curl workers).
- **Exact observed output:** `curl_parity locs=96 statuses={'200': 19, '404': 77}`
- **Impacted claim/axis:** C1 freshness; the unit reports 93 canonical locations, 19 served, and 74 missing.
- **Smallest fix:** Update the parity baseline to 96 / 19 / 77 and do not reuse the historical missing-path classification without rechecking it.

### P2 — Sitemap change commit reference is stale

- **Exact command:** `curl -sS -o /dev/null -w '%{http_code} %{url_effective}\\n' https://github.com/VeigaPunk/ds4cc-marketplace/commit/f3d2ecd`
- **Exact observed output:** `404 https://github.com/VeigaPunk/ds4cc-marketplace/commit/f3d2ecd`
- **Additional source evidence:** The live sitemap history page identifies `0b1116766de2d9895a3673c88678049b4946cf3c`; its patch shows 75 sitemap additions, and raw sitemap counts are `2b5fd57 loc_count=18` then `0b1116766de2d9895a3673c88678049b4946cf3c loc_count=93`.
- **Impacted claim/axis:** C1 freshness; the erratum attributes the 75-entry expansion to `f3d2ecd`.
- **Smallest fix:** Point the erratum at the reachable `0b1116766de2d9895a3673c88678049b4946cf3c` revision and preserve the verified 18→93 change as a historical fact.

## Checked and held

- The Kimi index still has the three directory targets in its same-origin static `href`/`src` set. Kimi GETs returned `404` for `/omarchy-usage/`, `/omegag/`, and `/speedrun/`; their respective `/index.html` URLs returned `200`. The parallel GitHub Pages check still returned `301` for the no-trailing-slash forms and `200` for each trailing-slash and `index.html` form. The directory-index failure claim is HOLD.
- The `burnerchrome-kimi` link-sweep claim is HOLD. After excluding the fragment-only anchor, the page yielded 15 same-origin targets and all 15 GETs returned `200` (`burnerchrome_root=GET-200 same_origin_nonfragment_targets=15 status_counts={'200': 15}`; `non_200=[]`).

```json
{
  "unit": "kimi-subpath-audit",
  "path": "corpus/knowledge/kimi-subpath-audit.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "ds4cc.com's `sitemap.xml` (93 locs) is the \"should-serve\" set for ds4cc.kimi.page.",
      "claim": "The live canonical sitemap currently has 93 entries and is the should-serve inventory for the Kimi mirror.",
      "surface": "GET https://ds4cc.com/sitemap.xml",
      "method": "GET",
      "observation": "Count command output: loc_count=96.",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, the live ds4cc.com sitemap contains 96 <loc> entries and remains the should-serve inventory for ds4cc.kimi.page."
    },
    {
      "id": "c1",
      "anchor": "ds4cc-kimi-mirror — 93 canonical locs → 19 served, 74 missing",
      "claim": "Parity of the canonical list reports 19 served and 74 missing Kimi paths.",
      "surface": "GET https://ds4cc.com/sitemap.xml; GET all 96 mapped paths on https://ds4cc.kimi.page (trailing / mapped to index.html)",
      "method": "GET",
      "observation": "curl_parity locs=96 statuses={'200': 19, '404': 77}",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, the live sitemap has 96 canonical locations and the 96 directory-mapped Kimi GETs return 19 HTTP 200 and 77 HTTP 404."
    },
    {
      "id": "c1",
      "anchor": "404 on kimi while `*/index.html` serves 200",
      "claim": "The index-linked omarchy-usage, omegag, and speedrun directory URLs fail on Kimi while their index.html paths serve.",
      "surface": "GET https://ds4cc.kimi.page/{omarchy-usage,omegag,speedrun}{/,/index.html}",
      "method": "GET",
      "observation": "404 https://ds4cc.kimi.page/omarchy-usage/; 200 https://ds4cc.kimi.page/omarchy-usage/index.html; 404 https://ds4cc.kimi.page/omegag/; 200 https://ds4cc.kimi.page/omegag/index.html; 404 https://ds4cc.kimi.page/speedrun/; 200 https://ds4cc.kimi.page/speedrun/index.html",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "| burnerchrome-kimi | 15 | 0 |",
      "claim": "The burnerchrome Kimi index has 15 same-origin link targets and zero non-200 targets.",
      "surface": "GET https://burnerchrome.kimi.page/ and its 15 unique same-origin non-fragment href/src targets",
      "method": "GET",
      "observation": "burnerchrome_root=GET-200 same_origin_nonfragment_targets=15 status_counts={'200': 15}; non_200=[]",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "sitemap commit `f3d2ecd` adds **75** `<url>` entries (18→93 locs);",
      "claim": "The source-history pointer f3d2ecd is the sitemap change adding 75 URLs to the 18-entry list, reaching 93.",
      "surface": "GET https://github.com/VeigaPunk/ds4cc-marketplace/commits/main/sitemap.xml; GET https://github.com/VeigaPunk/ds4cc-marketplace/commit/f3d2ecd; GET raw sitemap at 2b5fd57 and 0b1116766de2d9895a3673c88678049b4946cf3c",
      "method": "GET",
      "observation": "f3d2ecd commit URL: HTTP 404; reachable history shows 0b1116766de2d9895a3673c88678049b4946cf3c; count outputs: 2b5fd57 loc_count=18 and 0b1116766de2d9895a3673c88678049b4946cf3c loc_count=93.",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, the reachable sitemap history shows commit 0b1116766de2d9895a3673c88678049b4946cf3c adding 75 locations (parent 2b5fd57: 18; new tree: 93), while the cited f3d2ecd URL returns 404."
    }
  ]
}
```

## Skipped claims

- The `sync-check` identity/marker guarantee and the byte-rewrite examples were not rechecked because that requires inspecting the source-side sync implementation and comparison markers, not just public URL GETs.
- The JavaScript-rendered `PROPERTIES[]` blind spot and `${esc(...)}` filtering rule were not rechecked in a rendered browser DOM or source; the sweeps here cover static HTML href/src values only.
- The 74-path stale-vs-rot/not-in-source classification, 63/10/1 add-date decomposition, old publish vintage, and embedded-date maxima were not recomputed path by path. The current mirror count and the historical 75-addition commit were checked, but no full file-add-date / publication-vintage classification was done.
- Other live-row link-sweep counts and embedded-date claims were not rechecked for plazir27-kimi-page, plazir27runs-on, ufofsd-charter, plazir27runson, ufo-fsd-kimi-pro, veigapunk-page, ufo-fsd.kimi.page (vault), or ufofsd; burnerchrome was the selected non-mirror row.
- The future-facing claim that the directory failure is permanent until a rewrite/source fix was not tested; current GETs confirm only the present behavior, not permanence or cause.
- The round-21 historical absence of the local checkout, `kimi_audit.py`, and kimi-surface tooling, plus metadata contract S019, was not retroactively reverified.

## Limits

All site and GitHub requests used public unauthenticated GETs; no tools were installed or updated. An initial Python `urllib` parity attempt received 403 for all 96 Kimi URLs, so it was discarded; the recorded 19/77 parity result comes from curl GETs, which successfully returned 200 for sampled served pages. Client-dependent 403 behavior remains a caveat. Static HTML checks do not establish what a JavaScript-rendered browser DOM exposes.
