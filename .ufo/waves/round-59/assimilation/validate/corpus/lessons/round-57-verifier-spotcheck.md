author: hyaku closure (non-author integrator, @m_sonnet)
round: 57 (kake lane-round 57)
date: 2026-10-26 (closure run; UTC)
subject: lane base `28fa0b23e699303725aba2727094531f5e44494d` -> tip `20217f23eca15862febe14545523832e21584106`

# Round 57 — verifier spot-check (non-author)

Driver digest (`.ufo/watchdog.log`, copied because the log is mutable):
`2026-10-25T20:34:46-03:00 launch kake round=57 pgid=465319 driver=hyaku-inline attempt=1`;
`2026-10-25T22:25:39-03:00 complete kake round=57; hyaku-inline attempt=1`.

No gate or counter of the lane was executed (PROTOCOL §Gate standard, Closure consequence): claims resting on a counter are
**evidence-verified** (committed receipts, selftest tallies, measured revision). The plain measurements below were re-measured by me.
The one lane tool I ran, `scripts/id_resolver.py` (read-only, `--revision`), is a tool and not one of the three counters.

## 1. Step-1 conformance

| Check | Command | Observed |
|---|---|---|
| Report committed by the lane identity | `git log --format='%an %H' -- .ufo/reports/round-57/kake.md` | `kake-shokunin bdfe1efd6ceecc8632508c47e8be2630e7289bd4` |
| `SHONEN` heading + one line per box | read report lines 79-84 | one `## SHONEN`, four `[ ]` lines |
| Cited hashes exist and are ancestors of `master` | `git rev-parse --verify -q <h>^{commit}` + `git merge-base --is-ancestor <h> master` for b9a5d012f7fd f7c98ff26928 cddef5b4fd36 4b8c73050470 51921b971246 32754df75774 31b61a4ddfca 20217f23eca1, and the full measured-revision hash | 8 of 8 `ok`, full hash `ancestor-full` |
| Pushed | `jj-lane.sh state kake-shokunin` | `local=remote=20217f23… ahead=0 behind=0 head=detached` |
| Leftover uncommitted work | `git status --porcelain` | one untracked file: `.ufo/waves/round-57/w1/ExecPinsIndependent.files/relabels.json` (see defect D2) |
| Prompt carries the template contract | read `.ufo/prompts/kake-round-57.md` (545 lines, §6 hyaku addendum at line 141, SHONEN rule line 118) | present |
| Every commit in the range is the lane's | `git log --format=%an 28fa0b23..20217f23` | 8 commits, all `kake-shokunin` |

Status: **ok** (real report, real commits).

## 2. Per-claim re-check

### C1 calibration — receipt relabels disclosed, this round's three receipts carry the revision they ran at (evidence-verified, plus partial re-measurement)

- Before, re-read from the committed base receipt `controls/base-c1-receipt-pins-v2.txt`:
  `undisclosed_relabels=6 … new_receipts=0 scorecard_pin=0 met=False`, three of the six relabel lines shown (`.ufo/waves/round-52/control/c1-ledger-real.txt 3a50ae4321e6 -> 1ae8de5d4dee at a4a890cf1381`).
- After, `controls/after-c1-receipt-pins.txt` at the tip: `undisclosed_relabels=0 phantom_errata=0 deleted_receipts=0 new_relabelled=0 new_unpinned=0 new_receipts=3 scorecard_pin=1 met=True`,
  `revision: 32754df7…`, `EXIT=0`. Selftest tally `controls/c1-selftest-final.txt`: `c57 receipt-pins selftest: 71/71`.
- Re-measured by me: `python3 -c` over `receipt-errata.json` → 6 entries, one per base relabel (r52 x2, r55 x2, r56 x2) with from/to hashes; `git diff 28fa0b23 20217f23 -- SCORECARD.md` is one purely
  additive hunk (+31 lines, the round-57 section; no existing line changed or deleted); `git log -- controls/after-c2-idresolver.txt controls/after-c3-quote-truth.txt` → one commit each
  (`31b61a4`), never rewritten.
