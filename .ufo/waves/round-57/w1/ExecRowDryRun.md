# ExecRowDryRun

Dry-run of the registry append mechanics for S421/S422, done entirely in a scratch dir
(`/tmp/r57-rowdryrun.PWHF9B`, created with `mktemp -d`; nothing outside it was written). The scratch mirrors what
`round-56/validate_append.sh` copies: the lane's whole `corpus/` tree, then the pre-append registry copied over
`corpus/SOURCES.md`, plus `SCORECARD.md`, `SKILL.md`, `scripts/source_recheck.py`,
`.ufo/waves/round-41/{c1_count.py,oracle_crosscheck.py}`, and two empty placeholder entries at the two used-by paths.
Base registry (pre-append mirror) = 158 rows; after the two rows = 160 rows.

## CANDIDATE ROWS:

Insert after the S420 row (line 166 of the pre-append mirror), still inside `## Registry`, one physical line each:

```
| S421 | 百度搜索资源平台 — 搜索问答剧场 【六】“死链”常见问题解析 — https://ziyuan.baidu.com/college/articleinfo?id=3458 | docs | A | **What the operator's own FAQ calls a dead link and what it asks a publisher to do about one** — the two kinds it splits dead links into (protocol and content), the five origins it lists, the site-level effect it warns of, and the status its submission tool accepts | § 一、了解死链 (发布日期 2022-09-09); 教你如何处理死链页面 for the submission steps and 使用【死链提交】工具的注意事项 for the tool limits | Baidu splits dead links into protocol dead links, whose TCP or HTTP status such as 403, 404 or 503 already marks the page dead, and content dead links, which answer with HTTP 200 and unrelated content such as deleted or permission-gated pages and cannot be set to 404; the page lists five origins, says a large number of dead links may affect the site's overall evaluation, and asks for a 404 page plus a dead-link file whose tool recognises only 404, allows no directory-level submission and takes 1-2 weeks | mined | 2026-10-25 | 180d | corpus/knowledge/baidu-dead-link-types.md |
| S422 | 百度搜索资源平台 — 百度搜索Spider3.0升级对站点有什么好处 — https://ziyuan.baidu.com/wiki/867 | docs | A | **What the Spider3.0 announcement says its new dead-link model recognises and how fast a submitted dead link clears** — the three dead-link kinds it names, the processing interval it claims, and its advice that a protocol dead link is the best choice; not a measured crawl outcome | § 百度搜索Spider3.0升级对站点有什么好处 (发布日期 2016-06-30); the 『死链处理更及时—被黑低质页面全屏蔽』 paragraph for the dead-link model | Spider3.0's new dead-link model recognises protocol dead links plus most content dead links and redirect dead links; the announcement says a dead link submitted through the webmaster platform used to clear very slowly, sometimes with a snapshot lingering for a while, but after the upgrade it clears in about a few days, and that a protocol dead link is the best choice when the best processing result is wanted; the page states no measurement of its own | mined | 2026-10-25 | 180d | corpus/knowledge/baidu-spider3-dead-link-model.md |
```

Derivation and checked facts (all verified, none inferred):

- Cell 2 shape copies S416/S417 on the same host: site name — page title — URL. Title = the `<title>` text minus the
  trailing channel-and-site suffix (`_搜索学堂_百度搜索资源平台` / `_搜索资讯_百度搜索资源平台`), exactly the suffix
  S416/S417 drop. Both titles are raw substrings of the retained bodies (`搜索问答剧场 【六】“死链”常见问题解析`
  occurs 3× in `S421.html`; `百度搜索Spider3.0升级对站点有什么好处` 2× in `S422.html`), which is what C5's
  `title in texts[sid]` needs. The S421 title carries the page's own curly quotes around 死链; the counter's curly-quote
  refusal scans lesson/entry lines only (`c57_quote_truth.py:396,416`), never registry cells, and C5 demands the printed
  title verbatim, so this is required. If the L1 prefers keeping `_搜索学堂` in the title it is also a raw substring
  (1×), but it departs from the S416/S417 convention.
