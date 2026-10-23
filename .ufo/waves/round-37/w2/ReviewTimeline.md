# ReviewTimeline — round 37 wave 2 (falsify): C1 freeze order

Attacked: "every C1 rule (predicate, counter, key, target) was fixed before any build seat existed and before any build was measured", plus the ordering claims "control receipts committed before any build" and "disposition before any build is measured". Read-only git and file reads in the lane. No sandbox writes, no network, no tool installs, no processes left running.

## Commands (all exit 0)
- `git log --format='%H %cI %aI %s' 621fb528..79d3c780` (7 commits)
- `git diff 202d625a 79d3c780 -- .ufo/waves/round-37/sealed_count.py | wc -c` printed 0 (empty). `git log -- .ufo/waves/round-37/sealed_count.py` shows one commit, 202d625. `git log -- scripts/robots_audit.py` shows one commit, 9dbc88b.
- `git show 424aa248:.ufo/waves/round-37/sealed/cases.json | sha256sum` gives 93ad9ee6…0a90, equal to `KEY_SHA256` at 202d625a:.ufo/waves/round-37/sealed_count.py:49. `git cat-file -e <rev>:…/sealed/cases.json` fails at 202d625a, 4b089da6, ccc3b2b9, 528a6d02 and 9dbc88bb. The first add is 424aa24.
- `git diff 202d625a 79d3c780 -- SCORECARD.md`: 0 removed lines, so the file is append-only. The declared predicate text is unchanged.
- Every `verification/c1-*.json` and `control-CtlC1*.json` has counterSha256 2ebb39b5…f0e3, equal to the declared digest and to the tip counter. The predicate field reads "passed >= 25 of 28 sealed cases" in all of them. `git show 9dbc88bb:scripts/robots_audit.py | sha256sum` gives 5eb767ec…cabae, equal to w1/ExecRobotsTool.md:11.

## Timeline (-03:00; commit = committer date; file times are mtimes)
| When | Event | Evidence |
|---|---|---|
| 23:57 | Counter file written (KEY_SHA256, TOOL, CASES=28, TARGET=25, PREDICATE pinned) | sealed_count.py mtime; lines 48-53 |
| 00:00:50 | Base receipt: 0/28, exit 1 | verification/c1-at-621fb528.json |
| 00:01:14 | **Declaration** 202d625a: predicate, counter, key sha pin, target | SCORECARD.md@202d625a:1754-1831 |
| 00:01:48 | Control wave dispatched (03:01:48Z) | ctl-dispatched-at.txt (committed at 4b089da6) |
| 00:07-00:21:36 | Control receipts: 0, 0, 0, 4, 20, 0 | verification/control-*.json mtimes |
| 00:21:56 | **Control receipts + C2 withdrawal** 4b089da6 | SCORECARD "control call" |
| 00:22:30 | **Wave-1 dispatch** (03:22:30Z); ExecRobotsTool told to build at 4b089da6 | w1-dispatched-at.txt; w1-spec.json (11× "at 4b089da6…") |
| 00:28:47 / 00:29:13 | Shortcut follow-up report; its receipt: **28/28, met, exit 0** | ctl/CtlC1NoReader-shortcut.md; control-CtlC1Shortcut-followup.json |
| 00:29:45 | **Shortcut follow-up + disposition** ccc3b2b9 | SCORECARD.md@ccc3b2b9:1949, 1966 |
| 00:36:51 | 528a6d02 non-claim repairs; this commit is also where w1-dispatch*, w1-spec.json and w1-dispatched-at.txt first land (authored 00:29:45) | `git show --name-status 528a6d02` |
| 00:39:23 | ExecRobotsTool report written | w1/ExecRobotsTool.md |
| 00:39:37 | **Build landed** 9dbc88bb (file unedited, sha 5eb767ec…) | robots_audit.py history |
| 00:39:44 | **First C1 measurement of a build**: 28/28, exit 0 (pre-reveal, uses the key file) | verification/c1-at-9dbc88bb.json mtime |
| 00:39:57 | **Reveal** 424aa248 (key sha equals the pin) | commit; sha256sum |
| 00:40:04 | Key-revision receipts: 0/28 at 621fb528, 202d625a, 4b089da6, ccc3b2b9, 528a6d02; 28/28 at 9dbc88bb; exit 2 at 424aa248 | c1-keyrev-at-*.json |
| 00:42:24 | Measured results 79d3c780 | SCORECARD "measured results" |

