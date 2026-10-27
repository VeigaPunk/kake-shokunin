# ExecC2GateSelftest

Claim C2, wave-1 attack item: port the round-58 gate selftest (`_stub`, `_base_tool`, `_fixture_lane`,
`_control`, `selftest`) to the 21-case round-59 counter, correct every expected score, add sniffing controls,
and score the gate. No claim measured; no after-state scored.

Deliverable: `.ufo/waves/round-59/w1/ExecC2GateSelftest.files/c59_resolver_cases.py` (sha256
`b8dffd0e…93959710`, 42,905 bytes) — the lane counter plus the ported selftest. The lane file
`.ufo/waves/round-59/c59_resolver_cases.py` was NOT touched (lane bounds: seats write only their own report
and `<Seat>.files/`); the L1/builder integrates the copy.

Method. `git show fd6303ce5c14b3f892dec586297a942ab6e4193b:scripts/id_resolver.py` (1,026 lines) read once and
used as the single substrate: every control is that tool with one textual mutation (`_patch` raises if an anchor
is not unique), so each cheat class is scored on real code and the round-58 `MINI_STUB` re-implementation is
gone. `_stub()` keeps the round-58 flag vocabulary (`fence_drop`, `always_exit_one`, `blanket_dangling`,
`tally`); `_partial_fix`, `_symlink_refuser`, `_dash_dropper`, `_full_fix` are the round-59 controls. Each
control is committed as `scripts/id_resolver.py` of a gate-built fixture lane (106 rows, all cited, P7 floor met
on a fixture; repo `rev-parse --show-toplevel` asserted; commits with `user.name=selftest`), then scored with
the counter's own unmodified `measure()` over the 21 cases. Expected scores were derived from the case specs in
the counter before the run, then asserted per case (`must_pass`/`must_fail`), not fitted to output.

## CONTROLS:

Expected / observed (score out of 21; failing cases in short form):

| control | expected | observed | failing cases |
| --- | --- | --- | --- |
| const_green | 1 | 1 | all but P1 (its fixed green line satisfies P1) |
| fence_drop | 9 | 9 | K1,K2,K3,K6 (fenced rows count) + K8–K14 + P6 |
| always_exit_one | 10 | 10 | K8–K14 + P1,P2,P6,P7 (every exit-0 case) |
| blanket_dangling | 1 | 1 | all but P5 |
| near_miss_p6 (tally 65/65) | 13 | 13 | K8–K14 + P6 |
| tally_liar (tally 66/66) | 14 | 14 | K8–K14 (P6 green on an unearned tally) |
| base_tool (fd6303ce) | 13 | 13 | K8–K14 + P6 |
| partial_fix_k8_k9 | 15 | 15 | K10–K14 + P6 |
| symlink_refuser | 14 | 14 | K8,K9,K10,K11,K13,K14,P6 (K12 passed by sniffing) |
| dash_dropper_any | 1 | 1 | all but P5 (table header's own dashes line empties the registry) |
| dash_dropper_exact | 14 | 14 | K8,K10,K11,K12,K13,K14,P6 (K9 passed by sniffing) |
| full_fix | 21 | 21 | none (`exit=0`) |
| full_fix_no_suite | 20 | 20 | P6 only (seven routes closed, base 59-case suite) |

Two derivations were corrected after inspection, not silently fitted: `dash_dropper_any` was first stated 0/21
and is 1/21 because P5's `--fleet`-absent check runs before any registry parse (so no parser cheat can break
P5); the header table and the spec were corrected with that reason. Everything else matched on the first run.
`full_fix` closes the seven routes on the base tool: comment strip (K8), setext section end (K9),
`os.walk(..., followlinks=True)` plus the existing inside-lane realpath guard (K10), `git ls-tree` modes and
in-tree symlink resolution (K11), registry-symlink refusal (K12), `surrogateescape` path decoding plus
`stdout.reconfigure(errors="backslashreplace")` (K13), repo-toplevel check (K14); its built-in suite grows
59 → 66 with seven real cases so P6 is earned.

## TALLY:

```
  ok   const_green: score=1/21 exit=1
  ok   fence_drop: score=9/21 exit=1
  ok   always_exit_one: score=10/21 exit=1
  ok   blanket_dangling: score=1/21 exit=1
  ok   near_miss_p6: score=13/21 exit=1
  ok   tally_liar: score=14/21 exit=1
  ok   base_tool: score=13/21 exit=1
  ok   partial_fix_k8_k9: score=15/21 exit=1
  ok   symlink_refuser: score=14/21 exit=1
  ok   dash_dropper_any: score=1/21 exit=1
  ok   dash_dropper_exact: score=14/21 exit=1
  ok   full_fix: score=21/21 exit=0 failing=[-]
  ok   full_fix_no_suite: score=20/21 exit=1 failing=[P6_tool_selftest]
selftest: ok (13 controls scored; P7 satisfied on a fixture lane) exit 0
```

