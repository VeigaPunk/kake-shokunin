# ToolSourceGaming: is the C2 30/30 earned?

Seat: KakeR29.ToolSourceGaming (leaf attack, no subagents). Axis: operability. Milestone: r29-falsify.
Target: scripts/base_path_audit.py at 7697990cbca20291f3b0367b8ff4220e93b38b03.
Sandbox: /fast/scratch/hyaku/kake-r29/w2/ToolSourceGaming/ (clone/, mutant/, mutant-repo/, probe/, probe2/).

## Verdict
- Gaming: NO GAMING FOUND. No embedded case ids, fixture names, content hashes or matrix-specific branches.
- 30/30: HOLDS for the 30 frozen cases (exit, verdict, reason, element, attribute, value). LIMIT TO STATE: it does not test id, page, resolved, pagesChecked, referencesChecked, browser parity or reference coverage (findings 1-3).
- Docstring claim of browser-style resolution (tool lines 35-39): BROKEN on the URL classes in finding 1.

## What I read
- All 756 lines. Blob e5167fa13dab6af9b7b4f99b9ee2099a8efe302d at both 98dbab2 and 7697990; `git diff 98dbab2 7697990 -- scripts` is empty. 98dbab2 is the only commit touching the tool.
- Literal branches are HTML and URL grammar only (tool 331-334, 362, 398, 519-535, 542-547). Stdlib imports only. No hashlib, environment reads, .ufo paths or fixture strings. The only non-ASCII character is the ellipsis at line 130.
- Matrix c2-matrix.json: sha256 75c08f64...2e84a, equal to the pin at c2_matrix_count.py:28. 30 cases: defect 14, input 8, control 7, usage 1. Script-checked: the id set equals the 30 fixture directories with no duplicates, and expected findings use only reason, element, attribute and value.

## Commands and exit codes
1. git clone; checkout 7697990 -> 0
2. git cat-file -e fe1805cf:scripts/base_path_audit.py -> 128 (file absent; commit exists)
3. python3 -B scripts/base_path_selftest.py (clone) -> 0, "30/30 fixtures passed"
4. python3 -B .ufo/waves/round-29/c2_matrix_count.py --root . --revision 7697990 -> 0, "C2 30/30"; toolSha256 e3264615...65aa; constant gates 7/30, 0/30, 7/30, all rejected
5. Same counter at fe1805c -> 1, toolPresent false, 0/30 (baseline is a missing file)
6. Selftest with --tool on mutant A (bytes identical to commit 9bc3bd0: id "x", page and resolved null, pagesChecked and referencesChecked 0) -> 0, 30/30
7. Counter on mutant A -> 0, 30/30
8. Counter on mutant B (commit e54cea2, REASON_OUTSIDE renamed) -> 1, 16/30, defect 0/14
9. Probes: Python 3.14.8 for the tool; Node 24.21.0 as WHATWG reference (see findings)

## Findings
1. MEDIUM. Browser-parity false negatives. Page https://o.github.io/repo/, base /repo/. WHATWG (Node) result, then tool verdict:
   - https:///o.github.io/other/ -> https://o.github.io/other/ (flag); tool clean
   - https:/o.github.io/other/ -> https://o.github.io/o.github.io/other/ (flag); tool clean
   - http:o.github.io/other/ -> http://o.github.io/other/ (flag); tool clean
   - https://%6f.github.io/other/ -> https://o.github.io/other/ (flag); tool clean
   - https://<fullwidth o>.github.io/other/ -> https://o.github.io/other/ (flag); tool clean
   - <base href="https:///o.github.io/x/"> then href="y" -> https://o.github.io/x/y (flag); tool clean
   Causes: _parse_absolute returns None on empty netloc (355-366, 412); percent-encoded and IDNA hosts compared raw (364, 345-352); an unparseable base href is ignored silently (569-573).
   Agreements: https:o.github.io/other/ (inside); port 443; upper-case scheme and host; http://o.github.io/other/ (flagged).
2. MEDIUM. 30/30 is blind to five output fields. selftest FINDING_KEYS (52) and counter project/judge (62-64, 75-97) never read id, page, resolved, pagesChecked or referencesChecked. Mutant A passes both gates, although the matrix interface documents all five as output.
3. MEDIUM (coverage). Reference set (tool 76-92) omits attributes browsers fetch or navigate. Probes formaction, object data, svg use href and input type=image src all returned refs=0 and clean. frame src and link imagesrcset are code-reading only. None is listed under "does NOT check" (tool 20-33). A root-relative <object data="/x.pdf"> is invisible.
4. LOW. Input finding ids equal the reason (597-599). Two unreadable pages give two findings both with id "input_invalid" (probe dup_missing_pages); two outside pages give two "page_outside_base_path" (probe dup_outside_pages).
5. LOW. Count semantics are undefined in the docstring. Observed: pagesChecked increments per evaluated page (712); referencesChecked adds every extracted candidate (594, 713), so ignored external values count (probe ids_and_counts: refs=2 with one ignored). DETAILS 136-141 calls these "checked references" yet says some are ignored. Both counts are zero on any input failure (659-660, 690-691, 707-708).
6. LOW. Usage path prints verdict "could-not-evaluate" with exit 64 (USAGE_RESULT 94-99; no-args probe). Case U1 returns ok on exit 64 before reading stdout (counter 81-82; selftest 211-212), so this JSON is unpinned.
7. INFO. Finding id is {file}#{n}:{element}[{attribute}]={value} (586). n is the 1-based index over all extracted candidates, ignored ones included, so ids shift when an ignored link is inserted above. Probe: second anchor is #2. srcset candidates index separately (srcset_two: #2, #3). The format is not documented; the only comment (75) says the index is kept stable.
8. INFO. The matrix interface "ignored:" entry judges other origins by "(scheme, host, port)". Code (345-352) and the module docstring (37) treat http and https on one host as the same site, and the tool does flag http://o.github.io/other/. The contract text is wrong. The wave-1 CriticMatrixOracle cross-scheme miss does not reproduce at 7697990.

## Held (checked, no defect)
- Name invariance: renaming index.html leaves JSON identical in 25 of 30 fixtures after id normalization (skipped: I1 manifest not JSON, I4 page missing, I6 and I8 no index.html page, U1 no manifest). Comment invariance: identical in the same 25.
- resolved equals WHATWG href (fragment dropped) for 18 of 18 defect findings.
- Base element not counted (base_not_counted refs=1); template contents skipped (refs=0); default port and upper-case host normalized.

## Not verified
- I did not re-derive all 30 expected outcomes; I read them and relied on the wave-1 critic oracle (its 21/21 claim is seat-reported).
- WHATWG reference is Node 24.21.0 only. Chromium, Gecko and WebKit not run.
- srcset malformed-descriptor drop, frame src and link imagesrcset: code reading only.
- Seat-reported, not re-run: MutantsCounterC2 (20 of 24 killed); ReviewCounterC2Code F2 (latent union-of-keys projection).
- No network use; no live probes of owned properties.

## Installs, updates and lane access
None. Used host node v24.21.0 and python 3.14.8 as found. Lane git: read-only `git show`, `git clone` (source only) and one `git status --short`; the status may refresh the lane index stat cache but changed no tracked content.
