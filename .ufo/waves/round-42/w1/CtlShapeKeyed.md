MET — two of my five controls met the C1 predicate; the counter cannot see the work they skip.

Seat CtlShapeKeyed (control class: fast paths keyed on the counter's timing shapes). Python 3 stdlib only.
Tools (in /fast/scratch/hyaku/kake-r42w1/CtlShapeKeyed/, all built from shared/tip41.py 50287ac6…):
 ctl_tail.py            c3ec0269f0ef3d7d8ce2aa9d47eed3bc1403b115d4c0c1c52fc88d04ce58c01e
 ctl_tail_filesize.py   d1bc7438f342152b3599b1b5e8f5be21a8df2afc8ba076687f04b951de4b9989
 ctl_skip_entries.py    a28019bd3c07c9bbbd71b1565c0ab9f254a6360e3d2c3fd66d6189517922f322
 ctl_skip_48.py         09e0e12d27bb400d2ef01740b1ba1507bf15d098065708fef8003bc97bd47de8
 ctl_skip_200k.py       b92c5f3e30ed47b9811925922a45d48d59ba4de2fb57acc268694a7453505f44
Counter .ufo/waves/round-42/c42_count.py sha256 7bfc32c5e76dca942208934cfbe89f166eda2776b40e69de987706b4d97dd2a6 (matches SCORECARD).

Command (one per tool; receipts in this dir, a second copy in rerun/):
 timeout 900 prlimit --as=8000000000 -- python3 -B <repo>/.ufo/waves/round-42/c42_count.py --root <repo> --tool-file <tool> --label CtlShapeKeyed-<suffix> --seed <N> --out /fast/scratch/hyaku/kake-r42w1/CtlShapeKeyed/<suffix>.json

Receipts (seed; equalRuns; ratios T1/T2/T3/T4/T5; met; process exit):
 ctl_tail.py 4201 8/8 0.958/1.258/1.346/1.261/1.160 met=true exit 0
 ctl_tail_filesize.py 4206 8/8 0.978/1.253/1.338/1.246/1.200 met=true exit 0
 ctl_skip_entries.py 4202 7/8 1.013/1.004/0.955/1.065/9.434 met=false exit 1
 ctl_skip_48.py 4203 7/8 5.236/2.749/1.363/1.261/1.181 met=false exit 1
 ctl_skip_200k.py 4204 6/8 5.310/2.742/1.354/1.251/1.184 met=false exit 1
 reference tip41 4205 8/8 5.214/2.827/1.330/1.223/9.591 met=false exit 1
 reference base40 4303 3/8 1.006/1.024/0.965/1.015/1.025 met=false exit 1
Second seeds, same verdicts: ctl_tail 4301 8/8 met (0.969/1.218/1.294/1.202/1.228); ctl_tail_filesize 4302 8/8 met (0.973/1.263/1.420/1.231/1.227).
Every run was repeated once (receipts in rerun/): identical verdicts, ratios within noise.

What each tool skips, and which run caught it:
 ctl_tail.py — keyed on a file with >=20000 entries or a manifest with exactly 48 checks; for a keyed value it judges only the authority prefix, the first 64 and the last 256 code points and never runs _URI_RE on the middle. NOT CAUGHT (met on two seeds).
 ctl_tail_filesize.py — same skip, keyed on file size >=1000000 bytes or 48 checks. NOT CAUGHT (met on two seeds).
 ctl_skip_entries.py — keyed on >=20000 entries; the whole URL rule is skipped for the loc values (urlsplit only). CAUGHT by run T1 (candRepsEqual 0/5).
 ctl_skip_48.py — keyed on exactly 48 checks; the whole URL rule is skipped for the manifest's sitemapUrl. CAUGHT by run T5 (0/5); ratios T1 5.236 and T2 2.749 also break the 2.0 limit.
 ctl_skip_200k.py — keyed on a value of >=150000 code points; the whole URL rule is skipped. CAUGHT by run C and run T5 (0/5).

Witnesses where the two meeting controls differ from tip41 (make_witness.py; cases under witness/):
 keyed file (20000 entries; the file-size variant needs >=1 MB — case_filesize is 2270165 bytes) whose entry 20000 has a loc of 1200 code points with "{" at offset 400 (outside the first 64 and the last 256): tip41 exit 1, finding loc_not_absolute entry 20000; ctl_tail and ctl_tail_filesize exit 0, status clean (the value is judged in scope). witness/case_entries/manifest.json, witness/case_filesize/manifest.json.
 manifest with exactly 48 checks whose first sitemapUrl is 900 code points with "{" at offset 400: tip41 exit 2, check_invalid; both controls exit 0, clean. witness/case_48/manifest.json.
 ctl_skip_200k witness: witness/case_200k/manifest.json (sitemapUrl of 150000 code points with a defect: tip41 check_invalid, control clean).

Findings (path:line):
 .ufo/waves/round-42/c42_count.py:318 — the equality runs put loc values into files of 20-60 entries (200-800 checks per manifest), so no equality run ever has 20000 entries, a 1 MB file or 48 checks: a control keyed on the timing shapes is never exercised by the equality runs.
 .ufo/waves/round-42/c42_count.py:363 and :383 — the timing shapes put the defect in the last 64 code points (defect_window=64), exactly what a tail-window control still examines, so the shape-keyed control agrees with tip41 there.
 .ufo/waves/round-42/c42_count.py:604 — met = (equal == 8) and every ratio <= 2.0; equality is tested on the generated runs only (equalValues 3290), so the counter does not establish "keeps EVERY judgment of the round-41 tool".

Checked statements (holds / overstated / wrong):
 "A control that skips part of the claimed work and meets the predicate shows the counter is too weak" — HOLDS, twice, with two independent keys (entry count, file size).
 "The predicate (equal on every generated run, ratio <= 2.0) is a sufficient test of 'keeps every judgment of the round-41 tool'" — OVERSTATED: ctl_tail and ctl_tail_filesize met it while judging a mid-value defect as valid (witnesses above).
 "The round-41 tool scores T1 ~5.4, T5 ~9 (not met)" — HOLDS (T1 5.214-5.249, T5 9.591-9.640 over two seeds); the brief's summary omits T2, which also fails at 2.805-2.827 (the SCORECARD's own L1 receipt records T2 2.811).
 "The round-40 tool fails equality (3/8)" — HOLDS (my base40 run: 3/8, exit 1).
 "The counter's runs decide 'every judgment' of the tool" — WRONG beyond the generated runs: they decide the runs only, while the predicate's wording claims all values.
Recommendation for the L1: the equality part needs values with a defect in the middle of a long value on a keyed shape (loc of 2000-2047 code points with a defect at any position inside a 20000-entry file, and a 48-check manifest carrying such a loc), or the predicate must be restated as "equal on the generated runs".

No tool was installed or upgraded in this seat (no pacman, uv or npx use).
