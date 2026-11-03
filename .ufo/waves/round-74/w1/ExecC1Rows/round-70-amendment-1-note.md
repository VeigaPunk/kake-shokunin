# Round 70 — Amendment 1 (recorded after the W1 attacks, before any after-state measurement)

Recorded by the L1 on 2026-11-03 after the W1 build and attack reports
(`w1/ReviewerPredicates.md`, `w1/CriticAdoption.md`, `w1/MutC1Counter.md`, `w1/SentinelAdoption.md`,
`w1/ScribeEntries.md`, `w1/ExecMirror.md`, `w1/ExecCensusProbe.md`) and before any after-state
measurement. The v1 counter's base receipt (`w1/ExecC1Counter/base-run.txt`, unannotated=19) is
kept as history. Predicates keep their sentences; these lines define the terms they use.

## C1 term refinements (counter v2, `.ufo/waves/round-70/c70_pointer_audit.py`)

- Repo-class extraction: extension cap `{1,7}` → `{1,16}` with a right boundary `(?![A-Za-z0-9])`,
  so `.ufo/waves/round-39/r38w2-evidence.SHA256SUMS` is extracted whole instead of truncating to a
  phantom `.SHA256S` token that fails `cat-file` while the real file resolves
  (ReviewerPredicates, live false positive at base).
- A repo token dangles iff BOTH the literal token and its `os.path.normpath` form fail
  `git cat-file -e` — the `scripts/../.ufo/waves/round-51/c51_wave_ledger.py` spelling of a real
  file resolves (ReviewerPredicates). The annotation cell matches the literal token.
- Home/tmp dangling uses `os.path.exists` (`test -e` semantics), not `os.path.lexists`
  (SentinelAdoption: a broken symlink is not a resolving pointer).
- A home token whose expansion escapes `$HOME` is excluded from the population (SentinelAdoption:
  no host-path existence oracle outside the home tree); exclusions print as detail lines.
- The annotation locus is a markdown table row of the section outside fenced code blocks
  (MutC1Counter F7 / SentinelAdoption: a fenced line is not a table row).
- The selftest's dangling tmp token is minted under `TMPDIR`/`gettempdir()`, never a literal
  `/tmp` (round-69 QUALITY criterion; SentinelAdoption found the v1 literal at `:188`).
- New conjunct with `--base <rev>`: `append_only=true` — every base line of `SCORECARD.md`
  survives unchanged at the measured revision (base is a line-prefix of the tip), closing the
  no-effort bypass of rewriting a dangling token into a non-matching spelling
  (ReviewerPredicates). Selftest extended to 8 cases (fenced row, broken symlink, home escape).
- Expected base with v2: `unannotated=17`, exit 1 (19 v1 minus the two live false positives).
  Measured base receipt: `controls/c1-base-v2.txt` (exactly 17). Kill rule unchanged: base green
  ⇒ unprovable.

## Motivating-evidence corrections (contract prose, not predicates)

- The contract's "12 `/tmp/kake-rNN` tokens across the move-log rows 10–18" is corrected to the
  measured population: 9 distinct tokens (11 occurrences; r17 repeats at lines 4461 and 4478),
  8 dangling on this host today (`/tmp/kake-r16` exists — a sweep-selftest fixture directory
  created 2026-11-03T18:50Z, before this round's dispatch; RevengerTmp divergence 2).
- The contract's "staged id S352 collides with the lane registry's S352" is false at base: the
  lane registry holds no `S352` (0 occurrences; 175 rows, max S437). The measured collision set
  of the staged file is `S312 S329 S367 S372 S373 S374 S390 S409` — eight other staged ids, none
  adopted this round. The adopted id stays **S438** by the registry's next-unused rule (first gap
  after the maximum; ids never reused), not by collision; the renumber map is the single pair
  `S352 → S438` with the collision evidence pasted in the report (ExecMirror `collisions`).
- The dated-event class "the 2026-10-12 `~/Projects` W7 prune" keeps the corpus's committed
  annotation date (the r18-era inline annotations say 2026-10-12; the round-18 sweep that caught
  it ran 2026-10-14 — both named in the calibration rows); the lowercase `~/projects` removal is
  the W6 consolidation of 2026-09-29, not W7 (RevengerTmp divergence 3).

## C2 term refinements

- Conjunct (a) pin: the `source:` line within the first five lines carries BOTH the `S438` id and
  the URL `https://developer.chrome.com/docs/crux/bigquery` (ReviewerPredicates).
- Conjunct (c) receipt binding (CriticAdoption §4 + SentinelAdoption §3): the receipt's `sha256`
  and `bytes` must equal the retained file's recomputed values, the receipt's access date is
  2026-11-03, and the retained bytes carry the document's canonical/og:url equal to the entry's
  source URL. Named residual (not machine-checked this round): a fully self-consistent fabricated
  body would still pass; the non-author closure may re-fetch.
- Quote-class pin: `collapsed-only` = whitespace collapse (`\s+` → single space), case- and
  punctuation-sensitive; the mandated C2(c) quote is collapsed-only (three independent
  derivations: ScoutSources, CriticAdoption, ScribeEntries). The ENTRY's own blockquotes are
  raw-substring spans per the round-55 brand-new-entry bar: "a list of all origins included in
  the dataset" (raw, the schema list's description of `origin_summary`) and "it is updated
  monthly with the latest list of origins in the dataset" (raw); the free-tier and account/SQL
  facts are stated in the lane's prose with their collapsed-only derivations recorded in the
  Gate (ScribeEntries finding 2 resolution).
- Conjunct (d′): the registry id set at the tip ⊇ base ids ∪ {S438} (rows 175 → 176; no
  deletion) — the census alone is baseline-free (ReviewerPredicates deletion hatch).
- Anchor correction: the staged anchor "Data structures" does not occur in the retained body; the
  row's anchor is the body's actual headings "§ CrUX on BigQuery → Materialized table schema →
  origin_summary", pinned by the doc's printed "Last updated 2026-10-13 UTC" (ScribeEntries
  finding 3).
- Gate wording correction: the planned reject's probe rows are staged S303 (the CrUX Vis docs
  row) and S304 (the own-work POST probe) — the contract's "S303 companion S304" swapped their
  roles (ReviewerPredicates nit).
