# ReviewSemantics — round 86 C2 RFC review

Axes: RFC fidelity; bounded-contract honesty; frozen-case compatibility; evidence reproducibility. This is an author-side scoped review/recommendation, not independent closure or admission. No production edits, counter runs, candidate execution, runtime dispatch, or VCS mutations.

## Findings, highest severity first

### P1 — Candidate snapshot cannot satisfy frozen qualified-no-cache case

`.ufo/waves/round-86/w1/ExecCalc/cache_control_effective.py`, read snapshot E5BB, lines 120–123 lowercases field names and lines 143–144 return that list. Frozen `count.py` case 12 expects `no_cache_qualified=["Set-Cookie"]`; the candidate produces `["set-cookie"]` by direct source evaluation. `count.py` compares JSON values exactly, not field-name semantics. This is a counter-contract mismatch, not an RFC case-insensitivity violation. **Static inference; not executed.** ExecCalc reports a spelling repair; that repair was not reread or verified. Do not infer 15/15 from this review.

The same snapshot sets `conflict=true` whenever max-age and any no-cache appear (line 148; selftest line 192), but frozen case 12 expects false for qualified no-cache. **Static inference.** ExecCalc reports its seat literally requires conflict whenever both appear, and has escalated that counter/seat disagreement to Main. This is an assignment inconsistency to resolve transparently, not permission to retrofit frozen expectations. Qualified no-cache has field-specific semantics; the global conflict flag is a tool convention.

### P2 — Date-absent Expires path is not implemented or expressly excluded by the frozen interface

RFC 9111 §4.2.1, retained source lines 664–667: use Expires minus Date, **“using the time the message was received if it is not present”**. Frozen case 9 supplies both dates and correctly expects 1680 seconds; it does not test receipt-time fallback. The contract permits `date:null` but has no receipt-time input. Candidate lines 136–137 require both dates; an Expires-only input falls through to `basis="no-explicit-expiration"`, even though Expires is explicit expiration information. **Static inference.** A deliberate offline Expires+Date-only convention needs explicit limitation and honest reporting of missing-Date inputs; the current frozen prose says only “Expires − Date fallback”. A full RFC fallback would require receipt-time context, not treating Expires as absent.

### P2 disclosure limit — Candidate rejects an Expires field an RFC cache must ignore

RFC §5.3, retained lines 1494–1498: with max-age, recipients MUST ignore Expires; with s-maxage, shared caches MUST ignore it. Candidate lines 93–94 parse dates before choosing directive precedence. For `{"cache_control":["max-age=60"],"expires":"invalid"}`, `http_date` raises and `main` returns 1 rather than returning lifetime 60. The same applies to shared s-maxage. **Static inference; not executed.** ExecCalc subsequently reports its seat explicitly requires unparsable expires/date strings to exit 1. Therefore this is not a breach of that seat requirement: it is a bounded-input validation convention differing from RFC cache processing. Disclose the distinction; do not silently change schema validation to implement a broader cache model.

### P2 — no-store lifetime-null is a frozen tool convention, not a disclosed RFC equation

RFC §5.2.2.5, retained lines 1297–1305, says MUST NOT store/use (with the must-understand exception cross-reference at 1312–1313). It does **not** define `freshness_lifetime_seconds=null`. Contract lines 48–49 correctly tie no-store to `storable=false`, but do not explicitly disclose lifetime-null. Frozen cases 4/13/14 require null, and candidate lines 128–135 implement it. The convention is inferable from cases, not expressly distinguished from RFC semantics in the contract. Document it as output policy: no-store suppresses computed lifetime in this reader, even if max-age exists. Do not cite §5.2.2.5 as mandating null. ExecCalc says its report will disclose this; no later report was inspected.

### P2 disclosure limit — No-argument directives accept RFC-forbidden arguments

RFC §5.2 retained lines 1108–1109: no argument is defined **“(nor allowed) unless stated otherwise.”** Candidate lines 112–124 parse an argument for any directive but only validate numeric ages and qualified no-cache specially. Consequently `no-store=anything` is placed in `first`, sets `storable=false`, and is absent from `invalid_directives`; similarly `must-understand=anything` sets its flag. **Static inference.** ExecCalc reports its assignment leaves this validation unspecified and asks presence-only decoding. Thus treat this as an RFC-validity limitation of the bounded reader, not a demonstrated breach of an explicit seat validation requirement. A green fifteen-case count would not prove these inputs valid RFC directives.

### P3 — Contract overstates recommendation strength and leaves a normalization implicit

