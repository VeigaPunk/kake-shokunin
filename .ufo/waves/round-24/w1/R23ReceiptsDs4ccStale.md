## Verdict

Freshness C1 review: the round-23 receipts and their appended live-reverification sections contain stale local-path observations for the restored `~/Projects/ds4cc-marketplace` checkout and its `burnerchrome` and `speedrun` subtrees. The current checkout was born at `2026-10-21 05:19:01.033916520 -0300`; it is present at observation time, with HEAD `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28`. I recommend appending the exact r24 restoration notes below; do not alter the r23 observations.

Observation timestamp: `date -u +%FT%TZ` returned `2026-10-21T11:47:16Z` (a later call returned `2026-10-21T11:48:10Z`). No tools were installed or updated.

## Findings

### P2 — Round-23 C1 local absence observations have been superseded by the restored checkout

Impacted claim/axis for each item: round-23 contract C1, freshness. The receipt claim id and current observation are listed per item; the smallest fix is to append the quoted text to that exact line, without changing its r23 text.

1. **`SKILL.md:423` — `property-map:c2`** (receipt `.ufo/waves/round-23/receipts/property-map.json`). The C1 row says the `ds4cc-marketplace/burnerchrome` source path was absent and mentions the ds4cc root as historically unavailable. R23 observation: `ABSENT /home/vgpnk/Projects/ds4cc-marketplace/burnerchrome` and the other tested paths `/home/vgpnk/Projects/plazir-15-site`, `/home/vgpnk/Projects/lucario`, `/home/vgpnk/Projects/lucario/site` were also `ABSENT`.
   - Current command: `test -e /home/vgpnk/Projects/ds4cc-marketplace; echo "exit=$? ds4cc-marketplace"; test -e /home/vgpnk/Projects/ds4cc-marketplace/burnerchrome; echo "exit=$? ds4cc-marketplace/burnerchrome"`.
   - Exact output: `exit=0 ds4cc-marketplace` / `exit=0 ds4cc-marketplace/burnerchrome`. `stat -c '%n | birth=%w | mtime=%y' /home/vgpnk/Projects/ds4cc-marketplace` returned `/home/vgpnk/Projects/ds4cc-marketplace | birth=2026-10-21 05:19:01.033916520 -0300 | mtime=2026-10-21 05:21:03.733544920 -0300`; `git -C /home/vgpnk/Projects/ds4cc-marketplace rev-parse HEAD` returned `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28`.
   - Append exactly: ` *[r24 restoration 2026-10-21: /home/vgpnk/Projects/ds4cc-marketplace and /home/vgpnk/Projects/ds4cc-marketplace/burnerchrome are present (test -e exit 0; root birth 2026-10-21 05:19:01 -0300; checkout HEAD 1fbdb8ed); this supersedes the r23 ds4cc-root/burnerchrome state, while the Plazir-15 and Lucario path results and the charter-root note remain historical observations.]*`

2. **`SKILL.md:431` — `property-map:c10`** (same receipt). R23 correction states `/home/vgpnk/Projects/ds4cc-marketplace/burnerchrome` is absent and names `/home/vgpnk/Projects/burnerchrome` as another candidate.
   - Current command: `test -e /home/vgpnk/Projects/ds4cc-marketplace/burnerchrome; echo "exit=$? ds4cc-marketplace/burnerchrome"; test -e /home/vgpnk/Projects/burnerchrome; echo "exit=$? burnerchrome (surviving candidate)"`.
   - Exact output: `exit=0 ds4cc-marketplace/burnerchrome` / `exit=0 burnerchrome (surviving candidate)`. The checkout HEAD is `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28`.
   - Append exactly: ` *[r24 restoration 2026-10-21: /home/vgpnk/Projects/ds4cc-marketplace/burnerchrome is present (test -e exit 0; directory birth 2026-10-21 05:19:05.038621636 -0300; checkout HEAD 1fbdb8ed); the r23 burnerchrome-path result remains a historical observation, and the separate /home/vgpnk/Projects/burnerchrome candidate does not establish source/deployment identity.]*`

