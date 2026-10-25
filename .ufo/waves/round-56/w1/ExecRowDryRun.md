# ExecRowDryRun

Scope: dry-run the registry append mechanics for round 56 before the three entries exist. Nothing in the lane was
written except this report. Scratch root `$S=/tmp/execrowdryrun.P5G7N5` (mktemp -d); no git, jj or index operation
anywhere.

Mirror built exactly as `validate_append.sh` does, from the pre-append source of truth:
- `$S/corpus/SOURCES.md` <- `.ufo/waves/round-56/assimilation/pre-append/corpus/SOURCES.md` (verified byte-identical
  to the lane working-tree `corpus/SOURCES.md`, 271 lines, 156 registry rows).
- rest of `corpus/` <- lane `corpus/` (145 files, same count as the lane corpus).
- `SCORECARD.md`, `SKILL.md`, `scripts/source_recheck.py`, `.ufo/waves/round-41/c1_count.py`,
  `.ufo/waves/round-41/oracle_crosscheck.py` copied with their relative dirs, per the loop in `validate_append.sh`.
- three placeholder files created at the used-by paths inside `$S` only:
  `corpus/knowledge/yahoo-japan-link-target-crawl-restriction.md`,
  `corpus/knowledge/yahoo-japan-deleted-url-recrawl.md`,
  `corpus/knowledge/yahoo-japan-nonexistent-url-recrawl.md` (each a one-line dry-run placeholder, not an entry draft).

Pre-checks: pages 002856 / 002857 appear 0 times in the pre-append registry (no E04 risk); all three used-by paths
are absent from the lane tree, so the placeholders are load-bearing for E11.

## CANDIDATE ROWS:

Appended after the last registry row (S418, line 164), inside `## Registry`, before the blank line that precedes
`## Paths` (so no E12). Both rows are NF=13 (11 cells, no pipe inside any cell).

```
| S419 | Yahoo!検索 インフォセンター — 削除したウェブページが巡回され続ける — https://info-search.yahoo.co.jp/archives/002856.php | docs | A | **What keeps a deleted page in the crawl** — the operator's own account of a deleted URL still being crawled when the server answers HTTP 200 for it, and the two remedies it names: a 404 status, or an index-refusal meta tag on the error page | § 削除したウェブページが巡回され続ける (h1), body paragraphs 1–3 (更新日 2010年11月24日) | a server that answers HTTP 200 for a deleted URL keeps the crawler from recognizing the deletion, so it may keep crawling that page; the page's remedy is to answer 404 Not Found, and where that cannot be set, to refuse index registration with a meta tag in the error page's head | mined | 2026-10-25 | 180d | corpus/knowledge/yahoo-japan-deleted-url-recrawl.md |
| S420 | Yahoo!検索 インフォセンター — 存在しないウェブページが巡回される — https://info-search.yahoo.co.jp/archives/002857.php | docs | A | **Why a non-existent URL keeps being crawled** — the operator's own account of an error page served with HTTP 200 for a URL that does not exist, which the crawler does not treat as an error page, and the two remedies it names: a 404 status, or an index-refusal meta tag | § 存在しないウェブページが巡回される (h1), body paragraphs 1–2 (更新日 2010年11月24日) | serving an error page as HTTP 200 for a URL that does not exist means the crawler does not treat it as an error page and keeps crawling; the remedy is to answer 404 Not Found, and where that cannot be set, to refuse indexing with a meta tag in the error page's head | mined | 2026-10-25 | 180d | corpus/knowledge/yahoo-japan-nonexistent-url-recrawl.md |
```

S367 used-by extension (cell 12 only; cells 2–11 compared field-by-field, 10/10 identical to base):

```
base used-by: corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md
new  used-by: corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md, corpus/knowledge/yahoo-japan-link-target-crawl-restriction.md
```

Grounding for the `teaches` cells, all checked with `span_tools.py check` against the retained bodies (raw substring,
inside the article window, page-unique, not in another adopted body):

| page | span | units | page-unique |
|---|---|---|---|
| S419 | `削除したURLのウェブページにアクセスしたときに「HTTP 200 OK」` | 23 | yes |
| S419 | `削除されたウェブページと認識できず、` | 17 | yes |
| S419 | `そのウェブページを巡回し続ける可能性があります` | 23 | yes |
| S419 | `設定されているかを確認してください` (the 404 remedy clause; the full sentence is 36u) | 17 | yes |
| S419 | `メタタグを使ったインデックスへの登録拒否の設定` | 23 | yes |
| S420 | `存在しないウェブページを表示しようとしたときに、` | 23 | yes |
| S420 | `サーバーが「HTTP 200 OK」` | 7 | yes |
| S420 | `クローラーはエラーページとみなさず、` | 17 | yes |
| S420 | `巡回を続けます` | 7 | yes |
| S420 | `存在しないウェブページを表示しようとしたときには、` | 24 | yes |
| S420 | `のステータスを返すように設定を行ってください` | 22 | yes |
| S420 | `メタタグを使ったインデックス拒否の設定` | 19 | yes |

