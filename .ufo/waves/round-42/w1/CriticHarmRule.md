# CriticHarmRule — read-only review
Axes: operability (compatibility, runnable cost); freshness/evidence provenance (not re-scored).
Scope: H1–H4 against round-41 routed defect 1; no admission or round verdict.
Commands/exit codes: none; read/grep/glob inspection only. No code, counter, oracle, judge, or other runtime invoked.

## Per-clause assessment
- **H1 HOLDS prospectively** (`SCORECARD.md:2977-2982`): all new round-42 fixtures are declared guards, with zero change fixtures, and must pass both pinned round-41 bytes and the build. This avoids demanding red-on-base guards. The universal designation is explicit, although individual new fixture IDs/counts are not enumerated yet.
- H1 is achievable by doing nothing: the retained final receipt records 225/225, exit 0 (`.ufo/waves/round-41/verification/build3/selftest-final-on-50287ac6.txt:1-2`). That is appropriate for a parity guard, not independent speed-up evidence. New round-42 guards have not been exercised by this review.
- **H2 HOLDS as a requirement** (`SCORECARD.md:2982-2983`): a fixed retained-real-run output identity is a meaningful guard. Interpret the stated hash as equality of `jq -S .` output, not arbitrary raw JSON formatting. Existing unchanged bytes already satisfy it in the retained record (`corpus/lessons/round-41-verifier-spotcheck.md:68-69`); no new build pass is established.
- **H3 HOLDS, with explicitly bounded scope** (`SCORECARD.md:2937-2945,2983`): five shapes, five alternating samples, descendant-inclusive CPU, median ratios, fixed round-40 comparator, and a 2.0 ceiling price cost before the future build. This allows up to 2x round-40 CPU; it does not assert zero slowdown, a universal runtime bound, or memory/wall-time parity.
- H3 is NOT met by doing nothing: the two retained round-41 receipts fail T1/T2/T5 (details below). No logical contradiction makes the ceiling unmeetable, but no successful implementation or feasibility proof was checked.
- **H4 OVERSTATED as a fully frozen operational check** (`SCORECARD.md:2984-2986`): its acceptance inequalities are coherent and compatible with preserving round-41 judgments, but “the closure's probe method” does not explicitly fix this round's seed(s), sample count, input ordering, or whether the closure's in-class filter applies. The closure reports one finite sample, not all-value equivalence (`corpus/lessons/round-41-verifier-spotcheck.md:85-96`).
- The available original `/tmp/hk41/probe/probe.py:28-34,36-40,59-64` excludes bracket authorities, non-ASCII, and excessive ports from the principal assertions, and consumes unsorted glob order. Its sample size and seed are command arguments. Thus inheriting its method is not a durable, unambiguous run contract. Existing round-41 probe results satisfy both inequalities on the recorded sample, so this too can hold without a speed-up.

## Strongest counterexamples and provenance
- **WRONG if the 29/13 split is offered as a retrospective rule.** `r41_loc_path_pct_7e` uses `http://example.com/a%7eb` and expects clean (`scripts/sitemap_audit_selftest.py:938-941`); it is one of the 13 green-on-base fixtures (`corpus/lessons/round-41-verifier-spotcheck.md:64-72`). Calling it a guard now cannot satisfy the old requirement that every new fixture be red on base.
- The split is descriptively supported by the retained data: base 196/225, 29 named failures, final 225/225 (`.ufo/waves/round-41/verification/build3/selftest-final-on-base-8eb121c8.txt:1-31`; final receipt above). It is a post-data classification, NOT evidence that round 41 declared those classes beforehand.
- **HOLDS: the closure forbids retroactive exemption but permits a new no-harm establishment.** Its lines 104-109 expressly reject exempting guards after data; routed defect 2 at lines 162-164 permits re-establishing under a correctly frozen cost/zone rule. Current `SCORECARD.md:2909,2915-2920` preserves round-41 rejection and describes a new establishment, rather than claiming the old rule passed.
- **OVERSTATED freeze provenance:** `SCORECARD.md:2912` says this section “freezes nothing yet,” while `:2976` says the harm rule is “frozen now.” This leaves two authorities for when H1–H4 become binding. The historical 29/13 description is valid; neither wording can make it pre-data round-41 evidence.
- The declared zone tightening is a real retained tradeoff, not an impossible H4 condition: `http://[fe80::1%é]/a` changes acceptance but is RFC-3986-invalid (`corpus/lessons/round-41-verifier-spotcheck.md:76-78`). H4 does not require keeping every base-accepted invalid value. Its disposition belongs to the canonical judge.

## Smallest safe correction
- Explicitly distinguish the draft C1 predicate from the already-binding harm rule, naming its frozen revision; retain round-41 harmed/rejected status and label the 29/13 split historical observations only.
- Preserve “all new round-42 fixtures are guards”; enumerate/hash actual additions before candidate build results, without converting a red-on-round-41 fixture into a change fixture after seeing results.
- Retain/hash the closure probe and exact input-order/filter/seed/count contract before new build results, then attach a final-byte receipt. This clarifies H4 without changing its acceptance inequalities or pretending the finite probe proves universal equivalence.
- The full routed defect also requires a grounded QUALITY criterion (`corpus/lessons/round-41-verifier-spotcheck.md:159-161`); the inspected `corpus/QUALITY.md:1021-1047` ends at round-41 criteria. H1–H4 alone do not establish that separate deliverable.

## Retained counter evidence only — no tool scored by this seat
- Prefix P = `.ufo/waves/round-42/verification/pre/`; `P/donothing-tip-42001.json:3-14,157-162`: met=false, equalRuns=8/8, T1–T5=[5.367,2.811,1.51,1.222,8.87].
- `P/donothing-tip-42002.json:3-14,157-162`: met=false, equalRuns=8/8, T1–T5=[5.35,2.732,1.334,1.287,9.354]. These are prior L1 runs, not this seat's executions.
- Receipt-declared hashes (not freshly rehashed): `scripts/sitemap_audit.py` / shared `tip41.py` = `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d`; shared `base40.py` = `4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e`.
- Shared tool directory: `/fast/scratch/hyaku/kake-r42/shared/`. Counter `.ufo/waves/round-42/c42_count.py` receipt SHA256 = `7bfc32c5e76dca942208934cfbe89f166eda2776b40e69de987706b4d97dd2a6`.
- No clause is shown contradictory by construction. H1/H2/H4 can pass unchanged; the conjunction cannot do so on these recorded runs because H3 fails. Passing future finite checks would remain scoped evidence, not saturation or universal no-harm proof.
No installs/upgrades, network, subagents, source changes, or processes started. Only this report written.
