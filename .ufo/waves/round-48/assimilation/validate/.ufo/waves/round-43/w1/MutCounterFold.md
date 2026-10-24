SURVIVED: 1 of 4 one-member weakenings of counter v4 (M3, `segment_smu` → root-dir derived sitemapUrl) lets the case-fold memo control MEET the predicate (11/11, met true) with a live witness; M1/M2/M4 are KILLED (control still fails, 10/11). The tasking sentence "control must MEET every weakening and FAIL unweakened v4" holds only for M3 plus the fail half.

Aliases: `R=/home/vgpnk/Projects/shokunin/kake-shokunin`; `S=/fast/scratch/hyaku/kake-r43/MutCounterFold`. Lane tip `7c070797eb5b` (freeze b49cba9 ancestor); lane counter `.ufo/waves/round-43/c43_count_v4.py` sha256 `1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab` (unchanged). Control `$S/casefold_ctl.py` = lane `.ufo/waves/round-43/controls-r42/v1_casefold.py`, sha256 `9993b842427d1592713309420626e46e42f1e56defab28b2f5349e6391cf4bc4`; ref41 `$S/ref41.py` sha256 `50287ac6…`; base40 `$S/base40.py` sha256 `4de35f8c…`. All four variants are byte-copies of v4 with exactly one hunk changed (diff shown below), `PREDICATE` byte-identical (True for all four), scored WITHOUT `--seed`.

Command template, one instantiation per row: `timeout 900 prlimit --as=8000000000 -- env TMPDIR=$S/tmp python3 -B $S/<file> --root $R --tool-file $S/casefold_ctl.py --label MutCounterFold-<tag> --out $S/receipt_<tag>.json`

| tag | path (in $S) | sha256 | one-member change | seed | equalRuns | met | exit | fails | verdict |
|---|---|---|---|---|---|---|---|---|---|
| v4_pristine | v4_pristine.py | 1c3b9661…fe8eab | none (unweakened v4) | 227027283937805 | 9/11 | false | 1 | F,T2 | control KILLED |
| M1 | counter_M1.py | ef70ab9b0b599641f18288af0c31641071f5d9f31766d626609b2c5426d0ef99 | drop the 120 run-F `foldpair` units (v4:469-471) | 129771476919044 | 10/11 | false | 1 | F | KILLED |
| M2 | counter_M2.py | 6d37d7e20e94960aac6461c5c1c83d2d56da6d75c5f327cd9143887b7d71b824 | T2 second member independent: `b = long_tail_value(rng, scheme, host, seg, False)` instead of the exact fold partner (v4:616) | 223501742987858 | 10/11 | false | 1 | F | KILLED |
| M3 | counter_M3.py | 40ab684d69d27c8fba8c036e2d13ef4a08367a370cfae872b3ba6cf0e0b552ce | `segment_smu` returns root-dir derived `<root>/sitemap.xml`, no segment casing (v4:493-503) | 56640396605412 | 11/11 | true | 0 | — | SURVIVED |
| M4 | counter_M4.py | d29112e96a6b9a9851be19495954fff6ce95e8ed1c1f3b45aa886fe184698983 | drop the fold pairs inside run-F `pairfile` (2 per file, 40 files, v4:474-478) | 158317152376345 | 10/11 | false | 1 | F | KILLED |

Receipts: `$S/receipt_<tag>.json` (seeds above, `counterSha256` = mutant sha, `toolSha256` = control sha, ratios all ≤1.57). Timing rows under every mutant: T1-T5 ratios 1.15-1.57, so no mutant died on cost; all deaths are equality deaths on run F (exit 2 both tools, differing per-check findings) and, for pristine, run F plus T2 (T2 `candRepsEqual` 0/5).

Survivor M3, witness (control differs from the round-41 tool on a value M3 never generates): `$S/witness/{f.xml,m.json,probe.json}`. `f.xml` holds `http://h.example/Ab/x` and `http://h.example/ab/x` under check sitemapUrl `http://h.example/Ab/sitemap.xml`. `python3 -B $S/ref41.py --manifest $S/witness/m.json` → exit 1 `{"verdict":"failed-policy",…"findings":[{"code":"loc_out_of_scope","entry":2}]}`; `python3 -B $S/casefold_ctl.py --manifest $S/witness/m.json` → exit 0 `{"verdict":"clean",…"findings":[]}`. The control's fold cache answers the lowercase member from the cased member; with M3's root-dir sitemapUrl both are in scope and the wrong answer is unobservable, so M3 lets an unsound cache through.

Findings (`R/.ufo/waves/round-43/c43_count_v4.py`):
- `:493-503` `segment_smu` is the single load-bearing case-fold member (call sites `:555` run F, `:625` T2). Removing segment casing alone admits the control (M3 met true).
- `:469-471` `foldpair` units and `:474-478` `pairfile` fold pairs are redundant with each other: M1 (units gone) still fails F via pairfile; M4 (pairfile folds gone) still fails F via the units. So the class power is two-deep in F, not one-member deep.
- `:614-616` T2's fold pair self-degenerates: when the drawn `seg[j]` is a digit, `seg[j].upper()` is a no-op, `seg_a == seg`, and `b = a.replace(...) == a`; the pair is then not a fold pair. Replay of M1 seed 129771476919044 (`$S/diag_t2/calls_M1.json`, calls 24/25 identical sha `2b4166dfa122`, smu segment `lznth872`, first two locs equal) shows this is why M1/M2/M4 pass T2. Fresh-seed sample: 5 of 8 seeds degenerate.
- `:625-626` only the last of the 20 files `shape_t2` writes is referenced by the returned manifest; the other 19 are generated and never audited, so T2's fold coverage is one pair in one file, not twenty.

Per checked statement: "control FAILS unweakened v4" holds (9/11, met false); "control must MEET every weakening" wrong (3 of 4 killed); the implication that each named member carries the catch is wrong for F's two fold members and unreliable for T2 (degenerate pairs).

Restoration/containment: lane counter sha unchanged `1c3b9661…`; only this report was written in the lane; all mutants/receipts/logs/diagnostics are inside `$S` (640 KB); no sibling or lane files touched, no git/jj mutation (read-only `git show` only), no network, no installs/updates, no subagents, all started processes exited.
