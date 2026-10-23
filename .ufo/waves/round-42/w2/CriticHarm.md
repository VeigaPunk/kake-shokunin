OVERSTATED — scoped H1–H5 evidence is not unconditional no-harm or retrospective admission of round 41.
Axes: operability (compatibility, CPU, memory, elapsed time, maintenance); freshness (evidence provenance only; no fresh source claim).
Scope: read-only critic; no round verdict, admission, edits to implementation, counter scoring, or other runtime invoked.
Commands executed / exit codes: none / not applicable; only read/grep inspection. Retained results below are not reruns; unrun checks have not passed here.

Receipt-declared identities, not freshly rehashed:
- Landed `scripts/sitemap_audit.py` at `020bc457`: sha256 `914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021`.
- `/fast/scratch/hyaku/kake-r42/shared/tip41.py`: `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d`.
- `/fast/scratch/hyaku/kake-r42/shared/base40.py`: `4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e`.
- `.ufo/waves/round-42/c42_count_v3.py`: `ce2d5a0ca2c3768ce2b1d7b9a57592817d7f16616ee7fb25989e580a70160acc` (build receipts, lines 10–13).

## Per-clause assessment
- H1 HOLDS in retained evidence: `verification/harm/selftest-{build,tip41-235}-py314.txt:1-2` each records `PASS 235/235`, exit 0. The ten new guards include accepted/rejected zone IDs and long-value parity (`scripts/sitemap_audit_selftest.py:997-1036`). This does not make the historical 13 green-on-base fixtures red.
- H2 HOLDS as reported, not independently rehashed here: `SCORECARD.md:3102-3104` records the round-39 sorted-JSON hash `fd985a41…`, tool exit 1. That is equal findings output, not a clean real run.
- H3 HOLDS on the recorded population: all three `verification/build/c1-v3-020bc457-{1,2,3}.json:173-185` ratios are below 2.0 and each receipt records equality 10/10. This prices whole-tool CPU on five shapes, not every URL-check cost or all resources.
- H4 OVERSTATED if read as covering every generated value: `harm/h4_probe.py:190-198` skips the out-of-class values before `validReject`/`newAccept` at :217-222. The zero counters in `verification/harm/h4-020bc457-924141.json:5-20` establish only the filtered population. The H4 reviewer independently confirmed the coverage gap; no missed violation was observed in its samples. Probe exit 0 means receipt written, not predicate satisfied (:31-32,252).
- H5 HOLDS as an observed Python-3.10.22 compatibility guard: `verification/harm/selftest-{build,tip41}-py310.txt:1-2` each records 235/235, exit 0. It establishes neither all Python-3 versions nor a pre-data rule.

## H5 provenance: data-responsive, not a preregistered condition
- WRONG if “before data” includes H5: `SCORECARD.md:3084-3093` expressly says the L1 first saw round-41/scanner 225/225 and regex 0/225 under Python 3.10, then chose the scanner and added H5. “Before counter scoring” is true but is not “before build outcome data.” `LOG.md:1621-1622` needs that qualification.
- The rule is therefore fitted to an observed compatibility difference, without evidence of deceptive intent. The original contract says “Python 3 standard library only” (`round-39/c1-contract.md:11-13`), not an explicit version matrix or specifically 3.10.22.
- This is a defensible stricter safeguard, not a relaxation that turns a failed H1–H4 build into a pass. It excludes a known-incompatible alternative; it does not falsify the scanner's recorded compatibility success. The regex's later met receipt is explicitly information-only (`verification/build/info-execbuildregex.json:3,7,13,173-185`).

## Repricing/admission: honest budget, not zero trade
- HOLDS: the baseline is still round 40, not the slower round 41, and the fixed ceiling is 2.0. Round-41 do-nothing still fails T1/T2/T5 (`SCORECARD.md:3047-3050`); the scanner removes the large measured surcharge.
- HOLDS: round 41 remains rejected-harmed; the new establishment is prospective (`corpus/lessons/round-42.md:50-52`). Reclassifying its 29/13 fixtures cannot amend the old frozen rule (`round-41-verifier-spotcheck.md:100-117`).
- OVERSTATED: “cost repriced” as a claim about all cost. The build retains measured round-40 CPU increases: T3 1.390–1.427 and real-run T4 1.235–1.276 (`verification/build/c1-v3-020bc457-{1,2,3}.json:176-184`). These are disclosed, permitted budget costs, not evidence of zero slowdown.
- A narrower local trade also appears in the independent build seat's report: short real URL 1.93→2.66 microseconds versus tip41 (`w1/ExecBuildIndependent.md:28`, pre-comment-correction tool). That is not a final-byte wall-time measurement, but defeats an inference that every workload became cheaper.

## Unpriced harm and strongest source-level counterexample
- Memory/early rejection [INFERENCE; not executed]: use a manifest `sitemapUrl` equal to `https://a/|` followed by 32,000,000 ASCII `a` characters. Tip41's anchored regex rejects at the early `|` (`shared/tip41.py:76-93`); the scanner first encodes the entire string (:215), then slices the path and translates a full-size mask (`scripts/sitemap_audit.py:163-176`). Original string, encoded bytes, path slice and mask can coexist. This exposes linear extra allocation and full-tail scanning where the old URL predicate rejects on a short prefix; no numerical RSS/latency regression was measured here.
- This reaches the CLI: manifest reading is uncapped (:523-541), and `sitemapUrl` goes directly to `_parse_url` (:573-582); the 2,048-code-point `loc` finding is not a manifest-URL limit. It is not an asserted counter failure.
- Wall time is not priced: the runner records only user+system CPU (`c42_count_v3.py:574-575,630-638`); 600-second timeout and 4-GiB address-space ceiling are absolute containment, not relative elapsed-time/RSS parity. No wall/RSS acceptance result exists in these receipts.
- Maintainability is unpriced, not demonstrated harmed: table generation, percent checks, branch boundaries and fallback host starts replace a compact regex (`scripts/sitemap_audit.py:105-284` versus `shared/tip41.py:73-86`). More code alone is not a defect; preserving subtle legacy rules now requires maintaining this scanner plus downstream `urlsplit`. Differential evidence mitigates this risk but does not measure maintenance cost.

## Smallest safe correction
- Append a precise chronology: H1–H4 prospective; H5 supplemental after compatibility results, before counter scoring. Preserve H5's factual pass without calling it pre-data evidence.
- Limit “no-harm re-established” to the exercised guards and declared CPU budget; disclose remaining CPU costs and unmeasured wall/RSS/maintenance dimensions. Do not retro-admit round 41 or silently tighten/relax the scored rule.
- Repair the H4 measurement coverage separately, rather than interpreting filtered zeros as the unqualified requirement. Any demonstrated resource/maintenance regression is a real operability trade for the canonical judge, not cured merely by H3 passing; this review does not assert such an unmeasured regression occurred.
No installs, updates, network, subprocesses, or subagents. Only this report written; no process tree remains from this seat.
