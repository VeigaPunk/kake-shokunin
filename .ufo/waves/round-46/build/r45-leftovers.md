# r45 leftovers sweep — kake-r46 / RevengerRound45Leftovers

Swept lane working tree `/home/vgpnk/Projects/shokunin/kake-shokunin` at HEAD `ded938d2` (round-46 v2 spec), 2026-10-24. Deleted nothing.

## Verdict

| Probe | Result |
|---|---|
| Untracked / uncommitted (`git status --porcelain`) | **1 file, expected**: `.ufo/waves/round-46/w1/swarm-registry.json` (live round-46 harness registry). No r45 bytes uncommitted. |
| Stray `__pycache__` under `.ufo/waves/round-45/` | **PRESENT (finding)** — 3 stale `.pyc`, gitignored, untracked, pre-date r45 tip. Owner should `rm -r`; this seat deletes nothing. |
| Files newer than r45 tip `7cdbaefd` outside `.ufo/waves/round-46/` | **3 files, all clean & committed** at `bd86ee8` (round-46 freeze): `LOG.md`, `corpus/lessons/round-46.md`, `SCORECARD.md`. Only other newer entries are `.jj/` VCS internals. No stray content. |
| Seat reports vs registries, `w1/` + `w2/` | **COMPLETE**: w1 32/32, w2 32/32; zero missing reports, zero orphan reports. |

## Evidence (verbatim)

r45 tip used as mtime baseline: `7cdbaefd3ecbbc8814eca1f013fcee101a6157b0` "round-45 verifier spot-check (integrator, hyaku)", committer epoch `1792816643` (2026-10-24T01:37:23-03:00).

### 1. Working tree status

```
$ git status --porcelain=v1 --untracked-files=all
?? .ufo/waves/round-46/w1/swarm-registry.json
```

### 2. Stray pycache

```
$ find .ufo/waves/round-45 -name __pycache__ -o -path '*__pycache__/*'
.ufo/waves/round-45/__pycache__
.ufo/waves/round-45/__pycache__/c45_audit.cpython-314.pyc
.ufo/waves/round-45/__pycache__/c45_count.cpython-314.pyc
.ufo/waves/round-45/__pycache__/c45_freshness.cpython-314.pyc

$ git check-ignore -v .ufo/waves/round-45/__pycache__/c45_audit.cpython-314.pyc
.gitignore:2:__pycache__/	.ufo/waves/round-45/__pycache__/c45_audit.cpython-314.pyc
$ git ls-files .ufo/waves/round-45/__pycache__/
(nothing tracked)
$ stat -c '%y %n' .ufo/waves/round-45/__pycache__/*
2026-10-24 01:01:38 .ufo/waves/round-45/__pycache__/c45_audit.cpython-314.pyc
2026-10-24 00:39:36 .ufo/waves/round-45/__pycache__/c45_count.cpython-314.pyc
2026-10-24 00:59:29 .ufo/waves/round-45/__pycache__/c45_freshness.cpython-314.pyc
```

All three mtimes pre-date the r45 tip → stale r45 instrument byproduct, invisible to `git status` because gitignored.

### 3. Newer-than-tip sweep

```
$ find . -path ./.git -prune -o -path ./.ufo/waves/round-46 -prune -o -type f -newermt "@1792816643" -printf '%p\n' | grep -v '^\./\.jj/'
./LOG.md
./corpus/lessons/round-46.md
./SCORECARD.md            # each mtime 2026-10-24 01:45:59

$ git log -1 --format='%h %s' -- LOG.md   # same for the other two
bd86ee8 round-46: freeze claims (C1 redirect/rewrite audit capability, C2 citation-hygiene gate)
$ git status --porcelain -- LOG.md corpus/lessons/round-46.md SCORECARD.md
(clean — no output)
```

(`.jj/` entries are jj op-log/working-copy metadata refreshed by the round-46 commits up to `ded938d2`; not lane content.)

### 4. Registries vs reports

```
$ python3 - (diff registry["members"] vs <wave>/*.md)
[w1] registry=32 reports=32
  missing reports: NONE
  orphan reports (in dir, not in registry): NONE
[w2] registry=32 reports=32
  missing reports: NONE
  orphan reports (in dir, not in registry): NONE
```

## Recommended (not executed — deletion out of my bounds)

L1/integrator may `rm -r /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/__pycache__` and, if r45-era byproducts should never reappear, add `-B` discipline (all r45 counters already run `python3 -B` per round claims; the `.pyc` came from imports, e.g. `c45_freshness`).

No blockers. Full seat report: `.ufo/waves/round-46/w1/RevengerRound45Leftovers.md`.
