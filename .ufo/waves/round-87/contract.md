# Round 87 — frozen predicates

Base: 86ca7803fd964db7ae2a628c7e9048741c78a45f (master).
Two causally separable claims; no receipt or other claim output is an input.

## C1 — calibration (lowest owned axis, 2 HOLD)

Finite gate-agreement self-assessment ledger for the eight gate decisions in the
round-84/85/86 outside spotchecks: mismatches 8 → 0. Predicate: exactly one full
row equal to each expected-ledger.json row, with matching source snapshot digest,
and no additional rows. Missing rows are mismatches. Count.py implements this
predicate. This mines considerthese/2026-10-26.md proposal 4 (gate-agreement ledger).
It does not close D84-2/3/4, certify sources or establish universal calibration.
JSON output at corpus/knowledge/gate-agreement-ledger.json is a self-assessment
artifact, not an admitted domain knowledge entry; the sourced domain entry is C2.
Snapshot inputs are committed here, not live fleet files. A copied lie could pass
this finite counter; independent comparison against the source tables is required.

## C2 — freshness, bounded capability (10 HOLD)

An offline conservative RFC9111 §4.2.3 current-age calculator: absent cases0/17 →
cases17/17 using age-cases.json, plus independent sequential implementation,
selftest and actual property GET trial. Predicate: all seventeen case exits and
all twelve valid-case complete JSON outputs match the fixed oracle.

Tool scripts/cache_current_age.py reads stdin JSON object with required integer
(not bool) date_value, request_time, response_time, now; optional age_value=0.
All are seconds on one epoch clock. date_value may be negative; other inputs are
nonnegative. Require request_time <= response_time <= now. Reject missing keys,
nonintegers, negative age or inverted local time via exit1 and a diagnostic on
stderr. Unknown keys may be rejected. Valid inputs exit0 with only a JSON object:
apparent_age=max(0,response_time-date_value); response_delay=response_time-request_time;
corrected_age_value=age_value+response_delay;
corrected_initial_age=max(apparent_age,corrected_age_value);
resident_time=now-response_time; current_age=corrected_initial_age+resident_time.
All six keys are required; exact integers, arbitrary precision (Python), no
saturation is needed because arithmetic does not overflow. The conservative max
is a chosen allowed profile, not the RFC's sole permitted algorithm. No clock,
network, Date parser, storage/reuse approval, Cache-Control interpretation or
browser behavior is implemented. Missing Date is unsupported; no synthetic
request timing may be relabeled as observed timing.

New source S462 must re-open RFC9111 this round, bounded to §4.2.3 conservative
age arithmetic (not S461's duplicate/lifetime scope). An actual public owned
property GET is captured with request/response times, Date/Age if available,
then tool called offline; missing Date yields an honest could-not-evaluate trial,
not fabricated input. Do not publish or modify a source repository.

## Counting and controls

python3 -B .ufo/waves/round-87/count.py --root . --revision REV --claim c1
python3 -B .ufo/waves/round-87/count.py --root . --revision REV --claim c2 --work /fast/scratch/hyaku/kake-r87/L1/count

Kill: any finite target missed is reported, not narrowed; no frozen bytes amended
after scoring. Pre-freeze do-nothing control is the base tree with neither new
artifact. C1 empty/tampered/altered/duplicate row mutants must fail; C2 constant-zero
and Age-only shortcuts must miss the frozen target. Separate production selftests
cover CLI entry, input rejection and formula terms. No blanket no-harm claimed:
old decoder bytes + historical counterexample bytes are preserved; scores held.
Independent seats attack predicates and semantics; outside closure owns admission.

One v1 wave12 seats: scout1, executor3, scribe3, reviewer2, critic1,
mutation-tester1, connector1; attack4/12. L1 planner; validator forbids planner
role; existing D84-4 operator question remains open, not silently resolved.
Assimilation: none; no merge/kake row append this round. One considerthese proposal
is mined through C1. The inherited r86 raw HTML mirror is scratch disposal debt.
