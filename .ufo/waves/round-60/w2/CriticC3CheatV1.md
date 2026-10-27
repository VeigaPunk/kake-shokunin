# CriticC3CheatV1
ATTACKS: C3 at B1 with frozen v1 counter; tested the measured tree, then checked adversarial claim semantics beyond the declared quote-truth limits.

CHEATS:
- Measured B1 directly with `python3 -B <clone>/.ufo/waves/round-60/c60_quote_truth.py --root <clone> --revision 8b33fd248d126b48d838af5c38bc175850f41a09 --json`; output reports all C1–C9 pass, `conditions_passed: 9`, `met: true`, `exit: 0`.
- No safe one-line “cheat” commit was made: C3 checks the retained immutable body hashes and receipts, so altered source HTML cannot evade this counter without breaking those checks. The strongest extant counterexample is a semantic/provenance contradiction in the actual correction, already passing 9/9.

HOLES:
- The S428 article says “generally ignore”; the entry faithfully records that qualified quote (lines 30–34, 67–76), but the correction goes beyond the source: “a publisher still cannot count on robots.txt to hold a user-triggered fetch back” and “the later page no longer says that every such fetch ignores it” (googlebot-verification.md:41–42). “Generally” neither defines exceptions nor establishes what publishers can count on; the entry itself concedes the source names no exception (google-user-triggered-fetchers.md:32–34, 80–81). Thus the correction presents an inference as sourced posture, despite C9 quote truth. This is the exact semantic-support gap named in contract § C3 limits (line 252 / § C3 line 186).
- Counter C9 accepts any qualifying quote attached to a correction-tag line, plus presence of stale wording and tag. It does not assert that adjacent prose is supported, nor that claims distinguish source text from inference.

TIGHTENINGS:
- Do not make C3's freshness predicate pretend to prove semantic fidelity through more lexical checks. Require reviewer adjudication that each substantive conclusion is explicitly marked `[INFERENCE]` or directly supported by source text; here revise the correction's absolute publisher guidance into an explicitly labeled inference or remove it. Keep the `generally` qualification and explicitly state the exception is unspecified.

FINDINGS:
| severity | target file:line | issue | evidence command | fix |
|---|---|---|---|---|
| medium | corpus/knowledge/googlebot-verification.md:41-42 | Correction attributes practical publisher guidance / universal-negative conclusion to a page that only says “generally” and names no exceptions; counter passes despite contradiction in evidential strength. | `python3 -B .ufo/waves/round-60/c60_quote_truth.py --root <B1 clone> --revision 8b33fd248d126b48d838af5c38bc175850f41a09 --json` → all 9 pass; compare `corpus/knowledge/google-user-triggered-fetchers.md:32-34,80-81`. | Mark the implication `[INFERENCE]` or delete it; describe the source narrowly as qualified and silent on exceptions. |

Impacted axis: C3 freshness/sourced reliability; the frozen counter's 9/9 is a structural/quote-truth result, not evidence that the correction's conclusions are source-supported.

VERDICT: C3 v1 reaches 9/9 at B1, but a passing correction still overstates what its cited source establishes; semantic review remains necessary as the contract acknowledges.