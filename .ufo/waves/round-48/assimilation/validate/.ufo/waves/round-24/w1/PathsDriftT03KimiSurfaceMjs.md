## Verdict

T03: drift; the target is absent at the observed filesystem path. The 2026-10-21T11:50:05Z paths sweep still reports this target as drift, with one unannotated cite. The receipt records present state; it does not claim the round is reconciled or admitted.

## Findings

### P2 — C1 freshness: one non-author cite remains unannotated

- **Exact command:** node /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/freshness-sweep.mjs --section=paths --json
- **Exact observed output (relevant projection):** generatedAt=2026-10-21T11:50:05Z; code=1; drift[~/Projects/webzites/scripts/kimi-surface.mjs].unannotatedCites=[corpus/lessons/round-6-aggregator-audit.md:48]; counts={drift:3,newMissing:12,recovered:4}.
- **Impacted claim/axis:** C1, freshness. corpus/lessons/round-6-aggregator-audit.md is non-author and must not be edited.
- **Smallest fix:** add one absent entry to corpus/knowledge/freshness-sidecar.json (kake-paths-sidecar-v1), bound to line 48 exact bytes by SHA-256 ac953adf1c0d16eb966dce60c338660c0d99da7cca7e72d71204caf7fe5cfd5a. Proposed note: “As of 2026-10-21, ~/Projects/webzites/scripts/kimi-surface.mjs is absent. Existing r18/r20 annotations report W7, the 2026-10-12 ~/Projects prune/migration; the event for this exact file and its actor are not independently verified. The cited table command is a historical record, not an executable instruction.”
- **Why r18/r20 did not cover it:** current annotate() blanks citations on the citing line, then searches only that line or its ±2-line window. Line 48’s window (46–50) has no absence word. git blame shows line 48 was added in commit 9639ec7 on 2026-10-19, after round 18’s 2026-10-14 census. The r20 marker at line 145 is 97 lines away; its own section heading says “table-distance uncleared.” Neither old annotation can satisfy the per-citation window for line 48.

### P3 — Gate coverage includes incidental neighboring-line bleed

The receipt marks the other 27 citations annotated-true in the gate’s sense: the target is absent and annotate() finds absence vocabulary at the cite or within ±2. This is not independent verification of every historical behavior claim. In particular, SKILL.md:223 is covered by the unrelated word “missing” in line 221; free-read-verbs.md:10 is covered by the r18 annotation on sibling source files at line 9; and vault-properties.md:103 is covered by “no longer” in line 102 about an unrelated page-link claim. The contract’s sole T03 unannotatedCites fix remains the line-48 sidecar; no non-author source edits are proposed.

## Checked and held

- Read every population cite with local context and recorded exact current cite-line bytes in the receipt. Classification follows the gate predicate, not whether a cited historical behavior can be reproduced.
- Target checks: test -e exit 1; target stat fails with “No such file or directory”; nearest existing ancestor is /home/vgpnk/Projects (24 directories, no files in the rendered listing). Its recorded birth/mtime/ctime are in the receipt.
- The target itself and parent webzites tree are not a Git repository. The containing repo root is /home/vgpnk; its last-three commit output and empty remote output are recorded in the receipt. No Projects/webzites path-history output was returned.
- Round-open paths-before.json also records T03 as drift with the same single unannotated cite; current sweep independently matches that classification.
- No tools were installed or updated. No source, lane production file, git index, or repository state was modified; only this report was written.

## Limits

The 2026-10-12 W7 prune/migration is attributed by existing r18/r20 annotations; round-18 LOG.md records the child-set reduction and removal of webzites, but this checkout does not independently identify who removed this exact file or its precise removal time. No restore or publish operation was attempted. This report does not run a post-integration C1 counter or claim a green sweep.

## C1 target receipt

c1-receipts/T03.json content:

