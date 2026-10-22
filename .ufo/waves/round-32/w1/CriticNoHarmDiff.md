# CriticNoHarmDiff — round 32 wave 1, no-harm scan of a0b0dff..285abca

Verdict (advisory): no out-of-scope change and no harmful deletion. The only
deleted lines (5) are rewrites inside `scripts/citing_set_hostile_selftest.py`
that keep the prior text or make the check stricter. Axis: operability, harmed
by none of these changes.

## Commands (all run read-only in the lane, exit 0)
1. `git diff --stat a0b0dff… 285abca…` gives 13 files, 464 insertions, 5 deletions.
2. `git diff --numstat` / `--name-status` (same range): 9 added files (A), 4 modified (M).
   Only `scripts/citing_set_hostile_selftest.py` has deletions (16 added, 5 deleted).
3. `git show --numstat` per commit: 5b32cc7 adds only the two counters and appends to SCORECARD.md (+31/-0).
   2f2f12d changes SOURCES.md +1/-0, the entry +13/-0, the selftest +16/-5, and adds P6 and other new files.
   285abca adds the two after-receipts and changes SOURCES.md +1/-1.
4. Byte-prefix check (`cmp` of base blob vs the same-length head of the tip blob):
   SCORECARD.md prefix_ok=yes (1007 to 1038 lines); render-web-services.md prefix_ok=yes
   (77 to 90 lines). Both are strictly appended at the end of the file.
5. `git diff -U1` hunks for SCORECARD.md, corpus/SOURCES.md, the entry and scripts/.
6. `git diff --word-diff=porcelain 2f2f12d 285abca -- corpus/SOURCES.md`.
7. `git grep` at tip for `reason_contains`, callers of the selftest, and stale "five hostile" counts.

## Per-file findings
- SCORECARD.md: one hunk `@@ -1007 +1007,32 @@`, which adds only the "## Round 32 — declared
  claims" section after the old last line (`all three layers shows harm. No fixture pins that guard alone.`).
  This is append-only. Pass.
- corpus/knowledge/render-web-services.md: one hunk `@@ -77 +77,14 @@`, which adds only
  "## Retained copies (round 32, append-only)" after the old last line. This is append-only. Pass.
- corpus/SOURCES.md: hunk `@@ -69,2 +69,3 @@` inserts exactly one line, S062, at line 70,
  directly after S061 (the last registry row) and before `## Paths` (line 72). The row has 13 cells,
  the same count as the S061 row. The rest of the file is unchanged. The 285abca change rewrites one cell
  in that same row. The word diff shows only the recheck cell, which changed from
  `on ds4cc-marketplace render.yaml or Dockerfile change` to `90d`. The file changes only through the S062 row. Pass.
  Note: prefix_ok=no for SOURCES.md only because the table end is not the end of the file; the
  insertion is still at the end of the table.
- scripts/: the changed files are exactly `citing_set_hostile_selftest.py` (M) and
  `fixtures/citing-set-hostile/P6-commit-before-init/hostile.json` (A, 26 lines). No other
  file under scripts/ changed. In particular, `scripts/citing_set_selftest.py` and specs P1 to P5
  are untouched. Pass.
- .ufo/waves/round-32/ (8 files): all are newly added (counters, retained source copies, receipts).
  There are no deletions and no modifications to earlier files.

## The 5 deleted lines (all in scripts/citing_set_hostile_selftest.py at the tip)
- `@@ -46,5 +52,5 @@` reflows a docstring. The old text "every hostile case is a failure, no canary exists,
  and the victim repository's HEAD, refs and commit count are unchanged." is kept word for word.
  The only addition is "(with its ``reason_contains`` text, when given)". Harmless.
- `@@ -77,3 +83,3 @@` widens `CASE_KEYS` by one key, `"reason_contains"`. `load_spec`
  (tip :142-144) validates the key only when it is present (it must be a non-empty string). Harmless.
- `@@ -208,4 +217,6 @@` changes `passed` by adding the conjunct `all(detail["reasonChecks"].values())`
  (tip :218-222). The other conjuncts are unchanged. For P1 to P5, which have no `reason_contains`,
  `wanted` is empty and `all([])` is True, so their pass and fail behaviour does not change.
  This is strictly stricter for P6 only. Harmless.

## Not a defect (noted only)
- PROVINCE.md:122 still says "five hostile fixture shapes". It describes round 31's runner change
  as history, it is not in the diff, and no claim in this round covers PROVINCE.md. If the L1 wants
  the province summary current, the smallest edit is to append a round-32 sentence; do not rewrite line 122.

## Not verified
- I ran nothing (no counter, selftest or hash-object). I did not check the byte identity of the retained
  copies or the truth of the S062 row cells. Sibling seats own those checks.
- I deliberately did not pursue whether `reasonChecks` trusts the runner's reported reason text
  (that line of attack is on hold).
- No sandbox clone was made; no files were written other than this report. No tools were installed.
