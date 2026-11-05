# ExecIndexTwin — agreement check, C1 predicate (round 97)

Twin written from `c97_index.py` docstring lines 1-45 only (code not read).
Twin: `twin_index.py` (sha256 22b9f3b9f5d02ef70a5c832707b37fbb15ba642f76c9275a1a85e1a58df9dacb).
Frozen counter: `c97_index.py` (sha256 8535150e91bd610bd42186b3ad8be23477b0386a1f8d14b95aba8375788aa008, verified against controls/instrument-sha256.txt).

Commands (cwd = scratch, rc observed):
- `python3 twin_index.py --root LANE --revision 36d148f5… --work SCRATCH` → rc=1 (`twin-base.txt`)
- `python3 twin_index.py --root LANE --revision 9e27ce0b… --work SCRATCH` → rc=0 (`twin-repair.txt`)
- `python3 -B c97_index.py --root LANE --revision 36d148f5… --work SCRATCH` → rc=1 (`counter-base.txt`)
- `python3 -B c97_index.py --root LANE --revision 9e27ce0b… --work SCRATCH` → rc=0 (`counter-repair.txt`)

Summary lines:
- base twin: `TWIN … entries=84 indexed=46 unindexed=38 dangling=0 mismatches=38 met=false`
- base counter: `C1v97 … entries=84 indexed=46 unindexed=38 dangling=0 mismatches=38 met=false`
- repair twin: `TWIN … entries=84 indexed=84 unindexed=0 dangling=0 mismatches=0 met=true`
- repair counter: `C1v97 … entries=84 indexed=84 unindexed=0 dangling=0 mismatches=0 met=true`

Per-entry agreement (counter per-entry = absence from line-2 `unindexed` JSON; line-2 lists unindexed entries only, so indexed = not listed):
- base: agree 84/84, disagreements 0
- repair: agree 84/84, disagreements 0

