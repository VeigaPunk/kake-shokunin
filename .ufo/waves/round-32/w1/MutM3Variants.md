# MutM3Variants — which round-31 m3 variants does the new P6 spec kill?

Seat: KakeR32.MutM3Variants (mutation tester, leaf). Axis judged: operability. Milestone r32-build.
Target: the round-31 m3 variants m3b, m3c, m3d, m3e, m3f, m3g, defined in
`.ufo/waves/round-31/a2-w2/MutRunnerGuards.md`, section "Attribution of the m3 survivor".

## Result

**The P6 spec kills four of the six variants (m3b, m3c, m3e plus m3 itself); m3d, m3f and m3g survive.**
The declaration's disclaimer about m3d/m3f is **accurate but incomplete**: m3d and m3f do survive, exactly as
disclaimed — but so does **m3g**, which the declaration never mentions. m3g removes the gate-side
`GIT_CEILING_DIRECTORIES` ceiling only and is not killed by any committed instrument, exactly like m3d/m3f.
The disclosed limit is worded "The Git-pin mutants m3d/m3f stay unprobed alone; they are not claimed"
(`SCORECARD.md:1037-1038`); the round-31 report's own table lists **three** survivors in that family
(m3d, m3f, m3g), so the disclosure under-counts by one.

The P6 spec (`scripts/fixtures/citing-set-hostile/P6-commit-before-init/hostile.json:23`) adds
`reason_contains: "needs an earlier 'git_init'"`, which is what converts the reason-only kills into
instrument-level kills for the whole git_init-requirement family.

## Variant table (runner copy at 285abcad632e3c1c57bb402232e7d218054db383)

Pristine runner sha256 `7c95a18e4621ca6c4f0085eb9d208a0f1e6a1211989e51dd0c733ee1488b8969`
(`scripts/citing_set_selftest.py`; L1 guard at line 363, L2 at line 490, setup ceiling line 443,
`git_command` pin lines 447-451, gate ceiling line 711).

| variant | layers removed | hostile exit | failing specs | benign 45 | verdict |
|---|---|---|---|---|---|
| m3 | L1 load-time guard only | **1** | **P6-commit-before-init** (`reasonChecks h6` false; reason "case setup failed: git_commit needs the repository created by git_init") | 0 failed | **KILLED** |
| m3b | L1 + L2 | **1** | **P6-commit-before-init** (`reasonChecks h6` false; reason "setup command failed (128): fatal: not a git repository: .../h6/.git") | 0 failed | **KILLED** |
| m3c | L1 + L2 + setup pins | **1** | **P3-commit-without-init** and **P6-commit-before-init**; `victimUnchanged: false` on both | 0 failed | **KILLED (harm)** |
| m3d | setup pins only | **0** | none | 0 failed | **SURVIVED** |
| m3e | L1 + L2 only (pins kept) | **1** | **P6-commit-before-init** (`reasonChecks h6` false) | 0 failed | **KILLED** |
| m3f | setup pins + gate ceiling | **0** | none | 0 failed | **SURVIVED** |
| m3g | gate ceiling only | **0** | none | 0 failed | **SURVIVED** |

m3b and m3e are the same edit set (both remove L1 and L2, keep the pins); they differ only in the marker
comment, and their verdicts match.

Detector baseline (pristine, must be green before any mutant counts): hostile selftest exit 0, 6/6 specs
pass, `reasonChecks h6` true, `victimUnchanged` true everywhere; benign 45 cases, `failed: 0`.

Declared C1 counter `.ufo/waves/round-32/c1_m3_probe.py` agrees: at `285abcad` `killed 1`, `guard_ok true`,
pristine exit 0, mutant exit 1, benign 45/0; at base `a0b0dff` `killed 0`, `guard_ok true`.

## Does the declaration's m3d/m3f disclaimer hold?

Accurate as far as it goes. Measured at the tip: m3d and m3f both give hostile exit 0 and pass the
round-31 counter 5/5 with control K1 true, so they are indeed unprobed and correctly not claimed.
Two gaps in the disclosure:

1. **m3g is unprobed too and is not named.** It gives hostile exit 0 and passes the round-31 counter 5/5
   (K1 true). The round-31 report's own attribution table lists m3d, m3f and m3g as the three survivors of
   the pin family; the round-32 disclosure names only two.
