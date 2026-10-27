# ExecValidateDryrun

Claim C3 append-gate dry run: two candidate rows S423/S424 appended to a copy of `corpus/`, the census run against the copy, cross-lane duplicate check, and a review of `validate_append.sh`. No lane file was touched (lane tree, jj and git state untouched; only this report was written).

## RUN:

Scratch: `/fast/scratch/hyaku/kake-r58/ExecValidateDryrun/v` (deleted after this report was written). Layout replicated from `validate_append.sh`, because `--file …/v/corpus/SOURCES.md` resolves every used-by path relative to the *parent* of the corpus dir (`resolve_targets`: `dir_abs=$(realpath dirname(file)/..)`), i.e. lane-root-relative:

- `cp -r <lane>/corpus v/corpus`
- the same five non-corpus used-by targets the script copies: `SCORECARD.md`, `SKILL.md`, `scripts/source_recheck.py`, `.ufo/waves/round-41/c1_count.py`, `.ufo/waves/round-41/oracle_crosscheck.py`
- two zero-byte placeholders: `v/corpus/knowledge/baidu-spider-identification.md`, `v/corpus/knowledge/baidu-spider-unblocking.md`
- rows S423/S424 inserted as the last two rows of the `## Registry` table (directly after S422), i.e. inside the section, nothing else in the file changed (`diff` = exactly `+2` lines).

Commands and observed results (all run from the scratch dir; `--file` absolute):

| run | command | exit | stdout |
|---|---|---|---|
| baseline (unmodified mirror) | `sources-census.sh validate --file …/v/corpus/SOURCES.md` | **0** | 14 `W04`, 0 `E`, tail `file<TAB>ok<TAB>…` |
| with S423/S424 + placeholders | same | **0** | 14 `W04`, 0 `E`, no S423/S424 line, tail `file<TAB>ok<TAB>…` |
| census mode, same file | `sources-census.sh census --file …` | 0 | `rows 162` (lane base registry = `rows 160`), `tier.A 139` (base 137) |

Controls injected into the same mirror (prove the gate is live on these rows, not vacuous):

| control | observed |
|---|---|
| delete placeholder `baidu-spider-unblocking.md` | exit **1**: `file E11 S424 missing used-by corpus/knowledge/baidu-spider-unblocking.md` |
| S423 row + one extra cell (12 data cells) | exit **1**: `file E01 S423 fields=12` |
| duplicate of the S423 row under id `S425` (same URL, same scope) | exit **1**: `file E04 S425 duplicate url ziyuan.baidu.com/college/articleinfo?id=3457 within scope …` |
| duplicate id `S423` with a different URL | exit **1**: `file E03 S423 duplicate id` |
| same mirror with `--today 2026-10-25` | exit **1**: `E08 S423 opened=2026-10-26`, `E08 S424 opened=2026-10-26` |
| restore final file, re-run | exit 0, stdout byte-identical to the earlier run (`cmp`) |

## FINDINGS:

1. **Row schema is accepted.** With the two rows and the two placeholder entry files, the validate run emits **no E and no W line naming S423 or S424**, exit 0. No `E01` (11 data cells, no pipe inside a cell), `E02`, `E03`, `E04`, `E05` (`docs`), `E06` (`A`), `E07` (`mined`), `E08` (`opened 2026-10-26` = round date, not future), `E09` (`180d` is a valid NNd cadence), `E10`, `E11`, `E12` (rows inside `## Registry`). Row count moves 160 → 162 and `tier.A` 137 → 139, which is the positive proof the rows were parsed (the absence of W/E lines alone would also be consistent with an unparsed line).
2. **Source-cell form matters more than the census shows.** The census only needs a URL anywhere in cell 2, so a 2-part `title — url` cell validates clean. The C3 counter does not: `row[1].split(" — ")[1:-1]` means cell 2 must be **`<site> — <page title> — <url>`** (the shape of S421/S422). With a 2-part cell the extracted title is `""` and C5 fails `row title … is not the page's <title> text`. Corrected rows used here:
   - `百度搜索资源平台 — 搜索问答剧场 【五】“百度蜘蛛”全面解析 — https://ziyuan.baidu.com/college/articleinfo?id=3457`
   - `百度搜索资源平台 — 开发者如何解除封禁百度蜘蛛 — https://ziyuan.baidu.com/college/articleinfo?id=3028`
   Evaluated with the counter's own helpers (`parse_registry`, `row_url`, `units`, `in_content`, its anchor regex): both rows give `cells=11`, title equal to `<title>` before `_` (15 / 13 units), `row_url == ROW_URL`, `status=mined`, `opened=2026-10-26`, `recheck=180d`, scope/teaches ≥ 20 chars, no cell containing `|`, and anchors that satisfy the new-row rule: `§ 如何才能识别当前抓取是正确的百度蜘蛛 (发布日期：2022-08-19)` (18 units, page-unique, inside an article text node) and `§ 如何验证网站和智能小程序是否存在封禁百度蜘蛛的情况？ (发布日期：2020-07-23)` (25 units, page-unique, in a text node). The printed dates `发布日期：2022-08-19` / `发布日期：2020-07-23` are text nodes of the retained bodies (checked with `span_tools.py check`). The scope/teaches wording is my draft, advisory for the entry drafter.
