# ExecCalc — round 86 candidate

Axes: contract correctness; offline isolation; reproducible evidence; minimal stdlib implementation.

## Deliverable

Candidate `.ufo/waves/round-86/w1/ExecCalc/cache_control_effective.py` is intended for L1 integration into `scripts/cache_control_effective.py`; no production file changed. It implements ordered case-insensitive directives, quoted-string/quoted-pair parsing, first-occurrence duplicate handling, bounded delta-seconds including very long strings, shared freshness precedence, qualified/unqualified no-cache, flags, HTTP-date fallback, input-type validation, exit codes, and isolated subprocess selftests.

## Source and access

Read mandatory host rules, frozen contract, counter declarations and invocation code only (not frozen CASES), and local `.ufo/waves/round-86/sources/rfc9111.txt` §§1.2.2, 4.2.1, 5.2, 5.2.2.1/.4/.5/.10. No network calls, credentials, installations, production edits, VCS mutations, or delegation. LSP is unavailable: no LSP tool is mounted in the current tool inventory. New-file implementation requires no symbol refactor.

## Retained evidence and defect

- `.ufo/waves/round-86/w1/ExecCalc/initial-receipt.txt`: initial selftest exit 0 (28 isolated fixtures), counter exit 1, 14/15, selftest_ok=1, tool_offline=1.
- `.ufo/waves/round-86/w1/ExecCalc/spelling-repair-receipt.txt`: same outcomes after preserving qualified field-name spelling. This corrected unnecessary output normalization but did not increase the counter total.
- `.ufo/waves/round-86/w1/ExecCalc/final-receipt.txt`: final selftest exit 0 (29 fixtures); counter exit 0, cases=15/15, selftest_ok=1, tool_offline=1, met=true.
- Counter commands are recorded in full in the receipts; counter itself was never modified. No lint/build/unassigned test run.

## Explicit bounded conventions

This is not an RFC-complete cache or storage-permission model. `storable` is false only for no-store; no-store yields null lifetime, not the RFC age equation. Negative Expires differences clamp to zero. Expires fallback requires both supplied dates, with no receipt-time inference. All supplied date strings are validated eagerly, even when max-age takes precedence, because the seat expressly requires unparsable dates to exit 1. Presence flags do not model prohibited-argument semantics for bare directives. Qualified no-cache output preserves field-name spelling; field-name comparison is case-insensitive in HTTP. Vary/Age/Pragma/private permission/must-understand permission remain outside scope.

No-options with JSON decodes, as required by the assigned counter. No-options with empty input returns usage64. The wording 'No args ... exit64' conflicts with the counter's no-options JSON interface; this is the narrowly compatible interpretation, not an invented required positional option.

L1 KakeR86 explicitly authorized interpreting conflict as global conflict from unqualified no-cache only. The original seat wording included any no-cache; literal implementation passed 14/15. Reviewer identified the qualified-form discrepancy without the implementer opening frozen CASES. Final candidate adopts L1's authorized convention, not a claim that the original wording was unambiguous. Qualified no-cache alone does not set conflict; unqualified no-cache with max-age does.

Selftest uses TemporaryDirectory honoring TMPDIR and deletes its fixtures. Tool runtime auto-backgrounded synchronous requests on peer interruptions; this seat requested no background execution.

## Handoff and self-evaluation

Author-side candidate measurement only; no independent closure, committed-carrier result, C1 result, assimilation append, or D84 queue closure is claimed. L1 owns integration and post-integration counter execution. D84-2 and D84-3 remain retained-open. No installations or tool updates.

Self-evaluation (1–5): accuracy 4 (bounded contract passes; not full RFC semantics); completeness 4 (candidate complete, integration reserved to L1); clarity 4 (two ambiguous seat conventions explicitly disclosed); actionability 4 (candidate plus exact receipts ready, parent must integrate); conciseness 4 (receipts intentionally retain both failed measurements). Overall 4.0. Most important improvement is parent-side integration with the documented bounded conflict convention; no broader conformance inference is justified.

Report: .ufo/waves/round-86/w1/ExecCalc.md
