# MutC3Counter
ATTACKS: C3 `c60_quote_truth.py` at B1 (`8b33fd248d126b48d838af5c38bc175850f41a09`); 25 mutation probes targeting scope, was/now, block boundaries, fence/comment handling, receipts, ancestry/footer, anchors, used-by, and subjects. Baseline selftest: `140/140 (baseline exit 0, 9/9 conditions; 129 fixtures, 125 red, 4 green)`.

MUTANTS:
- Executed 25 text-substitution mutation attempts; most literal append substitutions were invalid source perturbations (syntax/name errors), so not valid kills. The meaningful mutants: scope-regex predicate disabled by changing its `robots\\.txt` token; fenced-code handling disabled by changing the fence marker. Other probes included effectiveUrl, footer marker, used-by constants, subjects, receipt pin, stale window/tag, title, digest, unique span threshold, curly quotes, status/date, mirror pin, receipt URL, and citation tokens.
- Scope mutant output: selftest `139/140`; `FAIL fail_s427_scope_overclaim: expected exit 1 ... got exit 0, adding []`. Counter remained `9/9 met=True EXIT=0` on B1 fixture.
- Fence mutant output: selftest `139/140`; `FAIL fail_entry_quote_inside_fence: expected exit 1 ... got exit 0, adding []`. Counter remained `9/9 met=True EXIT=0` on B1 fixture.
- Additional typo/constant mutations produced selftest baseline failures and/or exit 2 (`NameError`); these are invalid mutants, excluded from killed/survived counts.

SURVIVORS:
- Two valid mutants survived the B1 behavior detector: (1) scope overclaim detection can be removed while all 9 conditions pass; (2) fenced quote exclusion can be removed while all 9 conditions pass. They are coverage findings, not contract changes.
- Remaining attempts were not valid mutants because the substitutions corrupted identifiers/source and caused baseline failures; do not count them as killed.

CASES TO ADD:
- A9 T1: independently remove/neutralize the S427 scope overclaim regex and require selftest to fail specifically on `fail_s427_scope_overclaim`.
- A9 T4: make an otherwise sufficient three-span entry rely on a quote only inside a fenced block; require C5 rejection. Existing selftest fixture `fail_entry_quote_inside_fence` did not kill this mutation, so strengthen its construction/expectation.
- Follow-on probes to add as genuine isolated behavior mutants: T2 was/now phrase linkage; T3 one insertion run/block-boundary invariant; T6 effectiveUrl and receipts blob pin; T7 validation ancestry; T8 footer-only revision; A1 nearest heading; exact used-by sets; per-row subject. This probe did not establish their mutation-kill coverage.

FINDINGS:
| severity | target file:line | issue | evidence command | fix |
| medium | `.ufo/waves/round-60/c60_quote_truth.py` (scope rule) | Removing the scope overclaim predicate does not fail the selftest or B1 counter. | `python3 -B <mutated-script> --selftest` → `139/140`, failed `fail_s427_scope_overclaim`; `python3 -B <mutated-script> --root <B1-clone> --revision 8b33fd248d126b48d838af5c38bc175850f41a09` → `9/9`, exit 0. | Strengthen/retain a selftest mutation that demonstrably kills loss of the A9 regex. |
| medium | `.ufo/waves/round-60/c60_quote_truth.py` (fence stripping) | Removing fenced-code exclusion survives the counter; a fixture failure is detected only by the mutation selftest, not the production predicate. | Same commands; selftest `139/140` on `fail_entry_quote_inside_fence`, counter `9/9`, exit 0. | Make the production case require a fenced-only span and validate that the selftest fixture kills this mutant. |

Restoration evidence: pristine B1 source SHA-256 before and after mutation cycle `0532c76e0174af1e7e2422fd9dc22ea8f9fc995073c77cfd96a2a67d1942eb9b`; byte equality verified (`restored True`). Pristine selftest was observed at `140/140`; pristine B1 detector was observed at `9/9`, exit 0. Scratch clone removed after probing.
VERDICT: Two valid surviving mutants expose coverage gaps (scope overclaim and fenced quote exclusion); other attempts were invalid source perturbations, not kills.