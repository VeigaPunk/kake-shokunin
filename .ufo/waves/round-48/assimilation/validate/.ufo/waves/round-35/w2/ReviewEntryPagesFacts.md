# ReviewEntryPagesFacts — C2 GitHub Pages build statements (wave 2, falsify)

This item attacks the C2 entry's GitHub Pages /s (corpus/knowledge/security-txt-publishing.md)
that cite S006, S080, S086, S001, S002, against the retained texts and the wave-1 reports
(RevengerJekyllInclude.md, ScoutPagesDotfilesSource.md). No repo mutation, no network fetch
(no named URL opened by this seat), no sandbox clone needed: all reads were in-repo read-only.
Tool installs: none.

## Method (read-only; exit codes)
- read/grep over corpus/knowledge/security-txt-publishing.md (sentences at lines 77-95, 123-124)
- read/grep/eval over .ufo/waves/round-35/sources/S006.txt, S080.txt, S086.txt (retained texts; sha256 per front matter)
- read/grep/eval over .ufo/waves/round-27/fetched/text/S001-1.txt (v4.0.0 action.yml),
  S001-2.txt (main action.yml), S002-1.txt (v4.0.0 release), S002-2.txt (v5.0.0 release)
- grep over corpus/SOURCES.md rows S001/S002/S006/S080/S086; ghp-served-set.md line 93 (v3 adjudication)

## Sentence list with verdicts
1. "Branch build: paths starting with `_`, `.` or `#` are skipped by default, and `include`
   is the documented way to process them (S006)." — PASS. S006.txt: "By default, Jekyll doesn't
   build files or folders that ... Start with _ , . , or # ... If you want Jekyll to process any of
   these files, you can use the include setting". Partial category list (omits `~`, node_modules/vendor)
   is selective, not wrong.
2. "Jekyll's options page says dotfiles are excluded by default and that Jekyll 4 `include` entries
   override `exclude` entries (S080)." — PASS. S080.txt: ".htaccess is a good example since dotfiles
   are excluded by default"; "With Jekyll 4, the include configuration option entries override the
   exclude option entries."
3. "[INFERENCE] A branch-published site therefore needs `include: [".well-known"]` or an equivalent
   glob; the retained texts give the mechanism, not that value." — PASS (correctly labelled; value
   appears in no retained text; consistent with Revenger Q3).
4. "Branch publishing can skip Jekyll altogether: an empty `.nojekyll` file at the root of the
   publishing source disables the Jekyll build (S086)" — PASS. S086.txt: "disable the Jekyll build
   process by creating an empty file called .nojekyll in the root of your publishing source".
   BUT the tail clause "which is the lever when `include` cannot express the path" is unlabelled
   lane reasoning in an S086-cited sentence — see F1.
5. "Artifact build: packaging decides dotfiles. v4.0.0 ... drops hidden paths by default; v5.0.0
   adds an `include-hidden-files` input (S002)." — PASS with nitpick (F3). S002-1.txt: "Potentially
   breaking change: hidden files (specifically dotfiles) will not be included in the artifact";
   S002-2.txt v5.0.0 Changelog: "feat: add include-hidden-files input @jonchurch (#137)".
6. "Even with that input on, `.git` and `.github` are excluded unconditionally (S001), so another
   dot-directory is includable [INFERENCE]; a pipeline that never sets the input ships no
   `/.well-known/` (S001, S002)." — First half PASS (S001-2.txt input text: "Excludes .git and
   .github regardless"; default "false"; labelled inference sound). Second half over-broad without a
   version qualifier — see F2.
7. "For an Actions publishing source the artifact must carry the entry file at its top level (S086);
   dot-directory survival there is decided at packaging (S001, S002), while the branch path is decided
   by `include` (S006, S080) [INFERENCE: one switch does not cover the other]." — PASS. S086.txt:
   "the artifact that you deploy must include the entry file at the top level of the artifact";
   packaging/branch attributions match S001/S002/S006/S080; final switch clause labelled.
8. Decision 5: "`include` for a branch build, `include-hidden-files` for a v5 artifact build (S006,
   S080, S001, S002)." — PASS (same grounding as above; "v5" matches S002-2.txt).

## Findings by severity
- F1 (low-moderate, mislabelled inference): entry lines 84-85, "which is the lever when `include`
  cannot express the path", is lane reasoning presented inside an S086-cited sentence without an
  [INFERENCE] label, violating the entry's own ground rule ("lane reasoning is marked [INFERENCE]").
  It also edges toward the documentation gap Scout recorded (docs state the `.nojekyll` mechanism but
  nowhere state dot-paths become served once Jekyll is bypassed); the sentence stops short of claiming
  dotdirs are served, so no factual overreach. Fix: mark it [INFERENCE].
- F2 (low, over-broad statement): "a pipeline that never sets the input ships no `/.well-known/`"
  is false for upload-pages-artifact v3.0.1, which has no such input and does not drop dot patterns
  (ghp-served-set.md line 93: read the v3.0.1 half as an S002 claim; SOURCES.md line 137: "No
  inclusion input is attributed to v4"). As written the sentence covers v3 pipelines. Fix: qualify
  "on v4.0.0+".
- F3 (nitpick): "v4.0.0 ... drops hidden paths by default" — v4.0.0 has no input; the drop is
  unconditional (S001-1.txt archive steps hard-code `--exclude=".[^/]*"`). "By default" is v5
  semantics; minor imprecision.

## Consistency vs wave-1 reports
No contradiction with RevengerJekyllInclude.md (include mechanism, Q1/Q3 confirmed by S006/S080
bytes) or ScoutPagesDotfilesSource.md. The entry avoids Scout's S001 citation defect: the
`include-hidden-files` input is attributed to S002 (retained release pages), and S001 is used only
for the unconditional `.git`/`.github` exclusion — correct per S001-2.txt.

## Not verified
- No live fetch of any cited URL (network restricted for this seat); S001/S002 byte quotes come from
  round-27 retained text extracts (sha256 receipts in round-27 fetched manifest).
- v3.0.1 action.yml bytes are not retained anywhere (round-26 UNVERIFIABLE); F2 rests on the corpus's
  own adjudication, not on fresh bytes.
- No independent check of the front-matter sha256 receipt hashes (S006/S080/S086) beyond reading the
  retained text files themselves.