3. **No duplicate-URL finding, and S421's shared host does not warn.** `W04` compares a normalized *full URL* (scheme stripped, host lowercased, trailing `/` and fragment dropped), never the host, so `articleinfo?id=3457/3028` vs S421's `id=3458` on `ziyuan.baidu.com` produces nothing. The base 14 `W04` lines are pre-existing (S033, S088, S092, S098, S099, S102, S110, S111, S115, S116, S117, S127, S416, S417) and are **unchanged** by the append — no new W of any class. `E04` is reachable on this URL within the same scope (control above), so the clean result is a real negative, not an unreachable check.
4. **The green depends on the entry files existing.** `E11` fires as soon as a used-by target is absent; the check is `[ -e ]`, so a zero-byte file (or a directory) at the path satisfies it. The census therefore proves the target *path exists*, not that the entry carries content — content truth is C1/C2/C5's job.
5. **`opened` acceptance is clock-dependent.** `validate_append.sh` passes no `--today`; the default is `date -u +%F`. Same mirror, `--today 2026-10-25` → two `E08`, exit 1. A host clock behind the round date fails an otherwise correct append; a clock ahead of it cannot fail one.
6. **Pre-existing registry nit (not this round's):** S056 (`queued`) carries used-by `-` (ASCII hyphen) where the sentinel is `—`. `usedby_findings` only inspects `mined` rows, so it is silent today; if S056 is mined, E11 fires on a literal path `-`.

## CROSS-LANE:

- `grep -l 'articleinfo?id=3457\|articleinfo?id=3028' /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md` → **no file matched** (rc=1) over the 21 lane registries present.
- Wider read-only sweep for `ziyuan\.baidu\.com/college/articleinfo?id=3457|3028` over every `*-shokunin/corpus/` and `/home/vgpnk/Projects/shokuknow`: the only hits are in shokuknow staging (kake round14 `SOURCES-PROPOSED.md`, `KNOWLEDGE-PROPOSED.md`, `CHANNELS.md`, `SEARCH-LOG.md`, scout/queue files) — the staged provenance of S395, not a lane registry.
- The only `college/articleinfo?id=…` URL in any lane registry fleet-wide is S421's `id=3458`, so a fleet `shared` run would not pair these URLs with another lane either. No collision risk for `sources-census.sh shared`.

## SCRIPT REVIEW:

`validate_append.sh` (round-58 copy of the round-57 block) does mirror what the census needs for the **current** registry:

- `--file` + no `--root` is the argv form C7 requires, and `cp -r corpus "$V/corpus"` covers every corpus-relative used-by target.
- The non-corpus targets are hardcoded as five files; extracting the registry's actual non-corpus used-by set gives exactly those five (`SCORECARD.md` 9 refs, `scripts/source_recheck.py` 5, `SKILL.md` 1, `.ufo/waves/round-41/oracle_crosscheck.py` 1, `.ufo/waves/round-41/c1_count.py` 1). My baseline run reproducing that layout was E-free, so the list is complete **today**.
- Evidence: `census-argv.txt` / `census-stdout.txt` / `census-stderr.txt` / `census-exit.txt` are written after the run, and the stdout ends in `file<TAB>ok<TAB><validated registry>`, which is the shape C7 accepts.

Gaps worth knowing (none changed by me; the script is a round-58 freeze artifact I did not modify):

1. **Working-tree mirror, no tracking check.** The mirror is `cp -r` of the working tree, so a used-by target that exists only as an untracked file satisfies E11. C7 later compares the scratch copy of the two adopted entries and the registry against the committed bytes, which closes this for S423/S424 and the registry; a *third* untracked used-by target would pass the census and not be covered by that comparison.
2. **The script's own exit status is `tail`'s (0)**, not the census's: `$ARGV > … ; echo "exit=$?"` records the census status only in `census-exit.txt`, and the last command is `tail -2`. A caller chaining on `validate_append.sh` sees success on a failing census; only re-reading the receipt exposes it.
3. **No `--today` pin** (finding 5): acceptance of `opened` depends on the host clock; the census also defaults `TODAY` to `date -u +%F` when run bare.
4. **No `set -e` / `pipefail`.** A failed `cp` of one of the five targets does not abort; it surfaces later as `E11` plus exit 1 (visible, but attributed to the row rather than to the mirror).
5. **The census proves existence, not content** (finding 4), so the mirror's zero-byte entries are indistinguishable from real entries at this gate — deliberate, given C1/C2/C5 check content.
6. `rm -rf "$V"` before each run means the receipt files are regenerated, not appended: a prior failing run leaves no record. That is outside C1's surface (`control(s)/` only), but it does mean the validate receipt is a "latest run only" record.

Nothing in the gaps blocks the append: with the five non-corpus targets, the whole-corpus mirror and the two entries present, the gate is exit 0 / 0 E / 14 W for the two new rows.

VERDICT: Census accepts the S423/S424 append — exit 0, 0 E, W list unchanged at 14, rows 160→162 — provided cell 2 is the three-part `site — title — url` form and both entry paths exist in the mirror; no lane registry anywhere in the fleet carries either URL.
