# ReviewGitCorpusBlob: C1 repair hunk, GitSource.corpus_files at corpus/knowledge

Seat: KakeR28a3.ReviewGitCorpusBlob (leaf reviewer; axis operability; milestone r28-build).
Advisory input for L1 and the non-author closure. Not a verdict.

Pinned to repair commit b5d423f (gate copy sha256 28ba9965...). Lane HEAD moved to 8ecbefe
during the review. Its follow-up changes only the top-level check (b5d423f lines 299, 302, 308),
so the corpus results below hold at HEAD too. Line numbers are b5d423f's; HEAD adds 4 lines above
corpus_files.

## Answer

The hunk does what C1 claims for the surfaces in scope. A blob, a symlink, or a gitlink at exactly
corpus/knowledge, and an absent surface, all exit 2 with input_invalid in Git mode and never measure
clean. The blob case was a real false green at base and is fixed. Legitimate inputs still measure
clean, so I found no over-rejection. The hunk does change Git-mode reason codes for a symlink and a
gitlink at the path (F1, low).

## Findings

F1 (LOW, introduced by this hunk). Git-mode reason codes for a symlink or gitlink at the exact path
changed. They now differ from base and from working-tree mode.
- Code: scripts/citing_set.py:357-358 runs the `path == CORPUS_DIR` check before the mode 120000
  check (359-360) and the non-blob check (361-362).
- Observed (out-b5d423f.txt, rows G3, G3b, G4, G5):
  - symlink at path: base git symlink_rejected; repair git not_a_directory. Working tree gives
    symlink_rejected at base and at repair.
  - gitlink at path: base git not_a_regular_file; repair git not_a_directory.
  - Exit 2 in every row, so C1's "not clean" holds.
- Scratch what-if (lane not edited; not run through the counter): move the exact-path check after
  the 120000 and non-blob checks (make_reorder.py). Result in out-reorder-whatif.txt: symlink gives
  symlink_rejected and gitlink gives not_a_regular_file, matching base and working tree. Blob still
  gives not_a_directory. Controls K0-K4 still clean. This is a label-only change for L1 to weigh.
  I did not make it.

F2 (LOW, out of this hunk). Cross-mode divergence for a populated submodule. Git mode refuses the
tree at HEAD (not_a_directory). Working-tree mode measures it clean, and the `.git` pointer file is
counted as a corpus document.
- Evidence: out-b5d423f.txt G5 rows; cases/G5-submodule-real/repair-wt.stdout.txt (verdict clean,
  corpusFiles 2); `ls -A` of cases/G5-submodule-real/corpus/knowledge shows `.git` and `entry.md`.
  WorkingTreeSource._walk (scripts/citing_set.py:263-285) takes `.git` as a regular file.
- Not a C1 breach: the surface is present and readable, and no uncited citation was missed. Record
  as open, or fold into C1 if L1 wants both modes to agree.

F3 (INFO). The brief's parenthetical "(submodule at the path, symlink at the path)" under
"no records -> corpus_directory_missing" does not match the code. Those two produce a record
(120000 blob, 160000 commit), so Git mode never returns corpus_directory_missing for them. The
declared SCORECARD C1 text fixes exit 2 and not-clean, not reason codes. No breach.

F4 (INFO, pre-existing, out of hunk). Label drift only; exit 2 at base and at repair.
- Working tree, corpus is a regular file: corpus_directory_unreadable (NotADirectoryError falls into
  the OSError branch, line 246), not not_a_directory (G8).
- Empty directory: Git mode corpus_directory_missing, working tree corpus_empty (G9). Git cannot
  store empty directories.

F5 (INFO, pointer only). HEAD's follow-up commit message says the b5d423f top-level check
over-refused "bare repositories and trailing-space roots". I did not verify that and did not review
that hunk. It belongs to the top-level seat.

## Commands and exit codes

Scratch root: /fast/scratch/hyaku/kake-r28a3/w1/ReviewGitCorpusBlob/. Lane access was read-only
(git show, diff, log, ls-tree, rev-parse, merge-base; counter run with --scratch into my area).

1. git -C lane diff 22c1669 b5d423f -- scripts/citing_set.py -> the hunk (exit status not captured).
2. git -C lane show <rev>:scripts/citing_set.py > citing_set_<rev>.py for b5d423f, 22c1669, 8ecbefe
   -> exit 0. sha256 28ba9965..., 3a361a00..., 6b83299d...
3. python3 -B harness.py > out-b5d423f.txt -> exit 0. Repair: PASS 29, FAIL 2, INFO 33. Both FAILs
   are my expectation error: I expected a working-tree not_a_directory for a symlink, but the
   working tree checks S_ISLNK first (scripts/citing_set.py:253), as at base.
4. python3 -B c1_interface_count.py --root <lane> --revision b5d423f... --scratch .../counter
   -> exit 0. passed 15/15 (defect 11/11, control 4/4). counter-b5d423f.json. The 29-case selftest
   is one of the 4 controls.
5. Same counter at 8ecbefe -> exit 0. 15/15. counter-8ecbefe.json.
6. python3 -B runner.py citing_set_8ecbefe.py cases-head > out-head-8ecbefe.txt -> exit 0.
   PASS 29, FAIL 2 (same two expectation errors), INFO 1.
7. git merge-base --is-ancestor b5d423f HEAD -> ancestor. git diff -U0 b5d423f 8ecbefe --
   scripts/citing_set.py -> hunks at 299, 302, 308 only. Exit 0.
8. python3 -B make_reorder.py -> exit 0. runner.py citing_set_reorder.py cases-reorder ->
   exit 0 (out-reorder-whatif.txt: PASS 25, FAIL 6). The 4 Git-mode FAILs are the intended reason
   changes; the 2 working-tree FAILs are my expectation error.
9. Grep of scripts/: the reason strings appear only in citing_set.py. Grep of GitSource( and
   .corpus_files(: one caller, evaluate (b5d423f line 465); GitSource built in main (lines 697-698).

## Cases (16 cases, 2 gates, 2 modes; full table in out-b5d423f.txt)

- K0-K4 (valid entry; nested `knowledge` names; sibling corpus/knowledge.md present; names with tab,
  space, Unicode, newline): clean in both modes at repair. No over-rejection seen.
- G1, G6, G7 (absent; corpus/knowledge.md only; corpus/knowledgebase only): corpus_directory_missing
  in both modes at repair. No prefix leak through the ls-tree pathspec. Base said clean in both modes.
- G2 (blob at path): repair not_a_directory in both modes. Base Git mode said clean (the false green).
- G3, G3b (symlink, dangling symlink): see F1.
- G4, G5 (fake and real gitlink): see F1 and F2.
- G8, G9, G10 (corpus is a file; empty directory; unreadable directory): see F4. G10 Git mode is
  clean, as expected, because Git reads committed blobs.

## Tools

No install or update performed. git 2.56.0 and Python 3.14.8 as already installed.
xd://lsp is not mounted ("No such tool: xd://lsp. Mounted devices: ast_edit, debug"). Caller and
definition checks are literal grep fallback, not semantic proof.

## Not verified

- LSP references and diagnostics (no server available).
- The reorder through the counter (the counter needs a commit). I ran only my 16-case harness on it.
- Corpus itself as a symlink in Git mode (expected corpus_directory_missing, since ls-tree does not
  descend symlinks). Not run.
- Object database corruption; gitlink nested inside corpus/knowledge in working-tree mode;
  case-insensitive filesystems.
- The top-level check hunk (b5d423f and 8ecbefe): reviewed only as far as the diff header.
