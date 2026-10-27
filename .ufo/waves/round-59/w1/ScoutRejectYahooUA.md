# ScoutRejectYahooUA

Question: screen staged `yahoo-crawler-ua-carrier-survey.md` (row S394, `merge/kake/SOURCES.append.md:114`) as a second crawler-identity candidate. All fetches 2026-10-27T01:46Z, GET only, `curl -L --compressed`, no auth. Bodies were kept in the seat scratch and removed at exit.

## SOURCES:
S394 is an own-work row, not a URL. Its cite is `lanes/kake/round13/.evidence/ua_carrier_sweep_r13.txt`, which sits at `/home/vgpnk/Projects/shokuknow/lanes/kake/round13/.evidence/`. The `.txt` and its `.sh` exist there. They are not in the lane repo (no `lanes/` dir in kake-shokunin) and are not in the lane registry (`corpus/SOURCES.md` holds no S394, S364, S368, S350 or S386). The entry quotes no page text; it reports counts. The five surfaces the sweep names were re-fetched:

| surface | http | bytes / CJK now | recorded in sweep | quote found? |
|---|---|---|---|---|
| support.yahoo-net.jp/PccSearch/s/article/H000007955 | 200 | 22,864 / 57 | 22,866 / 57 | the shell has zero `ユーザーエージェント`, zero `クローラー`, zero `Y!J-`; `<noscript>` JS-required notice. Count matches within 2 bytes. |
| support.yahoo-net.jp/SccSearch/s/article/H000007955 | 200 | 23,792 / 57 | 23,792 / 57 | same, exact match |
| ads-help.yahoo-net.jp/s/article/H000044807?language=ja | 200 | **102,822 / 8** | **436,802 / 268** | zero `クローラー`. **Drifted:** the body is about a quarter of the recorded size and its title is `LINEヤフー広告 ヘルプ`. The recheck cannot reproduce 436,802 or 268 today. |
| info-search.yahoo.co.jp/archives/002855.php | 200 | 8,703 / 1,002 | 8,703 / 1,002 | exact. Server-rendered, sha256 `9ce5a4ab…`. UA-token 6, `クローラー` 14. |
| info-search.yahoo.co.jp/crawl/ | 200 | 9,299 / 1,194 | 9,299 / 1,194 | exact. sha256 `498d36db…`. |
| help.yahoo.co.jp/help/jp/search/indexing/indexing-27.html | none | curl exit 6, host does not resolve | "curl exit 000" | consistent, still dead |

Verbatim operator sentences that DO exist (no whitespace in Japanese, so each is one whitespace token and the S425/S426 6..25-token rule cannot count it; a CJK-ceiling route is needed):
- 002855: `サーバーでクローラーのアクセス制限を行う場合には、IPアドレスによるアクセス制限ではなく、前述のDNSを参照したアクセス制限をおすすめします。` (1 hit, 71 characters). Also `ユーザーエージェント名を偽装するようなクローラーは、robots.txtなどの記述に従いません。` (1 hit).
- 002855 steps `nslookup {IPアドレス}` -> the domain is shown, and `nslookup {ドメイン}` -> the IP address is shown (1 hit each). This is a two-way lookup mechanism, which the round-55 S386 reject said the index page lacks.
- `/crawl/` index: `…このページに記載されているドメインネームサーバー（DNS）を使ったアクセス制限をおすすめします。` (1 hit).
- The entry's own headline phrase `the names remain a client-rendered surface only` is in the `.txt` (count 1). The entry quotes no operator page.

## Findings
1. **The load-bearing claim rests on a page the lane does not hold.** The entry's "the operator's own answer is a DNS lookup" comes from 002855 and `/crawl/` (staged S350 and S386). The entry cites only S394, an own-work count file. The lane has no row for either page. Round 55 rejected staged S386 for exactly this (`corpus/lessons/round-55.md:36-39`; flip: adopt 002855 as a lane row, cite it).
2. **The registry flip was already named and not met.** Round 55 rejected S364 as "client-rendered body, only chrome quotable" (flip: restate as a pinned measurement, or re-ground on the server-rendered 002855). Round 58 excluded id=2855 as "no entry rests on it" (`corpus/lessons/round-58.md:104`). S394 is a pinned measurement of the same shell, with no 002855 row.
3. **The recheck is not a recheck.** `ua_carrier_sweep_r13.sh` fetches nothing. It reads files already in `.evidence/`, so the printed counts are cached bytes. The stated recheck (`bash … && grep -F -c 'the names remain a client-rendered surface only'` -> 1) greps the string the script itself echoes into the file. It would print 1 whatever the live pages serve. Live today, the ads page has drifted (436,802 -> 102,822 bytes).
4. **The `.sh` contradicts the entry.** The script labels the ads page (268 CJK) `server-rendered text`, and its own threshold is cjk>=200. The entry calls the same page "a page shell". The entry also cites the 268 count as a shell figure. That figure no longer reproduces.
5. **Unmarked inference.** "The names exist, on a surface that renders them — closing this needs one headless-browser fetch" is unobserved: no render was run, and the shell's body holds zero names. A headless fetch would also be tabi's adjacent province (PROVINCE.md Adjacent: browser-driving belongs to tabi). "Three rounds searched" is a lane-history claim with no cite.
6. **No operator-page quote.** An entry whose only source is own-work cannot carry the quote-truth rule (page-substring quotes). Registry precedent: own-work rows exist (S014, S019) only for lane scripts, and S394's evidence file is outside the lane.

## PROVINCE fit
Publisher-side verification of who fetches a property is in scope (round 58 admitted S423/S424 on that basis; `PROVINCE.md` Frontier "crawl hygiene per host" and crawler identity). A Yahoo! JAPAN crawler-identity entry fits, but only when grounded on the operator's own page 002855. This entry grounds on a measurement of unreachable names, not on what the operator says. The "lane's existing Yahoo! JAPAN entries" are seven: `yahoo-japan-{deleted-url-recrawl, link-target-crawl-restriction, nonexistent-url-recrawl, rel-nofollow-semantics, robots-pattern-syntax, robots-txt-basics, robots-txt-refusal-rules}.md`. None covers crawler identity. The 002855 DNS content is not duplicated, so a re-grounded entry would add ground. The staged S378 (ads FTP crawler) was refused on scope in round 58 and is untouched here.

## DECISION LINE:
**Reject as staged; admit later, re-grounded.** Reason: it cites an own-work count file outside the lane and the registry, quotes no operator page, and its DNS thesis belongs to unheld page `archives/002855.php`. Its recheck is a tautology over cached files, and the ads-page figures no longer reproduce.
**Flip:** adopt `https://info-search.yahoo.co.jp/archives/002855.php` as a new lane row (page retained 2026-10-27, 8,703 bytes, sha256 `9ce5a4abd0087191485aa744e7a37c5b0d400ca4631b86984de11ea89fdd05e6`). Re-cut the entry on its sentences (DNS-not-IP restriction; forged-UA crawlers ignore robots.txt; the `nslookup` two-way steps), with a CJK-units quote rule. Demote the shell measurement to a single dated, tagged `[INFERENCE]` aside, with the ads figures re-measured. Drop the "headless fetch will find the names" sentence. Replace the recheck with a live `curl | grep -F` of a page string. S364 (shell) and S386 (index) need not become rows.
Not blockers: PccSearch (2-byte drift) and the SccSearch/002855/`/crawl/` byte counts reproduced exactly.

VERDICT: REJECT staged yahoo-crawler-ua-carrier-survey (S394) as staged; admit later only as a 002855-grounded entry, since none of its counts or quotes comes from a page the lane holds and its recheck cannot fail.
