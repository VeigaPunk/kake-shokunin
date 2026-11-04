# Round 58 verifier spot-check — kake

author: hyaku closure (non-author integrator, @m_opus)
date: 2026-10-26 (closed 2026-10-26 UTC)
lane tip verified: `9892ea4ab42d305adb408905a3f19f7b7109f095` = `origin/master`
report: `.ufo/reports/round-58/kake.md`; prompt: `.ufo/prompts/kake-round-58.md`

## 1. Step-1 conformance

| Item | Check | Observed |
|---|---|---|
| Report attribution | `git log --format='%an %H' -- .ufo/reports/round-58/kake.md` | `kake-shokunin 8f8c5365119de37c17dc8780c87c03a9c2506d1f "round-58: kake report"` — lane identity |
| SHONEN heading | `grep '^## SHONEN'` + one line per box | 1 heading, 4 box lines ([~],[ ],[~],[~]) |
| Cited commits exist + ancestry | `git cat-file -e` + `git merge-base --is-ancestor <h> master` for all 10 cited hashes + 3 measured/base revisions | all 13 ancestors of master |
| Push state | `scripts/hyaku/jj-lane.sh state` | `branch=master local=9892ea4a remote=9892ea4a ahead=0`; `git status --porcelain` empty; `ls-remote origin master` = `9892ea4a…` |
| Prompt fidelity | re-read `.ufo/prompts/kake-round-58.md` | full round contract verbatim (mission/axes, claims contract, L2 floor, commit-then-push, push scope, L0 channel) + five child-lane items (report path, commit-before-report, SHONEN heading, hash citation, write scope). Route map is an operator addendum; MISSION.md defers routing to host table — consistent. |
| Dispatch/complete evidence | `.ufo/watchdog.log` | `2026-10-26T20:30:12-03:00 launch kake round=58 pgid=797640 driver=hyaku-inline attempt=1`; `2026-10-26T22:00:00-03:00 complete kake round=58; hyaku-inline attempt=1` |
| Round shape | `w1-results.json`, `r1-results.json` | 68 + 8 = 76 seat results, all present; role mix matches report; within v2 band (64–128) |
| Report minimum content | re-read | all required sections present; real committed work; a real report, not a marker |

Conformance defects (status-neutral, in notes): (a) lane-declared frontier-step defect — six `present` quarantine rows (S142, S156, S161, S193–S195) hand-checked but held unappended under the frozen C3 mirror predicate; L0 question filed and committed at `43cba16`. (b) C1 works `calibration`, a round-54 sub-axis outside the prompt's operability/freshness ownership — the lane itself flags ownership as open for the operator.

## 2. Claim re-checks

### C1 — calibration (re-measured independently)

