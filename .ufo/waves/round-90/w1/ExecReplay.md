VERDICT: C1 and C2 replay as frozen (C1 open=0 closed=3 met=true; C2 4/4, 57/57, met=true on two random seeds; frozen bytes match freeze.md). Three defects found: (1) the gate's audit-hook sandbox can be bypassed, so an oracle-reading candidate is admitted; (2) run_controls.sh no longer replays because it reads a lane-root file that has since moved; (3) the sandbox reports ordinary crashes as `violation`.

Seat: ExecReplay (leaf; no delegation, no labrat used). All receipts are under `.ufo/waves/round-90/w1/ExecReplay/`. Scratch `/fast/scratch/hyaku/kake-r90/ExecReplay/` was used as `--work` and TMPDIR, and was deleted before yield. One scratch clone existed at a time (the controls `fx`; the script deletes and re-creates it per run). No lane, fleet or git mutation. No installs. No network.

## 1. Measurement replay (counters invoked from the lane path; bytes equal the frozen sha256, see §3)

| Run | Command | First line (receipt) | exit | Agrees with |
|---|---|---|---|---|
| C1 carrier | `python3 -B $R/c90_defects.py --root $LANE --revision e50c95660a9651fd9abe45119abab0bc3e8aaa56 --work $SCR/w-c1c` | `items=3 open=0 closed=3 met=true` (`c1-carrier.txt`) | 0 | `controls/after-c1-carrier.txt` — identical incl. JSON line |
| C1 base | same, `--revision 209027f4…` | `items=3 open=3 closed=0 met=false` (`c1-base.txt`) | 1 | `controls/base-c1.txt` first line + exit. **JSON line differs** (see D-R4) |
| C2 carrier seed A | `python3 -B $R/c90_gate.py --root $LANE --revision 7f6c68f1… --work $SCR/w-c2a` | `gate=present positives=4/4 negatives_refused=57/57 false_admits=0 errors=0 anti_table=ok population=ok seed=1336114608 met=true` (`c2-carrier-seedA.txt`) | 0 | `controls/after-c2-carrier.txt` (seed 923161196) |
| C2 carrier seed B | same, fresh SystemRandom seed | `… 4/4 … 57/57 … seed=1864621630 met=true` (`c2-carrier-seedB.txt`) | 0 | same |
| C2 base | same, `--revision 209027f4…` | `gate=absent positives=0/4 negatives_refused=0/57 … met=false` (`c2-base.txt`) | 1 | `controls/base-c2.txt` |

Per-subject verdicts are identical across seeds A and B. Only the generated pass counts move (for example `adv-member-ows` generated 58/120 vs 50/120). The admitted set is the same at both seeds: `scripts/cache_key.py`, `w1/L1/cache_key.py`, `M33-header-name-casefold`, `M36-duplicate-member-deduped`.

## 2. Controls replay

The command copies `controls/run_controls.sh` with only OUT and SCR changed (`run_controls.diff`) and runs it as `bash run_controls.sh` (exit 0). The first line and exit of each section were compared after normalising `revision=`: `verdict-diff.txt`.

- **ctl-c2: 5/5 sections agree** (first line and exit). The JSON body is also identical apart from the revision.
- **ctl-c1: 7/9 sections agree; 2 disagree:**
  - `## c1-F-D1a`: my first line is `cp: cannot stat '/home/vgpnk/Projects/shokunin/kake-shokunin/baseclean.out'`. The forgery was never built: `git commit` printed `nothing to commit`. The counter line `open=3 … met=false` still agrees, but for the wrong reason. D1 reads `relocated copy … not tracked`, not the lane receipt's `live: untracked lane-root entry baseclean.out`.
  - `## c1-positive`: same `cp` failure. The result is **`open=1 closed=2 met=false`, exit 1** (lane receipt: `open=0 closed=3 met=true`, exit 0), with `D1: relocated copy … not tracked`.

**Disclosed variant v2 (beyond the two-variable edit).** I re-ran the controls with only the two `cp "$LANE/baseclean.out"` sources replaced by `git show e50c9566:.ufo/waves/round-90/inherited/baseclean.out`, whose sha256 `4046c204…f00f` equals the counter's `INHERITED_SHA`; the edit is in `v2/run_controls_v2.diff`. Result: ctl-c1 and ctl-c2 section headers, first lines and exits are **identical** to the lane receipts (`v2/ctl-c1.txt`, `v2/ctl-c2.txt`). The only JSON difference is the do-nothing D1 body (D-R4). So the controls hold on today's bytes once their input is pinned.

## 3. Frozen bytes (`freeze-hashes.txt`)

The command is `git show <rev>:.ufo/waves/round-90/<p> | sha256sum`, run at 4ee62b18, 7f6c68f1 and e50c9566 for `c90_defects.py`, `c90_gate.py`, `frozen/c2-population.sha256`, `frozen/neg-oracle-path-import.py` and `frozen/neg-exec-source.py`. All 15 readings are equal to `freeze.md` (`462224f6…`, `703b0058…`, `a57f8985…`, `3621e359…`, `ad251e4a…`). The working-tree copies are equal too. The relocated `inherited/baseclean.out` at e50c9566 hashes to `INHERITED_SHA`. `baseclean.out` is not in the tree at 79e1aac2 and is absent from the lane root.

