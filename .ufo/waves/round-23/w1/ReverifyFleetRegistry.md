## Verdict

C1 freshness is mixed: three selected live-status claims are **STALE**, the current `sites[]` count is **UNVERIFIABLE**, and four selected current-surface claims are **HOLD**. The registry source is still absent at the recorded path. This is an author-side re-verification, not an independent admission.

## Findings

### P2 — `plazir27.kimi.page` is not currently live

- **Exact command:** `curl -sS -L --max-time 25 -o /dev/null -w 'http=%{http_code} final=%{url_effective} bytes=%{size_download}\n' https://plazir27.kimi.page/`
- **Exact observed output:** `http=404 final=https://plazir27.kimi.page/ bytes=13409`
- **Body check:** the fetched HTML contains `<title>404</title>` and `<div class="text">404 Page Not Found</div>`.
- **Impacted claim / axis:** the `plazir27-kimi-page` row says `live (canonical kimi charter)`; C1 freshness.
- **Smallest fix:** change that row's live status to broken/404 unless a current GET verifies a replacement URL.
- **Correction:** As of 2026-10-21, `https://plazir27.kimi.page/` returns HTTP 404 (`404 Page Not Found`) rather than serving a live canonical Kimi charter.

### P2 — `plazir27runson.kimi.page` is not currently live

- **Exact command:** `curl -sS -L --max-time 25 -o /dev/null -w 'http=%{http_code} final=%{url_effective} bytes=%{size_download}\n' https://plazir27runson.kimi.page/`
- **Exact observed output:** `http=404 final=https://plazir27runson.kimi.page/ bytes=13409`
- **Body check:** the fetched HTML contains `<title>404</title>` and `<div class="text">404 Page Not Found</div>`.
- **Impacted claim / axis:** the `plazir27runson` row says `live (Night Trilogy)`; C1 freshness.
- **Smallest fix:** mark this row broken/404; do not merge it with the distinct `plazir27runs-on` row on hostname similarity alone.
- **Correction:** As of 2026-10-21, `https://plazir27runson.kimi.page/` returns HTTP 404 (`404 Page Not Found`), so its `live (Night Trilogy)` status is stale.

### P2 — `xsnapshot.app` no longer returns NXDOMAIN

- **Exact command:** `curl -sS -L --max-time 25 -o /dev/null -w 'http=%{http_code} final=%{url_effective} bytes=%{size_download}\n' https://xsnapshot.app/`
- **Exact observed output:** `http=200 final=https://xsnapshot.app/ bytes=1985`
- **Body check:** `<title>xsnapshot — your X profile, persistent and crawlable</title>`; `<span class="tag">domain live · build in progress</span>`.
- **Impacted claim / axis:** the `xsnapshot-app` row says `queued (NXDOMAIN)`; C1 freshness.
- **Smallest fix:** replace the NXDOMAIN reason with the observed live/build-in-progress state and reassess the queued label against the operator's publish criteria.
- **Correction:** As of 2026-10-21, `https://xsnapshot.app/` resolves and returns HTTP 200 with a page stating `domain live · build in progress`, so NXDOMAIN is no longer an accurate basis for its queued status.

### P3 — the current registry row count cannot be reverified

- **Exact command:** `test -f "/home/vgpnk/Projects/webzites/fleet/fleet.config.json" && node -p 'const c=require("/home/vgpnk/Projects/webzites/fleet/fleet.config.json"); [c.schema,c.updatedAt,c.sites.length].join(" ")' || echo "absent: operator must restore the fleet source or retire this entry"`
- **Exact observed output:** `absent: operator must restore the fleet source or retire this entry`
- **Impacted claim / axis:** `len(sites) = 21` and any current status/updatePath totals; C1 freshness.
- **Smallest fix:** keep those numbers explicitly historical until the canonical config is restored and counted, or retire the current-count claims if it will not be restored.

## Checked and held

Anchors below were copied from the `b5d599e19bead54b96f589444e9ec64cdf67c28a` blob of `corpus/knowledge/fleet-registry.md`. The following is the single C1 receipt for this unit:

