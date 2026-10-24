## Verdict

T08 was **absent** at the lane-rooted path at 2026-10-21T11:50:02Z. Its sole cite, `corpus/knowledge/vault-properties.md:100`, is lane-authored and truthfully reports that there is no local copy at the cited lane paths. Classify it `annotated-true`; append nothing (`action: none`, empty `text`). The outstanding C1 issue is that this observed miss was not yet in `pins.pathsMissSet`.

The lane git history contains no tracked creation or deletion of `fleet/vault-properties.json`. The historical corpus says a relative `fleet/vault-properties.json` snapshot existed around 2026-09-20 and was checked on 2026-09-28, but does not establish that the lane-rooted absolute path in T08 ever existed. The 2026-10-12 webzites prune is a possible explanation for loss of an external source, not a proven removal event for this T08 path; the receipt event is therefore `unknown`.

## Findings

- **P2 — C1 freshness / unpinned new miss.** Exact command: `test -e /home/vgpnk/Projects/shokunin/kake-shokunin/fleet/vault-properties.json; echo "exit=$?"`. Exact observed output: `exit=1`. `paths-before.json` also records `state` evidence `word=absent`, `direct=true`, `mentions=true` for this token and cite; `c1-population.json` classifies it `newMissing`. Smallest fix: L1 should add the observed token `~/Projects/shokunin/kake-shokunin/fleet/vault-properties.json` to `pins.pathsMissSet` in integration. Do not edit the true cite annotation.
- **P3 — Historical event is not attributable to this lane-rooted path.** Exact commands: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin log -S'vault-properties.json' --format='%h %cI %s' -- fleet/vault-properties.json`; `git -C /home/vgpnk/Projects/shokunin/kake-shokunin log --all --format=%h -- fleet/vault-properties.json`. Exact observed output: both commands emitted no lines. The relative historical claim in `vault-properties.md:22-25` and the W7 record that `~/Projects/webzites` was removed in the 2026-10-12 prune do not prove this different absolute path existed or vanished then. Impact: T08 history/event only; current absence and annotation truth are established. Smallest fix: leave the event `unknown` unless direct archival evidence for this exact path is recovered; do not append an unsupported cause.

## Checked and held

- Read the only cited line with ±3 lines (`vault-properties.md:97-103`). Exact cite bytes:
  `- [vault-properties:c8] **HOLD** — The lane has no local copy at the expected source paths of fleet/vault-properties.json or kimi-surface.mjs. Surface (all absent, not executable): `/home/vgpnk/Projects/shokunin/kake-shokunin/fleet/vault-properties.json; /home/vgpnk/Projects/shokunin/kake-shokunin/fleet/kimi-surface.mjs; /home/vgpnk/Projects/shokunin/kake-shokunin/kimi-surface.mjs`.`
- The lane-root `ls -la` shows no `fleet/` entry. `stat` of the target failed with `No such file or directory (os error 2)`. The lane's latest three commits ended at base `f7de3ab4e9f030a15a857a5a08631bd8e690f436`; remote output was `origin https://github.com/VeigaPunk/kake-shokunin.git (fetch)` and `(push)`.
- Round-23 receipt c8 corroborates a `test -e` observation: `fleet/vault-properties.json: ABSENT; fleet/kimi-surface.mjs: ABSENT; kimi-surface.mjs: ABSENT; fleet.config.json: ABSENT` (verdict `HOLD`). The c8 line with `(all absent, not executable)` was committed on 2026-10-21 in `1b309c9`; the absolute lane-root path first appears in the round-23 corpus addition `83098b5`.
- The original corpus text at `vault-properties.md:22-25` documents `fleet/vault-properties.json` with mtime 2026-09-20 / generatedAt 23:40:17Z and says it was byte-equivalent to the live literal on 2026-09-28. This is a historical lane-document claim, not current file evidence. The round-21 provenance header says external fleet evidence was unavailable locally by 2026-10-20. `LOG.md:410-412` later records the 2026-10-12 `~/Projects` prune/migration removing `webzites`; that supports the external-tree disappearance but not this lane path's history.
- The C1 receipt below records the observed state, not independent admission or a claim that a lane-local file's deletion was observed.

## C1 target receipt

```json
{
  "id": "T08",
  "token": "~/Projects/shokunin/kake-shokunin/fleet/vault-properties.json",
  "class": "newMissing",
  "observedAt": "2026-10-21T11:50:02Z",
  "state": "absent",
  "observation": {
    "commands": [
      "test -e /home/vgpnk/Projects/shokunin/kake-shokunin/fleet/vault-properties.json; echo \"exit=$?\"",
      "stat -c '%n %w %y' /home/vgpnk/Projects/shokunin/kake-shokunin/fleet/vault-properties.json",
      "ls -la /home/vgpnk/Projects/shokunin/kake-shokunin",
      "git -C /home/vgpnk/Projects/shokunin/kake-shokunin log -3 --format='%H %cI %s'",
      "git -C /home/vgpnk/Projects/shokunin/kake-shokunin remote -v",
      "git -C /home/vgpnk/Projects/shokunin/kake-shokunin log -S'vault-properties.json' --format='%h %cI %s' -- fleet/vault-properties.json",
      "git -C /home/vgpnk/Projects/shokunin/kake-shokunin log --all --format=%h -- fleet/vault-properties.json"
    ],
    "output": "test -e: exit=1; stat: cannot stat '/home/vgpnk/Projects/shokunin/kake-shokunin/fleet/vault-properties.json': No such file or directory (os error 2); nearest existing ancestor listing: total 196, with .git, .jj, .ufo, corpus, scripts and other lane-root entries, no fleet/ entry; git log -3: f7de3ab4e9f030a15a857a5a08631bd8e690f436 2026-10-21T06:00:18-03:00 round-23: record final committed measurements and recovery audit dispositions; dd58390d3a0b2942ffdd8f0330c0da3dda7b87e1 2026-10-21T05:48:54-03:00 round-23: recover evidence, preserve lesson corrections and reject malformed content type; 5bef55b1464d7ccbff802edab400d138597a621c 2026-10-21T05:18:26-03:00 round-23: verify final URL against captured redirect chain before re-audit; remote: origin https://github.com/VeigaPunk/kake-shokunin.git (fetch); origin https://github.com/VeigaPunk/kake-shokunin.git (push); both path-history commands emitted no lines; observedAt 2026-10-21T11:50:02Z"
  },
  "event": "unknown",
  "cites": [
    {
      "cite": "corpus/knowledge/vault-properties.md:100",
      "lineText": "- [vault-properties:c8] **HOLD** — The lane has no local copy at the expected source paths of fleet/vault-properties.json or kimi-surface.mjs. Surface (all absent, not executable): `/home/vgpnk/Projects/shokunin/kake-shokunin/fleet/vault-properties.json; /home/vgpnk/Projects/shokunin/kake-shokunin/fleet/kimi-surface.mjs; /home/vgpnk/Projects/shokunin/kake-shokunin/kimi-surface.mjs`.",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    }
  ]
}
```

## Limits

Git history proves no tracked lane-file occurrence or deletion, not the nonexistence of a past untracked file. The cited September existence statement is not independently verifiable now, and the missing webzites tree prevents tying its relative `fleet/` snapshot to T08's lane-rooted path. No install, build, lint, formatter, or test was run.