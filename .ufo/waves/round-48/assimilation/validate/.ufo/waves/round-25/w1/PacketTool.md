# PacketTool — retained sandbox draft only

## Disposition and axes

- Axes: **operability** and **freshness**.
- **Uncredited / superseded.** L1's latest instruction says this seat's initial terminal result was `failed capacity turn_rate_limit_exceeded` after five retries; no replacement or retry is authorized. This reported state was not independently rechecked.
- A sandbox draft had already been written when that instruction arrived. It remains evidence only. No further implementation changes were made, and no production readiness or integrated capability is claimed here.
- L1 has independently authored production `scripts/accessibility_packet.py` and owns integration. Its announced quote rule is at least six words with word-boundary normalization and a source-hash pin, without a uniqueness expansion. **The retained draft does not implement that superseding rule and must not be substituted for production.**

## Files written

1. `.ufo/waves/round-25/sandboxes/tool/scripts/accessibility_packet.py`
2. `.ufo/waves/round-25/w1/PacketTool.md` — this exclusive advisory report.

No lane-production file, sibling sandbox, Git index, commit, global configuration, account, or external substrate was modified. `LOG.md` and other integration documentation remain intentionally unchanged under this seat's single-file/report ownership.

## Exact retained evidence

- Draft path: `.ufo/waves/round-25/sandboxes/tool/scripts/accessibility_packet.py`
- Draft SHA-256: `ac196de6bd5bdd4e3d0b5d1fb81ee4dc67eb68a80b218f0bb03238add1fca76a`.
- The write tool retained snapshot tag `BC8A`, reported 19,922 bytes written, and automatically marked the new script executable.
- Digest obtained with `sha256sum .ufo/waves/round-25/sandboxes/tool/scripts/accessibility_packet.py`. This was artifact identification only; the Python file was not imported, compiled, or executed.
- Initial contract evidence: `.ufo/waves/round-25/contract.json`, read snapshot `707D`, naming base `6883f1d580d811f7c434d1db4642596362f822b1` and a 55-card offline manual-review capability, not website conformity. The base is contract-provided; no Git command was run to reconfirm it.
- Initial population evidence: `.ufo/waves/round-25/population.json`, read snapshot `673E`, plus a JSON projection showing exactly 55 entries and entry keys `anchor,id,level,normativeText,source,text,title`.
- That population declares source `https://www.w3.org/TR/2024/REC-WCAG22-20241212/`, `opened=2026-10-21`, and `sourceSha256=6e3c5fe397257cae509a2fb4752b73062cf8cbeb92c2cec618989b17e4cf7057`. This is retained declared source metadata, **not** an independently verified HTML digest or freshness result. The draft does not load or verify an HTML source file.

## Draft behavior as authored — unexecuted

Code paths: `parse_cli`, `audit_packet`, `_load_population`, `_card_findings`, `_result`, `selftest`, and `main` in the retained draft above.

