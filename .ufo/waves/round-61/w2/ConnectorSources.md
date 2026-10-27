# ConnectorSources

Cross-source pattern scan for S430–S433 (round-61 C2 capability acquisition) and S001–S010 (round-61 C3 oldest-10 freshness due set) across the round-61 worktree, retained bodies, receipts, census tooling, and wave-1/wave-2 evidence.

## 1. Cross-Source Pattern Scan

### S430–S433 (C2 response-header expectation audit rows)
- **S430** (`https://www.rfc-editor.org/rfc/rfc6797.html`): `kind: spec`, `tier: A`, scope `HSTS policy signalling (STS response header)`. Anchor: §§6.1 and 5.1 (RFC 6797, Nov 2012). Retained body: 133,951 B, SHA-256 `f086bfac…`, HTTP 200 on 2026-10-27T09:14:55Z. Gate quote: "The Strict-Transport-Security HTTP response header field (STS header field) indicates to a UA that it MUST enforce the HSTS Policy" (20 units, 130 chars, §6.1). Contract typo `rfc6790` was corrected before row drafting; row references RFC 6797 exclusively.
- **S431** (`https://www.w3.org/TR/CSP3/`): `kind: spec`, `tier: A`, scope `Content-Security-Policy header as policy conveyance`. Anchor: §3.1 (W3C Working Draft `WD-CSP3-20261027`, 27 Oct 2026). Retained body: 1,011,256 B, SHA-256 `be8f2468…`, HTTP 200 on 2026-10-27T09:14:55Z. Gate quote: "HTTP response header field is the preferred mechanism for delivering a policy from a server to a client." (18 units, 104 chars, §3.1).
- **S432** (`https://fetch.spec.whatwg.org/`): `kind: spec`, `tier: A`, scope `X-Content-Type-Options nosniff value rule`. Anchor: §3.6 (WHATWG Living Standard accessed 2026-10-27). Retained body: 1,854,393 B, SHA-256 `63b0a018…`, HTTP 200 on 2026-10-27T09:14:55Z. Gate quote: "Web developers and conformance checkers must use the following" (9 units, 62 chars, §3.6).
- **S433** (`https://www.rfc-editor.org/rfc/rfc9110.html`): `kind: spec`, `tier: A`, scope `Content-Type field semantics and HTTP field-line rules`. Anchor: §§8.3 and 5.2 (RFC 9110, June 2022). Retained body: 1,187,554 B, SHA-256 `d4317606…`, HTTP 200 on 2026-10-27T09:14:55Z. Gate quote: "Although Content-Type is defined as a singleton field, it is sometimes incorrectly generated multiple times" (15 units, 107 chars, §8.3).

### S001–S010 (C3 oldest-10 freshness due set)
- **S001** (`actions/upload-pages-artifact` `action.yml` at v4.0.0 AND main `5f327015`): `kind: code`, `tier: A`. Recheck cell: `on-release` (carried unpinned).
- **S002** (`actions/upload-pages-artifact` release notes v4.0.0 AND v5.0.0): `kind: code`, `tier: A`. Recheck cell: pinned to `2027-01-17`.
- **S003–S007** (GitHub Docs & REST API): `kind: docs`, `tier: A`. Recheck cells: pinned to `2027-01-17` (`opened + 90d`).
- **S008** (GNU tar manual `tar.texi` at commit `cfdb891b`): `kind: docs`, `tier: A`. Recheck cell: pinned to `2027-10-19` (`opened + 365d`).
- **S009** (nginx source `ngx_http_core_module.c` at tag `release-1.28.0`): `kind: code`, `tier: A`. Recheck cell: pinned to `2027-10-19` (`opened + 365d`).
- **S010** (RFC 9110 HTTP Semantics `https://www.rfc-editor.org/rfc/rfc9110.html#section-8.8`): `kind: spec`, `tier: A`. Recheck cell: pinned to `2027-10-19` (`opened + 365d`).

---

## 2. Source-Row Reuse and Duplicate URL Scope Effects

### The RFC 9110 Multi-Row Reuse Cluster
Across the 171-row registry, RFC 9110 is cited by 5 distinct rows:
- `S010` (`rfc9110.html#section-8.8`): Entity tag validators.
- `S028` (`rfc9110.txt`): http/https URI scheme authority.
- `S033` (`rfc9110.txt`): Content-Type media-type grammar.
- `S088` (`rfc9110.html#section-15.4`): Redirects and 404/410 status codes.
- `S433` (`rfc9110.html`): Content-Type singleton semantics and field line combining rules.