* Quoted arguments: RFC §5.2, retained lines 1098–1102, really says recipients **“ought to accept both forms”**, not MUST. Contract line 45's “recipients accept quoted” is acceptable as the chosen tool behavior but must not be represented as an RFC MUST. Quoted numeric acceptance is source-supported; candidate `argument()` accepts token/quoted forms.
* Duplicate values: §4.2.1, lines 677–684, says either first occurrence **“should”** be used **or** the response **“should”** be considered stale. These are lowercase words, not the contract's uppercase “SHOULD”; first-occurrence is a supported chosen branch, not the only permitted RFC behavior. Keep the witness described as discriminating implementations of the chosen tool rule, not proving universal RFC exclusivity.
* Negative Expires−Date: §4.2 lines 609–613 explicitly supports a past expiration meaning already stale; §4.2's formula at 619–624 also makes a nonpositive lifetime nonfresh for nonnegative age. However §4.2.1 specifies subtraction, not `max(0, ...)`. Candidate line 137 and selftest line 204 clamp negatives to zero. Zero is a defensible nonnegative tool normalization preserving nonfreshness, **not the literal RFC subtraction result**. The frozen contract does not disclose that clamp, and case 9 tests only a positive difference. The stale interpretation has RFC basis; a claim that the RFC mandates numeric zero does not.

## Required checks without an additional defect

* **must-understand scope is disclosed.** Contract lines 58–59 expressly excludes “must-understand store-permission”. RFC §5.2.2.3, retained lines 1252–1256, says a cache implementing that directive SHOULD ignore no-store if it understands and implements the status code's caching requirements. Candidate line 146 only sets presence flag `must_understand`; no status input or status-aware permission logic exists, and no-store still wins. This matches the disclosed bounded scope, not a full storage-permission implementation. `storable=true` must not be sold as full RFC cacheability; the candidate's module docstring already warns it is not a cache permission model.
* **Section citations checked:** quoted forms §5.2; Expires fallback §4.2.1; no-store §5.2.2.5; must-understand §5.2.2.3; s-maxage §5.2.2.10. No numbering defect found.
* No claim about C1 closure, D84-2/3 closure, whole D84 queue closure, assimilation gates, saturation, identity routing, or resume continuity is made: those are outside this seat's C2 semantic assignment.

## Evidence, commands, exits, and limitations

Fresh GET performed 2026-11-04 against https://www.rfc-editor.org/rfc/rfc9111.txt. Retained body: `.ufo/waves/round-86/w1/ReviewSemantics/rfc9111.txt` (1956 lines, 84477 bytes), SHA-256 `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`. Source anchors: https://www.rfc-editor.org/rfc/rfc9111.html#section-5.2 ; https://www.rfc-editor.org/rfc/rfc9111.html#section-4.2.1 ; https://www.rfc-editor.org/rfc/rfc9111.html#section-5.2.2.3 ; https://www.rfc-editor.org/rfc/rfc9111.html#section-5.2.2.5 ; https://www.rfc-editor.org/rfc/rfc9111.html#section-5.3 .

Commands (absolute paths; no shell environment assumed):

1. Initial `mkdir && curl && wc` shell request used nonexistent scratch as cwd and failed before execution; corrected by starting from the existing fleet cwd with all write targets absolute.
2. `mkdir -p /fast/scratch/hyaku/kake-r86/ReviewSemantics-2 && curl -sS -o /fast/scratch/hyaku/kake-r86/ReviewSemantics-2/rfc9111.txt https://www.rfc-editor.org/rfc/rfc9111.txt && wc -lc /fast/scratch/hyaku/kake-r86/ReviewSemantics-2/rfc9111.txt && sha256sum /fast/scratch/hyaku/kake-r86/ReviewSemantics-2/rfc9111.txt` completed exit 0. No HTTP headers/status receipt was captured; the retained fetched body and digest are the evidence, not a claimed independently recorded status 200.
3. Two initial shell text-search batches located RFC clauses (outputs retained in transcript); subsequent evidence was direct ranged file reads. Those shell searches were a tooling-policy deviation; they are not semantic caller proof.
4. `sha256sum` on the candidate, counter, and contract completed exit 0 and reported respectively `cb9ad1314e965e61767ded338da35bd4dca027ae08a79a506aa0519c66ac3ca8`, `f21c3a73f82c053d9a45257a245c92fec35973bb56d7c98c4985eb6e1c2af421`, `cc461017e5960ac29dcdb1bee6e383a93f08f333fb57922252a5d1f7d8f7d365`. Candidate is a live sibling file: the read snapshot E5BB, not any subsequent repair or hash stability, grounds line-level findings.
5. Created only the seat receipt directory and copied the fetched RFC body into it; copy completed without error. Scratch cleanup is recorded in the companion receipt.

LSP device unavailable: reading `xd://lsp` returned “No such tool”. Thus status/references/definition/diagnostics could not be requested; this is source inspection, not semantic-index verification. Candidate inspected once, not polled. No tests/selftests/counters were run; all candidate-output assertions above are explicitly static. No installs or updates.

Residual risk: positive bounded cases do not cover Date absence, invalid ignored Expires, malformed no-argument directives, or negative normalization. Subsequent candidate fixes need the main agent's assigned checks; this report does not verify them. Six requested semantic topics are covered, but the frozen measurement alone cannot establish general RFC conformance.

Report: .ufo/waves/round-86/w1/ReviewSemantics.md

Additional coordination evidence: L1 (`KakeR86`) independently reports RFC 7234 §4.2.1 treats duplicate directive values as invalid and encourages staleness, not a duplicate “most-restrictive” rule. That comparison was not independently fetched by this seat; do not treat the frozen RFC-7234 comparison as verified by this report. Preserve frozen bytes and append any sourced correction rather than changing the measurement.
