source: ~/Projects/webzites/reports/keepers/repos-r1.md … repos-r8.md (wz-repos lane, run gqab44994c06d7e7a4; sources absent since the 2026-10-12 ~/Projects prune, retained as historical record) — metadata contract S019 (format authority only; entry evidence is the wz-repos reports)
verified-at: 2026-09-21 (wz-repos terminal round r8, run gqab44994c06d7e7a4; original evidence) — historical-not-live-reverified; no live domain recheck performed
recheck: when ~/Projects/webzites is restored — test -e ~/Projects/webzites/reports/keepers/repos-r1.md && test -d ~/Projects/webzites/repos && echo present || echo absent; sources vanished, so operator must restore them from the prune/migration archive or retire this entry as historical

# Origin repos — the 50-clone canonical-source map

Source: `~/Projects/webzites/reports/keepers/repos-r1.md … repos-r8.md` <!-- r18 re-census 2026-10-14: ~/Projects/webzites/reports/keepers/repos-r1.md absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
(wz-repos lane, terminal round 2026-09-21, run `gqab44994c06d7e7a4`).
Clones live at `~/Projects/webzites/repos/<name>` — **read-only evidence <!-- r18 re-census 2026-10-14: ~/Projects/webzites/repos absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
snapshots** cloned via `origin repo clone jo-o-veiga/<name>`; the editable
working checkouts are `~/Projects/<name>` (e.g. `~/Projects/ds4cc-marketplace`). <!-- r18 re-census 2026-10-14: ~/Projects/ds4cc-marketplace absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
`origin repo list` = 224 repos under `jo-o-veiga` (unchanged r4→r8);
50/50 clones re-fetched `HEAD == @{u}` at r8 — zero drift.

## Byte-verified canonical writers (sha256-matched live ↔ repo tip, r5–r8)

| property | canonical repo | verdict |
|---|---|---|
| `ds4cc.com` | `repos/ds4cc-marketplace` (live index sha `b6f65899…`, also == `~/Projects/ds4cc-marketplace`) | byte-verified | <!-- r18 re-census 2026-10-14: ~/Projects/ds4cc-marketplace absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
| `veigapunk.github.io` root | `repos/VeigaPunk.github.io` (sha `20805500…`, the Plazir-15 codex deck) | byte-verified |
| `burnerchrome.kimi.page` | `repos/burnerchrome/index.html` (live 11819B vs 11775B = sdk-seed + serialization delta) | byte-verified |
| `veigapunk.github.io/llm-wiki/` | `repos/llm-wiki` — CI builds `site/` from `site-src/`+`wiki/`; `site/` is never committed | declared+live 200 |
| `veigapunk.github.io/plazir-15-site/` | `repos/plazir-15-site` | live 200 |
| `veigapunk.github.io/charter-ufo-fsd/` | `repos/charter-ufo-fsd` | live 200 |
| `plazir27runs-on.kimi.page` (63KB doctrine) | `repos/charter-ufo-fsd` variant | mapped |
| `plazir27.kimi.page` | `repos/ufo-fsd-alpha/docs/charter-ufo-fsd` [INFERENCE — third variant, sha mismatches both charter clones] | inferred |
| `xsnapshot.app` (queued) | `snapshot-x` (Workers `xsnap`+D1, `wrangler deploy`) newest; `xsnapshot` (static generator) fallback; `x-profile-snapshot` superseded | queued |

## Name traps proved by bytes (round-1 table already warned; these are the sha receipts)

- **`ds4cc-website` ≠ ds4cc.com source.** Its sitemap claims ds4cc.com but
  index sha `70b2241e…` (master, 2026-04-26) is a stale earlier candidate;
  it serves only `veigapunk.github.io/ds4cc-website/`. Canonical is
  `ds4cc-marketplace` — corrected by byte-match in r5.
- **`VeigaPunk.github.io` vs `plazir-15-site` single-writer risk**: both
  clones carry the same codex tree (1337b/512qa/iqrunway/sekhmet/speedrun);
  r5 byte-verified root → `VeigaPunk.github.io`. `plazir-15-site` is the
  project-page face. Edit the right repo for the right URL.
- **`ds4cc-marketplace/burnerchrome/` vendored copy** ≠ `repos/burnerchrome`
  tip — kimi mirror canonical is the standalone repo, not the vendored dir.