```json
{
  "unit": "fleet-registry",
  "path": "corpus/knowledge/fleet-registry.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1-01",
      "anchor": "<!-- r18 re-census 2026-10-14: ~/Projects/webzites/fleet/fleet.config.json absent — gone in the 2026-10-12",
      "claim": "The canonical fleet configuration is currently absent at its recorded source path.",
      "surface": "test -e /home/vgpnk/Projects/webzites/fleet/fleet.config.json",
      "method": "test -e",
      "observation": "absent: /home/vgpnk/Projects/webzites/fleet/fleet.config.json",
      "verdict": "HOLD"
    },
    {
      "id": "c1-02",
      "anchor": "Verified 2026-09-28: `len(sites)` = **21 rows**",
      "claim": "The current raw sites[] array contains 21 rows.",
      "surface": "test -f \"/home/vgpnk/Projects/webzites/fleet/fleet.config.json\" && node -p 'const c=require(\"/home/vgpnk/Projects/webzites/fleet/fleet.config.json\"); [c.schema,c.updatedAt,c.sites.length].join(\" \")' || echo \"absent: operator must restore the fleet source or retire this entry\"",
      "method": "run",
      "observation": "absent: operator must restore the fleet source or retire this entry",
      "verdict": "UNVERIFIABLE",
      "reason": "The canonical fleet.config.json is absent, so there is no current sites[] array to count; the command took its absent-file branch and the 21-row value remains historical evidence only."
    },
    {
      "id": "c1-03",
      "anchor": "`high` (revenue/brand: veigapunk-page, ds4cc-com)",
      "claim": "Both named high-priority endpoints remain publicly reachable at their listed URLs.",
      "surface": "GET https://veigapunk.kimi.page/; GET https://ds4cc.com/",
      "method": "GET",
      "observation": "http=200 final=https://veigapunk.kimi.page/ bytes=10059; http=200 final=https://ds4cc.com/ bytes=76159",
      "verdict": "HOLD"
    },
    {
      "id": "c1-04",
      "anchor": "lucario.kimi.page | **broken (404, never published — see warning)** | `~/Projects/lucario` (canonical: `veigapunk.github.io/lucario/`)",
      "claim": "The current endpoint split remains a 404 at the Kimi alias and a live GitHub Pages canonical; this does not re-prove the historical ‘never published’ wording.",
      "surface": "GET https://lucario.kimi.page/; GET https://veigapunk.github.io/lucario/",
      "method": "GET",
      "observation": "http=404 final=https://lucario.kimi.page/ bytes=13409; http=200 final=https://veigapunk.github.io/lucario/ bytes=3435",
      "verdict": "HOLD"
    },
    {
      "id": "c1-05",
      "anchor": "| plazir27-kimi-page | plazir27.kimi.page | live (canonical kimi charter) | charter repo |",
      "claim": "The plazir27.kimi.page row remains live as the canonical Kimi charter.",
      "surface": "GET https://plazir27.kimi.page/",
      "method": "GET",
      "observation": "http=404 final=https://plazir27.kimi.page/ bytes=13409; body contains <title>404</title> and 404 Page Not Found",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, https://plazir27.kimi.page/ returns HTTP 404 (404 Page Not Found) rather than serving a live canonical Kimi charter."
    },
    {
      "id": "c1-06",
      "anchor": "| plazir27runson | plazir27runson.kimi.page | live (Night Trilogy) | none |",
      "claim": "The plazir27runson.kimi.page row is live (Night Trilogy).",
      "surface": "GET https://plazir27runson.kimi.page/",
      "method": "GET",
      "observation": "http=404 final=https://plazir27runson.kimi.page/ bytes=13409; body contains <title>404</title> and 404 Page Not Found",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, https://plazir27runson.kimi.page/ returns HTTP 404 (404 Page Not Found), so its live (Night Trilogy) status is stale."
    },
    {
      "id": "c1-07",
      "anchor": "| xsnapshot-app | xsnapshot.app | queued (NXDOMAIN) | none |",
      "claim": "The xsnapshot-app row is queued because xsnapshot.app is NXDOMAIN.",
      "surface": "GET https://xsnapshot.app/",
      "method": "GET",
      "observation": "http=200 final=https://xsnapshot.app/ bytes=1985; title: xsnapshot — your X profile, persistent and crawlable; page tag: domain live · build in progress",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, https://xsnapshot.app/ resolves and returns HTTP 200 with a page stating domain live · build in progress, so NXDOMAIN is no longer an accurate basis for its queued status."
    },
    {
      "id": "c1-08",
      "anchor": "| charter-ghp | veigapunk.github.io/charter-ufo-fsd | live (canonical doc) |",
      "claim": "The listed GitHub Pages canonical charter document is currently live.",
      "surface": "GET https://veigapunk.github.io/charter-ufo-fsd/",
      "method": "GET",
      "observation": "http=200 final=https://veigapunk.github.io/charter-ufo-fsd/ bytes=53660",
      "verdict": "HOLD"
    }
  ]
}
```

