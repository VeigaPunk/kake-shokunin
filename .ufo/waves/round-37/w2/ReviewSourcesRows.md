# ReviewSourcesRows — registry conformance of round-37 SOURCES changes (r37-falsify, freshness)

Attacked: `git diff 621fb528 79d3c780 -- corpus/SOURCES.md` (S011 used-by change; new S095, S096, S097)
against CORPUS.md contract v1 (`/home/vgpnk/Projects/shokunin/CORPUS.md:64-148`) and the lesson Gate
(`corpus/lessons/round-37.md:30-69`). Sandbox clone `/fast/scratch/hyaku/kake-r37w2/ReviewSourcesRows/clone`
at 79d3c780f9afb9bc013e3b13e73ee73e6a8ac13c. Lane worktree SOURCES.md == 79d3c780 (`git diff --quiet` exit 0).
No tools installed or updated.

## Commands and outputs
- `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → exit 0; output (3× W04 for S033,
  S088, S092, then `kake ok …/SOURCES.md`) is byte-for-byte the same as `.ufo/waves/round-37/census-before.txt`
  (committed 202d625a, before the rows landed in 528a6d0). The new rows add no findings.
- Frozen contract census (CORPUS.md:135-147) in the clone: 621fb528 had 94 rows, 0 malformed, A=77 B=2 C=15,
  mined=69 queued=8 rejected=17. 79d3c780 has 97 rows, 0 malformed, A=79 B=2 C=16, mined=71 queued=8
  rejected=18. Duplicate-id, enum/tier-inflation and missing-used-by checks are all empty. Deltas: +2 A, +1 C,
  +2 mined, +1 rejected, which matches S095/S096 (A, mined) and S097 (C, rejected).
- Cell split: S011, S095, S096 and S097 each have NF=13 (11 cells).
- Retained-text sha256 values (`sha256sum .ufo/waves/round-37/sources/*.txt`) equal the hashes in the anchors:
  S095 a9094853…dbbc6, S096 d17aa81d…15574, S097 a42aee4e…bbe3801. `receipts.json` finalUrl/status match the rows.
- Gate quotes: `grep -cF` against the retained text gives 1 for each of S011, S095, S096 and S097. Word counts are
  6, 11, 5 and 11 (limit 25).
- Validator mutation test (`mkmut.py`, 12 row mutants, `sources-census.sh validate <mutant-dir>`).
  Caught (exit 1): m01 used-by path missing (E11), m04 community at tier A (E10), m05 dropped column (E01).
  Warning only (exit 0): m12 mined with used-by `—` (W03).
  Not detected (exit 0, `ok`): m02 used-by is a script (out of class), m03 used-by file does not cite the row,
  m06 `opened` edited in place, m07 `scope` edited in place, m08 rejected `teaches` without `flip:`,
  m09 tier A→B, m10 bare-homepage anchor, m11 rejected row with used-by.

## Verdicts per statement
1. Column shape: holds. All four rows have 11 cells, no `|` inside a cell, and the ids are the next unused (max was S094).
2. Tiers: hold. S095 is docs/A, scoped to Google crawlers. S096 is code/A. S097 is community/C and rejected.
   There is no community-at-A.
3. Scope wording, S095/S096/S097: holds. Each scope is bounded ("not protocol-wide requirements"; "not all crawler
   policy outside parsing and matching"; "not current crawler semantics"). S097 `teaches` has the
   `REJECTED: …; flip: …` form.
4. Scope and anchor, S011: **wrong (medium)**. The row's scope is "Host-root scope of robots.txt rules", anchored at
   §2.3 and §2.3.1.4 (`corpus/SOURCES.md:19`). The only in-place change was used-by, which added
   `corpus/knowledge/robots-txt-rules.md`. That entry cites S011 for §1, §§2.2.1–2.2.4, 2.3.1.1–2.3.1.5, 2.4,
   2.5 and §3: group matching, rule precedence, normalization and parse limits
   (`robots-txt-rules.md:1,9,29,33,39,49,51,57,61,77,79`). Tier A is scoped to `scope` (CORPUS.md:93).
   The Gate still asserts "RFC 9309 grounds every rule of (a)–(e)" (`round-37.md:41`). Wave-1 flagged this
   exact gap: "the gap is scope, not staleness. Widen the row's scope/anchor before the Gate treats S011 as
   backing (a)–(e)" (`git show a5ae028:.ufo/waves/round-37/w1/ScoutReopenS011.md`, line 42). It was not acted on.
   Rule 2 forbids widening scope in place, so the conforming fix is a new RFC 9309 row with a §2.2/§2.5 scope.
   That row would raise W04 only.
5. Anchor, S096: **overstated (medium)**. The anchor lists README sections and a fetch timestamp plus hash, but no
   version, commit or publication date, which CORPUS.md:99-100 requires. Rows S009 and S008 pin commits. The entry
   also cites S096 for content outside the anchor: `robots.cc`/`robots.h` behavior (`robots-txt-rules.md:63`)
   and README "Quickstart" (`:1`, `:73`). The retained `S096.txt` is the GitHub landing page: it has 0 matches
   for robots.cc code identifiers, and no robots.cc/.h bytes are retained under `.ufo/waves/round-37` (glob: 0).
   The only revision pin, master `22b355ff855419e6a3ff8ff09c0ad7fdb17116f9`, exists only in
   `w1/ScoutReopenS096.md:12-13`. The code-level claims are not reproducible at the row's anchor.
6. Used-by paths: hold for the four rows. All paths are `corpus/knowledge/*.md` and each file cites its row:
   S011 is cited 3× in crawl-scope-per-host and 28× in robots-txt-rules, S095 8×, S096 5×. S097 used-by is `—`
   and only the round-37 lesson cites S097. Gate lessons are omitted from used-by, which matches lane practice:
   the round-20 and round-26 lessons cite S011 but are not listed either.
7. Old→new log: holds. `round-37.md:64-69` logs S011's used-by change exactly as the diff shows, states that
   status/opened/recheck are unchanged, and logs S095–S097 as new rows plus S095's 301 move. Rule 1 (URL, access
   date, quote ≤25 words with location for every new row) also holds (`round-37.md:40-58`).
8. Gate evidence pointers at the measured tip: **irreproducible at 79d3c780 (low)**. `round-37.md:36` cites
   `w1/ScoutReopenS011.md`, `S095`, `S096`, `S097`. At 79d3c780,
   `git ls-tree -r --name-only 79d3c780 .ufo/waves/round-37/w1 | wc -l` returns 0. The files land only in
   `a5ae028` (00:42:36, 12 s after the tip). Commit a5ae028 fixes this.
9. "Census ok" as conformance evidence: **overstated (low)** if read as proof. Output and exit code match the
   before-census exactly, but the validator caught only 3 of 12 row mutants. Out-of-class or non-citing used-by,
   in-place edits to append-only cells, a missing `flip:` and a bare anchor all pass `ok`. Statements 1–7 above
   rest on the manual checks, not on the census.

## Residual risk and verification gaps
- Pre-existing, not part of this diff: S088–S092 used-by name `scripts/source_recheck.py`, which is outside the
  knowledge-entry/lesson class. Round-37 notes this (`round-37.md:149-150`); the census accepts it because the
  file exists. S056 (queued) has used-by `-` (ASCII hyphen) rather than `—`.
- I did not re-fetch any live URL (no URL is named in this item). Hashes and quotes were checked against the
  retained text only.
- Sandbox artifacts: `/fast/scratch/hyaku/kake-r37w2/ReviewSourcesRows/{clone,mut/,mkmut.py}`. No processes are left running.