- Standard-library-only CLI: `--root ROOT [--json] [--selftest]`; standalone `--selftest [--json]` is also supported. `--json` is optional because normal stdout is already one JSON object. `--help` emits CLI help instead.
- Ordinary operation reads only `.ufo/waves/round-25/population.json` and `corpus/knowledge/accessibility-review-cards.json` beneath the supplied root. No network operation or file write exists on that path.
- Output schema is `kake-accessibility-packet-v1`; `expected` is fixed at 55; `websiteConformance` is always `not-assessed`. Criterion rows follow population order and have exactly `id`, Boolean `accepted`, and sorted unique `findings`. Global findings are sorted unique strings.
- Population input must contain 55 unique identities with nonempty `id/title/level/source/normativeText` and levels A or AA. Missing `normativeText` is unevaluable; full `text` is never a fallback.
- Cards require the exact ten shared keys, all nonempty strings; metadata must match the corresponding population criterion exactly. Duplicate criterion IDs reject that criterion. Unknown IDs produce global metadata findings and any displaced expected identity remains missing.
- Draft quote rule: `len(sourceQuote.split()) <= 25`, and a literal, case-sensitive substring of the matching `normativeText`. Whitespace and punctuation are not normalized; no minimum length, word boundary, cross-reference exclusion, or uniqueness rule is enforced. This is the initial contract interpretation, **not L1's superseding production policy**.
- Status must be exactly `not-assessed`. Content acceptance is packet readiness only; no website is inspected or declared passed, failed, inapplicable, or conformant.
- Exits: 0 / `clean`; 1 / `failed`; 2 / `could-not-evaluate` for unavailable or invalid input; 64 / `could-not-evaluate` for usage. Usage emits no finding IDs. With valid population but unusable card input, all 55 rows are rejected with `input_invalid`; unusable population yields no criterion rows.
- JSON decoding rejects repeated object-member names, non-JSON numeric constants, malformed JSON, and non-UTF-8 input as `input_invalid`.
- `selftest` is authored to invoke `main` against synthetic temporary fixtures, covering pristine55, absent/malformed inputs, duplicate/missing/changed identities, metadata, exact fields, empty/nonstring prose, quote length/body/case/spacing, false status, population shape, and usage exits. It uses `tempfile.TemporaryDirectory` only and ignores any supplied ROOT. Its one JSON object adds `selftest` metadata explicitly identifying synthetic fixtures; it is not an assessment of the real packet. **It was never run.**

## Every draft stable error ID

| Stable ID | Meaning in this draft |
| --- | --- |
| `metadata_mismatch` | Unknown/nonstring identity, or id/title/level/source not matching the selected population entry. Unknown cards remain global findings rather than invented criterion rows. |
| `duplicate_id` | More than one card claims an expected criterion identity; that row is rejected. |
| `missing_id` | No card claims an expected criterion identity. |
| `fields_mismatch` | Card is not an object, or its key set differs from the exact ten shared keys. |
| `empty_field` | A required card value is absent, not a string, or whitespace-only. |
| `quote_too_long` | Nonempty sourceQuote has more than 25 whitespace-delimited words. |
| `quote_not_from_source` | Nonempty sourceQuote is not a literal substring of the matched criterion's normativeText. |
| `status_not_assessed` | Card status differs from the literal `not-assessed`, including absent status. |
| `input_invalid` | Input cannot be read/decoded, has an unsupported top-level shape, or population lacks valid 55-entry metadata/normativeText. Also used if selftest temporary-file setup fails. Exit 2. |
| `selftest_failed` | One or more authored built-in CLI assertions fail when selftest is explicitly invoked. Exit 1; not emitted by ordinary packet validation. |

Except for `input_invalid`, ordinary card findings produce exit 1. Multiple findings may be emitted for one defect. For example, replacing an expected ID with an unknown ID yields global `metadata_mismatch` and `missing_id` on the displaced row; changing it to another known ID also creates `duplicate_id` on the duplicated row.

## Coordination, tooling, risks, and checks

- Initial ID/row/exit coordination was sent to `KakeR25.PacketTests` and `KakeR25.PacketCounter`. After L1's stop notice, both received explicit correction that this draft and its earlier interface advice are superseded and production coordination belongs to `KakeR25`. `KakeR25.QuoteCritic` received the same disposition.
- No tools were installed or updated. The implementation uses the Python standard library only.
- The inspected `xd://` inventory exposed 207 REA devices and no mounted LSP device. Therefore no supported Python definition/reference/refactor operation could be invoked; no empty LSP result was treated as evidence of symbol absence. The assigned script was a new file.
- **No builds, tests, selftests, linters, formatters, smoke runs, imports, syntax checks, or production validation were performed.** No result is represented as passing.
- Main owns any post-integration gate execution. Use L1's production implementation and chosen contract, not this superseded draft, for the focused packet checks, built-in selftest, and independent revision counter.
- Blocking condition for promotion: L1 explicitly forbids this seat's retry/resumption and owns production already. The retained draft additionally differs from the announced production quote minimum/normalization/boundary/hash policy. It is evidence only, not a candidate awaiting automatic integration.
