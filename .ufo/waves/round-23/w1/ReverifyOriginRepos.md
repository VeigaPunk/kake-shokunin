## Verdict

Recommendation only, not an admission: C1 freshness for `origin-repos` is mixed. Of the eight selected claims, three are STALE, three are HOLD for current count/availability observations, and two are UNVERIFIABLE because the referenced clone evidence is absent.

## Findings

- **P2 — stale documented clone location.** Command: `for p in "$HOME/Projects/webzites/reports/keepers/repos-r1.md" "$HOME/Projects/webzites/repos" "$HOME/Projects/ds4cc-marketplace" "$HOME/Projects/webzites/repos/ds4cc-marketplace" "$HOME/Projects/webzites/repos/VeigaPunk.github.io" "$HOME/Projects/webzites/repos/burnerchrome" "$HOME/Projects/webzites/repos/llm-wiki" "$HOME/Projects/webzites/repos/plazir-15-site" "$HOME/Projects/webzites/repos/charter-ufo-fsd" "$HOME/Projects/webzites/repos/snapshot-x"; do if test -e "$p"; then printf 'present %s\\n' "$p"; else printf 'absent %s\\n' "$p"; fi; done`. Exact relevant output: `absent /home/vgpnk/Projects/webzites/repos` (the other nine listed paths also printed `absent`). Impact: C1 freshness, the assertion that the clone tree lives at the documented path. Smallest fix: replace current-presence wording with the dated absence observation unless the tree is restored.
- **P2 — current web observations invalidate two dated entries.** Commands: `curl -sS -L --max-time 30 -o /dev/null -w 'http_code=%{http_code} url=%{url_effective} size_download=%{size_download} content_type=%{content_type}\\n' https://burnerchrome.kimi.page/` and the same command with `https://plazir27.kimi.page/`. Exact outputs: `http_code=200 url=https://burnerchrome.kimi.page/ size_download=11976 content_type=text/html`; `http_code=404 url=https://plazir27.kimi.page/ size_download=13409 content_type=text/html; charset=utf-8`. Impact: C1 freshness, the 11,819-byte live-size claim and the inferred live-property mapping. Smallest fix: update the burnerchrome live-size observation and remove or mark the 404 property as not currently served; the absent repository prevents refreshing its repo-side byte comparison.
- **P3 — byte-level canonical mappings and historical clone synchronization cannot be reverified.** The documented clone tree and `ds4cc-marketplace` checkout both returned `absent`; `GET https://ds4cc.com/` returned `http_code=200 url=https://ds4cc.com/ size_download=76159 content_type=text/html; charset=utf-8`, which proves availability but not byte identity. Impact: C1 freshness, `ds4cc.com` canonical-source hash and the 50/50 `HEAD == @{u}` result. Smallest fix: retain these as historical/unverifiable until the relevant checkout plus full historical evidence is available; do not present them as newly live-verified.

## Checked and held

The current Origin list count command `origin repo list | paste - - | wc -l` returned exactly `224`. Four GitHub Pages GETs returned HTTP 200; `plazir27runs-on.kimi.page` also returned HTTP 200. These verify only present count and endpoint availability, not repository/source equality or publishing state.

