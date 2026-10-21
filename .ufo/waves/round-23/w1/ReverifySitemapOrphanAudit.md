# sitemap-orphan-audit — C1 freshness re-verification

## Verdict

Recommend recording this scoped receipt: 5 of 8 sampled claims are STALE and 3 HOLD. The 2026-09-28/09-30 observations and one cited local source path are not current/available as recorded. This is an author-side freshness report, not an independent admission; it does not establish live-to-artifact membership or prove an orphan count.

## Findings

- **P2 — Plazir live sitemap count is stale (C1 / freshness).** The base claim says 8 locs. Command A below performed a public GET; observed output (relevant fields): `status=200, bytes=1144, loc_count=7`. **Smallest fix:** append the dated correction in the receipt and distinguish this live count from unavailable source-side counts.
- **P2 — ds4cc sitemap is no longer a live 404 (C1 / freshness).** Command A GET returned `status=200, bytes=7565, loc_count=96`, not 404. **Smallest fix:** append the dated correction; do not reuse the earlier staged 93-loc count as the current live count.
- **P2 — Cited staged sitemap is absent at the local path (C1 / freshness).** Command C below ran `test -e` against `/home/vgpnk/Projects/ds4cc-marketplace/sitemap.xml`; observed output: `absent /home/vgpnk/Projects/ds4cc-marketplace/sitemap.xml`. The claim asserts that the staged 93-loc sitemap exists at local HEAD. **Smallest fix:** append the dated correction and do not claim a current local staged copy at that path.
- **P2 — Charter live marker changed (C1 / freshness).** Command A GET returned HTTP 200, 53,660 bytes, with the literal `2026-09-30 scribe beat (the-scribe via local-fallback)`, not the recorded 2026-09-28 literal. **Smallest fix:** append the dated live-marker correction.
- **P2 — The dead-404 set is stale for lucario (C1 / freshness).** Command B GETs returned 404/13,409 bytes for `plazir15.kimi.page` and `charter-ufo-fsd.kimi.page`, but 200/3,435 bytes for `veigapunk.github.io/lucario/`. **Smallest fix:** remove lucario from the current dead-404 set while retaining the two observed 404 rows.

### C1 receipt

