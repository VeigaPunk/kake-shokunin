# ReviewerC2Counter

Axis reviewed: C2 operability. Additional checks: denominator, control separation, and output/exit contract.

## Findings

### High — R3 rejects the frozen implementation before auditing its canonical manifest

`.ufo/waves/round-61/c61_header_cases.py:471-512` materializes every round-61 JSON file, treats every version-1 object with a `checks` list as a manifest, then fails when more than one candidate exists. At `f512eee` and measured `f5a9b8a`, R3 reports ambiguity including the canonical `.ufo/waves/round-61/capture/manifest.json`, `w1/CriticC2Semantics.files/manifest.json`, and `w1/MutationC2Probe.files/fixtures/.../manifest.json`. Contract A4 explicitly names the canonical manifest path and says R3 is a separate shape gate. Consequently both revisions report H1–H18 18/18 but `R3 pass=false`, `met=false`, exit 1. A direct run on the canonical manifest produces `checks=12 findings=13`, exit 1; that live verdict is permitted to be non-clean and should be recorded, not block the shape gate. R3 should inspect the canonical path rather than reject unrelated JSON fixtures.

### Medium — R3 does not establish that sources are capture receipts

At `.ufo/waves/round-61/c61_header_cases.py:519-531`, source validation only checks `os.path.isfile(path)` and that the 12 source strings are distinct. It does not require a source to be under the capture directory or to be a response receipt; aliases can also name one file with distinct strings. Thus an existing unrelated file can satisfy the stated “each bound to a capture receipt” shape condition. This remains after resolving the candidate ambiguity.

## CASES / DENOMINATOR

The counter enumerates exactly H1–H18 (`NCASES = 18`, `ALL_IDS`), and sums one pass/fail result per H case; sub-fixtures are folded into that case. The judge checks expected exit, summary, and finding class/check ID for clean, finding, and could-not-evaluate cases (`:379-420`). R3 and R4 are separate gates and are not added to `cases_passed` (`:841-848`), consistent with A4.

Observed runs, all in the scratch clone with seed 611:

- Base `9f07731a`: 0/18, met=false, exit 1; R4 passed (`header_audit.py` absent, 0/18, exit 1).
- Early implementation tree `8ad7e2a`: 18/18; R3 failed because no version-1 manifest was present; exit 1.
- Frozen implementation `f512eee` and current measured `f5a9b8a`: 18/18; R3 failed on ambiguous manifests; R4 passed; exit 1. `045b499` and `f512eee` have identical trees and identical counter/tool blobs.
- Counter `--selftest`: all seven controls passed (missing tool, always clean, always exit 1, manifest sniffing, reference implementation, and two R3 shape controls).
- Direct canonical-manifest audit: 12 checks, 13 findings, exit 1; recorded live result, not asserted as clean.

## Residual risk and verification gaps

The counter's candidate-selection defect prevents R3 from exercising the real manifest at the frozen/current implementation. Its R3 source-shape check is also weaker than the contract. No LSP device was mounted (`xd://lsp` unavailable), so no LSP references/definitions/diagnostics were run. No tools were installed.

VERDICT: FAIL — H1–H18 and R4 behave as specified, but R3 blocks the frozen/current counter from meeting its exit contract.