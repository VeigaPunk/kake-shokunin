# ExecControlAudit — round 84 wave w1

## Verdict
PASS for the scoped frozen-control audit: all 12 receipts satisfy the contract; the complete changed-header sets match both frozen expectation sources; all 28 rebuilt pair files match the freeze byte-for-byte.
This is not a C2 counter verdict or admission decision.

## Axes
- Calibration: independent receipt/body checks and exact header-set comparison.
- Freshness: distinguish value-level policy changes from order-only rewrites.
- Operability: reproduce the frozen builder without touching its committed targets.

## Receipt table
All statuses below are JSON integers, all methods are GET, and all truncated flags are false.
`digest OK` means independently computed SHA-256 equals the receipt's sha256; full digests are printed in the retained output.

| Receipt | Method | Status | Receipt bytes / body length | Digest | Truncated | headerCount / actual |
|---|---|---:|---|---|---|---|
| control/a/ds4cc-primary | GET | 200 | 78897 / 78897 | OK | false | 22 / 22 |
| control/a/ds4cc-robots | GET | 200 | 62 / 62 | OK | false | 22 / 22 |
| control/a/ds4cc-sitemap | GET | 200 | 7810 / 7810 | OK | false | 24 / 24 |
| control/b/ds4cc-primary | GET | 200 | 78897 / 78897 | OK | false | 22 / 22 |
| control/b/ds4cc-robots | GET | 200 | 62 / 62 | OK | false | 23 / 23 |
| control/b/ds4cc-sitemap | GET | 200 | 7810 / 7810 | OK | false | 24 / 24 |
| equivalent/a/ds4cc-primary | GET | 200 | 78897 / 78897 | OK | false | 22 / 22 |
| equivalent/a/ds4cc-robots | GET | 200 | 62 / 62 | OK | false | 22 / 22 |
| equivalent/a/ds4cc-sitemap | GET | 200 | 7810 / 7810 | OK | false | 24 / 24 |
| equivalent/b/ds4cc-primary | GET | 200 | 78897 / 78897 | OK | false | 22 / 22 |
| equivalent/b/ds4cc-robots | GET | 200 | 62 / 62 | OK | false | 22 / 22 |
| equivalent/b/ds4cc-sitemap | GET | 200 | 7810 / 7810 | OK | false | 24 / 24 |

## Exhaustive header differences
Comparison lowercases field names and retains every value per name, including duplicates, rather than silently dropping repeated headers.

| Pair | Surface | Header | Old → new | Frozen value-level class |
|---|---|---|---|---|
| control | ds4cc-primary | cache-control | max-age=600 → max-age=60 | numeric_parameter |
| control | ds4cc-robots | x-frame-options | absent → SAMEORIGIN | header_added |
| control | ds4cc-sitemap | referrer-policy | no-referrer, strict-origin → strict-origin, no-referrer | reordered |
| equivalent | ds4cc-sitemap | referrer-policy | no-referrer, strict-origin → strict-origin, no-referrer | reordered |

These are all changes across the six surface comparisons, including non-policy header names: no additional header differences were found.
The exact surface/header/class maps equal policy-expectations.json; each old/new/class row also matches contract.md lines 130–133.
Bodies are byte-identical across each a/b comparison; status and digest do not move.
Every receipt field outside headers/headerCount is unchanged across each a/b comparison.
Each synthetic body's bytes, status and digest also match its original round-81 surface.

## Builder reproduction and exact retained evidence
Audit driver: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-84/w1/ExecControlAudit/audit.py`.
Complete stdout, per-receipt SHA-256 values, and every individual cmp/git command and exit code: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-84/w1/ExecControlAudit/audit-output.txt`.
Executed `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-84/w1/ExecControlAudit/audit.py` — exit 0.
The driver created the dedicated scratch directory and copied the round-81 capture to its rebuild root with shutil.copytree before invoking the builder.
Executed `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-84/build_control_pairs.py --root /fast/scratch/hyaku/kake-r84/ExecControlAudit/rebuild-copy` — exit 0.
Builder stdout: `built pair=control surfaces=3 built_pair=equivalent surfaces=3 receipts=12`.
All 28 corresponding pair files, including four manifests, were compared using `cmp <absolute committed path> <absolute rebuilt path>` — every exit 0, with identical file inventories.
All 28 committed pair files were also fetched with `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show f358022f7e1b2f3846be8ceacbe3a7ef22edf4be:<pair-file>` — every exit 0 and each returned byte string equals its rebuilt file.
Executed `cmp /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-84/policy-expectations.json /fast/scratch/hyaku/kake-r84/ExecControlAudit/rebuild-copy/.ufo/waves/round-84/policy-expectations.json` — exit 0.
Retained summary: `receipts=12 valid=12 changed_headers=4 pair_files=28 cmp_failures=0 frozen_mismatches=0 expectations_match=true`.
Cleanup completed in finally; retained output confirms `SCRATCH_REMOVED=True`.

## Distinguishability and counter blind spot
Yes: the frozen value-level class table alone distinguishes these fixtures. The control pair has numeric_parameter=1, header_added=1, reordered=1 and therefore policy-changed; the equivalent pair has reordered=1 only and therefore policy-rewritten-equivalent.
A counter summing only changed sees 3 versus 1, but cannot establish whether either total includes semantic movement: an order-only rewrite still increments changed.
Such a counter could count a benign rewrite as a policy change, miss incorrect per-header classes, or accept wrong verdicts even when totals happen to match.
These verdicts follow the frozen class table, not an independent claim that arbitrary Referrer-Policy reorderings preserve browser semantics.

## Builder inspection, risks and boundaries
The builder copies source captures, seeds referrer-policy on sitemap a sides, copies those a sides to b, then applies the declared three/one changes; set_header updates headerCount.
Its target replacement uses shutil.rmtree and it rewrites expectations under the supplied root; running it only inside the scratch copy prevented committed-file mutation.
The builder relies on source shape and updates only the first same-name header; this audit establishes reproduction for the frozen inputs, not behavior on malformed or duplicate-header inputs.
No production files, frozen controls, global configuration, credentials, or external state were modified; no network was used and no tools were installed.
No LSP tool is exposed in this seat's tool inventory; source inspection used file reads. No symbol change/refactor was performed.
No builds, linters, formatters, production classifier tests, or C1/C2 counters were run; those remain the parent's integration gates.
No dead ends, partial reads, observed control mismatches, or blockers remain within this assignment.

## Files written
- This report.
- The retained audit driver and audit-output.txt under the exclusive ExecControlAudit receipt directory.
