# KakeR36.ReviewCorrections — wave-2 falsify: the two appended round-35 corrections

Seat: leaf reviewer (freshness), 2026-10-22. Read-only in the lane except this report.
No subagents, no network fetches, no tool installs (operator tooling directive 2026-10-19:
none needed, none performed). All git read-only; GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset.

## Attacked
1. `corpus/lessons/round-35.md` end: "## Round-36 correction of the S084 Gate line (appended)".
2. `corpus/knowledge/security-txt-publishing.md` end: "Round-36 correction … routed defect 5"
   (Preferred-Languages citation narrowed to S078 alone).
Attack questions: (a) is each faithful to the retained texts (`.ufo/waves/round-35/sources/
S084.txt`, `S078.txt`) and to round-35 closure routed defect 5; (b) was any original line
rewritten (additions-only required)?

## Commands and results (exit codes in parentheses)
1. `git diff b720d799ae99c19a7c97f2b1391d4fe928be0e11 f3a38bf8e68f6cee386125d34b5e95ac9b2df66e -- corpus/lessons/round-35.md corpus/knowledge/security-txt-publishing.md` (0)
   → `2 files changed, 14 insertions(+), 0 deletions(-)`; exactly two hunks, both at EOF:
   security-txt-publishing.md `@@ -148,3 +148,9 @@` (+6), round-35.md `@@ -235,3 +235,11 @@` (+8).
2. Same diff piped to `grep -c '^-[^-]'` → `0` (grep exit 1 = zero removed lines); `grep -c '^-'`
   → `2` (only the two `--- a/…` diff headers). Additions-only confirmed.
3. `grep -n '^- S084 —' corpus/lessons/round-35.md` → line 50, ending
   `…(whole served body, field lines; 8 words)`. The correction's `:50` pointer and its
   quotation of the mislabel are exact.
4. `cat .ufo/waves/round-35/sources/S084.txt` → one line, 7 fields: Contact, Acknowledgments,
   Preferred-Languages, Canonical, Policy, Hiring, Expires. The row-50 quote is an exact
   substring holding exactly 4 (Acknowledgments, Preferred-Languages, Canonical, Policy); the
   3 missing fields are exactly the Contact, Hiring, Expires the correction names.
5. `grep -c -o "If this field is absent, security researchers may assume that English is the language to be used" .ufo/waves/round-35/sources/S078.txt` → `1`; it sits under the body
   header `2.5.8. Preferred-Languages` (header occurs twice: TOC and §2.5.8 body).
6. `grep -o -i english .ufo/waves/round-35/sources/S079.txt | wc -l` → `0`: S079 lacks the
   clause, so "Only S078 carries it" holds.
7. `git diff --stat b720d799… f3a38bf8… -- .ufo/waves/round-35/sources/S084.txt .ufo/waves/round-35/sources/S078.txt .ufo/waves/round-35/sources/S079.txt` → empty (0);
   `git status --porcelain -- .ufo/waves/round-35/sources/` → empty (0). The retained artifacts
   checked are the frozen ones the round-35 closure saw, with no worktree drift.
8. Routed defect 5 read at `corpus/lessons/round-35-verifier-spotcheck.md:199-200`:
   "S084's 'whole served body' (the quote is 4 of 7 lines). The entry's 'absent → English'
   clause cites S079, but S079 lacks it (S078 §2.5.8 carries it)." Both appended corrections
   map 1:1 onto its two clauses; the S084 nit also appears in the spotcheck gate row at :154.
   Closure entry: `/home/vgpnk/Projects/shokunin/MANIFEST.json:14979-14985` (spotcheck pointer
   @b720d799 — the same base revision used here).
9. Attribution: `.ufo/waves/round-36/w1/ScribeCorrectionsR35.md` exists and drafts exactly
   these two corrections with the same pointers (round-35.md:50, S084.txt:1, S078 §2.5.8).

## Verdicts
- Correction A (`corpus/lessons/round-35.md:239-245`): CLEAN. Faithful to `S084.txt:1`
  (4 of 7 fields; missing exactly Contact/Hiring/Expires) and to defect 5 clause 1; the `:50`
  pointer is exact; "the admit, tier and status stand" is true of line 50 (admit, tier A,
  mined, all unchanged); the original line is not rewritten.
- Correction B (`corpus/knowledge/security-txt-publishing.md:151-156`): CLEAN. The bullet it
  quotes says verbatim "if absent, English may be assumed (S078, S079)"; the clause appears
  exactly once in S078 under §2.5.8 (count 1) and never in S079 (count 0). Narrowing only the
  final clause is the right scope: S079 does carry the rest of the bullet (Preferred-Languages
  "Optional", "Only 1 allowed", comma-separated list — S079.txt field table), so leaving the
  joint citation on the earlier clauses is correct, not an under-correction. Original bullet
  unchanged.

## Findings
No defect at any severity in either correction. One advisory wording note, no action required:
the retained `S084.txt` stores the seven fields space-separated on a single physical line;
"field lines" is the Gate row's and the spotcheck's own term for the seven fields, so the
correction's counting language stays consistent with both artifacts.

## Residual risk / not verified
- No live refetch of github.com or rfc-editor.org (bounds; also unnecessary: both corrections
  cite the retained artifacts, which I verified byte-identical base→head and clean in the
  worktree). Whether the live GitHub body still matches `S084.txt` is outside this item;
  `Expires` churn there is already documented in the knowledge file's wave-2 correction.
- I verified the landed bytes directly against the base→head diff and the retained texts; I
  did not re-derive the sha256 values recorded in `w1/ScribeCorrectionsR35.md`.
