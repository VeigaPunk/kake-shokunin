# KakeR31a2.RerunC1Counter — C1 counter rerun (wave 2, falsify seat)

Axis: operability. No installs performed (none needed). All work in sandbox
`/fast/scratch/hyaku/kake-r31/a2-w2/RerunC1Counter/` (clone at tip 92235a0,
clean, `git status --porcelain` = 0 entries after all runs); the only lane
write is this report.

## What I attacked

Re-ran the declared C1 counter at the three declared revisions and diffed every
named receipt field. Looked for: unreproducible receipts, sha drift in the
counter/runner bytes, per-probe behaviour/fixture divergence, K1 control
breakage, and counter writes escaping the sandbox.

## Commands and exit codes

Sandbox prep (rc 0):
`git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin .../RerunC1Counter/clone`

Sha checks (`git -C clone show <rev>:<path> | sha256sum` equivalent, via
subprocess; `.ufo/waves/round-31/c1_sandbox_probes.py` and
`scripts/citing_set_selftest.py`):

- f1ffb81 counter: **ABSENT (rc=128)** — file does not exist in the base tree;
  runner `9f2d1ecb280b…49e14d3` (matches receipt).
- c88b97e counter: `4707cebf8831eb9a8e79405fcc07ad77e118110f980dac2826c5934a43166d1a`
  (= declared); runner `5371530d93ec…4c0ce6c` (matches receipt).
- fde133a counter: `4707cebf…43166d1a` (= declared); runner `5371530d…4c0ce6c`
  (matches receipt).
- tip 92235a0 on-disk counter: same `4707cebf…43166d1a`.

Counter runs (one bash-equivalent thread each, parallel, TMPDIR inside
sandbox, `--scratch <sandbox>/counter`; each run got a fresh
`counter/c1-<rev7>-<rand>` mkdtemp dir — verified isolated):

1. `python3 -B .ufo/waves/round-31/c1_sandbox_probes.py --root <clone> --revision f1ffb81738c92c0537b99b30970143ab9419f990 --scratch <sandbox>/counter`
   → **exit 1**, stderr: `C1 0/5 K1=hold at f1ffb81738c92c0537b99b30970143ab9419f990` (92.1 s)
2. same, `--revision c88b97e6b02d85357b4b1e12d4bc09669ef82035`
   → **exit 0**, stderr: `C1 5/5 K1=hold at c88b97e6b02d85357b4b1e12d4bc09669ef82035` (2.4 s)
3. same, `--revision fde133ab48086bb9a06911b4ab045e2ad9086347`
   → **exit 0**, stderr: `C1 5/5 K1=hold at fde133ab48086bb9a06911b4ab045e2ad9086347` (2.3 s)

## Receipt comparison

Compared rerun JSON vs committed receipts — fields `counter`, `counterSha256`,
`revision`, `runnerSha256`, `passed`, `total`, `controlK1`, `k1` (exit+cases),
`hostileSelftest` (present/exit/cases), and per probe `id`, `gap`, `passed`,
`behaviour`, `fixture`, `fixtureDirs`, plus `detail` key sets (values excluded:
fresh mkdtemp paths and freshly created victim commit shas are nondeterministic
by design):

- vs `verification/c1-before-f1ffb81.json`: **IDENTICAL, 0 diffs.**
  (passed 0/5, controlK1 true, k1 {exit 0, cases 45}, hostileSelftest
  present=false, all probes behaviour=false fixture=false fixtureDirs=[])
- vs `verification/c1-after-c88b97e.json`: **IDENTICAL, 0 diffs.**
  (passed 5/5, K1 hold, hostileSelftest exit 0, all five cases true, every
  probe behaviour=true fixture=true with its named fixtureDir)
- vs `verification/c1-after-fde133a.json`: **IDENTICAL, 0 diffs.** (same shape)

Receipt bytes vs history: `c1-before-f1ffb81.json` (f06a4075093e) and
`c1-after-c88b97e.json` (d5e437e00af7) are byte-identical at fde133a, 92235a0
and the lane worktree; `c1-after-fde133a.json` is absent at fde133a (rc=128)
and first present at 92235a0 (f33e0ef53bfe) = the worktree copy I diffed. The
attempt-2 receipts are what I compared; the earlier-round receipts for
before/c88b97e never changed.

## Findings

1. **[minor, wording-level] The declared per-rev counter-sha check is
   unsatisfiable at the base revision.** The assignment says to check
   `git show <rev>:.ufo/waves/round-31/c1_sandbox_probes.py | sha256sum` at
   f1ffb81; that path does not exist in the base tree (rc=128). The before
   receipt's `counterSha256` therefore can only refer to the later-committed
   counter bytes — which are identical at c88b97e, fde133a and 92235a0, so the
   before rerun I performed (tip counter, `--revision f1ffb81`) is the only
   faithful reproduction and it matches the receipt exactly. This weakens
   nothing material, but SCORECARD/counter prose implying the counter rode
   along at the base revision would be overstated. Evidence: `git show
   f1ffb81:…c1_sandbox_probes.py` rc=128; receipts at
   `.ufo/waves/round-31/verification/c1-before-f1ffb81.json:4`.
2. **Timing asymmetry, corroborating:** before run 92.1 s vs after runs ~2.3 s.
   Consistent with the repaired runner refusing hostile fixtures immediately
   instead of executing them to their 20 s per-case timeouts; not proof on its
   own, but no anomaly indicator.
3. **No defect found in C1 measurement.** All three runs reproduce the
   receipts with zero diffs on every named field; K1 holds at all three
   revisions (45 cases, exit 0); counter exit codes match the 0/5 and 5/5
   semantics; `00-benign` never failed; no-canary / victim-unchanged
   conditions held where required (probes passed).
4. Structural corroboration of the before shape: base tree has no
   `scripts/citing_set_hostile_selftest.py` (rc=128) and no
   `scripts/fixtures/citing-set-hostile/` entries (ls-tree count 0), so
   `present:false` + `fixture:false` at base is structural, not accidental.

## Hygiene

- Counter writes confined to `--scratch` subdirs (three `c1-<rev>-<rand>`
  dirs observed); clone still clean after runs; nothing written outside my
  sandbox except this report.
- I did not rerun at 92235a0 itself; my runs target the three declared
  revisions. The tip is content-identical to fde133a for everything C1
  touches (counter and runner sha256 equal), so a 92235a0 rerun is not
  expected to differ; the attempt-2 L1's 92235a0 receipts are byte-identical
  to what I diffed.
- `detail` payloads compared by key set only (fresh paths/commit shas inside
  are nondeterministic by construction); I did not audit their internal values
  beyond that.

Artifacts (sandbox): `out/before.json`, `out/c88b97e.json`, `out/fde133a.json`
(+ `.stderr`), outputs of the three reruns; receipts at
`.ufo/waves/round-31/verification/c1-*.json`.
