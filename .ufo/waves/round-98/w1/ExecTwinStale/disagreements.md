# ExecTwinStale — disagreements (twin vs frozen oracle, C2)

Primary run (deliverable `diff-run.txt`): `python3 gen.py --count 2400 --seed 98`, inputs=2505
(targeted 105, random 2400), disagreements=9.
Command for every row: `python3 twin.py < input` and `python3 frozen/pos-oracle.py < input`,
observed rc listed per row. Full per-input table: `diff-run.txt`. Machine-readable: `disagreements.jsonl`
(note: its `expect` field holds 5000-digit integers; parse with `sys.set_int_max_str_digits(0)`).

Summary of the primary run: **oracle_defects=4, contract_ambiguities=5, twin_defects=0**.

Contract sentences quoted below are from `LANE/.ufo/waves/round-98/stale-contract.md`.

---

## A. oracle-defect — oracle refuses valid 5000-digit integers (4 inputs)

The oracle's stderr for every case below is the Python int-string limit, not a contract refusal:
`invalid_input: Exceeds the limit (4300 digits) for integer string conversion: value has 5000 digits; use sys.set_int_max_str_digits() to increase the limit` (rc=1, stdout empty).
This is an implementation limit leaking out as `invalid_input`.

### A1. `swr-huge-clamped` (targeted)
- Input: `{"response_cc": "stale-while-revalidate=" + "9"*5000, "freshness_lifetime": 0, "current_age": 2147483649, "event": "request"}`
- twin: rc=0 `{"decision": "revalidate", "staleness": 2147483649}`
- oracle: rc=1, stdout empty, stderr = int-limit message above.
- Classification: **oracle-defect**. Contract step 4: "valid only as an unquoted token of 1*DIGIT; values above 2147483648 are clamped to 2147483648". The token is 1*DIGIT, so the value is clamped to W=2147483648; staleness 2147483649 > W → `revalidate`. Twin is correct.
- Also: identical in seeds 1, 2, 3.

### A2. `swr-huge-clamped-inside` (targeted)
- Input: as A1 with `current_age: 2147483648`.
- twin: rc=0 `{"decision": "serve-stale-revalidate", "staleness": 2147483648}`
- oracle: rc=1, int-limit refusal.
- Classification: **oracle-defect**, same sentence. Staleness 2147483648 ≤ clamped W 2147483648 (inclusive boundary) → `serve-stale-revalidate`. Twin correct.
- Also: identical in seeds 1, 2, 3.

### A3. `swr-leading-zeros-5000` (targeted)
- Input: `{"response_cc": "stale-while-revalidate=" + "0"*5000 + "5", "freshness_lifetime": 0, "current_age": 5, "event": "request"}`
- twin: rc=0 `{"decision": "serve-stale-revalidate", "staleness": 5}`
- oracle: rc=1, int-limit refusal (value has 5001 digits).
- Classification: **oracle-defect**. Contract step 4: "valid only as an unquoted token of 1*DIGIT". Leading zeros are DIGITs and the value is 5 ≤ W, so `serve-stale-revalidate`. The oracle already accepts `00012` (match in run), so only the length trips it.
- Also: identical in seeds 1, 2, 3.

### A4. `big-age-staleness-exact` (targeted)
- Input: `{"response_cc": "stale-while-revalidate=5", "freshness_lifetime": 0, "current_age": "7"*5000 (a JSON integer of 5000 digits), "event": "request"}`
- twin: rc=0 `{"decision": "revalidate", "staleness": <the 5000-digit integer 77…7>}`
- oracle: rc=1, int-limit refusal.
- Classification: **oracle-defect**. Contract, input table: `current_age | integer ≥ 0 (same) | JSON booleans and floats refused`. The only refusals the contract lists for integer fields are booleans and floats, so a 5000-digit integer is not a listed refusal. Note: the contract states no magnitude bound; if the L1 reads "integer" as implicitly bounded, reclassify this one row as contract-ambiguity (run count would become oracle_defects=3, contract_ambiguities=6).
- Also: identical in seeds 1, 2, 3.

---

## B. contract-ambiguity — duplicate top-level key (5 inputs, primary run)

