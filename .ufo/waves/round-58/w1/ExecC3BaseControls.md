# ExecC3BaseControls

Claim C3 controls, built before any data. Shared clone of the lane (`git clone -q --shared`) at
`/fast/scratch/hyaku/kake-r58/ExecC3BaseControls/freeze`; every control is one `selftest <selftest@local>` commit on a branch from
`fff3eea` (the contract commit, so the mirror add-commit is an ancestor and strictly earlier), scored with the frozen counter:

    python3 -B .ufo/waves/round-58/c58_quote_truth.py --root <clone> --revision <commit> --json

Each control carries a genuine census receipt: `corpus/` copied to `assimilation/validate/corpus/` plus the five non-corpus used-by
targets, `sources-census.sh validate --file <scratch registry>` run for real, exit 0 in every control (W04 only, no E03/E04) — the
lane census sees none of the junk. Nothing was written to the lane; fixtures, commits and scored revisions exist only in the clone
(revisions in `ExecC3BaseControls.files/manifest.tsv`, counter JSONs beside it). Base do-nothing control re-run at `0440485`: 0/8, exit 1.

## CONTROLS:

`conditions passed` lists the eight counter conditions; a control's `fail` set is where it was caught.

| control | what it skips | tally | passing conditions | caught by |
|---|---|---|---|---|
| base `0440485` | everything | 0/8, exit 1 | — | C1–C8 |
| scaffold | real observation; one-line prose, 3 real article spans per entry | 8/8, exit 0 | C1 C2 C3 C4 C5 C6 C7 C8 | not caught (valid minimum) |
| (a) a-nav | entries **and** Gate quotes made only of nav/sidebar text `搜索学堂`, `推荐阅读`, `百度蜘蛛` | 7/8, exit 1 | C1 C2 C3 C4 C6 C7 C8 | C5: `S423: entry line 9 quotes '搜索学堂'… which sits outside the page's content block`; `entry carries 0 page-unique quoted spans, expected 3+`; `no Gate quote carries the page-named subject 百度蜘蛛`; `Gate line carries no double-quoted located quote of 6+ units` |
| (b) b-title | entries **and** Gate quote the page `<title>` text only (S423 `搜索问答剧场 【五】“百度蜘蛛”全面解析`, S424 `开发者如何解除封禁百度蜘蛛`) | 7/8, exit 1 | C1 C2 C3 C4 C6 C7 C8 | C5: `Gate line uses curly double quotes; the declared form is ASCII` (S423); `a Gate quote occurs more than once in its own body … (not page-unique)`; `entry carries 0 page-unique quoted spans, expected 3+` (both) |
| (c) c-usedby | rows' used-by cells swapped between S423/S424 | 7/8, exit 1 | C1 C2 C3 C5 C6 C7 C8 | C4: `S423: used-by is ['corpus/knowledge/baidu-spider-unblocking.md'], expected ['corpus/knowledge/baidu-spider-identification.md']` |
| (d) d-root | validate receipt genuinely produced with `sources-census.sh validate --root <validate dir> <validate dir>` and labelled as such | 7/8, exit 1 | C1 C2 C3 C4 C5 C6 C8 | C7: `validation argv does not use --file`; `validation stdout does not end in file<TAB>ok<TAB><validated registry path>` |
| (d) d-mislabel | the same `--root` run, argv rewritten as `… validate --file <registry>` | 7/8, exit 1 | C1 C2 C3 C4 C5 C6 C8 | C7 on the payload only: the census labels `--file` runs `file`, a positional lane dir with the dir basename (`validate`), so a `--root` run cannot present the required tail |
| (e) e-promo | S423 entry **and** Gate quote only the page's trailing promo + related-link nodes | **8/8, exit 0** | C1 C2 C3 C4 C5 C6 C7 C8 | not caught — see H1 |
| (f) f-swap | entry bodies and Gate lines swapped between the two ids | 7/8, exit 1 | C1 C2 C3 C4 C6 C7 C8 | C5: `S423: entry line 9 quotes '…' which is not a raw substring of the retained body` (3 notes) |
| (h) h-mirror | pre-append mirror edited to carry the two new rows | 7/8, exit 1 | C1 C2 C3 C4 C5 C6 C7 | C8: `mirror bytes differ from the base-revision registry`; `S423/S424: the mirror bytes already carry the row`; `mirror sha256 8940dfb2… != pinned 57c83362…`; `mirror rows 162 != pinned 160`; `registry rows 162 != mirror rows 162 + 2` |
| (i) i-repeat | one span quoted three times ("3 unique spans" via repetition) | 7/8, exit 1 | C1 C2 C3 C4 C6 C7 C8 | C5: `entry carries 1 page-unique quoted spans, expected 3+`; `no page-unique span of the entry carries the page-named subject 百度蜘蛛` |
| (j) j-ceiling | one 30-unit span (S423) and one 186-character span (S424) | 7/8, exit 1 | C1 C2 C3 C4 C6 C7 C8 | C5: `entry line 11 quotes 30 units, ceiling 25`; `entry line 11 quotes 186 characters, character ceiling 40`; `entry carries 2 page-unique quoted spans, expected 3+` |

