# ReviewRealRunInput — real-input run selection & manifest

Attacked: `realrun/{input.json,manifest.json,audit.json,snap-bodies.tar.xz}` at
`f3a38bf8e68f` — input selection, owned-host inclusion, silent drops, audit
reproducibility. Sandbox `/fast/scratch/hyaku/kake-r36w2/ReviewRealRunInput/`
(clone @f3a38bf8, `snap/` = extracted tarball, `audit-rerun.json`).

## Coverage and drops

94 SOURCES rows vs 90 input ids; missing: **S014, S019, S035, S056**.
- S014 (own-work command), S019 (own-work corpus contract), S056 (sibling-lane
  path): no URL anywhere — correctly un-fetchable; extractor report names all
  three (w1/ExecGateQuoteExtractor.md "rows with no extracted quote",
  "ids with no URL anywhere").
- **S035 — dropped fetchable row (finding).** gate_quotes.json holds one record:
  `https://www.w3.org/TR/2024/REC-WCAG22-20241212/` + quote "Conformance (and
  conformance level) is for full web page(s) only", shape `prose-lookahead`
  (round-25.md:22-23). Every input row's chosen record is `bullet-gate`,
  `table-quote-column` or `table-reopen`, so the builder filtered shapes — S035's
  only shape is prose-lookahead. The drop mechanism is inferable but documented
  nowhere: lesson round-36.md:66 says "90 Gate quotes (one per row id)" without
  naming the 4 skipped ids or the shape rule; extractor notes only "quote is on
  line 23" for S035, not exclusion. Low severity: exclude was deterministic,
  single row, and prose-lookahead is a weak delimiter — but the run's "one per
  row id" wording overstates coverage (89 fetchable → 90 rows incl. drafts is
  consistent only after adding the 7 draft rows; 84 fetchable triples − S035 =
  83 extracted + 7 drafts = 90 ✓).

## Owned hosts — none

`urlsplit` over all 90 input URLs: 42 distinct hosts, zero match against
ds4cc.com, app.ds4cc.com, *.onrender.com, *.kimi.page, *.kimi.pro,
veigapunk.github.io, and every host named in `corpus/knowledge/freshness-pins.json`
(none are URLs there). Two quotes *mention* owned hosts — S052 quote contains
"onrender.com subdomain", S065 quote contains "ds4cc.com/magga/frostbite/" — but
the fetched URLs are `render.com/docs/custom-domains` (vendor docs, not an
operator onrender host) and `github.com/VeigaPunk/ds4cc-marketplace/commit/…`
(allowed by bound). Fetch URLs of S062/S065/S066 are github.com/api.github.com
reads of the public VeigaPunk/ds4cc-marketplace repo — allowed.

## Sample table (15 ids: quote ↔ lesson line ↔ SOURCES row)

All verified verbatim; `record` = extractor record matching both quote and URL.

| id | shape | lesson:line | SOURCES url match | quote in lesson |
|----|-------|------------|-------------------|-----------------|
| S001 | table-quote-column | round-20.md:203 | 2nd of 2 row URLs | yes |
| S004 | table-quote-column | round-20.md:206 | yes | yes |
| S005 | table-quote-column | round-20.md:207 | yes | yes |
| S013 | table-quote-column | round-20.md:215 | yes | yes |
| S020 | table-reopen | round-22-verifier-spotcheck.md:122 | yes | yes |
| S036 | table-reopen | round-28-verifier-spotcheck.md:158 | yes | yes |
| S040 | bullet-gate | round-29.md:36 | yes | yes |
| S052 | bullet-gate | round-30.md:46 | yes | yes |
| S062 | table-quote-column | round-32.md:31 | yes (row also cites local clone) | yes |
| S065 | table-quote-column | round-33.md:31 | yes | yes |
| S066 | table-quote-column | round-33.md:32 | yes (1st of 2 api URLs) | yes |
| S071 | bullet-gate | round-34.md:38 | yes | yes |
| S075 | bullet-gate | round-34.md:42 | yes | yes |
| S087 | bullet-gate | round-35.md:53 | yes | yes |
| S093 | draft (round-36.md:43) | — | yes | yes |

Multi-record ids (S020/S036/S062…) always picked a canonical shape per the
extractor's own advice; no input quote/url pair came from two different records
(checked all 90: `(quote,url)` pair ∈ one extractor record, or draft row).

Drafts S088–S094 (`from: "round-36.md (draft)"`): quote and URL both appear
verbatim in landed `corpus/lessons/round-36.md:38-44` — accurate `from` label.

## Manifest vs snapshot vs input

- `manifest.json` checks=90; id/url/quote identical to input.json (no drift).
- Tarball `./` + manifest.json + receipts.json + 89 `.body` files (S087 recorded
  404 → no `body` key, correct per contract (a)/shape rule).
- `snap/manifest.json` == lane `manifest.json` (sorted-JSON diff identical).
- `receipts.json` 90 items: every `hops` array equals the manifest's; all 89
  `bodySha256` match sha256 of the extracted `.body` files (0 mismatches).

## Audit re-run

`cd snap && python3 -B scripts/source_recheck.py --manifest manifest.json`
→ exit 1; output **byte-identical** to `realrun/audit.json` (verdict
failed-policy, 90 evaluated, 14 findings on 13 rows). `audit.exit`=1 agrees.
Lesson finding census (9 quote_missing/2 moved/1 gone/2 unsupported_type)
matches the JSON exactly.

## Notes (non-findings)

- S071 chain 307→308 gets no `moved` — contract-correct: SCORECARD (b) grants
  `moved` only when the *leading* hop run is permanent
  (`moved_target` source_recheck.py:480 `hops[0] in PERMANENT_STATUSES`).
- S087's input quote is literally the recorded 404 page's text; audit reports
  `gone`, consistent with the rejected row status.
- S016/S066 `unsupported_type` on JSON bodies: contract-plausible (e).

## Residual risk / not verified

- Did not re-fetch any live URL (no fetch authorization this seat).
- S035 exclusion mechanism is inferred from shape distribution, not from a
  builder script — no input-builder code exists in the lane (built at L1 level).
- `snap-bodies.tar.xz` vs original recorder output: verified via receipts
  sha256 only, not against a second copy.

Commands (all exit shown): tar extraction 0; `source_recheck.py` re-run 1;
`git clone`/`checkout` 0; all python3 comparisons 0. Tooling installed: none.
