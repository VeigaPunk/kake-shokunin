# ReviewContainment — kake round 37, wave 2 (falsify), leaf reviewer

Attacked: did any round-37 seat write outside its sandbox or report path, and did any file land at the fleet root (a misroot)? I also checked the L1's containment record (`corpus/lessons/round-37.md:19,158`; LOG round 37). Axis: operability. No installs. Writes: this report, plus `/fast/scratch/hyaku/kake-r37w2/ReviewContainment/{scan.py,hits.tsv}`.
Method: read-only filesystem checks and git, plus a scan of every seat transcript under `~/.omp/agent/sessions/-Projects-shokunin/2026-10-23T00-54-50-959Z_01a16640-e34f-76e4-8a3b-4d245a8bb241/KakeR37/` (call this T). I scanned twice: first 57 transcripts, then all 74 once more wave-2 seats had started. I also scanned `../KakeR37.jsonl`, the L1's own transcript. I did not use LSP, because no code changed: this is a filesystem and transcript audit. I did not open `/fast/scratch/hyaku/kake-r37/`.

## Commands (all exit 0)
- `git -C /home/vgpnk/Projects/shokunin status --porcelain` lists 27 entries. The only kake entry is ` M .ufo/state/kake.report-baseline`, which changed `25 e3b0…` to `37 e3b0…` at 02:46:03Z. That is 1 s before `.ufo/watchdog.log` logs `launch kake round=37 pgid=3604149`, so the harness wrote it, not a seat.
- `find /home/vgpnk/Projects/shokunin -maxdepth 6 -newermt '2026-10-23 02:46:00Z'` (lane dirs excluded) finds only harness files for kake: `.ufo/prompts/kake-round-37.md` and `.ufo/state/kake.report-baseline`.
- `git -C kake-shokunin status --porcelain` shows only the L1's wave-2 files (`make_w2_spec.py`, `w2-*.json`, `w2/`). No stray lane file.
- `git ls-tree -r --name-only 79d3c780 -- .ufo/waves/round-37/` agrees with the L1's copy claims. These pairs are byte-identical (lane file = sandbox file, sha256 prefix): `scripts/robots_audit.py` = `kake-r37w1/ExecRobotsTool/robots_audit.py` (5eb767ec68a64914); `robots_audit_selftest.py` (0c5b1131); `criteria/{control_tree,polarity,bare_id}_check.py` (b592270e, 7ebc5d67, 8b8fe47d); `junk_control_receipt_check.py` (be94c6c6). `corpus/knowledge/robots-txt-rules.md` differs from the scribe draft (bdb58cea vs 07c20e6b): the L1 edited it, which is outside this axis.
- `timeout 300 python3 -B scan.py T > hits.tsv`. It checks every bash, write and edit call for: `/tmp` writes, the private directory, lane git mutations, `jj`, a fleet-root working directory, write targets outside the seat's sandbox, and `agent://` targets. I then resolved each patch target from its tool result.
- `find /tmp -maxdepth 1 -newermt '2026-10-23 02:46:00Z'`; I matched residue to seats with `sha256sum` and transcript grep.

