# MisrootSweep — round-29 seat-file misroot sweep (wave 2, falsify)

Seat: KakeR29.MisrootSweep. Lane commit attacked: 7697990cbca20291f3b0367b8ff4220e93b38b03.
Scope: read-only. Nothing moved or deleted. No file written except this report.
Tool installs: none (git 2.56.0, GNU find, GNU grep present).

## Question and verdict

**Item attacked:** are round-29 kake seat files misrooted outside the lane repo (written into the
fleet repo `/home/vgpnk/Projects/shokunin`)?

**Verdict: holds for the fleet repo as of the checks below — zero round-29 kake seat files there.**
Limit to state: the answer is repo-local and text-based (paths plus content). It does not certify
other roots (`/fast/scratch`, `~/.omp`), and it cannot see empty directories as files, only as `find`
output.

## Commands and observed output

1. `git -C /home/vgpnk/Projects/shokunin status --porcelain`
   exit 0. 16 entries, **no `??` line at all**:
   ```
    A .scratch/goal-20261022-hyaku-12h.md
    M .ufo/state/{chousa,kagi,kaidoku,kake,kama,kengaku,kumitate,mado,mori,tameshi,tsukuroi}.report-baseline
    A .ufo/state/kotoba.report-baseline
    A .ufo/state/kotodama.report-baseline
    A .ufo/state/revenger.report-baseline
    M .ufo/watchdog.log
    A scripts/hyaku/__pycache__/append-closure.cpython-314.pyc
    A write
   ```
   The three ` A` lines are intent-to-add in the fleet index, not plain untracked files.

2. `git -C ... ls-files --others --exclude-standard` → empty output, exit 0. No untracked files.

3. Content of every changed fleet file, `grep -ci 'KakeR29\|round 29\|round-29'` → `0` for all 16.

4. Content sweep for `KakeR29` outside the lane. A first `grep -rlI 'KakeR29' --exclude-dir=.git
   --exclude-dir=kake-shokunin .` was **killed at the 300 s shared job cap** (`error: interrupted`),
   so its output is not evidence of absence. Replaced by two sweeps that both completed:
   `git grep -lI 'KakeR29' -- . ':(exclude)kake-shokunin'` (exit 0, real 0m0.021s, tracked files)
   and `find .ufo .scratch 'bash: /' -type f -size -2M -print0 | xargs -0 grep -lI 'KakeR29'`
   (exit 0, ignored and scratch trees). Both return the same single path:
   `.ufo/waves/hyaku/PHASE3.md` line 292, the orchestrator dispatch log
   (`Dispatch kake r29 attempt 1 ... base fe1805cf ... L1 KakeR29`). No seat file.

5. `find . -maxdepth 6 \( -name '*KakeR29*' -o -name '*MisrootSweep*' \) -not -path './.git/*'` →
   seven hits, all other lanes and other rounds:
   kaidoku round-18/w2 and round-19/w1, kengaku round-25, kotoba round-48, tameshi round-16,
   mori round-17 and round-20. None for kake round 29.

6. `/home/vgpnk/Projects/shokunin/.ufo/waves/round-29` **exists and is empty**:
   `ls -A ... | wc -l` → `0`; `stat` → `2026-10-21 13:48:43.884227628 -0300`, size 0.
   Empty since creation; git cannot represent it, so it never appears in status.
   Timing: 17h34m before the kake r29 launch recorded at `.ufo/watchdog.log:683`
   (`2026-10-22T07:22:41-03:00 launch kake round=29`), so it is not a kake r29 artifact.
   [INFERENCE] created by an earlier in-flight round-29 lane (kengaku or kotodama r29) whose seat
   ran a lane-relative `mkdir` with cwd at the fleet root; no file was ever written into it.

7. `/home/vgpnk/Projects/shokunin/.ufo/reports/round-29/` holds only `kengaku.md` and
   `kotodama.md`; `kake.md` absent, which is expected (the round report lands last).

## Side findings (operability, not round-29 seat files)

- `write` (fleet root, 25 bytes, no trailing newline, mtime 2026-10-21 19:52) is intent-to-add in
  the fleet index and contains `agent://U100N079H334f935b`. This is a misrouted `write` call: the
  path argument was dropped, the payload became the file name. It predates kake r29 and is not a
  seat file, but it is a misroot-class artifact sitting one `git commit` away from the fleet tree.
  Evidence: `git ls-files --stage -- write` → `100644 e69de29... 0 write`; `git diff --stat` shows
  `write | 1 +`.
- `scripts/hyaku/__pycache__/append-closure.cpython-314.pyc` (10738 bytes) is likewise intent-to-add;
  compiled bytecode staged in the fleet index. Precedent for this class: commit `9c220bf`
  (`souji: correction — untrack files swept in by e20f4fa (git add -A overshoot)`).
- Literal directory tree `bash: /home/vgpnk/Projects/shokunin/souji-shokunin/tests/tools` (four
  empty dirs, mtime 2026-10-18 14:01) at the fleet root. Matched by `.gitignore:1` (`*-shokunin/`),
  so it shows only under `--ignored`; empty, so harmless to content, but it is a surviving
  shell-redirect misroot from an earlier round.
- `.ufo/state/kake.report-baseline` still reads `29 e3b0c442...` (line `29`, empty-blob SHA-256),
  i.e. no kake r29 report recorded yet; consistent with an in-flight round, not a misroot.

## Not verified

- Roots outside the fleet repo (`/fast/scratch/hyaku/...`, `~/.local/state/shokunin-hyaku`).
- Files whose text names round 29 without the string `KakeR29` or `round-29` in the same file
  outside the lane: not exhaustively classified. One sweep,
  `find . -newermt '2026-10-22 07:00' -type f -not -path './.git/*' -not -path './kake-shokunin/*' -print0
  | xargs -0 grep -liI 'kake'`, was **killed at the 300 s job cap** (`error: interrupted`) after
  emitting 20 hits. All hits read so far are sibling-lane documents naming kake in passing, not
  round-29 seat files: `kotoba-shokunin/corpus/knowledge/sibling-overlap-census-round49.md:69` (kake
  row in a sibling census), `kotoba-shokunin/.ufo/waves/round-49/build/MineMistake.md:74` (lane-name
  regex), `kaidoku-shokunin/.ufo/waves/round-25/a3/w1/FleetMisrootPrecheck.md:30,58` (fleet status
  line `M .ufo/state/kake.report-baseline` and "kake r28"), plus fleet `.ufo` files
  (`.ufo/prompts/kake-round-29.md`, `.ufo/waves/hyaku/PHASE3.md`, `.ufo/l0-questions.md`,
  `.ufo/watchdog.log`). Remaining hits in the interrupted list are the same kotoba round-49 wave
  directory and lane-root files; they were sampled, not each read line by line.
- Empty-directory provenance (finding 6) is inferred from mtime and the launch log; no creator
  process or audit trail was recovered.