Timing, measured: the 12-control run took 10.6 s wall; the 13-control run and the base re-measurement together
13.8 s (python 3.14.8, git only; nothing installed or upgraded). Machine-checked tally and the full per-control
failing lists: `.files/selftest-final.out`.

Do-nothing control re-measured through the ported copy, seed 59:
`C2 resolver-cases 13/21 met=False (met: cases_passed == 21 of 21) … EXIT=1`, failing
`K8 K9 K10 K11 K12 K13 K14 P6` — byte-for-byte the same verdict and failing set as the committed
`controls/base-c2-resolver-cases.txt`. The port therefore did not disturb `measure()`/`case_results()`.
Receipt: `.files/base-measure.out`.

## DIFF:

`.files/ported-vs-v1.diff` is one hunk, `@@ -290,14 +290,423 @@`, on the lane's version-1 counter: the 14-line
`selftest()` stub (`BASE_REV` + the "version 1 stub; exit 2" print) is replaced by 423 lines — the control
constants/patches, `_stub`, `_partial_fix`, `_symlink_refuser`, `_dash_dropper`, `_full_fix`, `_lane_root`,
`_base_tool`, `_fixture_lane`, `_control`, `selftest`. No other line of the counter changes; the module docstring
and the frozen prose are untouched. Integration note: `derive_c59_resolver_cases.py` regenerates this counter from
the round-58 v2 body, so the ported selftest must be applied **after** the last regeneration (or the generator
must carry it), otherwise the stub returns.

## GATE DEFECTS:

1. **P6 is a printed-tally gate.** `tally_liar` prints `selftest: 66/66`, exits 0 and scores 14/21 with P6
   green; P6 cannot distinguish an earned suite from a lie (disclosed in the contract; now demonstrated).
2. **K12 and K14 are reason-blind.** Both assert only `exit 2` plus the absence of a green summary line, so
   `symlink_refuser` (refuse whenever any symlink exists) passes K12 without doing what K12 describes. The gate
   as a whole still catches it (14/21, K10/K11 fail), but neither case alone can. Same class: K9 is passed by
   `dash_dropper_exact` (drop everything after any `---` line) — K9 alone does not prove section-end correctness;
   the crude variant that also fires on `| --- |` is caught hard (1/21).
3. **Satisfiability was never demonstrated (now closed).** Base 13/21 and every round-58-style cheat leave
   K10, K11, K13, K14 failing; with no control above 15/21 an unsatisfiable case would have looked like an
   expected failure in all of them and the selftest would still have printed `ok`. The added `full_fix`
   (21/21, exit 0) now shows all 21 cases passable and doubles as the reachable after-state reference.
4. **P6 floor couples to the tool's private suite.** `P6_FLOOR = 66` vs the base tool's 59 built-in cases:
   `full_fix_no_suite` (all seven routes closed, suite left at 59) scores 20/21, failing only P6. P6 measures the
   suite size, not the routes; the after-state must add ≥7 real cases or it cannot reach 21/21 whoever is right
   about C2. The contract states the floor but not this coupling.
5. **P7 is never exercised against the real lane under `--selftest`** (a fixture lane satisfies
   `ids_cited >= 106`, the round-58 expedient). A P7 that only works on the real lane, or one that is simply
   unreachable, would not be caught by the selftest; only a real measurement tests it.
6. Cosmetic: the counter's own fixture commits (`commit_all`) use `user.name=gate`, while this seat's fixture lane
   uses `selftest`/`selftest@local` per the wave rules; no behavioural difference, noted for provenance.

Risks / limits: P7 in the selftest is fixture-satisfied (defect 5), so the tally proves the 20 other cases and
P7's plumbing, not P7 on the lane; the ported counter lives in `.files/` until integrated; no sibling file, lane
Git/jj state, or the fleet repo was touched. Tooling: none installed or upgraded (python3 3.14.8, git).

VERDICT: Gate selftest ported and green on 13 controls with every expected score derived then matched (base 13/21, partial 15/21, cheating variants 1–14/21, full_fix 21/21), and the port exposes four real gate defects — tally-only P6, reason-blind K12/K14, undemonstrated satisfiability (now closed by full_fix) and the P6-suite coupling — none of which changes the counter's v1 predicate.
