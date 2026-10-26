# ScoutSpotcheckPrep

Read: `corpus/lessons/round-57.md` at `4b8c73050470ada9e6583f3b12d659d1bed6a17f` AND the working tree (HEAD `51921b9`; `git diff --stat 4b8c730 HEAD -- corpus scripts` is empty, so the lesson file is identical). `w1/ReviewerPlan.md`; the `w2/` reports present at run time. All commands below were run 2026-10-25 UTC from `/home/vgpnk/Projects/shokunin/kake-shokunin` (`R=.ufo/waves/round-57/sources`, scratch `D=$(mktemp -d)`, nothing written outside `D` and this file).

**Central fact (confirmed by reading):** `corpus/lessons/round-57.md` § Rejects is the placeholder `(filled after wave 2 re-reads each reason against the page)` at 4b8c730 and in the working tree. § Gate says "Rejected as staged (… see § Rejects below …)" and "rejects as logged in § Rejects", but logs none. The reject half of the spot-check set is therefore EMPTY until L1 fills it. The REJECT COMMANDS below cover the two candidates `w1/ReviewerPlan.md` § REJECT CANDIDATES proposes (the same two the W2 seats `ScoutRejectBaiduUA` / `ScoutRejectBaiduAgents` re-read). If L1 logs different rejects, the command shapes transfer, the rows do not.

## ADMIT COMMANDS:

Quotes (§ Gate, 4b8c730 lines 16/17): S421 `协议死链和内容死链` (9 units); S422 `能识别协议死链，以及大多数内容死链、跳转死链等低质网页` (25 units).

```
UA=spotcheck; D=$(mktemp -d); R=/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-57/sources
# A1 live GET (status, redirect, size) — S421 and S422
curl -sS -L --compressed --max-time 60 -A $UA -o $D/S421.html -w 'http=%{http_code} redirects=%{num_redirects}\n' 'https://ziyuan.baidu.com/college/articleinfo?id=3458'
curl -sS -L --compressed --max-time 60 -A $UA -o $D/S422.html -w 'http=%{http_code} redirects=%{num_redirects}\n' 'https://ziyuan.baidu.com/wiki/867'
# A2 recheck: grep -F -c of the Gate quote, live and retained
curl -fsSL --compressed -A $UA 'https://ziyuan.baidu.com/college/articleinfo?id=3458' | grep -F -c '协议死链和内容死链'
curl -fsSL --compressed -A $UA 'https://ziyuan.baidu.com/wiki/867' | grep -F -c '能识别协议死链，以及大多数内容死链、跳转死链等低质网页'
grep -F -c '协议死链和内容死链' $R/S421.html ; grep -F -c '能识别协议死链，以及大多数内容死链、跳转死链等低质网页' $R/S422.html
# A3 sha256: retained vs Gate pin vs live (whole body, then article window)
sha256sum $R/S421.html $R/S422.html            # Gate pins 32eaf8b7…7182 / 7cf2e27d…71ff
diff $R/S421.html $D/S421.html; diff $R/S422.html $D/S422.html   # expect only passport cdnversion / passreg port lines
python3 -B - <<'EOF'
import hashlib
for i in ("S421","S422"):
    f=lambda p:open(p,encoding="utf-8",newline="").read()
    def win(t): s=min(m for m in (t.find('class="article-info"'),t.find('class="zz_dldes_content')) if m>=0); return t[s:t.find('class="footer"')]
    a,b=win(f(f"{R}/{i}.html")),win(f(f"{D}/{i}.html")); print(i,"article window equal:",a==b,hashlib.sha256(a.encode()).hexdigest()[:16])
EOF
# (replace $R with the absolute .ufo/waves/round-57/sources path inside the python heredoc, or export R first)
# A4 span rules + section/date location
python3 -B .ufo/waves/round-57/span_tools.py check S421 '协议死链和内容死链'
python3 -B .ufo/waves/round-57/span_tools.py check S422 '能识别协议死链，以及大多数内容死链、跳转死链等低质网页'
grep -F -n -e '发布日期' $R/S421.html $R/S422.html | cut -c1-120
grep -F -o -e '<h2>一、了解死链</h2>' $R/S421.html ; grep -F -o -e '『死链处理更及时—被黑低质页面全屏蔽』' $R/S422.html
# A5 registry-row shape (committed rows) + census
git show 4b8c73050470ada9e6583f3b12d659d1bed6a17f:corpus/SOURCES.md | grep -E '^\| S42[12] ' | awk -F' \\| ' '{print NF": "$1" | "$3" | "$4" | "$6" | "$8" | "$9" | "$10" | "$11}'
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake; echo exit=$?
```