## Readings the twin chose (docstring allowed more than one)
- R1 fence: line starting with ``` or ~~~ toggles fence state.
- R2 header: pipe line followed by a GFM delimiter row; "Entry" matched after stripping backticks/space, case-folded.
- R3 table body: consecutive pipe lines after the delimiter; first non-pipe ends the table.
- R4 source line: first 15 lines, stripped line starting with literal `source:`; S### and ranges (hyphen or en dash) expanded.
- R5 (c) words: alphanumeric tokens across all non-Entry cells; >=8 tokens and >=2 distinct tokens of >=6 letters occurring in the entry text (case-folded).
- R6 exclusion: fence/HTML-comment state evaluated at the row line.
- R7 dangling: only backticked `knowledge/X.md` tokens. A first twin draft also counted `.json` tokens (4 at each revision); the docstring names `.md` only, so I restricted it. This is a twin-side correction, not a counter disagreement; the counter reports dangling=0 at both revisions.

Where the readings could matter (not exercised beyond this population): the R5 letter count (I used alphabetic length of the token), the R2 delimiter-row test, and the R6 comment handling. All 84 entries land identically under the twin's readings, so this population did not discriminate between them.

## Per-entry table
| entry | twin base | counter base | twin repair | counter repair | verdict |
|---|---|---|---|---|---|
| `accessibility-review-packet.md` | true | true | true | true | agree |
| `baidu-dead-link-types.md` | true | true | true | true | agree |
| `baidu-friendly-crawl-guidance.md` | true | true | true | true | agree |
| `baidu-mobile-matching-error-causes.md` | true | true | true | true | agree |
| `baidu-spider-identification.md` | true | true | true | true | agree |
| `baidu-spider-unblocking.md` | true | true | true | true | agree |
| `baidu-spider3-dead-link-model.md` | true | true | true | true | agree |
| `cache-control-effective.md` | false | false | true | true | agree |
| `cache-current-age.md` | false | false | true | true | agree |
| `cache-key-conformance-gate.md` | false | false | true | true | agree |
| `cache-key-construction.md` | false | false | true | true | agree |
| `canonical-selection.md` | true | true | true | true | agree |
| `capture-drift-validators.md` | true | true | true | true | agree |
| `claim-count-derivation.md` | false | false | true | true | agree |
| `commit-citation-hygiene.md` | true | true | true | true | agree |
| `conditional-list-membership.md` | false | false | true | true | agree |
| `conditional-request-evaluation.md` | false | false | true | true | agree |
| `crawl-budget-consequences.md` | true | true | true | true | agree |
| `crawl-error-status-table.md` | true | true | true | true | agree |
| `crawl-scope-per-host.md` | false | false | true | true | agree |
| `crawler-identity-signals.md` | true | true | true | true | agree |
| `crawler-identity.md` | true | true | true | true | agree |
| `crux-bigquery-origin-membership.md` | true | true | true | true | agree |
| `crux-keyless-check.md` | true | true | true | true | agree |
| `drift-detection.md` | false | false | true | true | agree |
| `dynamic-rendering-workaround-limits.md` | true | true | true | true | agree |
| `field-performance-cwv.md` | true | true | true | true | agree |
| `fire-journal-codes.md` | false | false | true | true | agree |
| `fleet-registry.md` | false | false | true | true | agree |
| `free-read-verbs.md` | false | false | true | true | agree |
| `freshness-sweep.md` | false | false | true | true | agree |
| `gate-agreement-metadata.md` | false | false | true | true | agree |
| `gate-status-ledger.md` | false | false | true | true | agree |
| `ghp-custom-domain.md` | false | false | true | true | agree |
| `ghp-etag-anatomy.md` | false | false | true | true | agree |
| `ghp-served-set.md` | false | false | true | true | agree |
| `ghp-subpath-spotcheck.md` | false | false | true | true | agree |
| `google-user-triggered-fetchers.md` | true | true | true | true | agree |
| `googlebot-verification.md` | true | true | true | true | agree |
| `header-change-classes.md` | true | true | true | true | agree |
| `heuristic-freshness.md` | false | false | true | true | agree |
| `hreflang-declaration.md` | true | true | true | true | agree |
| `http-date-grammar.md` | true | true | true | true | agree |
| `http-list-and-method-grammar.md` | false | false | true | true | agree |
| `instrument-receipts.md` | false | false | true | true | agree |
| `js-rendering-queue.md` | true | true | true | true | agree |
| `keeper-timer-inert.md` | false | false | true | true | agree |
| `kimi-subpath-audit.md` | true | true | true | true | agree |
| `link-preview-metadata.md` | true | true | true | true | agree |
| `meta-robots-directives.md` | false | false | true | true | agree |
| `mirror-pitfalls.md` | false | false | true | true | agree |
| `ops-automation.md` | false | false | true | true | agree |
| `origin-repos.md` | false | false | true | true | agree |
| `pages-base-path.md` | true | true | true | true | agree |
| `policy-value-classes.md` | false | false | true | true | agree |
| `probe-delta-alerting.md` | false | false | true | true | agree |
| `publish-channels.md` | false | false | true | true | agree |
| `publish-queue.md` | false | false | true | true | agree |
| `receipt-integrity.md` | true | true | true | true | agree |
| `redirect-rewrite-rules.md` | true | true | true | true | agree |
| `referrer-policy-effective.md` | true | true | true | true | agree |
| `render-static-sites.md` | true | true | true | true | agree |
| `render-web-services.md` | true | true | true | true | agree |
| `response-header-expectations.md` | true | true | true | true | agree |
| `revalidation-exchange.md` | false | false | true | true | agree |
| `robots-txt-limits.md` | true | true | true | true | agree |
| `robots-txt-rules.md` | true | true | true | true | agree |
| `security-txt-publishing.md` | false | false | true | true | agree |
| `sidecar-reobservation.md` | true | true | true | true | agree |
| `sitemap-formats.md` | false | false | true | true | agree |
| `sitemap-orphan-audit.md` | true | true | true | true | agree |
| `speedrun-pipeline.md` | false | false | true | true | agree |
| `static-canonical-preflight.md` | false | false | true | true | agree |
| `stored-response-reuse.md` | false | false | true | true | agree |
| `vary-matching.md` | false | false | true | true | agree |
| `vault-properties.md` | true | true | true | true | agree |
| `x-robots-tag-header.md` | true | true | true | true | agree |
| `yahoo-japan-deleted-url-recrawl.md` | true | true | true | true | agree |
| `yahoo-japan-link-target-crawl-restriction.md` | true | true | true | true | agree |
| `yahoo-japan-nonexistent-url-recrawl.md` | true | true | true | true | agree |
| `yahoo-japan-rel-nofollow-semantics.md` | true | true | true | true | agree |
| `yahoo-japan-robots-pattern-syntax.md` | true | true | true | true | agree |
| `yahoo-japan-robots-txt-basics.md` | true | true | true | true | agree |
| `yahoo-japan-robots-txt-refusal-rules.md` | true | true | true | true | agree |

EXEC-TWIN agree_base=84/84 agree_repair=84/84
