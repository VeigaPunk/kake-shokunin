## Verdict

T17 (`~/Projects/ds4cc-marketplace/CNAME`) is **recovered; state present**, observed at `2026-10-21T11:50:15Z`. The current 9-byte CNAME value is exactly `ds4cc.com` and is tracked at local HEAD `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28`. The one population cite is in a non-author `*aggregator*.md` file, so the correction must be a `restored` entry in the lane-owned sidecar, not an inline edit. This is author-side evidence only; no independent admission is claimed.

## Findings

### P2 — T17's r18 current-state annotation is stale after the fresh clone (freshness)

**Exact read-only commands and observed output** (commands run against the restored source tree):

- `date -u +%Y-%m-%dT%H:%M:%SZ` → `2026-10-21T11:50:15Z`
- `test -e /home/vgpnk/Projects/ds4cc-marketplace/CNAME && echo 'CNAME exists' || echo 'CNAME absent'` → `CNAME exists`
- `stat -c '%n %w %y' /home/vgpnk/Projects/ds4cc-marketplace/CNAME` → `/home/vgpnk/Projects/ds4cc-marketplace/CNAME 2026-10-21 05:19:05.036234032 -0300 2026-10-21 05:19:05.036234032 -0300`
- `ls -la /home/vgpnk/Projects/ds4cc-marketplace` → abbreviated faithfully: `total 268`; `-rw-r--r-- 1 vgpnk vgpnk     9 Oct 21 05:19 CNAME`; `drwxr-xr-x 1 vgpnk vgpnk   248 Oct 21 05:19 burnerchrome`; `drwxr-xr-x 1 vgpnk vgpnk   112 Oct 21 05:19 speedrun`; other directory rows omitted.
- `od -c /home/vgpnk/Projects/ds4cc-marketplace/CNAME` → `0000000   d   s   4   c   c   .   c   o   m` then `0000011` (9 bytes, no final newline).
- `git -C /home/vgpnk/Projects/ds4cc-marketplace hash-object --no-filters -- CNAME` → `0883895ee82a66676768a7665488b3dde4089f09`; `git -C /home/vgpnk/Projects/ds4cc-marketplace ls-tree HEAD -- CNAME` → `100644 blob 0883895ee82a66676768a7665488b3dde4089f09\tCNAME`.
- `git -C /home/vgpnk/Projects/ds4cc-marketplace log -3 --format='%H %cI %s'` → `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28 2026-10-21T05:51:24-03:00 omarchy-usage: sync page to usage-tray 1.10.0 (14 omp-metered providers, how it works, working install)`; `95dbeb69b2db413f00f5310a171334967c368924 2026-10-21T05:21:55-03:00 os-tuning: add gkeep (local post-it notes for the Omarchy bar) at /gkeep/`; `6e888784ae1bac9d341cc9af7fe12f9c5d83f31f 2026-10-20T14:33:09Z magga: Enduro — Classic & Remastered`.
- `git -C /home/vgpnk/Projects/ds4cc-marketplace remote -v` → `origin\thttps://github.com/VeigaPunk/ds4cc-marketplace.git (fetch)` and `origin\thttps://github.com/VeigaPunk/ds4cc-marketplace.git (push)`.
- `cat /home/vgpnk/Projects/ds4cc-marketplace/.git/logs/HEAD` first entry → `0000000000000000000000000000000000000000 6e888784ae1bac9d341cc9af7fe12f9c5d83f31f r20 <r20@example.invalid> 1792570745 -0300\tclone: from https://github.com/VeigaPunk/ds4cc-marketplace.git`. The epoch resolves to `2026-10-21T05:19:05-03:00`, matching the CNAME birth time. The directory's birth time was `2026-10-21 05:19:01.033916520 -0300`.

The CNAME value cell in the historical round-1 cite (`ds4cc.com` ✓) matches current bytes. The line's r18 annotation says the target was absent after the 2026-10-12 prune and explicitly retains the cite as a historical record. That dated observation is not rewritten; it is now stale as a description of current presence. There are no r20 or r23 absence notes on this cite. The round-1 command result itself remains historical and is not re-executed by this observation.

The precise citation is `corpus/lessons/round-1-aggregator-audit.md:30`; its current line bytes are:

`| ds4cc CNAME | `cat ~/Projects/ds4cc-marketplace/CNAME` | `ds4cc.com` ✓ | <!-- r18 re-census 2026-10-14: ~/Projects/ds4cc-marketplace/CNAME absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->`