```json
{
  "unit": "sitemap-orphan-audit",
  "path": "corpus/knowledge/sitemap-orphan-audit.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "plazir15-ghp ✓ (8 locs)",
      "claim": "The live plazir sitemap currently lists 8 <loc> URLs.",
      "surface": "https://veigapunk.github.io/plazir-15-site/sitemap.xml",
      "method": "GET",
      "observation": "status=200, bytes=1144, loc_count=7",
      "verdict": "STALE",
      "correction": "On 2026-10-21, the live plazir-15-site sitemap returned HTTP 200 with 7 <loc> entries, not 8."
    },
    {
      "id": "c1",
      "anchor": "charter-ghp ✓ (2 locs)",
      "claim": "The live charter sitemap currently lists 2 <loc> URLs.",
      "surface": "https://veigapunk.github.io/charter-ufo-fsd/sitemap.xml",
      "method": "GET",
      "observation": "status=200, bytes=502, loc_count=2",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "ds4cc.com/sitemap.xml → **404 live",
      "claim": "The public ds4cc.com sitemap endpoint returns HTTP 404.",
      "surface": "https://ds4cc.com/sitemap.xml",
      "method": "GET",
      "observation": "status=200, bytes=7565, loc_count=96",
      "verdict": "STALE",
      "correction": "On 2026-10-21, https://ds4cc.com/sitemap.xml returned HTTP 200 and listed 96 <loc> entries, not HTTP 404."
    },
    {
      "id": "c1",
      "anchor": "**404 live but exists at local HEAD** (93",
      "claim": "The staged 93-loc ds4cc sitemap exists at local HEAD.",
      "surface": "/home/vgpnk/Projects/ds4cc-marketplace/sitemap.xml",
      "method": "test -e",
      "observation": "absent /home/vgpnk/Projects/ds4cc-marketplace/sitemap.xml",
      "verdict": "STALE",
      "correction": "On 2026-10-21, the cited local /home/vgpnk/Projects/ds4cc-marketplace/sitemap.xml file was absent, so the 93-loc staged-copy presence claim does not hold at that path."
    },
    {
      "id": "c1",
      "anchor": "plazir live `/tetris/` = 200/1,650B",
      "claim": "The direct live plazir /tetris/ route returns HTTP 200 and 1,650 bytes.",
      "surface": "https://veigapunk.github.io/plazir-15-site/tetris/",
      "method": "GET",
      "observation": "status=200, bytes=1650, location=null",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "live literal is now `2026-09-28 scribe beat (the-scribe via local-fallback)`.",
      "claim": "The current charter homepage marker is 2026-09-28 scribe beat (the-scribe via local-fallback).",
      "surface": "https://veigapunk.github.io/charter-ufo-fsd/",
      "method": "GET",
      "observation": "status=200, bytes=53660; matched `s=\"thread-note rv\" data-i18n=\"s3.scribeBeat\">2026-09-30 scribe beat (<b>the-scribe</b> via <code>local-fallback</code>): <`",
      "verdict": "STALE",
      "correction": "On 2026-10-21, the charter homepage contained `2026-09-30 scribe beat (the-scribe via local-fallback)`, not the `2026-09-28` literal."
    },
    {
      "id": "c1",
      "anchor": "`plazir15`,\n`charter-ufo-fsd-kimi`, `lucario` = dead 404 rows;",
      "claim": "The plazir15, charter-ufo-fsd-kimi, and lucario rows each return HTTP 404.",
      "surface": "https://plazir15.kimi.page/; https://charter-ufo-fsd.kimi.page/; https://veigapunk.github.io/lucario/",
      "method": "GET",
      "observation": "plazir15.kimi.page status=404 bytes=13409; charter-ufo-fsd.kimi.page status=404 bytes=13409; veigapunk.github.io/lucario/ status=200 bytes=3435",
      "verdict": "STALE",
      "correction": "On 2026-10-21, plazir15.kimi.page and charter-ufo-fsd.kimi.page still returned HTTP 404, but https://veigapunk.github.io/lucario/ returned HTTP 200, so lucario is no longer in the dead-404 set."
    },
    {
      "id": "c1",
      "anchor": "`plazir27-kimi-pro` =\npreview-404",
      "claim": "plazir27-kimi-pro redirects to the preview-404 page.",
      "surface": "https://plazir27.kimi.pro/",
      "method": "GET",
      "observation": "status=302, bytes=72, location=https://statics.kimi.ai/pages/preview-404-en.html",
      "verdict": "HOLD"
    }
  ]
}
```

## Checked and held

- Read the entire current unit, the frozen contract, the C1 population, and the base-revision unit (`b5d599e19bead54b96f589444e9ec64cdf67c28a`) to select exact anchors. Base command: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show b5d599e19bead54b96f589444e9ec64cdf67c28a:corpus/knowledge/sitemap-orphan-audit.md | nl -ba`.
- **Command A (read-only public GETs):** `node -e 'const rows=[['"'"'plazir-sitemap'"'"','"'"'https://veigapunk.github.io/plazir-15-site/sitemap.xml'"'"'],['"'"'charter-sitemap'"'"','"'"'https://veigapunk.github.io/charter-ufo-fsd/sitemap.xml'"'"'],['"'"'ds4cc-sitemap'"'"','"'"'https://ds4cc.com/sitemap.xml'"'"'],['"'"'plazir-tetris'"'"','"'"'https://veigapunk.github.io/plazir-15-site/tetris/'"'"'],['"'"'charter-home'"'"','"'"'https://veigapunk.github.io/charter-ufo-fsd/'"'"']]; (async()=>{for(const [name,url] of rows){try{const r=await fetch(url,{redirect:"manual"});const b=Buffer.from(await r.arrayBuffer());const t=b.toString("utf8");const o={name,url,status:r.status,bytes:b.length,location:r.headers.get("location")};if(name.endsWith("sitemap")){o.locs=[...t.matchAll(/<loc>\s*([^<]+)\s*<\/loc>/gi)].map(m=>m[1]);o.loc_count=o.locs.length;}if(name==="charter-home")o.scribeBeatMatches=[...t.matchAll(/.{0,45}\d{4}-\d{2}-\d{2} scribe beat.{0,55}/g)].map(m=>m[0]);console.log(JSON.stringify(o));}catch(e){console.log(JSON.stringify({name,url,error:String(e)}));}}})()'`. Exact relevant observations: plazir sitemap `status=200, bytes=1144, loc_count=7`; charter sitemap `status=200, bytes=502, loc_count=2`; ds4cc sitemap `status=200, bytes=7565, loc_count=96`; plazir `/tetris/` `status=200, bytes=1650, location=null`; charter homepage `status=200, bytes=53660`, matching `s="thread-note rv" data-i18n="s3.scribeBeat">2026-09-30 scribe beat (<b>the-scribe</b> via <code>local-fallback</code>): <`.
- **Command B (read-only public GETs):** `node -e 'const rows=[['"'"'plazir15-kimi'"'"','"'"'https://plazir15.kimi.page/'"'"'],['"'"'charter-kimi'"'"','"'"'https://charter-ufo-fsd.kimi.page/'"'"'],['"'"'plazir27-kimipro'"'"','"'"'https://plazir27.kimi.pro/'"'"'],['"'"'lucario-ghp'"'"','"'"'https://veigapunk.github.io/lucario/'"'"']]; (async()=>{for(const [name,url] of rows){try{const r=await fetch(url,{redirect:"manual"});const b=Buffer.from(await r.arrayBuffer());console.log(JSON.stringify({name,url,status:r.status,bytes:b.length,location:r.headers.get("location")}));}catch(e){console.log(JSON.stringify({name,url,error:String(e)}));}}})()'`. Exact observations: plazir15 Kimi `status=404, bytes=13409`; charter Kimi `status=404, bytes=13409`; plazir27 Kimi Pro `status=302, bytes=72, location=https://statics.kimi.ai/pages/preview-404-en.html`; lucario GHP `status=200, bytes=3435`.
- **Command C (read-only local existence checks):** `for p in /tmp/orphan-check.mjs /home/vgpnk/Projects/ds4cc-marketplace/sitemap.xml /home/vgpnk/Projects/ds4cc-marketplace/.github/workflows/pages.yml /home/vgpnk/Projects/plazir-15-site/sitemap.xml /home/vgpnk/Projects/plazir-15-site/.github/workflows/pages.yml /home/vgpnk/Projects/webzites/fleet/fleet.config.json; do if test -e "$p"; then printf 'present %s\n' "$p"; else printf 'absent %s\n' "$p"; fi; done`. All six outputs were `absent <path>`.
- HOLD observations: charter's live sitemap still has 2 locs; `/tetris/` remains 200/1,650 bytes; and plazir27.kimi.pro still redirects (302) to the preview-404 page. Both Kimi hard-404 root probes also remain 404, though the combined dead-row claim is stale because lucario is 200.

## Limits

- The 93-loc staged-copy claim is marked STALE against the cited absent local path; no claim is made about a remote repository HEAD's sitemap count. The 0-orphan / “fresh snapshot of the entire checked-out tree” conclusion and all other source-side membership claims (including the 102 source-side total and five-commit lead) were not reverified: the cited `pages.yml`, source checkouts, and fleet config are absent, and no actual uploaded/deployed artifact or build output was available. The unit's round-20 correction itself requires comparison with that actual output; no checkout-based inference was used.
- Skipped the historical 103-URL all-GET/zero-dead sweep as a current aggregate: only the selected public surfaces were checked, and the three current sitemap GETs total 105 locs (96 + 7 + 2), not the old 103. No status sweep of those 105 URLs was performed.
- The live plazir sitemap's seven `<loc>`s omit `/tetris/`, while direct `/tetris/` GET is 200. This observation alone does not establish a live orphan: its presence in the source or deployed artifact was not checked.
- No selected claim was UNVERIFIABLE. The selected missing local sitemap file asserts presence and was marked STALE; unavailable workflow/artifact membership claims were skipped with the reasons above. No public auth, cookies, forms, publish actions, local modifications, or tool installations were used.
