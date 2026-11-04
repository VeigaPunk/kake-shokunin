# ReviewC2 — round 84 wave w1

Axes: freshness/capability acquisition; calibration/evidence integrity; operability/offline reproducibility.

## Findings by severity

### High — instrument unavailable at review snapshot
- `scripts/policy_value_class.py` was absent on initial read and two bounded rechecks.
- Read-only `git diff fe42ad11eb1084ad2ea68d12c5bbb2922a089868 -- scripts/policy_value_class.py` exited 0 with no output; this does not establish existence of an untracked implementation.
- The actual frozen C2 counter exited 1: `real_changed=-1`, `real_verdict=tool-unevaluable`, `record_equal=0`, `determinism=0`, `tool_offline=0`, `selftest_ok=0`, `met=false`.
- Receipt: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-84/w1/ReviewC2/counter.json`.
- Consequently no implementation boundary, selftest, import reuse, caller, or error-path behavior is represented as exercised here. A later landing requires a new implementation review.

### High — frozen reorder-equivalence table is not universally semantically sound
- `contract.md:104-118,130-138` requires referrer-policy `no-referrer, strict-origin` → `strict-origin, no-referrer` to be `reordered` and hence equivalent.
- Manual grammar derivation agrees with the frozen syntactic class: the two directive multisets match and only order changes.
- But Referrer-Policy fallback lists choose the last recognized policy. For an agent recognizing both tokens, these values select `strict-origin` and `no-referrer`, respectively; outgoing referrer disclosure changes.
- This is a concrete value pair the field-agnostic grammar misclassifies as equivalent in the semantic sense claimed by C2, even if an implementation perfectly follows the frozen table.
- The finding is about the frozen contract, not an observed implementation defect. Do not patch the frozen expectations; qualify the claim as syntactic reorder classification, or repair field-specific semantics in a later contract.
- Additional grammar limitation: valid Expires dates such as `Wed, 04 Nov 2026 11:47:14 GMT` are not comma-separated name[=parameter] directives. Decisive `unclassified` is honest for this unsupported policy field, not proof of changed semantics.

### Medium — deterministic canned real output can satisfy the predicate
- `c84_policy_values.py:178-181` trusts the real stdout summary's `changed` and `verdict`; it does not independently derive real changed-policy rows.
- `:183-195` compares only control change-row dictionaries with frozen expectations, plus selected summary values.
- `:197-217` checks stored-output equality, repeat-output equality, a textual import scan, and the tool's own selftest exit code.
- Therefore yes: a tool can compute both control runs correctly, branch on the real pair, emit a matching canned real string, and return 0 for its selftest. If the committed record contains that same canned string, every predicate conjunct can be true. This is a logical construction from the acceptance code, not an executed mutant or a claim that any author did this.
- `record_equal` adds provenance/record freshness: the saved receipt must match current output. `determinism` only compares two live outputs and cannot detect a stale committed receipt. Neither establishes input dependence, generalization, correct row arithmetic, or semantic correctness.
- Exact closing checks: independently enumerate normalized changed policy headers from both input header lists; require change-row keys to equal that set; independently classify each value pair; validate exactly one declaration-ordered surface row per id; reject duplicate, unknown, missing, or extra rows/fields; require every surface category count to match its change rows and `changed` to equal the category sum; require summary counts to equal surface sums and derive verdicts from those counts.
- Add counter-owned, unpredictable offline mutations of real-pair copies at paths unrelated to control names: numeric change, reorder, add, remove, unparsable value, and swap A/B. Require independently derived expected changes/verdicts, invalid-receipt rejection, and preservation of untouched surfaces. This rejects the specified real-pair canned branch; no finite public fixture suite proves arbitrary absence of hardcoding.
- `:199-200` also uses `rstrip("\n")`, removing all terminal newlines rather than the contract's one newline. `:201-202` ignores the second process exit code; equal stdout with a failed second run still passes `determinism`.
- Offline evidence is limited: `:43-44,136-141` scans only direct import syntax in the one tool. It does not inspect transitive imports or dynamic imports and is not a sandbox/no-socket proof.

## Independent receipt verification and manual classification
- Independently loaded all 18 response documents and their referenced body files, without calling either production classifier or the counter's `receipt_ok`.
- All six real receipts and all twelve synthetic receipts pass GET, exact integer status in 100..599, byte length, recomputed SHA-256, and literal false truncation checks.
- All sides retain body lengths primary=78897, robots=62, sitemap=7810.
- Full per-receipt checks and literal before/after header values: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-84/w1/ReviewC2/independent-receipts.json`.
- Real primary changes exactly four headers: date, x-fastly-request-id, x-served-by, x-timer.
- Real robots changes exactly five: date, x-cache, x-fastly-request-id, x-served-by, x-timer.
- Real sitemap changes exactly the same five names as robots.
- All 14 names are in `header_change_class.py:42-48`'s frozen per-request set. No changed name is policy: 4+5+5=14, per-request=14, policy=0.
- Thus the real pair's `policy-unchanged` verdict is arithmetically correct independently of whether the new tool exists.
- Control primary: cache-control `max-age=600` → `max-age=60`; same directive name, one numeric parameter difference => `numeric_parameter`.
- Control robots: x-frame-options absent → `SAMEORIGIN`; presence alone => `header_added`, before applying the value parser.
- Control sitemap: referrer-policy `no-referrer, strict-origin` → `strict-origin, no-referrer`; frozen multiset rule => `reordered` (semantic caveat above).
- Equivalent pair: only sitemap's identical referrer-policy reorder changes; primary and robots have zero changed fields.
- Frozen arithmetic therefore gives control changed=3, numeric_parameter=1, header_added=1, reordered=1, verdict=policy-changed; equivalent changed=1, reordered=1, verdict=policy-rewritten-equivalent.
- Boundary requirements not dynamically tested against an absent tool: reversed presence must be `header_removed`; malformed changed `max-age==60` must be `unclassified`, making the surface and summary `policy-unclassified` even alongside ordinary changes. The two frozen pairs do not test either case.

