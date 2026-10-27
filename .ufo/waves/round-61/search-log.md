# Search log — round 61, seat ScribeSearchLog

Lane: kake-shokunin. Date: 2026-10-27 (UTC). Base revision `9f07731a873585e655a6518233ea39f5d9fb8204`;
the reads below were made from the lane worktree whose `git rev-parse HEAD` printed
`eaa9177e2965a50fa038d57254934a53909052b6` (read-only; this seat committed nothing, checked out nothing).
Scope of this log: three bounded searches (A, B, C) that the round-61 build needed before writing the
C1/C2 instruments. Nothing here is a claim; it records what was looked for, where, what was found, and
why the sweep stopped. No live fetch, no clone, no fixture was made for these searches.

## A — does any existing lane tool already detect receipt rewrites?

Question: before building `scripts/receipt_lineage.py`, does the lane already own a committed check that
turns an undisclosed post-commit rewrite of a receipt into a finding?

Query (case-insensitive, whole-file): `lineage`, `rewrit`, `receipt-history`, `receipt_history`,
`pending_filled`, `undisclosed`. Earlier related query: `receipt[-_]?(pin|errata)`, `errata`, `revision\s*:`.
Where: `kake-shokunin/scripts/` (28 code files: 25 `.py`, 3 `.mjs`; `fixtures/` and `__pycache__/`
excluded), the whole of `kake-shokunin/corpus/knowledge/` (57 `.md` files), plus `SKILL.md`,
`SCORECARD.md` and `.ufo/waves/round-57/` for the counter the lessons name.

