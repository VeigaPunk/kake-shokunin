# SentinelC2 — security review, round-72 kake (w1)

**Verdict: blocking=1 routed=3 note=3**

Scope: `.ufo/waves/round-72/c72_tmp_v2.py` (frozen, committed at a19d38ea) and `.ufo/waves/round-72/controls/j3-control.sh`.
Base: lane HEAD a19d38ea (round-72 freeze), contract base 3c68645a / cc6b4e0b.
Tools: python3 3.14.8, git 2.56.0 (pre-existing). Installed nothing.

Headline: the counter is safe against option injection and shell injection (check 1 and 2 hold). The
J3 control script's committed bytes cannot produce the `c72_exit=1` line that the frozen receipt requires
(B1), and the lane's working tree carries an uncommitted edit to the same script that fails open (R1).

---

## Blocking

### B1 — committed j3-control.sh cannot emit the receipt's `c72_exit=1` line
The committed script runs under `set -eu`. When the round-72 counter exits 1, `set -e` aborts the script
before `echo "c72_exit=$?"` runs. The frozen receipt `controls/c2-j3-control.txt` contains `j3_script_exit=1`,
which no committed script writes. Its provenance is an uncommitted wrapper.

Commands (scratch clone `$S/clone` = lane HEAD; `$S` = my scratch):
```
env HYAKU_SCRATCH="$S" sh "$S/clone/.ufo/waves/round-72/controls/j3-control.sh" > h1.txt 2>&1; echo $?
  -> exit=1 ; grep -c '^c72_exit' h1.txt -> 0
  h1.txt: J3_CONTROL_COMMIT=f34e9ab2... / c71_exit=0 / c72 C2v2 ... met=False  (no c72_exit line)
git -C LANE grep -n c72_exit <all commits>  -> only the echo inside j3-control.sh and contract.md text;
  no committed receipt contains c72_exit. Receipt contains j3_script_exit=1 (line 7), committed in 4 commits.
diff <(sed -E 's/[0-9a-f]{40}/HASH/g' receipt.txt) <(sed -E 's/[0-9a-f]{40}/HASH/g' harness_out.txt)
  -> empty only when harness_out appends "j3_script_exit=$?" (my wrapper), not when running the committed script.
```
Impact: contract C2 counting command "→ `c71_exit=0` and `c72_exit=1`" is not reproducible from committed
bytes; the receipt is evidence of a harness the lane does not commit. Smallest fix: drop `set -e` on the
counter invocations (keep `set -u`), or capture `c72_rc=$?` explicitly, and commit the receipt's producer.

---

## Routed

### R1 — uncommitted working-tree edit to j3-control.sh fails open
At 19:01 (not by this seat; I made no lane writes) the lane working tree gained an uncommitted edit:
`set -eu` -> `set -u`, plus a rewritten `receipts.json` and an untracked `controls/c2-j3-control-r2.txt`.
`git -C LANE status --porcelain` lists them; HEAD is still a19d38ea.
```
diff <(git show a19d38ea:.ufo/waves/round-72/controls/j3-control.sh) j3_worktree.sh
  -> 5c5 < set -eu / > set -u
env PATH=<stub git that fails clone>:/usr/bin:/bin HYAKU_SCRATCH=$S/fo sh j3_worktree.sh ; echo $?
  -> J3_CONTROL_COMMIT= ... c71_exit=2 ... c72_exit=2 ; exit=0
env PATH=<same stub> HYAKU_SCRATCH=$S/fo sh <frozen committed script>; echo $?  -> exit=128
```
Impact: the working-tree variant reports green exit (0) when both counters are unevaluable. Under both
variants the script's exit code is the last `echo`'s status unless `set -e` aborts, so the exit code is not
the verdict. Do not commit `set -u`; B1 needs a fix that keeps the failure exit. Route to the integrator.