## REJECT COMMANDS:

Staged files live in `/home/vgpnk/Projects/shokuknow/merge/kake/knowledge/corpus/knowledge/` (read-only). Held retained bodies: `.ufo/waves/round-53/sources/S390.html`, `S409.html`.

**R1 — staged `baidu-render-crawl-ua.md` (cites S390, `https://ziyuan.baidu.com/wiki/990`).** Claim tested: its `source:` line says "the page prints no update stamp", locator `§ 公告正文（最新UA如下）`, text says "from 24 March 2017 Baidu started fetching … with a dedicated user agent". Deciding page sentences: stamp `发布日期：2017-03-24` printed in `<p class="info-item-time">`; body `从3月24日（2017）开始，百度搜索抽取了部分优质站点进行抓取内测，可能会对站点服务器造成一定压力影响，请尽量不要对UA进行封禁，以免造成不可逆转的损失。最新UA如下：`.
```
S=/home/vgpnk/Projects/shokuknow/merge/kake/knowledge/corpus/knowledge; N=.ufo/waves/round-53/sources
curl -sS -L --compressed -A $UA -o $D/S390.html -w 'http=%{http_code}\n' 'https://ziyuan.baidu.com/wiki/990'
for f in $N/S390.html $D/S390.html; do grep -F -c '发布日期：2017-03-24' $f; grep -F -c '公告正文' $f; grep -F -c '抽取了部分优质站点进行抓取内测' $f; done
grep -c '"' $S/baidu-render-crawl-ua.md                      # double-quoted spans in the staged entry
grep -n 'wiki/990' corpus/SOURCES.md | cut -c1-60            # row already held (S390)
```
**R2 — staged `baidu-render-and-crawl-agents.md` (cites S409 `wiki/1021`, S410 `wiki/963`).** Claims tested: locators `§ the article body's beta-and-rollout passage` / `§ the announcement's opening paragraph and the UA list below it`; "render agent is an accounted-for crawler"; reading "the agent that fetches JavaScript is one the operator asks publishers to allow". Deciding page sentence (S409): `内测期间分析了多个抓取量异常的case，均非渲染UA造成。本周百度Spider渲染UA在移动端全流量上线，PC端还未全部覆盖。特提醒PC站长，…对搜索引擎和用户有价值的内容，还是尽量不要使用JS加载的方式，以免造成不能索引等损失。` (the PC/JS warning is omitted by the staged text). S410: `近期发现部分网站出现抓取异常情况，主要问题是网站误封了百度UA。`
```
curl -sS -L --compressed -A $UA -o $D/S409.html -w 'http=%{http_code}\n' 'https://ziyuan.baidu.com/wiki/1021'
curl -sS -L --compressed -A $UA -o $D/S410.html -w 'http=%{http_code}\n' 'https://ziyuan.baidu.com/wiki/963'
grep -F -c '内测期间分析了多个抓取量异常的' $D/S409.html ; grep -F -c 'PC端还未全部覆盖' $D/S409.html ; grep -F -c '不要使用JS加载的方式' $D/S409.html
grep -F -c '近期发现部分网站出现抓取异常情况，主要问题是网站误封了百度UA。' $D/S410.html
grep -F -c -e "beta-and-rollout passage" -e "opening paragraph and the UA list" $D/S409.html $D/S410.html   # English locators
grep -c '"' $S/baidu-render-and-crawl-agents.md ; grep -c 'wiki/963' corpus/SOURCES.md ; grep -c 'wiki/1021' corpus/SOURCES.md
```

