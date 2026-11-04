# Handoff r12 — `cmdProbe` snapshot-clobber merge fix (for the webzites source owner)

**Kake does not edit webzites source** (operator rule: domain source repos are
read-only to lanes). This is the verified patch + test recipe for whoever owns
`~/Projects/webzites`. It supersedes the r11 F1 proposal <!-- r18 re-census 2026-10-14: ~/Projects/webzites absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
(`/tmp/kake-r11/scout-verbs.md:126`), which was **refuted** this round: its
guard `positionals.length > 0 && !flags.all` still clobbers on
`probe <id> --all` (selection `src/cli.mjs:75` ignores `--all`; the BOOL is
parsed at `:57`, reaches `cmdProbe` via `:1070-1071`, and is never read —
grep: 0 uses of `flags.all`).

## Defect

`cmdProbe` (`src/cli.mjs:72-89`) passes the raw probed subset to
`saveProbe(ROOT, results)` at `src/cli.mjs:78`, overwriting
`state/probe-latest.json` with only the probed rows. A `probe <id>` shrinks the
18-row fleet snapshot to 1 row; `status` exit flips 1→0 (masking 5 violated +
1 error) until the next 6h sweep. This violates `saveProbe`'s own intent
comment (`src/fleet.mjs:27-29` — site-scoped verbs "must not erase every other
site's verdict"). `grokbot tick` (`src/cli.mjs:289`) and `bots task`
(`src/cli.mjs:647`) already merge via `mergeProbeResults`; `cmdProbe` was left
raw in the r2-era fix (webzites-side archaeology: `/tmp/kake-r11/revenger-merge.md`).

## Patch (one line + comment; replica-verified `/tmp/kake-r12/revenger-replica`)

```diff
--- a/src/cli.mjs
+++ b/src/cli.mjs
@@ cmdProbe (src/cli.mjs:72-89)
-  saveProbe(ROOT, results);
+  // Merge like tick/bots task (cli.mjs:289, :647): a subset probe must not
+  // erase the fleet snapshot (fleet.mjs:27-29 intent). Bare probe = full set.
+  saveProbe(ROOT, positionals.length > 0 ? mergeProbeResults(loadLastProbe(ROOT), results, config.sites.map((site) => site.id)) : results);
```

Both `mergeProbeResults` (`src/fleet.mjs:30-37`) and `loadLastProbe`
(`src/fleet.mjs:14-18`) are already imported at `src/cli.mjs:7` — no import
changes. `node --check` clean on the patched replica.

## Verified behavior (replica, byte-identical source baseline sha `8c5bb8ca…`)

| command | before (unpatched) | after (patched) |
|---|---|---|
| `probe plazir15-ghp --quiet` | exit 0; snapshot 18→1 rows; history `total:1` | exit 0; **18 rows kept** (12 ok/5 violated/1 error preserved, plazir15-ghp refreshed); history `total:18` |
| `status` after subset probe | exit 0 (masked) | exit 1 (fleet truth preserved) |
| `status --json` | always 0 (unchanged) | always 0 (unchanged) |
| `probe <id> --all` (edge) | 18→1 rows (clobber — **this is what refutes the r11 guard**) | 18 rows (merged) |

Behavior notes: history lines for subset probes now record merged fleet totals
(matches tick/`bots task` precedent; `probe-delta.mjs`'s spot-row suppression
rule keys on `total:1`, so merged rows stop fabricating phantom clear/re-enter
pairs — this *removes* 40-of-42 phantom noise at the source); exit codes,
stdout, `--quiet`/`--json` semantics unchanged; rows removed from
`fleet.config.json` may persist stale in the merged snapshot until the next
bare `probe` (pre-existing tick property; bare probe stays the full-reset path).

## Owner test recipe

```bash
cd ~/Projects/webzites <!-- r18 re-census 2026-10-14: ~/Projects/webzites absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
cp state/probe-latest.json /tmp/pl.bak && cp state/probe-history.jsonl /tmp/ph.bak
node bin/webzites.mjs probe plazir15-ghp --quiet      # apply patch first
node -e 'console.log(require("./state/probe-latest.json").results.length)'   # expect 18
node bin/webzites.mjs status; echo "exit=$?"           # expect exit 1 (fleet truth)
node bin/webzites.mjs probe plazir15-ghp --all --quiet # edge: expect still 18 rows
# rollback: cp /tmp/pl.bak state/probe-latest.json && cp /tmp/ph.bak state/probe-history.jsonl && git -C . checkout -- src/cli.mjs
```

Evidence chain: `/tmp/kake-r12/revenger-patch.md` (verified line pins),
`/tmp/kake-r12/revenger-replica/` (patched tree + run logs), r11 live clobber
18→1 (`/tmp/kake-r11/labrat-probe.md`), history line 77 = the permanent r11
`total:1` spot row (append-only, `src/fleet.mjs:51`). Round report:
`.ufo/reports/round-12/kake.md`.
