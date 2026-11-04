
## Round 75 — quote corrections (appended round 76)

Five claim-row spans in the round-75 section quoted observed output that no committed receipt line
contains: each splices across an observed field, or appends a token printed only by a different counter.
Each correction row below names the defective span verbatim, quotes the whole receipt line it should have
quoted (exact equality with a receipt line after trimming), and names the receipt file and line. Appended
2026-11-03 by the round-76 C1 repair; no earlier line was rewritten or removed. The two remaining spans of
the same population are corrected in `corpus/QUALITY.md` (section "Round-76 criterion — quoted receipts are
whole") and `corpus/lessons/round-75.md` (section "Corrections").

| # | Defective span (as quoted) | Whole receipt line (verbatim) | Receipt file:line | Correction |
|---|---|---|---|---|
| 1 | `files=18 mismatches=0 append_only=true met=true missing_frozen=0` | `C1v1 revision=f87d14a9 rows=32 live=20 files=18 mismatches=0 classes=- append_only=true met=true missing_frozen=0` | `.ufo/waves/round-75/controls/after-c1-row-truth.txt:4` | The observed line carries classes=- between mismatches=0 and append_only=true; the claim dropped it, so the quoted fragment is contiguous in no receipt. `[r76-correction 2026-11-03]` |
| 2 | `mismatches=3 classes=E3 append_only=false missing_frozen=1` | `C1v1 revision=153fa2a9eda8d95618697186feb18574cc7daae1 rows=27 live=15 files=15 mismatches=3 classes=E3 append_only=false met=false missing_frozen=1` | `.ufo/waves/round-75/controls/ctl-deletion-landed.txt:3` | The observed line carries met=false between append_only=false and missing_frozen=1; the claim dropped it, so the quoted fragment is contiguous in no receipt. `[r76-correction 2026-11-03]` |
| 3 | `population=18 bound=18 mismatches=0 met=true missing_frozen=0` | `C2v1 revision=f87d14a949e1b5f8b4ec5807b75f22aa3e337353 population=18 bound=18 mismatches=0 met=true` and `population: derived=18 frozen=16 missing_frozen=0 beyond_frozen=2` | `.ufo/waves/round-75/controls/after-c2-receipts.txt:5-6` | The C2 line ends at met=true; missing_frozen=0 is printed on the following derived-population line, so the claim spliced two lines into one and the fragment is contiguous in no receipt. `[r76-correction 2026-11-03]` |
| 4 | `receipt: source=committed declared_valid=true` | `receipt: source=committed worktree=identical declared=abfbfaac58bcee2514490940d1b16365027a07c9 declared_match=false declared_valid=true` | `.ufo/waves/round-75/controls/after-c2-receipts.txt:7` | The claim dropped worktree=identical, the declared revision and declared_match=false between source=committed and declared_valid=true. `[r76-correction 2026-11-03]` |
| 5 | `mismatches=0 met=true missing_frozen=0` | `C1v1 revision=f87d14a9 rows=32 live=20 files=18 mismatches=0 classes=- append_only=true met=true missing_frozen=0` | `.ufo/waves/round-75/controls/after-c1-row-truth.txt:4` | The move-log cell jumped from mismatches=0 to met=true, dropping the observed classes=- append_only=true; the fragment is contiguous in no receipt. `[r76-correction 2026-11-03]` |
