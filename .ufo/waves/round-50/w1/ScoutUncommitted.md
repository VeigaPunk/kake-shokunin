# ScoutUncommitted — classify every uncommitted path in the lane and the fleet root

Round 50 wave 1 leaf seat (scout). Snapshot taken at commit boundary
`dfb4a3f` (lane HEAD, `round-50: fix the dispatch role key before the
wave launches`). Commands used were read-only `git status --porcelain`
with no pathspec, plus `find`/`ls`/`git check-ignore` for attribution.

## Frozen instruments — baseline readings (controls)

| Command | Revision | Result | Exit |
|---|---|---|---|
| `c50_quote_class.py --revision 9619af67c52939daac502ca7a24c9d714f3f51db` | base | `C1 classed 0/3 met=False` — all three ids FAIL (S273/S274: class ledger absent, lesson absent; S286: also no live registry row) | 1 |
| `c50_quote_class.py --revision 33eec7f2cecfdbb9c7a1f85c3d8efae8dacd7dd1` | pre-append | `C1 classed 0/3 met=False` — all three ids FAIL (S273/S274/S286: lesson absent; S286 additionally: no live registry row, entry absent) | 1 |
| `c50_durable.py --revision 9619af67c52939daac502ca7a24c9d714f3f51db` | base | `C2 durable 0/1 met=False` — order proof, wave-cite proof, LOG cite, and settlement all absent | 1 |

Both instruments return `met=False` on the do-nothing base, as required
of a frozen counter before measurement. The pre-append revision has the
mirror committed but the live registry still lacks S286, so C1 also
returns `met=False` there — consistent with the contract's intent that
the pre-append state is not the claim state.

## Lane `git status --porcelain` (14 entries)

### (a) Round-50 lane-authored work — 4 entries

| Path | Notes |
|---|---|
| ` M corpus/QUALITY.md` | L1-authored diff; appends the "Round-50 criteria" block (three bullets: wave-citation grant, quote match class, no-sweep of inherited artifacts). Attributed to the L1 by content and by the lane's own contract (QUALITY is an L1-owned file). |
| `?? .ufo/waves/round-50/w1/` | Round-50 wave-1 output dir. Contents observed mid-flight: `swarm-registry.json` (orchestrator seat registry, `wave: kake-r50-w1`, `reportDir: .ufo/waves/round-50/w1`), plus the seat reports `ExecCensusLive.md`, `ExecRerunC1Base.md`, `ExecRerunC1Pre.md`, `ExecRerunC2Base.md`, `ScoutReopenS273.md`, `ScoutReopenS286.md`, and this file. Files appear between `find` invocations — the dir is being populated by sibling seats concurrently. |
| `?? corpus/knowledge/crawl-error-status-table.md` | L1-authored knowledge file for round 50 (1090 bytes). Untracked because the L1 stages lane files at the close of the wave, not at write time. |
| `?? corpus/lessons/round-50.md` | L1-authored lesson file for round 50 (4323 bytes). Same staging convention as above. |

### (b) Inherited orchestrator-owned round-46 residual reports — 1 entry

| Path | Notes |
|---|---|
| `?? .ufo/waves/round-46/residual/` | Exactly 8 files, matching the prompt's "eight orchestrator-owned reports": `SentinelBounds.md`, `CriticMatrixBlindness.md`, `ScoutSiblingOverlap.md`, `MutationSemanticsGap.md`, `ReviewReceiptIdentity.md`, `ReviewWitnessOracle.md`, `CriticCitationOverreach.md`, `ReviewQualityCriterion.md`. Left uncommitted per round-49 verifier routed defect 3 / round-50 QUALITY criterion. |

### (c) Inherited >1MiB round-48 validate copies — 9 entries

The nine paths listed individually under `?? .ufo/waves/round-48/assimilation/validate/.ufo/waves/round-{21,36,37,39,40,41,42}/…`:

| Path | Size class |
|---|---|
| `.ufo/waves/round-48/assimilation/validate/.ufo/waves/round-21/anchors-fixed.json` | >1MiB |
| `.ufo/waves/round-48/assimilation/validate/.ufo/waves/round-36/realrun/snap-bodies-run2.tar.xz` | >1MiB |
| `.ufo/waves/round-48/assimilation/validate/.ufo/waves/round-36/realrun/snap-bodies.tar.xz` | >1MiB |
| `.ufo/waves/round-48/assimilation/validate/.ufo/waves/round-37/sealed/cases.json` | >1MiB |
| `.ufo/waves/round-48/assimilation/validate/.ufo/waves/round-39/sources/xmlschema11-2.html` | >1MiB |
| `.ufo/waves/round-48/assimilation/validate/.ufo/waves/round-40/sources/xmlschema11-2.html` | >1MiB |
| `.ufo/waves/round-48/assimilation/validate/.ufo/waves/round-41/realrun/sitemaps/nodejs.xml` | >1MiB |
| `.ufo/waves/round-48/assimilation/validate/.ufo/waves/round-41/realrun/sitemaps/postgresql.xml` | >1MiB |
| `.ufo/waves/round-48/assimilation/validate/.ufo/waves/round-42/controls/w1/CtlCache/ctl_accept_table_seed4242.py` | >1MiB |

