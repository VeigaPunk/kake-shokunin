# ExecC2Counter — round 74 w1

## Delivered

- `.ufo/waves/round-74/w1/ExecC2Counter/c74_sidecar_reobserve.py`
- `.ufo/waves/round-74/w1/ExecC2Counter/base-observation.json`
- This report. No production files changed; no repository mutations or tool installations.

Axes: revision fidelity, host-observation accuracy, fixture coverage, write containment.

The counter reads sidecar bytes with `git show --end-of-options <revision>:corpus/knowledge/freshness-sidecar.json`; probes only each token via `os.stat`; expands home tokens from HOME; distinguishes FileNotFoundError/NotADirectoryError from other OSError failures. Repeated entries remain independently counted. The CLI provides --root, --revision, --json, --selftest and exits 0/1/2/64. JSON includes independent annotation findings against the frozen base (restored-note vocabulary and preserved prior date/kind/note). Function-level g1–g6 fixtures allocate no temporary files, so no fallback temporary location is used.

## Exact retained evidence

Required base observation command (cwd `/fast/scratch/hyaku/kake-r74/ExecC2Counter`, TMPDIR explicitly the same):

```sh
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-74/w1/ExecC2Counter/c74_sidecar_reobserve.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision ced2878a1e77f57afb4ee3baebf1021e5130399b
```

Exit **1**, empty stderr. Full command, environment path, stdout and exit retained in `ExecC2Counter/base-observation.json` beside the implementation.

```text
C2v1 revision=ced2878a1e77f57afb4ee3baebf1021e5130399b entries=174 absent=148 restored=26 absent_present=144 absent_absent=4 absent_unevaluable=0 restored_present=26 restored_absent=0 restored_unevaluable=0 contradictions=144 met=false
```

Other commands executed, each exit 0:

```sh
git -C /home/vgpnk/Projects/shokunin/kake-shokunin show b35dd4d7:.ufo/waves/round-74/controls/base-c2-sidecar.txt
git -C /home/vgpnk/Projects/shokunin/kake-shokunin show ced2878a1e77f57afb4ee3baebf1021e5130399b:corpus/knowledge/freshness-sidecar.json
git -C /home/vgpnk/Projects/shokunin/kake-shokunin show ced2878a1e77f57afb4ee3baebf1021e5130399b:.ufo/waves/round-73/c73_wave_pointers.py
mkdir -p /fast/scratch/hyaku/kake-r74/ExecC2Counter
```

Scratch removed in Python `finally: shutil.rmtree(scratch)` after receipt retention; observed `scratch_removed=true`.

## Risks and parent gates

- All numeric base-control fields and exit reproduce exactly. **Byte-for-byte control output does not:** the frozen receipt has four summary lines plus samples/distinct-token details, whereas the assigned CLI demands one summary line. The delivered line follows the explicit CLI format. This unresolved contract inconsistency is disclosed, not claimed passed.
- The seat's explicit `met iff AP==0 and RA==0 and AU+RU==0` formula does not incorporate the frozen contract's additional note/history conjuncts. The implementation preserves that formula and reports note/history violations separately in JSON. g4/g5 exercise that real helper, not fabricated stat failures. Parent must retain the separate conjunct checks; a zero count result alone is not the full C2 claim.
- Annotation-history matching uses (file,line,token); changed citation line numbers may require the parent to check history identity independently. The frozen base must be available for metadata comparison, including when measuring a later revision.
- Per leaf editing-wave restriction, **selftest, lint, build, JSON CLI and malformed-input CLI checks were not run**. Parent should run `python3 -B <counter> --selftest` (expect six fixtures), then JSON and CLI error-path checks, and the landing-tip C2/harm battery. No tests are represented as passing.
- LSP definitions/references tools are not exposed in this seat's tool inventory; existing instrument conventions were read directly from committed source. No supported-symbol refactor was performed.

## Self-evaluation

Accuracy 4/5: observed base counts and status retained; full after-state remains unmeasured. Completeness 3/5: executable fixture implementation delivered but parent-owned fixture run pending; the two contradictory contract requirements above cannot both be represented by the required summary formula/layout. Clarity 4/5: count predicate and separate metadata findings are explicitly distinguished. Actionability 4/5: artifact and exact parent commands supplied, pending integration. Conciseness 4/5: scoped standard-library implementation and one receipt; report retains required caveats. Overall 3.8/5. Highest-impact improvement: parent resolve the disclosed conjunct/layout tension without silently changing the frozen claim, then execute fixtures and landing gates. The user should agree because unrun gates and mismatches are named rather than hidden.
