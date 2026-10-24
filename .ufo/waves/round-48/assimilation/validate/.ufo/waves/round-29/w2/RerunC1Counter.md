# RerunC1Counter: C1 after-value re-derivation (round 29, wave 2, falsify)

Judged on: freshness. Milestone: r29-falsify. Commit attacked: 7697990cbca20291f3b0367b8ff4220e93b38b03 (committed bytes only).
Sandbox: /fast/scratch/hyaku/kake-r29/w2/RerunC1Counter/clone, checked out at 7697990; `git status --porcelain` empty after all runs.
Installs or updates: none. Python 3 standard library only.
Lane writes: this report only (its directory was created with mkdir -p). The lane was read with git rev-parse, git show and one file read; no git status, add, commit or checkout ran there.

## 1. Counter runs
Command: `python3 -B .ufo/waves/round-29/c1_quote_truth.py --root <sandbox> --revision <full hash>`, run from the sandbox checkout. Each revision ran twice.

| revision | exit | passed | controlBroken | two runs identical | stderr line |
|---|---|---|---|---|---|
| fe1805cf32a7aadf4574637a3a8912354cee2c7b | 1 | 0/4 | false | yes | C1 0/4 at fe1805cf... |
| 7697990cbca20291f3b0367b8ff4220e93b38b03 | 0 | 4/4 | false | yes | C1 4/4 at 7697990... |
| f8675e5a2aac9007ade31bf98813fcb1deee8093 (extra) | 0 | 4/4 | false | yes | C1 4/4 at f8675e5... |
| 98dbab22ae93d325c9dcd791728c38ecf79ba0b6 (extra) | 0 | 4/4 | false | yes | C1 4/4 at 98dbab2... |

- At fe1805cf the counter file is absent (rev-parse rc 1), receipts.json is absent (cat-file rc 128), and SOURCES.md has 0 rows for S040-S043. The 0/4 is an absence baseline, measured with the 7697990 counter.
- At 7697990 each of S040-S043 passes checks a_row, b, c and d.

## 2. Counter blob and diff
- `git diff --stat d18bbf3055f33a992fc9adc4b757172554ec9981 7697990cbca20291f3b0367b8ff4220e93b38b03 -- .ufo/waves/round-29/c1_quote_truth.py`: no output, exit 0. Full diff: 0 bytes.
- Blob 139ede1efbbfeed612201239a4244b43aeda855d at d18bbf3, 7697990, f8675e5 and 98dbab2.
- Lane working-tree copy equals the committed 7697990 bytes (sha256 prefix 1b8225b570cb458e): True.
- Contrast: `git diff --stat d18bbf3 fe1805cf` deletes the file (124 lines), so the counter was added after fe1805cf.

## 3. Source chain re-derived from committed bytes (outside the counter)
- S040-S043: .html.gz body sha256 equals receipts bodySha256 (4/4). Retained .txt sha256 equals receipts textSha256 (4/4). The counter checks only the text hash, never the body hash.
- Re-deriving each .txt from its HTML (tags replaced by one space, entities decoded, whitespace collapsed) reproduces it exactly (4/4). Replacing tags with nothing matches none. The receipts textRule ("tags removed") does not say this.
- Quote against tag-stripped page text, with no inserted spaces:
  - S041 exact. S042 exact.
  - S040 not exact; equal once whitespace is removed. Raw markup `http(s):/<wbr/>/<wbr/>&lt;owner&gt;.github.io`: the `<wbr/>` tags become spaces.
  - S043 not exact; equal once whitespace is removed. Raw markup `&lt;REPO&gt;</code>), then` and `&#39;/&lt;REPO&gt;/&#39;</code>.`: the `</code>` boundaries become spaces.

## 4. Findings
- F1 Medium (claim wording). corpus/knowledge/pages-base-path.md:20 quotes S040 with spaces the page does not show, and says "the retained text collapses that cell's spacing". The mechanism is the reverse: markup breaks become spaces. Line 40 has the same defect for S043. The counter's d-check (c1_quote_truth.py:111) compares against retained text, so it passes and cannot see this.
- F2 Medium (freshness recheck). The recheck command in pages-base-path.md:3 cannot pass on a later re-mine: c1_quote_truth.py:100 hard-codes cells[8] == "2026-10-22". A re-mine that changes the mined date returns 0/4 even when every quote still matches. The counter reads committed bytes only (show, lines 46-48) and never re-fetches, so it cannot detect live drift; the "recheck" label overstates it.
- F3 Low (receipt rule). The textRule in .ufo/waves/round-29/sources/receipts.json omits the tag-to-space step the retained text needs (section 3).
- F4 Low (control runs only on the pass path). c1_quote_truth.py:113 runs the control only when ok is true, so controlBroken=false at fe1805cf is vacuous. The control flips one letter (lines 66-69).
- F5 Low (b-check is presence only). c1_quote_truth.py:102 tests that the id appears as a word after line 8. It does not test that the cited claim matches the quote.
- F6 Info. S040's requested URL redirects (receipts finalUrl .../what-is-github-pages). corpus/SOURCES.md:48 discloses it; a_row (lines 100-101) checks the requested URL.

## 5. Verdict on the attacked item
- C1 after-value (4/4 at 7697990): HOLDS. Counts, exits, determinism, blob and diff all reproduced.
- C1 "true quotes" wording: LIMIT TO STATE. Quotes are verbatim to the retained extraction; S040 and S043 carry spaces the page does not display (F1).
- C1 freshness recheck: LIMIT TO STATE (F2). The counter measures committed snapshots, and the documented recheck path fails after a re-mine.

## 6. Residual risk and verification gaps
- No live page was opened. This seat was not told to fetch a named URL, so the four sources are verified against retained snapshots (receipts accessedUtc 2026-10-22T10:29:37Z), not current pages.
- The 0/4 at fe1805cf uses the 7697990 counter, which is absent at fe1805cf by design.
- No mutation run. The control and b-check were read, not exercised with fabricated inputs.
- The f8675e5 and 98dbab2 counts are extra checks; their content was not audited beyond the counter output.
