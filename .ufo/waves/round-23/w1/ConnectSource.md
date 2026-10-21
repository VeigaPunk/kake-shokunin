## Verdict

One bounded, non-blocking source/coverage seam: keep the validator's foreign-content handling fail-closed, but make its authority explicit in the current knowledge entry and keep “could-not-evaluate” distinct from clean in C2 reporting. This improves operability by preserving a replayable rejection boundary and freshness by giving the new parser rule a dated source trail; it does not broaden policy or claim browser/Google equivalence. No independent admission is claimed.

## Findings

### P2 — Foreign-content behavior is present in code and fixtures, but its standards boundary is not in the current knowledge entry

**Evidence (local repository / round-23 cache only):**

- `corpus/knowledge/static-canonical-preflight.md:13-30` distinguishes the relation semantics from policy: RFC 6596 permits relative and different-host targets (13-16); Google guidance is not a selection guarantee and absence/cross-domain are not inherently errors (18-25); exact agreement with `expectedCanonical` is explicitly the lane's stricter local policy, not an RFC violation (27-30).
- `corpus/SOURCES.md:28-35` scopes S020 to preferred-relation semantics, S021 to Google's documented signals/limitations, S023 to the WHATWG canonical link-type keyword, and S026 to Python HTMLParser's tokenizer limitations. It has no source row for the foreign-content/tree-building rule. The knowledge entry's source list (`static-canonical-preflight.md:1`) likewise has no WHATWG row.
- The round-22 lesson already states the intended bound: `corpus/lessons/round-22.md:108-110` says canonical/base declarations in ambiguous unsupported contexts, including foreign content, must not become browser-equivalent clean results. In the candidate validator, `scripts/canonical_audit.py:197-224,285-302` permits ordinary SVG/MathML after the explicit head but marks a canonical-looking `link` in that subtree unsupported; `:351-362` makes an unsupported parser shape fail `finish_supported()`.
- Concrete counterexample to the broad claim “body SVG/MathML is always safe to ignore”: the self-test declaration at `scripts/canonical_audit.py:814` expects `<svg><link rel=canonical ...></svg>` to produce `html_unsupported`, while `:815-816` has ordinary body SVG/MathML positive controls. Conversely, `:804`'s `wrong_host` fixture is a local `canonical_mismatch`; it is not evidence that RFC 6596 forbids a cross-host target (see knowledge-entry lines 14-15 and 25-30).
- The cached C2 result makes the outcome distinction operationally relevant. `.ufo/waves/round-23/live/plazir15-ghp/fetch.json:2-12` records a GET, status 200, and a body digest; its `audit.json:2-12` is `exit: 2`, finding `html_unsupported`, verdict `could-not-evaluate`. The body has a head canonical at `page.html:3-10` and body SVG at `:43-45`. This is an observed result, not proof that SVG caused it; the audit receipt does not report the parser reason.
- The frozen contract is narrower than “all 12 sites have a clean canonical verdict”: `.ufo/waves/round-23/contract.json:22-26` requires reproducible snapshots/audit receipts and records non-served status, while explicitly limiting conclusions to fetch-time bytes and policy comparison—not search-engine selection. `SKILL.md:212` likewise says a clean exit applies only to evaluated checks and skipped/suspended sections are not complete-check proof.

**Affected axes:** Operability—operators need an explicit not-evaluated class rather than interpreting an exit-2 receipt as a policy pass. Freshness—foreign-content handling is new behavior but lacks a directly scoped, dated source row in the current knowledge entry. The C1 population does not include `static-canonical-preflight.md`, so this proposal claims no C1 receipt or count improvement in this round.

**Proposed move (one bounded change):** promote the round-22 foreign-content qualification into `static-canonical-preflight.md`, classify the current treatment as the lane's conservative parser boundary, and attach a source-registry row only after opening the relevant official WHATWG HTML parsing section. Preserve the current three-way distinction: ordinary body SVG/MathML may coexist with a valid head signal; a canonical-looking foreign-subtree link is unsupported; a policy mismatch remains a policy finding, not a standards violation. Keep C2 summaries explicitly partitioned into `clean`, `failed-policy`, `could-not-evaluate`, and `not-served`; a replayable receipt in the latter two classes is operational evidence, not a clean canonical evaluation.

**Risks:** HTMLParser is not an HTML5 tree builder (`static-canonical-preflight.md:67-72`), so adding a WHATWG citation must not be presented as browser emulation. WHATWG is a living standard; date and exact section need recording. Do not infer Google-selected canonical behavior from the local validator or from a fetched body. The cached Plazir result's `html_unsupported` cause is not established by the receipt.

**Verification (not run here):** after the source note is integrated, re-open the exact official source section and record its access date; run `python3 scripts/canonical_audit.py --selftest` and `python3 .ufo/waves/round-22/matrix.py --root .`; then use the round-23 C2 counter on the integrated revision and confirm `could-not-evaluate` remains distinct from `clean`. This session did not invoke a runtime or rerun any check.

## Checked and held

- Read `PROVINCE.md:50-58`: the lane's canonical artifact is local publisher-policy validation, not a live repair or Google-selected-canonical observation; the broader rendered-canonical frontier remains open.
- Read `corpus/README.md:42`, `corpus/knowledge/static-canonical-preflight.md:1-94`, `corpus/SOURCES.md:28-46`, `SKILL.md:208-214`, and `.ufo/waves/round-23/contract.json:1-30`.
- Read the round-23 C2 population, validator implementation/self-test declarations, and cached fetch/audit receipts. No public URL was fetched; no runtime, self-test, matrix, build, or counter was run. No source files or round state were changed; only this report was written.

## Limits

Evidence is restricted to the current round cache and local repository. External RFC/WHATWG/Google pages were not reopened, so no claim is made that their contents were independently current-verified in this run. Fixture declarations and cached receipts were inspected, not executed or independently admitted.