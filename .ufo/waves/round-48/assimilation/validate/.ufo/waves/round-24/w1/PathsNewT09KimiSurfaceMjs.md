# C1 T09 — `~/Projects/shokunin/kake-shokunin/kimi-surface.mjs` (newMissing)

Observed 2026-10-21T11:46:10Z at lane HEAD `f7de3ab4e9f030a15a857a5a08631bd8e690f436` (round 23, admitted — unchanged during this check). Scratch: `/tmp/kake-r24-PathsNewT09-HaY5` (empty; no lane writes besides this report). No tools installed (none needed). Leaf: no subagents.

## Verdict

Target is genuinely ABSENT and was never present in lane history; the existing annotation at the sole cite is TRUE as of this observation. Receipt action: `none`. The only integration duty for the L1 is to add the token to `pins.pathsMissSet` (that pin, not an annotation, is what `newMissing` flags). Cite classification: `annotated-true` — the citing line itself carries the absence claim (authored with the citation in round 23), and every absence word on it verifies today.

## Findings

None (P0–P3). No defect found in the cite, its annotation, or the pin gap beyond the known round-open `newMissing` condition this round exists to close.

## Checked and held

### Current filesystem state (read-only)

- `test -e /home/vgpnk/Projects/shokunin/kake-shokunin/kimi-surface.mjs` → ABSENT (exit 1). Not a symlink (`test -L` false).
- `stat -c '%n %w %y' kimi-surface.mjs` → `stat: cannot stat 'kimi-surface.mjs': No such file or directory (os error 2)`.
- `ls -la` of the nearest existing ancestor (lane root): only `AGENTS.md LOG.md PROVINCE.md README.md SCORECARD.md SHONEN.md SKILL.md considerthese corpus plans scripts .git .jj .ufo .gitignore` — no `kimi-surface.mjs`.
- `test -e fleet` → `ls: cannot access 'fleet': No such file or directory`; `fleet/vault-properties.json` and `fleet/kimi-surface.mjs` both ABSENT (the other two paths surfaced on the same cite line).
- Upstream origin `~/Projects/webzites/scripts/kimi-surface.mjs` also ABSENT (pruned 2026-10-12, W7 `~/Projects` prune/migration; corpus/lessons/round-18.md:12,16) — no copy survives to restore.

### Did it ever exist? Lane history (git + jj refs)

- `git log --all --format='%h %cI %s' -- kimi-surface.mjs` → empty. `git log --all -- fleet 'fleet/'` → empty (fleet/ never tracked either).
- `git log --all --diff-filter=A --format='%h %cI %s' -- '*kimi-surface*'` → empty. `--all` includes the collocated jj refs (`git for-each-ref refs/jj/**` lists `refs/jj/keep/…`), so no jj-only commit ever added any `kimi-surface` path. Lane history starts `1126144 2026-09-28T15:29:47-03:00 seed: kake shonen`; `git log -S'kimi-surface.mjs' --all` shows only prose/corpus edits, never a file add. Conclusion: `kimi-surface.mjs` NEVER existed in the lane repo; there is no vanishing event to date.

### The cite — `corpus/knowledge/vault-properties.md:100` (±3 read; lines 97–103)

Exact current bytes of line 100 (from `sed -n '100p'`):

```
- [vault-properties:c8] **HOLD** — The lane has no local copy at the expected source paths of fleet/vault-properties.json or kimi-surface.mjs. Surface (all absent, not executable): `/home/vgpnk/Projects/shokunin/kake-shokunin/fleet/vault-properties.json; /home/vgpnk/Projects/shokunin/kake-shokunin/fleet/kimi-surface.mjs; /home/vgpnk/Projects/shokunin/kake-shokunin/kimi-surface.mjs`.
```