## OUTPUTS:

ADMITS (live GET 2026-10-25, UA `kake-shokunin-round57-w2-spotcheck`):
- A1: S421 `http=200 redirects=0` (10,542 transfer bytes, 34,750 decoded); S422 `http=200 redirects=0` (27,327 decoded). Confirmed by running.
- A2: live `grep -F -c` → S421 `1`, S422 `1`; retained → `1`, `1`; `grep -F -o | wc -l` also `1`/`1`.
- A3: retained sha256 `32eaf8b74012c99dff8ae6cc3db0658d3f7520b04045336b8228461dab447182` / `7cf2e27dc7e6dcba4e7bbeba09ed6f23a7c6322dc2a377e3cd36dee8c1de71ff` = Gate pins = `receipts.json`. Live sha256 DIFFERS (S421 `8021374c…3921`, S422 `9b8279fc…e03c`): `diff` shows only `passport.baidu.com/…?cdnversion=` lines 346-347 (S421) and 318-319 + `passreg … %3A8186%2F` line 333 (S422), all inside `<script>`. Article windows (`article-info`/`zz_dldes_content` → `footer`) are byte-equal: S421 12,482 chars `f905eedc…`, S422 3,814 chars `a4d6bbe5…`. A naive whole-body sha compare will "fail" every time; the pin proves the retained file only.
- A4: `span_tools check` → S421 `units 9, raw_substring True, in_content True, count_in_page 1`; S422 `units 25, raw True, in_content True, count 1, in_other_adopted_body False`. Dates: `发布日期：2022-09-09` (line 273) / `发布日期：2016-06-30` (line 274). S421 quote sits at offset 10340 inside `<span><b>协议死链和内容死链</b></span>` in the answer `A：死链一般是指…包括协议死链和内容死链。` under `<h3>1、死链都有哪些类型？</h3>`, which is under `<h2>一、了解死链</h2>` (offset 10037) — the Gate's § is the `h2`. S422 quote is in the paragraph `在死链处理方面，Spider3.0启用了全新的死链识别模型，能识别协议死链，以及大多数内容死链、跳转死链等低质网页，…`, whose label is a plain `<p><span>『死链处理更及时—被黑低质页面全屏蔽』` (not an `h*` tag).
- A5: both rows 11 cells; S421 `type docs, tier A, anchor § 一、了解死链 (发布日期 2022-09-09), mined, 2026-10-25, 180d, corpus/knowledge/baidu-dead-link-types.md`; S422 `§ 死链处理更及时—被黑低质页面全屏蔽 (发布日期 2016-06-30), mined, 2026-10-25, 180d, corpus/knowledge/baidu-spider3-dead-link-model.md`; cell 2 URLs equal the Gate URLs; registry rows 160 (last ids S420,S421,S422). Census `validate --root … kake`: exit 0, 0 E-codes (W04 only for S416/S417 pre-existing). (Census via `--file` on a scratch extract gives E11 noise because non-corpus `used-by` targets are absent — use `--root`.)

