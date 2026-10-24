# MutM3Variants — which round-31 m3 variants does the new P6 spec kill?

Seat: KakeR32.MutM3Variants (mutation tester, leaf). Axis judged: operability. Milestone r32-build.
Target: the round-31 m3 variants m3b, m3c, m3d, m3e, m3f, m3g, defined in
`.ufo/waves/round-31/a2-w2/MutRunnerGuards.md`, section "Attribution of the m3 survivor".

## Result

**The P6 spec kills four of the six named variants (m3b, m3c, m3e, plus m3 itself); m3d, m3f and m3g survive.**
The declaration's disclaimer about m3d/m3f is **accurate but under-counts**: m3d and m3f do survive, exactly
as disclaimed — but so does **m3g**, which the declaration never names. m3g removes the gate-side
`GIT_CEILING_DIRECTORIES` ceiling only and is not killed by any committed instrument, exactly like m3d/m3f.
The disclosed limit is worded "The Git-pin mutants m3d/m3f stay unprobed alone; they are not claimed"
(`SCORECARD.md:1037-1038` at both the assigned rev and the current tip); the round-31 report's own attribution
table lists **three** survivors in that family (m3d, m3f, m3g), so the disclosure under-counts by one.

The P6 spec (`scripts/fixtures/citing-set-hostile/P6-commit-before-init/hostile.json:23`) adds
`reason_contains: "needs an earlier 'git_init'"`, which is what converts the reason-only kills into
instrument-level kills for the whole git_init-requirement family.

## Variant table

Measured on a copy of the runner at the assigned rev `285abcad632e3c1c57bb402232e7d218054db383`
(runner sha256 `7c95a18e4621ca6c4f0085eb9d208a0f1e6a1211989e51dd0c733ee1488b8969`; L1 guard line 363,
L2 line 490, setup ceiling line 443, `git_command` pin lines 447-451, gate ceiling line 711) and re-measured
on the current lane tip `df31d30604ddb01d2e6210aca27a2420f4afe69d` (runner sha256
`7a6365e0e72fa513136d433b4dc3d382c8ca4812076e52a49836668f1c68827f`). **Verdicts are identical at both.**

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
comment, and their verdicts match. The layer names are the round-31 report's: L1 = load-time guard in
`load_case_setup`, L2 = apply-time re-check in `apply_setup`, L3 = the Git pins.

Detector baseline (pristine, must be green before any mutant counts): hostile selftest exit 0, 6/6 specs
pass, `reasonChecks h6` true, `victimUnchanged` true everywhere; benign 45 cases, `failed: 0`.

Declared C1 counter `.ufo/waves/round-32/c1_m3_probe.py` agrees at both revs: at `285abcad` and at the
current tip `df31d30` -> `killed 1`, `guard_ok true`, pristine exit 0, mutant exit 1, benign 45/0; at base
`a0b0dff` -> `killed 0`, `guard_ok true`.

## Is the declaration's m3d/m3f disclaimer accurate?

Accurate as far as it goes. Measured at both revs: m3d and m3f give hostile exit 0 and pass the round-31
counter 5/5 with control K1 true, so they are indeed unprobed and correctly not claimed. Two gaps:

1. **m3g is unprobed too and is not named.** It gives hostile exit 0 and passes the round-31 counter 5/5
   (K1 true) at both revs. The round-31 report's own attribution table lists m3d, m3f and m3g as the three
   survivors of the pin family; the round-32 disclosure names only two. The disclosure is not wrong — m3g is
   also "not claimed" — but it does not say that the whole pin family (three variants) is still open.
2. **The runner docstring was stale at the assigned rev and a sibling fixed it during this wave.** At
   `285abcad` the docstring said "The hostile specs probe five routed shapes (N1, N2, N3, N5, N6)" and did
   not mention P6 at all, while six spec directories (P1..P6) existed. The current tip `df31d30` corrects
   this ("and, since round 32, which layer refuses a ``git_commit`` with no earlier ``git_init`` (P6, mutant
   m3: ...)"), so that finding is closed by the landed repair; I record it only to note it was real at the
   assigned rev. The pins sentence in the docstring remains accurate as written and is confirmed here:
   m3d, m3f and m3g all pass both the hostile selftest and the round-31 counter.

## Advisory note (no contract change proposed)

