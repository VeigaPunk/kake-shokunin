## Verdict

T16 `~/Projects/ds4cc-marketplace` is present at the observation time. Its `.git` birth timestamp is 2026-10-21 05:19:01 -03, its reflog records a clone from `https://github.com/VeigaPunk/ds4cc-marketplace.git` at 05:19:05 -03, and its current HEAD is `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28`. The eight assigned citations are lane-authored and carry now-stale absence annotations or statements; each receipt item proposes an append-only correction. No lane corpus file was edited; this report is the only lane write.

## Findings

- **P2 — C1 freshness, restored target and stale annotations.** Exact commands: `test -e /home/vgpnk/Projects/ds4cc-marketplace`; `stat -c '%n %w %y' /home/vgpnk/Projects/ds4cc-marketplace`; `git -C /home/vgpnk/Projects/ds4cc-marketplace log -3 --format='%H %cI %s'`; `git -C /home/vgpnk/Projects/ds4cc-marketplace remote -v`. Observed: `test -e` exit 0 (stdout empty); `stat` returned `/home/vgpnk/Projects/ds4cc-marketplace 2026-10-21 05:19:01.033916520 -0300 2026-10-21 05:21:03.733544920 -0300`; log HEAD `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28` (`2026-10-21T05:51:24-03:00`), followed by `95dbeb69b2db413f00f5310a171334967c368924` (`2026-10-21T05:21:55-03:00`) and `6e888784ae1bac9d341cc9af7fe12f9c5d83f31f` (`2026-10-20T14:33:09Z`); remote fetch/push both `https://github.com/VeigaPunk/ds4cc-marketplace.git`. Impact: C1/T16; lines 49, 50, 64, 11, 19, 70, 69, and 55 each need a restoration correction. Smallest fix: append the exact per-cite text in the receipt below; preserve their older observations unchanged.
- **P2 — C1 freshness, current tree differs from one cited content identity.** Exact commands: `sha256sum /home/vgpnk/Projects/ds4cc-marketplace/index.html`; `git -C /home/vgpnk/Projects/ds4cc-marketplace show e6bd071887bfaa87eff07ab03d323d5b92760fba:index.html | sha256sum`; `git -C /home/vgpnk/Projects/ds4cc-marketplace rev-list --count e6bd071887bfaa87eff07ab03d323d5b92760fba..HEAD`. Observed: current HEAD index hash `d0a2f357b19832e8ec8b0cbf80fa045734eff8a63d28e040434b9dcb5790f1d9` (77,625 bytes); e6bd0718 index hash `b6f65899e3e6aaf3b2df0c4ef82157fa328faf1c6e5d871c8806a450052f1d33` (79,453 bytes); e6bd0718 is an ancestor 28 commits behind HEAD. Thus the b6f65899 hash matches the historical e6bd0718 index, but the origin-repos.md:19 `also ==` claim does not hold for current HEAD. Smallest fix: append the receipt's qualified note; do not rewrite the old finding.
- **P2 — C1 lane-wide paths gate remains red outside this target.** Exact command: `node /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/freshness-sweep.mjs --section=paths --json --offline` (stdout redirected to `/tmp/kake-r24-PathsRestoredDs4ccCorpus-lw4p/paths.json` to avoid tool-output truncation). Observed exit 1; parsed JSON reported paths counts `drift=3`, `newMissing=12`; `~/Projects/ds4cc-marketplace` appears in `resolve` and `setDelta.recovered`, with no drift entry. Overall reason: `§paths: 3 unannotated miss · 12 NOT in pins.pathsMissSet`. Impact: C1 global, not a new failure of T16. Smallest fix is outside this scoped target: the integration owner must reconcile the remaining population and pins.

## Checked and held