- Anchor: the counter takes `row[5].split("§")[1].split(" (")[0]` as the heading and requires it raw, and requires
  `发布日期 <date>` in the cell while `发布日期：<date>` is printed in the body. `一、了解死链` occurs 1× in
  `S421.html` (`<h2>`); `发布日期：2022-09-09` 1×. `百度搜索Spider3.0升级对站点有什么好处` occurs 2× in `S422.html`
  (`<h1>`); `发布日期：2016-06-30` 1×. The S421 anchor's second clause names two section headings that are also raw
  (`教你如何处理死链页面`, `使用【死链提交】工具的注意事项`).
- Teaches grounding: S421 — 协议死链 vs 内容死链 (403/404/503; 200 with deleted/permission content, cannot be set to
  404), five origins (1)-(5), 可能影响网站整体评价, 设置404页面 + 死链文件, 仅识别404, 不支持目录级提交, 生效周期 1-2周.
  S422 — 全新的死链识别模型 recognising 协议死链 plus 大多数内容死链、跳转死链, clearing in 大约几天 after the
  upgrade, and 协议死链是最好的选择 for the best result. Both cells avoid the page's unverifiable numbers
  (500亿, 80%, 60%--100%) rather than restating them.
- Re-parsed with the counter's own helpers (`parse_registry`, `row_url`, `used_by`, `CURLY`): 11 cells each, no pipe and
  no escaped pipe in any cell, `row_url` returns exactly the contract URL, kind `docs`, tier `A`, status `mined`,
  opened `2026-10-25`, recheck `180d`, used-by a single exact path (C4 wants exactly one), scope 265/280 chars,
  teaches 508/454 chars (C3 floors: 11 cells, 20 chars on scope and teaches).

## CENSUS OUTPUT:

```
cd /tmp/r57-rowdryrun.PWHF9B
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /tmp/r57-rowdryrun.PWHF9B/corpus/SOURCES.md
exit=0
```

- 14 `W04` warnings, all pre-existing at base and identical before/after (S033 S088 S092 S098 S099 S102 S110 S111 S115
  S116 S117 S127 S416 S417 — duplicate URL across scopes); the append adds none. No `E` code of any kind, no W01/W02/W03.
- The same command over a copy of the pre-append mirror (`corpus/SOURCES-base.md`, same dir) also exits 0 and prints the
  same 14 `W04` lines (`diff` of the two W04 sets: identical), so the append introduces no warning either.
- Last non-empty stdout line (the form C7 requires): `file	ok	/tmp/r57-rowdryrun.PWHF9B/corpus/SOURCES.md`.
- `--file` makes the census resolve used-by paths from the parent of the `corpus/` dir (`resolve_targets` sets
  `dir=$(dirname file)/..`), so the scratch must hold the whole `corpus/` tree — a registry-only copy would raise E11 on
  every held row.

## MANUAL CENSUS:

Frozen commands from `/home/vgpnk/Projects/shokunin/CORPUS.md` § Census, run from the scratch root (`corpus/SOURCES.md`):

| command | base (pre-append) | after append |
|---|---|---|
| rows | 158 | 160 |
| malformed (NF!=13), must print 0 | 0 | 0 |
| tier histogram | A=135 B=6 C=17 | A=137 B=6 C=17 |
| status histogram | mined=128 queued=8 rejected=22 | mined=130 queued=8 rejected=22 |
| duplicate ids, must print nothing | (nothing) | (nothing) |
| enum violations / tier inflation, must print nothing | (nothing) | (nothing) |
| mined used-by paths missing, must print nothing | (nothing) | (nothing) |

The delta is exactly the two new rows, both tier A and mined, matching the contract's before/after (158 → 160).

## BREAKS:

Each break is a separate copy of the appended registry, broken inside `## Registry`, run with the same `--file` argv.

