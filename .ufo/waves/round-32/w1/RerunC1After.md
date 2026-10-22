# KakeR32.RerunC1After — C1 counter re-run at build commit and lane tip (wave 1)

Attack: re-run the declared C1 counting command independently in a fresh sandbox clone at
2f2f12deb0fe33d8fa7d9bd14c75d855f005f71a (build) and 285abcad632e3c1c57bb402232e7d218054db383
(lane tip), and compare field-for-field with the landed receipt
`.ufo/waves/round-32/verification/c1-after-2f2f12d.json`. Verdict below is advisory.

## Commands and exit codes

Sandbox: `/fast/scratch/hyaku/kake-r32/w1/RerunC1After/` (tmp/ + clone/). TMPDIR exported there.
No tool installs were needed; none performed. No pacman transactions. Lane untouched (probe uses
`git archive`; report file is my only lane write).

1. `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin .../clone` — exit 0 (HEAD 285abca).
2. Run A: `git -C clone checkout -q 2f2f12d...` then
   `python3 -B .ufo/waves/round-32/c1_m3_probe.py --repo . --rev 2f2f12deb0fe33d8fa7d9bd14c75d855f005f71a`
   — probe exit 0.
3. Run B: `git -C clone checkout -q 285abca...` then
   `python3 -B .ufo/waves/round-32/c1_m3_probe.py --repo . --rev 285abcad632e3c1c57bb402232e7d218054db383`
   — probe exit 0.
4. `git show <r>:.ufo/waves/round-32/c1_m3_probe.py | sha256sum` for r in
   {5b32cc7c..., 2f2f12d..., 285abca...} — exit 0.
5. Deep-compare (eval py): fresh re-run of the rev-2f2f12d probe vs the receipt JSON parsed and
   compared with `==` — probe exit 0, `receipt == got` True, differing keys [].

## Observed outputs

Run A (rev 2f2f12d, probe exit 0), JSON fields:

- schema kake-r32-c1-m3-v1; m3Applied true; runnerSha256
  7c95a18e4621ca6c4f0085eb9d208a0f1e6a1211989e51dd0c733ee1488b8969
- pristine: exit 0; P1..P6 all true (P6-commit-before-init true)
- mutant: exit 1; P1..P5 true, P6-commit-before-init false (only failure)
- benign: exit 0, cases 45, failed 0
- guard_ok true; killed 1

Run B (rev 285abca, probe exit 0): identical fields except `"rev"` is the tip hash; killed 1,
guard_ok true, mutant fails only P6, benign 45/0.

Probe byte identity (sha256, all three revisions identical):

- 5b32cc7c... 411498bb858fbc481b4b2320f5ec6a38e53980d3090cf83cf70b06a01bfe6c27
- 2f2f12d.... 411498bb858fbc481b4b2320f5ec6a38e53980d3090cf83cf70b06a01bfe6c27
- 285abca.... 411498bb858fbc481b4b2320f5ec6a38e53980d3090cf83cf70b06a01bfe6c27

So the probe bytes are unchanged from the declaration commit through the tip, and the tip does
not flip C1.

## Comparison with receipt

- Run A is deep-equal to `c1-after-2f2f12d.json` (all keys, including runnerSha256 and both spec
  lists): `receipt == got` True. No difference from the receipt.
- Run B matches the receipt on every field except `rev`, as expected. Declared "after 1 with
  guard_ok true" is reproduced at both revisions.

## Findings

- None blocking. C1's after-measurement reproduces exactly, deterministically (second fresh run
  also deep-equal), at both the build commit and the lane tip.
- Advisory nuance (no action asked): the probe's `killed` is `mutant exit == 1` — it does not
  itself assert that the mutant failure is P6-specific. In all three runs the mutant spec list
  shows P6 as the only false case, so the kill is P6-specific in fact; the probe JSON carries the
  evidence either way.

## Not verified

- I did not re-derive the round-31 m3 mutant definition beyond the probe's own guard-deletion
  regex (matched exactly once at both revs; `m3Applied` true); held items forbid re-litigating
  runner-reported reason text, and none was judged.
- Benign sweep observed only through the probe's own 45/0 summary; I did not re-count fixtures
  independently (out of this item's scope).

Evidence pointers: runs above from
`/fast/scratch/hyaku/kake-r32/w1/RerunC1After/clone` (clone of lane master);
receipt at `.ufo/waves/round-32/verification/c1-after-2f2f12d.json`;
probe source `.ufo/waves/round-32/c1_m3_probe.py:44-99` (fields written; `killed`/`guard_ok`
definitions at lines 95-96 of the read range shown as 95-96 → file lines ~95-96).
