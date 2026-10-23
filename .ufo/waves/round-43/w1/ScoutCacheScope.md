REFUTED: v1_casefold does not meet the split-fold variant; run F stays unequal.

Hypothesis (the fold pair defeats v1_casefold only because both members share one manifest file) fails the prescribed test. Splitting each `layout_f` fold-pair unit into two files and two segment-cased sitemapUrls does not make the control meet. The shared file is necessary for that unit, but it is not the only co-located fold pair in v4.

Unequal-run lists (`runs.<key>.equal == false`; neither receipt has a `runs.unequal` key):

- Unweakened freeze `.ufo/waves/round-43/verification/freeze/r42ctl-v1_casefold.json` seed 75489578906268, counter sha256 1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab, tool sha256 9993b842427d1592713309420626e46e42f1e56defab28b2f5349e6391cf4bc4: met false, equalRuns 9/11. Unequal: F (exits 2/2), T2 (exits 1/1, candRepsEqual 0/5).
- Split `/fast/scratch/hyaku/kake-r43/ScoutCacheScope/split.json` seed 94750098915824, counter sha256 30b16c342da57fbb903f17dde8590dc3709d0336184edc6748519d92b4daf012, same tool sha256: met false, equalRuns 10/11, ratios all <= 1.552. Unequal: F only (exits 2/2). T2 equal, candRepsEqual 5/5.

Command (exit 1):

`timeout 900 prlimit --as=8000000000 -- python3 -B /fast/scratch/hyaku/kake-r43/ScoutCacheScope/c43_count_v4_splitfold.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-43/controls-r42/v1_casefold.py --label ScoutCacheScope-split --out /fast/scratch/hyaku/kake-r43/ScoutCacheScope/split.json`

Diff against frozen `c43_count_v4.py` is only `layout_f`: `foldpair` writes one check per member (`segment_smu` of that member). `prefixpair`, `pairfile`, and `shape_t2` are unchanged. T2's flip is the seed, not the edit.

Witness (exit 0, direct python3, not the bwrap score): `timeout 240 prlimit --as=8000000000 -- python3 -B /fast/scratch/hyaku/kake-r43/ScoutCacheScope/witness_f.py` → `/fast/scratch/hyaku/kake-r43/ScoutCacheScope/witness_f.json`. Seeds 1, 2, and 94750098915824:

- split `foldpair` only: equal (3/3)
- frozen shared-file `foldpair` only: unequal (3/3). Seed 1 check `fafjzoce`: round-41 `loc_out_of_scope` entry 2, casefold `clean`
- split `pairfile` only: unequal (3/3). Seed 1 check `p7rtpzfxjhd`: round-41 `loc_out_of_scope` entries 2–5; casefold drops entry 2
- split `prefixpair` and `value`: equal (3/3)
- direct `shape_t2` (code unchanged): seeds 1 and 2 equal; seed 3 unequal, round-41 keeps `loc_out_of_scope` entry 2 and casefold omits it

Checked statements:

- Shared sitemap file is why a dedicated fold pair disagrees: holds (`c43_count_v4.py:507-512`, `550-556`; control cache `controls-r42/v1_casefold.py:295-304`).
- That shared file is the only reason v1_casefold fails v4: wrong. `pairfile` (`c43_count_v4.py:557-562`) still co-locates two fold pairs under one segment-cased sitemapUrl and keeps F red. `shape_t2` (`603-625`) does the same on seeds that emit a real case variant; the freeze seed did, this score seed did not.
- Meeting the split variant would show the single-file layout is load-bearing: antecedent false this run (exit 1).

No tool installs. No processes left running.
