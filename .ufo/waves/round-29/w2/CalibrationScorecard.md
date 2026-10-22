# CalibrationScorecard — round 29 self-assessment versus repo state at 7697990

Item attacked: what SCORECARD.md "Round 29 — declared claims" and its declaration notes, corpus/lessons/round-29.md, the corpus/README.md and PROVINCE.md changes (plus the round-29 SKILL.md, SOURCES.md and QUALITY.md additions) assert, compared with the committed bytes at 7697990cbca20291f3b0367b8ff4220e93b38b03.
Sandbox: /fast/scratch/hyaku/kake-r29/w2/CalibrationScorecard/ (clone at 7697990, TMPDIR inside). Python 3.14.8. No network, no installs.

## Result: 6 mismatches (none changes a C1 or C2 number), plus 2 gaps that no round document asserts

1. SCORECARD.md:640-641 (declaration notes): "C2 enters a SCORECARD Capabilities row in this round". At 7697990, SCORECARD.md §Capabilities (lines 187-193) has no base-path row, and `grep base_path SCORECARD.md` matches only the claim table. This is pending, not false: rounds 22 and 25 added their rows in a later "record" commit (adc04da, 97404de).
2. QUALITY.md:337 cites "`PROTOCOL.md:398-402` (§Gate standard, Self-test)". In fleet PROTOCOL.md (unchanged since 7c5b34f, 2026-10-19), lines 398-402 are the **Registry** bullet; Self-test is at line 385. The path also does not resolve from the lane: the lane has no PROTOCOL.md.
3. QUALITY.md:373-374 says "round 29 did not work it (see the round-29 note below)". No such note exists: the section ends at line 394 on the "new gate ships its fixtures" bullet, and `grep -n 'round-29 note'` matches only line 374.
4. PROVINCE.md:81-82 still says "The remaining field-performance, Jekyll and Render frontier is unchanged" (blame 9f62cda, round 25). That contradicts PROVINCE.md:26-28 in the same file, where Jekyll/base-path now has a first entry plus a gate. README.md:269-271 calls the statement "historical", but PROVINCE itself was left unannotated.
5. SKILL.md:716 gives `bundle exec jekyll serve --baseurl = ""` (S041) as a code span, so it reads as a command to run. The retained S041 HTML (.ufo/waves/round-29/sources/S041.html.gz) has `--baseurl</span><span class="o">=</span>...""`, which is `--baseurl=""`. The spaces come from tag removal. Copying the SKILL command passes `=` as the baseurl and `""` as a stray argument. The lesson flags this artifact for S040 (lesson:41-42) but not for S041. knowledge/pages-base-path.md:35 repeats it, inside quote marks. README.md:253 has `jekyll serve --baseurl ""`, which is correct.
6. .ufo/waves/round-29/sources/screened/receipts.json records C2 (Stack Overflow) as `"opened": true, "status": 403`. The lesson (round-29.md:56, "Not opened (C2)") and the SOURCES.md:102 search log ("opened 9") call it unopened. The prose matches the seat report (w1/ScreenRejectCandidates.md:33); the receipt field contradicts both.

Gaps that no round document asserts:
- SKILL.md has no gate-registry row for base-path-audit, its self-test or the C1/C2 counters. Prior gates do have rows: canonical-audit (SKILL.md:411), receipt-replay (537), accessibility-packet (555) and citing-set (616-618). PROTOCOL.md:398-402 makes SKILL.md the child lane's registry home. SKILL.md:707 and PROVINCE.md:27 both call the tool a "gate".
- reject_path_check.py prints `"rejectedRowsInRegistry": 5` on the landed rows, but the registry has 3 rejected rows (S044-S046); S047 and S048 are queued. The field name is wrong; the lesson's "5/5" means 5 screened candidates passed, which holds.

