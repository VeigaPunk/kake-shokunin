# SentinelMisroot

ATTACKS: round hygiene after wave 1, three surfaces. (a) **FLEET ROOT** — every `git status
--porcelain -uall` entry plus every gitignored root (`.tower/`, `.ufo/state/`, `.ufo/waves/*/*-scratch/`,
`*-shokunin/`) grepped for kake round-60 tokens (`S427|S428|S429|c60_gate_status|c60_guard_cases|
c60_quote_truth|append_guard`), and every fleet-root file touched after round open (00:56Z-03) listed.
(b) **SCRATCH** — every dir under `/fast/scratch/hyaku/kake-r60` (size, mtime, clone kind: `.git`
file + `objects/info/alternates` = `--shared`), `/fast/scratch/hyaku` itself, `/fast/scratch`, `/tmp`
(all files in the w1 window 00:56..02:40 grepped for kake tokens). (c) **LANE** — w1 tree shape
(paths outside `<Seat>.md` / `<Seat>.files/`), `97cdc12..1ea3059` diff outside `.ufo/waves/round-60`,
`w1-results.json` ↔ report bijection, declared `files_changed` vs seat prefix, symlinks, committed
`.pyc`, secrets patterns, and all lane writes after w2 dispatch (02:40) outside `w2/`. All findings
below are from commands I ran; raw output: `w2/SentinelMisroot.files/misroot-audit.txt`.

## FLEET ROOT:

Clean for kake round 60. `git -C /home/vgpnk/Projects/shokunin status --porcelain -uall` = **0** at
02:44 and again at 02:55. No untracked file anywhere at the fleet root, so no misrooted seat file
exists in the tracked/untracked space. The ignored roots are also clean for kake: `grep -rIlE
'S42[789]|c60_(gate_status|guard_cases|quote_truth)|append_guard' .tower/quarantine .ufo/state` = 0
hits; `.ufo/state/kake.{mission,out,round,report-baseline}` are dispatcher state (00:56), not seat
output; `.ufo/prompts/kake-round-60.md` is the prompt.

Two stray events of *this class* landed at the fleet root inside the round window, neither kake, both
already quarantined by `.tower` (so also 0 in `git status`, `.tower/` being gitignored):

- `.tower/quarantine/fleet-root-strays-20261027T0225/{e,o}` — written 01:42 (round open 00:56),
  quarantined 01:58. `e` is 0 bytes, `o` is 115 bytes of a `xmodmap`-style keysym dump
  (`keysym: eacute (0x00e9)`). A bare `> o 2> e` at the fleet root, content unrelated to kake.
- `.tower/quarantine/fleet-root-strays-20261027T0600/kengaku-shokukin/.ufo/waves/round-46/w1/
  R46CritC1Freeze.md` — a mis-rooted **kengaku** wave-46 seat dir (note the misspelling
  `shokukin`), quarantined 02:28, i.e. during round-60 w1. Not kake.
- (Adjacent, just before open: `...T0020/.ufo/waves/round-51/w2/T51W2Read14.md`, quarantined 00:16.)

The audit method itself has a hole: because `.tower/`, `.ufo/state/*` and `.ufo/waves/*/*-scratch/`
are gitignored, a misrooted file dropped in any of them is invisible to `git status --porcelain`,
which is the detector the wave spec names. A fleet-root filesystem grep is the only working form.

## SCRATCH:

- Seat root `/fast/scratch/hyaku/kake-r60` holds **32 dirs, no files**: `L1` plus 31 w2 seat dirs.
  **No w1 kake scratch dir survived** — every dir mtime is ≥02:33 (L1) / ≥02:40 (w2), so the w1
  `trap 'rm -rf -- "$S"' EXIT` held and nothing w1 is left for me to report.
- Clone kind is compliant: `ReviewerC1Rows/lane/.git` is 3 MB with `objects/info/alternates` present
  (a `.git` file, not a dir) while the checkout is 283 MB of lane tree — i.e. `git clone --shared`.
  Same shape under `MutC1Counter/clone`, `ReviewerLedgerProse/clone`.
- Volume is the weak point: **9.5 GB** at 02:55 (`du -sm`), growing during the wave, ~10 seats
  carrying a full 283–1268 MB lane worktree each (SentinelGuard 1268, SentinelC1Exec 1107, L1 865,
  ReviewerC1Rows 848). Disk is 29 % used / 572 GB free (`df -h /fast`) — no action needed, but a
  seat that only reads counters still pays 283 MB.
