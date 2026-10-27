# ReviewerEntryIdentification

Sentence-level fidelity review of `corpus/knowledge/baidu-spider-identification.md` at lane build c1e39ef3567542b2dc602cc235ed717d6dfbd915 (working tree verified identical: status/diff empty) against retained body `S423.html` (sha256 `8b8aef60…736ec` re-hashed, matches receipts.json HTTP 200 / 29007 bytes). Checks run: `span_tools.py check S423` on all 23 quoted spans + `【抓取篇】` (all: in_text_node True, count_in_body 1, unique True, within_ceilings True; every span 0 occurrences in S424; zero curly quotes in the entry); `span_tools.py window S423` read in full and term-scanned (渲染/脚本/JavaScript/JS/CSS/2017/日本/IP段: zero hits); UA strings measured per node; cross-links confirmed via `git ls-tree`/`git show` at the build; S423 registry row confirmed at `corpus/SOURCES.md:169`. Not run: live re-fetch (retained body only), any counter, w1 draft comparison. Reference: w1/ReviewerEntryFidelityPrep.md; must-not: w1/CriticEntryOverreach.md. Must-not list respected throughout (no render fetch/execute claim, no mobile-only render, no IP ranges, no *.baidu.jp-is-Japan, no robots timing, no UA-confirms, reverse+forward both carried, no QA7, no S409/2017, dates carried, `正常返回码是200` not quoted).

FINDINGS:

1. Line 49–50 — WRONG (numeric claim about the page).
   Entry: "The three channel blocks print the full strings verbatim, at 186 to 219 characters each".
   Page: the channel blocks print five strings measuring 186 (mobile Linux), 209 (mobile iPhone), 83 (PC `Baiduspider/2.0`), 90 (PC `Baiduspider-render/2.0`), 219 (Mini Program) characters — measured on the node-split window text. The two PC strings are far below the stated floor of 186.
   Fix: e.g. "at 83 to 219 characters each" or per-channel lengths. The conclusion ("far past this lane's quotation ceilings") survives — the shortest string is 83 > 40 — but the range as stated is false for 2 of 5 strings.

2. Line 149 — OVERREACH (unmarked inference attributed to the page).
   Entry: "…the page's second method exists because a string can be copied."
   Page: S423 nowhere states a rationale for 方式二; it only prints the two steps and the impostor verdicts. The copyability rationale is the entry's own inference, presented as fact about the page, in a section that is otherwise strictly about non-establishment.
   Fix: reword entry-side ("— consistent with a UA string being copyable") or mark [INFERENCE].

3. Line 147 — WRONG (minor, channel count).
   Entry: "It does not establish that the two UA strings per channel are exhaustive…".
   Page: the mobile and PC blocks each list two strings joined by 或, but the 小程序 block lists exactly one string (219 chars, the only line under 小程序UA：). Not two per channel.
   Fix: "the listed UA strings per channel".

4. Lines 39, 43 — DROPPED QUALIFIER (low; partially mitigated).
   Entry: "The page then fixes the channel split" / "(rendered: the UA is divided into mobile, PC)".
   Page: "目前 UA分为移动、PC、和小程序 三个应用场景" — 目前 ("currently") time-scopes the enumeration (reference trap 9: exhaustive only as of the 2022-08-19 printing). The hedge at lines 147–148 covers currency of the strings beyond that date, which blunts but does not restore the qualifier at the point of claim; "fixes" reads as permanent.
   Fix: "currently splits" / "at the 2022-08-19 printing, divides".

5. Lines 43–45 — MINOR (citation attachment).
   Entry: "…and the next node adds 小程序 (Mini Program) [S423]: > \"这三个渠道UA分别如下：\"".
   Page nodes: "、和小程序" (the node adding 小程序) and, next, "三个应用场景，这三个渠道UA分别如下：" — the quoted span is the second node and contains no 小程序. Every word of the entry's prose is supported, but the colon-plus-quote reads as if the quote evidenced the 小程序 addition, against the entry's own discipline (line 163–164) of keeping quote and node aligned.
   Fix: attach the quote to the "三个应用场景…" node explicitly, or describe the "、和小程序" node without quoting it.

6. Line 114 — DROPPED QUALIFIER (low, modal strength).
   Entry rendering: "(rendered: do not apply any block)" for "一定不要做任何封禁".
   Page/reference: 一定不要 = strong prohibition ("must not / by no means", reference marks 任何 = "any at all"); "do not apply any block" keeps the prohibition and the universal 任何 but drops the 一定 emphasis.
   Fix: "never apply any block" or "apply no block at all".

Everything else checked is supported. Specifically verified clean: title/`发布日期：2022-08-19`/fifth-episode claims (window; exact title in `corpus/SOURCES.md:169` at the build); four questions under `【抓取篇】` (count_in_body 1); purpose-not-capability and all render absence claims (term scan zero hits); UA-channel token sentence apart from Finding 1 (`Baiduspider/2.0` in mobile form 1 + PC form 1, `Baiduspider-render/2.0` in mobile form 2 + PC form 2 + Mini Program form, `Smartapp` appended only there); wrong-UA exclusion direction preserved ("直接判断为非…" rendered as exclusion, not confirmation); "publisher compares against" (查看UA信息 + 如果UA信息不对…); two-step DNS with strict binary verdicts and 可确认 modal kept; per-platform host/nslookup/dig renderings (windows+IBM OS/2, mac os as printed); "given as examples" (如…分别如下); Q3 conditional (一般会的 rendered "generally", condition = fresh material), reminder addressed to a site that wants crawling, log-check purpose clause; 封禁 left undefined with the pointer to `corpus/knowledge/baidu-spider-unblocking.md` and nothing quoted from 【封禁篇】; Q4 two candidate causes with epistemic "may", back-reference to Q2, 搜索资源平台-【抓取频次】工具 rendering, "no numbers" claim; all four cross-link glosses match the linked files' own source lines (crawler-identity=S263 Googlebot, robots-txt-rules=S011 RFC 9309, baidu-friendly-crawl-guidance=S329 ziyuan.baidu.com, js-rendering-queue=S137–139 Google rendering queue); quote-class section's byte/sha256/HTTP-200/ceilings/uniqueness claims all reproduced.

CLEAN LINES: 159 of 168 (flagged: 39, 43–45, 49–50, 114, 147, 149).

VERDICT: Ship-worthy with fixes — all 23 quotes and the must-not discipline verify clean against S423, but line 49's "186 to 219 characters each" is factually wrong for the PC strings (83/90) and lines 147/149 carry a channel-count slip and an unmarked page-rationale inference; three low dropped-qualifier/attachment nits.