### R2 — round-72 counter accepts a symlinked SKILL.md (vacuous pass)
`git show <rev>:SKILL.md` on a mode-120000 blob returns the link target text. A commit that replaces
SKILL.md with a symlink to /dev/null gives met=True.
```
D=<clone of lane>; ln -sf /dev/null "$D/SKILL.md"; git add -A; git commit ...
git ls-tree REV SKILL.md -> 120000 blob dc1dc0cd...  SKILL.md
python3 -B c72_tmp_v2.py --lane "$D" --revision REV ; echo $?
  -> C2v2 revision=1d22f617... brace_findings=0 command_findings=0 prose_findings=0 findings=[]
     removed=1396 added=1 guard=ok met=True ; exit=0
control (regular file with a real /tmp line): exit=1, command_findings=1, met=False
```
Impact: a non-regular SKILL.md passes C2. The counter is frozen, so no edit this round; route to the
round-73 counter (check `ls-tree` mode is 100644 before `git show`).

### R3 — relative HYAKU_SCRATCH makes the EXIT trap delete outside scratch
The script `cd`s to LANE before exit. The trap `rm -rf -- "$ROOT"` resolves a relative `$ROOT` against
LANE, not the caller's cwd. Startup `mkdir` used the caller cwd.
```
env -i PATH=<rm stub that prints RM_CWD>:/usr/bin:/bin HYAKU_SCRATCH=.. sh j3-control.sh
  -> RM_CWD=/home/vgpnk/Projects/shokunin/kake-shokunin ARGS: -rf -- ../kake-r72/j3-control
     (resolves to /home/vgpnk/Projects/shokunin/kake-r72/j3-control, outside any scratch)
HYAKU_SCRATCH=relative -> RM_CWD=LANE ARGS: -rf -- relative/kake-r72/j3-control
```
Impact: requires an operator-set relative value; default and absolute values are fine (see check 3).
Smallest fix: `case $HYAKU_SCRATCH in /*) ;; *) exit 64;; esac`, or `ROOT=$(cd ... && pwd)` before the `cd`.

---

## Note

### N1 — concurrent runs collide on the fixed ROOT
Two runs with the same `HYAKU_SCRATCH` (the default path is fixed) corrupt each other: run1 exit 1 with
`cannot copy ... hooks/*.sample: File exists`; run2 exit 128 `Unable to create .../alternates.lock`. The
startup `rm -rf` and the trap `rm -rf` of one run can delete another run's clone. Two seats using the
default path produce false reds. Fix: `mktemp -d` under `$HYAKU_SCRATCH`.

### N2 — startup `rm -rf "$ROOT"` lacks `--`
Trap uses `--`; startup does not. Only triggers if HYAKU_SCRATCH begins with `-`. Checked in an isolated
dir: `rm -rf "-rf /victim"` -> `error: unexpected argument '- '` exit 1, `victim/keepme` intact. No deletion,
but add `--` for symmetry.

### N3 — absolute HYAKU_SCRATCH=/ targets `/kake-r72/j3-control`
Dry trace: `HYAKU_SCRATCH=/` -> `rm -rf -- //kake-r72/j3-control`. That is exactly the documented target
`$HYAKU_SCRATCH/kake-r72/j3-control`, so it is in-contract. Operator-controlled env, not an injection.

---

## Checks (contract questions 1-5)

**(1) Revision reaches git after --end-of-options.** Holds.
```
python3 -B c72_tmp_v2.py --lane $S/clone --revision "--output=$S/pwned"   -> exit=2  (C2 unevaluable ... exit 128)
... "--no-index"          -> exit=2 ;  "--output=$S/pwned2:" -> exit=2
... "--upload-pack=id" / "--exec-path=/tmp" / "-o" / "--work-tree=/tmp" / "--" / "--paginate" / "--textconv" / "--stat" / "-p" / "--notes" -> exit=2 each
ls $S/pwned* -> no such file (no write). Legit rev 3c68645a -> exit=0 met=True.
Load-bearing check: git show --output=$S/lanetest/would_write 3c68645a:SKILL.md -> exit=0, file created (0 bytes).
```

