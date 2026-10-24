MET — counter v3 (`ce2d5a0c…`) caught all seven non-equivalent one-member mutants of the landed build's path/pchar tables (`_TABLE_PCHAR` sitemap_audit.py:128, `_path_ok` :163-179); the only tool that met is byte-equivalent (no witness exists). Attacked build `914ebdee…`; tip41 `50287ac6…`, base40 `4de35f8c…`.

Detector, per tool (no `--seed`; exit 0 met / 1 not met / 2 cannot evaluate), ~35-75 s each:
`timeout 900 prlimit --as=8000000000 -- python3 -B .ufo/waves/round-42/c42_count_v3.py --root <lane> --tool-file <tool> --label MutBuildPath-<name> --out <receipt>`
Baseline on the untouched copy: seed 227916472535417, equalRuns 10/10, ratios T1 1.088 / T2 1.334 / T3 1.432 / T4 1.254 / T5 1.237, met true, exit 0. Every mutant is a separate file derived from those bytes; the pristine copy was never edited.

Tools (`/fast/scratch/hyaku/kake-r42w2/MutBuildPath/`, receipt = same name `.json`):

| tool | sha256 | one-line change | seed | equalRuns | ratios T1/T2/T3/T4/T5 | met | caught by |
|---|---|---|---|---|---|---|---|
| mut1_drop_at | 80d5991bd7ae… | :122 drop `+ b"@"` from `_PCHAR_ASCII` (one class member) | 91708816275618 | 1/10 | 0.998/0.973/1.138/1.219/1.173 | false | A,B,C,D,E,T1,T2,T3,T5 (T4 equal) |
| mut2_add_bracket | d94373ea07da… | :122 `+ b"@["` (one class member added) | 274144040538888 | 2/10 | 1.119/1.381/1.154/1.294/1.115 | false | A,C,D,E,T1,T2,T3,T5 (B,T4 equal) |
| mut3_table_colon | a214238c8892… | :128 table byte 0x3A (`:`) set to 0x01 (one table byte) | 208978087220872 | 1/10 | 0.991/1.219/1.392/1.241/1.079 | false | A,B,C,D,E,T1,T2,T3,T5 (T4 equal) |
| mut4_pct_tail2 | e5f67184ffb5… | :166 `_BAD_PCT_RE.search(segment)` → `search(segment[:-2])` (branch) | 31433165955138 | 1/10 | 0.960/1.145/1.208/1.264/1.160 | false | A,B,C,D,E,T1,T2,T3,T5 (T4 equal) |
| mut5_step_plus1 | 09bac6e64397… | :176 `at = size if edge < 0 else edge` → `edge + 1` (branch) | 108914815929810 | 0/10 | 1.129/0.964/0.801/0.968/0.949 | false | A,B,C,D,E,T1,T2,T3,T4,T5 |
| mut6_loop_last | 4322cc14c147… | :171 `while at < size:` → `while at < size - 1:` (branch) | 106931149175975 | 4/10 | 0.956/1.344/1.387/1.342/1.099 | false | A,D,E,T1,T2,T3 (B,C,T4,T5 equal) |
| mut7_dead_byte | 47cf11408869… | :128 table byte 0xF5 set to 0x01 (one table byte) | 5334967241201 | 10/10 | 1.052/1.704/1.426/1.220/1.620 | **true** | none — equivalent; witness: none found |
| mut8_short_path | 873ac0aa808c… | :166 inserted `if len(segment) <= 2: return True` (branch) | 140016419931197 | 9/10 | 0.987/1.332/1.497/1.473/1.183 | false | **A only** |
| mut8_short_path reruns | 873ac0aa808c… | same bytes, two fresh seeds | 137921102632317 / 188675091119672 | 9/10, 9/10 | 1.067/1.200/1.411/1.473/1.203 · 1.054/1.313/1.268/1.084/1.196 | false, false | A only, A only |

Kill/survive: mut1-mut6 and mut8 killed (counter exit 1 each; mut8 three seeds); mut7 survived (exit 0) and is equivalent (no witness); none inconclusive (no exit 2).

Witnesses (`_parse_url`: tip41 vs mutant; CLI via `cli/manifest_w.json`, one `loc` per check, pristine `sitemap_audit.py` as reference):
- mut1 `https://example.com/a@b`: tuple vs None; CLI clean → `loc_not_absolute`.
- mut2 `https://example.com/a[b`: None vs tuple; CLI `loc_not_absolute` → clean.
- mut3 `https://example.com/a:b`: tuple vs None; CLI clean → `loc_not_absolute`.
- mut4 `https://example.com/a%4`: None vs tuple; CLI `loc_not_absolute` → clean (also `a%`, `a%4?q`, `a%4#f`).
- mut5 `https://example.com/a/b`: tuple vs None (any ≥2-segment path); CLI clean → `loc_not_absolute`.
- mut6 `https://example.com/a[`: None vs tuple; CLI `loc_not_absolute` → clean.
- mut7: none. Bytes C0, C1, F5–FF occur in no UTF-8 encoding of U+0000–U+10FFFF under `surrogatepass` (243 distinct bytes reachable), and the table is read only through `value.encode("utf-8","surrogatepass")` (`_uri_ok`, :215) — the 0xF5 entry is dead, so this tool cannot be a control.
- mut8 `https://example.com/[`: None vs tuple; CLI `loc_not_absolute` → clean (also `https://example.com/%`).

Findings (per checked statement):
- "One-member class changes are caught": holds, strongly — run A (`cases_a`, every ASCII unit in the path slot) was unequal for every killed mutant and run E (`cases_e`, eleven slots) for all but mut8; mut1/mut3/mut4 were each killed by 9 of 10 runs.
- "A malformed-triplet corner at the end of the path escapes": wrong — mut4's 2-byte tail (`segment[:-2]`) was still caught by A-E and T1/T2/T3, because the generators place defects at end-of-value (`long_value`'s `rng.randint(lo, len(value))`).
- "Every path length is exercised": overstated — a 2-byte path (`/` plus one byte) comes only from run A's single-empty-segment case (`make_url`, ~1/30 of path cases). mut8 was killed by run A alone on 3/3 seeds; B, C, D, E and all five timing shapes were byte-equal on that defect. If a future generator removes that corner, a short-path fast path would meet.
- "Runs A-E exit 2 (could-not-evaluate), so they do not test value judgments": wrong — both tools exit 2 because generated `sitemapUrl` values include invalid ones, but :634-652 still builds and emits one item per check, and the output hashes differ for every killed mutant (e.g. mut1 run A `ea6e51072888` vs `01c75f149c51`), so those runs do compare per-value judgments.
- "'/' or '?' added to the pchar set is a defect": not a control — the path is cut at `?`/`#` before the table is read (:229-286) and the loop accepts only `0x2F` at each segment head (:172-173), so those table bytes are unobservable (code-level reasoning, not scored as a mutant).

Restoration: pristine copy sha256 before 914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021, after 914ebdee… (identical); lane `scripts/sitemap_audit.py` 914ebdee… (read-only); counter `ce2d5a0c…`. No packages installed or upgraded. Artifacts total 416 KB under the sandbox; all counter processes finished (exit codes 0/1, none 2).
