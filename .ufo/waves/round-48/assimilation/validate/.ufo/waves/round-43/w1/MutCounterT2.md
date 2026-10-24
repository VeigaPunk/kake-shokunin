SURVIVED — the T2 scoped restructure is NOT load-bearing for the two named controls: all five one-member T2 reverts still score the case-fold memo 9-10/11 and the 32-prefix tool 8-9/11 with met=false, while unweakened v4 scores 9/11 and 9/11. The tasking expectation that those controls "MEET the reverted counter" is falsified — a coverage finding, not a contract change.

Detector (frozen command; no --seed; exit 1 = not met on every run):
`timeout 900 prlimit --as=8000000000 -- python3 -B <counter> --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file <tool> --label MutCounterT2-<tag> --out /fast/scratch/hyaku/kake-r43/MutCounterT2/<tag>.json`

Mutants (copy of `.ufo/waves/round-43/c43_count_v4.py`, sha256 1c3b9661…, PREDICATE byte-identical — asserted in builder and in every receipt's `predicate` field; only `shape_t2` differs; each scored against both controls, one receipt per score):
| mutant path (in /fast/scratch/hyaku/kake-r43/MutCounterT2/) | sha256 | one-member change | v1_casefold receipt | v2_prefix32 receipt |
|---|---|---|---|---|
| c43_count_v4_t2-named-revert.py | 55daf5571c0f69e3f0fba5ea3b66ef123b62fb4ac9d1778f35519bc6095a7fdb | T2 = one write_single, 20,000 long values, 1-3% defects, no fold pair (v3 body), rest of v4 kept | 10/11 met=false, false=F | 9/11 met=false, false=F,T3 |
| c43_count_v4_t2-memberB-nofold.py | 3d1b215aa3104cb4c62ed77eb70319c71518b9ee466a896d850dbf9db69078f2 | only the fold pair removed | 10/11 false=F | 9/11 false=F,T2 |
| c43_count_v4_t2-memberA-onefile.py | f2ff1638a7905efe75e561d06178c8f3c8e32429b478d289fa91821ccaddbb7d | only the 20-file scoping removed (one write_scoped file of 20,000; fold pair kept) | 10/11 false=F | 8/11 false=F,T2,T3 |
| c43_count_v4_t2-memberC-hosturl.py | ad4c1b832ae430ca28d2d18b14e7a6b04ea3eb86c07d35b8791400836657737c | only the segment-cased sitemapUrl removed (host-derived) | 10/11 false=F | 8/11 false=F,T2,T3 |
| c43_count_v4_t2-memberD-noport.py | 38c9f8d6c117ab40a22526c54c3a62896c5c4b16537b1145c4ceda878edeeb29 | only the 2% long-port class removed | 9/11 false=F,T2 | 8/11 false=A,F,T3 |
Baseline v4 itself on this host: v1_casefold 9/11 false=F,T2; v2_prefix32 9/11 false=F,T3 (both met=false, rc=1); receipts base-v4-v1.json, base-v4-p32.json.

Fresh controls built from the build (`scripts/sitemap_audit.py` sha256 914ebdee…; `_parse_url` wrapped with the same skip): fresh-casefold.py efc011fbcf43… and fresh-prefix32.py 9ada31ab83… . Unweakened v4: fresh-casefold 10/11 false=F (met=false), fresh-prefix32 8/11 false=F,T2,T3. Named revert: fresh-casefold 10/11 false=F, fresh-prefix32 9/11 false=F,T3. All rc=1, met=false.

Witnesses (survivor evidence; ref41 = tool at 1ef7a0e9, sha256 50287ac6…):
- case-fold, value 2 `Http://g3C+(1H.com/djgk65iy6rl/sldk?e7,d%dEv4` under sitemapUrl `Http://g3C+(1H.com/djgk65Iy6rl/sitemap.xml`: ref41 exit 1 `{"verdict":"failed-policy",…"loc_out_of_scope","entry":2}`; case-fold memo exit 0 `{"verdict":"clean"}`. Still caught by run F (120 fold pairs + 40 pairfiles) in every mutant, so the mutant detects it.
- 32-prefix, value 2 `HTtp://rxJ9tuc1.test/ywif/j812cj/ahibvh/w5vzq0uzwd` (42-cp shared prefix): ref41 findings [loc_not_absolute entry 1]; prefix32 findings [entry 1, entry 2]. Still caught by F and T3.

Per checked statement:
1. "case-fold control MEETS the reverted counter" — WRONG (10/11, F false, all mutants and fresh control).
2. "32-prefix control MEETS the reverted counter" — WRONG (8-9/11; F and T3 false in 6/6 runs).
3. "both controls FAIL unweakened v4" — HOLDS (met=false for all four controls; my v1_casefold 9/11 matches freeze r42ctl-v1_casefold 9/11, my v2_prefix32 9/11 vs freeze 7/11 is seed variance in E/T2 only — F and T3 false in both).
4. "T2 restructure is load-bearing" — WRONG/overstated for these classes. F already carries the fold class (`cases_f` :466-478, `layout_f` :549-556) and T3 the prefix class (:798-799); T2's own equality power is one 1,000-value file, not 20,000 values: `shape_t2` returns only the last `write_scoped` manifest (c43_count_v4.py:625-626) and the run passes one `--manifest`, so 19 of 20 files (19,000 values) are never read (verified 5 seeds: 20 xml files, 1 check, 1,000 live locs).
5. Additional live defect: the "case-fold pair" collapses to two identical values when the uppercased position is a digit — `seg[j].upper()` on a digit is a no-op at c43_count_v4.py:613-614 (same helper shape for run F at :433-434). Measured 537/2000 = 26.9%. T2's live head pair is genuine only in the seeds where the char is a letter (6-seed probe: T2 differs from ref41 at seeds 3,4,6; not at 1,2,5); F's 200 draws make F reliable. This is why reverting T2 costs nothing.

Restoration evidence: no byte of the lane repo or fleet repo was written; `.ufo/waves/round-43/c43_count_v4.py` still sha256 1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab; controls unchanged 9993b842… / eadf5df4…; build unchanged 914ebdee…. All work in /fast/scratch/hyaku/kake-r43/MutCounterT2 (824 KB; generated case directories deleted). No tool installs or upgrades. No stray processes left (pgrep empty).
