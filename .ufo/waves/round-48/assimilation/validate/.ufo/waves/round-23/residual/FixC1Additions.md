# Round 23 C1 additions review — FixC1Additions

Date: 2026-10-21. Scope: the five requested receipts and their appended unit sections, compared with the wave-2 reports and frozen revisions. Review recommendation: **no actionable finding in the reviewed additions**.

## Diff reviewed

Compared current receipt JSON with `5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd` extracted in the isolated scratch clone:

- `drift-detection`: 6→8 claims; added c7/c8 for the live Plazir sitemap and page metadata; corrected c5's observed h1 literal.
- `fleet-registry`: 8→9; added c9 for the charter marker.
- `ops-automation`: 6→7; added c7 for the pre-probe freshness gate.
- `vault-properties`: 8→10; added c9 for same-origin links and c10 for the sourceDir-null guard.
- `property-map`: 55→57; added c56/c57 and revised c10's correction to identify, but not assert deployment binding to, the surviving burnerchrome source candidate.

The b5d599e19bead54b96f589444e9ec64cdf67c28a files were checked in a fresh `git clone --no-hardlinks` under `/tmp/kake-r23res-FixC1Additions-m9VKAt/lane` and detached at that revision. A read-only consistency pass over all 91 receipt rows found: every `anchor` is an exact substring of the corresponding b5d599e unit file; every current unit contains its claim ID and any exact `correction`/`reason`; no missing `surface`, `observation`, or valid `HOLD`/`STALE`/`UNVERIFIABLE` verdict. Result: zero anchor, section-ID, correction/reason, or required-field mismatches.

## Wave-2 findings rechecked

- **HoldDriftDetection:** c7/c8 cover the omitted load-bearing r16 observations, and their corrections preserve dated history without asserting present source/live synchronization. c5 now records `<h1>lucario<span>.</span></h1>`, resolving the exact-literal error.
- **HoldFleetRegistry:** c9 updates the old 09-26/09-28 marker comparison with the live 09-30 marker and correctly says the current config pin cannot be checked while its source is absent. c2 remains UNVERIFIABLE, not promoted to a current 21-row count.
- **HoldOpsAutomation:** c7 marks the pre-probe `at`-versus-mtime implementation claim UNVERIFIABLE; it distinguishes the historical safety recommendation from verified current behavior. The absent snapshot and implementation do not support a live age/enforcement assertion.
- **HoldVaultProperties:** c9 records the live veigapunk self-origin link and marks the old zero-same-origin cross-check stale. c10 leaves the `cmdUpdate`/`cmdRecreate` guard UNVERIFIABLE because neither implementation nor an authorized operation trace is available; it does not try to infer code behavior from HTML.
- **StalePropertyMap:** c10 still marks the mapped `ds4cc-marketplace/burnerchrome` path absent, while its revised correction names `/home/vgpnk/Projects/burnerchrome` as a content-matching candidate and explicitly says deployment binding is unproved. c57 separately covers the missing `apps-sdk` source path and avoids treating endpoint reachability as source/deployment evidence. The c2 correction remains scoped to its tested paths; the candidate detail is supplied by adjacent c10 rather than being asserted as a verified replacement.
- **StaleDriftDetection:** c56 explicitly marks the old `SKILL.md:292` Function-Compute diagnosis superseded; the detailed dated redirect/Byte-nginx correction is also present at `corpus/knowledge/drift-detection.md:104`. The old sentence remains textually in SKILL.md, but the new entry does not leave it presented as current without a superseding note.

## Targeted observations

Public unauthenticated GETs used `curl -sS --max-time 30 -L -D <scratch headers> -o <scratch body> -w ...`; no cookies or credentials were supplied.

- Plazir: `sitemap.xml` → 200/1,144 bytes, seven `<loc>` entries, no `/tetris/`; `/tetris/` → 200/1,650 bytes. `snake/index.html` → 200/8,013 bytes with one `og:url` for the Plazir snake URL; `speedrun/` → 200/5,048 bytes with canonical `https://ds4cc.com/speedrun/`.
- Charter GHP: 200/53,660 bytes; fetched body contained one `2026-09-30 scribe beat` and no `2026-09-26` or `2026-09-28 scribe beat` marker.
- Veigapunk vault: GET → 200/10,059 bytes; a non-executing scan of the `const PROPERTIES` literal found its own `https://veigapunk.kimi.page` URL.
- `plazir27.kimi.pro`: followed GET ended at `https://statics.kimi.ai/pages/preview-404-en.html`, 200/5,995 bytes. Captured headers showed the initial 302 and final `server: Byte-nginx`, `x-request-id`, and no observed `x-fc-request-id`.
- Burnerchrome: `burnerchrome.kimi.page` → 200/11,976 bytes. The surviving local candidate's `index.html` and live page have the same title (`burnerchrome — Musketeer family`) and h1 (`Four adapters. One permanent burner Chrome.`). The isolated no-hardlinks candidate clone's `main` ref is `ee834920de8411f8014236948e2d5b9f5f82dde2`, with origin URL `https://github.com/VeigaPunk/burnerchrome.git`. This establishes a matching local candidate, **not** that it is the Kimi deployment source.
- Local existence probes returned ABSENT for `/home/vgpnk/Projects/webzites/scripts/kimi-surface.mjs`, `/home/vgpnk/Projects/webzites/state/probe-latest.json`, `/home/vgpnk/Projects/ds4cc-marketplace/burnerchrome`, and `/home/vgpnk/Projects/ds4cc-marketplace/apps-sdk`; `/home/vgpnk/Projects/burnerchrome/index.html` was PRESENT.

Commands used included `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kake-shokunin /tmp/kake-r23res-FixC1Additions-m9VKAt/lane`, `git -C /tmp/kake-r23res-FixC1Additions-m9VKAt/lane checkout --detach b5d599e19bead54b96f589444e9ec64cdf67c28a`, and `git archive 5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd ... | tar -x -C /tmp/kake-r23res-FixC1Additions-m9VKAt/pre-fix` for the named five receipts and five units.

## Residual risk and verification gaps

- LSP was unavailable: `read xd://lsp` returned `No such tool`. The anchor/correction pass is literal file-content verification, not semantic LSP proof; these are Markdown/JSON surfaces, not changed code callers.
- GETs were targeted to the additions above, not a re-census of every legacy row or every endpoint in the five units. They establish only observations at request time. No Kimi account/chat binding or publish path was accessed; no write/publish operation was attempted.
- The content match for the burnerchrome candidate does not establish Kimi deployment binding. The sourceDir-null and pre-probe implementation claims remain explicitly UNVERIFIABLE for the stated missing-source reasons.
- No installs, builds, linters, formatters, tests, or runtime/rerouting/saturation probes were performed; no runtime or routing implementation was changed in this C1 delta.