2. **The runner docstring claim is now stale in one clause.** `scripts/citing_set_selftest.py:83-86` says
   "The Git pins named above (--git-dir/--work-tree, GIT_CEILING_DIRECTORIES for setup and gate) are not
   separately probed: a runner without them still passes the hostile selftest and the round-31 C1 counter."
   The pins part still holds (m3d, m3f, m3g all pass both). But the sentence sits next to "The hostile specs
   probe five routed shapes (N1, N2, N3, N5, N6)" — there are now **six** spec directories
   (P1..P6) at the tip, and the P6 spec does probe the git_init requirement, which the docstring does not
   mention. The count and the coverage list are both out of date.

## Advisory note (no contract change proposed)

P6 kills m3b and m3e for the *right* reason but with the same shape as m3: the refusal reason text changes,
not the harm. In m3b/m3e the shape is still refused by the Git pins (the runner reports "not a git
repository"), and `victimUnchanged` stays true. The kill is a **reason-text** kill, not a harm kill; only
m3c produces actual harm (`victimUnchanged: false`). The P6 spec therefore pins the *load-time layer*
specifically, which is what the round-31 routed item 2 asked for, but it inherits the round-31 finding that
the git_init requirement has no harm-based fixture of its own.

## Commands (exit codes)

- `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin <sandbox>/clone` + `checkout -q 285abcad...` -> 0.
- pristine hostile selftest -> 0 (6/6 specs pass); pristine benign 45 -> 0 (`failed: 0`).
- `python3 -B mutate_m3_variants.py` -> 0; m3/m3b/m3c/m3e hostile exit 1 (P6 and, for m3c, P3 failing),
  m3d/m3f/m3g hostile exit 0; lane runner sha256 unchanged before and after
  (`7c95a18e4621ca6c4f0085eb9d208a0f1e6a1211989e51dd0c733ee1488b8969`).
- `python3 -B benign_variants.py` -> 0; all eight runs (pristine + 7 variants) exit 0, 45 cases, 0 failed.
- `python3 -B .ufo/waves/round-32/c1_m3_probe.py --rev 285abcad...` -> 0 (`killed 1`, `guard_ok true`);
  `--rev a0b0dff...` -> 0 (`killed 0`, `guard_ok true`). Read-only against the lane repo.
- round-31 counter `.ufo/waves/round-31/c1_sandbox_probes.py` on sandbox-only mutant commits
  (m3, m3d, m3f, m3g) -> exit 0, 5/5 probes, control K1 true in every case.

## Restoration evidence

The lane was never written: every variant was a separate file under `<sandbox>/mutants/`, and the lane
runner's sha256 is `7c95a18e...b8969` before and after (unchanged). The sandbox clone was committed only
inside the sandbox for the round-31 counter runs and was restored with
`git reset --hard 285abcad...`; `git status --porcelain` in the sandbox clone is empty and the runner there
hashes to the pristine value. No git add/commit/stash/checkout/reset ran in the lane repo; no jj command
ran anywhere; no network fetch; no owned web property was contacted.

## Evidence pointers

- Sandbox `/fast/scratch/hyaku/kake-r32/w1/MutM3Variants/`
- `m3-variant-results.json` (per-variant exit, failing specs, reason checks, victim flags, hashes)
- `benign-results.json` (per-variant 45-case benign runs)
- `h-base.json` (pristine detector baseline), `h-m3.json` .. `h-m3g.json` (per-variant hostile output)
- `counter-285abcad...json`, `counter-a0b0dff...json` (declared C1 counter receipts)
- `r31counter-m3.json`, `r31counter-m3d.json`, `r31counter-m3f.json`, `r31counter-m3g.json`
- `mutate_m3_variants.py`, `benign_variants.py` (drivers, in the sandbox)
- Lane citations: `SCORECARD.md:1033-1038` (disclosed limits), `scripts/citing_set_selftest.py:363` (L1),
  `:490` (L2), `:443` / `:447-451` (setup pins), `:711` (gate ceiling), `:83-86` (docstring),
  `scripts/fixtures/citing-set-hostile/P6-commit-before-init/hostile.json:23` (`reason_contains`)

## What I did not verify

- The mutants are runner-only edits; I did not mutate `scripts/citing_set.py` (the gate) or the specs.
- I did not re-derive the L1's after-receipts; my counter run is my own measurement, not theirs.
- I did not test whether a per-layer harm fixture for the git_init requirement would close the
  reason-only gap in m3b/m3e — that is a design question for the L1, and the contract is unchanged here.
- The lane tip moved past 285abcad during my run (`d061f38`); `git diff 285abcad..HEAD -- scripts/` is
  empty, so the runner and the P6 spec are identical at the tip and every verdict above holds there too.