- Required filesystem observation: `ls -la /home/vgpnk/Projects/` listed `ds4cc-marketplace/`; tool output elided intermediate entries and ended `0 files, 24 dirs`.
- `CNAME` reads `ds4cc.com` (9 bytes, no trailing newline); HEAD's top-level tree contains `CNAME`, `apps-sdk`, `burnerchrome`, `index.html`, `sitemap.xml`, and `speedrun`. Local `index.html` matches HEAD; `git --no-optional-locks -C /home/vgpnk/Projects/ds4cc-marketplace status --porcelain=v1` produced no output. Local `origin/main..HEAD` is `0`; reflog records origin/main updates by push at 05:34:58 -03 and 05:51:26 -03.
- All eight assigned cites are classified `annotated-stale`, `authored: lane`, `action: append-inline`. The three fleet-registry table rows and origin-repos.md:19 use HTML-comment restoration markers; prose lines use the required italic restoration marker. Their exact original line bytes and append text are in the receipt.
- Presence-dependent claims still unverified: live status/bytes for `ds4cc.com` and `ds4cc.kimi.page`; equality with the `~/Projects/webzites/repos/ds4cc-marketplace` checkout (the webzites tree is not present here); current mirror-property mapping; and current PQ-2 remote predicate. The other three paths named by round-23 c3 returned `ABSENT`: `/home/vgpnk/Projects/plazir-15-site`, `/home/vgpnk/Projects/webzites`, and `/home/vgpnk/Projects/ephemeral/wz1/ds4cc`. The round-23 c3 receipt has only a date, so its observation time relative to the 05:19 restoration is unrecorded. The local CNAME and checkout do not establish public serving or remote equivalence.
- No tools installed or updated. No public GET/HEAD was performed. No production files were edited and no tests/builds/linters were run.

## Limits

This is a filesystem/git observation at `2026-10-21T11:50:37Z`; the domain-tree restoration is operator-owned. The local reflog records the clone and subsequent commits/pushes, but not the operator or trigger. The full sweep remains exit 1 for other paths-gate population items. No independent admission is claimed.

