# ReviewCLI — r25 C1 packet CLI operability check

Milestone: r25-falsify-accessibility-packet · Axes: operability, freshness · Lane: leaf, read-only production.

## Verdict

**Not falsified.** All three assigned invocations behave as the contract says. The `--json` run returns `verdict: "clean"` with 55/55 criteria accepted and no findings. Every output, including selftest and usage-error output, carries `websiteConformance: "not-assessed"`. No production file was edited, no website/browser/r24 command was run, and no tools were installed.

## Environment (freshness)

- Repo HEAD at run time: `9f62cda0a6b71a9c0c86d2088f01673f25787715` (contract `base` is `6883f1d5…`; HEAD has moved past base).
- `git status --porcelain` reported no changes on the script, cards, population or source snapshot.
- Interpreter: Python 3.14.8, run with `-B`. No environment overrides.
- Input digests (SHA-256):

| File | SHA-256 |
|---|---|
| `scripts/accessibility_packet.py` | `581b2080cefd75b86a7d7ccfda6905f8f9dce5b65db67fd69fa39bbf2d5736a8` |
| `corpus/knowledge/accessibility-review-cards.json` | `504ddb098426cb59ceb50a8582b9eae536de13435d6ad8a79a50e74cbcc7332d` |
| `.ufo/waves/round-25/population.json` | `4751dc24db2e3698c2b276bb81bff57412c8fbf6c1c0a62f1aa2ad9e0f903058` (equals pinned `POPULATION_SHA256`) |
| `.ufo/waves/round-25/source-wcag22.html` | `6e3c5fe397257cae509a2fb4752b73062cf8cbeb92c2cec618989b17e4cf7057` (equals pinned `SOURCE_SHA256`) |

## Assigned checks (exact observed results)

Commands were run from the repo root. `<root>` stands for the kake-shokunin checkout.

### 1. `python3 -B scripts/accessibility_packet.py --root <root> --json`

- Exit **0**. stderr empty. stdout is 2973 bytes, one JSON line, SHA-256 `db94eca25c42f309aedbf08142eb61ff5650bbbf8236f9af2487d54c8497d200`.
- Top-level keys: `accepted, criteria, expected, findings, schema, verdict, websiteConformance`.
- `schema: "kake-accessibility-packet-v1"`, `verdict: "clean"`, `expected: 55`, `accepted: 55`, `findings: []`, `websiteConformance: "not-assessed"`.
- `criteria`: 55 rows, 55 unique ids. Each row has exactly the keys `{accepted, findings, id}`. All rows have `accepted: true, findings: []`. The id order matches `population.json` order exactly (1.1.1 … 4.1.3).
- Cross-check of the inputs: 55 cards, and every card `status` is `not-assessed`. The population has 31 Level A and 24 Level AA criteria (55 total).

### 2. `python3 -B scripts/accessibility_packet.py --selftest`

- Exit **0**. stderr empty. SHA-256 `cd613ea891f26c11313a0d16546c0bc034f58c5c50b461f0755caa38b6eee129`.
- Exact stdout: `{"failures": [], "passed": 16, "schema": "kake-accessibility-packet-v1", "selftest": true, "total": 16, "websiteConformance": "not-assessed"}`

### 3. `python3 -B scripts/accessibility_packet.py --unknown-option`

- Exit **64** (EX_USAGE). stderr empty. SHA-256 `ca447d11fbdf69d749440435c4dd29621797e6ba2c08918fe854b65d4315511d`.
- Exact stdout: `{"accepted": 0, "criteria": [], "expected": 55, "findings": ["usage"], "schema": "kake-accessibility-packet-v1", "verdict": "could-not-evaluate", "websiteConformance": "not-assessed"}`

## Static confirmation: `websiteConformance` is always `not-assessed`

These findings come from source review of `scripts/accessibility_packet.py`. They are observed in code, not inferred.

- The value has only two producers, and both hard-code the literal `'not-assessed'`: `result()` (line 31) and the selftest output dict (line 148). No code path builds the key any other way.
- `main()` (lines 161–173) always prints the output of either `result()` (usage error, line 169), `selftest()`, or `load()`. `load()` returns `result()` on every branch: `snapshot_tampered`, `input_invalid`, or via `validate()`, which returns only `result()`.
- `load()` checks both pinned SHA-256 digests before parsing. It catches `OSError`, `UnicodeError` and `ValueError` and turns them into `input_invalid` with exit 2.
- `clean` (line 92) requires all three of: `accepted == 55`, no findings, and `len(cards) == 55`. So `clean` attests packet structure only. The module docstring says the same: "Validate review-packet readiness, never a website's WCAG conformance."

## Operability observations (no defect against the C1 claim)

1. **`--json` has no effect.** It is declared (line 164) but `args.json` is never read; output is always JSON. Harmless, but the flag suggests a non-JSON mode that does not exist.
2. **Usage errors drop argparse's message.** `Parser.error` raises `UsageError`, and the message is discarded. The caller sees only `findings: ["usage"]` with exit 64 and nothing on stderr, with no hint of which option was rejected.
3. **[INFERENCE, not run because it was not assigned]** `--help` goes through argparse's help action, which prints plain text and exits 0. It does not go through `error`, so it would not emit JSON. This is the one CLI path that does not produce schema output.
4. **Selftest coverage gaps (static).** The 16 cases cover `validate()` only. These paths are not exercised:
   - `load()` and its `snapshot_tampered` branch
   - the `fields_mismatch` finding
   - global `metadata_mismatch` from an extra card with an unknown id
   - global `input_invalid` from a non-dict card
   - the `population_invalid` branches
   - the exit-64 usage path

   The real-data run and run 3 above exercise the pristine `load()` path and the usage path. The other paths have no automated check.
5. **[INFERENCE]** A Python exception other than the three caught in `load()` would print a traceback with no JSON. Reviewing `validate()` found no input-reachable path to one: types are guarded before `.strip()`, `re.escape` is used on quotes, and non-dict cards are bucketed as `input_invalid`.

## Remaining unknowns

- Whether `.ufo/waves/round-25/measure.py`, the contract measurement, agrees with this CLI's verdict. Not assigned and not run.
- The quality of criterion card content beyond the structural checks the tool enforces (quote grounding, 6–25 word length, non-empty prose). Out of scope for a CLI operability lane.

## Tooling

None installed or updated.