## Out-of-bounds actions found (each points to a transcript in T)
| # | Seat (wave) | Action, time (Z) | Disclosed? | Residue now |
|---|---|---|---|---|
| 1 | ExecRobotsTool (w1) | `test -e /fast/scratch/hyaku/kake-r37/` (a stat of the private directory), 03:38:25 | yes, `w1/ExecRobotsTool.md:3-5`; lesson `:19` | none |
| 2 | ReviewRoutedDisposition (w1) | `jq … > /tmp/kake-w1-items.txt`, then moved it into its sandbox, 03:27:34 | yes, `w1/ReviewRoutedDisposition.md:4-5` | none (file absent) |
| 3 | CtlC1NoReader (control) | harness temp dir in `/tmp`, removed on exit | yes, `ctl/CtlC1NoReader.md:26` | none seen |
| 4 | SimplifierCounters (w1) | `git show 4b089da:.ufo/waves/round-36/sealed_count.py > /tmp/r36sealed.py`, 03:28:35 | **no** (`w1/SimplifierCounters.md:3-5` claims bounds only) | `/tmp/r36sealed.py`, sha256 88ec5914…ff8e, a copy of the public round-36 counter |
| 5 | ScoutPriorTools (w1) | the selftest and CLI loops redirect output to `/tmp/$s.{out,err}` and `/tmp/$t.{h,n,x}.{out,err}`, 03:24:31 | **no** | 30 files, `/tmp/{canonical_audit,base_path_audit,link_preview_audit,source_recheck}.*` and `/tmp/*_selftest.{out,err}`, written 03:24:31–03:24:38 |
| 6 | ReviewC2Counter (w1) | its "writes-tmp" probe tool writes `/tmp/kake-probe-junk`; the run ends with `rm -f /tmp/kake-probe-junk` | partial: `w1/ReviewC2Counter.md:12` names the probe but not a host write | none. [INFERENCE] The host write happened only if the run_case path is unjailed |
| 7 | ConnectorSiblings, CtlC1NoReader, ExecCriteriaRepairs, ExecRecheckHardening, ReviewC2Counter, ReviewRoutedDisposition | all replied to `agent://MadoR24` (another lane's L1) between 03:33:24 and 03:33:36. The bounds allow messages to `agent://KakeR37` only | **no** | none. The trigger was MadoR24's broadcast `x` (`"broadcast":true`). The replies carried status only; no key or case data |
| 8 | ReviewSourcesRows (w2) | `/tmp/ReviewSourcesRows-census.txt`, 03:44:31 | **no** (`w2/ReviewSourcesRows.md`, no `/tmp`) | present |
| 9 | ReviewKnowledgeEntry (w2) | `git show 79d3c780:SCORECARD.md > /tmp/kr37_sc.md`, 03:44:42 | **no** (`w2/ReviewKnowledgeEntry.md`) | present, sha256 27eb050a… = SCORECARD@79d3c78 |
| 10 | ReopenGateS097 (w2) | `curl -D /tmp/s097.hdr -o /tmp/s097.html` (robotstxt.org), 03:44:46; reused through 03:48 | **no** (`w2/ReopenGateS097.md`) | present |
| 11 | ReviewLessonNumbers (w2) | `git show 79d3c780:SCORECARD.md > /tmp/sc37.md`, then `mv` into its sandbox | **no** (`w2/ReviewLessonNumbers.md`) | none (file absent) |

Not breaches (checked):
- MutRefPass ran `sealed_count.py --root <lane> --key-file …/private/cases.json`. The counter only runs `git show` against the root and keeps its scratch in `tempfile.TemporaryDirectory`, with `TMPDIR` set to the seat's sandbox (`sealed_count.py:79-80,185-209`). Key access was by design (lesson `:158`).
- The `git merge-base` and `rev-parse` calls by RerunC1Sealed are read-only.
- ExecRecheckHardening's `open(p,'w')` targeted its own report.
- Twelve seats ran with the fleet root as their working directory, and every write in those calls used an absolute sandbox path. Their only relative write ops were `mkdir -p "$s/tools"` and `rm -r "$s/dump"`, with `$s` set to a sandbox path.
- The L1 transcript (138 tool calls) has no `/tmp` write, no write to the fleet root, and no message to another lane.
- The four dead critics made no flagged call.
- No seat ran a mutating git command in the lane, any `jj` command, or `pacman`.

## Misroot list
- **Landed kake misroots: 0.** These paths are all absent: `/home/vgpnk/Projects/shokunin/{fast,kake-r37w1}` and `kake-shokunin/province-r37.md`.
- **Attempted kake misroots: 3.** In each case a relative path in an edit call would have resolved against the fleet root. The edit tool rejected all three with "File not found", and each seat then rewrote the file at its sandbox path:
  - ScribeProvinceStep: `kake-shokunin/province-r37.md` (lane root)
  - ScribeKnowledgeEntry: `fast/scratch/hyaku/kake-r37w1/ScribeKnowledgeEntry/robots-txt-rules.md`
  - ScribeSourcesRows: `kake-r37w1/ScribeSourcesRows/sources-rows.md`
- **Non-kake, routed to the chousa lane:** `/home/vgpnk/Projects/shokunin/.ufo/waves/round-30/falsify/ConnectorKagiPin.md` was a copy of `chousa-shokunin/.ufo/waves/round-30/falsify/ConnectorKagiPin.md`. It appeared at 03:42:50Z (directory mtime) and was gone by my later `cmp` (exit 2, no such file).

## Verdicts
- "No lane file written except this report", stated in the wave-1 and control reports: **holds**. Every write or edit to the lane targeted the seat's own report.
- "No fleet-root misroot by any round-37 seat": **holds** for landed files. Three attempts failed harmlessly, and the chousa round-30 file is not a kake file.
- L1 copy claims against `ls-tree` at 79d3c780: **hold** for every copied tool and checker (byte-identical, listed above).
- Containment record in `corpus/lessons/round-37.md:19` and LOG round 37 (`LOG.md:1508-1524`): **overstated by omission**. It records only action 1. Actions 2 and 3 were disclosed by their seats but never integrated. Actions 4, 5 and 7 went undisclosed in wave 1, and action 6 only partly. Round 37's LOG also has no misroot-sweep line, which round 28 had (`LOG.md:1237`).
- Wave-2 seats 8–11 filed reports with undisclosed `/tmp` writes: **wrong** as filed. Their reports need a disclosure line.
- ReviewSourcesRows also ran the fleet script `./scripts/sources-census.sh validate` from the fleet root. The script writes only to stdout (`scripts/sources-census.sh:7`), so the only write was its `/tmp` redirect, action 8.

## Residual risk and gaps
- I cannot attribute `/tmp` writes made by child processes that do not name `/tmp` in the command line, for example `tempfile` calls with `TMPDIR` unset. The scan sees only what appears in tool-call arguments.
- Wave-2 seats still running after this report may add actions that are not listed here.
- I did not inspect `/fast/scratch/hyaku/kake-r37/`, as the bounds require. So I cannot verify the control seats' claim that they never opened `private/`, apart from their transcripts showing no read of that path.
- Leftover `/tmp` files are not removed; cleaning them up is not my job.