## 4. Defects

**D-R1 (C2 gate forgeable — sandbox bypass; severity high for the gate's stated property, does not change the frozen C2 predicate).**
- The sandbox hook in `scripts/cache_key_conformance.py@7f6c68f1` reads the module globals `_roots` / `_cand` each time it runs. Nothing stops a candidate from reaching them, because `sys._getframe` is not in `_DENY`.
- The probe `probes/bypass-frame-roots.py` (9 lines) walks `sys._getframe().f_back` until it finds the globals holding `_hook`, sets `_roots = ("/",)`, then calls `runpy.run_path("<LANE>/scripts/cache_key.py")`. That is the very oracle-path import `neg-oracle-path-import.py` is meant to model.
- Command: `python3 -B gate.py --candidate probe/nonce9.py --seed 7 --work $SCR/tmp`, where `gate.py` = `git show 7f6c68f1:scripts/cache_key_conformance.py` (sha256 `2840f32e…7591`, `probes/gate-at-7f6c68f1.sha256`).
- Result: `clauses=6/6 hand=70/70 generated=120/120 sandbox=ok seed=7 met=true`, **exit 0** (`probes/probe-receipts.txt`).
- The docstring says a candidate "may open no file other than itself and the standard library". That property is false. The 57/57 reading holds only because no frozen negative uses this trick.
- Other in-process bypasses are plausible (rebinding `os._exit`, mutating `_STD`), but I did not test them.
- Fix direction: keep no mutable decision state reachable from the candidate (closure or frozen tuple captured in default args), deny `sys._getframe` / `object.__getattr__` / `sys._current_frames` audit events, or move confinement out of process.

**D-R2 (controls script not replayable after the fix).**
- `run_controls.sh` copies its D1 inputs from the live `$LANE/baseclean.out`. The C1 fix itself removed that file.
- After the carrier, the D1a forgery silently turns into an empty commit, and the positive control reads `open=1 met=false`. That would look like a counter failure to any replayer (§2).
- Neither `set -e` nor an existence check catches it.
- Pinning the input to a committed blob (v2) restores the receipts exactly.

**D-R3 (sandbox mislabels crashes as violations).**
- If a candidate raises an uncaught exception, the traceback machinery opens the wrapper `sandbox.py` (linecache). The hook reports this as `SANDBOX_VIOLATION open …/sandbox.py`.
- Example: the round-89 `ctl-constant-key.py` (stdin → `{"key":"k"}`), run with `--verbose`, gets `refusals/malformed-json: violation` and `refusals/empty-input: violation` (`probes/probe-receipts.txt`).
- Consequence: all 5 round-89 shortcut controls report `sandbox=violation` with `clauses=0/6 hand=0/70`. The receipts therefore attribute their refusal to confinement, but at least ctl-constant-key fails behaviourally and only crashed on bad JSON.
- The verdict is unaffected (refuse either way), but `sandbox=violation` is not evidence of an escape attempt. Any count of "sandbox refusals" drawn from these lines would be overstated.
- The lesson's §4 row ("Sandbox denied the interpreter's own import machinery") is a related failure mode that is still not covered.

**D-R4 (C1 base reading is time-dependent, disclosed but worth noting).**
- D1's `live` conjunct reads the lane working tree, not `--revision`. So `--revision 209027f4` now gives a different D1 body than `controls/base-c1.txt`: the `live: untracked lane-root entry baseclean.out` reason has gone.
- The first line and exit still agree. `freeze.md` discloses that the conjunct is live.
- Limit: a C1 reading at any revision certifies the live tree only at run time.
- The do-nothing control's header ("live tree carries the inherited baseclean.out") is stale for any replay after the fix.

**D-R5 (minor pin weakness).**
- `freeze.md` names the two round-90 sandbox negatives by 8-hex prefixes only (`3621e359…`, `ad251e4a…`).
- Their full digests are pinned in `frozen/c2-population.sha256`, which is itself pinned in full, so nothing is actually loose. The freeze text alone would not suffice.

## 5. Limits
- I re-executed the counters and the gate. I did not audit the C1 counter's D2/D3 parsing logic beyond the forgery controls, and I did not review the gate's hand cases clause by clause against `c2-contract.md`.
- The bypass is shown for one technique only. I did not test whether `neg-exec-source`-style candidates bypass the sandbox the same way (likely, since the same hook state is reachable).
- `c90_gate.py` (the counter) runs the gate on the frozen population only. It has no adversarial-sandbox subject, so D-R1 is invisible to the frozen C2 predicate by construction.

Checks for main agent: re-run `probes/bypass-frame-roots.py` against `scripts/cache_key_conformance.py` at any later gate revision; regenerate `controls/ctl-c1.txt` with a pinned `baseclean.out` source.
