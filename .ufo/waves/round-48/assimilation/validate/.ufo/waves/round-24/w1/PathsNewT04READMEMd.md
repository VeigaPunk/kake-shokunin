## Verdict

C1 T04 (`~/Projects/lucario/site/README.md`, `newMissing`) is absent as observed at `2026-10-21T11:50:41Z`. Its only cite, `SKILL.md:458`, already directly marks the local directory and README absent and correctly classifies the README's alleged publish-gate contents as `UNVERIFIABLE`; no append-only cite text is proposed (`action: none`). The freshness gap is the missing token in `pins.pathsMissSet`, not an unannotated cite.

Historical evidence supports that a Lucario README with the quoted “pending — gated” text existed by 2026-09-28, but does not independently prove that the exact local file path was read then. The tree was last positively observed with `lucario` present on 2026-09-29 and first documented absent by the 2026-10-14 round-18 sweep. The lane attributes the removal to the W7 prune/migration dated 2026-10-12; the exact deletion time of this README is not retained.

## Findings

### P2 — T04 is an unpinned missing path (C1, freshness)

**Exact commands and observed output:**

- `test -e /home/vgpnk/Projects/lucario/site/README.md` → `absent (exit=1)`.
- `stat -c '%n %w %y' /home/vgpnk/Projects/lucario/site/README.md` → `stat: cannot stat '/home/vgpnk/Projects/lucario/site/README.md': No such file or directory (os error 2)`; exit 1.
- `ls -la /home/vgpnk/Projects` → complete listing of the nearest existing ancestor; there is no `lucario` entry. It includes `ds4cc-marketplace` (reappeared), but no Lucario directory.
- `git -C /home/vgpnk/Projects/lucario log -3 --format='%H %cI %s'` and `git -C /home/vgpnk/Projects/lucario remote -v` each → `fatal: cannot change to '/home/vgpnk/Projects/lucario': No such file or directory`; each exit 128. The project checkout is absent, so its git history/remotes cannot be queried.
- `git -C /home/vgpnk/Projects/shokunin/kake-shokunin log --all -S'~/Projects/lucario/site/README.md' --format='%h %cI %s' -- corpus/knowledge/freshness-pins.json` → no output. The current pin file contains `~/Projects/lucario` and `~/Projects/lucario/site`, but not the README token.

**Cite classification:** `SKILL.md` is lane-authored. The exact current line is:

`- [property-map:c37] **UNVERIFIABLE** — The referenced README still documents a pending, gated first publish. Surface: `/home/vgpnk/Projects/lucario/site/README.md`. Unverifiable: The mapped source directory and README are absent at this host, and the live 404 cannot determine whether the upstream README's publish gate remains pending.`

The absence assertion is directly true at this host. The README-content claim is explicitly marked unverifiable; the line does not present its current state as verified. Therefore the annotation is `annotated-true`, with `action: none` and no proposed appended text.

**History / existence:**

- `git -C /home/vgpnk/Projects/shokunin/kake-shokunin log -S'lucario/site/README.md' --format='%h %cI %s' -- SKILL.md` shows the cite entering the HEAD history in `83098b5` (`2026-10-21T04:26:49-03:00`, round-23 integration). The matching line is unchanged in the frozen round-24 base.
- `corpus/knowledge/fleet-registry.md:1-3,16-19` records `verified-at: 2026-09-28` and quotes the Lucario README as “first publish pending — gated.” This supports prior README existence/content; the exact local `site/README.md` identity is an inference from the mapped source path, not an independently preserved file-level observation.
- At round 17, `72eb112` pins `lucario` in `projectsChildrenSet` and records the set match on 2026-09-29. The round-18 lesson (`corpus/lessons/round-18.md:9-16`) says W7 removed `lucario` and other project trees, dates the prune/migration to 2026-10-12, and bounds it as sometime after r17 and before the 2026-10-14 r18 census. Round-18 pins include `~/Projects/lucario` and `~/Projects/lucario/site` in `pathsMissSet`. This establishes the disappearance window, not an exact deletion timestamp.