- One write outside the mandated scratch root: `/fast/scratch/hyaku/kake-r27` — empty dir, mtime
  **2026-10-27 02:42**, inside the w2 window. Wrong round in the path (`r27`), unattributable from
  the filesystem. I did not touch it.
- `/tmp`: no kake round-60 content. Every `/tmp` file written in the w1 window (80 files, e.g.
  `ours.txt`/`theirs.txt` 01:58, `mv.txt`, `gl2.2`, `pub-list` 2.3 MB at 02:00) greps 0 for
  `S427|S428|S429|c60_*|append_guard|kake`; the `/tmp` hits that do exist are other lanes' work
  (`tameshi-r17-*`, `pcp_*`, `chousa` audio `frontier-pipewire` lists). `/tmp/e` (0 bytes, 02:31) is
  a bare stderr redirect, under the 50 MB rule and not cited by anyone.
- Pre-existing, not attributable to w1 (reported, not deleted): `chousa-r55` 1647 MB (01:21),
  `run-receipt-z1d4iklc` 400 MB (live, 02:43), `hyaku-run8`, `hyaku-run9`, `t52w2fix14_{skill_cand0.md,
  mar_cand0.sh,ledger.md}`, `/tmp/closure-r58-kake.json` (round 58), `kake-r27` above.

## LANE:

Read-only: lane HEAD stayed `45f46fb2ec45eb02edce3ba9971db2272428b1dc`; I ran no git/jj mutation.

- **w1 tree shape is clean.** The only non-seat path under `w1/` is the dispatcher's
  `w1/swarm-registry.json`; all 44 other top-level entries are `<Seat>.md` or `<Seat>.files/`
  (`git ls-tree -r --name-only HEAD .ufo/waves/round-60/w1/ | grep -vE '^...w1/[A-Za-z0-9_-]+(\.md|\.files/)'`
  → 1 line, the registry). 0 symlinks under `w1/`.
- **No tracked lane write outside the wave dir.** `git diff --name-status 97cdc12 1ea3059 --
  . ':!.ufo/waves/round-60' | wc -l` = **0**; the build commit's lane changes (`SKILL.md`,
  `scripts/append_guard.py`, `corpus/...`) are 8b33fd2 (L1 integration), not seat writes.
- **Results ↔ reports: exact 44/44 bijection**, no duplicates, no result without a report, no report
  without a result (`w1-results.json` `seats: 44`). No dead seats. Committed w1 tree carries 0 `.pyc`.
- **Secrets: 0** (`grep -rIlE 'sk-[A-Za-z0-9]{20}|ghp_[A-Za-z0-9]{20}|op://|AKIA[0-9A-Z]{16}'` over
  `w1/` + `w2/`).
- **Defect: a w2 seat wrote bytecode at the lane round-60 root**, outside its report and `.files/`.
  `.ufo/waves/round-60/__pycache__/c60_gate_status.cpython-314.pyc`, 76658 bytes,
  mtime **02:42:50** — after `w2.ready.dispatched` (02:41). A process with cwd in
  `.ufo/waves/round-60` imported `c60_gate_status` without `-B`. It is invisible to
  `git status --porcelain` (lane `.gitignore` lines 2–3: `__pycache__/`, `*.pyc`), so the wave's own
  lane check cannot see it, and it stays in the worktree past the wave. The three w1 `.files/`
  pycache dirs (`ExecC1Counter.files/`, `ExecC2Counter.files/`, `ExecGuardTool.files/`) are the same
  class, but sit inside their own `.files/`; the round-60-root one does not.
- **Defect: three w1 results declare writes with fleet-root-relative paths**, i.e. those seats were
  cwd'd at the fleet root, not the lane: `results[5] ExecC1Data53`, `results[12] ExecGuardTool2`,
  `results[29] ExecSourceLive` each list `files_changed` entries beginning `kake-shokunin/.ufo/...`
  (full lists in the evidence file), and `w1/EntryUserTriggered.md:108`/`:110` write entry/report
  paths the same way. Every such path still resolved inside the lane, so nothing escaped — the
  failure is the guard, not the outcome: with a bare `> file` these three would have dropped strays
  at the fleet root exactly like the `.tower/quarantine` entries above.
- `w2/swarm-registry.json` (mode 0600, 02:40) and the four `w2-{dispatch,spec}.json` /
  `w2.ready*` / `w2-validator.err` files are dispatcher-owned, not seat writes; `git status` shows
  them as the only untracked lane entries (`w2.ready`, `w2.ready.dispatched`, `w2/`).

## FINDINGS:

