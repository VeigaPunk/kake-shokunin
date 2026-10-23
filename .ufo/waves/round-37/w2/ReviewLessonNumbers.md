# ReviewLessonNumbers — round 37 wave 2 (falsify), figures in `corpus/lessons/round-37.md` and SCORECARD "Round 37 — measured results"

Attacked: every number and hash in both texts at tip `79d3c780`, each checked against its committed receipt. Where I could, I re-ran the check in my sandbox clone `/fast/scratch/hyaku/kake-r37w2/ReviewLessonNumbers/clone` (checked out at `79d3c780`; clean `git status` afterwards; re-run outputs are in `../rerun/`). Installed nothing.

## Findings by severity
1. **Medium — citations to wave-1 reports do not resolve at the measured tip.** The lesson cites `w1/ScoutReopenS011.md`, `S095`, `S096` and `S097` (line 36) and leans on about 20 other wave-1 seat reports (ScoutContractVsGoogle, ReviewSealedCounter, SentinelCounterJail, MutC2Counter, ScribeMistakeMine, ReviewRoutedDisposition and others). `git ls-tree -r 79d3c780 | grep -c round-37/w1/` gives 0. Those reports first land in the later commit `a5ae0280` ("wave-1 seat reports (28 returned, 4 dead)"), which descends from the tip. At `79d3c780` they are dangling evidence. The claims I checked against `a5ae0280` hold (rows below).
2. **Low — wrong figure.** Lesson line 58 says the S097 quote "It is not an official standard backed by a standards body" is 10 words. `wc -w` gives **11**. The other three counts are correct: S011 6, S095 11, S096 5.
3. **Low — cannot be verified from repo files.** The dead-seat details have no committed receipt: "within 5 s", the quoted "Individual quota reached … Resets in 59h" and route `gemini-4-argon`. `git grep` at `a5ae0280` finds only `LOG.md:1514,1517`, which says "429 quota" and "4 critics dead on the same quota error". The 429 status and the dead-seat count hold; the timing and the quoted text do not have a receipt.
4. **Note.** The S095 "301" is not in the L1 fetch receipt, which records `url`≠`finalUrl` but no redirect status. It is confirmed only by `w1/ScoutReopenS095.md:8-10` at `a5ae0280` (`redirects=1`, `301 location: /crawling/docs/...`). `control-r36-junk.json` records neither its key revision (`fd1fb723`) nor a key file, and its `toolFile` points into the L1's private directory. My re-run with the committed copy confirms it anyway (row below).

## Hash resolution (`git cat-file -e <h>^{commit}`, run in the lane repo, read-only)
All of these give exit 0 and are ancestors of `79d3c780`: `621fb528…`, `202d625a`, `4b089da6`, `ccc3b2b9`, `528a6d02`, `9dbc88bb`, `424aa248…`, `1a16b8e3`, `4d5b3d55`, `fd1fb723`.
`bf9b2089` and its full hash give exit 128, as the lesson itself says. `git bundle list-heads .ufo/waves/round-36/retained/r36-l1-postfix-remeasure.bundle` → `bf9b20892d24… refs/heads/postfix`, so the bundle named in the lesson does contain it. **Holds.**