`scripts/sources-census.sh` (`url_of`) normalizes URLs by stripping URI fragments (`#...`), trailing slashes, and protocol schemes, folding hostnames to lowercase:
- S010, S088, and S433 map identically to `www.rfc-editor.org/rfc/rfc9110.html`.
- S028 and S033 map identically to `www.rfc-editor.org/rfc/rfc9110.txt`.

**Scope Evaluation:**
- Census rule `E04` flags duplicate normalized URLs with *identical* scope (exit 1).
- Census rule `W04` flags duplicate normalized URLs with *different* scopes (exit 0).
- Because S010, S088, and S433 declare mutually distinct scopes, census emits exactly two W04 warnings (S088 and S433) against `rfc9110.html`, retaining clean exit 0.
- Creating S433 rather than reusing S010 or S088 is strictly governed by `SOURCES-CONTRACT-v1` Rules 1 and 2: a row is an immutable claim tied to a specific learner scope. Reusing S010 would either dilute S010's narrow entity-tag validator scope or require an illegal in-place edit of immutable fields.

### Multi-URL Packing Anti-Pattern (S001 and S002)
In contrast to the clean single-URL, multi-row pattern of S433/S010, legacy rows S001 and S002 pack two URLs separated by semicolons into a single `source` cell:
- S001: v4.0.0 `action.yml` AND main commit `5f327015.../action.yml`.
- S002: v4.0.0 release notes AND v5.0.0 release notes.

**Second-Order Pathologies:**
1. **Census Blind Spot:** `sources-census.sh:601` uses `match(s, /https?:\/\/[^[:space:]|]+/)`, matching only the first URL in the string. The second URL is invisible to `E04`, `W04`, and cross-lane `shared` detection.
2. **Automated Recheck Asymmetry:** Recheck fetchers (`w1/ExecC3Fetch.files/fetch_recheck.py`, `scripts/source_recheck.py`) perform a single GET per row, retrieving only the primary URL.
3. **Anchor Displacement & Freshness Pinning Halting:**
   - In S001, the anchor specifies `inputs.include-hidden-files lines 17-20 and Archive artifact steps lines 37-39`.
   - The primary fetched URL (v4.0.0) contains no `include-hidden-files` input (that input exists only in the second URL at `5f327015`), and its Archive artifact steps occupy lines 24–39/42–57/60–76.
   - `ExecC3Quote` observed `include-hidden-files` 0 times and returned `verdict: anchor_moved`.
   - `ExecC3Pins` therefore excluded S001 from concrete date pinning, leaving S001 as the sole unpinned due row carried at `on-release`.
   - In S002, only the v4.0.0 release page was fetched; the v5.0.0 changelog clause was never verified on the wire, resulting in an unverified shadow claim.

---

## 3. Tier Conflicts and Governance

### S431: Contract REC Claim vs Substrate Working Draft
- Contract.md §C2 (lines 147, 203) explicitly designates S431 as a "W3C CSP Level 3 REC row" and assigns `kind: spec`, `tier: A`.
- The retained HTML body (`sources/S431.html`) identifies the document as `WD-CSP3-20261027`, a W3C **Working Draft** dated 27 October 2026.
- Under W3C process, a Working Draft is not a Recommendation (REC). `SOURCES-CONTRACT-v1` line 26 defines Tier A as "primary or authoritative for that scope (spec, official docs, source code, original paper, maintainer statement...)".
- While S431's Tier A status is defendable based on the authority of the Web Application Security Working Group, the contract text carries a factual error ("REC"). ReviewerC2Sources and ScribeC2Rows documented this conflict, confirming that the row must remain labelled as a Working Draft to prevent contract-to-substrate drift.