| break | what changed | exit | finding |
|---|---|---|---|
| duplicate id | an extra S421 row appended after S422, its URL changed to `?id=9999` so E04/W04 cannot confound | 1 | `file	E03	S421 duplicate id` |
| 10-cell row | S422 row reduced to 10 cells (recheck and used-by removed; NF=12) | 1 | `file	E01	S422 fields=10` |
| used-by path missing | S422 used-by → `corpus/knowledge/baidu-spider3-dead-link-model-missing.md` | 1 | `file	E11	S422 missing used-by corpus/knowledge/baidu-spider3-dead-link-model-missing.md` |

Each break emits that single code and nothing else (no cascade; the gawk `next`s after E01). Incidental finding from the
first attempt: a row appended after `## Paths` instead of after S420 yields `E12 <id> row outside Registry section`
(exit 1) — the insertion point is load-bearing, the section header resets `in_registry`.

## VALIDATE SCRIPT:

Save exactly this as `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-57/validate_append.sh` (18 lines):

```bash
#!/usr/bin/env bash
# Round-57 append-block validation (C3 rows, C7 census receipt). Re-run after ANY edit to corpus/SOURCES.md or the
# two adopted entries: mirrors the working-tree corpus/ (registry + entries included) into assimilation/validate/ and
# gates the append on `sources-census.sh validate --file <mirror registry>` (exit 0 required).
set -u
LANE=/home/vgpnk/Projects/shokunin/kake-shokunin
cd "$LANE" || exit 64
V=.ufo/waves/round-57/assimilation/validate
rm -rf "$V"; mkdir -p "$V"
cp -r corpus "$V/corpus"   # whole-corpus mirror: the census checks that every used-by path exists
for f in SCORECARD.md SKILL.md scripts/source_recheck.py .ufo/waves/round-41/c1_count.py .ufo/waves/round-41/oracle_crosscheck.py; do
  mkdir -p "$V/$(dirname "$f")"; cp "$f" "$V/$f"   # non-corpus used-by targets named by held rows
done
ARGV="/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $V/corpus/SOURCES.md"
printf '%s\n' "$ARGV" > "$V/census-argv.txt"
$ARGV > "$V/census-stdout.txt" 2> "$V/census-stderr.txt"
echo "exit=$?" > "$V/census-exit.txt"
cat "$V/census-exit.txt"; tail -2 "$V/census-stdout.txt"
```

Notes:

- An untracked file already exists at that path (not in the base revision). Its diff against this text is one line:
  line 2 reads `# Round-56 append-block validation (C7 receipts). …` there and the round-57 header above here. Its
  other deltas from `round-56/validate_append.sh` are the `two adopted entries` comment and `V=.ufo/waves/round-57/...`.
  Everything else in the mechanics is unchanged from round 56 on purpose: C7 consumes exactly
  `assimilation/validate/{census-argv.txt,census-stdout.txt,census-exit.txt,corpus/SOURCES.md}`.
- Mechanics proven in scratch: copied the text, changed only the `LANE=` line to the scratch dir (verified diff = that
  one line), ran it — script exit 0, `census-exit.txt` = `exit=0`, `census-argv.txt` =
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file .ufo/waves/round-57/assimilation/validate/corpus/SOURCES.md`
  (no `--root`), last stdout line `file	ok	<abs>/.ufo/waves/round-57/assimilation/validate/corpus/SOURCES.md`, mirrored
  registry byte-equal to the appended registry, both mirrored placeholder entries byte-equal to their sources.
  `bash -n` clean. The script was never run against the lane.

Risks / limits: the row titles and anchors are verified against the retained bodies in the lane's `sources/` only; the
teaches cells are paraphrase (no measurement claimed) and a critic must judge support, which no census does. The census
proves shape and path existence, not that the entries will carry quote-true spans.

VERDICT: append mechanics dry-run clean — 160 rows, census exit 0 with no E codes, all three deliberate breaks caught as E03/E01/E11, and the round-57 `validate_append.sh` text is ready to save (one header line from the untracked file already there).