## Figure table
| Claim | Receipt / re-run | Verdict |
|---|---|---|
| C1 before: 0/28 at 621fb528, 202d625a, 4b089da6, ccc3b2b9, 528a6d02 | `verification/c1-keyrev-at-*.json` show passed 0, `.exit` 1. My re-run of the counting command at each revision: exit 1, passed 0 | holds |
| C1 after: 28/28 at 9dbc88bb, met | `c1-keyrev-at-9dbc88bb.json` and `c1-at-9dbc88bb.json` show 28, exit 0. My re-run: exit 0, 28, tool sha `5eb767ec` | holds |
| Measuring the reveal commit 424aa248 exits 2 | Receipt exit 2, "key visible at the measured revision". My re-run: exit 2 | holds |
| Tool sha256 `5eb767ec…cabae`, unedited | `sha256sum` of `scripts/robots_audit.py` at 9dbc88bb and at 79d3c780 both give `5eb767ec…542cabae`; 9dbc88bb touches only this file | holds |
| Key sha256 `93ad9ee6…0a90`, equal to the pin | Key at 424aa248 hashes to `93ad9ee6…0c8c0a90`, equal to `sealed_count.py:49` | holds |
| Counter and predicate unchanged since 202d625a | `sealed_count.py` is `2ebb39b5…` and `c2_mutkill.py` is `d72e232e…` at all seven commits; `git log` shows no change | holds |
| Independent implementation 28/28 | `independent-selftest-reference.json` shows 28. My re-run: exit 0, 28 | holds |
| Selftest has 131 fixtures; 131/131 on the tool | `robots-selftest-at-9dbc88bb-tool.json` shows 131/131. My re-run: exit 0, 131/131 | holds |
| Shortcut follow-up 126/131, listing the failures | Receipt shows 5 failures: b09, b10 (trim of key and value), c10 (ASCII folding), d07 (non-final `$`), d13 (`$` counted in specificity) | holds |
| Stock parser 119/131 | `robots-selftest-on-CtlC1NaiveReader.json` shows 119/131; the control uses `urllib.robotparser` (`CtlC1NaiveReader-robots_audit.py:16,213`) | holds |
| L1 reference 130/131, failing on group-name folding | Receipt fails only c10. My re-run on `sealed/reference/ref.py`: exit 1, 130/131 | holds |
| Controls: base 0, constant clean 0, junk 0, no-reader 0, all-false 4, stock parser 20, shortcut 28, reference 28 | `control-*.json`, `c1-at-621fb528.json` and `ablations/reference.json`. My re-run of every retained tool: 0, 0, 0, 0, 4, 20, 28, 28 with the matching exits | holds |
| 34 ablations scored 16–24 | 34 `ablation-*.json` files: minimum 16, maximum 24, none met. `ablation-pre.json` lists 34; all 34 committed at 202d625a | holds |
| Mutation pass: 28 of 42 meet; M40 survives | `ctl/MutRefPass.md:3` says "met 28/42"; line 50 shows M40 at 28/28 | holds |
| Shortcut is the stdlib plus six one-line patches | `ctl/CtlC1NoReader-shortcut.md:17` says "stdlib + 6 one-line patches" | holds |
| C2 27 → 32 of 32; 106 fixtures, all valid on E1 and E2 | `c2-at-621fb528.json` shows killed 27; `c2-evidence-at-528a6d02.json` shows 32, 106/106 fixtures, `failedOnE1` and `failedOnE2` both empty | holds |
| Sources accessed 02:50:49Z–02:50:51Z, all HTTP 200 | `sources/receipts.json` gives the times as 49, 49, 50, 51; status 200 for each | holds |
| Quotes match once each with `grep -cF` | 1/1/1/1 against `sources/S0xx.txt` | holds |
| Quote word counts 6 / 11 / 5 / 10 | Measured 6 / 11 / 5 / **11** | **wrong** (S097) |
| Retained source text is byte-identical to the scouts' live extraction | `ScoutReopenS0xx.md` at a5ae0280: text sha equal for all four (S011:7, S095:14, S096:9, S097:9) | holds; receipt absent at tip |
| S097 contradicts the contract on seven points | `ScoutReopenS097.md:29-35` lists 7 bullets; line 39 says "seven listed sentences" | holds; receipt absent at tip |
| Real run: 12 hosts, all 200, 03:23:15Z–03:23:31Z | `realrun/robots/receipts.json`: 12 receipts, status 200, 0 redirects, earliest 03:23:15Z, latest 03:23:31Z | holds |
| Real run: 55 checks, clean, exit 0; stdlib control the same | `audit.json` shows clean/55 and `audit.exit` 0. My re-run: exit 0, output equal to the receipt; the stdlib control is also clean/55 with exit 0 | holds |
| Wikipedia file starts with a BOM; 165-record GitHub group; empty `Disallow:` present | `en_wikipedia_org.txt` starts with `efbbbf`. The GitHub `*` group has 165 allow/disallow lines (166 lines counting its user-agent line). Empty `Disallow:` appears in the wikipedia and robotstxt files | holds (165 counts rule lines only) |
| Hardening tool sha256 `37a8a8ef…0e95` | `source_recheck.py` at 528a6d02 and at 79d3c780 hashes to `37a8a8ef…1c820e95` | holds |
| Six hardening fixtures, red on 4d5b3d55, green on the fix | My re-run: 0/6 on the 4d5b3d55 tool (exit 1), 6/6 on the fixed tool (exit 0) | holds |
| Fixed tool: round-36 selftest 106/106; round-36 sealed counter 28/28 | My re-runs: 106/106 (exit 0); `round-36/sealed_count.py --tool-file <528a6d02 tool> --key-revision fd1fb723` exit 0, 28 | holds |
| Junk check: exit 1 at 1a16b8e3, exit 0 at 4b089da6 | My re-runs: exit 1 "FAIL: no later correction…", exit 0 "PASS: … (0/28, met=false, exit=1)" | holds |
| Round-36 junk control 0/28 with key fd1fb723, exit 1 | `control-r36-junk.json` shows 0; its counter sha `88ec5914` equals `round-36/sealed_count.py`. My re-run with the retained junk file (sha `4c23062f`) and key revision fd1fb723: exit 1, 0 | holds (receipt does not record its key) |
| Round-36 lesson lines 143 and 105-109 | `round-36.md` at 621fb528: line 143 is "No do-nothing, junk, …"; lines 105-109 are "## Holds" saying the junk control has no receipt | holds |
| Criteria v2 checks each red and green | `criteria/receipts/criterion-{bare-id,control-tree-v2,polarity}.txt` each show RED exit 1 and GREEN exit 0 | holds (not re-run) |
| 2 of 13 counter mutants equivalent | `MutC2Counter.md:4` lists 13 mutants; lines 28-29 mark CM08 and CM13 equivalent | holds; receipt absent at tip |
| 4 critics and CtlC1Shortcut died on a quota error | `LOG.md:1514,1517` at a5ae0280 | holds |
| "within 5 s"; "Resets in 59h"; route gemini-4-argon | No committed receipt | unverifiable |
| Axis ratings unchanged (10 → 10) | The SCORECARD axis table shows operability 10; nothing in round 37 changes it | holds |

## Residual risk and verification gaps
- I did not re-run the criteria v2 scripts or the C2 counter; I read their receipts only.
- I did not re-check source section titles (for example "Section 2.3.1.4") against the retained text; only the quote substrings and word counts were checked.
- There is no source for the dead-seat timing; the harness transcripts (`history://`) were not read.
- All processes I started have exited; I wrote no lane files other than this report.