- Provenance: authored 2026-10-21T05:11:15-03:00 in commit `1b309c9` "round-23: integrate falsifier corrections and snapshot integrity fixes" (`git blame -L 100,100`). It is the citation line AND its own absence annotation (claim-inline), which is why the round-open sweep matched it (`paths-before.json` evidence: `word: "absent", line: 100, direct: true, mentions: true`).
- Truthfulness, verified today: "The lane has no local copy at the expected source paths" — TRUE (all three surfaced paths absent; `fleet/` entirely absent). "(all absent, not executable)" — TRUE. Nothing on the line is stale; per contract, existing annotations are never rewritten and no correction is owed.
- Why it still gated: the sweep's annotation side is satisfied, but the token `~/Projects/shokunin/kake-shokunin/kimi-surface.mjs` is absent from `pins.pathsMissSet` (`corpus/knowledge/freshness-pins.json`, 55 tokens; only the webzites tokens `~/Projects/webzites/fleet/kimi-surface-ops.md` and `~/Projects/webzites/scripts/kimi-surface.mjs` are pinned; no `kake-shokunin`-root token is). `newMissing` = miss not yet pinned; the L1 must add this token to `pins.pathsMissSet` so `pins.pathsMissSet == observed missSet`.
- Dated event anchor: `.ufo/waves/round-23/receipts/vault-properties.json` entry `c8` (seat `ReverifyVaultProperties`, method `test -e`): `fleet/vault-properties.json: ABSENT; fleet/kimi-surface.mjs: ABSENT; kimi-surface.mjs: ABSENT; fleet.config.json: ABSENT` — landed in `1b309c9` 2026-10-21T05:11:15-03:00.
- Neighborhood hazard check: nearest other cites are `[vault-properties:c7]` at line 99 and `[vault-properties:c9]` at line 103 — none within ±2 lines requires a restoration correction, and action is `none` anyway.

### C1 target receipt

```json
{"id": "T09", "token": "~/Projects/shokunin/kake-shokunin/kimi-surface.mjs", "class": "newMissing", "observedAt": "2026-10-21T11:46:10Z", "state": "absent", "observation": {"commands": ["test -e /home/vgpnk/Projects/shokunin/kake-shokunin/kimi-surface.mjs", "stat -c '%n %w %y' /home/vgpnk/Projects/shokunin/kake-shokunin/kimi-surface.mjs", "ls -la /home/vgpnk/Projects/shokunin/kake-shokunin", "test -e /home/vgpnk/Projects/shokunin/kake-shokunin/fleet", "git -C /home/vgpnk/Projects/shokunin/kake-shokunin log --all --diff-filter=A --format='%h %cI %s' -- '*kimi-surface*'"], "output": "test -e => ABSENT (exit 1); stat: cannot stat 'kimi-surface.mjs': No such file or directory (os error 2); ls -la lane root: no kimi-surface.mjs (AGENTS.md LOG.md PROVINCE.md README.md SCORECARD.md SHONEN.md SKILL.md considerthese corpus plans scripts .git .jj .ufo .gitignore only); fleet: No such file or directory; git log --all --diff-filter=A -- '*kimi-surface*' => empty across all refs incl. refs/jj/*"}, "event": "No vanishing event: the file never existed in lane history. git log --all --diff-filter=A -- '*kimi-surface*' is empty over every ref including collocated refs/jj/* (history starts 1126144 2026-09-28T15:29:47-03:00 'seed: kake shonen') and git log --all -- fleet is empty. The absence claim itself is the round-23 falsifier correction authored 2026-10-21T05:11:15-03:00 (commit 1b309c9 'round-23: integrate falsifier corrections and snapshot integrity fixes'; .ufo/waves/round-23/receipts/vault-properties.json c8, seat ReverifyVaultProperties, method test -e: 'fleet/vault-properties.json: ABSENT; fleet/kimi-surface.mjs: ABSENT; kimi-surface.mjs: ABSENT'). The upstream source ~/Projects/webzites/scripts/kimi-surface.mjs was pruned 2026-10-12 in the W7 ~/Projects prune/migration (corpus/lessons/round-18.md:12,16), so no copy survives to restore; the standing miss belongs in pins.pathsMissSet.", "cites": [{"cite": "corpus/knowledge/vault-properties.md:100", "lineText": "- [vault-properties:c8] **HOLD** — The lane has no local copy at the expected source paths of fleet/vault-properties.json or kimi-surface.mjs. Surface (all absent, not executable): `/home/vgpnk/Projects/shokunin/kake-shokunin/fleet/vault-properties.json; /home/vgpnk/Projects/shokunin/kake-shokunin/fleet/kimi-surface.mjs; /home/vgpnk/Projects/shokunin/kake-shokunin/kimi-surface.mjs`.", "authored": "lane", "status": "annotated-true", "action": "none", "text": ""}]}
```

## Limits

- Absence of an untracked working-tree file before 2026-10-21 cannot be proven from git alone; the strongest available evidence is that no commit in any git/jj ref ever added the path, and the first recorded absence observation is the round-23 falsifier receipt (2026-10-21). On-disk untracked history is `unknown` beyond that.
- The collocated jj store was inspected via `git log --all` (covers `refs/jj/*`); no `jj` CLI command was run, keeping the lane's jj state strictly untouched.
- Filesystem truth is at observation time (2026-10-21T11:46:10Z); a later restore would be new drift for a later round.
