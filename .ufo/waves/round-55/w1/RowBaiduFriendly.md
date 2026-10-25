# RowBaiduFriendly

Claim C1 (coverage-map calibration). Read `corpus/knowledge/baidu-friendly-crawl-guidance.md` in full
(70 lines) and `corpus/README.md` §Coverage map (lines 15–45, header + rows 1–21). No file was edited;
this report is the only path written. No pacman transaction, no git/jj write, no tool install.

ROW:
```markdown
| Baiduspider robots scope, wildcards and spider trap | `knowledge/baidu-friendly-crawl-guidance.md` (S329) | Baiduspider robots scope: a block on that agent binds the desktop and mobile crawlers; wildcard symbols `*` and `$`; the spider trap as a parameter-generated URL space with a robots remedy. |
```

Row self-checks run against the candidate line (read-only, python): Area = 7 words; Coverage = 31
whitespace tokens (10–45); no `|` in Coverage; does not start with `TBD`; shares 14 five-plus-letter
words with the file's H1 + first 1500 characters (`baiduspider, robots, scope, block, binds, agent,
desktop, mobile, crawlers, wildcard, symbols, parameter-generated, space, remedy`). Under
`c55_readme_index.py` semantics the row is non-thin and its Entry token resolves under `corpus/`.
The file is named by no existing coverage-map row (grep over `corpus/README.md`: 0 hits), so the row is
new, not a duplicate.

EVIDENCE:
- `corpus/knowledge/baidu-friendly-crawl-guidance.md:6` — H1: "A Baiduspider robots block binds the desktop and mobile crawlers at once" (12 whitespace tokens). Grounds the Area phrase and the Coverage clause "a block on that agent binds the desktop and mobile crawlers".
- `:11` — `"如果封禁的agent是Baiduspider，会对PC和移动同时生效"` (18 units). Verified raw substring of the retained body `.ufo/waves/round-52/sources/S329.html` (sha256 `452aabc38f47…`) at byte 11503, under heading `如何正确识别Baiduspider移动ua` (anchor `h2_article_title15`). Grounds "a block on that agent binds".
- `:17`, `:19-20` — `"支持使用通配符"` (7 units; raw at byte 19415, under heading `robots写法`, anchor `h2_article_title18`), with the page's list naming `*` and `$` on lines 19–20. Grounds "wildcard symbols `*` and `$`".
- `:25`, `:29` — `"蜘蛛黑洞特指网站通过极低的成本制造出大量参数过多"` (24 units; raw at byte 22012, under heading `使用robots巧妙避免蜘蛛黑洞`, anchor `h2_article_title21`), and line 29's remedy sentence (`robots.txt` rule over the generated space). Grounds "the spider trap as a parameter-generated URL space with a robots remedy".

Quote verification ran twice: python `in` on the body and `grep -cF` (1 hit each). Unit counts use the
wave rule (one per CJK character, one per non-CJK whitespace token).

RISKS:
- **Stale header line in the file.** `source:` (line 1) still says "(no revision printed on the page — …)", but the round-53 append at line 68 withdraws that and reports the page header `最新更新章节：2019-09-18`. The row therefore states no revision date; do not add one from line 1 or line 68 without resolving the contradiction.
- **The revision date is not one raw run.** In the retained body `最新更新章节：` sits at byte 9736 and the date is inside a following `<span class="time">2019-09-18</span>`; the backticked string in the correction is rendered text, so it cannot be quoted as a raw substring under the 25-unit/raw-substring rule.
- **The file's own third quotation is over the ceiling.** `"蜘蛛黑洞特指网站通过极低的成本制造出大量参数过多、内容类同但"` measures 30 units under the wave rule (>25). The row quotes nothing and EVIDENCE uses the 24-unit prefix; noted as an observation on the file, not a claim that the file is defective (the contract ceiling is scoped to new material).
- **Locator supersession.** The PC/mobile clause's line-1 locator (§ 友好抓取 → robots写法 / 使用robots巧妙避免蜘蛛黑洞) is superseded for that clause by the correction: the clause sits under `如何正确识别Baiduspider移动ua` — confirmed in S329 itself (anchor 15). The wildcard and trap quotes sit under the other two headings. A row carrying a single section locator would overreach, so the row carries none.
- **S416 body unverified here.** The correction names S416 as the superseding locator source; no `S416.html` exists in this lane's wave source trees (find over the lane: 0 hits), so that page's body was not re-checked in this seat.
- **Limits the row must not imply** (file lines 47–56): it does not establish that Baiduspider executes script, a crawl-rate limit or per-host budget, how long a blocked object stays unfetched after the block lifts, or other operators' wildcard support. The row attributes wildcards to this page/agent only and says nothing about rendering or budgets.
- **Compression in the H1.** "desktop and mobile crawlers" compresses `PC和移动`; the row keeps the file's own compression and does not generalise to all Baidu user agents (the quote is about the `Baiduspider` agent token).
- **Age.** Page header is 2019-09-18, fetched 2026-10-25, `recheck: 180d`; the content is 2019 course text. The row states no dates, so it makes no freshness claim either way.

VERDICT: One new coverage-map row drafted and self-checked for the C1 counter's non-thin/non-dangling rules, with every clause traced to verified file lines and raw source substrings; no file edited.