- Not re-derived: the 44-receipt relabel population itself (the counter's job; I did not run it).
- Limit the lane states and I confirm: the counter certifies pin consistency, not that a counter ran. Score stays 1/10 (honest).
- Verdict: **improved** (calibration, evidence-verified); score unchanged by design.

### C2 operability — `scripts/id_resolver.py` (capability acquisition) (re-measured + evidence-verified)

- Before: `controls/base-c2-idresolver-v2.txt` → `0/5 met=False`, `G1_tool_present FAIL … scripts/id_resolver.py absent at 28fa0b23e699`; `git diff --stat 28fa0b23 20217f23` shows the file added (894 lines).
- After (evidence): `controls/after-c2-idresolver.txt` → `5/5 met=True`, `G4_red_before PASS exit=1 summary=(99, 94, 5, 5, 0)`, `G5_green PASS exit=0 summary=(106, 106, 0, 0, 0)`,
  `revision: 32754df7…`, `EXIT=0`; `controls/tool-selftest-final.txt` → `selftest: 49/49`.
- Re-measured by me: `python3 -B scripts/id_resolver.py --root . --revision 20217f23eca15862febe14545523832e21584106` → `ids_cited=106 ids_resolved=106 dangling=0 owned_elsewhere=0 unowned=0`, exit 0
  (the 106 equals the gate's `reference ids_cited=106`); `--help` shows `--root --revision --fleet --selftest`. The capability exists and runs.
- Verdict: **improved** (operability). Disclosed limits (fence-blind in a registry; drops non-ASCII knowledge paths; G4 reads live sibling registries) are real constraints, not harms for this lane's ASCII, unfenced entries.

### C3 freshness (sourced) — two Baidu dead-link entries on rows opened this round (re-measured)

- Registry rows: `git show <rev>:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → base 158, tip 160. Knowledge files `git ls-tree -r --name-only <rev> corpus/knowledge | wc -l` → 52 → 54 (the report's "coverage map 52 → 54 files" agrees).
- Base absence: `git grep -E '死链|S421|S422'` over `corpus/knowledge` at base → 0 hits for `死链`; the only `dead.link` hits are incidental (`baidu-mobile-matching-error-causes.md:20`, `publish-queue.md:128,205`).
  The report's phrase "0 knowledge files cited either page or 死链" is true as written; "dead link" in English appears in two unrelated files.
- Live re-open (2026-10-26, `curl -sL`): S421 HTTP 200, 34750 bytes; S422 HTTP 200, 27327 bytes — both equal the byte counts the lesson records for the retained bodies. `grep -c` of the recheck strings: S421 `协议死链和内容死链` → 1; S422 `能识别协议死链，以及大多数内容死链、跳转死链等低质网页` → 1 (also with the full `启用了全新的死链识别模型，…` form → 1 through `curl -fsSL --compressed`).
- Quote truth of the entries: a script extracted every `> "…"` span from both tip entries and tested raw substring against the live page (HTML or text-node): 22 of 22 (`baidu-dead-link-types.md`) and 11 of 11 (`baidu-spider3-dead-link-model.md`) found, 0 missing.
- Evidence (not run by me): `controls/after-c3-quote-truth.txt` `8/8 met=True`, `c3-selftest-final.txt` `120/120`, base `0/8`.
- Verdict: **improved** (freshness). Quote truth, not support, is what the counter certifies; support was spot-read below.

### Axis check

| Axis | Verdict | Basis |
|---|---|---|
| calibration | improved | C1 as above; no SCORECARD line changed (additive hunk only) |
| operability | improved | C2 tool runs; 106/106 cited ids resolve |
| freshness | improved | C3 as above |
| coverage | improved | two entries on ground the coverage map did not hold (README rows + frontier map 9 -> 11 per-engine entries) |
| depth, adjacency | unchanged | no claim; adjacency reported (8 of 21 lanes cite ids their own registry lacks, 41 ids) not absorbed |

No owned axis harmed. One disclosed regression, not harm: `c56_quote_truth.py` reads 6/8 at the tip by design (its mirror pins 158 rows); lane notes it in SCORECARD (see D3).
Axis ownership note: C1 was declared on calibration (the round-54 bounded sub-axis), which is outside the prompt's operability + freshness list; the lane flagged the ownership question to the operator. I grade it on its declared axis.

## 3. Discernment spot-check (LEARNING.md)

Source: `corpus/lessons/round-57.md` `## Gate`. Every re-open below was a fresh `curl -sL -A 'Mozilla/5.0'` of the page on 2026-10-26 and a `grep` of what the decision rests on.

| Item | Decision | Re-opened source | agree/disagree | Reason |
|---|---|---|---|---|
| S421 `baidu-dead-link-types` | admit | `https://ziyuan.baidu.com/college/articleinfo?id=3458` | agree | HTTP 200, 34750 B; prints `发布日期：2022-09-09`; contains `协议死链和内容死链` once; the page text contains `内容死链，服务器端返回HTTP状态码200，无法设置为404`, the sentence the row's claim rests on; all 22 quoted spans of the entry occur in the page |
| S422 `baidu-spider3-dead-link-model` | admit | `https://ziyuan.baidu.com/wiki/867` | agree | HTTP 200, 27327 B; prints `发布日期：2016-06-30` (the entry dates its claims from 2016); `大约几天内就可以处理掉了` and `协议死链是最好的选择` are on the page, matching the row's processing-time and protocol-preference claims; 11 of 11 spans found |
| S390 `baidu-render-crawl-ua` | reject as staged | `https://ziyuan.baidu.com/wiki/990` | agree | page prints `发布日期：2017-03-24` (staged "no stamp" claim is wrong); `公告正文` count 0 (locator absent); `最新UA如下` count 1 (a plain line) — every fact in the reject reason reproduces |
| S409 `baidu-render-and-crawl-agents` | reject as staged | `https://ziyuan.baidu.com/wiki/1021` | agree | page contains `…端还未全部覆盖。特提醒` (PC coverage sentence the staged text omitted), count 1 |
| S410 (same staged entry) | reject as staged | `https://ziyuan.baidu.com/wiki/963` | agree | `grep -c -E '渲染\|JavaScript\|JS'` over the body → 0; the page cannot carry the staged claim about the JS-fetching agent |
| S358 `ollama-openapi-contract` | reject, outside domain | `PROVINCE.md` lines 3, 6, 41; `kama-shokunin/corpus/SOURCES.md` | agree | line 3 domain is web properties and publishing, line 6 `Refuses: anything outside this domain`, line 41 `kama owns local model-serving endpoints`; kama rows S009-S011 already hold the Ollama docs |
| S404/S414 staged | reject as staged | not re-opened | not checked | rests on read-only shokuknow checkout paths; I did not re-count; reason is internally consistent with the lane's `test -e` claim (unprovable by me, not disagreement) |
| New `SOURCES.md` rows S421, S422 | row shape and quote | `git show 20217f23:corpus/SOURCES.md`, rows S421/S422; live pages | agree | quotes `协议死链和内容死链` (9 units) and `能识别协议死链，以及大多数内容死链、跳转死链等低质网页` (25 units) are each at most 25 words/units and at most 40 characters, both raw substrings of the live page, each once |

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → exit 0, 14 W04 duplicate-URL warnings, the same count the lane reports at round start and end (the two new rows S416/S417 are among them from earlier rounds; S421/S422 add none).

Result: 2 of 2 admits and 5 of 5 re-checked rejects agree; no disagreement to learn from, no rejection stands on an unreadable page. The lane's own correction (S390 "no stamp" wrong; 2 wrong claims in staged S403) is borne out.

## 4. Trend verdicts

- expansion: **improved** — two entries on ground the coverage map did not hold (`git ls-tree` 52 -> 54 knowledge files, base `死链` 0 hits), each citing a `mined` row (S421, S422 are `mined` in the tip registry); plus a capability (`id_resolver.py`).
- quality: **improved** — no admitted entry fails its recheck (both recheck greps print 1 live; 33 quoted spans resolve); the two entries were repaired after 21 sentence-level findings before landing. Bounded: entry fidelity beyond quote truth rests on lane reviewers, not on a counter.
- discernment: **improved** — the outside spot-check agrees with the gate on both admits and on five rejects, with the reject reasons reproduced against the pages; no disagreement left unlearned.

## 5. Routed defects (status-neutral, for the lane's next round)

- **D1 receipt rewrite stated as absent.** Report line 60 says "No receipt carrying a `revision:` line was rewritten after commit." `controls/after-c1-receipt-pins.txt` was committed at T0 (`31b61a4`) as `pending` + `revision: 32754df7…` + `EXIT=0`, and rewritten in `20217f2` (diff: `-pending`, `+` counter line and `+  tip: 31b61a4d…`). The landing table discloses it ("placeholder C1 receipt", "written after its run"), so the report self-contradicts; the exact pattern C1 was built to forbid (a pre-written receipt with a revision line and exit code, filled in later). Next round: commit receipts only after the run, or name the placeholder exception in the counter.
- **D2 uncommitted leftover.** `.ufo/waves/round-57/w1/ExecPinsIndependent.files/relabels.json` is untracked in the lane tree at the tip (a W1 seat's artifact; its siblings `relabels.out.txt`, `relabels.py` are committed). Commit it or delete it.
- **D3 regression carried as design.** `c56_quote_truth.py` is 6/8 at the tip because its mirror pins 158 rows. It is disclosed and mirrored in SCORECARD, but a gate that goes red on every later tree is a standing conformance item: pin it to its measured revision or register it as a historical gate.
- **D4 SHONEN boxes.** All four are `[ ]` and are not checkable by a non-author from this round's evidence alone; promotion remains operator-owned. Nothing written to SHONEN.md.
- **D5 carried limits** (tool fence-blind and non-ASCII path drop; C1 cannot prove a run happened; C2 G4 reads live sibling registries) stay open; the first two were found after the freeze and are named in the report.

## 6. Verdict

`admitted`: every claim verifies on its declared axis, no axis harmed; status ok. Exploratory claim: none.
