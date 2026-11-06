# ReviewDeterminism — round 100 w1 findings

Seat: ReviewDeterminism (leaf; no subagents). Axis named for this wave: **determinism of the two
frozen counters on committed bytes** — cheap to iterate (re-runs), parallel (independent runs),
kept because it underwrites every downstream verdict that cites a control receipt.

## Verdict
Hypothesis held. At the round base `3989618d9f8310b2eb5fb456aa7c4e58fb0b5ff5`, both frozen
counters reproduce byte-identical receipts:

- `c100_registry.py`: 3/3 runs byte-identical to `controls/base-c1.txt` minus its `$`/`exit=`
  lines (sha256 f93da0853d542f4887459f556833964ebc8edf551c0b5243c0eb0a48ae74628c), rc=1 each
  (base expectation `met=false`, exit 1), stderr 0 bytes.
- `c100_fresh304.py`: 3/3 runs byte-identical to `controls/base-c2.txt` minus its `$`/`exit=`
  lines (sha256 794dc26df2fa7f2f50b4f375f030bc8d7bcd17f75b19bd93149a255e5faed10f), rc=1 each,
  stderr 0 bytes. Run-to-run: b1==b2==b3.
- Seeded: `--seed 1` twice → byte-identical pair (sha256 9c0e1eadc34427528de26ed5a04d194e7fd15ea06a08b119d090893f947055a9),
  rc=1; correctly differs from the default-seed receipt (seed=965304717 = int("3989618d",16),
  generated=224/300) because seed 1 draws generated=225/300, refusals=85/132.

Evidence detail, exact commands and observed rcs: `w1/ReviewDeterminism/runs.txt`; raw receipts in
`w1/ReviewDeterminism/` (a-run*, b-run*, seed*, base-c{1,2}.stripped, receipts.sha256).

## Instrument integrity (precondition, verified)
All 20 digests in `controls/instrument-sha256.txt` match both the working tree and
`git show d7b73d16…` for every listed file; `git diff --stat d7b73d16..master` over round-100 is
additive-only (715 insertions, 0 deletions). No counter drift since the freeze.

## Defects found
None. No non-determinism, no instrument mismatch, no receipt drift. Nothing patched, nothing
re-stamped; controls reproduced, never edited.

## Residual risk / gaps (routed, not repaired)
1. Scope: one host (linux 7.2.11-arch1-1, python3 3.14.8, bwrap 0.13.1), one revision (the base).
   Cross-runtime and cross-revision determinism untested — out of this seat's frozen item.
2. Receipt defined as stdout+exit code; per-run scratch is rmtree'd by the counters themselves, so
   work-dir residue was not an additional comparison surface.
3. Registry triple ran concurrently; equal to the serially produced control byte-for-byte (this
   strengthens the claim), but no separate serial triple was executed.
4. Environment note: bwrap unprivileged sandboxing worked without any host change; no sysctls or
   host config touched; no tools installed (recorded per operator tooling rule: zero installs).

DETERMINISM registry_identical=3/3 fresh304_identical=3/3 seeded_identical=true hypothesis=held