3. **`SKILL.md:445` — `property-map:c24`** (same receipt). R23 observation is `SOURCE_PATH=absent (test -e exit 1)` for `/home/vgpnk/Projects/ds4cc-marketplace`.
   - Current command: `test -e /home/vgpnk/Projects/ds4cc-marketplace; echo "exit=$? ds4cc-marketplace"`.
   - Exact output: `exit=0 ds4cc-marketplace`; the directory birth and HEAD are as reported under item 1.
   - Append exactly: ` *[r24 restoration 2026-10-21: /home/vgpnk/Projects/ds4cc-marketplace is present (test -e exit 0; directory birth 2026-10-21 05:19:01 -0300; checkout HEAD 1fbdb8ed); the r23 source-path observation remains historical and does not establish current deployed content or Pages settings.]*`

4. **`SKILL.md:448` — `property-map:c27`** (same receipt). R23 observation is `absent`; its claim says the corresponding local path is still absent after historical preservation.
   - Current command: `test -e /home/vgpnk/Projects/ds4cc-marketplace; echo "exit=$? ds4cc-marketplace"`.
   - Exact output: `exit=0 ds4cc-marketplace`.
   - Append exactly: ` *[r24 restoration 2026-10-21: /home/vgpnk/Projects/ds4cc-marketplace is present (test -e exit 0; directory birth 2026-10-21 05:19:01 -0300; checkout HEAD 1fbdb8ed); the r23 statement about this path remains a historical observation, not a current source-content or publishing-configuration check.]*`

5. **`SKILL.md:449` — `property-map:c28`** (same receipt). R23 observation/reason says the mapped checkout is absent, preventing a local workflow recheck.
   - Current command: `test -e /home/vgpnk/Projects/ds4cc-marketplace; echo "exit=$? ds4cc-marketplace"; test -e /home/vgpnk/Projects/ds4cc-marketplace/.github/workflows/pages.yml && echo "HEAD has .github/workflows/pages.yml"`.
   - Exact output: `exit=0 ds4cc-marketplace` / `HEAD has .github/workflows/pages.yml`.
   - Append exactly: ` *[r24 restoration 2026-10-21: /home/vgpnk/Projects/ds4cc-marketplace is present (test -e exit 0; checkout HEAD 1fbdb8ed), and HEAD contains .github/workflows/pages.yml; the r23 checkout-state rationale remains historical, while current Pages configuration is not independently verified here.]*`

6. **`SKILL.md:450` — `property-map:c29`** (same receipt). R23 observation/reason likewise says the mapped checkout is absent; it leaves current GitHub Pages configuration unverified.
   - Current command/output: as item 5, `test -e /home/vgpnk/Projects/ds4cc-marketplace` → `exit=0`; `git -C /home/vgpnk/Projects/ds4cc-marketplace rev-parse HEAD` → `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28`.
   - Append exactly: ` *[r24 restoration 2026-10-21: /home/vgpnk/Projects/ds4cc-marketplace is present (test -e exit 0; checkout HEAD 1fbdb8ed); the r23 checkout-state rationale remains historical, while the Actions-versus-branch custom-domain setting remains unverified by this filesystem observation.]*`

7. **`SKILL.md:496` — `property-map:c57`** (same receipt; included because this C1 row explicitly asserts that the nested `ds4cc-marketplace/apps-sdk` path is absent). R23 observation: `test -e exits 1 (absent)`.
   - Current command: `test -e /home/vgpnk/Projects/ds4cc-marketplace/apps-sdk && echo "PRESENT ds4cc-marketplace/apps-sdk"; test -e /home/vgpnk/Projects/ds4cc-marketplace/apps-sdk/Dockerfile && echo "PRESENT apps-sdk/Dockerfile"`.
   - Exact output: `PRESENT ds4cc-marketplace/apps-sdk` / `PRESENT apps-sdk/Dockerfile`; checkout HEAD `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28`.
   - Append exactly: ` *[r24 restoration 2026-10-21: /home/vgpnk/Projects/ds4cc-marketplace/apps-sdk and apps-sdk/Dockerfile are present (test -e exit 0; checkout HEAD 1fbdb8ed); the r23 local-path result remains historical, while current Render deployment binding is unverified by this filesystem check.]*`