```json
{
  "id": "T03",
  "token": "~/Projects/webzites/scripts/kimi-surface.mjs",
  "class": "drift",
  "observedAt": "2026-10-21T11:50:05Z",
  "state": "absent",
  "observation": {
    "commands": [
      "test -e /home/vgpnk/Projects/webzites/scripts/kimi-surface.mjs",
      "stat -c '%n %w %y' /home/vgpnk/Projects/webzites/scripts/kimi-surface.mjs",
      "ls -la /home/vgpnk/Projects",
      "stat -c '%n | birth=%w | mtime=%y | ctime=%z' ~/Projects",
      "git -C /home/vgpnk log -3 --format='%H %cI %s'",
      "git -C /home/vgpnk remote -v",
      "git -C /home/vgpnk log --format='%H %cI %s' -- Projects/webzites",
      "node /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/freshness-sweep.mjs --section=paths --json"
    ],
    "output": "Observation at 2026-10-21T11:49:42Z: test -e returned exit 1. stat reported `cannot stat '/home/vgpnk/Projects/webzites/scripts/kimi-surface.mjs': No such file or directory (os error 2)` (exit 1). `ls -la /home/vgpnk/Projects` returned 0 files, 24 dirs; tool output elided 12 entries. Ancestor stat: `/home/vgpnk/Projects | birth=2026-10-03 17:48:28.004231881 -0300 | mtime=2026-10-21 05:19:01.033916520 -0300 | ctime=2026-10-21 05:19:01.033916520 -0300`. Nearest Git root: `/home/vgpnk`; last three commits were `870a97615b8a700e0679a21c131595a584b11d21 2026-10-08T19:06:06-03:00 omp: devin twins back deepseek/glm-5.3 cascades; qwen3.6-flash purged (3.8-flash flash bucket, 3.8-max strong)`, `33e63498e7bbebf03f3cf5f73605de993b1eb3b2 2026-10-08T18:54:22-03:00 omp: re-primary m_grok on grok-4.7:xhigh; grok-4.20-reasoning excluded from routing`, `325c6b12e182345291cb7e51e57745efaa1dcc97 2026-10-08T18:52:25-03:00 omp: drop grok-4.20-multi-agent from all cascades (not routable per operator)`. `git remote -v` returned no lines (exit 0); path-specific webzites history returned no lines. Paths sweep generated 2026-10-21T11:50:05Z, exit 1, T03 drift with 28 cites and sole `unannotatedCites` entry `corpus/lessons/round-6-aggregator-audit.md:48`; overall counts drift 3, newMissing 12, recovered 4."
  },
  "event": "2026-10-12 W7 mega-prune of ~/Projects (round-18 LOG.md says the 36→14 child-set change removed webzites, and existing r18/r20 annotations date that prune/migration); the exact file removal timing and actor remain unverified.",
  "cites": [
    {
      "cite": "SKILL.md:111",
      "lineText": "   `node ~/Projects/webzites/scripts/kimi-surface.mjs sync-check [<id>]` (run *[r20 citation-local 2026-10-19: `~/Projects/webzites/scripts/kimi-surface.mjs` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; this citing command is a historical record, not an executable instruction; it is not executable until restored and re-checked.]*",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "SKILL.md:223",
      "lineText": "| kimi bindings | `node ~/Projects/webzites/scripts/kimi-surface.mjs kimi-map` | chat→domain truth: publishedUrl, publishState, version ids; sweeps project chats top-level ListChats misses | chats beyond sweep pages |",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/drift-detection.md:7",
      "lineText": "Source: `~/Projects/webzites/{bin/webzites.mjs, scripts/kimi-surface.mjs,",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/fire-journal-codes.md:1",
      "lineText": "source: ~/Projects/webzites/scripts/kimi-surface.mjs (die/throw sites) + ~/Projects/webzites/state/{update,recreate,rebuild}-*.json run journals + state/rebuild-charter-fire.log (own-work; no SOURCES.md id); metadata format per S019 (metadata authority only, not a platform source)",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/fire-journal-codes.md:3",
      "lineText": "recheck: on journal or script change — test -e ~/Projects/webzites/scripts/kimi-surface.mjs && echo present || echo absent; grep -lE '\"fire\": *true' ~/Projects/webzites/state/recreate-plazir15-*.json; script vanished in W7 — operator must restore it or retire this entry",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/fire-journal-codes.md:7",
      "lineText": "Source: `~/Projects/webzites/scripts/kimi-surface.mjs` (die/throw sites grep'd",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/fire-journal-codes.md:8",
      "lineText": "> *[r20 citation-local 2026-10-19: `~/Projects/webzites/scripts/kimi-surface.mjs` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; historical record, not an executable instruction.]*",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/fire-journal-codes.md:82",
      "lineText": "- [fire-journal-codes:c1] **HOLD** — The recorded kimi-surface.mjs path remains absent now. Surface: `/home/vgpnk/Projects/webzites/scripts/kimi-surface.mjs`.",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/fire-journal-codes.md:83",
      "lineText": "- [fire-journal-codes:c2] **UNVERIFIABLE** — The current implementation writes each metered run to a JSON journal under state/. Surface: `/home/vgpnk/Projects/webzites/scripts/kimi-surface.mjs`. Unverifiable: The cited implementation and its state directory are both absent; no live source remains to inspect or run to establish this behavior.",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/fire-journal-codes.md:85",
      "lineText": "- [fire-journal-codes:c4] **UNVERIFIABLE** — The listed code-6 new-chat anomaly is classified as consuming a metered fire. Surface: `/home/vgpnk/Projects/webzites/scripts/kimi-surface.mjs`. Unverifiable: The throw-site implementation and the associated journals are unavailable, so the historical code-6 behavior and fired-step state cannot be checked.",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/free-read-verbs.md:1",
      "lineText": "source: ~/Projects/webzites/{bin/webzites.mjs, src/cli.mjs, src/fleet.mjs, src/probe.mjs, src/reconcile.mjs, scripts/kimi-surface.mjs, fleet/fleet.config.json} — local webzites tree read 2026-09-28, entry-internal live-run captures cited in body; metadata contract S019 (corpus/SOURCES.md, metadata authority only, not platform authority)",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/free-read-verbs.md:10",
      "lineText": "`~/Projects/webzites/bin/webzites.mjs`, `~/Projects/webzites/scripts/kimi-surface.mjs`",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/free-read-verbs.md:3",
      "lineText": "recheck: on webzites source change or operator restore — `ls -l ~/Projects/webzites/bin/webzites.mjs ~/Projects/webzites/src/cli.mjs ~/Projects/webzites/scripts/kimi-surface.mjs`; tree absent since the 2026-10-12 ~/Projects prune, so operator must restore it and re-run the cited verbs, or retire the live-run claims and counts in this entry",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/free-read-verbs.md:324",
      "lineText": "| sync-check | `node ~/Projects/webzites/scripts/kimi-surface.mjs sync-check <ids>` / bare | `/tmp/kake-r11/labrat-sync.md` (per-row exits + verdicts, exit-code table, fs-write isolation proof, nondeterminism caveat); `/tmp/kake-r11/sync-all.out` + `sync-all-2nd.out` (repeat determinism), `sync-fleet.json`, `sync-fleet.err`, `sync-burnerchrome.out`, `sync-ds4cc-mirror.out`; unknown-id path (EXIT=1) in `/tmp/kake-r11/err.txt` |",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/free-read-verbs.md:325",
      "lineText": "> *[r20 citation-local 2026-10-19: `~/Projects/webzites/scripts/kimi-surface.mjs` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; this citing command is a historical record, not an executable instruction; it is not executable until restored and re-checked.]*",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/probe-delta-alerting.md:120",
      "lineText": "- [probe-delta-alerting:c2] **HOLD** — The canonical history input and the two cited webzites CLI paths remain absent at their documented ~/Projects/webzites locations. Surface: `test -e /home/vgpnk/Projects/webzites/state/probe-history.jsonl; test -e /home/vgpnk/Projects/webzites/bin/webzites.mjs; test -e /home/vgpnk/Projects/webzites/scripts/kimi-surface.mjs; test -e /home/vgpnk/Projects/webzites`.",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/probe-delta-alerting.md:83",
      "lineText": "  `node ~/Projects/webzites/scripts/kimi-surface.mjs …` (bare `webzites` is",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/probe-delta-alerting.md:84",
      "lineText": "> *[r20 citation-local 2026-10-19: `~/Projects/webzites/scripts/kimi-surface.mjs` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; this citing command is a historical record, not an executable instruction; it is not executable until restored and re-checked.]*",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/publish-channels.md:34",
      "lineText": "`~/Projects/webzites/scripts/kimi-surface.mjs`:",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/publish-channels.md:35",
      "lineText": "> *[r20 citation-local 2026-10-19: `~/Projects/webzites/scripts/kimi-surface.mjs` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; this citing line is a historical record, not an executable instruction; it is not executable until restored and re-checked.]*",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/publish-channels.md:68",
      "lineText": "- [publish-channels:c2] **UNVERIFIABLE** — The Kimi script still enforces the listed update precondition and one-fire confirmation gate, with the documented human publish and post-click verification sequence. Surface: `test -e /home/vgpnk/Projects/webzites/scripts/kimi-surface.mjs; test -e /home/vgpnk/Projects/webzites/fleet/kimi-surface-ops.md; command -v kimi-webbridge; unauthenticated GET https://www.kimi.ai/apiv2/`. Unverifiable: The cited CLI and operations sources are absent, and the host's missing `kimi-webbridge` command does not establish the absence or behavior of every possible channel. An unauthenticated GET of the API root does not determine whether cookie-authenticated methods or the human-gated UI flow exist; those flows were not accessed under the no-auth/no-chat boundary.",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/vault-properties.md:103",
      "lineText": "- [vault-properties:c10] **UNVERIFIABLE** — sourceDir null is the hard blocker enforced by cmdUpdate and cmdRecreate. Surface: `/home/vgpnk/Projects/webzites/scripts/kimi-surface.mjs`. Unverifiable: No surviving implementation or authorized account-operation trace is available; public HTML does not verify sourceDir enforcement. Do not execute write/publish operations to test it.",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/lessons/round-4-aggregator-audit.md:31",
      "lineText": "  ~/Projects/webzites/scripts/kimi-surface.mjs | sort -u` → exactly {1..8, 64} —",
      "authored": "non-author",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/lessons/round-4-aggregator-audit.md:32",
      "lineText": "  > *[r20 citation-local 2026-10-19: `~/Projects/webzites/scripts/kimi-surface.mjs` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; this citing command is a historical record, not an executable instruction; it is not executable until restored and re-checked.]*",
      "authored": "non-author",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/lessons/round-4.md:4",
      "lineText": "`~/Projects/webzites/scripts/kimi-surface.mjs` throw sites (grep `code: [0-9]`,",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/lessons/round-4.md:5",
      "lineText": "> *[r20 citation-local 2026-10-19: `~/Projects/webzites/scripts/kimi-surface.mjs` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; historical record, not an executable instruction.]*",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/lessons/round-6-aggregator-audit.md:145",
      "lineText": "> *[r20 citation-local 2026-10-19: `~/Projects/webzites/scripts/kimi-surface.mjs` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; this citing command is a historical record, not an executable instruction; it is not executable until restored and re-checked.]*",
      "authored": "non-author",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/lessons/round-6-aggregator-audit.md:48",
      "lineText": "| zip-exclude chain `:903` / zip spawn `:906` (`vault-properties.md:60`) | `sed -n '899,908p' ~/Projects/webzites/scripts/kimi-surface.mjs` | `:903` filter, `:906` spawnSync | pass (r10 fix) |",
      "authored": "non-author",
      "status": "unannotated",
      "action": "sidecar",
      "text": "As of 2026-10-21, ~/Projects/webzites/scripts/kimi-surface.mjs is absent. Existing r18/r20 annotations report W7, the 2026-10-12 ~/Projects prune/migration; the event for this exact file and its actor are not independently verified. The cited table command is a historical record, not an executable instruction."
    }
  ]
}
```
