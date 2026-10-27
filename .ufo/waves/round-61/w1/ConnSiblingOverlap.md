# ConnSiblingOverlap

Sibling-overlap scan across `/home/vgpnk/Projects/shokunin/*-shokunin` (read-only) for round 61's three surfaces: receipt-lineage watch and undisclosed rewrite detection (C1), offline response-header expectation audit (C2), and live re-verification and date-pinning of the ten oldest registry rows S001–S010 (C3). Evaluated against base revision `9f07731a873585e655a6518233ea39f5d9fb8204` (2026-10-27). RULES.md channel record: no tools installed or updated.

OVERLAPS:

1. Receipt/measurement integrity & lineage watch (C1: scripts/receipt_lineage.py, c61_lineage_cases.py, .ufo/receipt-disclosures.json, population of 144 controls)
- **kumitate-shokunin** (`PROVINCE.md:3-7`, `SKILL.md:94-126`, `corpus/knowledge/receipt-identity-canonicalization.md:16-38`): owns orchestration and task receipt verification (`ufo-task-receipt-v1`), defining receipt record identity as canonical JCS JSON digest, not byte identity. Explicitly notes that "a byte rewrite with a recomputed sidecar passes the byte layer and is caught only by the window/tolerance policy".
- **tameshi-shokunin** (`PROVINCE.md:3-7`, `SKILL.md:476, 783, 860`): owns verification-fixture craft (honest checks, hermetic suites). Enforces "all 102 prior ledger rows + receipts byte-stable" invariant and measures single-edit mutants while classifying coordinated-rewrite mutants as unmeasured risk.
- **chousa-shokunin** (`PROVINCE.md:3-8`, `corpus/knowledge/receipt-verifier-subject-r39.md:7-24`): owns deep-research method and verifier-subject receipt binding (`verifier-sha256-mismatch`), preventing a weakened verifier from silently re-adjudicating old receipts.
- **kama-shokunin** (`PROVINCE.md:17`, `SKILL.md:1441-1541`): operates historical deletion and mutation audits (`tools/append-only-audit.py` v1–v6) with an external disclosure ledger (`registry/append-only-disclosures.tsv`) tracking sha256 line keys.
- **souji-shokunin** (`PROVINCE.md:3-4, 10-30`, `census/round-9/final-24.json:102`): owns fleet repository and workspace hygiene, enforcing receipt-gated removal and guarding against J13 class defects where read-only receipt inspections rewrite repository indices.
- **kake distinction**: Kake's C1 (`scripts/receipt_lineage.py`) evaluates git first-parent history exclusively over its own 144 frozen control files in `.ufo/waves/round-*/control*/`, detecting alterations in result spans (`# receipt:`, `revision:`, `EXIT=`, `met=`, etc.) and pending fills against `.ufo/receipt-disclosures.json`. It asserts no authority over sibling receipts.

2. HTTP response-header semantics (C2: scripts/response_snapshot.py, scripts/header_audit.py, c61_header_cases.py, S430–S433)
- **tabi-shokunin** (`PROVINCE.md:3-7`, `SKILL.md:1614`, `corpus/knowledge/redirect-and-retry-after-semantics.md:3-35`, `corpus/knowledge/rate-limit-policy-fields.md:61`): owns browser & web-interaction craft, consuming response headers (RFC 9110 §15.4 3xx redirect status codes and Retry-After header) strictly from the client journey driver perspective. Uses ephemeral test server setting `'x-content-type-options': 'nosniff'` (`scripts/webmcp-validation-round19.mjs:735`) in local loopback test harnesses only. Tabi drives browsers; kake owns publisher-side placement and expectations.
- **chousa-shokunin** (`PROVINCE.md:3-8`, `corpus/SOURCES.md:71`, `corpus/knowledge/exempt-hop-audit-r32.md:3-16`): cites RFC 9110 (S061) origin-server semantics (404 and 410) solely for evaluating whether dead links and citation hops can be followed.
- **mori-shokunin** (`PROVINCE.md:3-7`, `corpus/SOURCES.md:48, 227`, `corpus/knowledge/source-drift-hardening-r37.md:3`): cites RFC 9110 (S042, S221 §15.4) for redirect semantics in SSRF probe defense.
- **kama-shokunin** (`PROVINCE.md:100`, `SKILL.md:72, 171-176`): checks HTTP response headers (`Server: llama.cpp`, `Content-Type: application/json`) on local model-serving loopback endpoints.
- **Fleet-wide query scan**: 0 sibling lanes own publisher-side response-header expectation auditing (`Strict-Transport-Security` / RFC 6797 S430, `Content-Security-Policy` / CSP3 S431, `X-Content-Type-Options: nosniff` / WHATWG Fetch S432, or RFC 9110 S433 Content-Type and singleton field enforcement). Kake's C2 captures public surfaces via GET-only snapshot and audits headers offline without network access.

