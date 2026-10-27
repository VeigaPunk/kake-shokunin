# CriticGuardSemanticsV2

ATTACKS: C2 guard semantics vs committed wave-1 attacks K23–K36, CR1–CR8 and P5–P7. Axes: operability (guard), freshness/sourced only as indirectly affected; no C1/C3 implementation inspected.

CASES:

| id | fixture | tool result | class |
|---|---|---|---|
| CR1 / K23 | Base `a,d,z`; revision `a,[r60-correction 2026-10-27],d,evil,d,z`. The later duplicate `d` permits a tag-led alignment that leaves `evil` inside its run. | Exit 0, `files=1 findings=0`. Command: `python3 -B scripts/append_guard.py --root <fixture> --base <base> --revision <rev>`. | Disclosed limit: exact existential rule, explicitly carried in contract § Stated limits. It nevertheless demonstrates laundering of an untagged inserted line. |
| P5 | Base contains an earlier tagged correction; append an untagged line after it. Tested at base=revision's parent, so the prior tag is part of B. | Exit 0, `files=1 findings=0`. Same command shape. | Disclosed limit: contract expressly describes an older tag allowing adjacent untagged text to ride in a run; rolling base is the stated mitigation. |
| CR2 / K30a,b | Link-title and heading tag placement. | UNRUN. | Not classified; no claim made. |
| CR3 / K28 | Colon-suffixed legacy correction tag. | UNRUN. | Not classified; strict spelling is a stated limit. |
| CR4 / K36 | Empty-base and missing-final-newline edge cases. | UNRUN. | Not classified; empty-base `x` case is a stated limit. |
| CR5 / P6 | JSON knowledge files outside default `.md` scope. | UNRUN. | Not classified; contract explicitly discloses `.md` scope. |
| P7 | Frozen round-55 base window vs parameterized base. | UNRUN. | Not classified; contract discloses guard does not reproduce c55 frozen window. |
| CR6–CR8, K24–K27, K29, K31–K35 | Remaining semantic/CLI and exact-output assertions. | UNRUN. | Not classified. |

UNDISCLOSED:

None established by the executed fixtures. The CR1 output is a concrete false-clean under ordinary-language “untagged insertion” semantics, but the exact behavior is disclosed in the contract and cannot be treated as an undisclosed counterexample. P5 likewise is disclosed. Tests marked UNRUN remain unknown, not evidence of correctness.

FINDINGS:

| severity | target file:line | issue | evidence command | fix |
|---|---|---|---|---|
| medium | `scripts/append_guard.py` (any_clean_alignment) | Existential alignment accepts a malicious duplicate-line insertion that hides `evil` in a tag-led run. Contract explicitly discloses this limit; do not claim the guard detects every untagged insertion. | Built isolated fixture with base `a,d,z` and revision `a,TAG,d,evil,d,z`; tool returned `files=1 findings=0`, exit 0. | Smallest safe correction: retain disclosure in operator-facing C2 claim/report; if stronger semantics are required later, tighten matching rule and add this exact fixture without breaking K15. |
| low | `scripts/append_guard.py` (default scope) | Guard does not cover JSON knowledge blobs; this is a deliberate disclosed scope boundary, not full-corpus append-only protection. | Not run here; contract § stated limits says default `corpus/knowledge/**/*.md`. | Keep scope limitation explicit; widen only if C2 is intended to cover non-Markdown blobs. |

VERDICT: C2 has a demonstrated laundering counterexample, but it is exactly the disclosed existential-alignment limit; no undisclosed gap established in this review. P5 is also reproducible and disclosed. Several assigned attacks remain unrun and are not validated.