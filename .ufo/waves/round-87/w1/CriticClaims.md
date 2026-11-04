# CriticClaims — round 87 wave 1

Lane-internal adversarial findings only; no admission, scoring, integration or production edits performed.

## Axes and limits

Calibration is the lowest owned axis, **2 HOLD**; freshness is **10 HOLD**; operability is a no-harm surface, **10 unchanged**. The scorecard explicitly calls the old scores bounded historical assessments, not current whole-corpus certification. Eight newly represented historical decisions cannot establish universal calibration or justify a numeric increase.

## C1: meaningful metadata improvement, not new agreement

**Counterexample:** copy expected-ledger.json verbatim to the target while doing no source evaluation. The frozen ledger_errors returns zero with the pinned snapshots. The measured 8→0 is missing/inconsistent ledger rows→complete consistent rows, not eight previously wrong decisions becoming right. All eight outside judgments were already “agree” before this round. Consequently, “gate accuracy rose from 0/8 to 8/8” or “eight discernment mistakes repaired” would be false provenance.

**Independent evidence:** read all three source tables: r84 snapshot lines 71–75 supplies exactly three decisions; r85 lines 69–72 supplies two; r86 lines 87–91 supplies three. All eight expected items, decisions and agreement labels match those tables. All three retained snapshot SHA256s match the frozen expected digests (probe.json). No fabricated agreement was found. r84's admit/mined is legitimately normalized to admit; the actual decision was not inverted.

**Smallest safe correction:** preserve the frozen predicate and describe the deliverable as “eight historical gate decisions now have source-pinned, independently table-checked self-assessment metadata; ledger mismatches 8→0.” It is more than a raw quota because full row identity, decisions, outside judgments, exact cardinality and snapshot digests are checked. It remains a finite transcription/assessment ledger, not newly demonstrated source truth, statistical reliability or future drift detection. Proposal 4 at considerthese/2026-10-26.md:32 motivates historical gate-agreement tracking; this eight-row artifact does not implement a standing longitudinal watcher. Whether this bounded metadata move satisfies the lowest-axis obligation belongs to the canonical judge, not this seat.

## C2: demonstrated counter under-enforcement

**Counterexample (exercised):** for each of the twelve valid oracle outputs, replace every integer value with float(value). Python object equality in the frozen counter accepts **12/12**. Replacing all six zeros in case 1 with JSON false also compares equal. This violates the contract's exact-integer output requirement, although the finite counter is green under its actual implementation. See probe.json. This was an in-process bounded comparison probe, not a measured candidate revision or a seventeen-case CLI run.

**Additional source-inspected bypasses:** the five invalid fixtures check exit=1 only, so no stderr diagnostic is required by the counter, and arbitrary stdout is ignored. All twelve valid fixtures explicitly provide age_value, so default-zero handling is not exercised on valid input. A table keyed to the seventeen known inputs can satisfy the finite target without general age arithmetic. The constant-zero (2/17) and Age-only (3/17) controls defeat those two shortcuts, not lookup-table implementations or all nonwork. Neither shortcut receipt records its invocation/exit, so those details cannot be independently recovered from those JSON summaries.

**Impacted axes:** freshness capability evidence; calibration if green is presented as full conformance. **Smallest safe correction now:** do not alter frozen counter/fixtures after scoring; retain these defects and independently inspect candidate arithmetic and explicitly exercise exact output types, default age, error diagnostics and fresh unseen inputs in the separate authorized production selftests/review. Never infer these obligations from a finite green. If implementation evidence is absent or fails, report that limitation rather than silently narrowing the declared claim. A future instrument can use type(value) is int and diagnostic assertions, but not as a replacement for this round's frozen result.

## Source and adapter boundaries

Reopened https://httpwg.org/specs/rfc9111.html independently with the reader this round. §4.2.3 supports all six frozen equations, age_value=0 when absent, and the chosen conservative max. It explicitly says corrected_age_value MAY instead be used as corrected_initial_age; the max profile is permitted, not universally mandated. §4 separately imposes request/URI/Vary/validation/reuse constraints, so age alone is not permission to store, serve, publish or reuse.