Classification: **authored `non-author`; status `annotated-stale`; action `sidecar`**. The filename matches the frozen non-author `corpus/lessons/*aggregator*.md` rule. Exact-line SHA-256 (without newline), for the sidecar binding: `76dbe84b3874b39525582339f8d1ca7ddd796c2ef71ea2ba93cdbf1a334655c5`.

Smallest fix: add one `kind: restored` entry to `corpus/knowledge/freshness-sidecar.json` (`schema: kake-paths-sidecar-v1`), with `file: corpus/lessons/round-1-aggregator-audit.md`, `line: 30`, `token: ~/Projects/ds4cc-marketplace/CNAME`, the line SHA above, and `date: 2026-10-21`. Its exact `note` (also the proposed correction text) is:

`<!-- r24 restoration 2026-10-21: observed ~/Projects/ds4cc-marketplace/CNAME present at 2026-10-21T11:50:15Z: 9 bytes, exact value ds4cc.com, blob 0883895ee82a66676768a7665488b3dde4089f09 at HEAD 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28. This fresh clone confirms current presence and value only; the round-1 checkmark remains a historical/unverified observation of the prior checkout, and the r18 re-census remains a historical 2026-10-14 observation, not a statement of current state. -->`

### P2 — T17 is recovered but the existing pin is stale (freshness)

**Exact command:** `cd /home/vgpnk/Projects/shokunin/kake-shokunin && node scripts/freshness-sweep.mjs --section=paths --json` (JSON was captured under `/tmp/kake-r24-PathsRestoredT17CNAME-3ljF/paths.json` to avoid truncating the sweep output while summarizing it).

**Exact observed summary:** `sweep_exit=1`; `paths_ok False`; counts `{"declaredAbsent": 60, "declaredAbsentIndirect": 4, "drift": 3, "newDrift": 0, "newMissing": 12, "resolve": 19, "unresolved": 10}`; `resolve_CNAME True`; `drift_CNAME False`; `newMissing_CNAME False`; `recovered_CNAME True`; `recovered_all ["~/Projects/ds4cc-marketplace", "~/Projects/ds4cc-marketplace/CNAME", "~/Projects/ds4cc-marketplace/burnerchrome", "~/Projects/ds4cc-marketplace/speedrun"]`; reasons `["§paths: 3 unannotated miss · 12 NOT in pins.pathsMissSet"]`; stderr was empty. The current `freshness-pins.json` still includes the CNAME token in `pins.pathsMissSet`; the integrator must remove it in the coordinated re-pin. This single target does not clear the overall paths gate.

### P2 — Restored subtree and historical HEAD claims are not interchangeable (freshness / publishing)

**Observed comparison:** `git -C /home/vgpnk/Projects/ds4cc-marketplace ls-tree HEAD -- burnerchrome speedrun` lists both directories as tracked trees. `speedrun` has 47 tracked descendants; `speedrun/data/manifest.json`, `speedrun/index.html`, and `speedrun/main.js` are tracked. `burnerchrome` is also a tracked directory. The current tree therefore matches those directory-presence claims, but the pre-reappearance status cannot be reused as current status; T18/T19 own their respective receipts. Local tree presence does not establish current Kimi or Pages serving behavior.

The current local branch is `main` at `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28`; local `origin/main` also resolves to that commit and `git rev-list --count origin/main..HEAD` returned `0`. The corpus's pinned `pq2Remote` `e6bd071887bfaa87eff07ab03d323d5b92760fba` is an ancestor 28 commits behind current HEAD, not the current local tracking ref. The paired `pq2Unpushed: 20` figure is historical and does not describe this clone. Local `origin/main` reflog entries say `update by push` at `2026-10-21T05:34:58-03:00` and `2026-10-21T05:51:26-03:00`; no remote was contacted in this investigation, so remote state and deployment outcome remain unverified.

For the historical content comparison, `git -C /home/vgpnk/Projects/ds4cc-marketplace cat-file -s e6bd071887bfaa87eff07ab03d323d5b92760fba:index.html` returned `79453`, and its SHA-256 was `b6f65899e3e6aaf3b2df0c4ef82157fa328faf1c6e5d871c8806a450052f1d33`, matching the corpus's old `b6f65899…` value. Current HEAD's `index.html` is 77,625 bytes with SHA-256 `d0a2f357b19832e8ec8b0cbf80fa045734eff8a63d28e040434b9dcb5790f1d9`. Thus the old byte-identity claim is not a claim about current HEAD; what ds4cc.com currently serves is unverified here.

### C1 target receipt