Rejected as over-ceiling or non-unique (recorded so the entry seats do not retry them): S419
`メタタグを使ったインデックスへの登録拒否の設定を行ってください` = 31u; S420
`メタタグを使ったインデックス拒否の設定を行ってください` = 27u; `「HTTP 404 Not Found」` = 4u but occurs in both
S419 and S420 (not page-unique). `エラーページのHTMLの<head>に、` is not a raw substring (the body writes `&lt;head&gt;`).

## CENSUS OUTPUT:

Command (as `validate_append.sh` builds it, `--file` form; with `--file` the script resolves E11 against the parent
of `corpus/`, i.e. `$S`):

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /tmp/execrowdryrun.P5G7N5/corpus/SOURCES.md
```

exit=0. Findings, all warnings, none about this round's rows:

```
file	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
file	W04	S088 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
file	W04	S092 duplicate url html.spec.whatwg.org/multipage/syntax.html across scopes
file	W04	S098 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
file	W04	S099 duplicate url www.rfc-editor.org/rfc/rfc9309.html across scopes
file	W04	S102 duplicate url www.sitemaps.org/protocol.html across scopes
file	W04	S110 duplicate url www.w3.org/TR/xml across scopes
file	W04	S111 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
file	W04	S115 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
file	W04	S116 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
file	W04	S117 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
file	W04	S127 duplicate url www.rfc-editor.org/rfc/rfc9844.txt across scopes
file	W04	S416 duplicate url ziyuan.baidu.com/college/courseinfo?id=1399 across scopes
file	W04	S417 duplicate url ziyuan.baidu.com/college/courseinfo?id=267&page=15 across scopes
file	ok	/tmp/execrowdryrun.P5G7N5/corpus/SOURCES.md
```

14 W04 warnings, all pre-existing held rows (S033…S417); zero E01–E12; stderr empty. No S419/S420 finding of any
code, so the append adds no warning and no error.

## MANUAL CENSUS:

The frozen awk block from `/home/vgpnk/Projects/shokunin/CORPUS.md` § Census, run with cwd=`$S` (column-zero input,
as the frozen examples assume):

| check | command output |
|---|---|
| rows | `158` (156 base + 2) |
| malformed rows (NF!=13) | `0` |
| tier histogram | `A=135 B=6 C=17` |
| status histogram | `mined=128 queued=8 rejected=22` |
| duplicate ids | empty |
| enum violations / tier inflation | empty |
| mined used-by paths missing on disk | empty |

Both new rows report NF=13 under `awk -F'|'`, i.e. no stray pipe in any cell; the two `mined` counts and the `A`
count each moved by exactly 2, and `rows` by exactly 2 — the append is additive and nothing else moved.

## BREAKS:

Three copies of the full mirror (`b1`, `b2`, `b3`, each with `corpus/`, `SCORECARD.md`, `SKILL.md`, `scripts/`,
`.ufo/`), one deliberate defect each, validated with the same `--file` argv shape:

| break | mutation | census exit | finding code | finding line | manual awk |
|---|---|---|---|---|---|
| b1 | S420's id rewritten to `S419` (duplicate id) | `1` | `E03` | `file	E03	S419 duplicate id` | dup ids: `S419` |
| b2 | S419's `recheck` cell deleted (10 cells) | `1` | `E01` | `file	E01	S419 fields=10` | malformed: `1` |
| b3 | S420's used-by pointed at `…nonexistent-url-recrawl-MISSING.md` | `1` | `E11` | `file	E11	S420 missing used-by corpus/knowledge/yahoo-japan-nonexistent-url-recrawl-MISSING.md` | missing: `corpus/knowledge/yahoo-japan-nonexistent-url-recrawl-MISSING.md` |

Each break produced exactly one E finding (plus the same 14 pre-existing W04 lines) and exit 1; stderr empty in all
three. So the gate is live on all three mechanics the append depends on: id uniqueness, 11-cell width, and used-by
path existence.

Residual risk the dry-run does not cover (for the entry/integration seats): the real run mirrors the lane's working
`corpus/`, where the three entry files must exist as real entries before `validate_append.sh` exits 0; and E04 would
fire if either URL were re-appended under a second row with the same scope.

Tooling: nothing installed or upgraded this seat. No credential material, session tokens, `op://` refs or private
URLs in this report.

VERDICT: append mechanics dry-run clean — 158 rows, census exit 0 with only 14 pre-existing W04 warnings, manual census empty on all five checks, and the three deliberate breaks each caught (duplicate id -> E03/exit 1, 10-cell row -> E01/exit 1, missing used-by -> E11/exit 1).
