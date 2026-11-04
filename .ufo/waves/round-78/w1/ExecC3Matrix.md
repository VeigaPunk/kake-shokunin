PASS — committed carrier 82c3d02c39d16ae99c6cd34238fa3ec6ea089fb9: C3 met=true, exit 0.

## Deliverables
Axes: C3 operability/capability; preserve calibration/freshness gates.
Changed only round-78/c78_meta_robots_matrix.py, cases/ (36 frozen underscore ids), consts/ (four controls), controls/after-c3-matrix.txt and this seat's w1 report/evidence. Did not edit scripts/meta_robots_audit.py. No installs. No LSP facility was mounted; no symbol refactor was required.

- derivations.md:1 maps each case to contract/amendments 1–4 and its exact expected JSON. The fixed population is amendment 3 C4; amendment 4 overrides finding-case exits. g20 is retired; g34 intentionally lacks page.html; g35 duplicates a check id.
- Counter compares exit/effective/findings (faults: exit/error), rejects missing/extra IDs as case_set_mismatch, extracts the tool via git show from the requested revision, and enforces the tool's final selftest line P==T>=40.
- Input isolation copies only page payload and a no-expect manifest into random opaque scratch input/cwd, neutralizing check IDs/URLs. The oracle stays solely in the matrix. A sibling-expect echo adversary must fail, independently of the four constants.

## Exact retained evidence
controls/after-c3-matrix.txt:1 retains the full absolute-path command and output, rc=0:
`C3v1 revision=82c3d02c39d16ae99c6cd34238fa3ec6ea089fb9 cases=36 decided=36 correct=36 wrong=0 constants_failed=4/4 met=true`
Tool selftest: 94/94, exit 0. Case set: missing=[] extra=[]. Sibling-expect control rejected (true).
Tool blob ff0a9df0909428c1c7d5a498a157226ef2e4aa0a; SHA-256 886e88618f7064fb32b95f469ce825bd405b5ae943ba3e100bc0c645cf560ba3.
Case aggregate SHA-256 2ee1dea32d6a10bb1e48059e17ae3396864b773a7e8a89c4367ae93b1614baa2.

matrix-selftest.txt:1 retains exact command: 16/16, exit 0. Includes effective-only/finding-only differences and an integration fixture removing g16, requiring case_set_mismatch/metfalse.
constant-failures.txt:1 lists every failed ID from the same isolated runner: always_clean 32/36; empty_findings_real_exits 8/36; naive_substring 25/36; report_every_id 36/36. The committed-carrier receipt independently records those same failure counts.
sibling-control.txt:1 retains the separate sibling-label probe: rejected on 36/36 cases, control experiment rc=0.
artifact-sha256.txt:1 records retained artifact digests. Counter SHA-256 2fccf1946a2f8f7cb292ef77743bcd4bf1d5e9ac10eab397e2c44d070f6ec9e0.

## Limits / cleanup
No blockers. No build/lint/formatter run. Prescribed matrix, selftest and negative controls only. Fixed population does not establish every RFC822 zone terminal, timezone-offset merging, http-equiv-only behavior, or multi-finding ordering; the sequence-vs-sorted finding mutant survives the single-finding population and remains a stated limit. RFC850 is explicitly unimplemented. No cases/tool were edited after the carrier.
Superseded reference scaffolding removed. All seat scratch removed before yielding; no fleet-root or external substrates modified. Earlier pre-amendment experiments and absent-tool run were superseded, not represented as current after-state evidence.

Self-evaluation: accuracy4 (fixed-population limits above); completeness4 (all assigned artifacts, no broader semantic proof); clarity4 (derivations preserve the amendment chain); actionability4 (exact command retained); conciseness4 (per-case detail separated). Overall4.0. Highest-impact future improvement is a newly frozen population for multi-finding ordering, not widening this scored matrix. Would the user agree? Evidence is bounded to the measured carrier.
