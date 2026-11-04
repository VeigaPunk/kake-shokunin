# ReviewSemantics — round 85 / w1

Axes: field-semantic correctness; independent witness coverage; reproducible evidence; bounded claims; zero production mutation.

## Findings by severity

### High — historical r84 reorder equivalence is false for Referrer-Policy

The retained equivalent-control sitemap pair has `a = no-referrer, strict-origin` and `b = strict-origin, no-referrer`. The independent reference evaluates them to **strict-origin** and **no-referrer**, respectively. Executing the actual legacy classifier on these extracted fields returns `reordered` / `policy-rewritten-equivalent`.

Cause: `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/policy_value_class.py:55-60` compares multisets, erasing order. Lines 78-84 then label an all-reordered change equivalent. This is an observed historical defect, not a newly introduced decoder regression; lines 8-10 expressly limit the legacy grammar. Do not promote its verdict to field-specific semantic equivalence or claim D84 closed. The separate C2 decoder is an appropriate bounded capability, not a repair of every legacy caller.

Evidence: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-85/w1/ReviewSemantics/witness-results.json`; retained inputs are recorded there with absolute paths. Historical printed evidence also exists at `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-84/controls/tool-ctl-equivalent.txt:1-5`.

### Medium — frozen 10/10 is not full decoder-contract coverage

`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-85/count.py:11-22,39-53` tests ten successful JSON invocations only. It never requires recognition of `no-referrer-when-downgrade`, `origin-when-cross-origin`, or `strict-origin-when-cross-origin`; never tests malformed JSON/non-string entries/usage/selftest exit codes; and its uppercase token precedes a valid lowercase token, so that witness alone cannot distinguish case-sensitive matching from lowercasing.

Therefore 10/10 supports exactly the frozen numerator, not exhaustive §8.1 conformance or the entire CLI contract. Preserve the oracle; additional checks supplement, never replace or narrow it. An implementation with only the other five policy tokens could pass all ten while violating the frozen eight-token contract.

## Source attack and located quotes

GET-only source opened: https://w3c.github.io/webappsec-referrer-policy/ on 2026-11-04; rendered document identifies Editor’s Draft, 20 March 2026. This is a mutable work-in-progress source, not an immutable browser-conformance certificate.

- §8.1 step 2: “Let policy be the empty string.” (6 words)
- §8.1 step 3: “if token is a referrer policy and token is not the empty string, then set policy to token.” (18 words)
- §11.1: “unknown policy values will be ignored” (6 words)
- §11.1: “To specify multiple policy values in the Referrer-Policy header, a site can send multiple Referrer-Policy headers” (16 words)
- §4.1 note: “Referrer-Policy header values should not be quoted.” (7 words)

Direct section anchors: https://w3c.github.io/webappsec-referrer-policy/#parse-referrer-policy-from-header and https://w3c.github.io/webappsec-referrer-policy/#unknown-policy-values .

§3 enumerates exactly the eight frozen nonempty tokens plus the empty policy. §8.1 uses membership and successive assignment, not lowercasing or sorting: last recognized nonempty token wins; unknown/empty trailing tokens do not erase a prior valid token. §11.1 explicitly equates repeated headers with comma-separated values in the given order. `NO-REFERRER` is not an enumerated token. An empty parse result is not an instruction to substitute the browser default; §3.9 separately discusses fallback elsewhere.

Whitespace qualification: frozen contract line 11 explicitly strips surrounding whitespace. Our reference covers SP/HTAB, preserves interior characters, and ignores quoted/parameterized unknown strings. §8.1 step 1 delegates token extraction to Fetch; this review did not fetch that separate specification and does not certify arbitrary Unicode whitespace, malformed wire headers, or every HTTP extraction edge case. These are limits on a full-web-conformance claim, not grounds to silently alter the frozen JSON/string abstraction.

## Independent witness execution

Command (exit **0**):

`python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-85/w1/ReviewSemantics/reference_witness.py`

Working directory: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-85/w1/ReviewSemantics`.

**32/32 reference assertions passed**: eight individually recognized tokens; both comma orders; both repeated-field orders; unknown before/after valid; no fields; empty strings/tokens; empty after valid; uppercase-only and uppercase-after-valid; SP/HTAB; quoted and parameterized unknown strings; duplicates; eight unsupported data shapes. Independent reference searches backward for the first recognized token, rather than copying the specification’s forward update algorithm. This tests the hand-expected reference and the legacy counterexample, **not candidate behavior**. The driver reads retained metadata directly and performs no network calls.

Candidate discovery returned missing `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-85/w1/ExecDecoder/*`. Per assignment, no polling/retry was performed. Thus no candidate diff, candidate diagnostics, CLI exit behavior, selftest isolation, or candidate pass count is asserted.

## Outside-closure grounds (recommendations only)

**Admit bounded evidence** if the outside closer separately verifies the integrated candidate implements all eight tokens and ordered last-valid semantics; rejects unsupported JSON with exit 1; returns 64 for usage; emits precisely the prescribed JSON result for successful input; and has isolated selftests with exit assertions. Preserve frozen base/control receipts, unchanged ten-case oracle, and real retained-pair outputs. The present reference receipts substantiate the semantic requirement and r84 counterexample, not integrated admission.

**Reject broad closure** based solely on 10/10, legacy selftest success, order-insensitive multisets, lowercased values, first-valid selection, default-policy substitution, or an implementation ignoring any enumerated token. Reject any full D84-queue closure claim: contract lines 7,13,15 explicitly withhold that scope. C1 is registry discoverability only and is not independently reviewed here.

## Residual risk and verification gaps

- No candidate existed at discovery; implementation review remains outside this report’s evidence. No production files were edited or integrated.
- LSP device unavailable: `read xd://lsp` returned “No such tool.” No server status/references/definition/diagnostics could be requested. Literal searches and direct code reading are not semantic caller-completeness proof.
- No resume/run-routing/saturation logic is changed by the assigned artifact. This seat makes no claims about those unrelated runtime invariants.
- No counter, build, lint, candidate selftest, VCS mutation, browser, publish/deploy, or live property request executed. No tools installed. No sibling/fleet files written. No scratch was created; only final seat artifacts were used.
- Self-dispatched author-side review is not independent outside closure. Assimilation: none.

Self-evaluation: accuracy 4 (candidate unobserved, explicitly bounded); completeness 4 (all requested semantic axes covered, candidate unavailable); clarity 4 (reference and candidate results separated); actionability 4 (admit/reject requirements explicit); conciseness 4 (source and execution receipts retained in one report). Overall 4.0. Highest-impact improvement: outside closer runs the additional cases against the actual integrated candidate. The user should agree with the stated evidence limits.

Report: .ufo/waves/round-85/w1/ReviewSemantics.md
