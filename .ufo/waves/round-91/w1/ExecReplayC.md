# ExecReplayC — R90-C replay of `run_controls.sh` at the tip

VERDICT: R90-C holds for the claimed replay (`ONLY=c1` on a clean scratch clone at `f4fff130a52ae6de49af5de7d568d2ee320ebfb0`: `controls ok 9/9`, exit 0); `ONLY=all` is red at the same tip (`controls ok 11/14`, exit 1) because the C2 reader in `run_controls.sh` is wrong — routed to L1, script not edited.

Seat: ExecReplayC (executor, leaf). Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`. Tip replayed: `f4fff130a52ae6de49af5de7d568d2ee320ebfb0` (lane `master`, HEAD at my start, 2026-11-04T23:25:11Z). Script sha256 `00e339b8266eae324f7d5d56a3deabbaa1df1b7488d72944bad8d2dc3248c040` (matches freeze.md), `inherited/baseclean.out` sha256 `4046c204…f00f` (matches).

## 1. Replay (what was run, exit codes)

Scratch root `/fast/scratch/hyaku/kake-r91/ExecReplayC/` (deleted before yield; receipts copied under `w1/ExecReplayC/`).

| # | Command (LANE = scratch clone) | Exit | Last line | Receipt |
|---|---|---|---|---|
| 1 | `git clone -q --shared LANE $S/clone`; toplevel = `$S/clone` ✔; `git -C $S/clone checkout -q --detach f4fff130…` | 0 | — | `clone-status-after-checkout.txt` (0 lines) |
| 2 | `HYAKU_SCRATCH=$S/hs-c1 LANE=$S/clone ONLY=c1 bash $S/clone/.ufo/waves/round-90/controls/run_controls.sh` | 0 | `controls ok 9/9` | `replay-c1.out`, `replay-c1.rc` |
| 3 | same, `ONLY=all` | 1 | `controls ok 11/14`; `MISMATCH c2-admit / c2-hashtable / c2-nametable want=met=false got=met=true` | `replay-all.out`, `replay-all.rc`, `all-final.out` |
| 4 | Mirror of the counter's item C environment (`cwd=clone`, `LANE=clone`, `ONLY=c1`, `HYAKU_SCRATCH=<work>/scr`, c91 `item_c`) | 0 | `controls ok 9/9` | `item-c-mirror-c1.out/.err` |
| 5 | Diagnostic copy (see §3), `ONLY=all` | 0 | `controls ok 14/14` | `diag/replay-all-diag.out`, `diag-reader-outputs/` |
| 6 | Diagnostic copy, `ONLY=c1` | 0 | `controls ok 9/9` | `diag/replay-c1-diag.out`, `diag-c1-outputs/` |

Item-C predicates checked on the tip bytes (code of `c91_defects.py` `item_c`, sha256 `5239c7f8…629b`): no line copies `"$LANE"/baseclean.out` (lines with `baseclean`: 7, 8, 42, 66, 69, 74); literal relocated path appears 2× (lines 7 comment, 42 assignment); `LANE=${LANE:-` present (line 14); replay exit 0; last line `controls ok 9/9`, K == N = 9 ≥ 9. The counter's item C would read **closed** at this tip on its code. See F4 for the stricter wording it documents.

Clone and lane status: `git -C $S/clone status --porcelain` → 0 lines after every run, and after the attack resets. The replays used `LANE=$S/clone`, so they cannot write into the real lane. `git -C LANE status --porcelain --ignored` before the first run and after the replays differ only by other seats' new untracked entries (`w1/ReviewReuse/`, `corpus/lessons/round-91.md`, `scripts/stored_reuse.py`, `w1/ExecReuseTool*`) and by my own `w1/ExecReplayC*` receipts (`lane-status-before.txt`, `lane-status-final.txt`). The replay itself wrote nothing into LANE. Caveat: `git -C LANE status` may refresh `.git/index` stat data; `find LANE -newer marker` listed only `LANE/.git` for that reason.

## 2. Attacks on the controls (on the clone's working tree; restored by `git checkout -- .` + `git clean -fdq` between cases; status 0 after each)

Each row ran `ONLY=c1 bash run_controls.sh` against the clone. Counter-side attacks replaced `.ufo/waves/round-90/c90_defects.py` in the clone.

| Attack | Result | Caught? | Receipt |
|---|---|---|---|
| A1 counter replaced by `print("met=true")` | `controls ok 1/9`, exit 1; 8 MISMATCH (do-nothing, D1a–D3b) | yes, by do-nothing and fixtures | `attacks/A1-echo-true.out` |
| A2 counter replaced by `print("met=false")`, exit 1 | `controls ok 8/9`, exit 1; MISMATCH `c1-positive` | yes, by positive only | `attacks/A2-echo-false.out` |
| A3 relocated file symlinked to the absent lane-root path `$clone/baseclean.out` (the forbidden copy) | `controls ok 8/9`, exit 1; MISMATCH `c1-positive` | yes, by positive only | `attacks/A3-symlink-absent-root-copy.out` |
| A3b relocated file symlinked to a same-bytes copy outside the tree | `controls ok 9/9`, exit 0 | **no** (F6) | `attacks/A3b-symlink-same-bytes-outside.out` |
| A3c relocated file symlinked to junk outside the tree | `controls ok 8/9`, exit 1; MISMATCH `c1-positive` | yes, by positive only | `attacks/A3c-symlink-junk.out` |
| A4 `SCORECARD.md` symlinked out of the clone to a file with a fabricated correction line | `controls ok 9/9`, exit 0 | not a hole: the counter reads `SCORECARD.md`/`LOG.md` with `git show <rev>:<path>` (committed bytes, `item_d2`), so the working-tree symlink is invisible | `attacks/A4-scorecard-symlink-out.out` |
| A5 counter prints the true verdict, then a traceback, exit 3 | `controls ok 9/9`, exit 0 | **no** (F5) | `attacks/A5-counter-exit3-after-verdict.out` |

Scope of the attacks: the script reads the working tree of its LANE root, so working-tree mutations exercise the same script logic a committed mutation would. The counter's item C replays a fresh clone of the committed revision and cannot see working-tree edits, so A3b and A4 are not reachable through item C unless the symlink is committed; I did not commit anything.

## 3. Findings (defects in the controls, the counter and the round's routed list)

**F1 — `run_controls.sh` C2 reader is wrong; `ONLY=all` is red at the tip (routed to L1; not edited).** Line 26: `reading() { grep -oE 'met=(true|false)' "$1" | tail -1; }` takes the last `met=` token in the whole output. The counter's JSON dump of per-file candidate output (`"lines": {… "cache_key_conformance met=true" …}`) comes after its summary line, so the reader returns the candidate's echo, not the counter's verdict. Evidence: the summary line of `out-admit`, `out-hashtable`, `out-nametable` is `C2v90 … positives=4/4 negatives_refused=0/57 false_admits=57 … met=false` (diag run), while their last `met=` token is `met=true`. The same shape is in the round-90 receipt `.ufo/waves/round-90/controls/ctl-c2.txt`: each of the `admit`, `hashtable`, `nametable` sections contains 61 `cache_key_conformance met=true` tokens and its summary reads `met=false`. The counter is right; the reader is wrong. With a reader that takes `met=` from the summary line only (`grep -E '^C[12]v' | tail -1 | grep -oE 'met=(true|false)$'`), the same tip gives `controls ok 14/14`, exit 0 (diag copy). `ONLY=c1` is unaffected (its outputs carry no such dump; 9/9 both ways). This means R90-C is closed for the C1 replay the counter measures, but the script's own header claim ("every control is ASSERTED") is false for `ONLY=all`. Fix is an L1 integration decision.

**F2 — label collision: `out-do-nothing.txt` is written by both the C1 and the C2 do-nothing control.** The C2 section overwrites the C1 output within the same `ONLY=all` run. Pass/fail is unaffected (each reading is taken right after its own run), but the C1 evidence is lost in a full run. Seen in `diag-reader-outputs/out-do-nothing.txt`, which holds the C2 summary.

**F3 — shared scratch and destructive cleanup.** `SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kake-r91/replay` is not per-seat when `HYAKU_SCRATCH` is unset, and the script runs `rm -rf "$SCR"` at start (line 20) and end (line 169). Two seats replaying without `HYAKU_SCRATCH` will delete each other's directory. The counter sets `HYAKU_SCRATCH` (item C), so the counter path is safe. I did not run the script without the variable (that would have written outside my scratch root). The same `rm -rf` at the end deletes every per-control output, so a failing control cannot be inspected after the run; I had to make a diagnostic copy that keeps `SCR` (F1 evidence).

**F4 — counter item C (frozen, `c91_defects.py`) is weaker than its own wording.** The docstring (lines 25–27) says the script "names the relocated file on every line that mentions `baseclean.out`, and never the bare lane-root copy". The code does not implement that: it checks only the regex `"$LANE"/baseclean.out` / `${LANE}/baseclean.out` / `$LANE/baseclean.out` and `count(INHERITED) >= 2`. At the tip, lines 8, 66, 69 and 74 mention `baseclean.out` without the relocated path (line 66 and 74 use `$D/baseclean.out`, a fixture file, and lines 8 and 69 are comments). The count≥2 is met by a comment (line 7) and the assignment (line 42), not by a copy. Under the docstring's literal reading the tip script does not satisfy item C; under the code it does. This is a counter ambiguity for L1, not a script defect. Routed.

**F5 — the controls ignore the counter's exit status.** `reading()` never looks at `$?`. A counter that prints the right verdict and then a traceback with exit 3 passes every control (A5: `controls ok 9/9`, exit 0). The QUALITY bar (`corpus/QUALITY.md` line 161, round-24 row) says a nonzero exit with a traceback is a crash, not a successful rejection. Low severity for this replay, but the controls do not enforce the bar they cite.

**F6 — the controls do not assert a clean source tree.** The fixtures copy `"$LANE/$INHERITED"` and `"$R90/frozen"` from the working tree, so a dirty replay root passes (A3b: 9/9 with the relocated path a symlink to a same-bytes file outside the repo). Item C uses a fresh committed clone, so the counter cannot trigger this; a manual replay on a dirty lane can. Low.

**F7 — counter item C's forbidden-copy regex is evadable (frozen instrument; finding only).** Probed on the exact regex: caught `cp "$LANE/baseclean.out"`; **missed** `"$LANE/./baseclean.out"`, `"${LANE:-.}/baseclean.out"`, `"${LANE}"/baseclean.out`, `"$LANE"/"baseclean.out"`, `ROOT_COPY=baseclean.out; cp "$LANE/$ROOT_COPY"`, `"$LANE/../<dir>/baseclean.out"`. At the tip this is backstopped by the replay: the revision has no tracked lane-root `baseclean.out`, so a copy of it fails and the positive control fails (A3 shows the positive catching the absent-copy case). The regex is not the guard; the replay is. Probe output: `regex-probe.txt` in `w1/ExecReplayC/` (exact frozen regex, run inline).

**F8 — counter-side weakness observed while reading the instrument (frozen; finding only).** The round-90 receipts the new controls rely on show the same reader pattern as F1: any `met=` token in a counter dump can decide a control. Routed with F1.

## 4. Honest limits

- The replay is at `f4fff130`, the tip at my start. Later L1 commits are not covered.
- I did not run `c91_defects.py` itself (not my assignment). I reproduced its item-C environment exactly (`cwd`, `LANE`, `ONLY=c1`, `HYAKU_SCRATCH`) and the item-C code predicates by hand; the counter's other items (A battery, B receipt) are not measured here.
- The diagnostic reader (F1) is a scratch copy of the script with two lines changed (`reading()` and the final `rm -rf`). It is evidence for the cause, not a proposed patch of the frozen-byte script. The script in the lane is unchanged (sha256 above).
- The attacks ran on the clone's working tree (see §2 scope note). No commit was made anywhere.
- I did not use the labrat seat or any subagent. No network GET. No tools installed or upgraded (the `bash`, `git`, `python3`, `bash`/`sha256sum` already on the host were used).
- Concurrency: other seats write into LANE; the lane-status diff shows their untracked entries, attributable by path, not by my replay (which used `LANE=$S/clone`).

## 5. Receipts (`.ufo/waves/round-91/w1/ExecReplayC/`)

- `replay-c1.out`, `replay-c1.rc`: ONLY=c1, exit 0, `controls ok 9/9`.
- `replay-all.out`, `replay-all.rc`, `all-final.out`, `all-final.err`: ONLY=all, exit 1, `controls ok 11/14`.
- `item-c-mirror-c1.out/.err`: counter-equivalent replay, exit 0, `controls ok 9/9`.
- `diag/run_controls.diag.sh` (scratch copy; lines 26 and 169 changed), `diag/replay-*-diag.out`, `diag-reader-outputs/`, `diag-c1-outputs/`: retained counter outputs.
- `attacks/A1…A5*.out`: attack outputs (exit line at the end).
- `lane-status-before.txt`, `lane-status-after.txt`, `lane-status-final.txt`, `clone-status-after-checkout.txt`.
- `receipts.sha256`: sha256 of the replay outputs; `run-start-utc.txt`.
- Copy of the tip replay receipt: `.ufo/waves/round-91/controls/replay-tip.txt` (line 1 `revision=f4fff130a52ae6de49af5de7d568d2ee320ebfb0 exit=0 controls ok 9/9`).

## 6. Checks for the main agent to run

- `ONLY=c1 bash .ufo/waves/round-90/controls/run_controls.sh` on a clean clone at the tip: expect exit 0, `controls ok 9/9` (the R90-C claim).
- `ONLY=all` on the same clone: expect exit 1 and the three `c2-*` reader MISMATCH lines until F1 is decided.
- `git -C LANE status --porcelain` before and after any replay, and a clean scratch clone after the replay.
