VERDICT (attacked: counter v3's power over one-member defects of the landed build in query/fragment scanning): **7/7 single-member mutants killed, 0 met, no surviving witness** — no control in this area; C1's equality clause holds on the surface I attacked (sample, not a proof of the counter).

# Scope and bytes
- Build copied from lane `scripts/sitemap_audit.py`, sha256 `914ebdee7bcb…`; lane HEAD `b061585a` (tasking tip `721310b1` is its ancestor, `git merge-base --is-ancestor` exit 0); tool bytes unchanged before/after (`cmp` identical).
- refs: tip41 `/fast/scratch/hyaku/kake-r42/shared/tip41.py` `50287ac6de56…`, base40 `4de35f8c9d3e…`, counter `.ufo/waves/round-42/c42_count_v3.py` `ce2d5a0ca2c3…`.
- Mutation sites are all in the byte-table scanner: `scripts/sitemap_audit.py:123` (`_QUERY_ASCII`), `:129` (`_TABLE_QUERY`), `:206` (`_scan` fragment bound), `:253`/`:261` (`?`/`#` edge branches). Each mutant is one member of one file.

# Exact commands (all exit codes observed)
```
S=/fast/scratch/hyaku/kake-r42w2/MutBuildQueryFragment      # 556K total, 8 receipts, 10 logs
cd /home/vgpnk/Projects/shokunin/kake-shokunin
timeout 900 prlimit --as=8000000000 -- python3 -B .ufo/waves/round-42/c42_count_v3.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file $S/<t>.py \
  --label MutBuildQueryFragment-<t> --out $S/rcpt-<t>.json    # t=build→exit 0; mut1..mut6,mut8→exit 1
  (no --seed; ≤3 concurrent; batches 3+3+1+1)
python3 -B $S/diff.py <mutant>.py /fast/scratch/hyaku/kake-r42/shared/tip41.py   # exit 1, d=diff count
python3 -B <tool> --manifest manifest.json                                        # CLI witnesses, $S/wit/
cmp -s scripts/sitemap_audit.py $S/build.py && echo identical                     # identical
```
# Receipts + witnesses (build vs tip41 `_parse_url`: 0 diffs on 4,037 query/fragment values; CLI output equal)
| tool (path `$S/`) | sha256 | one-member change | seed | eq | ratios T1/T2/T3/T4/T5 | met | caught by | witness (build → mutant) |
|---|---|---|---|---|---|---|---|---|
| build.py | `914ebdee7bcb` | copy of the landed build | 103335987227855 | 10/10 | 1.03/1.267/1.382/1.256/1.179 | **met** | – | none (control baseline) |
| mut1.py | `2cddb90193c9` | `:123` drop `?` from `_QUERY_ASCII` (class member) | 269443291073253 | 2/10 | 0.994/1.281/1.299/1.277/1.191 | not met | A,C,D,E,T1,T2,T3,T5 | `http://h/a?b?c` accepts → rejects; CLI loc `loc_out_of_scope`→`loc_not_absolute` (d=378) |
| mut2.py | `bb95e364626a` | `:129` table allows `#` (`_QUERY_ASCII + b"#"`, one table byte) | 138950449609714 | 7/10 | 0.997/1.36/1.348/1.271/1.235 | not met | A,D,E | `http://h/a?b#c#d` rejects → accepts (second `#`); CLI `loc_not_absolute`→`loc_out_of_scope` (d=16) |
| mut3.py | `ab32e6009548` | `:253` path+`?` branch `query_end = size` (fragment start ignored) | 42405981941138 | 7/10 | 1.026/1.519/1.281/1.252/1.171 | not met | A,D,E | `http://h/a?b#c`, `http://h/a?#f` accept → reject; CLI entries 3 and 8 flip (d=2160) |
| mut4.py | `794b5a58911a` | `:206` fragment region starts one byte late (`fragment_start + 2`) | 104161093754015 | 5/10 | 1.04/1.436/1.255/1.228/1.194 | not met | A,D,E,T1,T3 | `http://h/a#\|x`, `http://h/a#%2` reject → accept; CLI entry 4 flips (d=70) |
| mut5.py | `e6ed23b98ad4` | `:129` `_class_table(_QUERY_ASCII, non_ascii=False)` (bytes ≥0x80) | 7897822695403 | 7/10 | 1.0/1.235/1.424/1.207/1.231 | not met | C,D,E | `http://h/a?bé`, `http://h/a#é` accept → reject; CLI entry 5 flips (d=61) |
| mut6.py | `da3f90fe2a2b` | `:261` `?`-after-authority branch `query_end = size` | 145472336881092 | 8/10 | 0.95/1.704/1.432/1.309/1.183 | not met | A,D | `http://h?q#f`, `http://h?#f` accept → reject; CLI entry 6 flips (d=3) |
| mut8.py | `3641e212839c` | `:206` fragment region bounded by `query_end`, not `size` | 53342358763630 | 3/10 | 1.073/1.337/1.292/1.195/1.219 | not met | A,C,D,E,T1,T2,T3 | `http://h/a?b#c\|`, `http://h/a?b#c#d` reject → accept; CLI entries 2 and 7 flip (d=583) |

Receipts: `$S/rcpt-{build,mut1,…,mut8}.json` (each with `counterSha256`, `ref41Sha256`, `toolSha256`, per-run `equal`, `equal`/`ratiosExact`).

# Per checked statement
- "counter v3 catches one-member query/fragment changes" — **holds for this sample** (7/7 killed, each on ≥2 runs, each with an independent `_parse_url` and CLI witness).
- "build met under counter v3" — **holds** independently: my own seed `103335987227855`, equal 10/10, max ratio 1.382 ≤ 2.0 (consistent with the L1's 1.006–1.427 receipts at SCORECARD:3099).
- "build tool sha256 `914ebdee…`" — **holds** (hash of lane file and of my copy; unchanged after my runs).
- "lane tip `721310b1`" — **stale at check time**: HEAD is `b061585a` (tasking tip is an ancestor); `scripts/sitemap_audit.py` is identical across them, so the probes stay valid.
- "run E inserts every unit in each of eleven slots" (counter docstring L43–51, code L321–377) — **holds**; E is where mut2/mut3/mut4/mut5/mut8 were killed.
- **Narrow coverage (observation, not a defect):** mut6's only divergences are `http(s)://host?a#f` with no `/` after the authority; run E never builds that shape (`slot_value` always appends `"/" + path`, counter:356) and all five T shapes carry paths, so only runs A (10% empty segments, counter:186–190) and D killed it. mut5 is reachable only by C/D/E (run A's units are ASCII+percent only, counter:108–110). Both were caught; the counter's redundancy is what carries these two.

# Restoration / cleanliness
- No lane, sibling or jj file written; only `$S/` and this report. Pristine bytes re-scored last and `cmp`-equal to the lane file. My process trees exited (remaining `c42_count_v3` process belongs to sibling seat `MutBuildPath`, not mine).
- No tool installs or upgrades (nothing needed). No network. All runs bounded by `timeout 900` and `prlimit --as=8000000000`, ≤3 concurrent, ≤556K written.
