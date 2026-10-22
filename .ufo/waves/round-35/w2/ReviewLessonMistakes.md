# KakeR35.ReviewLessonMistakes — falsify corpus/lessons/round-35.md (Kake r35 wave 2, r35-falsify)

Attacked: `corpus/lessons/round-35.md` at `7deacc46` — the four Mistakes rows, the six routed-defect
dispositions, the dcef39b5 correction, and the Carried-open claims. Axes: operability, freshness.
Method: sandbox clone `/fast/scratch/hyaku/kake-r35/w2/KakeR35.ReviewLessonMistakes/clone`
(checked out at `7deacc46`; GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset); retained-bundle commits
fetched with `git fetch <bundle> 'refs/heads/*:refs/bundles/<name>/*'`. Leaf seat: no subagents; no
lane mutation except this report; no tools installed.

## Verified (commands + exit codes)

1. Hashes: 7deacc46, 81d9fd74, 16a6b8b8, 4c6be2bd, 318561ef(=318561efa672…), bd14096a, b1cbbc39,
   95abec21, fd0d53b2, a2fe31b, 9ef758c, d08d8de, bc0304de, ce72dd1b all resolve (`git rev-parse
   --verify`, exit 0). dcef39b5(=dcef39b5f4e8…), 0cce15f0, 04848219, e5263d41, ae9fb361 resolve only
   after fetching the retained bundles (rev-parse exit 1 before, exit 0 after) — consistent with the
   bundles being the pointer, per round-34.md:176-177 retrieval note.
2. Correction line citations vs `git show dcef39b5:scripts/link_preview_audit.py | nl -ba`: lines 5–8
   are exactly the walk+read block; line 10 is exactly `h = hashlib.sha256(json.dumps(argv).encode())`;
   line 12 the `h.update(rel.encode() + b"\0" + files[rel]…)` line; line 15
   `r = r or T.get(key(argv)) or [0, "clean", []]`. 4/4 quotes match at the named lines; "hash argv
   plus every relative path and file content" is what lines 9–13 do. ACCURATE.
3. Able-to-fail receipts (`.ufo/waves/round-35/verification/`): criterion-prebuild-leak-r34-c2-at-
   a2fe31b.txt "FAIL: every matched value appears…(pre-build target published)" exit=1, twin r34-c1
   receipt exit=0; criterion-control-description-r34-row4.txt exit=1, twin r35-correction exit=0
   (run against doc-rev bc0304de; lessons file byte-identical bc0304de..HEAD — empty `git diff --stat`);
   criterion-registry-row-at-318561ef.txt exit=1 naming scripts/link_preview_audit.py, twin at fd0d53b2
   exit=0. All three checks shown able to fail. VERIFIED.
4. Receipt numbers vs lesson text: c1 14/24 met false exit 1 at 16a6b8b8+bd14096a, 24/24 exit 0 at
   b1cbbc39+95abec21; c2-at-95abec21 met true, 12/12, words 1388, copiedShare 0.0, goodCites 8;
   c1-at-4c6be2bd exit=2 (reveal refused); control-v2-c1-lookup-dcef39b5 exit 1, passed 7 of 24;
   control-v2-c2-hollow-0cce15f0 met false; v1 critic 0.0376/8 probes and 0.0043/6 (met false on
   probes only, so "passing size, copied and cites under version 1" holds); v2 critic copiedShare
   0.9781 both, goodCites [] (cites 0); control-v2-c2-reworded 0.0733, 6/12. ALL MATCH.
5. Pre-build leak row: c2-at-d08d8de.json added at a2fe31b (18:01:53, `git log --diff-filter=A`,
   exit 0) before entry at 9ef758c (18:13:49); its census.derived = pages 102, og:title 87, og:type 87,
   og:image 1, og:url 87, all-four 1, og-url-equals-canonical 87 = the seven values on
   corpus/knowledge/link-preview-metadata.md:128 at ce72dd1b. Matches routed defect 4
   (round-34-verifier-spotcheck.md:229-233). VERIFIED.
6. Registry row: `git grep -n 'link-preview-audit' 318561ef -- SKILL.md` exit 1 (nothing) in my clone;
   SKILL.md:1035 section present at fd0d53b2 and HEAD; tool constants EXIT_CLEAN 0/EXIT_POLICY 1/
   EXIT_INPUT 2/EXIT_USAGE 64 (scripts/link_preview_audit.py:65-68). "PROTOCOL §Gate standard
   (Registry)" resolves at fleet root PROTOCOL.md ("## Gate standard" :375, "Registry" :398). VERIFIED.
