# R25 w2 ReviewTool — falsify `scripts/accessibility_packet.py`

Scope: code review only of `scripts/accessibility_packet.py`, the fixed population
`.ufo/waves/round-25/population.json`, the cards
`corpus/knowledge/accessibility-review-cards.json`, the packet document, and the readiness
counter `.ufo/waves/round-25/measure.py` (read for contract comparison). Nothing was executed:
no CLI, selftest, counter, or suite run. No production edits, no delegation, no tool installs.
Claims about stdlib behavior come from documented CPython `json`/`argparse` semantics; any
claim I did not observe is marked [INFERENCE].

Axes: **operability** (the CLI's exit code and JSON contract, and agreement with the readiness
counter) and **freshness** (whether the document matches the code).

## D1 (operability, HIGH): the ordinary CLI accepts duplicate JSON keys, so a `passed` status can produce a clean result

**Counterexample.** Edit card `1.1.1` in the cards file so that it contains
`"status": "passed", …, "status": "not-assessed"`. Two other inputs show the same problem:
the same duplication on `id`, `title`, or `sourceQuote`, or a prose value written as `NaN`.

**Evidence.**
- `scripts/accessibility_packet.py:104` parses the cards with plain
  `json.loads(...read_text(encoding='utf-8'))`. By documented default, Python's `json` keeps the
  last value for a duplicated key and accepts `NaN`, `Infinity` and `-Infinity`.
- For the input above, `set(card) == FIELDS` (line 68) holds, and `card.get('status')` returns
  the last value, `'not-assessed'` (line 86). The CLI therefore returns `verdict: clean`
  with exit 0. That is the "structurally clean" signal the packet document's `recheck:` line
  and the "Inventory is clean" row of its decision table rely on. But the file contains
  `"status": "passed"`, and any first-value-wins reader or a human reading the JSON sees that
  value.
- The readiness counter disagrees. `.ufo/waves/round-25/measure.py:63-79` defines
  `strict_json` with `object_pairs_hook=unique_object` and `parse_constant=reject_constant`.
  At lines 348-353 it expects `could-not-evaluate` with exit 2 for these inputs, and lines
  363-364 then turn the CLI/counter mismatch into `input_invalid` with exit 2. The counter
  fails closed, but the ordinary CLI that the document tells reviewers to run gives a
  different answer on the same bytes. So the readiness contract and the CLI disagree.
- For a `NaN` prose value, the CLI exits 1 with `empty_field`, while the counter exits 2. That
  is a second divergence.
- No selftest covers this. Neither the built-in `selftest()` nor
  `.ufo/waves/round-25/packet_selftest.py` (cases at lines 178-251) has a duplicate-key or
  non-standard-constant case.

**Smallest safe correction.** Make the CLI's cards (and population) parse use the same rules as
the counter's `strict_json`: `object_pairs_hook` rejects duplicate members and
`parse_constant` raises `ValueError`. The existing
`except (OSError, UnicodeError, ValueError)` at line 105 then returns
`could-not-evaluate` / `['input_invalid']` with exit 2. The counter's `input_invalid_rows`
(`measure.py:317-318`) produces exactly that, so `strict_equal` passes. Add
`packet_selftest.py` cases `cards_duplicate_key_status` and `cards_nan_constant`, each
expecting exit 2 and `['input_invalid']`.

## D2 (operability, MEDIUM): deeply nested cards JSON makes the CLI crash with exit 1, and fixing only the CLI exposes the same crash in the counter

