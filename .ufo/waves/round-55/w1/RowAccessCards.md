# RowAccessCards

Seat: C1 coverage-map calibration, one new row for
`corpus/knowledge/accessibility-review-cards.json`. File read in full (662 lines,
163 613 bytes, top-level JSON array); `corpus/README.md` `## Coverage map` header plus
existing rows read for the 3-cell format. No file was edited; no git or jj mutation;
no network.

ROW:

```markdown
| WCAG 2.2 criterion review cards | `knowledge/accessibility-review-cards.json` | Preparation-only WCAG 2.2 success-criterion cards: a source quote, publisher check procedure, evidence needed, failure example and limitation per card; status is not-assessed and each names the shared handoff record. |
```

Cell checks (run, output observed):
- Area = 5 whitespace tokens (limit 8); no round tag emitted because the file carries
  none — top level is a bare array with no header object, and `r\d\d` / `round \d\d`
  matches inside the file: 0.
- Entry = backticked `knowledge/accessibility-review-cards.json`; no ` (S###)` suffix
  because the file's own `source:` lines hold only W3C URLs
  (`https://www.w3.org/TR/2024/REC-WCAG22-20241212/#…`, 55 distinct fragments, one
  base URL) and `S\d{3}` matches inside the file: 0.
- Coverage = 29 whitespace tokens (limit 10–45); `|` present: no; starts with `TBD`: no.
- Coverage shares 5+ letter words with the file's first 1500 characters
  (`criterion`, `preparation`, `procedure`, `source`); the file has no H1 line, so the
  first-1500-character half of the rule is the only applicable half.
- Table line splits into exactly 3 cells on `|`, matching `| Area | Entry | Coverage |`.

EVIDENCE:

1. `corpus/knowledge/accessibility-review-cards.json:8` —
   "Preparation only: kake inventories the scope and requests a separately operator-authorized evaluator"
   (12 units, exact prefix of `publisherCheck`, present on 55/55 cards) → grounds
   `Preparation-only`.
2. `corpus/knowledge/accessibility-review-cards.json:7` —
   "All non-text content that is presented to the user has a text alternative that serves the equivalent purpose"
   (18 units, exact substring of card 1.1.1 `sourceQuote`) → grounds `a source quote`.
3. `corpus/knowledge/accessibility-review-cards.json:9` —
   "Shared record for every card: reviewer, evaluation date, delivered build/revision"
   (10 units) together with "Use corpus/handoffs/accessibility-preparation.md" (2 units,
   same line, present on 55/55 cards) → grounds `the shared handoff record`.
4. `corpus/knowledge/accessibility-review-cards.json:9,12` —
   "A per-item inventory listing location" (5 units, inside `evidenceNeeded`) and
   `"status": "not-assessed"` (2 units, present on 55/55 cards) → grounds "evidence
   needed" and "status is not-assessed".

Every statement in the Coverage cell rests on a parsed property I measured over all 55
objects: keys `id, title, level, source, sourceQuote, publisherCheck, evidenceNeeded,
failureExample, limitation, status` on every card, no empty string field, no duplicate
`id`, levels `A`/`AA` only, `status` uniformly `not-assessed`.

RISKS:

- **The row duplicates existing ground.** `corpus/README.md:156` already carries a
  round-25 row naming `knowledge/accessibility-review-cards.json` (S035) with coverage
  "Fixed WCAG 2.2 A/AA criterion cards: publisher checks, manual evidence needs and
  limits; packet-structure gate only, no website evaluated". That row is already not
  thin by the round-55 counter predicate (19 tokens, shares `criterion` with the first
  1500 characters), and `c55_readme_index.py` measures only the *first* naming row per
  file, so this new row changes no C1 counter value. Landing it adds a second row for
  one file, not new coverage.
- **The file cannot supply an S-id or round tag.** S035 exists only in
  `corpus/SOURCES.md:43` and in README's round-25 row; the cards file itself records no
  S-id, no round, no authoring date and no fetch date. Adding `(S035)` to the Entry cell
  would therefore be copied from the README, not from the file, so I left it off.
- **Registry attribution gap noticed.** `corpus/SOURCES.md:43` gives S035's `used-by` as
  `corpus/knowledge/accessibility-review-packet.md, corpus/lessons/round-25.md` — the
  cards file is not listed, while README:156 attributes (S035) to it. One of the two is
  stale; I did not decide which, and my row makes no source-attribution claim.
- **No stated count, so no count in the row.** The file states no card count, no
  `all A/AA` and no completeness sentence. My parse counts 55 objects and the id set
  matches the WCAG 2.2 A/AA success criteria as far as I compared them, but that is my
  comparison, not the file's text, so the row says `WCAG 2.2 success-criterion cards`
  and never `all`/`every`/`complete`, and carries no number.
- **Limitation wording is not uniform, so no shared limitation quote is available.** 37
  of 55 `limitation` values contain a "no website was evaluated"-style clause and 18 do
  not; five cards (1.3.4, 1.4.5, 2.4.2, 2.4.5, 3.2.2) open "Packet readiness only" while
  all 55 `publisherCheck` values open "Preparation only". The row therefore states only
  the `status` field, not a paraphrased shared limitation.
- **Cards are instructions only; the row must not read as a result.** Each
  `publisherCheck` is gated ("requests a separately operator-authorized evaluator"), and
  no card records an evaluated website, a pass/fail or a conformance claim. A reader
  could over-read `publisher check procedure` as performed checks; the row's
  `Preparation-only` and `not-assessed` are the guard, nothing more.
- **Anchor freshness unverified from the file.** All 55 `source` values pin the W3C
  Recommendation dated 2024-12-12; the file records no recheck date. I did not fetch any
  W3C URL in this seat (no network use), so whether those fragments still resolve is
  **unrun**, not confirmed.

VERDICT: One calibrated row drafted for `knowledge/accessibility-review-cards.json` (preparation-only WCAG 2.2 criterion cards, per-card quote/procedure/evidence/example/limitation, status not-assessed, shared handoff record), all cell rules script-verified; risk: duplicates the existing round-25 README:156 row and changes no C1 counter.