3. Registry recheck and cadence pins (C3: S001–S010 live re-verification, corpus/SOURCES.md recheck cells, c61_recheck_pins.py)
- **chousa-shokunin** (`PROVINCE.md:3-8`, `SKILL.md:37, 88`): owns research method and quote-reopen verification (`tools/quote-reopen.py`).
- **kagi-shokunin** (`PROVINCE.md:54-55`, `SKILL.md:48, 787`): operates `corpus/release-clock.py` + `corpus/release-clocks.tsv` to bind `on-release` registry rows to external release feeds.
- **tabi-shokunin** (`SKILL.md:1614, 2470`): validates in-lane `corpus/SOURCES.md` via `node scripts/check-sources.mjs`.
- **kumitate-shokunin** (`PROVINCE.md:15`, `SKILL.md:613`): runs `node scripts/sources-check.mjs`.
- **kasegi-shokunin** (`SKILL.md:981`): runs `recheck-audit.py` to audit recheck receipt digests.
- **Fleet-wide census**: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` validates SOURCES-CONTRACT-v1 syntax across all 21 lanes. Its grammar (`:663-667`) explicitly permits valid ISO dates (`YYYY-MM-DD`), `NNd` cadences, and symbolic strings (`on-release`, `on-use`). Kake's C3 re-verifies S001–S010 live and pins concrete future dates into recheck cells, fully preserving fleet census syntax without imposing recheck policies on siblings.

CONTESTED:

1. **Receipt rewrite and lineage semantics (C1 vs kumitate / kama / tameshi)**:
   - Kumitate defines record-level JCS canonical digests; kama uses external line-key TSV disclosure tables; tameshi tests byte stability.
   - Contested boundary: If kake claimed global fleet receipt authority or redefined "receipt identity" for other lanes, it would conflict with kumitate's JCS standard.
   - Finding: Kake's `scripts/receipt_lineage.py` and `.ufo/receipt-disclosures.json` are bounded strictly to kake's own 144 frozen control files in `.ufo/waves/round-*/control*/`. Sibling receipt models remain autonomous.

2. **Publisher response-header expectations vs client/endpoint headers (C2 vs tabi / kama)**:
   - Tabi consumes HTTP headers as a client driver; kama checks local inference endpoints.
   - Contested boundary: Any claim regarding general web browser header handling would encroach on tabi's province.
   - Finding: Kake's C2 audits publisher-side response headers on its 12 public surfaces (ds4cc.com, kimi.page mirrors) offline via `scripts/header_audit.py`, testing publisher compliance (HSTS, CSP, nosniff, singletons). Tabi's client-side driving and kama's local model endpoints remain uncontested.

3. **Registry recheck date pins vs external feeds (C3 vs kagi / chousa / fleet)**:
   - Kagi binds `on-release` rows to release feeds; chousa validates citation chains; the fleet validates SOURCES syntax.
   - Contested boundary: Forcing concrete ISO date pins across fleet registries would break kagi's feed-driven model.
   - Finding: Kake's C3 pins concrete dates (`opened + cadence` or `opened + 90d`) only into kake's own `corpus/SOURCES.md` S001–S010 recheck cells upon live HTTP 200 and located anchor quotes. It adheres to fleet `sources-census.sh` syntax and exports no constraints to sibling lanes.

NON-OBVIOUS SYNTHESIS & MOVES:
- **Evidence**: Sibling inspection confirms zero fleet ownership of publisher-side HTTP response-header expectation audits (C2), while receipt-auditing (kumitate/kama/tameshi) and registry verification (chousa/kagi/tabi) are strictly partitioned by lane domain.
- **Affected Axes**: Operability (C2) and Freshness (C3), protected by Calibration (C1 lowest axis).
- **Proposed Move**: Maintain complete hermetic isolation across all three tools: (1) confine `scripts/receipt_lineage.py` to kake's `--root` with git first-parent walking and `.ufo/receipt-disclosures.json`, avoiding cross-repo receipt interference; (2) keep `scripts/header_audit.py` strictly offline, consuming only pre-recorded `response.json` capture receipts in manifest v1, guaranteeing no live network drift touches the audit; (3) ensure C3's pinned ISO dates (`YYYY-MM-DD`) in `corpus/SOURCES.md` evaluate cleanly under `scripts/sources-census.sh validate` with future due dates (`2027-01-17` and `2027-10-19`), preventing `overdue` warnings.
- **Risks**: Allowing `header_audit.py` to make live HTTP requests would violate the offline audit boundary and duplicate tabi's browser/fetch territory. Altering historical receipt files rather than disclosing via JSON would break C1's 144-file population fence. Invalid date formats in `SOURCES.md` would trip fleet-wide E09 syntax errors.
- **Verification**: Run `python3 -B scripts/receipt_lineage.py --selftest`, `python3 -B scripts/header_audit.py --selftest`, and `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`.

VERDICT: Sibling scan confirms zero contested overlap: kumitate/kama receipt tooling is self-scoped, tabi's header handling is client-side while kake's C2 audits publisher expectations offline, and kake's C3 concrete date pins strictly respect fleet sources-census syntax; nothing is absorbed.