REJECTS (live GET same day):
- R1: S390 live `http=200`, retained round-53 body sha `a8f9ae70…1506` (22,141 B), live sha `467697c6…9655` (22,141 B bytes; hashes differ, content not diffed — [INFERENCE] same cache-buster class). On both retained and live: `发布日期：2017-03-24` → 1, `公告正文` → **0**, `最新UA如下` → 1, `从3月24日（2017）开始` → 1, `抽取了部分优质站点进行抓取内测` → 1. Staged entry: `grep -c '"'` → 0 quoted spans. `grep -n 'wiki/990' corpus/SOURCES.md` → row S390 line 160 (held; staged row would duplicate it). So the staged "page prints no update stamp" and `§ 公告正文` locator are false (confirmed by running); staged text "Baidu started fetching … from 24 March 2017" drops the page's scope "抽取了部分优质站点进行抓取内测" (a beta on a sampled set of sites; `会全面启用` is a future).
- R2: S409 live 200 (56,621 B, retained 56,621 B), S410 live 200 (22,581 B). S409: `内测期间分析了多个抓取量异常的` 1, `发布日期：2017-06-07`; the `PC端还未全部覆盖` / JS warning sentence present (`…尽量不要使用JS加载的方式，以免造成不能索引等损失`) and absent from the staged text. S410: `近期发现部分网站出现抓取异常情况，主要问题是网站误封了百度UA。` 1, `发布日期：2017-02-16`, `手百` 1. Both English locators: 0 hits. Staged entry quoted spans 0. `wiki/963` in `corpus/SOURCES.md`: 0 rows (S410 not held; a new row would be needed); `wiki/1021`: 1 (S409 held).
- Side finding (confirmed by running): `ReviewerPlan.md` byte counts for the retained/live pages are stale (it says S390 20,626 / S409 55,152 / wiki/963 21,258; measured 22,141 / 56,621 / 22,581). Not a gate fact; fix before any lesson text copies them.

## WEAKEST DECISIONS:

1. **The rejects (weakest by absence).** The lesson logs zero rejects at 4b8c730 and HEAD; LEARNING.md requires ≥1 admit and ≥1 reject and a spot-check that "agrees … on admits *and* rejects". A closure reader has nothing to re-open until § Rejects is filled; the Gate even points at it ("as logged in § Rejects"). `[INFERENCE]` L1 intends to fill it from W2.
2. **R2 (S409/S410 agents) if logged.** Most of the staged claims are page-supported (anomalies "均非渲染UA造成", UA strings, 手百 form). The reject rests on form (0 quotes, English non-heading locators), one omission (PC not yet covered / avoid JS loading), and bridging claims (render agent "one the operator asks publishers to allow"). A closure could call the omission a QUALITY nit fixable by amendment rather than a reject, and note the same English-locator defect already sits in held row S409 (so it is not disqualifying by lane precedent). Also the reject splits across two rows (S409 held, S410 unheld), so the flip condition is mixed.
3. **R1 (S390 UA).** The false "no stamp" claim and non-existent `公告正文` locator are hard, run-verified defects, but the core claims (fetches CSS/JS/images, `Baiduspider-render/2.0`, do-not-block) are page-supported and the row is already held; a closure could argue "admit as amendment to held S390" instead of reject. Strongest reject of the three, still debatable on reject-vs-amend.
4. **S422 admit.** 25 units is exactly at the ceiling; the "section" is a bracketed `『…』` paragraph label, not a heading tag, and the row anchor drops the brackets; the page is a 2016 announcement; the quote supports "recognises dead links" only — scope claims about the 10-day / 40-80% figure and the processing time live elsewhere in the entry. The entry's own recheck says the curl arm was unrun at write time (the retained-body grep printed 1); this scout ran the curl arm: 1.
5. **S421 admit.** The 9-unit quote is a bare noun phrase inside a Q&A answer under `h3` `1、死链都有哪些类型？`, but the Gate cites the broader `h2` `§ 一、了解死链`; a pedantic closure could want the `h3` locator. The quote proves "two kinds named", not the entry's headline "content kind answers 200" (separate quotes in the entry, not part of the Gate pin).
6. **sha256 comparison.** Live whole-body hashes never match the pins (script cache-busters); a reader following only the Gate's sha line will think the page changed. Closure instructions must use the article-window hash or `diff`.

VERDICT: Admits S421/S422 re-open clean (live 200, grep -F -c = 1/1, article window byte-equal, rows 11-cell, census exit 0) but § Rejects is empty at 4b8c730 and HEAD, so the reject half of the spot-check has no logged decisions; commands and decisive page sentences for the two planned rejects (S390 UA, S409/S410 agents) are run and ready, with reject-vs-amend the likeliest closure disagreement.
