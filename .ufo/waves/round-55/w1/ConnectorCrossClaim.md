# ConnectorCrossClaim

Cross-claim pattern finder for round 55 W1. Base `fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d`.
Read: `contract.md`, `c55_readme_index.py`, `c55_quote_truth.py`, `corpus/README.md` §Coverage map,
lessons round-50..54, `corpus/SOURCES.md` rows, round-55 receipts. All measurements read-only
(`git show`/`ls-tree`) at base.

INTERACTIONS:

1. **C1 is hostage to C2 (asymmetric).** C1's counter counts `unindexed` over ALL files under
   `corpus/knowledge/` at the measured revision (`c55_readme_index.py:102-111`). C2's three new
   entries (`c55_quote_truth.py:74-78`) raise the knowledge set 46 → 49. If C2 lands without C1's
   rows, the 3 new files are unindexed → `index_mismatches >= 3` → C1 exit 1. C2 has no dependency
   on C1 (its conditions read SOURCES.md/lesson/entries only). So C1 is unverifiable without C2
   landed, never the reverse.
2. **C1 fails if it lands BEFORE C2 (dangling).** C1's `dangling` term resolves every backticked
   token in the coverage-map section (`c55_readme_index.py:119-123`). If C1's rows name
   `knowledge/yahoo-japan-robots-txt-refusal-rules.md`, `knowledge/yahoo-japan-robots-pattern-syntax.md`,
   `knowledge/yahoo-japan-robots-txt-basics.md` (or `lessons/round-55.md`, which only C2 creates)
   before those files exist, each token dangles → C1 fails even though C1's own work is correct.
   Corollary: C1's declared scope ("plus the three new entries") makes C1 fail if C2 is dropped or
   delayed; the two claims must land in the same committed revision, and verification must be run at
   the wave-complete tip, never an intermediate commit.
3. **Exact-basename coupling.** C1's `unindexed` match is exact (`knowledge/<basename>` followed by
   a non-word char, `c55_readme_index.py:107`). C2's basenames are fixed in `ADOPTED`
   (`c55_quote_truth.py:74-78`). If C1 writes a row with any different basename, the result is double
   failure: the real file stays unindexed AND the row's token dangles. C1 rows must cite the exact
   three basenames above.
4. **Thin-check couples C1 rows to C2's H1 choice.** C1 marks a file `thin` if its first naming
   row's coverage cell has <5 tokens or shares no 5+ letter word with the file's H1 + first 1500
   chars (`c55_readme_index.py:113-118`). C1's new rows must therefore be written against the H1
   titles C2 actually authors; a late rename of the entries turns C1's rows thin. Coordination
   requirement, not a counter bug.
5. **Section placement constraint.** `coverage_section` matches only the exact `## Coverage map`
   heading (`c55_readme_index.py:66-68`); rows added under any other heading (e.g. a new
   `## Coverage — round 55`) are invisible to the counter and leave the 21+3 files unindexed. Rows
   must go inside the existing table with the same 3-column shape.
6. **C2 is fragile to any other SOURCES.md append.** C8 asserts `len(rows) == len(mirror_rows) + 1`
   (`c55_quote_truth.py:419-420`) and reconstructs base bytes by removing exactly S418 and restoring
   S372/S373 used-by. Any other row added to the registry this round (quarantine slice is correctly
   not appended, contract.md:76-78) breaks C8. C1 touches no registry file, so C1 vs C2 do not
   conflict here; the risk is external.
7. **No byte-level collision between C1 and C2.** C1 reads `corpus/README.md` + knowledge tree;
   C2 reads/writes `corpus/SOURCES.md`, the three entries, `corpus/lessons/round-55.md`, sources and
   assimilation artifacts. Disjoint files; the only coupling is through the shared revision (1-4).

REPEATED PATTERNS:

1. **Counter never validates quote locator/heading (repeats r52 flaw).** r52's S329/S312 rows
   passed green counters with wrong section anchors (`round-52-verifier-spotcheck.md:84-85`;
   `round-53.md:22` "Quote locator copied from package description"). C5 checks raw substring, unit
   size, URL and date only (`c55_quote_truth.py:285-302`) — there is no heading/section check. A
   quote that is a true substring but located under a wrong section still passes 8/8. This round
   relies solely on the seat instruction ("a located quote names its heading/section"); the counter
   repeats the r52 gap.
2. **CJK unit-vs-word ceiling — avoided for new material, kept flagged for old.** r53/r54 routed
   that S367/S372/S373 measured 31/27/27 units > 25 and the ≤25-word rule was ambiguous
   (`round-53-verifier-spotcheck.md:57,82`; `round-54-verifier-spotcheck.md:67`). This round's C5
   enforces 6..25 units on every new Gate quote and entry span (`c55_quote_truth.py:295-296,313-314`)
   and the contract exempts only S367 (contract.md:56-58). Pattern avoided for new material; S367
   stays flagged.
3. **Mirror-integrity defect — avoided.** r51's C8 read the live registry at the mirror's
   add-commit and never the mirror bytes, so a contaminated mirror could still pass
   (`round-51-verifier-spotcheck.md:80-91`). This round's C8 reads `MIRROR` bytes, pins sha256, and
   hashes the blob at its add-commit (`c55_quote_truth.py:395,414-448`). Fixed.
4. **Dangling cross-registry citations — avoided.** r52 entries cited S367/S372/S373/S390/S409
   absent from kake's registry (`round-52-verifier-spotcheck.md:124-129`). This round S372/S373 are
   existing lane rows (opened r53, verified at base: 11 cells, used-by exactly
   `[NOFOLLOW]` / `[NOFOLLOW, BAIDU]`) and S418 is appended as a new row; the counter's C4 asserts
   the used-by deltas. No unresolvable id is cited if entries cite exactly S372/S373/S418.
5. **Append-only / used-by immutability — enforced.** C3 allows only used-by to differ for
   S372/S373 (`c55_quote_truth.py:248-253`); base rows confirmed byte-stable otherwise. Consistent
   with r52's "no existing row cell changed" conformance (`round-52-verifier-spotcheck.md:64`).
6. **Unverifiable-after-due-to-revision-drift — avoided.** Both counters take `--revision` and read
   committed bytes only; base controls (21 mismatches / 0/8) are frozen. The remaining risk is purely
   the ordering dependency in INTERACTIONS 1-2.

POINTERS TO UPDATE:

- **README: none.** `grep` of `corpus/README.md` for `S372|S373|S418|002849|002850|002885|yahoo|
  nofollow|baidu` finds zero references (only generic robots.txt prose, README:42,110,370-375). No
  README row or entry cites the Yahoo pages; no pointer update is needed there. C1 adds new rows for
  `yahoo-japan-rel-nofollow-semantics.md`, `baidu-friendly-crawl-guidance.md`,
  `baidu-mobile-matching-error-causes.md` and `robots-txt-rules.md` (all four are among the 21
  unindexed at base — reproduced by running C1's logic at base), but those are new index rows, not
  pointer updates.
- **Existing entries citing S372/S373 stay valid; no text change.** `yahoo-japan-rel-nofollow-semantics.md`
  lines 26-27 cite S372/S373 as "robots-refusal ground"; `baidu-friendly-crawl-guidance.md` lines
  38-40 cite S373 for pattern syntax. Both remain true after C2; only the registry used-by cells
  extend (C4), which is C2's own change, not a pointer edit.
- **Registry rows S372/S373 used-by WILL change** (prior + one new entry each, `c55_quote_truth.py:80,262-265`)
  — this is C2's expected diff, not a stale pointer. S418 is new (base confirmed absent).
- **Historical lessons (r52/r53/r54) and QUALITY.md:1139** reference S367/S372/S373 unit counts as
  historical record; leave untouched (append-only discipline, r53 lesson).

VERDICT: C1 and C2 must land in the same committed revision with exact-basename and H1-aware C1 rows; C1 is unverifiable without C2; counter C5 still lacks a locator check (r52 gap repeated); no README/entry pointer updates are owed for S372/S373/S418.