```json
{
  "id": "T17",
  "token": "~/Projects/ds4cc-marketplace/CNAME",
  "class": "recovered",
  "observedAt": "2026-10-21T11:50:15Z",
  "state": "present",
  "observation": {
    "commands": [
      "test -e /home/vgpnk/Projects/ds4cc-marketplace/CNAME && echo 'CNAME exists' || echo 'CNAME absent'",
      "stat -c '%n %w %y' /home/vgpnk/Projects/ds4cc-marketplace/CNAME",
      "ls -la /home/vgpnk/Projects/ds4cc-marketplace",
      "git -C /home/vgpnk/Projects/ds4cc-marketplace log -3 --format='%H %cI %s'",
      "git -C /home/vgpnk/Projects/ds4cc-marketplace remote -v",
      "od -c /home/vgpnk/Projects/ds4cc-marketplace/CNAME",
      "git -C /home/vgpnk/Projects/ds4cc-marketplace hash-object --no-filters -- CNAME",
      "git -C /home/vgpnk/Projects/ds4cc-marketplace rev-parse HEAD",
      "git -C /home/vgpnk/Projects/ds4cc-marketplace ls-tree HEAD -- CNAME",
      "cat /home/vgpnk/Projects/ds4cc-marketplace/.git/logs/HEAD"
    ],
    "output": "At 2026-10-21T11:50:15Z: CNAME exists; stat reports birth and mtime 2026-10-21 05:19:05.036234032 -0300; ls -la shows a 9-byte CNAME plus burnerchrome/ and speedrun/; od is `d s 4 c c . c o m` (9 bytes, no newline); hash-object and HEAD tree blob are both 0883895ee82a66676768a7665488b3dde4089f09; HEAD is 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28; git log's first row is that HEAD; remote origin is https://github.com/VeigaPunk/ds4cc-marketplace.git; first HEAD reflog row records `clone: from https://github.com/VeigaPunk/ds4cc-marketplace.git` at 2026-10-21T05:19:05-03:00."
  },
  "event": "2026-10-21T05:19:05-03:00 fresh clone of https://github.com/VeigaPunk/ds4cc-marketplace.git; the first .git/logs/HEAD row records `clone: from https://github.com/VeigaPunk/ds4cc-marketplace.git` at epoch 1792570745 -0300, and the CNAME birth time is the same timestamp.",
  "cites": [
    {
      "cite": "corpus/lessons/round-1-aggregator-audit.md:30",
      "lineText": "| ds4cc CNAME | `cat ~/Projects/ds4cc-marketplace/CNAME` | `ds4cc.com` ✓ | <!-- r18 re-census 2026-10-14: ~/Projects/ds4cc-marketplace/CNAME absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->",
      "authored": "non-author",
      "status": "annotated-stale",
      "action": "sidecar",
      "text": "<!-- r24 restoration 2026-10-21: observed ~/Projects/ds4cc-marketplace/CNAME present at 2026-10-21T11:50:15Z: 9 bytes, exact value ds4cc.com, blob 0883895ee82a66676768a7665488b3dde4089f09 at HEAD 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28. This fresh clone confirms current presence and value only; the round-1 checkmark remains a historical/unverified observation of the prior checkout, and the r18 re-census remains a historical 2026-10-14 observation, not a statement of current state. -->"
    }
  ]
}
```

## Checked and held

- Read the frozen round-24 contract and C1 population. T17 is the recovered target with exactly one cite, `corpus/lessons/round-1-aggregator-audit.md:30`.
- Read the cite line with ±3 lines of context. No other CNAME target cite exists in the C1 population; the line is a non-author aggregator file. Its value cell matches current CNAME bytes; its r18 marker is a dated historical observation whose current-state implication needs a restoration correction, not rewriting.
- The local Git tree has both `burnerchrome/` and `speedrun/`; presence alone leaves their external publishing, Kimi surface, and live-page claims unverified. T18/T19 should own their correction/receipt.
- Current CNAME has the same blob hash at current HEAD and the historical pinned `e6bd0718` revision; this corroborates the value in that Git history, not the old machine checkout or current live service.
- No tool was installed or updated.

## Limits

- Read-only local observation only. No remote Git query, live ds4cc.com request, Pages settings check, or deployment-run check was made; local tracking reflogs do not substitute for current remote or served-state verification.
- Did not modify corpus, pins, sweep code, any source tree, or Git state. Only this assigned report file was written. Full C1 acceptance is not claimed; the paths sweep remains exit 1 for other drift and new-missing targets.
