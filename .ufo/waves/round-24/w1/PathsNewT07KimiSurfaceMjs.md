## Verdict

T07 was **absent** at `2026-10-21T11:49:07Z`. The only cite, `corpus/knowledge/vault-properties.md:100`, truthfully states that the lane has no local copy at the listed source paths; classify it `annotated-true`, with `action: none` and no append text. No lane Git history or reflog entry shows `fleet/kimi-surface.mjs` ever existed as a file, so there is no evidenced vanish event or date. This does not prove that an untracked, ephemeral copy never existed.

T07 is nevertheless still a C1 `newMissing` target: it is absent from the 55-entry `pins.pathsMissSet`. The receipt records the observation; integration must still reconcile the pin set to the observed miss set. This report is author-side evidence, not independent admission.

## Findings

- **P2 — C1 pin reconciliation remains open for T07 (freshness).** Exact command: `node /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/freshness-sweep.mjs --section=paths`. Exact observed output: `declaredAbsent  ~/Projects/shokunin/kake-shokunin/fleet/kimi-surface.mjs  corpus/knowledge/vault-properties.md:100`; `VERDICT: DRIFT — §paths: 3 unannotated miss · 12 NOT in pins.pathsMissSet (exit 1)`. Pin membership query returned `pinned: null` and `pathsMissSetCount: 55`. Smallest fix: reconcile `pins.pathsMissSet` to the observed miss set during integration; do not change this already-true cite annotation.

## Checked and held

- The frozen round-24 contract names C1 as reconciliation of all 19 path targets and requires the final `pins.pathsMissSet` to equal the measured miss set.
- Cite read with ±3 lines: `corpus/knowledge/vault-properties.md:100` is a lane-authored round-23 HOLD in the “Live re-verification — round 23 (2026-10-21)” section. Exact current line:
  `- [vault-properties:c8] **HOLD** — The lane has no local copy at the expected source paths of fleet/vault-properties.json or kimi-surface.mjs. Surface (all absent, not executable): `/home/vgpnk/Projects/shokunin/kake-shokunin/fleet/vault-properties.json; /home/vgpnk/Projects/shokunin/kake-shokunin/fleet/kimi-surface.mjs; /home/vgpnk/Projects/shokunin/kake-shokunin/kimi-surface.mjs`.`
  It explicitly marks the listed copies absent, and the cited T07 path is among them. The existing claim remains true; no append is warranted.
- Direct observation: `test -e /home/vgpnk/Projects/shokunin/kake-shokunin/fleet/kimi-surface.mjs` returned false (`exists-rc=1`; final state loop printed `ABSENT  /home/vgpnk/Projects/shokunin/kake-shokunin/fleet/kimi-surface.mjs`). `stat -c '%n %w %y'` reported `cannot stat ...: No such file or directory`; `ls -la /home/vgpnk/Projects/shokunin/kake-shokunin/fleet` reported `No such file or directory`. The nearest existing ancestor, the lane root, listed `.git`, `corpus`, and `scripts`, with no `fleet/` directory. Its observed Git HEAD was `f7de3ab4e9f030a15a857a5a08631bd8e690f436 2026-10-21T06:00:18-03:00 round-23: record final committed measurements and recovery audit dispositions`; `remote -v` returned the GitHub origin for fetch and push.
- History does not show a disappearance. `git -C /home/vgpnk/Projects/shokunin/kake-shokunin log --all --format=%h -- fleet/kimi-surface.mjs`, the requested `-S'kimi-surface.mjs'` search scoped to that path, and the corresponding reflog/path query all returned no entries (exit 0). The 124 commits reachable through `--all` show no path history for `fleet/`; the checked round-23 commit `5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd` also had no `fleet/` tree entries. The lane-rooted absolute spelling first appears in the round-23 corpus update `83098b5` (2026-10-21), as a textual observation, not as a file addition. Accordingly, the receipt's `event` is `unknown`: no creation/removal event or vanish date is evidenced.
- Kept separate from T07: the historical webzites tree was pruned/migrated on 2026-10-12 (round-18 lesson), and its `scripts/kimi-surface.mjs` source path is distinct from this lane-rooted `fleet/kimi-surface.mjs` target. Current direct checks found the webzites tree and all checked candidate paths absent; this does not date a disappearance of T07.
- A live `--section=paths` probe exited 1 and reported T07 as `declaredAbsent` at the cite, while keeping it in `newMissing` because it is not pinned. This agrees with the round-open snapshot.

```json
{
  "id": "T07",
  "token": "~/Projects/shokunin/kake-shokunin/fleet/kimi-surface.mjs",
  "class": "newMissing",
  "observedAt": "2026-10-21T11:49:07Z",
  "state": "absent",
  "observation": {
    "commands": [
      "test -e /home/vgpnk/Projects/shokunin/kake-shokunin/fleet/kimi-surface.mjs",
      "stat -c '%n %w %y' /home/vgpnk/Projects/shokunin/kake-shokunin/fleet/kimi-surface.mjs",
      "ls -la /home/vgpnk/Projects/shokunin/kake-shokunin",
      "git -C /home/vgpnk/Projects/shokunin/kake-shokunin log -3 --format='%H %cI %s'",
      "git -C /home/vgpnk/Projects/shokunin/kake-shokunin remote -v",
      "git -C /home/vgpnk/Projects/shokunin/kake-shokunin log --all --format=%h -- fleet/kimi-surface.mjs",
      "git -C /home/vgpnk/Projects/shokunin/kake-shokunin log -S'kimi-surface.mjs' --format='%h %cI %s' -- fleet/kimi-surface.mjs",
      "git -C /home/vgpnk/Projects/shokunin/kake-shokunin log --reflog --format=%h -- fleet/kimi-surface.mjs",
      "node /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/freshness-sweep.mjs --section=paths"
    ],
    "output": "test -e: exists-rc=1 (ABSENT); stat: cannot stat '/home/vgpnk/Projects/shokunin/kake-shokunin/fleet/kimi-surface.mjs': No such file or directory; ls of lane root shows no fleet/ directory. git log -3: f7de3ab4e9f030a15a857a5a08631bd8e690f436 2026-10-21T06:00:18-03:00 round-23: record final committed measurements and recovery audit dispositions; remote: origin https://github.com/VeigaPunk/kake-shokunin.git (fetch), origin https://github.com/VeigaPunk/kake-shokunin.git (push). Git history and reflog path searches emitted no entries (exit 0). Sweep exit 1; exact relevant lines: declaredAbsent  ~/Projects/shokunin/kake-shokunin/fleet/kimi-surface.mjs  corpus/knowledge/vault-properties.md:100; VERDICT: DRIFT — §paths: 3 unannotated miss · 12 NOT in pins.pathsMissSet (exit 1)."
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

- A Git path search establishes no tracked or ref/reflog history for T07; it cannot rule out an untracked copy outside the recorded history. Therefore no vanish date is claimed.
- A broad project-wide glob timed out and was incomplete; it is not treated as proof of absence. The T07 current-state finding rests on direct named-path checks and lane history.
- No tools were installed or updated. No builds, linters, formatters, or tests were run; only the targeted freshness paths probe was run.