7. Round-34 cross-references: round-34.md:68 has the exact phrase "keys on the case directory name";
   :130 is exactly the carried-open "C1 counter: case identity leaks…" bullet; SCORECARD.md:1254
   "replays the matrix by case directory name"; round-34 criteria lookup_control_check.py:6 is the
   directory-name docstring line; spotcheck defects 1–5 + carried 6 (:213-243) match disposition rows
   1–6 statement-by-statement ("five defects" is right — item 6 is carried, not a defect). QUALITY
   round-35 at corpus/QUALITY.md:693: (a) sealed targets, (b) no pre-build receipt publishes a measured
   value, (c) control described by quoting its own bytes, (d) registry rows — letters match the
   lesson's (b)/(c)/(d) citations. VERIFIED.
8. Carried open: "closes the matching element and every element nested in it" — handle_endtag
   `del self.suppressed_elements[index:]` with that exact comment (stack pop of nested suppressed
   elements). Entry unedited: `git diff --stat 95abec21 7deacc46` on the entry file is empty.
   SOURCES.md:174 S074 note (reject kept); S006 used-by extended (:14); S078–S087 rows with 8 mined /
   2 rejected (:86-95). VERIFIED.
9. "No sealed case depends on an undecided point" (:126): scanned all 24 sealed cases (revealed
   sealed/c1-cases.json: 12 G + 4 R1 + 5 R2 + 3 R3) for the eight inputs CriticC1ContractAmbiguity
   marks Undecided (items 2,3,7,8,12,14,16,19): no NBSP/whitespace-only og:url, no template>svg/math
   nesting, no self-closed template/math, no noscript-wrapped template, no missing page file (case-06's
   page "d" is a directory = item 15, marked Decided), no duplicate URLs, no path escape. Nearest
   shape, case-24 (og:urls '/a/' then https://ex.org/a/, canonical https://ex.org/a/), is
   reading-invariant: '/a/' resolves against the page URL to the canonical value, so under either
   reading of item 3 the expected findings are the same {og_url_not_absolute, og_url_multiple}.
   CLAIM HOLDS on my scan.
10. "prompt §6.9" resolves: /home/vgpnk/Projects/shokunin/.ufo/prompts/kake-round-35.md §6 numbered
    item 9 "Claim sizing", cheapest-control bullet at :354. The literal string "6.9" appears nowhere;
    it is a section-item shorthand. NOT BROKEN.

## Findings (severity-ordered)

- LOW — "19 inputs, 7 undecided by the text" (round-35.md:124): the cited report marks EIGHT items
  Undecided (2, 3, 7, 8, 12, 14, 16, 19) and its summary names six (3,4,5,7,8,16) as result-flipping;
  "7" appears nowhere in it. Derivable only via an unstated exclusion (item 12 "low weight" or item 2
  "pointed weakly"). Evidence: w1/CriticC1ContractAmbiguity.md:16-33, :36-44.
- LOW — round-35.md:85 cites the round-34 correction as `round-34.md:168-175`; the "Carried-open names
  (wave-2 ReviewCarriedOpenShapes)" bullet starts at :167 (grep -n) and ends at :175. Off by one line.
- LOW — round-35.md:27 "one `test -e` on a path under the sealed directory (existence only, exit 1)":
  the disclosed check (w1/ScribeEntryDraft.md:1) is on the sealed directory itself
  (/fast/scratch/hyaku/kake-r35/sealed), not a path under it; and "exit 1 meaning it exists" inverts
  test(1) semantics (exit 0 = exists), which the lesson repeats uncritically. No seal consequence
  (the check reads nothing either way), but the landed sentence is inaccurate twice over.
- OBSERVATION (for the L1; not a lessons defect): untracked
  `.ufo/waves/round-35/criteria/knowledge_control_check.py` (mtime 2026-10-22 20:01:50, sha256
  87e770dbc4b4270a0f00b6e3…) appeared in the lane working tree during this review; `git ls-tree HEAD`
  on that directory lists exactly the three landed checks, and no lesson text cites it. Some wave-2
  seat wrote into the lane outside its report path.

## Broken pointers

None hard-broken. Three imprecisions above (7-vs-8 count; :168-175 off-by-one; the test -e sentence).

## Not verified (unrun checks have not passed)

- No counter or criterion was rerun; receipt contents trusted as committed (reruns belong to the
  RerunC1Sealed/RerunC2Sealed/Mut* seats). "Renaming case directories leaves it at 28 of 28" and "a
  one-comment HTML change drops it to 7 of 28" taken from round-34-verifier-spotcheck.md:222-224 and
  w1/ScribeControlCorrection.md, not reproduced by me.
- S078–S087 quotes vs retained source texts and the fetch timestamps in sources/receipts.json (my
  field-name probe printed None) not re-verified — ScribeGateLines/RerunC2Sealed own those.
- Routed row 1's "lookup_control_check.py reads the round-34 counter's `total` field" not traced into
  that script's body (its :6 docstring matches the correction's citation; the direct-receipt fallback
  is verified).
- CriticC1ContractAmbiguity's html5lib probe outputs accepted as that report's own evidence; I did not
  rerun its probe.