### S009: Strict Scoping of Implementation Code
- S009 cites nginx C source code (`ngx_http_core_module.c`) as `kind: code`, `tier: A`.
- Tier conflict is prevented by strict scope limitation: "nginx's own ETag format only; not an assertion about the GitHub Pages backend". This avoids illegitimate tier inflation (using third-party C code to make assertions about GitHub Pages' proprietary CDN architecture).

### S008: Pinned Upstream Manual Source
- S008 cites GNU tar's manual as `kind: docs`, `tier: A` using Savannah cgit texi source (`tar.texi` at commit `cfdb891b`), demonstrating valid Tier A authority when HTML documentation portals experience network timeouts.

---

## 4. Quote Collisions and Text-Node Fragmentation

### Intra-Page Quote Collision in S005
- S005 cites GitHub Docs custom-domain configuration for Actions-published sites across two sections: "Configuring an apex domain" and "Configuring a subdomain".
- Candidate quote `"Under 'Custom domain', type your custom domain, then click Save"` and statement `"no CNAME file is created, and any existing CNAME file is ignored and is not required"` appear verbatim in both sections (`count == 2`).
- Under the lane's quote rule, quotes must be page-unique. `ExecC3Quote` had to reject these candidate spans and locate a section-specific sentence in the apex opening to satisfy the uniqueness constraint.

### Inter-Row Quote Independence on Shared Document (S010 vs S433)
- Both S010 and S433 draw quotes from the same 1.18 MB HTML file (`rfc9110.html`).
- S010 quotes §8.8.1/§8.8.3 ("An entity tag consists of an opaque quoted string, possibly prefixed by a weakness indicator.").
- S433 quotes §8.3/§5.2 ("Although Content-Type is defined as a singleton field, it is sometimes incorrectly generated multiple times").
- Because they target distinct sections, no text collision occurs between the rows, demonstrating that multiple rows citing the same standard can maintain independent, page-unique quotes.

### Specification Node Fragmentation (S432 and S431)
- WHATWG Fetch (S432) uses dense inline markup (`<code>`, `<a>`, `<c-*>`), fragmenting normative sentences across multiple sub-6-unit text nodes. The normative ABNF production `X-Content-Type-Options = "nosniff"` and the comparison algorithm cannot be captured in any single text node. S432's Gate quote was forced to settle for an introductory lead-in ("Web developers and conformance checkers must use the following", 9 units), with normative grounding relying on entry prose and section citations.
- In W3C CSP3 (S431), the header name `Content-Security-Policy` sits in an adjacent `<code>` node, forcing the Gate quote to begin at "HTTP response header field is the preferred mechanism..." (18 units).

---

## 5. Clean Future Study Path

Currently, `corpus/SOURCES.md` contains 12 study sequences under `## Paths`. S010 is integrated into "Validators and crawl hygiene", but S430–S433 are absent from all paths.

### Proposed Study Path:
```markdown
- HTTP response-header expectation audit — S433 → S010 → S430 → S432 → S431: establish HTTP field-line combining rules and Content-Type singleton semantics (S433), connect to entity-tag validator guarantees (S010), establish transport security declaration over HTTPS (S430), enforce MIME-type conformance via nosniff (S432), then verify content policy conveyance (S431).
```

**Pedagogical and Standards Flow:**
1. **S433 (RFC 9110 §§5.2, 8.3):** Establish foundational HTTP field lines, comma-combining order, and Content-Type singleton rules.
2. **S010 (RFC 9110 §8.8):** Connect representation metadata to entity-tag caching and conditional validation.
3. **S430 (RFC 6797 §§5.1, 6.1):** Enforce transport security policy signalling via `Strict-Transport-Security`.
4. **S432 (WHATWG Fetch §3.6):** Enforce MIME-type protection via `X-Content-Type-Options: nosniff`, preventing clients from overriding the Content-Type established under S433.
5. **S431 (W3C CSP Level 3 §3.1):** Deliver declarative client-side execution boundaries via `Content-Security-Policy`.

---

## 6. Synthesis and Proposed Bounded Move

### Affected Axes
- **Freshness (C3):** Unblocks automated cadence pinning across the oldest registry rows.
- **Operability (C2):** Provides an authoritative, ordered study sequence for the response-header audit pipeline.
- **Calibration (C1):** Eliminates census parsing blind spots and rectifies contract-to-substrate discrepancies.

### Proposed Move
1. **Land the `HTTP response-header expectation audit` Study Path:** Append the 5-step sequence (`S433 → S010 → S430 → S432 → S431`) to `corpus/SOURCES.md` under `## Paths`.
2. **Decompose Legacy Multi-URL Rows in Round 62:** Establish an explicit registry rule that every row must carry exactly one URL in its `source` cell. In round 62, supersede S001 by splitting it into:
   - S001-superseding row: v4.0.0 `action.yml` (invariant tar exclusions, line-addressed).
   - New row: main commit `action.yml` (`inputs.include-hidden-files`).
   This eliminates the `anchor_moved` failure mode, allowing S001 to pin to a concrete date.
3. **Correct S431 Contract Nomenclature:** Amend future contract references to reflect S431 as a W3C Working Draft (WD) rather than a Recommendation (REC), preserving Tier A under Working Group authority without document-status exaggeration.

### Verification
- Run `sources-census.sh validate --file corpus/SOURCES.md`: verified exit 0, exactly 16 W04 warnings (15 base + S433).
- Path addition under `## Paths` does not alter table structure (NF=13), preserving census compliance and C3 Condition C6 row-level byte identity.

VERDICT: S430–S433 and S001–S010 exhibit clean cross-row RFC 9110 reuse (S433/S010 via W04) but reveal a critical failure in multi-URL rows (S001 anchor split halting C3 pinning); synthesized study path S433→S010→S430→S432→S431 connects both clusters cleanly.