- Ledger `.ufo/waves/round-58/receipt-rewrites.json`: 19 events; for each event `git rev-parse <commit>:<path>` == `toBlob` and `git rev-parse <commit>^:<path>` == `fromBlob` — **19/19 byte-exact, 0 mismatches** (plain git, this reviewer's own run).
- Independent population derivation: `git log --first-parent --diff-filter=MDAR -M --name-status` over `.ufo/waves/` → exactly **19 non-add events** on `round-N/control(s)/` paths, same commit set as the ledger.
- Committed receipts: `controls/base-c1-receipt-rewrites-v2.txt` (`events=19 undisclosed=19 … EXIT=1`, revision `0440485`) and `controls/after-c1-receipt-rewrites.txt` (`events=19 undisclosed=0 … new_receipts=2 met=True EXIT=0`, revision `de7d96e7`) — consistent with the measured tree (after-c1 receipt itself committed at `1b009b74`, after the run; single-write honored).
- Selftest tally `controls/c1-selftest-v2.txt`: 45 PASS lines + `c58 receipt-rewrites selftest: 45/45`, exit 0 (committed evidence; gate standard — sibling gates not executed).
- Residual limits confirmed in `r1/CriticC1V2Cheat.md`: pointer-only notes and classifier-consistent fabricated values still reach met=True; disclosed honestly. Verdict: **verified → calibration improved** (score 1→2, SCORECARD diff observed).

### C2 — operability (receipt-verified + code-level spot derivation)

- Committed receipts: `base-c2-resolver-cases-v2.txt` 6/14 exit 1 at `0440485`; `after-c2-resolver-cases.txt` **14/14 exit 0** at `8d340c15`; three-seed residual 14/14 recorded in `r1/CriticC2V2Cheat.md`.
- Code diff `scripts/id_resolver.py` (+144 lines): `FENCE_OPEN_RE`/`FENCE_CLOSE_RE` CommonMark-flat fence machine in `parse_registry`, `_nul_paths` NUL-split `git ls-tree -z --name-only` revision mode — the claimed mechanism is present in committed bytes.
- Selftest receipt `c2-selftest-v2.txt`: 7 control tools incl. `base_tool` scoring 6/14 at `0440485` — the counter is not tautological; the tool's own selftest prints 59/59 via P6 receipt.
- Residual limit demonstrated: P6 trusts a printed tally (hollow selftest mutant 14/14 — disclosed); non-UTF-8 filename → loud exit 2. Verdict: **verified → operability improved**.

### C3 — freshness, sourced (re-measured)

- Registry: `grep -cE '^\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` = **162** at tip, **160** at `0440485`; `git diff` on `SOURCES.md` = pure +2-line append of S423/S424; zero touched old rows (old→new none, confirmed by diff).
- Rows: both `mined`, opened 2026-10-26, recheck `180d`, `used-by` = the two new entries; anchor cites § + 发布日期.
- Entries: `baidu-spider-identification.md` (S423), `baidu-spider-unblocking.md` (S424) open with `source:`/`verified-at:`/`recheck:` trio citing their S-ids.
- Retained bodies: `sha256sum` of `sources/S423.html`/`S424.html` = `8b8aef60…` / `3ef1275b…`, matching `sources/receipts.json` (HTTP 200, fetchedAt 2026-10-26).
- Gate receipts: `base-c3-quote-truth-v2.txt` 0/8 exit 1; `after-c3-quote-truth.txt` 8/8 exit 0 at `8d340c15`; selftest `c3-selftest-v2.txt` 120/120. Verdict: **verified → freshness improved**.

### No owned axis harmed

`git diff 0440485 9892ea4a -- SCORECARD.md`: calibration 1→2, operability/freshness rows untouched at 10; round-58 claims block appended with commands, revisions and receipts. SKILL.md gate registry gains round-58 rows; four stale-by-design counters marked `historical` at their measured revisions. `r1/ReviewerNoHarm.md` shows `c57_receipt_pins` red is the disclosed frozen-set outcome, `c57_quote_truth` red is the documented mirror-pin historical condition; `c55_readme_index`, `c57_idresolver_gate`, `c52_wave_ledger`, `c56_selftally` green. No harm observed on any owned axis.

## 3. Discernment spot-check (non-author)

| Item | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S423 `baidu-spider-identification` | admit (staged S395, renumbered by document) | live `https://ziyuan.baidu.com/college/articleinfo?id=3457` (curl, HTTP 200, this session) | **agree** | registered quote `A：有两个方式可以判断百度蜘蛛。` present verbatim (count 1); `发布日期：2022-08-19` present; outbound `href` to `id=3028` confirmed — the lane-found S424 link is real. Quote ≤25 units (13). |
| S424 `baidu-spider-unblocking` | admit (lane-found) | live `…id=3028` (curl, HTTP 200) | **agree** | quote `导致百度蜘蛛无法正常抓取` present verbatim (count 1); `发布日期：2020-07-23` present; sha256 matches committed receipt. |
| S378 `yahoo-japan-crawler-address-change-notice` | reject as staged | live `https://ads-developers.yahoo.co.jp/ja/ads-api/announcement/260514.html` (curl, HTTP 200) | **agree** | both cited page sentences reproduce verbatim (`動的ディスプレイ広告の商品リストにおいて、定期更新（FTPによる定期巡回）…` and `動的ディスプレイ広告の配信が停止します`); page sits in an ads-API developer center, names an ads product-list FTP crawler — outside this lane's publisher-side province. |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → exit 0, same 14 W04 warnings as round start (all pre-existing duplicate-URL warnings, none new).

## 4. Axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| calibration | improved | C1 re-measured independently; 19/19 events verified byte-exact |
| operability | improved | C2 receipt-verified 6/14→14/14; mechanism present in committed code |
| freshness | improved | C3 re-measured 0/8→8/8, registry 160→162 pure append, quotes re-verified live |

No exploratory claim declared; all three claims measured.

## 5. Trend verdicts

- **expansion — improved**: two admitted entries on `Crawler identity` ground the coverage map held only for Googlebot (README frontier advanced), each citing `mined` rows S423/S424 opened this round.
- **quality — improved**: every admitted quote re-verified against retained bodies and live pages; gate registry rows added; historical reds marked; new reds are disclosed by-design conditions.
- **discernment — improved**: this non-author spot-check agrees with the gate on both admits and the reject.

## 6. Routed defects the lane must fix next round

- **D1 (re-flagged, carried since round 51):** `corpus/knowledge/crawler-identity.md` lines ~31–34 "A user-agent string is the only thing a server log records about the crawler" remains unrepaired and now sits beside DNS-verification material the lane itself holds (`w1/ScoutLaneBaiduspider.md`). Qualify it (UA+IP are what a log records; verification needs reverse DNS on the IP) or mark it corrected in a new entry.
- **D2:** SentinelCounters residual limits on the round-58 counters — `c58_quote_truth.py` trusts inherited `GIT_*` (env-selectable measured repo, MEDIUM), `--base` never resolved (index read), `--revision` not pinned once; `id_resolver.py` registry/knowledge symlink escape at `--revision`. Fix (env scrub, pin resolution, `inside()` guard) or explicitly carry as contract exclusions next round.
- **D3:** frontier-step conformance defect — six `present` quarantine rows held under the frozen C3 predicate; lane-declared and awaiting the L0 ruling (`43cba16`). Next round: act on the operator's answer; not a lane fix if the ruling is "hold".
- **Carried limits (disclosed, keep on the board):** C1 pointer-only notes / fabricated values under a correct kind (needs prose-truth reviewer gate); C2 P6 hollow-tally trust (selftest must prove executed cases); `--first-parent` history boundary; non-UTF-8 filename exit 2.

## 7. SHONEN note for the operator

All four boxes read `[~]`/`[ ]` asserted-by-author; none carries a named non-author `[x]`. Boxes 1, 3, 4 look mechanically checkable by a non-author on committed bytes (SKILL decision tables + gate registry + cited sources; counter CLI contracts; PROVINCE scope notes + S378 reject); promotion remains operator-owned and nothing was written to SHONEN.md.
