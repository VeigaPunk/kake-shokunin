# CriticP6VsP3 — is P6 a distinct probe from P3, or P3 plus a text check? (round 32, wave 1)

Seat: KakeR32.CriticP6VsP3 (critic, leaf). Axis: operability. Tip read: 285abcad632e3c1c57bb402232e7d218054db383.
Sandbox: /fast/scratch/hyaku/kake-r32/w1/CriticP6VsP3/ (clone at tip; mutants in mut/; fixture variants rootB/, rootC/).

## Verdict: SUPPORTED as declared, but the gain is a check on which layer refuses first, not a safety gain
For m3 itself, P6 is P3 plus a reason-text check: the extra trailing `git_init` does not matter.
The trailing `git_init` only matters against an order-insensitive guard mutant, which nobody claimed.
SCORECARD.md:1033-1036 already discloses that m3 is behaviour-equivalent and is killed only by the reason
text, so the C1 row is not overstated. Calling it "repair of routed item 2" is half true: item 2
(corpus/lessons/round-31-verifier-spotcheck.md:168) also names the Git pins, and they stay unprobed
(SCORECARD.md:1037-1038).

## Layer analysis (runner scripts/citing_set_selftest.py at tip, sha256 7c95a18e…8969)
- L1, load time: `load_case_setup` lines 349-363. The guard at 362-363 raises
  "case.json setup op 'git_commit' needs an earlier 'git_init'".
- L2, apply time: `apply_setup` lines 488-490. If `.git` is not a directory, it raises "git_commit needs the
  repository created by git_init". This runs before any `git add` or `git commit`.
- L3, Git pins: lines 439-451 (`--git-dir`/`--work-tree` inside the copy, `GIT_CEILING_DIRECTORIES`).
  Without L1 and L2, `git add -A` fails with exit 128 ("not a git repository").
- P3 (P3-commit-without-init/hostile.json) has setup `[git_commit]`. P6 (P6-commit-before-init/hostile.json)
  has setup `[git_commit, git_init]` plus `reason_contains`.
- Under m3 (L1 deleted), `apply_setup` handles steps in order, so P6's first step `git_commit` hits L2 before
  its `git_init` ever runs. P3 and P6 then take the same code path and get the same reason. The only signal
  that separates them is `reasonChecks` (citing_set_hostile_selftest.py:218-221).
- Safety does not change under any m3 variant: the victim is unchanged and no canary appears (table below).
  The kill adds no protection; it pins which layer refuses first. The docstring at
  citing_set_hostile_selftest.py:38-43 states this honestly.

## Counterexample matrix (hostile selftest, `--runner` swapped; exit 0 = mutant survives)
Mutants: m3 deletes lines 362-363. m3order replaces them with an order-insensitive check after the loop
(`any git_commit` and no `git_init` anywhere). m3apply is m3 with lines 489-490 also deleted.
Fixture variants: rootB is the tip with `reason_contains` removed from P6. rootC is the tip with P6 deleted
and `reason_contains` added to P3.

| run | fixtures | runner | exit | failing specs | h3/h6 reason | victim unchanged |
|---|---|---|---|---|---|---|
| A-pristine | tip | tip | 0 | none | both L1 | yes |
| A-m3 | tip | m3 | 1 | P6 | both L2 | yes |
| A-m3order | tip | m3order | 1 | P6 | h3 L1, h6 L2 | yes |
| A-m3apply | tip | m3apply | 1 | P6 | both L3 (git exit 128) | yes |
| B-m3 | rootB | m3 | **0** | none | both L2 | yes |
| B-m3order | rootB | m3order | **0** | none | h6 L2 | yes |
| C-pristine | rootC | tip | 0 | none | L1 | yes |
| C-m3 | rootC | m3 | **1** | P3 | L2 | yes |
| C-m3order | rootC | m3order | **0** | none | h3 L1 | yes |

What the matrix shows:
1. B-m3: P6 without `reason_contains` does not kill m3. The setup shape alone adds nothing.
2. C-m3: P3 with `reason_contains` kills m3 just as well. For the declared mutant, P6 is a relabel of P3 plus a text check.
3. A-m3order compared with C-m3order: the commit-before-init order is what makes P6 distinct. It kills an
   order-insensitive guard that P3 with a text check cannot see. That is a real but unclaimed operability gain.
4. Every run leaves the victim unchanged with no canary. Without L1, refusal still comes from L2, then L3.

## Smallest safe correction (advisory)
- Keep P6. When the round is described, say C1 pins the load-time layer and its order sensitivity, and that
  P3 with `reason_contains` would kill m3 equally. Do not present P6 as a new hostile shape that closes a containment gap.
- Mark routed item 2 as partly open: the Git-pin mutants (m3d, m3f) are still unprobed alone.
- Doc drift: citing_set_selftest.py:83 still says "The hostile specs probe five routed shapes (N1, N2, N3, N5, N6)".
  There are now six specs, including P6, gap "m3". Not edited, since I am a leaf.
- Hold boundary: I did not attack whether trusting runner-reported reason text is sound (KakeR31.CriticC1Counter
  hold). I only note that it is the sole discriminator, which SCORECARD.md:1035 already says.

## Commands (cwd: the sandbox, TMPDIR=<sandbox>/tmp)
- `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin clone && git -C clone checkout -q 285abcad…` gave exit 0.
- `python3 -B clone/scripts/citing_set_hostile_selftest.py --root <R> --tmpdir tmp/<tag> --runner <M>` for the
  9 runs above, with exit codes as in the table. Outputs are in out-<tag>.json (for example out-A-m3.json, out-C-m3.json).
- Mutant sha256: m3 c4cacd0d…7320, m3order 03db33a0…dae001, m3apply 10961d8e…302a7.

## Not verified
- I did not run `.ufo/waves/round-32/c1_m3_probe.py` or the 45 benign fixtures. Sibling rerun seats cover those.
  I also did not test the L2-only deletion mutant.
- No tools were installed or updated. Lane writes: this report only.