**Smallest fix:** add `~/Projects/lucario/site/README.md` to the round-24 `pins.pathsMissSet` so the pin matches the observed miss set. No cite edit is recommended.

### C1 target receipt

```json
{
  "id": "T04",
  "token": "~/Projects/lucario/site/README.md",
  "class": "newMissing",
  "observedAt": "2026-10-21T11:50:41Z",
  "state": "absent",
  "observation": {
    "commands": [
      "date -u +%Y-%m-%dT%H:%M:%SZ",
      "p=/home/vgpnk/Projects/lucario/site/README.md; if test -e \"$p\"; then echo \"test -e $p => present\"; else r=$?; echo \"test -e $p => absent (exit=$r)\"; fi",
      "stat -c '%n %w %y' \"$p\" 2>&1",
      "ls -la /home/vgpnk/Projects",
      "stat -c '%n | birth=%w | mtime=%y | type=%F' /home/vgpnk/Projects /home/vgpnk",
      "git -C /home/vgpnk/Projects/lucario log -3 --format='%H %cI %s' 2>&1",
      "git -C /home/vgpnk/Projects/lucario remote -v 2>&1"
    ],
    "output": "2026-10-21T11:50:41Z; test -e /home/vgpnk/Projects/lucario/site/README.md => absent (exit=1); stat: cannot stat '/home/vgpnk/Projects/lucario/site/README.md': No such file or directory (os error 2) (exit=1); ls -la /home/vgpnk/Projects completed and the full listing contains no lucario entry; stat of /home/vgpnk/Projects: birth=2026-10-03 17:48:28.004231881 -0300, mtime=2026-10-21 05:19:01.033916520 -0300; git log and remote each: fatal: cannot change to '/home/vgpnk/Projects/lucario': No such file or directory (exit=128)."
  },
  "event": "W7 ~/Projects prune/migration, lane-dated 2026-10-12: corpus/lessons/round-18.md:9-16 names lucario among the removed roots; r17 (2026-09-29) is the last positive child-set record and r18 (2026-10-14) is the first negative census. The exact README deletion time is not retained.",
  "cites": [
    {
      "cite": "SKILL.md:458",
      "lineText": "- [property-map:c37] **UNVERIFIABLE** — The referenced README still documents a pending, gated first publish. Surface: `/home/vgpnk/Projects/lucario/site/README.md`. Unverifiable: The mapped source directory and README are absent at this host, and the live 404 cannot determine whether the upstream README's publish gate remains pending.",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    }
  ]
}
```

## Checked and held

- Read the frozen round-24 contract, the C1 population entry for T04, the round-open paths snapshot, and `SKILL.md:455-461` (the cite with ±3 lines of context). T04 has exactly one cite: `SKILL.md:458`.
- The round-open snapshot directly records T04 under `declaredAbsent` with evidence word `absent`, direct and mentioning at line 458; it is nevertheless `newMissing` because it was not in the pinned miss set. The C1 population labels it `newMissing`.
- Read the freshness-sweep annotation and set-delta logic: an absence word at the citing line makes this cite annotated; the independent pin delta still reports unpinned misses.
- No lane production file, pin, git index, or jj state was changed. No tool was installed. No current freshness sweep was run.

## Limits

- The local Lucario tree is absent, so its own repository history, remotes, and README bytes cannot be inspected. Historical lane prose supports prior README content but is not direct proof of exact local file identity.
- The best supported disappearance interval is after the 2026-09-29 r17 positive record and by the 2026-10-14 r18 negative census. The lane assigns the W7 event date 2026-10-12, but no surviving path-specific deletion timestamp establishes the exact moment.
- Current absence is filesystem truth at the receipt timestamp only; no upstream source, current publication state, or current Kimi 404 was rechecked for this assignment.