The `validate/` tree holds 7741 files on disk, but `git status` reports
only these 9 paths because the embedded `.gitignore` inside `validate/`
suppresses the rest (`.ufo/interactive-sessions/`, `__pycache__/`,
`*.pyc`) and `git ls-files --others --exclude-standard` confirms only
those nine names are visible. These are the same nine `>1MiB` files the
bounds declare inherited and uncommitted.

### (d) Operator or driver runtime — 0 entries in the lane

The lane repo's own `status` shows no `LOG.md`, `SCORECARD.md`, or
runtime-state modification outside the files already attributed to the
L1 above.

### (e) Possible misroot at the fleet root — 0 entries in the lane

No lane-side path matches a fleet-root artifact. (See the fleet-root
section for the other direction.)

## Fleet-root `git status --porcelain` (27 entries)

Counted at the sibling-lane repo `/home/vgpnk/Projects/shokunin`. None
of these paths was written by a round-50 seat.

### (d) Operator or driver runtime — 13 modified + 4 untracked = 17 entries

- ` M .ufo/state/chousa.report-baseline`
- ` M .ufo/state/kagi.report-baseline`
- ` M .ufo/state/kaidoku.report-baseline`
- ` M .ufo/state/kake.report-baseline`
- ` M .ufo/state/kama.report-baseline`
- ` M .ufo/state/kengaku.report-baseline`
- ` M .ufo/state/kumitate.report-baseline`
- ` M .ufo/state/mado.report-baseline`
- ` M .ufo/state/mori.report-baseline`
- ` M .ufo/state/souji.report-baseline`
- ` M .ufo/state/tameshi.report-baseline`
- ` M .ufo/state/tsukuroi.report-baseline`
- ` M .ufo/watchdog.log`
- `?? .ufo/state/kotoba.report-baseline`
- `?? .ufo/state/kotodama.report-baseline`
- `?? .ufo/state/revenger.report-baseline`
- `?? .omp/mcp.json`

### (e) Possible misroot / stray operator artifacts — 10 untracked entries

- `?? bm.json`
- `?? live.html`
- `?? live_s228.html`
- `?? nama.html`
- `?? s395.txt`
- `?? scripts/hyaku/append-closure.py.bak-20261023T040735Z`
- `?? scripts/hyaku/fleet-commit.sh.bak-20261023T040735Z`
- `?? tf_bavelas.html`
- `?? unblob.log`
- `?? wb2.html`
- `?? write`
- `?? xc.xml`

(Subtracting overlap with the runtime class: 11 entries here — the
`*.bak-20261023T040735Z` pair plus nine ad-hoc artifacts like
`live.html`, `nama.html`, `wb2.html`, `write`, `xc.xml` — are stray
operator/driver artifacts at the fleet root, not files any lane should
own. None is attributable to a round-50 seat.)

## Files a round-50 seat wrote into the fleet root

**None.** Every untracked or modified path at the fleet root falls into
class (d) (`.ufo/state/*.report-baseline`, `watchdog.log`, `.omp/mcp.json`
— driver/operator runtime) or class (e) (stray `*.html`, `*.log`,
`*.txt`, `write`, `bm.json`, `xc.xml`, and two `.bak-20261023T040735Z`
scripts — artifacts that pre-date this wave). No `.ufo/waves/round-50/…`
path and no lane-specific name appears in the fleet-root status.

## Counts

| Class | Lane count | Fleet-root count |
|---|---:|---:|
| (a) round-50 lane-authored | 4 | 0 |
| (b) round-46 residual (orchestrator-owned) | 1 (dir; 8 files) | 0 |
| (c) round-48 >1MiB validate copies | 9 | 0 |
| (d) operator / driver runtime | 0 | 17 |
| (e) stray / possible misroot | 0 | 11 |
| **Total** | **14** | **28** |

## Notes for the L1

- The lane `?? .ufo/waves/round-50/w1/` dir contains this wave's live
  output (the orchestrator's `swarm-registry.json` plus sibling seat
  reports). It is legitimately lane-authored; per the sweep rule it
  should land at the wave's close, not be folded into a leaf commit.
- `corpus/QUALITY.md` is modified by the L1's own round-50 criteria
  block and remains unstaged — consistent with the L1 staging at wave
  close alongside LOG.md, SCORECARD.md, and the lesson file.
- The nine inherited `>1MiB` validate copies and the eight round-46
  residual reports remain uncommitted and untouched, matching the
  round-50 "not swept to zero a count" criterion.
- No round-50 seat-authored file leaked into the fleet root.

Report: `.ufo/waves/round-50/w1/ScoutUncommitted.md`