**Counterexample.** Replace the cards file with a few hundred thousand `[` characters, for
example `'[' * 200000`. [INFERENCE: the exact depth that triggers the error depends on the
interpreter's recursion limit.]

**Evidence.**
- CPython's C JSON scanner raises `RecursionError`, a `RuntimeError` subclass, when nesting
  exceeds the limit. The `except (OSError, UnicodeError, ValueError)` at
  `scripts/accessibility_packet.py:105` does not catch it.
- The CLI therefore prints a traceback to stderr, writes no JSON to stdout, and exits 1
  [INFERENCE: not executed]. The packet document says
  "1 means a packet requirement failed; 2 means input could not be evaluated", so this
  contradicts it.
- Today the counter masks the problem. Any stderr output makes `parse_tool_result`
  (`measure.py:263-264`) raise `InputFailure`, which becomes exit 2.
- That mask goes away once the CLI is fixed. With clean stdout and no stderr,
  `measure.py:349` runs `strict_json(cards_raw)` and hits the same `RecursionError`. Only
  `(UnicodeError, ValueError)` is caught at line 351 and only `OSError` in `main` at line 380,
  so the counter itself would crash with exit 1.

**Smallest safe correction.** Add `RecursionError` to the exception tuple in two places:
`load()` at `scripts/accessibility_packet.py:105`, and the expected-result derivation at
`measure.py:351`. Both should route to `input_invalid` with exit 2. Change both in the same
step. Fixing only the CLI turns a fail-closed path into a crash in the counter.

## D3 (operability, LOW): `--help` / `-h` exits 0 and prints non-JSON text

**Evidence.** `Parser` overrides only `error()` (lines 156-158), and `add_help` keeps its
default, `True`. So `-h` prints argparse help to stdout and raises `SystemExit(0)`. That
bypasses the single JSON result and returns the exit code the document reserves for
"structurally clean". A wrapper that checks only the exit code would treat `--help` as clean.
This path is not reachable through the counter, which passes fixed arguments.

**Smallest safe correction.** Construct the parser with `Parser(description=__doc__,
add_help=False)`. `-h` and `--help` then go through `error()`, which returns `usage` with exit
64 as one JSON object. Optionally add `allow_abbrev=False` so that `--js` and `--self` are not
silently accepted.

## D4 (freshness, LOW): the document and the code count quote words differently

**Evidence.** The document says "Quotes contain 6–25 whitespace-delimited words". The code
counts `normalized(quote).split()` (lines 78-82), which runs after punctuation spacing is
removed. A raw quote with a lone `,` token, such as card `1.3.1`'s
`"Information, structure , and relationships …"`, therefore has one more raw word than the
number the code counts. At the boundary, a raw quote of 26 tokens that includes one lone `,`
is accepted.

**Smallest safe correction.** Change the document to "6–25 words, counted after the spacing
normalization below", or count `quote.split()` before normalizing. The document change is
cheaper and keeps the current cards valid.

## D5 (freshness, LOW): two cards repeat extractor spacing instead of the standard's text

**Evidence.**
- Card `1.3.1`'s `sourceQuote` contains `structure , and` (cards line 79).
- Card `2.5.3`'s contains `images of text , the name` (cards line 439).

The validator accepts both because normalization is applied on both sides. However, the
document describes the quote as a "short located quote", and these strings are not what the
REC says. A reviewer who copies one gets an extractor artifact.

**Smallest safe correction.** Remove the space before the comma in those two card quotes. Both
still validate (normalized equality), and the cards' frozen digest
(`frozen/expected.json` `cards.json`) must be re-pinned in the same change.

## Notes, not defects (tradeoffs for the judge)

- **Overloaded `input_invalid` finding.** A non-object card, or a card whose `id` is not a
  string, adds the global finding `input_invalid` but exits 1 (lines 51-53, 92-93). The same
  finding id also means exit 2 / `could-not-evaluate`. The counter mirrors this behavior
  (`measure.py:194-197`), so the two agree; only the naming of the taxonomy is ambiguous. No
  selftest covers this branch either. A non-string `sourceQuote` is likewise reported as
  `empty_field`, not as a type finding.
- **List labels inside `normativeText`.** The population's `normativeText` keeps WCAG
  definition-list labels joined to their body text (1.1.1:
  `"… Decoration, Formatting, Invisible If non-text content is pure decoration , …"`). As a
  result, a 9-word quote that starts with a list label splices the label and the body into a
  string the REC never presents as contiguous prose, and the validator accepts it. None of the
  current 55 card quotes does this (all inspected at cards lines 7-655). Fixing it requires a
  separator at list boundaries, which means re-pinning the population bytes (`POPULATION_SHA256`
  appears in the CLI, the counter, and `frozen/expected.json`). That is a judge-level tradeoff,
  not a bounded fix.
- **`--json` does nothing.** The CLI always prints JSON. The flag is harmless, but it is dead
  weight.
- **`population.sourceSha256` is ignored by the CLI** but checked by the counter
  (`measure.py:164-165`). This cannot be observed today because the population bytes are
  hash-pinned.
- **Checks with no defect found.** Duplicate and missing ids, the exact metadata comparison,
  the exact `status != 'not-assessed'` check, the case-sensitive word-boundary regex, and the
  pin-before-parse order behave as documented when the input is valid JSON.
- **Card population and status.** All 55 card ids appear once each, in population order, and
  every `status` line reads `"not-assessed"`. I checked this with grep over the cards file.

## Checks the main agent should run after integration

- `python3 -B scripts/accessibility_packet.py --root . --json`
- `python3 -B scripts/accessibility_packet.py --selftest`
- `python3 -B .ufo/waves/round-25/packet_selftest.py --root .`, with the new duplicate-key and
  `NaN` cases.
- `python3 -B .ufo/waves/round-25/frozen_replay.py --selftest`, after any card re-pin.
- `python3 -B .ufo/waves/round-25/measure.py --root . --revision <commit>`, plus a
  deep-nesting cards fixture to confirm the D2 fix in both files.

Tooling: none installed or updated.
