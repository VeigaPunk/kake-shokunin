# SentinelWriteScope — round-50 wave-1 write-scope audit

Seat: leaf (sentinel), wave 1 of round 50. Scope: attribute every dirty path in
the lane repo and the fleet repo to its writer; name anything a round-50 seat
wrote outside its own report file, especially at the fleet root. Read-only
audit — nothing was deleted or modified by this seat.

## Commands run

```
git -C /home/vgpnk/Projects/shokunin/kake-shokunin status --porcelain
git -C /home/vgpnk/Projects/shokunin status --porcelain
```

(Plus read-only `stat`, `git diff`, `cat`, `tail`, `file` to attribute mtimes and
contents. No mutating git/jj command was run.)

---

## Lane repo — `/home/vgpnk/Projects/shokunin/kake-shokunin`

`git status --porcelain` output (verbatim):

```
 M corpus/QUALITY.md
?? .ufo/waves/round-46/residual/
?? .ufo/waves/round-48/assimilation/validate/.ufo/waves/round-21/anchors-fixed.json
?? .ufo/waves/round-48/assimilation/validate/.ufo/waves/round-36/realrun/snap-bodies-run2.tar.xz
?? .ufo/waves/round-48/assimilation/validate/.ufo/waves/round-36/realrun/snap-bodies.tar.xz
?? .ufo/waves/round-48/assimilation/validate/.ufo/waves/round-37/sealed/cases.json
?? .ufo/waves/round-48/assimilation/validate/.ufo/waves/round-39/sources/xmlschema11-2.html
?? .ufo/waves/round-48/assimilation/validate/.ufo/waves/round-40/sources/xmlschema11-2.html
?? .ufo/waves/round-48/assimilation/validate/.ufo/waves/round-41/realrun/sitemaps/nodejs.xml
?? .ufo/waves/round-48/assimilation/validate/.ufo/waves/round-41/realrun/sitemaps/postgresql.xml
?? .ufo/waves/round-48/assimilation/validate/.ufo/waves/round-42/controls/w1/CtlCache/ctl_accept_table_seed4242.py
?? .ufo/waves/round-50/w1/
?? corpus/knowledge/crawl-error-status-table.md
?? corpus/lessons/round-50.md
```

### Attribution

| Path | Status | Attributed writer | In-scope for a w1 leaf seat? |
|------|--------|-------------------|------------------------------|
| `corpus/QUALITY.md` | modified (+28 lines, "Round-50 criteria") | **Orchestrator/L1** — appends the round-50 criteria block; mtime 22:39 aligns with L1 spec/dispatch work, not a leaf report. | NO — L1-owned production file. A leaf seat must not write it. |
| `corpus/knowledge/crawl-error-status-table.md` | untracked | L1 / item-10 assimilation contract author (knowledge file). | NO — production corpus file, L1-owned. |
| `corpus/lessons/round-50.md` | untracked | L1 (round-50 lesson; referenced by QUALITY.md grounding). | NO — production corpus file, L1-owned. |
| `.ufo/waves/round-50/w1/` | untracked | **Round-50 w1 leaf seats** — contains `ExecRerunC1Base.md`, `ExecRerunC1Pre.md`, `ExecRerunC2Base.md` (three leaf report files) + `swarm-registry.json` (orchestrator dispatch registry). | YES — this is the sanctioned w1 report directory. Each `.md` is a leaf's own report file. |
| `.ufo/waves/round-46/residual/` | untracked | **Orchestrator-owned** (eight residual reports). | NO — explicitly operator/orchestrator-owned; contract says leave uncommitted/untouched. Correctly still uncommitted. |
| `.ufo/waves/round-48/assimilation/validate/...` (9 entries) | untracked | **Inherited validation copies** from prior rounds (21/36/37/39/40/41/42). | NO — the nine `>1MiB` copies the contract says stay uncommitted. Correctly still uncommitted. |

**No leaf seat wrote outside its own report file inside the lane.** The only
round-50-attributable leaf writes are the three `w1/*.md` reports, all inside
the sanctioned `.ufo/waves/round-50/w1/` directory. The three production files
(`QUALITY.md`, `crawl-error-status-table.md`, `round-50.md`) are L1-authored,
not leaf-authored — and even so, they are writes a leaf seat is forbidden to
make; their presence is the L1's own committed-work-in-progress, not a leaf
violation.

---

## Fleet repo — `/home/vgpnk/Projects/shokunin`

`git status --porcelain` output (verbatim):