- **Not-sites in repos/** (don't map): `DS4CC` (Rust shortcut app),
  `ufo-fsd` (fleet overlay seats), `plazirsoon`, `Plazir27CLI`, `plazir27GT`,
  `plazir27-remediation`, `plazir18`, `properplazir`, `plazirhangar`,
  `plazir-hangar`, `veigapunk-command-center` (private ops map),
  `omegag-site`, `llm-wiki-public`, `llm-wiki-site` (placeholder faces),
  `charterlogs`, `314`, `stkballveigapnk`, `the-kimiraikkoner`,
  `tinyos-ufo`, `ufo-cli`, `ufogrokbd`, `xbgst-*`, `xbrd-grok`, `maua-*`,
  `notesfromthefrontier`, `sekhmet-site`, `website-leaderboard-*`,
  `grok-*`, `cc4cc*`, `harness-tester-*`, `veigapunk-bounty-audit-*`.

## The five sourceless artifacts (sdk-seed fingerprint, zero clone hits — stable r3→r8)

| artifact | size | sdk-seed |
|---|---|---|
| `ufo-fsd.kimi.page` vault (`VEIGAPUNK — Central Vault`) | 9809B | 1 |
| `ufofsd.kimi.page` WIP placeholder | 1756B | 1 |
| `plazir27runson.kimi.page` NIGHT TRILOGY (+`assets/film*.mp4`) | 15705B | 1 |
| `ufo-fsd.kimi.pro` DS4CC Vite shell | 612B | 1 |
| `plazir27.kimi.pro` 404 page (ballot app gone) | 5995B | 0 |

All five: [INFERENCE] built inside Kimi chat sandboxes, never exported to
Origin. Republish/extract path = kimi-surface `rebuild` + operator publish,
or manual DOM extraction into a new Origin repo — **never retype from
memory**.

## Fleet.config sourceDir drift (noted by wz-repos, owner = webzites keeper)

- `burnerchrome-kimi.sourceDir` → vendored `ds4cc-marketplace/burnerchrome`;
  canonical is `repos/burnerchrome` (byte-verdict).
- `ds4cc-com.sourceDir` → `~/Projects/ds4cc-marketplace` (second checkout, <!-- r18 re-census 2026-10-14: ~/Projects/ds4cc-marketplace absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
  byte-identical) — works, but `repos/ds4cc-marketplace` is the tracked clone.
- `veigapunk-page.sourceDir` = null; `repos/VeigaPunk.github.io` is the
  byte-verified root source [INFERENCE for the kimi slot].

## Live re-verification — round 23 (2026-10-21)

Read-only live checks; receipt `.ufo/waves/round-23/receipts/origin-repos.json` (claim, surface, method, observation). A HOLD is an observation on 2026-10-21, not a guarantee. Where this section and earlier text disagree, this section is newer.

- [origin-repos:c1] **STALE** — The documented `~/Projects/webzites/repos` clone root is present. Surface: `/home/vgpnk/Projects/webzites/repos`. Correction: As of 2026-10-21, `/home/vgpnk/Projects/webzites/repos` is absent, so clones are not currently available at the documented path.
- [origin-repos:c2] **HOLD** — The current `origin repo list` contains 224 repositories under `jo-o-veiga`. Surface: `origin repo list | paste - - | wc -l`.
- [origin-repos:c3] **UNVERIFIABLE** — All 50 clone HEADs matched their upstreams with zero drift at r8. Surface: `/home/vgpnk/Projects/webzites/repos`. Unverifiable: The documented clone tree and its individual Git worktrees are absent, so current HEAD/upstream equality for the 50 clones cannot be computed; the r8 result remains historical evidence.
- [origin-repos:c4] **UNVERIFIABLE** — The current `ds4cc.com` index remains byte-verified against the documented `ds4cc-marketplace` checkout. Surface: `GET https://ds4cc.com/; /home/vgpnk/Projects/webzites/repos/ds4cc-marketplace`. Unverifiable: The public page is reachable, but the mapped checkout is absent and the unit records only a truncated digest, so the claimed live-to-repository byte identity cannot be rechecked.
- [origin-repos:c5] **STALE** — The live `burnerchrome.kimi.page` response remains 11,819 bytes as recorded in the row. Surface: `https://burnerchrome.kimi.page/`. Correction: As of 2026-10-21, GET https://burnerchrome.kimi.page/ returned HTTP 200 with 11,976 bytes, not the cited 11,819-byte live size; the repository-side 11,775-byte comparison is not currently verifiable because its checkout is absent.
- [origin-repos:c6] **HOLD** — The listed GitHub Pages root and the `llm-wiki`, `plazir-15-site`, and `charter-ufo-fsd` paths currently return HTTP 200. Surface: `GET https://veigapunk.github.io/; GET https://veigapunk.github.io/llm-wiki/; GET https://veigapunk.github.io/plazir-15-site/; GET https://veigapunk.github.io/charter-ufo-fsd/`.
- [origin-repos:c7] **HOLD** — The listed `plazir27runs-on.kimi.page` public property is currently reachable. Surface: `https://plazir27runs-on.kimi.page/`.
- [origin-repos:c8] **STALE** — The inferred `plazir27.kimi.page` property is currently served as a live mapped variant. Surface: `https://plazir27.kimi.page/`. Correction: As of 2026-10-21, GET https://plazir27.kimi.page/ returns HTTP 404, so this is not a currently served public property and its inferred live-source mapping should be withdrawn or retested only after a working endpoint exists.


## Round-24 path reconciliation

These dated corrections supersede only current local-state readings of the cited lines; original bytes and coordinates are preserved. Evidence: `.ufo/waves/round-24/c1-receipts/` and `corpus/knowledge/freshness-sidecar.json` (lane-relative).

- 2026-10-21: ~/Projects/ds4cc-marketplace present (test -e exit 0; checkout 1fbdb8ed); prior local-state annotations at corpus/knowledge/origin-repos.md:11 are historical. Deployment, chat binding and byte continuity with the historical checkout remain unverified.
- 2026-10-21: ~/Projects/ds4cc-marketplace present (test -e exit 0; checkout 1fbdb8ed); prior local-state annotations at corpus/knowledge/origin-repos.md:19 are historical. Deployment, chat binding and byte continuity with the historical checkout remain unverified.
- 2026-10-21: ~/Projects/ds4cc-marketplace present (test -e exit 0; checkout 1fbdb8ed); prior local-state annotations at corpus/knowledge/origin-repos.md:70 are historical. Deployment, chat binding and byte continuity with the historical checkout remain unverified.
