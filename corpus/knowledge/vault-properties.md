source: Historical fleet/vault-properties.json, Kimi surface source and 2026-09-28 live PROPERTIES[] observations cited below; external fleet evidence is unavailable locally. Metadata authority only: S019 in corpus/SOURCES.md, not present-day property state.
verified-at: 2026-09-28 original baseline GETs and +157B seed finding, introduced in kake commit ed0b632; dd4eabf only re-pinned a line reference. Historical-not-live-reverified; no round-21 domain recheck.
recheck: historical-only; no local copy of fleet/vault-properties.json or kimi-surface.mjs exists here, so the operator must restore the fleet tree or retire this entry. Local check once restored: node -p "const j=require('./fleet/vault-properties.json'); j.generatedAt+' '+j.properties.length" (expect 13 entries); the live GET Method block stays operator-run, not run here

# Vault PROPERTIES[] — the JS-rendered surface, audited without a browser

Scope: `veigapunk.kimi.page` + `ufo-fsd.kimi.page` (byte-twin vaults). The
fleet index is a client-rendered array literal — a static GET sees the full
`const PROPERTIES = [...]` source, so **rot-checking needs NO rendered DOM**:
extract the literal, GET every `url`. Residual README gap closed 2026-09-28.

## Method (repeatable)

```bash
curl -s https://veigapunk.kimi.page/ > /tmp/vault.html
node -e "const s=require('fs').readFileSync('/tmp/vault.html','utf8');
  const d=eval(s.match(/const PROPERTIES = (\[[\s\S]*?\]);/)[1]);
  d.forEach(x=>console.log(x.status, x.name, '->', x.url))"
# GET every non-null url; classify 200 / redirect / 404 / NXDOMAIN
```

`fleet/vault-properties.json` (mtime 2026-09-20, `generatedAt` 23:40:17Z) is a
lowercase-schema extraction (`properties[]`, 13 entries, keys
name/tld/desc/status/url/vid/com) — **verified byte-equivalent to the live
literal** on both twins 2026-09-28; safe to reuse as the canonical checklist.

## Baseline 2026-09-28 (self-verified GETs)

13 entries, 3 `url:null` (ds4cc-mirror, snapshot.kimi.pro, burnerchrome .com),
10 live URLs. **3 of the 10 are dead while marked `"live"`**:

| entry | claimed | actual 09-28 |
|---|---|---|
| `charter-ufo-fsd.kimi.page` | live | **404** (13,409B sentinel, sha `93ddca9a…`) |
| `plazir15.kimi.page` | live | **404** (same sentinel) |
| `plazir27.kimi.pro` | live | **302 → `statics.kimi.ai/pages/preview-404-en.html`** (soft-404; distinct class from hard 404) |
| `xsnapshot.app` | queue | NXDOMAIN (curl exit 6; `dig` unavailable — `getent hosts` rc=2) |
| ds4cc entry | live | `url:null` while `ds4cc.kimi.page` serves — **link missing, not dead** |

6 healthy: ds4cc.com, veigapunk, burnerchrome, plazir27runson, ufofsd,
ufo-fsd.kimi.pro (all 200). `lucario` is absent from PROPERTIES[] entirely —
not just the dead slot; the row isn't listed.

Cross-checks: zero same-origin (kimi.page) links inside PROPERTIES[] — the
vault links only outward; zero `/cdn-cgi/` noise; zero `<img>/<video>/<iframe>`
in vault body.


`sourceDir:null` is the single hard blocker: `cmdUpdate` refuses at
`kimi-surface.mjs:483` when no `sourceDir/index.html` exists; `cmdRecreate`
refuses at `:845-849` when the slot serves live 200 (dead-slot gate, code 3).

- `veigapunk-page`, `ufofsd`, `ufo-fsd.kimi.page` — **fully self-contained
  single-file bodies** (10,059B / 1,913B / 9,966B). Recipe: save body →
  `index.html` → set `sourceDir` → `update --chat=<bound>` (veigapunk:
  `1a0c20ea-6372-…`; ufofsd: `1a073c1f-5792-…`). Vault has NO bound chat →
  `recreate --new-chat --canonical=https://veigapunk.kimi.page/` (fetch-fallback
  covered at `:916-921`; marker `WZ-CANARY-FIX-veigapunk` is in the twin body).
  Auto-twin resolution at `:817-822` never matches two `sourceDir:null` rows —
  pass `--canonical` explicitly.
- `plazir27runson` — NOT self-contained: 7 same-origin assets incl. 3 film
  `.mp4` = ~147MB (exceeds the 32MB `fetchLive` maxBuffer at `:339-346` and any
  card budget). Extract `index.html` + `assets/` minus films; fire with
  `--zip-exclude='assets/*.mp4'` (exclude chain `:903`, zip spawn `:906`).
- `ufo-fsd.kimi.pro` — 612B SPA shell is NOT the content: real bundle is
  `/assets/index-Bw9NLFv4.js` (739,018B) + `index-B-Hzbnm3.css` (82,871B); a
  body-only fire produces a blank DS4CC. Extract html+assets (~822KB zip).
- `plazir27-kimi.pro` — nothing extractable (302 sentinel only).

## Fleet-wide seed injection (+157B)

Between 09-26 and 09-28 every kimi-surface body grew exactly **+157B**: the
injected `sdk-seed.js` script tag gained `data-kimi-disable-watermark="false"
data-kimi-analytics="true" data-kimi-website-id="…" data-kimi-website-env=
"published"` attributes. Consequence: post-publish byte-digest checks MUST
normalize the seed tag; byte deltas alone cannot carry freshness evidence.
(Verified across 6 rows: ds4cc 74,484→74,641; plazir27 8,733→8,890; veigapunk
9,902→10,059; vault 9,809→9,966; ufofsd-charter 9,116→9,273; runs-on
63,264→63,421.)

## Site-id collision (keeper flag)

`data-kimi-website-id="1a0acf59-c082-8794-8000-0000eaa74687"` serves on BOTH
`ufo-fsd.kimi.pro` AND `ufo-fsd.kimi.page` — config note at
`fleet.config.json:298` claims "fleet-unique 1/17"; now 2/18. An `update` fire
on one could co-write the other; re-pin the `ufo-fsd-kimi-pro` marker to a
non-colliding literal.