```
 M .ufo/state/chousa.report-baseline
 M .ufo/state/kagi.report-baseline
 M .ufo/state/kaidoku.report-baseline
 M .ufo/state/kake.report-baseline
 M .ufo/state/kama.report-baseline
 M .ufo/state/kengaku.report-baseline
 M .ufo/state/kumitate.report-baseline
 M .ufo/state/mado.report-baseline
 M .ufo/state/mori.report-baseline
 M .ufo/state/souji.report-baseline
 M .ufo/state/tameshi.report-baseline
 M .ufo/state/tsukuroi.report-baseline
 M .ufo/watchdog.log
?? .omp/mcp.json
?? .ufo/state/kotoba.report-baseline
?? .ufo/state/kotodama.report-baseline
?? .ufo/state/revenger.report-baseline
?? bm.json
?? live.html
?? live_s228.html
?? nama.html
?? s395.txt
?? scripts/hyaku/append-closure.py.bak-20261023T040735Z
?? scripts/hyaku/fleet-commit.sh.bak-20261023T040735Z
?? tf_bavelas.html
?? unblob.log
?? wb2.html
?? write
?? xc.xml
```

### Attribution — is any of this a round-50 kake seat's write?

**Modified `.ufo/state/*.report-baseline` + `.ufo/watchdog.log`:** fleet
orchestrator (hyaku) runtime state. `watchdog.log` tail shows
`launch kake round=50` at 21:49:51 and per-lane launch/complete lines; each
`*.report-baseline` mtime matches that lane's own round run. These are the
**fleet orchestrator's own bookkeeping writes**, not any leaf seat's — and not
at a leaf-writable scope regardless. Not a round-50 leaf violation, but they
are fleet-root-dwelling writes made by the orchestrator, flagged here for
completeness.

**`.omp/mcp.json` (untracked):** REA MCP server registration block (`rea-agents`
stdio, `enabled: false`). Pre-existing host/tooling config, not authored by a
round-50 seat. mtime 18:07 predates the round-50 launch (21:49).

**`scripts/hyaku/*.bak-20261023T040735Z` (×2):** orchestrator backup files dated
2026-10-23. Pre-round-50, orchestrator-owned. Not a leaf write.

**Loose files at fleet root — all mtime 2026-10-24 18:07, ~3.7 h before the
round-50 launch:**

| File | Content sniff | Likely origin |
|------|---------------|---------------|
| `bm.json`, `live.html`, `live_s228.html`, `nama.html`, `tf_bavelas.html`, `wb2.html`, `xc.xml` | Cloudflare "Just a moment…" challenge pages, a "Too many requests" (Perseus) page, a Wayback-Machine bot-block page | A **web-fetch / crawl tool's scratch output** dumped at the fleet root (wrong CWD) — fetch artifacts, not report writes. |
| `unblob.log` | unblob extraction debug log (`/tmp/test-fw.bin`) | A firmware-extraction tool's stray log dropped at fleet root. |
| `write` | `agent://U100N079H334f935b` (25 bytes, no newline) | An agent-URI token written to a file literally named `write` — a misdirected CLI output redirect. |
| `s395.txt` | empty (0 bytes) | Empty scratch file. |

None of these carry a round-50 signature, none lives under
`.ufo/waves/round-50/`, and all predate the wave-1 dispatch. **They are not
attributable to a round-50 kake leaf seat.** They are, however, writes at the
**fleet root** — exactly the "especially anything at the fleet root" category —
left by an earlier crawl/extract/dispatch step running with the fleet repo as
its CWD. They are flagged here as foreign debris the orchestrator may want to
note; this seat does not touch them per the no-delete bound.

---

## Counting-command baselines (rerun by this seat for evidence)

- C1 @ base `9619af6` → `classed 0/3 met=False` (all ids FAIL; S286 fails all 5 signals).
- C1 @ pre-append `33eec7f` → `classed 0/3 met=False` (S273/S274 lesson absent; S286 lesson + live-registry-row + entry absent).
- C2 @ base `9619af6` → `durable 0/1 met=False` (order proof, wave-cite proof, LOG.md wave cite, settlement all FAIL).

Controls behave as required: both predicates are unmet at the do-nothing base.

---

## Conclusion

- **Inside the lane:** no round-50 leaf seat wrote outside its own report file.
  The only round-50 leaf writes are the three `w1/*.md` reports in the
  sanctioned directory. The dirty production files and the round-46/48
  inherited copies are L1/orchestrator-owned or inherited — correctly
  uncommitted and untouched by any leaf.
- **At the fleet root:** a cluster of stray files (crawl HTML dumps, an unblob
  log, a `write` agent-URI token, an empty `s395.txt`, two `.bak` scripts,
  `.omp/mcp.json`) sits uncommitted. None is round-50-attributable; all are
  foreign debris from earlier tooling runs with the fleet repo as CWD. They are
  the only "writes outside a report file at the fleet root," and they are
  flagged, not touched.
- No deletion or modification was performed by this seat.

Report: .ufo/waves/round-50/w1/SentinelWriteScope.md
