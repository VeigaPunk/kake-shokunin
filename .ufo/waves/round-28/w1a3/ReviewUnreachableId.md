# ReviewUnreachableId — C1 hunk review: `load_population` non-numeric id rejection

Round 28 attempt 3, wave 1. Lane: kake-shokunin. Axes: operability, freshness.
Scope: the single `load_population` hunk in
`git diff 22c1669c1fec83d1a0769de6b9ce686c75657e66 b5d423fc02057f67a6f3a255808313ce40d29069 -- scripts/citing_set.py`
(new lines: `key = id_key(identifier)` then `if key[0] != "n": raise InputInvalid("population_id_unreachable", relative, "population", row=identifier)`).

## Verdict

No defect found in this hunk. It implements exactly what C1 claims and does not
over-reject any committed fixture, frozen r27 population, real corpus population,
or reachable id spelling.

## Findings by severity

### Critical / Major / Minor
None.

### Advisory (no action required)

A1. First-offender-only reporting: the check raises on the first non-numeric row,
so a population with several bad ids yields one `input_invalid` finding, not one
per row. This matches the contract wording "One per unusable input" (the
population document is the input). Evidence: case F below reported `row: " S001"`
from `{"rows":[{"id":"S001"},{"id":" S001"}]}`.

A2. Pre-existing, unchanged by the hunk: a corpus citing only ids outside the
population still measures `clean` with `outsidePopulation` counting
(scripts/citing_set.py:492-494 at b5d423f). Contract-sanctioned; the hunk neither
introduces nor worsens it.

A3. The accepted set is precisely the citable set. `_NUMERIC_ID_RE = ^S([0-9]+)$`
(scripts/citing_set.py:125) is anchored, ASCII-only, no strip; the grammar
`(?<!\w)S([0-9]{3,})(?!\w)` (line 116) produces only uppercase S + >=3 ASCII
digits. Every accepted numeric id is reachable via zero-padding (`S12` via
`S012`, `S0` via `S000` — case D/H), and every rejected spelling (`" S001"`,
`"s001"`, `"X9"`, unicode digits) is unproducible by the grammar. The docstring's
reachability rationale holds in both directions.

## Evidence

Sandbox: /fast/scratch/hyaku/kake-r28a3/w1/ReviewUnreachableId/
(clone at b5d423fc02057f67a6f3a255808313ce40d29069; gate sha256
28ba996524b444b2e1c23e3751f3fa662a9a44adbfcb6337a0d23fcebaf8f415; base gate
extracted from 22c1669c1fec83d1a0769de6b9ce686c75657e66, sha256
3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228).
No tool installs were needed; none performed. Lane repo untouched except this report.

1. Committed-data audit (exit 0): scanned every tracked JSON with a `rows` list
   of id-bearing rows — 30 files: all 29 `scripts/fixtures/citing-set/*/population.json`
   (minus 15/16, which are deliberately invalid), `.ufo/waves/round-26/population.json`
   (32 rows), `.ufo/waves/round-27/frozen/population.json` (32 rows), and
   `.ufo/waves/round-28/verification/c2-before.json` (not a gate input).
   Non-`S[0-9]+` ids found: 0. Unstripped ids: 0.
   The round-23/24/25 `*population*.json` files are different-schema selection
   records (keys round/source/targets/criteria), not gate inputs.
   The lane working-copy `corpus/` contains no population.json.

2. Selftest at the repair commit (exit 0):
   `timeout 120 python3 -B scripts/citing_set_selftest.py` in the sandbox clone —
   29/29 cases pass, `passed: true`.

3. Behavioral cases (gate runs with `--json`, `timeout 15`, all exited 0 for the
   harness; gate exit codes shown):

   | case | population ids | corpus/ledger | base | repair |
   |---|---|---|---|---|
   | A | S001,S002 | cites S001, adjudicated | exit 0 clean | exit 0 clean |
   | B | " S001",S002 | no citations | (base: would be clean) | exit 2 `population_id_unreachable` row=" S001" |
   | C | s001 | cites S001 | exit 1 ledger_pair_not_cited | exit 2 `population_id_unreachable` row="s001" |
   | D | S12 | cites S012, adjudicated | exit 0 clean | exit 0 clean |
   | E | X9 | none | — | exit 2 `population_id_unreachable` row="X9" |
   | F | S001," S001" | none | — | exit 2, first offender reported |
   | G | [] (empty) | none | exit 0 clean | exit 0 clean |
   | H | S0 | cites S000, adjudicated | exit 0 clean | exit 0 clean |
   | I | S001; ledger row " S001" | cites S001 | exit 1 | exit 1, findings byte-identical to base |
   | J | S001; ledger row "s001" | cites S001 | exit 1 | exit 1, findings byte-identical to base |

   Cases I/J show the hunk leaves ledger-row id handling untouched
   (`ledger_keys = [(id_key(row), name) ...]`, scripts/citing_set.py:528): a
   whitespace- or lower-case-padded ledger row fails as `ledger_pair_not_cited`
   exactly as at base — no new `input_invalid`, no new silence.
   Case B is the intended C1 flip: a population row the grammar can never cite
   could sit dead while the gate measured clean; it is now unusable input,
   verdict `could-not-evaluate`, exit 2, JSON report on stdout with
   `{"id":"input_invalid","reason":"population_id_unreachable","scope":"population",
   "path":"population.json","row":" S001"}`.

4. `key[0]` is safe: the preceding check guarantees `identifier` is a non-empty
   str, and `id_key` (scripts/citing_set.py:155-163) always returns a 2-tuple.
   The sole caller is `evaluate` at scripts/citing_set.py:462, after
   `load_json_document` shape validation. No other caller exists (text search;
   no LSP server was used for this leaf data audit — recorded as method note).

## Residual risk and verification gaps

- I did not rerun the full C1 counter against the lane's frozen round-27
  population end-to-end with `--revision`; the L1's recorded evidence
  (.ufo/waves/round-28/verification/c1-after-b5d423f.json, 15/15) covers that
  run. My audit verifies the frozen population's 32 ids are all `S[0-9]+`, which
  is the property this hunk gates on.
- I did not test a population id with unicode whitespace (e.g. NBSP-padded);
  by code reading it takes the same `("s", ...)` path as case B and is rejected.
- Method note: caller/definition checks were text searches and direct reads;
  no `lsp` device is available to this seat.