## Commands, scope, and verification gaps
- Command: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff fe42ad11eb1084ad2ea68d12c5bbb2922a089868 -- scripts/policy_value_class.py`; exit 0, empty output.
- Command: `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-84/c84_policy_values.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --work /fast/scratch/hyaku/kake-r84/ReviewC2/counter`; exit 1, stderr empty; full stdout retained.
- Independent Python Eval audit completed normally; it was an in-process cell, not a subprocess with a reported exit code. Its retained receipt contains every check and every changed value.
- LSP device discovery returned `No such tool: xd://lsp`; no server/status/reference/definition/diagnostic route is mounted. Static source/line inspection is the explicit fallback, not semantic-reference proof.
- No network, installation, VCS mutation, production edit, alternate agent runtime, or subagent dispatch occurred.
- Scratch `/fast/scratch/hyaku/kake-r84/ReviewC2` was removed in `finally`; observed `scratch_removed=True`.
- One canonical agent runtime was used. No rerouting, saturation claim, or resume path is in this diff's scope; no resume-continuity claim is inferred.
- Residual risk: these receipts validate retained bytes, not authenticity of their original HTTP acquisition. The counter's syntactic controls do not establish arbitrary policy semantics.
- Self-evaluation: accuracy 4 (no implementation available); completeness 4 (implementation checks explicitly blocked); clarity 4 (separates syntax from semantics); actionability 4 (specific counter checks); conciseness 4 (receipt details kept out of report). Overall 4.0. Highest-impact next step is review of the landed tool, then independent mutation checks; neither is claimed passed.

## Verdict
Recommendation: C2 is not presently established (`met=false`, instrument absent). The real-pair 14/14 per-request arithmetic is verified, but frozen reorder equivalence overclaims semantic preservation and the predicate permits canned real output. No admission or integration verdict is issued.