```json
{
  "unit": "origin-repos",
  "path": "corpus/knowledge/origin-repos.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "Clones live at `~/Projects/webzites/repos/<name>` — **read-only evidence",
      "claim": "The documented `~/Projects/webzites/repos` clone root is present.",
      "surface": "/home/vgpnk/Projects/webzites/repos",
      "method": "test -e",
      "observation": "absent /home/vgpnk/Projects/webzites/repos",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, `/home/vgpnk/Projects/webzites/repos` is absent, so clones are not currently available at the documented path."
    },
    {
      "id": "c1",
      "anchor": "`origin repo list` = 224 repos under `jo-o-veiga`",
      "claim": "The current `origin repo list` contains 224 repositories under `jo-o-veiga`.",
      "surface": "origin repo list | paste - - | wc -l",
      "method": "run",
      "observation": "224",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "50/50 clones re-fetched `HEAD == @{u}` at r8 — zero drift.",
      "claim": "All 50 clone HEADs matched their upstreams with zero drift at r8.",
      "surface": "/home/vgpnk/Projects/webzites/repos",
      "method": "test -e",
      "observation": "absent /home/vgpnk/Projects/webzites/repos; individual clone worktrees are unavailable",
      "verdict": "UNVERIFIABLE",
      "reason": "The documented clone tree and its individual Git worktrees are absent, so current HEAD/upstream equality for the 50 clones cannot be computed; the r8 result remains historical evidence."
    },
    {
      "id": "c1",
      "anchor": "| `ds4cc.com` | `repos/ds4cc-marketplace` (live index sha `b6f65899…`, also == `~/Projects/ds4cc-marketplace`) | byte-verified |",
      "claim": "The current `ds4cc.com` index remains byte-verified against the documented `ds4cc-marketplace` checkout.",
      "surface": "GET https://ds4cc.com/; /home/vgpnk/Projects/webzites/repos/ds4cc-marketplace",
      "method": "GET",
      "observation": "http_code=200 url=https://ds4cc.com/ size_download=76159 content_type=text/html; charset=utf-8; absent /home/vgpnk/Projects/webzites/repos/ds4cc-marketplace",
      "verdict": "UNVERIFIABLE",
      "reason": "The public page is reachable, but the mapped checkout is absent and the unit records only a truncated digest, so the claimed live-to-repository byte identity cannot be rechecked."
    },
    {
      "id": "c1",
      "anchor": "| `burnerchrome.kimi.page` | `repos/burnerchrome/index.html` (live 11819B vs 11775B = sdk-seed + serialization delta) | byte-verified |",
      "claim": "The live `burnerchrome.kimi.page` response remains 11,819 bytes as recorded in the row.",
      "surface": "https://burnerchrome.kimi.page/",
      "method": "GET",
      "observation": "http_code=200 url=https://burnerchrome.kimi.page/ size_download=11976 content_type=text/html",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, GET https://burnerchrome.kimi.page/ returned HTTP 200 with 11,976 bytes, not the cited 11,819-byte live size; the repository-side 11,775-byte comparison is not currently verifiable because its checkout is absent."
    },
    {
      "id": "c1",
      "anchor": "## Byte-verified canonical writers (sha256-matched live ↔ repo tip, r5–r8)",
      "claim": "The listed GitHub Pages root and the `llm-wiki`, `plazir-15-site`, and `charter-ufo-fsd` paths currently return HTTP 200.",
      "surface": "GET https://veigapunk.github.io/; GET https://veigapunk.github.io/llm-wiki/; GET https://veigapunk.github.io/plazir-15-site/; GET https://veigapunk.github.io/charter-ufo-fsd/",
      "method": "GET",
      "observation": "http_code=200 url=https://veigapunk.github.io/ size_download=38262 content_type=text/html; charset=utf-8 | http_code=200 url=https://veigapunk.github.io/llm-wiki/ size_download=16338 content_type=text/html; charset=utf-8 | http_code=200 url=https://veigapunk.github.io/plazir-15-site/ size_download=38337 content_type=text/html; charset=utf-8 | http_code=200 url=https://veigapunk.github.io/charter-ufo-fsd/ size_download=53660 content_type=text/html; charset=utf-8",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "| `plazir27runs-on.kimi.page` (63KB doctrine) | `repos/charter-ufo-fsd` variant | mapped |",
      "claim": "The listed `plazir27runs-on.kimi.page` public property is currently reachable.",
      "surface": "https://plazir27runs-on.kimi.page/",
      "method": "GET",
      "observation": "http_code=200 url=https://plazir27runs-on.kimi.page/ size_download=63421 content_type=text/html",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "| `plazir27.kimi.page` | `repos/ufo-fsd-alpha/docs/charter-ufo-fsd` [INFERENCE — third variant, sha mismatches both charter clones] | inferred |",
      "claim": "The inferred `plazir27.kimi.page` property is currently served as a live mapped variant.",
      "surface": "https://plazir27.kimi.page/",
      "method": "GET",
      "observation": "http_code=404 url=https://plazir27.kimi.page/ size_download=13409 content_type=text/html; charset=utf-8",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, GET https://plazir27.kimi.page/ returns HTTP 404, so this is not a currently served public property and its inferred live-source mapping should be withdrawn or retested only after a working endpoint exists."
    }
  ]
}
```

**Skipped claims and why:** The historical `unchanged r4→r8` comparison cannot be recreated from the current Origin count without the missing old list/report. For `VeigaPunk.github.io`, `llm-wiki`, `plazir-15-site`, `charter-ufo-fsd`, and `plazir27runs-on`, repository byte identity, CI source/build behavior, and variant mapping were not established by HTTP status; the documented clone checkouts are absent. `xsnapshot.app`'s queued/newest/fallback/superseded workflow state is not exposed by its public page (the checked URL returned HTTP 200), and its listed clone path is absent. The `ds4cc-website` versus `ds4cc.com` byte distinction, duplicate codex-tree writer risk, vendored burnerchrome distinction, not-sites inventory, and `Fleet.config sourceDir` drift were skipped because they require repository contents/configuration not present at the documented clone paths. The five sourceless artifact sizes and sdk-seed fingerprints, their Kimi-sandbox provenance, and extraction/rebuild path were not sampled; a URL status alone would not validate those byte/provenance claims.

## Limits

Only read-only local existence/count commands and unauthenticated public HTTP GETs were used. No clones were fetched, no credentials/cookies were used, no files other than this report were written, and no publishing or repository mutation was attempted. Status and byte counts are observations at `observedAt`; public availability does not establish the historical repository/source mappings.

Report: .ufo/waves/round-23/w1/ReverifyOriginRepos.md
