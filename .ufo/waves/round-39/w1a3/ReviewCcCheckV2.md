# ReviewCcCheckV2 — QUALITY (j) control-consequence check v2

Target: `.ufo/waves/round-39/criteria/control_consequence_check.py` @72edf21 (sha256
`39d6e4ed36d3a5b6a72bf53bd6dd954d921d5e9b324eec8f3f0298ef0af100a0`; working-tree bytes identical).
Counter sha `f3a0cd60…6084593` matches declaration; PREDICATE/CASES/TARGET/KEY_SHA256 parsed from
`sealed_count.py:16-19`. No tool installs needed (stdlib python3 + git only).

## Q1 — Can any receipt meet the predicate yet pass as non-control? **HOLDS** (one input-layout caveat below)
- Classification is content-only: file filter is `.json` suffix (:55); `label`, `note`, `toolFile`,
  `revision`, directory and class text are never read in `evaluate` (:51-88). Foreign receipts
  (predicate/counterSha256/keySha256/cases/target) → PROBLEM → exit 2 (:66-69,:121).
- `met`/`passed` not trusted: recomputed from rows, `pass is True` strict (:75-76); disagreement →
  exit 2 (:77-79). `bsha is not None` guard (:83) stops `None==None` passing as BUILD.
- Live demo (sandbox `rx2/`): forged receipt named `deep/build-forged.json`, `label:"build"`,
  toolSha256 of dead CtlJunk, 24/24 rows, `met:true` → `CONTROL-MEETS`, exit 1. Name and label ignored.
- Only paths to exit 0 for a meeting receipt: toolSha256 == build bytes (`git show REV:scripts/
  sitemap_audit.py`, :46-48) or an argv `--oracle-sha` (:83-87). Receipts cannot self-exempt
  (oracles set built from argv only, :98,:111).
- **Finding F1 (low):** `os.walk` without `followlinks` (:53) silently skips symlinked receipt
  subdirs. Probe: `rx4/` = dead-CtlJunk.json (visible) + meeting ref.json behind `linked/` symlink
  → `receipts read 1`, **exit 0** while a meeting control exists. All-hidden fails closed
  (`n==0` → exit 2, rx3 probe); partial hiding is silent. Operator-bounded but the docstring's
  "every *.json under --receipts (recursive)" (:10) overclaims. Fix: `followlinks=True` or reject
  symlinked dirs.

## Q2 — Does reading B (`--oracle-sha`) widen beyond the one named tool? **YES, but bounded and loud**
- `:97` `action="append"`, `:85` exempts ANY meeting receipt whose toolSha256 is argv-named — not
  limited to the declaration's oracle (`663e051e…`, named in SCORECARD@915e9e8 drafting-defect).
- Demo: `--oracle-sha fc7b986d…` (dead CtlJunk bytes) exempted my forged control → `EXEMPT`
  printed (:86); exit stayed 1 while other meeting controls remained; naming all meeting shas
  would reach exit 0.
- Bounds: default `[]`; byte-bound equality; receipt content cannot trigger it; every exemption
  printed with path+sha (:86,:116-118). **F2 (low):** no cross-check that named shas equal the
  declaration's oracle; misuse is detectable only via the printed EXEMPT lines.

## Q3 — Runs (all commands from lane root; -B, read-only)
- `python3 -B .ufo/waves/round-39/criteria/control_consequence_check.py --selftest` → PASS 14/14, exit 0
  (all 14 cases incl. "control named build-*.json", "one hex digit off", "met field lies", "oracle not named").
- Invocation A: `… --receipts .ufo/waves/round-39/verification/a3` → exit 1:
  `CONTROL-MEETS …/a3/ref.json (tool 663e051e10b9, passed 24)` at the 15-receipt snapshot;
  re-run on grown a3 (75 receipts, HEAD 4c080d3) → exit 1, 16 CONTROL-MEETS incl. ref.json +
  MutUrlAuthority M03/M04/M05/M09/M10, MutNamespaceBinding M02/M03/M04/M07/M08/M09/M10/M11,
  MutStdlibSubstitution M09, MutEntryNumbering M02.
- Invocation B: same + `--oracle-sha 663e051e…2d69f8` → snapshot exit 0 `EXEMPT ref.json (oracle
  663e051e10b9)` (matches committed `a3-jcheck/B.txt`); on current a3 → exit 1 (15 controls still
  meet — reading B rescues only the one named tool).
- `--build-revision 72edf21` → `cannot evaluate: … sitemap_audit.py … exit status 128` → exit 2
  (fail-closed while build absent; consistent with kill-rule ordering).

## Residual risk
F1 (symlink skip) is the only actionable defect found; F2 is a hardening note. Check's own verdicts
are content-honest; current a3 exits 1 under both readings, agreeing with the L1's kill rule (1)
firing at 4c080d3. No verdict on C1 itself.
Fixtures: `/fast/scratch/hyaku/kake-r39a3w1/ReviewCcCheckV2/rx{,2,3,4}/`.