The kill of m3b and m3e is a **reason-text** kill, not a harm kill: under both mutants the shape is still
refused (the case still fails, exit 1, `victimUnchanged` true) — only the reported reason differs, and P6's
`reason_contains` check is what rejects it. This is the mechanism the declaration already discloses
("C1 kills m3 by the refusal *reason* (the load-time message) because m3 is otherwise behaviour-equivalent",
`SCORECARD.md:1033-1035`), and it now covers the L1+L2 removal as well. Only **m3c** produces actual harm
(`victimUnchanged: false` on P3 and P6): the git_init requirement must be gone *and* the Git pins gone before
the shape reaches the victim repository, which is the round-31 attribution finding unchanged. The contract is
unchanged; the coverage of the git_init requirement is now better than at round 31, and the coverage of the
Git pins is still open in all three variants.

## Commands (exit codes)

- `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin <sandbox>/clone` + `checkout -q 285abcad...` -> 0.
- pristine hostile selftest -> 0 (6/6 specs pass); pristine benign 45 -> 0 (`failed: 0`).
- `python3 -B mutate_m3_variants.py` -> 0 at `285abcad`; m3/m3b/m3c/m3e hostile exit 1 (P6 failing, plus P3
  for m3c), m3d/m3f/m3g hostile exit 0; lane runner sha256 unchanged before and after.
  Re-run at the tip `df31d30` -> 0, **identical verdicts**.
- `python3 -B benign_variants.py` -> 0 at both revs; all runs (pristine + 7 variants) exit 0, 45 cases,
  0 failed.
- `python3 -B .ufo/waves/round-32/c1_m3_probe.py --rev 285abcad...` -> 0 (`killed 1`, `guard_ok true`);
  `--rev a0b0dff...` -> 0 (`killed 0`, `guard_ok true`); `--rev df31d30...` -> 0 (`killed 1`, `guard_ok true`).
  Read-only against the lane repo (`git archive`).
- round-31 counter `.ufo/waves/round-31/c1_sandbox_probes.py` on sandbox-only mutant commits
  (m3, m3d, m3f, m3g) at both revs -> exit 0, 5/5 probes, control K1 true in every case.

## Restoration evidence

The lane was never written: every variant was a separate file under `<sandbox>/mutants/`, and the lane
runner's sha256 is unchanged before and after each sweep. The sandbox clone was committed only inside the
sandbox for the round-31 counter runs and was restored with `git reset --hard <rev>`;
`git status --porcelain` in the sandbox clone is empty and the runner there hashes to the pristine value for
that rev. No git add/commit/stash/checkout/reset ran in the lane repo; no jj command ran anywhere; no network
fetch; no owned web property was contacted. The only file written in the lane is this report.

## Evidence pointers

- Sandbox `/fast/scratch/hyaku/kake-r32/w1/MutM3Variants/`
- `m3-variant-results.json` (rev 285abcad) and `m3-variant-results-tip2.json` (rev df31d30): per-variant
  exit, failing specs, reason checks, victim flags, mutant hashes
- `benign-results.json`: per-variant 45-case benign runs
- `h-base.json` (pristine detector baseline), `h-m3.json` .. `h-m3g.json` (per-variant hostile output)
- `counter-285abcad...json`, `counter-a0b0dff...json`, `counter-tip2.json` (declared C1 counter receipts)
- `r31counter-m3.json`, `r31counter-m3d.json`, `r31counter-m3f.json`, `r31counter-m3g.json` (rev 285abcad);
  `r31c2-m3d.json`, `r31c2-m3f.json`, `r31c2-m3g.json` (rev df31d30)
- `mutate_m3_variants.py`, `benign_variants.py` (drivers, in the sandbox)
- Lane citations: `SCORECARD.md:1033-1038` (disclosed limits), `:1069` ("Git-pin half of routed item 2
  (m3d/m3f) stays open"), `scripts/citing_set_selftest.py:363` (L1), `:490` (L2), `:443` / `:447-451`
  (setup pins), `:711` (gate ceiling), `:83-92` (docstring),
  `scripts/fixtures/citing-set-hostile/P6-commit-before-init/hostile.json:23` (`reason_contains`)

## What I did not verify

- The mutants are runner-only edits; I did not mutate `scripts/citing_set.py` (the gate) or the specs.
- I did not re-derive the L1's after-receipts; my counter runs are my own measurements, not theirs.
- I did not test whether a per-layer harm fixture for the git_init requirement would close the
  reason-only gap in m3b/m3e — that is a design question for the L1, and the contract is unchanged here.
- I did not mutate the P6 spec itself (e.g. drop `reason_contains` and re-measure) to isolate how much of
  each kill is the reason check; the observed reason strings above already show which check rejected.