```json
{
  "id": "T16",
  "token": "~/Projects/ds4cc-marketplace",
  "class": "recovered",
  "observedAt": "2026-10-21T11:50:37Z",
  "state": "present",
  "observation": {
    "commands": [
      "date -u +%Y-%m-%dT%H:%M:%SZ",
      "test -e /home/vgpnk/Projects/ds4cc-marketplace",
      "stat -c '%n %w %y' /home/vgpnk/Projects/ds4cc-marketplace",
      "ls -la /home/vgpnk/Projects/",
      "git -C /home/vgpnk/Projects/ds4cc-marketplace log -3 --format='%H %cI %s'",
      "git -C /home/vgpnk/Projects/ds4cc-marketplace remote -v",
      "git -C /home/vgpnk/Projects/ds4cc-marketplace log -g --date=iso -n 4 --format='%H | %gd | %gs | %ci'",
      "git -C /home/vgpnk/Projects/ds4cc-marketplace show HEAD:CNAME",
      "git -C /home/vgpnk/Projects/ds4cc-marketplace ls-tree --name-only HEAD burnerchrome speedrun apps-sdk sitemap.xml CNAME index.html",
      "git -C /home/vgpnk/Projects/ds4cc-marketplace rev-list --count origin/main..HEAD",
      "sha256sum /home/vgpnk/Projects/ds4cc-marketplace/index.html",
      "git -C /home/vgpnk/Projects/ds4cc-marketplace show e6bd071887bfaa87eff07ab03d323d5b92760fba:index.html | sha256sum",
      "git --no-optional-locks -C /home/vgpnk/Projects/ds4cc-marketplace status --porcelain=v1"
    ],
    "output": "2026-10-21T11:50:37Z; test -e exit 0 (stdout empty); stat: /home/vgpnk/Projects/ds4cc-marketplace 2026-10-21 05:19:01.033916520 -0300 2026-10-21 05:21:03.733544920 -0300; ls -la lists ds4cc-marketplace/ (other entries elided; summary 0 files, 24 dirs); git log: 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28 2026-10-21T05:51:24-03:00 omarchy-usage: sync page to usage-tray 1.10.0 (14 omp-metered providers, how it works, working install); 95dbeb69b2db413f00f5310a171334967c368924 2026-10-21T05:21:55-03:00 os-tuning: add gkeep (local post-it notes for the Omarchy bar); 6e888784ae1bac9d341cc9af7fe12f9c5d83f31f 2026-10-20T14:33:09Z magga: Enduro — Classic & Remastered at /magga/enduro/; remote: origin https://github.com/VeigaPunk/ds4cc-marketplace.git (fetch) and (push); reflog clone 2026-10-21 05:19:05 -0300; CNAME=ds4cc.com; HEAD index.html SHA-256=d0a2f357b19832e8ec8b0cbf80fa045734eff8a63d28e040434b9dcb5790f1d9; e6bd0718 index.html SHA-256=b6f65899e3e6aaf3b2df0c4ef82157fa328faf1c6e5d871c8806a450052f1d33; HEAD tree entries CNAME, apps-sdk, burnerchrome, index.html, sitemap.xml, speedrun; origin/main..HEAD=0; status output empty"
  },
  "event": "2026-10-21 05:19:05 -03:00: local git reflog records clone from https://github.com/VeigaPunk/ds4cc-marketplace.git; .git directory birth is 05:19:01 -03. Reflog then records commits and pushes of 95dbeb69 and 1fbdb8ed. The operator or trigger is not recorded.",
  "cites": [
    {
      "cite": "corpus/knowledge/fleet-registry.md:49",
      "lineText": "| ds4cc-com | ds4cc.com | live | `~/Projects/ds4cc-marketplace` | <!-- r18 re-census 2026-10-14: ~/Projects/ds4cc-marketplace absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->",
      "authored": "lane",
      "status": "annotated-stale",
      "action": "append-inline",
      "text": "<!-- r24 restoration 2026-10-21: observed ~/Projects/ds4cc-marketplace present (directory birth 2026-10-21 05:19:01 -03; HEAD 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28; CNAME ds4cc.com). The r18 note remains a historical record of the 2026-10-14 census; this filesystem check does not verify ds4cc.com live status. -->"
    },
    {
      "cite": "corpus/knowledge/fleet-registry.md:50",
      "lineText": "| ds4cc-kimi-mirror | ds4cc.kimi.page | live, STALE (~Aug-29 DOM) | `~/Projects/ds4cc-marketplace` | <!-- r18 re-census 2026-10-14: ~/Projects/ds4cc-marketplace absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->",
      "authored": "lane",
      "status": "annotated-stale",
      "action": "append-inline",
      "text": "<!-- r24 restoration 2026-10-21: observed ~/Projects/ds4cc-marketplace present (directory birth 2026-10-21 05:19:01 -03; HEAD 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28; CNAME ds4cc.com). The r18 note remains a historical record of the 2026-10-14 census; this filesystem check does not verify ds4cc.kimi.page status or mirror contents. -->"
    },
    {
      "cite": "corpus/knowledge/fleet-registry.md:64",
      "lineText": "| ds4cc-kimi-mirror-vault-row | null | pruned→ds4cc-kimi-mirror | `~/Projects/ds4cc-marketplace` | <!-- r18 re-census 2026-10-14: ~/Projects/ds4cc-marketplace absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->",
      "authored": "lane",
      "status": "annotated-stale",
      "action": "append-inline",
      "text": "<!-- r24 restoration 2026-10-21: observed ~/Projects/ds4cc-marketplace present (directory birth 2026-10-21 05:19:01 -03; HEAD 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28; CNAME ds4cc.com). The r18 note and pruned->ds4cc-kimi-mirror label remain historical fleet data; current mirror-property mapping and public status are unverified by this filesystem check. -->"
    },
    {
      "cite": "corpus/knowledge/origin-repos.md:11",
      "lineText": "working checkouts are `~/Projects/<name>` (e.g. `~/Projects/ds4cc-marketplace`). <!-- r18 re-census 2026-10-14: ~/Projects/ds4cc-marketplace absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->",
      "authored": "lane",
      "status": "annotated-stale",
      "action": "append-inline",
      "text": "*[r24 restoration 2026-10-21: observed ~/Projects/ds4cc-marketplace present (directory birth 2026-10-21 05:19:01 -03; HEAD 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28; CNAME ds4cc.com). The r18 note remains historical to the 2026-10-14 census; the example checkout is present at this observation.]*"
    },
    {
      "cite": "corpus/knowledge/origin-repos.md:19",
      "lineText": "| `ds4cc.com` | `repos/ds4cc-marketplace` (live index sha `b6f65899…`, also == `~/Projects/ds4cc-marketplace`) | byte-verified | <!-- r18 re-census 2026-10-14: ~/Projects/ds4cc-marketplace absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->",
      "authored": "lane",
      "status": "annotated-stale",
      "action": "append-inline",
      "text": "<!-- r24 restoration 2026-10-21: observed ~/Projects/ds4cc-marketplace present (directory birth 2026-10-21 05:19:01 -03; HEAD 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28; CNAME ds4cc.com; current HEAD index.html SHA-256 d0a2f357b19832e8ec8b0cbf80fa045734eff8a63d28e040434b9dcb5790f1d9, 77,625 bytes; e6bd0718 index.html SHA-256 b6f65899e3e6aaf3b2df0c4ef82157fa328faf1c6e5d871c8806a450052f1d33, 79,453 bytes). The r18 note remains historical to 2026-10-14; the \"also ==\" equality is historical to e6bd0718 and does not hold at current HEAD. The repos/ds4cc-marketplace counterpart and live ds4cc.com bytes remain unverified. -->"
    },
    {
      "cite": "corpus/knowledge/origin-repos.md:70",
      "lineText": "- `ds4cc-com.sourceDir` → `~/Projects/ds4cc-marketplace` (second checkout, <!-- r18 re-census 2026-10-14: ~/Projects/ds4cc-marketplace absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->",
      "authored": "lane",
      "status": "annotated-stale",
      "action": "append-inline",
      "text": "*[r24 restoration 2026-10-21: observed ~/Projects/ds4cc-marketplace present (directory birth 2026-10-21 05:19:01 -03; HEAD 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28; CNAME ds4cc.com). The r18 note remains historical to 2026-10-14; byte identity with repos/ds4cc-marketplace and the \"works\" behavior remain unverified on this host.]*"
    },
    {
      "cite": "corpus/knowledge/publish-channels.md:69",
      "lineText": "- [publish-channels:c3] **HOLD** — The named historical project/workspace trees remain absent at their recorded local paths on this host. Surface: `for p in /home/vgpnk/Projects/ds4cc-marketplace /home/vgpnk/Projects/plazir-15-site /home/vgpnk/Projects/webzites /home/vgpnk/Projects/ephemeral/wz1/ds4cc; do if test -e \"$p\"; then printf 'EXISTS %s\\n' \"$p\"; else printf 'ABSENT %s\\n' \"$p\"; fi; done`.",
      "authored": "lane",
      "status": "annotated-stale",
      "action": "append-inline",
      "text": "*[r24 restoration 2026-10-21: observed ~/Projects/ds4cc-marketplace present (directory birth 2026-10-21 05:19:01 -03; HEAD 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28; CNAME ds4cc.com). Round-23 c3 recorded a date-only observation; its timing relative to the restoration is unrecorded. The other three named paths are outside this target's restoration correction; live-domain state is unverified by this local check.]*"
    },
    {
      "cite": "corpus/lessons/round-18.md:55",
      "lineText": "- **PQ-2** — `~/Projects/ds4cc-marketplace` gone; gate reads `ANOMALY`,",
      "authored": "lane",
      "status": "annotated-stale",
      "action": "append-inline",
      "text": "*[r24 restoration 2026-10-21: observed ~/Projects/ds4cc-marketplace present (directory birth 2026-10-21 05:19:01 -03; clone recorded in git reflog; HEAD 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28). The earlier PQ-2 diagnosis and gate output remain historical; the restoration branch of its stated unblock condition is satisfied, while the current remote predicate is unverified here.]*"
    }
  ]
}
```
## Receipt JSON transport erratum

Standalone corrected copy of the T16 receipt; evidence and observations are unchanged.

```json
{
  "id": "T16",
  "token": "~/Projects/ds4cc-marketplace",
  "class": "recovered",
  "observedAt": "2026-10-21T11:50:37Z",
  "state": "present",
  "observation": {
    "commands": [
      "date -u +%Y-%m-%dT%H:%M:%SZ",
      "test -e /home/vgpnk/Projects/ds4cc-marketplace",
      "stat -c '%n %w %y' /home/vgpnk/Projects/ds4cc-marketplace",
      "ls -la /home/vgpnk/Projects/",
      "git -C /home/vgpnk/Projects/ds4cc-marketplace log -3 --format='%H %cI %s'",
      "git -C /home/vgpnk/Projects/ds4cc-marketplace remote -v",
      "git -C /home/vgpnk/Projects/ds4cc-marketplace log -g --date=iso -n 4 --format='%H | %gd | %gs | %ci'",
      "git -C /home/vgpnk/Projects/ds4cc-marketplace show HEAD:CNAME",
      "git -C /home/vgpnk/Projects/ds4cc-marketplace ls-tree --name-only HEAD burnerchrome speedrun apps-sdk sitemap.xml CNAME index.html",
      "git -C /home/vgpnk/Projects/ds4cc-marketplace rev-list --count origin/main..HEAD",
      "sha256sum /home/vgpnk/Projects/ds4cc-marketplace/index.html",
      "git -C /home/vgpnk/Projects/ds4cc-marketplace show e6bd071887bfaa87eff07ab03d323d5b92760fba:index.html | sha256sum",
      "git --no-optional-locks -C /home/vgpnk/Projects/ds4cc-marketplace status --porcelain=v1"
    ],
    "output": "2026-10-21T11:50:37Z; test -e exit 0 (stdout empty); stat: /home/vgpnk/Projects/ds4cc-marketplace 2026-10-21 05:19:01.033916520 -0300 2026-10-21 05:21:03.733544920 -0300; ls -la lists ds4cc-marketplace/ (other entries elided; summary 0 files, 24 dirs); git log: 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28 2026-10-21T05:51:24-03:00 omarchy-usage: sync page to usage-tray 1.10.0 (14 omp-metered providers, how it works, working install); 95dbeb69b2db413f00f5310a171334967c368924 2026-10-21T05:21:55-03:00 os-tuning: add gkeep (local post-it notes for the Omarchy bar); 6e888784ae1bac9d341cc9af7fe12f9c5d83f31f 2026-10-20T14:33:09Z magga: Enduro — Classic & Remastered at /magga/enduro/; remote: origin https://github.com/VeigaPunk/ds4cc-marketplace.git (fetch) and (push); reflog clone 2026-10-21 05:19:05 -0300; CNAME=ds4cc.com; HEAD index.html SHA-256=d0a2f357b19832e8ec8b0cbf80fa045734eff8a63d28e040434b9dcb5790f1d9; e6bd0718 index.html SHA-256=b6f65899e3e6aaf3b2df0c4ef82157fa328faf1c6e5d871c8806a450052f1d33; HEAD tree entries CNAME, apps-sdk, burnerchrome, index.html, sitemap.xml, speedrun; origin/main..HEAD=0; status output empty"
  },
  "event": "2026-10-21 05:19:05 -03:00: local git reflog records clone from https://github.com/VeigaPunk/ds4cc-marketplace.git; .git directory birth is 05:19:01 -03. Reflog then records commits and pushes of 95dbeb69 and 1fbdb8ed. The operator or trigger is not recorded.",
  "cites": [
    {
      "cite": "corpus/knowledge/fleet-registry.md:49",
      "lineText": "| ds4cc-com | ds4cc.com | live | `~/Projects/ds4cc-marketplace` | <!-- r18 re-census 2026-10-14: ~/Projects/ds4cc-marketplace absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->",
      "authored": "lane",
      "status": "annotated-stale",
      "action": "append-inline",
      "text": "<!-- r24 restoration 2026-10-21: observed ~/Projects/ds4cc-marketplace present (directory birth 2026-10-21 05:19:01 -03; HEAD 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28; CNAME ds4cc.com). The r18 note remains a historical record of the 2026-10-14 census; this filesystem check does not verify ds4cc.com live status. -->"
    },
    {
      "cite": "corpus/knowledge/fleet-registry.md:50",
      "lineText": "| ds4cc-kimi-mirror | ds4cc.kimi.page | live, STALE (~Aug-29 DOM) | `~/Projects/ds4cc-marketplace` | <!-- r18 re-census 2026-10-14: ~/Projects/ds4cc-marketplace absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->",
      "authored": "lane",
      "status": "annotated-stale",
      "action": "append-inline",
      "text": "<!-- r24 restoration 2026-10-21: observed ~/Projects/ds4cc-marketplace present (directory birth 2026-10-21 05:19:01 -03; HEAD 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28; CNAME ds4cc.com). The r18 note remains a historical record of the 2026-10-14 census; this filesystem check does not verify ds4cc.kimi.page status or mirror contents. -->"
    },
    {
      "cite": "corpus/knowledge/fleet-registry.md:64",
      "lineText": "| ds4cc-kimi-mirror-vault-row | null | pruned→ds4cc-kimi-mirror | `~/Projects/ds4cc-marketplace` | <!-- r18 re-census 2026-10-14: ~/Projects/ds4cc-marketplace absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->",
      "authored": "lane",
      "status": "annotated-stale",
      "action": "append-inline",
      "text": "<!-- r24 restoration 2026-10-21: observed ~/Projects/ds4cc-marketplace present (directory birth 2026-10-21 05:19:01 -03; HEAD 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28; CNAME ds4cc.com). The r18 note and pruned->ds4cc-kimi-mirror label remain historical fleet data; current mirror-property mapping and public status are unverified by this filesystem check. -->"
    },
    {
      "cite": "corpus/knowledge/origin-repos.md:11",
      "lineText": "working checkouts are `~/Projects/<name>` (e.g. `~/Projects/ds4cc-marketplace`). <!-- r18 re-census 2026-10-14: ~/Projects/ds4cc-marketplace absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->",
      "authored": "lane",
      "status": "annotated-stale",
      "action": "append-inline",
      "text": "*[r24 restoration 2026-10-21: observed ~/Projects/ds4cc-marketplace present (directory birth 2026-10-21 05:19:01 -03; HEAD 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28; CNAME ds4cc.com). The r18 note remains historical to the 2026-10-14 census; the example checkout is present at this observation.]*"
    },
    {
      "cite": "corpus/knowledge/origin-repos.md:19",
      "lineText": "| `ds4cc.com` | `repos/ds4cc-marketplace` (live index sha `b6f65899…`, also == `~/Projects/ds4cc-marketplace`) | byte-verified | <!-- r18 re-census 2026-10-14: ~/Projects/ds4cc-marketplace absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->",
      "authored": "lane",
      "status": "annotated-stale",
      "action": "append-inline",
      "text": "<!-- r24 restoration 2026-10-21: observed ~/Projects/ds4cc-marketplace present (directory birth 2026-10-21 05:19:01 -03; HEAD 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28; CNAME ds4cc.com; current HEAD index.html SHA-256 d0a2f357b19832e8ec8b0cbf80fa045734eff8a63d28e040434b9dcb5790f1d9, 77,625 bytes; e6bd0718 index.html SHA-256 b6f65899e3e6aaf3b2df0c4ef82157fa328faf1c6e5d871c8806a450052f1d33, 79,453 bytes). The r18 note remains historical to 2026-10-14; the \"also ==\" equality is historical to e6bd0718 and does not hold at current HEAD. The repos/ds4cc-marketplace counterpart and live ds4cc.com bytes remain unverified. -->"
    },
    {
      "cite": "corpus/knowledge/origin-repos.md:70",
      "lineText": "- `ds4cc-com.sourceDir` → `~/Projects/ds4cc-marketplace` (second checkout, <!-- r18 re-census 2026-10-14: ~/Projects/ds4cc-marketplace absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->",
      "authored": "lane",
      "status": "annotated-stale",
      "action": "append-inline",
      "text": "*[r24 restoration 2026-10-21: observed ~/Projects/ds4cc-marketplace present (directory birth 2026-10-21 05:19:01 -03; HEAD 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28; CNAME ds4cc.com). The r18 note remains historical to 2026-10-14; byte identity with repos/ds4cc-marketplace and the \"works\" behavior remain unverified on this host.]*"
    },
    {
      "cite": "corpus/knowledge/publish-channels.md:69",
      "lineText": "- [publish-channels:c3] **HOLD** — The named historical project/workspace trees remain absent at their recorded local paths on this host. Surface: `for p in /home/vgpnk/Projects/ds4cc-marketplace /home/vgpnk/Projects/plazir-15-site /home/vgpnk/Projects/webzites /home/vgpnk/Projects/ephemeral/wz1/ds4cc; do if test -e \"$p\"; then printf 'EXISTS %s\\n' \"$p\"; else printf 'ABSENT %s\\n' \"$p\"; fi; done`.",
      "authored": "lane",
      "status": "annotated-stale",
      "action": "append-inline",
      "text": "*[r24 restoration 2026-10-21: observed ~/Projects/ds4cc-marketplace present (directory birth 2026-10-21 05:19:01 -03; HEAD 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28; CNAME ds4cc.com). Round-23 c3 recorded a date-only observation; its timing relative to the restoration is unrecorded. The other three named paths are outside this target's restoration correction; live-domain state is unverified by this local check.]*"
    },
    {
      "cite": "corpus/lessons/round-18.md:55",
      "lineText": "- **PQ-2** — `~/Projects/ds4cc-marketplace` gone; gate reads `ANOMALY`,",
      "authored": "lane",
      "status": "annotated-stale",
      "action": "append-inline",
      "text": "*[r24 restoration 2026-10-21: observed ~/Projects/ds4cc-marketplace present (directory birth 2026-10-21 05:19:01 -03; clone recorded in git reflog; HEAD 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28). The earlier PQ-2 diagnosis and gate output remain historical; the restoration branch of its stated unblock condition is satisfied, while the current remote predicate is unverified here.]*"
    }
  ]
}
```