| sev | target file:line | issue | evidence command | fix |
|---|---|---|---|---|
| medium | `.ufo/waves/round-60/__pycache__/c60_gate_status.cpython-314.pyc` (untracked, ignored) | w2 seat imported the counter from the round dir without `-B`, writing bytecode in the lane outside its report/`.files/`; `.gitignore` hides it from the wave's lane check | `stat -c '%n %y' .ufo/waves/round-60/__pycache__/c60_gate_status.cpython-314.pyc` → mtime 02:42:50; `git status --porcelain -uall` → does not list it | L1: `rm -rf .ufo/waves/round-60/__pycache__` before the wave commit; w2 spec repeats `python3 -B` **and** `PYTHONDONTWRITEBYTECODE=1`; round-hygiene step greps `--ignored` too |
| medium | `w1-results.json` results[5], [12], [29]; `w1/EntryUserTriggered.md:108,110` | seats ran with cwd = fleet root (paths declared `kake-shokunin/...`); the misroot failure mode of the quarantine strays, not yet a write outside the lane | `python3 -c "import json;r=json.load(open('.ufo/waves/round-60/w1-results.json'))['results'];[print(i,x['name']) for i,x in enumerate(r) if 'kake-shokunin/.ufo' in (x.get('output') or '')]"`; `sed -n '108,110p' .ufo/waves/round-60/w1/EntryUserTriggered.md` | seat spec: assert `git -C . rev-parse --show-toplevel` equals the lane before the first write (the host guard already demands this for fixtures); validator rejects `files_changed` not lane-relative |
| medium | `.tower/quarantine/fleet-root-strays-*/` (fleet root) | the round-hygiene detector (`git status --porcelain` at the fleet root) is blind to every gitignored root; strays landed there twice in the round window (01:42 keysym dump `e`/`o`; kengaku round-46 seat dir at 02:28) and were only caught by `.tower`, not by the check | `ls -la .tower/quarantine/fleet-root-strays-20261027T0225/ .tower/quarantine/fleet-root-strays-20261027T0600/`; `cat ...T0225/SHA256SUMS` | round-hygiene step: also `find` the fleet root for files newer than round open (excluding lane repos) and grep ignored roots for wave tokens; keep the `.tower` quarantine list in the round record |
| low | `/fast/scratch/hyaku/kake-r27` | empty dir created 02:42 in the w2 window outside the mandated `kake-r60/<seat>` root (wrong round in path); unattributable | `find /fast/scratch/hyaku/kake-r27 -printf '%TY-%Tm-%Td %TH:%TM %y %s %p\n'` → `2026-10-27 02:42 d 6` | spec line is already explicit; validator asserts each seat's scratch dir under `kake-r60/<seat>` and no new sibling dir under `/fast/scratch/hyaku` |
| low | `.ufo/waves/round-60/w1-results.json` (schema) | results carry `{name, agent, note, output}` only: no status field and `note` empty for all 44, so "dead seats are recorded from `w1-results.json`" (contract R59-D5) has no field to record a death in; today only a missing report would show it, and there is none | `python3 -c "import json;r=json.load(open('.ufo/waves/round-60/w1-results.json'))['results'];print(sorted(r[0]),sum(1 for x in r if not x.get('note')))"` → `['agent','name','note','output'] 44` | record the run status (or a per-seat `ok/abandoned`) in `w1-results.json`; otherwise drop the claim that results record dead seats |
| low | `/fast/scratch/hyaku/kake-r60` | 9.5 GB live, ~10 full 283 MB+ worktrees even for seats that only read counters; disk fine (572 GB free) | `du -sm /fast/scratch/hyaku/kake-r60/*/ \| sort -rn \| head -6` | seat spec: clone with `--shared --no-checkout` + sparse checkout of the round dir, or read the lane read-only when the counter accepts `--root` on a clone |

Not run (not claimed): the three round-60 counters and the build's entries; sibling lane *repos* were
only mtime-scanned at depth 3 (166 files, all inside those lanes' own active rounds) and no
attribution is possible from that scan.

VERDICT: No misrooted kake round-60 file exists at the fleet root and no w1 seat wrote a tracked lane file outside `.ufo/waves/round-60/` (44/44 reports, 0 diffs outside the wave dir, 0 secrets) — but the round-hygiene detectors are leaky and one w2 seat has already written bytecode outside its seat dir (`round-60/__pycache__`, ignored, 02:42), while three w1 seats ran cwd'd at the fleet root and one stray scratch dir (`kake-r27`) appeared during w2.