8. **`corpus/knowledge/publish-channels.md:69` — `publish-channels:c3`** (receipt `.ufo/waves/round-23/receipts/publish-channels.json`). R23 claim says the ds4cc, Plazir-15, webzites, and ephemeral trees all remain absent. Its command was the four-path `for p ...` loop.
   - Current command (same loop): `for p in /home/vgpnk/Projects/ds4cc-marketplace /home/vgpnk/Projects/plazir-15-site /home/vgpnk/Projects/webzites /home/vgpnk/Projects/ephemeral/wz1/ds4cc; do if test -e "$p"; then printf 'EXISTS %s\\n' "$p"; else printf 'ABSENT %s\\n' "$p"; fi; done`.
   - Exact output: `EXISTS /home/vgpnk/Projects/ds4cc-marketplace` / `ABSENT /home/vgpnk/Projects/plazir-15-site` / `ABSENT /home/vgpnk/Projects/webzites` / `ABSENT /home/vgpnk/Projects/ephemeral/wz1/ds4cc`.
   - Append exactly: ` *[r24 restoration 2026-10-21: /home/vgpnk/Projects/ds4cc-marketplace is present (test -e succeeds; directory birth 2026-10-21 05:19:01 -0300; checkout HEAD 1fbdb8ed); this updates only the ds4cc result in the grouped r23 observation, whose other path results remain separate historical findings.]*`

9. **`corpus/knowledge/mirror-pitfalls.md:63` — `mirror-pitfalls:c4`** (receipt `.ufo/waves/round-23/receipts/mirror-pitfalls.json`). R23 correction says both the Plazir-15 and ds4cc speedrun paths are absent.
   - Current command: `test -e /home/vgpnk/Projects/plazir-15-site/speedrun; echo "exit=$? plazir-15-site/speedrun"; test -e /home/vgpnk/Projects/ds4cc-marketplace/speedrun; echo "exit=$? ds4cc-marketplace/speedrun"`.
   - Exact output: `exit=1 plazir-15-site/speedrun` / `exit=0 ds4cc-marketplace/speedrun`. The ds4cc speedrun directory birth was `2026-10-21 05:19:05.120101209 -0300`.
   - Append exactly: ` *[r24 restoration 2026-10-21: /home/vgpnk/Projects/ds4cc-marketplace/speedrun and speedrun/index.html are present (test -e exit 0; directory birth 2026-10-21 05:19:05 -0300; checkout HEAD 1fbdb8ed); this updates only the ds4cc canonical-path portion, while the Plazir-15 result and the rel=canonical relationship remain historical/unverified.]*`

10. **`corpus/knowledge/speedrun-pipeline.md:78` — `speedrun-pipeline:c3`** (receipt `.ufo/waves/round-23/receipts/speedrun-pipeline.json`). R23 claim says the historically designated local authority path `/home/vgpnk/Projects/ds4cc-marketplace/speedrun` remains absent.
    - Current command: `test -e /home/vgpnk/Projects/ds4cc-marketplace/speedrun; echo "exit=$? ds4cc-marketplace/speedrun"; test -e /home/vgpnk/Projects/ds4cc-marketplace/speedrun/data/manifest.json && echo "PRESENT speedrun/data/manifest.json"`.
    - Exact output: `exit=0 ds4cc-marketplace/speedrun` / `PRESENT speedrun/data/manifest.json`; directory birth `2026-10-21 05:19:05.120101209 -0300`.
    - Append exactly: ` *[r24 restoration 2026-10-21: /home/vgpnk/Projects/ds4cc-marketplace/speedrun and speedrun/data/manifest.json are present (test -e exit 0; directory birth 2026-10-21 05:19:05 -0300; checkout HEAD 1fbdb8ed); the r23 authority-path observation remains historical, and this file-presence check does not re-verify current writer safety or publishing permissions.]*`

11. **`corpus/knowledge/speedrun-pipeline.md:82` — `speedrun-pipeline:c7`** (same receipt; implicit local-path assertion). Its UNVERIFIABLE rationale says the “local source/authority tree is absent”; the source mapping at `speedrun-pipeline.md:13` identifies that authority as `~/Projects/ds4cc-marketplace/speedrun/`.
    - Current command/output: `test -e /home/vgpnk/Projects/ds4cc-marketplace/speedrun; echo "exit=$? ds4cc-marketplace/speedrun"` → `exit=0 ds4cc-marketplace/speedrun`.
    - Append exactly: ` *[r24 restoration 2026-10-21: the local authority tree ~/Projects/ds4cc-marketplace/speedrun is present (test -e exit 0; checkout HEAD 1fbdb8ed); the r23 source-tree rationale remains historical, while the public board's GitHub Pages origin and any separate upload API remain unverified by this local presence check.]*`