Conditions that pass on junk, per condition: **C1, C2, C3, C4, C6, C7, C8 pass on every junk fixture tested** (7/8 is the junk floor
whenever C5's structure is met); **C5 passes on junk in control (e)** and, trivially, on scaffolding whose entries are junk prose around
three real spans (scaffold). C2 accepts any header values; C6 is free because the receipts were frozen at the contract commit; C7 accepts
any recorded argv/stdout pair; C4 only compares a path string; C3 only row cells; C8 only mirror bytes and append-only equality.
`--selftest` is still the version-1 stub (exit 2), so no selftest class scored anything here.

## HOLES:

**H1 — must close before data. The S423 article window's tail is promo boilerplate, and it is worth 8/8.**
`content_window("S423")` = (9367, 14801); the end marker `往期回顾` sits at 14801, *after* the block the entry writer would call not-content:
the last real identification/unblocking claim ends at 14485 (`，需要查看防火墙配置系统后台，检查是否存在百度蜘蛛的IP级别封禁措施。`), then the page
carries the related-page link `《开发者如何解除封禁百度蜘蛛》` at 14612, the promo heading `——什么是【搜索问答剧场】？` at 14672 and the
platform blurb `定期为开发者运营过程中产生的疑惑问题进行梳理解答，` at 14750 — all in-window, all page-unique, all accepted. Control (e)
quotes exactly those three in the S423 entry and the first two in the S423 Gate line and scores 8/8 exit 0 (rev `c2a54f7c8b23`), i.e. an
entry with zero identification content is green; worse, the 13-unit related-link title carries `百度蜘蛛`, so it alone satisfies C5's
topic rule for entry and Gate. This is outside the contract's declared junk class ("sidebar/nav quotes outside the article block"): the
text is inside the crude window. Close by moving `ARTICLE_END["S423"]` to the promo/cross-link trailer (e.g. `——什么是【搜索问答剧场】` or the
`详情可参考` pair) and re-deriving the expected span set, or by requiring the topic-carrying span to precede the trailer. S424 is clean
(window 9352–11025, marker `推荐阅读` is the last node region, no promo inside); the fix is per-sid already.

**H2 — neither page's own heading can serve as the row anchor.** Both `<title>`/h1 texts occur 3× in the body (`搜索问答剧场 【五】“百度蜘蛛”全面解析`,
`开发者如何解除封禁百度蜘蛛`; measured `title count in body: 3` for each), so the anchor rule (4+ units, page-unique, inside an article text
node) rejects both. The scaffold and (e) pass only by anchoring on internal subheadings (`方式二：双向DNS解析认证`, `robots文件说明：`). Data seats
must know this before writing rows; the alternative is a variant of the uniqueness rule (unique within the window, not the body).

**H3 — `verify()` returns True for an out-of-block span, and C5 still counts it as page-unique.** `in_content` failure only appends a note;
`unique_spans.add(...)` does not consult it, so an entry can report "3 page-unique spans" with all three outside the block and still only
fail C5 through the separate note. No 8/8 escape was reachable (a-nav fails C5 on the note and on 0 unique spans, because nav strings are
also non-unique), but the facts and the 3-span floor are overstated. Close by returning False from `verify()` on the block test, or by
excluding such spans from `unique_spans`.

**H4 — seven of eight conditions are shape-only.** C1 existence, C2 header keys, C3 row cells, C4 path string, C6 (receipts pinned at the
contract commit), C7 recorded-run shape and C8 mirror bytes all pass on junk scaffolding; only C5 carries content, and its content floor is
three page-unique in-block spans per entry. A seat can therefore be green on everything except quote truth — which is the design, but the
L1 should read "7/8" as the junk floor, not as near-completion.

**H5 — C7 residual (not reachable without fabricating the payload).** The honest `--root` receipt fails twice: the argv token and the
payload label (`file` is emitted only in `--file` mode; a positional lane dir emits its basename). Residual exposure: `census-argv.txt`
and `census-stdout.txt` are free files, so a seat that ran `--root` can paste a `--file` run's stdout and pass; no shape check can tell.
Also the argv target test uses `endswith("/" + VALIDATE_REG)`, so a scratch tree outside the lane with that suffix is accepted — content is
still tied byte-equal to the landed registry and entries, so there is no content escape.

**Note (intended, not a hole):** the S423 page heading carries curly quotes, so control (b) also trips the ASCII-quote rule; and both
titles are non-unique, so a title-only entry can never reach 3 unique spans.

VERDICT: junk floor is 7/8; one junk class reaches 8/8 (S423 promo/related-link spans inside the crude article window) and the anchor rule rejects both page headings — close H1/H2 before data.