All five have the top-level key `"event"` written twice (the generator's duplicate mutation). Twin rc=1 with `invalid_input: duplicate key in top-level object`; oracle rc=0 (last occurrence wins).

Contract sentences: "Input object (unknown keys → refuse)" and the Interface line "reads ONE JSON object on stdin." Neither says what a repeated key does. Twin refuses (my policy, not in the contract); the oracle last-wins. The contract does not decide it, so both policies are defensible and I did not change the twin.

Verified: a scratch-only probe twin with last-wins (`probe-lastwins-twin.py`, receipts in this directory) agrees with the oracle on every such input (see `probe-lastwins-output.txt`).

| label | input (`"event"` duplicated) | twin rc / output | oracle rc / output | classification |
|---|---|---|---|---|
| rand-00260 | `{"response_cc": "private=\"5\",must-revalidate=5,\tpublic=59", "freshness_lifetime": 86400, "current_age": 86406, "event":"request","event": "error", "request_cc": "", "error": 100}` | 1 / refused: duplicate key | 0 / `{"decision": "not-an-error", "staleness": 6}` | contract-ambiguity |
| rand-00367 | `{"response_cc": "Stale-While-Revalidate=1 , Stale-While-Revalidate=2147483648", "freshness_lifetime": 1200, "current_age": 1199, "event":"request","event": "error", "request_cc": "no-cache=00012", "error": 502}` | 1 / refused | 0 / `{"decision": "error-through", "staleness": 0}` | contract-ambiguity |
| rand-01064 | `{"response_cc": "Stale-While-Revalidate=\"\" , Stale-While-Revalidate=100", "freshness_lifetime": 1800, "current_age": 1797, "event":"request","event": "error", "error": 503}` | 1 / refused | 0 / `{"decision": "fresh", "staleness": 0}` | contract-ambiguity |
| rand-01316 | `{"response_cc": "s-maxage=\"5\",\timmutable=2147483648", "freshness_lifetime": 5, "current_age": 4, "event":"request","event": "request", "request_cc": ""}` | 1 / refused | 0 / `{"decision": "fresh", "staleness": 0}` | contract-ambiguity |
| rand-01447 | `{"response_cc": "Stale-If-Error , Stale-If-Error", "freshness_lifetime": 60, "current_age": 58, "event":"request","event": "request", "request_cc": ""}` | 1 / refused | 0 / `{"decision": "fresh", "staleness": 0}` | contract-ambiguity |

---

## C. twin-defects: none

The twin disagreed with the oracle only where the oracle is wrong (A) or the contract is silent (B). Two of my own hand-derived expectations were wrong in the first generator run (`error-503-counts`, `error-504-counts`: I wrote `error-through`; the correct answer is `serve-stale-error`, since staleness 50 ≤ stale-if-error 50 is inclusive). Both implementations returned `serve-stale-error`, so the twin was not at fault. I corrected my expectations and reran. These two were not counted as disagreements and are not defects in either instrument.

Other twin-side failures during authoring: a `sys.set_int_max_str_digits` import ordering slip in gen.py and a stray-indentation slip in gen.py. Both were fixed in the generator; neither touched the twin.

---

## D. Agreed interpretations (no disagreement, but the contract is the only evidence for them)

These are cases where twin and oracle agreed. Agreement does not prove them; the L1 may wish to pin them in the contract:
- Refusal of `shared: null` and `request_cc: null` (contract: "boolean", "string"; nulls not listed).
- Presence of `no-cache`, `must-revalidate`, `proxy-revalidate`, `s-maxage` counts regardless of the value they carry (contract says "carries").
- A request `stale-if-error` that is invalid (quoted or non-digit) falls back to the response value (contract step 4 "absent" convention).
- C1 controls U+0080–U+009F are accepted inside quoted-strings (qdtext `%x80-FF`) and refused outside (contract "a control character → refuse" read as CTL = %x00-1F/%x7F).
- All refusals take precedence over any decision (contract does not state an order).
- `staleness` is reported on not-an-error and on the no-cache/prohibited paths (contract: "staleness is always reported").

## E. Extra seeds (scratch corroboration, not the verdict)

Seeds 1, 2, 3 (3000 random each, same generator, `diff-run-seed{1,2,3}.txt`):
- seed 1: match=3099 disagree=6 (4 oracle-int-limit rows, 2 duplicate-key)
- seed 2: match=3094 disagree=11 (4 oracle-int-limit rows, 7 duplicate-key)
- seed 3: match=3097 disagree=8 (4 oracle-int-limit rows, 4 duplicate-key)
- Across all four runs: the only disagreement families are A1–A4 and B; no new family appeared. `probe-lastwins` on all 34 disagreeing inputs: 18 duplicate-key inputs match the oracle, and the 16 remaining rows are the four 5000-digit inputs where the oracle's refusal is the int-limit (see A). No unexplained row.
