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

## Live re-verification — round 23 (2026-10-21)

Read-only live checks; receipt `.ufo/waves/round-23/receipts/vault-properties.json` (claim, surface, method, observation). A HOLD is an observation on 2026-10-21, not a guarantee. Where this section and earlier text disagree, this section is newer.

- [vault-properties:c1] **HOLD** — A static GET exposes a PROPERTIES literal with 13 records, 3 null URLs and 10 non-null URLs; lucario is absent from that literal. Surface: `https://veigapunk.kimi.page/ and https://ufo-fsd.kimi.page/`.
- [vault-properties:c2] **STALE** — The veigapunk.kimi.page and ufo-fsd.kimi.page GET bodies are byte-twin responses. Surface: `https://veigapunk.kimi.page/ and https://ufo-fsd.kimi.page/`. Correction: As of 2026-10-21, the GET bodies are not byte-identical: veigapunk.kimi.page is 10,059 bytes (SHA-256 a0a7f33aba443a85a4952a0bf57aa52947fdf95638b5ac7aba1c7d92b87a92fb) and ufo-fsd.kimi.page is 9,966 bytes (SHA-256 d93d6a0c00e773f74389ebc6d052773262052d6a0fc6b6a21581f1c12cb3920c).
- [vault-properties:c3] **STALE** — The unit reports three of the ten non-null property URLs as dead while marked live. Surface: `https://charter-ufo-fsd.kimi.page; https://plazir15.kimi.page; https://plazir27.kimi.pro; https://plazir27runson.kimi.page`. Correction: As of 2026-10-21, four of the nine URLs marked live (among ten non-null property URLs) are non-200: charter-ufo-fsd.kimi.page, plazir15.kimi.page, and plazir27runson.kimi.page return 404; plazir27.kimi.pro returns 302 to https://statics.kimi.ai/pages/preview-404-en.html (soft-404).
- [vault-properties:c4] **STALE** — The queued xsnapshot.app URL is NXDOMAIN. Surface: `https://xsnapshot.app`. Correction: As of 2026-10-21, xsnapshot.app still has queue status in the literal but resolves to 2606:4700:3032::ac43:cafd and 2606:4700:3030::6815:163d, and GET returns HTTP 200 (1,985 bytes; SHA-256 63b7146c39df128f5ebab88c4e60b652d1a7dfce65a443966298928807827da0), not NXDOMAIN.
- [vault-properties:c5] **STALE** — The six listed properties are healthy and all return 200. Surface: `https://ds4cc.com; https://veigapunk.kimi.page; https://burnerchrome.kimi.page; https://plazir27runson.kimi.page; https://ufofsd.kimi.page; https://ufo-fsd.kimi.pro; https://xsnapshot.app`. Correction: As of 2026-10-21, the six non-null property URLs returning 200 are veigapunk.kimi.page, burnerchrome.kimi.page, ufofsd.kimi.page, ufo-fsd.kimi.pro, ds4cc.com, and xsnapshot.app; plazir27runson.kimi.page now returns 404 (13,409 bytes; SHA-256 93ddca9a021664d562e698eb99d52b84d696f81485847dcfeaf6f4a5c8fca966).
- [vault-properties:c6] **HOLD** — The website id 1a0acf59-c082-8794-8000-0000eaa74687 occurs on both ufo-fsd.kimi.pro and ufo-fsd.kimi.page. Surface: `https://ufo-fsd.kimi.pro/ and https://ufo-fsd.kimi.page/`.
- [vault-properties:c7] **HOLD** — ufo-fsd.kimi.pro serves a 612-byte shell referencing the 739,018-byte JavaScript bundle and 82,871-byte stylesheet. Surface: `https://ufo-fsd.kimi.pro/; https://ufo-fsd.kimi.pro/assets/index-Bw9NLFv4.js; https://ufo-fsd.kimi.pro/assets/index-B-Hzbnm3.css`.
- [vault-properties:c8] **HOLD** — The lane has no local copy at the expected source paths of fleet/vault-properties.json or kimi-surface.mjs. Surface: `/home/vgpnk/Projects/shokunin/kake-shokunin/fleet/vault-properties.json; /home/vgpnk/Projects/shokunin/kake-shokunin/fleet/kimi-surface.mjs; /home/vgpnk/Projects/shokunin/kake-shokunin/kimi-surface.mjs`.