Screened / included / excluded:
- `scripts/`: 28 screened; `lineage` 0 files, `undisclosed|pending_filled|receipt_history` 0 files,
  `rewrit` 6 files (`append_guard.py`, `base_path_selftest.py`, `citing_set_selftest.py`,
  `id_resolver.py`, `redirect_audit.py`, `sitemap_audit.py`) — all excluded on reading: each occurrence
  is about rewriting a *file inside a fixture/scope* (append_guard), rewriting an *expectation*
  (selftests' docstrings), a host *rewrite rule* (redirect_audit), or a grammar *rewrite* of an
  implementation (sitemap_audit), never about a committed receipt's history.
- `corpus/knowledge/`: 57 screened, 21 matched the query terms, 0 included. Every match is body prose
  about HTML/byte rewriting (kimi mirrors, `mirror-pitfalls.md`, `drift-detection.md`), a publisher
  rewrite rule (`redirect-rewrite-rules.md`), or the words "are not rewritten" in append-only recheck
  notes (`ghp-etag-anatomy.md`, `crawl-scope-per-host.md`, `static-canonical-preflight.md`,
  `ghp-served-set.md`, `ghp-custom-domain.md`). `corpus/knowledge/receipt-integrity.md` (round 45) is
  the adjacent entry: it binds a receipt to the run that wrote it (validity of one version), and it
  contains no occurrence of rewrite, relabel, history or `git cat-file` — excluded as out of class.
- Adjacent instrument found (included as a *conflict to report*, not as an answer): 
  `.ufo/waves/round-57/c57_receipt_pins.py`, 870 lines, committed. It walks the whole ancestry,
  follows renames, compares every commit with its first parent, and counts `undisclosed_relabels`
  against `.ufo/waves/round-57/receipt-errata.json` (6 entries, rounds 52/55/56). Its population is
  frozen narrower: `POP_RE = ^\.ufo/waves/round-5[2-7]/(control|controls)/[^/]+\.(txt|json)$`; its
  receipt detector is `REV_RE` (a 40-hex `revision:`/`revision=` line) only; its predicate is
  round-57-specific (`new_receipts == 3 AND scorecard_pin == 1`), so it cannot pass on a later tree.
  `SKILL.md:1273` registers it as `receipt-pin-counter`, marked historical and "red on later trees by
  design"; `SCORECARD.md:4362` and `:4378` carry the round-57 rows. `pending` appears in that file only
  inside selftest fixture bodies (lines 526, 532), so it has no `pending_filled` kind.

Stop rationale: both scopes were swept exhaustively (whole `scripts/` tree by extension, whole
`corpus/knowledge/` by glob), and the only history-reading instrument in the lane was found and read at
its definitions. A wider sweep cannot answer the question differently unless a tool lives outside
`scripts/`, so I extended once to `.ufo/waves/round-5*/` (the lessons' own pointers) and stopped.

Result, stated plainly: no lane *script* detects a receipt rewrite. The lane does own a committed,
wave-local relabel counter for rounds 52–57 `revision:` pins. The round-61 contract's motivation
sentence — the lane owns no committed check for the class — is therefore true of `scripts/` and of the
144-file population, and not true of `.ufo/waves/round-57/`. That conflict is reported verbatim for the
canonical judge; this seat does not resolve it.

## B — does any lane gate already audit response headers?

Question: before building `scripts/header_audit.py`, does any committed lane gate compare recorded
response headers with declared expectations?

Query (case-insensitive): `strict-transport`, `content-security-policy`, `x-content-type-options`,
`header_audit`, `response_snapshot`, `headers`. Where: `kake-shokunin/scripts/` (same 28 files), then
`corpus/knowledge/` and `corpus/lessons/` by the three policy-header names.

Screened / included / excluded:
- `scripts/`: 28 screened, 0 matched the three policy-header names; 0 file named or mentioning
  `header_audit` / `response_snapshot`. Header *capture* exists only as one field: `live_snapshot.py`
  reads `response.headers.get("Content-Type")` (lines 81, 85) into the `contentType` meta key (line 97);
  `source_snapshot.py` returns the header object and keeps only `Content-Type` (lines 199, 200); 
  `receipt_replay.py` parses `contentType` of the round-23 captures as an RFC 9110 media type.
  Excluded on reading: `redirect_audit.py` (manifest of redirect/rewrite *decisions*),
  `base_path_audit.py` (its own not-covered list at line 28 names response headers), `canonical_audit.py`
  (line 5), `sitemap_audit.py`, `robots_audit.py`, `link_preview_audit.py`, `receipt_replay.py`.
- `corpus/knowledge/` + `corpus/lessons/`: 0 files match any of the three header names; no
  `response-header-expectations` entry exists yet, so the C2 entry is new ground, not a duplicate.

Stop rationale: the header-audit question reduces to a name search over the only executable directory
(`scripts/`) plus the knowledge base; both returned zero for the three policy fields, and the two
capture tools were read at the lines that touch headers to confirm they store a single field and audit
nothing. Further sweeping would only re-find the same captures.

Result: no existing lane gate audits response headers against declared expectations. Two tools record a
subset (`Content-Type`) for other purposes; nothing matches HSTS, CSP, `X-Content-Type-Options` or
field-line duplication.

## C — the considerthese proposals not taken this round (1, 3, 4, 5)

Read: `considerthese/2026-10-26.md` Part 2 (five proposals), against `contract.md` "Considerthese:
proposal 2 … is claim C1; proposals 1/3/4/5 recorded as read with reasons not taken this round."

- Proposal 1 (read the lane's own tool receipts daily instead of duplicating them) — excluded: it is an
  operator-scribe *practice* change with no lane surface, no committed instrument and no falsifiable
  predicate on operability/freshness/calibration; the evidence it would read (id_resolver, landed_check,
  frontier map) is already committed and cited.
- Proposal 3 (operator-decision queue with wait counts) — excluded: it orders work for the operator and
  needs operator input; it cannot be met or failed by an in-lane counter, and its four items (calibration
  sub-axis, CJK quote rule, SHONEN promotion, `wip/operator-save-20261023`) are already carried in the
  round-61 contract and the dispatch text as operator-held.
- Proposal 4 (gate-agreement ledger over verifier agree/disagree counts) — excluded: it is bookkeeping
  over *past* spot-check verdicts, would restate the R60-D1 process note, and adds no new instrument;
  the round-61 shape gives the verifier a fresh w2 instead.
- Proposal 5 (historical-gate list for gates red by design) — excluded: the same fact is already
  committed in `SKILL.md:1273` (the `receipt-pin-counter` row carries its historical note and its pin)
  and in the round-60 pin cell; a second list would drift from the first with nothing to measure.

Stop rationale: the five proposals are a closed list in one committed file; all five were read, one is
already C1, four are excluded above. Proposal 2 was not re-argued here (it is the contract's own claim).

Counts: identified 5, screened 5, included 1 (proposal 2, already claim C1 by the contract),
excluded 4 (reasons above).
