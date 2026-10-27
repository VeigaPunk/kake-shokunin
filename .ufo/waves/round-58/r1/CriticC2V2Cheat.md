# CriticC2V2Cheat

## CHEATS:

Build under attack: `c1e39ef3567542b2dc602cc235ed717d6dfbd915`. Baseline run of its committed resolver: 14/14 met at seeds 17, 58, 2026 (all K1–K7 and P1–P7 passed each run). The K IDs differed across seeds as expected.

| Stub/commit | Construction | Tallies (seed 17, 58, 2026) | Met? |
|---|---|---|---|
| Hollow selftest, `0ffe1b0dbfefb3aa8be39e86ffc974d8f7772102` | Started from the committed resolver; replaced `run_selftest()` with a function that only prints `selftest: 59/59` and returns 0. Operational resolver logic remained unchanged. Committed as `scripts/id_resolver.py` with selftest identity. | 14/14, 14/14, 14/14 | Yes, all three |

The gate invokes that selftest for P6 and only checks return code, final `selftest: N/N` line, and N >= 55. The fake tally makes P6 pass without running any of the claimed 59 tests. Since all other behavior remains the correct build, this is a minimal direct demonstration that P6 does not measure selftest execution/non-vacuity.

## HOLES:

- P6 remains a report-string check, not evidence the tool actually ran its selftests. The hollow-selftest mutant passes the full 14-case gate; thus the purported selftest safeguard can be bypassed without changing the resolver's runtime behavior.
- The counter directly executes the committed `id_resolver.py` via Python, so executable-bit/shebang and normal CLI invocation properties are not exercised by this counter. This is a scope limitation, not shown to affect C2's two disclosed false-green defect claims.
- No other wrong-resolver mutant was measured in this pass; the committed resolver's three-seed scores above establish only that the gate remains green on this build.

VERDICT: The committed build meets all 14 cases at three seeds, but P6 can be satisfied by a stub selftest that runs zero cases and prints `59/59`; the smallest safe correction is to make the selftest outcome depend on executed case results (and test the hollow-tally mutant as a failing control), rather than trusting its final printed tally.