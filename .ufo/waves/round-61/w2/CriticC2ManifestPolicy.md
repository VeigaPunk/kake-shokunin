# CriticC2ManifestPolicy

## Axes

Expectation uniformity/predeclaration; false-green resistance (H16); HTTPS-to-HSTS binding; source confinement and receipt integrity; status handling.

## Counterexamples and evidence

1. **All-false expectations force green on violating headers (H16).** Against the committed `scripts/header_audit.py` at `f5a9b8a`, a 200 HTTPS receipt with two `Content-Type` fields and `X-Content-Type-Options: sniff`, but all expectations false, returned `exit=0`, `checks=1 findings=0`. The auditor intentionally evaluates declared expectations only; H16 blesses this clean result, though its own fixture uses compliant headers. Thus the 18-case predicate does not establish that the audit catches policy violations when a manifest under-declares policy. The real manifest is uniform in inspected bytes (12/12 checks have the same four true flags, same singleton list, and `https: true`); this is an artifact fact, not a counter-enforced invariant.

2. **The `https` field overrides the check URL.** A check with `url=https://real.example/`, `https=false`, `hsts_present=true`, and a 200 receipt lacking STS returned `exit=0`. The same check with `https=true` finds missing HSTS. `declared_https()` trusts an explicit boolean; it falls back to the manifest URL scheme only if the field is absent, and never reads the receipt's `finalUrl`. Conversely, setting `https=true` with an HTTPS manifest URL and an HTTP `finalUrl` still produces an HSTS finding. H3 explicitly expects `https:false` to suppress the finding, so this escape is frozen into the passing cases.

3. **Source path is not confined to capture receipts; receipt provenance is not checked by the auditor.** A manifest source of `../outside.json` resolved to a JSON receipt outside the capture directory and returned clean (`exit=0`). `find_receipt()` also accepts absolute paths and searches root, manifest directory, cwd, and repository root. The audit does not bind receipt `url`/`finalUrl` to check `url`, nor validate capture metadata (`fetchedAt`, `userAgent`, `sha256`, `headerCount`, etc.); a fabricated or modified status/headers object can be evaluated as evidence. In the probe, deliberately bogus `sha256` metadata was ignored. The real 12 receipts inspected have matching manifest/receipt/final URLs, `round61` userAgent, fetchedAt, and SHA field; that does not close the tool-level trust gap.

4. **Status behavior observed.** Status 600 yields a per-check `could_not_evaluate status_unparseable` and exit 1; status 301 with missing HSTS yields `hsts_present` and exit 1. Only Content-Type is status-gated to 2xx; HSTS/CSP/XCTO/singleton/syntax checks apply to any parseable 100–599 status. This matches the current frozen prose for Content-Type and is not, by itself, a counterexample to that contract. Missing/malformed per-check receipts are represented as findings (thus exit 1), as H13 specifies.

5. **Current counter's R3 gate is ambiguous at the measured revision.** Running `c61_header_cases.py` at `f5a9b8a` yielded H1–H18 all passing but R3 `pass=false`: `pick_manifest()` finds the canonical `capture/manifest.json` plus committed w1 fixture manifests under `w1/*Critic*.files/` and `w1/*Mutation*.files/`, and `r3_check()` rejects multiple candidates. The JSON output was truncated after listing candidates, but the reported failure and cause are explicit. This prevents the complete predicate from passing at this revision despite the fixture results. R3 should select/require the canonical path rather than treating every materialized version-1 JSON fixture as a competing manifest (or materialization should be scoped to capture/).

## Impacted axes

- **False-green resistance / policy grounding:** H16 accepts under-declaration; expectations are not validated against a frozen policy.
- **HSTS correctness:** explicit manifest `https` can contradict URL evidence and suppress HSTS evaluation.
- **Provenance / source integrity:** path traversal and unverified receipt metadata permit non-capture or altered evidence.
- **Operability:** R3 is currently non-passing due to ambiguous manifest discovery at the tested committed revision.
- **Status handling:** observed behavior is explicit and consistent with the stated status rules; no separate defect asserted.

## Smallest safe correction

For a future counter/tool revision, bind expectations to a predeclared policy (or a single frozen policy table) and make the real-manifest shape gate assert that exact uniform set; derive HTTPS from the checked URL/recorded final URL and reject contradictions; constrain source resolution to the canonical capture subtree and bind each receipt to its check URL/id, while verifying immutable receipt pins. Separately, scope R3 manifest discovery to the canonical `.ufo/waves/round-61/capture/manifest.json`. These are counterexamples to the present claim's enforcement, not changes made to the frozen lane.

VERDICT: C2's current real manifest is uniform and well-formed, but the claim does not enforce that policy: H16 and the manifest-controlled `https` flag permit false-green declarations, source paths/provenance are unbound, and R3 fails from ambiguous committed fixtures; tighten policy/evidence bindings and canonicalize R3 discovery before accepting the claim.