Integer-epoch JSON, nonnegative local timing, explicit rejection of booleans, arbitrary-precision arithmetic and unsupported missing Date are local adapter choices, not blanket RFC requirements. No parser, clock observation, browser behavior or live policy diagnosis follows. Trial timing must come from the actual request/response; reused historical observations or synthetic timing cannot be labeled newly observed. Missing Date must remain an honest could-not-evaluate trial.

Existing S456 includes a broader §4.2.3 age-estimate context, but S461 is explicitly duplicate/explicit-lifetime rules, not this calculator. S462 is therefore a same-document, newly reopened scoped source slice, not independent corroboration or a wholly new RFC discovery. No S462 row was present when this seat read the registry; source admission, final provenance trio and actual owned-property GET trial remain other seats/L1 evidence, not findings certified here. PROVINCE preserves publisher-side interpretation, browser execution adjacency and operator-gated publication; no sibling authority should be absorbed by the calculator.

## Controls, separability and no-harm

- Read retained base controls: base 86ca7803fd964db7ae2a628c7e9048741c78a45f gives C1 mismatches=8, met=false, exit1; C2 cases=0/17, met=false, exit1. Their exact commands are recorded in the respective control files. These were evidence-read, not rerun. The actual counter treats missing artifacts as red; do-nothing cannot meet either target.
- C1 reads only the ledger plus named snapshot blobs; C2 reads only its script plus fixed oracle. Neither consumes the other claim's output or a success receipt. The r86 cross-claim/self-receipt cycle is absent in the frozen implementation. That structural improvement does not certify later implementation or trial receipts.
- Preserving prior decoder and historical counterexample bytes is required; this read-only seat did not compare integrated production revisions and makes no blanket no-harm claim. Independent integration preservation evidence is still necessary.
- D84-2 remains general defect-instrument soundness debt, including prose/string/exit-token gaps; this ledger does not fix that instrument.
- D84-3 remains general semantic/input-dependence debt. Retain the Referrer-Policy failing witness and canned-output limitation; current-age arithmetic cannot approve the old classifier or response-policy equivalence.
- D84-4 remains open: literal dispatched L2 planner requirement versus validator planner prohibition. L1 planner plus scout data-walk is disclosed mitigation, not resolution. r84 snapshot lines 95–98, r85 lines 88–92 and r86 lines 111–118 establish these continuing limits.
- r86 mirror disposal and pre-SOURCES quarantine ordering are separate procedural obligations, not automatically satisfied by either finite target. No assimilation or merge-row credit is appropriate.

## Commands, receipts and limits

Executed shell commands (both exit0):

```sh
mkdir -p /fast/scratch/hyaku/kake-r87/CriticClaims /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/CriticClaims
rmdir /fast/scratch/hyaku/kake-r87/CriticClaims
```

Executed one stdlib Python Eval cell successfully (tool success; no process exit code): loaded frozen count.py using importlib.util.spec_from_file_location, hashed the three snapshots, called ledger_errors(EXPECTED, read_bytes), and evaluated `{k: float(v) for k,v in case['output'].items()} == case['output']` for all valid cases plus `{k: False for k in CASES[0]['output']} == CASES[0]['output']`. Exact results retained at /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/CriticClaims/probe.json. No main() invocation, candidate execution, base rerun, builds/lints/general tests, clone, git mutation, install, service, provider probe, credential access, browser or production write. Scratch was explicitly created then removed.

This is a frozen-contract/source-table/counter attack, not a final integrated candidate review. Candidate-specific source/trial/selftest/preservation outcomes are not fabricated. Canonical judgment remains outside this seat.

Self-evaluation (review only): accuracy4—counter comparison probe distinguished from CLI proof; completeness4—covers assigned claims/debts/boundaries, not unlanded candidate outcomes; clarity4—bounded findings separated from admission; actionability4—corrections preserve frozen bytes; conciseness4—long report retains reproducibility and limits. Overall4.0. Highest-impact improvement applied: explicit type-loophole result and narrow C1 wording rather than treating finite green as semantic proof.