12. **`corpus/knowledge/sitemap-orphan-audit.md:136` — `sitemap-orphan-audit:c4`** (receipt `.ufo/waves/round-23/receipts/sitemap-orphan-audit.json`). R23 correction says `/home/vgpnk/Projects/ds4cc-marketplace/sitemap.xml` was absent and the 93-location staged-copy assertion did not hold.
    - Current commands: `test -e /home/vgpnk/Projects/ds4cc-marketplace/sitemap.xml; echo "exit=$? ds4cc-marketplace/sitemap.xml"`; `git -C /home/vgpnk/Projects/ds4cc-marketplace rev-parse HEAD:sitemap.xml`; `git -C /home/vgpnk/Projects/ds4cc-marketplace hash-object sitemap.xml`; read-only parse of both working and HEAD sitemap XML.
    - Exact outputs: `exit=0 ds4cc-marketplace/sitemap.xml`; both Git blob hashes are `f6e254afae651c87b5ad9f87195e8caf5735eb7d`; working file equals HEAD; bytes `7614`; SHA-256 `18c51c45d62dd1cea99f9d88e7e19c0e9bd00c75f7e2ccf36e002a702823e53d`; parsed `<loc>` count `97` (regex count also `97`).
    - Append exactly: ` *[r24 restoration 2026-10-21: /home/vgpnk/Projects/ds4cc-marketplace/sitemap.xml is present and byte-identical to HEAD (test -e exit 0; 7,614 bytes; SHA-256 18c51c45d62dd1cea99f9d88e7e19c0e9bd00c75f7e2ccf36e002a702823e53d; 97 parsed <loc> entries); the r23 file-state finding remains historical, and this 97-entry file does not verify the earlier 93-entry count.]*`

## Checked and held

- Read round-23 contract C1: it covers all receipt claim rows, whose live observations and corrections are appended in each unit's round-23 section. Queried all 18 files in `.ufo/waves/round-23/receipts/` for the ds4cc path and related local-source/authority terms, then matched the findings against the unit sections.
- Round-24 `c1-population.json` identifies recovered targets T16–T19: `~/Projects/ds4cc-marketplace`, `~/Projects/ds4cc-marketplace/CNAME`, `~/Projects/ds4cc-marketplace/burnerchrome`, and `~/Projects/ds4cc-marketplace/speedrun`. The current filesystem checks found the root and relevant subtrees present. `cat /home/vgpnk/Projects/ds4cc-marketplace/CNAME` output `ds4cc.com`; `wc -c < /home/vgpnk/Projects/ds4cc-marketplace/CNAME` output `9`.
- No round-23 claim in the scanned receipts/unit sections asserts that the local CNAME file itself is absent. The round-23 `property-map:c1` remote CNAME observation and `rejected:c1` both report the repository CNAME body `ds4cc.com`; the local CNAME file now also contains that value. The r18 notes at `SKILL.md:16,19,364` are outside this round-23-only assignment.
- Excluded `origin-repos:c4` (`corpus/knowledge/origin-repos.md:82`): it refers to the distinct `/home/vgpnk/Projects/webzites/repos/ds4cc-marketplace` path, which returned `exit=1`, not the restored `/home/vgpnk/Projects/ds4cc-marketplace` checkout. `origin-repos:c5` concerns `webzites/repos/burnerchrome`, also a distinct path. `drift-detection:c8` tests Plazir URLs and does not identify the ds4cc local checkout as the “absent checkout.”
- The additional `speedrun-pipeline:c7` row is included as an implicit-path case because its stated absent authority tree is mapped to the ds4cc speedrun tree within the same unit. The `property-map:c57` row is also included as a deeper nested path explicitly under ds4cc, although `apps-sdk` is not one of the four T16–T19 recovered tokens.
- The whole round-23 checkout identity observed read-only: `git -C /home/vgpnk/Projects/ds4cc-marketplace rev-parse HEAD` → `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28`; `git -C /home/vgpnk/Projects/ds4cc-marketplace log -1 --format='%H %cI %s'` → `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28 2026-10-21T05:51:24-03:00 omarchy-usage: sync page to usage-tray 1.10.0 (14 omp-metered providers, how it works, working install)`.

## Limits

- These are read-only filesystem and Git observations on 2026-10-21. They establish current path presence and current HEAD identity, not byte equivalence to the checkout or source content observed during round 23, nor current deployment binding, Pages settings, or writer safety.
- The round-23 `mirror-pitfalls:c4` composite line still has a Plazir-15 local path result and a copy/canonical assertion that this review did not re-establish; the proposed restoration text updates only its ds4cc speedrun portion.
- The restored local sitemap is 97 parsed `<loc>` entries at HEAD, not the 93-entry count in the historical round-23 text. The observation is bounded to the current local file.