**(2) --lane is a path only; no shell.** Holds.
```
grep -nE "shell=True|os\.system|os\.popen|bash -c|sh -c|eval |exec " counter -> NONE
subprocess.run(["git","-C",lane,"show","--end-of-options",f"{rev}:{PATH}"], capture_output=True, text=True)  (line 89)
--lane 'a b; touch $S/lanetest/pwned_lane; echo hi' -> exit=2, no file created
--lane "--output=$S/lanetest/pwned_lane2" -> git: cannot change to '--output=...' exit 128 -> counter exit=2, no file
--lane non-repo / --lane a file -> exit=2
Config vectors (repo with real history, BASE present): .gitattributes textconv=evil -> exit=0, no marker;
core.pager -> exit=0, no marker; GIT_EXTERNAL_DIFF -> exit=0, no marker; .git/hooks -> exit=0, no marker.
```

**(3) j3-control.sh rm target.** Holds for empty and unset.
```
sh -n j3-control.sh with HYAKU_SCRATCH= -> exit=0
HYAKU_SCRATCH= (empty) dry trace (stub rm/git/python3/mkdir; sh -x):
  + ROOT=/fast/scratch/hyaku/kake-r72/j3-control
  + rm -rf /fast/scratch/hyaku/kake-r72/j3-control        (argv-exact stub: arg2=[/fast/scratch/hyaku/kake-r72/j3-control])
  + rm -rf -- /fast/scratch/hyaku/kake-r72/j3-control     (EXIT trap)
HYAKU_SCRATCH unset: same target.
HYAKU_SCRATCH=$S (absolute) dry trace target: $S/kake-r72/j3-control.
```
Real run (frozen committed script) with HYAKU_SCRATCH=$S: exit=1 (B1 behaviour). `$S/kake-r72` empty afterwards;
no lane change (before/after `find` of lane tree and `.git` identical, 31764 and 1398 entries).
Shared stub of `rm` printing argv only, for HYAKU_SCRATCH in {"", "/", "-rf /", "relative", "/tmp/x"} -> targets as above; no real rm invoked.

**(4) Committed bytes only; no lane writes.** Holds.
```
dirty clone SKILL.md (appended a /tmp line) -> counter --revision 3c68645a -> met=True, unchanged (committed bytes).
counter run against the LANE (cwd=LANE, --revision 3c68645a): tree and .git find-snapshots identical before/after; exit=0.
lane status after my runs = peers' files only; my only new path is w1/SentinelC2.md.
__pycache__ under scripts/ predates this seat (mtimes 2026-10-26/27); no .pyc newer than 40 min.
```

**(5) Credentials.** None.
```
grep -nE "op://|AKIA|ghp_|gho_|sk-[A-Za-z0-9]{16,}|xox[baprs]-|BEGIN .*PRIVATE KEY|eyJ...|password|passwd|secret[=:]|api[_-]?key|token[=:]|Authorization:|https?://"
  on lane working-tree j3-control.sh and c72_tmp_v2.py -> no matches
receipts.json (working tree) -> no credential matches (URLs only; not secrets)
```

---

## Side effects and disclosures
- Lane writes by this seat: none. The only file I wrote in the lane is this report.
- Peer activity seen during the review: working-tree edits to `j3-control.sh` and `receipts.json` and the
  untracked `c2-j3-control-r2.txt` appeared at 19:01 (see R1). I did not create them and did not message peers.
- One mistake: I ran `rm -rf "--/nonexistent-proof-xyz"` from the shell's cwd (the fleet root). It was rejected by
  rm as an unparseable option (exit 1); nothing was removed. Disclosed for completeness.
- Scratch: `/fast/scratch/hyaku/kake-r72/SentinelC2/` (about 2.5 GB of clones and stubs), deleted before yield.