The additional URL checks used the read-only GET template `curl -sS -L --max-time 25 -o /dev/null -w 'http=%{http_code} final=%{url_effective} bytes=%{size_download}\n' <URL>`; observations are exact. The checked row endpoints not selected as separate receipt claims were:

| Row | Observed GET result |
|---|---|
| `vault` — `https://ufo-fsd.kimi.page/` | `http=200 final=https://ufo-fsd.kimi.page/ bytes=9966` |
| `ds4cc-kimi-mirror` — `https://ds4cc.kimi.page/` | `http=200 final=https://ds4cc.kimi.page/ bytes=74641` |
| `burnerchrome-kimi` — `https://burnerchrome.kimi.page/` | `http=200 final=https://burnerchrome.kimi.page/ bytes=11976` |
| `ufofsd` — `https://ufofsd.kimi.page/` | `http=200 final=https://ufofsd.kimi.page/ bytes=1913` |
| `ufofsd-charter` — `https://ufofsd-charter.kimi.page/` | `http=200 final=https://ufofsd-charter.kimi.page/ bytes=9273` |
| `plazir27runs-on` — `https://plazir27runs-on.kimi.page/` | `http=200 final=https://plazir27runs-on.kimi.page/ bytes=63421` |
| `plazir15` — `https://plazir15.kimi.page/` | `http=404 final=https://plazir15.kimi.page/ bytes=13409` |
| `plazir15-ghp` — `https://veigapunk.github.io/plazir-15-site/` | `http=200 final=https://veigapunk.github.io/plazir-15-site/ bytes=38337` |
| `charter-ufo-fsd-kimi` — `https://charter-ufo-fsd.kimi.page/` | `http=404 final=https://charter-ufo-fsd.kimi.page/ bytes=13409` |
| `plazir27-kimi-pro` — `https://plazir27.kimi.pro/` | `http=200 final=https://statics.kimi.ai/pages/preview-404-en.html bytes=5995`; body contains `<title>404</title>` and `404 Page Not Found` |
| `ufo-fsd-kimi-pro` — `https://ufo-fsd.kimi.pro/` | `http=200 final=https://ufo-fsd.kimi.pro/ bytes=612` |
| `charter-ghp` — `https://veigapunk.github.io/charter-ufo-fsd/` | `http=200 final=https://veigapunk.github.io/charter-ufo-fsd/ bytes=53660` |

Skipped claims and why:

- The current `12 live / 3 pruned / 3 broken / 3 queued` and `14 / 4 / 2 / 1` `updatePath` distributions were not separately receipted: the canonical config is absent, so no current rows can establish these counts. The 21-row count is explicitly UNVERIFIABLE above.
- The `charter-ghp` stale-marker episode is dated 2026-09-28 and cannot be reconstructed from today's GET. The current page is 200 and its HTML contains a `2026-09-30 scribe beat`, but the expected marker/configuration and `src/probe.mjs` are unavailable because `/home/vgpnk/Projects/webzites/fleet/` is absent. I therefore did not treat the historical marker claim as a current pass/fail.
- The `ds4cc-kimi-mirror` “STALE (~Aug-29 DOM)” age/marker claim was not reverified: the URL is reachable (200), but its expected marker and source pin are unavailable without the missing config/report/source. Likewise, the `lucario` “never published” and README quotation are historical; the current 404/200 split does not prove publication history, and `/home/vgpnk/Projects/lucario` is absent.
- Remaining rows in the table above were checked but omitted from the eight-claim receipt because their current results did not reveal a new status discrepancy, or because the receipt already covers higher-impact findings. The `ufofsd-charter` 200 response does not by itself refute its `pruned→plazir27-kimi-page` registry label: the unit describes pruning as a registry-level label, not an HTTP-down state.
- `ds4cc-kimi-mirror-vault-row`, `snapshot-kimi-pro`, and `burnerchrome-com` have `null` URLs, so there is no public URL to GET. Their labels were not tested beyond that recorded absence.
- Schema-field definitions, raw-byte marker matching, and `probe.mjs`'s pruning behavior were not independently checked: the noted fleet source tree, `fleet.dedupe-report.md`, and `src/probe.mjs` are absent. No inference from the HTTP sweep is used as proof of those code behaviors.

## Limits

All public-surface checks were read-only GETs; local checks were read-only existence tests and a read of the base-commit blob. No authentication, cookies, publishing, deploy, source edits, or tool installation/update was used. HTTP reachability and response size do not establish title-regex or expected-marker correctness without the absent canonical configuration. The fleet config and dedupe report were both absent at the checked paths; the present row counts and pin details therefore remain historical rather than live-reverified.
