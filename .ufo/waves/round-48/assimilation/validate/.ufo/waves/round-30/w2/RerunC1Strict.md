# Kake R30 wave 2 — RerunC1Strict (falsify C1 strict supplement)

- Seat: KakeR30.RerunC1Strict (leaf). Axes: operability, freshness.
- Target: the C1 strict supplement result at 71c6bfabd7aa957d15732d9224888bb32849238a
  (receipt `.ufo/waves/round-30/verification/c1-strict-after-71c6bfa.json`, 6/6).
- Sandbox: `/fast/scratch/hyaku/kake-r30/w2/RerunC1Strict/` (clone, tree71 export, scratch, run outputs).
  No writes inside the lane except this report. No installs performed; no pacman; no live requests.

## Verdict: HOLDS

The strict supplement reproduces end-to-end from a clean sandbox at 71c6bfa and matches the
landed receipt exactly; the checker blob is identical at 71c6bfa and 04637bd, and is still
identical at master HEAD 451e98f, so the receipt is fresh for the current lane head.

## Identity checks (all exit 0)

- Blob ids: `71c6bfa:.ufo/waves/round-30/c1_strict_checks.py` = `04637bd:…` =
  `451e98f:…` = `d8b43fb6538419c4b7b4a0dec5867215fdcda22b` (git cat-file -t blob).
  Sibling counter blob likewise identical at all three: `232172de3079dae7c3628c84ac27ba0e724e6d12`.
- sha256 of the 71c6bfa checker blob: `96e7bbcd8ec9144316a1c717570f802b8d5e16a63a16c8a009049bf5d0e9500f`
  = receipt `checkerSha256`; counter `be2a1287ab7f2abdca8695d8274504d14b9e1c6b0afe95e940c890bfb8bcc53e`
  = receipt `declaredCounterSha256`.
- `git archive 71c6bfa` → `tree71/`: gate `scripts/citing_set.py` sha256
  `dbfade45e59351fb5edc010dfc45a4e15e1213fdb6fad9ec1668ffd3b77b7f02` = receipt `gateSha256`;
  runner `citing_set_selftest.py` `0fc87d5b8134c841b02d0db33d8a3262fb774d0c8aacaefc6b6811f190b6530a`
  = receipt `runnerSha256`.
- Freshness: `git diff --stat 71c6bfa..451e98f -- scripts .ufo/waves/round-30/c1_strict_checks.py
  .ufo/waves/round-30/c1_reason_count.py` is empty; clone worktree not dirty for those paths.

## Reproduction run (exit 0, 19.5 s)

```
python3 -B tree71/.ufo/waves/round-30/c1_strict_checks.py \
  --root <sandbox>/clone \
  --revision 71c6bfabd7aa957d15732d9224888bb32849238a \
  --scratch <sandbox>/strict-scratch
# stderr: C1 strict 6/6 at 71c6bfa… {'S1': True, 'S2': True, 'S3': True, 'S4': True, 'S5': True, 'S6': True}
```

- Structural diff of my stdout JSON vs the receipt: 0 differences outside S5; S5 matches
  structurally and even literally (`deviceOpens [['/dev/pts/1', 526592]]`, `ttyNr 0`,
  `problems []` both runs). All five identity fields equal the receipt's.
- S1/S2 cover 10 codes each (8 R-codes + document_duplicate_key + document_nonfinite_number),
  all `passed: true`, `problems: []`; S3 all 17 repeat-flag variants exit 64 with usage object
  plus "each option once" exit 0; S4 1000-deep corpus walk exit 1 with the single
  unadjudicated-pair finding; S6 all 5 duplicate-key / non-finite cases exact.
- Artifacts: `<sandbox>/strict-stdout.json` (full checker JSON), `<sandbox>/strict-stderr.txt`,
  `<sandbox>/tree71/` (exported 71c6bfa tree), `<sandbox>/clone` (clone of the lane).

## Falsification controls (checker is not vacuously green)

- Base revision 0356681 (pre-round-30 gate, `gateSha256 d7e79ba102ff27761d830f95ad91e1970ebfcc942eea9728a0bdf3b0c3479d48`):
  exit 1, `C1 strict 0/6 … {'S1': False, 'S2': False, 'S3': False, 'S4': False, 'S5': False, 'S6': False}`.
  The strict suite genuinely discriminates the pre-round-30 gate from the 71c6bfa gate.
- Unresolvable revision `no-such-revision-r30`: exit 2, stdout
  `{"error": "cannot export scripts/ at revision", "revision": "no-such-revision-r30"}` —
  the documented bad-input path works.

## Residual risk / not verified

- I re-ran the checker as landed; I did not independently re-derive each S1–S6 assertion's
  correctness from the interface contract (that is CriticStrictChecker's lane). A checker bug
  that makes both runs identically green would pass here; the base-revision 0/6 control bounds
  but does not eliminate that risk.
- I did not re-run the C1 counter (c1_reason_count.py 14/14) — RerunC1Counter's item.
- Tooling: no tool installed or upgraded this seat (none needed).
