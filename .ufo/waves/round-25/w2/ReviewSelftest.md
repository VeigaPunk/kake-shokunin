# ReviewSelftest — r25 C1 packet selftest falsification

Role: critic (leaf). Milestone: r25-falsify-accessibility-packet. Axes: operability, freshness.
Scope: read `.ufo/waves/round-25/packet_selftest.py` and `scripts/accessibility_packet.py` (`selftest()`);
one assigned run. No production edits, no other commands, no r24 material, no tool installs.

## Assigned run (only command executed)

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-25/packet_selftest.py --root /home/vgpnk/Projects/shokunin/kake-shokunin
```

- exit: `0`
- stdout: `{"failures": [], "passed": 26, "schema": "kake-accessibility-packet-selftest-v1", "total": 26}`
- stderr: empty

All 26 cases pass. The real 55 cards contain 55 `"status": "not-assessed"` (grep count 55/55).

## Verdict

| Check | Can it fail when broken? | Gap |
|---|---|---|
| False conformance `status` | Yes, for listed values | The cases use a denylist, so a denylist regression is not caught |
| Heading/doclink quote | **No**, in `packet_selftest.py`; partly in the built-in `--selftest` | No case uses real heading or doc-link text |
| `websiteConformance` output | Yes; asserted on every case | Constant in `result()`, so no data path |

## Finding 1 — the heading/doclink guard is untested (operability)

**Counterexample (derived by reading the code, not executed: only the assigned command was authorized).**
At `scripts/accessibility_packet.py:84`, matching uses `normalized(ref['normativeText'])`.
Change it to `normalized(ref.get('text', ref['normativeText']))`. The validator then accepts a quote taken from the heading or doc-link wrapper. Every pinned row has a `text` field that starts with that wrapper. For example, population 1.1.1:
`"Success Criterion 1.1.1 Non-text Content Understanding Non-text Content | How to Meet Non-text Content (Level A) All non-text content ..."`.
`Success Criterion 1.1.1 Non-text Content Understanding Non-text Content` is 8 whitespace words. It passes the 6–25 length rule, so `quote_not_from_source` is the only finding that guards it.

Why both selftests stay green under that mutation:
- `packet_selftest.py` writes the real `population_raw` bytes, so `text` is present. But its quotes come only from `normativeText`: the 10-word prefixes in `pristine55` and the 1.2.4 punctuation fixture. Each `normativeText` is a substring of `text`, so all of them still match. `quote_not_from_source` uses a made-up sentence that appears in neither field. `quote_partial_word_boundary` fails on word boundaries, whichever field is searched. The file contains no heading or doc-link case (grep for `heading|Understanding|How to Meet|'text'` across round-25 `*.py`: no matches).
- Built-in `selftest()` `heading_quote` (`'Criterion 0'`, lines 133/137) has two weaknesses:
  1. Its fixture rows have no `text` key, so the `.get('text', ...)` fallback reads `normativeText` and the case stays green.
  2. The quote is 2 words, so `quote_too_short` also fires. The case asserts only `finding in output['findings']` (line 141), not the exact finding set. It does catch one other mutation: matching against `title + normativeText`.

The data side holds today: no `normativeText` in `population.json` contains `Understanding `, `How to Meet`, `(Level A` or a `Success Criterion X.Y.Z Title` heading (grep count 0). `measure.py:231` also matches only `normativeText`. Whether `measure.py` would expose a divergence from the production tool depends on how the judge compares the two [INFERENCE, not verified].

**Smallest safe correction.** Add one case to `packet_selftest.py` `build_cases`. Set card 0's `sourceQuote` to the `text` prefix before `normativeText`. For 1.1.1 that is the 14-token heading-plus-doc-link string ending `How to Meet Non-text Content`. Expect exactly `['quote_not_from_source']`, exit 1. Optionally make the built-in `heading_quote` use a quote of 6 or more words, give its fixture rows a `text` field, and assert the exact findings set.

## Finding 2 — the false conformance status check is a denylist (operability)

Production uses exact equality: `card.get('status') != 'not-assessed'` (line 86). This is correct, and it rejects case variants, whitespace variants, non-strings and a missing key.

The `packet_selftest.py` cases are `passed`, `failed`, `inapplicable` and `conformant` (lines 249–250). Each asserts exact findings `['status_not_assessed']` and exit 1. Removing the production check therefore fails 4 cases, so the check can fail.

**Counterexample.** Replace the check with the denylist `card.get('status') in ('passed', 'failed', 'inapplicable', 'conformant')`. All 26 cases still pass. The built-in `false_result` uses `passed`, so it stays green too. Real-world status words such as `supports`, `partially-supports`, `meets`, `AA` or `pass` would then be accepted as clean. That is a false conformance claim on a card, against the contract's statement "no website conformity claim".

**Smallest safe correction.** Add one case with a status outside the list, for example `supports`, and one with the `status` key removed (expect `fields_mismatch` and `status_not_assessed`). An allowlist regression then fails.

## Minor (no action required)

- In `packet_selftest.py`, lines 196 and 198 append `b'\\n'`: two bytes, a backslash and `n`, not a newline. The bytes still change, so `snapshot_tampered` is still exercised correctly. Only the stated intent is off.
- Freshness: `packet_selftest.py` builds its fixtures from the live pinned population and source bytes, so it tracks the current pins. Built-in `selftest()` is fully synthetic and does not depend on the pins. Neither is stale relative to the pinned SHA-256 values in the production tool, because the assigned run's `pristine55` passed against the real bytes.

## Impacted axes

- operability: Findings 1 and 2. These are test-adequacy defects with cheap fixes; current production behavior is correct.
- freshness: no defect found.

No production files were changed. The only write is this report.