## Verdicts
1. **Holds.** Predicate, counter, key and target were fixed before any build seat existed and before any measurement.
   - All four are fixed at 202d625a (00:01:14), 21 minutes before the wave-1 build seat was dispatched (00:22:30) and 38 minutes before the first build measurement (00:39:44).
   - The counter is byte-identical through the tip (diff empty, one commit).
   - The key is fixed by its sha256 pin, and the revealed bytes match it.
   - TOOL and TARGET are constants in that unchanged file.
2. **Overstated.** The 4b089da6 heading "control call, before any build" and the declared rule "control receipts … committed before any build" (SCORECARD.md@202d625a:1884-1885) are not met in full.
   - One C1 control receipt, the shortcut follow-up, was committed at ccc3b2b9. That is 7 min 15 s after the build seat was dispatched, while the build was in progress (its report is from 00:39:23).
3. **Wrong against the rule of record.** The declaration says "A control that meets a predicate means that counter or target is wrong; it is fixed before any build" (SCORECARD.md@202d625a:1893-1894).
   - The shortcut follow-up met the predicate (28/28).
   - Neither the counter nor the target was fixed. ccc3b2b9 instead records a discretionary disposition: "this control does not skip the claimed work … C1 is kept as declared" (SCORECARD.md@ccc3b2b9:1966).
   - The ccc3b2b9 heading also narrows the declared boundary from "before any build" (declaration lines 1784, 1885 and 1894) to "before any build is measured" (ccc3b2b9:1949).
   - Rules aside, a fix "before any build" was no longer possible once the build seat was running.
4. **Does the late receipt matter?** For the measurement: **no, as far as the receipts show.**
   - The frozen rules did not move.
   - The build seat's spec pins 4b089da6 and never mentions the shortcut (`rg -c shortcut w1-spec.json`: 0 matches).
   - The build report mentions neither controls nor the shortcut, and it says "no urllib.robotparser" (w1/ExecRobotsTool.md:12).
   - The disposition is timestamped before the first build measurement.

   For process integrity: **yes.**
   - A keep-or-withdraw decision triggered by a predicate-meeting control was made by the L1 after a build seat existed.
   - The declared fallback (fix the counter or target before any build, or drop the claim, as was done for C2 at 4b089da6) was skipped.
   - Admission should weigh C1 under the ccc3b2b9 disposition, not under the literal declared rule.
5. **Overstated, minor.** The dispatch times are self-attested, and committed after the events they record.
   - w1-dispatched-at.txt landed at 528a6d02 (00:36:51), 14 min after the dispatch it records. The w1 spec's "at 4b089da6" only proves dispatch came after 00:21:56.
   - The earliest w1 artefact is w1/swarm-registry.json, mtime 00:22:18, which brackets dispatch at about 00:22.
   - "Measured before reveal" (c1-at-9dbc88bb.json) is backed only by its mtime: 00:39:44 is before the reveal commit at 00:39:57, but the receipt itself is committed inside 424aa248.
6. **Holds.** No revision before the reveal contains the key, and the counter refuses the reveal revision (exit 2 receipt).

## Residual risk / gaps
- **Not tested:** whether the L1 scored ExecRobotsTool's file privately (`--tool-file`) before 00:29:45. Only the L1's private directory (off-limits) or the transcripts could show it. A private score would turn finding 4 into a defect.
- **Not run:** the counter. That is RerunC1Sealed's item; I relied on receipt contents and hashes only.
- **Information flow, not an ordering defect:** before dispatch, the w1 context pointed seats at verification/, where the per-case control receipts already sat (in 4b089da6). Case ids name their bullets: control-CtlC1NaiveReader.json perCase shows a1-a4 passing and b1-b4 failing. That tells builders which bullets the stdlib parser fails, but not the case contents.
- **Declared control set incomplete:** the declared shortcut ("keyed on ids, URL words, user-agent names and file names", SCORECARD.md@202d625a:1887-1888) was never scored. CtlC1Shortcut died, and the follow-up is a different design (stdlib plus six rule patches).
