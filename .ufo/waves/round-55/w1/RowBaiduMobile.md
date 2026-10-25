# RowBaiduMobile

ROW:

```markdown
| Baidu mobile-matching correspondence errors | `knowledge/baidu-mobile-matching-error-causes.md` (S312) | Baidu's mobile-matching correspondence-error list: an ajax-loaded mobile body and a Baiduspider robots block, both quoted raw; the five-item list also names an unusable mobile page, a rule-pattern format error and a wrong PC-mobile mapping; no matching algorithm or threshold stated. |
```

EVIDENCE:

1. `corpus/knowledge/baidu-mobile-matching-error-causes.md:8-9` — the row's subject and "correspondence" framing rest on: "Baidu's mobile-matching tool manual lists the causes of a failed PC↔mobile correspondence" (12 units, raw substring of the file).
2. `corpus/knowledge/baidu-mobile-matching-error-causes.md:11` — "an ajax-loaded mobile body … quoted raw" rests on the file's quotation `"手机页使用了ajax等异步加载的方法加载内容主体"` (21 units; verified `in` the retained body `.ufo/waves/round-52/sources/S312.html`, sha256 `126c3da4e960916b3e5a…`, matching the file's own `sha256 126c3da4…`).
3. `corpus/knowledge/baidu-mobile-matching-error-causes.md:16` — "a Baiduspider robots block" rests on the head of that line's quotation, `"放开对Baiduspider的robots封禁"` (8 units; raw substring of the same retained body). The full line-16 quotation is 29 units, so only this head is quoted here.
4. `corpus/knowledge/baidu-mobile-matching-error-causes.md:19-22` — "the five-item list also names an unusable mobile page, a rule-pattern format error and a wrong PC-mobile mapping" rests on "The list names five causes in all: the mobile page is unusable (for example a" (15 units), "a format error in the submitted rule pattern," (8 units) and "and a wrong correspondence (for example a desktop content page mapped to a mobile home or list" (17 units), each a raw single-line substring. `:46` supports "no matching algorithm or threshold stated": "It does not state the matching algorithm, a pass threshold, or how long a resubmission takes" (16 units).

Row constraint checks run (python, read-only, on the file text): Coverage = 40 words (10-45); no `|` character; does not start with `TBD`; shares 5+-letter words with the H1/first 1500 chars (`mobile`, `correspondence`, `Baiduspider`, `matching`, `format`, `pattern`, `robots`, `quoted`, `unusable`, `wrong`, `names`, `error`, `block`, `baidu`). Entry cell path and `(S312)` are copied from the file's own `source:` line. Area is 4 words and carries no round tag, because the file's header (`:1-4`) holds no round tag. `grep -n "baidu\|Baidu" corpus/README.md` returns nothing, so no existing row is being duplicated.

RISKS:

- **Not the formal submission-failure list.** `:61` says the list "describes common correspondence errors; it is not the separate formal `校验失败` list of submission failures". The row therefore says "correspondence-error list" and must not be rewritten as a submission-verdict taxonomy.
- **Causation and exhaustiveness are unestablished by the file.** `:43-45` does not establish that Baiduspider executes the page's script; `:48-49` says the two quoted causes are not the whole list. The row names five items as the file states them and claims nothing about script execution, pass thresholds or reflection latency.
- **The file's own header locator is stale.** `:1` prints `§ 移动适配 → 对应关系错误的常见原因`; the string `对应关系错误的常见原因` is absent from the retained body (`in` check = False), while `如何提升移动适配效果` and `以下是常见的对应不准确错误` are each present once, exactly as `:61` corrects. A row must not repeat the superseded locator.
- **Internal contradiction on the date.** `:50` still says "The chapter prints 2020-08-14 as its timestamp", while `:61` says that string is the page-header `最新更新章节` marker, not a timestamp on the quoted section. Append-only text keeps both; the row carries no date claim.
- **Quote-length overrun inside the file.** The full line-16 quotation measures 29 units under the assignment's unit rule (one per CJK character, one per non-CJK whitespace token), above the 25-unit cap; line 11's is 21. Not edited — recorded for a quote-budget gate.
- **Item-5 compression.** The retained body's item 5 carries sub-cases the file's five-cause summary does not render (`手机页本身无主体内容或主体内容过少`, login-gated body, no one-to-one correspondence). The row cannot mention a login-gated body or thin body content, because the file does not.
- **Round-55 freshness not re-observed by this seat.** The entry's source is S312, retained at `.ufo/waves/round-52/sources/S312.html`; the round-55 retained set is S372/S373/S418 only, so this round re-fetched nothing for this entry and `verified-at: 2026-10-25` (`:2`) is the file's self-declaration. The round-53 re-read body `.ufo/waves/round-53/sources/S312-reread.html` has a different digest (`2b4d8116f42b7d6615…`) than the body the entry cites.
- **Placement is not this seat's call.** Only the table line is drafted; whether it joins the main `## Coverage map` table (`corpus/README.md:17`) or a round-tagged section is the planner's decision. No product file was edited; no git or jj state was touched.
- **Write-path correction (audit trail).** My first `write` used the lane-relative path and resolved against the workspace root, landing the bytes at `/home/vgpnk/Projects/shokunin/.ufo/waves/round-55/w1/RowBaiduMobile.md`. I copied those bytes to the lane path, removed the stray file and the two directories the write had created; `/home/vgpnk/Projects/shokunin/.ufo/waves/round-55` no longer exists (verified), and `git status --porcelain` in the lane shows 0 tracked modifications.

VERDICT: One coverage row drafted for `knowledge/baidu-mobile-matching-error-causes.md` (S312), all cells traceable to the file's own lines with row constraints machine-checked; three file-side defects (stale locator, date contradiction, 29-unit quotation) reported, unedited.