## Commands (exit codes)
- `c1_quote_truth.py --root . --revision R`: fe1805cf gives 0/4, exit 1. f8675e5, 98dbab2 and 7697990 each give 4/4, exit 0.
- `c2_matrix_count.py --root . --revision R`: fe1805cf gives 0/30, exit 1. 98dbab2 and 7697990 give 30/30, exit 0. Kinds 7/14/8/1. Constant gates pass 7/30, 0/30 and 7/30; all are rejected. Matrix sha256 75c08f64… matches the pinned value. Tool sha256 is e3264615….
- `scripts/base_path_selftest.py`: exit 0, "30/30 fixtures passed". Fixture directories by prefix: 14 D, 8 I, 7 K, 1 U.
- `base_path_audit.py` on the 3 real-input manifests: exits 1, 0 and 1. Each result object is identical to `result` in out/*.json. All 4 findings are `<a href>` links to sibling projects. Each page.html is byte-identical (sha256) to .ufo/waves/round-23/live/<site>/page.html.
- `reject_path_check.py` on the tip registry, lesson and entry: exit 0, passed 5. The same check on the committed f8675e5 copies: exit 0. Mutations M1-M5: exit 1 each, including `--registry mut/M2-no-flip.md`.
- `sources-census.sh validate` on a `git archive 7697990` extract (with a copied script): exit 0, with the single W04 (S033) warning also present at base.
- Stored verification JSON (c1-before, c1-after-f8675e5, c1-after-98dbab2, c2-before, c2-after-98dbab2) is field-identical to my runs.

## Assertions that hold
- Counter blobs at d18bbf3 equal the tip blobs: 139ede1e…, 58dde062… and 0687433e…. 9e541a1d… is a commit object in the lane.
- Receipts for S040-S043 and C1-C6: text sha256, body sha256, byte counts and word counts all match. S040's finalUrl is what-is-github-pages. All four primary sources were fetched at 10:29:37Z with HTTP 200. ReviewSourcesReopen reports 10:33:42Z and 4/4 identical.
- All 9 Gate and screened quotes are exact substrings of their retained text, between 10 and 21 words each. The S044=C1, S045=C3, S046=C5, S047=C4 and S048=C6 mapping holds.
- SOURCES.md has only additions: 9 rows, 1 Paths line and 1 search-log paragraph. "Identified 10" adds up (4 primary plus 6 candidates). S048 is tier A in both the row and the lesson. S016 lists Jekyll 3.10.0. S024 says the first base href wins.
- There are 29 citing-set fixtures, and `grep -rl reason scripts/fixtures/citing-set` finds 0 files. The 8 round-28 reason codes appear only in scripts/citing_set.py.
- Line references that check out: c2_source_count.py:126-131, c1_interface_count.py:141 and 150-151, round-28-verifier-spotcheck.md:70-74, 223-227 and 228-231, QUALITY.md:298-332 and 317, and goal file line 173 (the drift sentinel row).
- The SKILL interface claims (exit 2 reasons, exit 64, manifest rules, `interface` field) match c2-matrix.json.

## Not verified
- Sandbox commits 609e6777… and 1f9ffdc… are not in the lane object store, so I did not reproduce the one-letter flips.
- I did not check whether the entry's claims follow from its quotes. The declaration notes leave that to the closure.
- I did not reopen any live page (no network allowed).

## Verdict: limit to state
Every numeric, hash, counter and receipt-digest assertion holds at 7697990. The six mismatches are in prose, pointers and receipt fields. Items 5 and 1 affect operability; items 2, 3, 4 and 6 affect freshness and provenance accuracy. Smallest safe correction:
- Change SKILL.md:716 to `--baseurl=""` and add an S041 spacing note next to lesson:41-42.
- Fix the QUALITY.md:337 citation to fleet `PROTOCOL.md:385-389`, and remove or write the note that QUALITY.md:374 points to.
- Annotate PROVINCE.md:81 as superseded for Jekyll/base-path.
- Correct the C2 `opened` field, or define it as "requested".
- Add the Capabilities row and a SKILL registry row at closure.
