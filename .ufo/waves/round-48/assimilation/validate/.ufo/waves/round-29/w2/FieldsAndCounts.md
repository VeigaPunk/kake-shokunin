# W2 FieldsAndCounts: C2 base_path_audit.py, fields the counter does not compare

Axes: operability and freshness. Commit 7697990cbca20291f3b0367b8ff4220e93b38b03; tool blob
sha256 e32646159b652710be4053bbdb001c3d11929ef63b055b7f57545231ac6965aa (git show = checkout).
Sandbox: /fast/scratch/hyaku/kake-r29/w2/FieldsAndCounts/clone. Python 3.14.8. No installs.

## The gap
c2_matrix_count.py projects only the keys named by expected findings (line 64); judge()
compares only those (lines 75-97). The expected findings name only reason, element,
attribute and value. id, page, resolved, pagesChecked and referencesChecked are never
compared. Counter rerun in the sandbox (rc=0): C2 30/30, constantGatesAllRejected true,
toolSha256 matches.

## Commands (all rc=0 unless stated)
1. fieldcheck.py: 30 matrix cases and 3 real sites, each run twice. All 33 byte-identical
   (stdout, rc, stderr). U1 exits 64 as expected.
2. Heredoc 5-run loop: D3, D10, D11, D14, I5 and the 3 real sites. All identical.
   Exit codes 1, 1, 1, 1, 2 and 0, 1, 1.
3. refcount.py (my own counter): lucario 1, plazir15 46, charter 67 references. It reuses
   the REFERENCE_ATTRIBUTES table order, so it checks totals and cross-element order only.
4. Regex tag tally: plazir 35 a + 6 link + 4 img + 1 script = 46; charter 60 + 4 + 1 + 2 = 67;
   lucario 1. No <base> element in any page.
5. Committed out/*.json against fresh runs: stdout and exit equal for all 3 sites.
6. Probe: manifest with two missing page files: rc=2, two findings, both id "input_invalid".

## Per field verdicts
- id: HOLDS for stability (33 inputs twice, 8 five times: zero diffs). Content holds on the
  12 findings hand-checked: fixtures D3 (#3), D10 (#1, #3), D11 (#2 on sub/page.html),
  D14 (#1, #2, #3, #5); real plazir (#38), charter (#21, #27, #54).
  LIMIT: unique for outside findings (file#index; manifest file names must differ,
  base_path_audit.py:634) but not for input findings, where id = reason (line 599).
- page: BROKEN as literally stated. page is the manifest entry's url (line 588), e.g.
  "https://o.github.io/repo/". The manifest file name appears only as the id prefix
  ("index.html#3:..."). It holds only as "page names the manifest entry URL": true on all
  12 findings and on I5.
- resolved: HOLDS on the 12 findings; each equals the hand-joined absolute URL (D3 /b.png
  becomes https://o.github.io/b.png). I5 refusal: null.
  LIMIT: fragments dropped by design; non-default ports kept, default ports elided
  (serialize_url). No input tests either; code reading only.
- pagesChecked: HOLDS. Fixtures 1 each, D11 2 (two pages), I5 0; real sites 1, 1, 1.
  LIMIT: every refusal reports 0 pages and 0 references (lines 659, 690, 707), even when
  some pages were fine. Stated behaviour, not a counter fault.
- referencesChecked: HOLDS. Fixtures D3 3, D10 3, D11 3, D14 5, I5 0. Real: lucario 1,
  plazir15 46, charter 67, matching the hand tallies. External and inside references count
  (line 713 adds every extracted reference before filtering).

## Residual risk and gaps
- Not tested: in-element id order when markup order differs from table order; srcset
  invalid-descriptor skip; ports; fragments; query strings.
- Stability tested on one Python version and one host only.
- Real-page checks rest on three counts (tool, my counter, regex tally); no line-by-line
  read of all 67 references.
- Closing the counter gap is the L1's decision.

Artifacts (sandbox only): fieldcheck.py, refcount.py, matrix_runs.json, counter-7697990.json.
Process note: two of my writes used a relative path and left a copy under the fleet root
(.ufo/waves/round-29/w2/). I removed that copy and the w2 directory my write created.
