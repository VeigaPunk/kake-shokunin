# MutationC1Json

MUTANTS
- JSON result-span mutation: changed a committed fixture receipt from `"met": true`, `"findings": 3`, `"members": 144` to `"met": false`, `"findings": 4`, `"members": 145`. The lane tool's result-span regex at `scripts/receipt_lineage.py:104-107` recognizes `met\s*=`, `findings\s*=`, and `members\s*=`, but not JSON colon forms. Baseline and mutant both returned exit 0, `receipts=1 events=0 undisclosed=0 met=True`; this is a surviving false-green against A3.
- Duplicate/order probe: changed an ordinary receipt's result lines from `EXIT=0, met=True, findings=3` to reordered lines with a duplicate `met=True`. Tool returned exit 0, `events=0`. This matches the contract's set-of-whole-lines semantics: reorder and duplicate-count-only changes leave the span set unchanged. The contract tool selftest explicitly covers reorder (L10), but not duplicate add/remove; the frozen C1 counter's contract cases L1-L16 contain neither JSON colon forms nor duplicate/order cases.

KILLED
- None by the frozen C1 counter: `.ufo/waves/round-61/c61_lineage_cases.py` is absent at lane HEAD `f5a9b8acc8e4d0995e8ba849c4a9d56ba1ab0a8f`, so that detector cannot be run. The tool's own `--selftest` passed 68/68 before and after the fixture probe; it does not exercise JSON colon result-span changes or duplicate lines. It does include a reorder case.

ACTUAL OUTPUTS
- Pristine JSON fixture, revision `df886692a9ae3d65dc298d436ab2084e1f7a31dc`: exit 0; `receipts=1 events=0 undisclosed=0 met=True`.
- Mutated JSON fixture, revision `bbd34ab87f03fb95d70edea8d8ccd12810c374ae`: exit 0; same summary, no events/findings despite all three JSON result fields changing.
- Restored pristine fixture revision: exit 0; same clean summary. Fixture files were restored byte-for-byte in scratch.
- Reordered/duplicate fixture, revision `7f9356659a6c74f070d5c50881dfccb8d24ebfe0`: exit 0; `receipts=2 events=0 undisclosed=0 met=True`.
- Tool selftest output: `receipt_lineage selftest: 68 checks passed`, exit 0 (both initial and restored runs).

HASHES / RESTORATION
- JSON receipt pristine/restored SHA-256: `1f4338f6fab2f4691809671b2918c50babd1fa4dadbf0f11da2665f2571513d8`.
- JSON receipt mutated SHA-256: `0a9f85af4579dbd0c827467e79e8327cc5b6eeda4fa0fd29cd6c5feda657a543`.
- Order receipt pristine/restored SHA-256: `9fb100526479e971b7a096db692d950eef8f67dbba99502ec6723bca1fbc4667`; reordered+duplicate SHA-256: `e2f7ce2a236904e343681139e5d990ab702e58d0c16b84962bef4aa6f245f97c`.
- Tested tool source SHA-256 remained `3dd29b8646adab70d5e0b25697f6297cc740bee88b03fdedc961e30d01c82a78`; no tool source was mutated. Scratch fixture files restored; lane source and score were untouched. No tools installed.

VERDICT: JSON-colon result-span mutation SURVIVES (A3 coverage gap and observed false-green); order/duplicate changes are intentionally span-set invariant, with no duplicate-specific frozen counter case; counter verdict unavailable because the C1 counter file is absent.
