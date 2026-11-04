source: S462 — RFC 9111 §4.2.3 Calculating Age — https://httpwg.org/specs/rfc9111.html#age.calculations; opened 2026-11-04; retained source/access evidence .ufo/waves/round-87/w1/ScoutAge/ and w1/ScribeRegistry/source-access.md. S461 retains its separate lifetime/duplicate scope.
verified-at: 2026-11-04 — source reopened by L1, ScoutAge and scribes; implementation and independent review receipts under .ufo/waves/round-87/w1/ExecAge/, ReviewAge/, MutAge/; production revision measurement under controls/after-c2-carrier.txt.
recheck: 180d or source/adapter change; reopen https://httpwg.org/specs/rfc9111.html#age.calculations and compare section 4.2.3 equations; the offline selftest command is item 4 of the checklist below.

# Conservative HTTP current-age arithmetic

This entry holds the Age-arithmetic slice of the round-86 coverage frontier,
not header extraction, cache policy, storage/reuse authorization or browser
behavior. `scripts/cache_current_age.py` reads caller-supplied integer seconds,
never a clock or network. Missing Date or local timestamps are unsupported.

Located quote, §4.2.3 paragraph following the first equation block (8 words):
“The corrected_age_value MAY be used as the corrected_initial_age.” The
following paragraph permits a more conservative maximum in the presence of old
caches that might not insert Age correctly. The maximum below is our chosen
allowed profile, not the RFC's only algorithm, and no old-cache occurrence is
inferred on the observed path.

## Decision table

| Output | Equation | Meaning |
|---|---|---|
| apparent_age | max(0, response_time − date_value) | Date-based estimate; future Date is clamped |
| response_delay | response_time − request_time | Transit interval measured from request initiation |
| corrected_age_value | age_value + response_delay | Received Age, default zero when unavailable, plus transit |
| corrected_initial_age | max(apparent_age, corrected_age_value) | Conservative allowed profile; do not add independent estimates |
| resident_time | now − response_time | Local residence since receipt |
| current_age | corrected_initial_age + resident_time | Conservative age at the supplied current timestamp |

Inputs: one JSON object with required `date_value`, `request_time`,
`response_time`, `now`; optional `age_value=0`. All supplied values must be
integers, not bool/float/string/null. Date may be negative; local times and Age
must be nonnegative. Require request_time ≤ response_time ≤ now. Unknown keys
are rejected. Valid exit0 emits exactly the six integer keys, no stderr;
invalid exit1 emits `invalid_input:` on stderr and no stdout.

One common epoch and integer-second resolution are local adapter conventions.
Python arbitrary precision avoids arithmetic overflow; no unconditional 2^31
cap is applied. This does not abolish RFC overflow rules for fixed-width caches.
The CLI disables Python's decimal conversion digit limit; resource exhaustion
is not covered by the bounded correctness claim. Date text conversion occurs
upstream in the retained trial, not in this tool. Missing Date is not a general
RFC prohibition against processing a response; it is this adapter's boundary.

## Error patterns

- Age alone omits transit, Date dominance and residence; now−Date alone ignores
  received Age. Adding the two independent initial estimates double-counts.
- Treating Python bool as an accepted integer violates the JSON adapter.
- Inventing a missing Date/request time, or clamping an inverted local clock,
  turns an unsupported input into false evidence.
- A computed age, including zero, does not prove freshness or reuse permission.
  RFC §4.2 also requires `freshness_lifetime > current_age`; §4 adds URI/method,
  Vary, directives, validation and other applicable reuse conditions.

## Runnable checklist

1. From the lane root, run:
   `printf '%s\n' '{"date_value":80,"request_time":90,"response_time":100,"now":130,"age_value":5}' | python3 -B scripts/cache_current_age.py`.
   Expected six values in table order: 20,10,15,20,30,50; exit0.
2. Omitted Age with Date60/request45/response60/now75 yields 0,15,15,15,15,30.
3. Missing Date, bool input, negative Age or inverted local time yields exit1
   and `invalid_input:`; inspect each process exit separately.
4. Create explicit TMPDIR and run `--selftest`; the actual CLI is exercised on
   isolated fixtures. Independent evidence is `w1/ReviewAge/fresh-results.json`,
   60 fresh cases; `w1/ExecAge/receipts.json`, 61 CLI fixtures; six actual mutants
   are killed in `w1/MutAge.md`. Counts carry their commands in those receipts.
5. Actual domain handoff: `.ufo/waves/round-87/w1/ExecTrial/trial-record.json`
   retains one public GET, observed Date/Age and times. Replay with
   `python3 -B .ufo/waves/round-87/w1/ExecTrial/retained_trial.py --tool /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/cache_current_age.py`.
   Its observed times share one second and Age0: the all-zero result is a real
   invocation but not a discriminator against constant-zero/Age-only shortcuts.

The frozen counter's 17-case equality is weaker than the complete adapter
contract: Python equality accepts equivalent floats/bools and invalid diagnostics
are not checked. Independent exact-type/diagnostic/default-Age checks and sequential
code review supply separate evidence, not a claim that the frozen counter enforces
those properties. No universal conformance or publishing approval follows.
6. Offline selftest without a fixed scratch path: TMPDIR=$(mktemp -d) python3 -B scripts/cache_current_age.py --selftest; the directory is created by the shell and removed by the operator.
